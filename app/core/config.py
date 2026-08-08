"""Application settings — Pydantic v2 `BaseSettings`.

Scope note: this module is treated by Task A.2 as pre-existing (per the
task's context block, app/core/config.py already exists from A.1). It was
not found in this sandbox, so a minimal version matching the described
shape was recreated here to give A.2 something to build on top of. A.2
does not wire it into any endpoint — that starts in A.3.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    mock_repo: bool = True

    database_url: str = "postgresql+asyncpg://cargolink:cargolink@localhost:5432/cargolink"

    jwt_secret: str = "change-me"
    jwt_access_ttl_minutes: int = 15
    jwt_refresh_ttl_days: int = 30

    aws_s3_bucket: str = ""
    aws_region: str = "ap-south-1"

    osrm_base_url: str = "http://localhost:5000"

    msg91_api_key: str = ""
    gupshup_api_key: str = ""
    sendgrid_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
