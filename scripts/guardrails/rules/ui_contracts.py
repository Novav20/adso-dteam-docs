"""
Layer 2 Pure Guardrail Rules: UI Contracts, C# Types, DRY & Blazor Hygiene (`GRD-05`..`GRD-08`).

Scopes: `contracts`, `ui`.
"""

from __future__ import annotations

import re

from ..config import (
    CSHARP_ENUM_ALIASES,
    CSHARP_SUBSET_ENUM_ALIASES,
    PRESENTATION_PROJECTION_ENUMS,
    SSOT_PATHS,
    UI_LOCAL_ENUM_ALLOWLIST,
)
from ..models import SEVERITY_BLOCKER, SEVERITY_WARNING, Finding
from ..parsers import RepoIndex
from ..parsers.csharp_parser import CSharpProp, CSharpRecord
from ..parsers.sql_dbml_parser import ColumnDef, SchemaModel
from .domain_erd_parity import extract_controlled_vocabularies

_CSHARP_LANGS = frozenset({"csharp", "c#", "cs", "razor"})

_VIEWPORT_TYPE_RE = re.compile(
    r"(?:Viewport|Transform|Point2D|Coordinate|Bounds|Cartographic|Pixel|Pan|Zoom|Scale|"
    r"Overlay|ClusterPill|SimopsConflict)",
    re.IGNORECASE,
)

_SPATIAL_GEOM_PROP_RE = re.compile(
    r"(?:Coordinate[XYZ]?$|Centroid[XYZ]?$|RadiusMeters$|DistanceMeters$)"
)

# Operational/telemetry/financial/engineering quantities that MUST use decimal (never long/float/double)
_DECIMAL_PROP_RE = re.compile(
    r"(?:Hours$|Quantity$|Qty$|Stock$|Price$|Cost$|UnitCost$|Rate$|Threshold$|Limit$|"
    r"MeasuredValue$|ReadingValue$|Value$|Score$|Weight$|Voltage$|Pressure$|Radius$|"
    r"MinLevel$|MaxLevel$|ReorderPoint$|Tolerance$)",
)

_NON_DECIMAL_ALLOW_RE = re.compile(
    r"(?:Count$|TotalRows$|Page$|PageSize$|Days$|Years$|Minutes$|Seconds$|Length$|"
    r"ExpirationHours$|ConcurrencyToken$|ThresholdCount$|MaxAgeDays$|MinLength$|LockoutThreshold$|"
    r"IsMonotonicity|String|Text|Label|Tag|Name|Id$|Ids$|Status$|Type$|Code$|Unit$)",
)

_OFFLINE_COMMAND_NAMES: frozenset[str] = frozenset(
    {
        "SubmitTechnicalClosureCommand",
        "RegisterInventoryTransactionCommand",
        "ExecuteAssetSwapCommand",
        "UpsertMeshMappingCommand",
    }
)

# Read-side audit/chain DTOs allowed to carry PreviousHash
_AUDIT_READ_DTO_RE = re.compile(r"(?:Audit.*Entry|AuditLog.*|ChainVerificationGap).*Dto$")

# Blazor code-behind constructs banned in pure contract snippets
_CODE_BEHIND_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bComponentBase\b"), "ComponentBase inheritance"),
    (re.compile(r"\[Inject\]"), "[Inject] dependency injection attribute"),
    (re.compile(r"^\s*(?:private|protected)\s+[^\n;]*\b_[a-z][A-Za-z0-9_]*\b", re.MULTILINE), "mutable _privateField"),
    (re.compile(r"\bOn(?:Initialized|ParametersSet|AfterRender)(?:Async)?\b"), "Blazor lifecycle override"),
    (re.compile(r"^\s*namespace\s+[A-Za-z0-9_.]+", re.MULTILINE), "namespace declaration"),
)

