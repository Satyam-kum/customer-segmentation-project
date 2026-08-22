from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier

from ml.feature_engineering import (
    create_customer_features
)

from ml.evaluation import (
    classification_metrics
)


# ============================================================
# PATHS
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

TRANSACTIONS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "transactions.csv"
)

MODEL_DIR = (
    ROOT_DIR
    / "models"
)

RESULTS_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "churn_model_results.csv"
)


# ============================================================
# CHURN FEATURES
# ============================================================

CHURN_FEATURES = [

    "recency",

    "frequency",

    "monetary",

    "average_order_value",

    "customer_lifetime",

    "total_quantity",

    "unique_products",

    "avg_purchase_interval",

    "median_purchase_interval",

    "weekend_purchase_ratio",

    "avg_monthly_orders"
]


# ============================================================
# CREATE TEMPORAL SNAPSHOT
# ============================================================

def create_snapshot_dataset(
    df,
    observation_end,
    prediction_days=90
):

    """
    Create a customer snapshot.

    Features:
        transactions <= observation_end

    Label:
        1 = no purchase during next prediction_days
        0 = purchased during next prediction_days
    """

    observation_end = pd.Timestamp(
        observation_end
    )

    prediction_end = (
        observation_end
        + pd.Timedelta(
            days=prediction_days
        )
    )

    # --------------------------------------------------------
    # Historical data
    # --------------------------------------------------------

    historical = df[
        df["InvoiceDate"]
        <= observation_end
    ].copy()

    # --------------------------------------------------------
    # Future data
    # --------------------------------------------------------

    future = df[
        (
            df["InvoiceDate"]
            > observation_end
        )
        &
        (
            df["InvoiceDate"]
            <= prediction_end
        )
    ].copy()

    # --------------------------------------------------------
    # Customer features
    # --------------------------------------------------------

    customer_features = (
        create_customer_features(
            historical,
            reference_date=(
                observation_end
                + pd.Timedelta(days=1)
            )
        )
    )

    # --------------------------------------------------------
    # Future purchasers
    # --------------------------------------------------------

    future_customers = set(
        future["CustomerID"]
        .astype(str)
    )

    # --------------------------------------------------------
    # Churn label
    # --------------------------------------------------------

    customer_features["churn"] = (
        ~customer_features[
            "CustomerID"
        ]
        .astype(str)
        .isin(
            future_customers
        )
    ).astype(int)

    return customer_features


# ============================================================
# TEMPORAL TRAIN / TEST
# ============================================================

def create_temporal_train_test(
    df,
    initial_cutoff,
    prediction_days=90
):

    """
    Create train and test snapshots.

    Train:
        cutoff -> next 90 days

    Test:
        later cutoff -> next 90 days
    """

    initial_cutoff = pd.Timestamp(
        initial_cutoff
    )

    # --------------------------------------------------------
    # Training snapshot
    # --------------------------------------------------------

    train = create_snapshot_dataset(
        df,
        initial_cutoff,
        prediction_days
    )

    # --------------------------------------------------------
    # Later test snapshot
    # --------------------------------------------------------

    test_cutoff = (
        initial_cutoff
        + pd.Timedelta(
            days=prediction_days
        )
    )

    test = create_snapshot_dataset(
        df,
        test_cutoff,
        prediction_days
    )

    # --------------------------------------------------------
    # Remove customers that existed in training
    # --------------------------------------------------------

    train_ids = set(
        train["CustomerID"]
        .astype(str)
    )

    test = test[
        ~test["CustomerID"]
        .astype(str)
        .isin(train_ids)
    ].copy()

    return (
        train,
        test
    )


# ============================================================
# BUILD MODELS
# ============================================================

