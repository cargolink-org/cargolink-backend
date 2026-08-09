"""
Shared enums for CargoLink.

These are consumed by BOTH layers of the codebase:
  - app/<domain>/schemas.py  (Task A.2 — API-facing Pydantic models)
  - app/repositories/models.py (Task A.3 — internal domain models)

Reconstruction note (Task A.3 session): this sandbox has no persisted state
from prior sessions (no network access to pull the real repo), so this file
is recreated here as a prerequisite for A.3. Values are inferred from the
technical specification and the source documentation's module descriptions
(§4.1, §4.5) where the original spec only sketched free-text fields
(e.g. `cargo_type TEXT`, `checkpoint_name TEXT`). Inference choices are
called out inline.
"""

from enum import Enum


class UserRole(str, Enum):
    SHIPPER = "shipper"
    TRANSPORTER = "transporter"
    ADMIN = "admin"


class CargoType(str, Enum):
    # Per smart-freight-matching-system-documentation.md §4.1 Shipper Portal.
    GENERAL = "general"
    FRAGILE = "fragile"
    HAZARDOUS = "hazardous"
    REFRIGERATED = "refrigerated"


class VehicleType(str, Enum):
    # Per §4.1 Transporter Portal: "mini-truck, container truck, trailer, etc."
    # OTHER added to cover the "etc." without an unbounded free-text field.
    MINI_TRUCK = "mini_truck"
    CONTAINER_TRUCK = "container_truck"
    TRAILER = "trailer"
    OTHER = "other"


class LoadStatus(str, Enum):
    # Inferred lifecycle consistent with the core flow in
    # smart-freight-matching-system-documentation.md §3 and the
    # accept/track/deliver flow used throughout the Execution Plan.
    POSTED = "posted"
    MATCHED = "matched"
    ACCEPTED = "accepted"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class LoadMatchStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class ComplianceDocType(str, Enum):
    # Per §4.1 Transporter Portal document uploads. Owner-type inference:
    # DRIVING_LICENSE implies a *user* (transporter) owner; RC / permits /
    # insurance imply a *vehicle* owner. Flagged again in
    # repository-interfaces.md for Kishor's schema review, since the `documents`
    # table in the technical spec only has a single `owner_id` column with no
    # owner-type discriminator.
    DRIVING_LICENSE = "driving_license"
    RC = "rc"  # Registration Certificate
    NATIONAL_PERMIT = "national_permit"
    STATE_PERMIT = "state_permit"
    INSURANCE = "insurance"


class ShipmentDocType(str, Enum):
    # Per §4.5(a) Document checklist/tracker.
    COMMERCIAL_INVOICE = "commercial_invoice"
    PACKING_LIST = "packing_list"
    BILL_OF_LADING = "bill_of_lading"
    AIRWAY_BILL = "airway_bill"
    CUSTOMS_CLEARANCE_CERTIFICATE = "customs_clearance_certificate"
    CERTIFICATE_OF_ORIGIN = "certificate_of_origin"


class DocumentStatus(str, Enum):
    # Shared by ComplianceDocument and ShipmentDocument per §4.5(a):
    # "Pending -> Uploaded -> Verified -> Cleared". REJECTED added per
    # F.1's "admin/manual review rejecting a document" edge case, which
    # needs a distinct terminal-ish state instead of resetting to PENDING.
    PENDING = "pending"
    UPLOADED = "uploaded"
    VERIFIED = "verified"
    CLEARED = "cleared"
    REJECTED = "rejected"


class CheckpointName(str, Enum):
    # Per §4.5(b): "origin warehouse -> port/border -> customs hold ->
    # cleared -> destination".
    ORIGIN_WAREHOUSE = "origin_warehouse"
    PORT_BORDER = "port_border"
    PORT_OR_BORDER = "port_border"
    CUSTOMS_HOLD = "customs_hold"
    CLEARED = "cleared"
    DESTINATION = "destination"


class CheckpointStatus(str, Enum):
    # Per-checkpoint status, distinct from CheckpointName (the "where"),
    # this is the "what happened there". Kept small and inferred from
    # ordinary logistics checkpoint semantics.
    PENDING = "pending"
    COMPLETE = "complete"
    REACHED = "reached"
    DELAYED = "delayed"


class NotificationType(str, Enum):
    # Per §4.7 Notifications: booking confirmation, pickup confirmation,
    # delay alert, delivery confirmation.
    BOOKING_CONFIRMATION = "booking_confirmation"
    PICKUP_CONFIRMATION = "pickup_confirmation"
    DELAY_ALERT = "delay_alert"
    DELIVERY_CONFIRMATION = "delivery_confirmation"
