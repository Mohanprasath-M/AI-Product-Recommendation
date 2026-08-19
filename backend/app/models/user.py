import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


def get_uuid():
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=get_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="CUSTOMER", nullable=False)  # ADMIN, ANALYST, CUSTOMER
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    customer = relationship("Customer", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, default=get_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    customer_code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), index=True, nullable=False)
    phone = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    location = Column(String(100), nullable=True)
    persona = Column(String(100), default="General Shopper")
    
    # Aggregated metrics for fast lookups
    total_spend = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    avg_order_value = Column(Float, default=0.0)
    clv_historical = Column(Float, default=0.0)
    clv_estimated = Column(Float, default=0.0)
    churn_risk_score = Column(Float, default=0.0)  # 0.0 to 1.0
    churn_risk_level = Column(String(20), default="LOW")  # LOW, MEDIUM, HIGH
    segment_id = Column(String(36), ForeignKey("customer_segments.id", ondelete="SET NULL"), nullable=True)
    
    favorite_category = Column(String(100), nullable=True)
    favorite_brand = Column(String(100), nullable=True)
    preferred_price_min = Column(Float, default=0.0)
    preferred_price_max = Column(Float, default=1000.0)

    last_active_at = Column(DateTime, default=utc_now)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="customer")
    segment = relationship("CustomerSegment", back_populates="customers")
    interactions = relationship("Interaction", back_populates="customer", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="customer", cascade="all, delete-orphan")
    wishlist_items = relationship("Wishlist", back_populates="customer", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="customer", cascade="all, delete-orphan")
