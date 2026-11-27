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
    affected_files: tuple[str, ...] = ()

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
    # Module 1: rules/domain_erd_parity.py (scopes: domain, erd)
    RuleSpec(
        rule_id="GRD-01",
        name="SQL CHECK & Controlled Vocabulary Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("domain", "erd"),
        description=(
            "Verifies every ck_* CHECK constraint in DT-ERD-001.sql matches DT-DM-DOC-001 §4 "
            "controlled vocabularies and catches non-enum table leaks (CB-SQL-01)."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-02",
        name="ERD Markdown-to-SQL Schema Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("domain", "erd"),
        description=(
            "Verifies 1:1 structural parity between DT-ERD-DOC-001.md and DT-ERD-001.sql "
            "(tables, column names, SQL types, nullability, defaults, PKs, FKs, and indexes)."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-03",
        name="ERD Markdown-to-DBML Schema Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("domain", "erd"),
        description=(
            "Verifies 1:1 structural parity between DT-ERD-DOC-001.md and DT-ERD-001.dbml "
            "(tables, columns, types, pk/not null/default attributes, and Ref relationships)."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-04",
        name="Domain Constants, State Machine & PlantUML Consistency",
        default_severity=SEVERITY_BLOCKER,
        scopes=("domain", "erd"),
        description=(
            "Verifies DT-DM-DOC-001 §5 constants (SOD-*, 0.0 V, 0.5 psig, 15 m, 13 m, 5 m) "
            "and entity/state consistency across DT-DM-DOC-001, DT-DM-DOC-002, and DT-DM-001.puml."
        ),
        implemented=True,
    ),
    # Module 2: rules/ui_contracts.py (scopes: contracts, ui)
    RuleSpec(
        rule_id="GRD-05",
        name="C# DTO/Command Type, Precision & Nullability Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("contracts", "ui"),
        description=(
            "Validates SCR-*.md §7.2 and DT-UI-CTR-001.md C# types (decimal, DateTimeOffset/DateOnly, "
            "uint? ConcurrencyToken) and nullability against DT-ERD-DOC-001.md."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-06",
        name="Shared Contract DRY Enforcement",
        default_severity=SEVERITY_BLOCKER,
        scopes=("contracts", "ui"),
        description=(
            "Fails if any C# record, enum, or .razor component contract is duplicated across >= 2 "
            "SCR-*.md files instead of residing in DT-UI-CTR-001.md or DT-DM-DOC-001 §4."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-07",
        name="C# Enum Parity & Pure Blazor Contract Hygiene",
        default_severity=SEVERITY_BLOCKER,
        scopes=("contracts", "ui"),
        description=(
            "Validates C# enums against DT-DM-DOC-001 §4 aliases/subsets and bans Blazor "
            "code-behind constructs (ComponentBase, [Inject], _privateFields, OnInitialized*, namespace)."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-08",
        name="Command PreviousHash Prohibition",
        default_severity=SEVERITY_BLOCKER,
        scopes=("contracts", "ui"),
        description=(
            "Bans PreviousHash on all mutating *Command and *RequestDto records, permitting it "
            "exclusively on read-side audit entry and chain-verification DTOs."
        ),
        implemented=True,
    ),
    # Module 3: rules/use_cases_rbac.py (scopes: uc, nav, rbac)
    RuleSpec(
        rule_id="GRD-09",
        name="SCR/UC Structural Completeness & Bidirectional Traceability",
        default_severity=SEVERITY_BLOCKER,
        scopes=("uc", "nav", "rbac"),
        description=(
            "Validates SCR-*.md (9 sections, §7.1-§7.3, YAML keys) and UC-*.md (6 sections, YAML keys) "
            "along with bidirectional SCR.use_cases <-> UC.Related Screens traceability."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-10",
        name="Navigation Routes, ISA-101 Levels & Alternate Flow Coverage",
        default_severity=SEVERITY_BLOCKER,
        scopes=("uc", "nav", "rbac"),
        description=(
            "Validates navigation routes and ISA-101 L1-L4 levels against DT-UI-NAV-DOC-001 §§5-6 "
            "and verifies every UC-* AF-* alternate flow is covered in linked SCR-*.md specs."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-11",
        name="RBAC Roles & SoD Reference Governance",
        default_severity=SEVERITY_BLOCKER,
        scopes=("uc", "nav", "rbac"),
        description=(
            "Validates roles across SCR-*, UC-*, and DT-UI-NAV-DOC-001 §5 against approved RBAC roles "
            "and verifies SOD-* references resolve to DT-DM-DOC-001 §5."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-12",
        name="Use Case Black-Box Invariant",
        default_severity=SEVERITY_BLOCKER,
        scopes=("uc", "nav", "rbac"),
        description=(
            "Dynamically loads ERD tables/columns/schemas and bans physical DB leaks, Class.Method(), "
            "/api/ routes, --dt-* CSS tokens, CMP-*, HTML tags, and SCR-* clutter in UC flow steps."
        ),
        implemented=True,
    ),
    # Module 4: rules/architecture_runtime.py (scopes: arch, api)
    RuleSpec(
        rule_id="GRD-13",
        name="Bidirectional REST API Catalog Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("arch", "api"),
        description=(
            "Asserts bidirectional parity of all VERB /api/v1/... endpoints between SCR-*.md "
            "and DT-ARQ-CMP-DOC-001 §6.1."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-14",
        name="SignalR Hub, Client Method & Event Record Parity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("arch", "api"),
        description=(
            "Asserts parity of SignalR /hubs/* paths, typed client methods, and event payload "
            "records between SCR-*.md and DT-ARQ-CMP-DOC-001 §§5-5.1."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-15",
        name="WORM Immutability, Idempotency & If-Match Governance",
        default_severity=SEVERITY_BLOCKER,
        scopes=("arch", "api"),
        description=(
            "Bans xmin/If-Match on WORM/append-only tables and validates RLS/partitioning/hypertables "
            "plus X-Idempotency-Key / If-Match conventions on mutating REST endpoints."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-16",
        name="ADR-003/ADR-006 SSoT, Obsolete Terms & SCR Narrative Purity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("arch", "api"),
        description=(
            "Enforces ADR-003 (Hk hash) and ADR-006 (LOTO timers / 5-step outbox) as sole SSoTs, "
            "bans obsolete terms (IActionFilter, Kubernetes), and bans DB mechanics in SCR §§1-5."
        ),
        implemented=True,
    ),
    # Module 5: rules/hygiene_ssot.py (scopes: links, ul, tokens, srs)
    RuleSpec(
        rule_id="GRD-17",
        name="Relative Links, GFM Anchors, Artifact IDs & Zero Body Wikilinks",
        default_severity=SEVERITY_BLOCKER,
        scopes=("links", "ul", "tokens", "srs"),
        description=(
            "Validates relative Markdown links, GFM section anchors, 4-segment DT-* artifact IDs, "
            "and prohibits [[...]] wikilinks in document bodies."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-18",
        name="Dimension-Agnostic 2D/3D UL & Layer Purity",
        default_severity=SEVERITY_BLOCKER,
        scopes=("links", "ul", "tokens", "srs"),
        description=(
            "Enforces dimension-agnostic domain language and layer purity across DT-UL-DOC-001.md, "
            "DT-DM-DOC-001/002, UC-*.md, and srs.csv (permitting MeshMapping entity identifier)."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-19",
        name="UI Foundation Docs, --dt-* Token Parity & WCAG 2.1 Contrast",
        default_severity=SEVERITY_BLOCKER,
        scopes=("links", "ul", "tokens", "srs"),
        description=(
            "Audits DT-UI-DS-DOC-001, DT-UI-SVG-DOC-001, DT-UI-NAV-DOC-001, --dt-* token parity "
            "against tokens.css (light & dark), and WCAG 2.1 AA contrast ratios."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-20",
        name="SVG Icons, Screenshots, Language Policy, LaTeX & Mermaid",
        default_severity=SEVERITY_WARNING,
        scopes=("links", "ul", "tokens", "srs"),
        description=(
            "Verifies #icon-* symbols in icons.svg, SCR §2 screenshot assets, Technical English in .md / "
            "Spanish UI copy in prototypes, LaTeX $...$ parity, and Mermaid block validity."
        ),
        implemented=True,
    ),
    RuleSpec(
        rule_id="GRD-21",
        name="SRS CSV Quality, TR-* Sync, Framework Ban & Dynamic MVP Index",
        default_severity=SEVERITY_WARNING,
        scopes=("links", "ul", "tokens", "srs"),
        description=(
            "Checks srs.csv integrity and TR-*.md sync, bans unapproved frameworks (React/Angular/Vue/"
            "Flutter), and dynamically verifies MVP SCR-*/UC-* index alignment."
        ),
        implemented=True,
    ),
)

RULE_SPEC_MAP: dict[str, RuleSpec] = {spec.rule_id: spec for spec in RULE_SPECS}
