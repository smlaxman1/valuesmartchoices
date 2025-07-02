from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel


# Replace with your actual DB credentials
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://<username>:<password>@localhost:3306/valuesmart_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    print("db connection is :", db)
    try:
        yield db
    finally:
        db.close()