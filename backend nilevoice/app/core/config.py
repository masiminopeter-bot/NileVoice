from pathlib import Path
from typing import Any

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = Field("NileVoice AI", env="APP_NAME")
    app_version: str = Field("0.1.0", env="APP_VERSION")
    app_env: str = Field("development", env="APP_ENV")

    db_host: str = Field("localhost", env="DB_HOST")
    db_port: int = Field(3306, env="DB_PORT")
    db_user: str = Field("root", env="DB_USER")
    db_password: str = Field("", env="DB_PASSWORD")
    db_name: str = Field("nilevoice", env="DB_NAME")

    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_access_token_expires_minutes: int = Field(60, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expires_days: int = Field(7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")
    email_verification_token_expires_hours: int = Field(48, env="EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS")
    password_reset_token_expires_hours: int = Field(2, env="PASSWORD_RESET_TOKEN_EXPIRE_HOURS")

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
