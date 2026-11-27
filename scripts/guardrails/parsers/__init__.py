"""
Layer 1 Single-Pass Repository Indexer (`RepoIndex` & `build_repo_index`).

Guarantees each file under `root` (and optional `prototype_dir`) is read from disk
at most once during an audit run.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ..config import IGNORED_DIR_NAMES, SSOT_PATHS
from .asset_parser import (
    CsvTable,
    IconsModel,
    PrototypeAsset,
    TokensModel,
    parse_csv_table,
    parse_icons_svg,
    parse_prototype_asset,
    parse_tokens_css,
)
from .csharp_parser import (
    CSharpEnum,
    CSharpRecord,
    RazorContract,
    parse_csharp_blocks_in_doc,
)
from .markdown_parser import ParsedMarkdownDoc, parse_markdown_text
from .sql_dbml_parser import (
    SchemaModel,
    parse_dbml_schema,
    parse_erd_doc_schema,
    parse_sql_schema,
)


@dataclass(slots=True)
class RepoIndex:
    root: Path
    prototype_dir: Path | None
    markdown_docs: dict[str, ParsedMarkdownDoc] = field(default_factory=dict)
    screen_docs: dict[str, ParsedMarkdownDoc] = field(default_factory=dict)
    usecase_docs: dict[str, ParsedMarkdownDoc] = field(default_factory=dict)
    csharp_records: dict[str, list[CSharpRecord]] = field(default_factory=dict)
    csharp_enums: dict[str, list[CSharpEnum]] = field(default_factory=dict)
    razor_contracts: dict[str, list[RazorContract]] = field(default_factory=dict)
    sql_schema: SchemaModel | None = None
    dbml_schema: SchemaModel | None = None
    erd_doc_schema: SchemaModel | None = None
    tokens: TokensModel | None = None
    icons: IconsModel | None = None
    prototype_assets: dict[str, PrototypeAsset] = field(default_factory=dict)
    csv_tables: dict[str, CsvTable] = field(default_factory=dict)
    srs_rows: tuple[dict[str, str], ...] = ()
    raw_texts: dict[str, str] = field(default_factory=dict)
    read_counts: dict[str, int] = field(default_factory=dict)
    repo_files: frozenset[str] = field(default_factory=frozenset)

    @property
    def total_files_indexed(self) -> int:
        return len(self.read_counts)

    def all_csharp_records(self) -> list[CSharpRecord]:
        out: list[CSharpRecord] = []
        for recs in self.csharp_records.values():
            out.extend(recs)
        return out

    def all_csharp_enums(self) -> list[CSharpEnum]:
        out: list[CSharpEnum] = []
        for enms in self.csharp_enums.values():
            out.extend(enms)
        return out

    def all_razor_contracts(self) -> list[RazorContract]:
        out: list[RazorContract] = []
        for razs in self.razor_contracts.values():
            out.extend(razs)
        return out


def _is_ignored_rel(rel_parts: tuple[str, ...]) -> bool:
    return any(part in IGNORED_DIR_NAMES or part.startswith(".") for part in rel_parts)


def _discover_non_hidden_files(root: Path, suffix: str) -> list[Path]:
    found: list[Path] = []
    for p in root.rglob(f"*{suffix}"):
        if not p.is_file():
            continue
        try:
            rel_parts = p.relative_to(root).parts
        except ValueError:
            continue
        if _is_ignored_rel(rel_parts):
            continue
        found.append(p)
    return sorted(found, key=lambda item: item.relative_to(root).as_posix())


def build_repo_index(
    root: Path,
    prototype_dir: Path | None = None,
) -> RepoIndex:
    """
    Build a complete `RepoIndex` in a single pass, reading every file at most once.
    """
    resolved_root = root.resolve()
    if not resolved_root.is_dir():
        raise FileNotFoundError(f"Repository root directory does not exist: {resolved_root}")

    resolved_proto_dir: Path | None = None
    if prototype_dir is not None:
        resolved_proto_dir = prototype_dir.resolve()
        if not resolved_proto_dir.is_dir():
            raise FileNotFoundError(f"Prototype directory does not exist: {resolved_proto_dir}")
    else:
        for candidate in (
            resolved_root / "ui-ux" / "prototypes",
            resolved_root / "prototypes",
        ):
            if candidate.is_dir():
                resolved_proto_dir = candidate.resolve()
                break

    index = RepoIndex(root=resolved_root, prototype_dir=resolved_proto_dir)
    text_cache: dict[Path, str] = {}

    def read_once(abs_path: Path, rel_key: str) -> str | None:
        canonical = abs_path.resolve()
        if canonical in text_cache:
            return text_cache[canonical]
        if not canonical.is_file():
            return None
        content = canonical.read_text(encoding="utf-8")
        text_cache[canonical] = content
        index.raw_texts[rel_key] = content
        index.read_counts[rel_key] = index.read_counts.get(rel_key, 0) + 1
        return content

    # 1. Discover and parse all non-hidden Markdown files
    csharp_target_rel_paths: set[str] = {
        SSOT_PATHS.ui_ctr_doc,
        SSOT_PATHS.arq_cmp_doc,
    }
    for md_path in _discover_non_hidden_files(resolved_root, ".md"):
        rel = md_path.relative_to(resolved_root).as_posix()
        if rel.startswith("reports/"):
            continue
        raw = read_once(md_path, rel)
        if raw is None:
            continue
        doc = parse_markdown_text(rel, md_path.resolve(), raw)
        index.markdown_docs[rel] = doc

        name = md_path.name
        if name.startswith("SCR-") and name.endswith(".md"):
            index.screen_docs[rel] = doc
            csharp_target_rel_paths.add(rel)
        elif name.startswith("UC-") and name.endswith(".md"):
            index.usecase_docs[rel] = doc

        # Parse C#/Razor blocks for SCR-*.md, DT-UI-CTR-001.md, and DT-ARQ-CMP-DOC-001.md
        if rel in csharp_target_rel_paths:
            recs, enms, razs = parse_csharp_blocks_in_doc(doc)
            if recs:
                index.csharp_records[rel] = recs
            if enms:
                index.csharp_enums[rel] = enms
            if razs:
                index.razor_contracts[rel] = razs

    # 2. Parse SQL, DBML, and ERD Markdown schema
    sql_path = resolved_root / SSOT_PATHS.erd_sql
    sql_text = read_once(sql_path, SSOT_PATHS.erd_sql)
    if sql_text is not None:
        index.sql_schema = parse_sql_schema(sql_text, source=SSOT_PATHS.erd_sql)

    dbml_path = resolved_root / SSOT_PATHS.erd_dbml
    dbml_text = read_once(dbml_path, SSOT_PATHS.erd_dbml)
    if dbml_text is not None:
        index.dbml_schema = parse_dbml_schema(dbml_text, source=SSOT_PATHS.erd_dbml)

    erd_doc = index.markdown_docs.get(SSOT_PATHS.erd_doc)
    if erd_doc is not None:
        index.erd_doc_schema = parse_erd_doc_schema(erd_doc, source=SSOT_PATHS.erd_doc)

    # 3. Parse Design System tokens.css and icons.svg
    tokens_path = resolved_root / SSOT_PATHS.tokens_css
    tokens_text = read_once(tokens_path, SSOT_PATHS.tokens_css)
    if tokens_text is not None:
        index.tokens = parse_tokens_css(tokens_text)

    icons_path = resolved_root / SSOT_PATHS.icons_svg
    icons_text = read_once(icons_path, SSOT_PATHS.icons_svg)
    if icons_text is not None:
        index.icons = parse_icons_svg(icons_text)

    # 4. Parse requirements/data/*.csv
    req_data_dir = resolved_root / "requirements" / "data"
    if req_data_dir.is_dir():
        for csv_path in sorted(req_data_dir.glob("*.csv"), key=lambda p: p.name):
            rel = csv_path.relative_to(resolved_root).as_posix()
            csv_text = read_once(csv_path, rel)
            if csv_text is None:
                continue
            table = parse_csv_table(rel, csv_text)
            index.csv_tables[rel] = table
            if rel == SSOT_PATHS.srs_csv:
                index.srs_rows = table.rows

    # 5. Parse prototype .html / .css / .js assets if present
    proto_roots: list[tuple[Path, str]] = []
    if resolved_proto_dir is not None:
        try:
            prefix_rel = resolved_proto_dir.relative_to(resolved_root).as_posix()
        except ValueError:
            prefix_rel = resolved_proto_dir.name
        proto_roots.append((resolved_proto_dir, prefix_rel))

    # Also scan any .html/.css/.js inside repo ui-ux/ (excluding tokens.css already parsed above)
    ui_ux_dir = resolved_root / "ui-ux"
    if ui_ux_dir.is_dir():
        proto_roots.append((ui_ux_dir, "ui-ux"))

    seen_proto_paths: set[Path] = set()
    for scan_dir, _ in proto_roots:
        for ext in (".html", ".css", ".js"):
            for asset_path in _discover_non_hidden_files(scan_dir, ext):
                rel_to_scan = asset_path.relative_to(scan_dir).parts
                if any(
                    part in {"suggested-doc-changes", "suggested-sena-evidence"}
                    for part in rel_to_scan
                ):
                    continue
                canonical = asset_path.resolve()
                if canonical in seen_proto_paths:
                    continue
                seen_proto_paths.add(canonical)
                try:
                    rel = canonical.relative_to(resolved_root).as_posix()
                except ValueError:
                    rel = f"{scan_dir.name}/{canonical.relative_to(scan_dir).as_posix()}"
                if rel == SSOT_PATHS.tokens_css:
                    continue
                asset_text = read_once(canonical, rel)
                if asset_text is not None:
                    index.prototype_assets[rel] = parse_prototype_asset(rel, asset_text)

    # 6. Parse PlantUML and Structurizr DSL texts for pure Layer 2 inspection
    puml_path = resolved_root / SSOT_PATHS.dm_puml
    read_once(puml_path, SSOT_PATHS.dm_puml)
    for dsl_path in _discover_non_hidden_files(resolved_root, ".dsl"):
        rel_dsl = dsl_path.relative_to(resolved_root).as_posix()
        read_once(dsl_path, rel_dsl)

    # 7. Collect non-hidden repository file paths (stat-only, zero reads) for link/asset checks
    repo_file_set: set[str] = set()
    for any_path in resolved_root.rglob("*"):
        if not any_path.is_file():
            continue
        try:
            rel_parts = any_path.relative_to(resolved_root).parts
        except ValueError:
            continue
        if _is_ignored_rel(rel_parts):
            continue
        repo_file_set.add(any_path.relative_to(resolved_root).as_posix())
    index.repo_files = frozenset(repo_file_set)

    return index
