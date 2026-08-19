from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.interaction import Interaction
from app.models.review import Review


class ProductIntelligenceEngine:
    """Calculates product conversion metrics, trend velocities, and sentiment profiles."""

    def compute_product_metrics(self, db: Session, product: Product) -> Dict[str, Any]:
        views = product.views_count or 0
        clicks = product.clicks_count or 0
        carts = product.cart_adds_count or 0
        purchases = product.purchases_count or 0
        
        view_to_cart = round((carts / views * 100), 2) if views > 0 else 0.0
        cart_to_purchase = round((purchases / carts * 100), 2) if carts > 0 else 0.0
        conversion_rate = round((purchases / views * 100), 2) if views > 0 else 0.0

        # Reviews sentiment
        reviews = db.query(Review).filter(Review.product_id == product.id).all()
        total_rev = len(reviews)
        pos_rev = sum(1 for r in reviews if r.sentiment_label == "POSITIVE")
        neu_rev = sum(1 for r in reviews if r.sentiment_label == "NEUTRAL")
        neg_rev = sum(1 for r in reviews if r.sentiment_label == "NEGATIVE")

        pos_pct = round((pos_rev / total_rev * 100), 1) if total_rev > 0 else 0.0
        neu_pct = round((neu_rev / total_rev * 100), 1) if total_rev > 0 else 0.0
        neg_pct = round((neg_rev / total_rev * 100), 1) if total_rev > 0 else 0.0

        # Extract top positive & negative topics
        pos_topics = []
        neg_topics = []
        for r in reviews:
            if r.positive_topics and isinstance(r.positive_topics, list):
                pos_topics.extend(r.positive_topics)
            if r.negative_topics and isinstance(r.negative_topics, list):
                neg_topics.extend(r.negative_topics)

        from collections import Counter
        top_pos = [item[0] for item in Counter(pos_topics).most_common(5)]
        top_neg = [item[0] for item in Counter(neg_topics).most_common(5)]

        return {
            "views": views,
            "clicks": clicks,
            "cart_adds": carts,
            "purchases": purchases,
            "revenue": round(product.revenue_generated, 2),
            "view_to_cart_rate": view_to_cart,
            "cart_to_purchase_rate": cart_to_purchase,
            "conversion_rate": conversion_rate,
            "average_rating": round(product.rating, 2),
            "total_reviews": total_rev,
            "sentiment_score": round(product.sentiment_score, 2),
            "positive_sentiment_pct": pos_pct,
            "neutral_sentiment_pct": neu_pct,
            "negative_sentiment_pct": neg_pct,
            "top_positive_topics": top_pos,
            "top_negative_topics": top_neg,
            "trend_score": round(product.trend_score, 2),
            "trend_status": product.trend_status
        }


product_intelligence = ProductIntelligenceEngine()
