"""
CargoLink backend configuration.

Centralizes every piece of environment-driven config the app needs:
database, JWT, S3, OSRM, SMS (MSG91/Gupshup), email (SendGrid), Sentry,
and the MOCK_REPO toggle that decides whether business logic runs against
in-memory repositories or real SQLAlchemy-backed ones.

Design intent (per Task A.1):
- Local/dev/test must work with ZERO configuration: every field has a safe
  default, MOCK_REPO defaults to true, and no live DB/OSRM/S3/SMS/email
  provider is required to boot the app or run the test suite.
- Production is held to a stricter bar: `validate_production_requirements`
  fails fast and loudly at startup if a real deployment is missing
  required secrets or (worse) still has MOCK_REPO enabled.

Missing *required* config should never fail obscurely on first request --
it fails here, at settings construction time, before the app can serve
any traffic.
"""
from enum import Enum
from typing import Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- App / environment ---
    environment: Environment = Field(
        default=Environment.LOCAL,
        description="Deployment environment: local, test, staging, or production.",
    )
    app_name: str = Field(default="CargoLink Backend", description="Human-readable application name.")
    debug: bool = Field(default=True, description="Enable debug mode (verbose logging, SQL echo).")

    # --- Repository mode (the mock/real switch the whole architecture hinges on) ---
    mock_repo: bool = Field(
        default=True,
        description=(
            "When true, every repository interface resolves to its "
            "in-memory mock implementation instead of the real "
            "SQLAlchemy-backed one. Must be false in production."
        ),
    )

    # --- Database ---
    database_url: Optional[str] = Field(
        default=None,
        description=(
            "Async SQLAlchemy PostgreSQL connection string, e.g. "
            "postgresql+asyncpg://user:pass@host:5432/cargolink. "
            "Not required while mock_repo=true."
        ),
    )

    # --- JWT / Auth ---
    jwt_secret_key: str = Field(
        default="dev-insecure-secret-change-me",
        description="Secret key used to sign JWT access/refresh tokens. MUST be overridden outside local/test.",
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT signing algorithm.")
    jwt_access_token_expire_minutes: int = Field(
        default=15, description="Access token lifetime in minutes (short-lived, per the security checklist)."
    )
    jwt_refresh_token_expire_days: int = Field(
        default=30, description="Refresh token lifetime in days (rotating, reuse-detected)."
    )

    # --- AWS S3 (document storage) ---
    aws_access_key_id: Optional[str] = Field(default=None, description="AWS access key ID for S3 document storage.")
    aws_secret_access_key: Optional[str] = Field(default=None, description="AWS secret access key for S3.")
    aws_region: str = Field(default="ap-south-1", description="AWS region hosting the S3 bucket.")
    s3_bucket_name: Optional[str] = Field(
        default=None, description="S3 bucket name for CargoLink documents. Bucket must never be public."
    )
    s3_signed_url_expire_seconds: int = Field(
        default=600, description="Expiry (seconds) for S3 signed upload/read URLs."
    )

    # --- OSRM (self-hosted routing) ---
    osrm_base_url: str = Field(
        default="http://localhost:5000", description="Base URL of the self-hosted OSRM instance."
    )
    osrm_timeout_seconds: float = Field(default=3.0, description="Timeout for OSRM HTTP calls, in seconds.")

    # --- SMS / OTP (MSG91 / Gupshup, DLT-compliant) ---
    sms_provider: str = Field(default="msg91", description="Active SMS provider: 'msg91' or 'gupshup'.")
    msg91_auth_key: Optional[str] = Field(default=None, description="MSG91 auth key.")
    msg91_otp_template_id: Optional[str] = Field(
        default=None, description="DLT-approved MSG91 template ID used for OTP delivery."
    )
    gupshup_api_key: Optional[str] = Field(default=None, description="Gupshup API key.")
    gupshup_source_number: Optional[str] = Field(
        default=None, description="Gupshup DLT-registered sender number."
    )

    # --- Email (SendGrid) ---
    sendgrid_api_key: Optional[str] = Field(default=None, description="SendGrid API key for email delivery.")
    sendgrid_from_email: str = Field(
        default="no-reply@cargolink.example", description="Verified SendGrid sender address."
    )

    # --- Monitoring ---
    sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN for error monitoring.")

    # --- Rate limiting ---
    otp_request_rate_limit: str = Field(
        default="5/minute",
        description="slowapi rate-limit string applied to /auth/otp/request, keyed per phone number.",
    )

    @model_validator(mode="after")
    def validate_production_requirements(self) -> "Settings":
        """
        Fails fast at startup -- not on first request -- if a production
        deployment is missing anything it genuinely cannot run without.
        Local/test/staging are intentionally lenient so the app boots with
        zero configuration during early sprints.
        """
        if self.environment == Environment.PRODUCTION:
            problems: list[str] = []
            if self.mock_repo:
                problems.append("MOCK_REPO must be false in production")
            if self.jwt_secret_key == "dev-insecure-secret-change-me":
                problems.append("JWT_SECRET_KEY must be overridden in production")
            if not self.database_url:
                problems.append("DATABASE_URL is required in production")
            if not self.s3_bucket_name:
                problems.append("S3_BUCKET_NAME is required in production")
            if problems:
                raise ValueError("Invalid production configuration: " + "; ".join(problems))
        return self


settings = Settings()
