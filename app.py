import streamlit as st
import json

# ============================================
# PERSONAL FINANCE OPTIMISER
# Recurz Hackathon — Fintech PS2
# ============================================

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Personal Finance Optimiser",
    page_icon="💰",
    layout="wide"
)

# --- TITLE ---
st.title("💰 Personal Finance Optimiser")
st.markdown("**Optimise your money across savings, investments, debt, emergency fund, and goals.**")
st.divider()

# ============================================
# SECTION 1: INPUT FORM
# ============================================
st.header("📋 Your Financial Profile")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Income & Expenses")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=1000)
    expenses = st.number_input("Monthly Fixed Expenses (₹)", min_value=0, value=20000, step=1000)

with col2:
    st.subheader("Risk & Horizon")
    risk = st.selectbox("Risk Tolerance", ["conservative", "moderate", "aggressive"])
    horizon = st.slider("Planning Horizon (months)", 12, 120, 60)

st.divider()

# --- DEBTS ---
st.subheader("💳 Debts")
num_debts = st.number_input("How many debts do you have?", 0, 5, 1)
debts = []
for i in range(num_debts):
    col1, col2, col3 = st.columns(3)
    with col1:
        d_name = st.text_input(f"Debt {i+1} Name", value=f"Debt {i+1}", key=f"dname{i}")
    with col2:
        d_balance = st.number_input(f"Balance (₹)", 0, 10000000, 50000, key=f"dbal{i}")
    with col3:
        d_rate = st.number_input(f"Interest Rate (%)", 0.0, 50.0, 12.0, key=f"drate{i}")
    d_min = st.number_input(f"Min Monthly Payment (₹)", 0, 100000, 2000, key=f"dmin{i}")
    debts.append({"name": d_name, "balance": d_balance, "interest_rate": d_rate / 100, "min_payment": d_min})

st.divider()

# --- GOALS ---
st.subheader("🎯 Financial Goals")
num_goals = st.number_input("How many goals?", 0, 5, 1)
goals = []
for i in range(num_goals):
    col1, col2, col3 = st.columns(3)
    with col1:
        g_name = st.text_input(f"Goal {i+1} Name", value=f"Goal {i+1}", key=f"gname{i}")
    with col2:
        g_amount = st.number_input(f"Target Amount (₹)", 0, 10000000, 500000, key=f"gamt{i}")
    with col3:
        g_deadline = st.number_input(f"Deadline (months)", 1, 120, 36, key=f"gdead{i}")
    goals.append({"name": g_name, "amount": g_amount, "deadline_months": g_deadline})

st.divider()

# --- EMERGENCY FUND ---
st.subheader("🛡️ Emergency Fund")
emergency_current = st.number_input("Current Emergency Fund (₹)", 0, 10000000, 50000)
emergency_months = st.slider("Target (months of expenses)", 1, 12, 6)
emergency_target = expenses * emergency_months

st.info(f"Your emergency fund target: **₹{emergency_target:,.0f}** ({emergency_months} months × ₹{expenses:,.0f})")

st.divider()

# ============================================
# SECTION 2: BUILD PROFILE & RUN OPTIMISER
# ============================================

profile = {
    "income_monthly": income,
    "expenses_monthly": expenses,
    "liabilities": debts,
    "goals": goals,
    "emergency_fund_current": emergency_current,
    "emergency_fund_target": emergency_target,
    "risk_tolerance": risk,
    "horizon_months": horizon
}

