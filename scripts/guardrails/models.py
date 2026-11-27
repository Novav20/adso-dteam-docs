"""
Core data models for guardrail findings, rule specifications, and audit reports.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

SEVERITY_BLOCKER = "BLOCKER"
SEVERITY_WARNING = "WARNING"
SEVERITY_INFO = "INFO"

SEVERITY_ORDER: dict[str, int] = {
    SEVERITY_BLOCKER: 0,
    SEVERITY_WARNING: 1,
    SEVERITY_INFO: 2,
}


@dataclass(frozen=True, slots=True)
class Finding:
    """Single deterministic verification finding emitted by a guardrail rule."""

    rule_id: str
    severity: str
    scope: str
    file: str
    line: int | None
    message: str
    remediation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class RuleSpec:
    """Metadata specification for a guardrail rule (`GRD-01`..`GRD-21`)."""

    rule_id: str
    name: str
    default_severity: str
    scopes: tuple[str, ...]
    description: str
    implemented: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "default_severity": self.default_severity,
            "scopes": list(self.scopes),
            "description": self.description,
            "implemented": self.implemented,
        }


@dataclass(frozen=True, slots=True)
class AuditSummary:
    """Aggregate counts and verdict for an audit execution."""

    total: int
    blocker: int
    warning: int
    info: int
    strict_mode: bool
    passed: bool
    files_scanned: int = 0
    rules_evaluated: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AuditReport:
    """Complete result bundle passed to console, JSON, and Markdown reporters."""

    root: str
    scope: str
    evaluated_rules: tuple[RuleSpec, ...]
    findings: list[Finding] = field(default_factory=list)
    files_scanned: int = 0
    strict_mode: bool = False
    target_files: tuple[str, ...] = ()

    @property
    def summary(self) -> AuditSummary:
        blocker = sum(1 for f in self.findings if f.severity == SEVERITY_BLOCKER)
        warning = sum(1 for f in self.findings if f.severity == SEVERITY_WARNING)
        info = sum(1 for f in self.findings if f.severity == SEVERITY_INFO)
        passed = blocker == 0 and (not self.strict_mode or warning == 0)
        return AuditSummary(
            total=len(self.findings),
            blocker=blocker,
            warning=warning,
            info=info,
            strict_mode=self.strict_mode,
            passed=passed,
            files_scanned=self.files_scanned,
            rules_evaluated=len(self.evaluated_rules),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "root": self.root,
            "scope": self.scope,
            "target_files": list(self.target_files),
            "summary": self.summary.to_dict(),
            "rules_evaluated": [r.to_dict() for r in self.evaluated_rules],
            "findings": [f.to_dict() for f in self.findings],
        }


RULE_SPECS: tuple[RuleSpec, ...] = (
    RuleSpec(
        rule_id="GRD-01",
        name="Ubiquitous Language & Dimension-Agnostic Purity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("ul", "seam1", "uc"),
        description=(
            "Verifies DT-UL-DOC-001 consistency and detects rendering-coupled 2D/3D/SVG/canvas "
            "or infrastructure/UI bleed inside domain and use-case specifications."
        ),
    ),
    RuleSpec(
        rule_id="GRD-02",
        name="Domain Model & State Machine Coherence",
        default_severity=SEVERITY_BLOCKER,
        scopes=("seam1", "erd", "uc"),
        description=(
            "Cross-checks DT-DM-DOC-001 entities and DT-DM-DOC-002 state transitions against "
            "ERD tables and use-case preconditions/postconditions."
        ),
    ),
    RuleSpec(
        rule_id="GRD-03",
        name="Controlled Vocabulary & Enum Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("seam1", "erd", "ui"),
        description=(
            "Verifies 1:1 parity between DT-DM-DOC-001 §4 controlled vocabularies, PostgreSQL "
            "CHECK constraints in DT-ERD-001.sql, and C# enum definitions across SCR/CTR specs."
        ),
    ),
    RuleSpec(
        rule_id="GRD-04",
        name="ERD Three-Way Schema Parity (SQL / DBML / Markdown)",
        default_severity=SEVERITY_BLOCKER,
        scopes=("erd", "seam2"),
        description=(
            "Verifies structural parity across DT-ERD-DOC-001.md §§3-4, DT-ERD-001.sql, and "
            "DT-ERD-001.dbml for schemas, tables, columns, nullability, types, FKs, and indexes."
        ),
    ),
    RuleSpec(
        rule_id="GRD-05",
        name="PostgreSQL DDL Temporal, PK & Concurrency Conventions",
        default_severity=SEVERITY_BLOCKER,
        scopes=("erd", "seam2"),
        description=(
            "Enforces TIMESTAMPTZ for all timestamps, UUIDv7 PK defaults, explicit FK referential "
            "actions, GIN jsonb_path_ops indexes, and partial unique active-slot indexes."
        ),
    ),
    RuleSpec(
        rule_id="GRD-06",
        name="WORM & Append-Only Table Governance",
        default_severity=SEVERITY_BLOCKER,
        scopes=("erd", "seam2", "seam3"),
        description=(
            "Validates append-only immutability, RLS/REVOKE protections, partitioning/hypertable "
            "setup, and ADR-003 SHA-256 chain hash consistency on WORM tables."
        ),
    ),
    RuleSpec(
        rule_id="GRD-07",
        name="Application Layer Purity & Cross-DbContext Unit of Work",
        default_severity=SEVERITY_WARNING,
        scopes=("seam2", "seam3"),
        description=(
            "Audits architectural port ownership, shared DbTransaction boundaries across "
            "DbContexts (DT-ARQ-DB-DOC-001), and ADR-010 slot/asset separation."
        ),
    ),
    RuleSpec(
        rule_id="GRD-08",
        name="REST API Catalog, Idempotency & Optimistic Concurrency Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("seam3",),
        description=(
            "Cross-checks /api/v1/... endpoints in SCR-*.md against DT-ARQ-CMP-DOC-001 §6, "
            "verifying X-Idempotency-Key on mutations and If-Match/uint ConcurrencyToken."
        ),
    ),
    RuleSpec(
        rule_id="GRD-09",
        name="SignalR Hub & Real-Time Event Contract Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("seam3", "seam4"),
        description=(
            "Cross-checks /hubs/* endpoints, typed client interfaces, event method signatures, "
            "and payload DTO fields against DT-ARQ-CMP-DOC-001 §5."
        ),
    ),
    RuleSpec(
        rule_id="GRD-10",
        name="Numeric Precision Boundary (decimal vs Viewport double)",
        default_severity=SEVERITY_BLOCKER,
        scopes=("seam3", "seam4", "ui"),
        description=(
            "Enforces C# decimal for operational, telemetry, financial, and engineering quantities; "
            "restricts double strictly to non-persisted spatial viewport/zoom coordinates."
        ),
    ),
    RuleSpec(
        rule_id="GRD-11",
        name="Shared UI Contracts & DRY Screen Specification Guard",
        default_severity=SEVERITY_BLOCKER,
        scopes=("seam4", "ui"),
        description=(
            "Verifies DT-UI-CTR-001.md SSoT compliance and prevents inline duplication of shared "
            "lookup DTOs, shared Razor shell/form components, or DT-DM-DOC-001 §4 enums in SCR-*.md."
        ),
    ),
    RuleSpec(
        rule_id="GRD-12",
        name="C# & Razor Contract Hygiene & Cross-Screen Consistency",
        default_severity=SEVERITY_BLOCKER,
        scopes=("seam4", "ui"),
        description=(
            "Prohibits DateTime, ComponentBase, [Inject], namespaces, and mutable private fields in "
            "§7 contracts while checking DTO property name/type/required/nullable parity across screens."
        ),
    ),
    RuleSpec(
        rule_id="GRD-13",
        name="Design Token Coverage & CSS Hygiene",
        default_severity=SEVERITY_BLOCKER,
        scopes=("ui", "tokens"),
        description=(
            "Validates all referenced --dt-* tokens against ui-ux/assets/tokens.css (light & dark), "
            "prevents duplicate token keys, token-literal shadowing, raw hex colors, and raw CSS in prose."
        ),
    ),
    RuleSpec(
        rule_id="GRD-14",
        name="SVG Iconography & Spatial Contract Integrity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("ui", "tokens"),
        description=(
            "Validates that every #icon-* reference across SCR-*.md, DT-UI-DS-DOC-001, and UI "
            "prototypes resolves to a symbol in ui-ux/assets/icons.svg and aligns with DT-UI-SVG-DOC-001."
        ),
    ),
    RuleSpec(
        rule_id="GRD-15",
        name="Screen Specification Structure, ISA-101 & Language Policy",
        default_severity=SEVERITY_BLOCKER,
        scopes=("ui",),
        description=(
            "Checks SCR-*.md frontmatter keys, 9 canonical sections and §7.1-§7.3 order, §8 "
            "responsive tiers, ISA-101 L1-L4 bounds, zero Unicode emojis, and 100% Technical English."
        ),
    ),
    RuleSpec(
        rule_id="GRD-16",
        name="UI Prototype Asset & DOM Copy Purity",
        default_severity=SEVERITY_WARNING,
        scopes=("ui", "tokens"),
        description=(
            "Scans prototype .html/.css/.js files for leaked spec IDs (FR/NFR/TR/SCR), "
            "engineering meta-jargon, and undefined CSS custom properties."
        ),
    ),
    RuleSpec(
        rule_id="GRD-17",
        name="Use Case Integrity & MVP Scope Guard",
        default_severity=SEVERITY_BLOCKER,
        scopes=("uc", "seam1"),
        description=(
            "Enforces approved MVP UC-*/SCR-*/ADR-* indexes, approved RBAC actor names, "
            "and structural completeness of UC-*.md specifications."
        ),
    ),
    RuleSpec(
        rule_id="GRD-18",
        name="Universal Relative Links, GFM Anchors & Zero Body Wikilinks",
        default_severity=SEVERITY_BLOCKER,
        scopes=("links",),
        description=(
            "Verifies all relative Markdown links resolve on disk (respecting planned-stub "
            "allowlists), all #anchor fragments match GFM heading slugs, and zero [[...]] exist in bodies."
        ),
    ),
    RuleSpec(
        rule_id="GRD-19",
        name="SRS CSV & Requirements Traceability Parity",
        default_severity=SEVERITY_WARNING,
        scopes=("srs", "uc", "ui"),
        description=(
            "Cross-checks FR-*/NFR-* IDs in requirements/data/srs.csv and TR-* references against "
            "use cases, screen §9 traceability matrices, and DT-ARQ-CMP-DOC-001 §4."
        ),
    ),
    RuleSpec(
        rule_id="GRD-20",
        name="Offline-First Outbox, LOTO Watchdog & Idempotency Replay Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("seam3", "seam4"),
        description=(
            "Verifies ADR-006 FIFO offline outbox semantics, LOTO 2s heartbeat / 30s grace window, "
            "cryptographic offline lease boundaries, and omission/handling of If-Match on offline replay."
        ),
    ),
    RuleSpec(
        rule_id="GRD-21",
        name="Markdown Formatting, Mermaid Diagrams, LaTeX & Roadmap Sync",
        default_severity=SEVERITY_WARNING,
        scopes=("ui", "links", "srs"),
        description=(
            "Checks fenced Mermaid block validity, balanced LaTeX $...$/$$...$$ math delimiters, "
            "section numbering continuity, and TODO.md artifact path alignment."
        ),
    ),
)

RULE_SPEC_MAP: dict[str, RuleSpec] = {spec.rule_id: spec for spec in RULE_SPECS}
