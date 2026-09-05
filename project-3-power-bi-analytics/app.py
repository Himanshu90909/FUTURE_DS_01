"""Python/Streamlit replacement for the Power BI analytics report."""
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
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    for column in ["Sales", "Quantity", "Discount", "Profit"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df.dropna(subset=["Order Date", "Sales", "Profit", "Quantity"])


def main():
    st.set_page_config(page_title="Power BI Sales Analytics", page_icon="🧭", layout="wide")
    st.title("🧭 Power BI Sales Analytics")
    st.caption("Interactive Python implementation of the Power BI report design")
    df = load_data()

    with st.sidebar:
        st.header("Report slicers")
        years = st.multiselect("Year", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
        categories = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
        region = st.selectbox("Region", ["All regions"] + sorted(df["Region"].unique()))
        subcategories = st.multiselect("Sub-category", sorted(df["Sub-Category"].unique()), default=sorted(df["Sub-Category"].unique()))

    filtered = df[df["Year"].isin(years) & df["Category"].isin(categories) & df["Sub-Category"].isin(subcategories)].copy()
    if region != "All regions":
        filtered = filtered[filtered["Region"] == region]

    sales = filtered["Sales"].sum()
    profit = filtered["Profit"].sum()
    prior = df[df["Year"].isin([year - 1 for year in years])]["Sales"].sum()
    yoy = (sales - prior) / prior if prior else 0

    kpi = st.columns(5)
    kpi[0].metric("Total sales", f"${sales:,.0f}")
    kpi[1].metric("Total profit", f"${profit:,.0f}")
    kpi[2].metric("Profit margin", f"{profit / sales:.1%}" if sales else "0.0%")
    kpi[3].metric("Sales YoY", f"{yoy:.1%}")
    kpi[4].metric("Customers", f"{filtered['Customer ID'].nunique():,}")

    if filtered.empty:
        st.warning("No records match the selected slicers.")
        return

    overview, product, customer = st.tabs(["Executive overview", "Product and geography", "Customer and fulfillment"])
    with overview:
        monthly = filtered.groupby("Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        category = filtered.groupby("Category", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        col1, col2 = st.columns(2)
        col1.plotly_chart(px.line(monthly, x="Month", y=["Sales", "Profit"], markers=True, title="Sales and profit over time"), use_container_width=True)
        col2.plotly_chart(px.bar(category, x="Category", y=["Sales", "Profit"], barmode="group", title="Category performance"), use_container_width=True)

    with product:
        product_summary = filtered.groupby(["Category", "Sub-Category"], as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        state = filtered.groupby("State", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).nlargest(15, "Sales")
        col1, col2 = st.columns(2)
        col1.plotly_chart(px.treemap(product_summary, path=["Category", "Sub-Category"], values="Sales", color="Profit", title="Sales hierarchy and profit"), use_container_width=True)
        col2.plotly_chart(px.bar(state.sort_values("Sales"), x="Sales", y="State", color="Profit", orientation="h", title="Top states by sales"), use_container_width=True)
        st.dataframe(product_summary.sort_values("Sales", ascending=False), use_container_width=True, hide_index=True)

    with customer:
        segment = filtered.groupby("Segment", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        ship = filtered.groupby("Ship Mode", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        col1, col2 = st.columns(2)
        col1.plotly_chart(px.bar(segment, x="Segment", y=["Sales", "Profit"], barmode="group", title="Customer segment performance"), use_container_width=True)
        col2.plotly_chart(px.bar(ship, x="Ship Mode", y=["Sales", "Profit"], barmode="group", title="Fulfillment performance"), use_container_width=True)
        st.plotly_chart(px.scatter(filtered.sample(min(3000, len(filtered)), random_state=42), x="Discount", y="Profit", color="Segment", hover_data=["State", "Category"], title="Discount impact on profit").add_hline(y=0, line_dash="dash"), use_container_width=True)


if __name__ == "__main__":
    main()