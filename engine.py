"""
Shared optimisation engine for Personal Finance Optimiser.
Contains: LP/QP optimiser, waterfall fallback, replan, projections, recommendations.
"""

import json
import numpy as np
from scipy.optimize import minimize


def waterfall_fallback(profile):
    """Rule-based fallback if solver fails. Always produces output."""
    available = profile["income_monthly"] - profile["expenses_monthly"]
    if available <= 0:
        return {"emergency_fund": 0, "debt_payment": 0, "savings": 0, "investments": 0, "goals": {}}

    alloc = {"emergency_fund": 0, "debt_payment": 0, "savings": 0, "investments": 0, "goals": {}}
    remaining = available

    ef_gap = profile.get("emergency_fund_target", 0) - profile.get("emergency_fund_current", 0)
    if ef_gap > 0:
        ef_alloc = min(remaining * 0.3, ef_gap)
        alloc["emergency_fund"] = round(ef_alloc)
        remaining -= ef_alloc

    total_min = sum(d["min_payment"] for d in profile.get("liabilities", []))
    if total_min > 0:
        alloc["debt_payment"] = min(total_min, remaining)
        remaining -= alloc["debt_payment"]

    for d in sorted(profile.get("liabilities", []), key=lambda x: x["interest_rate"], reverse=True):
        if d["interest_rate"] > 0.10 and remaining > 0:
            extra = min(remaining * 0.2, d["balance"])
            alloc["debt_payment"] += round(extra)
            remaining -= extra

    for g in sorted(profile.get("goals", []), key=lambda x: x["deadline_months"]):
        if remaining > 0:
            needed = g["amount"] / max(g["deadline_months"], 1)
            g_alloc = min(remaining * 0.3, needed)
            alloc["goals"][g["name"]] = round(g_alloc)
            remaining -= g_alloc

    risk = profile.get("risk_tolerance", "moderate")
    if risk == "conservative":
        alloc["savings"] = round(remaining * 0.6)
        alloc["investments"] = round(remaining * 0.4)
    elif risk == "moderate":
        alloc["savings"] = round(remaining * 0.3)
        alloc["investments"] = round(remaining * 0.7)
    else:
        alloc["savings"] = round(remaining * 0.1)
        alloc["investments"] = round(remaining * 0.9)

    return alloc


def optimise_finances(profile, horizon_months=60):
    """LP/QP optimiser using scipy.optimize.minimize (SLSQP)."""
    available = profile["income_monthly"] - profile["expenses_monthly"]
    if available <= 0:
        return waterfall_fallback(profile), "fallback"

    goals = profile.get("goals", [])
    n_goals = len(goals)
    n_vars = 4 + n_goals

    x0 = np.ones(n_vars) * (available / n_vars)

    emergency_target = profile.get("emergency_fund_target", 0)
    emergency_current = profile.get("emergency_fund_current", 0)
    emergency_gap = max(0, emergency_target - emergency_current)

    liabilities = profile.get("liabilities", [])
    total_min_payment = sum(d["min_payment"] for d in liabilities)
    total_debt = sum(d["balance"] for d in liabilities)

    def objective(x):
        emer, debt, save, inv = x[0], x[1], x[2], x[3]
        goal_allocs = x[4:]
        score = 0

        emer_progress = min(emer / max(emergency_gap / 12, 1), 1.0) if emergency_gap > 0 else 1.0
        score += 0.20 * emer_progress

        if total_debt > 0:
            debt_ratio = min(debt / max(total_debt * 0.05, 1), 1.0)
            score += 0.25 * debt_ratio
        else:
            score += 0.25

        score += 0.20 * min(inv / max(available * 0.2, 1), 1.0)

        if goals:
            goal_scores = []
            for i, g in enumerate(goals):
                monthly_needed = g["amount"] / max(g["deadline_months"], 1)
                if monthly_needed > 0:
                    goal_scores.append(min(goal_allocs[i] / monthly_needed, 1.0))
                else:
                    goal_scores.append(1.0)
            score += 0.25 * np.mean(goal_scores)
        else:
            score += 0.25 * 0.5

        for i, g in enumerate(goals):
            monthly_needed = g["amount"] / max(g["deadline_months"], 1)
            if goal_allocs[i] < monthly_needed * 0.5:
                score -= 0.10

        if emergency_current < emergency_target * 0.5 and emer < available * 0.2:
            score -= 0.15

        return -score

    constraints = [
        {"type": "ineq", "fun": lambda x: available - np.sum(x)},
    ]
    if total_min_payment > 0:
        constraints.append({"type": "ineq", "fun": lambda x: x[1] - total_min_payment})

    bounds = [(0, available)] * n_vars

    try:
        result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=constraints,
                          options={"maxiter": 500, "ftol": 1e-8})
        if result.success or result.fun < 0:
            alloc = {
                "emergency_fund": round(max(0, result.x[0])),
                "debt_payment": round(max(0, result.x[1])),
                "savings": round(max(0, result.x[2])),
                "investments": round(max(0, result.x[3])),
                "goals": {}
            }
            for i, g in enumerate(goals):
                alloc["goals"][g["name"]] = round(max(0, result.x[4 + i]))
            return alloc, "optimised"
        else:
            return waterfall_fallback(profile), "fallback"
    except Exception:
        return waterfall_fallback(profile), "fallback"


