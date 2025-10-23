# backend/services/auth_service.py

from datetime import datetime, timedelta
import secrets
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.core.config import settings
from backend.db.mongo_model import users_col
from backend.services.email_services import send_email_notification

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXP_MINUTES = int(getattr(settings, "JWT_EXP_MINUTES", 60))

# --------------- Password utilities ----------------
def hash_password(password: str) -> str:
    print("DEBUG: hash_password called with:", password)  # 👈 Add this line
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # ✅ truncate plain password before verifying
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

# --------------- JWT utilities ----------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXP_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

# --------------- User CRUD / Auth ----------------
def get_user_by_email(email: str):
    return users_col.find_one({"email": email})

def create_user(email: str, password: str, full_name: str = None) -> dict:
    """
    Create user with hashed password.
    Returns inserted user dict (without password).
    """
    email = email.lower()
    if get_user_by_email(email):
        raise ValueError("User already exists")

    hashed = hash_password(password)
    user_doc = {
        "email": email,
        "password": hashed,
        "full_name": full_name or "",
        "created_at": datetime.utcnow(),
        # default preferences
        "notify_news": True,
        "news_time": None,
        "tracked_companies": [],
        "holdings": [],
        # OTP fields for password reset:
        "pwd_reset_otp": None,
        "pwd_reset_expires": None,
    }
    res = users_col.insert_one(user_doc)
    user_doc["_id"] = str(res.inserted_id)
    # don't return password
    user_doc.pop("password", None)
    return user_doc

def authenticate_user(email: str, password: str) -> Optional[dict]:
    user = get_user_by_email(email.lower())
    if not user:
        return None
    hashed = user.get("password")
    if not hashed:
        return None
    if verify_password(password, hashed):
        # convert _id to string for convenience
        user["_id"] = str(user["_id"])
        user.pop("password", None)
        return user
    return None

# --------------- Password reset (OTP) ----------------
def generate_and_send_otp(email: str, otp_lifetime_minutes: int = 10) -> bool:
    """
    Generate OTP, store hashed or plain OTP in db with expiry,
    send email via email service.
    """
    user = get_user_by_email(email.lower())
    if not user:
        # do not reveal user existence to client ideally
        return False

    # generate 6-digit OTP
    otp = f"{secrets.randbelow(10**6):06d}"  # zero-padded 6 digits
    expiry = datetime.utcnow() + timedelta(minutes=otp_lifetime_minutes)

    # store (we store plain OTP here for simplicity; for higher security hash it)
    users_col.update_one(
        {"email": email.lower()},
        {"$set": {"pwd_reset_otp": otp, "pwd_reset_expires": expiry}}
    )

    # send OTP via email
    subject = "Your password reset OTP"
    message = (
        f"Hello,\n\nYour password reset OTP is: {otp}\n\n"
        f"This code is valid for {otp_lifetime_minutes} minutes.\n\n"
        "If you did not request this, please ignore."
    )
    try:
        send_email_notification(email, subject, message)
    except Exception:
        # still return true to avoid enumerating users
        pass

    return True

def verify_otp_and_reset_password(email: str, otp: str, new_password: str) -> bool:
    user = get_user_by_email(email.lower())
    if not user:
        return False

    stored_otp = user.get("pwd_reset_otp")
    expires = user.get("pwd_reset_expires")
    if not stored_otp or not expires:
        return False

    # expiry stored as python datetime in Mongo (UTC)
    if isinstance(expires, str):
        # if stored as string, try to parse is possible
        try:
            expires_dt = datetime.fromisoformat(expires)
        except Exception:
            expires_dt = None
    else:
        expires_dt = expires

    if not expires_dt or datetime.utcnow() > expires_dt:
        return False

    if otp != stored_otp:
        return False

    # All good: update password and clear otp fields
    hashed = hash_password(new_password)
    users_col.update_one(
        {"email": email.lower()},
        {"$set": {"password": hashed}, "$unset": {"pwd_reset_otp": "", "pwd_reset_expires": ""}}
    )
    return True
