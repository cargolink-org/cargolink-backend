"""
Async SQLAlchemy engine/session wiring.

This module is intentionally inert when settings.mock_repo is True: no
engine is created and no connection is attempted, so the app can boot,
serve /docs, and run its full test suite entirely against in-memory
repositories with zero live database -- the explicit Sprint 1 requirement
(Task A.1, acceptance criteria).

Once mock_repo=false (from Sprint 5 onward, per the execution plan's
Backend <-> Database swap), the engine/session factory below is what
Kishor's real `sqlalchemy_impl/` repositories use for actual queries.
Business logic never imports this module directly -- only concrete
repository implementations do.
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker] = None


def get_engine() -> AsyncEngine:
    """
    Lazily creates the async engine on first real use.

    Only ever called from real repository implementations (never from
    business logic, never while mock_repo=true). Raises immediately with a
    clear message if DATABASE_URL isn't configured, rather than failing
    obscurely deep inside a query.
    """
    global _engine
    if _engine is None:
        if not settings.database_url:
            raise RuntimeError(
                "DATABASE_URL is not configured. This is expected while "
                "MOCK_REPO=true -- the real engine should never be "
                "requested in mock mode. If you're seeing this with "
                "MOCK_REPO=false, set DATABASE_URL in your environment."
            )
        _engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
        )
    return _engine


def get_session_factory() -> async_sessionmaker:
    """Lazily builds the session factory, bound to the lazily-created engine."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _session_factory


@asynccontextmanager
async def get_db_session() -> AsyncIterator[AsyncSession]:
    """
    Async context manager yielding a real DB session.

    Must only be entered when settings.mock_repo is False. Raises loudly
    if called in mock mode -- this should never happen, since business
    logic depends only on repository interfaces, never on a concrete DB
    session directly (per the architecture rule in the implementation
    guide's Section 4.1).
    """
    if settings.mock_repo:
        raise RuntimeError(
            "get_db_session() was called while MOCK_REPO=true. Business "
            "logic must depend on repository interfaces, never on a "
            "concrete DB session -- this indicates a layering violation."
        )
    factory = get_session_factory()
    async with factory() as session:
        yield session


async def dispose_engine() -> None:
    """Cleanly disposes of the engine on app shutdown, if one was ever created."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
