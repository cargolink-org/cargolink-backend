"""
auth — FastAPI router stub (Task A.2).

Reconstructed here as a prerequisite for Task A.3 — see the note at the
top of app/core/enums.py. Every route below is an intentional stub raising
HTTP 501 until this domain's business-logic cluster is implemented; Task
A.3 must NOT change this file (per its "DO NOT" list) beyond this initial
recreation.

Endpoints (technical spec Sec. 5): POST /auth/otp/request, POST /auth/otp/verify, POST /auth/refresh
"""

from fastapi import APIRouter, HTTPException

from app.core.errors import ERROR_RESPONSES

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/_stub", responses=ERROR_RESPONSES)
async def auth_stub():
    """Placeholder route — replaced by real endpoints as this domain's
    business logic (see Dinesh-Backend-Implementation-Guide.md, Clusters
    B-H) is implemented."""
    raise HTTPException(status_code=501, detail={"error": {"code": "not_implemented", "message": "auth endpoints not implemented yet"}})
