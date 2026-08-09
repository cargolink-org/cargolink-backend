"""
Repository DI registrations (Task A.3, requirement 7).

register_all_repositories() is called exactly once, at FastAPI startup
(see app/main.py's on_event("startup") handler) — never at import time,
so tests can freely call app.core.di.reset_registry() and then
register_all_repositories() again per test module without import-order
surprises.

NOTE on count: the task prompt's prose says "all 15 interfaces above" but
its own ENTITIES & REPOSITORY DESIGN section enumerates 16 named
repositories (including RefreshTokenRepository, itself flagged in the
prompt as "an A.3 addition — not explicitly named in the guide's entity
list"). All 16 are registered below; the discrepancy is called out here
rather than silently dropping one.

Every registration below provides ONLY a mock_factory — no real_factory.
This is intentional: real_factory additions are explicitly Kishor's
Sprint 5+ work (sqlalchemy_impl/), scheduled after the Data/Schema
Contract freeze (Week 4) and the real database becoming available
(Week 8). Until then, app/core/di.py's MOCK_REPO=false guard means this
function — and therefore the whole app — refuses to boot in a
production-configured environment, by design (see
tests/test_di_registrations.py).
"""

from app.core.di import register_repository
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

from app.repositories.mock_impl.checkpoint_update import InMemoryCheckpointUpdateRepository
from app.repositories.mock_impl.compliance_document import InMemoryComplianceDocumentRepository
from app.repositories.mock_impl.container import InMemoryContainerRepository
from app.repositories.mock_impl.fare_quote import InMemoryFareQuoteRepository
from app.repositories.mock_impl.load import InMemoryLoadRepository
from app.repositories.mock_impl.load_match import InMemoryLoadMatchRepository
from app.repositories.mock_impl.location_ping import InMemoryLocationPingRepository
from app.repositories.mock_impl.notification import InMemoryNotificationRepository
from app.repositories.mock_impl.otp import InMemoryOtpRepository
from app.repositories.mock_impl.rating import InMemoryRatingRepository
from app.repositories.mock_impl.refresh_token import InMemoryRefreshTokenRepository
from app.repositories.mock_impl.shipment_document import InMemoryShipmentDocumentRepository
from app.repositories.mock_impl.shipper_profile import InMemoryShipperProfileRepository
from app.repositories.mock_impl.transporter_profile import InMemoryTransporterProfileRepository
from app.repositories.mock_impl.user import InMemoryUserRepository
from app.repositories.mock_impl.vehicle import InMemoryVehicleRepository


def register_all_repositories() -> None:
    """Register every repository interface's mock factory with the DI
    container. Idempotent-ish: calling it twice re-registers (and, per
    app/core/di.py, drops any cached singleton instance for) every
    interface — tests rely on this after a reset_registry() call."""

    register_repository(UserRepository, mock_factory=InMemoryUserRepository)
    register_repository(OtpRepository, mock_factory=InMemoryOtpRepository)
    register_repository(RefreshTokenRepository, mock_factory=InMemoryRefreshTokenRepository)
    register_repository(ShipperProfileRepository, mock_factory=InMemoryShipperProfileRepository)
    register_repository(
        TransporterProfileRepository, mock_factory=InMemoryTransporterProfileRepository
    )
    register_repository(
        ComplianceDocumentRepository, mock_factory=InMemoryComplianceDocumentRepository
    )
    register_repository(VehicleRepository, mock_factory=InMemoryVehicleRepository)
    register_repository(LoadRepository, mock_factory=InMemoryLoadRepository)
    register_repository(LoadMatchRepository, mock_factory=InMemoryLoadMatchRepository)
    register_repository(FareQuoteRepository, mock_factory=InMemoryFareQuoteRepository)
    register_repository(LocationPingRepository, mock_factory=InMemoryLocationPingRepository)
    register_repository(
        ShipmentDocumentRepository, mock_factory=InMemoryShipmentDocumentRepository
    )
    register_repository(
        CheckpointUpdateRepository, mock_factory=InMemoryCheckpointUpdateRepository
    )
    register_repository(ContainerRepository, mock_factory=InMemoryContainerRepository)
    register_repository(NotificationRepository, mock_factory=InMemoryNotificationRepository)
    register_repository(RatingRepository, mock_factory=InMemoryRatingRepository)
