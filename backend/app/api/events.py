from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.interaction import Interaction
from app.schemas.event import TrackEventRequest, SearchEventRequest, LiveActivityItem
from app.events.event_tracker import event_tracker
from app.models.user import Customer
from app.models.product import Product

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/track", status_code=status.HTTP_201_CREATED)
async def track_user_event(
    event_in: TrackEventRequest,
    db: Session = Depends(get_db)
):
    interaction = await event_tracker.track_event(
        db=db,
        customer_id=event_in.customer_id,
        event_type=event_in.event_type,
        product_id=event_in.product_id,
        session_id=event_in.session_id,
        metadata=event_in.metadata_json
    )
    return {"status": "recorded", "event_id": interaction.id}


@router.post("/search", status_code=status.HTTP_201_CREATED)
async def track_search_event(
    search_in: SearchEventRequest,
    db: Session = Depends(get_db)
):
    search_ev = await event_tracker.track_search(
        db=db,
        query=search_in.query,
        customer_id=search_in.customer_id,
        result_count=search_in.result_count,
        clicked_product_id=search_in.clicked_product_id,
        session_id=search_in.session_id
    )
    return {"status": "recorded", "search_id": search_ev.id}


@router.get("/live", response_model=List[LiveActivityItem])
def get_recent_live_events(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    events = (
        db.query(Interaction)
        .order_by(desc(Interaction.timestamp))
        .limit(limit)
        .all()
    )
    
    cids = list(set([e.customer_id for e in events if e.customer_id]))
    pids = list(set([e.product_id for e in events if e.product_id]))
    
    customers = {c.id: c.name for c in db.query(Customer).filter(Customer.id.in_(cids)).all()}
    products = {p.id: p.name for p in db.query(Product).filter(Product.id.in_(pids)).all()}

    results = []
    for e in events:
        results.append(LiveActivityItem(
            id=e.id,
            customer_id=e.customer_id,
            customer_name=customers.get(e.customer_id, "Customer"),
            product_id=e.product_id,
            product_name=products.get(e.product_id),
            event_type=e.event_type,
            timestamp=e.timestamp,
            metadata_json=e.metadata_json or {}
        ))
    return results
