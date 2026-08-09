"""
Dependency-injection container (Task A.1), reconstructed here as a
prerequisite for A.3 — see note in app/core/enums.py. Its public contract
(register_repository / get_repository / reset_registry, and the
MOCK_REPO=false production guard) is exactly what Task A.3's prompt
describes and depends on; A.3 does not change this mechanism, it only
calls register_repository() for the first time, for every entity, via the
new app/core/di_registrations.py.

Design:
- `register_repository` stores a (mock_factory, real_factory) pair per
  interface. It refuses to register a mock-only entry when
  settings.MOCK_REPO is False, since that would silently let mocks leak
  into a production-configured environment.
- `get_repository` resolves and *caches* a singleton instance per
  interface for the lifetime of the process (so in-memory mock state is
  actually shared across requests within one app run, not reset on every
  call — the mocks themselves stay instance-scoped per requirement 3 of
  A.3, but the DI container is what gives that instance a stable home).
- `reset_registry` clears both the registration table and the instance
  cache. Tests call this between test modules (see tests/test_di.py and
  tests/repositories/conftest.py) to get fresh, isolated repository
  instances without import-order surprises.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Type

from app.core.config import settings


@dataclass
class _RegistryEntry:
    mock_factory: Callable[[], Any]
    real_factory: Optional[Callable[[], Any]]


_registry: Dict[Type, _RegistryEntry] = {}
_instances: Dict[Type, Any] = {}


class RepositoryNotRegisteredError(LookupError):
    """Raised by get_repository() when no factory was registered for the interface."""


def register_repository(
    interface: Type,
    mock_factory: Callable[[], Any],
    real_factory: Optional[Callable[[], Any]] = None,
) -> None:
    """
    Register the mock (and, later, real) factory for a repository interface.

    Raises RuntimeError if settings.MOCK_REPO is False and no real_factory
    is provided — production must never silently fall back to an
    in-memory mock. This check exists in A.1 and is intentionally not
    re-implemented or relaxed by A.3; A.3's test suite only *confirms* it
    (see tests/test_di_registrations.py).
    """
    if not settings.MOCK_REPO and real_factory is None:
        raise RuntimeError(
            f"Refusing to register {interface!r} with only a mock factory "
            f"while MOCK_REPO=false. A real_factory is required outside "
            f"local/test environments."
        )
    _registry[interface] = _RegistryEntry(mock_factory=mock_factory, real_factory=real_factory)
    # Drop any cached instance from a previous registration of this interface
    # (relevant in tests, where the same interface may be re-registered
    # across test modules after a reset_registry() call).
    _instances.pop(interface, None)


def get_repository(interface: Type) -> Any:
    """
    Resolve a repository instance for the given interface.

    Returns a process-lifetime-cached singleton: the first call constructs
    the instance (mock or real, per settings.MOCK_REPO) and every
    subsequent call for the same interface returns that same instance, so
    in-memory mock state persists across requests within one run.
    """
    if interface in _instances:
        return _instances[interface]

    entry = _registry.get(interface)
    if entry is None:
        raise RepositoryNotRegisteredError(
            f"No repository registered for {interface!r}. Did you call "
            f"register_all_repositories() (app/core/di_registrations.py) "
            f"at startup, or reset_registry() without re-registering in a test?"
        )

    if settings.MOCK_REPO:
        instance = entry.mock_factory()
    else:
        if entry.real_factory is None:
            # Defensive: register_repository() should have already refused
            # this combination, but guard here too in case settings.MOCK_REPO
            # flips after registration (e.g. a test mutates settings directly).
            raise RuntimeError(
                f"{interface!r} has no real_factory registered and "
                f"MOCK_REPO=false — cannot resolve a repository instance."
            )
        instance = entry.real_factory()

    _instances[interface] = instance
    return instance


def reset_registry() -> None:
    """Clear all registrations and cached instances. Test-only utility."""
    _registry.clear()
    _instances.clear()


def is_registered(interface: Type) -> bool:
    return interface in _registry
