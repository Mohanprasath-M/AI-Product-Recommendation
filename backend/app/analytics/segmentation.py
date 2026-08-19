import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from app.ml.model_registry import registry


class CustomerSegmentationEngine:
    """K-Means Customer Segmentation with automated persona labeling."""

    def __init__(self):
        self._load_model()

    def _load_model(self):
        self.artifact = registry.load_artifact("customer_segmentation_model")
        # artifact contains: {'kmeans': model, 'scaler': scaler, 'cluster_labels': dict, 'feature_names': list}

    def reload(self):
        self._load_model()

    def predict_segment(self, feature_vector: List[float]) -> Tuple[int, str]:
        if not self.artifact:
            self._load_model()
        if not self.artifact:
            return (0, "General Shoppers")

        scaler = self.artifact.get("scaler")
        kmeans = self.artifact.get("kmeans")
        cluster_labels = self.artifact.get("cluster_labels", {})

        if not scaler or not kmeans:
            return (0, "General Shoppers")

        scaled = scaler.transform([feature_vector])
        cluster_idx = int(kmeans.predict(scaled)[0])
        label = cluster_labels.get(cluster_idx, f"Segment {cluster_idx + 1}")
        return (cluster_idx, label)

    def generate_persona_label(self, centroid: np.ndarray, feature_names: List[str]) -> Tuple[str, List[str]]:
        """
        Creates human-readable segment names and bullet characteristics from cluster centroid.
        features: [total_spend, total_orders, avg_order_value, recency_days, total_interactions]
        """
        feat_dict = dict(zip(feature_names, centroid))
        spend = feat_dict.get("total_spend", 0.0)
        orders = feat_dict.get("total_orders", 0.0)
        aov = feat_dict.get("avg_order_value", 0.0)
        recency = feat_dict.get("recency_days", 0.0)
        interactions = feat_dict.get("total_interactions", 0.0)

        traits = []
        if spend > 1500 or aov > 150:
            name = "High-Value VIPs"
            traits = ["Top 10% revenue contributors", "High average order value", "Prefers premium brands"]
        elif orders > 8 and recency < 20:
            name = "Loyal Frequent Buyers"
            traits = ["Consistently high purchase cadence", "Low churn risk", "High category diversity"]
        elif recency > 60 and spend > 400:
            name = "Lapsing / At-Risk High Spenders"
            traits = ["High historical value", "Prolonged inactivity", "Needs win-back incentives"]
        elif aov < 40 and orders > 3:
            name = "Budget & Discount Seekers"
            traits = ["Price sensitive", "High response to promotions", "Frequent small basket purchases"]
        else:
            name = "Casual & New Explorers"
            traits = ["Moderate browsing activity", "Low to medium order history", "High exploration rate"]

        return name, traits


segmentation_engine = CustomerSegmentationEngine()
