import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score
)


# ============================================================
# CLASSIFICATION METRICS
# ============================================================

def classification_metrics(
    y_true,
    y_pred,
    y_probability
):

    """
    Calculate classification metrics.
    """

    return {

        "accuracy":
            float(
                accuracy_score(
                    y_true,
                    y_pred
                )
            ),

        "precision":
            float(
                precision_score(
                    y_true,
                    y_pred,
                    zero_division=0
                )
            ),

        "recall":
            float(
                recall_score(
                    y_true,
                    y_pred,
                    zero_division=0
                )
            ),

        "f1":
            float(
                f1_score(
                    y_true,
                    y_pred,
                    zero_division=0
                )
            ),

        "roc_auc":
            float(
                roc_auc_score(
                    y_true,
                    y_probability
                )
            ),

        "pr_auc":
            float(
                average_precision_score(
                    y_true,
                    y_probability
                )
            ),

        "confusion_matrix":
            confusion_matrix(
                y_true,
                y_pred
            ).tolist()
    }


# ============================================================
# CLUSTERING METRICS
# ============================================================

def clustering_metrics(
    X,
    labels
):

    """
    Calculate clustering quality metrics.

    DBSCAN may produce -1 noise labels, so those
    observations are removed for the metric calculation.
    """

    X = np.asarray(X)
    labels = np.asarray(labels)

    valid_mask = (
        labels != -1
    )

    X_valid = X[
        valid_mask
    ]

    labels_valid = labels[
        valid_mask
    ]

    unique_labels = (
        np.unique(labels_valid)
    )

    if len(unique_labels) < 2:

        return {}

    return {

        "silhouette":
            float(
                silhouette_score(
                    X_valid,
                    labels_valid
                )
            ),

        "davies_bouldin":
            float(
                davies_bouldin_score(
                    X_valid,
                    labels_valid
                )
            ),

        "calinski_harabasz":
            float(
                calinski_harabasz_score(
                    X_valid,
                    labels_valid
                )
            )
    }


# ============================================================
# PRINT CLASSIFICATION REPORT
# ============================================================

def print_classification_metrics(
    results
):

    print("\nClassification Results")
    print("-" * 50)

    for metric, value in results.items():

        if metric == "confusion_matrix":

            print(
                f"{metric}:"
            )

            print(
                np.array(value)
            )

        else:

            print(
                f"{metric:<20}: "
                f"{value:.4f}"
            )


# ============================================================
# PRINT CLUSTERING RESULTS
# ============================================================

def print_clustering_metrics(
    name,
    metrics
):

    print(
        f"\n{name} Clustering"
    )

    print("-" * 50)

    if not metrics:

        print(
            "Unable to calculate metrics."
        )

        return

    for metric, value in metrics.items():

        print(
            f"{metric:<20}: "
            f"{value:.4f}"
        )