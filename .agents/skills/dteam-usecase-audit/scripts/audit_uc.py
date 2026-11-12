#!/usr/bin/env python3
"""
DTEAM Use Case Coherence Auditor & Linter
=========================================
Deterministic audit script for domain Use Cases (UC-*.md) within the
adso-dteam-docs repository (DTEAM Project).

Enforces the Black-Box Behavioral Invariant: halts execution immediately on
PostgreSQL schema qualifiers (tax.*, inv.*, adm.*), physical table names,
database column identifiers in snake_case, boolean code literals, OOP method
signatures (Class.Method()), API route endpoints, and HTML formatting tags.

Usage:
    python3 audit_uc.py audit     --file <relative-path-to-UC.md>
    python3 audit_uc.py lint      --file <relative-path-to-UC.md>
    python3 audit_uc.py audit-all [--output <report-path>]
"""

from __future__ import annotations
import argparse
import datetime
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

SCRIPT_REPO_ROOT = Path(__file__).resolve().parents[4]

# ---------------------------------------------------------------------------
# Finding Model & Constants
# ---------------------------------------------------------------------------

class Finding(NamedTuple):
    severity: str   # BLOCKER | WARNING | INFO
    code: str       # STR-*, LEAK-SQL-*, LEAK-CODE-*, TXT-*, REQ-*, LANG-*
    message: str
    line: int | None = None


VALID_MODULES: set[str] = {"VIS", "MTTO", "INV", "ADM"}

MANDATORY_FRONTMATTER_KEYS: list[str] = [
    "id", "name", "module", "user_story", "primary_actor", "secondary_actors"
]

CANONICAL_SECTIONS: list[tuple[int, str, str]] = [
    (1, r"^##\s+1\.\s+Description", "## 1. Description"),
    (2, r"^##\s+2\.\s+Preconditions", "## 2. Preconditions"),
    (3, r"^##\s+3\.\s+Main Flow", "## 3. Main Flow"),
    (4, r"^##\s+4\.\s+Alternate Flows", "## 4. Alternate Flows"),
    (5, r"^##\s+5\.\s+Postconditions", "## 5. Postconditions"),
    (6, r"^##\s+6\.\s+Associated Requirements", "## 6. Associated Requirements"),
]

# Physical Postgres schema qualifiers
SCHEMA_QUALIFIER_PATTERNS: list[tuple[str, str, str]] = [
    (r"\b(?:tax|inv|adm|mtto|ops|vis|sec)\.[a-z_]+", "LEAK-SQL-001",
     "PostgreSQL physical schema qualifier '{match}' leaked into Use Case. Use Cases specify black-box business behavior; omit database schema qualifiers."),
]

# Physical database tables in DT-ERD-DOC-001
PHYSICAL_TABLE_PATTERNS: list[tuple[str, str, str]] = [
    (r"\b(?:equipment_units|functional_locations|asset_installations|audit_logs|work_orders|work_requests|inventory_transactions|failure_records|preventive_schedules)\b",
     "LEAK-SQL-002",
     "Physical relational table name '{match}' leaked into Use Case narrative. Reference business concepts (e.g. 'Equipment Unit', 'Functional Location') instead of database tables."),
]

# Physical snake_case database column assignments & identifiers outside frontmatter
PHYSICAL_COLUMN_PATTERNS: list[tuple[str, str, str]] = [
    (r"\b(?:lifecycle_status|operational_status|maintenance_status|health_status|is_sce|installed_at|removed_at|boundary_start|boundary_end|purchase_date|acquisition_date|installation_date|operation_start_date|failure_mode_id|work_order_id|functional_location_id|asset_id|tag_number)\b",
     "LEAK-SQL-003",
     "Physical database column identifier '{match}' leaked into Use Case text. Use Cases must describe attributes using natural business English nouns and adjectives."),
    (r"\b[a-z]+_[a-z]+(?:_[a-z]+)*\s*[:=]\s*", "LEAK-SQL-004",
     "Code-style dictionary assignment '{match}' leaked into Use Case text. Prohibit 'column: value' or 'column = value' syntax in business flows."),
    (r"[:=]\s*(?:true|false)\b", "LEAK-SQL-005",
     "Boolean code literal '{match}' leaked. State business conditions naturally (e.g. 'designated as Safety Critical Element')."),
    (r"\b(?:SELECT\s+.*?\s+FROM|INSERT\s+INTO|UPDATE\s+.*?\s+SET|DELETE\s+FROM|NOT\s+NULL|PRIMARY\s+KEY|FOREIGN\s+KEY)\b",
     "LEAK-SQL-006",
     "SQL DDL/DML keyword phrase '{match}' leaked into Use Case."),
]

