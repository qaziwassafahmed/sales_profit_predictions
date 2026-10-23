import pandas as pd
import streamlit as st

from utils.style import apply_style

from utils.data_loader import load_data, load_evaluation, load_model

st.set_page_config(page_title="Profit Prediction", page_icon="🎯", layout="wide")
apply_style()
st.title("🎯 Profit Prediction")
st.write("Enter the details of a new order to estimate its profit.")

df, model, ev = load_data(), load_model(), load_evaluation()

sub_map = df.groupby("Category")["Sub_Category"].unique().to_dict()
region_map = df.groupby("Market")["Region"].unique().to_dict()
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def profit_category(value):
    if value < 0:
        return "Loss"
    if value < 20:
        return "Low Profit"
    if value < 100:
        return "Medium Profit"
    return "High Profit"


c1, c2, c3 = st.columns(3)
with c1:
    category = st.selectbox("Product category", sorted(sub_map))
    sub_category = st.selectbox("Sub-category", sorted(sub_map[category]))
    segment = st.selectbox("Customer segment", sorted(df["Segment"].unique()))
    quantity = st.number_input("Quantity", min_value=1, max_value=100, value=3, step=1)
with c2:
    market = st.selectbox("Market", sorted(region_map))
    region = st.selectbox("Region", sorted(region_map[market]))
    unit_price = st.number_input("Unit price before discount ($)", min_value=0.01, value=50.0, step=1.0)
    discount = st.slider("Discount", 0.0, 0.85, 0.0, 0.05, format="%.2f")
with c3:
    ship_mode = st.selectbox("Ship mode", sorted(df["Ship_Mode"].unique()))
    priority = st.selectbox("Order priority", ["Low", "Medium", "High", "Critical"])
    shipping_cost = st.number_input("Shipping cost ($)", min_value=0.0, value=10.0, step=1.0)
    month = st.selectbox("Order month", months, index=5)

if st.button("Predict profit", type="primary"):
    row = pd.DataFrame([{
        "Quantity": quantity, "Unit_Price": unit_price, "Discount": discount,
        "Shipping_Cost": shipping_cost, "Order_Month": months.index(month) + 1,
        "Category": category, "Sub_Category": sub_category, "Segment": segment,
        "Ship_Mode": ship_mode, "Order_Priority": priority, "Market": market, "Region": region,
    }])
    try:
        predicted = float(model.predict(row)[0])
    except Exception as exc:  # keeps the app alive on unexpected input
        st.error(f"Prediction failed: {exc}")
        st.stop()

    sale = quantity * unit_price * (1 - discount)
    label = profit_category(predicted)
    a, b, c = st.columns(3)
    a.metric("Predicted profit", f"-${abs(predicted):,.2f}" if predicted < 0 else f"${predicted:,.2f}")
    b.metric("Profit category", label)
    c.metric("Estimated order value", f"${sale:,.2f}")

    if predicted < 0:
        st.error("⚠️ Loss warning: this order is predicted to lose money. "
                 "Consider reducing the discount or the shipping cost.")
    elif label == "Low Profit":
        st.warning("Low expected profit. A lower discount may improve it.")
    else:
        st.success("This order is expected to be profitable.")

    st.caption(f"Model: {ev['best_name']} (R² = {ev['results'].loc[0, 'R2']:.2f} on test data). "
               "Estimates are approximate and should support, not replace, business judgement.")
