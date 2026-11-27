"""
Layer 2 Pure Guardrail Rules: Use Cases, Navigation & RBAC Governance (`GRD-09`..`GRD-12`).

Scopes: `uc`, `nav`, `rbac`.
"""

from __future__ import annotations

import re

from ..config import (
    APPROVED_RBAC_ROLES,
    APPROVED_SYSTEM_ACTORS,
    CANONICAL_SOD_CODES,
    SSOT_PATHS,
)
from ..models import SEVERITY_BLOCKER, SEVERITY_WARNING, Finding
from ..parsers import RepoIndex
from ..parsers.markdown_parser import ParsedMarkdownDoc

_SCR_REQUIRED_FM_KEYS: tuple[str, ...] = (
    "id",
    "title",
    "module",
    "isa101_level",
    "platform",
    "target_device",
    "roles",
    "user_stories",
    "use_cases",
    "status",
    "version",
    "date",
)

_UC_REQUIRED_FM_KEYS: tuple[str, ...] = (
    "id",
    "name",
    "module",
    "user_story",
    "primary_actor",
    "secondary_actors",
)

_SCR_ID_RE = re.compile(r"\bSCR-[A-Z]+-\d+\b")
_UC_ID_RE = re.compile(r"\bUC-[A-Z]+-\d+\b")
_AF_HEADING_RE = re.compile(r"^###\s+(AF-\d+)\b")
_AF_REF_RE = re.compile(r"\bAF-\d+\b")
_SOD_RE = re.compile(r"\bSOD-[A-Z]+-\d+\b")
_ISA_LEVEL_RE = re.compile(r"(?<![A-Za-z0-9\-./])L(\d+)\b")

_ISO14224_CTX_RE = re.compile(
    r"(?:ISO\s*14224|taxonom|functional\s+location|equipment\s+unit|subunit|maintainable\s+item|"
    r"hierarchy|cascading|picker|selector|slot|boundary|boundaries|tag|breadcrumb|asset|equipment|"
    r"parent|child|node|tree|level|L1\s*(?:to|[-–—])\s*L[56789]|L[5678]\s*[-–/→]\s*L[6789]|"
    r"L[5678]\s*\$\\to\$\s*L[6789]|component|spare|master\s+data)",
    re.IGNORECASE,
)

# Black-box leak patterns inside UC bodies
_UC_INFRA_TECH_RE = re.compile(
    r"\b(?:PostgreSQL|SQLite|sqlite-net-pcl|SQLCipher|EF\s+Core|DbContext|DbTransaction|"
    r"AuditSaveChangesInterceptor|SignalR|Redis|Azure\s+Blob|JSONB|UUIDv7|xmin|"
    r"FOR\s+UPDATE\s+NOWAIT|SyncOutbox|Blazor|MAUI|Razor)\b",
    re.IGNORECASE,
)
_UC_CLASS_METHOD_RE = re.compile(r"\b[A-Z][A-Za-z0-9_]+\.[A-Z][A-Za-z0-9_]+\(")
_UC_API_ROUTE_RE = re.compile(r"(?:^|[\s`'\"])(/api/[a-zA-Z0-9_/{}/?=&-]+)")
_UC_CSS_TOKEN_RE = re.compile(r"--dt-[a-z0-9-]+")
_UC_CMP_ID_RE = re.compile(r"\bCMP-\d+\b")
_UC_HTML_TAG_RE = re.compile(
    r"<(?:div|span|button|input|table|thead|tbody|tr|td|th|svg|path|select|form|label|section)\b[^>]*>",
    re.IGNORECASE,
)


def _extract_related_screens(uc_doc: ParsedMarkdownDoc) -> list[str]:
    found: list[str] = []
    for line in uc_doc.raw_text.splitlines():
        if "Related Screens" in line:
            for scr in _SCR_ID_RE.findall(line):
                if scr not in found:
                    found.append(scr)
    return found


def _scr_id_to_rel(index: RepoIndex) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for rel, doc in index.screen_docs.items():
        scr_id = str(doc.frontmatter.get("id") or "").strip()
        if not scr_id:
            m = _SCR_ID_RE.search(rel)
            if m:
                scr_id = m.group(0)
        if scr_id:
            mapping[scr_id] = rel
    return mapping


