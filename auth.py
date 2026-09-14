from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi import Cookie, HTTPException
from jose import jwt, JWTError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
