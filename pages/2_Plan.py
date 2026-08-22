"""
Plan Dashboard — Financial plan report + Groq AI advisor (Violet/Navy design)
"""
import streamlit as st
from engine import optimise_finances, project_finances, generate_summary, PRESET_PROFILES
from ai_advisor import get_ai_recommendations, get_chat_response
from ui import (inject_css, top_nav, page_footer, plan_report,
                PURPLE, PURPLE_BG, PURPLE_SOFT, TEXT, TEXT_SEC, TEXT_MUTED,
                CARD, BG, BORDER_LIGHT, GREEN, AMBER, RED, TEAL, SHADOW_SM, SHADOW_MD, GRAD)

st.set_page_config(page_title="Your Plan — Finance Optimiser", page_icon="📊", layout="wide")
inject_css()

# ── Deferred redirects (before any rendering) ─────────────────────────
if st.session_state.pop("_plan_go_profile", False):
    st.switch_page("pages/1_Profile.py")

if st.session_state.pop("_plan_demo", False):
    p = PRESET_PROFILES["young_pro"]
    with st.spinner("Loading demo..."):
        a, m = optimise_finances(p, p["horizon_months"])
        j    = project_finances(p, a, p["horizon_months"])
        s    = generate_summary(p, a, j)
    st.session_state.update({"profile": p, "allocation": a, "method": m, "projections": j, "summary": s})
    st.session_state.pop("ai_recommendations", None)
    st.session_state.pop("chat_history", None)
    st.rerun()

top_nav("Plan")

