"""
Guardrail rule registry and scope/filter resolver (`GRD-01`..`GRD-21`).

Batch G1 registers all 21 rule specifications with deterministic no-op stubs
that return empty finding lists until rule implementations are added in Batch G2.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from ..config import VALID_SCOPES
from ..models import RULE_SPECS, SEVERITY_ORDER, Finding, RuleSpec
from ..parsers import RepoIndex

RuleFunc = Callable[[RepoIndex], list[Finding]]


def _unimplemented_rule(_index: RepoIndex) -> list[Finding]:
    return []


RULE_REGISTRY: dict[str, tuple[RuleSpec, RuleFunc]] = {
    spec.rule_id: (spec, _unimplemented_rule) for spec in RULE_SPECS
}


def register_rule(spec: RuleSpec, func: RuleFunc) -> None:
    """Register or replace a rule implementation in `RULE_REGISTRY`."""
    RULE_REGISTRY[spec.rule_id] = (spec, func)


def parse_rule_id_args(raw_rules: list[str] | None) -> list[str] | None:
    """Normalize `--rules` CLI arguments (supports space-separated and comma-separated IDs)."""
    if not raw_rules:
        return None
    normalized: list[str] = []
    for token in raw_rules:
        for item in token.split(","):
            cleaned = item.strip().upper()
            if cleaned and cleaned not in normalized:
                normalized.append(cleaned)
    return normalized or None


def resolve_rules(
    scope: str = "all",
    rule_ids: list[str] | None = None,
) -> list[tuple[RuleSpec, RuleFunc]]:
    """Resolve active `(RuleSpec, RuleFunc)` entries matching `scope` and optional `rule_ids`."""
    norm_scope = scope.strip().lower()
    if norm_scope not in VALID_SCOPES:
        valid_str = ", ".join(VALID_SCOPES)
        raise ValueError(f"Unknown scope '{scope}'. Valid scopes: {valid_str}.")

    requested_ids = parse_rule_id_args(rule_ids)
    if requested_ids is not None:
        unknown = [rid for rid in requested_ids if rid not in RULE_REGISTRY]
        if unknown:
            raise ValueError(f"Unknown guardrail rule ID(s): {', '.join(unknown)}.")

    selected: list[tuple[RuleSpec, RuleFunc]] = []
    for spec in RULE_SPECS:
        registered_spec, func = RULE_REGISTRY[spec.rule_id]
        if norm_scope != "all" and norm_scope not in registered_spec.scopes:
            continue
        if requested_ids is not None and registered_spec.rule_id not in requested_ids:
            continue
        selected.append((registered_spec, func))

    return selected


def normalize_target_files(root: Path, raw_files: list[str] | None) -> tuple[str, ...]:
    """Normalize `--files` entries to repository-relative POSIX paths."""
    if not raw_files:
        return ()
    resolved_root = root.resolve()
    normalized: list[str] = []
    for item in raw_files:
        for part in item.split(","):
            raw = part.strip()
            if not raw:
                continue
            candidate = Path(raw)
            if candidate.is_absolute():
                try:
                    rel = candidate.resolve().relative_to(resolved_root).as_posix()
                except ValueError:
                    rel = candidate.as_posix()
            else:
                rel = raw.replace("\\", "/").lstrip("./")
            if rel not in normalized:
                normalized.append(rel)
    return tuple(normalized)


def run_rules(
    index: RepoIndex,
    scope: str = "all",
    rule_ids: list[str] | None = None,
    target_files: list[str] | None = None,
) -> tuple[tuple[RuleSpec, ...], list[Finding], tuple[str, ...]]:
    """Execute resolved rules against `RepoIndex`, applying optional file filtering and sorting."""
    resolved = resolve_rules(scope=scope, rule_ids=rule_ids)
    norm_files = normalize_target_files(index.root, target_files)
    file_filter = set(norm_files)

    raw_findings: list[Finding] = []
    for _spec, func in resolved:
        raw_findings.extend(func(index))

    if file_filter:
        raw_findings = [
            f for f in raw_findings if f.file.replace("\\", "/").lstrip("./") in file_filter
        ]

    # Deduplicate and sort deterministically
    seen: set[tuple[str, str, str, int | None, str]] = set()
    unique: list[Finding] = []
    for f in raw_findings:
        key = (f.rule_id, f.severity, f.file, f.line, f.message)
        if key not in seen:
            seen.add(key)
            unique.append(f)

    unique.sort(
        key=lambda f: (
            SEVERITY_ORDER.get(f.severity, 99),
            f.rule_id,
            f.file,
            f.line if f.line is not None else 0,
            f.message,
        )
    )

    specs = tuple(spec for spec, _ in resolved)
    return specs, unique, norm_files