def build_models():

    """
    Return candidate churn models.
    """

    preprocessing = Pipeline([

        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        ),

        (
            "scaler",
            StandardScaler()
        )
    ])

    models = {

        "Logistic Regression":

            Pipeline([

                (
                    "preprocessing",
                    preprocessing
                ),

                (
                    "model",

                    LogisticRegression(
                        max_iter=3000,
                        class_weight="balanced",
                        random_state=42
                    )
                )
            ]),

        "Random Forest":

            Pipeline([

                (
                    "preprocessing",
                    preprocessing
                ),

                (
                    "model",

                    RandomForestClassifier(

                        n_estimators=400,

                        max_depth=12,

                        min_samples_leaf=5,

                        class_weight="balanced",

                        random_state=42,

                        n_jobs=-1
                    )
                )
            ]),

        "XGBoost":

            Pipeline([

                (
                    "preprocessing",
                    preprocessing
                ),

                (
                    "model",

                    XGBClassifier(

                        n_estimators=400,

                        max_depth=5,

                        learning_rate=0.05,

                        subsample=0.8,

                        colsample_bytree=0.8,

                        objective="binary:logistic",

                        eval_metric="logloss",

                        random_state=42
                    )
                )
            ])
    }

    return models


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 4 — CUSTOMER CHURN PREDICTION")
    print("=" * 70)

    if not TRANSACTIONS_PATH.exists():

        raise FileNotFoundError(
            "transactions.csv not found.\n"
            "Run preprocessing first."
        )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Load transactions
    # --------------------------------------------------------

    df = pd.read_csv(
        TRANSACTIONS_PATH,
        parse_dates=["InvoiceDate"]
    )

    max_date = (
        df["InvoiceDate"]
        .max()
    )

    # Need enough future data for the
    # prediction window.
    initial_cutoff = (
        max_date
        - pd.Timedelta(
            days=180
        )
    )

    print(
        f"Dataset maximum date: "
        f"{max_date}"
    )

    print(
        f"Training cutoff: "
        f"{initial_cutoff}"
    )

    # --------------------------------------------------------
    # Temporal datasets
    # --------------------------------------------------------

    (
        train,
        test
    ) = create_temporal_train_test(
        df,
        initial_cutoff
    )

    if len(test) < 50:

        print(
            "\nWARNING:"
        )

        print(
            "Temporal test set contains "
            f"only {len(test)} customers."
        )

        print(
            "Consider using an earlier "
            "observation cutoff."
        )

    # --------------------------------------------------------
    # Feature matrix
    # --------------------------------------------------------

    X_train = train[
        CHURN_FEATURES
    ].copy()

    y_train = train[
        "churn"
    ].copy()

    X_test = test[
        CHURN_FEATURES
    ].copy()

    y_test = test[
        "churn"
    ].copy()

    print(
        f"\nTraining customers: "
        f"{len(train):,}"
    )

    print(
        f"Test customers: "
        f"{len(test):,}"
    )

    print(
        "\nTraining churn distribution:"
    )

    print(
        y_train.value_counts(
            normalize=True
        )
    )

    print(
        "\nTest churn distribution:"
    )

    print(
        y_test.value_counts(
            normalize=True
        )
    )

    # --------------------------------------------------------
    # Train models
    # --------------------------------------------------------

    models = build_models()

    results = {}

    probabilities = {}

    predictions = {}

    for name, model in models.items():

        print(
            f"\nTraining {name}..."
        )

        model.fit(
            X_train,
            y_train
        )

        prediction = (
            model.predict(
                X_test
            )
        )

        probability = (
            model
            .predict_proba(
                X_test
            )[:, 1]
        )

        metrics = (
            classification_metrics(
                y_test,
                prediction,
                probability
            )
        )

        results[name] = metrics

        probabilities[name] = (
            probability
        )

        predictions[name] = (
            prediction
        )

        print(
            f"ROC-AUC: "
            f"{metrics['roc_auc']:.4f}"
        )

        print(
            f"F1: "
            f"{metrics['f1']:.4f}"
        )

        print(
            f"Recall: "
            f"{metrics['recall']:.4f}"
        )

    # --------------------------------------------------------
    # Model comparison
    # --------------------------------------------------------

    comparison = (
        pd.DataFrame(results)
        .T
    )

    printable_columns = [
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
        "pr_auc"
    ]

    print(
        "\nModel Comparison:"
    )

    print(
        comparison[
            printable_columns
        ]
        .sort_values(
            "roc_auc",
            ascending=False
        )
        .to_string()
    )

    # --------------------------------------------------------
    # Select best model
    # --------------------------------------------------------

    best_model_name = (
        comparison[
            "roc_auc"
        ]
        .idxmax()
    )

    best_model = (
        models[
            best_model_name
        ]
    )

    print(
        f"\nBest model: "
        f"{best_model_name}"
    )

    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    joblib.dump(
        best_model,
        MODEL_DIR
        / "churn_model.pkl"
    )

    joblib.dump(
        CHURN_FEATURES,
        MODEL_DIR
        / "feature_columns.pkl"
    )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    comparison[
        printable_columns
    ].sort_values(
        "roc_auc",
        ascending=False
    ).to_csv(
        RESULTS_PATH
    )

    # --------------------------------------------------------
    # Generate customer risk table
    # --------------------------------------------------------

    best_probability = (
        probabilities[
            best_model_name
        ]
    )

    best_prediction = (
        predictions[
            best_model_name
        ]
    )

    risk_df = test[
        [
            "CustomerID",
            "recency",
            "frequency",
            "monetary",
            "average_order_value"
        ]
    ].copy()

    risk_df[
        "churn_probability"
    ] = best_probability

    risk_df[
        "prediction"
    ] = best_prediction

    risk_df[
        "churn_risk"
    ] = pd.cut(

        risk_df[
            "churn_probability"
        ],

        bins=[
            -0.01,
            0.45,
            0.75,
            1.0
        ],

        labels=[
            "LOW",
            "MEDIUM",
            "HIGH"
        ]
    )

    # --------------------------------------------------------
    # Retention recommendation
    # --------------------------------------------------------

    def recommendation(row):

        probability = (
            row["churn_probability"]
        )

        monetary = (
            row["monetary"]
        )

        if (
            probability >= 0.75
            and monetary >= 1000
        ):

            return (
                "VIP retention campaign"
            )

        if probability >= 0.75:

            return (
                "Personalized reactivation"
            )

        if probability >= 0.45:

            return (
                "Targeted engagement"
            )

        if monetary >= 1000:

            return (
                "Loyalty reward"
            )

        return (
            "Standard engagement"
        )

    risk_df[
        "retention_action"
    ] = risk_df.apply(
        recommendation,
        axis=1
    )

    # --------------------------------------------------------
    # Save risk predictions
    # --------------------------------------------------------

    risk_output = (
        ROOT_DIR
        / "data"
        / "processed"
        / "customer_churn_predictions.csv"
    )

    risk_df.to_csv(
        risk_output,
        index=False
    )

    # --------------------------------------------------------
    # Business summary
    # --------------------------------------------------------

    high_risk = (
        risk_df[
            "churn_risk"
        ]
        == "HIGH"
    )

    high_risk_count = int(
        high_risk.sum()
    )

    revenue_at_risk = (
        risk_df
        .loc[
            high_risk,
            "monetary"
        ]
        .sum()
    )

    print(
        "\nBusiness Summary"
    )

    print("-" * 50)

    print(
        f"High-risk customers : "
        f"{high_risk_count:,}"
    )

    print(
        f"Revenue at risk     : "
        f"{revenue_at_risk:,.2f}"
    )

    print(
        f"\nModel saved to:\n"
        f"{MODEL_DIR / 'churn_model.pkl'}"
    )

    print(
        f"\nPrediction file saved to:\n"
        f"{risk_output}"
    )


if __name__ == "__main__":

    main()