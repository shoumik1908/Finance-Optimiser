"""
Personal Finance Optimiser — Home Page (White + Purple)
"""
import streamlit as st
from ui import inject_css, PURPLE, PURPLE_BG, TEXT, TEXT_SEC, CARD

st.set_page_config(page_title="Personal Finance Optimiser", page_icon="💰", layout="wide")
inject_css()

st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
section[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Nav — compact, no overflow
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; padding:16px 24px; border-bottom:1px solid #E5E7EB; background:{CARD}; margin:-1rem -1rem 32px -1rem; padding:16px 48px; position:sticky; top:0; z-index:999;">
    <span style="font-family:'JetBrains Mono',monospace; font-size:1.1rem; color:{PURPLE}; font-weight:700;">💰 Finance Optimiser</span>
    <div style="display:flex; gap:4px; flex-wrap:wrap;">
        <a href="/" target="_self" style="font-family:Inter,sans-serif; font-size:0.8rem; color:white; text-decoration:none; padding:6px 12px; border-radius:6px; background:{PURPLE}; font-weight:600;">Home</a>
        <a href="/Profile" target="_self" style="font-family:Inter,sans-serif; font-size:0.8rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 12px; border-radius:6px;">Profile</a>
        <a href="/Plan" target="_self" style="font-family:Inter,sans-serif; font-size:0.8rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 12px; border-radius:6px;">Plan</a>
        <a href="/Simulate" target="_self" style="font-family:Inter,sans-serif; font-size:0.8rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 12px; border-radius:6px;">Simulate</a>
        <a href="/Scenario_Lab" target="_self" style="font-family:Inter,sans-serif; font-size:0.8rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 12px; border-radius:6px;">Lab</a>
        <a href="/How_It_Works" target="_self" style="font-family:Inter,sans-serif; font-size:0.8rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 12px; border-radius:6px;">About</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown(f"""
<div style="text-align:center; padding:20px 0 20px;">
    <h1 style="font-family:'JetBrains Mono',monospace; font-size:2.8rem; color:{PURPLE}; margin-bottom:12px;">💰 Personal Finance Optimiser</h1>
    <p style="font-family:Inter,sans-serif; font-size:1.15rem; color:{TEXT}; max-width:600px; margin:0 auto 8px; line-height:1.5;">
        Optimise your money across savings, investments, debt, and goals — and see your plan adapt when life changes.
    </p>
    <p style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; max-width:500px; margin:0 auto 32px;">
        Built for Recurz Hackathon 2026 · Fintech PS2 · Mathematical Optimisation
    </p>
</div>
""", unsafe_allow_html=True)

# CTA
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown(f"""
    <a href="/Profile" target="_self" style="display:block; text-align:center; padding:14px 28px; background:{PURPLE}; color:white; font-family:Inter,sans-serif; font-weight:700; font-size:1.05rem; border-radius:10px; text-decoration:none; box-shadow:0 2px 8px rgba(108,76,224,0.3);">
        Build Your Plan →
    </a>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Features
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid #E5E7EB; border-radius:12px; padding:24px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
        <div style="font-size:2rem; margin-bottom:8px;">🧮</div>
        <h3 style="color:{TEXT}; font-size:1rem; font-family:Inter,sans-serif;">Mathematical Optimisation</h3>
        <p style="color:{TEXT_SEC}; font-size:0.85rem; font-family:Inter,sans-serif;">LP/QP solver maximises financial well-being, not just wealth.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid #E5E7EB; border-radius:12px; padding:24px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
        <div style="font-size:2rem; margin-bottom:8px;">🔄</div>
        <h3 style="color:{TEXT}; font-size:1rem; font-family:Inter,sans-serif;">Dynamic Re-planning</h3>
        <p style="color:{TEXT_SEC}; font-size:0.85rem; font-family:Inter,sans-serif;">Simulate life events and watch your plan adapt in real time.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background:{CARD}; border:1px solid #E5E7EB; border-radius:12px; padding:24px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
        <div style="font-size:2rem; margin-bottom:8px;">📊</div>
        <h3 style="color:{TEXT}; font-size:1rem; font-family:Inter,sans-serif;">AI-Powered Insights</h3>
        <p style="color:{TEXT_SEC}; font-size:0.85rem; font-family:Inter,sans-serif;">Groq AI analyzes your profile and gives personalised advice.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align:center; padding:40px 0 20px; border-top:1px solid #E5E7EB; margin-top:40px;">
    <p style="font-family:Inter,sans-serif; font-size:0.8rem; color:{TEXT_SEC};">
        🔒 All data is processed in-session and is not stored or transmitted to any third party.
    </p>
</div>
""", unsafe_allow_html=True)
