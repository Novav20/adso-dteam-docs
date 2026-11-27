"""
Human-readable Technical English console reporter.
"""

from __future__ import annotations

from ..models import AuditReport


def render_console(report: AuditReport) -> str:
    """Format an `AuditReport` for terminal output."""
    summary = report.summary
    verdict = "PASS" if summary.passed else "FAIL"
    strict_note = " (strict: warnings treated as failures)" if summary.strict_mode else ""

    lines: list[str] = [
        "=" * 76,
        "DTEAM ARCHITECTURAL & DOCUMENTATION GUARDRAILS REPORT",
        "=" * 76,
        f"Repository Root : {report.root}",
        f"Scope           : {report.scope}",
        f"Rules Evaluated : {summary.rules_evaluated}",
        f"Files Indexed   : {summary.files_scanned}",
    ]
    if report.target_files:
        lines.append(f"Target Files    : {', '.join(report.target_files)}")
    lines.extend(
        [
            (
                f"Findings        : {summary.blocker} BLOCKER | "
                f"{summary.warning} WARNING | {summary.info} INFO"
            ),
            f"Verdict         : {verdict}{strict_note}",
            "=" * 76,
        ]
    )

    if not report.findings:
        lines.append("PASS: No guardrail violations detected.")
        return "\n".join(lines)

    lines.append("")
    for f in report.findings:
        loc = f"{f.file}:{f.line}" if f.line is not None else f.file
        lines.append(f"[{f.severity}][{f.rule_id}][{f.scope}] {loc} - {f.message}")
        lines.append(f"  Remediation: {f.remediation}")

    return "\n".join(lines)
