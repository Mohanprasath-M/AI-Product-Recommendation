import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from app.core.database import Base


def get_uuid():
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class MLModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(String(36), primary_key=True, default=get_uuid)
    model_name = Column(String(100), index=True, nullable=False)  # hybrid_recommender, sentiment_classifier, segmentation_kmeans
    version = Column(String(50), nullable=False)  # v1.0, v1.1
    algorithm = Column(String(100), nullable=False)
    hyperparameters = Column(JSON, default=dict)
    metrics = Column(JSON, default=dict)  # Precision@10, NDCG, Silhouette, F1, etc.
    is_active = Column(Boolean, default=False)
    artifact_path = Column(String(255), nullable=True)
    dataset_size = Column(Integer, default=0)
    training_duration_seconds = Column(Float, default=0.0)
    trained_by = Column(String(100), default="SYSTEM")
    created_at = Column(DateTime, default=utc_now)


class ModelMetric(Base):
    __tablename__ = "model_metrics"

    id = Column(String(36), primary_key=True, default=get_uuid)
    model_version_id = Column(String(36), ForeignKey("model_versions.id", ondelete="CASCADE"), nullable=False)
    metric_name = Column(String(100), nullable=False)  # precision_at_k, recall_at_k, ndcg_at_k, silhouette, f1_score
    metric_value = Column(Float, nullable=False)
    k_value = Column(Integer, nullable=True)  # e.g., 5, 10
    created_at = Column(DateTime, default=utc_now)


class RecommendationEvent(Base):
    __tablename__ = "recommendation_events"

    id = Column(String(36), primary_key=True, default=get_uuid)
    customer_id = Column(String(36), index=True, nullable=False)
    product_id = Column(String(36), index=True, nullable=False)
    model_version = Column(String(50), default="v1.0")
    recommendation_type = Column(String(50), default="HYBRID")  # HYBRID, CONTENT, COLLABORATIVE, TRENDING, BASKET
    score = Column(Float, default=0.0)
    rank = Column(Integer, default=1)
    
    clicked = Column(Boolean, default=False)
    added_to_cart = Column(Boolean, default=False)
    purchased = Column(Boolean, default=False)
    experiment_group = Column(String(20), default="A")  # A/B Testing: A, B
    
    timestamp = Column(DateTime, default=utc_now, index=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=get_uuid)
    user_id = Column(String(36), nullable=True)
    user_email = Column(String(255), nullable=True)
    action = Column(String(100), nullable=False)  # LOGIN, RETRAIN_MODEL, CREATE_PRODUCT, BULK_IMPORT
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=utc_now, index=True)
