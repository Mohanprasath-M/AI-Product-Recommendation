import logging
import numpy as np
from typing import List, Dict, Tuple, Optional
from app.ml.model_registry import registry

logger = logging.getLogger(__name__)


class ContentBasedRecommender:
    def __init__(self):
        self._load_model()

    def _load_model(self):
        self.artifact = registry.load_artifact("content_based_model")
        # artifact contains: {'vectorizer': tfidf, 'tfidf_matrix': matrix, 'product_ids': list, 'id_to_idx': dict, 'sim_matrix': cosine_sim}

    def reload(self):
        self._load_model()

    def get_similar_products(self, product_id: str, top_k: int = 10) -> List[Tuple[str, float]]:
        if not self.artifact:
            self._load_model()
        if not self.artifact:
            return []

        id_to_idx = self.artifact.get("id_to_idx", {})
        if product_id not in id_to_idx:
            return []

        idx = id_to_idx[product_id]
        sim_matrix = self.artifact.get("sim_matrix")
        product_ids = self.artifact.get("product_ids", [])

        if sim_matrix is not None:
            sim_scores = sim_matrix[idx]
        else:
            # Fallback: compute cosine sim on the fly
            tfidf_matrix = self.artifact.get("tfidf_matrix")
            if tfidf_matrix is None:
                return []
            from sklearn.metrics.pairwise import cosine_similarity
            sim_scores = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()

        # Sort indices by similarity descending
        similar_indices = np.argsort(sim_scores)[::-1]
        results = []
        for i in similar_indices:
            p_id = product_ids[i]
            if p_id != product_id:
                score = float(sim_scores[i])
                results.append((p_id, score))
                if len(results) >= top_k:
                    break
        return results

    def score_products_for_user_history(self, interacted_product_ids: List[str], candidate_ids: List[str]) -> Dict[str, float]:
        if not self.artifact:
            self._load_model()
        if not self.artifact or not interacted_product_ids:
            return {p_id: 0.0 for p_id in candidate_ids}

        id_to_idx = self.artifact.get("id_to_idx", {})
        sim_matrix = self.artifact.get("sim_matrix")
        tfidf_matrix = self.artifact.get("tfidf_matrix")
        product_ids = self.artifact.get("product_ids", [])

        valid_user_indices = [id_to_idx[pid] for pid in interacted_product_ids if pid in id_to_idx]
        if not valid_user_indices:
            return {p_id: 0.0 for p_id in candidate_ids}

        # Average similarity to user's history
        if sim_matrix is not None:
            user_sim_profile = np.mean([sim_matrix[i] for i in valid_user_indices], axis=0)
        else:
            from sklearn.metrics.pairwise import cosine_similarity
            user_vec = np.mean([tfidf_matrix[i].toarray() for i in valid_user_indices], axis=0)
            user_sim_profile = cosine_similarity(user_vec, tfidf_matrix).flatten()

        idx_to_score = {product_ids[i]: float(user_sim_profile[i]) for i in range(len(product_ids))}
        return {p_id: idx_to_score.get(p_id, 0.0) for p_id in candidate_ids}


content_recommender = ContentBasedRecommender()
