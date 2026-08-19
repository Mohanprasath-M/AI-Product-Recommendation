import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.user import Customer
from app.models.interaction import Interaction
from app.core.config import settings
from app.core.redis_client import cache
from app.recommender.content_based import content_recommender
from app.recommender.collaborative import collaborative_recommender
from app.recommender.behavioral import behavioral_booster
from app.recommender.popularity import popularity_ranker
from app.recommender.association import association_recommender
from app.recommender.ranking import candidate_ranker
from app.recommender.explainer import explainer

logger = logging.getLogger(__name__)


class HybridRecommendationEngine:
    """Production Hybrid Recommendation Engine combining multi-source signals."""

    def __init__(self):
        self.default_weights = {
            "weight_content": settings.WEIGHT_CONTENT,
            "weight_collaborative": settings.WEIGHT_COLLABORATIVE,
            "weight_behavior": settings.WEIGHT_BEHAVIOR,
            "weight_popularity": settings.WEIGHT_POPULARITY,
            "weight_rating": settings.WEIGHT_RATING,
            "weight_personalization": settings.WEIGHT_PERSONALIZATION,
        }

    def get_active_weights(self) -> Dict[str, float]:
        cached = cache.get_json("ab_test_weights")
        if cached and isinstance(cached, dict):
            return cached
        return self.default_weights

    def recommend(
        self,
        db: Session,
        customer_id: Optional[str] = None,
        limit: int = 10,
        exclude_purchased: bool = False,
        category: Optional[str] = None,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        weights = custom_weights or self.get_active_weights()
        
        # 1. Fetch Candidate Products from DB
        query = db.query(Product).filter(Product.status == "ACTIVE")
        if category:
            query = query.filter(Product.category == category)
        all_products = query.all()
        
        if not all_products:
            return []

        all_pids = [p.id for p in all_products]
        customer = db.query(Customer).filter(Customer.id == customer_id).first() if customer_id else None

        # Determine products to exclude (already bought or recent)
        exclude_pids = []
        user_history_pids = []
        if customer:
            recent_interactions = db.query(Interaction).filter(Interaction.customer_id == customer.id).all()
            user_history_pids = list(set([i.product_id for i in recent_interactions]))
            if exclude_purchased:
                purchased = [i.product_id for i in recent_interactions if i.event_type == "PURCHASE"]
                exclude_pids.extend(purchased)

        # 2. Content-Based Scoring
        content_scores = content_recommender.score_products_for_user_history(user_history_pids, all_pids)

        # 3. Collaborative Filtering Scoring
        collab_scores = collaborative_recommender.score_products_for_user(customer.id if customer else "", all_pids)

        # 4. Behavioral & Recency Scoring
        behavior_scores = behavioral_booster.score_behavioral_signals(db, customer.id if customer else "", all_products)

        # 5. Popularity & Trend Scoring
        popularity_scores = popularity_ranker.score_popularity(all_products)

        # 6. Customer Profile Personalization Scoring
        personalization_scores = {}
        for p in all_products:
            score = 0.0
            if customer:
                if customer.favorite_category and customer.favorite_category == p.category:
                    score += 0.5
                if customer.favorite_brand and customer.favorite_brand.lower() == p.brand.lower():
                    score += 0.3
                if customer.preferred_price_min <= p.price <= customer.preferred_price_max:
                    score += 0.2
            personalization_scores[p.id] = float(min(1.0, score))

        # 7. Rank & Deduplicate Candidates
        ranked_list = candidate_ranker.rank(
            products=all_products,
            content_scores=content_scores,
            collab_scores=collab_scores,
            behavior_scores=behavior_scores,
            popularity_scores=popularity_scores,
            personalization_scores=personalization_scores,
            weights=weights,
            limit=limit,
            exclude_ids=exclude_pids
        )

        # 8. Attach Explainability & Structure Results
        results = []
        for idx, item in enumerate(ranked_list):
            prod = item["product"]
            reason, rec_type = explainer.explain(prod, item["signals"], customer=customer)
            results.append({
                "product": prod,
                "score": round(item["score"], 4),
                "rank": idx + 1,
                "reason": reason,
                "recommendation_type": rec_type,
                "signals": item["signals"]
            })

        return results

    def get_similar_products(self, db: Session, product_id: str, limit: int = 6) -> List[Dict[str, Any]]:
        sim_pairs = content_recommender.get_similar_products(product_id, top_k=limit)
        if not sim_pairs:
            # Cold start fallback: same category products
            target = db.query(Product).filter(Product.id == product_id).first()
            if target:
                fallback = (
                    db.query(Product)
                    .filter(Product.category == target.category, Product.id != product_id, Product.status == "ACTIVE")
                    .order_by(Product.rating.desc(), Product.views_count.desc())
                    .limit(limit)
                    .all()
                )
                sim_pairs = [(p.id, 0.75) for p in fallback]

        pids = [pid for pid, _ in sim_pairs]
        prods = {p.id: p for p in db.query(Product).filter(Product.id.in_(pids)).all()}
        
        results = []
        for rank, (pid, sim_score) in enumerate(sim_pairs):
            if pid in prods:
                prod = prods[pid]
                results.append({
                    "product": prod,
                    "score": round(sim_score, 4),
                    "rank": rank + 1,
                    "reason": f"Shares similar specifications, features, and brand traits.",
                    "recommendation_type": "SIMILAR",
                    "signals": {"content": sim_score}
                })
        return results

    def get_frequently_bought_together(self, db: Session, product_id: str, limit: int = 4) -> List[Dict[str, Any]]:
        affinity_pairs = association_recommender.get_frequently_bought_together(product_id, top_k=limit)
        pids = [pid for pid, _ in affinity_pairs]
        prods = {p.id: p for p in db.query(Product).filter(Product.id.in_(pids)).all()}

        results = []
        for rank, (pid, conf) in enumerate(affinity_pairs):
            if pid in prods:
                prod = prods[pid]
                results.append({
                    "product": prod,
                    "score": round(conf, 4),
                    "rank": rank + 1,
                    "reason": "Frequently purchased together in the same shopping order.",
                    "recommendation_type": "BASKET",
                    "signals": {"basket_confidence": conf}
                })
        return results


recommender_engine = HybridRecommendationEngine()
