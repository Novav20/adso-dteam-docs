#!/usr/bin/env python3
"""
DTEAM UI/UX Screen Specification Coherence Auditor & Linter
===========================================================
Deterministic audit script for UI/UX screen specifications (SCR-*.md)
within the adso-dteam-docs repository (DTEAM Project).

Verifies structural integrity, architectural layer segregation (no DB schema,
no SQL functions, no Blazor code-behind, no raw CSS/hex), token conformance,
and ISA-101/HPHMI rules without relying on LLM heuristic evaluation.

Usage:
    uv run audit.py audit     --file <relative-path-to-SCR.md>
    uv run audit.py lint      --file <relative-path-to-SCR.md>
    uv run audit.py audit-all [--output <report-path>]
"""

from __future__ import annotations
import argparse
import datetime
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Finding Model & Constants
# ---------------------------------------------------------------------------

class Finding(NamedTuple):
    severity: str   # BLOCKER | WARNING | INFO
    code: str       # STR-001, SQL-001, CS-001, CSS-001, etc.
    message: str
    line: int | None = None


VALID_MODULES: set[str] = {"VIS", "MTTO", "INV", "ADM"}

MANDATORY_FRONTMATTER_KEYS: list[str] = [
    "id", "title", "module", "isa101_level", "platform",
    "target_device", "roles", "user_stories", "use_cases",
    "version", "date", "status"
]

CANONICAL_SECTIONS: list[tuple[int, str, str]] = [
    (1, r"^##\s+1\.\s+Purpose and Operational Context", "## 1. Purpose and Operational Context"),
    (2, r"^##\s+2\.\s+Visual Artifact", "## 2. Visual Artifact"),
    (3, r"^##\s+3\.\s+Functional Component Inventory", "## 3. Functional Component Inventory"),
    (4, r"^##\s+4\.\s+Screen State Matrix", "## 4. Screen State Matrix"),
    (5, r"^##\s+5\.\s+Interaction Rules and Data Flow", "## 5. Interaction Rules and Data Flow"),
    (6, r"^##\s+6\.\s+Industrial and Safety Considerations", "## 6. Industrial and Safety Considerations"),
    (7, r"^##\s+7\.\s+Frontend Component Contract", "## 7. Frontend Component Contract (Blazor / Razor)"),
    (8, r"^##\s+8\.\s+Layout and Responsive Adaptability", "## 8. Layout and Responsive Adaptability"),
    (9, r"^##\s+9\.\s+Traceability and Requirements Matrix", "## 9. Traceability and Requirements Matrix"),
]

MANDATORY_SUBSECTIONS_7: list[tuple[str, str]] = [
    (r"^###\s+7\.1\.?\s+Component Hierarchy", "### 7.1 Component Hierarchy & File Mapping"),
    (r"^###\s+7\.2\.?\s+Physical Component Parameters", "### 7.2 Physical Component Parameters & DTO Contracts"),
    (r"^###\s+7\.3\.?\s+Client-Side DOM", "### 7.3 Client-Side DOM & Interop Bridge"),
]

# Prohibited persistence / SQL leak patterns
PERSISTENCE_LEAK_PATTERNS: list[tuple[str, str, str]] = [
    (r"\b(mtto|tax|adm|ops|auth)\.[a-z0-9_]+", "SQL-001",
     "Physical database schema qualifier '{match}' leaked into specification. Use frontend DTO/command types."),
    (r"\btimestamptz\b", "SQL-002",
     "PostgreSQL physical type 'timestamptz' leaked. Use C# 'DateTimeOffset' or ISO-8601 string."),
    (r"\bUUID PRIMARY KEY\b", "SQL-002",
     "Physical SQL DDL constraint 'UUID PRIMARY KEY' leaked into specification."),
    (r"\b(?:BIG)?SERIAL(?:\s+PRIMARY\s+KEY|\s+NOT\s+NULL|\s*,)\b", "SQL-002",
     "Physical SQL DDL type 'SERIAL' leaked into specification."),
    (r"\bclock_timestamp\(\)", "SQL-003",
     "PostgreSQL server function 'clock_timestamp()' leaked into specification. Use client/application timestamp semantics."),
    (r"\bNOW\(\)", "SQL-003",
     "SQL server function 'NOW()' leaked into specification."),
    (r"\bINSERT\s+INTO\b", "SQL-004",
     "SQL DML 'INSERT INTO' query leaked into specification. Describe client command dispatch via API endpoints."),
    (r"\bUPDATE\s+[a-z_]+(?:\.[a-z_]+)?\s+SET\b", "SQL-004",
     "SQL DML 'UPDATE ... SET' query leaked into specification. Describe client command dispatch via API endpoints."),
    (r"\bDELETE\s+FROM\b", "SQL-004",
     "SQL DML 'DELETE FROM' query leaked into specification."),
    (r"\bck_[a-z0-9_]+", "SQL-005",
     "Physical database CHECK constraint '{match}' leaked. Translate into frontend validation rules or domain enums."),
]

