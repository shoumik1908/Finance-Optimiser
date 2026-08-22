"""
Shared UI Design System — Personal Finance Optimiser
Violet (#6C4CE0) + Navy hero/nav + White/off-white cards
"""
import streamlit as st
import plotly.graph_objects as go

# ── Design Tokens ──────────────────────────────────────────────────
PURPLE      = "#6C4CE0"
PURPLE_2    = "#8B6FF7"
PURPLE_DARK = "#4A35B8"
PURPLE_BG   = "#F0EEFF"
PURPLE_SOFT = "#EDE9FF"
NAVY        = "#14141F"
NAVY_2      = "#1A1A2E"
NAVY_3      = "#1E1E3A"
BG          = "#F4F5F9"
CARD        = "#FFFFFF"
TEXT        = "#1A1A2E"
TEXT_SEC    = "#4A4B6F"
TEXT_MUTED  = "#8B8DAA"
BORDER      = "rgba(108, 76, 224, 0.12)"
BORDER_LIGHT = "#E4E6F0"
GREEN       = "#10B981"
AMBER       = "#F59E0B"
RED         = "#F43F5E"
TEAL        = "#06B6D4"
SHADOW_SM   = "0 2px 8px rgba(108, 76, 224, 0.10)"
SHADOW_MD   = "0 4px 24px rgba(108, 76, 224, 0.12)"
SHADOW_LG   = "0 8px 40px rgba(108, 76, 224, 0.15)"
GRAD        = f"linear-gradient(135deg, {PURPLE} 0%, {TEAL} 100%)"
GRAD_SOFT   = f"linear-gradient(135deg, {PURPLE_SOFT} 0%, #E0F2FE 100%)"


