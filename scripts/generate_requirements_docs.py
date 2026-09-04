#!/usr/bin/env python3
"""Generador unificado de Historias de Usuario (US) y Requisitos Transversales (TR)

para el repositorio adso-dteam-docs.

Uso:
  python scripts/generate_requirements_docs.py                  # Modo seguro (Dry-run)
  python scripts/generate_requirements_docs.py --write          # Escribe en disco
  python scripts/generate_requirements_docs.py --diff           # Muestra diferencias
  python scripts/generate_requirements_docs.py --modules MTTO --write
"""

from __future__ import annotations

import argparse
import csv
import difflib
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent

# Rutas por defecto relativas a la raíz del repositorio
DEFAULT_DATA_DIR = REPO_ROOT / "requirements" / "data"
DEFAULT_US_OUT = REPO_ROOT / "requirements" / "user-stories"
DEFAULT_COMMON_OUT = REPO_ROOT / "requirements" / "common"

ALLOWED_MODULES = {"ADM", "INV", "VIS", "MTTO"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera documentación Markdown para US y TR a partir de CSVs maestros."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="Directorio donde residen los CSVs maestros.",
    )
    parser.add_argument(
        "--us-out",
        type=Path,
        default=DEFAULT_US_OUT,
        help="Directorio de salida para Historias de Usuario.",
    )
    parser.add_argument(
        "--common-out",
        type=Path,
        default=DEFAULT_COMMON_OUT,
        help="Directorio de salida para Requisitos Transversales (COMMON).",
    )
    parser.add_argument(
        "--modules",
        nargs="*",
        help="Filtrar por módulos específicos (ADM, INV, VIS, MTTO).",
    )
    parser.add_argument(
        "--ids",
        nargs="*",
        help="Filtrar por IDs específicos (ej. MTTO-001, TR-003).",
    )
    parser.add_argument(
        "--only-us",
        action="store_true",
        help="Generar únicamente Historias de Usuario.",
    )
    parser.add_argument(
        "--only-tr",
        action="store_true",
        help="Generar únicamente Requisitos Transversales.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Escribe los cambios en disco (por defecto opera en dry-run).",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Muestra diferencias unificadas contra archivos existentes.",
    )
    parser.add_argument(
        "--write-index",
        action="store_true",
        help="Genera y sobreescribe INDEX.md en la carpeta common.",
    )
    return parser.parse_args()


# ==============================================================================
# Funciones Utilitarias de Limpieza y Formato
# ==============================================================================

def clean(value: str | None) -> str:
    return (value or "").replace("\r", "").replace("\n", " ").strip()


def md_escape(value: str) -> str:
    return clean(value).replace("|", "\\|")


def req_num_sort_key(req_id: str) -> tuple[int, str]:
    m = re.search(r"(\d+)$", req_id)
    return (int(m.group(1)) if m else 99999, req_id)


def tr_sort_key(tr_id: str) -> tuple[int, str]:
    match = re.match(r"TR-(\d+)", tr_id or "")
    return (int(match.group(1)) if match else 999, tr_id or "")


def us_sort_key(us_id: str) -> tuple[str, int, str]:
    m = re.match(r"^([A-Z]+)-(\d+)$", us_id)
    if m:
        return (m.group(1), int(m.group(2)), us_id)
    return ("ZZZ", 99999, us_id)


def read_csv_safe(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def find_csv_file(data_dir: Path, possible_names: list[str]) -> Path:
    for name in possible_names:
        candidate = data_dir / name
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"No se encontró ninguno de los archivos {possible_names} en {data_dir}"
    )


# ==============================================================================
# Lógica de Generación: Requisitos Transversales (TR / COMMON)
# ==============================================================================

def parse_tr_title(raw_tr: str, tr_id: str) -> str:
    text = clean(raw_tr)
    if not text:
        return f"{tr_id} - Requisito Transversal"
    match = re.match(r"^(TR-\d+):\s*(.+?)(?:\s*\(https?://[^)]+\))?$", text)
    if match:
        return match.group(2).strip()
    cleaned = re.sub(r"^TR-\d+:\s*", "", text).strip()
    cleaned = re.sub(r"\(https?://\S+\)", "", cleaned).strip()
    return cleaned or f"{tr_id} - Requisito Transversal"


def normalize_refs(value: str) -> str:
    raw = (value or "").replace("\r", "").strip()
    if not raw:
        return ""
    parts = [
        re.sub(r"^[•\-*]+\s*", "", line.strip())
        for line in raw.split("\n")
        if line.strip()
    ]
    if not parts:
        return ""
    return f"<ul>{''.join(f'<li>{item}</li>' for item in parts)}</ul>"


