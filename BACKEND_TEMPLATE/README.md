# Production-Grade FastAPI Template

A clean, lean, production-ready FastAPI template with JWT authentication, email verification, password reset, and clean architecture.

---

## 📁 Project Structure

```text
my_fastapi_project/
├── app/
│   ├── api/                 # API routers and endpoints
│   │   ├── dependencies.py  # Reusable dependency injections (e.g., get_db, current_user)
│   │   └── v1/              # API versioning
│   │       ├── endpoints/
│   │       │   ├── users.py # User & Auth endpoints (signup, signin, verify, reset)
│   │       │   └── items.py # CRUD example with ownership authorization
│   │       └── api.py       # Aggregates all v1 routers into one APIRouter
│   ├── core/                # App-wide settings and security
│   │   ├── config.py        # Pydantic BaseSettings for environment variables
│   │   └── security.py      # Password hashing (bcrypt), JWT token generation (PyJWT)
│   ├── crud/                # Database CRUD operations
│   │   ├── base.py          # Generic CRUD class to reduce boilerplate
│   │   ├── crud_user.py     # Specific database queries for User model
│   │   └── crud_item.py     # Specific database queries for Item model
│   ├── db/                  # Database connections and sessions
│   │   ├── session.py       # SQLAlchemy engine and sessionmaker
│   │   └── base.py          # SQLAlchemy declarative base (imports all models)
│   ├── models/              # SQLAlchemy ORM models (Database shape)
│   │   ├── user.py          # User table with status, verification & timestamps
│   │   └── item.py          # Item table linked to User via ForeignKey
│   ├── schemas/             # Pydantic models (Data validation / API shape)
│   │   ├── user.py          # UserCreate, UserUpdate, UserResponse, Verify/Reset schemas
│   │   ├── item.py          # ItemCreate, ItemUpdate, ItemResponse schemas
│   │   ├── token.py         # Token and TokenPayload schemas
│   │   └── msg.py           # Standard message response schema
│   ├── services/            # Business logic (Keeps endpoints thin)
│   │   ├── user_service.py  # Signup, authentication, token verification, password reset
│   │   └── email_service.py # Email delivery via SMTP or development logger
│   ├── tests/               # Pytest test suite
│   │   ├── conftest.py      # Test fixtures (isolated DB session, test client)
│   │   └── api/             # API test cases
│   │       ├── test_users.py
│   │       └── test_items.py
│   └── main.py              # FastAPI application instance & entry point
├── .env                     # Local environment settings (git-ignored)
├── .env.example             # Example environment variables template
├── .gitignore               # Standard git ignore definitions
└── requirements.txt         # Project dependencies
```

---

## 🚀 Features

- **Production Architecture**: Strict separation of concerns (API -> Services -> CRUD -> Models/DB).
- **JWT Authentication**: Secure JSON Web Tokens using `PyJWT` and bcrypt password hashing.
- **Email Verification Flow**: Signups receive an email verification token expiring in 24 hours.
- **Forgot & Reset Password**: Secure token-based password reset expiring in 2 hours with anti-enumeration protection.
- **Database Agnostic**: Pre-configured for PostgreSQL (Neon / AWS RDS / local) or SQLite for fast local development.
- **Interactive API Docs**: Built-in Swagger UI (`/docs`) and ReDoc (`/redoc`) with OAuth2 Bearer authorization.
- **Thin Endpoints & Generic CRUD**: Generic reusable `CRUDBase` class and dedicated service layer.
- **Automated Tests**: Pytest test suite using in-memory SQLite for instant, isolated test runs.

---

## 🛠️ Getting Started

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux / macOS:
source .venv/bin/activate
# On Windows (cmd):
.venv\Scripts\activate.bat
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create `.env` based on `.env.example`:

```bash
cp .env.example .env
```

Your `.env` includes:
```ini
PROJECT_NAME="FastAPI Production Template"
VERSION="1.0.0"
API_V1_STR="/api/v1"
ENVIRONMENT="development"
DEBUG=true

# Secret key for JWT signing (replace in production!)
SECRET_KEY="your-super-secret-jwt-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
EMAIL_RESET_TOKEN_EXPIRE_HOURS=2
EMAIL_VERIFY_TOKEN_EXPIRE_HOURS=24

# Database URL (PostgreSQL / Neon or SQLite)
DATABASE_URL="postgresql://user:password@host/dbname?sslmode=require"

# Email / SMTP Settings (Optional: if empty, tokens log to terminal console)
EMAILS_FROM_EMAIL="noreply@example.com"
EMAILS_FROM_NAME="FastAPI Template"
```

---

## 🏃 Running the Application

Start the local development server with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Interactive API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧪 Running Tests

Execute the Pytest test suite:

```bash
pytest -v
```

Tests run in an isolated in-memory SQLite database without modifying your live database.

---

## 📡 API Endpoints Overview

### Authentication & Users (`/api/v1/users`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/users/signup` | Register a new user & trigger verification email | No |
| `POST` | `/api/v1/users/login` | Authenticate with JSON `{"email", "password"}` | No |
| `POST` | `/api/v1/users/login/oauth` | OAuth2 form login (used by Swagger UI "Authorize") | No |
| `POST` | `/api/v1/users/verify-email` | Verify email with token | No |
| `POST` | `/api/v1/users/resend-verification`| Resend verification email | No |
| `POST` | `/api/v1/users/forgot-password` | Request password reset token | No |
| `POST` | `/api/v1/users/reset-password` | Reset password using token | No |
| `GET` | `/api/v1/users/me` | Get currently logged-in user profile | Bearer Token |
| `PATCH`| `/api/v1/users/me` | Update current user profile or password | Bearer Token |
| `GET` | `/api/v1/users/` | List all users (admin only) | Superuser Token |
| `GET` | `/api/v1/users/{id}` | Get user by ID | Bearer Token |

### Items (`/api/v1/items`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/v1/items/` | List items belonging to authenticated user | Bearer Token |
| `POST` | `/api/v1/items/` | Create a new item owned by current user | Bearer Token |
| `GET` | `/api/v1/items/{id}` | Retrieve specific item by ID | Bearer Token (Owner) |
| `PUT` | `/api/v1/items/{id}` | Update item by ID | Bearer Token (Owner) |
| `DELETE`| `/api/v1/items/{id}` | Delete item by ID | Bearer Token (Owner) |
