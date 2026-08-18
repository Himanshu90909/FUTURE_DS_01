"""Future Interns Task 1: Business Sales Performance Analytics.

The script reads the repository's Amazon product dataset, cleans monetary and
percentage fields, computes business KPIs, exports summary tables, and creates
charts for revenue, category, product, and rating analysis.
"""
from pathlib import Path
import re

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "amazon.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="talk")
PALETTE = "#2563eb"
ACCENT = "#f59e0b"


def parse_money(value):
    if pd.isna(value):
        return float("nan")
    cleaned = re.sub(r"[^0-9.]", "", str(value).replace(",", ""))
    return float(cleaned) if cleaned else float("nan")


def parse_percent(value):
    if pd.isna(value):
        return float("nan")
    cleaned = re.sub(r"[^0-9.]", "", str(value))
    return float(cleaned) if cleaned else float("nan")


def parse_count(value):
    if pd.isna(value):
        return float("nan")
    cleaned = re.sub(r"[^0-9]", "", str(value))
    return int(cleaned) if cleaned else float("nan")


def save_table(df, name):
    df.to_csv(OUTPUT_DIR / name, index=False)


def main():
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip() for c in df.columns]

    for column in ["discounted_price", "actual_price"]:
        df[column] = df[column].map(parse_money)
    df["discount_percentage"] = df["discount_percentage"].map(parse_percent)
    df["rating_count"] = df["rating_count"].map(parse_count)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["category"] = df["category"].fillna("Unknown").str.split("|").str[0]
    df["product_name"] = df["product_name"].fillna("Unknown product")
    df["estimated_revenue"] = df["discounted_price"] * df["rating_count"]
    df["estimated_savings"] = (df["actual_price"] - df["discounted_price"]) * df["rating_count"]
    df = df.dropna(subset=["discounted_price", "rating_count", "rating"])

    category = (
        df.groupby("category", as_index=False)
        .agg(
            products=("product_id", "nunique"),
            estimated_revenue=("estimated_revenue", "sum"),
            average_discounted_price=("discounted_price", "mean"),
            average_rating=("rating", "mean"),
            review_count=("rating_count", "sum"),
        )
        .sort_values("estimated_revenue", ascending=False)
    )
    products = (
        df.groupby("product_name", as_index=False)
        .agg(
            category=("category", "first"),
            estimated_revenue=("estimated_revenue", "sum"),
            rating_count=("rating_count", "sum"),
            rating=("rating", "mean"),
            discounted_price=("discounted_price", "mean"),
        )
        .sort_values("estimated_revenue", ascending=False)
    )

    kpis = pd.DataFrame(
        {
            "metric": [
                "Products analyzed",
                "Categories analyzed",
                "Estimated revenue proxy",
                "Total ratings/reviews",
                "Average rating",
                "Average discount",
            ],
            "value": [
                len(df),
                df["category"].nunique(),
                df["estimated_revenue"].sum(),
                df["rating_count"].sum(),
                df["rating"].mean(),
                df["discount_percentage"].mean(),
            ],
        }
    )
    save_table(kpis, "kpis.csv")
    save_table(category, "category_performance.csv")
    save_table(products.head(20), "top_20_products.csv")

    fig, ax = plt.subplots(figsize=(12, 7))
    top = category.head(10).sort_values("estimated_revenue")
    ax.barh(top["category"], top["estimated_revenue"] / 1e6, color=PALETTE)
    ax.set_title("Estimated Revenue by Category (log scale)", weight="bold")
    ax.set_xscale("log")
    ax.set_xlabel("Estimated revenue proxy (₹ millions, log scale)")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "revenue_by_category.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 8))
    top_products = products.head(10).sort_values("estimated_revenue")
    labels = top_products["product_name"].str.slice(0, 38)
    ax.barh(labels, top_products["estimated_revenue"] / 1e6, color=ACCENT)
    ax.set_title("Top Products by Estimated Revenue Proxy", weight="bold", pad=18)
    ax.tick_params(axis="y", labelsize=11)
    ax.set_xlabel("Estimated revenue proxy (₹ millions)")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "top_products.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 7))
    sns.scatterplot(
        data=df,
        x="rating_count",
        y="rating",
        hue="discount_percentage",
        size="estimated_revenue",
        sizes=(30, 600),
        palette="viridis",
        alpha=0.75,
        ax=ax,
        legend=False,
    )
    ax.set_xscale("log")
    ax.set_title("Customer Engagement and Product Rating", weight="bold")
    ax.set_xlabel("Rating count (log scale)")
    ax.set_ylabel("Average rating")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "rating_engagement.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df["discount_percentage"], bins=15, color=PALETTE, ax=ax)
    ax.set_title("Distribution of Product Discounts", weight="bold")
    ax.set_xlabel("Discount percentage")
    ax.set_ylabel("Products")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "discount_distribution.png", dpi=180)
    plt.close(fig)

    insights = [
        f"The analysis covers {len(df):,} products across {df['category'].nunique()} top-level categories.",
        f"The highest estimated-revenue category is {category.iloc[0]['category']} with an estimated revenue proxy of ₹{category.iloc[0]['estimated_revenue']:,.0f}.",
        f"The highest estimated-revenue product is {products.iloc[0]['product_name'][:100]}.",
        f"The mean product rating is {df['rating'].mean():.2f}/5, while the mean discount is {df['discount_percentage'].mean():.1f}%.",
        "Regional performance cannot be assessed because the source file has no region, geography, or seller-location field.",
        "The revenue metric is a prioritization proxy calculated as discounted price multiplied by rating count; it should not be interpreted as audited sales revenue because unit sales are not included in the source data.",
    ]
    (OUTPUT_DIR / "insights.txt").write_text("\n".join(f"- {item}" for item in insights) + "\n", encoding="utf-8")

    print("Analysis completed")
    print(kpis.to_string(index=False))
    print("Top category:", category.iloc[0]["category"])
    print("Top product:", products.iloc[0]["product_name"][:100])


if __name__ == "__main__":
    main()
