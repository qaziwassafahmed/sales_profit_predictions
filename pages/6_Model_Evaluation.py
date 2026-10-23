import streamlit as st

from utils.style import apply_style

from utils import charts
from utils.data_loader import load_evaluation

st.set_page_config(page_title="Model Evaluation", page_icon="🤖", layout="wide")
apply_style()
st.title("🤖 Model Evaluation")
ev = load_evaluation()
results, best = ev["results"], ev["best_name"]

st.success(f"Best model: **{best}** (highest R², lowest error)")
st.subheader("Model comparison")
st.dataframe(results.style.format({"MAE": "{:.2f}", "MSE": "{:,.0f}", "RMSE": "{:.2f}", "R2": "{:.3f}"}))
st.pyplot(charts.model_comparison_chart(results))

st.subheader("Predictions and errors")
name = st.selectbox("Choose a model", list(ev["predictions"].keys()),
                    index=list(ev["predictions"].keys()).index(best))
y, p = ev["y_test"], ev["predictions"][name]
a, b = st.columns(2)
a.pyplot(charts.actual_vs_predicted(y, p, name))
b.pyplot(charts.residual_distribution(y, p, name))

st.subheader("Feature importance")
tree_name = st.selectbox("Tree-based model", list(ev["importance"].keys()), index=1)
st.pyplot(charts.feature_importance_chart(ev["importance"][tree_name], tree_name))

with st.expander("Why were some columns excluded? (data leakage)"):
    st.markdown(
        """
- **Total_Sale** already contains the effect of price, quantity and discount together with profit
  behaviour, and is not a clean input for predicting profit before the order is complete.
  The model uses *Unit_Price* and *Quantity* instead.
- **Order_ID, Customer_ID, Customer_Name** are identifiers / personal names, not real drivers of profit.
- Preprocessing (scaling and one-hot encoding) is fitted **only on the training data** inside a pipeline.
"""
    )
st.caption(f"Train shape: {ev['train_shape']}  |  Test shape: {ev['test_shape']}")
