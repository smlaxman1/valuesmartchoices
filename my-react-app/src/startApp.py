
from fastapi import FastAPI, Request,Depends
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth2Session
from sqlalchemy.orm import Session
from typing import List

from models.product import Product, ProductResponse
from database.dbConnect import get_db

app = FastAPI()



CLIENT_ID = "XXXXX"
CLIENT_SECRET = "XXXXXX"
REDIRECT_URI = "XXXXXX"

AUTHORIZATION_BASE_URL = "XXXXX"
TOKEN_URL = "XXXXX"
SCOPE = ["XXXXX", "XXXX"]



@app.get("/login")
def login():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    auth_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, access_type="offline")
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
def callback(request: Request):
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    google.fetch_token(
        TOKEN_URL,
        client_secret=CLIENT_SECRET,
        authorization_response=str(request.url)
    )
    userinfo = google.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    return userinfo

# @app.get("/", response_model=[])
# def get_products():
#     print(" the db connection is :", )
#     # products = db.query(Product).all()
#     # return products
#     a=['hello','hi']
#     return a

@app.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    print(" the db connection is :")
    products = db.query(Product).all()
    return products

    # return [
    #     {
    #         "id": 1,
    #         "title": "4K TV",
    #         "description": "Smart LED 50-inch",
    #         "price": 499.99,
    #         "image": "https://cdn.example.com/images/1.jpg"
    #
    #     },
    #     {
    #         "id": 2,
    #         "title": "Bluetooth Speaker",
    #         "description": "Portable audio device",
    #         "price": 29.99,
    #         "image": "https://cdn.example.com/images/2.jpg"
    #     }
    # ]


# @app.get("/")
# def test():
#     return {"message": "It works"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}