def _uc_id_to_rel(index: RepoIndex) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for rel, doc in index.usecase_docs.items():
        uc_id = str(doc.frontmatter.get("id") or "").strip()
        if not uc_id:
            m = _UC_ID_RE.search(rel)
            if m:
                uc_id = m.group(0)
        if uc_id:
            mapping[uc_id] = rel
    return mapping


def _as_str_list(val: object) -> list[str]:
    if val is None:
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    s = str(val).strip()
    return [s] if s else []


def _as_id_list(val: object) -> list[str]:
    out: list[str] = []
    for raw in _as_str_list(val):
        cleaned = raw.strip()
        if cleaned.startswith("[[") and cleaned.endswith("]]"):
            cleaned = cleaned[2:-2].split("|", 1)[0].strip()
        if cleaned:
            out.append(cleaned)
    return out


def _extract_isa_levels(raw_level: object) -> tuple[list[str], list[str]]:
    text = str(raw_level or "").strip()
    valid: list[str] = []
    invalid: list[str] = []
    for m in _ISA_LEVEL_RE.finditer(text):
        lvl = f"L{m.group(1)}"
        if lvl in ("L1", "L2", "L3", "L4"):
            if lvl not in valid:
                valid.append(lvl)
        elif lvl not in invalid:
            invalid.append(lvl)
    return valid, invalid


def _clean_role_token(raw: str) -> str:
    cleaned = re.sub(r"\s*\([^)]*\)", "", raw).strip().strip(".").strip()
    return cleaned


