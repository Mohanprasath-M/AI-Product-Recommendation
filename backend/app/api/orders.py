import uuid
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.order import Order, OrderItem
from app.models.interaction import CartItem
from app.models.product import Product
from app.models.user import Customer
from app.schemas.order import CartItemAdd, CartItemOut, OrderCreate, OrderOut, OrderItemOut
from app.schemas.product import ProductOut
from app.events.event_tracker import event_tracker
from app.api.deps import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders & Cart"])


@router.get("/cart/{customer_id}", response_model=List[CartItemOut])
def get_cart_items(customer_id: str, db: Session = Depends(get_db)):
    items = db.query(CartItem).filter(CartItem.customer_id == customer_id).all()
    results = []
    for it in items:
        p_out = ProductOut.model_validate(it.product)
        results.append(CartItemOut(
            id=it.id,
            product_id=it.product_id,
            product=p_out,
            quantity=it.quantity,
            unit_price=it.unit_price,
            total_price=it.quantity * it.unit_price
        ))
    return results


@router.post("/cart/{customer_id}", response_model=CartItemOut)
async def add_to_cart(
    customer_id: str,
    item_in: CartItemAdd,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.customer_id == customer_id, CartItem.product_id == item_in.product_id)
        .first()
    )

    if cart_item:
        cart_item.quantity += item_in.quantity
    else:
        cart_item = CartItem(
            customer_id=customer_id,
            product_id=item_in.product_id,
            quantity=item_in.quantity,
            unit_price=product.price
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    # Track ADD_TO_CART event asynchronously
    await event_tracker.track_event(
        db=db,
        customer_id=customer_id,
        event_type="ADD_TO_CART",
        product_id=item_in.product_id,
        metadata={"quantity": item_in.quantity}
    )

    p_out = ProductOut.model_validate(cart_item.product)
    return CartItemOut(
        id=cart_item.id,
        product_id=cart_item.product_id,
        product=p_out,
        quantity=cart_item.quantity,
        unit_price=cart_item.unit_price,
        total_price=cart_item.quantity * cart_item.unit_price
    )


@router.delete("/cart/{customer_id}/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    customer_id: str,
    product_id: str,
    db: Session = Depends(get_db)
):
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.customer_id == customer_id, CartItem.product_id == product_id)
        .first()
    )
    if cart_item:
        db.delete(cart_item)
        db.commit()
        await event_tracker.track_event(
            db=db,
            customer_id=customer_id,
            event_type="REMOVE_FROM_CART",
            product_id=product_id
        )
    return None


@router.post("/checkout/{customer_id}", response_model=OrderOut)
async def checkout_order(
    customer_id: str,
    order_in: OrderCreate,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    if not order_in.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

    total_amount = 0.0
    order_items = []
    order_id = str(uuid.uuid4())

    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue
        item_total = product.price * item.quantity
        total_amount += item_total
        
        # Decrement stock & increment purchases count
        product.stock = max(0, product.stock - item.quantity)
        product.purchases_count = (product.purchases_count or 0) + item.quantity
        product.revenue_generated = (product.revenue_generated or 0.0) + item_total

        order_item = OrderItem(
            order_id=order_id,
            product_id=product.id,
            product_name=product.name,
            quantity=item.quantity,
            unit_price=product.price,
            total_price=item_total
        )
        order_items.append(order_item)

    order = Order(
        id=order_id,
        order_code=f"ORD-{order_id[:8].upper()}",
        customer_id=customer.id,
        total_amount=total_amount,
        discount_amount=0.0,
        tax_amount=round(total_amount * 0.08, 2),
        final_amount=round(total_amount * 1.08, 2),
        status="COMPLETED",
        payment_method=order_in.payment_method,
        shipping_address=order_in.shipping_address,
        created_at=datetime.now(timezone.utc)
    )
    db.add(order)
    for oi in order_items:
        db.add(oi)

    # Update customer spend and order count
    customer.total_spend += order.final_amount
    customer.total_orders += 1
    customer.avg_order_value = customer.total_spend / customer.total_orders
    customer.clv_historical = customer.total_spend

    # Clear customer cart
    db.query(CartItem).filter(CartItem.customer_id == customer_id).delete()
    db.commit()
    db.refresh(order)

    # Track PURCHASE events
    for item in order_in.items:
        await event_tracker.track_event(
            db=db,
            customer_id=customer_id,
            event_type="PURCHASE",
            product_id=item.product_id,
            metadata={"order_id": order.id, "amount": total_amount}
        )

    return OrderOut(
        id=order.id,
        order_code=order.order_code,
        customer_id=order.customer_id,
        total_amount=order.total_amount,
        discount_amount=order.discount_amount,
        tax_amount=order.tax_amount,
        final_amount=order.final_amount,
        status=order.status,
        payment_method=order.payment_method,
        created_at=order.created_at,
        items=[OrderItemOut.model_validate(oi) for oi in order.items]
    )


@router.get("/history/{customer_id}", response_model=List[OrderOut])
def get_order_history(customer_id: str, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.customer_id == customer_id).order_by(Order.created_at.desc()).all()
    results = []
    for o in orders:
        results.append(OrderOut(
            id=o.id,
            order_code=o.order_code,
            customer_id=o.customer_id,
            total_amount=o.total_amount,
            discount_amount=o.discount_amount,
            tax_amount=o.tax_amount,
            final_amount=o.final_amount,
            status=o.status,
            payment_method=o.payment_method,
            created_at=o.created_at,
            items=[OrderItemOut.model_validate(oi) for oi in o.items]
        ))
    return results
