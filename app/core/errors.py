"""Shared error-response contract.

Mirrors the exact shape already produced by app/main.py's global exception
handler: { "error": { "code": ..., "message": ... } }. Every domain router
in this project references `ErrorResponse` (not a locally invented shape)
as the documented error response for 4xx/5xx statuses, per A.2 requirement 6.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(
        ...,
        description="Machine-readable error code (e.g. 'not_found', 'validation_error', 'rate_limited').",
        examples=["validation_error"],
    )
    message: str = Field(
        ...,
        description="Human-readable explanation of what went wrong, safe to display to an end user.",
        examples=["The requested load could not be found."],
    )


class ErrorResponse(BaseModel):
    """Standard error envelope returned by every endpoint in this API.

    Matches app/main.py's global exception handler exactly:
        { "error": { "code": "...", "message": "..." } }
    Do not introduce a second error shape anywhere in the contract.
    """

    error: ErrorDetail


# Reusable OpenAPI "responses" fragment. Every router in this project splats
# this into its @router.<verb>(..., responses=ERROR_RESPONSES) call so
# Swagger documents the standard error envelope on every endpoint without
# repeating the same boilerplate dict in each domain module.
ERROR_RESPONSES: dict[int | str, dict] = {
    400: {"model": ErrorResponse, "description": "Validation error."},
    401: {"model": ErrorResponse, "description": "Missing or invalid authentication."},
    403: {"model": ErrorResponse, "description": "Authenticated but not authorized for this action."},
    404: {"model": ErrorResponse, "description": "Resource not found."},
    409: {"model": ErrorResponse, "description": "Conflict with current resource state."},
    429: {"model": ErrorResponse, "description": "Rate limited."},
    500: {"model": ErrorResponse, "description": "Unexpected server error."},
}