def evaluate_grd_09(index: RepoIndex) -> list[Finding]:
    """GRD-09: Validate SCR-*.md (9 sections, §7.1-§7.3, YAML), UC-*.md (6 sections, YAML) & bidirectional traceability."""
    findings: list[Finding] = []
    scr_map = _scr_id_to_rel(index)
    uc_map = _uc_id_to_rel(index)

    # 1. SCR-*.md structure & outgoing UC links
    for rel, doc in sorted(index.screen_docs.items()):
        fm = doc.frontmatter
        for key in _SCR_REQUIRED_FM_KEYS:
            if key not in fm:
                findings.append(
                    Finding(
                        rule_id="GRD-09",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=1,
                        message=f"SCR specification '{rel}' is missing required YAML frontmatter key '{key}'.",
                        remediation=f"Add '{key}:' to YAML frontmatter matching SCR-TEMPLATE.",
                    )
                )

        h2_nums: list[int] = []
        h2_lines: dict[int, int] = {}
        sec7_subs: list[str] = []
        in_sec7 = False
        for h in doc.headings:
            if h.level == 2:
                m = re.match(r"^(\d+)\.", h.text)
                if m:
                    num = int(m.group(1))
                    h2_nums.append(num)
                    h2_lines[num] = h.line
                    in_sec7 = num == 7
                else:
                    in_sec7 = False
            elif h.level == 3 and in_sec7:
                sm = re.match(r"^(7\.[123])\b", h.text)
                if sm:
                    sec7_subs.append(sm.group(1))

        if h2_nums != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            findings.append(
                Finding(
                    rule_id="GRD-09",
                    severity=SEVERITY_BLOCKER,
                    scope="uc",
                    file=rel,
                    line=None,
                    message=f"SCR '{rel}' must have ordered sections ## 1. through ## 9. (found {h2_nums}).",
                    remediation="Align top-level sections with the 9 canonical SCR-TEMPLATE sections.",
                )
            )
        if sec7_subs != ["7.1", "7.2", "7.3"]:
            findings.append(
                Finding(
                    rule_id="GRD-09",
                    severity=SEVERITY_BLOCKER,
                    scope="uc",
                    file=rel,
                    line=h2_lines.get(7),
                    message=f"SCR '{rel}' §7 must contain ordered subsections ### 7.1, ### 7.2, ### 7.3 (found {sec7_subs}).",
                    remediation="Ensure §7.1 Page/View Parameters, §7.2 Component State & Contracts, §7.3 Component Tree.",
                )
            )

        scr_id = str(fm.get("id") or "").strip()
        for uc_id in _as_id_list(fm.get("use_cases")):
            if uc_id not in uc_map:
                findings.append(
                    Finding(
                        rule_id="GRD-09",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=1,
                        message=f"SCR '{scr_id}' references unknown use case '{uc_id}' in frontmatter 'use_cases'.",
                        remediation=f"Verify '{uc_id}' exists under domain-models/use-cases/.",
                    )
                )
                continue
            uc_rel = uc_map[uc_id]
            uc_doc = index.usecase_docs[uc_rel]
            rel_scrs = _extract_related_screens(uc_doc)
            if scr_id and scr_id not in rel_scrs:
                findings.append(
                    Finding(
                        rule_id="GRD-09",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=uc_rel,
                        line=None,
                        message=(
                            f"Asymmetric traceability: '{scr_id}' lists '{uc_id}' in frontmatter 'use_cases', "
                            f"but '{uc_rel}' omits '{scr_id}' in '* **Related Screens:**'."
                        ),
                        remediation=f"Add [{scr_id}](...) to '* **Related Screens:**' in '{uc_rel}'.",
                    )
                )

    # 2. UC-*.md structure & outgoing SCR links
    for rel, doc in sorted(index.usecase_docs.items()):
        fm = doc.frontmatter
        for key in _UC_REQUIRED_FM_KEYS:
            if key not in fm:
                findings.append(
                    Finding(
                        rule_id="GRD-09",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=1,
                        message=f"Use Case '{rel}' is missing required YAML frontmatter key '{key}'.",
                        remediation=f"Add '{key}:' to YAML frontmatter.",
                    )
                )

        h2_nums = []
        for h in doc.headings:
            if h.level == 2:
                m = re.match(r"^(\d+)\.", h.text)
                if m:
                    h2_nums.append(int(m.group(1)))
        if h2_nums != [1, 2, 3, 4, 5, 6]:
            findings.append(
                Finding(
                    rule_id="GRD-09",
                    severity=SEVERITY_BLOCKER,
                    scope="uc",
                    file=rel,
                    line=None,
                    message=f"Use Case '{rel}' must have ordered sections ## 1. through ## 6. (found {h2_nums}).",
                    remediation="Align sections with canonical UC template (## 1..## 6).",
                )
            )

        uc_id = str(fm.get("id") or "").strip()
        rel_scrs = _extract_related_screens(doc)
        if not rel_scrs:
            findings.append(
                Finding(
                    rule_id="GRD-09",
                    severity=SEVERITY_BLOCKER,
                    scope="uc",
                    file=rel,
                    line=None,
                    message=f"Use Case '{uc_id}' is missing '* **Related Screens:**' traceability in §6.",
                    remediation=f"Add '* **Related Screens:** [SCR-...](...)' under §6 of '{rel}'.",
                )
            )
            continue

        for scr_id in rel_scrs:
            if scr_id not in scr_map:
                findings.append(
                    Finding(
                        rule_id="GRD-09",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=None,
                        message=f"Use Case '{uc_id}' links unknown screen '{scr_id}' in Related Screens.",
                        remediation=f"Verify '{scr_id}' exists under ui-ux/screens/.",
                    )
                )
                continue
            scr_rel = scr_map[scr_id]
            scr_ucs = _as_id_list(index.screen_docs[scr_rel].frontmatter.get("use_cases"))
            if uc_id and uc_id not in scr_ucs:
                findings.append(
                    Finding(
                        rule_id="GRD-09",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=scr_rel,
                        line=1,
                        message=(
                            f"Asymmetric traceability: '{uc_id}' references '{scr_id}' in Related Screens, "
                            f"but '{scr_rel}' omits '{uc_id}' in frontmatter 'use_cases'."
                        ),
                        remediation=f"Add '{uc_id}' to frontmatter 'use_cases' in '{scr_rel}'.",
                    )
                )

    return findings


