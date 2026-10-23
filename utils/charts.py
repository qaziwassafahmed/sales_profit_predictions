"""Reusable chart functions. Each takes a DataFrame and returns a matplotlib Figure."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

BG, PANEL, TEXT, GRID = "#0A0A0A", "#12121A", "#F2F2F2", "#2A2A36"
BLUE, ROSE = "#1FB6E8", "#FF2D95"   # Cerulean (brightened for dark bg) and Neon Rose
sns.set_theme(style="darkgrid", rc={
    "figure.facecolor": BG, "axes.facecolor": PANEL, "savefig.facecolor": BG,
    "axes.edgecolor": GRID, "grid.color": GRID, "text.color": TEXT,
    "axes.labelcolor": TEXT, "xtick.color": TEXT, "ytick.color": TEXT,
    "axes.titlecolor": TEXT, "legend.facecolor": PANEL, "legend.labelcolor": TEXT,
})
NEON_CMAP = LinearSegmentedColormap.from_list("neon", [ROSE, PANEL, BLUE])
MONEY = "{x:,.0f}"


def _finish(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    return ax.figure


def _monthly(df, col, title, ylabel):
    m = df.groupby(df["Order_Date"].dt.to_period("M"))[col].sum()
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(m.index.astype(str), m.values, marker="o", markersize=3, color=BLUE)
    ax.set_xticks(range(0, len(m), 6))
    ax.set_xticklabels(m.index.astype(str)[::6], rotation=45)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    return _finish(ax, title, "Month", ylabel)


def monthly_sales(df):
    return _monthly(df, "Total_Sale", "Monthly Sales Trend", "Total Sales")


def monthly_profit(df):
    return _monthly(df, "Profit", "Monthly Profit Trend", "Total Profit")


def _bar(df, group, value, title, xlabel, ylabel, top=None, horizontal=False, agg="sum"):
    s = df.groupby(group)[value].agg(agg).sort_values(ascending=False)
    if top:
        s = s.head(top)
    fig, ax = plt.subplots(figsize=(9, 5 if horizontal else 4.5))
    if horizontal:
        sns.barplot(x=s.values, y=[str(i)[:40] for i in s.index], ax=ax, color=BLUE)
        return _finish(ax, title, ylabel, xlabel)
    sns.barplot(x=s.index, y=s.values, ax=ax, color=BLUE)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    return _finish(ax, title, xlabel, ylabel)


def sales_by_category(df):
    return _bar(df, "Category", "Total_Sale", "Sales by Category", "Category", "Total Sales")


def profit_by_category(df):
    return _bar(df, "Category", "Profit", "Profit by Category", "Category", "Total Profit")


def sales_by_subcategory(df):
    return _bar(df, "Sub_Category", "Total_Sale", "Sales by Sub-Category", "Sub-Category", "Total Sales")


def profit_by_subcategory(df):
    return _bar(df, "Sub_Category", "Profit", "Profit by Sub-Category", "Sub-Category", "Total Profit")


def top_products_sales(df, n=10):
    return _bar(df, "Product_Name", "Total_Sale", f"Top {n} Products by Sales",
                "Product", "Total Sales", top=n, horizontal=True)


def top_products_profit(df, n=10):
    return _bar(df, "Product_Name", "Profit", f"Top {n} Products by Profit",
                "Product", "Total Profit", top=n, horizontal=True)


def sales_by_region(df):
    return _bar(df, "Region", "Total_Sale", "Sales by Region", "Region", "Total Sales")


def profit_by_region(df):
    return _bar(df, "Region", "Profit", "Profit by Region", "Region", "Total Profit")


def top_countries_sales(df, n=10):
    return _bar(df, "Country", "Total_Sale", f"Top {n} Countries by Sales",
                "Country", "Total Sales", top=n, horizontal=True)


def top_customers(df, n=10):
    return _bar(df, "Customer_Name", "Total_Sale", f"Top {n} Customers by Sales",
                "Customer", "Total Sales", top=n, horizontal=True)


def discount_vs_profit_scatter(df, sample=5000):
    d = df.sample(min(sample, len(df)), random_state=42)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(d["Discount"], d["Profit"], alpha=0.35, s=10, color=BLUE)
    ax.axhline(0, color=ROSE, linewidth=1)
    return _finish(ax, "Discount vs Profit (sample of orders)", "Discount", "Profit")


def avg_profit_by_discount_level(df):
    order = ["No Discount", "Low", "Medium", "High"]
    s = df.groupby("Discount_Level")["Profit"].mean().reindex(order)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=s.index, y=s.values, ax=ax, color=BLUE)
    return _finish(ax, "Average Profit per Order by Discount Level", "Discount Level", "Average Profit")


def loss_rate_by_subcategory(df):
    s = (df.groupby("Sub_Category")["Is_Loss"].mean() * 100).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.barplot(x=s.index, y=s.values, ax=ax, color=ROSE)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    return _finish(ax, "Loss-Making Order Rate by Sub-Category", "Sub-Category", "% of Orders with Loss")


def ship_mode_distribution(df):
    s = df["Ship_Mode"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.barplot(x=s.index, y=s.values, ax=ax, color=BLUE)
    return _finish(ax, "Orders by Ship Mode", "Ship Mode", "Number of Orders")


def segment_performance(df):
    s = df.groupby("Segment")[["Total_Sale", "Profit"]].sum().reset_index().melt(
        id_vars="Segment", var_name="Measure", value_name="Amount")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(data=s, x="Segment", y="Amount", hue="Measure", ax=ax, palette=[BLUE, ROSE])
    return _finish(ax, "Sales and Profit by Customer Segment", "Segment", "Amount")


def correlation_heatmap(df):
    cols = ["Total_Sale", "Profit", "Quantity", "Discount", "Shipping_Cost",
            "Unit_Price", "Discount_Amount", "Profit_Margin", "Order_Month"]
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df[cols].corr(), annot=True, fmt=".2f", cmap=NEON_CMAP, center=0, ax=ax)
    return _finish(ax, "Correlation Heatmap of Numerical Features", "", "")


ALL_EDA_CHARTS = {
    "monthly_sales": monthly_sales, "monthly_profit": monthly_profit,
    "sales_by_category": sales_by_category, "profit_by_category": profit_by_category,
    "sales_by_subcategory": sales_by_subcategory, "profit_by_subcategory": profit_by_subcategory,
    "top_products_sales": top_products_sales, "top_products_profit": top_products_profit,
    "sales_by_region": sales_by_region, "profit_by_region": profit_by_region,
    "top_countries_sales": top_countries_sales, "top_customers": top_customers,
    "discount_vs_profit": discount_vs_profit_scatter,
    "avg_profit_by_discount": avg_profit_by_discount_level,
    "loss_rate_subcategory": loss_rate_by_subcategory,
    "ship_mode": ship_mode_distribution, "segment_performance": segment_performance,
    "correlation_heatmap": correlation_heatmap,
}


# ---------- Model evaluation charts ----------
def actual_vs_predicted(y_true, y_pred, name):
    fig, ax = plt.subplots(figsize=(6.5, 6))
    ax.scatter(y_true, y_pred, alpha=0.3, s=10, color=BLUE)
    lo, hi = min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())
    ax.plot([lo, hi], [lo, hi], color=ROSE, linewidth=1, label="Perfect prediction")
    ax.legend()
    return _finish(ax, f"Actual vs Predicted Profit ({name})", "Actual Profit", "Predicted Profit")


def residual_distribution(y_true, y_pred, name):
    residuals = y_true - y_pred
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.histplot(residuals, bins=80, kde=True, ax=ax, color=BLUE)
    ax.set_xlim(residuals.quantile(0.01), residuals.quantile(0.99))
    return _finish(ax, f"Residual Distribution ({name})", "Residual (Actual - Predicted)", "Count")


def model_comparison_chart(results):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    sns.barplot(data=results, x="Model", y="R2", ax=axes[0], color=BLUE)
    axes[0].set_title("R² Score by Model (higher is better)", fontweight="bold")
    sns.barplot(data=results, x="Model", y="RMSE", ax=axes[1], color=ROSE)
    axes[1].set_title("RMSE by Model (lower is better)", fontweight="bold")
    for a in axes:
        plt.setp(a.get_xticklabels(), rotation=20, ha="right")
        a.set_xlabel("Model")
    plt.tight_layout()
    return fig


def feature_importance_chart(importance, name, top=10):
    s = importance.head(top)[::-1]
    labels = [i.replace("num__", "").replace("cat__", "") for i in s.index]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(labels, s.values, color=BLUE)
    return _finish(ax, f"Top {top} Feature Importances ({name})", "Importance", "Feature")
