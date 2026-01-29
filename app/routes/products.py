from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas
from app.db import get_db
from app.cache import cache

router = APIRouter()

@router.post("/add", response_model=schemas.ProductOut)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Add a new product"""
    return crud.create_product(db, product)

@router.get("/search", response_model=List[schemas.ProductOut])
def search(q: Optional[str] = None,
           category: Optional[str] = None,
           min_price: Optional[float] = None,
           max_price: Optional[float] = None,
           min_rating: Optional[float] = None,
           sort_by: Optional[str] = Query(None, regex="^(price|rating)$"),
           sort_order: str = Query("asc", regex="^(asc|desc)$"),
           page: int = 1,
           size: int = 20,
           db: Session = Depends(get_db)):
    """Search products with filters, sort and pagination. Results are cached briefly."""
    cat_key = category.strip().lower() if category else ""
    key = f"search:{q}:{cat_key}:{min_price}:{max_price}:{min_rating}:{sort_by}:{sort_order}:{page}:{size}"
    cached = cache.get(key)
    if cached:
        # Convert cached ORM models to schemas
        return [schemas.ProductOut.model_validate(p) for p in cached]

    offset = (page - 1) * size
    # Pass stripped category to avoid whitespace/case issues
    results, total = crud.search_products(db, q=q, category=category.strip() if category else None, min_price=min_price, max_price=max_price, min_rating=min_rating, sort_by=sort_by, sort_order=sort_order, limit=size, offset=offset)
    cache.set(key, results, ttl=30)
    return results

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    prod = crud.get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    prod = crud.update_product(db, product_id, data)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    # Invalidate caches that may be affected
    cache.invalidate("popular")
    return prod

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    cache.invalidate("popular")
    return {"status": "deleted"}

@router.get("/{product_id}/view", response_model=schemas.ProductOut)
def view_product(product_id: int, db: Session = Depends(get_db)):
    prod = crud.increment_view(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    cache.invalidate("popular")
    return prod

@router.get("/{product_id}/click", response_model=schemas.ProductOut)
def click_product(product_id: int, db: Session = Depends(get_db)):
    prod = crud.increment_click(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    cache.invalidate("popular")
    return prod
