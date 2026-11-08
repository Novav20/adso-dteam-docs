#!/usr/bin/env python3
"""
Mutation & Regression Test Suite for audit.py
=============================================
Verifies deterministic prevention of:
- TOK-003: Token-literal shadowing (--dt-* followed by raw px/rem/pt)
- CSS-002: Raw CSS dimension declarations in prose (width:, border-radius:, padding:, etc.)
- TOK-002: Hardcoded dimensions or raw hex colors in Section 3 Semantic Token column
- Negative controls: Invariant non-regressions for valid domain dimensions, breakpoints, and clean tokens.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Add script directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from audit import audit_tokens, audit_css_and_dimension_leaks, Finding


def run_mutation_tests() -> int:
    # Minimal mock set of valid tokens for testing
    valid_tokens = {
        "--dt-layout-drawer-width-tablet",
        "--dt-layout-drawer-width-desktop",
        "--dt-color-surface-drawer",
        "--dt-color-border-panel",
        "--dt-radius-lg",
        "--dt-space-4",
    }

    test_cases = [
        # --- Positive Mutation Cases (Must Trigger Blockers) ---
        {
            "name": "Regression Case: Comma Token-Literal Shadowing ($380\\text{px}$)",
            "content": "Context Container CMP-05 docks as lateral panel (sized by --dt-layout-drawer-width-tablet, $380\\text{px}$, strictly preserving $\\ge 70\\%$ canvas visibility).",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": "TOK-003",
            "expected_severity": "BLOCKER",
            "must_hit": True,
        },
        {
            "name": "Parenthetical Token Shadowing with LaTeX ($380\\text{px}$)",
            "content": "Drawer sized by --dt-layout-drawer-width-tablet ($380\\text{px}$).",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": "TOK-003",
            "expected_severity": "BLOCKER",
            "must_hit": True,
        },
        {
            "name": "Parenthetical Token Shadowing with raw px (380px)",
            "content": "Drawer sized by --dt-layout-drawer-width-tablet (380px).",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": "TOK-003",
            "expected_severity": "BLOCKER",
            "must_hit": True,
        },
        {
            "name": "Colon Token Shadowing (--dt-radius-lg: 12px)",
            "content": "Corner radius is governed by --dt-radius-lg: 12px.",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": "TOK-003",
            "expected_severity": "BLOCKER",
            "must_hit": True,
        },
        {
            "name": "Equals Token Shadowing (--dt-space-4 = 16px)",
            "content": "Padding follows --dt-space-4 = 16px.",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": "TOK-003",
            "expected_severity": "BLOCKER",
            "must_hit": True,
        },
        {
            "name": "Prose CSS Dimension Declaration Leak (width: 380px)",
            "content": "The lateral container specifies width: 380px; on tablet viewport.",
            "audit_fn": lambda c: audit_css_and_dimension_leaks(c),
            "expected_code": "CSS-002",
            "expected_severity": "BLOCKER",
            "must_hit": True,
        },
        {
            "name": "Prose CSS Dimension Declaration Leak (border-radius: 20px)",
            "content": "The drawer edge has border-radius: 20px; applied.",
            "audit_fn": lambda c: audit_css_and_dimension_leaks(c),
            "expected_code": "CSS-002",
            "expected_severity": "BLOCKER",
            "must_hit": True,
        },
        {
            "name": "Section 3 Raw Dimension in Semantic Token Column",
            "content": "## 3. Functional Component Inventory\n\n| ID | Control | Role | Semantic Token | Reference |\n| :--- | :--- | :--- | :--- | :--- |\n| `CMP-05` | Drawer | Lateral panel | Width: 380px | §5.2 |",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": "TOK-002",
            "expected_severity": "BLOCKER",
            "must_hit": True,
        },
        {
            "name": "Section 3 Raw Hex Color in Semantic Token Column",
            "content": "## 3. Functional Component Inventory\n\n| ID | Control | Role | Semantic Token | Reference |\n| :--- | :--- | :--- | :--- | :--- |\n| `CMP-05` | Drawer | Lateral panel | Surface: #1e293b | §5.2 |",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": "TOK-002",
            "expected_severity": "BLOCKER",
            "must_hit": True,
        },

        # --- Negative Control Cases (Must PASS with Zero Findings) ---
        {
            "name": "Negative Control: Clean Token Reference (No Shadowing)",
            "content": "Context Container CMP-05 docks as lateral panel (sized by --dt-layout-drawer-width-tablet, strictly preserving $\\ge 70\\%$ canvas visibility).",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": None,
            "must_hit": False,
        },
        {
            "name": "Negative Control: Physical Equipment Dimension (27.2m ø × 12m)",
            "content": "Tanque Atmosférico API-650 (27.2m ø × 12m) operating in Process Area 01.",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": None,
            "must_hit": False,
        },
        {
            "name": "Negative Control: Viewport Breakpoint Range (1280px - 1919px)",
            "content": "Responsive tier for Tablet Landscape (1280px - 1919px) displays lateral docked drawer.",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": None,
            "must_hit": False,
        },
        {
            "name": "Negative Control: Target Display Resolution ($1280 \\times 800\\text{px}$)",
            "content": "Target physical device displays $1280 \\times 800\\text{px}$ resolution at standard DPI.",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": None,
            "must_hit": False,
        },
        {
            "name": "Negative Control: Section 3 Clean Semantic Tokens",
            "content": "## 3. Functional Component Inventory\n\n| ID | Control | Role | Semantic Token | Reference |\n| :--- | :--- | :--- | :--- | :--- |\n| `CMP-05` | Drawer | Lateral panel | Surface: `--dt-color-surface-drawer`<br>Border: `--dt-color-border-panel` | §5.2 |",
            "audit_fn": lambda c: audit_tokens(c, valid_tokens),
            "expected_code": None,
            "must_hit": False,
        },
    ]

    total = len(test_cases)
    passed = 0
    failed = 0

    print("========================================================================")
    print("DTEAM UI Audit Mutation Test Suite (audit.py)")
    print("========================================================================")

    for tc in test_cases:
        findings: list[Finding] = tc["audit_fn"](tc["content"])
        
        if tc["must_hit"]:
            matches = [f for f in findings if f.code == tc["expected_code"] and f.severity == tc["expected_severity"]]
            if matches:
                print(f"[PASS] {tc['name']}")
                passed += 1
            else:
                print(f"[FAIL] {tc['name']} -> Expected {tc['expected_code']} ({tc['expected_severity']}), got: {[f.code for f in findings]}")
                failed += 1
        else:
            if not findings:
                print(f"[PASS] {tc['name']}")
                passed += 1
            else:
                print(f"[FAIL] {tc['name']} -> Expected 0 findings, got: {[f.code + ':' + f.message for f in findings]}")
                failed += 1

    print("------------------------------------------------------------------------")
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    print("========================================================================")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_mutation_tests())
