"""
Scenario Lab — Compare up to 3 portfolio strategies (Violet/Navy design)
"""
import json
import streamlit as st
import plotly.graph_objects as go
from engine import optimise_finances, project_finances, generate_summary, PRESET_PROFILES
from ui import (inject_css, top_nav, page_footer,
                PURPLE, PURPLE_2, PURPLE_BG, PURPLE_SOFT, TEXT, TEXT_SEC, TEXT_MUTED,
                CARD, BG, BORDER_LIGHT, GREEN, AMBER, RED, TEAL, SHADOW_SM, SHADOW_MD, GRAD)

st.set_page_config(page_title="Scenario Lab — Finance Optimiser", page_icon="⚗️", layout="wide")
inject_css()
top_nav("Scenario Lab")

SCENARIO_COLORS = [PURPLE, TEAL, AMBER]
SCENARIO_LABELS = ["Scenario A", "Scenario B", "Scenario C"]
SCENARIO_ICONS  = ["🟣", "🔵", "🟡"]

SCENARIO_PRESETS = {
    "Max Wealth (FIRE)": {
        "income_monthly": 200000, "expenses_monthly": 70000,
        "assets": [{"type":"mutual_fund","amount":2000000,"return_rate":0.14}],
        "liabilities": [], "goals": [],
        "emergency_fund_current": 500000, "emergency_fund_target": 420000,
        "risk_tolerance": "aggressive", "horizon_months": 120,
        "icon": "🔥", "description": "Maximum compounding — aggressive equity allocation."
    },
    "Balanced Safety": {
        "income_monthly": 150000, "expenses_monthly": 80000,
        "assets": [{"type":"fd","amount":500000,"return_rate":0.065}],
        "liabilities": [{"name":"Home Loan","balance":2500000,"interest_rate":0.085,"min_payment":20000}],
        "goals": [{"name":"Children's Education","amount":1500000,"deadline_months":72}],
        "emergency_fund_current": 300000, "emergency_fund_target": 480000,
        "risk_tolerance": "moderate", "horizon_months": 84,
        "icon": "🛡️", "description": "Balanced approach: debt reduction + goal funding."
    },
    "Conservative Savers": {
        "income_monthly": 80000, "expenses_monthly": 40000,
        "assets": [{"type":"savings","amount":200000,"return_rate":0.045}],
        "liabilities": [{"name":"Personal Loan","balance":200000,"interest_rate":0.14,"min_payment":5000}],
        "goals": [{"name":"Emergency Corpus","amount":300000,"deadline_months":24}],
        "emergency_fund_current": 100000, "emergency_fund_target": 240000,
        "risk_tolerance": "conservative", "horizon_months": 60,
        "icon": "💰", "description": "Safety-first: emergency fund and low-risk savings."
    },
}

# ── Page Header ────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg, #14141F 0%, #1E1E3A 100%);
            padding:36px 48px 40px; position:relative; overflow:hidden;">
    <div style="position:absolute; width:350px; height:350px; top:-120px; right:-60px;
                border-radius:50%; background:radial-gradient(circle, rgba(245,158,11,0.18) 0%, transparent 70%);
                pointer-events:none;"></div>
    <div style="position:relative; z-index:1;">
        <span style="font-size:0.72rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
                     color:rgba(253,230,138,0.8);">Side-by-Side Portfolio Analysis</span>
        <h1 style="font-size:2rem; font-weight:800; color:#FFFFFF !important; margin:6px 0 6px;">
            Scenario Lab
        </h1>
        <p style="font-size:0.9rem; color:rgba(255,255,255,0.5) !important; margin:0; max-width:540px;">
            Compare up to 3 financial strategies side-by-side — presets or fully custom JSON profiles — to identify the optimal path.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

# ── Scenario Builder ──────────────────────────────────────────────────
def get_default_profile():
    if "profile" in st.session_state:
        return st.session_state.profile
    return PRESET_PROFILES["young_pro"]

scenarios = []

tab1, tab2, tab3 = st.tabs([f"{SCENARIO_ICONS[i]} {SCENARIO_LABELS[i]}" for i in range(3)])

