"""
Personal Finance Optimiser — Home / Landing Page
"""
import streamlit as st
from ui import inject_css, AMBER, TEXT, TEXT_DIM, BG, SURFACE

st.set_page_config(page_title="Personal Finance Optimiser", page_icon="💰", layout="wide")
inject_css()

# Hide Streamlit's default multipage nav
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
section[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Custom top nav
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid rgba(62,92,118,0.2); margin-bottom:32px;">
    <span style="font-family:'JetBrains Mono',monospace; font-size:1.1rem; color:{AMBER}; font-weight:700;">💰 Finance Optimiser</span>
    <div style="display:flex; gap:8px;">
        <a href="/" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{AMBER}; text-decoration:none; padding:6px 14px; border-radius:6px; background:{SURFACE};">Home</a>
        <a href="/Profile" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Profile</a>
        <a href="/Plan" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Plan</a>
        <a href="/Simulate" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Simulate</a>
        <a href="/Scenario_Lab" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Scenario Lab</a>
        <a href="/How_It_Works" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero section
st.markdown(f"""
<div style="text-align:center; padding:60px 0 40px;">
    <h1 style="font-family:'JetBrains Mono',monospace; font-size:3rem; color:{AMBER}; margin-bottom:16px;">💰 Personal Finance Optimiser</h1>
    <p style="font-family:Inter,sans-serif; font-size:1.25rem; color:{TEXT}; max-width:600px; margin:0 auto 12px;">
        Optimise your money across savings, investments, debt, and goals — and see your plan adapt when life changes.
    </p>
    <p style="font-family:Inter,sans-serif; font-size:0.9rem; color:{TEXT_DIM}; max-width:500px; margin:0 auto 40px;">
        Built for Recurz Hackathon 2026 · Fintech PS2 · Mathematical Optimisation
    </p>
</div>
""", unsafe_allow_html=True)

# CTA
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown(f"""
    <a href="/Profile" target="_self" style="display:block; text-align:center; padding:16px 32px; background:{AMBER}; color:{BG}; font-family:Inter,sans-serif; font-weight:700; font-size:1.1rem; border-radius:8px; text-decoration:none; margin-bottom:12px;">
        Build Your Plan →
    </a>
    """, unsafe_allow_html=True)

st.markdown("")
st.markdown("")

# Features
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div style="border:1px solid rgba(62,92,118,0.3); border-radius:8px; padding:24px; text-align:center;">
        <div style="font-size:2rem; margin-bottom:8px;">🧮</div>
        <h3 style="color:{TEXT}; font-size:1rem;">Mathematical Optimisation</h3>
        <p style="color:{TEXT_DIM}; font-size:0.85rem;">LP/QP solver maximises financial well-being, not just wealth.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="border:1px solid rgba(62,92,118,0.3); border-radius:8px; padding:24px; text-align:center;">
        <div style="font-size:2rem; margin-bottom:8px;">🔄</div>
        <h3 style="color:{TEXT}; font-size:1rem;">Dynamic Re-planning</h3>
        <p style="color:{TEXT_DIM}; font-size:0.85rem;">Simulate life events and watch your plan adapt in real time.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="border:1px solid rgba(62,92,118,0.3); border-radius:8px; padding:24px; text-align:center;">
        <div style="font-size:2rem; margin-bottom:8px;">📊</div>
        <h3 style="color:{TEXT}; font-size:1rem;">Clear Projections</h3>
        <p style="color:{TEXT_DIM}; font-size:0.85rem;">Net worth, debt payoff, goal progress — visualised honestly.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align:center; padding:40px 0 20px; border-top:1px solid rgba(62,92,118,0.2); margin-top:40px;">
    <p style="font-family:Inter,sans-serif; font-size:0.8rem; color:{TEXT_DIM};">
        🔒 All data is processed in-session and is not stored or transmitted to any third party.
    </p>
</div>
""", unsafe_allow_html=True)
