from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class TrackEventRequest(BaseModel):
    customer_id: str
    product_id: Optional[str] = None
    event_type: str  # VIEW_PRODUCT, CLICK_PRODUCT, ADD_TO_WISHLIST, REMOVE_FROM_WISHLIST, ADD_TO_CART, REMOVE_FROM_CART, CHECKOUT, PURCHASE, RATING, REVIEW, CATEGORY_VIEW, BRAND_VIEW
    session_id: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = Field(default_factory=dict)


class SearchEventRequest(BaseModel):
    customer_id: Optional[str] = None
    query: str
    result_count: int = 0
    clicked_product_id: Optional[str] = None
    session_id: Optional[str] = None


class LiveActivityItem(BaseModel):
    id: str
    customer_id: str
    customer_name: Optional[str] = "Anonymous"
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    event_type: str
    timestamp: datetime
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
