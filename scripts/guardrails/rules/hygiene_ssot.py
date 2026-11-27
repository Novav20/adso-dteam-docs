"""
Layer 2 Pure Guardrail Rules: Links, UL Purity, Design Tokens/WCAG, UI Hygiene & SRS (`GRD-17`..`GRD-21`).

Scopes: `links`, `ul`, `tokens`, `srs`.
"""

from __future__ import annotations

import posixpath
import re
from pathlib import PurePosixPath

from ..config import (
    APPROVED_COLOR_PALETTE,
    MVP_APPROVED_SCREENS,
    MVP_APPROVED_UCS,
    PLANNED_STUBS,
    SSOT_PATHS,
)
from ..models import SEVERITY_BLOCKER, SEVERITY_WARNING, Finding
from ..parsers import RepoIndex
from ..parsers.markdown_parser import ParsedMarkdownDoc

# ---------------------------------------------------------------------------
# Shared Helpers
# ---------------------------------------------------------------------------

_OUT_OF_SCOPE_HEADING_RE = re.compile(
    r"^###\s+Use Cases Planned for Later Phases\b", re.IGNORECASE
)
_ADR_ALT_HEADING_RE = re.compile(
    r"^##\s+(?:Alternatives\s+Considered|Rejected\s+Alternatives|Superseded)\b",
    re.IGNORECASE,
)
_PROHIBITION_CTX_RE = re.compile(
    r"(?:discarded|rejected|not\s+allowed|forbidden|prohibited|excluded|avoid|"
    r"superseded|replaced\s+by|instead\s+of|decouple|legacy|obsolete)",
    re.IGNORECASE,
)


def _strip_planned_and_code(text: str) -> str:
    """Mask out planned post-MVP sections and fenced code blocks while keeping 1-based lines."""
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    in_planned = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence:
            out.append("")
            continue
        if _OUT_OF_SCOPE_HEADING_RE.match(stripped):
            in_planned = True
            out.append("")
            continue
        if in_planned and re.match(r"^#{1,3}\s+", stripped):
            in_planned = False
        out.append("" if in_planned else line)
    return "\n".join(out)


def _strip_adr_alternatives(text: str) -> str:
    """Mask out ADR `supersedes:` frontmatter and `Alternatives Considered` sections."""
    lines = text.splitlines()
    out: list[str] = []
    in_alt = False
    for line in lines:
        if re.match(r"^\s*supersedes\s*:", line, re.IGNORECASE):
            out.append("")
            continue
        if _ADR_ALT_HEADING_RE.match(line.strip()):
            in_alt = True
            out.append("")
            continue
        if in_alt and re.match(r"^##\s+", line.strip()):
            in_alt = False
        out.append("" if in_alt else line)
    return "\n".join(out)


def _is_planned_stub(path_str: str) -> bool:
    norm = path_str.replace("\\", "/")
    return any(re.search(pat, norm) for pat in PLANNED_STUBS)


def _repo_has_artifact(repo_files: frozenset[str], artifact_id: str) -> bool:
    if re.fullmatch(r"ASR-0*(?:1|2)", artifact_id):
        return "architecture/asr/DT-ARQ-ASR-001.md" in repo_files
    for rf in repo_files:
        name = rf.rsplit("/", 1)[-1]
        stem = name.split(".", 1)[0]
        if stem == artifact_id or name.startswith(f"{artifact_id}-") or name.startswith(f"{artifact_id}."):
            return True
    return False


# ---------------------------------------------------------------------------
# GRD-17: Relative Links, GFM Anchors, Artifact IDs & Zero Body Wikilinks
# ---------------------------------------------------------------------------

_ARTIFACT_ID_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"(?<![A-Z0-9-])UC-[A-Z]+-\d+\b"), "Use Case"),
    (re.compile(r"(?<![A-Z0-9-])SCR-[A-Z]+-\d+\b"), "Screen"),
    (re.compile(r"(?<![A-Z0-9-])ADR-\d+\b"), "Architecture Decision Record"),
    (re.compile(r"(?<![A-Z0-9-])DT-(?:[A-Z]+-){1,3}(?:DOC-)?\d+\b"), "DTEAM Artifact"),
)
_DT_MALFORMED_RE = re.compile(r"\bDT-[A-Za-z0-9-]+\b")
_WINDOWS_ABS_RE = re.compile(r"^[A-Za-z]:[\\/]")


def _strip_fm_planned_and_code(doc: ParsedMarkdownDoc) -> str:
    """Mask frontmatter, planned post-MVP sections, and fenced code while keeping 1-based lines."""
    masked = _strip_planned_and_code(doc.raw_text)
    if doc.frontmatter_line_count <= 0:
        return masked
    lines = masked.splitlines()
    for i in range(min(doc.frontmatter_line_count, len(lines))):
        lines[i] = ""
    return "\n".join(lines)


