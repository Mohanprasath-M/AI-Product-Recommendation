import math
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.user import Customer
from app.models.order import Order
from app.models.interaction import Interaction
from app.models.product import Product


class CustomerIntelligenceEngine:
    """Calculates CLV, Churn Risk, Conversion Funnels, and Customer Insights."""

    def compute_clv(self, total_spend: float, total_orders: int, customer_lifespan_days: float = 180.0) -> Dict[str, float]:
        """
        Historical CLV = actual revenue.
        Estimated CLV = (AOV * Purchase Frequency * Estimated Retention Horizon).
        """
        historical_clv = round(total_spend, 2)
        if total_orders == 0:
            return {"historical_clv": 0.0, "estimated_clv": 50.0, "aov": 0.0}

        aov = total_spend / total_orders
        # Purchase rate per month (30 days)
        months = max(1.0, customer_lifespan_days / 30.0)
        purchase_frequency_per_month = total_orders / months

        # 12-month expected forward value with 0.85 retention rate
        retention_rate = 0.85
        margin = 0.30
        forward_months = 12
        discount_factor = 0.95

        forward_orders = purchase_frequency_per_month * forward_months * retention_rate
        estimated_clv = historical_clv + (forward_orders * aov * margin * discount_factor)

        return {
            "historical_clv": historical_clv,
            "estimated_clv": round(estimated_clv, 2),
            "aov": round(aov, 2)
        }

    def compute_churn_risk(
        self,
        days_since_last_active: float,
        days_since_last_purchase: float,
        cart_abandonments: int = 0,
        total_orders: int = 0
    ) -> Dict[str, Any]:
        """
        Calculates risk score (0.0 to 1.0) and key risk drivers.
        """
        score = 0.0
        factors = []

        # Recency inactivity score
        if days_since_last_active > 60:
            score += 0.45
            factors.append(f"Inactive for {int(days_since_last_active)} days")
        elif days_since_last_active > 30:
            score += 0.25
            factors.append(f"Reduced activity in the last {int(days_since_last_active)} days")

        # Purchase lapse score
        if days_since_last_purchase > 90 and total_orders > 0:
            score += 0.35
            factors.append("Prolonged duration without new purchase")
        elif days_since_last_purchase > 45 and total_orders > 0:
            score += 0.15

        # Cart abandonment score
        if cart_abandonments > 2:
            score += 0.20
            factors.append(f"Multiple abandoned cart items ({cart_abandonments})")

        risk_score = round(min(1.0, score), 2)
        if risk_score >= 0.65:
            level = "HIGH"
        elif risk_score >= 0.35:
            level = "MEDIUM"
        else:
            level = "LOW"

        return {
            "churn_risk_score": risk_score,
            "churn_risk_level": level,
            "factors": factors or ["Consistent healthy engagement"]
        }

    def get_customer_journey_funnel(self, db: Session, customer_id: str) -> List[Dict[str, Any]]:
        interactions = db.query(Interaction).filter(Interaction.customer_id == customer_id).all()
        
        stages = {
            "SEARCH": 0,
            "VIEW": 0,
            "CLICK": 0,
            "WISHLIST": 0,
            "CART": 0,
            "PURCHASE": 0
        }

        for i in interactions:
            t = i.event_type.upper()
            if "SEARCH" in t:
                stages["SEARCH"] += 1
            elif "VIEW" in t:
                stages["VIEW"] += 1
            elif "CLICK" in t:
                stages["CLICK"] += 1
            elif "WISHLIST" in t:
                stages["WISHLIST"] += 1
            elif "CART" in t:
                stages["CART"] += 1
            elif "PURCHASE" in t or "CHECKOUT" in t:
                stages["PURCHASE"] += 1

        # Calculate step-by-step conversion & dropoff
        stage_names = ["Search", "View", "Click", "Wishlist", "Cart", "Purchase"]
        keys = ["SEARCH", "VIEW", "CLICK", "WISHLIST", "CART", "PURCHASE"]
        funnel = []

        base_count = max(1, stages["VIEW"] + stages["SEARCH"])
        for idx, (name, key) in enumerate(zip(stage_names, keys)):
            count = stages[key]
            conv_rate = round((count / base_count) * 100.0, 1)
            dropoff_rate = round(max(0.0, 100.0 - conv_rate), 1) if idx > 0 else 0.0
            funnel.append({
                "stage": name,
                "count": count,
                "conversion_rate": min(100.0, conv_rate),
                "dropoff_rate": dropoff_rate
            })

        return funnel

    def get_recommended_actions(self, customer: Customer) -> List[str]:
        actions = []
        if customer.churn_risk_level == "HIGH":
            actions.append("Send Win-Back personalized discount (15% OFF favorite category).")
            actions.append("Trigger re-engagement email highlighting newly added trending items.")
        elif customer.churn_risk_level == "MEDIUM":
            actions.append("Recommend complementary items based on previous purchases.")
            actions.append("Send limited-time free shipping incentive.")
        else:
            actions.append("Enroll in VIP loyalty tier & exclusive early-access deals.")
            actions.append("Prompt for verified product reviews on recent orders.")

        if customer.favorite_category:
            actions.append(f"Feature top-tier {customer.favorite_category} arrivals on personalized homepage.")

        return actions


customer_intelligence = CustomerIntelligenceEngine()
