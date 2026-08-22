"""
Landing Page — Personal Finance Optimiser (Violet/Navy design)
"""
import streamlit as st
from engine import optimise_finances, project_finances, generate_summary, PRESET_PROFILES
from ui import (inject_css, top_nav, page_hero, section_header, stat_card,
                page_footer, PURPLE, PURPLE_BG, TEXT, TEXT_MUTED,
                CARD, BORDER_LIGHT, GREEN, AMBER, TEAL, SHADOW_SM)

st.set_page_config(page_title="Finance Optimiser", page_icon="⚡", layout="wide")
inject_css()

# ── Deferred redirect (must run BEFORE any rendering) ─────────────────
# Streamlit re-runs the whole script on every interaction.
# We store the intent in session_state on button click, then act on it
# at the very top of the next run — before st.switch_page is buried
# inside a column or conditional block.
_pending = st.session_state.pop("_load_preset", None)
if _pending:
    p = PRESET_PROFILES[_pending]
    with st.spinner(f"Loading {p.get('name', _pending)}..."):
        alloc, method = optimise_finances(p, p["horizon_months"])
        proj          = project_finances(p, alloc, p["horizon_months"])
        summ          = generate_summary(p, alloc, proj)
    st.session_state.profile    = p
    st.session_state.allocation = alloc
    st.session_state.method     = method
    st.session_state.projections = proj
    st.session_state.summary    = summ
    st.session_state.pop("ai_recommendations", None)
    st.session_state.pop("chat_history", None)
    st.switch_page("pages/2_Plan.py")

if st.session_state.pop("_go_profile", False):
    st.switch_page("pages/1_Profile.py")

# ── Nav ───────────────────────────────────────────────────────────────
top_nav("Home")

# ── Hero ─────────────────────────────────────────────────────────────
page_hero(
    badge="Mathematical · AI-Powered · Real-Time",
    title="Optimise Every Rupee.<br>Own Your Financial Future.",
    subtitle="Harness deterministic SLSQP optimisation and Groq AI to build a personalised plan "
             "that balances emergency reserves, debt payoff, wealth goals, and compound growth."
)

st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

# ── Primary CTA ───────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding:0 24px 24px;">
    <p style="font-size:0.85rem; font-weight:600; color:{TEXT_MUTED}; text-transform:uppercase;
       letter-spacing:0.06em; margin:0 0 20px;">Start in 3 steps: Profile → Optimise → Simulate</p>
</div>
""", unsafe_allow_html=True)

_, cta_col, _ = st.columns([1, 1.4, 1])
with cta_col:
    if st.button("✨  Build Your Financial Profile  →",
                 use_container_width=True, type="primary", key="cta_profile"):
        st.session_state["_go_profile"] = True
        st.rerun()

# ── Divider ───────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex; align-items:center; gap:16px; margin:16px 48px 40px;">
    <div style="flex:1; height:1px; background:{BORDER_LIGHT};"></div>
    <span style="font-size:0.78rem; font-weight:600; color:{TEXT_MUTED}; text-transform:uppercase;
          letter-spacing:0.08em; white-space:nowrap;">Or try an instant archetype</span>
    <div style="flex:1; height:1px; background:{BORDER_LIGHT};"></div>
</div>
""", unsafe_allow_html=True)

