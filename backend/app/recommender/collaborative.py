import logging
import numpy as np
from typing import List, Dict, Tuple, Optional
from app.ml.model_registry import registry

logger = logging.getLogger(__name__)


class CollaborativeRecommender:
    def __init__(self):
        self._load_model()

    def _load_model(self):
        self.artifact = registry.load_artifact("collaborative_model")
        # artifact contains: {'user_factors': matrix, 'item_factors': matrix, 'user_ids': list, 'product_ids': list, 'user_to_idx': dict, 'product_to_idx': dict, 'svd_model': model}

    def reload(self):
        self._load_model()

    def score_products_for_user(self, customer_id: str, candidate_ids: List[str]) -> Dict[str, float]:
        if not self.artifact:
            self._load_model()
        if not self.artifact:
            return {p_id: 0.0 for p_id in candidate_ids}

        user_to_idx = self.artifact.get("user_to_idx", {})
        product_to_idx = self.artifact.get("product_to_idx", {})
        user_factors = self.artifact.get("user_factors")
        item_factors = self.artifact.get("item_factors")

        if customer_id not in user_to_idx or user_factors is None or item_factors is None:
            return {p_id: 0.0 for p_id in candidate_ids}

        u_idx = user_to_idx[customer_id]
        u_vec = user_factors[u_idx]  # shape: (n_components,)

        # Dot product with item latent vectors
        scores = {}
        for p_id in candidate_ids:
            if p_id in product_to_idx:
                p_idx = product_to_idx[p_id]
                p_vec = item_factors[p_idx]
                score = float(np.dot(u_vec, p_vec))
                scores[p_id] = score
            else:
                scores[p_id] = 0.0

        # Min-Max normalize non-zero scores between 0 and 1
        val_list = [v for v in scores.values() if v > 0]
        if val_list:
            min_v, max_v = min(val_list), max(val_list)
            if max_v > min_v:
                for k in scores:
                    if scores[k] > 0:
                        scores[k] = (scores[k] - min_v) / (max_v - min_v)
        return scores

    def get_similar_users(self, customer_id: str, top_k: int = 5) -> List[str]:
        if not self.artifact:
            self._load_model()
        if not self.artifact:
            return []
        user_to_idx = self.artifact.get("user_to_idx", {})
        user_factors = self.artifact.get("user_factors")
        user_ids = self.artifact.get("user_ids", [])
        if customer_id not in user_to_idx or user_factors is None:
            return []
        u_idx = user_to_idx[customer_id]
        u_vec = user_factors[u_idx].reshape(1, -1)
        from sklearn.metrics.pairwise import cosine_similarity
        sims = cosine_similarity(u_vec, user_factors).flatten()
        ranked = np.argsort(sims)[::-1]
        results = []
        for i in ranked:
            uid = user_ids[i]
            if uid != customer_id:
                results.append(uid)
                if len(results) >= top_k:
                    break
        return results


collaborative_recommender = CollaborativeRecommender()
