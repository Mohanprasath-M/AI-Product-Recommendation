import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


def get_uuid():
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String(36), primary_key=True, default=get_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), index=True, nullable=False)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), index=True, nullable=False)
    
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    title = Column(String(255), nullable=True)
    comment = Column(Text, nullable=False)
    
    # NLP inference results
    sentiment_label = Column(String(20), default="NEUTRAL")  # POSITIVE, NEUTRAL, NEGATIVE
    sentiment_score = Column(Float, default=0.0)  # -1.0 to 1.0 (or probability)
    positive_topics = Column(JSON, default=list)  # extracted keywords
    negative_topics = Column(JSON, default=list)  # extracted keywords
    
    verified_purchase = Column(Integer, default=1)
    helpful_votes = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=utc_now, index=True)

    customer = relationship("Customer", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
