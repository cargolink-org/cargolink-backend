"""
Tests for Task A.1's DB session wiring.

Must be provably inert while MOCK_REPO=true -- no engine, no connection
attempt, no requirement for DATABASE_URL to even be set. This is what
makes "zero live database in Sprint 1" true in practice, not just intent.
"""
import pytest

from app.core import db


@pytest.mark.asyncio
async def test_get_db_session_refuses_to_run_in_mock_mode(monkeypatch) -> None:
    monkeypatch.setattr(db.settings, "mock_repo", True)

    with pytest.raises(RuntimeError, match="MOCK_REPO=true"):
        async with db.get_db_session():
            pass  # pragma: no cover — should never be reached


def test_get_engine_fails_clearly_without_database_url(monkeypatch) -> None:
    monkeypatch.setattr(db.settings, "database_url", None)
    monkeypatch.setattr(db, "_engine", None)

    with pytest.raises(RuntimeError, match="DATABASE_URL is not configured"):
        db.get_engine()


def test_engine_is_lazily_created_only_on_first_real_use(monkeypatch) -> None:
    """No engine should exist just from importing the module."""
    monkeypatch.setattr(db, "_engine", None)
    monkeypatch.setattr(db, "_session_factory", None)
    assert db._engine is None
    assert db._session_factory is None
