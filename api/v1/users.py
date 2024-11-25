from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from models.user import UserCreate, UserResponse, LoginSchema
from services.user_service import (
    register_user,
    login_user,
    initiate_password_reset,
    complete_password_reset,
    verify_password_reset_otp,
    resend_password_reset_otp,
    verify_signup_otp,
    resend_signup_otp,
)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user_endpoint(user_request: UserCreate):
    try:
        user_data = user_request.dict()
        user = register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=dict)
async def login_user_endpoint(user_request: LoginSchema):
    email = user_request.email
    password = user_request.password
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required.")
    
    auth_result = login_user(email, password)
    if not auth_result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return JSONResponse(content={"data": auth_result}, status_code=200)

@router.post("/forgot-password")
async def forgot_password(email: str = Body(..., embed=True)):
    try:
        result = initiate_password_reset(email)
        return JSONResponse(content=result, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/verify-password-reset-otp")
async def verify_password_reset_otp_endpoint(email: str = Body(..., embed=True), otp: str = Body(..., embed=True)):
    try:
        verify_password_reset_otp(email, otp)
        return JSONResponse(content={"message": "OTP verified successfully"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/resend-password-reset-otp")
async def resend_password_reset_otp_endpoint(email: str = Body(..., embed=True)):
    try:
        resend_password_reset_otp(email)
        return JSONResponse(content={"message": "OTP resent successfully"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reset-password")
async def reset_password(email: str = Body(..., embed=True), new_password: str = Body(..., embed=True)):
    try:
        result = complete_password_reset(email, new_password)
        return JSONResponse(content={"message": "Password reset successfully"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify-signup-otp")
async def verify_signup_otp_endpoint(email: str = Body(..., embed=True), otp: str = Body(..., embed=True)):
    try:
        verify_signup_otp(email, otp)
        return JSONResponse(content={"message": "Account verified successfully"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/resend-signup-otp")
async def resend_signup_otp_endpoint(email: str = Body(..., embed=True)):
    try:
        resend_signup_otp(email)
        return JSONResponse(content={"message": "OTP resent successfully"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