# Documented read-DTO projection / derived / aggregate properties exempt from 1:1 ERD NOT NULL check
_PROJECTION_EXEMPT_RE = re.compile(
    r"(?:^(?:Id|ConcurrencyToken|TotalCount|Page|PageSize|Items|RowVersion|Message|Reason|Status|"
    r"Summary|Metrics|Badges|Events|Alerts|History|Children|Nodes|Details|Is[A-Z].*|Has[A-Z].*|"
    r"Can[A-Z].*|AssignedEquipmentUnitId|TagNumber|EquipmentTag|FunctionalLocationTag|"
    r"EquipmentName|LocationName|PlanTitle|WorkOrderNumber|SerialNumber|PartName|Sku|"
    r"RoleName|UserName|ActorName|Permits|WorkOrders|Conflicts|Gaps|IntegrityStatus|"
    r"ValidationStatus|ErrorMessage|DisplayTitle|Formatted.*|.*Count$|.*Total$|.*Summary$|"
    r".*Url$|.*Label$|.*Name$|.*Title$|.*Badge.*)$)"
)

# Map known read DTOs cleanly to primary ERD table names when unambiguous
_DTO_TABLE_MAP: dict[str, str] = {
    "EquipmentUnitMasterCardDto": "tax.equipment_units",
    "InstalledAssetDetailsDto": "tax.equipment_units",
    "EquipmentBoundaryCardDto": "tax.equipment_units",
    "FunctionalLocationTreeNodeDto": "tax.functional_locations",
    "SparePartMasterItemDto": "inv.spare_parts",
    "SparePartAvailabilityDto": "inv.spare_parts",
    "KardexTransactionRowDto": "inv.inventory_transactions",
    "BacklogItemDto": "mtto.backlog_items",
    "MaintenancePlanSummaryDto": "mtto.maintenance_plans",
    "WorkOrderClosingContextDto": "mtto.work_orders",
    "ActiveWorkOrderSummaryDto": "mtto.work_orders",
    "LotoIsolationPlanDto": "vis.work_order_isolations",
    "PtwOverlayDto": "vis.work_permits",
    "AuditLogEntryDto": "adm.audit_logs",
    "UserAccountRowDto": "adm.users",
    "RoleSummaryDto": "adm.roles",
}


def _to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _base_csharp_type(type_name: str) -> str:
    t = type_name.strip()
    if t.endswith("?"):
        t = t[:-1].strip()
    return t


def _check_erd_column_compatibility(
    rec: CSharpRecord,
    prop: CSharpProp,
    erd: SchemaModel,
) -> tuple[str, str] | None:
    """Return `(message, remediation)` if a mapped read DTO property violates ERD type or nullability."""
    tbl_name = _DTO_TABLE_MAP.get(rec.name)
    if tbl_name is None or tbl_name not in erd.tables:
        return None
    if _PROJECTION_EXEMPT_RE.match(prop.name):
        return None

    col_name = _to_snake(prop.name)
    col: ColumnDef | None = erd.tables[tbl_name].columns.get(col_name)
    if col is None:
        return None

    sql_type = col.data_type.upper()
    base_cs = _base_csharp_type(prop.type_name)

    # Check numeric type parity
    if ("DECIMAL" in sql_type or "NUMERIC" in sql_type) and base_cs in ("int", "long", "float", "double"):
        return (
            f"{rec.name}.{prop.name} uses '{prop.type_name}' but '{tbl_name}.{col_name}' is {sql_type} (requires decimal).",
            f"Change {rec.name}.{prop.name} to 'decimal{'?' if prop.is_nullable else ''}'.",
        )
    if sql_type == "BIGINT" and base_cs in ("int", "short"):
        return (
            f"{rec.name}.{prop.name} uses '{prop.type_name}' but '{tbl_name}.{col_name}' is BIGINT (requires long).",
            f"Change {rec.name}.{prop.name} to 'long{'?' if prop.is_nullable else ''}'.",
        )
    if sql_type == "DATE" and base_cs in ("DateTime", "DateTimeOffset"):
        return (
            f"{rec.name}.{prop.name} uses '{prop.type_name}' on DATE column '{tbl_name}.{col_name}' (use DateOnly).",
            f"Change {rec.name}.{prop.name} to 'DateOnly{'?' if prop.is_nullable else ''}'.",
        )

    # Check required non-nullable property on read DTO against nullable ERD column
    if not rec.name.endswith("Command") and prop.is_required and not prop.is_nullable and col.nullable:
        return (
            f"Read DTO property {rec.name}.{prop.name} is 'required' non-nullable '{prop.type_name}' "
            f"but ERD column '{tbl_name}.{col_name}' is NULL.",
            f"Make {rec.name}.{prop.name} nullable ('{base_cs}?') or enforce NOT NULL in DT-ERD-DOC-001.md.",
        )

    return None


def evaluate_grd_05(index: RepoIndex) -> list[Finding]:
    """GRD-05: C# DTO/Command type precision, temporal types, ConcurrencyToken & ERD nullability."""
    findings: list[Finding] = []
    erd = index.erd_doc_schema

    target_files = sorted(
        rel
        for rel in index.csharp_records
        if rel.startswith("ui-ux/screens/") or rel == SSOT_PATHS.ui_ctr_doc
    )

    for rel in target_files:
        for rec in index.csharp_records.get(rel, ()):
            is_viewport_type = bool(_VIEWPORT_TYPE_RE.search(rec.name))
            is_command = rec.name.endswith("Command")

            for prop in rec.properties:
                base_t = _base_csharp_type(prop.type_name)

                # 1. Ban DateTime / DateTime?
                if base_t == "DateTime":
                    findings.append(
                        Finding(
                            rule_id="GRD-05",
                            severity=SEVERITY_BLOCKER,
                            scope="contracts",
                            file=rel,
                            line=prop.line or rec.line,
                            message=(
                                f"Property {rec.name}.{prop.name} uses forbidden 'DateTime' "
                                f"(use 'DateTimeOffset' for UTC timestamps or 'DateOnly' for dates)."
                            ),
                            remediation="Replace DateTime with DateTimeOffset (or DateOnly for calendar dates).",
                        )
                    )

                # 2. Numeric precision boundary: decimal vs float/double/long
                if not is_viewport_type and not _SPATIAL_GEOM_PROP_RE.search(prop.name):
                    if base_t in ("float", "double"):
                        findings.append(
                            Finding(
                                rule_id="GRD-05",
                                severity=SEVERITY_BLOCKER,
                                scope="contracts",
                                file=rel,
                                line=prop.line or rec.line,
                                message=(
                                    f"Non-viewport property {rec.name}.{prop.name} uses IEEE-754 '{prop.type_name}' "
                                    f"(use 'decimal' for operational/telemetry/engineering quantities)."
                                ),
                                remediation=f"Change {rec.name}.{prop.name} to 'decimal{'?' if prop.is_nullable else ''}'.",
                            )
                        )
                    elif (
                        base_t in ("long", "int")
                        and _DECIMAL_PROP_RE.search(prop.name)
                        and not _NON_DECIMAL_ALLOW_RE.search(prop.name)
                    ):
                        # Operational hours/quantities/thresholds must be decimal (CB-R02)
                        if prop.name in ("OperatingHours", "SurveillanceHours", "InitialOperatingHoursBaseline") or prop.name.endswith("Hours"):
                            findings.append(
                                Finding(
                                    rule_id="GRD-05",
                                    severity=SEVERITY_BLOCKER,
                                    scope="contracts",
                                    file=rel,
                                    line=prop.line or rec.line,
                                    message=(
                                        f"Operational hours property {rec.name}.{prop.name} uses '{prop.type_name}' "
                                        f"instead of 'decimal' (CB-R02)."
                                    ),
                                    remediation=f"Change {rec.name}.{prop.name} to 'decimal{'?' if prop.is_nullable else ''}'.",
                                )
                            )

                # 3. ConcurrencyToken conventions
                if prop.name == "ConcurrencyToken":
                    if base_t != "uint":
                        findings.append(
                            Finding(
                                rule_id="GRD-05",
                                severity=SEVERITY_BLOCKER,
                                scope="contracts",
                                file=rel,
                                line=prop.line or rec.line,
                                message=(
                                    f"{rec.name}.ConcurrencyToken has type '{prop.type_name}' "
                                    f"(must map PostgreSQL xmin as 'uint' or 'uint?')."
                                ),
                                remediation="Change ConcurrencyToken to 'uint' (online) or 'uint?' (offline-capable/upsert).",
                            )
                        )
                    elif is_command and rec.name in _OFFLINE_COMMAND_NAMES and not prop.is_nullable:
                        findings.append(
                            Finding(
                                rule_id="GRD-05",
                                severity=SEVERITY_BLOCKER,
                                scope="contracts",
                                file=rel,
                                line=prop.line or rec.line,
                                message=(
                                    f"Offline-capable command {rec.name}.ConcurrencyToken must be nullable 'uint?' "
                                    f"so offline FIFO replays can omit stale xmin (ADR-006)."
                                ),
                                remediation="Change ConcurrencyToken to 'uint?' on offline-capable commands.",
                            )
                        )

                # 4. ERD column parity on mapped read DTOs
                if erd is not None:
                    compat_err = _check_erd_column_compatibility(rec, prop, erd)
                    if compat_err is not None:
                        msg, rem = compat_err
                        findings.append(
                            Finding(
                                rule_id="GRD-05",
                                severity=SEVERITY_BLOCKER,
                                scope="contracts",
                                file=rel,
                                line=prop.line or rec.line,
                                message=msg,
                                remediation=rem,
                            )
                        )

    return findings


