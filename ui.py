"""
Shared UI components — White + Purple theme (forced via CSS)
"""
import streamlit as st
import plotly.graph_objects as go

# Colors
PURPLE = "#6C4CE0"
PURPLE_LIGHT = "#7B5CF0"
PURPLE_BG = "#F3EEFF"
NAVY = "#1A1A2E"
BG = "#FAFAFA"
CARD = "#FFFFFF"
TEXT = "#1A1A2E"
TEXT_SEC = "#6B7280"
TEAL = "#0EA5E9"
GREEN = "#10B981"
AMBER = "#F59E0B"
RED = "#EF4444"


def inject_css():
    """Inject custom CSS — forces light theme regardless of Streamlit config."""
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap');

    /* FORCE LIGHT THEME */
    .stApp {{
        background-color: {BG} !important;
        color: {TEXT} !important;
    }}
    .stApp > header {{
        background-color: transparent !important;
    }}
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    .main .block-container {{
        background-color: {BG} !important;
        color: {TEXT} !important;
    }}

    /* Fix all text to dark */
    p, span, label, h1, h2, h3, h4, h5, h6, div, td, th, li, a {{
        color: {TEXT} !important;
    }}
    h1 {{ color: {PURPLE} !important; }}
    h2 {{ color: {TEXT} !important; }}
    h3 {{ color: {TEXT} !important; }}

    /* Fix Streamlit widget colors */
    .stSelectbox label, .stSlider label, .stNumberInput label, .stTextInput label {{
        color: {TEXT} !important;
    }}

    /* Fix input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {{
        background-color: {CARD} !important;
        color: {TEXT} !important;
        border: 1px solid #D1D5DB !important;
    }}

    /* Fix buttons */
    .stButton > button {{
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 8px;
        background-color: {PURPLE} !important;
        color: white !important;
        border: none !important;
    }}
    .stButton > button:hover {{
        background-color: {PURPLE_LIGHT} !important;
    }}

    /* Fix metric cards */
    [data-testid="stMetric"] {{
        background: {CARD} !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {PURPLE} !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {TEXT_SEC} !important;
    }}

    /* Fix sidebar if visible */
    section[data-testid="stSidebar"] {{
        background-color: {CARD} !important;
    }}

    /* Fix expander */
    .streamlit-expanderHeader {{
        color: {TEXT} !important;
    }}

    /* Fix tabs */
    .stTabs [data-baseweb="tab"] {{
        color: {TEXT_SEC} !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {PURPLE} !important;
    }}

    /* Monospace for numbers */
    .mono, [data-testid="stMetricValue"] {{
        font-family: 'JetBrains Mono', monospace !important;
    }}

    /* Hero metric */
    .hero-metric {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.2rem;
        font-weight: 700;
        color: {PURPLE};
        line-height: 1.1;
        margin: 0;
    }}
    .hero-label {{
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: {TEXT_SEC};
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 4px;
    }}

    /* Summary block */
    .summary-block {{
        border: 1px solid {PURPLE_BG};
        border-radius: 12px;
        padding: 20px 24px;
        background: {PURPLE_BG};
        margin: 16px 0;
    }}
    .summary-block p {{
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: {TEXT};
        line-height: 1.6;
        margin: 0;
    }}

    /* Goal progress */
    .goal-row {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 10px 0;
    }}
    .goal-bar-bg {{
        flex: 1;
        height: 8px;
        background: #E5E7EB;
        border-radius: 4px;
        overflow: hidden;
    }}
    .goal-bar-fill {{
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }}
    .goal-name {{
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: {TEXT};
        min-width: 120px;
        font-weight: 500;
    }}
    .goal-status {{
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: {TEXT_SEC};
        min-width: 200px;
    }}

    /* Allocation bar */
    .alloc-bar {{
        display: flex;
        height: 44px;
        border-radius: 8px;
        overflow: hidden;
        margin: 12px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    .alloc-segment {{
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: white;
        font-weight: 700;
        min-width: 30px;
    }}

    /* Step indicator */
    .step-indicator {{
        display: flex;
        gap: 8px;
        margin: 20px 0;
    }}
    .step-dot {{
        width: 32px;
        height: 4px;
        border-radius: 2px;
        background: #E5E7EB;
    }}
    .step-dot.active {{
        background: {PURPLE};
    }}
    .step-dot.done {{
        background: #C4B5FD;
    }}

    /* Chat bubbles */
    .chat-user {{
        background: {PURPLE};
        color: white !important;
        padding: 10px 16px;
        border-radius: 12px 12px 0 12px;
        max-width: 70%;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }}
    .chat-ai {{
        background: {PURPLE_BG};
        color: {TEXT} !important;
        padding: 10px 16px;
        border-radius: 12px 12px 12px 0;
        max-width: 70%;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }}

    /* Fix info/warning/error boxes */
    .stAlert {{
        background-color: {CARD} !important;
    }}

    /* Fix dataframe */
    .stDataFrame {{
        background-color: {CARD} !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def hero_metric_card(value, label, sub_metrics=None):
    html = f'<p class="hero-metric">{value}</p><p class="hero-label">{label}</p>'
    if sub_metrics:
        for sv, sl in sub_metrics:
            html += f'<p style="font-family: JetBrains Mono, monospace; font-size: 1rem; color: {TEXT_SEC}; margin-top: 8px;"><span style="color: {TEXT};">{sv}</span> {sl}</p>'
    st.markdown(html, unsafe_allow_html=True)


def summary_block(text):
    st.markdown(f'<div class="summary-block"><p>{text}</p></div>', unsafe_allow_html=True)


def allocation_stacked_bar(allocation):
    categories = [
        ("Emergency Fund", allocation.get("emergency_fund", 0), AMBER),
        ("Debt Payment", allocation.get("debt_payment", 0), TEAL),
        ("Savings", allocation.get("savings", 0), GREEN),
        ("Investments", allocation.get("investments", 0), PURPLE),
    ]
    for gname, gval in allocation.get("goals", {}).items():
        categories.append((f"Goal: {gname}", gval, "#8B5CF6"))

    total = max(1, sum(v for _, v, _ in categories))
    html = '<div class="alloc-bar">'
    for name, val, color in categories:
        pct = (val / total) * 100
        if pct > 5:
            html += f'<div class="alloc-segment" style="width:{pct}%; background:{color};" title="{name}: ₹{val:,.0f}">₹{val:,.0f}</div>'
    html += '</div>'

    html += '<div style="display:flex; flex-wrap:wrap; gap:16px; margin-top:8px;">'
    for name, val, color in categories:
        html += f'<span style="font-family:Inter,sans-serif; font-size:0.75rem; color:{TEXT_SEC};"><span style="display:inline-block; width:10px; height:10px; background:{color}; border-radius:3px; margin-right:4px;"></span>{name}: ₹{val:,.0f}</span>'
    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)


def combined_net_worth_chart(projections):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=projections["months"], y=projections["net_worth"],
        name="Net Worth", fill="tozeroy",
        line=dict(color=PURPLE, width=2),
        fillcolor="rgba(108, 76, 224, 0.08)"
    ))
    fig.add_trace(go.Scatter(
        x=projections["months"], y=projections["debt_remaining"],
        name="Debt Remaining",
        line=dict(color=TEAL, width=2)
    ))
    if projections.get("debt_free_month"):
        fig.add_vline(x=projections["debt_free_month"], line_dash="dot",
                      line_color=GREEN, annotation_text="Debt-free",
                      annotation_font_color=GREEN)

    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,1)",
        font=dict(family="Inter, sans-serif", color=TEXT_SEC),
        xaxis=dict(gridcolor="rgba(0,0,0,0.06)", title="Months"),
        yaxis=dict(gridcolor="rgba(0,0,0,0.06)", title="Amount (₹)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig


def goal_progress_bars(goals, allocation, horizon):
    for g in goals:
        monthly_needed = g["amount"] / max(g["deadline_months"], 1)
        goal_alloc = allocation.get("goals", {}).get(g["name"], 0)
        total_allocated = goal_alloc * g["deadline_months"]
        progress = min(100, (total_allocated / max(g["amount"], 1)) * 100)

        if goal_alloc >= monthly_needed * 0.8:
            status = f"On track for month {g['deadline_months']}"
            color = GREEN
        else:
            shortfall = monthly_needed - goal_alloc
            months_behind = round(shortfall / max(monthly_needed, 1) * g["deadline_months"])
            status = f"{months_behind} month(s) behind deadline"
            color = RED

        st.markdown(f"""
        <div class="goal-row">
            <span class="goal-name">{g['name']}</span>
            <div class="goal-bar-bg">
                <div class="goal-bar-fill" style="width:{progress}%; background:{color};"></div>
            </div>
            <span class="goal-status">{status} — ₹{g['amount']:,.0f} target</span>
        </div>
        """, unsafe_allow_html=True)


def plan_report(profile, allocation, method, projections, summary):
    horizon = profile.get("horizon_months", 60)
    final_nw = projections["net_worth"][-1] if projections["net_worth"] else 0
    debt_free = projections.get("debt_free_month")
    goals = profile.get("goals", [])
    on_track = sum(1 for g in goals if allocation.get("goals", {}).get(g["name"], 0) >= (g["amount"] / max(g["deadline_months"], 1)) * 0.8)

    sub_metrics = []
    if debt_free:
        sub_metrics.append((f"Month {debt_free}", "debt-free"))
    else:
        sub_metrics.append(("Not within horizon", "debt-free"))
    sub_metrics.append((f"{on_track}/{len(goals)}", "goals on track"))

    hero_metric_card(f"₹{final_nw:,.0f}", f"Projected Net Worth at Month {horizon}", sub_metrics)
    summary_block(summary)

    if method == "optimised":
        st.markdown(f'<span style="font-family:JetBrains Mono,monospace; font-size:0.75rem; color:{GREEN}; background:{GREEN}11; border-radius:6px; padding:4px 10px;">OPTIMISED (SLSQP)</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span style="font-family:JetBrains Mono,monospace; font-size:0.75rem; color:{AMBER}; background:{AMBER}11; border-radius:6px; padding:4px 10px;">FALLBACK (WATERFALL)</span>', unsafe_allow_html=True)

    st.markdown("")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### This Month's Allocation")
        allocation_stacked_bar(allocation)
        st.markdown("#### Key Numbers")
        disposable = profile["income_monthly"] - profile["expenses_monthly"]
        st.markdown(f"""
        | | |
        |---|---|
        | **Disposable Income** | ₹{disposable:,.0f} |
        | **Emergency Fund** | ₹{allocation['emergency_fund']:,.0f} |
        | **Debt Payment** | ₹{allocation['debt_payment']:,.0f} |
        | **Savings** | ₹{allocation['savings']:,.0f} |
        | **Investments** | ₹{allocation['investments']:,.0f} |
        """)
    with col2:
        st.markdown("#### Net Worth & Debt Over Time")
        fig = combined_net_worth_chart(projections)
        st.plotly_chart(fig, use_container_width=True)

    if goals:
        st.markdown("#### Goal Progress")
        goal_progress_bars(goals, allocation, horizon)

    recs = generate_recommendations(profile, allocation)
    if recs:
        st.markdown("#### Recommendations")
        for rec in recs:
            st.markdown(f"- {rec}")


def generate_recommendations(profile, allocation):
    recs = []
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
    if not recs:
        recs.append("Your plan looks well-balanced.")
    return recs
