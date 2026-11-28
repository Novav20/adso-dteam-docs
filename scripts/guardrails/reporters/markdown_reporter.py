"""
Technical English Markdown audit report generator.
"""

from __future__ import annotations

from ..models import SEVERITY_BLOCKER, SEVERITY_INFO, SEVERITY_WARNING, AuditReport, Finding


def _escape_cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _format_section(title: str, items: list[Finding]) -> list[str]:
    out = [f"## {title} ({len(items)})", ""]
    if not items:
        out.append("*No findings.*")
        out.append("")
        return out

    out.extend(
        [
            "| Rule | Scope | Location | Message | Remediation |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
    )
    for f in items:
        loc = f"`{f.file}:{f.line}`" if f.line is not None else f"`{f.file}`"
        out.append(
            f"| `{f.rule_id}` | `{f.scope}` | {loc} | "
            f"{_escape_cell(f.message)} | {_escape_cell(f.remediation)} |"
        )
    out.append("")
    return out


def render_markdown(report: AuditReport) -> str:
    """Render an `AuditReport` as a clean GitHub-Flavored Markdown report."""
    summary = report.summary
    verdict = "PASS" if summary.passed else "FAIL"
    strict_label = "Enabled" if summary.strict_mode else "Disabled"

    blockers = [f for f in report.findings if f.severity == SEVERITY_BLOCKER]
    warnings = [f for f in report.findings if f.severity == SEVERITY_WARNING]
    infos = [f for f in report.findings if f.severity == SEVERITY_INFO]

    lines: list[str] = [
        "# DTEAM Guardrails Verification Report",
        "",
        f"- **Repository Root:** `{report.root}`",
        f"- **Scope:** `{report.scope}`",
        f"- **Strict Mode:** {strict_label}",
        f"- **Files Indexed:** {summary.files_scanned}",
        f"- **Rules Evaluated:** {summary.rules_evaluated}",
        f"- **Verdict:** **{verdict}**",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| :--- | ---: |",
        f"| BLOCKER | {summary.blocker} |",
        f"| WARNING | {summary.warning} |",
        f"| INFO | {summary.info} |",
        f"| Total Findings | {summary.total} |",
        "",
    ]

    if report.target_files:
        lines.append("## Target File Filter")
        lines.append("")
        for tf in report.target_files:
            lines.append(f"- `{tf}`")
        lines.append("")

    lines.extend(_format_section("Blocker Findings", blockers))
    lines.extend(_format_section("Warning Findings", warnings))
    lines.extend(_format_section("Informational Findings", infos))

    lines.extend(
        [
            "## Rules Evaluated",
            "",
            "| Rule ID | Name | Default Severity | Scopes | Implemented |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]
    )
    for spec in report.evaluated_rules:
        scopes_str = ", ".join(f"`{s}`" for s in spec.scopes)
        impl = "Yes" if spec.implemented else "Stub (Pending Batch G2)"
        lines.append(
            f"| `{spec.rule_id}` | {_escape_cell(spec.name)} | "
            f"`{spec.default_severity}` | {scopes_str} | {impl} |"
        )
    lines.append("")

    return "\n".join(lines)
