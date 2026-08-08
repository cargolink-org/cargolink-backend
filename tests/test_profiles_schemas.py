from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.profiles.schemas import ShipperProfileCreateRequest, TransporterProfileCreateRequest


def test_shipper_profile_gstin_is_optional():
    req = ShipperProfileCreateRequest(company_name="Acme Freight")
    assert req.gstin is None


def test_shipper_profile_accepts_valid_gstin():
    req = ShipperProfileCreateRequest(company_name="Acme Freight", gstin="22AAAAA0000A1Z5")
    assert req.gstin == "22AAAAA0000A1Z5"


def test_shipper_profile_rejects_malformed_gstin():
    with pytest.raises(ValidationError):
        ShipperProfileCreateRequest(company_name="Acme Freight", gstin="not-a-gstin")


def test_shipper_profile_requires_company_name():
    with pytest.raises(ValidationError):
        ShipperProfileCreateRequest(company_name="")


def test_transporter_profile_requires_license_no():
    with pytest.raises(ValidationError):
        TransporterProfileCreateRequest(license_no="")
    req = TransporterProfileCreateRequest(license_no="DL-1234567890")
    assert req.license_no == "DL-1234567890"