for tab_idx, (tab, color, label, icon) in enumerate(zip([tab1, tab2, tab3], SCENARIO_COLORS, SCENARIO_LABELS, SCENARIO_ICONS)):
    with tab:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:18px;">
            <div style="width:6px; height:36px; border-radius:3px; background:{color};"></div>
            <div>
                <p style="font-size:1rem; font-weight:700; color:{TEXT} !important; margin:0;">{icon} {label}</p>
                <p style="font-size:0.8rem; color:{TEXT_MUTED} !important; margin:0;">Configure or load a preset</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Preset quick-fill
        preset_col, _ = st.columns([2, 1])
        with preset_col:
            selected_preset = st.selectbox(f"Load preset into {label}:",
                                           ["—", "My Current Profile"] + list(SCENARIO_PRESETS.keys()),
                                           key=f"psel_{tab_idx}")

        if selected_preset and selected_preset != "—":
            if selected_preset == "My Current Profile":
                p = get_default_profile()
            else:
                p = SCENARIO_PRESETS[selected_preset]
            default_json = json.dumps({k: v for k, v in p.items() if k not in ("icon","description","name")}, indent=2)
        else:
            default_json = json.dumps({
                "income_monthly":       get_default_profile()["income_monthly"],
                "expenses_monthly":     get_default_profile()["expenses_monthly"],
                "assets":               get_default_profile()["assets"],
                "liabilities":          get_default_profile().get("liabilities", []),
                "goals":                get_default_profile().get("goals", []),
                "emergency_fund_current": get_default_profile()["emergency_fund_current"],
                "emergency_fund_target":  get_default_profile()["emergency_fund_target"],
                "risk_tolerance":         get_default_profile().get("risk_tolerance", "moderate"),
                "horizon_months":         get_default_profile().get("horizon_months", 60),
            }, indent=2)

        # JSON editor
        with st.expander("✏️ Edit profile JSON", expanded=(tab_idx == 0 and not selected_preset)):
            raw = st.text_area(f"Profile JSON for {label}:", value=default_json,
                               height=260, key=f"json_{tab_idx}")

        # Parse
        parsed_profile = None
        try:
            parsed_profile = json.loads(raw)
            required = {"income_monthly","expenses_monthly","assets","liabilities",
                        "goals","emergency_fund_current","emergency_fund_target",
                        "risk_tolerance","horizon_months"}
            missing = required - set(parsed_profile.keys())
            if missing:
                st.markdown(f'<div class="pf-warn-box">⚠ Missing keys: {", ".join(missing)}</div>', unsafe_allow_html=True)
                parsed_profile = None
            else:
                st.markdown(f'<div class="pf-info-box">✓ Profile JSON valid · horizon {parsed_profile["horizon_months"]} months · {parsed_profile["risk_tolerance"]} risk</div>', unsafe_allow_html=True)
        except json.JSONDecodeError as e:
            st.markdown(f'<div class="pf-warn-box" style="color:{RED};">❌ JSON parse error: {e}</div>', unsafe_allow_html=True)

        scenarios.append((label, color, icon, parsed_profile))

# ── Run Comparisons ────────────────────────────────────────────────────
run = st.button("⚗️ Run Comparison →", type="primary", use_container_width=True)

if run:
    results = []
    for lbl, col, ico, p in scenarios:
        if p is None:
            continue
        h = p.get("horizon_months", 60)
        try:
            alloc, method = optimise_finances(p, h)
            proj          = project_finances(p, alloc, h)
            summ          = generate_summary(p, alloc, proj)
            results.append({"label": lbl, "color": col, "icon": ico,
                            "profile": p, "alloc": alloc, "proj": proj, "summary": summ})
        except Exception as e:
            st.warning(f"{lbl}: optimisation failed — {e}")
    st.session_state.scenario_results = results

if "scenario_results" not in st.session_state or not st.session_state.scenario_results:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px dashed {BORDER_LIGHT}; border-radius:16px;
                padding:48px; text-align:center; margin-top:8px;">
        <span style="font-size:2.5rem; display:block; margin-bottom:12px; opacity:0.4;">⚗️</span>
        <p style="font-size:1rem; font-weight:600; color:{TEXT_MUTED} !important; margin:0;">
            Configure your scenarios above and click "Run Comparison"
        </p>
    </div>
    """, unsafe_allow_html=True)
    page_footer()
    st.stop()

results = st.session_state.scenario_results

# ── Summary Banner ─────────────────────────────────────────────────────
st.markdown(f"""
<h3 style="font-size:1.2rem; font-weight:700; color:{TEXT} !important; margin:32px 0 16px;">
    📊 Comparison Results — {len(results)} Scenario{'s' if len(results)>1 else ''}
