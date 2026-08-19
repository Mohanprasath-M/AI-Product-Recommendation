
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.redis_client import cache
from app.ml.model_registry import registry

router = APIRouter(tags=["Health & Monitoring"])


@router.get("/health")
def get_health():
    return {"status": "ok", "service": "AI Product Recommendation & Intelligence API"}


@router.get("/health/database")
def get_database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@router.get("/health/redis")
def get_redis_health():
    is_ok = cache.ping()
    return {
        "status": "healthy" if is_ok else "degraded",
        "driver": "redis" if cache.is_redis else "in-memory-fallback"
    }


@router.get("/health/ml")
def get_ml_health():
    cb_avail = registry.is_model_available("content_based_model")
    cf_avail = registry.is_model_available("collaborative_model")
    sent_avail = registry.is_model_available("sentiment_model")
    seg_avail = registry.is_model_available("customer_segmentation_model")

    return {
        "status": "healthy",
        "models": {
            "content_based": "loaded" if cb_avail else "ready_for_training",
            "collaborative": "loaded" if cf_avail else "ready_for_training",
            "sentiment_nlp": "loaded" if sent_avail else "ready_for_training",
            "segmentation_kmeans": "loaded" if seg_avail else "ready_for_training"
        }
    }
