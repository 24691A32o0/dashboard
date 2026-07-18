"""
Sales Analytics Dashboard
--------------------------
An interactive sales analytics dashboard built with Streamlit + Plotly.

Run locally:
    streamlit run app.py
"""

import io
import os
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_PATH = os.path.join(APP_DIR, "data", "sales_data.csv")


# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------
@st.cache_data
def generate_sample_data(n_rows: int = 500, seed: int = 42) -> pd.DataFrame:
    """Fallback synthetic dataset, used only if the bundled CSV is missing."""
    rng = np.random.default_rng(seed)
    products = ["Widget A", "Widget B", "Gadget X", "Gadget Y", "Gizmo Z"]
    categories = {"Widget A": "Widgets", "Widget B": "Widgets",
                  "Gadget X": "Gadgets", "Gadget Y": "Gadgets", "Gizmo Z": "Gizmos"}
    regions = ["North", "South", "East", "West"]

    dates = pd.date_range("2024-01-01", "2024-12-31", periods=n_rows)
    product_choices = rng.choice(products, size=n_rows)
    quantity = rng.integers(1, 20, size=n_rows)
    unit_price = rng.uniform(10, 200, size=n_rows).round(2)
    sales = quantity * unit_price
    profit = (sales * rng.uniform(0.05, 0.35, size=n_rows)).round(2)

    df = pd.DataFrame({
        "Order_ID": [f"ORD-{i:05d}" for i in range(n_rows)],
        "Date": dates,
        "Product": product_choices,
        "Category": [categories[p] for p in product_choices],
        "Region": rng.choice(regions, size=n_rows),
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Sales": sales.round(2),
        "Profit": profit,
    })
    return df


@st.cache_data
def load_data(path_or_buffer) -> pd.DataFrame:
    df = pd.read_csv(path_or_buffer)

    # Basic cleaning, mirroring the original notebook's steps
    df.columns = [c.strip() for c in df.columns]
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.drop_duplicates()
    df = df.dropna(subset=["Date"]) if "Date" in df.columns else df

    if "Sales" not in df.columns and {"Quantity", "Unit_Price"}.issubset(df.columns):
        df["Sales"] = df["Quantity"] * df["Unit_Price"]

    if "Month" not in df.columns and "Date" in df.columns:
        df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()

    return df


def kpi_card(col, label, value, delta=None, prefix="", suffix=""):
    formatted = f"{prefix}{value:,.0f}{suffix}"
    col.metric(label, formatted, delta)


# --------------------------------------------------------------------------
# Sidebar — data source + filters
# --------------------------------------------------------------------------
st.sidebar.title("📊 Sales Dashboard")
st.sidebar.caption("Upload your own CSV or explore the bundled sample data.")

uploaded_file = st.sidebar.file_uploader("Upload sales CSV", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success(f"Loaded {uploaded_file.name}")
elif os.path.exists(DEFAULT_DATA_PATH):
    df = load_data(DEFAULT_DATA_PATH)
    st.sidebar.info("Using bundled sample dataset")
else:
    df = generate_sample_data()
    st.sidebar.warning(
        "Bundled sample file not found at `data/sales_data.csv` — "
        "showing generated placeholder data instead. Upload a CSV to use real data."
    )

required_cols = {"Date", "Product", "Category", "Region", "Sales"}
missing = required_cols - set(df.columns)
if missing:
    st.error(
        f"The dataset is missing required column(s): {', '.join(missing)}. "
        "Expected columns include Date, Product, Category, Region, Sales, Profit."
    )
    st.stop()

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

regions = sorted(df["Region"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

categories = sorted(df["Category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

products = sorted(df["Product"].dropna().unique().tolist())
selected_products = st.sidebar.multiselect("Product", products, default=products)

# Apply filters
mask = (
    (df["Date"] >= pd.to_datetime(start_date))
    & (df["Date"] <= pd.to_datetime(end_date))
    & (df["Region"].isin(selected_regions))
    & (df["Category"].isin(selected_categories))
    & (df["Product"].isin(selected_products))
)
fdf = df.loc[mask].copy()

st.sidebar.markdown("---")
csv_bytes = fdf.to_csv(index=False).encode("utf-8")
st.sidebar.download_button(
    "⬇️ Download filtered data",
    data=csv_bytes,
    file_name="filtered_sales_data.csv",
    mime="text/csv",
)

# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.title("📊 Sales Analytics Dashboard")
st.caption(
    f"Showing **{len(fdf):,}** of **{len(df):,}** orders "
    f"between **{pd.to_datetime(start_date).date()}** and **{pd.to_datetime(end_date).date()}**"
)

if fdf.empty:
    st.warning("No data matches the selected filters. Try widening your filter selection.")
    st.stop()

# --------------------------------------------------------------------------
# KPI row
# --------------------------------------------------------------------------
total_sales = fdf["Sales"].sum()
total_profit = fdf["Profit"].sum() if "Profit" in fdf.columns else np.nan
total_orders = fdf["Order_ID"].nunique() if "Order_ID" in fdf.columns else len(fdf)
avg_order_value = total_sales / total_orders if total_orders else 0
profit_pct = (total_profit / total_sales * 100) if total_sales else 0

k1, k2, k3, k4, k5 = st.columns(5)
kpi_card(k1, "Total Sales", total_sales, prefix="₹")
kpi_card(k2, "Total Profit", total_profit, prefix="₹")
kpi_card(k3, "Total Orders", total_orders)
kpi_card(k4, "Avg Order Value", avg_order_value, prefix="₹")
k5.metric("Profit Margin", f"{profit_pct:.1f}%")

st.markdown("---")

# --------------------------------------------------------------------------
# Charts row 1 — Product & Region
# --------------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Product-wise Sales")
    product_sales = (
        fdf.groupby("Product")["Sales"].sum().sort_values(ascending=False).reset_index()
    )
    fig = px.bar(
        product_sales,
        x="Product",
        y="Sales",
        color="Sales",
        color_continuous_scale="Blues",
        text_auto=".2s",
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Region-wise Sales Share")
    region_sales = fdf.groupby("Region")["Sales"].sum().reset_index()
    fig = px.pie(region_sales, names="Region", values="Sales", hole=0.45)
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------------------
# Charts row 2 — Monthly trend & Category
# --------------------------------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.subheader("Monthly Sales Trend")
    monthly = fdf.groupby(fdf["Date"].dt.to_period("M"))["Sales"].sum()
    monthly.index = monthly.index.to_timestamp()
    monthly = monthly.reset_index()
    fig = px.line(monthly, x="Date", y="Sales", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("Category-wise Profit")
    if "Profit" in fdf.columns:
        cat_profit = fdf.groupby("Category")["Profit"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(cat_profit, x="Category", y="Profit", color="Category")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No 'Profit' column found in this dataset.")

# --------------------------------------------------------------------------
# Top products / regions table
# --------------------------------------------------------------------------
st.markdown("---")
st.subheader("Top Performing Products")
top_n = st.slider("Number of products to show", 3, min(20, len(products)), 5)
top_products = (
    fdf.groupby("Product")
    .agg(Total_Sales=("Sales", "sum"), Total_Orders=("Order_ID", "nunique") if "Order_ID" in fdf.columns else ("Sales", "count"))
    .sort_values("Total_Sales", ascending=False)
    .head(top_n)
)
st.dataframe(top_products.style.format({"Total_Sales": "₹{:,.0f}"}), use_container_width=True)

# --------------------------------------------------------------------------
# Raw data explorer
# --------------------------------------------------------------------------
with st.expander("🔍 View raw filtered data"):
    st.dataframe(fdf, use_container_width=True)

st.caption("Built with Streamlit + Plotly · Sales Analytics Dashboard")
