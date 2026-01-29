from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, asc, func
from typing import List, Optional, Tuple
from app import models, schemas

# Basic CRUD operations

def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def update_product(db: Session, product_id: int, data: schemas.ProductUpdate) -> Optional[models.Product]:
    db_prod = get_product(db, product_id)
    if not db_prod:
        return None
    for k, v in data.dict(exclude_unset=True).items():
        setattr(db_prod, k, v)
    db.commit()
    db.refresh(db_prod)
    return db_prod


def delete_product(db: Session, product_id: int) -> bool:
    db_prod = get_product(db, product_id)
    if not db_prod:
        return False
    db.delete(db_prod)
    db.commit()
    return True


def increment_view(db: Session, product_id: int) -> Optional[models.Product]:
    prod = get_product(db, product_id)
    if not prod:
        return None
    prod.views = (prod.views or 0) + 1
    db.commit()
    db.refresh(prod)
    return prod


def increment_click(db: Session, product_id: int) -> Optional[models.Product]:
    prod = get_product(db, product_id)
    if not prod:
        return None
    prod.clicks = (prod.clicks or 0) + 1
    db.commit()
    db.refresh(prod)
    return prod


def search_products(db: Session,
                    q: Optional[str] = None,
                    category: Optional[str] = None,
                    min_price: Optional[float] = None,
                    max_price: Optional[float] = None,
                    min_rating: Optional[float] = None,
                    sort_by: Optional[str] = None,
                    sort_order: str = "asc",
                    limit: int = 20,
                    offset: int = 0) -> Tuple[List[models.Product], int]:
    query = db.query(models.Product)

    if q:
        query = query.filter(models.Product.name.ilike(f"%{q}%"))
    if category:
        # Case-insensitive category match (use ILIKE for DB portability; strip whitespace)
        cat = category.strip()
        query = query.filter(models.Product.category.ilike(cat))
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    if min_rating is not None:
        query = query.filter(models.Product.rating >= min_rating)

    total = query.count()

    if sort_by == "price":
        query = query.order_by(asc(models.Product.price) if sort_order == "asc" else desc(models.Product.price))
    elif sort_by == "rating":
        query = query.order_by(asc(models.Product.rating) if sort_order == "asc" else desc(models.Product.rating))

    results = query.offset(offset).limit(limit).all()
    return results, total


def get_popular(db: Session, limit: int = 10):
    # Simple popularity metric: rating * log(views+1) + clicks
    # Keep it simple and deterministic for a college project
    products = db.query(models.Product).all()
    def score(p: models.Product):
        from math import log
        return (p.rating or 0) * (log((p.views or 0) + 1) + 1) + (p.clicks or 0)
    products.sort(key=score, reverse=True)
    return products[:limit]


def related_products(db: Session, product: models.Product, price_delta: float = 20.0, limit: int = 10):
    low = product.price - price_delta
    high = product.price + price_delta
    # Case-insensitive category matching for related products
    q = db.query(models.Product).filter(
        models.Product.category.ilike(product.category.strip()),
        models.Product.id != product.id,
        models.Product.price.between(low, high)
    )
    return q.limit(limit).all()
