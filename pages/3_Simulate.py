"""
Simulate — Dynamic reassessment with before/after comparison.
"""
import streamlit as st
import json
import plotly.graph_objects as go
from engine import optimise_finances, project_finances, generate_summary, replan
from ui import inject_css, plan_report, hero_metric_card, summary_block, allocation_stacked_bar, combined_net_worth_chart, AMBER, SLATE, TEXT, TEXT_DIM, BG, SURFACE, GREEN, RED

st.set_page_config(page_title="Simulate — Finance Optimiser", page_icon="🔄", layout="wide")
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
        <a href="/Profile" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Profile</a>
        <a href="/Plan" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Plan</a>
        <a href="/Simulate" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{AMBER}; text-decoration:none; padding:6px 14px; border-radius:6px; background:{SURFACE};">Simulate</a>
        <a href="/Scenario_Lab" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Scenario Lab</a>
        <a href="/How_It_Works" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Check if profile exists
if "profile" not in st.session_state:
    st.markdown(f"""
    <div style="text-align:center; padding:80px 0;">
        <h2 style="color:{TEXT};">No profile yet</h2>
        <p style="color:{TEXT_DIM};">Build your financial profile first to simulate life events.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="/Profile" target="_self" style="display:block; text-align:center; padding:14px 28px; background:{AMBER}; color:{BG}; font-family:Inter,sans-serif; font-weight:700; border-radius:8px; text-decoration:none; max-width:300px; margin:0 auto;">Build Your Profile →</a>', unsafe_allow_html=True)
else:
    profile = st.session_state.profile
    orig_alloc = st.session_state.allocation
    orig_proj = st.session_state.projections

    st.markdown(f'<h2 style="color:{TEXT}; margin-bottom:4px;">Simulate a Life Event</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{TEXT_DIM}; font-size:0.9rem; margin-bottom:24px;">See how your plan adapts when conditions change.</p>', unsafe_allow_html=True)

    # Event form
    event_type = st.selectbox("What changed?", [
        "income_change", "expense_change", "rate_change", "new_goal", "emergency_expense"
    ], format_func=lambda x: {
        "income_change": "💰 Income Change",
        "expense_change": "📉 New Expense",
        "rate_change": "📈 Interest Rate Change",
        "new_goal": "🎯 New Financial Goal",
        "emergency_expense": "🚨 Emergency Expense",
    }[x])

    events = []
    horizon = profile.get("horizon_months", 60)

    if event_type == "income_change":
        new_income = st.number_input("New Monthly Income (₹)", 0, 10000000, int(profile["income_monthly"] * 0.75))
        event_month = st.slider("When? (month)", 1, horizon, min(12, horizon))
        events.append({"month": event_month, "type": "income_change", "new_income": new_income})

    elif event_type == "expense_change":
        new_expense = st.number_input("Additional Monthly Expense (₹)", 0, 100000, 5000)
        event_month = st.slider("When? (month)", 1, horizon, min(12, horizon))
        events.append({"month": event_month, "type": "expense_change", "amount": new_expense})

    elif event_type == "rate_change":
        new_rate = st.number_input("New Interest Rate (%)", 0.0, 50.0, 18.0)
        debt_names = [d["name"] for d in profile.get("liabilities", [])]
        target_debt = st.selectbox("Which debt?", debt_names) if debt_names else ""
        event_month = st.slider("When? (month)", 1, horizon, min(12, horizon))
        events.append({"month": event_month, "type": "rate_change", "target": target_debt, "new_rate": new_rate / 100})

    elif event_type == "new_goal":
        g_name = st.text_input("Goal Name", value="Wedding").strip()[:50]
        g_amount = st.number_input("Amount (₹)", 0, 10000000, 300000)
        g_deadline = st.number_input("Deadline (months from now)", 1, 120, 12)
        event_month = st.slider("When? (month)", 1, horizon, min(6, horizon))
        events.append({"month": event_month, "type": "new_goal", "goal": {"name": g_name, "amount": g_amount, "deadline_months": g_deadline}})

    elif event_type == "emergency_expense":
        amount = st.number_input("Emergency Expense (₹)", 0, 1000000, 20000)
        event_month = st.slider("When? (month)", 1, horizon, min(6, horizon))
        events.append({"month": event_month, "type": "emergency_expense", "amount": amount})

    if st.button("🔄 Run Simulation", type="primary", use_container_width=True):
        event_month = events[0]["month"]

        # Re-plan
        new_alloc, new_method, updated_profile = replan(profile, events, event_month)
        new_proj = project_finances(updated_profile, new_alloc, horizon - event_month)
        new_summary = generate_summary(updated_profile, new_alloc, new_proj)

        # Store for potential further use
        st.session_state.sim_result = {
            "new_alloc": new_alloc,
            "new_method": new_method,
            "new_proj": new_proj,
            "new_summary": new_summary,
            "event_month": event_month,
        }

        st.markdown("---")

        # Before/After comparison
        st.markdown(f'<h3 style="color:{TEXT};">Before vs After — Event at Month {event_month}</h3>', unsafe_allow_html=True)

        col_before, col_after = st.columns(2)

        with col_before:
            st.markdown(f'<h4 style="color:{TEXT_DIM};">Original Plan</h4>', unsafe_allow_html=True)
            final_nw_orig = orig_proj["net_worth"][-1] if orig_proj["net_worth"] else 0
            st.markdown(f'<p style="font-family:JetBrains Mono,monospace; font-size:2rem; color:{TEXT};">₹{final_nw_orig:,.0f}</p><p style="color:{TEXT_DIM}; font-size:0.8rem;">Projected Net Worth</p>', unsafe_allow_html=True)
            allocation_stacked_bar(orig_alloc)

        with col_after:
            st.markdown(f'<h4 style="color:{TEXT_DIM};">Revised Plan</h4>', unsafe_allow_html=True)
            final_nw_new = new_proj["net_worth"][-1] if new_proj["net_worth"] else 0
            delta = final_nw_new - final_nw_orig
            delta_color = GREEN if delta >= 0 else RED
            st.markdown(f'<p style="font-family:JetBrains Mono,monospace; font-size:2rem; color:{AMBER};">₹{final_nw_new:,.0f}</p><p style="color:{delta_color}; font-size:0.8rem;">₹{delta:+,.0f} vs original</p>', unsafe_allow_html=True)
            allocation_stacked_bar(new_alloc)

        # Combined net worth chart
        st.markdown("#### Net Worth: Original vs Revised")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=orig_proj["months"], y=orig_proj["net_worth"],
            name="Original Plan", line=dict(color=TEXT_DIM, width=2, dash="dot")
        ))
        # Combined: original before event + revised after
        combined_months = orig_proj["months"][:event_month] + [m + event_month for m in new_proj["months"]]
        combined_nw = orig_proj["net_worth"][:event_month] + new_proj["net_worth"]
        fig.add_trace(go.Scatter(
            x=combined_months, y=combined_nw,
            name="Revised Plan", line=dict(color=AMBER, width=2)
        ))
        fig.add_vline(x=event_month, line_dash="dot", line_color=RED,
                      annotation_text=f"Event (month {event_month})",
                      annotation_font_color=RED)

        fig.update_layout(
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=TEXT_DIM),
            xaxis=dict(gridcolor="rgba(62,92,118,0.15)", title="Months"),
            yaxis=dict(gridcolor="rgba(62,92,118,0.15)", title="Amount (₹)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=20, t=40, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Delta summary
        st.markdown("#### What Changed")
        cols = st.columns(5)
        for i, (label, orig_val, new_val) in enumerate([
            ("Emergency Fund", orig_alloc["emergency_fund"], new_alloc["emergency_fund"]),
            ("Debt Payment", orig_alloc["debt_payment"], new_alloc["debt_payment"]),
            ("Savings", orig_alloc["savings"], new_alloc["savings"]),
            ("Investments", orig_alloc["investments"], new_alloc["investments"]),
            ("Net Worth (final)", final_nw_orig, final_nw_new),
        ]):
            delta = new_val - orig_val
            delta_color = GREEN if delta >= 0 else RED
            cols[i].metric(label, f"₹{new_val:,.0f}", f"₹{delta:+,.0f}")

        st.markdown(f'<p style="color:{TEXT_DIM}; font-size:0.85rem; margin-top:16px;">{new_summary}</p>', unsafe_allow_html=True)