def evaluate_grd_10(index: RepoIndex) -> list[Finding]:
    """GRD-10: Navigation routes & ISA-101 levels vs DT-UI-NAV-DOC-001 §§5-6, plus UC AF-* coverage in SCR-*.md."""
    findings: list[Finding] = []
    nav_path = SSOT_PATHS.ui_nav_doc
    nav_doc = index.markdown_docs.get(nav_path)
    scr_map = _scr_id_to_rel(index)
    uc_map = _uc_id_to_rel(index)

    # 1. Validate DT-UI-NAV-DOC-001 §§5-6 screen links & ISA-101 levels
    if nav_doc is None:
        findings.append(
            Finding(
                rule_id="GRD-10",
                severity=SEVERITY_BLOCKER,
                scope="nav",
                file=nav_path,
                line=None,
                message=f"Missing '{nav_path}'.",
                remediation="Restore DT-UI-NAV-DOC-001.md.",
            )
        )
    else:
        for tbl in nav_doc.tables:
            hdrs_low = [h.lower() for h in tbl.headers]
            if not any("origin" in h for h in hdrs_low) or not any("destination" in h for h in hdrs_low):
                continue
            for r_idx, row in enumerate(tbl.rows):
                if len(row) < 4:
                    continue
                origin_cell, _, dest_cell, level_cell = row[0], row[1], row[2], row[3]
                row_line = tbl.start_line + 2 + r_idx
                origin_m = _SCR_ID_RE.search(origin_cell)
                dest_m = _SCR_ID_RE.search(dest_cell)

                for cell_m, role_lbl in ((origin_m, "origin"), (dest_m, "destination")):
                    if cell_m and cell_m.group(0) not in scr_map:
                        findings.append(
                            Finding(
                                rule_id="GRD-10",
                                severity=SEVERITY_BLOCKER,
                                scope="nav",
                                file=nav_path,
                                line=row_line,
                                message=f"Transition matrix {role_lbl} screen '{cell_m.group(0)}' does not exist in ui-ux/screens/.",
                                remediation="Ensure navigation transitions point to existing SCR-*.md specifications.",
                            )
                        )

                levels = re.findall(r"L(\d+)", level_cell)
                for lv in levels:
                    if lv not in ("1", "2", "3", "4"):
                        findings.append(
                            Finding(
                                rule_id="GRD-10",
                                severity=SEVERITY_BLOCKER,
                                scope="nav",
                                file=nav_path,
                                line=row_line,
                                message=f"Invalid ISA-101 level 'L{lv}' in transition matrix (only L1-L4 allowed).",
                                remediation="Use ISA-101 levels L1 through L4.",
                            )
                        )
                if len(levels) == 2 and origin_m and dest_m:
                    orig_id, dest_id = origin_m.group(0), dest_m.group(0)
                    if orig_id in scr_map:
                        orig_raw = index.screen_docs[scr_map[orig_id]].frontmatter.get("isa101_level")
                        orig_levels, _ = _extract_isa_levels(orig_raw)
                        if orig_levels and f"L{levels[0]}" not in orig_levels:
                            findings.append(
                                Finding(
                                    rule_id="GRD-10",
                                    severity=SEVERITY_BLOCKER,
                                    scope="nav",
                                    file=nav_path,
                                    line=row_line,
                                    message=(
                                        f"Origin ISA-101 mismatch for {orig_id}: NAV says L{levels[0]}, "
                                        f"screen frontmatter says {orig_raw}."
                                    ),
                                    remediation="Align ISA-101 level between DT-UI-NAV-DOC-001 §5 and SCR frontmatter.",
                                )
                            )
                    if dest_id in scr_map:
                        dest_raw = index.screen_docs[scr_map[dest_id]].frontmatter.get("isa101_level")
                        dest_levels, _ = _extract_isa_levels(dest_raw)
                        if dest_levels and f"L{levels[1]}" not in dest_levels:
                            findings.append(
                                Finding(
                                    rule_id="GRD-10",
                                    severity=SEVERITY_BLOCKER,
                                    scope="nav",
                                    file=nav_path,
                                    line=row_line,
                                    message=(
                                        f"Destination ISA-101 mismatch for {dest_id}: NAV says L{levels[1]}, "
                                        f"screen frontmatter says {dest_raw}."
                                    ),
                                    remediation="Align ISA-101 level between DT-UI-NAV-DOC-001 §5 and SCR frontmatter.",
                                )
                            )

    # 2. Validate ISA-101 level range (L1-L4) across SCR-*.md (excluding ISO 14224 taxonomy L5-L9 contexts)
    for rel, doc in sorted(index.screen_docs.items()):
        lv = str(doc.frontmatter.get("isa101_level") or "").strip()
        valid_lvs, invalid_lvs = _extract_isa_levels(lv)
        if not valid_lvs or invalid_lvs:
            findings.append(
                Finding(
                    rule_id="GRD-10",
                    severity=SEVERITY_BLOCKER,
                    scope="nav",
                    file=rel,
                    line=1,
                    message=f"Invalid frontmatter isa101_level '{lv}' in '{rel}' (must contain L1..L4).",
                    remediation="Set isa101_level to L1, L2, L3, or L4.",
                )
            )

        lines = doc.raw_text.splitlines()
        for line_no, line in enumerate(lines, start=1):
            for lm in _ISA_LEVEL_RE.finditer(line):
                lvl = f"L{lm.group(1)}"
                if lvl in ("L1", "L2", "L3", "L4"):
                    continue
                prev = lines[line_no - 2] if line_no >= 2 else ""
                if lvl in ("L5", "L6", "L7", "L8", "L9") and (
                    _ISO14224_CTX_RE.search(line) or _ISO14224_CTX_RE.search(prev)
                ):
                    continue
                findings.append(
                    Finding(
                        rule_id="GRD-10",
                        severity=SEVERITY_BLOCKER,
                        scope="nav",
                        file=rel,
                        line=line_no,
                        message=f"Invalid ISA-101 level '{lvl}' in '{rel}' (only L1-L4 allowed).",
                        remediation="Use L1-L4 for ISA-101 levels or clarify ISO 14224 taxonomy context.",
                    )
                )

    # 3. Verify every UC-* AF-### alternate flow is addressed in linked SCR-*.md
    for uc_rel, uc_doc in sorted(index.usecase_docs.items()):
        uc_id = str(uc_doc.frontmatter.get("id") or "").strip()
        declared_afs: list[tuple[str, int]] = []
        for idx, line in enumerate(uc_doc.raw_text.splitlines(), start=1):
            am = _AF_HEADING_RE.match(line.strip())
            if am:
                declared_afs.append((am.group(1), idx))
        if not declared_afs:
            continue

        # Collect linked SCR docs (either UC Related Screens or SCR frontmatter use_cases)
        linked_scr_rels: set[str] = set()
        for scr_id in _extract_related_screens(uc_doc):
            if scr_id in scr_map:
                linked_scr_rels.add(scr_map[scr_id])
        for scr_rel, scr_doc in index.screen_docs.items():
            if uc_id and uc_id in _as_id_list(scr_doc.frontmatter.get("use_cases")):
                linked_scr_rels.add(scr_rel)

        if not linked_scr_rels:
            continue

        # Only enforce AF coverage on primary owning SCR (where UC id module/number matches SCR or any linked SCR)
        combined_scr_texts = {
            scr_rel: set(_AF_REF_RE.findall(index.screen_docs[scr_rel].raw_text))
            for scr_rel in linked_scr_rels
        }
        all_covered_afs = set().union(*combined_scr_texts.values())

        # Resolve primary screen if matching numeric suffix exists
        primary_scr = next(
            (s for s in sorted(linked_scr_rels) if uc_id.replace("UC-", "SCR-") in index.screen_docs[s].frontmatter.get("id", "")),
            sorted(linked_scr_rels)[0],
        )

        for af_id, af_line in declared_afs:
            if af_id not in all_covered_afs:
                findings.append(
                    Finding(
                        rule_id="GRD-10",
                        severity=SEVERITY_WARNING,
                        scope="uc",
                        file=primary_scr,
                        line=None,
                        message=(
                            f"Alternate flow '{af_id}' from '{uc_id}' ({uc_rel}:{af_line}) is not explicitly "
                            f"referenced in linked screen(s): {', '.join(sorted(linked_scr_rels))}."
                        ),
                        remediation=f"Document '{af_id}' handling/state in §4 or §5 of '{primary_scr}'.",
                    )
                )

    return findings


