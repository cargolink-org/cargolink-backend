"""
Tests for app/core/di_registrations.py (Task A.3, requirement 10 + the
"Testing Requirements" for register_all_repositories()).

Covers:
- register_all_repositories() makes every one of the 16 interfaces
  resolvable via di.get_repository(...).
- Confirms (does not re-implement — see A.1's di.py) that
  register_repository() refuses mock-only registration when
  MOCK_REPO=false, by asserting register_all_repositories() itself raises
  under that condition, since it calls register_repository() with no
  real_factory for every interface.
"""

import pytest

from app.core import di
from app.core.config import settings
from app.core.di_registrations import register_all_repositories
from app.repositories.interfaces.checkpoint_update import CheckpointUpdateRepository
from app.repositories.interfaces.compliance_document import ComplianceDocumentRepository
from app.repositories.interfaces.container import ContainerRepository
from app.repositories.interfaces.fare_quote import FareQuoteRepository
from app.repositories.interfaces.load import LoadRepository
from app.repositories.interfaces.load_match import LoadMatchRepository
from app.repositories.interfaces.location_ping import LocationPingRepository
from app.repositories.interfaces.notification import NotificationRepository
from app.repositories.interfaces.otp import OtpRepository
from app.repositories.interfaces.rating import RatingRepository
from app.repositories.interfaces.refresh_token import RefreshTokenRepository
from app.repositories.interfaces.shipment_document import ShipmentDocumentRepository
from app.repositories.interfaces.shipper_profile import ShipperProfileRepository
from app.repositories.interfaces.transporter_profile import TransporterProfileRepository
from app.repositories.interfaces.user import UserRepository
from app.repositories.interfaces.vehicle import VehicleRepository
from app.repositories.mock_impl.user import InMemoryUserRepository

pytestmark = pytest.mark.asyncio

ALL_INTERFACES = [
    UserRepository,
    OtpRepository,
    RefreshTokenRepository,
    ShipperProfileRepository,
    TransporterProfileRepository,
    ComplianceDocumentRepository,
    VehicleRepository,
    LoadRepository,
    LoadMatchRepository,
    FareQuoteRepository,
    LocationPingRepository,
    ShipmentDocumentRepository,
    CheckpointUpdateRepository,
    ContainerRepository,
    NotificationRepository,
    RatingRepository,
]


def test_all_sixteen_interfaces_registered():
    # Documents the A.3 count discrepancy noted in
    # shared/contracts/repository-interfaces.md: the task prose says "15"
    # but the design section enumerates (and this test registers) 16.
    assert len(ALL_INTERFACES) == 16

    register_all_repositories()

    for interface in ALL_INTERFACES:
        assert di.is_registered(interface), f"{interface!r} was not registered"


async def test_every_interface_resolves_to_a_repository_instance():
    register_all_repositories()

    for interface in ALL_INTERFACES:
        instance = di.get_repository(interface)
        assert instance is not None


async def test_resolved_user_repository_is_functional():
    register_all_repositories()

    repo = di.get_repository(UserRepository)
    assert isinstance(repo, InMemoryUserRepository)

    # Prove it's a live, usable instance, not just a registered factory.
    from app.core.enums import UserRole

    user = await repo.create(phone="+919876543210", role=UserRole.SHIPPER)
    fetched = await repo.get_by_id(user.id)
    assert fetched.id == user.id


def test_register_all_repositories_raises_when_mock_repo_false(monkeypatch):
    monkeypatch.setattr(settings, "MOCK_REPO", False)

    # Every registration in register_all_repositories() supplies only a
    # mock_factory, so with MOCK_REPO=false the very first
    # register_repository() call must raise — this is A.1's di.py
    # production guard, confirmed (not re-implemented) here per
    # requirement 10.
    with pytest.raises(RuntimeError):
        register_all_repositories()


def test_calling_register_all_repositories_twice_is_safe():
    register_all_repositories()
    register_all_repositories()  # must not raise (e.g. duplicate-key errors)

    for interface in ALL_INTERFACES:
        assert di.is_registered(interface)
