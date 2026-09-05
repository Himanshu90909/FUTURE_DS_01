# FUTURE_DS_01 — Business Sales Performance Analytics

This project completes **Future Interns Data Science & Analytics Task 1** using a real transaction-level Superstore sales dataset. The project is designed for both a client-ready **Excel dashboard** and an interactive **Power BI report**.

> The dataset is a sample Superstore dataset for portfolio and dashboard practice. It should not be presented as audited company financial data.

## Deliverables

| File | Purpose |
| --- | --- |
| `superstore_sales.csv` | Power BI-ready transaction-level sales dataset |
| `analysis.py` | Reproducible Python analysis and chart-generation pipeline |
| `FUTURE_DS_01_Excel_Dashboard.xlsx` | Excel dashboard with KPI cards, charts, summary sheets, and methodology notes |
| `POWER_BI_GUIDE.md` | Power BI page design, loading, slicer, and model guidance |
| `measures.dax` | Reusable Power BI measures for sales, profit, margin, orders, and time intelligence |
| `outputs/kpis.csv` | Executive KPI table |
| `outputs/region_performance.csv` | Sales, profit, orders, quantity, and discount by region |
| `outputs/category_performance.csv` | Sales and profit by category and sub-category |
| `outputs/top_25_products.csv` | Top products ranked by sales |
| `outputs/monthly_trend.csv` | Monthly sales, profit, orders, and quantity trend |
| `outputs/segment_performance.csv` | Customer-segment performance |
| `outputs/ship_mode_performance.csv` | Shipping-mode performance |
| `outputs/*.png` | Supporting charts for the analysis report |

## Portfolio project links

The repository is organized into three portfolio-ready project folders so
each deliverable can be shared separately on LinkedIn:

1. [Project 1 — Python Sales Performance Analysis](project-1-python-sales-analysis/)
2. [Project 2 — Excel Sales Dashboard](project-2-excel-sales-dashboard/)
3. [Project 3 — Power BI Sales Analytics](project-3-power-bi-analytics/)

## Excel dashboard

Open `FUTURE_DS_01_Excel_Dashboard.xlsx` in Microsoft Excel or compatible spreadsheet software. The `Dashboard` worksheet provides KPI cards, regional sales and profit, monthly sales trend, and executive recommendations. Supporting sheets include `Clean_Data`, `Region_Summary`, `SubCategory_Summary`, `Top_Products`, `Monthly_Trend`, and `PowerBI_Guide`. The Python-generated CSV and PNG outputs are written to `outputs/`.

The dashboard covers the business questions required by the brief: revenue trends over time, top-selling products, category and sub-category performance, regional performance, customer segments, shipping modes, discounts, profit, and profit margin.

## Python dashboards

GitHub previews source files and folders, but it does not run Streamlit apps
inside a folder page. Each portfolio folder now includes a Python dashboard
that can be launched from the repository root:

```bash
streamlit run project-1-python-sales-analysis/app.py
streamlit run project-2-excel-sales-dashboard/app.py
streamlit run project-3-power-bi-analytics/app.py
```

To open all three from one dashboard:

```bash
streamlit run app.py
```

Install the shared dependencies first:

```bash
python3 -m pip install -r requirements.txt
```

The three apps use the same cleaned transaction dataset while presenting
different views: exploratory Python analysis, an executive dashboard, and
Power BI-style slicers and measures.

## Power BI workflow

In Power BI Desktop, select **Get data → Text/CSV**, load `superstore_sales.csv`, and verify that `Order Date` and `Ship Date` are dates while `Sales`, `Profit`, and `Quantity` are numeric. Use `POWER_BI_GUIDE.md` for the recommended report pages and `measures.dax` for reusable measures.

Recommended report pages are Executive Overview, Regional Performance, Product & Category, and Customer & Fulfillment. Add slicers for order date, region, state, category, sub-category, segment, and ship mode. For year-over-year analysis, create a Calendar table and relate it to `SalesData[Order Date]`.

## Python reproduction

Install the dependencies and regenerate the outputs:

```bash
python3 -m pip install -r requirements.txt
python3 analysis.py
python3 build_excel_dashboard.py
```

The analysis is based on the cleaned Superstore transaction file sourced from the public [WuCandice/Superstore-Sales-Analysis repository](https://github.com/WuCandice/Superstore-Sales-Analysis), which documents 9,993 U.S. sales transactions from 2019–2022.

## Key findings

The dataset contains **5,009 distinct orders**, **793 customers**, and **1,862 products**. Total sales are approximately **$2.30 million**, total profit is approximately **$286.41 thousand**, and overall profit margin is approximately **12.5%**. The generated outputs provide the detailed regional, category, product, monthly, segment, and shipping analyses needed for the Power BI report.

Before making operational decisions, enrich the dataset with actual business transactions, costs, returns, and audited financial measures. The current deliverable is intended as a professional portfolio and internship submission.

## Author

Manus AI, prepared for the Future Interns Data Science & Analytics track.
