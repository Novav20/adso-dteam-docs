"""
Layer 2 Pure Guardrail Rules: Architecture, REST/SignalR Parity, WORM & SSoT (`GRD-13`..`GRD-16`).

Scopes: `arch`, `api`.
"""

from __future__ import annotations

import re

from ..config import SSOT_PATHS, WORM_TABLES
from ..models import SEVERITY_BLOCKER, SEVERITY_WARNING, Finding
from ..parsers import RepoIndex

_REST_CALL_RE = re.compile(r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/api/v1/[A-Za-z0-9_./{}?=&-]+)")
_SCR_ID_RE = re.compile(r"\bSCR-[A-Z]+-\d+\b")
_HUB_RE = re.compile(r"(/hubs/[a-z0-9-]+)\b")
_SIGNALR_METHOD_RE = re.compile(r"`?([A-Z][A-Za-z0-9]+)\(([A-Za-z0-9_<>]+)\s+[A-Za-z0-9_]+\)`?")

_EXEMPT_IDEMPOTENCY_ROUTES: frozenset[str] = frozenset(
    {
        "/api/v1/taxonomy/maintainable-items/validate-exclusivity",
        "/api/v1/security/audit-logs/query",
        "/api/v1/maintenance/work-orders/{}/media-upload-sas",
    }
)

_WORM_ENTITY_KEYWORDS: tuple[str, ...] = (
    "audit-logs",
    "audit_logs",
    "auditlog",
    "auditretentionpartition",
    "telemetrysignal",
    "workorderhistory",
    "inventory-transaction",
    "inventory_transactions",
)

# Ad-hoc SHA-256 chain concatenation formulas outside ADR-003.md
_ADHOC_CHAIN_HASH_RE = re.compile(
    r"(?:SHA-256\s*\([^)]*(?:H_\{?k-1\}?|PreviousHash)|\\text\{IntegrityHash\}\s*=\s*\\text\{SHA-256\})",
    re.IGNORECASE,
)

# Obsolete architectural terms banned in active docs & Structurizr DSLs
_OBSOLETE_ARCH_TERM_RE = re.compile(r"\b(?:IActionFilter|Kubernetes|K8s)\b", re.IGNORECASE)
_PROHIBITION_CTX_RE = re.compile(
    r"(?:discarded|rejected|not\s+allowed|forbidden|prohibited|excluded|avoid|superseded|replaced\s+by|obsolete|no\s+longer)",
    re.IGNORECASE,
)

# Backend/DB implementation leaks forbidden in SCR-*.md §§1-5 narrative prose
_SCR_NARRATIVE_DB_LEAK_RE = re.compile(
    r"\b(?:AuditSaveChangesInterceptor|FOR\s+UPDATE\s+NOWAIT|FILTER\s*\(\s*WHERE|"
    r"ON\s+DELETE\s+RESTRICT|SQLCipher|JSONB)\b"
)


def _normalize_route(raw_route: str) -> str:
    # Strip query string and normalize path parameter placeholders ({id}, {workOrderId}, etc. -> {})
    base = raw_route.split("?", 1)[0].rstrip(".,;)`'\"")
    return re.sub(r"\{[^}]+\}", "{}", base)


def _scr_id_from_rel(rel: str, doc_fm: dict[str, object]) -> str:
    fm_id = str(doc_fm.get("id") or "").strip()
    if fm_id:
        return fm_id
    m = _SCR_ID_RE.search(rel)
    return m.group(0) if m else rel