def evaluate_grd_06(index: RepoIndex) -> list[Finding]:
    """GRD-06: Fail if any C# record, enum, or .razor component is duplicated across >= 2 SCR-*.md."""
    findings: list[Finding] = []

    ctr_records = {r.name for r in index.csharp_records.get(SSOT_PATHS.ui_ctr_doc, ())}
    ctr_enums = {e.name for e in index.csharp_enums.get(SSOT_PATHS.ui_ctr_doc, ())}
    ctr_razors = {
        rz.component_name
        for rz in index.razor_contracts.get(SSOT_PATHS.ui_ctr_doc, ())
        if rz.component_name
    }

    scr_records: dict[str, list[tuple[str, int]]] = {}
    scr_enums: dict[str, list[tuple[str, int]]] = {}
    scr_razors: dict[str, list[tuple[str, int]]] = {}

    for rel in sorted(index.screen_docs.keys()):
        for rec in index.csharp_records.get(rel, ()):
            scr_records.setdefault(rec.name, []).append((rel, rec.line))
            if rec.name in ctr_records:
                findings.append(
                    Finding(
                        rule_id="GRD-06",
                        severity=SEVERITY_BLOCKER,
                        scope="contracts",
                        file=rel,
                        line=rec.line,
                        message=(
                            f"Shared C# type '{rec.name}' is redeclared in '{rel}' "
                            f"even though it already lives in DT-UI-CTR-001.md."
                        ),
                        remediation="Remove the duplicate inline declaration and link to DT-UI-CTR-001.md.",
                    )
                )

        for enm in index.csharp_enums.get(rel, ()):
            scr_enums.setdefault(enm.name, []).append((rel, enm.line))
            if enm.name in ctr_enums or enm.name in CSHARP_ENUM_ALIASES:
                findings.append(
                    Finding(
                        rule_id="GRD-06",
                        severity=SEVERITY_BLOCKER,
                        scope="contracts",
                        file=rel,
                        line=enm.line,
                        message=(
                            f"Shared/canonical enum '{enm.name}' is redeclared inline in '{rel}' "
                            f"(must reference DT-DM-DOC-001 §4 or DT-UI-CTR-001.md)."
                        ),
                        remediation="Remove the inline enum block and add a link to DT-DM-DOC-001 §4.",
                    )
                )

        for rz in index.razor_contracts.get(rel, ()):
            if not rz.component_name:
                continue
            scr_razors.setdefault(rz.component_name, []).append((rel, rz.start_line))
            if rz.component_name in ctr_razors:
                findings.append(
                    Finding(
                        rule_id="GRD-06",
                        severity=SEVERITY_BLOCKER,
                        scope="contracts",
                        file=rel,
                        line=rz.start_line,
                        message=(
                            f"Shared Razor component '{rz.component_name}' is redeclared in '{rel}' "
                            f"even though its SSoT contract lives in DT-UI-CTR-001.md."
                        ),
                        remediation="Replace the inline Razor block with a 1-line link to DT-UI-CTR-001.md.",
                    )
                )

    for rec_name, locs in sorted(scr_records.items()):
        distinct_files = {f for f, _ in locs}
        if len(distinct_files) >= 2:
            others = sorted(distinct_files)
            for rel, line_no in locs:
                findings.append(
                    Finding(
                        rule_id="GRD-06",
                        severity=SEVERITY_BLOCKER,
                        scope="contracts",
                        file=rel,
                        line=line_no,
                        message=(
                            f"C# record/class '{rec_name}' is duplicated across {len(distinct_files)} screens "
                            f"({', '.join(others)})."
                        ),
                        remediation="Move shared DTO/record to DT-UI-CTR-001.md and link to it from SCR-*.md.",
                    )
                )

    for enm_name, locs in sorted(scr_enums.items()):
        distinct_files = {f for f, _ in locs}
        if len(distinct_files) >= 2:
            others = sorted(distinct_files)
            for rel, line_no in locs:
                findings.append(
                    Finding(
                        rule_id="GRD-06",
                        severity=SEVERITY_BLOCKER,
                        scope="contracts",
                        file=rel,
                        line=line_no,
                        message=(
                            f"C# enum '{enm_name}' is duplicated across {len(distinct_files)} screens "
                            f"({', '.join(others)})."
                        ),
                        remediation="Consolidate shared enum into DT-UI-CTR-001.md or DT-DM-DOC-001 §4.",
                    )
                )

    for rz_name, locs in sorted(scr_razors.items()):
        distinct_files = {f for f, _ in locs}
        if len(distinct_files) >= 2:
            others = sorted(distinct_files)
            for rel, line_no in locs:
                findings.append(
                    Finding(
                        rule_id="GRD-06",
                        severity=SEVERITY_BLOCKER,
                        scope="contracts",
                        file=rel,
                        line=line_no,
                        message=(
                            f"Razor component '{rz_name}' is duplicated across {len(distinct_files)} screens "
                            f"({', '.join(others)})."
                        ),
                        remediation="Consolidate shared Razor component contract into DT-UI-CTR-001.md.",
                    )
                )

    return findings