def evaluate_grd_17(index: RepoIndex) -> list[Finding]:
    """Validate relative links, GFM section anchors, artifact IDs, and ban body wikilinks."""
    findings: list[Finding] = []

    for rel, doc in sorted(index.markdown_docs.items()):
        # 1. Ban Obsidian wikilinks inside document body (frontmatter wikilinks remain valid)
        for wref in doc.body_wikilinks:
            findings.append(
                Finding(
                    rule_id="GRD-17",
                    severity=SEVERITY_BLOCKER,
                    scope="links",
                    file=rel,
                    line=wref.line,
                    message=f"Prohibited body wikilink `{wref.raw}` found outside YAML frontmatter.",
                    remediation="Replace body wikilinks with standard relative Markdown `[label](path#anchor)` links.",
                )
            )

        # 2. Validate relative Markdown links and GFM section anchors
        parent_dir = PurePosixPath(rel).parent.as_posix()
        for link in doc.links:
            if link.is_external:
                continue

            raw_url = link.url.strip()
            if not raw_url:
                findings.append(
                    Finding(
                        rule_id="GRD-17",
                        severity=SEVERITY_BLOCKER,
                        scope="links",
                        file=rel,
                        line=link.line,
                        message="Empty Markdown link target.",
                        remediation="Provide a valid relative path or `#anchor` target.",
                    )
                )
                continue

            t_path = link.target_path.strip()
            if t_path.startswith("/") or _WINDOWS_ABS_RE.match(t_path):
                findings.append(
                    Finding(
                        rule_id="GRD-17",
                        severity=SEVERITY_BLOCKER,
                        scope="links",
                        file=rel,
                        line=link.line,
                        message=f"Non-relative link path `{link.url}` is prohibited.",
                        remediation="Use a repository-relative path (e.g., `../path/file.md`).",
                    )
                )
                continue

            if not t_path:
                norm_target = rel
            else:
                joined = t_path if parent_dir == "." else f"{parent_dir}/{t_path}"
                norm_target = posixpath.normpath(joined)

            if norm_target.startswith(".."):
                findings.append(
                    Finding(
                        rule_id="GRD-17",
                        severity=SEVERITY_BLOCKER,
                        scope="links",
                        file=rel,
                        line=link.line,
                        message=f"Link `{link.url}` resolves outside the repository root (`{norm_target}`).",
                        remediation="Fix the relative path so it resolves within the repository.",
                    )
                )
                continue

            file_exists = norm_target in index.repo_files
            dir_prefix = norm_target.rstrip("/") + "/"
            dir_exists = (not file_exists) and any(
                rf.startswith(dir_prefix) for rf in index.repo_files
            )

            if not file_exists and not dir_exists:
                if _is_planned_stub(t_path) or _is_planned_stub(norm_target):
                    continue
                findings.append(
                    Finding(
                        rule_id="GRD-17",
                        severity=SEVERITY_BLOCKER,
                        scope="links",
                        file=rel,
                        line=link.line,
                        message=f"Broken relative link `{link.url}` -> `{norm_target}` does not exist.",
                        remediation="Update the link target path or restore the missing artifact.",
                    )
                )
                continue

            if link.anchor and norm_target in index.markdown_docs:
                target_doc = index.markdown_docs[norm_target]
                if link.anchor not in target_doc.anchors:
                    findings.append(
                        Finding(
                            rule_id="GRD-17",
                            severity=SEVERITY_BLOCKER,
                            scope="links",
                            file=rel,
                            line=link.line,
                            message=(
                                f"Broken section anchor `{link.url}`: "
                                f"`#{link.anchor}` not found in `{norm_target}`."
                            ),
                            remediation="Update the `#anchor` fragment to match the exact GFM heading slug.",
                        )
                    )

        # 3. Validate artifact IDs referenced in normative documents (skip backlog/README trackers)
        if rel == SSOT_PATHS.todo_md or rel.startswith("scripts/"):
            continue

        scoped_text = _strip_fm_planned_and_code(doc)
        seen_ids: set[str] = set()
        for pat, label in _ARTIFACT_ID_PATTERNS:
            for m in pat.finditer(scoped_text):
                art_id = m.group(0)
                if art_id in seen_ids:
                    continue
                seen_ids.add(art_id)
                if not _repo_has_artifact(index.repo_files, art_id):
                    line_no = scoped_text[: m.start()].count("\n") + 1
                    findings.append(
                        Finding(
                            rule_id="GRD-17",
                            severity=SEVERITY_BLOCKER,
                            scope="links",
                            file=rel,
                            line=line_no,
                            message=f"{label} `{art_id}` is referenced but does not exist in the repository.",
                            remediation=f"Create the missing `{art_id}` artifact or correct the reference.",
                        )
                    )

        # Catch malformed `DT-*` tokens missing numeric segment or proper structure
        for m in _DT_MALFORMED_RE.finditer(scoped_text):
            tok = m.group(0)
            if tok.startswith("DT-") and not re.search(r"-\d+(?:-[a-z0-9-]+)?$", tok):
                line_no = scoped_text[: m.start()].count("\n") + 1
                findings.append(
                    Finding(
                        rule_id="GRD-17",
                        severity=SEVERITY_BLOCKER,
                        scope="links",
                        file=rel,
                        line=line_no,
                        message=f"Malformed DTEAM artifact identifier `{tok}` (missing numeric suffix).",
                        remediation="Use full canonical 4-segment IDs such as `DT-DM-DOC-001` or `DT-ARQ-CMP-DOC-001`.",
                    )
                )

    return findings


# ---------------------------------------------------------------------------
# GRD-18: Dimension-Agnostic 2D/3D UL & Layer Purity
# ---------------------------------------------------------------------------

_DIM_COUPLED_RE = re.compile(
    r"\b(?:2D|3D|SVG|CanvasViewport2D|canvas|wireframe|webgl|three\.js)\b",
    re.IGNORECASE,
)
_DOMAIN_LAYER_LEAK_RE = re.compile(
    r"\b(?:PostgreSQL|TimescaleDB|SQLCipher|SyncOutbox|EF\s*Core|Entity\s*Framework|"
    r"Blazor|Razor|SignalR|Discrete\s+Switching\s*\(UI\))\b|"
    r"\.razor\b|--dt-[a-z0-9-]+|/api/v1/[A-Za-z0-9_./{}-]+",
    re.IGNORECASE,
)
_ERD_PATH_REF_RE = re.compile(r"DT-ERD-DOC-001(?:\.md)?(?:#[A-Za-z0-9-]+)?", re.IGNORECASE)


def evaluate_grd_18(index: RepoIndex) -> list[Finding]:
    """Enforce dimension-agnostic 2D/3D ubiquitous language and domain/use-case layer purity."""
    findings: list[Finding] = []

    domain_targets: list[tuple[str, ParsedMarkdownDoc | None]] = [
        (SSOT_PATHS.ul_doc, index.markdown_docs.get(SSOT_PATHS.ul_doc)),
        (SSOT_PATHS.dm_class_doc, index.markdown_docs.get(SSOT_PATHS.dm_class_doc)),
        (SSOT_PATHS.dm_state_doc, index.markdown_docs.get(SSOT_PATHS.dm_state_doc)),
    ]
    for rel, doc in sorted(index.usecase_docs.items()):
        domain_targets.append((rel, doc))

    for rel, doc in domain_targets:
        if doc is None:
            continue
        for line_no, raw_line in enumerate(doc.raw_text.splitlines(), start=1):
            # Ignore YAML frontmatter metadata lines
            if line_no <= doc.frontmatter_line_count:
                continue
            if _PROHIBITION_CTX_RE.search(raw_line):
                continue

            # Strip markdown link URLs so relative paths like `../DT-UI-SVG-DOC-001.md` don't trigger
            clean_line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw_line)

            dim_match = _DIM_COUPLED_RE.search(clean_line)
            if dim_match:
                findings.append(
                    Finding(
                        rule_id="GRD-18",
                        severity=SEVERITY_BLOCKER,
                        scope="ul",
                        file=rel,
                        line=line_no,
                        message=(
                            f"Rendering-coupled term `{dim_match.group(0)}` in dimension-agnostic "
                            "domain/use-case artifact."
                        ),
                        remediation=(
                            "Replace with dimension-agnostic terms (`Spatial Representation`, "
                            "`Spatial Mapping`, `Spatial Viewport`), keeping `MeshMapping` only as entity ID."
                        ),
                    )
                )

            # Layer purity applies strictly to UL and Domain Class/State models
            if rel in (SSOT_PATHS.ul_doc, SSOT_PATHS.dm_class_doc, SSOT_PATHS.dm_state_doc):
                leak_line = _ERD_PATH_REF_RE.sub("", clean_line)
                leak_match = _DOMAIN_LAYER_LEAK_RE.search(leak_line)
                if leak_match:
                    findings.append(
                        Finding(
                            rule_id="GRD-18",
                            severity=SEVERITY_BLOCKER,
                            scope="ul",
                            file=rel,
                            line=line_no,
                            message=(
                                f"Infrastructure/UI implementation leak `{leak_match.group(0)}` "
                                "inside domain/UL specification."
                            ),
                            remediation=(
                                "Express persistence/sync/UI constraints via domain policies or normative "
                                "references (`TR-001`, `DT-ERD-DOC-001`, `DT-UI-DS-DOC-001`)."
                            ),
                        )
                    )

    # Audit requirements/data/srs.csv for dimension-coupled terms (WARNING since Notion-exported CSV)
    for row_idx, row in enumerate(index.srs_rows, start=2):
        req_id = (row.get("Req ID") or f"row-{row_idx}").strip()
        desc = row.get("Description") or ""
        m = _DIM_COUPLED_RE.search(desc)
        if m:
            findings.append(
                Finding(
                    rule_id="GRD-18",
                    severity=SEVERITY_WARNING,
                    scope="ul",
                    file=SSOT_PATHS.srs_csv,
                    line=row_idx,
                    message=(
                        f"SRS requirement `{req_id}` contains rendering-coupled term `{m.group(0)}`."
                    ),
                    remediation="Align SRS requirement wording to dimension-agnostic spatial terminology.",
                )
            )

    return findings


