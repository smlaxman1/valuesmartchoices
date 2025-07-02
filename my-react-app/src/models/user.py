from pydantic import BaseModel
from sqlalchemy import Column, Integer, String,Boolean
from database.dbConnect import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)



class UserResponse(BaseModel):
    id: int
    email: str
    hashed_password: str
    is_verified: bool


    class Config:
        from_attributes  = True