# Prohibited C# Blazor code-behind / runtime leak patterns
CSHARP_LEAK_PATTERNS: list[tuple[str, str, str]] = [
    (r"\bclass\s+[A-Za-z0-9_]+\s*:\s*ComponentBase\b", "CS-001",
     "Blazor 'ComponentBase' class declaration leaked. Section 7 must define parameter contracts and DTO records only."),
    (r"\[Inject\]", "CS-002",
     "Dependency injection '[Inject]' leaked. DI is an internal implementation detail prohibited from parameter contracts."),
    (r"\bprivate\s+(?:bool|int|string|DateTime|DateTimeOffset|List<[^>]+>|Dictionary<[^>]+>|HashSet<[^>]+>|[A-Z][a-zA-Z0-9_]*)\s+_[a-zA-Z0-9_]+", "CS-003",
     "Private mutable component state field '{match}' leaked. Internal state management belongs to implementation code-behind."),
    (r"\boverride\s+(?:async\s+)?Task\s+On(?:Initialized|ParametersSet)(?:Async)?\b", "CS-004",
     "Blazor lifecycle override '{match}' leaked into specification."),
    (r"\bnamespace\s+[A-Za-z0-9_.]+\b", "CS-005",
     "C# 'namespace' statement leaked. Decoupled Namespaces Rule prohibits premature assembly coupling."),
]

# Prohibited CSS / styling / magic dimension patterns
CSS_LEAK_PATTERNS: list[tuple[str, str, str]] = [
    (r"\bposition:\s*(?:fixed|absolute|relative)\b", "CSS-002",
     "Raw CSS rule '{match}' leaked into specification prose. Use Design System layout tokens and component hierarchy."),
    (r"\bpointer-events:\s*(?:none|auto)\b", "CSS-002",
     "Raw CSS rule '{match}' leaked into specification prose."),
    (r"\bz-index:\s*\d+\b", "CSS-003",
     "Raw numeric z-index '{match}' leaked. Use '--dt-z-*' elevation tokens."),
]

# Prohibited browser / runtime globals
RUNTIME_LEAK_PATTERNS: list[tuple[str, str, str]] = [
    (r"\bwindow\.[a-zA-Z0-9_]+", "DOM-001",
     "Direct browser global '{match}' leaked. Abstract via JSInterop capability interfaces in §7.3."),
    (r"\bdocument\.[a-zA-Z0-9_]+", "DOM-001",
     "Direct DOM access '{match}' leaked."),
    (r"\bAudioContext\b", "DOM-001",
     "Direct Web Audio API 'AudioContext' leaked. Abstract via audio interop capability interface."),
    (r"\b(?:local|session)Storage\b", "DOM-001",
     "Direct browser storage '{match}' leaked. Abstract via 'IOfflineStorage'."),
    (r"\bsqlite-net-pcl\b", "DOM-002",
     "Concrete third-party package 'sqlite-net-pcl' leaked. Use abstract 'IOfflineStorage' / encrypted cache."),
]

# Spanish section title words (Language Policy: English only)
SPANISH_HEADER_WORDS: list[str] = [
    "Propósito", "Contexto Operacional", "Artefacto Visual", "Inventario Funcional",
    "Matriz de Estados", "Reglas de Interacción", "Consideraciones Industriales",
    "Contrato de Componentes", "Adaptabilidad", "Trazabilidad"
]

# ---------------------------------------------------------------------------
# Repository & Token Utilities
# ---------------------------------------------------------------------------

