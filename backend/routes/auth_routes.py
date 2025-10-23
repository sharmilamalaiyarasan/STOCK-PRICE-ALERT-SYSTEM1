# backend/routes/auth_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from backend.services.auth_service import create_user, authenticate_user, generate_and_send_otp, verify_otp_and_reset_password
from backend.schemas.auth_schema import LoginSchema
from backend.services.auth_service import authenticate_user, create_access_token
from fastapi import APIRouter, Depends
from backend.utils.token import verify_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ------------------ Request Models ------------------

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

# ------------------ Routes ------------------

@router.post("/signup")
async def signup_user(request: SignupRequest):
    """Register a new user"""
    try:
        user = create_user(request.email, request.password, request.full_name)
        return {"message": "✅ User created successfully", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login")
def login(user: LoginSchema):
    auth_user = authenticate_user(user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # ✅ Create access token (valid 1 hour by default)
    token = create_access_token({"user_id": auth_user["_id"], "email": auth_user["email"]})

    return {
        "message": "✅ Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": auth_user
    }

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """Send OTP for password reset"""
    success = generate_and_send_otp(request.email)
    if success:
        return {"message": "📧 OTP sent successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/verify-otp")
async def verify_otp(request: VerifyOtpRequest):
    """Verify OTP and reset password"""
    success = verify_otp_and_reset_password(request.email, request.otp, request.new_password)
    if success:
        return {"message": "🔐 Password reset successfully"}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

@router.get("/me")
async def get_me(token_data: dict = Depends(verify_access_token)):
    return {"message": "✅ Token verified", "user": token_data}
