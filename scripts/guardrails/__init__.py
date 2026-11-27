"""
DTEAM Architectural & Documentation Guardrails Package.

Provides deterministic, stdlib-only cross-seam verification across domain
models, ERD/SQL/DBML schemas, REST/SignalR contracts, Blazor/Razor UI
contracts, design tokens, SVG iconography, and requirements traceability.
"""

from __future__ import annotations

from .models import (
    AuditReport,
    AuditSummary,
    Finding,
    RuleSpec,
    SEVERITY_BLOCKER,
    SEVERITY_INFO,
    SEVERITY_ORDER,
    SEVERITY_WARNING,
)

__version__ = "0.1.0"

__all__ = [
    "AuditReport",
    "AuditSummary",
    "Finding",
    "RuleSpec",
    "SEVERITY_BLOCKER",
    "SEVERITY_INFO",
    "SEVERITY_ORDER",
    "SEVERITY_WARNING",
    "__version__",
]
