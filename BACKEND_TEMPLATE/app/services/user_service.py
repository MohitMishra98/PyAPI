from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_email_verification_token,
    create_password_reset_token,
    verify_email_verification_token,
    verify_password_reset_token,
)
from app.crud.crud_user import crud_user
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.services.email_service import email_service


class UserService:
    def register_user(self, db: Session, *, user_in: UserCreate) -> User:
        """
        Register a new user, dispatch email verification, and return the created user.
        """
        existing_user = crud_user.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists in the system.",
            )

        user = crud_user.create(db, obj_in=user_in)

        # Generate verification token and send verification email
        verification_token = create_email_verification_token(user.email)
        email_service.send_verification_email(email_to=user.email, token=verification_token)

        return user

    def authenticate_user(self, db: Session, *, email: str, password: str) -> Token:
        """
        Authenticate user credentials and generate a JWT access token.
        """
        user = crud_user.authenticate(db, email=email, password=password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not crud_user.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account.",
            )

        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token, token_type="bearer")

    def verify_email(self, db: Session, *, token: str) -> User:
        """
        Verify user email using a signed verification token.
        """
        email = verify_email_verification_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired email verification token.",
            )

        user = crud_user.get_by_email(db, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found for this token.",
            )

        if user.is_verified:
            return user

        return crud_user.mark_as_verified(db, user=user)

    def resend_verification(self, db: Session, *, email: str) -> None:
        """
        Resend email verification token. Always succeeds silently to prevent email enumeration.
        """
        user = crud_user.get_by_email(db, email=email)
        if user and not user.is_verified:
            token = create_email_verification_token(user.email)
            email_service.send_verification_email(email_to=user.email, token=token)

    def request_password_reset(self, db: Session, *, email: str) -> None:
        """
        Generate password reset token and dispatch email. Always returns 200 to prevent user enumeration.
        """
        user = crud_user.get_by_email(db, email=email)
        if user and user.is_active:
            reset_token = create_password_reset_token(user.email)
            email_service.send_password_reset_email(email_to=user.email, token=reset_token)

    def reset_password(self, db: Session, *, token: str, new_password: str) -> None:
        """
        Reset user password after validating reset token.
        """
        email = verify_password_reset_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired password reset token.",
            )

        user = crud_user.get_by_email(db, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account.",
            )

        crud_user.update_password(db, user=user, new_password=new_password)


user_service = UserService()
