import streamlit as st

from utils.style import apply_style

from utils import charts
from utils.data_loader import load_data, sidebar_filters

st.set_page_config(page_title="Sales Dashboard", page_icon="💰", layout="wide")
apply_style()
st.title("💰 Sales Dashboard")
df = sidebar_filters(load_data())

order_totals = df.groupby("Order_ID")[["Total_Sale", "Profit"]].sum()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${df['Total_Sale'].sum():,.0f}")
c2.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
c3.metric("Total Orders", f"{df['Order_ID'].nunique():,}")
c4.metric("Average Order Value", f"${order_totals['Total_Sale'].mean():,.2f}")
c5, c6, c7, c8 = st.columns(4)
c5.metric("Average Profit per Order", f"${order_totals['Profit'].mean():,.2f}")
c6.metric("Loss-Making Order Lines", f"{df['Is_Loss'].mean() * 100:.1f}%")
c7.metric("Average Discount", f"{df['Discount'].mean() * 100:.1f}%")
c8.metric("Profit Margin", f"{df['Profit'].sum() / max(df['Total_Sale'].sum(), 1) * 100:.1f}%")
st.caption("Return rate, rating and delivery days are not available in this dataset; "
           "loss-making rate and discount are shown instead.")

tab1, tab2 = st.tabs(["Monthly Sales", "Monthly Profit"])
with tab1:
    st.pyplot(charts.monthly_sales(df))
with tab2:
    st.pyplot(charts.monthly_profit(df))