# ---------------------------------------------------------------------------
# GRD-19: UI Foundation Docs, --dt-* Token Parity & WCAG 2.1 Contrast
# ---------------------------------------------------------------------------

_SQL_TABLE_LEAK_RE = re.compile(r"\b(?:tax|mtto|inv|vis|adm)\.[a-z][a-z0-9_]+\b")
_HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")
_SYM_ICON_RE = re.compile(r"\bsym-icon-[a-z0-9-]+\b")
_RULE_PREFIX_RE = re.compile(r"\*\*Rule\s+\d+\s*[—-]")
_DS_RAZOR_LEAK_RE = re.compile(
    r"\b(?:ViewportToolbar|UserProfileButton|CartographicHud)\b|\.razor\b"
)
_NAV_TECH_LEAK_RE = re.compile(r"\b(?:MAUI|Blazor|SQLCipher|C#)\b")
_CONCRETE_TOKEN_RE = re.compile(r"--dt-(?:[a-z0-9]+-)*[a-z0-9]+\b(?!-(?:\*|\{|[A-Z]\b))")


def _relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

    def _lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def _contrast_ratio(hex1: str, hex2: str) -> float:
    l1 = _relative_luminance(hex1)
    l2 = _relative_luminance(hex2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def _resolve_token_hex(
    table: dict[str, str], token: str, depth: int = 0
) -> tuple[str | None, str | None]:
    if depth > 6:
        return None, f"Circular token reference on `{token}`."
    if token not in table:
        return None, f"Undefined referenced token `{token}`."
    val = table[token].strip()
    if _HEX_RE.fullmatch(val):
        return val.upper(), None
    m = re.fullmatch(r"var\((--dt-[a-z0-9-]+)\)", val)
    if m:
        return _resolve_token_hex(table, m.group(1), depth + 1)
    return val, None


def evaluate_grd_19(index: RepoIndex) -> list[Finding]:
    """Audit UI foundation docs, `--dt-*` token parity, palette compliance, and WCAG 2.1 AA contrast."""
    findings: list[Finding] = []

    # --- A1. DT-UI-DS-DOC-001.md ---
    ds_doc = index.markdown_docs.get(SSOT_PATHS.ui_ds_doc)
    ds_declared_tokens: set[str] = set()
    if ds_doc is None:
        findings.append(
            Finding(
                rule_id="GRD-19",
                severity=SEVERITY_BLOCKER,
                scope="tokens",
                file=SSOT_PATHS.ui_ds_doc,
                line=None,
                message="Missing Design System SSoT `ui-ux/DT-UI-DS-DOC-001.md`.",
                remediation="Restore `ui-ux/DT-UI-DS-DOC-001.md`.",
            )
        )
    else:
        in_sec_31 = False
        seen_tokens: dict[str, int] = {}
        family_lum: dict[str, list[tuple[int, str, str, float]]] = {"gray": [], "slate": []}
        approved_upper = {c.upper() for c in APPROVED_COLOR_PALETTE}

        for idx, line in enumerate(ds_doc.raw_text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("### 3.1."):
                in_sec_31 = True
            elif stripped.startswith("### ") and not stripped.startswith("### 3.1."):
                in_sec_31 = False

            if _SYM_ICON_RE.search(line):
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_ds_doc,
                        line=idx,
                        message="Forbidden `#sym-icon-*` reference in Design System spec.",
                        remediation="Use `#icon-*` symbol identifiers matching `ui-ux/assets/icons.svg`.",
                    )
                )

            sql_m = _SQL_TABLE_LEAK_RE.search(line)
            if sql_m:
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_ds_doc,
                        line=idx,
                        message=f"SQL persistence table leak `{sql_m.group(0)}` in Design System spec.",
                        remediation="Remove physical schema/table names from Design System documentation.",
                    )
                )

            if _DS_RAZOR_LEAK_RE.search(line):
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_ds_doc,
                        line=idx,
                        message="Framework/Razor component leak in Design System spec.",
                        remediation="Move Razor component contracts to `ui-ux/contracts/DT-UI-CTR-001.md`.",
                    )
                )

            for match in _HEX_RE.finditer(line):
                hex_val = match.group(0).upper()
                if not in_sec_31:
                    if not (hex_val in ("#FFFFFF", "#000000") and "prohibited" in line.lower()):
                        findings.append(
                            Finding(
                                rule_id="GRD-19",
                                severity=SEVERITY_BLOCKER,
                                scope="tokens",
                                file=SSOT_PATHS.ui_ds_doc,
                                line=idx,
                                message=f"Raw HEX `{hex_val}` outside Section 3.1 Primitive Palette.",
                                remediation="Reference semantic `--dt-color-*` tokens instead of raw HEX.",
                            )
                        )
                elif hex_val not in approved_upper and not (
                    hex_val in ("#FFFFFF", "#000000") and "prohibited" in line.lower()
                ):
                    findings.append(
                        Finding(
                            rule_id="GRD-19",
                            severity=SEVERITY_WARNING,
                            scope="tokens",
                            file=SSOT_PATHS.ui_ds_doc,
                            line=idx,
                            message=f"HEX color `{hex_val}` is outside `APPROVED_COLOR_PALETTE`.",
                            remediation="Use an approved DT-UI-DS-DOC-001 v2.2/v2.3 primitive color.",
                        )
                    )

            for tm in _CONCRETE_TOKEN_RE.finditer(line):
                ds_declared_tokens.add(tm.group(0))

            if stripped.startswith("|"):
                cells = [c.strip().strip("`") for c in stripped.strip("|").split("|")]
                if "var(" in stripped:
                    findings.append(
                        Finding(
                            rule_id="GRD-19",
                            severity=SEVERITY_BLOCKER,
                            scope="tokens",
                            file=SSOT_PATHS.ui_ds_doc,
                            line=idx,
                            message="CSS `var(...)` syntax prohibited in DS-DOC tables; use bare `--dt-*` token names.",
                            remediation="Replace `var(--dt-...)` with bare `--dt-...` identifiers.",
                        )
                    )
                lower_line = stripped.lower()
                if "dark theme" in lower_line and "light theme" in lower_line:
                    if lower_line.index("light theme") < lower_line.index("dark theme"):
                        findings.append(
                            Finding(
                                rule_id="GRD-19",
                                severity=SEVERITY_BLOCKER,
                                scope="tokens",
                                file=SSOT_PATHS.ui_ds_doc,
                                line=idx,
                                message="Inverted theme columns (Light before Dark); standard order is Dark | Light.",
                                remediation="Reorder table columns to Dark Theme | Light Theme.",
                            )
                        )
                if in_sec_31 and len(cells) >= 2 and cells[0].startswith("--dt-primitive-"):
                    tok, hex_val = cells[0], cells[1]
                    if _HEX_RE.fullmatch(hex_val):
                        for fam in ("gray", "slate"):
                            if tok.startswith(f"--dt-primitive-{fam}-"):
                                family_lum[fam].append((idx, tok, hex_val, _relative_luminance(hex_val)))

                if len(cells) >= 2:
                    tok_cand = (
                        cells[0]
                        if cells[0].startswith("--dt-")
                        else (cells[1] if cells[1].startswith("--dt-") else "")
                    )
                    if tok_cand and not stripped.startswith("| **"):
                        if tok_cand in seen_tokens:
                            findings.append(
                                Finding(
                                    rule_id="GRD-19",
                                    severity=SEVERITY_BLOCKER,
                                    scope="tokens",
                                    file=SSOT_PATHS.ui_ds_doc,
                                    line=idx,
                                    message=(
                                        f"Duplicate token declaration `{tok_cand}` "
                                        f"(first declared at line {seen_tokens[tok_cand]})."
                                    ),
                                    remediation="Consolidate duplicate token rows in `DT-UI-DS-DOC-001.md`.",
                                )
                            )
                        else:
                            seen_tokens[tok_cand] = idx

        for fam, entries in family_lum.items():
            for prev, curr in zip(entries, entries[1:]):
                if curr[3] < prev[3] - 1e-6:
                    findings.append(
                        Finding(
                            rule_id="GRD-19",
                            severity=SEVERITY_BLOCKER,
                            scope="tokens",
                            file=SSOT_PATHS.ui_ds_doc,
                            line=curr[0],
                            message=(
                                f"Non-monotonic luminance in `{fam}` scale: "
                                f"`{curr[1]}` ({curr[2]}) is darker than `{prev[1]}` ({prev[2]})."
                            ),
                            remediation="Order primitive color scale entries monotonically from darkest to lightest.",
                        )
                    )

    # --- A2. DT-UI-SVG-DOC-001.md ---
    svg_doc = index.markdown_docs.get(SSOT_PATHS.ui_svg_doc)
    if svg_doc is not None:
        last_sub: dict[int, int] = {}
        for idx, line in enumerate(svg_doc.raw_text.splitlines(), start=1):
            if _SYM_ICON_RE.search(line):
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_svg_doc,
                        line=idx,
                        message="Forbidden `#sym-icon-*` reference in SVG ingestion spec.",
                        remediation="Use `#icon-*` symbol identifiers.",
                    )
                )
            hex_m = _HEX_RE.search(line)
            if hex_m:
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_svg_doc,
                        line=idx,
                        message=f"Raw HEX `{hex_m.group(0)}` prohibited in SVG spec; reference DS-DOC tokens.",
                        remediation="Replace raw HEX with `--dt-*` design tokens.",
                    )
                )
            sql_m = _SQL_TABLE_LEAK_RE.search(line)
            if sql_m:
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_svg_doc,
                        line=idx,
                        message=f"SQL persistence table leak `{sql_m.group(0)}` in SVG spec.",
                        remediation="Remove physical SQL table names from SVG ingestion spec.",
                    )
                )
            if re.search(r"\bC#\b", line):
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_svg_doc,
                        line=idx,
                        message="Language implementation leak (`C#`) in SVG contract.",
                        remediation="Keep `DT-UI-SVG-DOC-001.md` framework/language-agnostic.",
                    )
                )
            if "is_safety_critical" in line:
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_svg_doc,
                        line=idx,
                        message="Non-canonical attribute `is_safety_critical`; use `data-safety-critical`.",
                        remediation="Replace `is_safety_critical` with `data-safety-critical`.",
                    )
                )
            if _RULE_PREFIX_RE.search(line):
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_svg_doc,
                        line=idx,
                        message="Redundant copy-paste `Rule N —` prefix.",
                        remediation="Remove numbered `Rule N —` prefixes.",
                    )
                )
            sub_match = re.match(r"^###\s+(\d+)\.(\d+)\b", line.strip())
            if sub_match:
                major, minor = int(sub_match.group(1)), int(sub_match.group(2))
                expected = last_sub.get(major, 0) + 1
                if minor != expected:
                    findings.append(
                        Finding(
                            rule_id="GRD-19",
                            severity=SEVERITY_BLOCKER,
                            scope="tokens",
                            file=SSOT_PATHS.ui_svg_doc,
                            line=idx,
                            message=(
                                f"Skipped sub-section numbering (found {major}.{minor}, "
                                f"expected {major}.{expected})."
                            ),
                            remediation="Renumber sub-sections sequentially.",
                        )
                    )
                last_sub[major] = minor

    # --- A3. DT-UI-NAV-DOC-001.md ---
    nav_doc = index.markdown_docs.get(SSOT_PATHS.ui_nav_doc)
    if nav_doc is not None:
        for idx, line in enumerate(nav_doc.raw_text.splitlines(), start=1):
            if _SYM_ICON_RE.search(line):
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_nav_doc,
                        line=idx,
                        message="Forbidden `#sym-icon-*` reference in Navigation spec.",
                        remediation="Use `#icon-*` symbol identifiers.",
                    )
                )
            sql_m = _SQL_TABLE_LEAK_RE.search(line)
            if sql_m:
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_nav_doc,
                        line=idx,
                        message=f"SQL persistence table leak `{sql_m.group(0)}` in Navigation spec.",
                        remediation="Remove physical SQL table names from Navigation spec.",
                    )
                )
            tech_m = _NAV_TECH_LEAK_RE.search(line)
            if tech_m:
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_nav_doc,
                        line=idx,
                        message=f"Framework/storage leak (`{tech_m.group(0)}`) in Navigation spec.",
                        remediation="Keep `DT-UI-NAV-DOC-001.md` framework-agnostic.",
                    )
                )
            if "Isolation Points == TRUE" in line:
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.ui_nav_doc,
                        line=idx,
                        message=(
                            "Non-canonical LOTO guard `Isolation Points == TRUE`; "
                            "use `IsolationStatus == VERIFIED_ZERO_ENERGY`."
                        ),
                        remediation="Replace with `IsolationStatus == VERIFIED_ZERO_ENERGY`.",
                    )
                )

    # --- B. --dt-* Token Parity & Prototype Asset Coverage ---
    if index.tokens is None:
        findings.append(
            Finding(
                rule_id="GRD-19",
                severity=SEVERITY_BLOCKER,
                scope="tokens",
                file=SSOT_PATHS.tokens_css,
                line=None,
                message="Missing `ui-ux/assets/tokens.css`.",
                remediation="Regenerate `ui-ux/assets/tokens.css` from `DT-UI-DS-DOC-001.md`.",
            )
        )
        return findings

    toks = index.tokens
    for dup in toks.duplicate_light:
        findings.append(
            Finding(
                rule_id="GRD-19",
                severity=SEVERITY_BLOCKER,
                scope="tokens",
                file=SSOT_PATHS.tokens_css,
                line=None,
                message=f"Duplicate `:root` (light) CSS token `{dup}` in `tokens.css`.",
                remediation="Remove duplicate declaration and regenerate `tokens.css`.",
            )
        )
    for dup in toks.duplicate_dark:
        findings.append(
            Finding(
                rule_id="GRD-19",
                severity=SEVERITY_BLOCKER,
                scope="tokens",
                file=SSOT_PATHS.tokens_css,
                line=None,
                message=f"Duplicate `[data-theme=\"dark\"]` CSS token `{dup}` in `tokens.css`.",
                remediation="Remove duplicate declaration and regenerate `tokens.css`.",
            )
        )

    # Light vs Dark semantic coverage parity
    semantic_light = {
        k for k in toks.light_tokens if k.startswith(("--dt-color-", "--dt-shadow-"))
    }
    semantic_dark = {
        k for k in toks.dark_tokens if k.startswith(("--dt-color-", "--dt-shadow-"))
    }
    for missing_dark in sorted(semantic_light - semantic_dark):
        findings.append(
            Finding(
                rule_id="GRD-19",
                severity=SEVERITY_BLOCKER,
                scope="tokens",
                file=SSOT_PATHS.tokens_css,
                line=None,
                message=f"Semantic token `{missing_dark}` exists in `:root` (light) but is missing from `[data-theme=\"dark\"]`.",
                remediation="Add dark theme override for every `--dt-color-*` and `--dt-shadow-*` token.",
            )
        )
    for missing_light in sorted(semantic_dark - semantic_light):
        findings.append(
            Finding(
                rule_id="GRD-19",
                severity=SEVERITY_BLOCKER,
                scope="tokens",
                file=SSOT_PATHS.tokens_css,
                line=None,
                message=f"Semantic token `{missing_light}` exists in `[data-theme=\"dark\"]` but is missing from `:root` (light).",
                remediation="Add `:root` light theme definition for every dark token.",
            )
        )

    if ds_declared_tokens:
        for missing_in_css in sorted(ds_declared_tokens - toks.all_tokens):
            findings.append(
                Finding(
                    rule_id="GRD-19",
                    severity=SEVERITY_BLOCKER,
                    scope="tokens",
                    file=SSOT_PATHS.tokens_css,
                    line=None,
                    message=f"Token `{missing_in_css}` documented in `DT-UI-DS-DOC-001.md` is missing from `tokens.css`.",
                    remediation="Regenerate `tokens.css` from `DT-UI-DS-DOC-001.md`.",
                )
            )
        for missing_in_ds in sorted(toks.all_tokens - ds_declared_tokens):
            findings.append(
                Finding(
                    rule_id="GRD-19",
                    severity=SEVERITY_WARNING,
                    scope="tokens",
                    file=SSOT_PATHS.ui_ds_doc,
                    line=None,
                    message=f"Token `{missing_in_ds}` in `tokens.css` is not documented in `DT-UI-DS-DOC-001.md`.",
                    remediation="Document the token in `DT-UI-DS-DOC-001.md` or remove stale token from `tokens.css`.",
                )
            )

    for rel_asset, asset in sorted(index.prototype_assets.items()):
        if asset.kind == "css":
            local_decls = set(re.findall(r"^\s*(--dt-[a-z0-9-]+)\s*:", asset.content, re.MULTILINE))
            used_vars = dict.fromkeys(re.findall(r"var\(\s*(--dt-[a-z0-9-]+)", asset.content))
            for ref_tok in used_vars:
                if ref_tok not in toks.all_tokens and ref_tok not in local_decls:
                    has_fallback = bool(
                        re.search(rf"var\(\s*{re.escape(ref_tok)}\s*,", asset.content)
                    )
                    findings.append(
                        Finding(
                            rule_id="GRD-19",
                            severity=SEVERITY_WARNING if has_fallback else SEVERITY_BLOCKER,
                            scope="tokens",
                            file=rel_asset,
                            line=None,
                            message=f"Prototype CSS references undefined token `{ref_tok}`.",
                            remediation="Use an approved `--dt-*` token defined in `tokens.css`.",
                        )
                    )
        else:
            for ref_tok in asset.referenced_tokens:
                if ref_tok not in toks.all_tokens:
                    findings.append(
                        Finding(
                            rule_id="GRD-19",
                            severity=SEVERITY_BLOCKER,
                            scope="tokens",
                            file=rel_asset,
                            line=None,
                            message=f"Prototype asset references undefined CSS token `{ref_tok}`.",
                            remediation="Use an approved `--dt-*` token defined in `tokens.css`.",
                        )
                    )

    # --- C. Dynamic WCAG 2.1 AA Contrast Matrix ---
    light_map = dict(toks.light_tokens)
    dark_map = {**toks.light_tokens, **toks.dark_tokens}

    surfaces = (
        ("Canvas", "--dt-color-bg-canvas"),
        ("Base", "--dt-color-surface-base"),
        ("Card", "--dt-color-surface-card"),
    )
    fg_checks = (
        ("--dt-color-text-primary", 4.5, "Std Text"),
        ("--dt-color-text-body", 4.5, "Std Text"),
        ("--dt-color-text-muted", 4.5, "Std Text"),
        ("--dt-color-alarm-critical", 3.0, "UI/Graph"),
        ("--dt-color-alarm-warning", 3.0, "UI/Graph"),
        ("--dt-color-state-info", 3.0, "UI/Graph"),
        ("--dt-color-state-success", 3.0, "UI/Graph"),
        ("--dt-color-border-focus", 3.0, "UI/Graph"),
    )
    badge_checks = (
        ("--dt-color-alarm-text-critical", "--dt-color-alarm-critical", 3.0),
        ("--dt-color-alarm-text-warning", "--dt-color-alarm-warning", 4.5),
    )

    for theme_name, theme_map in (("Light", light_map), ("Dark", dark_map)):
        for surf_label, bg_tok in surfaces:
            bg_hex, bg_err = _resolve_token_hex(theme_map, bg_tok)
            if bg_err or not bg_hex or not _HEX_RE.fullmatch(bg_hex):
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.tokens_css,
                        line=None,
                        message=f"[{theme_name}] Could not resolve surface `{bg_tok}` to hex ({bg_err or bg_hex}).",
                        remediation="Fix token alias chain in `ui-ux/assets/tokens.css`.",
                    )
                )
                continue
            for fg_tok, target, kind in fg_checks:
                fg_hex, fg_err = _resolve_token_hex(theme_map, fg_tok)
                if fg_err or not fg_hex or not _HEX_RE.fullmatch(fg_hex):
                    findings.append(
                        Finding(
                            rule_id="GRD-19",
                            severity=SEVERITY_BLOCKER,
                            scope="tokens",
                            file=SSOT_PATHS.tokens_css,
                            line=None,
                            message=f"[{theme_name}] Could not resolve foreground `{fg_tok}` to hex ({fg_err or fg_hex}).",
                            remediation="Fix token alias chain in `ui-ux/assets/tokens.css`.",
                        )
                    )
                    continue
                ratio = _contrast_ratio(bg_hex, fg_hex)
                if ratio < target:
                    findings.append(
                        Finding(
                            rule_id="GRD-19",
                            severity=SEVERITY_BLOCKER,
                            scope="tokens",
                            file=SSOT_PATHS.tokens_css,
                            line=None,
                            message=(
                                f"[{theme_name}] WCAG 2.1 AA contrast failure on {surf_label} ({bg_tok}={bg_hex}) "
                                f"with {fg_tok}={fg_hex}: {ratio:.2f}:1 < {target:.1f}:1 ({kind})."
                            ),
                            remediation="Adjust primitive palette mapping in `DT-UI-DS-DOC-001.md` and regenerate `tokens.css`.",
                        )
                    )

        for fg_tok, bg_tok, target in badge_checks:
            fg_hex, fg_err = _resolve_token_hex(theme_map, fg_tok)
            bg_hex, bg_err = _resolve_token_hex(theme_map, bg_tok)
            if (
                fg_err
                or bg_err
                or not fg_hex
                or not bg_hex
                or not _HEX_RE.fullmatch(fg_hex)
                or not _HEX_RE.fullmatch(bg_hex)
            ):
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.tokens_css,
                        line=None,
                        message=f"[{theme_name}] Could not resolve badge tokens `{fg_tok}` / `{bg_tok}`.",
                        remediation="Fix badge token definitions in `ui-ux/assets/tokens.css`.",
                    )
                )
                continue
            ratio = _contrast_ratio(bg_hex, fg_hex)
            if ratio < target:
                findings.append(
                    Finding(
                        rule_id="GRD-19",
                        severity=SEVERITY_BLOCKER,
                        scope="tokens",
                        file=SSOT_PATHS.tokens_css,
                        line=None,
                        message=(
                            f"[{theme_name}] MAI badge WCAG contrast failure `{fg_tok}` ({fg_hex}) "
                            f"on `{bg_tok}` ({bg_hex}): {ratio:.2f}:1 < {target:.1f}:1."
                        ),
                        remediation="Adjust badge contrast colors in `DT-UI-DS-DOC-001.md`.",
                    )
                )

    return findings


