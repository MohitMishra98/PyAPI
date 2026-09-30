import json
from typing import Any, List, Optional, Union
from pydantic import EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "FastAPI Production Template"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security & JWT
    SECRET_KEY: str = "super-secret-jwt-key-replace-in-production-environments-998877"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 2
    EMAIL_VERIFY_TOKEN_EXPIRE_HOURS: int = 24

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Any) -> Any:
        if isinstance(v, str):
            # Normalizes postgres:// to postgresql:// for SQLAlchemy 2.0+
            if v.startswith("postgres://"):
                v = v.replace("postgres://", "postgresql://", 1)
        return v

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, str) and v.startswith("["):
            return json.loads(v)
        return v

    # Frontend URL for email verification and reset password links
    FRONTEND_URL: str = "http://localhost:3000"

    # Email / SMTP Settings (Required for sending emails)
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = ""
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: EmailStr = "noreply@example.com"
    EMAILS_FROM_NAME: str = "FastAPI Production Template"

    # RAG Settings
    QDRANT_API_KEY: str = ""
    QDRANT_URL: str = ""
    GROQ_API_KEY: str = ""
    COLLECTION_NAME: str = "knowledge"
    EMBEDDING_SIZE: int = 384

    # AI MODELS
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "openai/gpt-oss-120b"
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
