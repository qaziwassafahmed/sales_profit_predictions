import streamlit as st

from utils.style import apply_style

from utils import charts
from utils.data_loader import load_data, sidebar_filters

st.set_page_config(page_title="Product & Regional Analysis", page_icon="🌍", layout="wide")
apply_style()
st.title("🌍 Product and Regional Analysis")
df = sidebar_filters(load_data())

tab1, tab2, tab3, tab4 = st.tabs(["Categories", "Products", "Regions", "Segments"])
with tab1:
    a, b = st.columns(2)
    a.pyplot(charts.sales_by_category(df))
    b.pyplot(charts.profit_by_category(df))
    a.pyplot(charts.sales_by_subcategory(df))
    b.pyplot(charts.profit_by_subcategory(df))
    st.pyplot(charts.loss_rate_by_subcategory(df))
with tab2:
    n = st.slider("Number of top products", 5, 20, 10)
    a, b = st.columns(2)
    a.pyplot(charts.top_products_sales(df, n))
    b.pyplot(charts.top_products_profit(df, n))
    st.subheader("High sales but negative profit")
    prod = df.groupby("Product_Name").agg(Sales=("Total_Sale", "sum"), Profit=("Profit", "sum"))
    st.dataframe(prod[prod["Profit"] < 0].sort_values("Sales", ascending=False).head(10).round(0))
with tab3:
    a, b = st.columns(2)
    a.pyplot(charts.sales_by_region(df))
    b.pyplot(charts.profit_by_region(df))
    st.pyplot(charts.top_countries_sales(df))
with tab4:
    st.pyplot(charts.segment_performance(df))
    st.caption("Customer segment is used instead of salesperson (not in this dataset).")
