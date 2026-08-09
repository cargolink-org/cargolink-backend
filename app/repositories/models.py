"""
Internal domain models for the repository layer (Task A.3).

ARCHITECTURAL RULE (per the A.3 task prompt): these are NOT the same
objects as app/<domain>/schemas.py's API request/response models. API
schemas are what the HTTP layer speaks; these are the internal domain
representation and may carry fields the API must never expose verbatim
(e.g. OtpRecord.code, RefreshTokenRecord.token, User.password_hash).
Nothing in this file imports from any app/<domain>/schemas.py, and nothing
in app/<domain>/schemas.py should import from here — a mapping/translation
step belongs in each domain's service.py (Clusters B-H), not in this task.

Plain dataclasses were chosen over Pydantic BaseModel per the task
prompt's stated preference, and kept ORM-agnostic (ATB: no SQLAlchemy
Column/relationship, no Pydantic validators) — the whole point is that
these types must be identical whether the app is running against the
mock_impl/ or, from Sprint 5 onward, Kishor's sqlalchemy_impl/.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from app.core.enums import (
    CargoType,
    CheckpointName,
    CheckpointStatus,
    ComplianceDocType,
    DocumentStatus,
    LoadMatchStatus,
    LoadStatus,
    NotificationType,
    ShipmentDocType,
    UserRole,
    VehicleType,
)


def new_id() -> str:
    return str(uuid.uuid4())


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class GeoPoint:
    """Lightweight stand-in for the schema's PostGIS GEOGRAPHY(Point, 4326)
    columns (vehicles.current_location, loads.source/destination,
    location_pings.location). Kept as a plain (lat, lng) pair — no PostGIS
    dependency belongs in a mock/interface layer."""

    lat: float
    lng: float


@dataclass
class User:
    id: str
    role: UserRole
    phone: str
    name: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None  # nullable — OTP-only login is the primary flow
    created_at: datetime = field(default_factory=utcnow)


@dataclass
class OtpRecord:
    phone: str
    code: str
    expires_at: datetime
    attempts: int = 0


@dataclass
class RefreshTokenRecord:
    """A.3 addition (RefreshTokenRepository) — see the interface docstring
    for why this exists beyond the guide's originally named entity list."""

    token: str
    user_id: str
    family_id: str
    expires_at: datetime
    rotated: bool = False
    # Set True by invalidate_family() on reuse-detection — kept distinct
    # from `rotated` (a token can be neither rotated nor invalidated, or
    # rotated-but-not-invalidated during normal use, or both once its
    # whole family is torn down after a theft signal).
    invalidated: bool = False
    created_at: datetime = field(default_factory=utcnow)


@dataclass
class ShipperProfile:
    user_id: str
    company_name: Optional[str] = None
    gstin: Optional[str] = None


@dataclass
class TransporterProfile:
    user_id: str
    license_no: Optional[str] = None
    rating_avg: float = 0.0


@dataclass
class ComplianceDocument:
    """Table: `documents` in the technical spec — user- or vehicle-level
    verification documents (driving license, RC, permits, insurance).
    See ComplianceDocType's docstring for the owner_id inference flagged
    for Kishor's schema review."""

    id: str
    owner_id: str
    doc_type: ComplianceDocType
    file_url: str
    status: DocumentStatus = DocumentStatus.PENDING
    created_at: datetime = field(default_factory=utcnow)


@dataclass
class Vehicle:
    id: str
    transporter_id: str
    type: VehicleType
    capacity_kg: float
    capacity_volume: Optional[float] = None
    route_pref: Optional[str] = None
    current_location: Optional[GeoPoint] = None
    last_ping_at: Optional[datetime] = None
    is_available: bool = True


@dataclass
class Load:
    id: str
    shipper_id: str
    weight: float
    cargo_type: CargoType
    source: GeoPoint
    destination: GeoPoint
    deadline: datetime
    status: LoadStatus = LoadStatus.POSTED
    created_at: datetime = field(default_factory=utcnow)


@dataclass
class LoadMatch:
    id: str
    load_id: str
    vehicle_id: str
    status: LoadMatchStatus
    match_score: Optional[float] = None
    matched_at: datetime = field(default_factory=utcnow)


@dataclass
class FareQuote:
    id: str
    load_id: str
    base_fare: float
    distance_cost: float
    surcharge: float
    total: float


@dataclass
class LocationPing:
    id: str
    vehicle_id: str
    lat: float
    lng: float
    ts: datetime = field(default_factory=utcnow)


@dataclass
class ShipmentDocument:
    """Table: `shipment_documents` — per-load import/export checklist item.
    Natural key is (load_id, doc_type); no surrogate id in the technical
    spec's schema excerpt for this table's *usage* pattern (always read
    per-load, per-type), so mock/list operations key off the pair."""

    load_id: str
    doc_type: ShipmentDocType
    file_url: Optional[str] = None
    status: DocumentStatus = DocumentStatus.PENDING


@dataclass
class CheckpointUpdate:
    id: str
    load_id: str
    checkpoint_name: CheckpointName
    status: CheckpointStatus
    posted_by: str  # audit trail — security checklist requirement
    out_of_sequence: bool = False
    timestamp: datetime = field(default_factory=utcnow)


@dataclass
class Container:
    """Natural key is load_id (one container record per load; a load with
    no container data is purely road freight, per F.3's edge case)."""

    load_id: str
    container_no: Optional[str] = None
    vessel_or_flight: Optional[str] = None
    port_of_loading: Optional[str] = None
    port_of_discharge: Optional[str] = None


@dataclass
class Notification:
    id: str
    user_id: str
    type: NotificationType
    message: str
    read: bool = False
    dedupe_key: Optional[str] = None  # G.1 idempotency
    sent_at: datetime = field(default_factory=utcnow)


@dataclass
class Rating:
    id: str
    load_id: str
    rater_id: str
    ratee_id: str
    score: int
    comment: Optional[str] = None
