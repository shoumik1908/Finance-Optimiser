"""
Profile Wizard — 5-step financial profile builder (Violet/Navy design)
"""
import streamlit as st
from engine import optimise_finances, project_finances, generate_summary, PRESET_PROFILES
from ui import (inject_css, top_nav, wizard_stepper, section_header, page_footer,
                PURPLE, PURPLE_BG, PURPLE_SOFT, TEXT, TEXT_SEC, TEXT_MUTED,
                CARD, BG, BORDER_LIGHT, GREEN, AMBER, RED, TEAL, SHADOW_SM, SHADOW_MD)

st.set_page_config(page_title="Profile Wizard — Finance Optimiser", page_icon="📋", layout="wide")
inject_css()

# ── Deferred redirect (before any rendering) ────────────────────────────
if st.session_state.pop("_profile_submit", False):
    profile = st.session_state.pop("_pending_profile", None)
    if profile:
        with st.spinner("⚡ Optimising your financial plan..."):
            alloc, method = optimise_finances(profile, profile["horizon_months"])
            proj          = project_finances(profile, alloc, profile["horizon_months"])
            summ          = generate_summary(profile, alloc, proj)
        st.session_state.update({
            "profile": profile, "allocation": alloc,
            "method": method, "projections": proj, "summary": summ
        })
        st.session_state.pop("ai_recommendations", None)
        st.session_state.pop("chat_history", None)
        st.switch_page("pages/2_Plan.py")

top_nav("Profile")

# ── State ────────────────────────────────────────────────────────────
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1
step = st.session_state.wizard_step

# ── Page Header ──────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg, #14141F 0%, #1E1E3A 100%);
            padding:40px 48px 48px; position:relative; overflow:hidden;">
    <div style="position:absolute; width:400px; height:400px; top:-150px; right:-80px;
                border-radius:50%; background:radial-gradient(circle, rgba(108,76,224,0.2) 0%, transparent 70%);
                pointer-events:none;"></div>
    <div style="position:relative; z-index:1;">
        <span style="font-size:0.72rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
                     color:rgba(196,181,253,0.8);">Step {step} of 5</span>
        <h1 style="font-size:2rem; font-weight:800; color:#FFFFFF !important; margin:6px 0 6px;
                   line-height:1.2; letter-spacing:-0.02em;">Your Financial Profile</h1>
        <p style="font-size:0.95rem; color:rgba(255,255,255,0.55) !important; margin:0; max-width:480px;">
            Fill in each section carefully — the optimiser uses every field to generate a personalised, mathematically optimal allocation.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stepper ───────────────────────────────────────────────────────────
st.markdown("<div style='padding:0 48px;'>", unsafe_allow_html=True)
wizard_stepper(step, [
    ("💵", "Cashflow"),
    ("🏦", "Assets"),
    ("💳", "Debts"),
    ("🎯", "Goals"),
    ("🛡️", "Safety"),
])
st.markdown("</div>", unsafe_allow_html=True)