def render_tr_req_table(rows: list[dict], req_type: str) -> str:
    filtered = []
    for row in rows:
        rtype = clean(row.get("Tipo")).upper()
        req_id = clean(row.get("Req ID")).upper()
        if not rtype:
            rtype = "FR" if "-FR-" in req_id else "NFR" if "-NFR-" in req_id else ""
        if rtype == req_type:
            filtered.append(row)

    if not filtered:
        return "_Sin requisitos en esta categoría._\n"

    filtered.sort(key=lambda r: req_num_sort_key(clean(r.get("Req ID"))))
    lines = [
        "| ID | Descripción | Categoría ISO 25010 | Prioridad |",
        "|---|---|---|---|",
    ]
    for row in filtered:
        req_id = clean(row.get("Req ID"))
        desc = md_escape(clean(row.get("Descripción")))
        if desc.startswith(f"{req_id}:"):
            desc = desc[len(req_id) + 1:].strip()
        cat = md_escape(clean(row.get("Categoría ISO 25010")))
        prio = md_escape(clean(row.get("Prioridad")))
        lines.append(f"| {req_id} | {desc} | {cat} | {prio} |")
    return "\n".join(lines) + "\n"


def build_tr_markdown(
    tr_id: str,
    rows: list[dict],
    meta: dict[str, str],
) -> str:
    rows_sorted = sorted(rows, key=lambda r: req_num_sort_key(clean(r.get("Req ID"))))
    title = parse_tr_title(clean(rows_sorted[0].get("TR")), tr_id)
    if meta.get("name"):
        title = meta["name"]

    desc = meta.get("desc", "")
    scope = meta.get("scope", "")
    refs = meta.get("refs", "")

    total = len(rows_sorted)
    fr_total = sum(1 for r in rows_sorted if clean(r.get("Tipo")).upper() == "FR" or "-FR-" in clean(r.get("Req ID")).upper())
    nfr_total = sum(1 for r in rows_sorted if clean(r.get("Tipo")).upper() == "NFR" or "-NFR-" in clean(r.get("Req ID")).upper())

    parts = [
        "---",
        f"id: {tr_id}",
        f'nombre: "{title}"',
        'epic: "COMMON"',
        'tipo: "Requisito Transversal"',
        f"total_requisitos: {total}",
        f"fr: {fr_total}",
        f"nfr: {nfr_total}",
        "---",
        "",
        f"# {tr_id}: {title}",
        "",
        "## Contexto transversal",
        "",
        "| Descripción general | Alcance | Referencias normativas |",
        "| --- | --- | --- |",
        f"| {md_escape(desc)} | {md_escape(scope)} | {refs} |",
        "",
        "## Requisitos Funcionales (FR)",
        "",
        render_tr_req_table(rows_sorted, "FR").rstrip(),
        "",
        "## Requisitos No Funcionales (NFR)",
        "",
        render_tr_req_table(rows_sorted, "NFR").rstrip(),
        "",
        "## Fuente",
        "- Generado automáticamente desde `srs.csv`.",
        "",
    ]
    return "\n".join(parts)


def build_tr_index_markdown(grouped: dict[str, list[dict]], metadata: dict[str, dict[str, str]]) -> str:
    tr_ids = sorted(grouped.keys(), key=tr_sort_key)
    lines = [
        "---",
        "id: INDEX-COMMON",
        'title: "Requisitos Transversales — Índice Maestro"',
        "---",
        "",
        "# INDEX — COMMON (Requisitos Transversales)",
        "",
        "Consolidado de patrones arquitectónicos transversales aplicables a los módulos MTTO, INV, VIS y ADM.",
        "",
        "| ID | Nombre | FR | NFR | Total | Archivo |",
        "|---|---|---:|---:|---:|---|",
    ]
    for tr_id in tr_ids:
        rows = grouped[tr_id]
        meta = metadata.get(tr_id, {})
        title = meta.get("name") or parse_tr_title(clean(rows[0].get("TR")), tr_id)
        fr_total = sum(1 for r in rows if clean(r.get("Tipo")).upper() == "FR" or "-FR-" in clean(r.get("Req ID")).upper())
        nfr_total = sum(1 for r in rows if clean(r.get("Tipo")).upper() == "NFR" or "-NFR-" in clean(r.get("Req ID")).upper())
        total = len(rows)
        lines.append(f"| **{tr_id}** | {md_escape(title)} | {fr_total} | {nfr_total} | {total} | [[{tr_id}]] |")
    lines.append("")
    return "\n".join(lines)