def inject_css():
    """Inject full design system CSS."""
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* ── Reset & Base ── */
    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background-color: {BG} !important;
        color: {TEXT} !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    [data-testid="stHeader"] {{ background: transparent !important; display: none; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    footer {{ display: none !important; }}
    #MainMenu {{ display: none !important; }}
    .main .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}

    /* ── Typography ── */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: {TEXT} !important;
        font-weight: 700 !important;
        line-height: 1.25 !important;
    }}
    p, span, li, td, th {{ color: {TEXT_SEC} !important; line-height: 1.6; }}

    /* ── Page Wrapper ── */
    .pf-page {{
        min-height: 100vh;
        background: {BG};
        padding-bottom: 80px;
    }}

    /* ── Nav Bar ── */
    .pf-nav {{
        background: {NAVY};
        padding: 0 48px;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 1px 0 rgba(255,255,255,0.06), {SHADOW_MD};
    }}
    .pf-nav-brand {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.15rem;
        font-weight: 800;
        color: #FFFFFF !important;
        text-decoration: none;
    }}
    .pf-nav-brand .brand-icon {{
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: {GRAD};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        box-shadow: {SHADOW_SM};
    }}
    .pf-nav-links {{
        display: flex;
        align-items: center;
        gap: 4px;
    }}
    .pf-nav-link {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.875rem;
        font-weight: 500;
        color: rgba(255,255,255,0.65) !important;
        text-decoration: none;
        padding: 6px 14px;
        border-radius: 8px;
        transition: all 0.18s ease;
    }}
    .pf-nav-link:hover {{
        color: #FFFFFF !important;
        background: rgba(255,255,255,0.08);
    }}
    .pf-nav-link.active {{
        color: #FFFFFF !important;
        background: {PURPLE};
        font-weight: 600;
    }}

    /* ── Hero Block ── */
    .pf-hero {{
        background: linear-gradient(135deg, {NAVY} 0%, {NAVY_3} 60%, #1A1040 100%);
        padding: 72px 48px 80px;
        position: relative;
        overflow: hidden;
    }}
    .pf-hero::before {{
        content: '';
        position: absolute;
        width: 600px; height: 600px;
        top: -200px; right: -100px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(108,76,224,0.25) 0%, transparent 70%);
        pointer-events: none;
    }}
    .pf-hero::after {{
        content: '';
        position: absolute;
        width: 400px; height: 400px;
        bottom: -150px; left: -50px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%);
        pointer-events: none;
    }}
    .pf-hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(108,76,224,0.25);
        border: 1px solid rgba(108,76,224,0.4);
        color: #C4B5FD !important;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 5px 14px;
        border-radius: 9999px;
        margin-bottom: 20px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}
    .pf-hero-title {{
        font-size: 3rem;
        font-weight: 800;
        color: #FFFFFF !important;
        line-height: 1.12;
        margin: 0 0 16px;
        letter-spacing: -0.02em;
    }}
    .pf-hero-sub {{
        font-size: 1.1rem;
        color: rgba(255,255,255,0.65) !important;
        line-height: 1.6;
        max-width: 540px;
        margin: 0;
    }}

    /* ── Content Wrapper ── */
    .pf-content {{
        padding: 40px 48px;
        max-width: 1200px;
        margin: 0 auto;
    }}

    /* ── Section Header ── */
    .pf-section-label {{
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: {PURPLE} !important;
        margin: 0 0 6px;
        display: block;
    }}
    .pf-section-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {TEXT} !important;
        margin: 0 0 4px;
        line-height: 1.3;
    }}
    .pf-section-sub {{
        font-size: 0.9rem;
        color: {TEXT_MUTED} !important;
        margin: 0 0 24px;
    }}

    /* ── Cards ── */
    .pf-card {{
        background: {CARD};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 16px;
        padding: 24px;
        box-shadow: {SHADOW_SM};
        margin-bottom: 16px;
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}
    .pf-card:hover {{
        box-shadow: {SHADOW_MD};
    }}
    .pf-card-accent {{
        border-left: 4px solid {PURPLE};
    }}
    .pf-card-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }}

    /* ── Stat Card ── */
    .pf-stat {{
        background: {CARD};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 14px;
        padding: 20px;
        box-shadow: {SHADOW_SM};
        transition: box-shadow 0.2s, transform 0.2s;
    }}
    .pf-stat:hover {{
        box-shadow: {SHADOW_MD};
        transform: translateY(-2px);
    }}
    .pf-stat-icon {{
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
        margin-bottom: 12px;
    }}
    .pf-stat-value {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.5rem;
        font-weight: 700;
        color: {TEXT} !important;
        line-height: 1.15;
        margin: 0 0 4px;
    }}
    .pf-stat-label {{
        font-size: 0.78rem;
        font-weight: 600;
        color: {TEXT_MUTED} !important;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin: 0;
    }}
    .pf-stat-delta {{
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 6px;
        display: inline-flex;
        align-items: center;
        gap: 3px;
    }}
    .pf-stat-delta.up {{ color: {GREEN} !important; }}
    .pf-stat-delta.down {{ color: {RED} !important; }}

    /* ── Hero Metric ── */
    .pf-hero-metric {{
        background: {GRAD};
        border-radius: 20px;
        padding: 32px 36px;
        color: white;
        position: relative;
        overflow: hidden;
        margin-bottom: 24px;
        box-shadow: {SHADOW_LG};
    }}
    .pf-hero-metric::after {{
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        pointer-events: none;
    }}
    .pf-hero-metric-label {{
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: rgba(255,255,255,0.75) !important;
        margin: 0 0 8px;
    }}
    .pf-hero-metric-value {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.8rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0 0 12px;
        line-height: 1;
    }}
    .pf-hero-metric-chips {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 16px;
    }}
    .pf-hero-metric-chip {{
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 9999px;
        padding: 5px 14px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #FFFFFF !important;
        backdrop-filter: blur(4px);
    }}

    /* ── Badges & Pills ── */
    .pf-badge {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}
    .pf-badge-violet {{ background: {PURPLE_BG}; color: {PURPLE} !important; }}
    .pf-badge-green  {{ background: rgba(16,185,129,0.1); color: {GREEN} !important; }}
    .pf-badge-amber  {{ background: rgba(245,158,11,0.1); color: {AMBER} !important; }}
    .pf-badge-red    {{ background: rgba(244,63,94,0.1); color: {RED} !important; }}
    .pf-badge-teal   {{ background: rgba(6,182,212,0.1); color: {TEAL} !important; }}

    /* ── Buttons ── */
    .stButton > button {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 10px 22px !important;
        font-size: 0.9rem !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        background: {PURPLE} !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: {SHADOW_SM} !important;
        letter-spacing: 0.01em !important;
    }}
    .stButton > button:hover {{
        background: {PURPLE_DARK} !important;
        box-shadow: {SHADOW_MD} !important;
        transform: translateY(-1px);
    }}
    .stButton > button:active {{
        transform: translateY(0) !important;
        box-shadow: none !important;
    }}
    .stButton > button[kind="secondary"] {{
        background: {CARD} !important;
        color: {PURPLE} !important;
        border: 1.5px solid {PURPLE} !important;
        box-shadow: none !important;
    }}
    .stButton > button[kind="secondary"]:hover {{
        background: {PURPLE_BG} !important;
    }}

    /* ── Form Inputs ── */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {{
        background: {CARD} !important;
        border: 1.5px solid {BORDER_LIGHT} !important;
        border-radius: 10px !important;
        transition: border-color 0.18s, box-shadow 0.18s;
    }}
    div[data-baseweb="input"]:focus-within > div,
    div[data-baseweb="textarea"]:focus-within > div {{
        border-color: {PURPLE} !important;
        box-shadow: 0 0 0 3px rgba(108,76,224,0.12) !important;
    }}
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {{
        color: {TEXT} !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }}
    div[data-baseweb="select"] > div {{
        background: {CARD} !important;
        border: 1.5px solid {BORDER_LIGHT} !important;
        border-radius: 10px !important;
        color: {TEXT} !important;
    }}
    div[data-baseweb="select"]:focus-within > div {{
        border-color: {PURPLE} !important;
        box-shadow: 0 0 0 3px rgba(108,76,224,0.12) !important;
    }}
    label[data-testid="stWidgetLabel"] p,
    .stSlider label p,
    .stSelectbox label p,
    .stNumberInput label p,
    .stTextInput label p,
    .stTextArea label p {{
        color: {TEXT_SEC} !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        margin-bottom: 6px !important;
    }}

    /* ── Metrics ── */
    [data-testid="stMetric"] {{
        background: {CARD} !important;
        border: 1px solid {BORDER_LIGHT} !important;
        border-radius: 14px !important;
        padding: 20px !important;
        box-shadow: {SHADOW_SM} !important;
        transition: box-shadow 0.2s, transform 0.2s;
    }}
    [data-testid="stMetric"]:hover {{
        box-shadow: {SHADOW_MD} !important;
        transform: translateY(-1px);
    }}
    [data-testid="stMetricValue"] {{
        color: {PURPLE} !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {TEXT_MUTED} !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    [data-testid="stMetricDelta"] {{
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }}

    /* ── Expander ── */
    .streamlit-expanderHeader {{
        background: {CARD} !important;
        border: 1px solid {BORDER_LIGHT} !important;
        border-radius: 12px !important;
        color: {TEXT} !important;
        font-weight: 600 !important;
        padding: 14px 20px !important;
    }}
    .streamlit-expanderContent {{
        background: {CARD} !important;
        border: 1px solid {BORDER_LIGHT} !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 20px !important;
    }}

    /* ── Stepper ── */
    .pf-stepper {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        position: relative;
        margin: 28px 0 36px;
        padding: 0 8px;
    }}
    .pf-stepper::before {{
        content: '';
        position: absolute;
        top: 20px;
        left: 36px; right: 36px;
        height: 2px;
        background: {BORDER_LIGHT};
        z-index: 0;
    }}
    .pf-step {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
        position: relative;
        z-index: 1;
    }}
    .pf-step-circle {{
        width: 40px; height: 40px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.9rem;
        font-weight: 700;
        border: 2px solid {BORDER_LIGHT};
        background: {CARD};
        color: {TEXT_MUTED} !important;
        transition: all 0.25s ease;
    }}
    .pf-step-circle.active {{
        background: {PURPLE};
        border-color: {PURPLE};
        color: #FFFFFF !important;
        box-shadow: 0 0 0 4px rgba(108,76,224,0.2);
    }}
    .pf-step-circle.done {{
        background: {PURPLE_BG};
        border-color: {PURPLE};
        color: {PURPLE} !important;
    }}
    .pf-step-label {{
        font-size: 0.72rem;
        font-weight: 600;
        color: {TEXT_MUTED} !important;
        text-align: center;
        max-width: 70px;
        line-height: 1.3;
    }}
    .pf-step-label.active {{ color: {PURPLE} !important; }}
    .pf-step-label.done {{ color: {TEXT_SEC} !important; }}

    /* ── Allocation Bar ── */
    .pf-alloc-bar {{
        display: flex;
        height: 40px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: {SHADOW_SM};
        margin: 12px 0;
    }}
    .pf-alloc-seg {{
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 700;
        color: #FFFFFF;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        padding: 0 6px;
        transition: filter 0.18s;
    }}
    .pf-alloc-seg:hover {{ filter: brightness(1.1); }}

    /* ── Goal Progress ── */
    .pf-goal-card {{
        background: {CARD};
        border: 1px solid {BORDER_LIGHT};
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: {SHADOW_SM};
    }}
    .pf-goal-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }}
    .pf-goal-name {{
        font-weight: 700;
        font-size: 0.95rem;
        color: {TEXT} !important;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .pf-progress-track {{
        height: 8px;
        background: {BORDER_LIGHT};
        border-radius: 9999px;
        overflow: hidden;
        margin-bottom: 8px;
    }}
    .pf-progress-fill {{
        height: 100%;
        border-radius: 9999px;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .pf-goal-meta {{
        display: flex;
        justify-content: space-between;
        font-size: 0.78rem;
        color: {TEXT_MUTED} !important;
    }}

    /* ── Chat Bubbles ── */
    .pf-chat-user {{
        background: {GRAD};
        color: #FFFFFF !important;
        padding: 12px 16px;
        border-radius: 16px 16px 4px 16px;
        font-size: 0.9rem;
        line-height: 1.5;
        max-width: 78%;
        box-shadow: {SHADOW_SM};
    }}
    .pf-chat-ai {{
        background: {CARD};
        border: 1px solid {BORDER_LIGHT};
        color: {TEXT_SEC} !important;
        padding: 14px 18px;
        border-radius: 16px 16px 16px 4px;
        font-size: 0.9rem;
        line-height: 1.65;
        max-width: 80%;
        box-shadow: {SHADOW_SM};
    }}
    .pf-chat-ai-header {{
        font-size: 0.75rem;
        font-weight: 700;
        color: {PURPLE} !important;
        margin-bottom: 6px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}

    /* ── Chip / Quick Action ── */
    .pf-chip {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 14px;
        background: {CARD};
        border: 1.5px solid {BORDER_LIGHT};
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: {TEXT_SEC} !important;
        cursor: pointer;
        transition: all 0.18s;
    }}
    .pf-chip:hover {{
        background: {PURPLE_BG};
        border-color: {PURPLE};
        color: {PURPLE} !important;
    }}

    /* ── Summary Block ── */
    .pf-summary {{
        background: {PURPLE_SOFT};
        border: 1px solid rgba(108,76,224,0.18);
        border-left: 4px solid {PURPLE};
        border-radius: 12px;
        padding: 18px 22px;
        margin: 16px 0;
    }}
    .pf-summary p {{ color: {TEXT_SEC} !important; font-size: 0.95rem; line-height: 1.6; margin: 0; }}

    /* ── Tables ── */
    .pf-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.9rem;
    }}
    .pf-table th {{
        font-weight: 700;
        color: {TEXT_MUTED} !important;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 12px 16px;
        background: {BG};
        border-bottom: 1px solid {BORDER_LIGHT};
    }}
    .pf-table td {{
        padding: 12px 16px;
        color: {TEXT_SEC} !important;
        border-bottom: 1px solid {BORDER_LIGHT};
    }}
    .pf-table tr:last-child td {{ border-bottom: none; }}
    .pf-table .pf-table-val {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        color: {TEXT} !important;
    }}

    /* ── Info Alert ── */
    .pf-info-box {{
        background: rgba(6,182,212,0.07);
        border: 1px solid rgba(6,182,212,0.2);
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 0.88rem;
        color: {TEXT_SEC} !important;
        margin: 8px 0;
    }}
    .pf-warn-box {{
        background: rgba(245,158,11,0.07);
        border: 1px solid rgba(245,158,11,0.2);
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 0.88rem;
        color: {TEXT_SEC} !important;
        margin: 8px 0;
    }}

    /* ── Hide Streamlit sidebar nav ── */
    [data-testid="stSidebarNav"] {{ display: none !important; }}
    section[data-testid="stSidebar"] {{ display: none !important; }}

    /* ── Misc fixes ── */
    .stAlert {{ border-radius: 10px !important; }}
    .stDataFrame {{ border-radius: 12px !important; overflow: hidden; }}
    [data-testid="stSpinner"] p {{ color: {TEXT_SEC} !important; }}
    </style>
    """, unsafe_allow_html=True)


def top_nav(active: str = "Home"):
    """Render the unified dark-navy top navigation bar."""
    links = [
        ("Home", "/"),
        ("Profile", "/Profile"),
        ("Plan", "/Plan"),
        ("Simulate", "/Simulate"),
        ("Scenario Lab", "/Scenario_Lab"),
        ("How It Works", "/How_It_Works"),
    ]
    items = ""
    for name, href in links:
        cls = "pf-nav-link active" if name == active else "pf-nav-link"
        items += f'<a href="{href}" target="_self" class="{cls}">{name}</a>'

    st.markdown(f"""
    <nav class="pf-nav">
        <a href="/" target="_self" class="pf-nav-brand">
            <div class="brand-icon">⚡</div>
            Finance<span style="color:{PURPLE_2};">Optimiser</span>
        </a>
        <div class="pf-nav-links">{items}</div>
    </nav>
    """, unsafe_allow_html=True)


def page_hero(badge: str, title: str, subtitle: str):
    """Render a dark-navy hero section."""
    st.markdown(f"""
    <div class="pf-hero">
        <div style="position:relative; z-index:1; max-width:760px; margin:0 auto; text-align:center;">
            <div class="pf-hero-badge">✦ {badge}</div>
            <h1 class="pf-hero-title">{title}</h1>
            <p class="pf-hero-sub">{subtitle}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(label: str, title: str, sub: str = ""):
    """Render a consistent section header."""
    sub_html = f'<p class="pf-section-sub">{sub}</p>' if sub else ""
    st.markdown(f"""
    <div style="margin-bottom:8px;">
        <span class="pf-section-label">{label}</span>
        <h2 class="pf-section-title">{title}</h2>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def stat_card(icon: str, value: str, label: str, color: str = PURPLE, bg: str = PURPLE_BG, delta: str = "", delta_up: bool = True):
    delta_html = ""
    if delta:
        dcls = "up" if delta_up else "down"
        arrow = "↑" if delta_up else "↓"
        delta_html = f'<p class="pf-stat-delta {dcls}">{arrow} {delta}</p>'
    st.markdown(f"""
    <div class="pf-stat">
        <div class="pf-stat-icon" style="background:{bg};">
            <span style="font-size:1.2rem;">{icon}</span>
        </div>
        <p class="pf-stat-value" style="color:{color} !important;">{value}</p>
        <p class="pf-stat-label">{label}</p>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def hero_metric_card(value: str, label: str, chips: list = None):
    """Full-width gradient hero metric card."""
    chips_html = ""
    if chips:
        for cv, cl in chips:
            chips_html += f'<span class="pf-hero-metric-chip">{cv} · {cl}</span>'
        chips_html = f'<div class="pf-hero-metric-chips">{chips_html}</div>'
    st.markdown(f"""
    <div class="pf-hero-metric">
        <p class="pf-hero-metric-label">{label}</p>
        <p class="pf-hero-metric-value">{value}</p>
        {chips_html}
    </div>
    """, unsafe_allow_html=True)


def summary_block(text: str):
    st.markdown(f'<div class="pf-summary"><p>{text}</p></div>', unsafe_allow_html=True)


def wizard_stepper(current_step: int, steps: list):
    """Render the 5-step profile wizard stepper."""
    items = ""
    for i, (icon, name) in enumerate(steps, 1):
        if i < current_step:
            cls = "done"
            circle_content = "✓"
        elif i == current_step:
            cls = "active"
            circle_content = icon
        else:
            cls = ""
            circle_content = str(i)
        items += f"""
        <div class="pf-step">
            <div class="pf-step-circle {cls}">{circle_content}</div>
            <span class="pf-step-label {cls}">{name}</span>
        </div>
        """
    st.markdown(f'<div class="pf-stepper">{items}</div>', unsafe_allow_html=True)


def allocation_stacked_bar(allocation: dict):
    """Render the gradient allocation ribbon bar."""
    colors = [PURPLE, "#0EA5E9", GREEN, TEAL, "#8B5CF6", "#EC4899"]
    cats = [
        ("Emergency", allocation.get("emergency_fund", 0)),
        ("Debt",      allocation.get("debt_payment",  0)),
        ("Savings",   allocation.get("savings",       0)),
        ("Invest.",   allocation.get("investments",   0)),
    ]
    for gname, gval in allocation.get("goals", {}).items():
        cats.append((gname[:10], gval))

    total = max(1, sum(v for _, v in cats))
    segs  = ""
    leg   = ""
    for idx, (name, val) in enumerate(cats):
        pct = (val / total) * 100
        col = colors[idx % len(colors)]
        if pct > 3:
            segs += f'<div class="pf-alloc-seg" style="width:{pct:.1f}%; background:{col};" title="{name}: ₹{val:,.0f} ({pct:.1f}%)">₹{val:,.0f}</div>'
        leg += f"""
        <div style="display:flex; align-items:center; gap:6px;">
            <span style="width:10px; height:10px; border-radius:3px; background:{col}; display:inline-block; flex-shrink:0;"></span>
            <span style="font-size:0.78rem; color:{TEXT_SEC};">{name}</span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:0.78rem; font-weight:700; color:{TEXT}; margin-left:auto;">₹{val:,.0f}</span>
        </div>
        """
    st.markdown(f"""
    <div class="pf-alloc-bar">{segs}</div>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(160px, 1fr)); gap:8px; margin:10px 0 20px;">{leg}</div>
    """, unsafe_allow_html=True)


def goal_progress_cards(goals: list, allocation: dict, horizon: int):
    """Render modern goal progress cards."""
    if not goals:
        st.markdown(f'<div class="pf-info-box">No financial goals configured in your profile.</div>',
                    unsafe_allow_html=True)
        return
    for g in goals:
        monthly_needed = g["amount"] / max(g["deadline_months"], 1)
        goal_alloc     = allocation.get("goals", {}).get(g["name"], 0)
        total_projected = goal_alloc * g["deadline_months"]
        progress        = min(100.0, (total_projected / max(g["amount"], 1)) * 100)
        on_track        = goal_alloc >= monthly_needed * 0.8

        bar_color  = f"linear-gradient(90deg, {PURPLE} 0%, {TEAL} 100%)" if on_track else f"linear-gradient(90deg, {AMBER} 0%, {RED} 100%)"
        badge_html = f'<span class="pf-badge pf-badge-green">✓ On Track</span>' if on_track else f'<span class="pf-badge pf-badge-amber">⚠ Needs Attention</span>'

        months_text = f"{g['deadline_months']} mo deadline"
        alloc_text  = f"₹{goal_alloc:,.0f} / mo allocated"

        st.markdown(f"""
        <div class="pf-goal-card">
            <div class="pf-goal-header">
                <span class="pf-goal-name">🎯 {g['name']}</span>
                {badge_html}
            </div>
            <div class="pf-progress-track">
                <div class="pf-progress-fill" style="width:{progress:.1f}%; background:{bar_color};"></div>
            </div>
            <div class="pf-goal-meta">
                <span>{alloc_text}</span>
                <span style="font-family:'JetBrains Mono',monospace; font-weight:700; color:{TEXT};">₹{g['amount']:,.0f} target · {months_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def combined_net_worth_chart(projections: dict):
    """Violet-to-teal gradient Plotly net worth + debt chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=projections["months"], y=projections["net_worth"],
        name="Net Worth", mode="lines",
        line=dict(color=PURPLE, width=3, shape="spline"),
        fill="tozeroy", fillcolor="rgba(108,76,224,0.07)",
        hovertemplate="<b>Month %{x}</b><br>Net Worth: ₹%{y:,.0f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=projections["months"], y=projections["debt_remaining"],
        name="Debt Remaining", mode="lines",
        line=dict(color=RED, width=2, dash="dot"),
        hovertemplate="<b>Month %{x}</b><br>Debt: ₹%{y:,.0f}<extra></extra>"
    ))
    if projections.get("debt_free_month"):
        dfm = projections["debt_free_month"]
        fig.add_vline(x=dfm, line_dash="dash", line_color=GREEN, line_width=1.5,
                      annotation_text=f"Debt-Free (M{dfm})", annotation_position="top left",
                      annotation_font=dict(family="Plus Jakarta Sans", size=11, color=GREEN))

    fig.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,1)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=TEXT_MUTED, size=12),
        xaxis=dict(gridcolor="rgba(0,0,0,0.05)", title="Months",
                   title_font=dict(size=12, color=TEXT_MUTED), zeroline=False,
                   tickfont=dict(family="JetBrains Mono", size=11)),
        yaxis=dict(gridcolor="rgba(0,0,0,0.05)", title="Amount (₹)",
                   title_font=dict(size=12, color=TEXT_MUTED), zeroline=False,
                   tickfont=dict(family="JetBrains Mono", size=11)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=12, color=TEXT_SEC)),
        margin=dict(l=20, r=20, t=36, b=24),
        hovermode="x unified"
    )
    return fig


