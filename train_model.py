"""Train, compare and save the profit regression models (CPU only)."""
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

# Total_Sale is excluded (it contains the profit effect = data leakage).
# IDs and customer names are excluded (assignment rule).
NUMERIC = ["Quantity", "Unit_Price", "Discount", "Shipping_Cost", "Order_Month"]
CATEGORICAL = ["Category", "Sub_Category", "Segment", "Ship_Mode",
               "Order_Priority", "Market", "Region"]
TARGET = "Profit"

df = pd.read_csv("data/clean_data.csv", parse_dates=["Order_Date"])
X, y = df[NUMERIC + CATEGORICAL], df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Train:", X_train.shape, "Test:", X_test.shape)


def make_pipeline(model):
    prep = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    return Pipeline([("prep", prep), ("model", model)])


models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(max_depth=8, min_samples_leaf=10, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=14, min_samples_leaf=5,
                                           n_jobs=-1, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=150, max_depth=4,
                                                   learning_rate=0.1, random_state=42),
}

rows, fitted, preds = [], {}, {}
for name, model in models.items():
    start = time.time()
    pipe = make_pipeline(model).fit(X_train, y_train)
    p = pipe.predict(X_test)
    mse = mean_squared_error(y_test, p)
    rows.append({"Model": name,
                 "MAE": mean_absolute_error(y_test, p), "MSE": mse,
                 "RMSE": np.sqrt(mse), "R2": r2_score(y_test, p),
                 "Train_Seconds": round(time.time() - start, 1)})
    fitted[name], preds[name] = pipe, p
    print(f"{name:20s} R2={rows[-1]['R2']:.3f}  RMSE={rows[-1]['RMSE']:.1f}  ({rows[-1]['Train_Seconds']}s)")

results = pd.DataFrame(rows).sort_values("R2", ascending=False).reset_index(drop=True)
best_name = results.loc[0, "Model"]
print("\n", results.round(3).to_string(index=False))
print("\nBest model:", best_name)

# Feature importance (tree models)
feature_names = fitted[best_name].named_steps["prep"].get_feature_names_out()
importance = {}
for name in ["Decision Tree", "Random Forest", "Gradient Boosting"]:
    imp = pd.Series(fitted[name].named_steps["model"].feature_importances_, index=feature_names)
    importance[name] = imp.sort_values(ascending=False)
print("\nTop features (Random Forest):\n", importance["Random Forest"].head(8).round(3))

# Save everything the Streamlit app needs
joblib.dump(fitted[best_name], "models/model.pkl", compress=3)
joblib.dump({
    "results": results,
    "y_test": y_test.reset_index(drop=True),
    "predictions": {k: pd.Series(v) for k, v in preds.items()},
    "importance": importance,
    "best_name": best_name,
    "numeric": NUMERIC, "categorical": CATEGORICAL,
    "train_shape": X_train.shape, "test_shape": X_test.shape,
}, "models/evaluation.pkl", compress=3)
print("\nSaved models/model.pkl and models/evaluation.pkl")
