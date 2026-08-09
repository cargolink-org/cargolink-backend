"""
Tests for app/core/di.py (Task A.1), reconstructed as a prerequisite for
A.3 — see note in app/core/enums.py. A.3 does not modify di.py; these
tests just establish the reset_registry() pattern that
tests/repositories/conftest.py and tests/test_di_registrations.py build on.
"""

import pytest

from app.core import di
from app.core.config import settings


class _FakeInterface:
    pass


def test_register_and_get_returns_mock_instance():
    sentinel = object()
    di.register_repository(_FakeInterface, mock_factory=lambda: sentinel)

    assert di.get_repository(_FakeInterface) is sentinel


def test_get_repository_caches_singleton_instance():
    calls = {"count": 0}

    def factory():
        calls["count"] += 1
        return object()

    di.register_repository(_FakeInterface, mock_factory=factory)

    first = di.get_repository(_FakeInterface)
    second = di.get_repository(_FakeInterface)

    assert first is second
    assert calls["count"] == 1


def test_get_repository_unregistered_raises():
    with pytest.raises(di.RepositoryNotRegisteredError):
        di.get_repository(_FakeInterface)


def test_register_repository_refuses_mock_only_when_not_mock_repo(monkeypatch):
    monkeypatch.setattr(settings, "MOCK_REPO", False)

    with pytest.raises(RuntimeError):
        di.register_repository(_FakeInterface, mock_factory=lambda: object())


def test_register_repository_allows_mock_with_real_factory_when_not_mock_repo(monkeypatch):
    monkeypatch.setattr(settings, "MOCK_REPO", False)

    real_sentinel = object()
    di.register_repository(
        _FakeInterface,
        mock_factory=lambda: object(),
        real_factory=lambda: real_sentinel,
    )

    assert di.get_repository(_FakeInterface) is real_sentinel


def test_reset_registry_clears_registrations_and_cache():
    di.register_repository(_FakeInterface, mock_factory=lambda: object())
    di.get_repository(_FakeInterface)  # populate the instance cache

    di.reset_registry()

    assert not di.is_registered(_FakeInterface)
    with pytest.raises(di.RepositoryNotRegisteredError):
        di.get_repository(_FakeInterface)
