import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


def get_uuid():
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(String(36), primary_key=True, default=get_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), index=True, nullable=False)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), index=True, nullable=False)
    
    # Event types: VIEW_PRODUCT, CLICK_PRODUCT, ADD_TO_WISHLIST, REMOVE_FROM_WISHLIST,
    # ADD_TO_CART, REMOVE_FROM_CART, CHECKOUT, PURCHASE, RATING, REVIEW, CATEGORY_VIEW, BRAND_VIEW
    event_type = Column(String(50), index=True, nullable=False)
    weight = Column(Float, default=1.0)  # Implicit feedback weight
    session_id = Column(String(100), index=True, nullable=True)
    metadata_json = Column(JSON, default=dict)
    
    timestamp = Column(DateTime, default=utc_now, index=True)

    customer = relationship("Customer", back_populates="interactions")
    product = relationship("Product", back_populates="interactions")


class SearchEvent(Base):
    __tablename__ = "search_events"

    id = Column(String(36), primary_key=True, default=get_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="SET NULL"), nullable=True)
    query = Column(String(255), index=True, nullable=False)
    result_count = Column(Integer, default=0)
    clicked_product_id = Column(String(36), ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    purchased_product_id = Column(String(36), ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
    session_id = Column(String(100), nullable=True)
    timestamp = Column(DateTime, default=utc_now, index=True)


class Wishlist(Base):
    __tablename__ = "wishlists"

    id = Column(String(36), primary_key=True, default=get_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), index=True, nullable=False)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    customer = relationship("Customer", back_populates="wishlist_items")
    product = relationship("Product")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(String(36), primary_key=True, default=get_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), index=True, nullable=False)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), index=True, nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    customer = relationship("Customer", back_populates="cart_items")
    product = relationship("Product")
