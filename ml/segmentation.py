from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.cluster import (
    KMeans,
    AgglomerativeClustering,
    DBSCAN
)

from sklearn.preprocessing import (
    StandardScaler
)

from ml.evaluation import (
    clustering_metrics
)


# ============================================================
# PATHS
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    ROOT_DIR
    / "data"
    / "processed"
    / "customer_features.csv"
)

OUTPUT_PATH = INPUT_PATH

MODEL_DIR = (
    ROOT_DIR
    / "models"
)


# ============================================================
# FEATURES
# ============================================================

SEGMENTATION_FEATURES = [

    "recency",

    "frequency",

    "monetary",

    "average_order_value",

    "customer_lifetime",

    "unique_products",

    "total_quantity",

    "avg_purchase_interval",

    "median_purchase_interval",

    "weekend_purchase_ratio",

    "avg_monthly_orders"
]


# ============================================================
# PREPARE FEATURES
# ============================================================

def prepare_segmentation_matrix(
    df
):

    """
    Prepare customer features for clustering.

    Steps:
    - Select behavioral features
    - Log-transform skewed features
    - Handle missing values
    - Standardize features
    """

    missing = [
        column
        for column in SEGMENTATION_FEATURES
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            "Missing segmentation features: "
            + ", ".join(missing)
        )

    X = df[
        SEGMENTATION_FEATURES
    ].copy()

    # --------------------------------------------------------
    # Log transformation
    # --------------------------------------------------------

    log_features = [

        "recency",
        "frequency",
        "monetary",
        "average_order_value",
        "customer_lifetime",
        "unique_products",
        "total_quantity",
        "avg_purchase_interval",
        "median_purchase_interval",
        "avg_monthly_orders"
    ]

    for column in log_features:

        X[column] = np.log1p(
            X[column]
            .clip(lower=0)
        )

    # --------------------------------------------------------
    # Replace invalid values
    # --------------------------------------------------------

    X = X.replace(
        [
            np.inf,
            -np.inf
        ],
        np.nan
    )

    X = X.fillna(
        X.median()
    )

    # --------------------------------------------------------
    # Scaling
    # --------------------------------------------------------

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(
        X
    )

    return (
        X,
        X_scaled,
        scaler
    )


# ============================================================
# FIND BEST K
# ============================================================

def find_best_k(
    X_scaled,
    min_k=2,
    max_k=10
):

    results = []

    for k in range(
        min_k,
        max_k + 1
    ):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=20
        )

        labels = (
            model.fit_predict(
                X_scaled
            )
        )

        metrics = (
            clustering_metrics(
                X_scaled,
                labels
            )
        )

        results.append({

            "k": k,

            "inertia":
                float(
                    model.inertia_
                ),

            "silhouette":
                metrics.get(
                    "silhouette",
                    np.nan
                ),

            "davies_bouldin":
                metrics.get(
                    "davies_bouldin",
                    np.nan
                ),

            "calinski_harabasz":
                metrics.get(
                    "calinski_harabasz",
                    np.nan
                )
        })

    results_df = pd.DataFrame(
        results
    )

    best_row = (
        results_df
        .loc[
            results_df["silhouette"]
            .idxmax()
        ]
    )

    best_k = int(
        best_row["k"]
    )

    return (
        best_k,
        results_df
    )


# ============================================================
# BUSINESS SEGMENT NAMING
# ============================================================

