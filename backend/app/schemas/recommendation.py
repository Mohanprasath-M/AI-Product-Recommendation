from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.schemas.product import ProductOut


class RecommendationItem(BaseModel):
    product: ProductOut
    score: float
    rank: int
    reason: str
    recommendation_type: str  # HYBRID, CONTENT, COLLABORATIVE, BEHAVIORAL, POPULAR, BASKET
    signals: Dict[str, float] = Field(default_factory=dict)  # content, collab, behavior, popularity, rating, personalization


class RecommendationResponse(BaseModel):
    customer_id: Optional[str] = None
    recommendations: List[RecommendationItem]
    count: int
    model_version: str
    algorithm: str
    experiment_group: str = "A"


class RecommendationFeedback(BaseModel):
    product_id: str
    customer_id: str
    action: str  # CLICK, ADD_TO_CART, PURCHASE, DISMISS
    rank: int
    recommendation_type: str


class ABWeightConfig(BaseModel):
    weight_content: float = Field(0.35, ge=0, le=1)
    weight_collaborative: float = Field(0.30, ge=0, le=1)
    weight_behavior: float = Field(0.15, ge=0, le=1)
    weight_popularity: float = Field(0.08, ge=0, le=1)
    weight_rating: float = Field(0.05, ge=0, le=1)
    weight_personalization: float = Field(0.07, ge=0, le=1)
    active_group: str = "A"
