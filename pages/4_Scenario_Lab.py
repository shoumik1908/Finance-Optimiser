"""
Scenario Lab — Paste a JSON profile and test the optimiser.
"""
import streamlit as st
import json
from engine import optimise_finances, project_finances, generate_summary, DEFAULT_PROFILE
from ui import inject_css, plan_report, AMBER, TEXT, TEXT_DIM, BG, SURFACE

st.set_page_config(page_title="Scenario Lab — Finance Optimiser", page_icon="🧪", layout="wide")
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
        <a href="/Plan" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Plan</a>
        <a href="/Simulate" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Simulate</a>
        <a href="/Scenario_Lab" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{AMBER}; text-decoration:none; padding:6px 14px; border-radius:6px; background:{SURFACE};">Scenario Lab</a>
        <a href="/How_It_Works" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<h2 style="color:{TEXT}; margin-bottom:4px;">🧪 Scenario Lab</h2>', unsafe_allow_html=True)
st.markdown(f'<p style="color:{TEXT_DIM}; font-size:0.9rem; margin-bottom:24px;">Paste a JSON financial profile and test the optimiser. The unseen scenario test harness.</p>', unsafe_allow_html=True)

# Sample JSON
sample_json = json.dumps(DEFAULT_PROFILE, indent=2)

json_input = st.text_area("Paste JSON profile:", value=sample_json, height=300)

if st.button("🧪 Run Scenario", type="primary", use_container_width=True):
    try:
        test_profile = json.loads(json_input)

        # Input validation
        test_profile["income_monthly"] = max(0, min(test_profile.get("income_monthly", 0), 10000000))
        test_profile["expenses_monthly"] = max(0, min(test_profile.get("expenses_monthly", 0), 10000000))
        test_profile["horizon_months"] = max(1, min(test_profile.get("horizon_months", 60), 120))
        for d in test_profile.get("liabilities", []):
            d["balance"] = max(0, min(d.get("balance", 0), 10000000))
            d["interest_rate"] = max(0, min(d.get("interest_rate", 0), 1.0))
            d["min_payment"] = max(0, min(d.get("min_payment", 0), 1000000))
        for g in test_profile.get("goals", []):
            g["amount"] = max(0, min(g.get("amount", 0), 100000000))
            g["deadline_months"] = max(1, min(g.get("deadline_months", 12), 120))

        test_alloc, test_method = optimise_finances(test_profile, test_profile.get("horizon_months", 60))
        test_proj = project_finances(test_profile, test_alloc, test_profile.get("horizon_months", 60))
        test_summary = generate_summary(test_profile, test_alloc, test_proj)

        st.markdown("---")
        st.markdown(f'<h3 style="color:{TEXT};">Scenario Results</h3>', unsafe_allow_html=True)

        plan_report(test_profile, test_alloc, test_method, test_proj, test_summary)

    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please check your input.")
    except Exception:
        st.error("Something went wrong. Please check your inputs and try again.")
