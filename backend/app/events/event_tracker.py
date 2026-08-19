import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.interaction import Interaction, SearchEvent
from app.models.product import Product
from app.models.user import Customer
from app.core.redis_client import cache
from app.core.websocket_manager import manager

logger = logging.getLogger(__name__)

EVENT_WEIGHTS = {
    "VIEW_PRODUCT": 1.0,
    "CLICK_PRODUCT": 2.0,
    "SEARCH": 1.5,
    "ADD_TO_WISHLIST": 3.0,
    "REMOVE_FROM_WISHLIST": -1.0,
    "ADD_TO_CART": 4.0,
    "REMOVE_FROM_CART": -2.0,
    "CHECKOUT": 4.5,
    "PURCHASE": 5.0,
    "RATING": 3.5,
    "REVIEW": 4.0,
    "CATEGORY_VIEW": 1.0,
    "BRAND_VIEW": 1.0
}


class EventTracker:
    """Asynchronous real-time event tracker and live broadcaster."""

    async def track_event(
        self,
        db: Session,
        customer_id: str,
        event_type: str,
        product_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Interaction:
        weight = EVENT_WEIGHTS.get(event_type, 1.0)
        
        interaction = Interaction(
            customer_id=customer_id,
            product_id=product_id if product_id else "",
            event_type=event_type,
            weight=weight,
            session_id=session_id,
            metadata_json=metadata or {},
            timestamp=datetime.now(timezone.utc)
        )

        if product_id:
            db.add(interaction)
            
            # Increment real-time product metrics in DB
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                if event_type == "VIEW_PRODUCT":
                    product.views_count = (product.views_count or 0) + 1
                elif event_type == "CLICK_PRODUCT":
                    product.clicks_count = (product.clicks_count or 0) + 1
                elif event_type == "ADD_TO_CART":
                    product.cart_adds_count = (product.cart_adds_count or 0) + 1
                elif event_type == "ADD_TO_WISHLIST":
                    product.wishlist_adds_count = (product.wishlist_adds_count or 0) + 1

        # Update customer last active time
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            customer.last_active_at = datetime.now(timezone.utc)

        db.commit()

        # Invalidate recommendation cache for this customer
        cache.delete(f"rec:{customer_id}")

        # Broadcast live event to all connected dashboards (Admin / Analyst / WebSocket clients)
        prod_name = None
        if product_id and 'product' in locals() and product:
            prod_name = product.name

        live_msg = {
            "type": "LIVE_EVENT",
            "data": {
                "id": interaction.id,
                "customer_id": customer_id,
                "customer_name": customer.name if customer else "Customer",
                "product_id": product_id,
                "product_name": prod_name,
                "event_type": event_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "metadata": metadata or {}
            }
        }
        await manager.broadcast(live_msg)

        return interaction

    async def track_search(
        self,
        db: Session,
        query: str,
        customer_id: Optional[str] = None,
        result_count: int = 0,
        clicked_product_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> SearchEvent:
        search_ev = SearchEvent(
            customer_id=customer_id,
            query=query.strip(),
            result_count=result_count,
            clicked_product_id=clicked_product_id,
            session_id=session_id,
            timestamp=datetime.now(timezone.utc)
        )
        db.add(search_ev)
        db.commit()

        # Broadcast search event
        await manager.broadcast({
            "type": "SEARCH_EVENT",
            "data": {
                "query": query,
                "result_count": result_count,
                "customer_id": customer_id,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        })
        return search_ev


event_tracker = EventTracker()
