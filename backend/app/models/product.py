import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


def get_uuid():
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=get_uuid)
    name = Column(String(100), unique=True, index=True, nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), default="Tag")
    created_at = Column(DateTime, default=utc_now)

    products = relationship("Product", back_populates="category_rel")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(String(36), primary_key=True, default=get_uuid)
    name = Column(String(100), unique=True, index=True, nullable=False)
    logo_url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now)

    products = relationship("Product", back_populates="brand_rel")


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=get_uuid)
    product_code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    subcategory = Column(String(100), index=True, nullable=True)
    category_id = Column(String(36), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    brand = Column(String(100), index=True, nullable=False)
    brand_id = Column(String(36), ForeignKey("brands.id", ondelete="SET NULL"), nullable=True)
    
    price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)  # percentage discount (e.g. 10.0 for 10%)
    stock = Column(Integer, default=100)
    
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    image_url = Column(String(500), nullable=True)
    tags = Column(String(500), default="")  # comma-separated tags
    specifications = Column(JSON, default=dict)  # structured key-value specs
    status = Column(String(50), default="ACTIVE")  # ACTIVE, OUT_OF_STOCK, ARCHIVED

    # ML & Intelligence metrics
    views_count = Column(Integer, default=0)
    clicks_count = Column(Integer, default=0)
    cart_adds_count = Column(Integer, default=0)
    wishlist_adds_count = Column(Integer, default=0)
    purchases_count = Column(Integer, default=0)
    revenue_generated = Column(Float, default=0.0)
    popularity_score = Column(Float, default=0.0)
    trend_score = Column(Float, default=0.0)  # > 0 trending up, < 0 trending down
    trend_status = Column(String(20), default="STABLE")  # TRENDING_UP, STABLE, TRENDING_DOWN

    # NLP Sentiment aggregates
    sentiment_score = Column(Float, default=0.0)  # -1.0 to 1.0
    positive_sentiment_pct = Column(Float, default=0.0)
    neutral_sentiment_pct = Column(Float, default=0.0)
    negative_sentiment_pct = Column(Float, default=0.0)
    top_positive_topics = Column(JSON, default=list)
    top_negative_topics = Column(JSON, default=list)

    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    category_rel = relationship("Category", back_populates="products")
    brand_rel = relationship("Brand", back_populates="products")
    interactions = relationship("Interaction", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    feature_ml = relationship("ProductFeatureML", back_populates="product", uselist=False, cascade="all, delete-orphan")


class ProductFeatureML(Base):
    __tablename__ = "product_features_ml"

    id = Column(String(36), primary_key=True, default=get_uuid)
    product_id = Column(String(36), ForeignKey("products.id", ondelete="CASCADE"), unique=True, nullable=False)
    combined_features_text = Column(Text, nullable=False)  # Normalized text for TF-IDF
    tfidf_feature_indices = Column(JSON, default=list)
    embedding_vector = Column(JSON, default=list)  # SVD / Dense representation
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    product = relationship("Product", back_populates="feature_ml")