# ── Quick-fill Presets ────────────────────────────────────────────────
with st.expander("⚡ Quick-fill from an archetype (recommended for demos)"):
    st.markdown(f'<p style="font-size:0.85rem; color:{TEXT_MUTED}; margin:0 0 14px;">Select a curated profile to pre-populate all five steps with realistic numbers:</p>', unsafe_allow_html=True)
    qc1, qc2, qc3 = st.columns(3)

    def _apply_preset(key: str):
        p = PRESET_PROFILES[key]
        st.session_state.income    = p["income_monthly"]
        st.session_state.expenses  = p["expenses_monthly"]
        st.session_state.assets    = p["assets"]
        st.session_state.num_assets = len(p["assets"])
        st.session_state.debts     = p["liabilities"]
        st.session_state.num_debts = len(p["liabilities"])
        st.session_state.goals     = p["goals"]
        st.session_state.num_goals = len(p["goals"])
        st.session_state.ef_current = p["emergency_fund_current"]
        st.session_state.ef_months  = max(1, round(p["emergency_fund_target"] / max(p["expenses_monthly"], 1)))
        st.session_state.risk      = p["risk_tolerance"]
        st.session_state.horizon   = p["horizon_months"]
        st.rerun()

    if qc1.button("🚀 Young Professional", use_container_width=True):
        _apply_preset("young_pro")
    if qc2.button("🏡 Mid-Career Family", use_container_width=True):
        _apply_preset("family_builder")
    if qc3.button("🔥 FIRE Seeker", use_container_width=True):
        _apply_preset("fire_seeker")

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ── STEP 1: CASHFLOW ─────────────────────────────────────────────────
if step == 1:
    st.markdown(f"""
    <div style="padding:0 48px;">
        <span class="pf-section-label">Step 1</span>
        <h2 class="pf-section-title">💵 Monthly Income & Expenses</h2>
        <p class="pf-section-sub">Enter your predictable monthly take-home income and fixed living costs.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2, gap="large")
        with col1:
            income = st.number_input("Monthly Take-Home Income (₹)",
                                     min_value=0, value=st.session_state.get("income", 75000),
                                     step=1000, format="%d", key="s1_income")
        with col2:
            expenses = st.number_input("Monthly Fixed Expenses (₹)",
                                       min_value=0, value=st.session_state.get("expenses", 28000),
                                       step=1000, format="%d", key="s1_expenses")

    disposable   = max(0, income - expenses)
    savings_rate = (disposable / max(income, 1)) * 100

    st.markdown(f"""
    <div style="display:flex; gap:16px; flex-wrap:wrap; margin:20px 0;">
        <div style="flex:1; min-width:180px; background:{CARD}; border:1px solid {BORDER_LIGHT};
                    border-radius:14px; padding:18px 22px; box-shadow:{SHADOW_SM};">
            <p style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em;
                      color:{TEXT_MUTED} !important; margin:0 0 4px;">Monthly Disposable Surplus</p>
            <p style="font-family:'JetBrains Mono',monospace; font-size:1.6rem; font-weight:700;
                      color:{PURPLE} !important; margin:0;">₹{disposable:,.0f}</p>
        </div>
        <div style="flex:1; min-width:180px; background:{CARD}; border:1px solid {BORDER_LIGHT};
                    border-radius:14px; padding:18px 22px; box-shadow:{SHADOW_SM};">
            <p style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em;
                      color:{TEXT_MUTED} !important; margin:0 0 4px;">Potential Savings Rate</p>
            <p style="font-family:'JetBrains Mono',monospace; font-size:1.6rem; font-weight:700;
                      color:{GREEN if savings_rate >= 20 else AMBER} !important; margin:0;">{savings_rate:.1f}%</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, nav_col = st.columns([1, 1])
    with nav_col:
        if st.button("Next: Assets →", use_container_width=True, type="primary"):
            st.session_state.income = income
            st.session_state.expenses = expenses
            st.session_state.wizard_step = 2
            st.rerun()


# ── STEP 2: ASSETS ───────────────────────────────────────────────────
elif step == 2:
    st.markdown(f"""
    <div style="padding:0 48px;">
        <span class="pf-section-label">Step 2</span>
        <h2 class="pf-section-title">🏦 Current Assets & Investments</h2>
        <p class="pf-section-sub">List your savings accounts, FDs, mutual funds, equities, and other assets.</p>
    </div>
    """, unsafe_allow_html=True)

    num_assets = st.number_input("Number of asset accounts:", 0, 8,
                                 st.session_state.get("num_assets", 2), key="s2_num")
    assets = []
    existing = st.session_state.get("assets", [])

    for i in range(num_assets):
        st.markdown(f'<div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:14px; padding:18px 20px; margin-bottom:12px; box-shadow:{SHADOW_SM};">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.2, 1.4, 1])
        type_opts   = ["savings", "fd", "mutual_fund", "stocks", "other"]
        def_type    = existing[i]["type"] if i < len(existing) else "mutual_fund"
        def_amt     = int(existing[i]["amount"])       if i < len(existing) else 100000
        def_ret     = float(existing[i]["return_rate"] * 100) if i < len(existing) else 10.0

        with c1:
            a_type = st.selectbox(f"Type #{i+1}", type_opts,
                                  index=type_opts.index(def_type) if def_type in type_opts else 0,
                                  key=f"a_type_{i}")
        with c2:
            a_amt  = st.number_input(f"Current Value #{i+1} (₹)", 0, 100_000_000, def_amt, step=10000, key=f"a_amt_{i}")
        with c3:
            a_ret  = st.number_input(f"Annual Return #{i+1} (%)", 0.0, 40.0, def_ret, step=0.5, key=f"a_ret_{i}")
        st.markdown("</div>", unsafe_allow_html=True)
        assets.append({"type": a_type, "amount": a_amt, "return_rate": a_ret / 100})

    total_portfolio = sum(a["amount"] for a in assets)
    st.markdown(f"""
    <div style="background:{PURPLE_SOFT}; border:1px solid rgba(108,76,224,0.18); border-radius:12px;
                padding:14px 20px; margin:16px 0; display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:0.88rem; font-weight:600; color:{TEXT_SEC} !important;">Total Portfolio Value</span>
        <span style="font-family:'JetBrains Mono',monospace; font-size:1.2rem; font-weight:700;
                     color:{PURPLE} !important;">₹{total_portfolio:,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

    nav1, nav2 = st.columns(2, gap="medium")
    with nav1:
        if st.button("← Back", use_container_width=True):
            st.session_state.wizard_step = 1; st.rerun()
    with nav2:
        if st.button("Next: Debts →", use_container_width=True, type="primary"):
            st.session_state.num_assets = num_assets
            st.session_state.assets     = assets
            st.session_state.wizard_step = 3; st.rerun()


# ── STEP 3: DEBTS ────────────────────────────────────────────────────
elif step == 3:
    st.markdown(f"""
    <div style="padding:0 48px;">
        <span class="pf-section-label">Step 3</span>
        <h2 class="pf-section-title">💳 Debts & Liabilities</h2>
        <p class="pf-section-sub">Enter all active loans and credit obligations. The solver applies avalanche prioritisation automatically.</p>
    </div>
    """, unsafe_allow_html=True)

    num_debts = st.number_input("Number of active debts:", 0, 6,
                                st.session_state.get("num_debts", 1), key="s3_num")
    debts     = []
    exd       = st.session_state.get("debts", [])

    for i in range(num_debts):
        st.markdown(f'<div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:14px; padding:18px 20px; margin-bottom:12px; box-shadow:{SHADOW_SM};">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([1.4, 1.2, 1, 1])
        def_name = exd[i]["name"]              if i < len(exd) else f"Loan {i+1}"
        def_bal  = int(exd[i]["balance"])      if i < len(exd) else 50000
        def_rate = float(exd[i]["interest_rate"] * 100) if i < len(exd) else 12.0
        def_min  = int(exd[i]["min_payment"]) if i < len(exd) else 2000

        with c1:
            d_name = st.text_input(f"Debt Name #{i+1}", value=def_name, key=f"d_name_{i}").strip()[:50]
        with c2:
            d_bal  = st.number_input(f"Balance #{i+1} (₹)", 0, 100_000_000, def_bal, step=5000, key=f"d_bal_{i}")
        with c3:
            d_rate = st.number_input(f"APR #{i+1} (%)", 0.0, 60.0, def_rate, step=0.5, key=f"d_rate_{i}")
        with c4:
            d_min  = st.number_input(f"Min EMI #{i+1} (₹)", 0, 1_000_000, def_min, step=500, key=f"d_min_{i}")
        st.markdown("</div>", unsafe_allow_html=True)
        debts.append({"name": d_name, "balance": d_bal, "interest_rate": d_rate / 100, "min_payment": d_min})

    total_debt = sum(d["balance"]     for d in debts)
    total_min  = sum(d["min_payment"] for d in debts)
    st.markdown(f"""
    <div style="display:flex; gap:16px; flex-wrap:wrap; margin:12px 0 20px;">
        <div style="flex:1; min-width:160px; background:{CARD}; border:1px solid {BORDER_LIGHT};
                    border-radius:12px; padding:14px 18px; box-shadow:{SHADOW_SM};">
            <p style="font-size:0.7rem; text-transform:uppercase; letter-spacing:0.07em;
                      font-weight:700; color:{TEXT_MUTED} !important; margin:0 0 3px;">Total Debt</p>
            <p style="font-family:'JetBrains Mono',monospace; font-size:1.3rem; font-weight:700;
                      color:{RED} !important; margin:0;">₹{total_debt:,.0f}</p>
        </div>
        <div style="flex:1; min-width:160px; background:{CARD}; border:1px solid {BORDER_LIGHT};
                    border-radius:12px; padding:14px 18px; box-shadow:{SHADOW_SM};">
            <p style="font-size:0.7rem; text-transform:uppercase; letter-spacing:0.07em;
                      font-weight:700; color:{TEXT_MUTED} !important; margin:0 0 3px;">Total Monthly Minimums</p>
            <p style="font-family:'JetBrains Mono',monospace; font-size:1.3rem; font-weight:700;
                      color:{AMBER} !important; margin:0;">₹{total_min:,.0f}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav1, nav2 = st.columns(2, gap="medium")
    with nav1:
        if st.button("← Back", use_container_width=True):
            st.session_state.wizard_step = 2; st.rerun()
    with nav2:
        if st.button("Next: Goals →", use_container_width=True, type="primary"):
            st.session_state.num_debts = num_debts
            st.session_state.debts     = debts
            st.session_state.wizard_step = 4; st.rerun()


# ── STEP 4: GOALS ────────────────────────────────────────────────────
elif step == 4:
    st.markdown(f"""
    <div style="padding:0 48px;">
        <span class="pf-section-label">Step 4</span>
        <h2 class="pf-section-title">🎯 Financial Goals</h2>
        <p class="pf-section-sub">Define your specific milestones — house downpayment, education fund, international trip — with target amounts and deadlines.</p>
    </div>
    """, unsafe_allow_html=True)

    num_goals = st.number_input("Number of financial goals:", 0, 6,
                                st.session_state.get("num_goals", 1), key="s4_num")
    goals     = []
    exg       = st.session_state.get("goals", [])

    for i in range(num_goals):
        st.markdown(f'<div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:14px; padding:18px 20px; margin-bottom:12px; box-shadow:{SHADOW_SM};">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.6, 1.2, 1])
        def_name = exg[i]["name"]             if i < len(exg) else f"Goal {i+1}"
        def_amt  = int(exg[i]["amount"])      if i < len(exg) else 500000
        def_dead = int(exg[i]["deadline_months"]) if i < len(exg) else 36

        with c1:
            g_name = st.text_input(f"Goal #{i+1} Name", value=def_name, key=f"g_name_{i}").strip()[:50]
        with c2:
            g_amt  = st.number_input(f"Target Corpus #{i+1} (₹)", 0, 100_000_000, def_amt, step=50000, key=f"g_amt_{i}")
        with c3:
            g_dead = st.number_input(f"Deadline #{i+1} (months)", 1, 120, def_dead, step=6, key=f"g_dead_{i}")
        monthly = g_amt / max(g_dead, 1)
        st.markdown(f'<p style="font-size:0.78rem; color:{TEXT_MUTED}; margin:4px 0 0;">Monthly run-rate needed: <b style="font-family:\'JetBrains Mono\',monospace; color:{PURPLE};">₹{monthly:,.0f}</b></p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        goals.append({"name": g_name, "amount": g_amt, "deadline_months": g_dead})

    nav1, nav2 = st.columns(2, gap="medium")
    with nav1:
        if st.button("← Back", use_container_width=True):
            st.session_state.wizard_step = 3; st.rerun()
    with nav2:
        if st.button("Next: Safety & Risk →", use_container_width=True, type="primary"):
            st.session_state.num_goals = num_goals
            st.session_state.goals     = goals
            st.session_state.wizard_step = 5; st.rerun()


# ── STEP 5: SAFETY NET & RISK ─────────────────────────────────────────
elif step == 5:
    st.markdown(f"""
    <div style="padding:0 48px;">
        <span class="pf-section-label">Step 5 — Final Step</span>
        <h2 class="pf-section-title">🛡️ Emergency Safety Net & Risk Tolerance</h2>
        <p class="pf-section-sub">Set your liquid reserve target and investment risk profile. These directly influence the capital allocation weights.</p>
    </div>
    """, unsafe_allow_html=True)

    expenses = st.session_state.get("expenses", 28000)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        ef_current = st.number_input("Current Liquid Emergency Fund (₹)", 0, 50_000_000,
                                     st.session_state.get("ef_current", 60000), step=5000)
        ef_months  = st.slider("Reserve Target (months of expenses)", 1, 12,
                               st.session_state.get("ef_months", 6))
    with col2:
        risk    = st.selectbox("Investment Risk Tolerance",
                               ["conservative", "moderate", "aggressive"],
                               index=["conservative", "moderate", "aggressive"].index(
                                   st.session_state.get("risk", "moderate")),
                               help="Conservative: 60/40 savings/investments. Moderate: 30/70. Aggressive: 10/90.")
        horizon = st.slider("Planning Horizon (months)", 12, 120,
                            st.session_state.get("horizon", 60), step=6)

    ef_target = expenses * ef_months
    ef_gap    = max(0, ef_target - ef_current)

    st.markdown(f"""
    <div style="display:flex; gap:16px; flex-wrap:wrap; margin:16px 0 24px;">
        <div style="flex:1; min-width:160px; background:{CARD}; border:1px solid {BORDER_LIGHT};
                    border-radius:12px; padding:14px 18px; box-shadow:{SHADOW_SM};">
            <p style="font-size:0.7rem; text-transform:uppercase; letter-spacing:0.07em;
                      font-weight:700; color:{TEXT_MUTED} !important; margin:0 0 3px;">Reserve Target</p>
            <p style="font-family:'JetBrains Mono',monospace; font-size:1.3rem; font-weight:700;
                      color:{PURPLE} !important; margin:0;">₹{ef_target:,.0f}</p>
            <p style="font-size:0.72rem; color:{TEXT_MUTED}; margin:3px 0 0;">{ef_months} × ₹{expenses:,.0f}</p>
        </div>
        <div style="flex:1; min-width:160px; background:{CARD}; border:1px solid {BORDER_LIGHT};
                    border-radius:12px; padding:14px 18px; box-shadow:{SHADOW_SM};">
            <p style="font-size:0.7rem; text-transform:uppercase; letter-spacing:0.07em;
                      font-weight:700; color:{TEXT_MUTED} !important; margin:0 0 3px;">Reserve Gap</p>
            <p style="font-family:'JetBrains Mono',monospace; font-size:1.3rem; font-weight:700;
                      color:{"#10B981" if ef_gap == 0 else RED} !important; margin:0;">
                {"Fully Funded ✓" if ef_gap == 0 else f"₹{ef_gap:,.0f} needed"}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav1, nav2 = st.columns(2, gap="medium")
    with nav1:
        if st.button("← Back", use_container_width=True, key="s5_back"):
            st.session_state.wizard_step = 4
            st.rerun()
    with nav2:
        if st.button("⚡ Generate My Optimised Plan →", use_container_width=True,
                     type="primary", key="s5_generate"):
            # Save wizard data, stash profile, set redirect flag, rerun
            st.session_state.ef_current = ef_current
            st.session_state.ef_target  = ef_target
            st.session_state.ef_months  = ef_months
            st.session_state.risk       = risk
            st.session_state.horizon    = horizon
            st.session_state["_pending_profile"] = {
                "income_monthly":         st.session_state.get("income",   75000),
                "expenses_monthly":       st.session_state.get("expenses", 28000),
                "assets":                 st.session_state.get("assets",   [{"type":"savings","amount":80000,"return_rate":0.045}]),
                "liabilities":            st.session_state.get("debts",    []),
                "goals":                  st.session_state.get("goals",    []),
                "emergency_fund_current": ef_current,
                "emergency_fund_target":  ef_target,
                "risk_tolerance":         risk,
                "horizon_months":         horizon,
            }
            st.session_state["_profile_submit"] = True
            st.rerun()

page_footer()
