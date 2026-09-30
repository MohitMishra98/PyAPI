import pytest
from typing import Dict, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_db
from app.core.security import create_access_token
from app.crud.crud_user import crud_user
from app.db.base import Base
from app.main import app
from app.models.user import User
from app.schemas.user import UserCreate

# In-memory SQLite engine with StaticPool for fast, isolated tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Create tables in test database once for the session.
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def mock_email_service(monkeypatch):
    """
    Mock email sending during tests to prevent external network calls.
    """
    from app.services.email_service import email_service
    monkeypatch.setattr(email_service, "_send_email", lambda *args, **kwargs: None)



@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Fresh database session per test function with rollback/cleanup.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    TestClient configured with dependency override for get_db.
    """
    def _override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db: Session) -> User:
    """
    Fixture creating a standard verified user.
    """
    user_in = UserCreate(
        email="testuser@example.com",
        password="TestPassword123!",
        full_name="Test User",
    )
    user = crud_user.get_by_email(db, email=user_in.email)
    if not user:
        user = crud_user.create(db, obj_in=user_in)
        user = crud_user.mark_as_verified(db, user=user)
    return user


@pytest.fixture(scope="function")
def user_token_headers(test_user: User) -> Dict[str, str]:
    """
    Authorization header fixture for the test user.
    """
    token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {token}"}
