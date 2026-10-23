import streamlit as st

from utils.style import apply_style

from utils import charts
from utils.data_loader import load_data, sidebar_filters

st.set_page_config(page_title="Customer & Shipping Analysis", page_icon="🚚", layout="wide")
apply_style()
st.title("🚚 Customer and Shipping Analysis")
df = sidebar_filters(load_data())
st.caption("Gender, age, rating and delivery days are not in this dataset, so customer segment, "
           "ship mode, order priority and discounts are analysed instead.")

tab1, tab2, tab3, tab4 = st.tabs(["Customers", "Shipping", "Discount & Loss", "Order Size"])
with tab1:
    st.pyplot(charts.top_customers(df))
    seg = df.groupby("Segment")["Total_Sale"].sum().reset_index()
    st.dataframe(seg.rename(columns={"Total_Sale": "Total Sales"}))
with tab2:
    a, b = st.columns(2)
    a.pyplot(charts.ship_mode_distribution(df))
    summary = df.groupby("Ship_Mode").agg(Orders=("Order_ID", "count"), Avg_Profit=("Profit", "mean"),
                                           Avg_Shipping_Cost=("Shipping_Cost", "mean")).round(2)
    b.dataframe(summary)
    pr = df.groupby("Order_Priority")["Profit"].mean().round(2).reset_index()
    st.dataframe(pr)
with tab3:
    a, b = st.columns(2)
    a.pyplot(charts.avg_profit_by_discount_level(df))
    b.pyplot(charts.discount_vs_profit_scatter(df))
    loss = (df.groupby("Discount_Level")["Is_Loss"].mean() * 100).round(1).reset_index()
    st.dataframe(loss.rename(columns={"Is_Loss": "% orders with loss"}))
with tab4:
    size = df.groupby("Order_Size_Category").agg(Orders=("Order_ID", "count"),
                                                  Avg_Profit=("Profit", "mean")).round(2)
    st.dataframe(size)
