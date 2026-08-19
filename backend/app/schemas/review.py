from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    product_id: str
    customer_id: Optional[str] = None
    rating: float = Field(..., ge=1, le=5)
    title: Optional[str] = None
    comment: str = Field(..., min_length=3)


class ReviewOut(BaseModel):
    id: str
    customer_id: str
    customer_name: Optional[str] = "Customer"
    product_id: str
    product_name: Optional[str] = None
    rating: float
    title: Optional[str] = None
    comment: str
    sentiment_label: str  # POSITIVE, NEUTRAL, NEGATIVE
    sentiment_score: float
    positive_topics: List[str] = []
    negative_topics: List[str] = []
    verified_purchase: int
    helpful_votes: int
    created_at: datetime

    class Config:
        from_attributes = True


class SentimentSummary(BaseModel):
    product_id: str
    average_rating: float
    total_reviews: int
    positive_pct: float
    neutral_pct: float
    negative_pct: float
    top_positive_topics: List[Dict[str, Any]] = []
    top_negative_topics: List[Dict[str, Any]] = []
