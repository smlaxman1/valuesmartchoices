# from pydantic import BaseModel
# from sqlalchemy import Column, Integer, String,Float
# from database.dbConnect import Base
# from typing import Optional

# class ProductResponse(BaseModel):
#     id: int
#     title: str
#     product_description: str
#     price: float
#     image: str
#
#
#     class Config:
#         from_attributes  = True
#
#
# class Product(Base):
#     __tablename__ = "product"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(250))
#     product_description=Column(String(250))
#     price=Column(Float)
#     image = Column(String(100), unique=True)
#
#

from pydantic import BaseModel, Field
from typing import List

class foodProcessingMachinaryResponse(BaseModel):
    id: str = Field(alias="_id")  # Use alias to map MongoDB _id
    machine_name: str
    machine_image_location: str

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class domainSpecificResponse(BaseModel):
    id: str = Field(alias="_id")  # Use alias to map MongoDB _id
    domain: str
    domain_machinary: List[str]

    class Config:
        validate_by_name = True
        from_attributes = True


class   FoodProcessingMachinary_domainSpecificResponse(BaseModel):
    foodProcessingMachinary: List[foodProcessingMachinaryResponse]
    domainSpecific: List[domainSpecificResponse]


def convert_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc
