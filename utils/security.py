# Security utilities 
import jwt
import os
import hashlib
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM
import random

def hash_password(password: str) -> str:
    salt = os.urandom(16) 
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + hashed_password.hex()  

def verify_password(stored_password: str, provided_password: str) -> bool:
    salt = bytes.fromhex(stored_password[:32])  
    stored_hash = stored_password[32:]  
    hashed_password = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return hashed_password.hex() == stored_hash  

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})  
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})  
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  

def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
    except jwt.PyJWTError:
        return None  

def generate_password_reset_token(email: str, expires_delta: timedelta = timedelta(minutes=15)) -> str:
    expiration = datetime.utcnow() + expires_delta  
    payload = {
        "sub": email,  
        "exp": expiration
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  

def verify_password_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        return payload["sub"]  
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired. Please request a new password reset.")  
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token. Please request a new password reset.")
def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices("0123456789", k=length))
