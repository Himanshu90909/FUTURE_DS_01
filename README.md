# FUTURE_DS_01 — Business Sales Performance Analytics

This project completes **Future Interns Data Science & Analytics Task 1** using the Amazon product dataset already present in the repository. The analysis identifies revenue-prioritization trends, top products, high-value categories, pricing patterns, and customer-engagement signals.

> The dataset does not include audited unit sales. Therefore, this project uses an **estimated revenue proxy** defined as `discounted_price × rating_count` for prioritization only. It must not be presented as official company revenue.

## Project structure

| Path | Purpose |
| --- | --- |
| `analysis.py` | Reproducible cleaning, KPI computation, insight generation, and visualization script |
| `outputs/kpis.csv` | Executive KPI table |
| `outputs/category_performance.csv` | Category-level performance table |
| `outputs/top_20_products.csv` | Top products ranked by estimated revenue proxy |
| `outputs/insights.txt` | Automatically generated findings and analytical limitation |
| `outputs/*.png` | Publication-ready charts for the report or dashboard |

## How to run

From the repository root, install the dependencies and run the analysis:

```bash
python3 -m pip install -r requirements.txt
python3 analysis.py
```

The script reads `amazon.csv` from the repository root and writes all generated deliverables to `outputs/`.

## Analytical approach

The pipeline standardizes currency, percentage, rating, and rating-count fields; extracts the top-level product category; removes records without usable pricing, rating, or engagement values; and calculates an estimated revenue proxy. It then summarizes performance by category and product, produces an executive KPI table, and creates charts for category revenue, top products, rating engagement, and discount distribution.

## Business insights and recommendations

The generated outputs support four practical decisions. First, category-level estimated revenue can guide assortment and inventory prioritization. Second, the top-product table can identify products for merchandising, promotion, or stock monitoring. Third, the rating-versus-engagement chart can distinguish products with broad customer attention from products with limited evidence. Finally, discount distribution can inform promotion governance and help identify whether deep discounts are concentrated in specific parts of the catalog.

Before making operational decisions, the business should join this product-level dataset to transactional sales, order dates, units sold, returns, fulfillment cost, and margin data. That enrichment would convert the current prioritization proxy into a defensible sales-performance model.

## Author

Manus AI, prepared for the Future Interns Data Science & Analytics track.
