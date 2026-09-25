#!/usr/bin/env python3
"""
DTEAM SRS Quality Auditor
Validates raw requirements (srs.csv) against:
1. Domain-Driven Design (DDD) Vocabulary (e.g., ISO 14224 Equipment Unit vs "activo")
2. ISO 25010:2023 Categories (strict adherence, no deprecated terms like 'Usability')
3. Normative References (ensuring actionable architecture/security references)
"""

import csv
import re
import sys
from datetime import datetime
from pathlib import Path

# Configuration constants
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
SRS_PATH = REPO_ROOT / "requirements" / "data" / "srs.csv"
import datetime as _dt
REPORT_DIR = REPO_ROOT.parent / "sena-evidence" / "00-Overview" / "Audits" / "SRS"
REPORT_PATH = REPORT_DIR / f"AUD-SRS-QUALITY-{_dt.datetime.now().strftime('%Y%m%d')}.md"

ISO_25010_2023_CATEGORIES = {
    "Functional Suitability",
    "Performance Efficiency",
    "Compatibility",
    "Interaction Capability",
    "Reliability",
    "Security",
    "Maintainability",
    "Flexibility",
    "Safety"
}

FORBIDDEN_WORDS = {
    r"\bactivo\b": "Equipment Unit / Maintainable Item (ISO 14224)",
    r"\bactivos\b": "Equipment Units (ISO 14224)",
    r"\busability\b": "Interaction Capability (ISO 25010:2023)",
    r"\bportability\b": "Flexibility (ISO 25010:2023)",
}

VALID_REFS_REGEX = r"(ISO|NIST|OWASP|ACID|W3C|IETF|RFC|WCAG|NN/g|Nielsen|High Performance HMI|Enterprise Integration|FinOps|GDPR|RESTful|IEEE|FIPS|ACME|Token Bucket|Asynchronous|Offline-First|Role-Based|Attribute-Based|WORM|WebSockets?|SSE|SPA)"

def clean(val: str) -> str:
    return val.strip() if val else ""

def generate_markdown_report(findings, total_rows):
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    total_blockers = len(findings["BLOCKER"])
    total_warnings = len(findings["WARNING"])
    total_infos = len(findings["INFO"])
    
    status = "✅ PASSED"
    if total_blockers > 0:
        status = "🔴 BLOCKER"
    elif total_warnings > 0:
        status = "🟠 PASSED WITH WARNINGS"

    lines = [
        "# DTEAM SRS Quality & Domain Audit",
        "",
        f"**Date Executed:** {date_str}",
        f"**Target Source:** `adso-dteam-docs/requirements/data/srs.csv`",
        f"**Status:** {status}",
        "",
        "## 📊 Executive Summary",
        f"- **Requirements Scanned:** {total_rows}",
        f"- **Blockers (Critical Failures):** {total_blockers}",
        f"- **Warnings (Domain/Standards Violations):** {total_warnings}",
        f"- **Info (Recommendations):** {total_infos}",
        "",
        "---",
        ""
    ]

    if total_blockers > 0:
        lines.append("## 🔴 Blockers")
        lines.append("> [!WARNING]")
        lines.append("> These issues break architectural constraints or MVP definitions and MUST be resolved before integrating the dataset.")
        lines.append("")
        for f in findings["BLOCKER"]:
            lines.append(f"- {f}")
        lines.append("")

    if total_warnings > 0:
        lines.append("## 🟠 Domain & Standards Warnings")
        lines.append("> [!NOTE]")
        lines.append("> These issues represent deviations from the Ubiquitous Language (DDD) or lack strict Normative References. They should be corrected for maximum quality.")
        lines.append("")
        for f in findings["WARNING"]:
            lines.append(f"- {f}")
        lines.append("")

    if total_infos > 0:
        lines.append("## 🔵 Opportunities for Improvement")
        for f in findings["INFO"]:
            lines.append(f"- {f}")
        lines.append("")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    return REPORT_PATH

def run_audit():
    if not SRS_PATH.exists():
        print(f"❌ Error: srs.csv not found in {SRS_PATH}")
        sys.exit(1)

    print(f"🔍 Auditando {SRS_PATH.relative_to(REPO_ROOT)}...\n")
    
    findings = {
        "BLOCKER": [],
        "WARNING": [],
        "INFO": []
    }
    
    total_rows = 0
    try:
        with open(SRS_PATH, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            
            headers = reader.fieldnames or []
            required_headers = ["Req ID", "Description", "ISO 25010:2023 Category", "Normative Reference"]
            for h in required_headers:
                if h not in headers:
                    findings["BLOCKER"].append(f"Header Missing: La columna '{h}' no existe en el CSV.")
            
            if findings["BLOCKER"]:
                generate_markdown_report(findings, 0)
                print(f"❌ Structure validation failed. Report at: {REPORT_PATH}")
                return 2

            for row_num, row in enumerate(reader, start=2):
                req_id = clean(row.get("Req ID", f"Fila {row_num}"))
                desc = clean(row.get("Description", ""))
                cat = clean(row.get("ISO 25010:2023 Category", ""))
                ref = clean(row.get("Normative Reference", ""))
                
                if not req_id:
                    continue
                    
                total_rows += 1
                
                # 1. Validate ISO 25010:2023
                if cat and cat not in ISO_25010_2023_CATEGORIES:
                    findings["BLOCKER"].append(f"**[{req_id}]** Invalid Category: `{cat}` is not a valid ISO 25010:2023 standard.")
                
                # 2. Validate Domain Language (Description)
                desc_lower = desc.lower()
                for pattern, recommendation in FORBIDDEN_WORDS.items():
                    if re.search(pattern, desc_lower):
                        word_found = pattern.replace(r'\b', '')
                        findings["WARNING"].append(f"**[{req_id}]** DDD Violation: `{word_found}` detected in description. Should be `{recommendation}`.")
                
                # 3. Validate Normative Reference
                if ref:
                    if not re.search(VALID_REFS_REGEX, ref, re.IGNORECASE):
                        findings["WARNING"].append(f"**[{req_id}]** Weak Reference: `{ref}` does not appear to be a rigorous standard (ISO, NIST, OWASP, etc.).")
                else:
                    if "-FR-" in req_id or "-NFR-" in req_id or req_id.startswith("TR-"):
                        findings["BLOCKER"].append(f"**[{req_id}]** Missing Reference: Technical Requirements (TR) require a 'Normative Reference'.")
                    else:
                        findings["INFO"].append(f"**[{req_id}]** Missing Reference: Adding a standard is recommended.")
                        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
        
    report_file = generate_markdown_report(findings, total_rows)
    print(f"📄 Report generated at:\n  {report_file.relative_to(REPO_ROOT.parent)}\n")
    
    if findings["BLOCKER"]:
        print("🔴 Status: BLOCKER (Immediate action required)")
        sys.exit(2)
    elif findings["WARNING"]:
        print("🟠 Status: PASSED WITH WARNINGS (Corrections recommended)")
        sys.exit(0)
    else:
        print("✅ Status: PASSED (Dataset complies with all standards)")
        sys.exit(0)

if __name__ == "__main__":
    run_audit()
