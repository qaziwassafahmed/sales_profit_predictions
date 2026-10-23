"""Prints the answers to the Task 4 EDA questions (adapted to this dataset)."""
import pandas as pd

df = pd.read_csv("data/clean_data.csv", parse_dates=["Order_Date"])

print("Total revenue        :", f"{df['Total_Sale'].sum():,.0f}")
print("Total profit         :", f"{df['Profit'].sum():,.0f}")
print("Avg order value      :", f"{df.groupby('Order_ID')['Total_Sale'].sum().mean():,.2f}")
print("Avg profit per order :", f"{df.groupby('Order_ID')['Profit'].sum().mean():,.2f}")
print("Orders / customers / products / countries:",
      df["Order_ID"].nunique(), df["Customer_ID"].nunique(),
      df["Product_Name"].nunique(), df["Country"].nunique())
print("\nSales by Category:\n", df.groupby("Category")["Total_Sale"].sum().sort_values(ascending=False))
print("\nProfit by Category:\n", df.groupby("Category")["Profit"].sum().sort_values(ascending=False))
print("\nProfit by Region:\n", df.groupby("Region")["Profit"].sum().sort_values(ascending=False).head(5))
print("\nTop 5 Cities by sales:\n", df.groupby("City")["Total_Sale"].sum().sort_values(ascending=False).head(5))
print("\nMost common Ship Mode:\n", df["Ship_Mode"].value_counts())
print("\nSegment profit:\n", df.groupby("Segment")["Profit"].sum())
print("\nLoss order %:", round(df["Is_Loss"].mean() * 100, 1))
print("\nLoss rate by Sub-Category (top 5):\n",
      (df.groupby("Sub_Category")["Is_Loss"].mean() * 100).sort_values(ascending=False).head(5).round(1))
print("\nAvg profit by Discount level:\n",
      df.groupby("Discount_Level")["Profit"].mean().reindex(["No Discount", "Low", "Medium", "High"]).round(2))
print("\nLoss % by Discount level:\n",
      (df.groupby("Discount_Level")["Is_Loss"].mean() * 100).reindex(["No Discount", "Low", "Medium", "High"]).round(1))
sp = df.groupby("Product_Name").agg(sales=("Total_Sale", "sum"), profit=("Profit", "sum"))
print("\nHigh sales but negative profit (top 5 by sales):\n",
      sp[sp["profit"] < 0].sort_values("sales", ascending=False).head(5).round(0))
print("\nSales/Profit by Year:\n", df.groupby("Order_Year")[["Total_Sale", "Profit"]].sum())
print("\nProfit by Order Size:\n", df.groupby("Order_Size_Category")["Profit"].mean().round(2))
