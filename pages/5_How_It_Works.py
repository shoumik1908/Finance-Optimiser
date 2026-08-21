"""
How It Works — Methodology explanation.
"""
import streamlit as st
from ui import inject_css, AMBER, TEXT, TEXT_DIM, BG, SURFACE, SLATE

st.set_page_config(page_title="How It Works — Finance Optimiser", page_icon="🧠", layout="wide")
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
        <a href="/Scenario_Lab" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_DIM}; text-decoration:none; padding:6px 14px; border-radius:6px;">Scenario Lab</a>
        <a href="/How_It_Works" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{AMBER}; text-decoration:none; padding:6px 14px; border-radius:6px; background:{SURFACE};">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<h2 style="color:{TEXT}; margin-bottom:24px;">🧠 How It Works</h2>', unsafe_allow_html=True)

# Objective
st.markdown(f"""
<div style="border:1px solid rgba(62,92,118,0.3); border-radius:8px; padding:24px; margin-bottom:24px;">
    <h3 style="color:{AMBER};">The Objective</h3>
    <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7;">
        This system doesn't simply maximise wealth. It optimises for <strong>long-term financial well-being</strong> —
        a composite score that balances emergency preparedness, debt reduction, investment growth, and goal completion.
        A plan that leaves you debt-free but with no emergency fund is not a good plan. A plan that maximises
        investments but misses your house downpayment deadline is not a good plan. The optimiser finds the allocation
        that scores highest across all dimensions simultaneously.
    </p>
</div>
""", unsafe_allow_html=True)

