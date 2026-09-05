"""Python/Streamlit replacement for the Excel sales dashboard."""
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
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df.dropna(subset=["Order Date", "Sales", "Profit", "Quantity"])


def main():
    st.title("📈 Executive Sales Dashboard")
    st.caption("A Python implementation of the Excel dashboard deliverable")
    df = load_data()

    with st.sidebar:
        st.header("Dashboard filters")
        years = st.multiselect("Order year", sorted(df["Order Date"].dt.year.unique()), default=sorted(df["Order Date"].dt.year.unique()))
        regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
        ship_modes = st.multiselect("Ship mode", sorted(df["Ship Mode"].unique()), default=sorted(df["Ship Mode"].unique()))

    filtered = df[
        df["Order Date"].dt.year.isin(years)
        & df["Region"].isin(regions)
        & df["Ship Mode"].isin(ship_modes)
    ].copy()
    sales = filtered["Sales"].sum()
    profit = filtered["Profit"].sum()

    kpi = st.columns(5)
    kpi[0].metric("Sales", f"${sales:,.0f}")
    kpi[1].metric("Profit", f"${profit:,.0f}")
    kpi[2].metric("Margin", f"{profit / sales:.1%}" if sales else "0.0%")
    kpi[3].metric("Orders", f"{filtered['Order ID'].nunique():,}")
    kpi[4].metric("Units", f"{filtered['Quantity'].sum():,.0f}")

    if filtered.empty:
        st.warning("No records match the selected filters.")
        return

    tab1, tab2, tab3 = st.tabs(["Executive view", "Category and product", "Data export"])
    with tab1:
        monthly = filtered.groupby("Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        region = filtered.groupby("Region", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        col1, col2 = st.columns(2)
        col1.plotly_chart(px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly sales trend"), use_container_width=True)
        col2.plotly_chart(px.bar(region, x="Region", y=["Sales", "Profit"], barmode="group", title="Sales and profit by region"), use_container_width=True)

        segment = filtered.groupby("Segment", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        ship = filtered.groupby("Ship Mode", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        col1, col2 = st.columns(2)
        col1.plotly_chart(px.pie(segment, names="Segment", values="Sales", title="Sales mix by segment"), use_container_width=True)
        col2.plotly_chart(px.bar(ship, x="Ship Mode", y="Profit", color="Ship Mode", title="Profit by ship mode"), use_container_width=True)

    with tab2:
        category = filtered.groupby(["Category", "Sub-Category"], as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        products = filtered.groupby(["Product Name", "Category"], as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).nlargest(15, "Sales")
        col1, col2 = st.columns(2)
        col1.plotly_chart(px.bar(category.sort_values("Profit"), x="Profit", y="Sub-Category", color="Category", orientation="h", title="Profit by sub-category"), use_container_width=True)
        col2.plotly_chart(px.bar(products.sort_values("Sales"), x="Sales", y="Product Name", color="Category", orientation="h", title="Top 15 products"), use_container_width=True)
        st.dataframe(category.sort_values("Sales", ascending=False), use_container_width=True, hide_index=True)

    with tab3:
        export = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("Download filtered CSV", export, "filtered_sales_data.csv", "text/csv")
        st.dataframe(filtered.head(200), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()