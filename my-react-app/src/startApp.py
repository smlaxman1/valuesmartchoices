
from fastapi import FastAPI, Request,Depends,HTTPException
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth2Session
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr

from models.product import Product, ProductResponse
from models.user import User
from models.EmailRequest import EmailRequest
from database.dbConnect import get_db
from utils.token import generate_email_token, verify_email_token, get_password_hash, create_access_token

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



@app.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products



@app.post("/signup")
def signup(request: EmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.email == request.email) & ( User.is_verified == False)).first()
    print(user.is_verified)
    if user:
        token = generate_email_token(request.email)
        verify_link = f"http://localhost:3000/verify-email?token={token}"  # Point to frontend
        print("Send email with link:", verify_link)  # Replace with real email logic

    elif (user.is_verified == True):
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        new_user = User(email=request.email)
        db.add(new_user)
        db.commit()

        token = generate_email_token(request.email)
        verify_link = f"http://localhost:3000/verify-email?token={token}"  # Point to frontend
        print("Send email with link:", verify_link)  # Replace with real email logic

    return {"msg": "Verification email sent"}

# ---------------- Verify Email ----------------
@app.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()
    return {"msg": "Email verified. You can now set your password."}

# ---------------- Set Password ----------------
class SetPasswordRequest(BaseModel):
    email: EmailStr
    password: str

@app.post("/set-password")
def set_password(req: SetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not user.is_verified:
        raise HTTPException(status_code=400, detail="User not found or not verified")

    user.hashed_password = get_password_hash(req.password)
    db.commit()

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