# Objective Function
st.markdown(f"""
<div style="border:1px solid rgba(62,92,118,0.3); border-radius:8px; padding:24px; margin-bottom:24px;">
    <h3 style="color:{AMBER};">The Objective Function</h3>
    <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7;">
        The well-being score is a weighted combination of:
    </p>
    <table style="width:100%; border-collapse:collapse; margin:12px 0;">
        <tr style="border-bottom:1px solid rgba(62,92,118,0.2);">
            <td style="padding:8px; color:{AMBER}; font-family:'JetBrains Mono',monospace;">20%</td>
            <td style="padding:8px; color:{TEXT};">Emergency fund progress — how fast you reach your safety net target</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(62,92,118,0.2);">
            <td style="padding:8px; color:{AMBER}; font-family:'JetBrains Mono',monospace;">25%</td>
            <td style="padding:8px; color:{TEXT};">Debt reduction rate — faster payoff of high-interest debt</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(62,92,118,0.2);">
            <td style="padding:8px; color:{AMBER}; font-family:'JetBrains Mono',monospace;">20%</td>
            <td style="padding:8px; color:{TEXT};">Investment growth — building long-term wealth</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(62,92,118,0.2);">
            <td style="padding:8px; color:{AMBER}; font-family:'JetBrains Mono',monospace;">25%</td>
            <td style="padding:8px; color:{TEXT};">Goal completion — meeting your financial targets before their deadlines</td>
        </tr>
        <tr>
            <td style="padding:8px; color:{SLATE}; font-family:'JetBrains Mono',monospace;">penalties</td>
            <td style="padding:8px; color:{TEXT};">Underfunded goals and low emergency reserves reduce the score</td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

# Constraints
st.markdown(f"""
<div style="border:1px solid rgba(62,92,118,0.3); border-radius:8px; padding:24px; margin-bottom:24px;">
    <h3 style="color:{AMBER};">Constraints</h3>
    <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7;">
        The solver respects hard constraints that mirror real financial rules:
    </p>
    <ul style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.8;">
        <li><strong>Budget constraint:</strong> total allocations cannot exceed disposable income</li>
        <li><strong>Minimum debt payments:</strong> every debt must receive at least its minimum payment</li>
        <li><strong>Non-negativity:</strong> no category can receive a negative allocation</li>
        <li><strong>Emergency fund cap:</strong> stops adding once the target is reached</li>
        <li><strong>Goal feasibility:</strong> goals with impossible deadlines are flagged</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Solver
st.markdown(f"""
<div style="border:1px solid rgba(62,92,118,0.3); border-radius:8px; padding:24px; margin-bottom:24px;">
    <h3 style="color:{AMBER};">The Solver</h3>
    <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7;">
        The optimisation uses <strong>scipy.optimize.minimize</strong> with the SLSQP method
        (Sequential Least Squares Programming). This is a gradient-based optimiser that handles
        inequality constraints natively. It's fast (under 1 second per solve) and produces
        deterministic results.
    </p>
    <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7; margin-top:12px;">
        If the solver fails to converge on an edge case, a <strong>rule-based fallback</strong> (waterfall method)
        produces a reasonable allocation: emergency fund first, then highest-interest debt, then goals,
        then split remaining between savings and investments based on risk tolerance.
    </p>
</div>
""", unsafe_allow_html=True)

# Dynamic Re-planning
st.markdown(f"""
<div style="border:1px solid rgba(62,92,118,0.3); border-radius:8px; padding:24px; margin-bottom:24px;">
    <h3 style="color:{AMBER};">Dynamic Re-planning</h3>
    <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7;">
        When a life event occurs (income change, new expense, rate change, new goal, emergency expense),
        the system doesn't just tweak the existing plan. It <strong>re-runs the entire optimiser</strong> from
        the current state with updated parameters. This means the new plan is globally optimal for the
        new conditions, not just a local adjustment.
    </p>
    <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7; margin-top:12px;">
        The Simulate page shows the original plan and the revised plan side by side, with the
        divergence point clearly marked on the net worth chart. This is the feature that directly
        addresses the problem statement's requirement: "adapts to changing financial conditions."
    </p>
</div>
""", unsafe_allow_html=True)

# Tech Stack
st.markdown(f"""
<div style="border:1px solid rgba(62,92,118,0.3); border-radius:8px; padding:24px; margin-bottom:24px;">
    <h3 style="color:{AMBER};">Tech Stack</h3>
    <table style="width:100%; border-collapse:collapse; margin:12px 0;">
        <tr style="border-bottom:1px solid rgba(62,92,118,0.2);">
            <td style="padding:8px; color:{AMBER}; font-family:'JetBrains Mono',monospace;">Python</td>
            <td style="padding:8px; color:{TEXT};">Core language</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(62,92,118,0.2);">
            <td style="padding:8px; color:{AMBER}; font-family:'JetBrains Mono',monospace;">Streamlit</td>
            <td style="padding:8px; color:{TEXT};">Multipage web dashboard</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(62,92,118,0.2);">
            <td style="padding:8px; color:{AMBER}; font-family:'JetBrains Mono',monospace;">SciPy</td>
            <td style="padding:8px; color:{TEXT};">SLSQP optimisation engine</td>
        </tr>
        <tr style="border-bottom:1px solid rgba(62,92,118,0.2);">
            <td style="padding:8px; color:{AMBER}; font-family:'JetBrains Mono',monospace;">Plotly</td>
            <td style="padding:8px; color:{TEXT};">Interactive charts</td>
        </tr>
        <tr>
            <td style="padding:8px; color:{AMBER}; font-family:'JetBrains Mono',monospace;">NumPy</td>
            <td style="padding:8px; color:{TEXT};">Numerical computation</td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align:center; padding:24px 0; border-top:1px solid rgba(62,92,118,0.2); margin-top:24px;">
    <p style="font-family:Inter,sans-serif; font-size:0.8rem; color:{TEXT_DIM};">
        Built for Recurz Hackathon 2026 · Fintech PS2 · Personal Finance Optimiser
    </p>
    <p style="font-family:Inter,sans-serif; font-size:0.75rem; color:{TEXT_DIM}; margin-top:8px;">
        🔒 All data is processed in-session and is not stored or transmitted to any third party.
    </p>
</div>
""", unsafe_allow_html=True)
