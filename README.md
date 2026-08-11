# 🍬 Nassau Candy Distributor: Profitability & Supply Chain Analytics

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.61-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-6.9.0-3F4F75.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end data analytics, financial diagnostics, and interactive decision-support application built for **Nassau Candy Distributor**. This platform transforms raw sales and order transaction data into actionable operational intelligence for executive leadership, regional supply chain managers, and commercial trade stakeholders.

---

## 🌟 Key Features & Modules

- **🏠 Executive Overview & Network Map**: High-level KPIs (*Revenue, Gross Profit, Gross Margin %, Units, Profit/Unit*) and an interactive geospatial supply chain map connecting manufacturing plants (*Casa Grande AZ, Savannah GA, Moline IL, Memphis TN, Thief River Falls MN*) to regional customer states.
- **🍬 Product Profitability & 4-Quadrant Portfolio Matrix**: Strategic matrix classifying products into *Stars*, *Volume Drivers*, *Niche Drivers*, and *Laggards*.
- **🏢 Division Performance Dashboard**: Financial efficiency analysis comparing revenue share vs profit contribution and evaluating structural margin distribution.
- **⚠️ Cost & Margin Action Diagnostics**: Automated rules engine identifying SKU-level margin risk (*Reprice Immediately*, *Renegotiate Cost*, *Discontinuation Review*) paired with an **Interactive Repricing Simulator**.
- **📊 Pareto (80/20) Concentration Analysis**: Dual cumulative concentration curves identifying portfolio over-dependency.
- **🚚 Factory & Route Efficiency**: Production throughput benchmarks, shipping mode distribution, and turnaround time diagnostics.

---

## 📊 Key Analytical Findings

1. **Chocolate Division Dominance**: Delivers **93.4% of total revenue** (\$131,692.90) and **95.0% of total profit** (\$88,824.62) with a strong **67.4% gross margin**.
2. **Sugar Division Structural Deficit**: Operates at an **18.2% gross margin** with manufacturing costs consuming **81.8% of top-line sales**.
3. **80/20 Concentration**: Just **2 product lines** (*Wonka Bar Nutty Crunch* and *Wonka Bar Triple Dazzle Caramel*) account for **84.6% of total corporate profit**.
4. **Margin Risk SKU**: *Everlasting Gobstopper* operates at an **11.9% gross margin**. A 25% price adjustment expands margin to **29.5%**.

---

## 📁 Repository Structure

```
nassau_candy_analytics/
├── data/
│   └── nassau_candy_data.csv        # Primary sales & shipping dataset
├── src/
│   ├── data_loader.py               # Data ingestion, cleaning, factory GPS mapping
│   ├── analytics.py                 # Financial metrics, Pareto 80/20, diagnostic rules
│   └── components.py                # CSS dark glassmorphism theme & Plotly charts
├── app.py                           # Main Streamlit web application
├── research_paper.md                # Comprehensive academic EDA & financial paper
├── executive_summary.md             # Policy & C-Suite briefing document
├── requirements.txt                 # Python dependency manifest
└── README.md                        # Project documentation
```

---

## 🛠️ Quick Start & Local Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Installation
```bash
# Clone repository
git clone https://github.com/your-username/nassau-candy-analytics.git
cd nassau-candy-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch Streamlit Web Dashboard
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 📄 Documentation Deliverables

- **Research Paper**: See [`research_paper.md`](research_paper.md) for full methodology, EDA, and diagnostic models.
- **Executive Summary**: See [`executive_summary.md`](executive_summary.md) for C-Suite & government stakeholder policy recommendations.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
