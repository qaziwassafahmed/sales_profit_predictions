"""Run once: raw CSV -> data/clean_data.csv"""
import pandas as pd
from utils.preprocessing import clean_data, engineer_features

raw = pd.read_csv("data/Global_Superstore.csv")
clean = engineer_features(clean_data(raw))
clean.to_csv("data/clean_data.csv", index=False)

print("Raw shape  :", raw.shape)
print("Clean shape:", clean.shape)
print("Missing    :", int(clean.isnull().sum().sum()))
print("Date range :", clean["Order_Date"].min().date(), "to", clean["Order_Date"].max().date())
print(clean.dtypes)
