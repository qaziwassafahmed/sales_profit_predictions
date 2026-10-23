import streamlit as st

from utils.style import apply_style

from utils.data_loader import load_data

st.set_page_config(page_title="Sales Analytics & Profit Prediction", page_icon="📊", layout="wide")
apply_style()
df = load_data()

st.title("📊 Sales Performance Analytics and Profit Prediction Dashboard")
st.caption("Student: QAZI WASSAF AHMED   |   Course: Data Science and Machine Learning")

st.header("Business Problem")
st.write(
    "A retail company wants to understand its sales performance and improve profitability. "
    "It needs to know which products, categories and regions make money, how discounts affect profit, "
    "and what profit to expect from a new order."
)

st.header("Project Objectives")
st.markdown(
    """
- Analyse sales and profit by category, product, region, segment and time.
- Measure how discounts affect profit.
- Train and compare regression models that predict the profit of an order.
- Let business users get a profit estimate (with a loss warning) for a new order.
"""
)

st.header("Dataset Description")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{len(df):,}")
c2.metric("Orders", f"{df['Order_ID'].nunique():,}")
c3.metric("Customers", f"{df['Customer_ID'].nunique():,}")
c4.metric("Products", f"{df['Product_Name'].nunique():,}")
st.write(
    f"Global Superstore data covering **{df['Order_Year'].min()} to {df['Order_Year'].max()}**, "
    f"{df['Country'].nunique()} countries and {df['Market'].nunique()} markets. "
    "Target variable for machine learning: **Profit**."
)

with st.expander("Known data limitations"):
    st.markdown(
        """
- The original **Order Date** and **Ship Date** columns were corrupted, so the order date is rebuilt
  approximately from *Year* and *week number* (month and quarter are reliable, the exact day is not).
- Delivery days, customer rating, returns, brand, salesperson and payment method are **not** in this dataset.
"""
    )

st.info("Use the sidebar to open the other pages.")
