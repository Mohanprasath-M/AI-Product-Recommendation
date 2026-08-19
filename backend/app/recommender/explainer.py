from typing import Dict, Any, Tuple
from app.models.product import Product
from app.models.user import Customer


class RecommendationExplainer:
    """Generates transparent, human-readable explanations for AI recommendations."""

    def explain(
        self,
        product: Product,
        signals: Dict[str, float],
        customer: Customer = None,
        recommendation_type: str = "HYBRID"
    ) -> Tuple[str, str]:
        """
        Returns (reason_string, primary_recommendation_type)
        """
        if recommendation_type == "BASKET":
            return ("Frequently bought together with items in your cart or recent orders.", "BASKET")

        if recommendation_type == "SIMILAR":
            return (f"Similar in features and style to products you've explored in {product.category}.", "CONTENT")

        # Determine dominant signal
        dominant_signal = max(signals.items(), key=lambda x: x[1]) if signals else ("popularity", 1.0)
        sig_name, sig_val = dominant_signal

        if sig_name == "collaborative" and sig_val > 0.4:
            return ("Customers with shopping tastes similar to yours loved this product.", "COLLABORATIVE")

        elif sig_name == "behavior" and sig_val > 0.4:
            if customer and customer.favorite_brand and customer.favorite_brand.lower() == product.brand.lower():
                return (f"Matches your recent interest in {product.brand} products.", "BEHAVIORAL")
            return (f"Recommended because you recently viewed several {product.category} items.", "BEHAVIORAL")

        elif sig_name == "content" and sig_val > 0.35:
            return (f"Matches specifications and tags of items in your browsing history.", "CONTENT")

        elif sig_name == "personalization" and customer and customer.favorite_category == product.category:
            return (f"Tailored to your preference for top-tier {product.category}.", "PERSONALIZATION")

        elif product.trend_status == "TRENDING_UP":
            return (f"Trending now in {product.category} with surging customer demand.", "TRENDING")

        elif product.rating >= 4.5 and product.rating_count >= 10:
            return (f"Top-rated customer favorite with {product.rating}★ rating ({product.rating_count} reviews).", "POPULAR")

        else:
            return (f"Popular selection among shoppers exploring {product.category}.", "POPULAR")


explainer = RecommendationExplainer()
