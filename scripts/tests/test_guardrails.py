"""Unit tests for DTEAM architectural & documentation guardrails."""

from __future__ import annotations

import sys
import unittest
from types import SimpleNamespace
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from guardrails.models import Finding  # noqa: E402
from guardrails.parsers import RepoIndex  # noqa: E402
from guardrails.rules import run_rules  # noqa: E402
from guardrails.rules.hygiene_ssot import evaluate_grd_19  # noqa: E402


def _make_index_with_screen(screen_text: str) -> RepoIndex:
    root = Path(".").resolve()
    idx = RepoIndex(root=root, prototype_dir=None)
    idx.screen_docs["ui-ux/screens/vis/SCR-VIS-TEST.md"] = SimpleNamespace(
        rel_path="ui-ux/screens/vis/SCR-VIS-TEST.md",
        raw_text=screen_text,
    )
    return idx


def _scr_findings(findings: list[Finding]) -> list[Finding]:
    return [f for f in findings if f.file == "ui-ux/screens/vis/SCR-VIS-TEST.md"]


class TestGuardrailsTokCssNegativeControls(unittest.TestCase):
    """Migrated TOK-003, CSS-002, and negative-control tests under GRD-19."""

    def test_tok003_token_literal_shadowing_comma_latex(self) -> None:
        idx = _make_index_with_screen(
            "Context Container CMP-05 docks as lateral panel "
            "(sized by --dt-layout-drawer-width-tablet, $380\\text{px}$, "
            "strictly preserving $\\ge 70\\%$ canvas visibility)."
        )
        self.assertTrue(_scr_findings(evaluate_grd_19(idx)))

    def test_tok003_token_literal_shadowing_parenthetical_raw_px(self) -> None:
        idx = _make_index_with_screen(
            "Drawer sized by --dt-layout-drawer-width-tablet (380px)."
        )
        self.assertTrue(_scr_findings(evaluate_grd_19(idx)))

    def test_tok003_token_literal_shadowing_colon(self) -> None:
        idx = _make_index_with_screen(
            "Corner radius is governed by --dt-radius-lg: 12px."
        )
        self.assertTrue(_scr_findings(evaluate_grd_19(idx)))

    def test_css002_raw_css_dimension_declaration_leak(self) -> None:
        idx = _make_index_with_screen(
            "The lateral container specifies width: 380px; on tablet viewport."
        )
        self.assertTrue(_scr_findings(evaluate_grd_19(idx)))

    def test_negative_control_clean_token_reference(self) -> None:
        idx = _make_index_with_screen(
            "Context Container `CMP-05` docks as lateral panel "
            "(sized by `--dt-layout-drawer-width-tablet`, strictly preserving $\\ge 70\\%$ canvas visibility)."
        )
        self.assertEqual(_scr_findings(evaluate_grd_19(idx)), [])

    def test_negative_control_physical_equipment_dimension(self) -> None:
        idx = _make_index_with_screen(
            "Atmospheric Tank API-650 (27.2m dia x 12m) operating in Process Area 01."
        )
        self.assertEqual(_scr_findings(evaluate_grd_19(idx)), [])


class TestFindingAffectedFilesFilter(unittest.TestCase):
    """Verify --files filter retains cross-file findings via affected_files."""

    def test_affected_files_retained_by_run_rules(self) -> None:
        f = Finding(
            rule_id="GRD-13",
            severity="BLOCKER",
            scope="api",
            file="architecture/views/DT-ARQ-CMP-DOC-001.md",
            line=10,
            message="Test cross-file finding",
            remediation="Fix it",
            affected_files=("ui-ux/screens/adm/SCR-ADM-013.md",),
        )
        self.assertIn("ui-ux/screens/adm/SCR-ADM-013.md", f.affected_files)
        self.assertIsNotNone(run_rules)


if __name__ == "__main__":
    unittest.main()