</h3>
""", unsafe_allow_html=True)

metric_cols = st.columns(len(results), gap="large")
for col, r in zip(metric_cols, results):
    final_nw = r["proj"]["net_worth"][-1] if r["proj"]["net_worth"] else 0
    h        = r["profile"]["horizon_months"]
    dfm      = r["proj"].get("debt_free_month", None)
    with col:
        st.markdown(f"""
        <div style="background:{CARD}; border-top:4px solid {r['color']}; border:1px solid {BORDER_LIGHT};
                    border-radius:16px; padding:22px; box-shadow:{SHADOW_SM}; margin-bottom:16px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                <span style="width:12px; height:12px; border-radius:50%; background:{r['color']}; display:inline-block;"></span>
                <span style="font-size:0.82rem; font-weight:700; color:{r['color']} !important; text-transform:uppercase; letter-spacing:0.05em;">{r['label']}</span>
            </div>
            <p style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em;
                      color:{TEXT_MUTED} !important; margin:0 0 3px;">Net Worth @ Month {h}</p>
            <p style="font-family:'JetBrains Mono',monospace; font-size:1.75rem; font-weight:700;
                      color:{r['color']} !important; margin:0 0 8px;">₹{final_nw:,.0f}</p>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <span class="pf-badge pf-badge-violet">{r['profile']['risk_tolerance'].upper()}</span>
                {'<span class="pf-badge pf-badge-green">✓ DEBT-FREE</span>' if dfm else '<span class="pf-badge pf-badge-amber">HAS DEBT</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Net Worth Trajectories ────────────────────────────────────────────
st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT} !important; margin:12px 0 12px;">📈 Net Worth Trajectories</h4>', unsafe_allow_html=True)

fig = go.Figure()
for r in results:
    fig.add_trace(go.Scatter(
        x=r["proj"]["months"], y=r["proj"]["net_worth"],
        name=r["label"], mode="lines",
        line=dict(color=r["color"], width=3, shape="spline"),
        hovertemplate=f"<b>{r['label']}</b> M%{{x}}: ₹%{{y:,.0f}}<extra></extra>"
    ))
fig.update_layout(
    height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,1)",
    font=dict(family="Plus Jakarta Sans, sans-serif", color=TEXT_MUTED, size=12),
    xaxis=dict(gridcolor="rgba(0,0,0,0.05)", title="Months", zeroline=False,
               tickfont=dict(family="JetBrains Mono", size=11)),
    yaxis=dict(gridcolor="rgba(0,0,0,0.05)", title="Net Worth (₹)", zeroline=False,
               tickfont=dict(family="JetBrains Mono", size=11)),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=36, b=24), hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

# ── Allocation Comparison ──────────────────────────────────────────────
st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT} !important; margin:24px 0 12px;">💰 Monthly Allocation Breakdown</h4>', unsafe_allow_html=True)

alloc_cols = st.columns(len(results), gap="large")
alloc_keys  = ["emergency_fund", "debt_payment", "savings", "investments"]
alloc_names = ["Emergency", "Debt", "Savings", "Invest."]
bar_colors  = [PURPLE, TEAL, GREEN, AMBER]

for col, r in zip(alloc_cols, results):
    with col:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:6px; margin-bottom:14px;">
            <span style="width:10px; height:10px; border-radius:50%; background:{r['color']}; display:inline-block;"></span>
            <span style="font-size:0.85rem; font-weight:700; color:{r['color']} !important;">{r['label']}</span>
        </div>
        """, unsafe_allow_html=True)

        bar_fig = go.Figure(go.Bar(
            x=[r["alloc"].get(k, 0) for k in alloc_keys],
            y=alloc_names, orientation="h",
            marker=dict(color=bar_colors,
                        line=dict(color="rgba(255,255,255,0.3)", width=1)),
            text=[f"₹{r['alloc'].get(k,0):,.0f}" for k in alloc_keys],
            textposition="auto",
            textfont=dict(family="JetBrains Mono", size=10, color="#FFFFFF"),
            hovertemplate="%{y}: ₹%{x:,.0f}<extra></extra>"
        ))
        bar_fig.update_layout(
            height=220, showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,1)",
            margin=dict(l=60, r=10, t=10, b=10),
            xaxis=dict(gridcolor="rgba(0,0,0,0.05)", tickfont=dict(family="JetBrains Mono", size=9)),
            yaxis=dict(gridcolor=None, tickfont=dict(family="Plus Jakarta Sans", size=11))
        )
        st.plotly_chart(bar_fig, use_container_width=True)

# ── Recommendation Summaries ──────────────────────────────────────────
st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT} !important; margin:24px 0 12px;">💡 Strategy Summaries</h4>', unsafe_allow_html=True)

for r in results:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-left:4px solid {r['color']};
                border-radius:14px; padding:18px 22px; margin-bottom:12px; box-shadow:{SHADOW_SM};">
        <div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">
            <span style="font-size:0.82rem; font-weight:700; color:{r['color']} !important;">{r['label']}</span>
        </div>
        <p style="font-size:0.88rem; color:{TEXT_SEC} !important; line-height:1.65; margin:0;">{r['summary']}</p>
    </div>
    """, unsafe_allow_html=True)

page_footer()
