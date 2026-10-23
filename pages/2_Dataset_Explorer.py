import streamlit as st

from utils.style import apply_style

from utils.data_loader import load_data

st.set_page_config(page_title="Dataset Explorer", page_icon="🔎", layout="wide")
apply_style()
st.title("🔎 Dataset Explorer")
df = load_data()

st.sidebar.header("Filters")
rows = st.sidebar.selectbox("Rows to display", [10, 25, 50, 100, 500], index=1)
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()))
categories = st.sidebar.multiselect("Product category", sorted(df["Category"].unique()))
product_text = st.sidebar.text_input("Product name contains")
d_min, d_max = df["Order_Date"].min().date(), df["Order_Date"].max().date()
date_range = st.sidebar.date_input("Order date range", (d_min, d_max), min_value=d_min, max_value=d_max)

out = df
if regions:
    out = out[out["Region"].isin(regions)]
if categories:
    out = out[out["Category"].isin(categories)]
if product_text:
    out = out[out["Product_Name"].str.contains(product_text, case=False, regex=False)]
if isinstance(date_range, tuple) and len(date_range) == 2:
    out = out[(out["Order_Date"].dt.date >= date_range[0]) & (out["Order_Date"].dt.date <= date_range[1])]
else:
    st.info("Select both a start and an end date.")

st.write(f"Showing **{min(rows, len(out)):,}** of **{len(out):,}** matching rows.")
if out.empty:
    st.warning("No rows match these filters.")
else:
    st.dataframe(out.head(rows))
    st.download_button("⬇️ Download filtered data (CSV)", out.to_csv(index=False).encode("utf-8"),
                       file_name="filtered_sales_data.csv", mime="text/csv")

with st.expander("Dataset summary"):
    st.write("Shape:", df.shape)
    st.dataframe(df.select_dtypes("number").describe())
