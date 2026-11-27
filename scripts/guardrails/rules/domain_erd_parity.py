"""
Layer 2 Pure Guardrail Rules: Domain & ERD Parity (`GRD-01`..`GRD-04`).

Scopes: `domain`, `erd`.
"""

from __future__ import annotations

import re

from ..config import (
    CANONICAL_SAFETY_THRESHOLDS,
    CANONICAL_SOD_CODES,
    ENUM_ALIASES,
    SSOT_PATHS,
)
from ..models import SEVERITY_BLOCKER, SEVERITY_WARNING, Finding
from ..parsers import RepoIndex
from ..parsers.markdown_parser import ParsedMarkdownDoc
from ..parsers.sql_dbml_parser import SchemaModel

_ENUM_VAL_RE = re.compile(r"^[A-Z0-9_]+$|^-?\d+$")
_SEC4_HEADER_RE = re.compile(r"^####\s+4\.\d+\s+([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)")


def _pluralize(word: str) -> str:
    if word.endswith("y"):
        return word[:-1] + "ies"
    if word.endswith("s"):
        return word + "es"
    return word + "s"


def _to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _normalize_type(raw: str) -> str:
    t = re.sub(r"\s+", " ", raw.strip()).upper()
    t = re.sub(r"\(\s*", "(", t)
    t = re.sub(r"\s*\)", ")", t)
    t = re.sub(r"\s*,\s*", ",", t)
    if t.startswith("NUMERIC("):
        t = "DECIMAL(" + t[len("NUMERIC(") :]
    if t == "TIMESTAMP WITH TIME ZONE":
        t = "TIMESTAMPTZ"
    if t == "INTEGER":
        t = "INT"
    if t == "BOOL":
        t = "BOOLEAN"
    return t


def _normalize_default(raw: str | None) -> str | None:
    if raw is None:
        return None
    s = raw.strip().strip("`").strip()
    if not s or s.upper() in ("-", "NULL"):
        return None
    # Strip trailing ::type casts for cross-format comparison
    s = re.sub(r"::[A-Za-z0-9_ ()]+$", "", s).strip()
    if s.lower() in ("true", "false"):
        return s.lower()
    if re.fullmatch(r"-?\d+(\.0+)?", s):
        return s.split(".")[0]
    return re.sub(r"\s+", " ", s)


def extract_controlled_vocabularies(
    dm_doc: ParsedMarkdownDoc,
) -> tuple[dict[str, tuple[str, ...]], dict[str, tuple[str, ...]], list[tuple[int, str, str]]]:
    """
    Extract controlled vocabularies from `DT-DM-DOC-001.md` §4.

    Returns:
      - `by_entity_prop`: `{"Entity.prop": ("VAL1", ...)}`
      - `by_table_col`: `{"table_name.col_name": ("VAL1", ...)}`
      - `invalid_rows`: `[(line_no, entity_prop, raw_val)]` (CB-SQL-01 non-enum leaks)
    """
    by_entity_prop: dict[str, list[str]] = {}
    by_table_col: dict[str, list[str]] = {}
    invalid_rows: list[tuple[int, str, str]] = []

    in_sec4 = False
    current_entity_prop: str | None = None
    current_table_col: str | None = None

    for line_no, raw_line in enumerate(dm_doc.raw_text.splitlines(), start=1):
        stripped = raw_line.strip()
        if re.match(r"^##\s+4\.", stripped):
            in_sec4 = True
            current_entity_prop = None
            current_table_col = None
            continue
        if in_sec4 and re.match(r"^#{1,2}\s+", stripped):
            # Exiting §4 when a new top-level/## section starts (allowing ### Schema: subheadings inside §4)
            in_sec4 = False
            current_entity_prop = None
            current_table_col = None
            continue
        if not in_sec4:
            continue

        hm = _SEC4_HEADER_RE.match(stripped)
        if hm:
            ent, prop = hm.group(1), hm.group(2)
            current_entity_prop = f"{ent}.{prop}"
            current_table_col = f"{_pluralize(_to_snake(ent))}.{_to_snake(prop)}"
            by_entity_prop.setdefault(current_entity_prop, [])
            by_table_col.setdefault(current_table_col, [])
            continue

        if (
            current_entity_prop is not None
            and current_table_col is not None
            and stripped.startswith("|")
            and not re.match(r"^\|[\s:-]+\|", stripped)
        ):
            cells = [c.strip().strip("`") for c in stripped.strip("|").split("|")]
            if not cells or not cells[0]:
                continue
            header_low = cells[0].lower()
            if header_low in ("value", "code", "rule code", "domain mechanism", "physical field") or header_low.startswith("code ("):
                continue
            val = cells[0]
            if not _ENUM_VAL_RE.match(val):
                invalid_rows.append((line_no, current_entity_prop, val))
                continue
            if val not in by_entity_prop[current_entity_prop]:
                by_entity_prop[current_entity_prop].append(val)
            if val not in by_table_col[current_table_col]:
                by_table_col[current_table_col].append(val)

    return (
        {k: tuple(v) for k, v in by_entity_prop.items()},
        {k: tuple(v) for k, v in by_table_col.items()},
        invalid_rows,
    )


