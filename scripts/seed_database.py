import os
import sys
import csv
import pandas as pd
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.core.config import settings
from app.core.database import engine, SessionLocal, Base
from app.core.security import get_password_hash
from app.models.user import User, Customer
from app.models.product import Category, Brand, Product
from app.models.interaction import Interaction, SearchEvent
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.models.segmentation import CustomerSegment
from app.models.ml_metadata import RecommendationEvent, AuditLog

DATA_DIR = settings.DATA_DIR


def seed():
    print("==================================================")
    print("STARTING DATABASE SEEDING PROCESS")
    print("==================================================")

    # Initialize tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Create Default Users for Instant Testing
        print("-> Seeding Default Admin, Analyst, and Customer Users...")
        default_users = [
            {"email": "admin@platform.ai", "name": "Platform Administrator", "role": "ADMIN", "pass": "Admin@123456"},
            {"email": "analyst@platform.ai", "name": "Data & ML Analyst", "role": "ANALYST", "pass": "Analyst@123456"},
            {"email": "customer@platform.ai", "name": "Alex Mercer (VIP Shopper)", "role": "CUSTOMER", "pass": "Customer@123456"},
        ]

        created_users = {}
        for u in default_users:
            user = db.query(User).filter(User.email == u["email"]).first()
            if not user:
                user = User(
                    email=u["email"],
                    hashed_password=get_password_hash(u["pass"]),
                    full_name=u["name"],
                    role=u["role"],
                    is_active=True
                )
                db.add(user)
                db.flush()
            created_users[u["role"]] = user

        # 2. Seed Categories
        print("-> Seeding Categories...")
        cat_file = os.path.join(DATA_DIR, "categories.csv")
        cat_map = {}
        if os.path.exists(cat_file):
            df_cat = pd.read_csv(cat_file)
            for _, row in df_cat.iterrows():
                cat = db.query(Category).filter(Category.name == row["name"]).first()
                if not cat:
                    cat = Category(
                        name=row["name"],
                        slug=row["slug"],
                        icon=row["icon"],
                        description=row["description"]
                    )
                    db.add(cat)
                    db.flush()
                cat_map[cat.name] = cat.id

        # 3. Seed Products
        print("-> Seeding Products...")
        prod_file = os.path.join(DATA_DIR, "products.csv")
        if os.path.exists(prod_file):
            df_prods = pd.read_csv(prod_file)
            for _, row in df_prods.iterrows():
                prod = db.query(Product).filter(Product.id == str(row["id"])).first()
                if not prod:
                    prod = Product(
                        id=str(row["id"]),
                        product_code=str(row["product_code"]),
                        name=str(row["name"]),
                        description=str(row["description"]),
                        category=str(row["category"]),
                        category_id=cat_map.get(str(row["category"])),
                        brand=str(row["brand"]),
                        price=float(row["price"]),
                        discount=float(row.get("discount", 0.0)),
                        stock=int(row.get("stock", 100)),
                        rating=float(row.get("rating", 4.5)),
                        rating_count=int(row.get("rating_count", 25)),
                        image_url=str(row.get("image_url", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80")),
                        tags=str(row.get("tags", "")),
                        views_count=int(row.get("views_count", 200)),
                        purchases_count=int(row.get("purchases_count", 20)),
                        revenue_generated=float(row.get("revenue_generated", 1500.0)),
                        trend_score=float(row.get("trend_score", 15.0)),
                        trend_status=str(row.get("trend_status", "STABLE")),
                        status="ACTIVE"
                    )
                    db.add(prod)
            db.commit()

        # 4. Seed Customers
        print("-> Seeding Customers...")
        cust_file = os.path.join(DATA_DIR, "customers.csv")
        if os.path.exists(cust_file):
            df_cust = pd.read_csv(cust_file)
            for idx, row in df_cust.iterrows():
                cust = db.query(Customer).filter(Customer.id == str(row["id"])).first()
                if not cust:
                    # Link first customer to default customer user account
                    linked_uid = created_users["CUSTOMER"].id if idx == 0 else None
                    cust = Customer(
                        id=str(row["id"]),
                        user_id=linked_uid,
                        customer_code=str(row["customer_code"]),
                        name=str(row["name"]),
                        email=str(row["email"]),
                        age=int(row.get("age", 30)),
                        gender=str(row.get("gender", "Other")),
                        location=str(row.get("location", "New York, NY")),
                        persona=str(row.get("persona", "General Shopper")),
                        total_spend=float(row.get("total_spend", 500.0)),
                        total_orders=int(row.get("total_orders", 5)),
                        avg_order_value=float(row.get("avg_order_value", 100.0)),
                        clv_historical=float(row.get("clv_historical", 500.0)),
                        clv_estimated=float(row.get("clv_estimated", 1200.0)),
                        churn_risk_score=float(row.get("churn_risk_score", 0.25)),
                        churn_risk_level=str(row.get("churn_risk_level", "LOW")),
                        favorite_category=str(row.get("favorite_category", "Electronics")),
                        favorite_brand=str(row.get("favorite_brand", "Sony")),
                        preferred_price_min=float(row.get("preferred_price_min", 20.0)),
                        preferred_price_max=float(row.get("preferred_price_max", 500.0))
                    )
                    db.add(cust)
            db.commit()

        # 5. Seed Interactions Sample
        print("-> Seeding Interactions...")
        inter_file = os.path.join(DATA_DIR, "interactions.csv")
        if os.path.exists(inter_file):
            df_inter = pd.read_csv(inter_file)
            # Insert top 5000 directly for quick startup
            interactions_to_insert = []
            for _, row in df_inter.head(6000).iterrows():
                interactions_to_insert.append(Interaction(
                    id=str(row["id"]),
                    customer_id=str(row["customer_id"]),
                    product_id=str(row["product_id"]),
                    event_type=str(row["event_type"]),
                    weight=float(row["weight"]),
                    session_id=str(row.get("session_id", "sess_1")),
                    metadata_json={}
                ))
            db.bulk_save_objects(interactions_to_insert)
            db.commit()

        # 6. Seed Orders Sample
        print("-> Seeding Orders...")
        purch_file = os.path.join(DATA_DIR, "purchases.csv")
        if os.path.exists(purch_file):
            df_purch = pd.read_csv(purch_file)
            grouped = df_purch.groupby("order_id")
            count = 0
            for order_id, group in grouped:
                if count > 1500:
                    break
                first_row = group.iloc[0]
                order = Order(
                    id=str(order_id),
                    order_code=f"ORD-{str(order_id)[:8].upper()}",
                    customer_id=str(first_row["customer_id"]),
                    total_amount=float(first_row["total_amount"]),
                    discount_amount=0.0,
                    tax_amount=round(float(first_row["total_amount"]) * 0.08, 2),
                    final_amount=round(float(first_row["total_amount"]) * 1.08, 2),
                    status="COMPLETED",
                    payment_method="CREDIT_CARD"
                )
                db.add(order)
                for _, r in group.iterrows():
                    oi = OrderItem(
                        order_id=str(order_id),
                        product_id=str(r["product_id"]),
                        product_name=str(r["product_name"]),
                        quantity=int(r["quantity"]),
                        unit_price=float(r["unit_price"]),
                        total_price=float(r["unit_price"]) * int(r["quantity"])
                    )
                    db.add(oi)
                count += 1
            db.commit()

        # 7. Seed Reviews Sample
        print("-> Seeding Reviews...")
        rev_file = os.path.join(DATA_DIR, "reviews.csv")
        if os.path.exists(rev_file):
            df_rev = pd.read_csv(rev_file)
            reviews_to_insert = []
            for _, row in df_rev.head(2000).iterrows():
                pos_t = str(row.get("positive_topics", "")).split(",") if pd.notna(row.get("positive_topics")) else []
                neg_t = str(row.get("negative_topics", "")).split(",") if pd.notna(row.get("negative_topics")) else []
                reviews_to_insert.append(Review(
                    id=str(row["id"]),
                    customer_id=str(row["customer_id"]),
                    product_id=str(row["product_id"]),
                    rating=float(row["rating"]),
                    title=str(row["title"]),
                    comment=str(row["comment"]),
                    sentiment_label=str(row["sentiment_label"]),
                    sentiment_score=float(row["sentiment_score"]),
                    positive_topics=pos_t,
                    negative_topics=neg_t,
                    verified_purchase=1
                ))
            db.bulk_save_objects(reviews_to_insert)
            db.commit()

        print("==================================================")
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("==================================================")

    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