# ==============================================================================
# Lógica de Generación: Historias de Usuario (User Stories)
# ==============================================================================

def extract_us_id(row: dict[str, str]) -> str:
    direct = clean(row.get("US ID"))
    if re.match(r"^[A-Z]+-\d+$", direct):
        return direct
    name = clean(row.get("Nombre"))
    m = re.match(r"^([A-Z]+-\d+):", name)
    return m.group(1) if m else ""


def parse_us_title(row: dict[str, str], us_id: str) -> str:
    name = clean(row.get("Nombre"))
    if not name:
        return us_id
    return re.sub(r"^[A-Z]+-\d+:\s*", "", name) or us_id


def get_transversales_ids(row: dict[str, str]) -> list[str]:
    raw = clean(row.get("Transversales Aplicables")) or clean(row.get("Req IDs"))
    ids = re.findall(r"\bTR-\d+\b", raw.upper())
    unique: list[str] = []
    seen = set()
    for tr_id in ids:
        if tr_id not in seen:
            seen.add(tr_id)
            unique.append(tr_id)
    return unique


def build_acceptance_table(criteria: list[dict[str, str]]) -> str:
    if not criteria:
        return "_Sin criterios de aceptación en gherkin.csv para esta US._\n"
    lines = [
        "| Escenario | Dado (Contexto) | Cuando (Acción) | Entonces (Resultado) |",
        "|---|---|---|---|",
    ]
    for row in sorted(criteria, key=lambda r: req_num_sort_key(clean(r.get("AC ID")))):
        lines.append(
            f"| {md_escape(row.get('Escenario', ''))} | {md_escape(row.get('Contexto', ''))} | "
            f"{md_escape(row.get('Acción', ''))} | {md_escape(row.get('Resultado', ''))} |"
        )
    return "\n".join(lines) + "\n"


def build_us_reqs_table(rows: list[dict[str, str]], req_type: str) -> str:
    reqs = []
    for row in rows:
        rid = clean(row.get("Req ID")).upper()
        rtype = clean(row.get("Tipo")).upper()
        if not rtype:
            rtype = "FR" if rid.startswith("FR-") else "NFR" if rid.startswith("NFR-") else ""
        if rtype == req_type:
            reqs.append(row)

    if not reqs:
        return "_Sin requisitos en esta categoría._\n"

    reqs.sort(key=lambda r: req_num_sort_key(clean(r.get("Req ID"))))
    lines = [
        "| ID | Descripción | Categoría ISO 25010 | Prioridad | Fuente |",
        "|---|---|---|---|---|",
    ]
    for row in reqs:
        rid = md_escape(clean(row.get("Req ID")))
        desc_raw = clean(row.get("Descripción"))
        desc = md_escape(re.sub(r"^(?:FR|NFR)-\d+:\s*", "", desc_raw, flags=re.IGNORECASE))
        cat = md_escape(clean(row.get("Categoría ISO 25010")))
        prio = md_escape(clean(row.get("Prioridad")))
        fuente = md_escape(clean(row.get("Fuente")) or clean(row.get("Historia Relacionada")))
        lines.append(f"| {rid} | {desc} | {cat} | {prio} | {fuente} |")
    return "\n".join(lines) + "\n"


def render_us_markdown(
    us: dict,
    acceptance: list[dict[str, str]],
    srs_rows: list[dict[str, str]],
) -> str:
    us_id = us["us_id"]
    title = us["title"]

    frontmatter = [
        "---",
        f"id: {us_id}",
        f'nombre: "{title}"',
        f"prioridad: {us['moscow']}",
        f"puntos: {us['points']}",
        f"rol: {us['role']}",
        f"epic: {us['epic']}",
        f"observaciones: {us['obs']}",
    ]

    transversales = us.get("transversales", [])
    if transversales:
        frontmatter.append("transversales_aplicables:")
        for tr_id in transversales:
            frontmatter.append(f'  - "[[{tr_id}]]"')
    else:
        frontmatter.append("transversales_aplicables: []")

    frontmatter.append("---")

    body = [
        f"# {us_id}: {title}",
        "",
        "## Descripción de la Historia",
        "",
        "| Rol | Acción | Beneficio |",
        "|---|---|---|",
        f"| {md_escape('Como ' + us['role'])} | {md_escape('Quiero ' + us['quiero'])} | {md_escape('Para ' + us['para'])} |",
        "",
        "## Criterios de Aceptación",
        build_acceptance_table(acceptance).rstrip(),
        "",
        "## Requisitos Funcionales (FR)",
        build_us_reqs_table(srs_rows, "FR").rstrip(),
        "",
        "## Requisitos No Funcionales (NFR)",
        build_us_reqs_table(srs_rows, "NFR").rstrip(),
        "",
        "## Fuente",
        "- Generado automáticamente desde `user_stories.csv`, `gherkin.csv` y `srs.csv`.",
        "",
    ]
    return "\n".join(frontmatter + [""] + body)