# ── Archetype Cards ───────────────────────────────────────────────────
def _preset_card(p: dict, income_label: str, debt_label: str, badge_color: str):
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:16px;
                padding:24px; box-shadow:{SHADOW_SM}; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
            <span style="font-size:2rem; line-height:1;">{p.get('icon', '💡')}</span>
            <span style="background:{badge_color}18; color:{badge_color}; border:1px solid {badge_color}33;
                         border-radius:9999px; padding:3px 10px; font-size:0.72rem; font-weight:700;
                         letter-spacing:0.04em; text-transform:uppercase;">{income_label}</span>
        </div>
        <p style="font-size:1.05rem; font-weight:700; color:{TEXT} !important; margin:0 0 6px;">
            {p.get('name', 'Profile')}
        </p>
        <p style="font-size:0.82rem; color:{TEXT_MUTED} !important; line-height:1.45; margin:0 0 14px;">
            {p.get('description', '')}
        </p>
        <div style="border-top:1px solid {BORDER_LIGHT}; padding-top:10px;">
            <span style="font-size:0.75rem; color:{TEXT_MUTED} !important;">
                <span style="font-weight:700; color:{TEXT} !important; font-family:'JetBrains Mono',monospace;">
                    ₹{p['income_monthly']//1000}k
                </span> / mo income · {debt_label}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


ARCHETYPES = [
    ("young_pro",      "₹75k / mo",  "2 active debts", PURPLE, "home_p1"),
    ("family_builder", "₹1.5L / mo", "Home + Car loan", TEAL,  "home_p2"),
    ("fire_seeker",    "₹2L / mo",   "Debt-free",       GREEN, "home_p3"),
]

pc1, pc2, pc3 = st.columns(3, gap="large")
for col, (preset_key, income_lbl, debt_lbl, badge_col, btn_key) in zip([pc1, pc2, pc3], ARCHETYPES):
    with col:
        p = PRESET_PROFILES[preset_key]
        _preset_card(p, income_lbl, debt_lbl, badge_col)
        if st.button(
            f"Load {p.get('name', preset_key)} →",
            key=btn_key,
            use_container_width=True,
        ):
            # Store intent and rerun — switch happens at the top of next run
            st.session_state["_load_preset"] = preset_key
            st.rerun()

# ── Feature Spotlights ────────────────────────────────────────────────
st.markdown("<div style='height:48px;'></div>", unsafe_allow_html=True)

section_header(
    label="Platform Capabilities",
    title="Everything You Need to Take Control",
    sub="From mathematical optimisation to AI-powered advice — built for real financial decisions."
)

f1, f2, f3 = st.columns(3, gap="large")
features = [
    ("🧮", PURPLE, PURPLE_BG,
     "Mathematical Optimisation",
     "SciPy SLSQP solver maximises a composite well-being index across 4 pillars simultaneously — not just raw wealth."),
    ("🔄", TEAL, "rgba(6,182,212,0.08)",
     "Dynamic Life-Event Simulation",
     "Stress-test income shocks, new EMIs, or rate changes. The engine re-optimises globally from the event month forward."),
    ("🤖", GREEN, "rgba(16,185,129,0.08)",
     "Groq AI Financial Advisor",
     "Contextual, actionable advice powered by LLaMA 3.3 70B — with quick-action prompts and conversational follow-ups."),
]
for col, (icon, color, bg, title, desc) in zip([f1, f2, f3], features):
    with col:
        st.markdown(f"""
        <div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:16px;
                    padding:24px; box-shadow:{SHADOW_SM}; min-height:200px;">
            <div style="width:48px; height:48px; border-radius:13px; background:{bg};
                        display:flex; align-items:center; justify-content:center;
                        font-size:1.4rem; margin-bottom:16px; border:1px solid {color}22;">
                {icon}
            </div>
            <p style="font-size:1rem; font-weight:700; color:{TEXT} !important; margin:0 0 8px;">{title}</p>
            <p style="font-size:0.87rem; color:{TEXT_MUTED} !important; line-height:1.6; margin:0;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# ── Stats Row ─────────────────────────────────────────────────────────
st.markdown("<div style='height:48px;'></div>", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)
stats = [
    ("⚡", "< 50ms", "Solve Time",      PURPLE, PURPLE_BG),
    ("🛡️", "3–6×",  "Emergency Months", TEAL,   "rgba(6,182,212,0.08)"),
    ("📈", "SLSQP", "Solver Method",    GREEN,  "rgba(16,185,129,0.08)"),
    ("🤖", "70B",   "AI Model Params",  AMBER,  "rgba(245,158,11,0.08)"),
]
for col, (icon, val, lbl, color, bg) in zip([s1, s2, s3, s4], stats):
    with col:
        stat_card(icon, val, lbl, color, bg)

page_footer()