def evaluate_grd_07(index: RepoIndex) -> list[Finding]:
    """GRD-07: C# enum parity against DT-DM-DOC-001 §4 and ban Blazor code-behind constructs."""
    findings: list[Finding] = []
    dm_doc = index.markdown_docs.get(SSOT_PATHS.dm_class_doc)

    vocab_by_ent: dict[str, tuple[str, ...]] = {}
    if dm_doc is not None:
        vocab_by_ent, _, _ = extract_controlled_vocabularies(dm_doc)

    # 1. Validate all C# enums across SCR-*, DT-UI-CTR-001, and DT-ARQ-CMP-DOC-001
    for rel, enum_list in sorted(index.csharp_enums.items()):
        for enm in enum_list:
            members = set(enm.members)
            if enm.name in CSHARP_ENUM_ALIASES:
                key = CSHARP_ENUM_ALIASES[enm.name]
                expected = set(vocab_by_ent.get(key, ()))
                if not expected:
                    findings.append(
                        Finding(
                            rule_id="GRD-07",
                            severity=SEVERITY_BLOCKER,
                            scope="contracts",
                            file=rel,
                            line=enm.line,
                            message=f"Enum '{enm.name}' maps to '{key}', which was not found in DT-DM-DOC-001 §4.",
                            remediation="Verify DT-DM-DOC-001 §4 subsection name or CSHARP_ENUM_ALIASES.",
                        )
                    )
                else:
                    missing = sorted(expected - members)
                    extra = sorted(members - expected)
                    if missing or extra:
                        findings.append(
                            Finding(
                                rule_id="GRD-07",
                                severity=SEVERITY_BLOCKER,
                                scope="contracts",
                                file=rel,
                                line=enm.line,
                                message=(
                                    f"C# enum '{enm.name}' diverges from DT-DM-DOC-001 §4 '{key}': "
                                    f"missing={missing}, extra={extra}."
                                ),
                                remediation="Synchronize C# enum members 1:1 with DT-DM-DOC-001 §4.",
                            )
                        )
            elif enm.name in CSHARP_SUBSET_ENUM_ALIASES:
                key = CSHARP_SUBSET_ENUM_ALIASES[enm.name]
                expected = set(vocab_by_ent.get(key, ()))
                invalid = sorted(members - expected) if expected else []
                if not members or invalid:
                    findings.append(
                        Finding(
                            rule_id="GRD-07",
                            severity=SEVERITY_BLOCKER,
                            scope="contracts",
                            file=rel,
                            line=enm.line,
                            message=(
                                f"Subset enum '{enm.name}' contains values not in DT-DM-DOC-001 §4 '{key}': {invalid}."
                            ),
                            remediation="Restrict subset enum values strictly to members of the canonical domain enum.",
                        )
                    )
            elif enm.name in PRESENTATION_PROJECTION_ENUMS:
                expected_proj = set(PRESENTATION_PROJECTION_ENUMS[enm.name])
                if members != expected_proj:
                    findings.append(
                        Finding(
                            rule_id="GRD-07",
                            severity=SEVERITY_BLOCKER,
                            scope="contracts",
                            file=rel,
                            line=enm.line,
                            message=(
                                f"Presentation projection enum '{enm.name}' diverges from canonical set: "
                                f"expected={sorted(expected_proj)}, got={sorted(members)}."
                            ),
                            remediation="Align projection enum members with config.PRESENTATION_PROJECTION_ENUMS.",
                        )
                    )
            elif enm.name not in UI_LOCAL_ENUM_ALLOWLIST:
                findings.append(
                    Finding(
                        rule_id="GRD-07",
                        severity=SEVERITY_WARNING,
                        scope="contracts",
                        file=rel,
                        line=enm.line,
                        message=(
                            f"Unregistered C# enum '{enm.name}' is not mapped to DT-DM-DOC-001 §4 "
                            f"or UI_LOCAL_ENUM_ALLOWLIST."
                        ),
                        remediation="Map the enum in DT-DM-DOC-001 §4 + CSHARP_ENUM_ALIASES or register as UI presentation enum.",
                    )
                )

    # 2. Ban Blazor code-behind constructs in SCR-*.md and DT-UI-CTR-001.md
    target_docs = [*sorted(index.screen_docs.keys()), SSOT_PATHS.ui_ctr_doc]
    for rel in target_docs:
        doc = index.markdown_docs.get(rel)
        if doc is None:
            continue
        for block in doc.code_blocks:
            if block.language not in _CSHARP_LANGS:
                continue
            for offset, line_txt in enumerate(block.content.splitlines(), start=1):
                for pat, label in _CODE_BEHIND_PATTERNS:
                    if pat.search(line_txt):
                        findings.append(
                            Finding(
                                rule_id="GRD-07",
                                severity=SEVERITY_BLOCKER,
                                scope="ui",
                                file=rel,
                                line=block.start_line + offset,
                                message=(
                                    f"Forbidden Blazor code-behind construct ({label}) in pure §7 contract block."
                                ),
                                remediation="Keep §7 blocks strictly declarative ([Parameter] / DTOs only; no ComponentBase/[Inject]/_fields/lifecycle).",
                            )
                        )

    return findings


def evaluate_grd_08(index: RepoIndex) -> list[Finding]:
    """GRD-08: Ban PreviousHash on all mutating *Command / *RequestDto records (ADR-003)."""
    findings: list[Finding] = []

    for rel, rec_list in sorted(index.csharp_records.items()):
        for rec in rec_list:
            for prop in rec.properties:
                if prop.name != "PreviousHash":
                    continue
                is_mutating = rec.name.endswith("Command") or rec.name.endswith("RequestDto")
                is_allowed_read = bool(_AUDIT_READ_DTO_RE.search(rec.name))
                if is_mutating or not is_allowed_read:
                    findings.append(
                        Finding(
                            rule_id="GRD-08",
                            severity=SEVERITY_BLOCKER,
                            scope="contracts",
                            file=rel,
                            line=prop.line or rec.line,
                            message=(
                                f"Forbidden 'PreviousHash' property on '{rec.name}'. "
                                f"Per ADR-003, clients must never supply PreviousHash; only read-side audit DTOs may expose it."
                            ),
                            remediation="Remove PreviousHash from the command/DTO; let AuditSaveChangesInterceptor resolve H_{k-1} pre-commit.",
                        )
                    )

    return findings
