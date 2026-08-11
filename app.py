import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_raw_data, FACTORIES_INFO
from src.analytics import (
    calculate_product_metrics,
    calculate_division_metrics,
    calculate_pareto_analysis,
    calculate_factory_logistics,
)
from src.components import (
    inject_custom_css,
    render_kpi_card,
    create_plotly_theme,
    format_currency,
)

# Page Setup
st.set_page_config(
    page_title="Nassau Candy | Profitability & Supply Chain Analytics",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Modern CSS Styling
inject_custom_css()

# Load Data
@st.cache_data
def get_dataset():
    return load_raw_data()

raw_df = get_dataset()

# Sidebar Controls
st.sidebar.markdown("<h2 style='color:#7C3AED; font-weight:700;'>🍬 Nassau Candy</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#9CA3AF; font-size:0.85rem;'>Profitability & Logistics Intelligence</p>", unsafe_allow_html=True)
st.sidebar.divider()

# 1. Date Filter
min_date = raw_df["Order Date"].min().date() if "Order Date" in raw_df.columns and not raw_df["Order Date"].isna().all() else None
max_date = raw_df["Order Date"].max().date() if "Order Date" in raw_df.columns and not raw_df["Order Date"].isna().all() else None

if min_date and max_date:
    date_range = st.sidebar.date_input(
        "📅 Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    date_range = None

# 2. Division Filter
divisions = ["All"] + sorted(list(raw_df["Division"].unique()))
selected_division = st.sidebar.selectbox("🏢 Product Division", divisions)

# 3. Region Filter
regions = ["All"] + sorted(list(raw_df["Region"].unique()))
selected_region = st.sidebar.selectbox("🌍 Geographic Region", regions)

# 4. Margin Threshold Slider
margin_threshold = st.sidebar.slider(
    "📊 Gross Margin Filter (%)",
    min_value=0,
    max_value=100,
    value=(0, 100),
    step=5
)

# 5. Product Search
search_query = st.sidebar.text_input("🔍 Product Search", "")

# Apply Filters
df = raw_df.copy()

if date_range and len(date_range) == 2:
    start_d, end_d = date_range
    df = df[(df["Order Date"].dt.date >= start_d) & (df["Order Date"].dt.date <= end_d)]

if selected_division != "All":
    df = df[df["Division"] == selected_division]

if selected_region != "All":
    df = df[df["Region"] == selected_region]

df = df[(df["Gross Margin (%)"] >= margin_threshold[0]) & (df["Gross Margin (%)"] <= margin_threshold[1])]

if search_query:
    df = df[df["Product Name"].str.contains(search_query, case=False, na=False)]

st.sidebar.divider()
st.sidebar.caption(f"Filtered Orders: **{len(df):,}** / {len(raw_df):,}")

# Navigation Tabs
tabs = st.tabs([
    "🏠 Executive Overview",
    "🍬 Product Profitability",
    "🏢 Division Performance",
    "⚠️ Cost & Margin Diagnostics",
    "📊 Pareto (80/20) Analysis",
    "🚚 Factory & Route Efficiency"
])

# Plotly Theme Setup
plotly_theme = create_plotly_theme()

# ==========================================
# TAB 1: EXECUTIVE OVERVIEW
# ==========================================
with tabs[0]:
    st.markdown("<div class='section-title'>Executive Profitability Summary</div>", unsafe_allow_html=True)
    
    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()
    total_cost = df["Cost"].sum()
    overall_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    total_units = df["Units"].sum()
    profit_per_unit = (total_profit / total_units) if total_units > 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_kpi_card("Total Revenue", format_currency(total_sales), f"{len(df):,} Orders", "neutral")
    with col2:
        render_kpi_card("Gross Profit", format_currency(total_profit), f"Cost: {format_currency(total_cost)}", "positive")
    with col3:
        render_kpi_card("Gross Margin (%)", f"{overall_margin:.1f}%", "Target: >50.0%", "positive" if overall_margin >= 50 else "warning")
    with col4:
        render_kpi_card("Units Delivered", f"{int(total_units):,}", f"Avg ${total_sales/total_units:.2f}/unit" if total_units > 0 else "", "neutral")
    with col5:
        render_kpi_card("Profit per Unit", f"${profit_per_unit:.2f}", "Avg Profit / Unit", "positive")

    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([7, 5])
    with c1:
        st.markdown("<div class='section-title'>Manufacturing Factory & Regional Logistics Map</div>", unsafe_allow_html=True)
        
        # Build Map figure with pydeck or plotly scatter_geo
        factory_df = pd.DataFrame([
            {"Factory": k, "lat": v["lat"], "lon": v["lon"], "City": v["city"], "State": v["state"], "Type": "Factory"}
            for k, v in FACTORIES_INFO.items()
        ])
        
        # Route lines & destination aggregation
        dest_agg = df.groupby(["State/Province", "Factory", "Dest Lat", "Dest Lon"]).agg(
            Sales=("Sales", "sum"),
            Orders=("Row ID", "count")
        ).reset_index()

        fig_map = go.Figure()

        # Add route lines
        for _, r in dest_agg.iterrows():
            fac_info = FACTORIES_INFO.get(r["Factory"], {})
            if fac_info:
                fig_map.add_trace(go.Scattergeo(
                    lon=[fac_info["lon"], r["Dest Lon"]],
                    lat=[fac_info["lat"], r["Dest Lat"]],
                    mode="lines",
                    line=dict(width=1, color="rgba(124, 58, 237, 0.4)"),
                    hoverinfo="none",
                    showlegend=False
                ))

        # Add Factories
        fig_map.add_trace(go.Scattergeo(
            lon=factory_df["lon"],
            lat=factory_df["lat"],
            mode="markers+text",
            text=factory_df["Factory"],
            textposition="top center",
            marker=dict(size=14, color="#F59E0B", symbol="star", line=dict(width=1, color="#FFFFFF")),
            name="Factories",
            hovertemplate="<b>%{text}</b><br>City: %{customdata[0]}, %{customdata[1]}",
            customdata=factory_df[["City", "State"]]
        ))

        # Add Destinations
        fig_map.add_trace(go.Scattergeo(
            lon=dest_agg["Dest Lon"],
            lat=dest_agg["Dest Lat"],
            mode="markers",
            marker=dict(
                size=np.log1p(dest_agg["Sales"]) * 2,
                color="#06B6D4",
                opacity=0.7,
                line=dict(width=0.5, color="#FFFFFF")
            ),
            name="Customer States",
            hovertemplate="<b>%{customdata[0]}</b><br>Sales: $%{customdata[1]:,.2f}<br>Factory: %{customdata[2]}",
            customdata=dest_agg[["State/Province", "Sales", "Factory"]]
        ))

        fig_map.update_layout(
            geo=dict(
                scope="usa",
                projection_type="albers usa",
                showland=True,
                landcolor="#1E293B",
                subunitcolor="rgba(255,255,255,0.1)",
                countrycolor="rgba(255,255,255,0.2)",
                bgcolor="rgba(0,0,0,0)"
            ),
            margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB", family="Outfit")
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Division Financial Overview</div>", unsafe_allow_html=True)
        div_df = calculate_division_metrics(df)
        
        fig_div = px.bar(
            div_df,
            x="Division",
            y=["Total_Sales", "Total_Profit"],
            barmode="group",
            labels={"value": "USD ($)", "variable": "Metric"},
            color_discrete_sequence=["#3B82F6", "#10B981"]
        )
        fig_div.update_layout(plotly_theme["layout"])
        fig_div.update_layout(
            legend_title_text="",
            margin=dict(l=20, r=20, t=20, b=20),
            height=360
        )
        st.plotly_chart(fig_div, use_container_width=True)


# ==========================================
# TAB 2: PRODUCT PROFITABILITY OVERVIEW
# ==========================================
with tabs[1]:
    st.markdown("<div class='section-title'>Product Margin & Gross Profit Leaderboards</div>", unsafe_allow_html=True)
    prod_metrics = calculate_product_metrics(df)

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("#### 🏆 Top 7 Highest Gross Profit Products")
        fig_top_profit = px.bar(
            prod_metrics.head(7),
            x="Total_Profit",
            y="Product Name",
            orientation="h",
            color="Gross Margin (%)",
            color_continuous_scale="Viridis",
            labels={"Total_Profit": "Gross Profit ($)", "Product Name": ""}
        )
        fig_top_profit.update_layout(plotly_theme["layout"])
        fig_top_profit.update_layout(yaxis=dict(autorange="reversed"), height=340)
        st.plotly_chart(fig_top_profit, use_container_width=True)

    with p2:
        st.markdown("#### ⚠️ Lowest Margin Products (Margin Risk)")
        low_margin = prod_metrics.sort_values(by="Gross Margin (%)", ascending=True).head(7)
        fig_low_margin = px.bar(
            low_margin,
            x="Gross Margin (%)",
            y="Product Name",
            orientation="h",
            color="Gross Margin (%)",
            color_continuous_scale="Reds_r",
            labels={"Gross Margin (%)": "Margin (%)", "Product Name": ""}
        )
        fig_low_margin.update_layout(plotly_theme["layout"])
        fig_low_margin.update_layout(yaxis=dict(autorange="reversed"), height=340)
        st.plotly_chart(fig_low_margin, use_container_width=True)

    st.divider()
    st.markdown("<div class='section-title'>Strategic Product Matrix (Volume vs Margin)</div>", unsafe_allow_html=True)

    fig_matrix = px.scatter(
        prod_metrics,
        x="Total_Sales",
        y="Gross Margin (%)",
        size="Total_Units",
        color="Quadrant",
        hover_name="Product Name",
        hover_data=["Division", "Total_Profit", "Profit per Unit", "Factory"],
        color_discrete_map={
            "Stars (High Profit & High Volume)": "#10B981",
            "Volume Drivers (High Sales, Low Margin)": "#F59E0B",
            "Niche Drivers (Low Sales, High Margin)": "#3B82F6",
            "Laggards (Low Sales, Low Profit)": "#EF4444"
        },
        labels={"Total_Sales": "Total Revenue ($)", "Gross Margin (%)": "Gross Margin (%)"}
    )
    fig_matrix.update_layout(plotly_theme["layout"])
    fig_matrix.update_layout(height=480)
    st.plotly_chart(fig_matrix, use_container_width=True)

    st.markdown("#### Detailed Product Economics Table")
    st.dataframe(
        prod_metrics[[
            "Product Name", "Division", "Factory", "Total_Sales", "Total_Profit", 
            "Gross Margin (%)", "Profit per Unit", "Price per Unit", "Cost per Unit", "Diagnostic Flag"
        ]].style.format({
            "Total_Sales": "${:,.2f}",
            "Total_Profit": "${:,.2f}",
            "Gross Margin (%)": "{:.1f}%",
            "Profit per Unit": "${:.2f}",
            "Price per Unit": "${:.2f}",
            "Cost per Unit": "${:.2f}"
        }),
        use_container_width=True
    )


# ==========================================
# TAB 3: DIVISION PERFORMANCE DASHBOARD
# ==========================================
with tabs[2]:
    st.markdown("<div class='section-title'>Division-Level Financial Imbalance & Margin Distribution</div>", unsafe_allow_html=True)
    div_df = calculate_division_metrics(df)

    d1, d2 = st.columns([6, 6])
    with d1:
        st.markdown("#### Revenue Share vs Profit Share Imbalance")
        fig_imb = px.bar(
            div_df,
            x="Division",
            y="Financial Imbalance",
            color="Financial Imbalance",
            color_continuous_scale="Tropic",
            labels={"Financial Imbalance": "Profit Share % minus Revenue Share %"}
        )
        fig_imb.update_layout(plotly_theme["layout"])
        fig_imb.update_layout(height=360)
        st.plotly_chart(fig_imb, use_container_width=True)

    with d2:
        st.markdown("#### Product Gross Margin Distribution by Division")
        fig_box = px.box(
            df,
            x="Division",
            y="Gross Margin (%)",
            color="Division",
            points="all",
            color_discrete_sequence=["#8B5CF6", "#06B6D4", "#EC4899"]
        )
        fig_box.update_layout(plotly_theme["layout"])
        fig_box.update_layout(height=360)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("#### Division Performance Summary Table")
    st.dataframe(
        div_df.style.format({
            "Total_Sales": "${:,.2f}",
            "Total_Profit": "${:,.2f}",
            "Total_Cost": "${:,.2f}",
            "Gross Margin (%)": "{:.1f}%",
            "Revenue Share (%)": "{:.1f}%",
            "Profit Share (%)": "{:.1f}%",
            "Financial Imbalance": "{:+.1f}%",
            "Profit per Unit": "${:.2f}"
        }),
        use_container_width=True
    )


# ==========================================
# TAB 4: COST VS MARGIN DIAGNOSTICS
# ==========================================
with tabs[3]:
    st.markdown("<div class='section-title'>Manufacturing Cost vs Margin Diagnostics & Action Engine</div>", unsafe_allow_html=True)
    prod_metrics = calculate_product_metrics(df)

    m1, m2 = st.columns([7, 5])
    with m1:
        st.markdown("#### Manufacturing Cost per Unit vs Gross Margin (%)")
        fig_scatter = px.scatter(
            prod_metrics,
            x="Cost per Unit",
            y="Gross Margin (%)",
            size="Total_Sales",
            color="Diagnostic Flag",
            hover_name="Product Name",
            hover_data=["Price per Unit", "Profit per Unit", "Factory"],
            color_discrete_map={
                "Reprice Immediately": "#EF4444",
                "Renegotiate Cost": "#F59E0B",
                "Discontinuation Review": "#EC4899",
                "High Efficiency Driver": "#10B981",
                "Stable Core Product": "#3B82F6"
            },
            labels={"Cost per Unit": "Manufacturing Cost / Unit ($)", "Gross Margin (%)": "Gross Margin (%)"}
        )
        fig_scatter.update_layout(plotly_theme["layout"])
        fig_scatter.update_layout(height=420)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with m2:
        st.markdown("#### Interactive Repricing Simulator")
        st.info("Simulate the profit expansion effect of selective price adjustments on margin-poor products.")
        
        target_prod = st.selectbox("Select Product to Reprice", prod_metrics["Product Name"].unique())
        prod_row = prod_metrics[prod_metrics["Product Name"] == target_prod].iloc[0]
        
        c_price = prod_row["Price per Unit"]
        c_cost = prod_row["Cost per Unit"]
        c_units = prod_row["Total_Units"]
        c_margin = prod_row["Gross Margin (%)"]
        
        st.write(f"Current Price: **${c_price:.2f}** | Cost: **${c_cost:.2f}** | Margin: **{c_margin:.1f}%**")
        
        price_increase_pct = st.slider("Proposed Price Increase (%)", 0, 50, 10, 1)
        
        new_price = c_price * (1 + price_increase_pct / 100)
        new_profit_per_unit = new_price - c_cost
        new_margin = (new_profit_per_unit / new_price * 100) if new_price > 0 else 0
        incremental_profit = (new_profit_per_unit - (c_price - c_cost)) * c_units
        
        st.metric("New Selling Price", f"${new_price:.2f}", delta=f"+{price_increase_pct}%")
        st.metric("New Gross Margin (%)", f"{new_margin:.1f}%", delta=f"+{new_margin - c_margin:.1f}%")
        st.metric("Projected Incremental Annual Profit", format_currency(incremental_profit))


# ==========================================
# TAB 5: PROFIT CONCENTRATION (PARETO 80/20)
# ==========================================
with tabs[4]:
    st.markdown("<div class='section-title'>Pareto Concentration (80/20 Rule Analysis)</div>", unsafe_allow_html=True)
    sales_pareto, profit_pareto = calculate_pareto_analysis(df)

    par1, par2 = st.columns(2)
    with par1:
        st.markdown("#### 📈 Gross Profit Cumulative Concentration")
        fig_par_profit = go.Figure()
        fig_par_profit.add_trace(go.Bar(
            x=profit_pareto["Product Name"],
            y=profit_pareto["Profit"],
            name="Gross Profit ($)",
            marker_color="#10B981"
        ))
        fig_par_profit.add_trace(go.Scatter(
            x=profit_pareto["Product Name"],
            y=profit_pareto["Cum_Profit_Pct"],
            name="Cumulative Profit %",
            yaxis="y2",
            line=dict(color="#F59E0B", width=3)
        ))
        fig_par_profit.update_layout(plotly_theme["layout"])
        fig_par_profit.update_layout(
            yaxis=dict(title="Gross Profit ($)"),
            yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 105]),
            xaxis=dict(tickangle=-45),
            height=400,
            margin=dict(b=100)
        )
        st.plotly_chart(fig_par_profit, use_container_width=True)

    with par2:
        st.markdown("#### 💵 Revenue Cumulative Concentration")
        fig_par_sales = go.Figure()
        fig_par_sales.add_trace(go.Bar(
            x=sales_pareto["Product Name"],
            y=sales_pareto["Sales"],
            name="Revenue ($)",
            marker_color="#3B82F6"
        ))
        fig_par_sales.add_trace(go.Scatter(
            x=sales_pareto["Product Name"],
            y=sales_pareto["Cum_Sales_Pct"],
            name="Cumulative Revenue %",
            yaxis="y2",
            line=dict(color="#EC4899", width=3)
        ))
        fig_par_sales.update_layout(plotly_theme["layout"])
        fig_par_sales.update_layout(
            yaxis=dict(title="Sales Revenue ($)"),
            yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 105]),
            xaxis=dict(tickangle=-45),
            height=400,
            margin=dict(b=100)
        )
        st.plotly_chart(fig_par_sales, use_container_width=True)

    # Dependency Metric Callout
    top_80_profit_prods = profit_pareto[profit_pareto["Cum_Profit_Pct"] <= 85]
    pct_prods_for_80_profit = (len(top_80_profit_prods) / len(profit_pareto)) * 100
    
    st.info(f"💡 **Key Pareto Insight**: Just **{len(top_80_profit_prods)} out of {len(profit_pareto)} products** ({pct_prods_for_80_profit:.1f}% of total portfolio) account for **80%+ of Nassau Candy's total gross profit**.")