def _parse_cmp_rest_catalog(
    cmp_text: str,
) -> list[tuple[str, str, str, str, set[str], int]]:
    """
    Parse `DT-ARQ-CMP-DOC-001.md` §6.1 endpoint tables.

    Returns list of `(verb, norm_route, raw_route, idempotency_cell, consuming_screens, line_no)`.
    """
    entries: list[tuple[str, str, str, str, set[str], int]] = []
    in_sec61 = False
    for line_no, raw_line in enumerate(cmp_text.splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped.startswith("### 6.1"):
            in_sec61 = True
            continue
        if in_sec61 and stripped.startswith("## ") and not stripped.startswith("## 6."):
            break
        if not in_sec61 or not stripped.startswith("|"):
            continue
        if re.match(r"^\|[\s:-]+\|", stripped) or stripped.startswith("| Method + Route"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 4:
            continue
        m = _REST_CALL_RE.search(cells[0])
        if not m:
            continue
        verb = m.group(1).upper()
        raw_route = m.group(2)
        norm_route = _normalize_route(raw_route)
        idem_cell = cells[2]
        screens = set(_SCR_ID_RE.findall(cells[3]))
        entries.append((verb, norm_route, raw_route, idem_cell, screens, line_no))
    return entries


def _parse_cmp_signalr_catalog(
    cmp_text: str,
) -> tuple[dict[str, tuple[set[str], set[str], set[str], int]], dict[str, tuple[set[str], int]]]:
    """
    Parse `DT-ARQ-CMP-DOC-001.md` §5 and §5.1.

    Returns:
      - `methods_by_name`: `{method_name: (hubs, interfaces, consumers, line_no)}`
      - `records_by_name`: `{record_name: (field_names, line_no)}`
    """
    methods_by_name: dict[str, tuple[set[str], set[str], set[str], int]] = {}
    records_by_name: dict[str, tuple[set[str], int]] = {}
    section = ""

    for line_no, raw_line in enumerate(cmp_text.splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped.startswith("## 5."):
            section = "5"
            continue
        if stripped.startswith("### 5.1"):
            section = "5.1"
            continue
        if stripped.startswith("## ") and not stripped.startswith("## 5."):
            break
        if not section or not stripped.startswith("|"):
            continue
        if re.match(r"^\|[\s:-]+\|", stripped):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if section == "5" and len(cells) >= 5 and not cells[0].lower().startswith("hub"):
            hub_m = _HUB_RE.search(cells[0])
            hub = hub_m.group(1) if hub_m else cells[0].strip("` ")
            iface = cells[1].strip("` ")
            mm = _SIGNALR_METHOD_RE.search(cells[2])
            if mm:
                meth_name = mm.group(1)
                consumers = set(_SCR_ID_RE.findall(cells[4]))
                methods_by_name[meth_name] = ({hub}, {iface}, consumers, line_no)
        elif section == "5.1" and len(cells) >= 2 and not cells[0].lower().startswith("event record"):
            rec_name = cells[0].strip("*` ").strip()
            fields = set(re.findall(r"`([A-Z][A-Za-z0-9_]+)`\s*\(", cells[1]))
            if rec_name:
                records_by_name[rec_name] = (fields, line_no)

    return methods_by_name, records_by_name


def _strip_rejected_sections(raw_text: str) -> str:
    out: list[str] = []
    skip = False
    for line in raw_text.splitlines():
        if re.match(r"^\s*supersedes\s*:", line, re.IGNORECASE):
            out.append("")
            continue
        if re.match(r"^##\s+(?:Alternatives\s+Considered|Rejected\s+Alternatives|Superseded)", line, re.IGNORECASE):
            skip = True
            out.append("")
            continue
        if skip and re.match(r"^##\s+", line):
            skip = False
        out.append("" if skip else line)
    return "\n".join(out)


def evaluate_grd_13(index: RepoIndex) -> list[Finding]:
    """GRD-13: Bidirectional REST API catalog parity between SCR-*.md and DT-ARQ-CMP-DOC-001 §6.1."""
    findings: list[Finding] = []
    cmp_path = SSOT_PATHS.arq_cmp_doc
    cmp_doc = index.markdown_docs.get(cmp_path)
    if cmp_doc is None:
        findings.append(
            Finding(
                rule_id="GRD-13",
                severity=SEVERITY_BLOCKER,
                scope="api",
                file=cmp_path,
                line=None,
                message=f"Missing '{cmp_path}'.",
                remediation="Restore DT-ARQ-CMP-DOC-001.md.",
            )
        )
        return findings

    catalog = _parse_cmp_rest_catalog(cmp_doc.raw_text)
    catalog_map: dict[tuple[str, str], tuple[set[str], int]] = {}
    for verb, norm_route, _, _, screens, line_no in catalog:
        key = (verb, norm_route)
        if key in catalog_map:
            catalog_map[key][0].update(screens)
        else:
            catalog_map[key] = (set(screens), line_no)

    # Collect all VERB /api/v1/... calls in SCR-*.md
    scr_calls: dict[tuple[str, str], dict[str, int]] = {}
    scr_id_to_rel: dict[str, str] = {}

    for rel, doc in sorted(index.screen_docs.items()):
        scr_id = _scr_id_from_rel(rel, doc.frontmatter)
        scr_id_to_rel[scr_id] = rel
        for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
            for rm in _REST_CALL_RE.finditer(line):
                verb = rm.group(1).upper()
                norm_route = _normalize_route(rm.group(2))
                key = (verb, norm_route)
                scr_calls.setdefault(key, {})
                scr_calls[key].setdefault(scr_id, line_no)

                if key not in catalog_map:
                    findings.append(
                        Finding(
                            rule_id="GRD-13",
                            severity=SEVERITY_BLOCKER,
                            scope="api",
                            file=rel,
                            line=line_no,
                            message=(
                                f"Screen '{scr_id}' references undocumented REST endpoint "
                                f"'{verb} {rm.group(2).split('?', 1)[0]}' missing from DT-ARQ-CMP-DOC-001 §6.1."
                            ),
                            remediation="Register the endpoint in DT-ARQ-CMP-DOC-001 §6.1 or align the route path.",
                        )
                    )
                else:
                    expected_screens, cat_line = catalog_map[key]
                    if scr_id not in expected_screens:
                        findings.append(
                            Finding(
                                rule_id="GRD-13",
                                severity=SEVERITY_BLOCKER,
                                scope="api",
                                file=cmp_path,
                                line=cat_line,
                                message=(
                                    f"DT-ARQ-CMP-DOC-001 §6.1 route '{verb} {norm_route}' omits consuming "
                                    f"screen '{scr_id}' (used at {rel}:{line_no})."
                                ),
                                remediation=f"Append '{scr_id}' to Consuming Screens for '{verb} {norm_route}'.",
                            )
                        )

    # Reverse check: every screen listed in DT-ARQ-CMP-DOC-001 §6.1 must reference that route
    for (verb, norm_route), (expected_screens, cat_line) in sorted(catalog_map.items()):
        actual_screens = set(scr_calls.get((verb, norm_route), {}).keys())
        for scr_id in sorted(expected_screens - actual_screens):
            if scr_id not in scr_id_to_rel:
                continue
            findings.append(
                Finding(
                    rule_id="GRD-13",
                    severity=SEVERITY_BLOCKER,
                    scope="api",
                    file=cmp_path,
                    line=cat_line,
                    message=(
                        f"DT-ARQ-CMP-DOC-001 §6.1 lists '{scr_id}' as consumer of '{verb} {norm_route}', "
                        f"but '{scr_id_to_rel[scr_id]}' does not reference that endpoint."
                    ),
                    remediation=f"Remove '{scr_id}' from Consuming Screens or document the route in '{scr_id}'.",
                )
            )

    return findings


def evaluate_grd_14(index: RepoIndex) -> list[Finding]:
    """GRD-14: SignalR /hubs/* paths, client methods, and event records parity vs DT-ARQ-CMP-DOC-001 §§5-5.1."""
    findings: list[Finding] = []
    cmp_path = SSOT_PATHS.arq_cmp_doc
    cmp_doc = index.markdown_docs.get(cmp_path)
    if cmp_doc is None:
        return findings

    methods_map, records_map = _parse_cmp_signalr_catalog(cmp_doc.raw_text)
    known_hubs = {h for hubs, _, _, _ in methods_map.values() for h in hubs}

    # Check hubs and SignalR method references across SCR-*.md
    _hub_method_re = re.compile(r"`([A-Z][A-Za-z0-9_]+)\([^)]*\)`")
    for rel, doc in sorted(index.screen_docs.items()):
        for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
            has_hub = False
            for hm in _HUB_RE.finditer(line):
                has_hub = True
                hub = hm.group(1)
                if known_hubs and hub not in known_hubs:
                    findings.append(
                        Finding(
                            rule_id="GRD-14",
                            severity=SEVERITY_BLOCKER,
                            scope="api",
                            file=rel,
                            line=line_no,
                            message=f"Screen references unknown SignalR hub '{hub}' (not in DT-ARQ-CMP-DOC-001 §5).",
                            remediation="Register the hub in DT-ARQ-CMP-DOC-001 §5 or use a canonical hub path.",
                            affected_files=(cmp_path,),
                        )
                    )
            if has_hub and methods_map:
                for mm in _hub_method_re.finditer(line):
                    method_name = mm.group(1)
                    if method_name not in methods_map:
                        findings.append(
                            Finding(
                                rule_id="GRD-14",
                                severity=SEVERITY_BLOCKER,
                                scope="api",
                                file=rel,
                                line=line_no,
                                message=f"Screen references unknown SignalR client method '{method_name}' (not in DT-ARQ-CMP-DOC-001 §5).",
                                remediation="Register the SignalR client method in DT-ARQ-CMP-DOC-001 §5 or use a canonical method name.",
                                affected_files=(cmp_path,),
                            )
                        )

    # Validate SignalR event records declared as C# records in SCR-*.md / DT-UI-CTR-001.md
    for rel in [*sorted(index.screen_docs.keys()), SSOT_PATHS.ui_ctr_doc]:
        for rec in index.csharp_records.get(rel, ()):
            if rec.name not in records_map:
                continue
            expected_fields, _ = records_map[rec.name]
            actual_fields = {p.name for p in rec.properties}
            missing = sorted(expected_fields - actual_fields)
            extra = sorted(actual_fields - expected_fields)
            if missing or extra:
                findings.append(
                    Finding(
                        rule_id="GRD-14",
                        severity=SEVERITY_BLOCKER,
                        scope="api",
                        file=rel,
                        line=rec.line,
                        message=(
                            f"SignalR event record '{rec.name}' diverges from DT-ARQ-CMP-DOC-001 §5.1: "
                            f"missing={missing}, extra={extra}."
                        ),
                        remediation="Align SignalR event record fields with DT-ARQ-CMP-DOC-001 §5.1.",
                    )
                )

    return findings


def evaluate_grd_15(index: RepoIndex) -> list[Finding]:
    """GRD-15: Ban xmin/If-Match on WORM tables and check X-Idempotency-Key / If-Match REST conventions."""
    findings: list[Finding] = []

    # 1. DT-ARQ-DB-DOC-001 §3.12 must not list WORM tables as mutable xmin aggregate roots
    db_doc = index.markdown_docs.get(SSOT_PATHS.arq_db_doc)
    if db_doc is not None:
        in_312 = False
        for line_no, line in enumerate(db_doc.raw_text.splitlines(), start=1):
            s = line.strip()
            if s.startswith("### 3.12"):
                in_312 = True
                continue
            if in_312 and (s.startswith("### ") or s.startswith("## ")):
                break
            if in_312 and "exempt" not in s.lower() and "prohibited" not in s.lower():
                for wt in sorted(WORM_TABLES):
                    if wt in s:
                        findings.append(
                            Finding(
                                rule_id="GRD-15",
                                severity=SEVERITY_BLOCKER,
                                scope="arch",
                                file=SSOT_PATHS.arq_db_doc,
                                line=line_no,
                                message=(
                                    f"WORM/append-only table '{wt}' appears in DT-ARQ-DB-DOC-001 §3.12 "
                                    f"without explicit exemption (UPDATE/xmin concurrency is invalid on WORM tables)."
                                ),
                                remediation="Restrict xmin row-versioning strictly to mutable aggregate roots.",
                            )
                        )

    # 2. DT-ERD-001.sql WORM governance (RLS on audit_logs, partition_by, hypertable on telemetry_signals)
    sql = index.sql_schema
    if sql is not None:
        audit_tbl = sql.tables.get("adm.audit_logs")
        if audit_tbl is not None:
            if not (audit_tbl.rls_enabled and audit_tbl.rls_forced):
                findings.append(
                    Finding(
                        rule_id="GRD-15",
                        severity=SEVERITY_BLOCKER,
                        scope="arch",
                        file=SSOT_PATHS.erd_sql,
                        line=audit_tbl.line,
                        message="WORM table 'adm.audit_logs' must have ENABLE + FORCE ROW LEVEL SECURITY in DT-ERD-001.sql.",
                        remediation="Add ENABLE ROW LEVEL SECURITY and FORCE ROW LEVEL SECURITY on adm.audit_logs.",
                    )
                )
            if audit_tbl.partition_by != "timestamp":
                findings.append(
                    Finding(
                        rule_id="GRD-15",
                        severity=SEVERITY_BLOCKER,
                        scope="arch",
                        file=SSOT_PATHS.erd_sql,
                        line=audit_tbl.line,
                        message=(
                            f"WORM table 'adm.audit_logs' must use PARTITION BY RANGE (timestamp) "
                            f"(found {audit_tbl.partition_by!r})."
                        ),
                        remediation="Set PARTITIONED_TABLES['adm.audit_logs'] = 'timestamp' and regenerate DDL.",
                    )
                )

        telem_tbl = sql.tables.get("vis.telemetry_signals")
        if telem_tbl is not None and not telem_tbl.is_hypertable:
            findings.append(
                Finding(
                    rule_id="GRD-15",
                    severity=SEVERITY_BLOCKER,
                    scope="arch",
                    file=SSOT_PATHS.erd_sql,
                    line=telem_tbl.line,
                    message="Time-series WORM table 'vis.telemetry_signals' is missing TimescaleDB create_hypertable().",
                    remediation="Include create_hypertable('vis.telemetry_signals', ...) in DT-ERD-DOC-001-heuristics.sql.",
                )
            )

    # 3. DT-ARQ-CMP-DOC-001 §6.1 X-Idempotency-Key & WORM If-Match guard
    cmp_doc = index.markdown_docs.get(SSOT_PATHS.arq_cmp_doc)
    if cmp_doc is not None:
        for verb, norm_route, raw_route, idem_cell, _, line_no in _parse_cmp_rest_catalog(cmp_doc.raw_text):
            if verb in ("POST", "PUT", "PATCH", "DELETE"):
                is_exempt = norm_route in _EXEMPT_IDEMPOTENCY_ROUTES or "valet key" in idem_cell.lower() or "exempt" in idem_cell.lower()
                if not is_exempt and "x-idempotency-key" not in idem_cell.lower():
                    findings.append(
                        Finding(
                            rule_id="GRD-15",
                            severity=SEVERITY_BLOCKER,
                            scope="api",
                            file=SSOT_PATHS.arq_cmp_doc,
                            line=line_no,
                            message=(
                                f"Mutating endpoint '{verb} {raw_route}' lacks 'X-Idempotency-Key' in "
                                f"DT-ARQ-CMP-DOC-001 §6.1."
                            ),
                            remediation="Require X-Idempotency-Key (ADR-007) or document explicit read-only validation exemption.",
                        )
                    )
                if any(wk in norm_route.lower() for wk in _WORM_ENTITY_KEYWORDS) and "if-match" in idem_cell.lower():
                    findings.append(
                        Finding(
                            rule_id="GRD-15",
                            severity=SEVERITY_BLOCKER,
                            scope="api",
                            file=SSOT_PATHS.arq_cmp_doc,
                            line=line_no,
                            message=f"WORM endpoint '{verb} {raw_route}' must not enforce If-Match / xmin concurrency.",
                            remediation="Remove If-Match from append-only WORM endpoint.",
                        )
                    )

    # 4. Ban ConcurrencyToken on WORM entity DTOs/commands
    for rel, rec_list in sorted(index.csharp_records.items()):
        for rec in rec_list:
            if rec.name == "RegisterInventoryTransactionCommand":
                continue
            low_name = rec.name.lower()
            if any(wk.replace("-", "") in low_name for wk in _WORM_ENTITY_KEYWORDS):
                for prop in rec.properties:
                    if prop.name == "ConcurrencyToken":
                        findings.append(
                            Finding(
                                rule_id="GRD-15",
                                severity=SEVERITY_BLOCKER,
                                scope="arch",
                                file=rel,
                                line=prop.line or rec.line,
                                message=f"WORM DTO/Command '{rec.name}' must not declare ConcurrencyToken (xmin).",
                                remediation="Remove ConcurrencyToken from WORM/append-only entity contracts.",
                            )
                        )

    # 5. Check SCR-*.md §5 mutating endpoint prose for X-Idempotency-Key
    _scr_mut_re = re.compile(r"`(POST|PUT|PATCH|DELETE)\s+(/api/v1/[^`\s]+)`")
    for rel, doc in sorted(index.screen_docs.items()):
        lines = doc.raw_text.splitlines()
        in_sec5 = False
        for idx, line in enumerate(lines):
            line_no = idx + 1
            s = line.strip()
            if s.startswith("## 5."):
                in_sec5 = True
                continue
            if in_sec5 and s.startswith("## "):
                break
            if not in_sec5:
                continue
            window = "\n".join(lines[idx : min(idx + 3, len(lines))]).lower()
            for m in _scr_mut_re.finditer(line):
                verb, raw_route = m.group(1), m.group(2)
                norm_route = raw_route.rstrip("/")
                if (
                    norm_route in _EXEMPT_IDEMPOTENCY_ROUTES
                    or "valet key" in window
                    or "exempt" in window
                    or "media-upload-sas" in norm_route
                ):
                    continue
                if "x-idempotency-key" not in window:
                    findings.append(
                        Finding(
                            rule_id="GRD-15",
                            severity=SEVERITY_BLOCKER,
                            scope="api",
                            file=rel,
                            line=line_no,
                            message=f"Mutating endpoint '{verb} {raw_route}' in §5 prose lacks 'X-Idempotency-Key'.",
                            remediation="Document X-Idempotency-Key (ADR-007) alongside mutating endpoints in §5.",
                        )
                    )

    return findings


def evaluate_grd_16(index: RepoIndex) -> list[Finding]:
    """GRD-16: ADR-003/ADR-006 SSoT enforcement, obsolete term ban & SCR §§1-5 narrative purity."""
    findings: list[Finding] = []

    # 1. Verify ADR-003 defines canonical H_k chain hash formula & constants
    adr3 = index.markdown_docs.get(SSOT_PATHS.adr_003)
    if adr3 is None:
        findings.append(
            Finding(
                rule_id="GRD-16",
                severity=SEVERITY_BLOCKER,
                scope="arch",
                file=SSOT_PATHS.adr_003,
                line=None,
                message=f"Missing '{SSOT_PATHS.adr_003}'.",
                remediation="Restore ADR-003.md as sole SSoT for SHA-256 chain hash formula.",
            )
        )
    else:
        for req_tok in ("H_{k-1}", "CanonicalJson", "GENESIS", ">= 15", "7 years"):
            if req_tok not in adr3.raw_text:
                findings.append(
                    Finding(
                        rule_id="GRD-16",
                        severity=SEVERITY_BLOCKER,
                        scope="arch",
                        file=SSOT_PATHS.adr_003,
                        line=None,
                        message=f"ADR-003.md is missing canonical audit SSoT element '{req_tok}'.",
                        remediation="Ensure ADR-003 §Canonical Hash Formula & Audit Constants includes all canonical constants.",
                    )
                )

    # 2. Verify ADR-006 defines LOTO watchdog timers & 5-step outbox protocol
    adr6 = index.markdown_docs.get(SSOT_PATHS.adr_006)
    if adr6 is None:
        findings.append(
            Finding(
                rule_id="GRD-16",
                severity=SEVERITY_BLOCKER,
                scope="arch",
                file=SSOT_PATHS.adr_006,
                line=None,
                message=f"Missing '{SSOT_PATHS.adr_006}'.",
                remediation="Restore ADR-006.md as sole SSoT for offline outbox & LOTO timers.",
            )
        )
    else:
        for req_tok in ("2 seconds", "30 seconds", "60 minutes", "15 minutes", "8 hours", "Step 1", "Step 5"):
            if req_tok not in adr6.raw_text:
                findings.append(
                    Finding(
                        rule_id="GRD-16",
                        severity=SEVERITY_BLOCKER,
                        scope="arch",
                        file=SSOT_PATHS.adr_006,
                        line=None,
                        message=f"ADR-006.md is missing canonical offline/LOTO SSoT element '{req_tok}'.",
                        remediation="Restore canonical watchdog constants and 5-step outbox protocol in ADR-006.md.",
                    )
                )

    # 3. Ban ad-hoc SHA-256 chain hash formulas outside ADR-003.md, and ban obsolete terms across .md and .dsl
    for rel, doc in sorted(index.markdown_docs.items()):
        if rel != SSOT_PATHS.adr_003:
            for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
                if _ADHOC_CHAIN_HASH_RE.search(line):
                    findings.append(
                        Finding(
                            rule_id="GRD-16",
                            severity=SEVERITY_BLOCKER,
                            scope="arch",
                            file=rel,
                            line=line_no,
                            message=(
                                f"Ad-hoc SHA-256 chain hash formula found outside '{SSOT_PATHS.adr_003}'."
                            ),
                            remediation="Remove the inline hash concatenation formula and link to ADR-003.md.",
                        )
                    )

        # Obsolete architectural terms (exempt ADR rejected/alternatives sections and explicit prohibition lines)
        scoped_text = _strip_rejected_sections(doc.raw_text) if "architecture/adr/" in rel else doc.raw_text
        for line_no, line in enumerate(scoped_text.splitlines(), start=1):
            om = _OBSOLETE_ARCH_TERM_RE.search(line)
            if om and not _PROHIBITION_CTX_RE.search(line):
                findings.append(
                    Finding(
                        rule_id="GRD-16",
                        severity=SEVERITY_BLOCKER,
                        scope="arch",
                        file=rel,
                        line=line_no,
                        message=f"Obsolete architecture term '{om.group(0)}' detected in '{rel}'.",
                        remediation="Remove obsolete IActionFilter/Kubernetes references (Minimal API filters / Docker Compose).",
                    )
                )

        if rel.startswith("architecture/") and rel != SSOT_PATHS.adr_006:
            ttl_re = re.compile(r"\b(?:15[-\s]*min(?:ute)?s?|8[-\s]*hours?)\b", re.IGNORECASE)
            for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
                if ttl_re.search(line):
                    findings.append(
                        Finding(
                            rule_id="GRD-16",
                            severity=SEVERITY_BLOCKER,
                            scope="arch",
                            file=rel,
                            line=line_no,
                            message=f"Hardcoded ADR-006 session TTL literal duplicated in '{rel}'.",
                            remediation="Reference ADR-006 §Canonical Offline, Watchdog & Session Constants instead of hardcoding TTLs.",
                        )
                    )

    for rel, raw_dsl in sorted(index.raw_texts.items()):
        if not rel.endswith(".dsl"):
            continue
        for line_no, line in enumerate(raw_dsl.splitlines(), start=1):
            om = _OBSOLETE_ARCH_TERM_RE.search(line)
            if om and not _PROHIBITION_CTX_RE.search(line):
                findings.append(
                    Finding(
                        rule_id="GRD-16",
                        severity=SEVERITY_BLOCKER,
                        scope="arch",
                        file=rel,
                        line=line_no,
                        message=f"Obsolete architecture term '{om.group(0)}' detected in Structurizr DSL '{rel}'.",
                        remediation="Update Structurizr DSL to reflect approved architecture.",
                    )
                )

    # 4. Offline Delta Cards in SCR-*.md & DT-UI-NAV-DOC-001 §6 must reference ADR-006 (not drift)
    for rel, doc in sorted(index.screen_docs.items()):
        for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
            if "Offline Delta Card" in line and "ADR-006" not in line:
                # Check nearby lines for ADR-006 link
                window = "\n".join(doc.raw_text.splitlines()[max(0, line_no - 1) : line_no + 3])
                if "ADR-006" not in window:
                    findings.append(
                        Finding(
                            rule_id="GRD-16",
                            severity=SEVERITY_WARNING,
                            scope="arch",
                            file=rel,
                            line=line_no,
                            message="Offline Delta Card does not cite ADR-006 as its offline protocol SSoT.",
                            remediation="Reference ADR-006 in the Offline Delta Card.",
                        )
                    )

        # 5. Ban backend/DB mechanics in SCR-*.md §§1-5 narrative prose
        for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
            if line.strip().startswith("## 6.") or line.strip().startswith("## 7."):
                break
            bm = _SCR_NARRATIVE_DB_LEAK_RE.search(line)
            if bm:
                findings.append(
                    Finding(
                        rule_id="GRD-16",
                        severity=SEVERITY_BLOCKER,
                        scope="arch",
                        file=rel,
                        line=line_no,
                        message=(
                            f"Backend/DB persistence mechanic '{bm.group(0)}' leaked into SCR narrative §§1-5."
                        ),
                        remediation="Move DB/interceptor internals out of §§1-5 UI narrative and cite DT-ARQ-DB-DOC-001/ADR-003/ADR-006.",
                    )
                )

    return findings
