"""
Profile — Multi-step wizard for building your financial profile.
"""
import streamlit as st
from engine import optimise_finances, project_finances, generate_summary
from ui import inject_css, AMBER, TEXT, TEXT_DIM, BG, SURFACE, SLATE

st.set_page_config(page_title="Profile — Finance Optimiser", page_icon="📋", layout="wide")
inject_css()

st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
section[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Nav
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid rgba(62,92,118,0.2); margin-bottom:24px;">
    <span style="font-family:'JetBrains Mono',monospace; font-size:1.1rem; color:{AMBER}; font-weight:700;">💰 Finance Optimiser</span>
    <div style="display:flex; gap:8px;">
        <a href="/" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Home</a>
        <a href="/Profile" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{AMBER}; text-decoration:none; padding:6px 14px; border-radius:6px; background:{SURFACE};">Profile</a>
        <a href="/Plan" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Plan</a>
        <a href="/Simulate" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Simulate</a>
        <a href="/Scenario_Lab" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Scenario Lab</a>
        <a href="/How_It_Works" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Step state
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1

step = st.session_state.wizard_step

# Step indicator
dots = ""
for i in range(1, 6):
    cls = "active" if i == step else ("done" if i < step else "")
    dots += f'<div class="step-dot {cls}"></div>'
st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)

st.markdown(f'<p style="font-family:Inter,sans-serif; color:{TEXT_DIM}; font-size:0.85rem;">Step {step} of 5</p>', unsafe_allow_html=True)

# Step 1: Income & Expenses
if step == 1:
    st.markdown("### 💵 Income & Expenses")
    income = st.number_input("Monthly Income (₹)", min_value=0, value=st.session_state.get("income", 50000), step=1000, key="income_input")
    expenses = st.number_input("Monthly Fixed Expenses (₹)", min_value=0, value=st.session_state.get("expenses", 20000), step=1000, key="expenses_input")

    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.income = income
            st.session_state.expenses = expenses
            st.session_state.wizard_step = 2
            st.rerun()

# Step 2: Assets
elif step == 2:
    st.markdown("### 🏦 Current Assets")
    num_assets = st.number_input("How many assets?", 0, 5, st.session_state.get("num_assets", 1), key="num_assets_input")
    assets = []
    for i in range(num_assets):
        col1, col2, col3 = st.columns(3)
        with col1:
            a_type = st.selectbox(f"Asset {i+1} Type", ["savings", "fd", "mutual_fund", "stocks", "other"], key=f"atype{i}")
        with col2:
            a_amount = st.number_input(f"Value (₹)", 0, 10000000, st.session_state.get(f"a_amount_{i}", 100000), key=f"aamt{i}")
        with col3:
            a_return = st.number_input(f"Annual Return (%)", 0.0, 30.0, st.session_state.get(f"a_return_{i}", 6.0), key=f"aret{i}")
        assets.append({"type": a_type, "amount": a_amount, "return_rate": a_return / 100})

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.wizard_step = 1
            st.rerun()
    with col2:
        if st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.num_assets = num_assets
            for i in range(num_assets):
                st.session_state[f"a_amount_{i}"] = st.session_state.get(f"aamt{i}", 100000)
                st.session_state[f"a_return_{i}"] = st.session_state.get(f"aret{i}", 6.0)
            st.session_state.assets = assets
            st.session_state.wizard_step = 3
            st.rerun()

# Step 3: Debts
elif step == 3:
    st.markdown("### 💳 Debts")
    num_debts = st.number_input("How many debts?", 0, 5, st.session_state.get("num_debts", 1), key="num_debts_input")
    debts = []
    for i in range(num_debts):
        col1, col2, col3 = st.columns(3)
        with col1:
            d_name = st.text_input(f"Debt {i+1} Name", value=st.session_state.get(f"d_name_{i}", f"Debt {i+1}"), key=f"dname{i}").strip()[:50]
        with col2:
            d_balance = st.number_input(f"Balance (₹)", 0, 10000000, st.session_state.get(f"d_balance_{i}", 50000), key=f"dbal{i}")
        with col3:
            d_rate = st.number_input(f"Interest Rate (%)", 0.0, 50.0, st.session_state.get(f"d_rate_{i}", 12.0), key=f"drate{i}")
        d_min = st.number_input(f"Min Monthly Payment (₹)", 0, 100000, st.session_state.get(f"d_min_{i}", 2000), key=f"dmin{i}")
        debts.append({"name": d_name, "balance": d_balance, "interest_rate": d_rate / 100, "min_payment": d_min})

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.wizard_step = 2
            st.rerun()
    with col2:
        if st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.num_debts = num_debts
            for i in range(num_debts):
                st.session_state[f"d_name_{i}"] = st.session_state.get(f"dname{i}", f"Debt {i+1}")
                st.session_state[f"d_balance_{i}"] = st.session_state.get(f"dbal{i}", 50000)
                st.session_state[f"d_rate_{i}"] = st.session_state.get(f"drate{i}", 12.0)
                st.session_state[f"d_min_{i}"] = st.session_state.get(f"dmin{i}", 2000)
            st.session_state.debts = debts
            st.session_state.wizard_step = 4
            st.rerun()