def evaluate_grd_11(index: RepoIndex) -> list[Finding]:
    """GRD-11: Validate RBAC roles across SCR-*, UC-*, NAV §5 and verify SOD-* refs resolve to DT-DM-DOC-001 §5."""
    findings: list[Finding] = []
    approved_lower = {r.lower() for r in APPROVED_RBAC_ROLES}
    approved_actors_lower = approved_lower | {a.lower() for a in APPROVED_SYSTEM_ACTORS}
    canonical_sods = set(CANONICAL_SOD_CODES)

    # 1. SCR-*.md frontmatter roles + SOD-* references
    for rel, doc in sorted(index.screen_docs.items()):
        for role_raw in _as_str_list(doc.frontmatter.get("roles")):
            cleaned = _clean_role_token(role_raw)
            if cleaned.lower() not in approved_lower:
                findings.append(
                    Finding(
                        rule_id="GRD-11",
                        severity=SEVERITY_BLOCKER,
                        scope="rbac",
                        file=rel,
                        line=1,
                        message=f"Unapproved RBAC role '{role_raw}' in frontmatter of '{rel}'.",
                        remediation="Use canonical role names from config.APPROVED_RBAC_ROLES / SCR-ADM-013.",
                    )
                )
        for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
            for sm in _SOD_RE.finditer(line):
                sod_code = sm.group(0)
                if sod_code not in canonical_sods:
                    findings.append(
                        Finding(
                            rule_id="GRD-11",
                            severity=SEVERITY_BLOCKER,
                            scope="rbac",
                            file=rel,
                            line=line_no,
                            message=f"Unknown SoD rule code '{sod_code}' (canonical codes: {sorted(canonical_sods)}).",
                            remediation="Reference a canonical SOD-* code defined in DT-DM-DOC-001 §5.1.",
                        )
                    )

    # 2. UC-*.md actors + SOD-* references
    for rel, doc in sorted(index.usecase_docs.items()):
        for p_actor in _as_str_list(doc.frontmatter.get("primary_actor")):
            cleaned = _clean_role_token(p_actor)
            if cleaned.lower() not in approved_actors_lower:
                findings.append(
                    Finding(
                        rule_id="GRD-11",
                        severity=SEVERITY_BLOCKER,
                        scope="rbac",
                        file=rel,
                        line=1,
                        message=f"Unapproved primary_actor '{p_actor}' in '{rel}'.",
                        remediation="Use canonical RBAC roles from SCR-ADM-013 / config.APPROVED_RBAC_ROLES.",
                    )
                )
        for s_actor in _as_str_list(doc.frontmatter.get("secondary_actors")):
            cleaned = _clean_role_token(s_actor)
            if cleaned.lower() not in approved_actors_lower:
                findings.append(
                    Finding(
                        rule_id="GRD-11",
                        severity=SEVERITY_BLOCKER,
                        scope="rbac",
                        file=rel,
                        line=1,
                        message=f"Unapproved secondary_actor '{s_actor}' in '{rel}'.",
                        remediation="Use canonical RBAC roles or APPROVED_SYSTEM_ACTORS.",
                    )
                )
        for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
            for sm in _SOD_RE.finditer(line):
                sod_code = sm.group(0)
                if sod_code not in canonical_sods:
                    findings.append(
                        Finding(
                            rule_id="GRD-11",
                            severity=SEVERITY_BLOCKER,
                            scope="rbac",
                            file=rel,
                            line=line_no,
                            message=f"Unknown SoD rule code '{sod_code}' in '{rel}'.",
                            remediation="Reference a canonical SOD-* code from DT-DM-DOC-001 §5.1.",
                        )
                    )

    # 3. DT-UI-NAV-DOC-001 §5 Authorized Roles & SOD-* references
    nav_doc = index.markdown_docs.get(SSOT_PATHS.ui_nav_doc)
    if nav_doc is not None:
        for tbl in nav_doc.tables:
            hdrs_low = [h.lower() for h in tbl.headers]
            role_idx = next((i for i, h in enumerate(hdrs_low) if "role" in h), -1)
            if role_idx == -1:
                continue
            for r_idx, row in enumerate(tbl.rows):
                if role_idx >= len(row):
                    continue
                row_line = tbl.start_line + 2 + r_idx
                for candidate in row[role_idx].split(","):
                    cleaned = _clean_role_token(candidate)
                    if not cleaned:
                        continue
                    if cleaned.lower() not in approved_lower:
                        findings.append(
                            Finding(
                                rule_id="GRD-11",
                                severity=SEVERITY_BLOCKER,
                                scope="rbac",
                                file=SSOT_PATHS.ui_nav_doc,
                                line=row_line,
                                message=f"Unapproved RBAC role '{candidate.strip()}' in DT-UI-NAV-DOC-001 §5.",
                                remediation="Align Authorized Roles column with canonical RBAC roles.",
                            )
                        )
        for line_no, line in enumerate(nav_doc.raw_text.splitlines(), start=1):
            for sm in _SOD_RE.finditer(line):
                if sm.group(0) not in canonical_sods:
                    findings.append(
                        Finding(
                            rule_id="GRD-11",
                            severity=SEVERITY_BLOCKER,
                            scope="rbac",
                            file=SSOT_PATHS.ui_nav_doc,
                            line=line_no,
                            message=f"Unknown SoD rule code '{sm.group(0)}' in DT-UI-NAV-DOC-001.",
                            remediation="Reference a canonical SOD-* code from DT-DM-DOC-001 §5.1.",
                        )
                    )

    return findings


