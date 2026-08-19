from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.redis_client import cache
from app.models.ml_metadata import RecommendationEvent
from app.schemas.recommendation import RecommendationResponse, RecommendationItem, RecommendationFeedback, ABWeightConfig
from app.schemas.product import ProductOut
from app.recommender.hybrid import recommender_engine
from app.api.deps import get_current_user, get_current_active_admin

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/{customer_id}", response_model=RecommendationResponse)
def get_personalized_recommendations(
    customer_id: str,
    limit: int = Query(10, ge=1, le=50),
    category: Optional[str] = None,
    exclude_purchased: bool = Query(True),
    db: Session = Depends(get_db)
):
    cache_key = f"rec:{customer_id}:{category or 'all'}:{limit}"
    cached_data = cache.get_json(cache_key)
    if cached_data and isinstance(cached_data, dict):
        return RecommendationResponse(**cached_data)

    raw_results = recommender_engine.recommend(
        db=db,
        customer_id=customer_id,
        limit=limit,
        exclude_purchased=exclude_purchased,
        category=category
    )

    items = []
    for r in raw_results:
        p_out = ProductOut.model_validate(r["product"])
        items.append(RecommendationItem(
            product=p_out,
            score=r["score"],
            rank=r["rank"],
            reason=r["reason"],
            recommendation_type=r["recommendation_type"],
            signals=r["signals"]
        ))

    resp = RecommendationResponse(
        customer_id=customer_id,
        recommendations=items,
        count=len(items),
        model_version="v1.0",
        algorithm="Hybrid-TFIDF-SVD-Behavioral",
        experiment_group="A"
    )

    # Cache for 2 minutes
    cache.set_json(cache_key, resp.model_dump(), ex=120)
    return resp


@router.get("/product/{product_id}/similar", response_model=List[RecommendationItem])
def get_similar_products(
    product_id: str,
    limit: int = Query(6, ge=1, le=20),
    db: Session = Depends(get_db)
):
    raw_results = recommender_engine.get_similar_products(db, product_id=product_id, limit=limit)
    items = []
    for r in raw_results:
        p_out = ProductOut.model_validate(r["product"])
        items.append(RecommendationItem(
            product=p_out,
            score=r["score"],
            rank=r["rank"],
            reason=r["reason"],
            recommendation_type=r["recommendation_type"],
            signals=r["signals"]
        ))
    return items


@router.get("/product/{product_id}/bought-together", response_model=List[RecommendationItem])
def get_frequently_bought_together(
    product_id: str,
    limit: int = Query(4, ge=1, le=10),
    db: Session = Depends(get_db)
):
    raw_results = recommender_engine.get_frequently_bought_together(db, product_id=product_id, limit=limit)
    items = []
    for r in raw_results:
        p_out = ProductOut.model_validate(r["product"])
        items.append(RecommendationItem(
            product=p_out,
            score=r["score"],
            rank=r["rank"],
            reason=r["reason"],
            recommendation_type=r["recommendation_type"],
            signals=r["signals"]
        ))
    return items


@router.post("/feedback")
def track_recommendation_feedback(
    feedback: RecommendationFeedback,
    db: Session = Depends(get_db)
):
    event = RecommendationEvent(
        customer_id=feedback.customer_id,
        product_id=feedback.product_id,
        recommendation_type=feedback.recommendation_type,
        rank=feedback.rank,
        clicked=(feedback.action in ["CLICK", "ADD_TO_CART", "PURCHASE"]),
        added_to_cart=(feedback.action in ["ADD_TO_CART", "PURCHASE"]),
        purchased=(feedback.action == "PURCHASE")
    )
    db.add(event)
    db.commit()
    return {"status": "success", "event_id": event.id}


@router.get("/config/weights", response_model=ABWeightConfig)
def get_recommender_weights():
    weights = recommender_engine.get_active_weights()
    return ABWeightConfig(
        weight_content=weights.get("weight_content", 0.35),
        weight_collaborative=weights.get("weight_collaborative", 0.30),
        weight_behavior=weights.get("weight_behavior", 0.15),
        weight_popularity=weights.get("weight_popularity", 0.08),
        weight_rating=weights.get("weight_rating", 0.05),
        weight_personalization=weights.get("weight_personalization", 0.07),
        active_group="A"
    )


@router.post("/config/weights", response_model=ABWeightConfig)
def update_recommender_weights(
    config: ABWeightConfig,
    admin: Any = Depends(get_current_active_admin)
):
    weights_dict = {
        "weight_content": config.weight_content,
        "weight_collaborative": config.weight_collaborative,
        "weight_behavior": config.weight_behavior,
        "weight_popularity": config.weight_popularity,
        "weight_rating": config.weight_rating,
        "weight_personalization": config.weight_personalization
    }
    cache.set_json("ab_test_weights", weights_dict, ex=86400 * 30)
    return config