# ==============================================================================
# Controlador de Ejecución y Diff
# ==============================================================================

def print_diff(path: Path, old_text: str, new_text: str) -> None:
    diff = difflib.unified_diff(
        old_text.splitlines(keepends=True),
        new_text.splitlines(keepends=True),
        fromfile=f"{path.name} (actual)",
        tofile=f"{path.name} (propuesto)",
        lineterm="",
    )
    out = "".join(diff)
    if out:
        print(f"\n--- Diff en {path.relative_to(REPO_ROOT)} ---")
        print(out)


def main() -> None:
    args = parse_args()

    data_dir = args.data_dir.resolve()
    us_out_dir = args.us_out.resolve()
    common_out_dir = args.common_out.resolve()

    is_write = args.write
    show_diff = args.diff

    # Localizar archivos CSV
    us_csv = find_csv_file(data_dir, ["user-stories.csv", "user_stories.csv"])
    srs_csv = find_csv_file(data_dir, ["srs.csv"])
    gherkin_csv = find_csv_file(data_dir, ["gherkin.csv"])
    tr_csv = find_csv_file(data_dir, ["transversal-requirements.csv", "tr.csv"])

    print(f"📂 Leyendo datos maestros desde: {data_dir.relative_to(REPO_ROOT)}")

    srs_rows = read_csv_safe(srs_csv)
    modules_filter = {m.upper() for m in (args.modules or []) if m.upper() in ALLOWED_MODULES}
    ids_filter = {i.upper() for i in (args.ids or [])}

    total_created = 0
    total_modified = 0
    total_unchanged = 0

    # --------------------------------------------------------------------------
    # 1. Procesar Requisitos Transversales (TR / COMMON)
    # --------------------------------------------------------------------------
    if not args.only_us:
        print("\n🔧 Procesando Requisitos Transversales (COMMON)...")
        tr_rows_raw = read_csv_safe(tr_csv)
        tr_meta = {}
        for r in tr_rows_raw:
            tr_id = clean(r.get("TR ID")).upper()
            if tr_id:
                tr_meta[tr_id] = {
                    "name": clean(r.get("Name")),
                    "desc": clean(r.get("Descripción General")),
                    "scope": clean(r.get("Alcance")),
                    "refs": normalize_refs(r.get("Referencias Normativas")),
                }

        grouped_tr: dict[str, list[dict]] = defaultdict(list)
        for r in srs_rows:
            req_id = clean(r.get("Req ID")).upper()
            tr_id = clean(r.get("TR ID")).upper()
            if not req_id.startswith("TR-"):
                continue
            if not tr_id:
                m = re.match(r"^(TR-\d+)-", req_id)
                tr_id = m.group(1) if m else ""
            if tr_id:
                grouped_tr[tr_id].append(r)

        common_out_dir.mkdir(parents=True, exist_ok=True)

        for tr_id in sorted(grouped_tr.keys(), key=tr_sort_key):
            if ids_filter and tr_id not in ids_filter:
                continue

            target_file = common_out_dir / f"{tr_id}.md"
            content = build_tr_markdown(tr_id, grouped_tr[tr_id], tr_meta.get(tr_id, {}))
            current = target_file.read_text(encoding="utf-8") if target_file.exists() else ""

            if not target_file.exists():
                total_created += 1
                status = "✨ NUEVO"
            elif current != content:
                total_modified += 1
                status = "📝 MODIFICADO"
                if show_diff:
                    print_diff(target_file, current, content)
            else:
                total_unchanged += 1
                status = "💤 SIN CAMBIOS"

            if is_write and (current != content):
                target_file.write_text(content, encoding="utf-8")
                print(f"  {status}: {target_file.relative_to(REPO_ROOT)}")
            elif not is_write:
                print(f"  [DRY-RUN] {status}: {target_file.relative_to(REPO_ROOT)}")

        if args.write_index:
            index_file = common_out_dir / "INDEX.md"
            index_content = build_tr_index_markdown(grouped_tr, tr_meta)
            if is_write:
                index_file.write_text(index_content, encoding="utf-8")
                print(f"  🧭 ÍNDICE ESCRITO: {index_file.relative_to(REPO_ROOT)}")
            else:
                print(f"  [DRY-RUN] 🧭 ÍNDICE PROYECTADO: {index_file.relative_to(REPO_ROOT)}")

    # --------------------------------------------------------------------------
    # 2. Procesar Historias de Usuario (US por Módulo)
    # --------------------------------------------------------------------------
    if not args.only_tr:
        print("\n📋 Procesando Historias de Usuario (User Stories)...")
        us_rows_raw = read_csv_safe(us_csv)
        gherkin_rows_raw = read_csv_safe(gherkin_csv)

        # Indexar SRS y Gherkin
        srs_by_us: dict[str, list[dict]] = defaultdict(list)
        for r in srs_rows:
            rel = clean(r.get("Historia Relacionada"))
            m = re.match(r"^([A-Z]+-\d+):", rel)
            if m:
                srs_by_us[m.group(1)].append(r)

        gherkin_by_us: dict[str, list[dict]] = defaultdict(list)
        for r in gherkin_rows_raw:
            uid = clean(r.get("US ID")).upper()
            if re.match(r"^[A-Z]+-\d+$", uid):
                gherkin_by_us[uid].append(r)

        for row in us_rows_raw:
            us_id = extract_us_id(row).upper()
            if not us_id:
                continue
            module = clean(row.get("Epic")).upper() or us_id.split("-")[0]
            if module not in ALLOWED_MODULES:
                continue
            if modules_filter and module not in modules_filter:
                continue
            if ids_filter and us_id not in ids_filter:
                continue

            target_module_dir = us_out_dir / module.lower()
            target_module_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_module_dir / f"{us_id}.md"

            quiero = clean(row.get("Quiero")) or clean(row.get("Acción"))
            para = clean(row.get("Para")) or clean(row.get("Beneficio"))
            role = clean(row.get("Como")) or re.sub(r"\s*\(https?://[^)]+\)\s*$", "", clean(row.get("Rol (Como ...)")))

            us_dict = {
                "us_id": us_id,
                "module": module,
                "title": parse_us_title(row, us_id),
                "role": role,
                "quiero": re.sub(r"^Quiero\s+", "", quiero, flags=re.IGNORECASE),
                "para": re.sub(r"^Para\s+", "", para, flags=re.IGNORECASE),
                "moscow": clean(row.get("MoSCoW")) or "N/A",
                "points": clean(row.get("Puntos Fibonacci")) or "0",
                "epic": module,
                "obs": clean(row.get("Observaciones")),
                "transversales": get_transversales_ids(row),
            }

            content = render_us_markdown(us_dict, gherkin_by_us.get(us_id, []), srs_by_us.get(us_id, []))
            current = target_file.read_text(encoding="utf-8") if target_file.exists() else ""

            if not target_file.exists():
                total_created += 1
                status = "✨ NUEVO"
            elif current != content:
                total_modified += 1
                status = "📝 MODIFICADO"
                if show_diff:
                    print_diff(target_file, current, content)
            else:
                total_unchanged += 1
                status = "💤 SIN CAMBIOS"

            if is_write and (current != content):
                target_file.write_text(content, encoding="utf-8")
                print(f"  {status}: {target_file.relative_to(REPO_ROOT)}")
            elif not is_write:
                print(f"  [DRY-RUN] {status}: {target_file.relative_to(REPO_ROOT)}")

    # --------------------------------------------------------------------------
    # Resumen Final
    # --------------------------------------------------------------------------
    mode_str = "ESCRITURA DIRECTA (--write)" if is_write else "MODO SEGURO / SIMULACIÓN (--dry-run por defecto)"
    print("\n" + "=" * 60)
    print(f"🎯 Resumen de Ejecución [{mode_str}]:")
    print(f"   • Archivos nuevos proyectados:    {total_created}")
    print(f"   • Archivos modificados:          {total_modified}")
    print(f"   • Archivos al día (sin cambios): {total_unchanged}")
    print("=" * 60)
    if not is_write:
        print("💡 Para aplicar los cambios reales en disco, ejecute con el flag '--write'.")


if __name__ == "__main__":
    main()