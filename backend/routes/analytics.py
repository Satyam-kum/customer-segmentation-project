
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.database import SessionLocal
from backend.models import Customer, Transaction


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# ============================================================
# DATABASE DEPENDENCY
# ============================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# DASHBOARD
# ============================================================

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db)
):

    try:

        # ----------------------------------------------------
        # Total customers
        # ----------------------------------------------------

        total_customers = (
            db.query(
                func.count(Customer.id)
            )
            .scalar()
        ) or 0


        # ----------------------------------------------------
        # Total unique invoices
        # ----------------------------------------------------

        total_orders = (
            db.query(
                func.count(
                    func.distinct(
                        Transaction.invoice_no
                    )
                )
            )
            .scalar()
        ) or 0


        # ----------------------------------------------------
        # Total revenue
        # ----------------------------------------------------

        total_revenue = (
            db.query(
                func.coalesce(
                    func.sum(
                        Transaction.revenue
                    ),
                    0
                )
            )
            .scalar()
        ) or 0


        # ----------------------------------------------------
        # Revenue at risk
        # ----------------------------------------------------

        revenue_at_risk = 0.0


        # ----------------------------------------------------
        # High-risk customers
        # ----------------------------------------------------

        high_risk_customers = 0


        return {

            "total_customers":
                int(total_customers),

            "total_orders":
                int(total_orders),

            "total_revenue":
                float(total_revenue),

            "revenue_at_risk":
                float(revenue_at_risk),

            "high_risk_customers":
                int(high_risk_customers)
        }


    except Exception as error:

        print(
            "ERROR in /analytics/dashboard:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# REVENUE TREND
# ============================================================

@router.get("/revenue")
def get_revenue(
    db: Session = Depends(get_db)
):

    try:

        rows = (
            db.query(

                func.date_trunc(
                    "month",
                    Transaction.invoice_date
                ).label("month"),

                func.coalesce(
                    func.sum(
                        Transaction.revenue
                    ),
                    0
                ).label("revenue")
            )

            .group_by(

                func.date_trunc(
                    "month",
                    Transaction.invoice_date
                )
            )

            .order_by(

                func.date_trunc(
                    "month",
                    Transaction.invoice_date
                )
            )

            .all()
        )


        result = []


        for row in rows:

            result.append({

                "month":
                    row.month.strftime(
                        "%Y-%m"
                    ),

                "revenue":
                    float(
                        row.revenue or 0
                    )
            })


        return result


    except Exception as error:

        print(
            "ERROR in /analytics/revenue:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# SEGMENT DISTRIBUTION
# ============================================================

@router.get("/segments")
def get_segments(
    db: Session = Depends(get_db)
):

    try:

        rows = (
            db.query(

                Customer.segment.label(
                    "segment"
                ),

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
                desc("count")
            )

            .all()
        )


        result = []


        for row in rows:

            result.append({

                "segment":
                    row.segment,

                "count":
                    int(
                        row.count or 0
                    )
            })


        return result


    except Exception as error:

        print(
            "ERROR in /analytics/segments:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# RETENTION SUMMARY
# ============================================================

@router.get("/retention")
def get_retention(
    db: Session = Depends(get_db)
):

    try:

        # ----------------------------------------------------
        # Calculate order count for every customer
        # ----------------------------------------------------

        customer_orders = (

            db.query(

                Transaction.customer_id.label(
                    "customer_id"
                ),

                func.count(
                    func.distinct(
                        Transaction.invoice_no
                    )
                ).label(
                    "order_count"
                )
            )

            .filter(
                Transaction.customer_id.isnot(None)
            )

            .group_by(
                Transaction.customer_id
            )

            .subquery()
        )


        # ----------------------------------------------------
        # Total customers
        #
        # Use customers table because it represents the
        # complete customer population.
        # ----------------------------------------------------

        total_customers = (

            db.query(
                func.count(Customer.id)
            )

            .scalar()

        ) or 0


        # ----------------------------------------------------
        # Repeat customers
        #
        # A repeat customer has more than one unique invoice.
        # ----------------------------------------------------

        repeat_customers = (

            db.query(
                func.count(
                    customer_orders.c.customer_id
                )
            )

            .filter(
                customer_orders.c.order_count > 1
            )

            .scalar()

        ) or 0


        # ----------------------------------------------------
        # Repeat purchase rate
        # ----------------------------------------------------

        if total_customers > 0:

            repeat_purchase_rate = (
                float(repeat_customers)
                /
                float(total_customers)
            )

        else:

            repeat_purchase_rate = 0.0


        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return {

            "total_customers":
                int(total_customers),

            "repeat_customers":
                int(repeat_customers),

            "repeat_purchase_rate":
                float(repeat_purchase_rate)
        }


    except Exception as error:

        print(
            "ERROR in /analytics/retention:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# RETENTION BY SEGMENT
# ============================================================

@router.get("/retention-by-segment")
def get_retention_by_segment(
    db: Session = Depends(get_db)
):

    try:

        # ----------------------------------------------------
        # Aggregate transaction information per customer
        # ----------------------------------------------------

        customer_transaction_summary = (

            db.query(

                Transaction.customer_id.label(
                    "customer_id"
                ),

                func.count(
                    func.distinct(
                        Transaction.invoice_no
                    )
                ).label(
                    "frequency"
                ),

                func.coalesce(
                    func.sum(
                        Transaction.revenue
                    ),
                    0
                ).label(
                    "revenue"
                )

            )

            .filter(
                Transaction.customer_id.isnot(None)
            )

            .group_by(
                Transaction.customer_id
            )

            .subquery()
        )


        # ----------------------------------------------------
        # Join customer data with transaction summary
        #
        # LEFT OUTER JOIN is used so customers without
        # transaction information are not accidentally lost.
        # ----------------------------------------------------

        rows = (

            db.query(

                Customer.segment.label(
                    "segment"
                ),

                func.count(
                    Customer.id
                ).label(
                    "customers"
                ),

                func.coalesce(
                    func.sum(
                        customer_transaction_summary.c.revenue
                    ),
                    0
                ).label(
                    "revenue"
                ),

                func.coalesce(
                    func.avg(
                        customer_transaction_summary.c.frequency
                    ),
                    0
                ).label(
                    "average_frequency"
                ),

                func.coalesce(
                    func.avg(
                        Customer.recency
                    ),
                    0
                ).label(
                    "average_recency"
                )

            )

            .outerjoin(

                customer_transaction_summary,

                Customer.customer_id
                ==
                customer_transaction_summary.c.customer_id

            )

            .filter(
                Customer.segment.isnot(None)
            )

            .group_by(
                Customer.segment
            )

            .order_by(
                desc("revenue")
            )

            .all()
        )


        # ----------------------------------------------------
        # Format API response
        # ----------------------------------------------------

        result = []


        for row in rows:

            result.append({

                "segment":
                    (
                        row.segment
                        if row.segment
                        else "Unassigned"
                    ),

                "customers":
                    int(
                        row.customers or 0
                    ),

                "revenue":
                    float(
                        row.revenue or 0
                    ),

                "average_frequency":
                    float(
                        row.average_frequency or 0
                    ),

                "average_recency":
                    float(
                        row.average_recency or 0
                    )
            })


        return result


    except Exception as error:

        print(
            "ERROR in /analytics/retention-by-segment:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# TOP CUSTOMERS
# ============================================================

@router.get("/top-customers")
def get_top_customers(
    limit: int = 10,
    db: Session = Depends(get_db)
):

    try:

        # ----------------------------------------------------
        # Aggregate transaction information
        # ----------------------------------------------------

        transaction_summary = (

            db.query(

                Transaction.customer_id.label(
                    "customer_id"
                ),

                func.count(
                    func.distinct(
                        Transaction.invoice_no
                    )
                ).label(
                    "orders"
                ),

                func.coalesce(
                    func.sum(
                        Transaction.revenue
                    ),
                    0
                ).label(
                    "revenue"
                )
            )

            .filter(
                Transaction.customer_id.isnot(None)
            )

            .group_by(
                Transaction.customer_id
            )

            .subquery()
        )


        # ----------------------------------------------------
        # Join customers with transactions
        # ----------------------------------------------------

        rows = (

            db.query(

                Customer.customer_id,

                Customer.segment,

                Customer.recency,

                transaction_summary.c.orders,

                transaction_summary.c.revenue

            )

            .join(

                transaction_summary,

                Customer.customer_id
                ==
                transaction_summary.c.customer_id

            )

            .order_by(

                desc(
                    transaction_summary.c.revenue
                )
            )

            .limit(
                limit
            )

            .all()
        )


        # ----------------------------------------------------
        # Format API response
        # ----------------------------------------------------

        result = []


        for row in rows:

            result.append({

                "customer_id":
                    str(
                        row.customer_id
                    ),

                "segment":
                    (
                        row.segment
                        if row.segment
                        else "Unassigned"
                    ),

                "recency":
                    float(
                        row.recency or 0
                    ),

                "orders":
                    int(
                        row.orders or 0
                    ),

                "revenue":
                    float(
                        row.revenue or 0
                    )
            })


        return result


    except Exception as error:

        print(
            "ERROR in /analytics/top-customers:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )