"""
Dependency-injection wiring for CargoLink repositories.

This module defines *the mechanism* by which business logic modules
receive a repository instance without ever importing a concrete
implementation (`mock_impl/` or, later, `sqlalchemy_impl/`) directly.
Task A.1 only establishes this container + FastAPI-provider pattern;
concrete interface registrations are added incrementally starting with
Task A.3 (Users) and continuing through every later cluster.

Why this exists: it's what makes "swap MOCK_REPO=false" a one-line
config change instead of a rewrite. A registered interface resolves to
whichever factory (mock or real) is active for the current settings,
decided once, at registration time -- not scattered as `if mock_repo:
... else: ...` checks throughout business logic.

Usage (once A.3 registers real interfaces):
    # at startup, e.g. in app/core/di_registrations.py
    register_repository(
        LoadRepository,
        mock_factory=lambda: InMemoryLoadRepository(),
        real_factory=lambda: SqlAlchemyLoadRepository(),
    )

    # in a router
    @router.get("/loads/{id}")
    async def get_load(
        repo: LoadRepository = Depends(get_repository(LoadRepository)),
    ):
        ...
"""
from typing import Any, Callable, Dict, Optional, Type, TypeVar

from app.core.config import settings

T = TypeVar("T")

# Maps: interface type -> zero-arg factory producing the currently-active implementation.
_registry: Dict[Type[Any], Callable[[], Any]] = {}


def register_repository(
    interface: Type[T],
    mock_factory: Callable[[], T],
    real_factory: Optional[Callable[[], T]] = None,
) -> None:
    """
    Registers the mock (and, once it exists, real) factory for a
    repository interface. The active factory is selected immediately,
    based on the current `settings.mock_repo` value.

    Raises if MOCK_REPO=false but no real implementation has been
    registered yet -- this is expected and safe *before* Sprint 5 (real
    implementations land incrementally starting at the Week 10 swap); it
    is a genuine misconfiguration in production.
    """
    if settings.mock_repo:
        _registry[interface] = mock_factory
        return

    if real_factory is None:
        raise RuntimeError(
            f"MOCK_REPO=false but no real implementation is registered "
            f"for {interface.__name__} yet. Real (SQLAlchemy-backed) "
            f"implementations land incrementally starting Sprint 5 -- "
            f"if you're hitting this before then, keep MOCK_REPO=true."
        )
    _registry[interface] = real_factory


def get_repository(interface: Type[T]) -> Callable[[], T]:
    """
    Returns a zero-arg callable suitable for use directly as a FastAPI
    `Depends()` target, resolving to whichever implementation is
    currently registered for `interface`.
    """

    def _provide() -> T:
        try:
            factory = _registry[interface]
        except KeyError as exc:
            raise RuntimeError(
                f"No repository registered for {interface.__name__}. "
                f"Did app startup call register_repository() for it? "
                f"(Registrations are added per-entity starting Task A.3.)"
            ) from exc
        return factory()

    return _provide


def reset_registry() -> None:
    """Test-only helper: clears all registrations between test runs/modules."""
    _registry.clear()
