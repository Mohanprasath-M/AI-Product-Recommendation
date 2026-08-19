from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.product import ProductOut


class CartItemAdd(BaseModel):
    product_id: str
    quantity: int = Field(1, ge=1)


class CartItemOut(BaseModel):
    id: str
    product_id: str
    product: ProductOut
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class OrderItemOut(BaseModel):
    id: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[CartItemAdd]
    payment_method: str = "CREDIT_CARD"
    shipping_address: Optional[str] = "123 AI Innovation Way"


class OrderOut(BaseModel):
    id: str
    order_code: str
    customer_id: str
    total_amount: float
    discount_amount: float
    tax_amount: float
    final_amount: float
    status: str
    payment_method: str
    created_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
