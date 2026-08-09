"""
Shared fixtures for the repository contract-test suite (Task A.3,
requirement 9).

Pattern: for each entity, a fixture named `<entity>_repo` is parametrized
over a dict of {implementation_name: factory_callable}. Today every dict
has exactly one entry ("mock" -> the InMemory* class). Once Kishor's
sqlalchemy_impl/ classes exist (Sprint 5+), a second entry ("real" ->
the SqlAlchemy* class, likely wrapped to run inside a per-test transaction
against a test database) gets added to the SAME dict below, and every
existing test function that consumes the fixture automatically runs
against both implementations with zero test-code duplication. This is the
single highest-leverage piece of A.3 for making the Week 10 mock-to-real
swap safe, per the task prompt's requirement 9 — it exists now even
though there's only one implementation to test today.
"""

from typing import Callable, Dict

import pytest

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

# --- Implementation registries, one per entity --------------------------
# Add a "real": <factory> entry to any of these dicts once Kishor's
# sqlalchemy_impl/ classes exist — no other change needed anywhere in
# this test suite.
_USER_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryUserRepository}
_OTP_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryOtpRepository}
_REFRESH_TOKEN_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryRefreshTokenRepository}
_SHIPPER_PROFILE_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryShipperProfileRepository}
_TRANSPORTER_PROFILE_REPO_IMPLS: Dict[str, Callable] = {
    "mock": InMemoryTransporterProfileRepository
}
_COMPLIANCE_DOCUMENT_REPO_IMPLS: Dict[str, Callable] = {
    "mock": InMemoryComplianceDocumentRepository
}
_VEHICLE_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryVehicleRepository}
_LOAD_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryLoadRepository}
_LOAD_MATCH_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryLoadMatchRepository}
_FARE_QUOTE_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryFareQuoteRepository}
_LOCATION_PING_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryLocationPingRepository}
_SHIPMENT_DOCUMENT_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryShipmentDocumentRepository}
_CHECKPOINT_UPDATE_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryCheckpointUpdateRepository}
_CONTAINER_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryContainerRepository}
_NOTIFICATION_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryNotificationRepository}
_RATING_REPO_IMPLS: Dict[str, Callable] = {"mock": InMemoryRatingRepository}


def _make_repo_fixture(impls: Dict[str, Callable]):
    """Build a pytest fixture parametrized over every registered
    implementation name. request.param is the implementation name
    ("mock" today, "mock"/"real" later), useful in test IDs when a
    failure needs to be traced to a specific implementation."""

    @pytest.fixture(params=list(impls.keys()))
    def _fixture(request):
        factory = impls[request.param]
        return factory()

    return _fixture


user_repo = _make_repo_fixture(_USER_REPO_IMPLS)
otp_repo = _make_repo_fixture(_OTP_REPO_IMPLS)
refresh_token_repo = _make_repo_fixture(_REFRESH_TOKEN_REPO_IMPLS)
shipper_profile_repo = _make_repo_fixture(_SHIPPER_PROFILE_REPO_IMPLS)
transporter_profile_repo = _make_repo_fixture(_TRANSPORTER_PROFILE_REPO_IMPLS)
compliance_document_repo = _make_repo_fixture(_COMPLIANCE_DOCUMENT_REPO_IMPLS)
vehicle_repo = _make_repo_fixture(_VEHICLE_REPO_IMPLS)
load_repo = _make_repo_fixture(_LOAD_REPO_IMPLS)
load_match_repo = _make_repo_fixture(_LOAD_MATCH_REPO_IMPLS)
fare_quote_repo = _make_repo_fixture(_FARE_QUOTE_REPO_IMPLS)
location_ping_repo = _make_repo_fixture(_LOCATION_PING_REPO_IMPLS)
shipment_document_repo = _make_repo_fixture(_SHIPMENT_DOCUMENT_REPO_IMPLS)
checkpoint_update_repo = _make_repo_fixture(_CHECKPOINT_UPDATE_REPO_IMPLS)
container_repo = _make_repo_fixture(_CONTAINER_REPO_IMPLS)
notification_repo = _make_repo_fixture(_NOTIFICATION_REPO_IMPLS)
rating_repo = _make_repo_fixture(_RATING_REPO_IMPLS)