def find_repo_root(start: Path) -> Path | None:
    """Ascends from `start` looking for the .git directory of adso-dteam-docs."""
    current = start.resolve()
    for _ in range(10):
        if (current / ".git").exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def load_canonical_tokens(repo_root: Path) -> set[str]:
    """Loads all valid --dt-* design tokens from tokens.css."""
    tokens_file = repo_root / "ui-ux" / "assets" / "tokens.css"
    if not tokens_file.exists():
        return set()
    
    content = tokens_file.read_text(encoding="utf-8")
    tokens = set(re.findall(r"(--dt-[a-z0-9-]+)\s*:", content))
    return tokens


# ---------------------------------------------------------------------------
# Verification Axes
# ---------------------------------------------------------------------------

def audit_frontmatter(content: str) -> list[Finding]:
    """Verifies YAML frontmatter integrity, completeness, and values."""
    findings: list[Finding] = []
    lines = content.splitlines()

    if not lines or lines[0].strip() != "---":
        findings.append(Finding(
            severity="BLOCKER",
            code="STR-001",
            message="Document must begin with YAML frontmatter delimiter '---'.",
            line=1
        ))
        return findings

    fm_lines: list[str] = []
    fm_end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm_end = i
            break
        fm_lines.append(lines[i])

    if fm_end == -1:
        findings.append(Finding(
            severity="BLOCKER",
            code="STR-001",
            message="YAML frontmatter closing delimiter '---' not found.",
            line=1
        ))
        return findings

    fm_text = "\n".join(fm_lines)

    # Check mandatory keys
    for key in MANDATORY_FRONTMATTER_KEYS:
        pattern = rf"^{key}:"
        if not re.search(pattern, fm_text, re.MULTILINE):
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-001",
                message=f"Mandatory frontmatter key '{key}' is missing.",
                line=1
            ))

    # Verify ID format: SCR-[VIS|MTTO|INV|ADM]-[0-9]{3}
    id_match = re.search(r"^id:\s*(SCR-[A-Z]+-[0-9]{3})", fm_text, re.MULTILINE)
    if not id_match:
        findings.append(Finding(
            severity="BLOCKER",
            code="STR-002",
            message="Frontmatter 'id' must follow pattern 'SCR-[MODULE]-[NUM]' (e.g., SCR-VIS-008).",
            line=1
        ))
    else:
        module_match = re.search(r"^module:\s*([A-Z]+)", fm_text, re.MULTILINE)
        if module_match and module_match.group(1) not in VALID_MODULES:
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-002",
                message=f"Frontmatter 'module' '{module_match.group(1)}' is invalid. Must be one of {VALID_MODULES}.",
                line=1
            ))

    return findings


def audit_structure(content: str) -> list[Finding]:
    """Verifies that all 9 canonical sections and §7 subsections exist in exact order."""
    findings: list[Finding] = []
    lines = content.splitlines()

    # Check language of headers
    for idx, line in enumerate(lines, start=1):
        if line.startswith("#"):
            for sp_word in SPANISH_HEADER_WORDS:
                if sp_word in line:
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="LANG-001",
                        message=f"Header contains Spanish term '{sp_word}'. All screen specs must be 100% Technical English.",
                        line=idx
                    ))

    # Find section positions
    section_positions: dict[int, int] = {}
    for sec_num, pattern, label in CANONICAL_SECTIONS:
        found = False
        for idx, line in enumerate(lines, start=1):
            if re.search(pattern, line, re.IGNORECASE):
                section_positions[sec_num] = idx
                found = True
                break
        if not found:
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-003",
                message=f"Mandatory section missing: '{label}'.",
                line=None
            ))

    # Verify chronological ordering
    ordered_nums = sorted(section_positions.keys())
    for i in range(len(ordered_nums) - 1):
        current_num = ordered_nums[i]
        next_num = ordered_nums[i + 1]
        if section_positions[current_num] > section_positions[next_num]:
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-004",
                message=f"Section {current_num} (line {section_positions[current_num]}) appears after Section {next_num} (line {section_positions[next_num]}). Sections must be strictly ordered 1 through 9.",
                line=section_positions[current_num]
            ))

    # Check §7 subsections if §7 exists
    if 7 in section_positions:
        sec7_start = section_positions[7]
        sec8_start = section_positions.get(8, len(lines))
        sec7_text = "\n".join(lines[sec7_start - 1 : sec8_start])

        for pattern, label in MANDATORY_SUBSECTIONS_7:
            if not re.search(pattern, sec7_text, re.MULTILINE):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="STR-005",
                    message=f"Mandatory subsection in §7 missing: '{label}'.",
                    line=sec7_start
                ))

    # Check §8 responsive tiers if §8 exists
    if 8 in section_positions:
        sec8_start = section_positions[8]
        sec9_start = section_positions.get(9, len(lines))
        sec8_text = "\n".join(lines[sec8_start - 1 : sec9_start])

        tiers = ["Desktop", "Tablet Landscape", "Tablet Portrait"]
        for tier in tiers:
            if tier.lower() not in sec8_text.lower():
                findings.append(Finding(
                    severity="WARNING",
                    code="STR-006",
                    message=f"Section 8 should tabulate layout rules for '{tier}'.",
                    line=sec8_start
                ))

    return findings


