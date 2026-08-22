
from pathlib import Path

import pandas as pd

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import (
    create_tables,
    SessionLocal
)

from backend.models import (
    Customer,
    Transaction
)

from backend.routes import (
    customers,
    segmentation,
    churn,
    analytics
)


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="Customer Intelligence Platform API",
    description=(
        "Full-stack customer analytics, "
        "segmentation, retention and churn "
        "prediction platform."
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# ROUTES
# ============================================================

app.include_router(
    customers.router
)

app.include_router(
    segmentation.router
)

app.include_router(
    churn.router
)

app.include_router(
    analytics.router
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "application": "Customer Intelligence Platform",
        "version": "1.0.0",
        "status": "running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)


# ============================================================
# SAFE FLOAT CONVERSION
# ============================================================

def safe_float(value, default=0.0):

    try:

        if pd.isna(value):
            return default

        return float(value)

    except (ValueError, TypeError):

        return default


# ============================================================
# SAFE STRING CONVERSION
# ============================================================

def safe_string(value, default=""):

    if pd.isna(value):

        return default

    return str(value)


# ============================================================
# IMPORT PROCESSED DATA
# ============================================================

def import_processed_data():

    """
    Import generated ML datasets into PostgreSQL.

    Customers:
        data/processed/customer_features.csv

    Transactions:
        data/processed/transactions.csv

    Transaction data is loaded in chunks to avoid excessive
    memory usage.

    Existing records are skipped.
    """

    db = SessionLocal()

    try:

        # ====================================================
        # FILE PATHS
        # ====================================================

        customer_file = (
            ROOT_DIR
            / "data"
            / "processed"
            / "customer_features.csv"
        )

        transaction_file = (
            ROOT_DIR
            / "data"
            / "processed"
            / "transactions.csv"
        )

        print()
        print("=" * 60)
        print("DATA IMPORT")
        print("=" * 60)

        print(
            "Project root:",
            ROOT_DIR
        )

        print(
            "Customer file:",
            customer_file
        )

        print(
            "Transaction file:",
            transaction_file
        )

        # ====================================================
        # CHECK CUSTOMER FILE
        # ====================================================

        if not customer_file.exists():

            print(
                "WARNING: customer_features.csv not found."
            )

        # ====================================================
        # CHECK TRANSACTION FILE
        # ====================================================

        if not transaction_file.exists():

            print(
                "WARNING: transactions.csv not found."
            )

        # ====================================================
        # CUSTOMERS
        # ====================================================

        if customer_file.exists():

            print()
            print(
                "Loading customer_features.csv..."
            )

            customer_df = pd.read_csv(
                customer_file
            )

            print(
                "Customer rows:",
                len(customer_df)
            )

            print(
                "Customer columns:",
                list(customer_df.columns)
            )

            customer_count = 0
            customer_skipped = 0

            for _, row in customer_df.iterrows():

                # --------------------------------------------
                # Customer ID
                # --------------------------------------------

                if (
                    "CustomerID"
                    not in row
                ):

                    print(
                        "ERROR: CustomerID column not found "
                        "in customer_features.csv"
                    )

                    break

                if pd.isna(
                    row["CustomerID"]
                ):

                    customer_skipped += 1

                    continue

                customer_id = str(
                    row["CustomerID"]
                )

                # --------------------------------------------
                # Check whether customer already exists
                # --------------------------------------------

                existing = (
                    db.query(Customer)
                    .filter(
                        Customer.customer_id
                        == customer_id
                    )
                    .first()
                )

                if existing:

                    customer_skipped += 1

                    continue

                # --------------------------------------------
                # Create customer
                # --------------------------------------------

                customer = Customer(

                    customer_id=customer_id,

                    recency=safe_float(
                        row.get(
                            "recency",
                            0
                        )
                    ),

                    frequency=safe_float(
                        row.get(
                            "frequency",
                            0
                        )
                    ),

                    monetary=safe_float(
                        row.get(
                            "monetary",
                            0
                        )
                    ),

                    average_order_value=safe_float(
                        row.get(
                            "average_order_value",
                            0
                        )
                    ),

                    customer_lifetime=safe_float(
                        row.get(
                            "customer_lifetime",
                            0
                        )
                    ),

                    total_quantity=safe_float(
                        row.get(
                            "total_quantity",
                            0
                        )
                    ),

                    unique_products=safe_float(
                        row.get(
                            "unique_products",
                            0
                        )
                    ),

                    avg_purchase_interval=safe_float(
                        row.get(
                            "avg_purchase_interval",
                            0
                        )
                    ),

                    median_purchase_interval=safe_float(
                        row.get(
                            "median_purchase_interval",
                            0
                        )
                    ),

                    max_purchase_interval=safe_float(
                        row.get(
                            "max_purchase_interval",
                            0
                        )
                    ),

                    weekend_purchase_ratio=safe_float(
                        row.get(
                            "weekend_purchase_ratio",
                            0
                        )
                    ),

                    active_months=safe_float(
                        row.get(
                            "active_months",
                            0
                        )
                    ),

                    avg_monthly_orders=safe_float(
                        row.get(
                            "avg_monthly_orders",
                            0
                        )
                    ),

                    max_monthly_orders=safe_float(
                        row.get(
                            "max_monthly_orders",
                            0
                        )
                    ),

                    avg_monthly_revenue=safe_float(
                        row.get(
                            "avg_monthly_revenue",
                            0
                        )
                    ),

                    max_monthly_revenue=safe_float(
                        row.get(
                            "max_monthly_revenue",
                            0
                        )
                    ),

                    items_per_order=safe_float(
                        row.get(
                            "items_per_order",
                            0
                        )
                    ),

                    country_count=safe_float(
                        row.get(
                            "country_count",
                            0
                        )
                    ),

                    cluster=(
                        int(
                            row["cluster"]
                        )
                        if (
                            "cluster" in row
                            and pd.notna(
                                row["cluster"]
                            )
                        )
                        else None
                    ),

                    segment=(
                        str(
                            row["segment"]
                        )
                        if (
                            "segment" in row
                            and pd.notna(
                                row["segment"]
                            )
                        )
                        else None
                    )
                )

                db.add(
                    customer
                )

                customer_count += 1

            # --------------------------------------------
            # Commit customers
            # --------------------------------------------

            db.commit()

            print(
                "Customer data imported."
            )

            print(
                "New customers:",
                customer_count
            )

            print(
                "Skipped customers:",
                customer_skipped
            )

        # ====================================================
        # TRANSACTIONS
        # ====================================================

        if transaction_file.exists():

            print()
            print(
                "Loading transactions.csv..."
            )

            print(
                "Transaction file path:",
                transaction_file
            )

            # ------------------------------------------------
            # IMPORTANT:
            # Use transaction_file here.
            #
            # DO NOT use:
            #
            # pd.read_csv("data/transactions.csv")
            #
            # ------------------------------------------------

            transaction_count = 0
            transaction_skipped = 0
            chunk_number = 0

            # ------------------------------------------------
            # Read transactions in chunks
            # ------------------------------------------------

            chunks = pd.read_csv(
                transaction_file,
                chunksize=5000,
                parse_dates=[
                    "InvoiceDate"
                ]
            )

            for chunk in chunks:

                chunk_number += 1

                print()
                print(
                    f"Processing transaction chunk "
                    f"{chunk_number}..."
                )

                print(
                    "Rows in chunk:",
                    len(chunk)
                )

                # ------------------------------------------------
                # Validate required columns
                # ------------------------------------------------

                required_columns = [
                    "InvoiceNo",
                    "StockCode",
                    "Quantity",
                    "InvoiceDate",
                    "UnitPrice",
                    "CustomerID"
                ]

                missing_columns = [
                    column
                    for column in required_columns
                    if column not in chunk.columns
                ]

                if missing_columns:

                    raise ValueError(
                        "Missing transaction columns: "
                        + str(missing_columns)
                    )

                # ------------------------------------------------
                # Clean CustomerID
                # ------------------------------------------------

                chunk = chunk[
                    chunk["CustomerID"].notna()
                ]

                # ------------------------------------------------
                # Clean InvoiceNo
                # ------------------------------------------------

                chunk = chunk[
                    chunk["InvoiceNo"].notna()
                ]

                # ------------------------------------------------
                # Clean StockCode
                # ------------------------------------------------

                chunk = chunk[
                    chunk["StockCode"].notna()
                ]

                if chunk.empty:

                    print(
                        "Chunk contains no valid rows."
                    )

                    continue

                # ------------------------------------------------
                # Calculate Revenue if missing
                # ------------------------------------------------

                if "Revenue" not in chunk.columns:

                    print(
                        "Revenue column not found."
                        " Calculating Revenue..."
                    )

                    chunk["Revenue"] = (
                        chunk["Quantity"]
                        * chunk["UnitPrice"]
                    )

                # ------------------------------------------------
                # Convert IDs to strings
                # ------------------------------------------------

                chunk["InvoiceNo"] = (
                    chunk["InvoiceNo"]
                    .astype(str)
                )

                chunk["StockCode"] = (
                    chunk["StockCode"]
                    .astype(str)
                )

                chunk["CustomerID"] = (
                    chunk["CustomerID"]
                    .astype(str)
                )

                # ------------------------------------------------
                # Remove duplicates INSIDE current CSV chunk
                # ------------------------------------------------

                chunk = chunk.drop_duplicates(
                    subset=[
                        "InvoiceNo",
                        "CustomerID",
                        "StockCode"
                    ]
                )

                # ------------------------------------------------
                # Get invoice/customer/stock combinations already
                # existing in database.
                #
                # This avoids querying PostgreSQL once per row.
                # ------------------------------------------------

                existing_keys = set()

                for invoice_no in chunk[
                    "InvoiceNo"
                ].unique():

                    existing_rows = (
                        db.query(
                            Transaction
                        )
                        .filter(
                            Transaction.invoice_no
                            == invoice_no
                        )
                        .all()
                    )

                    for existing_row in existing_rows:

                        existing_keys.add(
                            (
                                str(
                                    existing_row.invoice_no
                                ),

                                str(
                                    existing_row.customer_id
                                ),

                                str(
                                    existing_row.stock_code
                                )
                            )
                        )

                # ------------------------------------------------
                # Prepare records for bulk insertion
                # ------------------------------------------------

                records = []

                for _, row in chunk.iterrows():

                    invoice_no = safe_string(
                        row["InvoiceNo"]
                    )

                    customer_id = safe_string(
                        row["CustomerID"]
                    )

                    stock_code = safe_string(
                        row["StockCode"]
                    )

                    key = (
                        invoice_no,
                        customer_id,
                        stock_code
                    )

                    # --------------------------------------------
                    # Skip existing transaction
                    # --------------------------------------------

                    if key in existing_keys:

                        transaction_skipped += 1

                        continue

                    # --------------------------------------------
                    # Invoice date
                    # --------------------------------------------

                    invoice_date = (
                        pd.to_datetime(
                            row["InvoiceDate"],
                            errors="coerce"
                        )
                    )

                    if pd.isna(
                        invoice_date
                    ):

                        transaction_skipped += 1

                        continue

                    # --------------------------------------------
                    # Description
                    # --------------------------------------------

                    description = safe_string(
                        row.get(
                            "Description",
                            ""
                        )
                    )

                    # --------------------------------------------
                    # Country
                    # --------------------------------------------

                    country = safe_string(
                        row.get(
                            "Country",
                            ""
                        )
                    )

                    # --------------------------------------------
                    # Quantity
                    # --------------------------------------------

                    quantity = safe_float(
                        row.get(
                            "Quantity",
                            0
                        )
                    )

                    # --------------------------------------------
                    # Unit price
                    # --------------------------------------------

                    unit_price = safe_float(
                        row.get(
                            "UnitPrice",
                            0
                        )
                    )

                    # --------------------------------------------
                    # Revenue
                    # --------------------------------------------

                    revenue = safe_float(
                        row.get(
                            "Revenue",
                            quantity * unit_price
                        )
                    )

                    # --------------------------------------------
                    # Create dictionary
                    # --------------------------------------------

                    records.append({

                        "invoice_no":
                            invoice_no,

                        "stock_code":
                            stock_code,

                        "description":
                            description,

                        "quantity":
                            quantity,

                        "invoice_date":
                            invoice_date.to_pydatetime(),

                        "unit_price":
                            unit_price,

                        "revenue":
                            revenue,

                        "customer_id":
                            customer_id,

                        "country":
                            country
                    })

                    # Add to existing keys so that duplicate
                    # rows within the same processing session
                    # are not inserted twice.

                    existing_keys.add(
                        key
                    )

                # ------------------------------------------------
                # Bulk insert
                # ------------------------------------------------

                if records:

                    db.bulk_insert_mappings(
                        Transaction,
                        records
                    )

                    db.commit()

                    transaction_count += len(
                        records
                    )

                    print(
                        "Inserted transactions:",
                        len(records)
                    )

                else:

                    print(
                        "No new transactions in this chunk."
                    )

            # ------------------------------------------------
            # Transaction import completed
            # ------------------------------------------------

            print()
            print(
                "Transaction data imported."
            )

            print(
                "New transactions:",
                transaction_count
            )

            print(
                "Skipped transactions:",
                transaction_skipped
            )

        # ====================================================
        # IMPORT COMPLETE
        # ====================================================

        print()
        print("=" * 60)
        print("DATA IMPORT COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print()

    except Exception as error:

        db.rollback()

        print()
        print("=" * 60)
        print("DATABASE IMPORT ERROR")
        print("=" * 60)

        print(
            type(error).__name__,
            ":",
            error
        )

        print("=" * 60)
        print()

        # IMPORTANT:
        # Raise the error so that the FastAPI startup does
        # not silently continue as if everything succeeded.

        raise

    finally:

        db.close()


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup():

    print()
    print("=" * 60)
    print("STARTING CUSTOMER INTELLIGENCE PLATFORM")
    print("=" * 60)

    print(
        "Creating database tables..."
    )

    create_tables()

    print(
        "Database tables ready."
    )

    import_processed_data()

    print()
    print("=" * 60)
    print("APPLICATION STARTUP COMPLETE")
    print("=" * 60)
    print()