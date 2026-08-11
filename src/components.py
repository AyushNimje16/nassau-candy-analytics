import streamlit as st
import plotly.express as px
import plotly.graph_objects as gg

# Modern Design System & CSS Injector
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Main Container Glassmorphism */
    .stApp {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 50%, #0F172A 100%);
        color: #F3F4F6;
    }

    /* Metric Cards Styling */
    .kpi-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 30px -5px rgba(124, 58, 237, 0.25);
        border-color: rgba(124, 58, 237, 0.4);
    }
    .kpi-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9CA3AF;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 700;
        background: linear-gradient(135deg, #F9FAFB 0%, #D1D5DB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-sub {
        font-size: 0.8rem;
        margin-top: 4px;
        font-weight: 500;
    }
    .text-positive { color: #10B981; }
    .text-negative { color: #EF4444; }
    .text-warning { color: #F59E0B; }
    .text-neutral { color: #3B82F6; }

    /* Custom Headers */
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #F9FAFB;
        margin-top: 15px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-title::before {
        content: '';
        display: inline-block;
        width: 4px;
        height: 22px;
        background: linear-gradient(180deg, #7C3AED 0%, #06B6D4 100%);
        border-radius: 4px;
    }

    /* Streamlit Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Badge Tags */
    .tag-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-reprice { background: rgba(239, 68, 68, 0.2); color: #FCA5A5; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-cost { background: rgba(245, 158, 11, 0.2); color: #FDE047; border: 1px solid rgba(245, 158, 11, 0.4); }
    .badge-discontinue { background: rgba(236, 72, 153, 0.2); color: #F472B6; border: 1px solid rgba(236, 72, 153, 0.4); }
    .badge-healthy { background: rgba(16, 185, 129, 0.2); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.4); }
    </style>
    """, unsafe_allow_html=True)


def render_kpi_card(title, value, subtext="", status="neutral"):
    status_class = f"text-{status}"
    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        {f'<div class="kpi-sub {status_class}">{subtext}</div>' if subtext else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def create_plotly_theme():
    return {
        "layout": {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"family": "Outfit, sans-serif", "color": "#E5E7EB"},
            "xaxis": {
                "gridcolor": "rgba(255,255,255,0.06)",
                "zerolinecolor": "rgba(255,255,255,0.1)",
                "tickfont": {"color": "#9CA3AF"}
            },
            "yaxis": {
                "gridcolor": "rgba(255,255,255,0.06)",
                "zerolinecolor": "rgba(255,255,255,0.1)",
                "tickfont": {"color": "#9CA3AF"}
            },
            "legend": {"font": {"color": "#E5E7EB"}},
            "hoverlabel": {
                "bgcolor": "#1E293B",
                "font": {"family": "Outfit, sans-serif", "color": "#F9FAFB", "size": 13}
            }
        }
    }


def format_currency(val):
    if abs(val) >= 1e6:
        return f"${val/1e6:.2f}M"
    elif abs(val) >= 1e3:
        return f"${val/1e3:.1f}K"
    else:
        return f"${val:.2f}"