# Step 4: Goals
elif step == 4:
    st.markdown("### 🎯 Financial Goals")
    num_goals = st.number_input("How many goals?", 0, 5, st.session_state.get("num_goals", 1), key="num_goals_input")
    goals = []
    for i in range(num_goals):
        col1, col2, col3 = st.columns(3)
        with col1:
            g_name = st.text_input(f"Goal {i+1} Name", value=st.session_state.get(f"g_name_{i}", f"Goal {i+1}"), key=f"gname{i}").strip()[:50]
        with col2:
            g_amount = st.number_input(f"Target (₹)", 0, 10000000, st.session_state.get(f"g_amount_{i}", 500000), key=f"gamt{i}")
        with col3:
            g_deadline = st.number_input(f"Deadline (months)", 1, 120, st.session_state.get(f"g_deadline_{i}", 36), key=f"gdead{i}")
        goals.append({"name": g_name, "amount": g_amount, "deadline_months": g_deadline})

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.wizard_step = 3
            st.rerun()
    with col2:
        if st.button("Next →", use_container_width=True, type="primary"):
            st.session_state.num_goals = num_goals
            for i in range(num_goals):
                st.session_state[f"g_name_{i}"] = st.session_state.get(f"gname{i}", f"Goal {i+1}")
                st.session_state[f"g_amount_{i}"] = st.session_state.get(f"gamt{i}", 500000)
                st.session_state[f"g_deadline_{i}"] = st.session_state.get(f"gdead{i}", 36)
            st.session_state.goals = goals
            st.session_state.wizard_step = 5
            st.rerun()

# Step 5: Emergency Fund & Risk
elif step == 5:
    st.markdown("### 🛡️ Emergency Fund & Risk")
    ef_current = st.number_input("Current Emergency Fund (₹)", 0, 10000000, st.session_state.get("ef_current", 50000))
    expenses = st.session_state.get("expenses", 20000)
    ef_months = st.slider("Target (months of expenses)", 1, 12, st.session_state.get("ef_months", 6))
    ef_target = expenses * ef_months
    st.info(f"Target: **₹{ef_target:,.0f}** ({ef_months} months × ₹{expenses:,.0f})")

    risk = st.selectbox("Risk Tolerance", ["conservative", "moderate", "aggressive"],
                        index=["conservative", "moderate", "aggressive"].index(st.session_state.get("risk", "moderate")))
    horizon = st.slider("Planning Horizon (months)", 12, 120, st.session_state.get("horizon", 60))

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.wizard_step = 4
            st.rerun()
    with col2:
        if st.button("🚀 Generate My Plan", use_container_width=True, type="primary"):
            st.session_state.ef_current = ef_current
            st.session_state.ef_target = ef_target
            st.session_state.ef_months = ef_months
            st.session_state.risk = risk
            st.session_state.horizon = horizon

            # Build profile
            profile = {
                "income_monthly": st.session_state.get("income", 50000),
                "expenses_monthly": st.session_state.get("expenses", 20000),
                "assets": st.session_state.get("assets", [{"type": "savings", "amount": 100000, "return_rate": 0.06}]),
                "liabilities": st.session_state.get("debts", [{"name": "Debt 1", "balance": 50000, "interest_rate": 0.12, "min_payment": 2000}]),
                "goals": st.session_state.get("goals", [{"name": "Goal 1", "amount": 500000, "deadline_months": 36}]),
                "emergency_fund_current": ef_current,
                "emergency_fund_target": ef_target,
                "risk_tolerance": risk,
                "horizon_months": horizon,
            }

            # Run optimiser
            allocation, method = optimise_finances(profile, horizon)
            projections = project_finances(profile, allocation, horizon)
            summary = generate_summary(profile, allocation, projections)

            st.session_state.profile = profile
            st.session_state.allocation = allocation
            st.session_state.method = method
            st.session_state.projections = projections
            st.session_state.summary = summary

            st.switch_page("pages/2_Plan.py")
