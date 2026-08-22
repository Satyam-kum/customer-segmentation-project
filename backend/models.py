from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Date,
    Text,
    ForeignKey,
    Index
)

from backend.database import Base


# ============================================================
# CUSTOMER
# ============================================================

class Customer(Base):

    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    recency = Column(
        Float,
        default=0
    )

    frequency = Column(
        Float,
        default=0
    )

    monetary = Column(
        Float,
        default=0
    )

    average_order_value = Column(
        Float,
        default=0
    )

    customer_lifetime = Column(
        Float,
        default=0
    )

    total_quantity = Column(
        Float,
        default=0
    )

    unique_products = Column(
        Float,
        default=0
    )

    avg_purchase_interval = Column(
        Float,
        default=0
    )

    median_purchase_interval = Column(
        Float,
        default=0
    )

    max_purchase_interval = Column(
        Float,
        default=0
    )

    weekend_purchase_ratio = Column(
        Float,
        default=0
    )

    active_months = Column(
        Float,
        default=0
    )

    avg_monthly_orders = Column(
        Float,
        default=0
    )

    max_monthly_orders = Column(
        Float,
        default=0
    )

    avg_monthly_revenue = Column(
        Float,
        default=0
    )

    max_monthly_revenue = Column(
        Float,
        default=0
    )

    items_per_order = Column(
        Float,
        default=0
    )

    country_count = Column(
        Float,
        default=0
    )

    first_purchase = Column(
        DateTime,
        nullable=True
    )

    last_purchase = Column(
        DateTime,
        nullable=True
    )

    cluster = Column(
        Integer,
        nullable=True
    )

    segment = Column(
        String(100),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        Index(
            "idx_customer_segment",
            "segment"
        ),
    )


# ============================================================
# TRANSACTION
# ============================================================

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_no = Column(
        String(50),
        nullable=False,
        index=True
    )

    stock_code = Column(
        String(50),
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    quantity = Column(
        Float,
        nullable=False
    )

    invoice_date = Column(
        DateTime,
        nullable=False,
        index=True
    )

    unit_price = Column(
        Float,
        nullable=False
    )

    revenue = Column(
        Float,
        nullable=False
    )

    customer_id = Column(
        String(50),
        ForeignKey(
            "customers.customer_id"
        ),
        nullable=False,
        index=True
    )

    country = Column(
        String(100),
        nullable=True
    )


# ============================================================
# CHURN PREDICTION
# ============================================================

class ChurnPrediction(Base):

    __tablename__ = "churn_predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        String(50),
        ForeignKey(
            "customers.customer_id"
        ),
        nullable=False,
        index=True
    )

    churn_probability = Column(
        Float,
        nullable=False
    )

    risk = Column(
        String(30),
        nullable=False
    )

    retention_action = Column(
        String(255),
        nullable=True
    )

    prediction_date = Column(
        DateTime,
        default=datetime.utcnow
    )