# ── Empty State ────────────────────────────────────────────────────────
if "profile" not in st.session_state:
    st.markdown(f"""
    <div style="min-height:80vh; display:flex; align-items:center; justify-content:center;
                flex-direction:column; text-align:center; padding:48px;">
        <div style="width:80px; height:80px; border-radius:20px; background:{PURPLE_BG};
                    display:flex; align-items:center; justify-content:center;
                    font-size:2.4rem; margin-bottom:20px;">📊</div>
        <h2 style="color:{TEXT} !important; font-size:1.8rem; margin:0 0 10px;">No Plan Generated Yet</h2>
        <p style="color:{TEXT_MUTED} !important; font-size:0.95rem; max-width:420px; margin:0 0 28px; line-height:1.6;">
            Complete the 5-step profile wizard to generate your personalised, mathematically optimised financial plan.
        </p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button("✨ Build My Profile →", use_container_width=True, type="primary", key="plan_go_profile"):
            st.session_state["_plan_go_profile"] = True
            st.rerun()
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Quick Demo: Young Professional", use_container_width=True, key="plan_demo"):
            st.session_state["_plan_demo"] = True
            st.rerun()
    st.stop()

# ── Plan Data ──────────────────────────────────────────────────────────
profile    = st.session_state.profile
allocation = st.session_state.allocation
method     = st.session_state.method
projections = st.session_state.projections
summary    = st.session_state.summary

# ── Page Header ──────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg, #14141F 0%, #1E1E3A 100%);
            padding:36px 48px 40px; position:relative; overflow:hidden;">
    <div style="position:absolute; width:350px; height:350px; top:-120px; right:-60px;
                border-radius:50%; background:radial-gradient(circle, rgba(108,76,224,0.22) 0%, transparent 70%);
                pointer-events:none;"></div>
    <div style="position:relative; z-index:1; display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:16px;">
        <div>
            <h1 style="font-size:2rem; font-weight:800; color:#FFFFFF !important; margin:0 0 6px;
                       letter-spacing:-0.02em;">Your Optimal Capital Plan</h1>
            <p style="font-size:0.9rem; color:rgba(255,255,255,0.5) !important; margin:0;">
                {profile["horizon_months"]}-month horizon · {profile["risk_tolerance"].capitalize()} risk profile
                · ₹{profile["income_monthly"]:,.0f}/mo income
            </p>
        </div>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <span style="background:rgba(16,185,129,0.2); color:#6EE7B7; border:1px solid rgba(16,185,129,0.3);
                         border-radius:9999px; padding:5px 14px; font-size:0.75rem; font-weight:700;
                         letter-spacing:0.04em; text-transform:uppercase;">✦ SLSQP Optimised</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

# ── Plan Report ────────────────────────────────────────────────────────
plan_report(profile, allocation, method, projections, summary)

# ── Divider ───────────────────────────────────────────────────────────
st.markdown(f"""
<div style="border-top:1px solid {BORDER_LIGHT}; margin:40px 0 32px; padding-top:32px;">
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:6px;">
        <div style="width:40px; height:40px; border-radius:12px; background:{PURPLE_BG};
                    display:flex; align-items:center; justify-content:center; font-size:1.2rem;">🤖</div>
        <div>
            <p style="font-size:1.15rem; font-weight:700; color:{TEXT} !important; margin:0;">AI Financial Advisor</p>
            <p style="font-size:0.82rem; color:{TEXT_MUTED} !important; margin:0;">
                Contextual recommendations powered by Groq · LLaMA 3.3 70B
            </p>
        </div>
        <span class="pf-badge pf-badge-violet" style="margin-left:auto;">AI Insights</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── AI Recommendations ─────────────────────────────────────────────────
if "ai_recommendations" not in st.session_state:
    with st.spinner("Analysing your profile with AI..."):
        recs = get_ai_recommendations(profile, allocation, projections, summary)
        st.session_state.ai_recommendations = recs

if st.session_state.get("ai_recommendations"):
    st.markdown(f"""
    <div style="background:{PURPLE_SOFT}; border:1px solid rgba(108,76,224,0.18);
                border-left:4px solid {PURPLE}; border-radius:14px; padding:20px 24px; margin-bottom:24px;">
        <p style="font-family:'Plus Jakarta Sans',sans-serif; font-size:0.92rem; color:{TEXT_SEC} !important;
                  line-height:1.75; white-space:pre-line; margin:0;">{st.session_state.ai_recommendations}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f'<div class="pf-info-box">AI recommendations unavailable. Built-in recommendations are shown in the plan above.</div>', unsafe_allow_html=True)

# ── Chat Interface ─────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{CARD}; border:1px solid {BORDER_LIGHT}; border-radius:16px;
            padding:24px; box-shadow:{SHADOW_SM}; margin-top:8px;">
    <p style="font-size:1rem; font-weight:700; color:{TEXT} !important; margin:0 0 4px;">
        💬 Ask the AI Advisor
    </p>
    <p style="font-size:0.82rem; color:{TEXT_MUTED} !important; margin:0 0 18px;">
        Ask about payoff strategies, investment options, goal feasibility, or tax-saving approaches.
    </p>
""", unsafe_allow_html=True)

# Quick prompts
st.markdown(f'<p style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:{TEXT_MUTED}; margin-bottom:10px;">Quick prompts:</p>', unsafe_allow_html=True)
qp1, qp2, qp3 = st.columns(3, gap="small")
prompt_to_send = None
if qp1.button("⚡ Reach goals 6 months faster", use_container_width=True):
    prompt_to_send = "How can I reach my financial goals 6 months faster?"
if qp2.button("💳 Debt vs invest trade-off", use_container_width=True):
    prompt_to_send = "Should I aggressively pay off debt or invest more? What's the optimal balance?"
if qp3.button("🛡️ Is my emergency buffer safe?", use_container_width=True):
    prompt_to_send = "Is my current emergency reserve sufficient for economic downturns or job loss?"

st.markdown("</div>", unsafe_allow_html=True)

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; margin:12px 0;">
            <div class="pf-chat-user">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start; margin:12px 0;">
            <div class="pf-chat-ai">
                <div class="pf-chat-ai-header">🤖 AI Advisor</div>
                {msg["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

user_input   = st.chat_input("Ask about your financial plan...")
active_prompt = prompt_to_send or user_input

if active_prompt:
    st.session_state.chat_history.append({"role": "user", "content": active_prompt})
    with st.spinner("Thinking..."):
        response = get_chat_response(active_prompt, profile, allocation)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.rerun()

if st.session_state.chat_history:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

page_footer()