def evaluate_grd_01(index: RepoIndex) -> list[Finding]:
    """GRD-01: SQL CHECK constraints & DT-DM-DOC-001 §4 controlled vocabulary parity (CB-SQL-01)."""
    findings: list[Finding] = []
    dm_path = SSOT_PATHS.dm_class_doc
    sql_path = SSOT_PATHS.erd_sql

    dm_doc = index.markdown_docs.get(dm_path)
    if dm_doc is None:
        findings.append(
            Finding(
                rule_id="GRD-01",
                severity=SEVERITY_BLOCKER,
                scope="domain",
                file=dm_path,
                line=None,
                message=f"Missing required SSoT file '{dm_path}'.",
                remediation="Restore DT-DM-DOC-001.md in domain-models/class/.",
            )
        )
        return findings

    if index.sql_schema is None:
        findings.append(
            Finding(
                rule_id="GRD-01",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=sql_path,
                line=None,
                message=f"Missing required DDL artifact '{sql_path}'.",
                remediation="Generate or restore DT-ERD-001.sql via scripts/generate_ddl.py.",
            )
        )
        return findings

    _, by_table_col, invalid_rows = extract_controlled_vocabularies(dm_doc)

    # 1. Catch non-enum table leaks inside §4 (CB-SQL-01)
    for line_no, ent_prop, bad_val in invalid_rows:
        findings.append(
            Finding(
                rule_id="GRD-01",
                severity=SEVERITY_BLOCKER,
                scope="domain",
                file=dm_path,
                line=line_no,
                message=(
                    f"Non-enum token '{bad_val}' detected under §4 vocabulary '{ent_prop}' "
                    f"(expected UPPER_SNAKE_CASE or integer code)."
                ),
                remediation="Ensure §4 subsections contain only valid enum codes or terminate §4 cleanly before §5.",
            )
        )

    # 2. Validate every ck_* CHECK constraint in DT-ERD-001.sql against DT-DM-DOC-001 §4
    sql_checks_by_col: dict[tuple[str, str], list[tuple[str, tuple[str, ...], int | None]]] = {}
    for chk in index.sql_schema.checks:
        tbl_short = chk.table_name.split(".", 1)[-1]
        col = chk.column_name or ""
        raw_key = f"{tbl_short}.{col}"
        resolved_key = ENUM_ALIASES.get(raw_key, raw_key)
        is_enum_ck = (chk.constraint_name or "").lower().startswith("ck_") or resolved_key in by_table_col
        if not is_enum_ck:
            continue

        sql_checks_by_col.setdefault((chk.table_name, col), []).append(
            (chk.constraint_name or "(anonymous)", chk.allowed_values, chk.line)
        )

        if resolved_key not in by_table_col:
            findings.append(
                Finding(
                    rule_id="GRD-01",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=sql_path,
                    line=chk.line,
                    message=(
                        f"SQL CHECK constraint '{chk.constraint_name}' on '{chk.table_name}.{col}' "
                        f"has no matching controlled vocabulary '{resolved_key}' in DT-DM-DOC-001 §4."
                    ),
                    remediation="Add the controlled vocabulary in DT-DM-DOC-001 §4 or map it in config.ENUM_ALIASES.",
                )
            )
            continue

        expected_vals = set(by_table_col[resolved_key])
        actual_vals = set(chk.allowed_values)
        if not actual_vals:
            findings.append(
                Finding(
                    rule_id="GRD-01",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=sql_path,
                    line=chk.line,
                    message=(
                        f"SQL CHECK constraint '{chk.constraint_name}' on '{chk.table_name}.{col}' "
                        f"could not be parsed into discrete enum/range values."
                    ),
                    remediation="Regenerate DT-ERD-001.sql via scripts/generate_ddl.py.",
                )
            )
            continue

        missing = sorted(expected_vals - actual_vals)
        extra = sorted(actual_vals - expected_vals)
        if missing or extra:
            findings.append(
                Finding(
                    rule_id="GRD-01",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=sql_path,
                    line=chk.line,
                    message=(
                        f"SQL CHECK '{chk.constraint_name}' ({chk.table_name}.{col}) drifts from "
                        f"DT-DM-DOC-001 §4 '{resolved_key}': missing={missing}, extra={extra}."
                    ),
                    remediation="Align DT-DM-DOC-001 §4 and regenerate DT-ERD-001.sql.",
                )
            )

    # 3. Verify every CHECK column declared in DT-ERD-DOC-001.md has a CHECK in SQL
    if index.erd_doc_schema is not None:
        for t_name, tbl in sorted(index.erd_doc_schema.tables.items()):
            for col_name, col in sorted(tbl.columns.items()):
                if not col.has_check:
                    continue
                if t_name not in (index.sql_schema.tables if index.sql_schema else {}):
                    continue
                sql_tbl = index.sql_schema.tables[t_name]
                if col_name not in sql_tbl.columns:
                    continue
                has_sql_chk = any(c.column_name == col_name for c in sql_tbl.checks)
                if not has_sql_chk:
                    findings.append(
                        Finding(
                            rule_id="GRD-01",
                            severity=SEVERITY_BLOCKER,
                            scope="erd",
                            file=sql_path,
                            line=sql_tbl.line,
                            message=(
                                f"Column '{t_name}.{col_name}' is marked CHECK in DT-ERD-DOC-001.md "
                                f"but lacks a CHECK constraint in DT-ERD-001.sql."
                            ),
                            remediation="Regenerate DT-ERD-001.sql via scripts/generate_ddl.py.",
                        )
                    )

    return findings


