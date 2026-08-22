"""
How It Works — Architecture, methodology, and model details (Violet/Navy design)
"""
import streamlit as st
import plotly.graph_objects as go
from ui import (inject_css, top_nav, page_footer, section_header,
                PURPLE, PURPLE_BG, PURPLE_SOFT, TEXT, TEXT_SEC, TEXT_MUTED,
                CARD, BG, BORDER_LIGHT, GREEN, AMBER, RED, TEAL, SHADOW_SM, SHADOW_MD, GRAD)

st.set_page_config(page_title="How It Works — Finance Optimiser", page_icon="🔬", layout="wide")
inject_css()
top_nav("How It Works")

# ── Page Hero ──────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg, #14141F 0%, #1E1E3A 100%);
            padding:60px 48px 64px; position:relative; overflow:hidden; text-align:center;">
    <div style="position:absolute; width:500px; height:500px; top:-200px; left:50%; transform:translateX(-50%);
                border-radius:50%; background:radial-gradient(circle, rgba(108,76,224,0.22) 0%, transparent 65%);
                pointer-events:none;"></div>
    <div style="position:absolute; width:300px; height:300px; bottom:-120px; right:0%;
                border-radius:50%; background:radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 65%);
                pointer-events:none;"></div>
    <div style="position:relative; z-index:1; max-width:680px; margin:0 auto;">
        <span style="display:inline-flex; align-items:center; gap:6px; background:rgba(108,76,224,0.22);
                     border:1px solid rgba(108,76,224,0.38); color:#C4B5FD;
                     border-radius:9999px; padding:5px 16px; font-size:0.78rem; font-weight:700;
                     text-transform:uppercase; letter-spacing:0.06em; margin-bottom:20px;">
            🔬 Technical Documentation
        </span>
        <h1 style="font-size:2.4rem; font-weight:800; color:#FFFFFF !important; margin:0 0 16px;
                   letter-spacing:-0.02em; line-height:1.15;">How the Engine Works</h1>
        <p style="font-size:1rem; color:rgba(255,255,255,0.55) !important; line-height:1.65; margin:0;">
            A complete walkthrough of the mathematical optimisation engine, constraint system, AI advisor integration,
            and simulation architecture powering Finance Optimiser.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:48px;'></div>", unsafe_allow_html=True)

# ── Architecture Grid ──────────────────────────────────────────────────
section_header("System Architecture", "Four Core Layers", "Each layer is independent yet deeply integrated.")

layers = [
    (PURPLE, "🧮", "Optimisation Engine",
     "SciPy SLSQP",
     "Solves a constrained nonlinear objective over monthly surplus. Maximises a composite well-being score across 4 pillars with priority weights."),
    (TEAL, "📐", "Constraint System",
     "10+ hard rules",
     "Enforces minimum EMI payments, emergency fund floors, goal deadlines, non-negativity, and budget bounds at every iteration."),
    (GREEN, "🤖", "AI Advisor Layer",
     "Groq · LLaMA 3.3 70B",
     "Receives full plan context (profile, allocation, projections) and generates contextual financial recommendations and conversational responses."),
    (AMBER, "🔄", "Simulation Engine",
     "Global re-optimise",
     "Applies life events (income shocks, new loans, emergencies) at a specified month and re-runs the full SLSQP solve from that month forward."),
]