if st.button("🚀 Optimise My Finances", type="primary", use_container_width=True):
    
    # --- SIMPLE WATERFALL ALGORITHM ---
    available = income - expenses  # disposable income each month
    
    if available <= 0:
        st.error("⚠️ Your expenses equal or exceed your income. No room to optimise.")
    else:
        allocation = {
            "emergency_fund": 0,
            "debt_payment": 0,
            "savings": 0,
            "investments": 0,
            "goals": {}
        }
        
        remaining = available
        
        # STEP 1: Emergency fund (if below target)
        if emergency_current < emergency_target:
            monthly_emergency = min(remaining * 0.3, emergency_target - emergency_current)
            allocation["emergency_fund"] = round(monthly_emergency)
            remaining -= monthly_emergency
        
        # STEP 2: Minimum debt payments
        total_min_payments = sum(d["min_payment"] for d in debts)
        if total_min_payments > 0:
            allocation["debt_payment"] = min(total_min_payments, remaining)
            remaining -= allocation["debt_payment"]
        
        # STEP 3: Extra debt payment (highest interest first)
        sorted_debts = sorted(debts, key=lambda x: x["interest_rate"], reverse=True)
        for d in sorted_debts:
            if d["interest_rate"] > 0.10 and remaining > 0:  # high interest debt
                extra = min(remaining * 0.2, d["balance"])
                allocation["debt_payment"] += round(extra)
                remaining -= extra
        
        # STEP 4: Goals (nearest deadline first)
        sorted_goals = sorted(goals, key=lambda x: x["deadline_months"])
        for g in sorted_goals:
            if remaining > 0:
                monthly_needed = g["amount"] / g["deadline_months"]
                g_alloc = min(remaining * 0.3, monthly_needed)
                allocation["goals"][g["name"]] = round(g_alloc)
                remaining -= g_alloc
        
        # STEP 5: Split remaining between savings and investments
        if risk == "conservative":
            allocation["savings"] = round(remaining * 0.6)
            allocation["investments"] = round(remaining * 0.4)
        elif risk == "moderate":
            allocation["savings"] = round(remaining * 0.3)
            allocation["investments"] = round(remaining * 0.7)
        else:  # aggressive
            allocation["savings"] = round(remaining * 0.1)
            allocation["investments"] = round(remaining * 0.9)
        
        # --- DISPLAY RESULTS ---
        st.divider()
        st.header("📊 Your Optimised Allocation")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Monthly Disposable", f"₹{available:,.0f}")
        col2.metric("Emergency Fund", f"₹{allocation['emergency_fund']:,.0f}")
        col3.metric("Debt Payment", f"₹{allocation['debt_payment']:,.0f}")
        col4.metric("Investments", f"₹{allocation['investments']:,.0f}")
        
        # Pie chart
        import plotly.graph_objects as go
        
        labels = ["Emergency Fund", "Debt Payment", "Savings", "Investments"]
        values = [
            allocation["emergency_fund"],
            allocation["debt_payment"],
            allocation["savings"],
            allocation["investments"]
        ]
        
        # Add goals
        for gname, gval in allocation["goals"].items():
            labels.append(f"Goal: {gname}")
            values.append(gval)
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
        fig.update_layout(title="Monthly Allocation Breakdown")
        st.plotly_chart(fig, use_container_width=True)
        
        # --- NET WORTH PROJECTION ---
        st.divider()
        st.header("📈 Net Worth Projection")
        
        months = list(range(horizon + 1))
        net_worth = []
        debt_remaining = []
        emergency_fund = []
        
        nw = 0
        ef = emergency_current
        total_debt = sum(d["balance"] for d in debts)
        
        for m in months:
            net_worth.append(nw)
            debt_remaining.append(total_debt)
            emergency_fund.append(ef)
            
            # Monthly growth
            nw += allocation["investments"] * 1.008  # ~10% annual return
            nw += allocation["savings"]
            ef += allocation["emergency_fund"]
            
            # Debt reduction
            if total_debt > 0:
                interest = total_debt * 0.01  # average monthly interest
                principal = allocation["debt_payment"] - interest
                total_debt = max(0, total_debt - principal)
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=months, y=net_worth, name="Net Worth", line=dict(color="green")))
        fig2.add_trace(go.Scatter(x=months, y=debt_remaining, name="Debt Remaining", line=dict(color="red")))
        fig2.add_trace(go.Scatter(x=months, y=emergency_fund, name="Emergency Fund", line=dict(color="blue")))
        fig2.update_layout(title="Financial Trajectory Over Time", xaxis_title="Months", yaxis_title="Amount (₹)")
        st.plotly_chart(fig2, use_container_width=True)
        
        # --- RECOMMENDATIONS ---
        st.divider()
        st.header("💡 Recommendations")
        
        if emergency_current < emergency_target:
            st.warning(f"🛡️ Your emergency fund is **₹{emergency_target - emergency_current:,.0f} short** of the target. We've prioritised building it.")
        
        for d in debts:
            if d["interest_rate"] > 0.15:
                st.warning(f"💳 **{d['name']}** has a high interest rate of {d['interest_rate']*100:.1f}%. Prioritise paying this off.")
        
        for g in goals:
            monthly_needed = g["amount"] / g["deadline_months"]
            if monthly_needed > available * 0.3:
                st.warning(f"🎯 **{g['name']}** needs ₹{monthly_needed:,.0f}/month but we can only allocate ₹{available * 0.3:,.0f}. Deadline may be tight.")
        
        st.success("✅ Allocation optimised for long-term financial well-being, not just wealth maximisation.")
        
        # --- STORE FOR DYNAMIC REASSESSMENT ---
        st.session_state["profile"] = profile
        st.session_state["allocation"] = allocation

# ============================================
# SECTION 3: DYNAMIC REASSESSMENT
# ============================================
st.divider()
st.header("🔄 Dynamic Reassessment")
st.markdown("Simulate a life event and see how your plan adapts.")

event_type = st.selectbox("What changed?", [
    "income_change",
    "new_expense",
    "rate_change",
    "new_goal"
])

if event_type == "income_change":
    new_income = st.number_input("New Monthly Income (₹)", 0, 10000000, int(income * 0.75))
    if st.button("Inject This Change"):
        st.session_state["profile"]["income_monthly"] = new_income
        st.warning(f"⚡ Income changed to ₹{new_income:,.0f}. Hit 'Optimise My Finances' again to see the new plan.")

elif event_type == "new_expense":
    new_expense = st.number_input("New Monthly Expense (₹)", 0, 100000, 5000)
    reason = st.text_input("Reason", value="Medical")
    if st.button("Inject This Change"):
        st.session_state["profile"]["expenses_monthly"] += new_expense
        st.warning(f"⚡ Added ₹{new_expense:,.0f}/month expense ({reason}). Hit 'Optimise' to see the impact.")

elif event_type == "rate_change":
    new_rate = st.number_input("New Interest Rate (%)", 0.0, 50.0, 18.0)
    if st.button("Inject This Change"):
        st.warning(f"⚡ Interest rate changed. Hit 'Optimise' to see the impact.")

elif event_type == "new_goal":
    g_name = st.text_input("Goal Name", value="Wedding")
    g_amount = st.number_input("Amount (₹)", 0, 10000000, 300000)
    g_deadline = st.number_input("Deadline (months)", 1, 120, 12)
    if st.button("Inject This Change"):
        st.session_state["profile"]["goals"].append({
            "name": g_name, "amount": g_amount, "deadline_months": g_deadline
        })
        st.warning(f"⚡ New goal added: {g_name}. Hit 'Optimise' to see the impact.")