def generate_segment_names(
    df,
    cluster_column="cluster"
):

    """
    Generate business-readable names based on
    relative cluster characteristics.

    IMPORTANT:
    These are heuristic names and should be reviewed
    using the generated cluster profile.
    """

    profile = (
        df.groupby(
            cluster_column
        )[
            [
                "recency",
                "frequency",
                "monetary",
                "average_order_value"
            ]
        ]
        .mean()
    )

    # Score each cluster using standardized relative
    # business characteristics.

    ranking = profile.copy()

    ranking["value_score"] = (
        ranking["monetary"].rank(
            pct=True
        )
        +
        ranking["frequency"].rank(
            pct=True
        )
        -
        ranking["recency"].rank(
            pct=True
        )
    )

    ordered = (
        ranking["value_score"]
        .sort_values(
            ascending=False
        )
        .index
        .tolist()
    )

    mapping = {}

    number_of_clusters = (
        len(ordered)
    )

    for position, cluster in enumerate(
        ordered
    ):

        if position == 0:

            mapping[cluster] = (
                "Champions"
            )

        elif position == 1:

            mapping[cluster] = (
                "Loyal Customers"
            )

        elif position == (
            number_of_clusters - 1
        ):

            mapping[cluster] = (
                "Low Value / At Risk"
            )

        else:

            mapping[cluster] = (
                f"Growth Segment {position}"
            )

    return (
        mapping,
        profile
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 3 — CUSTOMER SEGMENTATION")
    print("=" * 70)

    if not INPUT_PATH.exists():

        raise FileNotFoundError(
            "customer_features.csv not found.\n"
            "Run:\n"
            "python ml/feature_engineering.py"
        )

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df = pd.read_csv(
        INPUT_PATH
    )

    # --------------------------------------------------------
    # Prepare matrix
    # --------------------------------------------------------

    (
        X,
        X_scaled,
        scaler
    ) = prepare_segmentation_matrix(
        df
    )

    # --------------------------------------------------------
    # Find K
    # --------------------------------------------------------

    (
        best_k,
        k_results
    ) = find_best_k(
        X_scaled
    )

    print(
        "\nK-Means evaluation:"
    )

    print(
        k_results.to_string(
            index=False
        )
    )

    print(
        f"\nSelected K: {best_k}"
    )

    # --------------------------------------------------------
    # K-Means
    # --------------------------------------------------------

    kmeans = KMeans(
        n_clusters=best_k,
        random_state=42,
        n_init=20
    )

    df["cluster"] = (
        kmeans.fit_predict(
            X_scaled
        )
    )

    kmeans_metrics = (
        clustering_metrics(
            X_scaled,
            df["cluster"]
        )
    )

    print(
        "\nK-Means Metrics:"
    )

    for key, value in (
        kmeans_metrics.items()
    ):

        print(
            f"{key:<25}: "
            f"{value:.4f}"
        )

    # --------------------------------------------------------
    # Agglomerative
    # --------------------------------------------------------

    agglomerative = (
        AgglomerativeClustering(
            n_clusters=best_k
        )
    )

    agglomerative_labels = (
        agglomerative.fit_predict(
            X_scaled
        )
    )

    agglomerative_metrics = (
        clustering_metrics(
            X_scaled,
            agglomerative_labels
        )
    )

    # --------------------------------------------------------
    # DBSCAN
    # --------------------------------------------------------

    dbscan = DBSCAN(
        eps=0.8,
        min_samples=10
    )

    dbscan_labels = (
        dbscan.fit_predict(
            X_scaled
        )
    )

    dbscan_metrics = (
        clustering_metrics(
            X_scaled,
            dbscan_labels
        )
    )

    # --------------------------------------------------------
    # Model comparison
    # --------------------------------------------------------

    comparison = pd.DataFrame({

        "KMeans":
            kmeans_metrics,

        "Agglomerative":
            agglomerative_metrics,

        "DBSCAN":
            dbscan_metrics

    }).T

    print(
        "\nClustering Model Comparison:"
    )

    print(
        comparison.to_string()
    )

    # --------------------------------------------------------
    # Segment naming
    # --------------------------------------------------------

    (
        segment_mapping,
        profile
    ) = generate_segment_names(
        df
    )

    df["segment"] = (
        df["cluster"]
        .map(segment_mapping)
    )

    # --------------------------------------------------------
    # Save models
    # --------------------------------------------------------

    joblib.dump(
        scaler,
        MODEL_DIR / "scaler.pkl"
    )

    joblib.dump(
        kmeans,
        MODEL_DIR / "kmeans.pkl"
    )

    joblib.dump(
        SEGMENTATION_FEATURES,
        MODEL_DIR
        / "segmentation_features.pkl"
    )

    joblib.dump(
        segment_mapping,
        MODEL_DIR
        / "segment_mapping.pkl"
    )

    # --------------------------------------------------------
    # Save evaluation
    # --------------------------------------------------------

    comparison.to_csv(
        ROOT_DIR
        / "data"
        / "processed"
        / "segmentation_model_results.csv"
    )

    k_results.to_csv(
        ROOT_DIR
        / "data"
        / "processed"
        / "kmeans_k_search.csv",
        index=False
    )

    # --------------------------------------------------------
    # Save customer data
    # --------------------------------------------------------

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # --------------------------------------------------------
    # Print profile
    # --------------------------------------------------------

    print(
        "\nCluster Profile:"
    )

    print(
        profile.to_string()
    )

    print(
        "\nCustomer Segment Distribution:"
    )

    print(
        df["segment"]
        .value_counts()
        .to_string()
    )

    print(
        "\nSegmentation completed."
    )


if __name__ == "__main__":

    main()