from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class OverviewKPIs(BaseModel):
    total_customers: int
    total_products: int
    total_orders: int
    total_revenue: float
    conversion_rate: float
    avg_order_value: float
    active_customers: int
    recommendation_ctr: float
    recommendation_revenue_share: float


class RevenueTrendItem(BaseModel):
    date: str
    revenue: float
    orders: int
    new_customers: int


class CategoryPerformanceItem(BaseModel):
    category: str
    revenue: float
    orders: int
    views: int
    conversion_rate: float


class ConversionFunnelOut(BaseModel):
    searches: int
    views: int
    clicks: int
    wishlists: int
    carts: int
    purchases: int
    view_to_cart_pct: float
    cart_to_purchase_pct: float
    overall_conversion_pct: float


class TopProductItem(BaseModel):
    id: str
    name: str
    category: str
    price: float
    revenue: float
    purchases: int
    views: int
    trend_status: str
    rating: float


class AtRiskCustomerItem(BaseModel):
    id: str
    name: str
    email: str
    total_spend: float
    days_since_last_active: int
    churn_risk_score: float
    churn_risk_level: str
    favorite_category: Optional[str] = None


class SearchAnalyticsSummary(BaseModel):
    top_searches: List[Dict[str, Any]] = []
    zero_result_searches: List[Dict[str, Any]] = []
    search_to_click_rate: float = 0.0
    search_to_purchase_rate: float = 0.0
