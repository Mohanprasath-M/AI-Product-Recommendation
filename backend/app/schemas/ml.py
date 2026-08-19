from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class ModelVersionOut(BaseModel):
    id: str
    model_name: str
    version: str
    algorithm: str
    hyperparameters: Dict[str, Any] = {}
    metrics: Dict[str, Any] = {}
    is_active: bool
    dataset_size: int
    training_duration_seconds: float
    trained_by: str
    created_at: datetime

    class Config:
        from_attributes = True


class ModelTrainRequest(BaseModel):
    model_type: str = "ALL"  # ALL, RECOMMENDER, SENTIMENT, SEGMENTATION, BASKET
    force_retrain: bool = True
    parameters: Optional[Dict[str, Any]] = None


class ModelEvaluationOut(BaseModel):
    recommender_metrics: Dict[str, float]  # precision@10, recall@10, ndcg@10, hit_rate@10, map@10
    sentiment_metrics: Dict[str, float]    # accuracy, precision, recall, f1_score
    segmentation_metrics: Dict[str, float] # silhouette_score, davies_bouldin_score
    last_evaluated_at: datetime
    status: str
