"""
Simulate — Life-event simulation studio (Violet/Navy design)
"""
import streamlit as st
import plotly.graph_objects as go
from engine import optimise_finances, project_finances, generate_summary, replan, PRESET_PROFILES
from ui import (inject_css, top_nav, page_footer, allocation_stacked_bar, summary_block,
                PURPLE, PURPLE_BG, PURPLE_SOFT, TEXT, TEXT_SEC, TEXT_MUTED,
                CARD, BG, BORDER_LIGHT, GREEN, AMBER, RED, TEAL, SHADOW_SM, SHADOW_MD, GRAD)

st.set_page_config(page_title="Simulation Studio — Finance Optimiser", page_icon="🔄", layout="wide")
inject_css()

# ── Deferred redirects (before any rendering) ─────────────────────────
if st.session_state.pop("_sim_go_profile", False):
    st.switch_page("pages/1_Profile.py")

if st.session_state.pop("_sim_demo", False):
    p = PRESET_PROFILES["young_pro"]
    with st.spinner("Loading demo..."):
        a, m = optimise_finances(p, p["horizon_months"])
        j    = project_finances(p, a, p["horizon_months"])
        s    = generate_summary(p, a, j)
    st.session_state.update({"profile": p, "allocation": a, "method": m, "projections": j, "summary": s})
    st.rerun()

top_nav("Simulate")

# ── Empty State ────────────────────────────────────────────────────────
if "profile" not in st.session_state:
    st.markdown(f"""
    <div style="min-height:80vh; display:flex; align-items:center; justify-content:center;
                flex-direction:column; text-align:center; padding:48px;">
        <div style="width:80px; height:80px; border-radius:20px; background:rgba(6,182,212,0.1);
                    display:flex; align-items:center; justify-content:center;
                    font-size:2.4rem; margin-bottom:20px;">🔄</div>
        <h2 style="color:{TEXT} !important; font-size:1.8rem; margin:0 0 10px;">No Profile Loaded</h2>
        <p style="color:{TEXT_MUTED} !important; font-size:0.95rem; max-width:400px; margin:0 0 28px; line-height:1.6;">
            Build your profile or load a preset archetype to run life-event simulations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("✨ Build Profile →", use_container_width=True, type="primary", key="sim_go_profile"):
            st.session_state["_sim_go_profile"] = True
            st.rerun()
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Load Young Professional Demo", use_container_width=True, key="sim_demo"):
            st.session_state["_sim_demo"] = True
            st.rerun()
    st.stop()

profile    = st.session_state.profile
orig_alloc = st.session_state.allocation
orig_proj  = st.session_state.projections
horizon    = profile.get("horizon_months", 60)

# ── Page Header ────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg, #14141F 0%, #1E1E3A 100%);
            padding:36px 48px 40px; position:relative; overflow:hidden;">
    <div style="position:absolute; width:350px; height:350px; top:-120px; right:-60px;
                border-radius:50%; background:radial-gradient(circle, rgba(6,182,212,0.2) 0%, transparent 70%);
                pointer-events:none;"></div>
    <div style="position:relative; z-index:1;">
        <span style="font-size:0.72rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
                     color:rgba(103,232,249,0.8);">Dynamic Re-Optimisation</span>
        <h1 style="font-size:2rem; font-weight:800; color:#FFFFFF !important; margin:6px 0 6px;">
            Life-Event Simulation Studio
        </h1>
        <p style="font-size:0.9rem; color:rgba(255,255,255,0.5) !important; margin:0; max-width:540px;">
            Inject income changes, new expenses, rate shocks, or emergency events. The SLSQP engine globally re-optimises from the event month forward.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

# ── Event Config Card ──────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:16px;
            padding:28px 28px 20px; box-shadow:{SHADOW_SM}; margin-bottom:24px;">
    <p style="font-size:1rem; font-weight:700; color:{TEXT} !important; margin:0 0 18px;">⚡ Configure Life Event</p>
""", unsafe_allow_html=True)

col_type, col_params = st.columns([1, 2.2], gap="large")
with col_type:
    event_type = st.selectbox("Event Type", [
        "income_change", "expense_change", "rate_change", "new_goal", "emergency_expense"
    ], format_func=lambda x: {
        "income_change":    "💰 Income Change",
        "expense_change":   "📉 New Expense",
        "rate_change":      "📈 Rate Shock",
        "new_goal":         "🎯 New Goal",
        "emergency_expense":"🚨 Emergency Expense",
    }[x])

