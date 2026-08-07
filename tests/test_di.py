"""
Tests for the DI container scaffolding introduced in Task A.1.

Full repository registrations arrive in Task A.3 onward; this suite only
proves the registry mechanism itself -- registration, resolution, and the
mock<->real switch -- works correctly in isolation.
"""
import pytest

from app.core import di


class _FakeRepo:
    """Stand-in interface/implementation pair used only by these tests."""

    def __init__(self, label: str) -> None:
        self.label = label


@pytest.fixture(autouse=True)
def _clean_registry():
    di.reset_registry()
    yield
    di.reset_registry()


def test_register_and_resolve_mock_repository(monkeypatch) -> None:
    monkeypatch.setattr(di.settings, "mock_repo", True)
    di.register_repository(_FakeRepo, mock_factory=lambda: _FakeRepo("mock"))

    provider = di.get_repository(_FakeRepo)
    assert provider().label == "mock"


def test_register_and_resolve_real_repository(monkeypatch) -> None:
    monkeypatch.setattr(di.settings, "mock_repo", False)
    di.register_repository(
        _FakeRepo,
        mock_factory=lambda: _FakeRepo("mock"),
        real_factory=lambda: _FakeRepo("real"),
    )

    provider = di.get_repository(_FakeRepo)
    assert provider().label == "real"


def test_real_mode_without_real_factory_raises_clearly(monkeypatch) -> None:
    monkeypatch.setattr(di.settings, "mock_repo", False)
    with pytest.raises(RuntimeError, match="no real implementation is registered"):
        di.register_repository(_FakeRepo, mock_factory=lambda: _FakeRepo("mock"))


def test_unregistered_interface_raises_clear_error() -> None:
    provider = di.get_repository(_FakeRepo)
    with pytest.raises(RuntimeError, match="No repository registered"):
        provider()


def test_each_call_produces_a_fresh_instance_from_the_factory(monkeypatch) -> None:
    monkeypatch.setattr(di.settings, "mock_repo", True)
    di.register_repository(_FakeRepo, mock_factory=lambda: _FakeRepo("mock"))

    provider = di.get_repository(_FakeRepo)
    first, second = provider(), provider()
    assert first is not second
    assert first.label == second.label == "mock"
