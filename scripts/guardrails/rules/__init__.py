"""
Guardrail rule registry and scope/filter resolver (`GRD-01`..`GRD-21`).

Wires all 21 pure Layer 2 rule evaluators from the five domain-named modules:
- `domain_erd_parity` (`GRD-01`..`GRD-04`)
- `ui_contracts` (`GRD-05`..`GRD-08`)
- `use_cases_rbac` (`GRD-09`..`GRD-12`)
- `architecture_runtime` (`GRD-13`..`GRD-16`)
- `hygiene_ssot` (`GRD-17`..`GRD-21`)
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from ..config import VALID_SCOPES
from ..models import RULE_SPEC_MAP, RULE_SPECS, SEVERITY_ORDER, Finding, RuleSpec
from ..parsers import RepoIndex
from .architecture_runtime import (
    evaluate_grd_13,
    evaluate_grd_14,
    evaluate_grd_15,
    evaluate_grd_16,
)
from .domain_erd_parity import (
    evaluate_grd_01,
    evaluate_grd_02,
    evaluate_grd_03,
    evaluate_grd_04,
)
from .hygiene_ssot import (
    evaluate_grd_17,
    evaluate_grd_18,
    evaluate_grd_19,
    evaluate_grd_20,
    evaluate_grd_21,
)
from .ui_contracts import (
    evaluate_grd_05,
    evaluate_grd_06,
    evaluate_grd_07,
    evaluate_grd_08,
)
from .use_cases_rbac import (
    evaluate_grd_09,
    evaluate_grd_10,
    evaluate_grd_11,
    evaluate_grd_12,
)

RuleFunc = Callable[[RepoIndex], list[Finding]]

_RULE_EVALUATORS: dict[str, RuleFunc] = {
    "GRD-01": evaluate_grd_01,
    "GRD-02": evaluate_grd_02,
    "GRD-03": evaluate_grd_03,
    "GRD-04": evaluate_grd_04,
    "GRD-05": evaluate_grd_05,
    "GRD-06": evaluate_grd_06,
    "GRD-07": evaluate_grd_07,
    "GRD-08": evaluate_grd_08,
    "GRD-09": evaluate_grd_09,
    "GRD-10": evaluate_grd_10,
    "GRD-11": evaluate_grd_11,
    "GRD-12": evaluate_grd_12,
    "GRD-13": evaluate_grd_13,
    "GRD-14": evaluate_grd_14,
    "GRD-15": evaluate_grd_15,
    "GRD-16": evaluate_grd_16,
    "GRD-17": evaluate_grd_17,
    "GRD-18": evaluate_grd_18,
    "GRD-19": evaluate_grd_19,
    "GRD-20": evaluate_grd_20,
    "GRD-21": evaluate_grd_21,
}

RULE_REGISTRY: dict[str, tuple[RuleSpec, RuleFunc]] = {
    spec.rule_id: (spec, _RULE_EVALUATORS[spec.rule_id]) for spec in RULE_SPECS
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
        unknown = [rid for rid in requested_ids if rid not in RULE_SPEC_MAP]
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


def _strip_rel_prefix(path_str: str) -> str:
    norm = path_str.replace("\\", "/")
    while norm.startswith("./"):
        norm = norm[2:]
    return norm.lstrip("/")


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
                rel = _strip_rel_prefix(raw)
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
            f for f in raw_findings if _strip_rel_prefix(f.file) in file_filter
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
