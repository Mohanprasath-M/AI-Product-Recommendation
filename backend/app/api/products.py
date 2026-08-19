import io
import csv
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.core.database import get_db
from app.models.product import Product, Category, Brand
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut, PaginatedProducts, ProductStockUpdate, CategoryOut, BrandOut
from app.api.deps import get_current_user, get_current_active_admin

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=PaginatedProducts)
def list_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(12, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    status: Optional[str] = "ACTIVE",
    sort_by: Optional[str] = "popularity"  # popularity, price_asc, price_desc, rating, trending, newest
):
    query = db.query(Product)

    if status and status != "ALL":
        query = query.filter(Product.status == status)

    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern),
                Product.category.ilike(search_pattern),
                Product.brand.ilike(search_pattern),
                Product.tags.ilike(search_pattern)
            )
        )

    if category:
        query = query.filter(Product.category == category)
    if brand:
        query = query.filter(Product.brand == brand)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if min_rating is not None:
        query = query.filter(Product.rating >= min_rating)

    # Sorting logic
    if sort_by == "price_asc":
        query = query.order_by(asc(Product.price))
    elif sort_by == "price_desc":
        query = query.order_by(desc(Product.price))
    elif sort_by == "rating":
        query = query.order_by(desc(Product.rating), desc(Product.rating_count))
    elif sort_by == "trending":
        query = query.order_by(desc(Product.trend_score), desc(Product.views_count))
    elif sort_by == "newest":
        query = query.order_by(desc(Product.created_at))
    else:  # popularity default
        query = query.order_by(desc(Product.popularity_score), desc(Product.purchases_count), desc(Product.views_count))

    total = query.count()
    pages = (total + size - 1) // size
    items = query.offset((page - 1) * size).limit(size).all()

    return PaginatedProducts(
        items=[ProductOut.model_validate(p) for p in items],
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/categories", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    out = []
    for c in categories:
        cnt = db.query(Product).filter(Product.category == c.name).count()
        cat_data = CategoryOut.model_validate(c)
        cat_data.product_count = cnt
        out.append(cat_data)
    return out


@router.get("/brands", response_model=List[BrandOut])
def get_brands(db: Session = Depends(get_db)):
    brands = db.query(Brand).all()
    out = []
    for b in brands:
        cnt = db.query(Product).filter(Product.brand == b.name).count()
        b_data = BrandOut.model_validate(b)
        b_data.product_count = cnt
        out.append(b_data)
    return out


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductOut.model_validate(product)


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    admin: UserOut = Depends(get_current_active_admin)
):
    code = product_in.product_code or f"PROD-{int(db.query(Product).count()) + 1:04d}"
    product = Product(
        product_code=code,
        name=product_in.name,
        description=product_in.description,
        category=product_in.category,
        subcategory=product_in.subcategory,
        brand=product_in.brand,
        price=product_in.price,
        discount=product_in.discount,
        stock=product_in.stock,
        image_url=product_in.image_url,
        tags=product_in.tags or "",
        specifications=product_in.specifications or {},
        status=product_in.status or "ACTIVE"
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return ProductOut.model_validate(product)


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: str,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    admin: UserOut = Depends(get_current_active_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return ProductOut.model_validate(product)


@router.patch("/{product_id}/stock", response_model=ProductOut)
def update_product_stock(
    product_id: str,
    stock_in: ProductStockUpdate,
    db: Session = Depends(get_db),
    admin: UserOut = Depends(get_current_active_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product.stock = stock_in.stock
    if product.stock == 0:
        product.status = "OUT_OF_STOCK"
    elif product.status == "OUT_OF_STOCK" and product.stock > 0:
        product.status = "ACTIVE"

    db.commit()
    db.refresh(product)
    return ProductOut.model_validate(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    admin: UserOut = Depends(get_current_active_admin)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product)
    db.commit()
    return None


@router.get("/export/csv")
def export_products_csv(
    db: Session = Depends(get_db),
    admin: UserOut = Depends(get_current_active_admin)
):
    products = db.query(Product).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["product_id", "product_code", "name", "category", "brand", "price", "stock", "rating", "views", "purchases", "revenue"])
    for p in products:
        writer.writerow([p.id, p.product_code, p.name, p.category, p.brand, p.price, p.stock, p.rating, p.views_count, p.purchases_count, p.revenue_generated])
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=products_export.csv"}
    )
