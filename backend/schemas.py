from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# CUSTOMER
# ============================================================

class CustomerResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    customer_id: str

    recency: float = 0

    frequency: float = 0

    monetary: float = 0

    average_order_value: float = 0

    customer_lifetime: float = 0

    total_quantity: float = 0

    unique_products: float = 0

    avg_purchase_interval: float = 0

    median_purchase_interval: float = 0

    weekend_purchase_ratio: float = 0

    active_months: float = 0

    avg_monthly_orders: float = 0

    cluster: Optional[int] = None

    segment: Optional[str] = None


# ============================================================
# CUSTOMER LIST
# ============================================================

class CustomerListResponse(BaseModel):

    total: int

    page: int

    page_size: int

    customers: list[CustomerResponse]


# ============================================================
# SEGMENT
# ============================================================

class SegmentResponse(BaseModel):

    cluster: int

    segment: str

    customers: int

    revenue: float

    average_revenue: float

    average_frequency: float

    average_recency: float


# ============================================================
# CHURN
# ============================================================

class ChurnPredictionResponse(BaseModel):

    customer_id: str

    churn_probability: float

    risk: str

    retention_action: str


# ============================================================
# DASHBOARD
# ============================================================

class DashboardResponse(BaseModel):

    total_customers: int

    total_orders: int

    total_revenue: float

    average_order_value: float

    high_risk_customers: int

    revenue_at_risk: float


# ============================================================
# REVENUE
# ============================================================

class RevenuePoint(BaseModel):

    period: str

    revenue: float

    orders: int


# ============================================================
# COHORT
# ============================================================

class RetentionPoint(BaseModel):

    cohort: str

    month_index: int

    customers: int

    retention_rate: float