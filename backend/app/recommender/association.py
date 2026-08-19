import logging
from typing import List, Dict, Tuple
from app.ml.model_registry import registry

logger = logging.getLogger(__name__)


class AssociationRecommender:
    """Market basket affinity / frequently bought together recommender."""

    def __init__(self):
        self._load_model()

    def _load_model(self):
        self.artifact = registry.load_artifact("basket_association_model")
        # artifact contains: {'rules': {antecedent_pid: [(consequent_pid, confidence, lift)]}}

    def reload(self):
        self._load_model()

    def get_frequently_bought_together(self, product_id: str, top_k: int = 4) -> List[Tuple[str, float]]:
        if not self.artifact:
            self._load_model()
        if not self.artifact:
            return []

        rules = self.artifact.get("rules", {})
        if product_id not in rules:
            return []

        candidates = rules[product_id]  # list of (consequent_pid, confidence, lift)
        results = []
        for c_pid, conf, lift in candidates:
            score = float(conf)
            results.append((c_pid, score))
            if len(results) >= top_k:
                break
        return results


association_recommender = AssociationRecommender()
