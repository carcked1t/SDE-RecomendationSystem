from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.db import get_db
from app.crud import get_product, related_products, get_popular
from app.cache import cache

router = APIRouter()

@router.get("/recommend/{product_id}")
def recommend(product_id: int, db: Session = Depends(get_db)):
    prod = get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    # Related products (same category, similar price)
    related = related_products(db, prod)
    related_list = [schemas.ProductOut.model_validate(p) for p in related]

    # Popular products (cached)
    cached_pop = cache.get("popular")
    if cached_pop is None:
        cached_pop = get_popular(db, limit=10)
        cache.set("popular", cached_pop, ttl=60)
    
    popular_list = [schemas.ProductOut.model_validate(p) for p in cached_pop]

    return {"related": related_list, "popular": popular_list}

@router.get("/popular", response_model=List[schemas.ProductOut])
def popular(db: Session = Depends(get_db)):
    cached = cache.get("popular")
    if cached:
        return cached
    top = get_popular(db, limit=10)
    cache.set("popular", top, ttl=60)
    return top
