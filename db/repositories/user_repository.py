# User data access logic  
from db.database import db
from bson import ObjectId
from datetime import datetime

users_collection = db['users']

def create_user(user_data: dict) -> dict:
    new_user = users_collection.insert_one(user_data)
    user_data['_id'] = str(new_user.inserted_id) 
    return user_data

def get_user_by_email(email: str) -> dict:
    user = users_collection.find_one({"email": email})
    if user:
        user['_id'] = str(user['_id'])  
    return user

def store_tokens(user_id: str, access_token: str, refresh_token: str):
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "access_token": access_token,
            "refresh_token": refresh_token
        }}
    )

def update_password_reset_otp(user_id: str, otp: str):
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "password_reset_otp": otp,
            "password_reset_otp_created_at": datetime.utcnow()
        }}
    )

def verify_and_clear_password_reset_otp(user_id: str, otp: str) -> bool:
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user and user.get("password_reset_otp") == otp:
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$unset": {"password_reset_otp": "", "password_reset_otp_created_at": ""}}
        )
        return True
    return False


def reset_password(user_id: str, new_hashed_password: str):
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"hashed_password": new_hashed_password},
         "$unset": {
            "password_reset_token": "",
            "password_reset_token_created_at": ""
         }}
    )
def get_user_by_reset_token(reset_token: str) -> dict:
    user = users_collection.find_one({"password_reset_token": reset_token})
    if user:
        user['_id'] = str(user['_id']) 
    return user

def update_signup_otp(user_id: str, otp: str):
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "signup_otp": otp,
            "otp_created_at": datetime.utcnow()
        }}
    )

def verify_and_clear_signup_otp(user_id: str, otp: str) -> bool:
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user and user.get("signup_otp") == otp:
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_verified": True},
             "$unset": {"signup_otp": "", "otp_created_at": ""}}
        )
        return True
    return False