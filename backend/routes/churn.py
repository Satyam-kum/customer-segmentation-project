from pathlib import Path

import joblib

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from backend.database import get_db

from backend.models import (
    Customer,
    ChurnPrediction
)

from backend.schemas import (
    ChurnPredictionResponse
)


router = APIRouter(
    prefix="/api/churn",
    tags=["Churn"]
)


# ============================================================
# MODEL PATH
# ============================================================

ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parents[2]
)

MODEL_PATH = (
    ROOT_DIR
    / "models"
    / "churn_model.pkl"
)

FEATURE_PATH = (
    ROOT_DIR
    / "models"
    / "feature_columns.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

def load_churn_model():

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            "churn_model.pkl not found. "
            "Run python -m ml.train first."
        )

    return joblib.load(
        MODEL_PATH
    )


def load_feature_columns():

    if not FEATURE_PATH.exists():

        raise FileNotFoundError(
            "feature_columns.pkl not found."
        )

    return joblib.load(
        FEATURE_PATH
    )


# ============================================================
# RISK CLASSIFICATION
# ============================================================

def get_risk(
    probability: float
) -> str:

    if probability >= 0.75:

        return "HIGH"

    if probability >= 0.45:

        return "MEDIUM"

    return "LOW"


# ============================================================
# RETENTION ACTION
# ============================================================

def get_retention_action(
    probability: float,
    monetary: float
) -> str:

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


# ============================================================
# CUSTOMER CHURN
# ============================================================

@router.get(
    "/customer/{customer_id}",
    response_model=ChurnPredictionResponse
)
def predict_customer_churn(

    customer_id: str,

    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.customer_id
            == customer_id
        )
        .first()
    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    try:

        model = (
            load_churn_model()
        )

        feature_columns = (
            load_feature_columns()
        )

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    # --------------------------------------------------------
    # Build model input
    # --------------------------------------------------------

    data = {

        feature:
            getattr(
                customer,
                feature,
                0
            )

        for feature
        in feature_columns
    }

    import pandas as pd

    X = pd.DataFrame(
        [data],
        columns=feature_columns
    )

    probability = float(
        model.predict_proba(X)[0][1]
    )

    risk = get_risk(
        probability
    )

    action = get_retention_action(
        probability,
        customer.monetary
    )

    # --------------------------------------------------------
    # Store prediction
    # --------------------------------------------------------

    prediction = ChurnPrediction(

        customer_id=
            customer.customer_id,

        churn_probability=
            probability,

        risk=
            risk,

        retention_action=
            action
    )

    db.add(
        prediction
    )

    db.commit()

    return ChurnPredictionResponse(

        customer_id=
            customer.customer_id,

        churn_probability=
            round(
                probability,
                4
            ),

        risk=
            risk,

        retention_action=
            action
    )


# ============================================================
# HIGH-RISK CUSTOMERS
# ============================================================

@router.get(
    "/high-risk"
)
def get_high_risk_customers(

    limit: int = 50,

    db: Session = Depends(get_db)
):

    predictions = (
        db.query(
            ChurnPrediction
        )

        .filter(
            ChurnPrediction.risk
            == "HIGH"
        )

        .order_by(
            ChurnPrediction
            .churn_probability
            .desc()
        )

        .limit(limit)

        .all()
    )

    return [

        {
            "customer_id":
                row.customer_id,

            "churn_probability":
                row.churn_probability,

            "risk":
                row.risk,

            "retention_action":
                row.retention_action,

            "prediction_date":
                row.prediction_date
        }

        for row in predictions
    ]