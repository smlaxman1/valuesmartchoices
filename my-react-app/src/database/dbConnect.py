from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from pymongo import MongoClient

from models.product import domainSpecificResponse

# Replace with your actual DB credentials
SQLALCHEMY_DATABASE_URL = "mysql+pymysql:/<user>:<pwd>@localhost:3306/<db>"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

client = MongoClient("mongodb://localhost:27017")
db = client["valuesmart_db"]
collectionFoodProcessingMachinary = db["food_processing_machinary"]
collectionFoodDomainMachinary=db["food_Domain_categories"]


def get_db():
    db = SessionLocal()
    print("db connection is :", db)
    try:
        yield db
    finally:
        db.close()