def _fk_signature_set(schema: SchemaModel) -> dict[tuple[str, str], list[tuple[str | None, str | None, int | None]]]:
    sigs: dict[tuple[str, str], list[tuple[str | None, str | None, int | None]]] = {}
    for fk in schema.foreign_keys:
        key = (fk.source_table, fk.target_table)
        sigs.setdefault(key, []).append((fk.on_delete, fk.on_update, fk.line))
    return sigs


def evaluate_grd_02(index: RepoIndex) -> list[Finding]:
    """GRD-02: 1:1 structural parity between DT-ERD-DOC-001.md and DT-ERD-001.sql."""
    findings: list[Finding] = []
    erd_path = SSOT_PATHS.erd_doc
    sql_path = SSOT_PATHS.erd_sql
    erd = index.erd_doc_schema
    sql = index.sql_schema

    if erd is None or sql is None:
        missing_file = erd_path if erd is None else sql_path
        findings.append(
            Finding(
                rule_id="GRD-02",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=missing_file,
                line=None,
                message=f"Cannot run ERD-to-SQL parity: missing parsed schema for '{missing_file}'.",
                remediation="Ensure DT-ERD-DOC-001.md and DT-ERD-001.sql both exist.",
            )
        )
        return findings

    erd_tables = set(erd.tables.keys())
    sql_tables = set(sql.tables.keys())

    for tbl_name in sorted(erd_tables - sql_tables):
        findings.append(
            Finding(
                rule_id="GRD-02",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=sql_path,
                line=erd.tables[tbl_name].line,
                message=f"Table '{tbl_name}' defined in DT-ERD-DOC-001.md is missing from DT-ERD-001.sql.",
                remediation="Run scripts/generate_ddl.py to synchronize DT-ERD-001.sql with DT-ERD-DOC-001.md.",
            )
        )
    for tbl_name in sorted(sql_tables - erd_tables):
        findings.append(
            Finding(
                rule_id="GRD-02",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=sql_path,
                line=sql.tables[tbl_name].line,
                message=f"Table '{tbl_name}' in DT-ERD-001.sql is not documented in DT-ERD-DOC-001.md.",
                remediation="Document the table in DT-ERD-DOC-001.md or remove the stale DDL table.",
            )
        )

    for tbl_name in sorted(erd_tables & sql_tables):
        e_tbl = erd.tables[tbl_name]
        s_tbl = sql.tables[tbl_name]

        e_cols = set(e_tbl.columns.keys())
        s_cols = set(s_tbl.columns.keys())

        for c_name in sorted(e_cols - s_cols):
            findings.append(
                Finding(
                    rule_id="GRD-02",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=sql_path,
                    line=s_tbl.line,
                    message=f"Column '{tbl_name}.{c_name}' in DT-ERD-DOC-001.md is missing from DT-ERD-001.sql.",
                    remediation="Regenerate DT-ERD-001.sql from DT-ERD-DOC-001.md.",
                )
            )
        for c_name in sorted(s_cols - e_cols):
            findings.append(
                Finding(
                    rule_id="GRD-02",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=sql_path,
                    line=s_tbl.columns[c_name].line,
                    message=f"Column '{tbl_name}.{c_name}' in DT-ERD-001.sql is missing from DT-ERD-DOC-001.md.",
                    remediation="Update DT-ERD-DOC-001.md or regenerate DT-ERD-001.sql.",
                )
            )

        if tuple(e_tbl.primary_key) != tuple(s_tbl.primary_key):
            findings.append(
                Finding(
                    rule_id="GRD-02",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=sql_path,
                    line=s_tbl.line,
                    message=(
                        f"Primary key mismatch on '{tbl_name}': "
                        f"ERD={e_tbl.primary_key} vs SQL={s_tbl.primary_key}."
                    ),
                    remediation="Align primary key columns between DT-ERD-DOC-001.md and DT-ERD-001.sql.",
                )
            )

        for c_name in sorted(e_cols & s_cols):
            ec = e_tbl.columns[c_name]
            sc = s_tbl.columns[c_name]
            if _normalize_type(ec.data_type) != _normalize_type(sc.data_type):
                findings.append(
                    Finding(
                        rule_id="GRD-02",
                        severity=SEVERITY_BLOCKER,
                        scope="erd",
                        file=sql_path,
                        line=sc.line,
                        message=(
                            f"Type mismatch on '{tbl_name}.{c_name}': "
                            f"ERD={ec.data_type} vs SQL={sc.data_type}."
                        ),
                        remediation="Align SQL column type with DT-ERD-DOC-001.md.",
                    )
                )
            if ec.nullable != sc.nullable:
                findings.append(
                    Finding(
                        rule_id="GRD-02",
                        severity=SEVERITY_BLOCKER,
                        scope="erd",
                        file=sql_path,
                        line=sc.line,
                        message=(
                            f"Nullability mismatch on '{tbl_name}.{c_name}': "
                            f"ERD={'NULL' if ec.nullable else 'NOT NULL'} vs "
                            f"SQL={'NULL' if sc.nullable else 'NOT NULL'}."
                        ),
                        remediation="Synchronize NULL/NOT NULL constraint with DT-ERD-DOC-001.md.",
                    )
                )
            if _normalize_default(ec.default) != _normalize_default(sc.default):
                findings.append(
                    Finding(
                        rule_id="GRD-02",
                        severity=SEVERITY_BLOCKER,
                        scope="erd",
                        file=sql_path,
                        line=sc.line,
                        message=(
                            f"Default mismatch on '{tbl_name}.{c_name}': "
                            f"ERD={ec.default!r} vs SQL={sc.default!r}."
                        ),
                        remediation="Synchronize DEFAULT value with DT-ERD-DOC-001.md.",
                    )
                )

            # Every JSONB column must have a GIN index
            if "JSONB" in _normalize_type(sc.data_type):
                has_gin = any(
                    idx.method == "GIN" and any(c_name in col_expr.lower() for col_expr in idx.columns)
                    for idx in s_tbl.indexes
                )
                if not has_gin:
                    findings.append(
                        Finding(
                            rule_id="GRD-02",
                            severity=SEVERITY_BLOCKER,
                            scope="erd",
                            file=sql_path,
                            line=sc.line,
                            message=f"JSONB column '{tbl_name}.{c_name}' lacks a GIN index in DT-ERD-001.sql.",
                            remediation=f"Add CREATE INDEX ... ON {tbl_name} USING GIN ({c_name} jsonb_path_ops).",
                        )
                    )

            # Every FK column must have an index
            if sc.is_fk:
                has_fk_idx = any(
                    idx.columns and idx.columns[0].lower().startswith(c_name)
                    for idx in s_tbl.indexes
                )
                if not has_fk_idx:
                    findings.append(
                        Finding(
                            rule_id="GRD-02",
                            severity=SEVERITY_BLOCKER,
                            scope="erd",
                            file=sql_path,
                            line=sc.line,
                            message=f"FK column '{tbl_name}.{c_name}' lacks an index in DT-ERD-001.sql.",
                            remediation=f"Add CREATE INDEX IF NOT EXISTS idx_{s_tbl.name}_{c_name} ON {tbl_name} ({c_name}).",
                        )
                    )

    # Foreign key parity & ON DELETE / ON UPDATE actions
    erd_fks = _fk_signature_set(erd)
    sql_fks = _fk_signature_set(sql)
    for pair in sorted(set(erd_fks.keys()) - set(sql_fks.keys())):
        findings.append(
            Finding(
                rule_id="GRD-02",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=sql_path,
                line=erd_fks[pair][0][2],
                message=f"Foreign key {pair[0]} -> {pair[1]} documented in DT-ERD-DOC-001 §4 is missing in DT-ERD-001.sql.",
                remediation="Regenerate DT-ERD-001.sql foreign key constraints.",
            )
        )
    for pair in sorted(set(sql_fks.keys()) - set(erd_fks.keys())):
        findings.append(
            Finding(
                rule_id="GRD-02",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=sql_path,
                line=sql_fks[pair][0][2],
                message=f"Foreign key {pair[0]} -> {pair[1]} in DT-ERD-001.sql is missing from DT-ERD-DOC-001 §4.",
                remediation="Document the relationship in DT-ERD-DOC-001 §4.",
            )
        )
    for pair in sorted(set(erd_fks.keys()) & set(sql_fks.keys())):
        e_actions = {(d, u) for d, u, _ in erd_fks[pair]}
        s_actions = {(d, u) for d, u, _ in sql_fks[pair]}
        if e_actions != s_actions:
            findings.append(
                Finding(
                    rule_id="GRD-02",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=sql_path,
                    line=sql_fks[pair][0][2],
                    message=(
                        f"Referential action mismatch for FK {pair[0]} -> {pair[1]}: "
                        f"ERD={sorted(e_actions)} vs SQL={sorted(s_actions)}."
                    ),
                    remediation="Align ON DELETE / ON UPDATE clauses with DT-ERD-DOC-001 §4.",
                )
            )

    return findings


