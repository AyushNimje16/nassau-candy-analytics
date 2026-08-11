import pandas as pd
import numpy as np

def calculate_product_metrics(df):
    """Aggregates metrics at the Product level."""
    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()

    prod = df.groupby(["Product Name", "Division", "Factory"]).agg(
        Total_Sales=("Sales", "sum"),
        Total_Units=("Units", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum"),
        Order_Count=("Row ID", "count"),
        Avg_Transit_Days=("Transit Days", "mean")
    ).reset_index()

    prod["Gross Margin (%)"] = np.where(prod["Total_Sales"] > 0, (prod["Total_Profit"] / prod["Total_Sales"]) * 100, 0)
    prod["Profit per Unit"] = np.where(prod["Total_Units"] > 0, prod["Total_Profit"] / prod["Total_Units"], 0)
    prod["Cost per Unit"] = np.where(prod["Total_Units"] > 0, prod["Total_Cost"] / prod["Total_Units"], 0)
    prod["Price per Unit"] = np.where(prod["Total_Units"] > 0, prod["Total_Sales"] / prod["Total_Units"], 0)

    prod["Revenue Contribution (%)"] = np.where(total_sales > 0, (prod["Total_Sales"] / total_sales) * 100, 0)
    prod["Profit Contribution (%)"] = np.where(total_profit > 0, (prod["Total_Profit"] / total_profit) * 100, 0)

    # Risk Diagnostic Action Tagging
    avg_margin = prod["Gross Margin (%)"].mean()
    def assign_action(row):
        margin = row["Gross Margin (%)"]
        cost_ratio = (row["Total_Cost"] / row["Total_Sales"]) if row["Total_Sales"] > 0 else 1.0
        profit_share = row["Profit Contribution (%)"]
        
        if margin < 25.0 and row["Total_Sales"] > 5000:
            return "Reprice Immediately"
        elif cost_ratio > 0.65:
            return "Renegotiate Cost"
        elif margin < 20.0 and profit_share < 2.0:
            return "Discontinuation Review"
        elif margin >= 45.0:
            return "High Efficiency Driver"
        else:
            return "Stable Core Product"

    prod["Diagnostic Flag"] = prod.apply(assign_action, axis=1)

    # Strategic Matrix Quadrant
    median_sales = prod["Total_Sales"].median()
    median_margin = prod["Gross Margin (%)"].median()

    def assign_quadrant(row):
        high_sales = row["Total_Sales"] >= median_sales
        high_margin = row["Gross Margin (%)"] >= median_margin
        if high_sales and high_margin:
            return "Stars (High Profit & High Volume)"
        elif high_sales and not high_margin:
            return "Volume Drivers (High Sales, Low Margin)"
        elif not high_sales and high_margin:
            return "Niche Drivers (Low Sales, High Margin)"
        else:
            return "Laggards (Low Sales, Low Profit)"

    prod["Quadrant"] = prod.apply(assign_quadrant, axis=1)

    return prod.sort_values(by="Total_Profit", ascending=False)


def calculate_division_metrics(df):
    """Aggregates metrics at the Division level."""
    total_sales = df["Sales"].sum()
    total_profit = df["Gross Profit"].sum()

    div = df.groupby("Division").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Units=("Units", "sum"),
        Order_Count=("Row ID", "count"),
        Product_Count=("Product Name", "nunique")
    ).reset_index()

    div["Gross Margin (%)"] = (div["Total_Profit"] / div["Total_Sales"]) * 100
    div["Revenue Share (%)"] = (div["Total_Sales"] / total_sales) * 100
    div["Profit Share (%)"] = (div["Total_Profit"] / total_profit) * 100
    div["Financial Imbalance"] = div["Profit Share (%)"] - div["Revenue Share (%)"]
    div["Profit per Unit"] = div["Total_Profit"] / div["Total_Units"]

    return div.sort_values(by="Total_Profit", ascending=False)


def calculate_pareto_analysis(df, entity_col="Product Name"):
    """Calculates 80/20 Pareto metrics for Revenue and Gross Profit."""
    grouped = df.groupby(entity_col).agg(
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum")
    ).reset_index()

    # Sales Pareto
    sales_sorted = grouped.sort_values(by="Sales", ascending=False).copy()
    sales_sorted["Cum_Sales"] = sales_sorted["Sales"].cumsum()
    sales_sorted["Cum_Sales_Pct"] = (sales_sorted["Cum_Sales"] / sales_sorted["Sales"].sum()) * 100
    sales_sorted["Sales_Rank"] = range(1, len(sales_sorted) + 1)
    sales_sorted["Sales_Pct_Of_Items"] = (sales_sorted["Sales_Rank"] / len(sales_sorted)) * 100

    # Profit Pareto
    profit_sorted = grouped.sort_values(by="Profit", ascending=False).copy()
    profit_sorted["Cum_Profit"] = profit_sorted["Profit"].cumsum()
    profit_sorted["Cum_Profit_Pct"] = (profit_sorted["Cum_Profit"] / profit_sorted["Profit"].sum()) * 100
    profit_sorted["Profit_Rank"] = range(1, len(profit_sorted) + 1)
    profit_sorted["Profit_Pct_Of_Items"] = (profit_sorted["Profit_Rank"] / len(profit_sorted)) * 100

    return sales_sorted, profit_sorted


def calculate_factory_logistics(df):
    """Calculates operational and logistics metrics for manufacturing factories."""
    fac = df.groupby("Factory").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Units=("Units", "sum"),
        Total_Orders=("Row ID", "count"),
        Avg_Transit_Days=("Transit Days", "mean"),
        Product_Count=("Product Name", "nunique")
    ).reset_index()

    fac["Gross Margin (%)"] = (fac["Total_Profit"] / fac["Total_Sales"]) * 100
    fac["Profit per Unit"] = fac["Total_Profit"] / fac["Total_Units"]

    return fac.sort_values(by="Total_Sales", ascending=False)
