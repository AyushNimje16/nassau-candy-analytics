import os
import pandas as pd
import numpy as np

FACTORIES_INFO = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036, "city": "Casa Grande", "state": "Arizona"},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371, "city": "Savannah", "state": "Georgia"},
    "Sugar Shack": {"lat": 48.11914, "lon": -96.18115, "city": "Thief River Falls", "state": "Minnesota"},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487, "city": "Moline", "state": "Illinois"},
    "The Other Factory": {"lat": 35.1175, "lon": -89.971107, "city": "Memphis", "state": "Tennessee"},
}

PRODUCT_FACTORY_MAP = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory",
}

US_STATE_COORDS = {
    "Texas": {"lat": 31.9686, "lon": -99.9018},
    "Illinois": {"lat": 40.6331, "lon": -89.3985},
    "Pennsylvania": {"lat": 41.2033, "lon": -77.1945},
    "Kentucky": {"lat": 37.8393, "lon": -84.2700},
    "Georgia": {"lat": 32.1656, "lon": -82.9001},
    "California": {"lat": 36.7783, "lon": -119.4179},
    "Virginia": {"lat": 37.4316, "lon": -78.6569},
    "Delaware": {"lat": 38.9108, "lon": -75.5277},
    "South Carolina": {"lat": 33.8361, "lon": -81.1637},
    "Florida": {"lat": 27.6648, "lon": -81.5158},
    "Ohio": {"lat": 40.4173, "lon": -82.9071},
    "North Carolina": {"lat": 35.7596, "lon": -79.0193},
    "Michigan": {"lat": 44.3148, "lon": -85.6024},
    "Washington": {"lat": 47.7511, "lon": -120.7401},
    "New York": {"lat": 40.7128, "lon": -74.0060},
    "Indiana": {"lat": 40.2672, "lon": -86.1349},
    "Tennessee": {"lat": 35.5175, "lon": -86.5804},
    "Arizona": {"lat": 34.0489, "lon": -111.0937},
    "Colorado": {"lat": 39.5501, "lon": -105.7821},
    "Minnesota": {"lat": 46.7296, "lon": -94.6859},
}

def load_raw_data(filepath=None):
    if filepath is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(base_dir, "data", "nassau_candy_data.csv")
        if not os.path.exists(filepath):
            filepath = r"c:\Users\ayush\Downloads\Nassau Candy Distributor (3).csv"

    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()

    # Convert numeric fields
    numeric_cols = ["Sales", "Units", "Gross Profit", "Cost"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Standardize string fields
    str_cols = ["Product Name", "Division", "Region", "State/Province", "City", "Ship Mode"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Parse dates (formats can be DD-MM-YYYY or MM/DD/YYYY)
    for date_col in ["Order Date", "Ship Date"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")

    # Data validation: remove invalid zero or negative sales records
    df = df[df["Sales"] > 0].copy()

    # Feature Engineering
    df["Gross Margin (%)"] = np.where(df["Sales"] > 0, (df["Gross Profit"] / df["Sales"]) * 100, 0)
    df["Profit per Unit"] = np.where(df["Units"] > 0, df["Gross Profit"] / df["Units"], 0)
    df["Cost per Unit"] = np.where(df["Units"] > 0, df["Cost"] / df["Units"], 0)
    df["Price per Unit"] = np.where(df["Units"] > 0, df["Sales"] / df["Units"], 0)
    
    if "Ship Date" in df.columns and "Order Date" in df.columns:
        df["Transit Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
        df["Transit Days"] = df["Transit Days"].clip(lower=0)

    # Factory Mapping
    df["Factory"] = df["Product Name"].map(PRODUCT_FACTORY_MAP).fillna("Secret Factory")
    df["Factory Lat"] = df["Factory"].apply(lambda f: FACTORIES_INFO.get(f, {}).get("lat", 35.0))
    df["Factory Lon"] = df["Factory"].apply(lambda f: FACTORIES_INFO.get(f, {}).get("lon", -90.0))

    # Add Destination Coordinates for mapping
    df["Dest Lat"] = df["State/Province"].apply(lambda s: US_STATE_COORDS.get(s, {}).get("lat", 38.0))
    df["Dest Lon"] = df["State/Province"].apply(lambda s: US_STATE_COORDS.get(s, {}).get("lon", -95.0))

    return df

if __name__ == "__main__":
    df = load_raw_data()
    print(f"Data Loaded Successfully: {df.shape[0]} rows, {df.shape[1]} columns")
    print(df.groupby("Factory")[["Sales", "Gross Profit"]].sum())