def evaluate_grd_03(index: RepoIndex) -> list[Finding]:
    """GRD-03: 1:1 structural parity between DT-ERD-DOC-001.md and DT-ERD-001.dbml."""
    findings: list[Finding] = []
    erd_path = SSOT_PATHS.erd_doc
    dbml_path = SSOT_PATHS.erd_dbml
    erd = index.erd_doc_schema
    dbml = index.dbml_schema

    if erd is None or dbml is None:
        missing_file = erd_path if erd is None else dbml_path
        findings.append(
            Finding(
                rule_id="GRD-03",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=missing_file,
                line=None,
                message=f"Cannot run ERD-to-DBML parity: missing parsed schema for '{missing_file}'.",
                remediation="Ensure DT-ERD-DOC-001.md and DT-ERD-001.dbml both exist.",
            )
        )
        return findings

    erd_tables = set(erd.tables.keys())
    dbml_tables = set(dbml.tables.keys())

    for tbl_name in sorted(erd_tables - dbml_tables):
        findings.append(
            Finding(
                rule_id="GRD-03",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=dbml_path,
                line=erd.tables[tbl_name].line,
                message=f"Table '{tbl_name}' defined in DT-ERD-DOC-001.md is missing from DT-ERD-001.dbml.",
                remediation="Run scripts/generate_erd_dbml.py to synchronize DT-ERD-001.dbml.",
            )
        )
    for tbl_name in sorted(dbml_tables - erd_tables):
        findings.append(
            Finding(
                rule_id="GRD-03",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=dbml_path,
                line=dbml.tables[tbl_name].line,
                message=f"Table '{tbl_name}' in DT-ERD-001.dbml is not documented in DT-ERD-DOC-001.md.",
                remediation="Document the table in DT-ERD-DOC-001.md or regenerate DT-ERD-001.dbml.",
            )
        )

    for tbl_name in sorted(erd_tables & dbml_tables):
        e_tbl = erd.tables[tbl_name]
        d_tbl = dbml.tables[tbl_name]
        e_cols = set(e_tbl.columns.keys())
        d_cols = set(d_tbl.columns.keys())

        for c_name in sorted(e_cols - d_cols):
            findings.append(
                Finding(
                    rule_id="GRD-03",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=dbml_path,
                    line=d_tbl.line,
                    message=f"Column '{tbl_name}.{c_name}' in DT-ERD-DOC-001.md is missing from DT-ERD-001.dbml.",
                    remediation="Regenerate DT-ERD-001.dbml via scripts/generate_erd_dbml.py.",
                )
            )
        for c_name in sorted(d_cols - e_cols):
            findings.append(
                Finding(
                    rule_id="GRD-03",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=dbml_path,
                    line=d_tbl.columns[c_name].line,
                    message=f"Column '{tbl_name}.{c_name}' in DT-ERD-001.dbml is missing from DT-ERD-DOC-001.md.",
                    remediation="Update DT-ERD-DOC-001.md or regenerate DT-ERD-001.dbml.",
                )
            )

        if tuple(e_tbl.primary_key) != tuple(d_tbl.primary_key):
            findings.append(
                Finding(
                    rule_id="GRD-03",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=dbml_path,
                    line=d_tbl.line,
                    message=(
                        f"Primary key mismatch on '{tbl_name}' in DBML: "
                        f"ERD={e_tbl.primary_key} vs DBML={d_tbl.primary_key}."
                    ),
                    remediation="Align [pk] column markers in DT-ERD-001.dbml.",
                )
            )

        for c_name in sorted(e_cols & d_cols):
            ec = e_tbl.columns[c_name]
            dc = d_tbl.columns[c_name]
            if _normalize_type(ec.data_type) != _normalize_type(dc.data_type):
                findings.append(
                    Finding(
                        rule_id="GRD-03",
                        severity=SEVERITY_BLOCKER,
                        scope="erd",
                        file=dbml_path,
                        line=dc.line,
                        message=(
                            f"Type mismatch on '{tbl_name}.{c_name}' in DBML: "
                            f"ERD={ec.data_type} vs DBML={dc.data_type}."
                        ),
                        remediation="Regenerate DT-ERD-001.dbml from DT-ERD-DOC-001.md.",
                    )
                )
            if ec.nullable != dc.nullable:
                findings.append(
                    Finding(
                        rule_id="GRD-03",
                        severity=SEVERITY_BLOCKER,
                        scope="erd",
                        file=dbml_path,
                        line=dc.line,
                        message=(
                            f"Nullability mismatch on '{tbl_name}.{c_name}' in DBML: "
                            f"ERD={'NULL' if ec.nullable else 'NOT NULL'} vs "
                            f"DBML={'NULL' if dc.nullable else 'NOT NULL'}."
                        ),
                        remediation="Synchronize [not null] attribute in DT-ERD-001.dbml.",
                    )
                )
            if _normalize_default(ec.default) != _normalize_default(dc.default):
                findings.append(
                    Finding(
                        rule_id="GRD-03",
                        severity=SEVERITY_BLOCKER,
                        scope="erd",
                        file=dbml_path,
                        line=dc.line,
                        message=(
                            f"Default mismatch on '{tbl_name}.{c_name}' in DBML: "
                            f"ERD={ec.default!r} vs DBML={dc.default!r}."
                        ),
                        remediation="Synchronize DBML default attribute with DT-ERD-DOC-001.md.",
                    )
                )

    erd_fks = _fk_signature_set(erd)
    dbml_fks = _fk_signature_set(dbml)
    for pair in sorted(set(erd_fks.keys()) - set(dbml_fks.keys())):
        findings.append(
            Finding(
                rule_id="GRD-03",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=dbml_path,
                line=erd_fks[pair][0][2],
                message=f"DBML Ref {pair[0]} -> {pair[1]} documented in DT-ERD-DOC-001 §4 is missing.",
                remediation="Regenerate DT-ERD-001.dbml relationships.",
            )
        )
    for pair in sorted(set(dbml_fks.keys()) - set(erd_fks.keys())):
        findings.append(
            Finding(
                rule_id="GRD-03",
                severity=SEVERITY_BLOCKER,
                scope="erd",
                file=dbml_path,
                line=dbml_fks[pair][0][2],
                message=f"DBML Ref {pair[0]} -> {pair[1]} is not documented in DT-ERD-DOC-001 §4.",
                remediation="Update DT-ERD-DOC-001 §4 or regenerate DT-ERD-001.dbml.",
            )
        )
    for pair in sorted(set(erd_fks.keys()) & set(dbml_fks.keys())):
        e_actions = {(d, u) for d, u, _ in erd_fks[pair]}
        d_actions = {(d, u) for d, u, _ in dbml_fks[pair]}
        if e_actions != d_actions:
            findings.append(
                Finding(
                    rule_id="GRD-03",
                    severity=SEVERITY_BLOCKER,
                    scope="erd",
                    file=dbml_path,
                    line=dbml_fks[pair][0][2],
                    message=(
                        f"DBML Ref referential action mismatch for {pair[0]} -> {pair[1]}: "
                        f"ERD={sorted(e_actions)} vs DBML={sorted(d_actions)}."
                    ),
                    remediation="Align [delete: ..., update: ...] in DT-ERD-001.dbml with DT-ERD-DOC-001 §4.",
                )
            )

    return findings


