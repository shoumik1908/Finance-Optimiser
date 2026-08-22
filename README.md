# 💰 Personal Finance Optimiser

> **Recurz Hackathon 2026 — Fintech PS2**  
> Optimise your money across savings, investments, debt repayment, emergency fund, and financial goals — powered by mathematical optimisation + AI.

**🔗 Live:** [finance-optimiser.onrender.com](https://finance-optimiser.onrender.com)

---

## 🎯 Problem Statement

Personal financial planning requires balancing savings, investments, debt repayment, emergency reserves, and long-term financial goals. Optimising one decision can affect another, making it difficult to determine the best overall financial strategy.

## 💡 Our Solution

A **full-stack financial optimisation engine** that:

- Takes your complete financial profile as input
- Generates an **optimal monthly allocation** across 5 dimensions using **SciPy SLSQP constrained optimisation**
- Provides **AI-powered financial advice** via Llama 3.3 70B (Groq API)
- Computes a **Well-being Score (0-100)** across debt ratio, savings rate, investment diversification, and goal progress
- Lets you **simulate life events** (job loss, salary hike, new EMI) and see real-time plan adaptation
- Projects your **wealth trajectory over 5 years** with compound growth modelling

### Key Features

| Feature | Description |
|---------|-------------|
| 🧮 5-Dimension Optimisation | SLSQP solver allocates across Emergency Fund, Debt Repayment, SIP Investments, Goal Savings, Discretionary |
| 🤖 AI Financial Advisor | Llama 3.3 70B via Groq — ask anything about your finances in plain English |
| 📊 Well-being Score | Composite 0-100 score tracking your overall financial health |
| 🔄 Scenario Lab | Simulate job loss, salary hike, new loan, medical emergency |
| 📈 5-Year Projection | Compound growth modelling with market return assumptions |
| 🎯 Interactive Dashboard | Plotly charts: pie, bar, gauge, timeline, trajectory |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit (6-page multipage app) |
| Optimisation | SciPy SLSQP (Sequential Least Squares Programming) |
| AI Engine | Llama 3.3 70B via Groq API |
| Charts | Plotly (interactive, responsive) |
| Deployment | Render (free tier) |
| Language | Python 3.11 |

---

## 🚀 How to Run

```bash
git clone https://github.com/shoumik1908/Finance-Optimiser.git
cd Finance-Optimiser
pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Environment Variables (for AI advisor)
```bash
export GROQ_API_KEY="your_groq_api_key"
```

---

## 📁 Project Structure

```
Finance-Optimiser/
├── app.py                  # Main entry point, routing, theme
├── ui.py                   # Shared UI components, CSS, styling
├── engine.py               # SLSQP optimisation engine
├── ai_advisor.py           # Groq/Llama AI financial advisor
├── keep_alive.py           # Render keep-alive cron
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── pages/
│   ├── 1_Profile.py        # Financial profile builder
│   ├── 2_Plan.py           # Optimised allocation plan
│   ├── 3_Simulate.py       # What-if scenario simulator
│   ├── 4_Scenario_Lab.py   # Advanced scenario testing
│   └── 5_How_It_Works.py   # Algorithm explanation
└── screenshots/            # Dashboard screenshots
```

---

## 🧠 Algorithm

### Optimisation Formulation

**Maximise:** `W(x) = w₁·debt_ratio + w₂·savings_rate + w₃·investment_div + w₄·goal_progress + w₅·liquidity`

**Subject to:**
- `Σ xᵢ = income` (budget constraint)
- `xᵢ ≥ minᵢ` (minimum commitments)
- `x_debt ≥ min_payment` (EMI obligations)
- `emergency ≥ 3 months expenses`

Solved using SciPy's SLSQP (Sequential Least Squares Programming) — a gradient-based constrained optimiser that handles equality and inequality constraints natively.

---

## 👥 Team Details

- **Team Leader:** Khwaab — Manipal University Jaipur
- **Domain:** Fintech
- **Problem Statement:** PS2 — Personal Finance Optimiser
- **Hackathon:** Recurz 2026

---

## 📄 License

This project was built for Recurz Hackathon 2026, Manipal University Jaipur.

---

**Built with ❤️ at Recurz 2026**