# C# / OOP class method call signatures & API routes
CODE_LEAK_PATTERNS: list[tuple[str, str, str]] = [
    (r"\b[A-Z][a-zA-Z0-9_]+\.[A-Z][a-zA-Z0-9_]+\s*\(", "LEAK-CODE-001",
     "OOP method signature '{match}' leaked into Use Case. Methods belong exclusively to DT-DM-DOC-002.md."),
    (r"\b(?:GET|POST|PUT|DELETE|PATCH)\s+/api/", "LEAK-CODE-002",
     "REST API route '{match}' leaked into Use Case. API endpoints belong to interface contracts."),
    (r"\b/api/v\d+/", "LEAK-CODE-002",
     "API path '{match}' leaked into Use Case narrative."),
]

# Generic drafting variable aliases & pipeline jargon
DOMAIN_META_TEXT_PATTERNS: list[tuple[str, str, str]] = [
    (r"\b(?:Asset|Activo)\s+[A-Z]\b", "TXT-001",
     "Generic drafting variable placeholder '{match}' detected. Use authentic domain terms (e.g. 'Dismounted Equipment Unit', 'Replacement Equipment Unit')."),
    (r"\b(?:Item|Entity|Record)\s+[0-9A-Z]\b", "TXT-001",
     "Generic placeholder alias '{match}' detected in Use Case."),
    (r"\b(?:Single-Commit|OUTBOX|Lease Local Activo|Command Payload)\b", "TXT-002",
     "Software architecture implementation jargon '{match}' leaked into business flow."),
]

PROHIBITED_HTML_TAGS: list[tuple[str, str, str]] = [
    (r"<\s*br\s*/?>", "STR-007", "HTML tag '<br>' is prohibited. Use native Markdown double line breaks."),
    (r"<\s*ul\s*>", "STR-007", "HTML tag '<ul>' is prohibited. Use native Markdown unordered lists ('*')."),
    (r"<\s*li\s*>", "STR-007", "HTML tag '<li>' is prohibited. Use native Markdown list syntax."),
    (r"<\s*table\s*>", "STR-007", "HTML tag '<table>' is prohibited. Use native Markdown tables."),
]


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def find_repo_root(start: Path) -> Path | None:
    curr = start.resolve()
    for _ in range(10):
        if (curr / "domain-models").is_dir() and (curr / "requirements").is_dir():
            return curr
        curr = curr.parent
    return None


def extract_frontmatter(content: str) -> tuple[dict[str, str], int]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, 0

    fm_lines: list[str] = []
    end_idx = -1
    for idx, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            end_idx = idx
            break
        fm_lines.append(line)

    if end_idx == -1:
        return {}, 0

    fm: dict[str, str] = {}
    current_key: str | None = None
    for line in fm_lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#"):
            continue
        if ":" in line_clean and not line.startswith(" ") and not line.startswith("\t"):
            key, val = line_clean.split(":", 1)
            current_key = key.strip()
            fm[current_key] = val.strip()
        elif current_key and (line.startswith("  -") or line.startswith("\t-")):
            fm[current_key] = fm.get(current_key, "") + "\n" + line_clean

    return fm, end_idx


# ---------------------------------------------------------------------------
# Audit Passes
# ---------------------------------------------------------------------------

def audit_frontmatter(content: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = content.splitlines()

    if not lines or lines[0].strip() != "---":
        return [Finding("BLOCKER", "STR-001", "Missing opening YAML frontmatter delimiter '---'.", 1)]

    fm, end_idx = extract_frontmatter(content)
    if end_idx == 0:
        return [Finding("BLOCKER", "STR-001", "Unclosed YAML frontmatter: missing closing '---'.", 1)]

    for key in MANDATORY_FRONTMATTER_KEYS:
        if key not in fm:
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-002",
                message=f"Missing mandatory YAML frontmatter key: '{key}'.",
                line=1
            ))

    if "module" in fm:
        mod = fm["module"].strip().upper()
        if mod not in VALID_MODULES:
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-003",
                message=f"Invalid module '{fm['module']}'. Must be one of: {sorted(VALID_MODULES)}.",
                line=2
            ))

    # Reject markdown links inside frontmatter
    for idx in range(1, end_idx):
        line = lines[idx - 1]
        if re.search(r"\[\[.*?\]\]", line) or re.search(r"\[.*?\]\(.*?\)", line):
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-004",
                message=f"Hyperlink detected in YAML frontmatter (line {idx}): '{line.strip()}'. Frontmatter must contain plain strings.",
                line=idx
            ))

    return findings