def replan(current_profile, events, current_month):
    """Dynamic re-planning: apply events, re-optimise."""
    updated = json.loads(json.dumps(current_profile))

    for event in events:
        if event["month"] <= current_month:
            etype = event["type"]
            if etype == "income_change":
                updated["income_monthly"] = event["new_income"]
            elif etype == "expense_change":
                updated["expenses_monthly"] += event["amount"]
            elif etype == "rate_change":
                for d in updated.get("liabilities", []):
                    if d["name"] == event.get("target", ""):
                        d["interest_rate"] = event["new_rate"]
            elif etype == "new_goal":
                updated["goals"].append(event["goal"])
            elif etype == "emergency_expense":
                updated["emergency_fund_current"] = max(0, updated.get("emergency_fund_current", 0) - event["amount"])

    remaining_horizon = max(1, updated.get("horizon_months", 60) - current_month)
    alloc, method = optimise_finances(updated, remaining_horizon)
    return alloc, method, updated


def project_finances(profile, allocation, horizon_months):
    """Project finances over time with compound growth."""
    months = list(range(horizon_months + 1))

    net_worth = []
    debt_remaining = []
    emergency_fund = []
    savings_total = []
    investment_total = []
    goal_progress = {g["name"]: [] for g in profile.get("goals", [])}

    nw = sum(a["amount"] for a in profile.get("assets", []))
    ef = profile.get("emergency_fund_current", 0)
    total_debt = sum(d["balance"] for d in profile.get("liabilities", []))
    sv = sum(a["amount"] for a in profile.get("assets", []) if a["type"] == "savings")
    iv = sum(a["amount"] for a in profile.get("assets", []) if a["type"] != "savings")
    goal_cumulative = {g["name"]: 0 for g in profile.get("goals", [])}

    monthly_return = np.mean([a["return_rate"] / 12 for a in profile.get("assets", [])]) if profile.get("assets") else 0.04 / 12
    monthly_debt_rate = np.mean([d["interest_rate"] / 12 for d in profile.get("liabilities", [])]) if profile.get("liabilities") else 0

    debt_free_month = None

    for m in months:
        net_worth.append(round(nw))
        debt_remaining.append(round(total_debt))
        emergency_fund.append(round(ef))
        savings_total.append(round(sv))
        investment_total.append(round(iv))

        for g in profile.get("goals", []):
            goal_progress[g["name"]].append(round(goal_cumulative[g["name"]]))

        ef += allocation.get("emergency_fund", 0)
        sv += allocation.get("savings", 0)
        sv *= (1 + monthly_return * 0.5)
        iv += allocation.get("investments", 0)
        iv *= (1 + monthly_return)

        for g in profile.get("goals", []):
            goal_cumulative[g["name"]] += allocation.get("goals", {}).get(g["name"], 0)

        if total_debt > 0:
            interest = total_debt * monthly_debt_rate
            principal = max(0, allocation.get("debt_payment", 0) - interest)
            total_debt = max(0, total_debt - principal)
            if total_debt == 0 and debt_free_month is None:
                debt_free_month = m

        nw = sv + iv + ef - total_debt

    return {
        "months": months,
        "net_worth": net_worth,
        "debt_remaining": debt_remaining,
        "emergency_fund": emergency_fund,
        "savings": savings_total,
        "investments": investment_total,
        "goal_progress": goal_progress,
        "debt_free_month": debt_free_month,
    }


