from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class CategoryOut(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = "Tag"
    product_count: Optional[int] = 0

    class Config:
        from_attributes = True


class BrandOut(BaseModel):
    id: str
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    product_count: Optional[int] = 0

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    subcategory: Optional[str] = None
    brand: str
    price: float = Field(..., gt=0)
    discount: float = Field(0.0, ge=0, le=100)
    stock: int = Field(100, ge=0)
    image_url: Optional[str] = None
    tags: Optional[str] = ""
    specifications: Optional[Dict[str, Any]] = Field(default_factory=dict)
    status: Optional[str] = "ACTIVE"


class ProductCreate(ProductBase):
    product_code: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    discount: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    tags: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ProductStockUpdate(BaseModel):
    stock: int = Field(..., ge=0)


class ProductOut(ProductBase):
    id: str
    product_code: str
    rating: float
    rating_count: int
    views_count: int
    clicks_count: int
    cart_adds_count: int
    wishlist_adds_count: int
    purchases_count: int
    revenue_generated: float
    popularity_score: float
    trend_score: float
    trend_status: str
    sentiment_score: float
    positive_sentiment_pct: float
    neutral_sentiment_pct: float
    negative_sentiment_pct: float
    top_positive_topics: List[str] = []
    top_negative_topics: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedProducts(BaseModel):
    items: List[ProductOut]
    total: int
    page: int
    size: int
    pages: int