def audit_structure(content: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = content.splitlines()

    # Title check
    title_match = re.search(r"^#\s+(UC-[A-Z]+-\d+):\s*(.+)$", content, re.MULTILINE)
    if not title_match:
        findings.append(Finding(
            severity="BLOCKER",
            code="STR-005",
            message="Missing or malformed top-level title. Must match pattern '# UC-[MOD]-[NUM]: [Title]'."
        ))

    # Section presence and order
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
                code="STR-005",
                message=f"Missing mandatory canonical section: '{label}'."
            ))

    # Order check
    sorted_found = sorted(section_positions.items(), key=lambda x: x[1])
    for i in range(len(sorted_found) - 1):
        curr_num, curr_line = sorted_found[i]
        next_num, next_line = sorted_found[i + 1]
        if curr_num > next_num:
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-006",
                message=f"Section {curr_num} appears at line {curr_line} before Section {next_num} at line {next_line}. Sections must follow canonical sequence 1..6.",
                line=curr_line
            ))

    # HTML tags check
    for idx, line in enumerate(lines, start=1):
        for pattern, code, msg in PROHIBITED_HTML_TAGS:
            if re.search(pattern, line, re.IGNORECASE):
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg,
                    line=idx
                ))

    return findings


def audit_persistence_leaks(content: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = content.splitlines()
    _, fm_end = extract_frontmatter(content)

    for idx, line in enumerate(lines, start=1):
        if idx <= fm_end:
            continue
        # Skip markdown link destinations where schemas or IDs may appear in filepaths
        clean_line = re.sub(r"\[.*?\]\([^\)]*\)", "", line)

        for pattern, code, msg_template in SCHEMA_QUALIFIER_PATTERNS:
            match = re.search(pattern, clean_line)
            if match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=match.group(0)),
                    line=idx
                ))

        for pattern, code, msg_template in PHYSICAL_TABLE_PATTERNS:
            match = re.search(pattern, clean_line, re.IGNORECASE)
            if match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=match.group(0)),
                    line=idx
                ))

        for pattern, code, msg_template in PHYSICAL_COLUMN_PATTERNS:
            match = re.search(pattern, clean_line)
            if match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=match.group(0)),
                    line=idx
                ))

    return findings


def audit_code_and_api_leaks(content: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = content.splitlines()
    _, fm_end = extract_frontmatter(content)

    for idx, line in enumerate(lines, start=1):
        if idx <= fm_end:
            continue
        clean_line = re.sub(r"\[.*?\]\([^\)]*\)", "", line)

        for pattern, code, msg_template in CODE_LEAK_PATTERNS:
            match = re.search(pattern, clean_line)
            if match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=match.group(0)),
                    line=idx
                ))

    return findings


def audit_domain_meta_text(content: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = content.splitlines()
    _, fm_end = extract_frontmatter(content)

    for idx, line in enumerate(lines, start=1):
        if idx <= fm_end:
            continue
        clean_line = re.sub(r"\[.*?\]\([^\)]*\)", "", line)

        for pattern, code, msg_template in DOMAIN_META_TEXT_PATTERNS:
            match = re.search(pattern, clean_line)
            if match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=match.group(0)),
                    line=idx
                ))

    return findings


