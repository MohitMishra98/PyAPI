import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_active_superuser,
    get_current_user,
    get_db,
)
from app.crud.crud_user import crud_user
from app.models.user import User
from app.schemas.msg import Msg
from app.schemas.token import Token
from app.schemas.user import (
    ForgotPasswordRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    VerifyEmailRequest,
)
from app.services.user_service import user_service

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def signup(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create a new user account and dispatch an email verification token.
    """
    user = user_service.register_user(db, user_in=user_in)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Log in with JSON email & password",
)
def login_json(
    *,
    db: Session = Depends(get_db),
    login_data: UserLogin,
) -> Any:
    """
    Authenticate user with JSON payload and return a JWT access token.
    """
    return user_service.authenticate_user(
        db, email=login_data.email, password=login_data.password
    )


@router.post(
    "/login/oauth",
    response_model=Token,
    summary="OAuth2 compatible token login (used by Swagger UI)",
)
def login_oauth(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login for Swagger UI authorization dialog.
    Accepts 'username' (which is the user's email) and 'password'.
    """
    return user_service.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )


@router.post(
    "/verify-email",
    response_model=Msg,
    summary="Verify user email address",
)
def verify_email(
    *,
    db: Session = Depends(get_db),
    request_data: VerifyEmailRequest,
) -> Any:
    """
    Verify user's email using the token received in email.
    """
    user_service.verify_email(db, token=request_data.token)
    return Msg(message="Email verified successfully. You can now access all features.")


@router.post(
    "/resend-verification",
    response_model=Msg,
    summary="Resend verification email",
)
def resend_verification(
    *,
    db: Session = Depends(get_db),
    request_data: ResendVerificationRequest,
) -> Any:
    """
    Resend verification email. Always returns success to prevent user enumeration.
    """
    user_service.resend_verification(db, email=request_data.email)
    return Msg(
        message="If the email exists and is unverified, a verification email has been dispatched."
    )


@router.post(
    "/forgot-password",
    response_model=Msg,
    summary="Request password reset token",
)
def forgot_password(
    *,
    db: Session = Depends(get_db),
    request_data: ForgotPasswordRequest,
) -> Any:
    """
    Request a password reset email. Always returns success to prevent user enumeration.
    """
    user_service.request_password_reset(db, email=request_data.email)
    return Msg(
        message="If the email is registered, password reset instructions have been sent."
    )


@router.post(
    "/reset-password",
    response_model=Msg,
    summary="Reset password with token",
)
def reset_password(
    *,
    db: Session = Depends(get_db),
    request_data: ResetPasswordRequest,
) -> Any:
    """
    Reset user password using a valid reset token.
    """
    user_service.reset_password(
        db, token=request_data.token, new_password=request_data.new_password
    )
    return Msg(message="Password has been reset successfully. You can now log in.")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
def read_current_user(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Fetch the profile of the currently logged-in user.
    """
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
def update_current_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update profile details or password for the current user.
    """
    if user_in.email and user_in.email != current_user.email:
        existing = crud_user.get_by_email(db, email=user_in.email)
        if existing and existing.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            )
        # If email is updated, require re-verification
        current_user.is_verified = False

    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List users (Admin only)",
)
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Retrieve list of users. Requires superuser privileges.
    """
    return crud_user.get_multi(db, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
)
def read_user_by_id(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get a specific user by id. Users can view their own profile; superusers can view any.
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    if user.id != current_user.id and not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have sufficient privileges.",
        )
    return user