lc1, lc2, lc3, lc4 = st.columns(4, gap="large")
for col, (color, icon, title, badge, desc) in zip([lc1, lc2, lc3, lc4], layers):
    with col:
        st.markdown(f"""
        <div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-top:4px solid {color};
                    border-radius:16px; padding:22px; box-shadow:{SHADOW_SM}; height:100%; min-height:230px;">
            <div style="width:48px; height:48px; border-radius:13px; background:{color}18;
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.4rem; margin-bottom:14px; border:1px solid {color}30;">
                {icon}
            </div>
            <p style="font-size:0.95rem; font-weight:700; color:{TEXT} !important; margin:0 0 4px;">{title}</p>
            <span style="font-size:0.72rem; font-weight:700; background:{color}18; color:{color};
                         border-radius:6px; padding:2px 8px; display:inline-block; margin-bottom:10px;
                         letter-spacing:0.03em;">{badge}</span>
            <p style="font-size:0.82rem; color:{TEXT_MUTED} !important; line-height:1.6; margin:0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ── Objective Function ─────────────────────────────────────────────────
st.markdown("<div style='height:48px;'></div>", unsafe_allow_html=True)
section_header("Mathematical Core", "The Objective Function",
               "SLSQP minimises the negative of this composite score to find the optimal monthly capital split.")

st.markdown(f"""
<div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:16px;
            padding:28px 32px; box-shadow:{SHADOW_SM}; margin-bottom:24px;">
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:32px; align-items:start;">
        <div>
            <p style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em;
                      color:{PURPLE} !important; margin:0 0 12px;">Composite Objective</p>
            <div style="background:{PURPLE_SOFT}; border-radius:12px; padding:20px 24px; font-family:'JetBrains Mono',monospace;
                        font-size:0.88rem; color:{TEXT} !important; line-height:2.1;">
                <span style="color:{TEXT_MUTED};"># Maximise composite well-being W</span><br>
                <b>W</b> = w1 &times; S_emerg + w2 &times; S_debt<br>
                &nbsp;&nbsp;&nbsp;&nbsp;+ w3 &times; S_wealth + w4 &times; S_goals<br><br>
                <span style="color:{TEXT_MUTED};"># where S_emerg = ef_built / ef_target</span><br>
                <span style="color:{TEXT_MUTED};">#   S_debt  = debt_paid / total_debt</span><br>
                <span style="color:{TEXT_MUTED};">#   S_wealth = invested / (income - expenses)</span><br>
                <span style="color:{TEXT_MUTED};">#   S_goals = avg_goal_funding_rate</span>
            </div>
        </div>
        <div>
            <p style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em;
                      color:{PURPLE} !important; margin:0 0 12px;">Pillar Weights by Risk Profile</p>
            <div style="display:flex; flex-direction:column; gap:10px;">
""", unsafe_allow_html=True)

for risk, weights, color in [
    ("Conservative", [0.40, 0.30, 0.15, 0.15], AMBER),
    ("Moderate",     [0.30, 0.25, 0.25, 0.20], PURPLE),
    ("Aggressive",   [0.20, 0.20, 0.35, 0.25], GREEN),
]:
    labels  = ["Emergency", "Debt", "Wealth", "Goals"]
    pct_str = " · ".join(f"{l}: {w*100:.0f}%" for l, w in zip(labels, weights))
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:10px; padding:12px 16px;
                box-shadow:{SHADOW_SM}; margin-bottom:0;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-size:0.82rem; font-weight:700; color:{color} !important;">{risk}</span>
        </div>
        <div style="display:flex; height:8px; border-radius:9999px; overflow:hidden; gap:2px;">
            {''.join(f'<div style="flex:{w}; background:{c}; border-radius:9999px;"></div>' for w, c in zip(weights, [PURPLE, TEAL, GREEN, AMBER]))}
        </div>
        <p style="font-size:0.72rem; color:{TEXT_MUTED}; margin:6px 0 0; font-family:'JetBrains Mono',monospace;">{pct_str}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div></div></div>", unsafe_allow_html=True)

# ── Constraint Table ───────────────────────────────────────────────────
st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
section_header("Constraint System", "Hard Constraints Enforced per Iteration")

constraints = [
    ("Budget Feasibility",      "Sum of all allocations ≤ monthly disposable income",                              "Always"),
    ("Minimum EMI Payments",    "debt_payment ≥ Σ min_payment across all active liabilities",                     "Active debts"),
    ("Non-negativity",          "emergency_fund, debt_payment, savings, investments, goals ≥ 0",                  "Always"),
    ("Emergency Floor",         "emergency_fund_alloc ≥ 10% of disposable (until target met)",                   "Until funded"),
    ("Goal Deadline Pressure",  "goal_alloc[i] ≥ (goal.amount / months_remaining) × 0.7",                        "Per goal"),
    ("Savings Floor",           "savings ≥ 5% of disposable (conservative) / 3% (moderate) / 0% (aggressive)",   "Per risk tier"),
    ("Investment Floor",        "investments ≥ 0% (conservative) / 5% (moderate) / 10% (aggressive)",            "Per risk tier"),
    ("Debt Ceiling",            "debt_payment ≤ 50% of disposable (prevents over-payment lockout)",               "Always"),
]

rows_html = ""
for i, (name, rule, scope) in enumerate(constraints):
    bg = "background:#F8F9FF;" if i % 2 == 0 else ""
    rows_html += f"""
    <tr style="{bg}">
        <td style="padding:12px 16px; font-weight:700; color:{TEXT} !important;">{name}</td>
        <td style="padding:12px 16px; font-family:'JetBrains Mono',monospace; font-size:0.82rem; color:{TEXT_SEC} !important;">{rule}</td>
        <td style="padding:12px 16px;"><span class="pf-badge pf-badge-violet">{scope}</span></td>
    </tr>
    """

st.markdown(f"""
<div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:16px;
            overflow:hidden; box-shadow:{SHADOW_SM}; margin-bottom:24px;">
    <table style="width:100%; border-collapse:collapse;">
        <thead>
            <tr style="background:{BG}; border-bottom:1px solid {BORDER_LIGHT};">
                <th style="padding:12px 16px; text-align:left; font-size:0.72rem; font-weight:700; text-transform:uppercase;
                           letter-spacing:0.07em; color:{TEXT_MUTED} !important;">Constraint</th>
                <th style="padding:12px 16px; text-align:left; font-size:0.72rem; font-weight:700; text-transform:uppercase;
                           letter-spacing:0.07em; color:{TEXT_MUTED} !important;">Rule</th>
                <th style="padding:12px 16px; text-align:left; font-size:0.72rem; font-weight:700; text-transform:uppercase;
                           letter-spacing:0.07em; color:{TEXT_MUTED} !important;">Scope</th>
            </tr>
        </thead>
        <tbody>{rows_html}</tbody>
    </table>
</div>
""", unsafe_allow_html=True)

# ── Simulation Flow ─────────────────────────────────────────────────────
st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
section_header("Dynamic Re-Planning", "How Life Events Are Simulated",
               "The engine doesn't just adjust — it globally re-optimises from the event month forward.")

steps = [
    ("1", "Event Injection",     "A life event (income change, new loan, emergency) is inserted at month M with its parameters.",              PURPLE),
    ("2", "Profile Mutation",    "The profile is mutated: income updated, liabilities appended, goals added, or lump-sum deducted.",            TEAL),
    ("3", "SLSQP Re-solve",      "A fresh SLSQP optimisation runs on the mutated profile for the remaining (horizon - M) months.",              GREEN),
    ("4", "Divergence Analysis", "Both the original and re-planned net worth trajectories are compared to quantify the event's financial impact.", AMBER),
]

for snum, stitle, sdesc, scolor in steps:
    st.markdown(f"""
    <div style="display:flex; gap:16px; align-items:flex-start; margin-bottom:14px;
                background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:14px;
                padding:18px 20px; box-shadow:{SHADOW_SM};">
        <div style="width:40px; height:40px; border-radius:12px; background:{scolor}18;
                    display:flex; align-items:center; justify-content:center;
                    font-size:1rem; font-weight:700; color:{scolor}; flex-shrink:0;
                    border:1px solid {scolor}30; font-family:'JetBrains Mono',monospace;">
            {snum}
        </div>
        <div>
            <p style="font-size:0.92rem; font-weight:700; color:{TEXT} !important; margin:0 0 4px;">{stitle}</p>
            <p style="font-size:0.85rem; color:{TEXT_MUTED} !important; line-height:1.55; margin:0;">{sdesc}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Sample Solve Visualisation ─────────────────────────────────────────
st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
section_header("Live Example", "Moderate-Risk Allocation — ₹1.5L Income · ₹80k Expenses")

demo_surplus = 70000
demo_alloc   = {"emergency_fund": 10000, "debt_payment": 20000, "savings": 15000, "investments": 25000}
demo_labels  = list(demo_alloc.keys())
demo_values  = list(demo_alloc.values())
demo_colors  = [PURPLE, RED, GREEN, TEAL]

fig_pie = go.Figure(data=[go.Pie(
    labels=[l.replace("_"," ").title() for l in demo_labels],
    values=demo_values, hole=0.62,
    marker=dict(colors=demo_colors, line=dict(color="#FFFFFF", width=3)),
    textinfo="percent+label", textfont=dict(family="Plus Jakarta Sans", size=12, color="#FFFFFF"),
    hovertemplate="<b>%{label}</b>: ₹%{value:,.0f}<extra></extra>"
)])
fig_pie.update_layout(
    height=300, showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=20, b=20),
    annotations=[dict(text=f"₹{demo_surplus:,.0f}<br><span style='font-size:10px'>surplus</span>",
                       x=0.5, y=0.5, font=dict(size=15, family="JetBrains Mono", color=TEXT), showarrow=False)]
)

