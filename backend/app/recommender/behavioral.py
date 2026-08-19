from datetime import datetime, timezone
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.interaction import Interaction
from app.models.product import Product


class BehavioralBooster:
    """Calculates real-time session intent and recency weight signals."""

    def score_behavioral_signals(
        self,
        db: Session,
        customer_id: str,
        candidate_products: List[Product]
    ) -> Dict[str, float]:
        if not customer_id:
            return {p.id: 0.0 for p in candidate_products}

        # Fetch last 20 interactions sorted by timestamp desc
        recent_interactions = (
            db.query(Interaction)
            .filter(Interaction.customer_id == customer_id)
            .order_by(Interaction.timestamp.desc())
            .limit(20)
            .all()
        )

        if not recent_interactions:
            return {p.id: 0.0 for p in candidate_products}

        # Find recent categories and brands customer interacted with
        recent_pids = [i.product_id for i in recent_interactions]
        interacted_products = db.query(Product).filter(Product.id.in_(recent_pids)).all()
        pid_to_prod = {p.id: p for p in interacted_products}

        category_weights: Dict[str, float] = {}
        brand_weights: Dict[str, float] = {}

        now = datetime.now(timezone.utc)
        for idx, inter in enumerate(recent_interactions):
            # Recency decay factor (more recent = higher weight)
            recency_decay = 1.0 / (idx + 1)
            prod = pid_to_prod.get(inter.product_id)
            if prod:
                category_weights[prod.category] = category_weights.get(prod.category, 0.0) + (inter.weight * recency_decay)
                brand_weights[prod.brand] = brand_weights.get(prod.brand, 0.0) + (inter.weight * recency_decay)

        # Normalize category/brand weights
        max_cat = max(category_weights.values()) if category_weights else 1.0
        max_brand = max(brand_weights.values()) if brand_weights else 1.0

        scores = {}
        for p in candidate_products:
            cat_score = (category_weights.get(p.category, 0.0) / max_cat) if max_cat > 0 else 0.0
            brand_score = (brand_weights.get(p.brand, 0.0) / max_brand) if max_brand > 0 else 0.0
            
            # Blend category and brand intent
            combined = 0.6 * cat_score + 0.4 * brand_score
            scores[p.id] = float(min(1.0, combined))

        return scores


behavioral_booster = BehavioralBooster()
