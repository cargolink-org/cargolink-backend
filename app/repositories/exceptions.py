"""
Repository-layer exceptions (Task A.3, requirement 4).

Exactly two exceptions exist here on purpose: business logic (Clusters
B-H) must be able to catch one consistent pair regardless of which
repository implementation is active (mock today, Kishor's
sqlalchemy_impl/ from Sprint 5+), so mock implementations never raise a
bare KeyError/ValueError for these conditions.
"""


class NotFoundError(Exception):
    """Raised when a lookup by id/key finds no matching record."""


class ConflictError(Exception):
    """Raised when an operation would violate a uniqueness/state
    invariant (duplicate phone, duplicate rating triple, a vehicle
    double-booked across two active matches, etc.)."""
