from typing import List, Dict
from app.models.product import Product


class PopularityRanker:
    """Computes global popularity and trending velocity scores."""

    def score_popularity(self, products: List[Product]) -> Dict[str, float]:
        if not products:
            return {}

        max_views = max([p.views_count for p in products] or [1])
        max_purchases = max([p.purchases_count for p in products] or [1])
        max_rating_count = max([p.rating_count for p in products] or [1])

        scores = {}
        for p in products:
            view_ratio = p.views_count / max_views if max_views > 0 else 0.0
            purchase_ratio = p.purchases_count / max_purchases if max_purchases > 0 else 0.0
            rating_norm = (p.rating / 5.0) if p.rating else 0.0
            review_ratio = p.rating_count / max_rating_count if max_rating_count > 0 else 0.0

            # Composite popularity score: 40% purchases + 30% views + 20% rating + 10% review volume
            score = (
                0.40 * purchase_ratio +
                0.30 * view_ratio +
                0.20 * rating_norm +
                0.10 * review_ratio
            )
            scores[p.id] = float(min(1.0, score))

        return scores

    def score_trending(self, products: List[Product]) -> Dict[str, float]:
        if not products:
            return {}

        scores = {}
        for p in products:
            # Positive trend_score means trending up
            trend_val = p.trend_score if p.trend_score is not None else 0.0
            norm_trend = max(0.0, min(1.0, (trend_val + 50.0) / 100.0))
            scores[p.id] = float(norm_trend)

        return scores


popularity_ranker = PopularityRanker()
