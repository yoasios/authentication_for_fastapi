from fastapi import FastAPI, Depends, HTTPException, Cookie, Response
from sqlalchemy.orm import Session
from database import get_db, engine, base
from modals import User
from schemas import inputs
from jose import jwt, JWTError
from passlib.context import CryptContext
import datetime
import hashlib


app = FastAPI()

# Create tables
base.metadata.create_all(bind=engine)

pwd = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

@app.post("/signin/{email}/{password}")
def user_name(email: str, password: str, response: Response, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    # Check if user already has valid token
    if access_token:
        try:
            payload = jwt.decode(access_token, "secret_key", algorithms=["HS256"])
            return {"message": "Already logged in", "user_id": payload.get("user_id")}
        except JWTError:
            pass  # Token invalid, proceed with login
    
    users = db.query(User).filter(User.email == email).first()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    elif not pwd.verify(password, users.password):
        raise HTTPException(status_code=404, detail="Invalid password")
    elif pwd.verify(password, users.password):
        jwt_token = jwt.encode(
            {"user_id": users.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            "secret_key",
            algorithm="HS256"
        )
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        return {"message": "User found"} 
    
@app.post("/login")
def create_user(userl: inputs, response: Response, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    # Check if user already has valid token
    if access_token:
        try:
            payload = jwt.decode(access_token, "secret_key", algorithms=["HS256"])
            return {"message": "Already logged in", "user_id": payload.get("user_id")}
        except JWTError:
            pass  # Token invalid, proceed with registration
    
    new_user = User(name=userl.name, email=userl.email, password=pwd.hash(userl.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    jwt_token = jwt.encode(
        {"user_id": new_user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        "secret_key",
        algorithm="HS256"
    )
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return {"user": new_user.name}


@app.get("/protected")
def protected_route(access_token: str = Cookie(None) , db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not logged in")

    try:
        payload = jwt.decode(
            access_token,
            "secret_key",
            algorithms=["HS256"]
        )

        return {
            "message": "Protected route accessed",
            "user_id": payload.get("user_id")
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")