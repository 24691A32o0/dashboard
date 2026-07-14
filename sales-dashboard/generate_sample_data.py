"""
Generates a synthetic sales dataset at data/sales_data.csv.

Run:
    python generate_sample_data.py
"""

import numpy as np
import pandas as pd

np.random.seed(42)

PRODUCTS = {
    "Laptop": "Electronics", "Mobile": "Electronics", "TV": "Electronics",
    "Headphones": "Electronics", "Chair": "Furniture", "Table": "Furniture",
    "Sofa": "Furniture", "Bookshelf": "Furniture", "Notebook": "Stationery",
    "Pen": "Stationery", "Backpack": "Accessories", "Watch": "Accessories",
}
REGIONS = ["North", "South", "East", "West"]
PRICE_RANGE = {
    "Laptop": (35000, 90000), "Mobile": (8000, 45000), "TV": (15000, 60000),
    "Headphones": (500, 5000), "Chair": (1500, 8000), "Table": (3000, 15000),
    "Sofa": (10000, 40000), "Bookshelf": (2000, 9000), "Notebook": (30, 200),
    "Pen": (10, 100), "Backpack": (500, 3000), "Watch": (800, 12000),
}


def generate(n_rows: int = 1500, year: int = 2024) -> pd.DataFrame:
    dates = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
    rows = []
    order_id = 1000

    for _ in range(n_rows):
        date = np.random.choice(dates)
        product = np.random.choice(list(PRODUCTS.keys()))
        category = PRODUCTS[product]
        region = np.random.choice(REGIONS)
        low, high = PRICE_RANGE[product]
        unit_price = np.random.randint(low, high)
        qty = np.random.randint(1, 6)
        sales = unit_price * qty
        margin = np.random.uniform(0.08, 0.25)
        profit = round(sales * margin, 2)
        order_id += 1
        rows.append(
            [order_id, pd.Timestamp(date).strftime("%Y-%m-%d"), product,
             category, region, qty, unit_price, sales, profit]
        )

    df = pd.DataFrame(
        rows,
        columns=["Order_ID", "Date", "Product", "Category", "Region",
                 "Quantity", "Unit_Price", "Sales", "Profit"],
    )
    return df.sort_values("Date").reset_index(drop=True)


if __name__ == "__main__":
    df = generate()
    df.to_csv("data/sales_data.csv", index=False)
    print(f"Wrote {len(df)} rows to data/sales_data.csv")
