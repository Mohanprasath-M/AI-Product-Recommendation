from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.review import Review
from app.models.product import Product
from app.models.user import Customer
from app.schemas.review import ReviewCreate, ReviewOut, SentimentSummary
from app.analytics.sentiment_analyzer import sentiment_analyzer
from app.analytics.product_intelligence import product_intelligence
from app.events.event_tracker import event_tracker

router = APIRouter(prefix="/reviews", tags=["Reviews & NLP Sentiment"])


@router.get("/product/{product_id}", response_model=List[ReviewOut])
def get_product_reviews(
    product_id: str,
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100)
):
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(desc(Review.created_at))
        .limit(limit)
        .all()
    )
    cids = [r.customer_id for r in reviews]
    customers = {c.id: c.name for c in db.query(Customer).filter(Customer.id.in_(cids)).all()}

    results = []
    for r in reviews:
        results.append(ReviewOut(
            id=r.id,
            customer_id=r.customer_id,
            customer_name=customers.get(r.customer_id, "Verified Shopper"),
            product_id=r.product_id,
            rating=r.rating,
            title=r.title,
            comment=r.comment,
            sentiment_label=r.sentiment_label,
            sentiment_score=r.sentiment_score,
            positive_topics=r.positive_topics or [],
            negative_topics=r.negative_topics or [],
            verified_purchase=r.verified_purchase,
            helpful_votes=r.helpful_votes,
            created_at=r.created_at
        ))
    return results


@router.get("/product/{product_id}/summary", response_model=SentimentSummary)
def get_product_sentiment_summary(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    metrics = product_intelligence.compute_product_metrics(db, product)
    
    pos_topics = [{"topic": t, "count": 5} for t in metrics["top_positive_topics"]]
    neg_topics = [{"topic": t, "count": 2} for t in metrics["top_negative_topics"]]

    return SentimentSummary(
        product_id=product_id,
        average_rating=metrics["average_rating"],
        total_reviews=metrics["total_reviews"],
        positive_pct=metrics["positive_sentiment_pct"],
        neutral_pct=metrics["neutral_sentiment_pct"],
        negative_pct=metrics["negative_sentiment_pct"],
        top_positive_topics=pos_topics,
        top_negative_topics=neg_topics
    )


@router.post("", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == review_in.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Local NLP sentiment analysis
    nlp_result = sentiment_analyzer.analyze_text(review_in.comment)

    # Use existing customer or default customer
    cid = review_in.customer_id
    if not cid:
        cust = db.query(Customer).first()
        cid = cust.id if cust else "anonymous"

    review = Review(
        customer_id=cid,
        product_id=review_in.product_id,
        rating=review_in.rating,
        title=review_in.title or "Customer Review",
        comment=review_in.comment,
        sentiment_label=nlp_result["sentiment_label"],
        sentiment_score=nlp_result["sentiment_score"],
        positive_topics=nlp_result["positive_topics"],
        negative_topics=nlp_result["negative_topics"],
        verified_purchase=1
    )
    db.add(review)

    # Recalculate product rating
    reviews = db.query(Review).filter(Review.product_id == product.id).all()
    ratings_list = [r.rating for r in reviews] + [review_in.rating]
    product.rating_count = len(ratings_list)
    product.rating = round(sum(ratings_list) / len(ratings_list), 2)
    product.sentiment_score = nlp_result["sentiment_score"]

    db.commit()
    db.refresh(review)

    # Track REVIEW event
    await event_tracker.track_event(
        db=db,
        customer_id=cid,
        event_type="REVIEW",
        product_id=product.id,
        metadata={"rating": review_in.rating, "sentiment": nlp_result["sentiment_label"]}
    )

    customer = db.query(Customer).filter(Customer.id == cid).first()
    return ReviewOut(
        id=review.id,
        customer_id=review.customer_id,
        customer_name=customer.name if customer else "Customer",
        product_id=review.product_id,
        rating=review.rating,
        title=review.title,
        comment=review.comment,
        sentiment_label=review.sentiment_label,
        sentiment_score=review.sentiment_score,
        positive_topics=review.positive_topics,
        negative_topics=review.negative_topics,
        verified_purchase=review.verified_purchase,
        helpful_votes=review.helpful_votes,
        created_at=review.created_at
    )
