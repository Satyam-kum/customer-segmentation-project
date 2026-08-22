from ml.preprocessing import (
    main as run_preprocessing
)

from ml.feature_engineering import (
    main as run_feature_engineering
)

from ml.segmentation import (
    main as run_segmentation
)

from ml.churn_model import (
    main as run_churn_model
)


def main():

    print("=" * 80)
    print("CUSTOMER INTELLIGENCE PLATFORM")
    print("COMPLETE MACHINE LEARNING PIPELINE")
    print("=" * 80)

    # ========================================================
    # STEP 1
    # ========================================================

    print("\n")
    print("=" * 80)
    print("STEP 1 / 4 — PREPROCESSING")
    print("=" * 80)

    run_preprocessing()

    # ========================================================
    # STEP 2
    # ========================================================

    print("\n")
    print("=" * 80)
    print("STEP 2 / 4 — FEATURE ENGINEERING")
    print("=" * 80)

    run_feature_engineering()

    # ========================================================
    # STEP 3
    # ========================================================

    print("\n")
    print("=" * 80)
    print("STEP 3 / 4 — CUSTOMER SEGMENTATION")
    print("=" * 80)

    run_segmentation()

    # ========================================================
    # STEP 4
    # ========================================================

    print("\n")
    print("=" * 80)
    print("STEP 4 / 4 — CHURN MODELING")
    print("=" * 80)

    run_churn_model()

    # ========================================================
    # COMPLETE
    # ========================================================

    print("\n")
    print("=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)

    print(
        """
Generated files:

data/processed/
    ├── transactions.csv
    ├── customer_features.csv
    ├── churn_model_results.csv
    ├── customer_churn_predictions.csv
    ├── segmentation_model_results.csv
    └── kmeans_k_search.csv

models/
    ├── scaler.pkl
    ├── kmeans.pkl
    ├── segmentation_features.pkl
    ├── segment_mapping.pkl
    ├── churn_model.pkl
    └── feature_columns.pkl
"""
    )


if __name__ == "__main__":

    main()