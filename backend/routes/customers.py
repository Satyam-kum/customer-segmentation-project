from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from backend.database import get_db

from backend.models import Customer

from backend.schemas import (
    CustomerResponse,
    CustomerListResponse
)


router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"]
)


# ============================================================
# LIST CUSTOMERS
# ============================================================

@router.get(
    "",
    response_model=CustomerListResponse
)
def get_customers(

    page: int = Query(
        1,
        ge=1
    ),

    page_size: int = Query(
        20,
        ge=1,
        le=100
    ),

    search: str | None = Query(
        None
    ),

    segment: str | None = Query(
        None
    ),

    db: Session = Depends(get_db)
):

    query = db.query(
        Customer
    )

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    if search:

        query = query.filter(
            Customer.customer_id.ilike(
                f"%{search}%"
            )
        )

    # --------------------------------------------------------
    # Segment filter
    # --------------------------------------------------------

    if segment:

        query = query.filter(
            Customer.segment == segment
        )

    total = query.count()

    customers = (
        query
        .order_by(
            Customer.monetary.desc()
        )
        .offset(
            (page - 1) * page_size
        )
        .limit(
            page_size
        )
        .all()
    )

    return CustomerListResponse(

        total=total,

        page=page,

        page_size=page_size,

        customers=customers
    )


# ============================================================
# CUSTOMER DETAIL
# ============================================================

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(

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

    return customer