"""Interactive Python dashboard for Project 1: sales performance analysis."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "superstore_sales.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    for column in ["Order Date", "Ship Date"]:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    for column in ["Sales", "Quantity", "Discount", "Profit"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df["Profit Margin"] = df["Profit"].div(
        df["Sales"].where(df["Sales"].ne(0))
    ).fillna(0)
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df.dropna(subset=["Order Date", "Sales", "Profit", "Quantity"])


def money(value):
    return f"${value:,.0f}"


def main():
    st.title("📊 Python Sales Performance Analysis")
    st.caption("Interactive implementation of the Future Interns sales analytics project")
    df = load_data()

    with st.sidebar:
        st.header("Filters")
        min_date, max_date = df["Order Date"].min().date(), df["Order Date"].max().date()
        dates = st.date_input("Order date", (min_date, max_date), min_value=min_date, max_value=max_date)
        regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
        categories = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
        segments = st.multiselect("Segment", sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique()))

    start, end = (dates if isinstance(dates, tuple) and len(dates) == 2 else (min_date, max_date))
    filtered = df[
        df["Order Date"].dt.date.between(start, end)
        & df["Region"].isin(regions)
        & df["Category"].isin(categories)
        & df["Segment"].isin(segments)
    ].copy()

    sales = filtered["Sales"].sum()
    profit = filtered["Profit"].sum()
    margin = profit / sales if sales else 0
    kpi = st.columns(4)
    kpi[0].metric("Sales", money(sales))
    kpi[1].metric("Profit", money(profit))
    kpi[2].metric("Profit margin", f"{margin:.1%}")
    kpi[3].metric("Orders", f"{filtered['Order ID'].nunique():,}")

    if filtered.empty:
        st.warning("No records match the selected filters.")
        return

    left, right = st.columns(2)
    monthly = filtered.groupby("Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    left.plotly_chart(
        px.line(monthly, x="Month", y=["Sales", "Profit"], markers=True, title="Monthly sales and profit"),
        use_container_width=True,
    )
    region = filtered.groupby("Region", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    right.plotly_chart(
        px.bar(region, x="Region", y=["Sales", "Profit"], barmode="group", title="Regional performance"),
        use_container_width=True,
    )

    left, right = st.columns(2)
    products = (
        filtered.groupby(["Product Name", "Category"], as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .nlargest(10, "Sales")
        .sort_values("Sales")
    )
    left.plotly_chart(
        px.bar(products, x="Sales", y="Product Name", color="Category", orientation="h", title="Top 10 products by sales"),
        use_container_width=True,
    )
    right.plotly_chart(
        px.scatter(
            filtered.sample(min(3000, len(filtered)), random_state=42),
            x="Discount",
            y="Profit",
            color="Category",
            hover_data=["Product Name", "Region"],
            title="Discount versus profit",
        ).add_hline(y=0, line_dash="dash"),
        use_container_width=True,
    )

    st.subheader("Filtered detail")
    st.dataframe(
        filtered[["Order ID", "Order Date", "Region", "Category", "Sub-Category", "Sales", "Profit"]]
        .sort_values("Sales", ascending=False)
        .head(100),
        use_container_width=True,
        hide_index=True,
    )


if __name__ == "__main__":
    main()