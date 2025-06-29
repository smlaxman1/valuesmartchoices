from pydantic import BaseModel
from sqlalchemy import Column, Integer, String,Float
from database.dbConnect import Base
from typing import Optional

class ProductResponse(BaseModel):
    id: int
    title: str
    product_description: str
    price: float
    image: str


    class Config:
        from_attributes  = True


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250))
    product_description=Column(String(250))
    price=Column(Float)
    image = Column(String(100), unique=True)