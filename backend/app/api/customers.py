from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from app.core.database import get_db
from app.models.user import Customer
from app.models.segmentation import CustomerSegment
from app.models.interaction import Interaction
from app.models.order import Order
from app.models.product import Product
from app.schemas.customer import CustomerOut, CustomerInsightOut, PaginatedCustomers, CustomerSegmentOut
from app.analytics.customer_intelligence import customer_intelligence
from app.api.deps import get_current_user, get_current_active_analyst_or_admin

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=PaginatedCustomers)
def list_customers(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=100),
    search: Optional[str] = None,
    segment_id: Optional[str] = None,
    churn_risk_level: Optional[str] = None,
    sort_by: Optional[str] = "spend_desc"  # spend_desc, orders_desc, clv_desc, risk_desc, newest
):
    query = db.query(Customer)

    if search:
        pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Customer.name.ilike(pattern),
                Customer.email.ilike(pattern),
                Customer.customer_code.ilike(pattern),
                Customer.location.ilike(pattern)
            )
        )

    if segment_id:
        query = query.filter(Customer.segment_id == segment_id)
    if churn_risk_level:
        query = query.filter(Customer.churn_risk_level == churn_risk_level)

    if sort_by == "orders_desc":
        query = query.order_by(desc(Customer.total_orders))
    elif sort_by == "clv_desc":
        query = query.order_by(desc(Customer.clv_estimated))
    elif sort_by == "risk_desc":
        query = query.order_by(desc(Customer.churn_risk_score))
    elif sort_by == "newest":
        query = query.order_by(desc(Customer.created_at))
    else:
        query = query.order_by(desc(Customer.total_spend))

    total = query.count()
    pages = (total + size - 1) // size
    items = query.offset((page - 1) * size).limit(size).all()

    cust_outs = []
    for c in items:
        c_out = CustomerOut.model_validate(c)
        if c.segment:
            c_out.segment_name = c.segment.name
        cust_outs.append(c_out)

    return PaginatedCustomers(
        items=cust_outs,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/segments", response_model=List[CustomerSegmentOut])
def get_customer_segments(db: Session = Depends(get_db)):
    segments = db.query(CustomerSegment).order_by(CustomerSegment.cluster_index.asc()).all()
    return [CustomerSegmentOut.model_validate(s) for s in segments]


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    c_out = CustomerOut.model_validate(customer)
    if customer.segment:
        c_out.segment_name = customer.segment.name
    return c_out


@router.get("/{customer_id}/insights", response_model=CustomerInsightOut)
def get_customer_insights(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Recent interactions
    interactions = (
        db.query(Interaction)
        .filter(Interaction.customer_id == customer.id)
        .order_by(Interaction.timestamp.desc())
        .limit(10)
        .all()
    )
    pids = [i.product_id for i in interactions if i.product_id]
    prods = {p.id: p for p in db.query(Product).filter(Product.id.in_(pids)).all()}

    recent_list = []
    for i in interactions:
        p = prods.get(i.product_id)
        recent_list.append({
            "id": i.id,
            "event_type": i.event_type,
            "product_id": i.product_id,
            "product_name": p.name if p else "Product",
            "category": p.category if p else "General",
            "timestamp": i.timestamp.isoformat()
        })

    # Journey Funnel
    funnel = customer_intelligence.get_customer_journey_funnel(db, customer.id)

    # CLV breakdown
    clv_breakdown = customer_intelligence.compute_clv(customer.total_spend, customer.total_orders)

    # Churn factors & recommended actions
    risk_info = customer_intelligence.compute_churn_risk(
        days_since_last_active=15.0,
        days_since_last_purchase=30.0,
        total_orders=customer.total_orders
    )
    recommended_actions = customer_intelligence.get_recommended_actions(customer)

    c_out = CustomerOut.model_validate(customer)
    if customer.segment:
        c_out.segment_name = customer.segment.name

    return CustomerInsightOut(
        customer=c_out,
        recent_interactions=recent_list,
        top_categories=[{"category": customer.favorite_category or "Electronics", "count": 12}],
        top_brands=[{"brand": customer.favorite_brand or "Top Brand", "count": 8}],
        journey_funnel=funnel,
        recommended_actions=recommended_actions,
        clv_breakdown=clv_breakdown,
        churn_factors=risk_info["factors"]
    )
