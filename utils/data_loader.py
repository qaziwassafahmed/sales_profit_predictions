"""Cached loading helpers and shared sidebar filters."""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent


@st.cache_data
def load_data():
    return pd.read_csv(ROOT / "data" / "clean_data.csv", parse_dates=["Order_Date"])


@st.cache_resource
def load_model():
    return joblib.load(ROOT / "models" / "model.pkl")


@st.cache_resource
def load_evaluation():
    return joblib.load(ROOT / "models" / "evaluation.pkl")


def sidebar_filters(df):
    """Year and Market filters shared by the analysis pages."""
    st.sidebar.header("Filters")
    years = sorted(df["Order_Year"].unique())
    markets = sorted(df["Market"].unique())
    sel_years = st.sidebar.multiselect("Year", years, default=years)
    sel_markets = st.sidebar.multiselect("Market", markets, default=markets)
    out = df[df["Order_Year"].isin(sel_years) & df["Market"].isin(sel_markets)]
    if out.empty:
        st.warning("No data for the selected filters. Please select at least one year and one market.")
        st.stop()
    return out
