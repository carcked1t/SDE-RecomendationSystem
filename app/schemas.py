from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    rating: Optional[float] = 0.0
    stock: Optional[int] = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    stock: Optional[int] = None

class ProductOut(ProductBase):
    id: int
    views: int
    clicks: int

    model_config = ConfigDict(from_attributes=True)
