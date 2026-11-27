"""
Normalized schema parser for DT-ERD-001.sql, DT-ERD-001.dbml, and DT-ERD-DOC-001.md (§§3-4).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .markdown_parser import ParsedMarkdownDoc


@dataclass(frozen=True, slots=True)
class ColumnDef:
    name: str
    data_type: str
    nullable: bool
    is_pk: bool = False
    is_unique: bool = False
    default: str | None = None
    has_check: bool = False
    is_fk: bool = False
    comment: str | None = None
    line: int | None = None


@dataclass(frozen=True, slots=True)
class ForeignKeyDef:
    constraint_name: str | None
    source_table: str
    source_columns: tuple[str, ...]
    target_table: str
    target_columns: tuple[str, ...]
    on_delete: str | None = None
    on_update: str | None = None
    line: int | None = None


@dataclass(frozen=True, slots=True)
class CheckDef:
    constraint_name: str | None
    table_name: str
    column_name: str | None
    expression: str
    allowed_values: tuple[str, ...] = ()
    line: int | None = None


@dataclass(frozen=True, slots=True)
class IndexDef:
    name: str
    table_name: str
    columns: tuple[str, ...]
    is_unique: bool = False
    method: str | None = None
    where_clause: str | None = None
    line: int | None = None


@dataclass(slots=True)
class TableDef:
    schema: str
    name: str
    columns: dict[str, ColumnDef] = field(default_factory=dict)
    primary_key: tuple[str, ...] = ()
    unique_constraints: list[tuple[str, ...]] = field(default_factory=list)
    checks: list[CheckDef] = field(default_factory=list)
    foreign_keys: list[ForeignKeyDef] = field(default_factory=list)
    indexes: list[IndexDef] = field(default_factory=list)
    partition_by: str | None = None
    is_hypertable: bool = False
    rls_enabled: bool = False
    rls_forced: bool = False
    line: int | None = None

    @property
    def full_name(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass(frozen=True, slots=True)
class SchemaModel:
    source: str
    tables: dict[str, TableDef]
    foreign_keys: tuple[ForeignKeyDef, ...]
    checks: tuple[CheckDef, ...]
    indexes: tuple[IndexDef, ...]
    schemas: tuple[str, ...]


def _normalize_sql_type(raw_type: str) -> str:
    collapsed = re.sub(r"\s+", " ", raw_type.strip())
    # Normalize spaces inside precision specs: DECIMAL(10, 2) -> DECIMAL(10,2)
    collapsed = re.sub(r"\(\s*", "(", collapsed)
    collapsed = re.sub(r"\s*\)", ")", collapsed)
    collapsed = re.sub(r"\s*,\s*", ",", collapsed)
    return collapsed.upper()


def _line_at(text: str, pos: int) -> int:
    return text[:pos].count("\n") + 1


def _strip_sql_comments_preserve_lines(sql_text: str) -> str:
    """Replace SQL comments (`-- ...` and `/* ... */`) with spaces while keeping newlines."""
    out: list[str] = []
    i = 0
    n = len(sql_text)
    in_single = False
    in_dollar: str | None = None

    while i < n:
        ch = sql_text[i]
        # Dollar-quoted blocks (e.g. DO $$ ... END $$;)
        if not in_single and ch == "$":
            dm = re.match(r"\$[A-Za-z0-9_]*\$", sql_text[i:])
            if dm:
                tag = dm.group(0)
                if in_dollar is None:
                    in_dollar = tag
                    out.append(tag)
                    i += len(tag)
                    continue
                elif in_dollar == tag:
                    in_dollar = None
                    out.append(tag)
                    i += len(tag)
                    continue
        if in_dollar is not None:
            out.append(ch if ch == "\n" else " ")
            i += 1
            continue
        if in_single:
            out.append(ch)
            if ch == "'":
                if i + 1 < n and sql_text[i + 1] == "'":
                    out.append("'")
                    i += 2
                    continue
                in_single = False
            i += 1
            continue
        if ch == "'":
            in_single = True
            out.append(ch)
            i += 1
            continue
        if ch == "-" and i + 1 < n and sql_text[i + 1] == "-":
            while i < n and sql_text[i] != "\n":
                out.append(" ")
                i += 1
            continue
        if ch == "/" and i + 1 < n and sql_text[i + 1] == "*":
            out.append("  ")
            i += 2
            while i < n and not (sql_text[i] == "*" and i + 1 < n and sql_text[i + 1] == "/"):
                out.append("\n" if sql_text[i] == "\n" else " ")
                i += 1
            if i < n:
                out.append("  ")
                i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _find_matching_paren(text: str, open_idx: int) -> int:
    depth = 0
    in_single = False
    i = open_idx
    n = len(text)
    while i < n:
        ch = text[i]
        if in_single:
            if ch == "'":
                if i + 1 < n and text[i + 1] == "'":
                    i += 2
                    continue
                in_single = False
            i += 1
            continue
        if ch == "'":
            in_single = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _split_top_level_commas(text: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    in_single = False
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_single:
            buf.append(ch)
            if ch == "'":
                if i + 1 < n and text[i + 1] == "'":
                    buf.append("'")
                    i += 2
                    continue
                in_single = False
            i += 1
            continue
        if ch == "'":
            in_single = True
            buf.append(ch)
        elif ch == "(":
            depth += 1
            buf.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == "," and depth == 0:
            item = "".join(buf).strip()
            if item:
                parts.append(item)
            buf = []
        else:
            buf.append(ch)
        i += 1
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)
    return parts


def _extract_check_values(expr: str) -> tuple[str | None, tuple[str, ...]]:
    col_name: str | None = None
    col_m = re.match(r"^\s*\(?\s*\"?([a-zA-Z_][a-zA-Z0-9_]*)\"?", expr)
    if col_m:
        col_name = col_m.group(1)

    in_m = re.search(r"\bIN\s*\(([^)]+)\)", expr, re.IGNORECASE)
    if in_m:
        raw_vals = _split_top_level_commas(in_m.group(1))
        cleaned = tuple(v.strip().strip("'") for v in raw_vals if v.strip())
        return col_name, cleaned

    btw_m = re.search(r"\bBETWEEN\s+(-?\d+)\s+AND\s+(-?\d+)", expr, re.IGNORECASE)
    if btw_m:
        lo, hi = int(btw_m.group(1)), int(btw_m.group(2))
        if 0 <= hi - lo <= 100:
            return col_name, tuple(str(v) for v in range(lo, hi + 1))
        return col_name, (str(lo), str(hi))

    return col_name, ()


def parse_sql_schema(sql_text: str, source: str = "DT-ERD-001.sql") -> SchemaModel:
    """Parse PostgreSQL DDL (`DT-ERD-001.sql`) into a normalized `SchemaModel`."""
    clean_sql = _strip_sql_comments_preserve_lines(sql_text)

    schemas_list: list[str] = []
    for sm in re.finditer(r"\bCREATE\s+SCHEMA\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z_][a-zA-Z0-9_]*)", clean_sql, re.IGNORECASE):
        s_name = sm.group(1).lower()
        if s_name not in schemas_list:
            schemas_list.append(s_name)

    tables: dict[str, TableDef] = {}
    all_checks: list[CheckDef] = []
    all_fks: list[ForeignKeyDef] = []
    all_indexes: list[IndexDef] = []

    create_tbl_re = re.compile(
        r"\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?"
        r"([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(",
        re.IGNORECASE,
    )

    for tm in create_tbl_re.finditer(clean_sql):
        schema_name = tm.group(1).lower()
        table_name = tm.group(2).lower()
        full_name = f"{schema_name}.{table_name}"
        if schema_name not in schemas_list:
            schemas_list.append(schema_name)

        open_paren = tm.end() - 1
        close_paren = _find_matching_paren(clean_sql, open_paren)
        if close_paren == -1:
            continue

        body_str = clean_sql[open_paren + 1 : close_paren]
        after_str = clean_sql[close_paren + 1 : close_paren + 160]
        semi_pos = after_str.find(";")
        tail_clause = after_str[:semi_pos] if semi_pos != -1 else after_str
        part_m = re.search(r"PARTITION\s+BY\s+RANGE\s*\(([^)]+)\)", tail_clause, re.IGNORECASE)
        partition_by = part_m.group(1).strip() if part_m else None

        tbl = TableDef(
            schema=schema_name,
            name=table_name,
            partition_by=partition_by,
            line=_line_at(clean_sql, tm.start()),
        )

        # Track column lines approximately by searching item within body_str
        search_offset = open_paren + 1
        for item in _split_top_level_commas(body_str):
            item_pos = clean_sql.find(item[: min(30, len(item))], search_offset, close_paren)
            item_line = _line_at(clean_sql, item_pos if item_pos != -1 else tm.start())
            if item_pos != -1:
                search_offset = item_pos + len(item[: min(30, len(item))])

            compact = re.sub(r"\s+", " ", item).strip()
            if re.match(r"^(?:CONSTRAINT\s+\S+\s+)?(?:PRIMARY\s+KEY|UNIQUE|CHECK|FOREIGN\s+KEY)\b", compact, re.IGNORECASE):
                c_name_m = re.match(r"^CONSTRAINT\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+(.*)$", compact, re.IGNORECASE)
                c_name = c_name_m.group(1) if c_name_m else None
                rest = c_name_m.group(2) if c_name_m else compact

                pk_m = re.match(r"^PRIMARY\s+KEY\s*\(([^)]+)\)", rest, re.IGNORECASE)
                if pk_m:
                    pk_cols = tuple(c.strip().strip('"').lower() for c in pk_m.group(1).split(",") if c.strip())
                    tbl.primary_key = pk_cols
                    for col_n in pk_cols:
                        if col_n in tbl.columns:
                            prev = tbl.columns[col_n]
                            tbl.columns[col_n] = ColumnDef(
                                name=prev.name,
                                data_type=prev.data_type,
                                nullable=prev.nullable,
                                is_pk=True,
                                is_unique=prev.is_unique,
                                default=prev.default,
                                has_check=prev.has_check,
                                is_fk=prev.is_fk,
                                comment=prev.comment,
                                line=prev.line,
                            )
                    continue

                uq_m = re.match(r"^UNIQUE\s*\(([^)]+)\)", rest, re.IGNORECASE)
                if uq_m:
                    uq_cols = tuple(c.strip().strip('"').lower() for c in uq_m.group(1).split(",") if c.strip())
                    tbl.unique_constraints.append(uq_cols)
                    if len(uq_cols) == 1 and uq_cols[0] in tbl.columns:
                        prev = tbl.columns[uq_cols[0]]
                        tbl.columns[uq_cols[0]] = ColumnDef(
                            name=prev.name,
                            data_type=prev.data_type,
                            nullable=prev.nullable,
                            is_pk=prev.is_pk,
                            is_unique=True,
                            default=prev.default,
                            has_check=prev.has_check,
                            is_fk=prev.is_fk,
                            comment=prev.comment,
                            line=prev.line,
                        )
                    continue

                ck_m = re.match(r"^CHECK\s*\((.*)\)$", rest, re.IGNORECASE)
                if ck_m:
                    expr = ck_m.group(1).strip()
                    col_name, allowed = _extract_check_values(expr)
                    chk = CheckDef(
                        constraint_name=c_name,
                        table_name=full_name,
                        column_name=col_name.lower() if col_name else None,
                        expression=expr,
                        allowed_values=allowed,
                        line=item_line,
                    )
                    tbl.checks.append(chk)
                    all_checks.append(chk)
                    if col_name and col_name.lower() in tbl.columns:
                        prev = tbl.columns[col_name.lower()]
                        tbl.columns[col_name.lower()] = ColumnDef(
                            name=prev.name,
                            data_type=prev.data_type,
                            nullable=prev.nullable,
                            is_pk=prev.is_pk,
                            is_unique=prev.is_unique,
                            default=prev.default,
                            has_check=True,
                            is_fk=prev.is_fk,
                            comment=prev.comment,
                            line=prev.line,
                        )
                    continue

                continue

            # Column definition: name TYPE [NOT NULL] [DEFAULT ...]
            col_m = re.match(
                r'^"?([a-zA-Z_][a-zA-Z0-9_]*)"?\s+'
                r"([A-Za-z][A-Za-z0-9_ ]*?(?:\([^)]+\))?(?:\[\])?)"
                r"(?=\s+(?:NOT\s+NULL|NULL|DEFAULT|PRIMARY\s+KEY|UNIQUE|CHECK|REFERENCES)\b|$)"
                r"(.*)$",
                compact,
                re.IGNORECASE,
            )
            if not col_m:
                continue

            col_name = col_m.group(1).lower()
            col_type = _normalize_sql_type(col_m.group(2))
            qualifiers = col_m.group(3).strip()

            nullable = not bool(re.search(r"\bNOT\s+NULL\b", qualifiers, re.IGNORECASE))
            is_pk = bool(re.search(r"\bPRIMARY\s+KEY\b", qualifiers, re.IGNORECASE))
            is_unique = bool(re.search(r"\bUNIQUE\b", qualifiers, re.IGNORECASE))
            default_val: str | None = None
            def_m = re.search(
                r"\bDEFAULT\s+(.+?)(?=\s+(?:NOT\s+NULL|NULL|PRIMARY\s+KEY|UNIQUE|CHECK|REFERENCES)\b|$)",
                qualifiers,
                re.IGNORECASE,
            )
            if def_m:
                default_val = def_m.group(1).strip()

            tbl.columns[col_name] = ColumnDef(
                name=col_name,
                data_type=col_type,
                nullable=nullable,
                is_pk=is_pk,
                is_unique=is_unique,
                default=default_val,
                line=item_line,
            )
            if is_pk and col_name not in tbl.primary_key:
                tbl.primary_key = (*tbl.primary_key, col_name)

        tables[full_name] = tbl

    # ALTER TABLE ... ADD CONSTRAINT ... FOREIGN KEY ...
    fk_re = re.compile(
        r"\bALTER\s+TABLE\s+(?:ONLY\s+)?([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s+"
        r"ADD\s+CONSTRAINT\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+"
        r"FOREIGN\s+KEY\s*\(([^)]+)\)\s+"
        r"REFERENCES\s+([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]+)\)"
        r"([^;]*);",
        re.IGNORECASE | re.DOTALL,
    )
    for fm in fk_re.finditer(clean_sql):
        src_tbl = f"{fm.group(1).lower()}.{fm.group(2).lower()}"
        c_name = fm.group(3)
        src_cols = tuple(c.strip().strip('"').lower() for c in fm.group(4).split(",") if c.strip())
        ref_tbl = f"{fm.group(5).lower()}.{fm.group(6).lower()}"
        ref_cols = tuple(c.strip().strip('"').lower() for c in fm.group(7).split(",") if c.strip())
        tail = fm.group(8)
        del_m = re.search(r"\bON\s+DELETE\s+(SET\s+NULL|SET\s+DEFAULT|RESTRICT|CASCADE|NO\s+ACTION)", tail, re.IGNORECASE)
        upd_m = re.search(r"\bON\s+UPDATE\s+(SET\s+NULL|SET\s+DEFAULT|RESTRICT|CASCADE|NO\s+ACTION)", tail, re.IGNORECASE)
        fk = ForeignKeyDef(
            constraint_name=c_name,
            source_table=src_tbl,
            source_columns=src_cols,
            target_table=ref_tbl,
            target_columns=ref_cols,
            on_delete=re.sub(r"\s+", " ", del_m.group(1).upper()) if del_m else None,
            on_update=re.sub(r"\s+", " ", upd_m.group(1).upper()) if upd_m else None,
            line=_line_at(clean_sql, fm.start()),
        )
        all_fks.append(fk)
        if src_tbl in tables:
            tables[src_tbl].foreign_keys.append(fk)
            for sc in src_cols:
                if sc in tables[src_tbl].columns:
                    prev = tables[src_tbl].columns[sc]
                    tables[src_tbl].columns[sc] = ColumnDef(
                        name=prev.name,
                        data_type=prev.data_type,
                        nullable=prev.nullable,
                        is_pk=prev.is_pk,
                        is_unique=prev.is_unique,
                        default=prev.default,
                        has_check=prev.has_check,
                        is_fk=True,
                        comment=prev.comment,
                        line=prev.line,
                    )

    # CREATE [UNIQUE] INDEX ...
    idx_re = re.compile(
        r"\bCREATE\s+(UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?"
        r"([a-zA-Z_][a-zA-Z0-9_]*)\s+ON\s+([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*"
        r"(?:USING\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*)?\(([^;)]+)\)"
        r"(?:\s+WHERE\s+([^;]+))?\s*;",
        re.IGNORECASE | re.DOTALL,
    )
    for im in idx_re.finditer(clean_sql):
        is_uq = bool(im.group(1))
        idx_name = im.group(2)
        tbl_full = f"{im.group(3).lower()}.{im.group(4).lower()}"
        method = im.group(5).upper() if im.group(5) else None
        cols = tuple(re.sub(r"\s+", " ", c.strip()) for c in _split_top_level_commas(im.group(6)) if c.strip())
        where_clause = re.sub(r"\s+", " ", im.group(7)).strip() if im.group(7) else None
        idx_def = IndexDef(
            name=idx_name,
            table_name=tbl_full,
            columns=cols,
            is_unique=is_uq,
            method=method,
            where_clause=where_clause,
            line=_line_at(clean_sql, im.start()),
        )
        all_indexes.append(idx_def)
        if tbl_full in tables:
            tables[tbl_full].indexes.append(idx_def)

    # TimescaleDB hypertable markers
    for hm in re.finditer(r"create_hypertable\(\s*'([a-zA-Z_]+\.[a-zA-Z_]+)'", clean_sql, re.IGNORECASE):
        t_key = hm.group(1).lower()
        if t_key in tables:
            tables[t_key].is_hypertable = True

    # Row-Level Security markers
    for rm in re.finditer(
        r"\bALTER\s+TABLE\s+([a-zA-Z_]+\.[a-zA-Z_]+)\s+(ENABLE|FORCE)\s+ROW\s+LEVEL\s+SECURITY",
        clean_sql,
        re.IGNORECASE,
    ):
        t_key = rm.group(1).lower()
        mode = rm.group(2).upper()
        if t_key in tables:
            if mode == "ENABLE":
                tables[t_key].rls_enabled = True
            elif mode == "FORCE":
                tables[t_key].rls_forced = True

    return SchemaModel(
        source=source,
        tables=tables,
        foreign_keys=tuple(all_fks),
        checks=tuple(all_checks),
        indexes=tuple(all_indexes),
        schemas=tuple(schemas_list),
    )


def _split_dbml_attrs(attr_str: str) -> list[str]:
    """Split DBML `[pk, not null, default: `...`, note: '...']` safely."""
    items: list[str] = []
    buf: list[str] = []
    quote: str | None = None
    escape = False
    for ch in attr_str:
        if escape:
            buf.append(ch)
            escape = False
            continue
        if ch == "\\" and quote is not None:
            buf.append(ch)
            escape = True
            continue
        if quote is not None:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"', "`"):
            quote = ch
            buf.append(ch)
            continue
        if ch == ",":
            tok = "".join(buf).strip()
            if tok:
                items.append(tok)
            buf = []
            continue
        buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        items.append(tail)
    return items


def parse_dbml_schema(dbml_text: str, source: str = "DT-ERD-001.dbml") -> SchemaModel:
    """Parse `DT-ERD-001.dbml` into a normalized `SchemaModel`."""
    tables: dict[str, TableDef] = {}
    schemas_list: list[str] = []
    all_fks: list[ForeignKeyDef] = []
    all_indexes: list[IndexDef] = []

    lines = dbml_text.splitlines()
    i = 0
    total = len(lines)

    table_hdr_re = re.compile(
        r'^\s*Table\s+(?:"([a-zA-Z_][a-zA-Z0-9_]*)"\.|([a-zA-Z_][a-zA-Z0-9_]*)\.)?'
        r'(?:"([a-zA-Z_][a-zA-Z0-9_]*)"|([a-zA-Z_][a-zA-Z0-9_]*))\s*(?:\[[^\]]*\])?\s*\{\s*$'
    )
    col_re = re.compile(
        r'^\s*"?([a-zA-Z_][a-zA-Z0-9_]*)"?\s+"?([A-Za-z][A-Za-z0-9_(), ]*?)"?\s*(?:\[(.*)\])?\s*$'
    )
    ref_re = re.compile(
        r'^\s*Ref\s*(?:[A-Za-z0-9_]+\s*)?:\s*'
        r'"?([a-zA-Z_][a-zA-Z0-9_]*)"?\."?([a-zA-Z_][a-zA-Z0-9_]*)"?\."?([a-zA-Z_][a-zA-Z0-9_]*)"?\s*'
        r'([<>-]+)\s*'
        r'"?([a-zA-Z_][a-zA-Z0-9_]*)"?\."?([a-zA-Z_][a-zA-Z0-9_]*)"?\."?([a-zA-Z_][a-zA-Z0-9_]*)"?'
        r'(?:\s*\[([^\]]*)\])?'
    )

    while i < total:
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("//"):
            i += 1
            continue

        tg_m = re.match(r"^\s*TableGroup\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\{", stripped)
        if tg_m:
            s_name = tg_m.group(1).lower()
            if s_name not in schemas_list:
                schemas_list.append(s_name)
            while i < total and "}" not in lines[i]:
                i += 1
            i += 1
            continue

        tm = table_hdr_re.match(raw)
        if tm:
            schema_name = (tm.group(1) or tm.group(2) or "public").lower()
            table_name = (tm.group(3) or tm.group(4)).lower()
            full_name = f"{schema_name}.{table_name}"
            if schema_name not in schemas_list:
                schemas_list.append(schema_name)

            tbl = TableDef(schema=schema_name, name=table_name, line=i + 1)
            pk_cols: list[str] = []
            i += 1
            in_indexes = False

            while i < total:
                b_raw = lines[i]
                b_stripped = b_raw.strip()
                if b_stripped == "}":
                    if in_indexes:
                        in_indexes = False
                        i += 1
                        continue
                    break
                if not b_stripped or b_stripped.startswith("//"):
                    i += 1
                    continue
                if re.match(r"^Indexes\s*\{$", b_stripped, re.IGNORECASE):
                    in_indexes = True
                    i += 1
                    continue
                if in_indexes:
                    # Handle optional DBML index lines
                    idx_m = re.match(r"^(?:\(([^)]+)\)|([a-zA-Z0-9_]+))(?:\s*\[([^\]]*)\])?", b_stripped)
                    if idx_m:
                        cols_str = idx_m.group(1) or idx_m.group(2)
                        cols = tuple(c.strip().strip('"').lower() for c in cols_str.split(",") if c.strip())
                        opts = idx_m.group(3) or ""
                        name_m = re.search(r"name\s*:\s*'([^']+)'", opts)
                        is_uq = bool(re.search(r"\bunique\b", opts))
                        is_pk_idx = bool(re.search(r"\bpk\b", opts))
                        if is_pk_idx:
                            pk_cols.extend(cols)
                        else:
                            idx_def = IndexDef(
                                name=name_m.group(1) if name_m else f"idx_{table_name}_{'_'.join(cols)}",
                                table_name=full_name,
                                columns=cols,
                                is_unique=is_uq,
                                line=i + 1,
                            )
                            tbl.indexes.append(idx_def)
                            all_indexes.append(idx_def)
                    i += 1
                    continue

                cm = col_re.match(b_raw)
                if cm:
                    col_name = cm.group(1).lower()
                    col_type = _normalize_sql_type(cm.group(2))
                    attr_raw = cm.group(3) or ""
                    attrs = _split_dbml_attrs(attr_raw) if attr_raw else []
                    is_pk = False
                    nullable = True
                    is_unique = False
                    default_val: str | None = None
                    note_val: str | None = None
                    for a in attrs:
                        low = a.lower()
                        if low == "pk" or low == "primary key":
                            is_pk = True
                            nullable = False
                            if col_name not in pk_cols:
                                pk_cols.append(col_name)
                        elif low == "not null":
                            nullable = False
                        elif low == "null":
                            nullable = True
                        elif low == "unique":
                            is_unique = True
                        elif low.startswith("default:"):
                            default_val = a.split(":", 1)[1].strip().strip("`")
                        elif low.startswith("note:"):
                            note_val = a.split(":", 1)[1].strip().strip("'\"")

                    tbl.columns[col_name] = ColumnDef(
                        name=col_name,
                        data_type=col_type,
                        nullable=nullable,
                        is_pk=is_pk,
                        is_unique=is_unique,
                        default=default_val,
                        comment=note_val,
                        line=i + 1,
                    )
                    if is_unique:
                        tbl.unique_constraints.append((col_name,))
                i += 1

            tbl.primary_key = tuple(pk_cols)
            tables[full_name] = tbl
            i += 1
            continue

        rm = ref_re.match(raw)
        if rm:
            left_tbl = f"{rm.group(1).lower()}.{rm.group(2).lower()}"
            left_col = rm.group(3).lower()
            op = rm.group(4).strip()
            right_tbl = f"{rm.group(5).lower()}.{rm.group(6).lower()}"
            right_col = rm.group(7).lower()
            opts = rm.group(8) or ""

            if op == ">":
                child_tbl, child_col = left_tbl, left_col
                parent_tbl, parent_col = right_tbl, right_col
            else:
                # '<' or '-' (one-to-many or one-to-one where left is parent)
                parent_tbl, parent_col = left_tbl, left_col
                child_tbl, child_col = right_tbl, right_col

            del_m = re.search(r"delete\s*:\s*(set\s+null|set\s+default|restrict|cascade|no\s+action)", opts, re.IGNORECASE)
            upd_m = re.search(r"update\s*:\s*(set\s+null|set\s+default|restrict|cascade|no\s+action)", opts, re.IGNORECASE)
            fk = ForeignKeyDef(
                constraint_name=None,
                source_table=child_tbl,
                source_columns=(child_col,),
                target_table=parent_tbl,
                target_columns=(parent_col,),
                on_delete=re.sub(r"\s+", " ", del_m.group(1).upper()) if del_m else None,
                on_update=re.sub(r"\s+", " ", upd_m.group(1).upper()) if upd_m else None,
                line=i + 1,
            )
            all_fks.append(fk)
            if child_tbl in tables:
                tables[child_tbl].foreign_keys.append(fk)
                if child_col in tables[child_tbl].columns:
                    prev = tables[child_tbl].columns[child_col]
                    tables[child_tbl].columns[child_col] = ColumnDef(
                        name=prev.name,
                        data_type=prev.data_type,
                        nullable=prev.nullable,
                        is_pk=prev.is_pk,
                        is_unique=prev.is_unique,
                        default=prev.default,
                        has_check=prev.has_check,
                        is_fk=True,
                        comment=prev.comment,
                        line=prev.line,
                    )
        i += 1

    return SchemaModel(
        source=source,
        tables=tables,
        foreign_keys=tuple(all_fks),
        checks=(),
        indexes=tuple(all_indexes),
        schemas=tuple(schemas_list),
    )


def parse_erd_doc_schema(
    md_doc: ParsedMarkdownDoc | str,
    source: str = "DT-ERD-DOC-001.md",
) -> SchemaModel:
    """Parse `DT-ERD-DOC-001.md` §§3-4 into a normalized `SchemaModel`."""
    raw_text = md_doc.raw_text if isinstance(md_doc, ParsedMarkdownDoc) else md_doc
    lines = raw_text.splitlines()

    schemas_list: list[str] = []
    tables: dict[str, TableDef] = {}
    table_by_short_name: dict[str, str] = {}
    all_fks: list[ForeignKeyDef] = []

    current_schema: str | None = None
    current_table: TableDef | None = None
    in_section_3 = False
    in_section_4 = False

    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("## "):
            in_section_3 = stripped.startswith("## 3.")
            in_section_4 = stripped.startswith("## 4.")
            current_table = None
            continue

        if in_section_3:
            sm = re.match(r"^###\s+\d+\.\d+\s+Schema\s+`([a-zA-Z_][a-zA-Z0-9_]*)`", stripped)
            if sm:
                current_schema = sm.group(1).lower()
                if current_schema not in schemas_list:
                    schemas_list.append(current_schema)
                current_table = None
                continue

            tm = re.match(r"^####\s+\d+\.\d+\.\d+\s+([a-zA-Z_][a-zA-Z0-9_]*)", stripped)
            if tm and current_schema:
                t_name = tm.group(1).lower()
                full_name = f"{current_schema}.{t_name}"
                current_table = TableDef(schema=current_schema, name=t_name, line=line_idx)
                tables[full_name] = current_table
                table_by_short_name[t_name] = full_name
                continue

            if (
                current_table is not None
                and stripped.startswith("|")
                and not re.match(r"^\|[\s:-]+\|", stripped)
                and not stripped.startswith("| Physical Field")
            ):
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                if len(cells) >= 6 and cells[0]:
                    col_name = cells[0].strip("` ").lower()
                    col_type = _normalize_sql_type(cells[1].strip("` "))
                    null_str = cells[2].upper()
                    nullable = "NOT NULL" not in null_str
                    constraints_str = cells[3].upper()
                    default_raw = cells[4].strip("` ")
                    default_val = None if default_raw in ("", "-", "NULL") else default_raw
                    comment_raw = cells[5].strip()
                    comment = None if comment_raw in ("", "-") else comment_raw

                    is_pk = "PK" in constraints_str
                    is_uq = "UNIQUE" in constraints_str
                    has_check = "CHECK" in constraints_str
                    is_fk = "FK" in constraints_str

                    current_table.columns[col_name] = ColumnDef(
                        name=col_name,
                        data_type=col_type,
                        nullable=nullable,
                        is_pk=is_pk,
                        is_unique=is_uq,
                        default=default_val,
                        has_check=has_check,
                        is_fk=is_fk,
                        comment=comment,
                        line=line_idx,
                    )
                    if is_pk and col_name not in current_table.primary_key:
                        current_table.primary_key = (*current_table.primary_key, col_name)
                    if is_uq:
                        current_table.unique_constraints.append((col_name,))

        elif in_section_4:
            if (
                stripped.startswith("|")
                and not re.match(r"^\|[\s:-]+\|", stripped)
                and not stripped.startswith("| Parent Table")
            ):
                cells = [c.strip() for c in stripped.strip("|").split("|")]
                if len(cells) >= 6 and cells[0] and cells[2]:
                    parent_short = cells[0].strip("` ").lower()
                    child_short = cells[2].strip("` ").lower()
                    on_delete = cells[4].strip().upper()
                    on_update = cells[5].strip().upper()
                    parent_full = table_by_short_name.get(parent_short, parent_short)
                    child_full = table_by_short_name.get(child_short, child_short)
                    fk = ForeignKeyDef(
                        constraint_name=None,
                        source_table=child_full,
                        source_columns=(),
                        target_table=parent_full,
                        target_columns=("id",),
                        on_delete=on_delete,
                        on_update=on_update,
                        line=line_idx,
                    )
                    all_fks.append(fk)
                    if child_full in tables:
                        tables[child_full].foreign_keys.append(fk)

    return SchemaModel(
        source=source,
        tables=tables,
        foreign_keys=tuple(all_fks),
        checks=(),
        indexes=(),
        schemas=tuple(schemas_list),
    )
