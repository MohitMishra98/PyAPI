from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
import bcrypt
import jwt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed bcrypt password.
    """
    try:
        # bcrypt has a 72-byte limit
        return bcrypt.checkpw(
            plain_password.encode("utf-8")[:72],
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt with salt.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8")[:72], salt).decode("utf-8")


def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a signed JWT access token.
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "exp": expire,
        "nbf": now,
        "iat": now,
        "sub": str(subject),
        "type": "access",
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_email_verification_token(email: str) -> str:
    """
    Create a signed JWT token specifically for email verification.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours=settings.EMAIL_VERIFY_TOKEN_EXPIRE_HOURS)
    to_encode = {
        "exp": expire,
        "nbf": now,
        "iat": now,
        "sub": email,
        "type": "email_verification",
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_email_verification_token(token: str) -> Optional[str]:
    """
    Decode and verify an email verification token, returning the user email.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if payload.get("type") != "email_verification":
            return None
        return payload.get("sub")
    except (jwt.PyJWTError, Exception):
        return None


def create_password_reset_token(email: str) -> str:
    """
    Create a signed JWT token specifically for password reset.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    to_encode = {
        "exp": expire,
        "nbf": now,
        "iat": now,
        "sub": email,
        "type": "password_reset",
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Decode and verify a password reset token, returning the user email.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if payload.get("type") != "password_reset":
            return None
        return payload.get("sub")
    except (jwt.PyJWTError, Exception):
        return None
