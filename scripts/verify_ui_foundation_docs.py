#!/usr/bin/env python3
"""
Deterministic Guardrail Linter for UI/UX Foundation Specifications
==================================================================
Validates structural boundaries, token discipline, and framework-agnostic
purity across:
  - ui-ux/DT-UI-DS-DOC-001.md
  - ui-ux/DT-UI-SVG-DOC-001.md
  - ui-ux/DT-UI-NAV-DOC-001.md

Exit codes:
  0 = PASS (zero violations)
  1 = FAIL (one or more contract violations)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DS_DOC = ROOT / "ui-ux" / "DT-UI-DS-DOC-001.md"
SVG_DOC = ROOT / "ui-ux" / "DT-UI-SVG-DOC-001.md"
NAV_DOC = ROOT / "ui-ux" / "DT-UI-NAV-DOC-001.md"

SQL_TABLE_RE = re.compile(r"\b(?:tax|mtto|inv|vis|adm)\.[a-z][a-z0-9_]+\b")
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")
SYM_ICON_RE = re.compile(r"\bsym-icon-[a-z0-9-]+\b")
RULE_PREFIX_RE = re.compile(r"\*\*Rule\s+\d+\s*[—-]")


def relative_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def audit_ds_doc(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_section_31 = False
    seen_tokens: dict[str, int] = {}
    family_luminance: dict[str, list[tuple[int, str, str, float]]] = {"gray": [], "slate": []}

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped.startswith("### 3.1."):
            in_section_31 = True
        elif stripped.startswith("### ") and not stripped.startswith("### 3.1."):
            in_section_31 = False

        # 1. No #sym-icon-* leaks
        if SYM_ICON_RE.search(line):
            errors.append(f"DS-DOC:{idx}: Forbidden '#sym-icon-*' reference found.")

        # 2. No SQL schema/table leaks
        if SQL_TABLE_RE.search(line):
            errors.append(f"DS-DOC:{idx}: SQL persistence table leak ({SQL_TABLE_RE.search(line).group(0)}).")

        # 3. No Blazor/Razor component leaks
        if re.search(r"\b(?:ViewportToolbar|UserProfileButton|CartographicHud)\b|\.razor\b", line):
            errors.append(f"DS-DOC:{idx}: Framework/Razor component leak in Design System spec.")

        # 4. No raw HEX outside §3.1 (except #FFFFFF / #000000 prohibition note)
        if not in_section_31:
            for match in HEX_RE.finditer(line):
                hex_val = match.group(0).upper()
                if hex_val in ("#FFFFFF", "#000000") and "prohibited" in line.lower():
                    continue
                errors.append(f"DS-DOC:{idx}: Raw HEX '{hex_val}' outside Section 3.1 Primitive Palette.")

        # 5. Table-level checks
        if stripped.startswith("|"):
            cells = [c.strip().strip("`") for c in stripped.strip("|").split("|")]

            # No var(...) CSS syntax in token tables
            if "var(" in stripped:
                errors.append(f"DS-DOC:{idx}: CSS 'var(...)' syntax prohibited in DS-DOC tables; use bare '--dt-*' token names.")

            # Consistent Dark | Light column ordering
            lower_line = stripped.lower()
            if "dark theme" in lower_line and "light theme" in lower_line:
                if lower_line.index("light theme") < lower_line.index("dark theme"):
                    errors.append(f"DS-DOC:{idx}: Inverted theme columns (Light before Dark); standard order is Dark | Light.")

            # Primitive luminance monotonicity in §3.1
            if in_section_31 and len(cells) >= 2 and cells[0].startswith("--dt-primitive-"):
                tok, hex_val = cells[0], cells[1]
                if HEX_RE.fullmatch(hex_val):
                    for fam in ("gray", "slate"):
                        if tok.startswith(f"--dt-primitive-{fam}-"):
                            family_luminance[fam].append((idx, tok, hex_val, relative_luminance(hex_val)))

            # Duplicate token declarations across §§2–5
            if len(cells) >= 2:
                tok_candidate = cells[0] if cells[0].startswith("--dt-") else (cells[1] if cells[1].startswith("--dt-") else "")
                if tok_candidate and not stripped.startswith("| **"):
                    if tok_candidate in seen_tokens:
                        errors.append(f"DS-DOC:{idx}: Duplicate token declaration '{tok_candidate}' (first declared at line {seen_tokens[tok_candidate]}).")
                    else:
                        seen_tokens[tok_candidate] = idx

    for fam, entries in family_luminance.items():
        for prev, curr in zip(entries, entries[1:]):
            if curr[3] < prev[3] - 1e-6:
                errors.append(
                    f"DS-DOC:{curr[0]}: Non-monotonic luminance in '{fam}' scale: "
                    f"{curr[1]} ({curr[2]}) is darker than preceding {prev[1]} ({prev[2]})."
                )

    return errors


def audit_svg_doc(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    last_sub: dict[int, int] = {}

    for idx, line in enumerate(lines, start=1):
        if SYM_ICON_RE.search(line):
            errors.append(f"SVG-DOC:{idx}: Forbidden '#sym-icon-*' reference found.")
        if HEX_RE.search(line):
            errors.append(f"SVG-DOC:{idx}: Raw HEX '{HEX_RE.search(line).group(0)}' prohibited; reference DS-DOC tokens.")
        if SQL_TABLE_RE.search(line):
            errors.append(f"SVG-DOC:{idx}: SQL persistence table leak ({SQL_TABLE_RE.search(line).group(0)}).")
        if re.search(r"\bC#\b", line):
            errors.append(f"SVG-DOC:{idx}: Language implementation leak ('C#') in SVG contract.")
        if "is_safety_critical" in line:
            errors.append(f"SVG-DOC:{idx}: Non-canonical attribute 'is_safety_critical'; use 'data-safety-critical'.")
        if RULE_PREFIX_RE.search(line):
            errors.append(f"SVG-DOC:{idx}: Redundant copy-paste 'Rule N —' prefix.")

        sub_match = re.match(r"^###\s+(\d+)\.(\d+)\b", line.strip())
        if sub_match:
            major, minor = int(sub_match.group(1)), int(sub_match.group(2))
            expected = last_sub.get(major, 0) + 1
            if minor != expected:
                errors.append(f"SVG-DOC:{idx}: Skipped sub-section numbering (found {major}.{minor}, expected {major}.{expected}).")
            last_sub[major] = minor

    return errors


def audit_nav_doc(path: Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    for idx, line in enumerate(lines, start=1):
        if SYM_ICON_RE.search(line):
            errors.append(f"NAV-DOC:{idx}: Forbidden '#sym-icon-*' reference found.")
        if SQL_TABLE_RE.search(line):
            errors.append(f"NAV-DOC:{idx}: SQL persistence table leak ({SQL_TABLE_RE.search(line).group(0)}).")
        tech_match = re.search(r"\b(?:MAUI|Blazor|SQLCipher|C#)\b", line)
        if tech_match:
            errors.append(f"NAV-DOC:{idx}: Framework/storage leak ('{tech_match.group(0)}') in navigation spec.")
        if "Isolation Points == TRUE" in line:
            errors.append(f"NAV-DOC:{idx}: Non-canonical LOTO guard 'Isolation Points == TRUE'; use 'IsolationStatus == VERIFIED_ZERO_ENERGY'.")

    return errors


def main() -> int:
    all_errors: list[str] = []
    for label, path, fn in (
        ("DT-UI-DS-DOC-001", DS_DOC, audit_ds_doc),
        ("DT-UI-SVG-DOC-001", SVG_DOC, audit_svg_doc),
        ("DT-UI-NAV-DOC-001", NAV_DOC, audit_nav_doc),
    ):
        if not path.exists():
            all_errors.append(f"{label}: File not found at {path}")
            continue
        all_errors.extend(fn(path))

    if all_errors:
        print(f"UI Foundation Docs Audit FAILED ({len(all_errors)} violation(s)):")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("UI Foundation Docs Audit PASSED (DT-UI-DS-DOC-001, DT-UI-SVG-DOC-001, DT-UI-NAV-DOC-001): 0 violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