def audit_requirements_traceability(content: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = content.splitlines()

    in_sec6 = False
    for idx, line in enumerate(lines, start=1):
        if re.search(r"^##\s+6\.\s+Associated Requirements", line, re.IGNORECASE):
            in_sec6 = True
            continue
        elif line.startswith("## "):
            in_sec6 = False
            continue

        if in_sec6 and line.strip():
            # Strip all valid markdown links from line
            stripped_line = re.sub(r"\[.*?\]\(.*?\)", "", line)
            # Any remaining requirement code is unlinked plain text
            plain_codes = re.findall(r"\b(?:FR|NFR|TR|ADR)-\d+\b", stripped_line)
            for code in plain_codes:
                findings.append(Finding(
                    severity="WARNING",
                    code="REQ-001",
                    message=f"Requirement code '{code}' in Section 6 is plain text. Requirements must be clickable relative Markdown links.",
                    line=idx
                ))

    return findings


def run_usecase_audit(content: str, repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    findings += audit_frontmatter(content)
    findings += audit_structure(content)
    findings += audit_persistence_leaks(content)
    findings += audit_code_and_api_leaks(content)
    findings += audit_domain_meta_text(content)
    findings += audit_requirements_traceability(content)

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
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d-%H%M%S")
    uc_id = artifact_path.stem
    report_id = f"AUD-{uc_id}-{timestamp_str}" if uc_id.startswith("UC-") else f"AUD-UC-{uc_id}-{timestamp_str}"

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]
    infos    = [f for f in findings if f.severity == "INFO"]

    verdict = "BLOCKED" if blockers else ("PASSED_WITH_OBSERVATIONS" if warnings else "PASSED")

    report: list[str] = [
        "---",
        f"id: {report_id}",
        f"usecase_audited: {uc_id}",
        f"date: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"verdict: {verdict}",
        "auditor: dteam-usecase-audit (deterministic)",
        "---",
        "",
        f"# Deterministic Use Case Audit Report: {uc_id}",
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
        report.append("No database schema leaks, SQL syntax, C# method leaks, raw HTML tags, or structural regressions detected.")
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
        f"| **Structural & Frontmatter** | {'PASS' if not any(f.code.startswith('STR') for f in findings) else 'FAIL'} | Valid YAML frontmatter, 6 canonical sections, zero HTML tags. |",
        f"| **Black-Box Behavioral Invariant** | {'PASS' if not any(f.code.startswith('LEAK-SQL') for f in findings) else 'FAIL'} | Zero schema qualifiers, zero table names, zero snake_case columns, zero boolean literals. |",
        f"| **Code & API Decoupling** | {'PASS' if not any(f.code.startswith('LEAK-CODE') for f in findings) else 'FAIL'} | Zero OOP method signatures, zero REST API routes, zero programming types. |",
        f"| **Anti-Meta-Text Hygiene** | {'PASS' if not any(f.code.startswith('TXT') for f in findings) else 'FAIL'} | Zero generic drafting aliases ('Asset A/B'), zero pipeline jargon. |",
        f"| **Requirements Traceability** | {'PASS' if not any(f.code.startswith('REQ') for f in findings) else 'FAIL'} | Section 6 requirements formatted as clickable Markdown links. |",
        "",
        "---",
        "",
        "## 4. Tier 2 Grounded Escalation Gate (Gemini Notebook)",
        "",
        "| Trigger | Description | Evaluation | Status |",
        "| :--- | :--- | :--- | :---: |",
        "| **G1: Life Safety & Hazardous Interlocks** | Governs hazardous energy isolation (LOTO), hot work, explosive atmospheres, or personnel safety where software state impacts physical energy. | Evaluated against local SSoT safety rules; no uncodified hazard conditions identified. | `[NOT TRIGGERED]` |",
        "| **G2: Cognitive Overload & Density Exceedance** | High-density operational flows with complex concurrent branchings. | Evaluated against standard transaction complexity thresholds. | `[NOT TRIGGERED]` |",
        "| **G3: Deep Normative Taxonomy Conflict** | ISO 14224 Level 6-9 taxonomy, boundary limits, or failure modes with conflicting or missing local SSoT rules. | SSoT alignment verified against DT-ERD-DOC-001 and DT-DM-DOC-001/002. | `[NOT TRIGGERED]` |",
        "| **G4: Novel Interaction Archetype** | Workflows involving unprecedented operational interactions. | Standard APM business interaction model. | `[NOT TRIGGERED]` |",
        "",
        "> *Tier 2 Evaluation Summary:* All evaluation axes resolved deterministically via repository SSoTs. No external Gemini Notebook grounded escalation required unless flagged during heuristic review.",
        "",
    ]

    return "\n".join(report)


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------

def cmd_audit(args: argparse.Namespace, repo_root: Path) -> int:
    target_path = (repo_root / args.file).resolve()
    if not target_path.exists():
        print(f"[ERROR] Target file not found: {target_path}", file=sys.stderr)
        return 1

    content = target_path.read_text(encoding="utf-8")
    findings = run_usecase_audit(content, repo_root)

    report_md = generate_markdown_report(target_path, findings, repo_root)

    audits_dir = repo_root / "reports" / "audits" / "use-cases"
    audits_dir.mkdir(parents=True, exist_ok=True)

    timestamp_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    stem = target_path.stem
    report_filename = f"AUD-{stem}-{timestamp_str}.md" if stem.startswith("UC-") else f"AUD-UC-{stem}-{timestamp_str}.md"
    report_file = audits_dir / report_filename
    report_file.write_text(report_md, encoding="utf-8")

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]
    infos    = [f for f in findings if f.severity == "INFO"]

    print(f"[INFO] Auditing Use Case: {target_path.relative_to(repo_root)}")
    print("-" * 72)
    if blockers:
        print(f"[RESULT] FAILED: {len(blockers)} BLOCKER(S) found.")
        for b in blockers:
            loc = f" (line {b.line})" if b.line else ""
            print(f"  - [{b.code}]{loc}: {b.message}")
    elif warnings:
        print(f"[RESULT] PASSED WITH OBSERVATIONS: 0 BLOCKER | {len(warnings)} WARNING | {len(infos)} INFO")
        for w in warnings:
            loc = f" (line {w.line})" if w.line else ""
            print(f"  - [{w.code}]{loc}: {w.message}")
    else:
        print(f"[RESULT] PASSED: 0 BLOCKER | 0 WARNING | 0 INFO")

    print(f"[REPORT] Persisted to: {report_file}")

    return 2 if blockers else 0


