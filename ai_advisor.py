"""
AI Financial Advisor — Uses Groq API to generate personalised recommendations.
"""
import os
import streamlit as st
from groq import Groq

try:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", st.secrets.get("GROQ_API_KEY", ""))
except Exception:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")


def get_ai_recommendations(profile, allocation, projections, summary):
    """Generate AI-powered financial recommendations using Groq."""
    try:
        client = Groq(api_key=GROQ_API_KEY)

        # Build context for the AI
        disposable = profile["income_monthly"] - profile["expenses_monthly"]

        goals_text = ""
        for g in profile.get("goals", []):
            monthly_needed = g["amount"] / max(g["deadline_months"], 1)
            goal_alloc = allocation.get("goals", {}).get(g["name"], 0)
            status = "on track" if goal_alloc >= monthly_needed * 0.8 else "behind schedule"
            goals_text += f"  - {g['name']}: target ₹{g['amount']:,.0f} in {g['deadline_months']} months (₹{monthly_needed:,.0f}/month needed, ₹{goal_alloc:,.0f}/month allocated — {status})\n"

        debts_text = ""
        for d in profile.get("liabilities", []):
            debts_text += f"  - {d['name']}: ₹{d['balance']:,.0f} at {d['interest_rate']*100:.1f}% interest, min payment ₹{d['min_payment']:,.0f}/month\n"

        assets_text = ""
        for a in profile.get("assets", []):
            assets_text += f"  - {a['type']}: ₹{a['amount']:,.0f} (expected return {a['return_rate']*100:.1f}%)\n"

        final_nw = projections["net_worth"][-1] if projections["net_worth"] else 0

        prompt = f"""You are a financial advisor. Give 3-4 concise, actionable recommendations based on this financial profile. Be specific with numbers. Use ₹ for currency. Keep each recommendation to 1-2 sentences.

FINANCIAL PROFILE:
- Monthly Income: ₹{profile['income_monthly']:,.0f}
- Monthly Expenses: ₹{profile['expenses_monthly']:,.0f}
- Disposable Income: ₹{disposable:,.0f}
- Risk Tolerance: {profile['risk_tolerance']}
- Planning Horizon: {profile['horizon_months']} months

ASSETS:
{assets_text if assets_text else "  None"}

DEBTS:
{debts_text if debts_text else "  None"}

EMERGENCY FUND:
- Current: ₹{profile.get('emergency_fund_current', 0):,.0f}
- Target: ₹{profile.get('emergency_fund_target', 0):,.0f}

GOALS:
{goals_text if goals_text else "  None"}

OPTIMISED ALLOCATION:
- Emergency Fund: ₹{allocation['emergency_fund']:,.0f}/month
- Debt Payment: ₹{allocation['debt_payment']:,.0f}/month
- Savings: ₹{allocation['savings']:,.0f}/month
- Investments: ₹{allocation['investments']:,.0f}/month

PROJECTED NET WORTH at month {profile['horizon_months']}: ₹{final_nw:,.0f}

Give 3-4 specific, actionable recommendations. Focus on what they should prioritise and why. Be direct, no fluff."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a concise financial advisor. Give specific, actionable advice in 3-4 points. Use ₹ for Indian Rupees. Be direct."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Fallback to basic recommendations if API fails
        return None


def get_chat_response(user_message, profile=None, allocation=None):
    """Chat with the AI about your financial plan."""
    try:
        client = Groq(api_key=GROQ_API_KEY)

        system_prompt = "You are a helpful financial advisor. Give concise, actionable advice. Use ₹ for Indian Rupees."

        context = ""
        if profile and allocation:
            disposable = profile['income_monthly'] - profile['expenses_monthly']
            context = f"""
User's financial context:
- Income: ₹{profile['income_monthly']:,.0f}/month, Expenses: ₹{profile['expenses_monthly']:,.0f}/month
- Risk: {profile['risk_tolerance']}, Horizon: {profile['horizon_months']} months
- Allocation: Emergency ₹{allocation['emergency_fund']:,.0f}, Debt ₹{allocation['debt_payment']:,.0f}, Savings ₹{allocation['savings']:,.0f}, Investments ₹{allocation['investments']:,.0f}
"""
            system_prompt += f"\n{context}"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=400,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "I'm unable to respond right now. Please try again later."
