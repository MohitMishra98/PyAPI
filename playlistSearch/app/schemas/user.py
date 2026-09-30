import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True


# Properties to receive on signup
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password must be between 8 and 72 characters",
    )
    full_name: Optional[str] = None


# Properties to receive on signin
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Properties to receive on user update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=72)
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


# Properties to return via API
class UserResponse(UserBase):
    id: uuid.UUID
    is_verified: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Email verification request
class VerifyEmailRequest(BaseModel):
    token: str


# Resend verification request
class ResendVerificationRequest(BaseModel):
    email: EmailStr


# Password reset request
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# Password reset completion
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password must be between 8 and 72 characters",
    )