def audit_persistence_leaks(content: str) -> list[Finding]:
    """Scans for database schema, physical SQL types, and check constraints."""
    findings: list[Finding] = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        # Skip normative prohibition alerts/rules
        if "PROHIBITED" in line or "Prohibited" in line:
            continue

        # Exclude markdown link targets/URLs where schemas might appear in repository filepaths (e.g. adso-dteam-docs/...)
        stripped_line = re.sub(r"\[.*?\]\(.*?\)", "", line)

        for pattern, code, msg_template in PERSISTENCE_LEAK_PATTERNS:
            match = re.search(pattern, stripped_line, re.IGNORECASE)
            if match:
                matched_str = match.group(0)
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=matched_str),
                    line=idx
                ))

    return findings


def audit_csharp_leaks(content: str) -> list[Finding]:
    """Scans for C# Blazor code-behind, [Inject], private mutable state, and namespaces."""
    findings: list[Finding] = []
    lines = content.splitlines()

    in_code_block = False
    code_block_lang = ""

    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_lang = line.strip()[3:].strip().lower()
            else:
                in_code_block = False
                code_block_lang = ""
            continue

        # Skip C# comments and prohibition descriptions
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*") or "PROHIBITED" in line or "Prohibited" in line:
            continue

        for pattern, code, msg_template in CSHARP_LEAK_PATTERNS:
            match = re.search(pattern, line)
            if match:
                if code == "CS-005" and not (in_code_block and code_block_lang in ("csharp", "c#", "cs")):
                    continue
                matched_str = match.group(0)
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=matched_str),
                    line=idx
                ))

    return findings


def audit_css_and_dimension_leaks(content: str) -> list[Finding]:
    """Scans for raw CSS declarations, hex codes, and magic drawer dimensions."""
    findings: list[Finding] = []
    lines = content.splitlines()

    hex_pattern = re.compile(r"(?<![a-zA-Z0-9_\(\[/\$-])#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b(?![-a-zA-Z0-9_])")
    drawer_magic_pattern = re.compile(r"(?:drawer|sidebar|bottom\s*sheet|width).*?(?:\$?(?:440|320)\\?text\{px\}\$?|\b(?:440|320)px\b)", re.IGNORECASE)

    in_sec8 = False
    for idx, line in enumerate(lines, start=1):
        if re.search(r"^##\s+8\.\s+Layout and Responsive Adaptability", line, re.IGNORECASE):
            in_sec8 = True
            continue
        elif line.startswith("## "):
            in_sec8 = False
            continue

        clean_line = re.sub(r"\[.*?\]\([^\)]*#[^\)]*\)", "", line)
        clean_line = re.sub(r"\]\([^)]+\)", "", clean_line)

        # 1. Check raw CSS declarations
        for pattern, code, msg_template in CSS_LEAK_PATTERNS:
            match = re.search(pattern, clean_line)
            if match:
                matched_str = match.group(0)
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=matched_str),
                    line=idx
                ))

        # 2. Check raw hex colors in prose/tables
        hex_matches = hex_pattern.findall(clean_line)
        for h in hex_matches:
            findings.append(Finding(
                severity="BLOCKER",
                code="CSS-001",
                message=f"Raw hex color '{h}' found. Colors must use semantic tokens (--dt-color-*) or primitive tokens (--dt-primitive-*).",
                line=idx
            ))

        # 3. Check magic drawer dimensions
        if drawer_magic_pattern.search(line):
            if "--dt-layout-drawer-width" not in line:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="CSS-004",
                    message="Hardcoded drawer dimension detected without semantic token. Must reference '--dt-layout-drawer-width-desktop' (440px) or '--dt-layout-drawer-width-tablet' (320px).",
                    line=idx
                ))

        # 4. Check raw CSS calc() in Section 8
        if in_sec8 and not line.strip().startswith(">") and not line.strip().startswith("<!--"):
            if re.search(r"\bcalc\(", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="CSS-005",
                    message="Raw CSS 'calc()' expression found in Section 8. Use descriptive architectural offsets (e.g., 'offsets leftward by 50% of active drawer width (§5.2.3)').",
                    line=idx
                ))

    return findings


