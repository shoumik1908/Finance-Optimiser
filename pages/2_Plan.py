"""
Plan — Your financial plan dashboard (report style).
"""
import streamlit as st
from engine import optimise_finances, project_finances, generate_summary
from ui import inject_css, plan_report, AMBER, TEXT, TEXT_DIM, BG, SURFACE

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
<div style="display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid rgba(62,92,118,0.2); margin-bottom:24px;">
    <span style="font-family:'JetBrains Mono',monospace; font-size:1.1rem; color:{AMBER}; font-weight:700;">💰 Finance Optimiser</span>
    <div style="display:flex; gap:8px;">
        <a href="/" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Home</a>
        <a href="/Profile" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Profile</a>
        <a href="/Plan" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{AMBER}; text-decoration:none; padding:6px 14px; border-radius:6px; background:{SURFACE};">Plan</a>
        <a href="/Simulate" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Simulate</a>
        <a href="/Scenario_Lab" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Scenario Lab</a>
        <a href="/How_It_Works" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Check if profile exists
if "profile" not in st.session_state:
    st.markdown(f"""
    <div style="text-align:center; padding:80px 0;">
        <h2 style="color:{TEXT};">No plan yet</h2>
        <p style="color:{TEXT_DIM};">Build your financial profile first to generate a plan.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<a href="/Profile" target="_self" style="display:block; text-align:center; padding:14px 28px; background:{AMBER}; color:{BG}; font-family:Inter,sans-serif; font-weight:700; border-radius:8px; text-decoration:none; max-width:300px; margin:0 auto;">Build Your Profile →</a>', unsafe_allow_html=True)
else:
    profile = st.session_state.profile
    allocation = st.session_state.allocation
    method = st.session_state.method
    projections = st.session_state.projections
    summary = st.session_state.summary

    st.markdown(f'<h2 style="color:{TEXT}; margin-bottom:4px;">Your Financial Plan</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{TEXT_DIM}; font-size:0.9rem; margin-bottom:24px;">Based on your profile • {profile["horizon_months"]}-month horizon • {profile["risk_tolerance"]} risk</p>', unsafe_allow_html=True)

    plan_report(profile, allocation, method, projections, summary)
