# Power BI Implementation Guide

The revised project uses `superstore_sales.csv`, a real transaction-level Superstore dataset containing order dates, shipping dates, customer segments, geography, product hierarchy, sales, quantity, discount, and profit. This structure is substantially better suited to the Future Interns **Business Sales Performance Analytics** task than a catalog-only file because it supports time, regional, product, and profitability analysis.

## Load the data

In Power BI Desktop, choose **Get data → Text/CSV**, select `superstore_sales.csv`, and confirm that `Order Date` and `Ship Date` are typed as dates, `Sales`, `Profit`, and `Quantity` are numeric, and `Discount` is decimal. The file is already cleaned and ready for import.

## Recommended report pages

| Page | Recommended visuals | Business question |
| --- | --- | --- |
| Executive Overview | KPI cards for Sales, Profit, Profit Margin, Orders; monthly sales line chart; regional sales/profit bar chart | How is the business performing overall? |
| Regional Performance | Filled map or bar chart by Region and State; Sales vs Profit scatter; region slicer | Which regions drive growth and which require attention? |
| Product & Category | Treemap by Category/Sub-Category; top-product table; sales-versus-profit scatter | Which products and categories are high-value or loss-making? |
| Customer & Fulfillment | Segment bar chart; Ship Mode comparison; discount/profit scatter | How do customer mix, shipping, and discounting affect performance? |

## Suggested slicers

Use `Order Date`, `Region`, `State`, `Category`, `Sub-Category`, `Segment`, and `Ship Mode` as slicers. Add a date hierarchy or a dedicated Calendar table for year, quarter, month, and month number analysis.

## Data model

For a portfolio-ready report, keep `superstore_sales.csv` as the fact table and add a Calendar table related to `Calendar[Date]` → `SalesData[Order Date]`. The current CSV can also be used as a single-table model for a quick dashboard.

## Interpretation note

This is a sample Superstore dataset used for portfolio and dashboard practice. It should not be represented as audited financial data. The project focuses on finding performance trends, top categories, regional differences, and profitability opportunities.
