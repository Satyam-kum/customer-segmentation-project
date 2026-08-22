from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy import (
    func
)

from sqlalchemy.orm import Session

from backend.database import get_db

from backend.models import Customer

from backend.schemas import (
    SegmentResponse
)


router = APIRouter(
    prefix="/api/segmentation",
    tags=["Segmentation"]
)


# ============================================================
# SEGMENT SUMMARY
# ============================================================

@router.get(
    "/summary",
    response_model=list[SegmentResponse]
)
def get_segment_summary(

    db: Session = Depends(get_db)
):

    results = (
        db.query(

            Customer.cluster,

            Customer.segment,

            func.count(
                Customer.id
            ).label(
                "customers"
            ),

            func.sum(
                Customer.monetary
            ).label(
                "revenue"
            ),

            func.avg(
                Customer.monetary
            ).label(
                "average_revenue"
            ),

            func.avg(
                Customer.frequency
            ).label(
                "average_frequency"
            ),

            func.avg(
                Customer.recency
            ).label(
                "average_recency"
            )
        )

        .filter(
            Customer.segment.isnot(None)
        )

        .group_by(
            Customer.cluster,
            Customer.segment
        )

        .order_by(
            func.sum(
                Customer.monetary
            ).desc()
        )

        .all()
    )

    return [

        SegmentResponse(

            cluster=row.cluster,

            segment=row.segment,

            customers=row.customers,

            revenue=float(
                row.revenue or 0
            ),

            average_revenue=float(
                row.average_revenue or 0
            ),

            average_frequency=float(
                row.average_frequency or 0
            ),

            average_recency=float(
                row.average_recency or 0
            )
        )

        for row in results
    ]


# ============================================================
# CUSTOMER SEGMENT
# ============================================================

@router.get(
    "/customer/{customer_id}"
)
def get_customer_segment(

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

    return {

        "customer_id":
            customer.customer_id,

        "cluster":
            customer.cluster,

        "segment":
            customer.segment,

        "recency":
            customer.recency,

        "frequency":
            customer.frequency,

        "monetary":
            customer.monetary
    }


# ============================================================
# SEGMENT DISTRIBUTION
# ============================================================

@router.get(
    "/distribution"
)
def segment_distribution(

    db: Session = Depends(get_db)
):

    results = (
        db.query(
            Customer.segment,
            func.count(
                Customer.id
            ).label(
                "count"
            )
        )

        .filter(
            Customer.segment.isnot(None)
        )

        .group_by(
            Customer.segment
        )

        .order_by(
            func.count(
                Customer.id
            ).desc()
        )

        .all()
    )

    return [

        {
            "segment": row.segment,
            "customers": row.count
        }

        for row in results
    ]