def audit_runtime_leaks(content: str) -> list[Finding]:
    """Scans for browser globals and unapproved runtime packages."""
    findings: list[Finding] = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        for pattern, code, msg_template in RUNTIME_LEAK_PATTERNS:
            match = re.search(pattern, line)
            if match:
                matched_str = match.group(0)
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=matched_str),
                    line=idx
                ))

    return findings


def audit_tokens(content: str, valid_tokens: set[str]) -> list[Finding]:
    """Validates that all referenced --dt-* tokens exist in tokens.css and Section 3 uses valid tokens."""
    findings: list[Finding] = []
    lines = content.splitlines()
    token_pattern = re.compile(r"(--dt-[a-z0-9-]+(?:\*)?)")

    in_sec3 = False
    for idx, line in enumerate(lines, start=1):
        if re.search(r"^##\s+3\.\s+Functional Component Inventory", line, re.IGNORECASE):
            in_sec3 = True
            continue
        elif line.startswith("## "):
            in_sec3 = False
            continue

        if in_sec3 and line.strip().startswith("|") and not line.strip().startswith("| :---"):
            if re.match(r"\|\s*`CMP-\d+`", line):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 5:
                    col4 = parts[4]
                    if not ("--dt-" in col4 or "DT-UI-DS" in col4):
                        findings.append(Finding(
                            severity="BLOCKER",
                            code="TOK-002",
                            message=f"Section 3 component '{parts[1]}' lacks explicit Design System token in Semantic Token column ('{col4}'). Prohibit placeholder text; bind directly to '--dt-*' tokens.",
                            line=idx
                        ))

        if valid_tokens:
            matches = token_pattern.findall(line)
            for tok in matches:
                if tok.endswith("*"):
                    prefix = tok[:-1]
                    if not any(t.startswith(prefix) for t in valid_tokens):
                        findings.append(Finding(
                            severity="WARNING",
                            code="TOK-001",
                            message=f"Wildcard token prefix '{tok}' does not match any tokens in 'tokens.css'.",
                            line=idx
                        ))
                elif tok not in valid_tokens:
                    findings.append(Finding(
                        severity="WARNING",
                        code="TOK-001",
                        message=f"Referenced design token '{tok}' is not defined in 'tokens.css'. Verify token name against DT-UI-DS-DOC-001.",
                        line=idx
                    ))

    return findings


