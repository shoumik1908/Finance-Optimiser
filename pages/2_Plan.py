"""
Plan — Results dashboard (White + Purple theme) with AI recommendations
"""
import streamlit as st
from engine import optimise_finances, project_finances, generate_summary
from ai_advisor import get_ai_recommendations, get_chat_response
from ui import inject_css, plan_report, PURPLE, PURPLE_BG, TEXT, TEXT_SEC, CARD

st.set_page_config(page_title="Your Plan — Finance Optimiser", page_icon="📊", layout="wide")
inject_css()

st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
section[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Nav
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid #E5E7EB; margin-bottom:24px;">
    <span style="font-family:'JetBrains Mono',monospace; font-size:1.1rem; color:{PURPLE}; font-weight:700;">💰 Finance Optimiser</span>
    <div style="display:flex; gap:8px;">
        <a href="/" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">Home</a>
        <a href="/Profile" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">Profile</a>
        <a href="/Plan" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{PURPLE}; text-decoration:none; padding:6px 14px; border-radius:8px; background:{PURPLE_BG};">Plan</a>
        <a href="/Simulate" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">Simulate</a>
        <a href="/Scenario_Lab" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">Scenario Lab</a>
        <a href="/How_It_Works" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

if "profile" not in st.session_state:
    st.markdown(f"""
    <div style="text-align:center; padding:80px 0;">
        <h2 style="color:{TEXT};">No plan yet</h2>
        <p style="color:{TEXT_SEC};">Build your financial profile first to generate a plan.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="/Profile" target="_self" style="display:block; text-align:center; padding:14px 28px; background:{PURPLE}; color:white; font-family:Inter,sans-serif; font-weight:700; border-radius:10px; text-decoration:none; max-width:300px; margin:0 auto;">Build Your Profile →</a>', unsafe_allow_html=True)
else:
    profile = st.session_state.profile
    allocation = st.session_state.allocation
    method = st.session_state.method
    projections = st.session_state.projections
    summary = st.session_state.summary

    st.markdown(f'<h2 style="color:{TEXT}; margin-bottom:4px;">Your Financial Plan</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{TEXT_SEC}; font-size:0.9rem; margin-bottom:24px;">Based on your profile • {profile["horizon_months"]}-month horizon • {profile["risk_tolerance"]} risk</p>', unsafe_allow_html=True)

    plan_report(profile, allocation, method, projections, summary)

    # AI Recommendations
    st.markdown("---")
    st.markdown(f'<h3 style="color:{PURPLE};">🤖 AI Financial Advisor</h3>', unsafe_allow_html=True)

    if "ai_recommendations" not in st.session_state:
        with st.spinner("AI is analyzing your financial profile..."):
            ai_recs = get_ai_recommendations(profile, allocation, projections, summary)
            st.session_state.ai_recommendations = ai_recs

    if st.session_state.get("ai_recommendations"):
        st.markdown(f"""
        <div style="border:1px solid {PURPLE}22; border-radius:12px; padding:20px; background:{PURPLE_BG}; margin:16px 0;">
            <p style="font-family:Inter,sans-serif; font-size:0.95rem; color:{TEXT}; line-height:1.7; white-space:pre-line;">{st.session_state.ai_recommendations}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("AI recommendations unavailable. The optimiser's built-in recommendations are shown above.")

    # Chat
    st.markdown("---")
    st.markdown(f'<h3 style="color:{TEXT};">💬 Ask the AI Advisor</h3>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div style="display:flex; justify-content:flex-end; margin:8px 0;"><div class="chat-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="display:flex; justify-content:flex-start; margin:8px 0;"><div class="chat-ai">{msg["content"]}</div></div>', unsafe_allow_html=True)

    user_input = st.chat_input("Ask about your financial plan...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = get_chat_response(user_input, profile, allocation)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
