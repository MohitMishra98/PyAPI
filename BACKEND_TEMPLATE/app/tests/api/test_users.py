from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_email_verification_token, create_password_reset_token
from app.crud.crud_user import crud_user
from app.models.user import User


def test_root_and_health(client: TestClient):
    """
    Test root and healthcheck endpoints.
    """
    res_root = client.get("/")
    assert res_root.status_code == status.HTTP_200_OK
    assert res_root.json()["status"] == "online"

    res_health = client.get("/health")
    assert res_health.status_code == status.HTTP_200_OK
    assert res_health.json()["status"] == "healthy"


def test_signup_success(client: TestClient):
    """
    Test new user registration.
    """
    payload = {
        "email": "newuser@example.com",
        "password": "StrongPassword123!",
        "full_name": "New User",
    }
    response = client.post(f"{settings.API_V1_STR}/users/signup", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert data["is_verified"] is False
    assert "id" in data


def test_signup_duplicate_email(client: TestClient, test_user: User):
    """
    Test that registering an existing email returns 409 Conflict.
    """
    payload = {
        "email": test_user.email,
        "password": "AnotherPassword123!",
    }
    response = client.post(f"{settings.API_V1_STR}/users/signup", json=payload)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_login_json_success(client: TestClient, test_user: User):
    """
    Test JSON login with valid credentials returns a valid JWT token.
    """
    payload = {
        "email": test_user.email,
        "password": "TestPassword123!",
    }
    response = client.post(f"{settings.API_V1_STR}/users/login", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient, test_user: User):
    """
    Test JSON login with invalid password returns 401.
    """
    payload = {
        "email": test_user.email,
        "password": "WrongPassword!",
    }
    response = client.post(f"{settings.API_V1_STR}/users/login", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_oauth_form(client: TestClient, test_user: User):
    """
    Test OAuth2 form-data login for Swagger UI compatibility.
    """
    form_data = {
        "username": test_user.email,
        "password": "TestPassword123!",
    }
    response = client.post(f"{settings.API_V1_STR}/users/login/oauth", data=form_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data


def test_verify_email_flow(client: TestClient, db: Session):
    """
    Test email verification with token.
    """
    email = "unverified@example.com"
    signup_res = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json={"email": email, "password": "Password123!"},
    )
    assert signup_res.status_code == status.HTTP_201_CREATED

    token = create_email_verification_token(email)
    verify_res = client.post(
        f"{settings.API_V1_STR}/users/verify-email",
        json={"token": token},
    )
    assert verify_res.status_code == status.HTTP_200_OK
    assert "Email verified successfully" in verify_res.json()["message"]

    # Check database state
    user = crud_user.get_by_email(db, email=email)
    assert user is not None
    assert user.is_verified is True


def test_forgot_and_reset_password_flow(client: TestClient, db: Session, test_user: User):
    """
    Test requesting password reset and updating password.
    """
    # 1. Forgot password request
    forgot_res = client.post(
        f"{settings.API_V1_STR}/users/forgot-password",
        json={"email": test_user.email},
    )
    assert forgot_res.status_code == status.HTTP_200_OK

    # 2. Reset password using generated token
    token = create_password_reset_token(test_user.email)
    new_password = "BrandNewPassword123!"
    reset_res = client.post(
        f"{settings.API_V1_STR}/users/reset-password",
        json={"token": token, "new_password": new_password},
    )
    assert reset_res.status_code == status.HTTP_200_OK

    # 3. Log in with the newly set password
    login_res = client.post(
        f"{settings.API_V1_STR}/users/login",
        json={"email": test_user.email, "password": new_password},
    )
    assert login_res.status_code == status.HTTP_200_OK
    assert "access_token" in login_res.json()


def test_get_current_user_me(client: TestClient, user_token_headers: dict, test_user: User):
    """
    Test reading authenticated user profile.
    """
    response = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email
    assert data["id"] == test_user.id


def test_update_current_user_me(client: TestClient, user_token_headers: dict):
    """
    Test updating user profile.
    """
    update_data = {"full_name": "Updated Name"}
    response = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=user_token_headers,
        json=update_data,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["full_name"] == "Updated Name"