def audit_anti_redundancy(content: str) -> list[Finding]:
    """Verifies SSoT separation and anti-redundancy rules across Section 1, 3, and 5."""
    findings: list[Finding] = []
    lines = content.splitlines()

    current_section = 0

    for idx, line in enumerate(lines, start=1):
        # Section boundary tracking
        sec_match = re.match(r"^##\s+(\d+)\.", line)
        if sec_match:
            current_section = int(sec_match.group(1))
            continue
        elif line.startswith("## "):
            current_section = 0
            continue

        # Skip blockquotes (guidance rules) and comments
        stripped = line.strip()
        if stripped.startswith(">") or stripped.startswith("<!--"):
            continue

        # 1. Section 1 SSoT: Qualitative operational context only
        if current_section == 1:
            if re.search(r"--dt-breakpoint-[a-z0-9]+", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="RED-002",
                    message="Section 1 contains design system breakpoint token. Operational context in §1 must be qualitative; responsive breakpoints belong exclusively in §8.",
                    line=idx
                ))
            if re.search(r"\b\d+px\b|\b\d+vh\b", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="RED-002",
                    message="Section 1 contains explicit pixel/vh dimensions. Operational context in §1 must be qualitative; layout dimensions belong in §5 and §8.",
                    line=idx
                ))
            if re.search(r"\([A-Z_]{3,}(?:,\s*[A-Z_]{3,})+\)", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="RED-002",
                    message="Section 1 contains domain enum list. Domain enums belong exclusively in §5.3 and §7.2.3.",
                    line=idx
                ))

        # 2. Section 3 SSoT: Clean component cataloging
        elif current_section == 3:
            if stripped.startswith("|") and not stripped.startswith("| :---"):
                if re.search(r"\bMath\.(?:min|max|clamp)\b", line) or re.search(r"\bclamp\(", line):
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="RED-001",
                        message="Section 3 table cell contains mathematical calculation or clamping logic. §3 is a catalog; interaction algorithms belong exclusively in §5.",
                        line=idx
                    ))
                if re.match(r"\|\s*`CMP-\d+`", line):
                    if re.search(r"--dt-layout-drawer-width[a-z-]*", line):
                        findings.append(Finding(
                            severity="BLOCKER",
                            code="RED-003",
                            message="Section 3 table cell contains layout drawer token. Layout dimensions belong in §5.2 and §8.",
                            line=idx
                        ))
                    if re.search(r"\b\d+vh\b", line):
                        findings.append(Finding(
                            severity="BLOCKER",
                            code="RED-003",
                            message="Section 3 table cell contains viewport height (vh). Container dimensions and gesture physics belong in §5.2 and §8.",
                            line=idx
                        ))
                    if re.search(r"\([A-Z_]{3,}(?:,\s*[A-Z_]{3,})+\)", line):
                        findings.append(Finding(
                            severity="BLOCKER",
                            code="RED-003",
                            message="Section 3 table cell contains domain enum list. Domain enums belong in §7.2.3.",
                            line=idx
                        ))

        # 3. Section 5 SSoT: Zero exhaustive LaTeX enum sets
        elif current_section == 5:
            if re.search(r"\\in\s*\\\{[^\}]+\}", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="RED-004",
                    message="Section 5 contains exhaustive LaTeX enum set enumeration. Reference strongly-typed C# enums in §7.2.3 instead of enumerating string literals in prose or LaTeX.",
                    line=idx
                ))

    return findings


def audit_presentation_boundaries(content: str) -> list[Finding]:
    """Verifies presentation boundaries in UI sequence diagrams (Mermaid)."""
    findings: list[Finding] = []
    lines = content.splitlines()

    in_mermaid_seq = False

    for idx, line in enumerate(lines, start=1):
        if re.match(r"^```mermaid\s*$", line.strip()):
            continue
        if "sequenceDiagram" in line:
            in_mermaid_seq = True
            continue
        elif in_mermaid_seq and line.strip().startswith("```"):
            in_mermaid_seq = False
            continue

        if in_mermaid_seq:
            # 1. Check prohibited backend worker/DB participants
            worker_match = re.search(r"(?:participant|actor)\s+(?:[A-Za-z0-9_]+\s+as\s+)?(AUD|AuditWorker|Worker|DB|Database)\b", line)
            if worker_match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="DIAG-001",
                    message=f"Presentation sequence diagram leaks private backend participant '{worker_match.group(1)}'. UI sequence diagrams must only model interactions between Tech, UI, Interop, and the API gateway.",
                    line=idx
                ))

            # 2. Check prohibited backend internal self-calls
            backend_self_match = re.search(r"\b(API|INV|SVC|SRV|APP|BACKEND)\s*->>\s*\1\s*:", line)
            if backend_self_match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="DIAG-002",
                    message=f"Presentation sequence diagram leaks internal backend self-call '{backend_self_match.group(0).rstrip(':')}'. Internal domain execution must not be modeled as client sequence transitions.",
                    line=idx
                ))

    return findings


# ---------------------------------------------------------------------------
# Master Audit Orchestration
# ---------------------------------------------------------------------------

def run_screen_audit(content: str, repo_root: Path) -> list[Finding]:
    """Executes all deterministic audit axes and returns deduplicated findings."""
    valid_tokens = load_canonical_tokens(repo_root)

    findings: list[Finding] = []
    findings += audit_frontmatter(content)
    findings += audit_structure(content)
    findings += audit_persistence_leaks(content)
    findings += audit_csharp_leaks(content)
    findings += audit_css_and_dimension_leaks(content)
    findings += audit_runtime_leaks(content)
    findings += audit_tokens(content, valid_tokens)
    findings += audit_anti_redundancy(content)
    findings += audit_presentation_boundaries(content)

    # Deduplicate findings by (code, line, message)
    seen: set[tuple[str, int | None, str]] = set()
    unique: list[Finding] = []
    for f in findings:
        key = (f.code, f.line, f.message)
        if key not in seen:
            seen.add(key)
            unique.append(f)

    return unique


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

