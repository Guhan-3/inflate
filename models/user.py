# User model 
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    _id: str
    username: str
    email: EmailStr
    is_verified: bool = False

class LoginSchema(BaseModel):
    email: str
    password: str