# ---------------------------------------------------------------------------
# GRD-20: SVG Icons, Screenshots, Language Policy, LaTeX & Mermaid
# ---------------------------------------------------------------------------

_MD_ICON_REF_RE = re.compile(r"#(icon-[a-z0-9-]+)\b")
_EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")
_SPANISH_STOPWORD_RE = re.compile(
    r"\b(?:para|desde|hacia|según|sistema|usuario|pantalla|módulo|auditoría|"
    r"trazabilidad|mantenimiento|almacén|inventario|requisito|casos de uso)\b",
    re.IGNORECASE,
)
_KNOWN_MERMAID_TYPES: frozenset[str] = frozenset(
    {
        "flowchart",
        "graph",
        "sequencediagram",
        "statediagram",
        "statediagram-v2",
        "classdiagram",
        "erdiagram",
        "gantt",
        "pie",
        "gitgraph",
        "journey",
        "mindmap",
        "timeline",
        "c4context",
        "c4container",
        "c4component",
        "c4dynamic",
        "c4deployment",
    }
)


def evaluate_grd_20(index: RepoIndex) -> list[Finding]:
    """Verify SVG icon symbols, SCR screenshots, Technical English/Spanish prototype copy, LaTeX, and Mermaid."""
    findings: list[Finding] = []

    # 1. SVG icon sprite validation
    if index.icons is None:
        findings.append(
            Finding(
                rule_id="GRD-20",
                severity=SEVERITY_WARNING,
                scope="ui",
                file=SSOT_PATHS.icons_svg,
                line=None,
                message="Missing `ui-ux/assets/icons.svg` sprite sheet.",
                remediation="Restore `ui-ux/assets/icons.svg`.",
            )
        )
        known_icons: frozenset[str] = frozenset()
    else:
        known_icons = index.icons.symbol_ids
        for dup in index.icons.duplicate_ids:
            findings.append(
                Finding(
                    rule_id="GRD-20",
                    severity=SEVERITY_WARNING,
                    scope="ui",
                    file=SSOT_PATHS.icons_svg,
                    line=None,
                    message=f"Duplicate SVG `<symbol id=\"{dup}\">` in `icons.svg`.",
                    remediation="Ensure every SVG `<symbol>` ID in `icons.svg` is unique.",
                )
            )

    if known_icons:
        for rel, doc in sorted(index.markdown_docs.items()):
            for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
                for m in _MD_ICON_REF_RE.finditer(line):
                    sym = m.group(1)
                    if sym not in known_icons:
                        findings.append(
                            Finding(
                                rule_id="GRD-20",
                                severity=SEVERITY_WARNING,
                                scope="ui",
                                file=rel,
                                line=line_no,
                                message=f"Referenced icon `#{sym}` does not exist in `icons.svg`.",
                                remediation="Add the missing `<symbol>` to `ui-ux/assets/icons.svg` or fix the icon ID.",
                            )
                        )
        for rel_asset, asset in sorted(index.prototype_assets.items()):
            for sym in asset.referenced_icons:
                if sym not in known_icons:
                    findings.append(
                        Finding(
                            rule_id="GRD-20",
                            severity=SEVERITY_WARNING,
                            scope="ui",
                            file=rel_asset,
                            line=None,
                            message=f"Prototype references missing icon `#{sym}` not in `icons.svg`.",
                            remediation="Add the missing `<symbol>` to `ui-ux/assets/icons.svg` or fix the icon ID.",
                        )
                    )

    # 2. SCR-*.md §2 screenshot coverage
    for rel, doc in sorted(index.screen_docs.items()):
        png_imgs = [
            lnk for lnk in doc.links if lnk.is_image and lnk.target_path.lower().endswith(".png")
        ]
        if not png_imgs:
            findings.append(
                Finding(
                    rule_id="GRD-20",
                    severity=SEVERITY_WARNING,
                    scope="ui",
                    file=rel,
                    line=None,
                    message=f"Screen specification `{rel}` has no `.png` visual evidence embedded.",
                    remediation="Embed at least one `.png` screenshot under `## 2.` (`assets/SCR-...png`).",
                )
            )

    # 3. Language policy (Technical English + zero emojis in .md docs; lang="es" in screen HTML prototypes)
    for rel, doc in sorted(index.markdown_docs.items()):
        if not rel.startswith("scripts/"):
            in_fence = False
            for line_no, line in enumerate(doc.raw_text.splitlines(), start=1):
                s = line.strip()
                if s.startswith("```") or s.startswith("~~~"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                em = _EMOJI_RE.search(line)
                if em:
                    findings.append(
                        Finding(
                            rule_id="GRD-20",
                            severity=SEVERITY_WARNING,
                            scope="links",
                            file=rel,
                            line=line_no,
                            message=f"Unicode emoji `{em.group(0)}` found in Markdown documentation.",
                            remediation="Remove decorative emojis to preserve Technical English documentation hygiene.",
                        )
                    )
                    break

        stripped_doc = _strip_planned_and_code(doc.raw_text)
        es_hits = _SPANISH_STOPWORD_RE.findall(stripped_doc)
        if len(es_hits) >= 3:
            findings.append(
                Finding(
                    rule_id="GRD-20",
                    severity=SEVERITY_WARNING,
                    scope="links",
                    file=rel,
                    line=None,
                    message=(
                        f"Non-English (Spanish) documentation prose detected ({len(es_hits)} matches: "
                        f"{', '.join(dict.fromkeys(h.lower() for h in es_hits[:4]))})."
                    ),
                    remediation="Translate repository documentation to 100% Technical English.",
                )
            )

        # 4. LaTeX $...$ / $$...$$ parity
        clean_lines = [
            "" if line.strip().startswith(("```", "~~~")) else re.sub(r"`[^`\n]+`", "", line)
            for line in stripped_doc.splitlines()
        ]
        # Remove escaped dollars (`\$`) before delimiter counting
        masked_text = re.sub(r"\\\$", "  ", "\n".join(clean_lines))
        if masked_text.count("$$") % 2 != 0:
            findings.append(
                Finding(
                    rule_id="GRD-20",
                    severity=SEVERITY_WARNING,
                    scope="links",
                    file=rel,
                    line=None,
                    message="Unbalanced display LaTeX `$$...$$` delimiter block.",
                    remediation="Ensure every `$$` display math block is properly closed.",
                )
            )
        else:
            no_display = re.sub(r"\$\$.*?\$\$", "", masked_text, flags=re.DOTALL)
            for line_no, ln in enumerate(no_display.splitlines(), start=1):
                # Mask valid paired inline LaTeX spans ($...$) before checking for stray $
                ln_no_inline = re.sub(
                    r"(?<!\$)\$(?!\s|\$)([^$\n]+?)(?<!\s)\$(?!\d|\$)", "", ln
                )
                # Ignore standalone currency literals ($100, $1,200.50)
                ln_no_curr = re.sub(r"\$\d+(?:,\d{3})*(?:\.\d+)?(?![A-Za-z0-9$\\-])", "", ln_no_inline)
                if "$" in ln_no_curr:
                    findings.append(
                        Finding(
                            rule_id="GRD-20",
                            severity=SEVERITY_WARNING,
                            scope="links",
                            file=rel,
                            line=line_no,
                            message="Unbalanced inline LaTeX `$...$` delimiter on line.",
                            remediation="Close the inline `$...$` expression or escape literal currency as `\\$`.",
                        )
                    )

        # 5. Mermaid block validation
        for mb in doc.mermaid_blocks:
            body = mb.content.strip()
            if not body:
                findings.append(
                    Finding(
                        rule_id="GRD-20",
                        severity=SEVERITY_WARNING,
                        scope="links",
                        file=rel,
                        line=mb.start_line,
                        message="Empty Mermaid diagram block.",
                        remediation="Add valid Mermaid diagram content or remove the empty block.",
                    )
                )
                continue
            dtype = mb.diagram_type.lower()
            if dtype not in _KNOWN_MERMAID_TYPES:
                findings.append(
                    Finding(
                        rule_id="GRD-20",
                        severity=SEVERITY_WARNING,
                        scope="links",
                        file=rel,
                        line=mb.start_line,
                        message=f"Unrecognized Mermaid diagram type `{mb.diagram_type}`.",
                        remediation="Start the Mermaid fence with a valid diagram declaration (`flowchart`, `sequenceDiagram`, etc.).",
                    )
                )
            if dtype in ("flowchart", "graph"):
                sub_cnt = len(re.findall(r"^\s*subgraph\b", body, re.MULTILINE))
                end_cnt = len(re.findall(r"^\s*end\s*$", body, re.MULTILINE))
                if sub_cnt != end_cnt:
                    findings.append(
                        Finding(
                            rule_id="GRD-20",
                            severity=SEVERITY_WARNING,
                            scope="links",
                            file=rel,
                            line=mb.start_line,
                            message=f"Mermaid subgraph/end mismatch ({sub_cnt} subgraph vs {end_cnt} end).",
                            remediation="Ensure every Mermaid `subgraph` has a matching `end`.",
                        )
                    )
            elif dtype == "sequencediagram":
                open_cnt = len(
                    re.findall(
                        r"^\s*(?:alt|opt|loop|par|critical|break|rect)\b",
                        body,
                        re.MULTILINE,
                    )
                )
                end_cnt = len(re.findall(r"^\s*end\s*$", body, re.MULTILINE))
                if open_cnt != end_cnt:
                    findings.append(
                        Finding(
                            rule_id="GRD-20",
                            severity=SEVERITY_WARNING,
                            scope="links",
                            file=rel,
                            line=mb.start_line,
                            message=(
                                f"Mermaid sequenceDiagram block mismatch "
                                f"({open_cnt} alt/opt/loop/rect vs {end_cnt} end)."
                            ),
                            remediation="Ensure every sequence diagram control block has a matching `end`.",
                        )
                    )

    # Spanish UI copy validation in screen HTML prototypes (excluding developer utilities)
    for rel_asset, asset in sorted(index.prototype_assets.items()):
        if asset.kind != "html":
            continue
        fname = rel_asset.rsplit("/", 1)[-1].lower()
        if not fname.startswith("scr-"):
            continue
        if not re.search(r'<html\b[^>]*\blang=["\']es["\']', asset.content, re.IGNORECASE):
            findings.append(
                Finding(
                    rule_id="GRD-20",
                    severity=SEVERITY_WARNING,
                    scope="ui",
                    file=rel_asset,
                    line=1,
                    message=f"Screen prototype `{rel_asset}` is missing `<html lang=\"es\">` for Spanish UI copy.",
                    remediation="Declare `lang=\"es\"` on `<html>` and ensure end-user prototype copy is in Spanish.",
                )
            )

    return findings


# ---------------------------------------------------------------------------
# GRD-21: SRS CSV Quality, TR-* Sync, Framework Ban & Dynamic MVP Index
# ---------------------------------------------------------------------------

_FORBIDDEN_TECH_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"\bReact\b(?!\s+Native\s+Paper|\s+Native\s+Navigation)", re.IGNORECASE),
        "React (unapproved frontend — use Blazor)",
    ),
    (
        re.compile(r"\bAngular\b(?!\s+velocity\b)", re.IGNORECASE),
        "Angular (unapproved frontend — use Blazor)",
    ),
    (re.compile(r"\bVue\.?js\b", re.IGNORECASE), "Vue.js (unapproved frontend — use Blazor)"),
    (re.compile(r"\bReact Native\b", re.IGNORECASE), "React Native (unapproved platform — use .NET MAUI)"),
    (re.compile(r"\bFlutter\b", re.IGNORECASE), "Flutter (unapproved platform — use .NET MAUI)"),
    (
        re.compile(r"\bEntity Framework.*mobile\b", re.IGNORECASE),
        "EF Core on mobile (forbidden — use sqlite-net-pcl)",
    ),
)
_TR_REQ_ROW_RE = re.compile(r"\b(TR-\d+-(?:FR|NFR)-\d+)\b")
_SCR_REF_RE = re.compile(r"(?<![A-Z0-9-])SCR-[A-Z]+-\d+\b")
_UC_REF_RE = re.compile(r"(?<![A-Z0-9-])UC-[A-Z]+-\d+\b")