def generate_summary(profile, allocation, projections):
    """Generate plain-language summary."""
    lines = []
    horizon = profile.get("horizon_months", 60)

    # Highest interest debt
    liabilities = profile.get("liabilities", [])
    if liabilities:
        highest = max(liabilities, key=lambda x: x["interest_rate"])
        if highest["interest_rate"] > 0.10:
            lines.append(f"Paying off {highest['name']} ({highest['interest_rate']*100:.1f}% interest) first while maintaining minimum payments on other debts.")

    # Emergency fund
    ef_target = profile.get("emergency_fund_target", 0)
    ef_current = profile.get("emergency_fund_current", 0)
    ef_monthly = allocation.get("emergency_fund", 0)
    if ef_current < ef_target and ef_monthly > 0:
        months_to_target = max(1, round((ef_target - ef_current) / ef_monthly))
        lines.append(f"Emergency fund reaches target of ₹{ef_target:,.0f} in approximately month {months_to_target}.")

    # Goals
    goals = profile.get("goals", [])
    on_track = 0
    at_risk = 0
    for g in goals:
        monthly_needed = g["amount"] / max(g["deadline_months"], 1)
        goal_alloc = allocation.get("goals", {}).get(g["name"], 0)
        if goal_alloc >= monthly_needed * 0.8:
            on_track += 1
        else:
            at_risk += 1

    if goals:
        if at_risk == 0:
            lines.append(f"All {on_track} financial goal(s) on track.")
        else:
            lines.append(f"{on_track} goal(s) on track, {at_risk} may need adjustment.")

    # Net worth
    final_nw = projections["net_worth"][-1] if projections["net_worth"] else 0
    lines.append(f"Projected net worth at month {horizon}: ₹{final_nw:,.0f}.")

    if not lines:
        lines.append("Your financial plan is well-balanced.")

    return " ".join(lines)


def generate_recommendations(profile, allocation):
    """Generate actionable recommendations."""
    recs = []
    available = profile["income_monthly"] - profile["expenses_monthly"]

    ef_target = profile.get("emergency_fund_target", 0)
    ef_current = profile.get("emergency_fund_current", 0)
    if ef_current < ef_target:
        recs.append(f"Emergency fund is ₹{ef_target - ef_current:,.0f} short of target.")

    for d in profile.get("liabilities", []):
        if d["interest_rate"] > 0.15:
            recs.append(f"{d['name']} at {d['interest_rate']*100:.1f}% — prioritise paying this off.")

    for g in profile.get("goals", []):
        monthly_needed = g["amount"] / max(g["deadline_months"], 1)
        goal_alloc = allocation.get("goals", {}).get(g["name"], 0)
        if monthly_needed > 0 and goal_alloc < monthly_needed * 0.8:
            recs.append(f"{g['name']} needs ₹{monthly_needed:,.0f}/month but allocated ₹{goal_alloc:,.0f}.")

    if available < 0:
        recs.append("Expenses exceed income. Consider reducing spending.")

    if not recs:
        recs.append("Your plan looks well-balanced.")

    return recs


DEFAULT_PROFILE = {
    "income_monthly": 50000,
    "expenses_monthly": 20000,
    "assets": [{"type": "savings", "amount": 100000, "return_rate": 0.06}],
    "liabilities": [{"name": "Credit Card", "balance": 50000, "interest_rate": 0.12, "min_payment": 2000}],
    "goals": [{"name": "House", "amount": 500000, "deadline_months": 36}],
    "emergency_fund_current": 50000,
    "emergency_fund_target": 120000,
    "risk_tolerance": "moderate",
    "horizon_months": 60,
}
