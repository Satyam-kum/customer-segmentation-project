from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# PATHS
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "transactions.csv"
)

OUTPUT_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "customer_features.csv"
)


# ============================================================
# CUSTOMER FEATURES
# ============================================================

def create_customer_features(
    df: pd.DataFrame,
    reference_date=None
) -> pd.DataFrame:

    """
    Convert transaction-level data into customer-level features.
    """

    df = df.copy()

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"]
    )

    if reference_date is None:

        reference_date = (
            df["InvoiceDate"].max()
            + pd.Timedelta(days=1)
        )

    reference_date = pd.Timestamp(
        reference_date
    )

    # ========================================================
    # BASIC CUSTOMER FEATURES
    # ========================================================

    customer = (
        df.groupby("CustomerID")
        .agg(
            first_purchase=(
                "InvoiceDate",
                "min"
            ),

            last_purchase=(
                "InvoiceDate",
                "max"
            ),

            frequency=(
                "InvoiceNo",
                "nunique"
            ),

            monetary=(
                "Revenue",
                "sum"
            ),

            total_quantity=(
                "Quantity",
                "sum"
            ),

            unique_products=(
                "StockCode",
                "nunique"
            ),

            country_count=(
                "Country",
                "nunique"
            )
        )
        .reset_index()
    )

    # ========================================================
    # RECENCY
    # ========================================================

    customer["recency"] = (
        reference_date
        - customer["last_purchase"]
    ).dt.days

    customer["recency"] = (
        customer["recency"]
        .clip(lower=0)
    )

    # ========================================================
    # CUSTOMER LIFETIME
    # ========================================================

    customer["customer_lifetime"] = (
        customer["last_purchase"]
        - customer["first_purchase"]
    ).dt.days

    customer["customer_lifetime"] = (
        customer["customer_lifetime"]
        .clip(lower=0)
    )

    # ========================================================
    # AVERAGE ORDER VALUE
    # ========================================================

    customer["average_order_value"] = (
        customer["monetary"]
        /
        customer["frequency"].replace(
            0,
            np.nan
        )
    )

    # ========================================================
    # ITEMS PER ORDER
    # ========================================================

    customer["items_per_order"] = (
        customer["total_quantity"]
        /
        customer["frequency"].replace(
            0,
            np.nan
        )
    )

    # ========================================================
    # PURCHASE INTERVALS
    # ========================================================

    orders = (
        df[
            [
                "CustomerID",
                "InvoiceNo",
                "InvoiceDate"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "CustomerID",
                "InvoiceDate"
            ]
        )
    )

    orders["purchase_interval"] = (
        orders
        .groupby("CustomerID")["InvoiceDate"]
        .diff()
        .dt.days
    )

    interval_features = (
        orders
        .groupby("CustomerID")[
            "purchase_interval"
        ]
        .agg(
            avg_purchase_interval="mean",
            median_purchase_interval="median",
            max_purchase_interval="max"
        )
        .reset_index()
    )

    customer = customer.merge(
        interval_features,
        on="CustomerID",
        how="left"
    )

    # ========================================================
    # CALENDAR FEATURES
    # ========================================================

    df["weekday"] = (
        df["InvoiceDate"]
        .dt.dayofweek
    )

    df["month"] = (
        df["InvoiceDate"]
        .dt.to_period("M")
        .astype(str)
    )

    # Weekend purchase ratio
    weekend_ratio = (
        df.assign(
            is_weekend=
            df["weekday"] >= 5
        )
        .groupby("CustomerID")[
            "is_weekend"
        ]
        .mean()
        .rename(
            "weekend_purchase_ratio"
        )
        .reset_index()
    )

    customer = customer.merge(
        weekend_ratio,
        on="CustomerID",
        how="left"
    )

    # ========================================================
    # MONTHLY PURCHASE BEHAVIOR
    # ========================================================

    monthly_orders = (
        df.groupby(
            [
                "CustomerID",
                "month"
            ]
        )["InvoiceNo"]
        .nunique()
        .groupby("CustomerID")
        .agg(
            active_months="count",
            avg_monthly_orders="mean",
            max_monthly_orders="max"
        )
        .reset_index()
    )

    customer = customer.merge(
        monthly_orders,
        on="CustomerID",
        how="left"
    )

    # ========================================================
    # REVENUE BEHAVIOR
    # ========================================================

    monthly_revenue = (
        df.groupby(
            [
                "CustomerID",
                "month"
            ]
        )["Revenue"]
        .sum()
        .groupby("CustomerID")
        .agg(
            avg_monthly_revenue="mean",
            max_monthly_revenue="max"
        )
        .reset_index()
    )

    customer = customer.merge(
        monthly_revenue,
        on="CustomerID",
        how="left"
    )

    # ========================================================
    # CLEAN NUMERICAL VALUES
    # ========================================================

    numeric_columns = (
        customer
        .select_dtypes(
            include=np.number
        )
        .columns
    )

    customer[numeric_columns] = (
        customer[numeric_columns]
        .replace(
            [
                np.inf,
                -np.inf
            ],
            np.nan
        )
    )

    # Median imputation
    for column in numeric_columns:

        if column == "CustomerID":
            continue

        customer[column] = (
            customer[column]
            .fillna(
                customer[column].median()
            )
        )

    return customer


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 2 — CUSTOMER FEATURE ENGINEERING")
    print("=" * 70)

    if not INPUT_PATH.exists():

        raise FileNotFoundError(
            "transactions.csv not found.\n"
            "Run:\n"
            "python ml/preprocessing.py"
        )

    df = pd.read_csv(
        INPUT_PATH,
        parse_dates=["InvoiceDate"]
    )

    customer_features = (
        create_customer_features(df)
    )

    customer_features.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nCustomer features saved to:\n"
        f"{OUTPUT_PATH}"
    )

    print(
        f"Customers generated: "
        f"{len(customer_features):,}"
    )

    print("\nFeature columns:")

    for column in customer_features.columns:

        print(
            f"  - {column}"
        )


if __name__ == "__main__":

    main()