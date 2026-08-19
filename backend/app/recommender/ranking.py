from typing import List, Dict, Any
from app.models.product import Product


class CandidateRanker:
    """Combines multi-modal scores, normalizes, applies diversity, and ranks candidates."""

    def rank(
        self,
        products: List[Product],
        content_scores: Dict[str, float],
        collab_scores: Dict[str, float],
        behavior_scores: Dict[str, float],
        popularity_scores: Dict[str, float],
        personalization_scores: Dict[str, float],
        weights: Dict[str, float],
        limit: int = 10,
        exclude_ids: List[str] = None
    ) -> List[Dict[str, Any]]:
        exclude_set = set(exclude_ids or [])
        ranked_candidates = []

        w_content = weights.get("weight_content", 0.35)
        w_collab = weights.get("weight_collaborative", 0.30)
        w_behavior = weights.get("weight_behavior", 0.15)
        w_pop = weights.get("weight_popularity", 0.08)
        w_rating = weights.get("weight_rating", 0.05)
        w_pers = weights.get("weight_personalization", 0.07)

        # Normalize weights to sum to 1.0
        total_w = w_content + w_collab + w_behavior + w_pop + w_rating + w_pers
        if total_w > 0:
            w_content /= total_w
            w_collab /= total_w
            w_behavior /= total_w
            w_pop /= total_w
            w_rating /= total_w
            w_pers /= total_w

        for prod in products:
            if prod.id in exclude_set or prod.status != "ACTIVE":
                continue

            c_score = content_scores.get(prod.id, 0.0)
            cf_score = collab_scores.get(prod.id, 0.0)
            b_score = behavior_scores.get(prod.id, 0.0)
            p_score = popularity_scores.get(prod.id, 0.0)
            r_score = (prod.rating / 5.0) if prod.rating else 0.0
            pers_score = personalization_scores.get(prod.id, 0.0)

            final_score = (
                w_content * c_score +
                w_collab * cf_score +
                w_behavior * b_score +
                w_pop * p_score +
                w_rating * r_score +
                w_pers * pers_score
            )

            signals = {
                "content": float(c_score),
                "collaborative": float(cf_score),
                "behavior": float(b_score),
                "popularity": float(p_score),
                "rating": float(r_score),
                "personalization": float(pers_score)
            }

            ranked_candidates.append({
                "product": prod,
                "score": float(final_score),
                "signals": signals
            })

        # Sort descending by final score
        ranked_candidates.sort(key=lambda x: x["score"], reverse=True)
        return ranked_candidates[:limit]


candidate_ranker = CandidateRanker()
