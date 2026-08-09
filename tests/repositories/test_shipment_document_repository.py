"""Tests for InMemoryShipmentDocumentRepository (Task A.3, requirement 11)."""

import pytest

from app.core.enums import DocumentStatus, ShipmentDocType
from app.repositories.exceptions import NotFoundError

pytestmark = pytest.mark.asyncio


async def test_list_by_load_empty_when_none(shipment_document_repo):
    docs = await shipment_document_repo.list_by_load("load-1")

    assert docs == []


async def test_upsert_and_list_by_load(shipment_document_repo):
    doc = await shipment_document_repo.upsert(
        load_id="load-1",
        doc_type=ShipmentDocType.COMMERCIAL_INVOICE,
        file_url="s3://invoice.pdf",
        status=DocumentStatus.UPLOADED,
    )

    docs = await shipment_document_repo.list_by_load("load-1")

    assert docs == [doc]


async def test_list_by_load_only_returns_matching_load(shipment_document_repo):
    await shipment_document_repo.upsert(
        load_id="load-1", doc_type=ShipmentDocType.PACKING_LIST,
        file_url="s3://a", status=DocumentStatus.UPLOADED,
    )
    await shipment_document_repo.upsert(
        load_id="load-2", doc_type=ShipmentDocType.PACKING_LIST,
        file_url="s3://b", status=DocumentStatus.UPLOADED,
    )

    docs = await shipment_document_repo.list_by_load("load-1")

    assert len(docs) == 1
    assert docs[0].load_id == "load-1"


async def test_upsert_updates_existing_row_for_same_key(shipment_document_repo):
    await shipment_document_repo.upsert(
        load_id="load-1", doc_type=ShipmentDocType.BILL_OF_LADING,
        file_url="s3://v1.pdf", status=DocumentStatus.UPLOADED,
    )
    await shipment_document_repo.upsert(
        load_id="load-1", doc_type=ShipmentDocType.BILL_OF_LADING,
        file_url="s3://v2.pdf", status=DocumentStatus.VERIFIED,
    )

    docs = await shipment_document_repo.list_by_load("load-1")

    assert len(docs) == 1  # composite key (load_id, doc_type) — no duplicate row
    assert docs[0].file_url == "s3://v2.pdf"
    assert docs[0].status == DocumentStatus.VERIFIED


async def test_update_status_raises_not_found_when_no_row_yet(shipment_document_repo):
    with pytest.raises(NotFoundError):
        await shipment_document_repo.update_status(
            "load-1", ShipmentDocType.CERTIFICATE_OF_ORIGIN, DocumentStatus.VERIFIED
        )


async def test_update_status_transitions_existing_row(shipment_document_repo):
    await shipment_document_repo.upsert(
        load_id="load-1", doc_type=ShipmentDocType.AIRWAY_BILL,
        file_url="s3://awb.pdf", status=DocumentStatus.UPLOADED,
    )

    updated = await shipment_document_repo.update_status(
        "load-1", ShipmentDocType.AIRWAY_BILL, DocumentStatus.CLEARED
    )

    assert updated.status == DocumentStatus.CLEARED
