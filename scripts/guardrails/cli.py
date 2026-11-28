"""
Command-Line Interface for the DTEAM architectural and documentation guardrails suite.

Exit codes:
    0 - Verification passed (no BLOCKER findings, and no WARNING findings under --strict)
    1 - Runtime or configuration error (missing root, unknown scope/rule, I/O failure)
    2 - Verification failed due to guardrail findings
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .config import VALID_SCOPES
from .models import AuditReport
from .parsers import build_repo_index
from .reporters import render_console, render_json, render_markdown
from .rules import resolve_rules, run_rules


def _default_repo_root() -> Path:
    # scripts/guardrails/cli.py -> parents[2] is repository root
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="verify_all.py",
        description="Run cross-seam DTEAM Docs-as-Code architectural and UI guardrails.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=_default_repo_root(),
        help="Target repository root directory (defaults to parent of scripts/).",
    )
    parser.add_argument(
        "--prototype-dir",
        type=Path,
        default=None,
        help="Optional directory containing HTML/CSS/JS prototype screens.",
    )
    parser.add_argument(
        "--scope",
        choices=list(VALID_SCOPES),
        default="all",
        help="Guardrail verification scope filter (default: all).",
    )
    parser.add_argument(
        "--rules",
        nargs="+",
        default=None,
        help="Specific rule IDs to execute (e.g., GRD-01 GRD-04 or GRD-01,GRD-04).",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        default=None,
        help="Optional repository-relative file paths to filter reported findings.",
    )
    parser.add_argument(
        "--format",
        choices=["console", "json", "markdown"],
        default="console",
        help="Output report format (default: console).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output file path (defaults to stdout).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Treat WARNING findings as failures (exit code 2).",
    )
    parser.add_argument(
        "--list-rules",
        action="store_true",
        default=False,
        help="List guardrail rules matching --scope/--rules and exit.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        # Validate scope and rule IDs before indexing disk files
        selected = resolve_rules(scope=args.scope, rule_ids=args.rules)

        if args.list_rules:
            for spec, _ in selected:
                status = "implemented" if spec.implemented else "stub"
                scopes = ",".join(spec.scopes)
                print(
                    f"{spec.rule_id} [{spec.default_severity}] ({scopes}) [{status}] - {spec.name}"
                )
            return 0

        root = args.root.resolve()
        if not root.is_dir():
            print(
                f"[ERROR] Repository root directory does not exist: {root}",
                file=sys.stderr,
            )
            return 1

        index = build_repo_index(root=root, prototype_dir=args.prototype_dir)
        evaluated_specs, findings, norm_files = run_rules(
            index=index,
            scope=args.scope,
            rule_ids=args.rules,
            target_files=args.files,
        )

        report = AuditReport(
            root=str(root),
            scope=args.scope,
            evaluated_rules=evaluated_specs,
            findings=findings,
            files_scanned=index.total_files_indexed,
            strict_mode=args.strict,
            target_files=norm_files,
        )

        if args.format == "json":
            rendered = render_json(report)
        elif args.format == "markdown":
            rendered = render_markdown(report)
        else:
            rendered = render_console(report)

        if args.output is not None:
            out_path = args.output
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(rendered + "\n", encoding="utf-8")
        else:
            print(rendered)

        return 0 if report.summary.passed else 2

    except (ValueError, FileNotFoundError, OSError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - defensive runtime barrier
        print(f"[ERROR] Unexpected verification failure: {exc}", file=sys.stderr)
        return 1
