from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    stock = Column(Integer, default=0)

    # interaction counters
    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
