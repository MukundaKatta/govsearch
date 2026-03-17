"""Government document type definitions."""

from enum import Enum


class DocumentType(str, Enum):
    """Classification of government document types."""

    LEGISLATION = "legislation"
    REGULATION = "regulation"
    COURT_RULING = "court_ruling"
    EXECUTIVE_ORDER = "executive_order"
    BUDGET = "budget"
    REPORT = "report"

    @property
    def display_name(self) -> str:
        return self.value.replace("_", " ").title()

    @classmethod
    def from_string(cls, value: str) -> "DocumentType":
        """Parse a document type from a flexible string input."""
        normalized = value.lower().strip().replace(" ", "_").replace("-", "_")
        try:
            return cls(normalized)
        except ValueError:
            for member in cls:
                if normalized in member.value or member.value in normalized:
                    return member
            raise ValueError(
                f"Unknown document type: '{value}'. "
                f"Valid types: {', '.join(m.value for m in cls)}"
            )


class Jurisdiction(str, Enum):
    """Jurisdiction levels for government documents."""

    FEDERAL = "federal"
    STATE = "state"
    LOCAL = "local"
    INTERNATIONAL = "international"


class DocumentStatus(str, Enum):
    """Lifecycle status of a government document."""

    DRAFT = "draft"
    PROPOSED = "proposed"
    ACTIVE = "active"
    AMENDED = "amended"
    REPEALED = "repealed"
    SUPERSEDED = "superseded"
    EXPIRED = "expired"
