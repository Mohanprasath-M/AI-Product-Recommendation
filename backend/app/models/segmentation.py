import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


def get_uuid():
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    id = Column(String(36), primary_key=True, default=get_uuid)
    name = Column(String(100), unique=True, index=True, nullable=False)  # e.g., "High-Value Loyalists", "Budget Shoppers"
    cluster_index = Column(Integer, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    customer_count = Column(Integer, default=0)
    avg_spending = Column(Float, default=0.0)
    avg_order_value = Column(Float, default=0.0)
    avg_purchase_frequency = Column(Float, default=0.0)
    avg_churn_risk = Column(Float, default=0.0)
    key_characteristics = Column(JSON, default=list)  # bullet points of traits
    cluster_center = Column(JSON, default=list)  # normalized centroid vector
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    customers = relationship("Customer", back_populates="segment")


class CustomerFeature(Base):
    __tablename__ = "customer_features"

    id = Column(String(36), primary_key=True, default=get_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    recency_days = Column(Float, default=0.0)
    frequency = Column(Integer, default=0)
    monetary = Column(Float, default=0.0)
    avg_order_value = Column(Float, default=0.0)
    total_interactions = Column(Integer, default=0)
    view_to_purchase_ratio = Column(Float, default=0.0)
    category_entropy = Column(Float, default=0.0)
    discount_affinity = Column(Float, default=0.0)
    top_categories_json = Column(JSON, default=list)
    top_brands_json = Column(JSON, default=list)
    feature_vector = Column(JSON, default=list)
    
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