def generate_markdown_report(
    artifact_path: Path,
    findings: list[Finding],
    repo_root: Path
) -> str:
    """Constructs a formal markdown audit report adhering to repository standard."""
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d-%H%M%S")
    screen_id = artifact_path.stem

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]
    infos    = [f for f in findings if f.severity == "INFO"]

    verdict = "BLOCKED" if blockers else ("PASSED_WITH_OBSERVATIONS" if warnings else "PASSED")

    report: list[str] = [
        "---",
        f"id: AUD-UI-{screen_id}-{timestamp_str}",
        f"screen_audited: {screen_id}",
        f"date: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"verdict: {verdict}",
        "auditor: dteam-ui-coherence-audit (deterministic)",
        "---",
        "",
        f"# Deterministic UI Audit Report: {screen_id}",
        "",
        "## 1. Executive Summary",
        "",
        f"- **Audited File:** `{artifact_path.relative_to(repo_root)}`",
        f"- **Execution Timestamp:** {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Overall Verdict:** `[{verdict}]`",
        f"- **Findings Count:** {len(blockers)} BLOCKER | {len(warnings)} WARNING | {len(infos)} INFO",
        "",
        "---",
        "",
        "## 2. Audit Findings by Severity",
        "",
    ]

    if blockers:
        report.append("### 🔴 Blockers (Immediate Remediation Required)")
        report.append("")
        for f in blockers:
            loc = f" *(line {f.line})*" if f.line else ""
            report.append(f"- **[{f.code}]**{loc}: {f.message}")
        report.append("")
    else:
        report.append("### ✅ Zero Blockers Found")
        report.append("No database schema leaks, SQL syntax, C# code-behind wrappers, raw CSS rules, or structural regressions detected.")
        report.append("")

    if warnings:
        report.append("### ⚠️ Observations & Warnings")
        report.append("")
        for f in warnings:
            loc = f" *(line {f.line})*" if f.line else ""
            report.append(f"- **[{f.code}]**{loc}: {f.message}")
        report.append("")

    if infos:
        report.append("### ℹ️ Informational Notes")
        report.append("")
        for f in infos:
            loc = f" *(line {f.line})*" if f.line else ""
            report.append(f"- **[{f.code}]**{loc}: {f.message}")
        report.append("")

    report += [
        "---",
        "",
        "## 3. Compliance Matrix",
        "",
        "| Audit Axis | Status | Evaluated Rules |",
        "| :--- | :---: | :--- |",
        f"| **Structural & Frontmatter** | {'PASS' if not any(f.code.startswith('STR') and f.severity == 'BLOCKER' for f in findings) else 'FAIL'} | 9 mandatory sections, 3 §7 subsections, valid YAML frontmatter. |",
        f"| **Persistence Decoupling** | {'PASS' if not any(f.code.startswith('SQL') for f in findings) else 'FAIL'} | Zero Postgres schema qualifiers, zero SQL DDL/DML, zero check constraint names. |",
        f"| **Component Contract (C#)** | {'PASS' if not any(f.code.startswith('CS') for f in findings) else 'FAIL'} | Zero ComponentBase classes, zero [Inject], zero private fields, zero lifecycle overrides. |",
        f"| **Styling & Dimension Tokens** | {'PASS' if not any(f.code.startswith('CSS') for f in findings) else 'FAIL'} | Zero hex colors, zero raw layout rules, canonical drawer width tokens. |",
        f"| **Runtime & DOM Boundaries** | {'PASS' if not any(f.code.startswith('DOM') for f in findings) else 'FAIL'} | Zero direct DOM access, zero unapproved package names. |",
        f"| **Design Token Conformance** | {'PASS' if not any(f.code.startswith('TOK') for f in findings) else 'FAIL'} | All referenced --dt-* tokens verified against tokens.css. |",
        f"| **Language Policy** | {'PASS' if not any(f.code.startswith('LANG') for f in findings) else 'FAIL'} | 100% Technical English without untranslated Spanish terms. |",
        "",
    ]

    return "\n".join(report)


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------