def evaluate_grd_12(index: RepoIndex) -> list[Finding]:
    """GRD-12: UC Black-Box Invariant (ban physical DB leaks, Class.Method(), /api/, --dt-*, CMP-*, HTML, SCR-* clutter)."""
    findings: list[Finding] = []
    erd = index.erd_doc_schema

    # Dynamically collect schemas, physical table names, and non-generic physical snake_case column names
    schema_table_re: re.Pattern[str] | None = None
    phys_tables_re: re.Pattern[str] | None = None
    phys_cols_re: re.Pattern[str] | None = None

    if erd is not None and erd.tables:
        schemas = sorted({t.schema for t in erd.tables.values()})
        tbl_names = sorted({t.name for t in erd.tables.values()})
        # Multi-word snake_case physical column names unlikely in plain English prose
        col_names = sorted(
            {
                c
                for t in erd.tables.values()
                for c in t.columns
                if "_" in c and c not in {"serial_number", "work_order"}
            }
        )
        if schemas:
            schema_table_re = re.compile(rf"\b(?:{'|'.join(re.escape(s) for s in schemas)})\.[a-z][a-z0-9_]+\b")
        if tbl_names:
            phys_tables_re = re.compile(rf"\b(?:{'|'.join(re.escape(t) for t in tbl_names if '_' in t)})\b")
        if col_names:
            phys_cols_re = re.compile(rf"\b(?:{'|'.join(re.escape(c) for c in col_names)})\b")

    for rel, doc in sorted(index.usecase_docs.items()):
        lines = doc.raw_text.splitlines()
        in_fm = False
        fm_done = False
        current_h2 = ""

        for line_no, raw_line in enumerate(lines, start=1):
            stripped = raw_line.strip()
            if line_no == 1 and stripped == "---":
                in_fm = True
                continue
            if in_fm and not fm_done:
                if stripped == "---":
                    fm_done = True
                continue

            if stripped.startswith("## "):
                current_h2 = stripped
                continue

            # Exempt §6 Associated Requirements / Related Screens traceability section
            if current_h2.startswith("## 6.") or "Related Screens" in stripped:
                continue

            # 1. Physical schema.table, table_name, column_name leaks
            if schema_table_re is not None:
                m = schema_table_re.search(raw_line)
                if m:
                    findings.append(
                        Finding(
                            rule_id="GRD-12",
                            severity=SEVERITY_BLOCKER,
                            scope="uc",
                            file=rel,
                            line=line_no,
                            message=f"Physical schema.table leak '{m.group(0)}' inside black-box UC body.",
                            remediation="Replace physical SQL identifier with domain Ubiquitous Language term.",
                        )
                    )
            if phys_tables_re is not None:
                m = phys_tables_re.search(raw_line)
                if m:
                    findings.append(
                        Finding(
                            rule_id="GRD-12",
                            severity=SEVERITY_BLOCKER,
                            scope="uc",
                            file=rel,
                            line=line_no,
                            message=f"Physical DB table identifier '{m.group(0)}' inside black-box UC body.",
                            remediation="Use domain aggregate name instead of snake_case table name.",
                        )
                    )
            if phys_cols_re is not None:
                m = phys_cols_re.search(raw_line)
                if m:
                    findings.append(
                        Finding(
                            rule_id="GRD-12",
                            severity=SEVERITY_BLOCKER,
                            scope="uc",
                            file=rel,
                            line=line_no,
                            message=f"Physical DB column identifier '{m.group(0)}' inside black-box UC body.",
                            remediation="Use conceptual domain attribute phrasing instead of snake_case DB column.",
                        )
                    )

            # 2. Infrastructure / framework terms
            im = _UC_INFRA_TECH_RE.search(raw_line)
            if im:
                findings.append(
                    Finding(
                        rule_id="GRD-12",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=line_no,
                        message=f"Infrastructure/implementation leak '{im.group(0)}' inside black-box UC body.",
                        remediation="Remove DB/UI/framework implementation details from use-case behavior.",
                    )
                )

            # 3. Class.Method() calls
            cm = _UC_CLASS_METHOD_RE.search(raw_line)
            if cm:
                findings.append(
                    Finding(
                        rule_id="GRD-12",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=line_no,
                        message=f"Code method invocation '{cm.group(0)}' inside black-box UC body.",
                        remediation="Describe system behavior in domain terms without Class.Method() syntax.",
                    )
                )

            # 4. /api/ routes, --dt-* tokens, CMP-* IDs, HTML tags
            am = _UC_API_ROUTE_RE.search(raw_line)
            if am:
                findings.append(
                    Finding(
                        rule_id="GRD-12",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=line_no,
                        message=f"REST API route '{am.group(1)}' leaked into black-box UC body.",
                        remediation="Keep REST endpoints in SCR-*.md / DT-ARQ-CMP-DOC-001.md.",
                    )
                )
            tm = _UC_CSS_TOKEN_RE.search(raw_line)
            if tm:
                findings.append(
                    Finding(
                        rule_id="GRD-12",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=line_no,
                        message=f"Design token '{tm.group(0)}' leaked into black-box UC body.",
                        remediation="Keep CSS design tokens in DT-UI-DS-DOC-001.md and SCR-*.md.",
                    )
                )
            cmp_m = _UC_CMP_ID_RE.search(raw_line)
            if cmp_m:
                findings.append(
                    Finding(
                        rule_id="GRD-12",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=line_no,
                        message=f"UI component ID '{cmp_m.group(0)}' leaked into black-box UC body.",
                        remediation="Keep CMP-* component IDs inside SCR-*.md.",
                    )
                )
            hm = _UC_HTML_TAG_RE.search(raw_line)
            if hm:
                findings.append(
                    Finding(
                        rule_id="GRD-12",
                        severity=SEVERITY_BLOCKER,
                        scope="uc",
                        file=rel,
                        line=line_no,
                        message=f"Raw HTML tag '{hm.group(0)}' leaked into black-box UC body.",
                        remediation="Remove raw HTML tags from use-case specification.",
                    )
                )

            # 5. Inline SCR-* clutter inside §3 Main Flow or §4 Alternate Flows steps
            if current_h2.startswith("## 3.") or current_h2.startswith("## 4."):
                scr_m = _SCR_ID_RE.search(raw_line)
                if scr_m:
                    findings.append(
                        Finding(
                            rule_id="GRD-12",
                            severity=SEVERITY_BLOCKER,
                            scope="uc",
                            file=rel,
                            line=line_no,
                            message=f"Inline screen ID '{scr_m.group(0)}' inside '{current_h2}' flow steps.",
                            remediation="Keep SCR-* links exclusively in §6 Related Screens.",
                        )
                    )

    return findings