dc1, dc2 = st.columns([1.6, 1])
with dc1:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:16px;
                padding:24px; box-shadow:{SHADOW_SM};">
        <p style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.07em;
                  color:{PURPLE} !important; margin:0 0 14px;">SLSQP Optimal Split · Moderate Risk</p>
        <table style="width:100%; border-collapse:collapse;">
    """, unsafe_allow_html=True)
    for lbl, val, col in zip(demo_labels, demo_values, demo_colors):
        pct = val / demo_surplus * 100
        st.markdown(f"""
            <tr>
                <td style="padding:8px 0; width:130px;">
                    <span style="display:inline-flex; align-items:center; gap:7px;">
                        <span style="width:10px; height:10px; border-radius:3px; background:{col}; display:inline-block;"></span>
                        <span style="font-size:0.85rem; color:{TEXT_SEC} !important;">{lbl.replace("_"," ").title()}</span>
                    </span>
                </td>
                <td style="padding:8px 0; padding-left:20px; min-width:150px;">
                    <div style="height:8px; border-radius:9999px; background:{BORDER_LIGHT}; overflow:hidden;">
                        <div style="height:100%; width:{pct:.1f}%; background:{col}; border-radius:9999px;"></div>
                    </div>
                </td>
                <td style="padding:8px 0; padding-left:16px; font-family:'JetBrains Mono',monospace;
                           font-size:0.88rem; font-weight:700; color:{TEXT} !important; white-space:nowrap;">
                    ₹{val:,.0f} <span style="color:{TEXT_MUTED}; font-size:0.75rem;">({pct:.0f}%)</span>
                </td>
            </tr>
        """, unsafe_allow_html=True)
    st.markdown("</table></div>", unsafe_allow_html=True)
with dc2:
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Tech Stack ────────────────────────────────────────────────────────
st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
section_header("Technology Stack", "Built With", "Open-source, fast, and production-ready.")

tech = [
    ("🐍", "Python 3.11+",        "Runtime"),
    ("⚡", "Streamlit",            "UI Framework"),
    ("🧮", "SciPy SLSQP",         "Optimiser"),
    ("📊", "Plotly",               "Visualisation"),
    ("🤖", "Groq API",            "AI Backend"),
    ("🦙", "LLaMA 3.3 70B",       "Language Model"),
    ("📦", "NumPy / Pandas",       "Numerics"),
    ("🎨", "CSS / JS Animations",  "UI Polish"),
]

tc_cols = st.columns(4, gap="medium")
for i, (icon, name, role) in enumerate(tech):
    with tc_cols[i % 4]:
        st.markdown(f"""
        <div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:12px;
                    padding:14px 16px; box-shadow:{SHADOW_SM}; margin-bottom:12px; display:flex;
                    align-items:center; gap:12px;">
            <span style="font-size:1.4rem;">{icon}</span>
            <div>
                <p style="font-size:0.88rem; font-weight:700; color:{TEXT} !important; margin:0;">{name}</p>
                <p style="font-size:0.72rem; color:{TEXT_MUTED} !important; margin:0;">{role}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Data Privacy ──────────────────────────────────────────────────────
st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
st.markdown(f"""
<div style="background:{PURPLE_SOFT}; border:1px solid rgba(108,76,224,0.18); border-left:4px solid {PURPLE};
            border-radius:14px; padding:20px 24px; text-align:center; max-width:800px; margin:0 auto;">
    <p style="font-size:1.1rem; margin:0 0 6px;">🔒 <b style="color:{TEXT} !important;">Your data stays yours.</b></p>
    <p style="font-size:0.88rem; color:{TEXT_MUTED} !important; line-height:1.6; margin:0;">
        All financial computations happen entirely in-session on Streamlit's server.
        No profile data, income figures, or goal details are stored to any database or transmitted externally.
        AI prompts sent to Groq include only anonymised financial ratios, not personal identifiers.
    </p>
</div>
""", unsafe_allow_html=True)

page_footer()
