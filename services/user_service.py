from db.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    store_tokens,
    update_password_reset_otp,
    reset_password,
    update_signup_otp,
    verify_and_clear_password_reset_otp,
    verify_and_clear_signup_otp,
)
from utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    generate_otp,
)
from utils.email import (
    send_otp_email,
    send_password_reset_email,
    send_verification_success_email,
    send_password_reset_success_email,
)
from models.user import UserCreate


def register_user(user_data: dict) -> dict:
    if get_user_by_email(user_data["email"]):
        raise ValueError("User with this email already exists.")

    user_data["hashed_password"] = hash_password(user_data["password"])
    del user_data["password"]  

    otp = generate_otp()
    user = create_user(user_data)
    update_signup_otp(user["_id"], otp)

    send_otp_email(user_data["email"], otp)
    return {"id": user["_id"], "username": user["username"], "email": user["email"]}


def verify_signup_otp(email: str, otp: str):
    user = get_user_by_email(email)
    if not user:
        raise ValueError("User does not exist.")

    if not verify_and_clear_signup_otp(user["_id"], otp):
        raise ValueError("Invalid or expired OTP.")

    send_verification_success_email(email)


def resend_signup_otp(email: str):
    user = get_user_by_email(email)
    if not user:
        raise ValueError("User does not exist.")
    if user.get("is_verified"):
        raise ValueError("User is already verified.")

    otp = generate_otp()
    update_signup_otp(user["_id"], otp)

    send_otp_email(email, otp)


def login_user(email: str, password: str) -> dict:
    user = get_user_by_email(email)
    if not user or not verify_password(user["hashed_password"], password):
        raise ValueError("Invalid email or password.")

    access_token = create_access_token({"sub": user["_id"]})
    refresh_token = create_refresh_token({"sub": user["_id"]})
    store_tokens(user["_id"], access_token, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user["_id"],
            "username": user["username"],
            "email": user["email"],
        },
    }


def initiate_password_reset(email: str) -> dict:
    user = get_user_by_email(email)
    if not user:
        raise ValueError("Email not registered.")

    otp = generate_otp()
    update_password_reset_otp(user["_id"], otp)

    send_password_reset_email(email, otp)
    return {"message": "Password reset OTP sent"}


def verify_password_reset_otp(email: str, otp: str) -> str:
    user = get_user_by_email(email)
    if not user:
        raise ValueError("User does not exist.")

    if not verify_and_clear_password_reset_otp(user["_id"], otp):
        raise ValueError("Invalid or expired OTP.")

    return create_access_token({"sub": user["_id"]})
def resend_password_reset_otp(email: str):
    user = get_user_by_email(email)
    if not user:
        raise ValueError("User does not exist.")

    otp = generate_otp()
    update_password_reset_otp(user["_id"], otp)

    send_password_reset_email(email, otp)


def complete_password_reset(user_id: str, new_password: str): 
    hashed_password = hash_password(new_password)
    reset_password(user_id, hashed_password)

    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User does not exist.")
    
    send_password_reset_success_email(user["email"])
    return {"message": "Password reset successful"}
