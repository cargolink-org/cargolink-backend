"""
Future home of the real async SQLAlchemy engine + session factory.

Task A.3 explicitly must not import this module and must not touch it —
persistence for every entity in this task is provided exclusively by
app/repositories/mock_impl/. This file stays inert until Kishor's
sqlalchemy_impl/ classes are wired in from Sprint 5 onward (Data/Schema
Contract freeze at Week 4, real DB available Week 8, swap begins Week 10).
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


_engine: Optional[AsyncEngine] = None
_session_factory: Optional[sessionmaker[AsyncSession]] = None


def get_engine() -> AsyncEngine:
    global _engine, _session_factory

    if _engine is not None:
        return _engine

    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    _engine = create_async_engine(settings.database_url, future=True)
    _session_factory = sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)
    return _engine


@asynccontextmanager
async def get_db_session():
    if settings.MOCK_REPO:
        raise RuntimeError(
            "get_db_session() should never be called while MOCK_REPO=true; "
            "business logic must depend on repository interfaces, not this "
            "module, until the Week 10 swap."
        )

    if _session_factory is None:
        get_engine()

    assert _session_factory is not None
    async with _session_factory() as session:
        yield session