def evaluate_grd_21(index: RepoIndex) -> list[Finding]:
    """Validate `srs.csv` quality, `TR-*.md` sync, unapproved framework bans, and MVP index alignment."""
    findings: list[Finding] = []

    # 1. srs.csv integrity & TR-* sync
    if not index.srs_rows:
        findings.append(
            Finding(
                rule_id="GRD-21",
                severity=SEVERITY_WARNING,
                scope="srs",
                file=SSOT_PATHS.srs_csv,
                line=None,
                message="Missing or empty `requirements/data/srs.csv`.",
                remediation="Restore `requirements/data/srs.csv`.",
            )
        )
    else:
        seen_req_ids: dict[str, int] = {}
        seen_global_ids: dict[str, int] = {}
        srs_by_req_id: dict[str, dict[str, str]] = {}
        csv_tr_to_reqs: dict[str, set[str]] = {}

        for row_idx, row in enumerate(index.srs_rows, start=2):
            req_id = (row.get("Req ID") or "").strip()
            gid = (row.get("Global ID") or "").strip()
            desc = (row.get("Description") or "").strip()
            rtype = (row.get("Type") or "").strip()
            status = (row.get("Status") or "").strip()
            tr_id = (row.get("TR ID") or "").strip()

            if not req_id or not desc or not rtype or not status:
                findings.append(
                    Finding(
                        rule_id="GRD-21",
                        severity=SEVERITY_WARNING,
                        scope="srs",
                        file=SSOT_PATHS.srs_csv,
                        line=row_idx,
                        message=f"SRS row {row_idx} (`{req_id or 'UNKNOWN'}`) is missing required metadata (Req ID/Description/Type/Status).",
                        remediation="Populate all required columns in `requirements/data/srs.csv`.",
                    )
                )
            if req_id:
                if req_id in seen_req_ids:
                    findings.append(
                        Finding(
                            rule_id="GRD-21",
                            severity=SEVERITY_WARNING,
                            scope="srs",
                            file=SSOT_PATHS.srs_csv,
                            line=row_idx,
                            message=f"Duplicate `Req ID` `{req_id}` (first seen at line {seen_req_ids[req_id]}).",
                            remediation="Deduplicate `Req ID` entries in `requirements/data/srs.csv`.",
                        )
                    )
                else:
                    seen_req_ids[req_id] = row_idx
                    srs_by_req_id[req_id] = row
            if gid:
                if gid in seen_global_ids:
                    findings.append(
                        Finding(
                            rule_id="GRD-21",
                            severity=SEVERITY_WARNING,
                            scope="srs",
                            file=SSOT_PATHS.srs_csv,
                            line=row_idx,
                            message=f"Duplicate `Global ID` `{gid}` (first seen at line {seen_global_ids[gid]}).",
                            remediation="Ensure every `Global ID` in `srs.csv` is unique.",
                        )
                    )
                else:
                    seen_global_ids[gid] = row_idx
            if tr_id and req_id:
                csv_tr_to_reqs.setdefault(tr_id, set()).add(req_id)

        # Verify TR-*.md files match srs.csv
        tr_docs = {
            rel: doc
            for rel, doc in sorted(index.markdown_docs.items())
            if rel.startswith("requirements/common/TR-") and rel.endswith(".md")
        }
        seen_tr_ids: set[str] = set()
        for rel, doc in tr_docs.items():
            tr_id = str(doc.frontmatter.get("id") or rel.rsplit("/", 1)[-1].removesuffix(".md")).strip()
            seen_tr_ids.add(tr_id)
            doc_req_ids = set(_TR_REQ_ROW_RE.findall(doc.raw_text))
            fm_total = doc.frontmatter.get("total_requirements")
            if isinstance(fm_total, int) and fm_total != len(doc_req_ids):
                findings.append(
                    Finding(
                        rule_id="GRD-21",
                        severity=SEVERITY_WARNING,
                        scope="srs",
                        file=rel,
                        line=None,
                        message=(
                            f"`{tr_id}` frontmatter `total_requirements: {fm_total}` "
                            f"differs from parsed rows ({len(doc_req_ids)})."
                        ),
                        remediation="Regenerate `requirements/common/TR-*.md` from CSV.",
                    )
                )
            for rid in sorted(doc_req_ids):
                if rid not in srs_by_req_id:
                    findings.append(
                        Finding(
                            rule_id="GRD-21",
                            severity=SEVERITY_WARNING,
                            scope="srs",
                            file=rel,
                            line=None,
                            message=f"`{tr_id}` references `{rid}` which is missing from `srs.csv`.",
                            remediation="Regenerate `TR-*.md` from the latest `requirements/data/srs.csv`.",
                        )
                    )
                elif (srs_by_req_id[rid].get("TR ID") or "").strip() != tr_id:
                    findings.append(
                        Finding(
                            rule_id="GRD-21",
                            severity=SEVERITY_WARNING,
                            scope="srs",
                            file=rel,
                            line=None,
                            message=(
                                f"`{rid}` in `{rel}` maps to `TR ID={srs_by_req_id[rid].get('TR ID')}` "
                                f"in `srs.csv` instead of `{tr_id}`."
                            ),
                            remediation="Re-sync `srs.csv` and `TR-*.md`.",
                        )
                    )
            expected_csv_reqs = csv_tr_to_reqs.get(tr_id, set())
            for missing_in_doc in sorted(expected_csv_reqs - doc_req_ids):
                findings.append(
                    Finding(
                        rule_id="GRD-21",
                        severity=SEVERITY_WARNING,
                        scope="srs",
                        file=rel,
                        line=None,
                        message=f"`srs.csv` links `{missing_in_doc}` to `{tr_id}` but it is missing from `{rel}`.",
                        remediation="Regenerate `requirements/common/TR-*.md` from CSV.",
                    )
                )

        for csv_tr in sorted(csv_tr_to_reqs.keys() - seen_tr_ids):
            findings.append(
                Finding(
                    rule_id="GRD-21",
                    severity=SEVERITY_WARNING,
                    scope="srs",
                    file=SSOT_PATHS.srs_csv,
                    line=None,
                    message=f"`srs.csv` references `{csv_tr}` which has no `requirements/common/{csv_tr}.md` file.",
                    remediation="Generate the missing `TR-*.md` file from CSV.",
                )
            )

    # 2. Unapproved Framework Ban across Markdown docs
    for rel, doc in sorted(index.markdown_docs.items()):
        if rel.startswith("scripts/"):
            continue
        tech_text = _strip_adr_alternatives(doc.raw_text)
        tech_lines = tech_text.splitlines()
        for pat, desc in _FORBIDDEN_TECH_PATTERNS:
            for m in pat.finditer(tech_text):
                line_no = tech_text[: m.start()].count("\n") + 1
                line_text = tech_lines[line_no - 1] if 0 < line_no <= len(tech_lines) else ""
                if _PROHIBITION_CTX_RE.search(line_text):
                    continue
                findings.append(
                    Finding(
                        rule_id="GRD-21",
                        severity=SEVERITY_WARNING,
                        scope="srs",
                        file=rel,
                        line=line_no,
                        message=f"Unapproved technology reference `{desc}`.",
                        remediation="Align stack references with `DT-ARQ-TECH-001.md` and `ADR-004.md` (.NET MAUI + Blazor).",
                    )
                )

    # 3. Dynamic MVP SCR-*/UC-* index alignment
    for rel, doc in sorted(index.screen_docs.items()):
        scr_id = str(doc.frontmatter.get("id") or rel.rsplit("/", 1)[-1].removesuffix(".md")).strip()
        if scr_id not in MVP_APPROVED_SCREENS:
            findings.append(
                Finding(
                    rule_id="GRD-21",
                    severity=SEVERITY_WARNING,
                    scope="srs",
                    file=rel,
                    line=1,
                    message=f"Screen specification `{scr_id}` is outside `MVP_APPROVED_SCREENS`.",
                    remediation="Register `{scr_id}` in approved MVP index or move out of active MVP scope.",
                )
            )

    for rel, doc in sorted(index.usecase_docs.items()):
        uc_id = str(doc.frontmatter.get("id") or rel.rsplit("/", 1)[-1].removesuffix(".md")).strip()
        if uc_id not in MVP_APPROVED_UCS:
            findings.append(
                Finding(
                    rule_id="GRD-21",
                    severity=SEVERITY_WARNING,
                    scope="srs",
                    file=rel,
                    line=1,
                    message=f"Use Case `{uc_id}` is outside `MVP_APPROVED_UCS`.",
                    remediation="Register `{uc_id}` in approved MVP index or move to post-MVP section.",
                )
            )

    for rel, doc in sorted(index.markdown_docs.items()):
        if rel == SSOT_PATHS.todo_md or rel.startswith("scripts/"):
            continue
        scoped = _strip_planned_and_code(doc.raw_text)
        seen_extra: set[str] = set()
        for m in _SCR_REF_RE.finditer(scoped):
            sid = m.group(0)
            if sid not in MVP_APPROVED_SCREENS and sid not in seen_extra:
                seen_extra.add(sid)
                line_no = scoped[: m.start()].count("\n") + 1
                findings.append(
                    Finding(
                        rule_id="GRD-21",
                        severity=SEVERITY_WARNING,
                        scope="srs",
                        file=rel,
                        line=line_no,
                        message=f"Referenced screen `{sid}` is outside the approved MVP screen index.",
                        remediation="Verify whether this belongs in a post-MVP section or needs MVP approval.",
                    )
                )
        for m in _UC_REF_RE.finditer(scoped):
            uid = m.group(0)
            if uid not in MVP_APPROVED_UCS and uid not in seen_extra:
                seen_extra.add(uid)
                line_no = scoped[: m.start()].count("\n") + 1
                findings.append(
                    Finding(
                        rule_id="GRD-21",
                        severity=SEVERITY_WARNING,
                        scope="srs",
                        file=rel,
                        line=line_no,
                        message=f"Referenced use case `{uid}` is outside the approved MVP UC index.",
                        remediation="Move out-of-scope UCs under `### Use Cases Planned for Later Phases` or approve in index.",
                    )
                )

    return findings
