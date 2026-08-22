from pathlib import Path

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = (
    ROOT_DIR
    / "data"
    / "raw"
    / "online_retail_II.xlsx"
)

PROCESSED_DIR = (
    ROOT_DIR
    / "data"
    / "processed"
)

OUTPUT_PATH = (
    PROCESSED_DIR
    / "transactions.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_raw_data(
    file_path: Path = RAW_DATA_PATH
) -> pd.DataFrame:

    """
    Load all sheets from Online Retail II Excel workbook.

    Returns
    -------
    pd.DataFrame
        Combined transaction-level dataframe.
    """

    if not file_path.exists():

        raise FileNotFoundError(
            f"""
Dataset not found.

Expected location:
{file_path}

Please download the Online Retail II dataset and place
online_retail_II.xlsx inside:

data/raw/
"""
        )

    print("Loading Excel workbook...")

    sheets = pd.read_excel(
        file_path,
        sheet_name=None
    )

    frames = []

    for sheet_name, frame in sheets.items():

        print(
            f"  Loading sheet: {sheet_name}"
            f" | rows = {len(frame):,}"
        )

        frame = frame.copy()

        frame["SourceSheet"] = sheet_name

        frames.append(frame)

    if not frames:

        raise ValueError(
            "No worksheets were found in the Excel file."
        )

    df = pd.concat(
        frames,
        ignore_index=True
    )

    print(
        f"\nCombined raw dataset shape: "
        f"{df.shape}"
    )

    return df


# ============================================================
# STANDARDIZE COLUMN NAMES
# ============================================================

def standardize_columns(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Standardize column names across the workbook.
    """

    df = df.copy()

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    rename_map = {
        "Invoice": "InvoiceNo",
        "Price": "UnitPrice",
        "Customer ID": "CustomerID"
    }

    df = df.rename(
        columns=rename_map
    )

    return df


# ============================================================
# DATA CLEANING
# ============================================================

def clean_data(
    df: pd.DataFrame
) -> pd.DataFrame:

    """
    Clean transaction-level data.

    Cleaning steps:
    1. Standardize column names
    2. Validate required columns
    3. Remove missing Customer IDs
    4. Convert data types
    5. Remove cancellations
    6. Remove invalid quantities
    7. Remove invalid prices
    8. Calculate revenue
    9. Remove duplicates
    """

    df = standardize_columns(df)

    required_columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    initial_rows = len(df)

    # --------------------------------------------------------
    # Remove missing Customer IDs
    # --------------------------------------------------------

    df = df.dropna(
        subset=["CustomerID"]
    )

    # --------------------------------------------------------
    # Data type conversion
    # --------------------------------------------------------

    df["InvoiceNo"] = (
        df["InvoiceNo"]
        .astype(str)
        .str.strip()
    )

    df["CustomerID"] = (
        pd.to_numeric(
            df["CustomerID"],
            errors="coerce"
        )
    )

    df["CustomerID"] = (
        df["CustomerID"]
        .round()
        .astype("Int64")
        .astype(str)
    )

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"],
        errors="coerce"
    )

    # Remove conversion failures
    df = df.dropna(
        subset=[
            "InvoiceDate",
            "Quantity",
            "UnitPrice"
        ]
    )

    # --------------------------------------------------------
    # Remove cancelled transactions
    # --------------------------------------------------------

    cancellation_mask = (
        df["InvoiceNo"]
        .str.upper()
        .str.startswith("C")
    )

    cancelled_count = int(
        cancellation_mask.sum()
    )

    df = df[
        ~cancellation_mask
    ]

    # --------------------------------------------------------
    # Remove invalid quantities/prices
    # --------------------------------------------------------

    df = df[
        df["Quantity"] > 0
    ]

    df = df[
        df["UnitPrice"] > 0
    ]

    # --------------------------------------------------------
    # Revenue
    # --------------------------------------------------------

    df["Revenue"] = (
        df["Quantity"]
        * df["UnitPrice"]
    )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    df = df.drop_duplicates()

    # --------------------------------------------------------
    # Sort data
    # --------------------------------------------------------

    df = (
        df.sort_values(
            "InvoiceDate"
        )
        .reset_index(drop=True)
    )

    print("\nCleaning Summary")
    print("-" * 50)

    print(
        f"Initial rows       : {initial_rows:,}"
    )

    print(
        f"Cancelled rows     : {cancelled_count:,}"
    )

    print(
        f"Duplicate rows     : {duplicate_count:,}"
    )

    print(
        f"Final rows         : {len(df):,}"
    )

    print(
        f"Customers          : "
        f"{df['CustomerID'].nunique():,}"
    )

    print(
        f"Orders             : "
        f"{df['InvoiceNo'].nunique():,}"
    )

    print(
        f"Products           : "
        f"{df['StockCode'].nunique():,}"
    )

    print(
        f"Revenue            : "
        f"{df['Revenue'].sum():,.2f}"
    )

    return df


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("CUSTOMER INTELLIGENCE PLATFORM")
    print("STEP 1 — DATA PREPROCESSING")
    print("=" * 70)

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    raw_df = load_raw_data()

    clean_df = clean_data(
        raw_df
    )

    clean_df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nProcessed dataset saved to:\n"
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":

    main()