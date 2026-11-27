"""
Deterministic JSON reporter for CI pipelines and automated tooling.
"""

from __future__ import annotations

import json

from ..models import AuditReport


def render_json(report: AuditReport) -> str:
    """Serialize an `AuditReport` into pretty-printed UTF-8 JSON."""
    return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