events = []
with col_params:
    if event_type == "income_change":
        c1, c2 = st.columns(2)
        new_income   = c1.number_input("New Monthly Income (₹)", 0, 50_000_000,
                                       int(profile["income_monthly"] * 0.8), step=5000)
        event_month  = c2.slider("When? (Month)", 1, horizon, min(12, horizon))
        events.append({"month": event_month, "type": "income_change", "new_income": new_income})
        delta_pct = (new_income - profile["income_monthly"]) / max(profile["income_monthly"], 1) * 100
        color = GREEN if delta_pct >= 0 else RED
        st.markdown(f'<p style="font-size:0.82rem; font-weight:600; color:{color};">'
                    f'{"▲" if delta_pct>=0 else "▼"} {abs(delta_pct):.1f}% vs current income</p>',
                    unsafe_allow_html=True)

    elif event_type == "expense_change":
        c1, c2 = st.columns(2)
        new_exp  = c1.number_input("Additional Monthly Expense (₹)", 0, 1_000_000, 8000, step=1000)
        event_month = c2.slider("When? (Month)", 1, horizon, min(12, horizon))
        events.append({"month": event_month, "type": "expense_change", "amount": new_exp})

    elif event_type == "rate_change":
        debt_names = [d["name"] for d in profile.get("liabilities", [])]
        c1, c2, c3 = st.columns(3)
        target = c1.selectbox("Target Loan", debt_names) if debt_names else "—"
        new_rate    = c2.number_input("New APR (%)", 0.0, 60.0, 16.0, step=0.5)
        event_month = c3.slider("When? (Month)", 1, horizon, min(12, horizon))
        if not debt_names:
            st.markdown(f'<div class="pf-warn-box">⚠ No debts in your profile to apply a rate change.</div>', unsafe_allow_html=True)
        events.append({"month": event_month, "type": "rate_change", "target": target, "new_rate": new_rate / 100})

    elif event_type == "new_goal":
        c1, c2, c3, c4 = st.columns(4)
        g_name      = c1.text_input("Goal Name", "Wedding Fund").strip()[:50]
        g_amount    = c2.number_input("Target (₹)", 0, 50_000_000, 300000, step=25000)
        g_deadline  = c3.number_input("Deadline (months)", 1, horizon, 18, step=6)
        event_month = c4.slider("When? (Month)", 1, horizon, min(6, horizon))
        events.append({"month": event_month, "type": "new_goal",
                       "goal": {"name": g_name, "amount": g_amount, "deadline_months": g_deadline}})

    elif event_type == "emergency_expense":
        c1, c2 = st.columns(2)
        amount      = c1.number_input("Shock Amount (₹)", 0, 10_000_000, 50000, step=10000)
        event_month = c2.slider("When? (Month)", 1, horizon, min(6, horizon))
        events.append({"month": event_month, "type": "emergency_expense", "amount": amount})

st.markdown("</div>", unsafe_allow_html=True)

run = st.button("🔄 Run Simulation & Re-Optimise →", type="primary", use_container_width=True)

if run:
    event_month = events[0]["month"]
    new_alloc, new_method, updated_profile = replan(profile, events, event_month)
    new_proj   = project_finances(updated_profile, new_alloc, horizon - event_month)
    new_summary = generate_summary(updated_profile, new_alloc, new_proj)
    st.session_state.sim_result = {
        "new_alloc": new_alloc, "new_method": new_method,
        "new_proj": new_proj, "new_summary": new_summary, "event_month": event_month
    }

