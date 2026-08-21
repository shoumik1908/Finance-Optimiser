"""
How It Works — Methodology (White + Purple theme)
"""
import streamlit as st
from ui import inject_css, PURPLE, PURPLE_BG, TEXT, TEXT_SEC, TEAL

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
<div style="display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid #E5E7EB; margin-bottom:24px;">
    <span style="font-family:'JetBrains Mono',monospace; font-size:1.1rem; color:{PURPLE}; font-weight:700;">💰 Finance Optimiser</span>
    <div style="display:flex; gap:8px;">
        <a href="/" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">Home</a>
        <a href="/Profile" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">Profile</a>
        <a href="/Plan" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">Plan</a>
        <a href="/Simulate" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">Simulate</a>
        <a href="/Scenario_Lab" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{TEXT_SEC}; text-decoration:none; padding:6px 14px; border-radius:8px;">Scenario Lab</a>
        <a href="/How_It_Works" target="_self" style="font-family:Inter,sans-serif; font-size:0.85rem; color:{PURPLE}; text-decoration:none; padding:6px 14px; border-radius:8px; background:{PURPLE_BG};">How It Works</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<h2 style="color:{TEXT}; margin-bottom:24px;">🧠 How It Works</h2>', unsafe_allow_html=True)

sections = [
    ("The Objective", f"""
        <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7;">
            This system doesn't simply maximise wealth. It optimises for <strong>long-term financial well-being</strong> —
            a composite score that balances emergency preparedness, debt reduction, investment growth, and goal completion.
            A plan that leaves you debt-free but with no emergency fund is not a good plan. The optimiser finds the allocation
            that scores highest across all dimensions simultaneously.
        </p>
    """),
    ("The Objective Function", f"""
        <table style="width:100%; border-collapse:collapse; margin:12px 0;">
            <tr style="border-bottom:1px solid #E5E7EB;">
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">20%</td>
                <td style="padding:8px; color:{TEXT};">Emergency fund progress — how fast you reach your safety net target</td>
            </tr>
            <tr style="border-bottom:1px solid #E5E7EB;">
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">25%</td>
                <td style="padding:8px; color:{TEXT};">Debt reduction rate — faster payoff of high-interest debt</td>
            </tr>
            <tr style="border-bottom:1px solid #E5E7EB;">
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">20%</td>
                <td style="padding:8px; color:{TEXT};">Investment growth — building long-term wealth</td>
            </tr>
            <tr style="border-bottom:1px solid #E5E7EB;">
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">25%</td>
                <td style="padding:8px; color:{TEXT};">Goal completion — meeting your financial targets before their deadlines</td>
            </tr>
            <tr>
                <td style="padding:8px; color:{TEAL}; font-family:'JetBrains Mono',monospace; font-weight:700;">penalty</td>
                <td style="padding:8px; color:{TEXT};">Underfunded goals and low emergency reserves reduce the score</td>
            </tr>
        </table>
    """),
    ("Constraints", f"""
        <ul style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.8;">
            <li><strong>Budget constraint:</strong> total allocations cannot exceed disposable income</li>
            <li><strong>Minimum debt payments:</strong> every debt must receive at least its minimum payment</li>
            <li><strong>Non-negativity:</strong> no category can receive a negative allocation</li>
            <li><strong>Emergency fund cap:</strong> stops adding once the target is reached</li>
            <li><strong>Goal feasibility:</strong> goals with impossible deadlines are flagged</li>
        </ul>
    """),
    ("The Solver", f"""
        <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7;">
            The optimisation uses <strong>scipy.optimize.minimize</strong> with the SLSQP method
            (Sequential Least Squares Programming). Fast (under 1 second) and deterministic.
            If the solver fails, a <strong>rule-based fallback</strong> (waterfall method) produces a reasonable allocation.
        </p>
    """),
    ("Dynamic Re-planning", f"""
        <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7;">
            When a life event occurs, the system <strong>re-runs the entire optimiser</strong> from the current state with updated parameters.
            The new plan is globally optimal for the new conditions, not just a local adjustment.
            The Simulate page shows original vs revised plan side by side.
        </p>
    """),
    ("AI Advisor", f"""
        <p style="color:{TEXT}; font-family:Inter,sans-serif; line-height:1.7;">
            Powered by <strong>Groq (Llama 3.3 70B)</strong>, the AI advisor analyzes your financial profile and allocation
            to give personalized recommendations. You can also chat with the AI to ask questions about your plan.
        </p>
    """),
    ("Tech Stack", f"""
        <table style="width:100%; border-collapse:collapse; margin:12px 0;">
            <tr style="border-bottom:1px solid #E5E7EB;">
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">Python</td>
                <td style="padding:8px; color:{TEXT};">Core language</td>
            </tr>
            <tr style="border-bottom:1px solid #E5E7EB;">
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">Streamlit</td>
                <td style="padding:8px; color:{TEXT};">Multipage web dashboard</td>
            </tr>
            <tr style="border-bottom:1px solid #E5E7EB;">
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">SciPy</td>
                <td style="padding:8px; color:{TEXT};">SLSQP optimisation engine</td>
            </tr>
            <tr style="border-bottom:1px solid #E5E7EB;">
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">Plotly</td>
                <td style="padding:8px; color:{TEXT};">Interactive charts</td>
            </tr>
            <tr style="border-bottom:1px solid #E5E7EB;">
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">Groq</td>
                <td style="padding:8px; color:{TEXT};">AI-powered financial advisor</td>
            </tr>
            <tr>
                <td style="padding:8px; color:{PURPLE}; font-family:'JetBrains Mono',monospace; font-weight:700;">NumPy</td>
                <td style="padding:8px; color:{TEXT};">Numerical computation</td>
            </tr>
        </table>
    """),
]

for title, content in sections:
    st.markdown(f"""
    <div style="background:white; border:1px solid #E5E7EB; border-radius:12px; padding:24px; margin-bottom:16px; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
        <h3 style="color:{PURPLE}; margin-top:0;">{title}</h3>
        {content}
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align:center; padding:24px 0; border-top:1px solid #E5E7EB; margin-top:24px;">
    <p style="font-family:Inter,sans-serif; font-size:0.8rem; color:{TEXT_SEC};">
        Built for Recurz Hackathon 2026 · Fintech PS2 · Personal Finance Optimiser
    </p>
    <p style="font-family:Inter,sans-serif; font-size:0.75rem; color:{TEXT_SEC}; margin-top:8px;">
        🔒 All data is processed in-session and is not stored or transmitted to any third party.
    </p>
</div>
""", unsafe_allow_html=True)