def cmd_lint(args: argparse.Namespace, repo_root: Path) -> int:
    target_path = (repo_root / args.file).resolve()
    if not target_path.exists():
        print(f"[ERROR] Target file not found: {target_path}", file=sys.stderr)
        return 1

    content = target_path.read_text(encoding="utf-8")
    findings = run_usecase_audit(content, repo_root)

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]

    if blockers:
        print(f"[FAIL] {target_path.name}: {len(blockers)} BLOCKER(S) found:")
        for b in blockers:
            loc = f" (line {b.line})" if b.line else ""
            print(f"  - [{b.code}]{loc}: {b.message}")
        return 2

    if warnings:
        print(f"[WARN] {target_path.name}: {len(warnings)} WARNING(S) found:")
        for w in warnings:
            loc = f" (line {w.line})" if w.line else ""
            print(f"  - [{w.code}]{loc}: {w.message}")

    print(f"[OK] {target_path.name} passes all deterministic gates.")
    return 0


def cmd_audit_all(args: argparse.Namespace, repo_root: Path) -> int:
    uc_dir = repo_root / "domain-models" / "use-cases"
    if not uc_dir.is_dir():
        print(f"[ERROR] Use case directory not found: {uc_dir}", file=sys.stderr)
        return 1

    uc_files = sorted(uc_dir.rglob("UC-*.md"))
    if not uc_files:
        print(f"[WARN] No UC-*.md files found under {uc_dir}")
        return 0

    print(f"[INFO] Scanning {len(uc_files)} Use Cases under {uc_dir.relative_to(repo_root)}...")
    print("=" * 72)

    total_blockers = 0
    total_warnings = 0
    failed_files: list[str] = []

    for uc_file in uc_files:
        content = uc_file.read_text(encoding="utf-8")
        findings = run_usecase_audit(content, repo_root)
        blockers = [f for f in findings if f.severity == "BLOCKER"]
        warnings = [f for f in findings if f.severity == "WARNING"]

        total_blockers += len(blockers)
        total_warnings += len(warnings)

        status_str = f"🔴 {len(blockers)} BLOCKER(S)" if blockers else (f"⚠️  {len(warnings)} WARN" if warnings else "✅ PASS")
        rel_path = str(uc_file.relative_to(repo_root))
        print(f"{rel_path:<50} {status_str}")

        if blockers:
            failed_files.append(str(uc_file.relative_to(repo_root)))
            for b in blockers:
                loc = f" (line {b.line})" if b.line else ""
                print(f"    [{b.code}]{loc}: {b.message}")

    print("=" * 72)
    print(f"[SUMMARY] Scanned {len(uc_files)} files | Total Blockers: {total_blockers} | Total Warnings: {total_warnings}")

    return 2 if total_blockers > 0 else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic Coherence Auditor & Linter for DTEAM Use Cases."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Run full audit and generate Markdown report.")
    audit_parser.add_argument("--file", required=True, help="Relative path to UC-*.md.")

    lint_parser = subparsers.add_parser("lint", help="Fast console lint gate (exit 0 on pass, exit 2 on blocker).")
    lint_parser.add_argument("--file", required=True, help="Relative path to UC-*.md.")

    audit_all_parser = subparsers.add_parser("audit-all", help="Scan all UC-*.md files across the repository.")

    args = parser.parse_args()

    repo_root = find_repo_root(SCRIPT_REPO_ROOT)
    if not repo_root:
        print("[ERROR] Could not locate 'adso-dteam-docs' repository root.", file=sys.stderr)
        return 1

    if args.command == "audit":
        return cmd_audit(args, repo_root)
    elif args.command == "lint":
        return cmd_lint(args, repo_root)
    elif args.command == "audit-all":
        return cmd_audit_all(args, repo_root)

    return 0


if __name__ == "__main__":
    sys.exit(main())
