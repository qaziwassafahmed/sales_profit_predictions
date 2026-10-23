"""Cleaning and feature engineering for the Global Superstore dataset."""
import numpy as np
import pandas as pd

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Drop useless columns, fix names, rebuild the order date."""
    df = df.copy()

    # Order Date / Ship Date are corrupted in the CSV (every value is "00:00.0"),
    # so we rebuild an approximate date from Year + weeknum instead.
    df = df.drop(columns=["Order Date", "Ship Date", "ji_lu-shu", "Row ID", "Product ID"])

    df.columns = [c.strip().replace(" ", "_").replace("-", "_") for c in df.columns]
    df = df.rename(columns={"Market2": "Market_Group", "weeknum": "Order_Week",
                            "Year": "Order_Year", "Sales": "Total_Sale"})

    # Approximate order date = first day of the order's week
    start = pd.to_datetime(df["Order_Year"].astype(str) + "-01-01")
    df["Order_Date"] = start + pd.to_timedelta((df["Order_Week"] - 1) * 7, unit="D")
    year_end = pd.to_datetime(df["Order_Year"].astype(str) + "-12-31")
    df["Order_Date"] = df["Order_Date"].where(df["Order_Date"] <= year_end, year_end)

    # Remove stray spaces in text columns
    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]) and col != "Order_Date":
            df[col] = df[col].astype(str).str.strip()

    df = df.drop_duplicates().reset_index(drop=True)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add the new columns used for EDA and modelling."""
    df = df.copy()

    # Time features
    df["Order_Month"] = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Month"].map(lambda m: MONTH_NAMES[m - 1])
    df["Quarter"] = df["Order_Date"].dt.quarter

    # Price features (Total_Sale is already after discount)
    keep_fraction = 1 - df["Discount"]
    df["Revenue_Before_Discount"] = np.where(keep_fraction > 0,
                                             df["Total_Sale"] / keep_fraction, df["Total_Sale"])
    df["Discount_Amount"] = df["Revenue_Before_Discount"] - df["Total_Sale"]
    df["Unit_Price"] = df["Revenue_Before_Discount"] / df["Quantity"]

    # Profit margin (safe when Total_Sale is zero)
    df["Profit_Margin"] = np.where(df["Total_Sale"] > 0,
                                   df["Profit"] / df["Total_Sale"].replace(0, np.nan) * 100, 0)

    # Category features
    df["Order_Size_Category"] = pd.cut(df["Quantity"], bins=[0, 2, 5, np.inf],
                                       labels=["Small", "Medium", "Large"]).astype(str)
    df["Discount_Level"] = pd.cut(df["Discount"], bins=[-0.01, 0, 0.2, 0.4, 1],
                                  labels=["No Discount", "Low", "Medium", "High"]).astype(str)
    df["Is_Loss"] = (df["Profit"] < 0).astype(int)
    return df
