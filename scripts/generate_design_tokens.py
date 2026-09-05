#!/usr/bin/env python3
"""Generate ui-ux/assets/tokens.css and ui-ux/assets/tokens_penpot.json from the design-system Markdown source."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "ui-ux" / "DT-UI-DS-DOC-001.md"
DEFAULT_TARGET = ROOT / "ui-ux" / "assets" / "tokens.css"
DEFAULT_PENPOT_TARGET = ROOT / "ui-ux" / "assets" / "tokens_penpot.json"


def clean_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip("`"))


def comparable(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(
        char for char in normalized if not unicodedata.combining(char)
    ).lower()


def markdown_tables(text: str) -> list[tuple[str, list[str], list[list[str]]]]:
    lines = text.splitlines()
    tables: list[tuple[str, list[str], list[list[str]]]] = []
    current_heading = ""
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        heading = re.match(r"^#{2,4}\s+(.+)$", line)
        if heading:
            current_heading = heading.group(1).strip()
        if (
            line.startswith("|")
            and index + 1 < len(lines)
            and set(
                lines[index + 1]
                .replace("|", "")
                .replace(":", "")
                .replace("-", "")
                .strip()
            )
            == set()
        ):
            headers = [clean_cell(cell) for cell in line.strip("|").split("|")]
            rows: list[list[str]] = []
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(
                    [
                        clean_cell(cell)
                        for cell in lines[index].strip().strip("|").split("|")
                    ]
                )
                index += 1
            tables.append((current_heading, headers, rows))
            continue
        index += 1
    return tables


def table_for(tables, heading_fragment: str, header_fragment: str) -> list[list[str]]:
    for heading, headers, rows in tables:
        if comparable(heading_fragment) in comparable(heading) and comparable(
            header_fragment
        ) in comparable(" ".join(headers)):
            return rows
    raise ValueError(f"No se encontró tabla: {heading_fragment} / {header_fragment}")


def css_value(value: str) -> str:
    value = value.replace("**", "").strip()
    value = re.sub(r"\s+", " ", value)
    return value


def semantic_value(value: str) -> str:
    value = css_value(value)
    if value.startswith("--"):
        return f"var({value})"
    return value


def penpot_reference(value: str) -> str:
    value = css_value(value)
    if value.startswith("--dt-primitive-"):
        return "{" + value.removeprefix("--dt-primitive-") + "}"
    return value


def penpot_token(value: Any, token_type: str, description: str = "") -> dict[str, Any]:
    return {"$value": value, "$type": token_type, "$description": description}


def penpot_semantic_name(token: str) -> str:
    name = token.removeprefix("--dt-")
    return name.removeprefix("color-")


def emit_table_tokens(rows: list[list[str]], value_index: int = 1) -> list[str]:
    output = []
    for row in rows:
        if len(row) > value_index and row[0].startswith("--"):
            output.append(f"  {row[0]}: {css_value(row[value_index])};")
    return output


def parse_font_families(tables) -> tuple[str, str, str, str]:
    rows = table_for(tables, "Familias Tipográficas", "Rol Tipográfico")
    primary_penpot, primary_css = "", ""
    mono_penpot, mono_css = "", ""
    for row in rows:
        role = row[0].lower()
        if "primaria" in role:
            primary_penpot = clean_cell(row[1])
            primary_css = clean_cell(row[2])
        elif "monoespaciada" in role:
            mono_penpot = clean_cell(row[1])
            mono_css = clean_cell(row[2])
    return primary_penpot, primary_css, mono_penpot, mono_css


def extract_font_weight(raw_weight: str) -> str:
    match = re.search(r"\(?(\d{3,4})\)?", raw_weight)
    if match:
        return match.group(1)
    cleaned = raw_weight.lower()
    mapping = {
        "regular": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700",
    }
    for key, val in mapping.items():
        if key in cleaned:
            return val
    return "400"


def generate(source: Path, target: Path, penpot_target: Path) -> None:
    text = source.read_text(encoding="utf-8")
    tables = markdown_tables(text)
    spacing = table_for(tables, "Escala de Espaciado", "Token CSS")
    controls = table_for(tables, "Dimensiones de Controles", "Token de Control")
    breakpoints = table_for(tables, "Puntos de Quiebre", "Token de Breakpoint")
    primitives = table_for(tables, "Tokens Primitivos", "Token Primitivo")
    semantic = table_for(tables, "Tokens Semánticos", "Token Semántico")
    alarms = table_for(tables, "Semántica de Alarmas", "Estado / Severidad")
    typography = table_for(tables, "Escala Tipográfica", "Token Tipográfico")
    radii = table_for(tables, "Radios de Borde", "Token")
    zindex = table_for(tables, "Capas y Niveles", "Token Z-Index")
    font_base_penpot, font_base_css, font_mono_penpot, font_mono_css = parse_font_families(tables)

    # 1. Generación de ui-ux/assets/tokens.css
    lines = [
        "/* GENERATED FILE - Do not edit manually.",
        f" * Source: {source.relative_to(ROOT)}",
        " * Regenerate with: python3 scripts/generate_design_tokens.py",
        " */",
        ":root {",
        "  /* Primitive palette */",
        *emit_table_tokens(primitives),
        "",
        "  /* Spacing */",
        *emit_table_tokens(spacing, 1),
        "",
        "  /* Controls and responsive layout */",
        "  --dt-touch-target-mobile: 48px;",
    ]

    for row in controls:
        if not row or not row[0].startswith("--"):
            continue
        token, height, width = row[:3]
        if token == "--dt-touch-target-mobile":
            continue
        lines.append(f"  {token}: {css_value(height)};")
        if width != "auto":
            lines.append(
                f"  {token.replace('--dt-control-height-', '--dt-control-width-')}: {css_value(width)};"
            )

    lines.extend(
        [
            "",
            *emit_table_tokens(breakpoints),
            "",
            "  /* Typography */",
            f"  --dt-font-family-base: {css_value(font_base_css)};",
            f"  --dt-font-family-mono: {css_value(font_mono_css)};",
        ]
    )
    for row in typography:
        if row and row[0].startswith("--"):
            token = row[0]
            px = css_value(row[1])
            lines.append(f"  {token}: {px};")

    lines.extend(
        [
            "",
            "  /* Border radii */",
            *emit_table_tokens(radii),
            "",
            "  /* Z-index */",
            *emit_table_tokens(zindex),
            "",
        ]
    )

    for row in semantic:
        if row and row[0].startswith("--"):
            token, dark, light = row[:3]
            lines.append(f"  {token}: {semantic_value(light)};")
    for row in alarms:
        if row and len(row) > 3 and row[1].startswith("--"):
            _, token, dark, light = row[:4]
            lines.append(f"  {token}: {semantic_value(light)};")
    lines.append("}")
    lines.extend(["", "/* Dark theme semantic tokens */", '[data-theme="dark"] {'])
    for row in semantic:
        if row and row[0].startswith("--"):
            token, dark, _ = row[:3]
            lines.append(f"  {token}: {semantic_value(dark)};")
    for row in alarms:
        if row and len(row) > 3 and row[1].startswith("--"):
            _, token, dark, _ = row[:4]
            lines.append(f"  {token}: {semantic_value(dark)};")
    lines.extend(["}", ""])

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generado: {target}")

    # 2. Generación de ui-ux/assets/tokens_penpot.json
    penpot: dict[str, Any] = {
        "Global": {},
        "Primitives": {},
        "Semantic-Dark": {},
        "Semantic-Light": {},
        "$themes": [
            {
                "id": "dark-mode",
                "name": "Dark Mode",
                "group": "",
                "description": "",
                "isSource": False,
                "selectedTokenSets": {
                    "Global": "enabled",
                    "Primitives": "enabled",
                    "Semantic-Dark": "enabled",
                },
            },
            {
                "id": "light-mode",
                "name": "Light Mode",
                "group": "",
                "description": "",
                "isSource": False,
                "selectedTokenSets": {
                    "Global": "enabled",
                    "Primitives": "enabled",
                    "Semantic-Light": "enabled",
                },
            },
        ],
        "$metadata": {
            "tokenSetOrder": [
                "Global",
                "Primitives",
                "Semantic-Dark",
                "Semantic-Light",
            ],
            "activeThemes": ["/Dark Mode"],
            "activeSets": ["Global", "Primitives", "Semantic-Dark"],
        },
    }

    # Dimensiones y Espaciados
    for row in spacing:
        if row and row[0].startswith("--dt-space-"):
            penpot["Global"][row[0].removeprefix("--dt-")] = penpot_token(
                css_value(row[1]), "dimension"
            )
    for row in controls:
        if row and row[0].startswith("--dt-"):
            penpot["Global"][row[0].removeprefix("--dt-")] = penpot_token(
                css_value(row[1]), "dimension"
            )
    for row in radii:
        if row and row[0].startswith("--dt-radius-"):
            penpot["Global"][row[0].removeprefix("--dt-")] = penpot_token(
                css_value(row[1]), "borderRadius"
            )

    # Tipografía Compuesta (Penpot W3C standard)
    for row in typography:
        if row and row[0].startswith("--dt-font-"):
            token_id = row[0].removeprefix("--dt-")
            size_px = css_value(row[1])
            line_height_px = css_value(row[3])
            weight_str = extract_font_weight(row[4])
            description = row[5].replace("**", "").strip() if len(row) > 5 else ""

            is_mono = "mono" in token_id
            family_name = font_mono_penpot if is_mono else font_base_penpot

            penpot["Global"][token_id] = {
                "$value": {
                    "fontFamilies": [family_name],
                    "fontSizes": size_px,
                    "fontWeights": weight_str,
                    "lineHeights": line_height_px,
                    "letterSpacing": "0px",
                    "textCase": "none",
                    "textDecoration": "none",
                },
                "$type": "typography",
                "$description": description,
            }

    # Primitivos de Color
    for row in primitives:
        if row and row[0].startswith("--dt-primitive-"):
            penpot["Primitives"][row[0].removeprefix("--dt-primitive-")] = penpot_token(
                css_value(row[1]), "color"
            )

    # Semánticos de Color
    for row in semantic:
        if row and row[0].startswith("--dt-"):
            token, dark, light = row[:3]
            name = penpot_semantic_name(token)
            penpot["Semantic-Dark"][name] = penpot_token(
                penpot_reference(dark), "color"
            )
            penpot["Semantic-Light"][name] = penpot_token(
                penpot_reference(light), "color"
            )
    for row in alarms:
        if row and len(row) > 3 and row[1].startswith("--dt-"):
            _, token, dark, light = row[:4]
            name = penpot_semantic_name(token)
            penpot["Semantic-Dark"][name] = penpot_token(
                penpot_reference(dark), "color"
            )
            penpot["Semantic-Light"][name] = penpot_token(
                penpot_reference(light), "color"
            )

    penpot_target.parent.mkdir(parents=True, exist_ok=True)
    penpot_target.write_text(json.dumps(penpot, indent=2) + "\n", encoding="utf-8")
    print(f"Generado: {penpot_target}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--penpot-target", type=Path, default=DEFAULT_PENPOT_TARGET)
    args = parser.parse_args()
    generate(args.source.resolve(), args.target.resolve(), args.penpot_target.resolve())


if __name__ == "__main__":
    main()