def evaluate_grd_04(index: RepoIndex) -> list[Finding]:
    """GRD-04: DT-DM-DOC-001 §5 constants consistency with DT-DM-DOC-002 and DT-DM-001.puml."""
    findings: list[Finding] = []
    dm1_path = SSOT_PATHS.dm_class_doc
    dm2_path = SSOT_PATHS.dm_state_doc
    puml_path = SSOT_PATHS.dm_puml

    dm1 = index.markdown_docs.get(dm1_path)
    dm2 = index.markdown_docs.get(dm2_path)
    puml_text = index.raw_texts.get(puml_path)

    if dm1 is None:
        findings.append(
            Finding(
                rule_id="GRD-04",
                severity=SEVERITY_BLOCKER,
                scope="domain",
                file=dm1_path,
                line=None,
                message=f"Missing '{dm1_path}'.",
                remediation="Restore DT-DM-DOC-001.md.",
            )
        )
        return findings

    # 1. Verify DT-DM-DOC-001 §5 defines all canonical SoD & safety constants
    sec5_start = dm1.raw_text.find("## 5.")
    sec6_start = dm1.raw_text.find("## 6.")
    sec5_text = dm1.raw_text[sec5_start:sec6_start] if sec5_start != -1 else ""
    if not sec5_text:
        findings.append(
            Finding(
                rule_id="GRD-04",
                severity=SEVERITY_BLOCKER,
                scope="domain",
                file=dm1_path,
                line=None,
                message="DT-DM-DOC-001.md is missing '## 5. Domain Safety & Segregation of Duties (SoD) Constants'.",
                remediation="Restore §5 SoD and safety threshold tables in DT-DM-DOC-001.md.",
            )
        )
    else:
        for code in CANONICAL_SOD_CODES:
            if code not in sec5_text:
                findings.append(
                    Finding(
                        rule_id="GRD-04",
                        severity=SEVERITY_BLOCKER,
                        scope="domain",
                        file=dm1_path,
                        line=None,
                        message=f"Canonical SoD rule '{code}' missing from DT-DM-DOC-001 §5.1.",
                        remediation=f"Document '{code}' in DT-DM-DOC-001 §5.1.",
                    )
                )
        for thresh in CANONICAL_SAFETY_THRESHOLDS:
            if thresh not in sec5_text:
                findings.append(
                    Finding(
                        rule_id="GRD-04",
                        severity=SEVERITY_BLOCKER,
                        scope="domain",
                        file=dm1_path,
                        line=None,
                        message=f"Canonical safety threshold '{thresh}' missing from DT-DM-DOC-001 §5.2.",
                        remediation=f"Document '{thresh}' in DT-DM-DOC-001 §5.2.",
                    )
                )

    # Extract §3 entity names from DT-DM-DOC-001.md
    dm1_entities: set[str] = set()
    for tbl in dm1.tables:
        if "3" in tbl.heading or any(h.lower() in ("entity", "entidad") for h in tbl.headers):
            for row in tbl.rows:
                if row and row[0]:
                    ent = row[0].strip("` ").strip()
                    dm1_entities.add("RolePermission" if ent == "Permission" else ent)

    # 2. Validate DT-DM-DOC-002 classes, methods, and threshold references
    dm2_classes: dict[str, list[str]] = {}
    if dm2 is not None:
        lines = dm2.raw_text.splitlines()
        cur_cls: str | None = None
        for idx, line in enumerate(lines, start=1):
            cm = re.match(r"^###\s+\d+\.\d+\.\s+`([^`]+)`", line.strip())
            if cm:
                cur_cls = cm.group(1).strip()
                dm2_classes.setdefault(cur_cls, [])
                if dm1_entities and cur_cls not in dm1_entities:
                    findings.append(
                        Finding(
                            rule_id="GRD-04",
                            severity=SEVERITY_BLOCKER,
                            scope="domain",
                            file=dm2_path,
                            line=idx,
                            message=f"Aggregate/entity '{cur_cls}' in DT-DM-DOC-002 is absent from DT-DM-DOC-001 §3.",
                            remediation="Add the entity to DT-DM-DOC-001 §3 or align the class name.",
                        )
                    )
                continue
            if cur_cls and line.strip().startswith("|") and "`" in line:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if cells and "(" in cells[0] and not cells[0].lower().startswith("method"):
                    meth = cells[0].strip("`").split("(", 1)[0].strip()
                    if meth:
                        dm2_classes[cur_cls].append(meth)

        # Ensure DT-DM-DOC-002 does not contradict safety thresholds from DT-DM-DOC-001 §5
        for idx, line in enumerate(lines, start=1):
            # Flag conflicting voltage/pressure thresholds (e.g., > 0.5 psig or non-0.0 V)
            pm = re.search(r"(\d+(?:\.\d+)?)\s*psig\b", line, re.IGNORECASE)
            if pm and pm.group(1) != "0.5":
                findings.append(
                    Finding(
                        rule_id="GRD-04",
                        severity=SEVERITY_BLOCKER,
                        scope="domain",
                        file=dm2_path,
                        line=idx,
                        message=f"Pressure threshold '{pm.group(0)}' in DT-DM-DOC-002 conflicts with DT-DM-DOC-001 §5.2 ('0.5 psig').",
                        remediation="Reference DT-DM-DOC-001 §5.2 canonical threshold (0.5 psig).",
                    )
                )
            if re.search(r"loto|zero[- ]energy|voltage|electrical|energ", line, re.IGNORECASE):
                vm = re.search(r"(?<![A-Za-z0-9_.])(\d+(?:\.\d+)?)\s*V\b", line)
                if vm and vm.group(1) not in ("0.0", "0"):
                    findings.append(
                        Finding(
                            rule_id="GRD-04",
                            severity=SEVERITY_BLOCKER,
                            scope="domain",
                            file=dm2_path,
                            line=idx,
                            message=f"Voltage threshold '{vm.group(0)}' in DT-DM-DOC-002 conflicts with DT-DM-DOC-001 §5.2 ('0.0 V').",
                            remediation="Reference DT-DM-DOC-001 §5.2 canonical threshold (0.0 V).",
                        )
                    )

    # 3. Validate PlantUML DT-DM-001.puml parity with DT-DM-DOC-002 & DT-ERD-DOC-001
    if puml_text is None:
        findings.append(
            Finding(
                rule_id="GRD-04",
                severity=SEVERITY_WARNING,
                scope="domain",
                file=puml_path,
                line=None,
                message=f"PlantUML domain diagram '{puml_path}' not found.",
                remediation="Generate DT-DM-001.puml via scripts/generate_domain_puml.py.",
            )
        )
    else:
        puml_classes: dict[str, set[str]] = {}
        cur_puml_cls: str | None = None
        for line in puml_text.splitlines():
            s = line.strip()
            cm = re.match(r"^class\s+([A-Za-z0-9_]+)\b", s)
            if cm:
                cur_puml_cls = cm.group(1)
                puml_classes.setdefault(cur_puml_cls, set())
                continue
            if cur_puml_cls and s == "}":
                cur_puml_cls = None
                continue
            if cur_puml_cls and s.startswith("+ "):
                meth_name = s[2:].split("(", 1)[0].strip()
                if meth_name:
                    puml_classes[cur_puml_cls].add(meth_name)

        for cls_name, methods in sorted(dm2_classes.items()):
            if cls_name not in puml_classes:
                findings.append(
                    Finding(
                        rule_id="GRD-04",
                        severity=SEVERITY_BLOCKER,
                        scope="domain",
                        file=puml_path,
                        line=None,
                        message=f"Class '{cls_name}' from DT-DM-DOC-002 is missing in DT-DM-001.puml.",
                        remediation="Regenerate DT-DM-001.puml via scripts/generate_domain_puml.py.",
                    )
                )
                continue
            missing_meths = [m for m in methods if m not in puml_classes[cls_name]]
            if missing_meths:
                findings.append(
                    Finding(
                        rule_id="GRD-04",
                        severity=SEVERITY_BLOCKER,
                        scope="domain",
                        file=puml_path,
                        line=None,
                        message=(
                            f"Class '{cls_name}' in DT-DM-001.puml is missing methods from "
                            f"DT-DM-DOC-002: {missing_meths}."
                        ),
                        remediation="Regenerate DT-DM-001.puml via scripts/generate_domain_puml.py.",
                    )
                )

    return findings