def allocation_donut_chart(allocation: dict):
    """Violet-blue-teal donut for capital allocation."""
    labels = ["Emergency", "Debt", "Savings", "Investments"]
    values = [allocation.get("emergency_fund",0), allocation.get("debt_payment",0),
              allocation.get("savings",0), allocation.get("investments",0)]
    colors = [PURPLE, "#0EA5E9", GREEN, TEAL]
    for gname, gval in allocation.get("goals", {}).items():
        labels.append(gname[:12])
        values.append(gval)
        colors.append("#8B5CF6")

    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.64,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2.5)),
        textinfo="percent", textfont=dict(family="JetBrains Mono", size=11, color="#FFFFFF"),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>"
    )])
    total = sum(values)
    fig.update_layout(
        height=280, showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[dict(text=f"₹{total:,.0f}", x=0.5, y=0.5,
                          font=dict(size=14, family="JetBrains Mono", color=TEXT),
                          showarrow=False)]
    )
    return fig


def plan_report(profile: dict, allocation: dict, method: str, projections: dict, summary: str):
    """Render the full plan report with Stitch design."""
    horizon  = profile.get("horizon_months", 60)
    final_nw = projections["net_worth"][-1] if projections["net_worth"] else 0
    debt_free = projections.get("debt_free_month")
    goals     = profile.get("goals", [])
    on_track  = sum(1 for g in goals
                    if allocation.get("goals", {}).get(g["name"], 0)
                    >= (g["amount"] / max(g["deadline_months"], 1)) * 0.8)

    chips = []
    chips.append((f"Month {debt_free}" if debt_free else "Not in Horizon", "Debt-Free"))
    chips.append((f"{on_track}/{len(goals)}", "Goals On Track"))
    chips.append((f"₹{profile['income_monthly']-profile['expenses_monthly']:,.0f}", "Monthly Surplus"))

    hero_metric_card(f"₹{final_nw:,.0f}", f"Projected Net Worth at Month {horizon}", chips)
    summary_block(summary)

    m_badge = ("✦ OPTIMISED · SLSQP", "pf-badge-green") if method == "optimised" else ("⚠ FALLBACK · WATERFALL", "pf-badge-amber")
    st.markdown(f'<span class="pf-badge {m_badge[1]}" style="font-size:0.75rem;">{m_badge[0]}</span>', unsafe_allow_html=True)
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 0.9])
    with col1:
        st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT}; margin:0 0 12px;">📊 Monthly Capital Allocation</h4>', unsafe_allow_html=True)
        allocation_stacked_bar(allocation)

        disposable = profile["income_monthly"] - profile["expenses_monthly"]
        table_rows = [
            ("Disposable Surplus", f"₹{disposable:,.0f}"),
            ("Emergency Reserve", f"₹{allocation['emergency_fund']:,.0f}"),
            ("Debt Reduction", f"₹{allocation['debt_payment']:,.0f}"),
            ("Savings", f"₹{allocation['savings']:,.0f}"),
            ("Market Investments", f"₹{allocation['investments']:,.0f}"),
        ]
        rows_html = "".join(f'<tr><td>{k}</td><td class="pf-table-val">{v}</td></tr>' for k, v in table_rows)
        st.markdown(f"""
        <table class="pf-table" style="margin-top:4px;">
            <thead><tr><th>Category</th><th>Amount / Month</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT}; margin:0 0 12px;">🥧 Allocation Breakdown</h4>', unsafe_allow_html=True)
        st.plotly_chart(allocation_donut_chart(allocation), use_container_width=True)

    st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT}; margin:24px 0 12px;">📈 Net Worth & Debt Trajectory</h4>', unsafe_allow_html=True)
    st.plotly_chart(combined_net_worth_chart(projections), use_container_width=True)

    if goals:
        st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT}; margin:24px 0 12px;">🎯 Goal Progress</h4>', unsafe_allow_html=True)
        goal_progress_cards(goals, allocation, horizon)

    recs = generate_recommendations(profile, allocation)
    if recs:
        st.markdown(f'<h4 style="font-size:1rem; font-weight:700; color:{TEXT}; margin:24px 0 8px;">💡 Recommendations</h4>', unsafe_allow_html=True)
        for rec in recs:
            st.markdown(f"""
            <div style="display:flex; align-items:flex-start; gap:10px; margin-bottom:8px;">
                <span style="color:{PURPLE}; font-size:1rem; margin-top:1px;">›</span>
                <span style="font-size:0.9rem; color:{TEXT_SEC};">{rec}</span>
            </div>
            """, unsafe_allow_html=True)


def page_footer():
    """Consistent footer across all pages."""
    st.markdown(f"""
    <div style="text-align:center; padding:48px 24px 32px; border-top:1px solid {BORDER_LIGHT}; margin-top:56px;">
        <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:12px;">
            <span class="pf-badge pf-badge-violet">Recurz Hackathon 2026</span>
            <span class="pf-badge pf-badge-teal">SLSQP Engine</span>
            <span class="pf-badge pf-badge-green">Groq AI Advisor</span>
        </div>
        <p style="font-size:0.8rem; color:{TEXT_MUTED} !important; margin:0;">
            🔒 All financial data is processed locally in-session. Nothing is stored or transmitted.
        </p>
    </div>
    """, unsafe_allow_html=True)


def generate_recommendations(profile: dict, allocation: dict) -> list:
    recs = []
    ef_target  = profile.get("emergency_fund_target", 0)
    ef_current = profile.get("emergency_fund_current", 0)
    if ef_current < ef_target:
        recs.append(f"Emergency fund is ₹{ef_target - ef_current:,.0f} below target — consider increasing reserves.")
    for d in profile.get("liabilities", []):
        if d["interest_rate"] > 0.15:
            recs.append(f"{d['name']} at {d['interest_rate']*100:.1f}% APR — avalanche payoff will save significant interest.")
    for g in profile.get("goals", []):
        monthly_needed = g["amount"] / max(g["deadline_months"], 1)
        goal_alloc     = allocation.get("goals", {}).get(g["name"], 0)
        if monthly_needed > 0 and goal_alloc < monthly_needed * 0.8:
            recs.append(f"'{g['name']}' needs ₹{monthly_needed:,.0f}/mo — currently ₹{goal_alloc:,.0f} allocated ({goal_alloc/monthly_needed*100:.0f}% funded).")
    if not recs:
        recs.append("Your allocation is well-optimised across all financial pillars.")
    return recs