# ==========================================
# TAB 6: FACTORY & ROUTE LOGISTICS EFFICIENCY
# ==========================================
with tabs[5]:
    st.markdown("<div class='section-title'>Factory Production & Shipping Logistics Diagnostics</div>", unsafe_allow_html=True)
    fac_metrics = calculate_factory_logistics(df)

    f1, f2 = st.columns([6, 6])
    with f1:
        st.markdown("#### Gross Profit & Revenue by Manufacturing Factory")
        fig_fac_bar = px.bar(
            fac_metrics,
            x="Factory",
            y=["Total_Sales", "Total_Profit"],
            barmode="group",
            labels={"value": "USD ($)", "variable": "Financial Metric"},
            color_discrete_sequence=["#3B82F6", "#10B981"]
        )
        fig_fac_bar.update_layout(plotly_theme["layout"])
        fig_fac_bar.update_layout(height=360)
        st.plotly_chart(fig_fac_bar, use_container_width=True)

    with f2:
        st.markdown("#### Shipping Mode Distribution & Average Transit Time")
        ship_agg = df.groupby("Ship Mode").agg(
            Orders=("Row ID", "count"),
            Avg_Transit=("Transit Days", "mean"),
            Sales=("Sales", "sum")
        ).reset_index()

        fig_ship = px.pie(
            ship_agg,
            names="Ship Mode",
            values="Sales",
            hole=0.4,
            color_discrete_sequence=["#8B5CF6", "#06B6D4", "#F59E0B", "#EF4444"]
        )
        fig_ship.update_layout(plotly_theme["layout"])
        fig_ship.update_layout(height=360)
        st.plotly_chart(fig_ship, use_container_width=True)

    st.markdown("#### Factory Performance Benchmark Table")
    st.dataframe(
        fac_metrics.style.format({
            "Total_Sales": "${:,.2f}",
            "Total_Profit": "${:,.2f}",
            "Gross Margin (%)": "{:.1f}%",
            "Profit per Unit": "${:.2f}",
            "Avg_Transit_Days": "{:.1f} Days"
        }),
        use_container_width=True
    )

st.sidebar.markdown("---")
st.sidebar.caption("Nassau Candy Distributor BI Platform v2.4")
