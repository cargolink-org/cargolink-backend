"""
Application configuration (Task A.1).

Reconstruction note (Task A.3 session): recreated as a prerequisite — see
the note at the top of app/core/enums.py. Only the surface this session's
A.3 work actually depends on (MOCK_REPO, ENV) is asserted with confidence;
the remaining fields mirror the technical spec's confirmed stack and are
kept intentionally simple.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Environment = Field(Environment.LOCAL, env="ENV")
    mock_repo: bool = Field(True, env="MOCK_REPO")

    jwt_secret_key: str = Field("changeme-in-env", env="JWT_SECRET_KEY")
    jwt_access_token_ttl_minutes: int = Field(15, env="JWT_ACCESS_TOKEN_TTL_MINUTES")
    jwt_refresh_token_ttl_days: int = Field(30, env="JWT_REFRESH_TOKEN_TTL_DAYS")

    database_url: Optional[str] = Field(None, env="DATABASE_URL")
    s3_bucket_name: Optional[str] = Field(None, env="S3_BUCKET_NAME")

    osrm_base_url: str = Field("http://localhost:5000", env="OSRM_BASE_URL")
    msg91_api_key: str = Field("", env="MSG91_API_KEY")
    sendgrid_api_key: str = Field("", env="SENDGRID_API_KEY")

    @property
    def MOCK_REPO(self) -> bool:
        return self.mock_repo

    @MOCK_REPO.setter
    def MOCK_REPO(self, value: bool) -> None:
        self.mock_repo = value

    @property
    def JWT_SECRET_KEY(self) -> str:
        return self.jwt_secret_key

    @JWT_SECRET_KEY.setter
    def JWT_SECRET_KEY(self, value: str) -> None:
        self.jwt_secret_key = value

    @property
    def DATABASE_URL(self) -> Optional[str]:
        return self.database_url

    @DATABASE_URL.setter
    def DATABASE_URL(self, value: Optional[str]) -> None:
        self.database_url = value

    @property
    def S3_BUCKET_NAME(self) -> Optional[str]:
        return self.s3_bucket_name

    @S3_BUCKET_NAME.setter
    def S3_BUCKET_NAME(self, value: Optional[str]) -> None:
        self.s3_bucket_name = value

    @model_validator(mode="after")
    def validate_production_config(cls, values):
        if values.environment != Environment.PRODUCTION:
            return values

        errors = []
        if values.mock_repo:
            errors.append("MOCK_REPO must be false in production")
        if not values.jwt_secret_key or values.jwt_secret_key == "changeme-in-env":
            errors.append("JWT_SECRET_KEY must be overridden in production")
        if not values.database_url:
            errors.append("DATABASE_URL is required in production")
        if not values.s3_bucket_name:
            errors.append("S3_BUCKET_NAME is required in production")

        if errors:
            raise ValueError("; ".join(errors))

        return values


settings = Settings()
