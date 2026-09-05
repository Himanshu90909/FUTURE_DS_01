"""Future Interns Task 1: Business Sales Performance Analytics.

This pipeline uses the cleaned Superstore transaction CSV and produces
Power BI-ready summary tables and publication-ready charts.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / 'superstore_sales.csv'
OUTPUT_DIR = ROOT / 'outputs'
OUTPUT_DIR.mkdir(exist_ok=True)
sns.set_theme(style='whitegrid', context='talk')
REQUIRED_COLUMNS = {
    'Order ID', 'Order Date', 'Ship Date', 'Customer ID', 'Product ID',
    'Category', 'Sub-Category', 'Region', 'Segment', 'Ship Mode',
    'Sales', 'Quantity', 'Discount', 'Profit',
}


def load_data():
    """Load and normalize the transaction-level source data."""
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(
            f'Missing required columns in {DATA_PATH.name}: '
            f'{", ".join(sorted(missing))}'
        )

    for column in ['Order Date', 'Ship Date']:
        df[column] = pd.to_datetime(df[column], errors='coerce')
    for column in ['Sales', 'Quantity', 'Discount', 'Profit']:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    # The source stores this field as percentage points (33.75), while
    # Excel/Power BI percentage formats expect a decimal (0.3375).
    df['Profit Margin %'] = (
        df['Profit'].div(df['Sales'].where(df['Sales'].ne(0))).fillna(0)
    )
    return df


def main():
    df = load_data()
    df = df.dropna(subset=['Order Date', 'Sales', 'Profit', 'Quantity']).copy()
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)

    kpis = pd.DataFrame({
        'Metric': ['Orders', 'Customers', 'Products', 'Sales', 'Profit', 'Profit Margin', 'Quantity', 'Average Discount'],
        'Value': [
            df['Order ID'].nunique(), df['Customer ID'].nunique(), df['Product ID'].nunique(),
            df['Sales'].sum(), df['Profit'].sum(), df['Profit'].sum() / df['Sales'].sum(),
            df['Quantity'].sum(), df['Discount'].mean(),
        ],
    })
    region = df.groupby('Region', as_index=False).agg(Orders=('Order ID', 'nunique'), Sales=('Sales', 'sum'), Profit=('Profit', 'sum'), Quantity=('Quantity', 'sum'), Avg_Discount=('Discount', 'mean')).sort_values('Sales', ascending=False)
    category = df.groupby(['Category', 'Sub-Category'], as_index=False).agg(Orders=('Order ID', 'nunique'), Sales=('Sales', 'sum'), Profit=('Profit', 'sum'), Quantity=('Quantity', 'sum'), Avg_Discount=('Discount', 'mean')).sort_values('Sales', ascending=False)
    product = df.groupby(['Product ID', 'Product Name', 'Category', 'Sub-Category'], as_index=False).agg(Orders=('Order ID', 'nunique'), Sales=('Sales', 'sum'), Profit=('Profit', 'sum'), Quantity=('Quantity', 'sum')).sort_values('Sales', ascending=False)
    monthly = df.groupby('Month', as_index=False).agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum'), Orders=('Order ID', 'nunique'), Quantity=('Quantity', 'sum'))
    segment = df.groupby('Segment', as_index=False).agg(Orders=('Order ID', 'nunique'), Sales=('Sales', 'sum'), Profit=('Profit', 'sum'), Quantity=('Quantity', 'sum')).sort_values('Sales', ascending=False)
    ship = df.groupby('Ship Mode', as_index=False).agg(Orders=('Order ID', 'nunique'), Sales=('Sales', 'sum'), Profit=('Profit', 'sum')).sort_values('Sales', ascending=False)

    kpis.to_csv(OUTPUT_DIR / 'kpis.csv', index=False)
    region.to_csv(OUTPUT_DIR / 'region_performance.csv', index=False)
    category.to_csv(OUTPUT_DIR / 'category_performance.csv', index=False)
    product.head(25).to_csv(OUTPUT_DIR / 'top_25_products.csv', index=False)
    monthly.to_csv(OUTPUT_DIR / 'monthly_trend.csv', index=False)
    segment.to_csv(OUTPUT_DIR / 'segment_performance.csv', index=False)
    ship.to_csv(OUTPUT_DIR / 'ship_mode_performance.csv', index=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=region, x='Sales', y='Region', hue='Region', palette='Blues_r', legend=False, ax=ax)
    ax.set_title('Sales by Region', weight='bold'); ax.set_xlabel('Sales ($)'); ax.set_ylabel('')
    fig.tight_layout(); fig.savefig(OUTPUT_DIR / 'sales_by_region.png', dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=monthly, x='Month', y='Sales', marker='o', color='#2563EB', ax=ax)
    ax.set_title('Monthly Sales Trend', weight='bold'); ax.set_xlabel('Order month'); ax.set_ylabel('Sales ($)'); ax.tick_params(axis='x', rotation=60)
    fig.tight_layout(); fig.savefig(OUTPUT_DIR / 'monthly_sales_trend.png', dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 7))
    top = category.head(10).sort_values('Profit')
    sns.barplot(data=top, x='Profit', y='Sub-Category', hue='Sub-Category', palette='RdYlGn', legend=False, ax=ax)
    ax.set_title('Profit by Sub-Category', weight='bold'); ax.set_xlabel('Profit ($)'); ax.set_ylabel('')
    fig.tight_layout(); fig.savefig(OUTPUT_DIR / 'profit_by_subcategory.png', dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.scatterplot(data=df.sample(min(4000, len(df)), random_state=42), x='Discount', y='Profit', hue='Category', alpha=.55, ax=ax)
    ax.axhline(0, color='#111827', linewidth=1)
    ax.set_title('Discount and Profit Relationship', weight='bold'); ax.set_xlabel('Discount'); ax.set_ylabel('Profit ($)')
    fig.tight_layout(); fig.savefig(OUTPUT_DIR / 'discount_profit.png', dpi=180); plt.close(fig)

    insights = [
        f"The dataset contains {df['Order ID'].nunique():,} distinct orders from {df['Order Date'].min().date()} to {df['Order Date'].max().date()}.",
        f"Total sales are ${df['Sales'].sum():,.2f}, total profit is ${df['Profit'].sum():,.2f}, and overall profit margin is {df['Profit'].sum() / df['Sales'].sum():.1%}.",
        f"The leading region by sales is {region.iloc[0]['Region']} with ${region.iloc[0]['Sales']:,.2f} in sales.",
        f"The leading sub-category by sales is {category.iloc[0]['Sub-Category']}; the most profitable sub-category is {category.sort_values('Profit', ascending=False).iloc[0]['Sub-Category']}.",
        f"The lowest-profit sub-category is {category.sort_values('Profit').iloc[0]['Sub-Category']}; investigate pricing, discount depth, and fulfillment cost before expanding it.",
        "The data supports Power BI analysis of time, geography, product hierarchy, segment, shipping mode, sales, profit, quantity, discount, and margin.",
    ]
    (OUTPUT_DIR / 'insights.txt').write_text('\n'.join(f'- {x}' for x in insights) + '\n', encoding='utf-8')
    print('Analysis completed')
    print(kpis.to_string(index=False))


if __name__ == '__main__':
    main()
