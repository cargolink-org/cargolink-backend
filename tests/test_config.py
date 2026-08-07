"""
Tests for Task A.1's configuration module.

Local/dev/test defaults must let the app boot with zero configured
secrets. Production configuration gaps must fail fast and loudly at
Settings construction time, not obscurely on first request.
"""
import pytest
from pydantic import ValidationError

from app.core.config import Environment, Settings


def test_local_defaults_require_no_env_vars() -> None:
    settings = Settings(_env_file=None)
    assert settings.environment == Environment.LOCAL
    assert settings.mock_repo is True
    assert settings.database_url is None
    assert settings.s3_bucket_name is None


def test_production_without_required_config_fails_fast() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(_env_file=None, environment=Environment.PRODUCTION)

    message = str(exc_info.value)
    assert "MOCK_REPO must be false in production" in message
    assert "JWT_SECRET_KEY must be overridden in production" in message
    assert "DATABASE_URL is required in production" in message
    assert "S3_BUCKET_NAME is required in production" in message


def test_production_with_mock_repo_still_enabled_fails() -> None:
    with pytest.raises(ValidationError, match="MOCK_REPO must be false"):
        Settings(
            _env_file=None,
            environment=Environment.PRODUCTION,
            mock_repo=True,
            jwt_secret_key="a-real-production-secret",
            database_url="postgresql+asyncpg://user:pass@host/db",
            s3_bucket_name="cargolink-prod-docs",
        )


def test_production_with_full_config_succeeds() -> None:
    settings = Settings(
        _env_file=None,
        environment=Environment.PRODUCTION,
        mock_repo=False,
        jwt_secret_key="a-real-production-secret",
        database_url="postgresql+asyncpg://user:pass@host/db",
        s3_bucket_name="cargolink-prod-docs",
    )
    assert settings.environment == Environment.PRODUCTION
    assert settings.mock_repo is False


def test_staging_is_lenient_like_local() -> None:
    """Staging isn't held to production's strict bar in this task's scope."""
    settings = Settings(_env_file=None, environment=Environment.STAGING)
    assert settings.mock_repo is True  # default still applies; not force-validated
