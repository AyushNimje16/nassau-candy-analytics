import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from src.data_loader import load_raw_data, FACTORIES_INFO, PRODUCT_FACTORY_MAP, US_STATE_COORDS
from src.analytics import calculate_product_metrics, calculate_division_metrics, calculate_pareto_analysis, calculate_factory_logistics

def generate_powerbi_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    powerbi_dir = os.path.join(base_dir, "powerbi")
    os.makedirs(powerbi_dir, exist_ok=True)

    df = load_raw_data()

    # 1. Fact Table: Orders
    fact_orders = df[[
        "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID", 
        "State/Province", "Region", "Division", "Product ID", "Product Name", 
        "Sales", "Units", "Gross Profit", "Cost", "Gross Margin (%)", 
        "Profit per Unit", "Cost per Unit", "Price per Unit", "Transit Days", "Factory"
    ]].copy()

    # 2. Dim Table: Products
    prod_metrics = calculate_product_metrics(df)
    dim_products = prod_metrics[[
        "Product Name", "Division", "Factory", "Diagnostic Flag", "Quadrant"
    ]].drop_duplicates()

    # 3. Dim Table: Factories
    dim_factories = pd.DataFrame([
        {
            "Factory": k,
            "Latitude": v["lat"],
            "Longitude": v["lon"],
            "City": v["city"],
            "State": v["state"]
        }
        for k, v in FACTORIES_INFO.items()
    ])

    # 4. Dim Table: Geography
    dim_geography = df[["State/Province", "Region", "Dest Lat", "Dest Lon"]].drop_duplicates().rename(
        columns={"Dest Lat": "Latitude", "Dest Lon": "Longitude"}
    )

    # 5. Export formatted Excel workbook for Power BI Desktop
    excel_path = os.path.join(powerbi_dir, "Nassau_Candy_PowerBI_Model.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        fact_orders.to_excel(writer, sheet_name="Fact_Orders", index=False)
        dim_products.to_excel(writer, sheet_name="Dim_Products", index=False)
        dim_factories.to_excel(writer, sheet_name="Dim_Factories", index=False)
        dim_geography.to_excel(writer, sheet_name="Dim_Geography", index=False)

    print(f"Power BI Excel Dataset created at: {excel_path}")

if __name__ == "__main__":
    generate_powerbi_data()