# ── Results ────────────────────────────────────────────────────────────
if "sim_result" not in st.session_state:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px dashed {BORDER_LIGHT}; border-radius:16px;
                padding:48px; text-align:center; margin-top:8px;">
        <span style="font-size:2.5rem; display:block; margin-bottom:12px; opacity:0.4;">⏳</span>
        <p style="font-size:1rem; font-weight:600; color:{TEXT_MUTED} !important; margin:0;">
            Configure an event above and click "Run Simulation" to see before/after comparison
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    res         = st.session_state.sim_result
    new_alloc   = res["new_alloc"]
    new_proj    = res["new_proj"]
    new_summary = res["new_summary"]
    event_month = res["event_month"]

    final_nw_orig = orig_proj["net_worth"][-1] if orig_proj["net_worth"] else 0
    final_nw_new  = new_proj["net_worth"][-1]  if new_proj["net_worth"]  else 0
    delta         = final_nw_new - final_nw_orig
    delta_color   = GREEN if delta >= 0 else RED

    # ── Before / After Cards ──────────────────────────────────────────
    st.markdown(f"""
    <h3 style="font-size:1.15rem; font-weight:700; color:{TEXT} !important; margin:28px 0 14px;">
        Before vs. After · Event at Month {event_month}
    </h3>
    """, unsafe_allow_html=True)

    cb, ca = st.columns(2, gap="large")
    with cb:
        st.markdown(f"""
        <div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-top:3px solid {TEXT_MUTED};
                    border-radius:16px; padding:24px; box-shadow:{SHADOW_SM}; margin-bottom:16px;">
            <span class="pf-badge pf-badge-teal" style="margin-bottom:12px; display:inline-block;">Baseline</span>
            <p style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em;
                      color:{TEXT_MUTED} !important; margin:0 0 4px;">Projected Net Worth</p>
            <p style="font-family:'JetBrains Mono',monospace; font-size:2rem; font-weight:700;
                      color:{TEXT} !important; margin:0 0 20px;">₹{final_nw_orig:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:0.82rem; font-weight:600; color:{TEXT_MUTED}; margin:0 0 6px;">Original Allocation</p>', unsafe_allow_html=True)
        allocation_stacked_bar(orig_alloc)

    with ca:
        st.markdown(f"""
        <div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-top:3px solid {PURPLE};
                    border-radius:16px; padding:24px; box-shadow:{SHADOW_SM}; margin-bottom:16px;">
            <span class="pf-badge pf-badge-violet" style="margin-bottom:12px; display:inline-block;">Re-Planned</span>
            <p style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em;
                      color:{TEXT_MUTED} !important; margin:0 0 4px;">Revised Net Worth</p>
            <p style="font-family:'JetBrains Mono',monospace; font-size:2rem; font-weight:700;
                      color:{PURPLE} !important; margin:0 0 6px;">₹{final_nw_new:,.0f}</p>
            <p style="font-size:0.82rem; font-weight:700; color:{delta_color}; margin:0 0 14px;">
                {"▲" if delta>=0 else "▼"} ₹{abs(delta):,.0f} vs baseline
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:0.82rem; font-weight:600; color:{TEXT_MUTED}; margin:0 0 6px;">Revised Allocation</p>', unsafe_allow_html=True)
        allocation_stacked_bar(new_alloc)

    # ── Trajectory Chart ──────────────────────────────────────────────
    st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT} !important; margin:28px 0 12px;">📈 Trajectory Divergence</h4>', unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=orig_proj["months"], y=orig_proj["net_worth"],
        name="Baseline", mode="lines",
        line=dict(color=TEXT_MUTED, width=2.5, dash="dash"),
        hovertemplate="Baseline M%{x}: ₹%{y:,.0f}<extra></extra>"
    ))
    comb_months = orig_proj["months"][:event_month] + [m + event_month for m in new_proj["months"]]
    comb_nw     = orig_proj["net_worth"][:event_month] + new_proj["net_worth"]
    fig.add_trace(go.Scatter(
        x=comb_months, y=comb_nw,
        name="Re-Planned", mode="lines",
        line=dict(color=PURPLE, width=3.5),
        fill="tonexty", fillcolor="rgba(108,76,224,0.06)",
        hovertemplate="Re-Planned M%{x}: ₹%{y:,.0f}<extra></extra>"
    ))
    fig.add_vline(x=event_month, line_dash="dot", line_color=RED, line_width=1.5,
                  annotation_text=f"⚡ Event (M{event_month})",
                  annotation_position="top left",
                  annotation_font=dict(family="Plus Jakarta Sans", size=11, color=RED))

    fig.update_layout(
        height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,1)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=TEXT_MUTED, size=12),
        xaxis=dict(gridcolor="rgba(0,0,0,0.05)", title="Months", zeroline=False,
                   tickfont=dict(family="JetBrains Mono", size=11)),
        yaxis=dict(gridcolor="rgba(0,0,0,0.05)", title="Net Worth (₹)", zeroline=False,
                   tickfont=dict(family="JetBrains Mono", size=11)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=36, b=24), hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Delta Metrics Row ──────────────────────────────────────────────
    st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT} !important; margin:24px 0 12px;">📊 Capital Reallocation Delta</h4>', unsafe_allow_html=True)
    dc1, dc2, dc3, dc4, dc5 = st.columns(5)
    for col, (lbl, ov, nv) in zip([dc1,dc2,dc3,dc4,dc5], [
        ("Emergency",   orig_alloc["emergency_fund"], new_alloc["emergency_fund"]),
        ("Debt",        orig_alloc["debt_payment"],   new_alloc["debt_payment"]),
        ("Savings",     orig_alloc["savings"],         new_alloc["savings"]),
        ("Investments", orig_alloc["investments"],     new_alloc["investments"]),
        ("Net Worth",   final_nw_orig,                 final_nw_new),
    ]):
        col.metric(label=lbl, value=f"₹{nv:,.0f}", delta=f"{nv-ov:+,.0f}")

    # ── Strategy Takeaway ──────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:{PURPLE_SOFT}; border:1px solid rgba(108,76,224,0.18);
                border-left:4px solid {PURPLE}; border-radius:14px; padding:18px 22px; margin-top:24px;">
        <p style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em;
                  color:{PURPLE} !important; margin:0 0 6px;">💡 Adaptive Strategy Takeaway</p>
        <p style="font-size:0.92rem; color:{TEXT_SEC} !important; line-height:1.65; margin:0;">
            {new_summary}
        </p>
    </div>
    """, unsafe_allow_html=True)

page_footer()
