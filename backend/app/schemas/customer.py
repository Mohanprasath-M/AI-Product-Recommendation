from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class CustomerSegmentOut(BaseModel):
    id: str
    name: str
    cluster_index: int
    persona_title: str
    description: Optional[str] = None
    avg_spending: float
    avg_order_value: float
    avg_purchase_frequency: float
    key_characteristics: Optional[List[str]] = []
    customer_count: int
    updated_at: datetime

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    customer_code: str
    name: str
    email: str
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    persona: Optional[str] = "General Shopper"


class CustomerOut(CustomerBase):
    id: str
    total_spend: float
    total_orders: int
    avg_order_value: float
    clv_historical: float
    clv_estimated: float
    churn_risk_score: float
    churn_risk_level: str
    segment_id: Optional[str] = None
    segment_name: Optional[str] = None
    favorite_category: Optional[str] = None
    favorite_brand: Optional[str] = None
    last_active_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class CustomerJourneyStep(BaseModel):
    stage: str  # Search, View, Click, Wishlist, Cart, Purchase
    count: int
    conversion_rate: float
    dropoff_rate: float


class CustomerInsightOut(BaseModel):
    customer: CustomerOut
    recent_interactions: List[Dict[str, Any]] = []
    top_categories: List[Dict[str, Any]] = []
    top_brands: List[Dict[str, Any]] = []
    journey_funnel: List[CustomerJourneyStep] = []
    recommended_actions: List[str] = []
    clv_breakdown: Dict[str, Any] = {}
    churn_factors: List[str] = []


class PaginatedCustomers(BaseModel):
    items: List[CustomerOut]
    total: int
    page: int
    size: int
    pages: int