def cmd_audit(args: argparse.Namespace, repo_root: Path) -> int:
    """Executes full audit, prints console summary, and saves Markdown report."""
    target_path = (repo_root / args.file).resolve()
    if not target_path.exists():
        print(f"[ERROR] Target specification not found: {target_path}", file=sys.stderr)
        return 1

    content = target_path.read_text(encoding="utf-8")
    rel_path = target_path.relative_to(repo_root)
    print(f"[INFO] Auditing screen specification: {rel_path}")

    findings = run_screen_audit(content, repo_root)

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]
    infos    = [f for f in findings if f.severity == "INFO"]

    # Generate and persist report
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d-%H%M%S")
    out_dir = repo_root.parent / "sena-evidence" / "00-Overview" / "Audits" / "UI"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / f"AUD-UI-{target_path.stem}-{timestamp_str}.md"

    report_content = generate_markdown_report(target_path, findings, repo_root)
    report_file.write_text(report_content, encoding="utf-8")

    # Console output
    for f in findings:
        loc = f" (line {f.line})" if f.line else ""
        print(f"[{f.severity}] [{f.code}]{loc} {f.message}")

    print("-" * 72)
    status_str = "BLOCKED" if blockers else ("PASSED WITH OBSERVATIONS" if warnings else "PASSED")
    print(f"[RESULT] {status_str}: {len(blockers)} BLOCKER | {len(warnings)} WARNING | {len(infos)} INFO")
    print(f"[REPORT] Persisted to: {report_file}")

    return 2 if blockers else 0


def cmd_lint(args: argparse.Namespace, repo_root: Path) -> int:
    """Fast console linting without writing report files."""
    target_path = (repo_root / args.file).resolve()
    if not target_path.exists():
        print(f"[ERROR] Target specification not found: {target_path}", file=sys.stderr)
        return 1

    content = target_path.read_text(encoding="utf-8")
    findings = run_screen_audit(content, repo_root)

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]

    for f in findings:
        loc = f" (line {f.line})" if f.line else ""
        print(f"[{f.severity}] [{f.code}]{loc} {f.message}")

    if not findings:
        print(f"[OK] {target_path.name} is 100% compliant with UI/UX architecture standards.")

    return 2 if blockers else 0


def cmd_audit_all(args: argparse.Namespace, repo_root: Path) -> int:
    """Audits all screen specifications in ui-ux/screens/."""
    screens_dir = repo_root / "ui-ux" / "screens"
    if not screens_dir.exists():
        print(f"[ERROR] Screens directory not found: {screens_dir}", file=sys.stderr)
        return 1

    spec_files = sorted(screens_dir.rglob("SCR-*.md"))
    print(f"[INFO] Found {len(spec_files)} screen specifications to audit.")
    print("=" * 72)

    total_blockers = 0
    total_warnings = 0
    summary_table: list[tuple[str, int, int, str]] = []

    for spec_file in spec_files:
        content = spec_file.read_text(encoding="utf-8")
        findings = run_screen_audit(content, repo_root)
        blockers = sum(1 for f in findings if f.severity == "BLOCKER")
        warnings = sum(1 for f in findings if f.severity == "WARNING")
        status = "FAIL" if blockers else ("WARN" if warnings else "PASS")

        total_blockers += blockers
        total_warnings += warnings
        summary_table.append((spec_file.stem, blockers, warnings, status))

    print(f"{'Screen ID':<16} | {'Status':<6} | {'Blockers':<8} | {'Warnings':<8}")
    print("-" * 48)
    for s_id, b, w, st in summary_table:
        print(f"{s_id:<16} | {st:<6} | {b:<8} | {w:<8}")
    print("=" * 72)
    print(f"[SUMMARY] Total Screens: {len(spec_files)} | Total Blockers: {total_blockers} | Total Warnings: {total_warnings}")

    return 2 if total_blockers > 0 else 0


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="DTEAM UI/UX Screen Specification Coherence Auditor & Linter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="Full deterministic audit + Markdown report")
    p_audit.add_argument("--file", required=True, help="Relative path to target SCR-*.md from repo root")

    p_lint = sub.add_parser("lint", help="Fast console linting without report generation")
    p_lint.add_argument("--file", required=True, help="Relative path to target SCR-*.md from repo root")

    p_all = sub.add_parser("audit-all", help="Scan and audit all screen specifications")
    p_all.add_argument("--output", default=None, help="Optional summary output report path")

    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        print("[ERROR] Git repository root not found. Run from inside adso-dteam-docs/.", file=sys.stderr)
        return 1

    dispatch = {
        "audit":     cmd_audit,
        "lint":      cmd_lint,
        "audit-all": cmd_audit_all,
    }
    return dispatch[args.command](args, repo_root)


if __name__ == "__main__":
    sys.exit(main())
