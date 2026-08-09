"""Tests for InMemoryComplianceDocumentRepository (Task A.3, requirement 11)."""

import pytest

from app.core.enums import ComplianceDocType, DocumentStatus
from app.repositories.exceptions import NotFoundError

pytestmark = pytest.mark.asyncio


async def test_create_and_list_by_owner(compliance_document_repo):
    doc = await compliance_document_repo.create(
        owner_id="user-1", doc_type=ComplianceDocType.DRIVING_LICENSE, file_url="s3://bucket/dl.pdf"
    )

    assert doc.status == DocumentStatus.PENDING
    docs = await compliance_document_repo.list_by_owner("user-1")
    assert docs == [doc]


async def test_list_by_owner_empty_when_none(compliance_document_repo):
    docs = await compliance_document_repo.list_by_owner("user-1")

    assert docs == []


async def test_list_by_owner_only_returns_matching_owner(compliance_document_repo):
    await compliance_document_repo.create(
        owner_id="user-1", doc_type=ComplianceDocType.DRIVING_LICENSE, file_url="s3://a"
    )
    await compliance_document_repo.create(
        owner_id="vehicle-1", doc_type=ComplianceDocType.RC, file_url="s3://b"
    )

    docs = await compliance_document_repo.list_by_owner("user-1")

    assert len(docs) == 1
    assert docs[0].owner_id == "user-1"


async def test_update_status(compliance_document_repo):
    doc = await compliance_document_repo.create(
        owner_id="user-1", doc_type=ComplianceDocType.INSURANCE, file_url="s3://c"
    )

    updated = await compliance_document_repo.update_status(doc.id, DocumentStatus.VERIFIED)

    assert updated.status == DocumentStatus.VERIFIED


async def test_update_status_raises_not_found(compliance_document_repo):
    with pytest.raises(NotFoundError):
        await compliance_document_repo.update_status("no-such-id", DocumentStatus.VERIFIED)
