"""Async SQLAlchemy session factory — inert scaffold.

Treated as pre-existing per A.1 (not found in this sandbox, recreated
minimally). No engine/session is actually used by any endpoint yet. Real
wiring happens once Kishor's schema is frozen and the sqlalchemy_impl/
repositories exist (Sprint 5+). A.2 does not touch this file's behavior;
its presence is only assumed by app/core/di.py.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

from app.core.config import get_settings

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

try:
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
except ImportError:  # pragma: no cover - sqlalchemy not installed in this sandbox
    async_sessionmaker = None  # type: ignore[assignment]
    create_async_engine = None  # type: ignore[assignment]


_engine: "AsyncEngine | None" = None
_session_factory = None


def get_engine() -> "AsyncEngine | None":
    global _engine
    if _engine is None and create_async_engine is not None:
        _engine = create_async_engine(get_settings().database_url, echo=False)
    return _engine


def get_session_factory():
    global _session_factory
    if _session_factory is None and async_sessionmaker is not None:
        _session_factory = async_sessionmaker(get_engine(), expire_on_commit=False)
    return _session_factory


async def get_db_session() -> AsyncGenerator["AsyncSession", None]:  # pragma: no cover
    """FastAPI dependency — unused until real repositories exist (Sprint 5+)."""
    factory = get_session_factory()
    if factory is None:
        raise RuntimeError("SQLAlchemy is not installed / DB not configured yet.")
    async with factory() as session:
        yield session
