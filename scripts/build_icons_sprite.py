#!/usr/bin/env python3
"""
build_icons_sprite.py
=====================
Docs-as-Code build pipeline for SVG icons.
Traverses authoring icon sources (ui-ux/assets/icons-src/) and compiles them
into a zero-dependency, theme-decoupled SVG symbol sprite sheet (ui-ux/assets/icons.svg).

Standard: DT-UI-DS-DOC-001 v1.8 (Section 6.4)
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = ROOT / "ui-ux" / "assets" / "icons-src"
DEFAULT_TARGET = ROOT / "ui-ux" / "assets" / "icons.svg"
DEFAULT_PROTOTYPE_TARGET = ROOT / "ui-ux" / "temp" / "ui-prototype" / "assets" / "icons.svg"

# Built-in fallback UI & Navigation symbols if not overridden in icons-src
DEFAULT_UI_SYMBOLS = {
    "icon-search": """
      <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/>
      <line x1="16.5" y1="16.5" x2="21" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    """,
    "icon-layers": """
      <polygon points="12,2 2,7 12,12 22,7" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
      <polyline points="2,12 12,17 22,12" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
      <polyline points="2,17 12,22 22,17" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
    """,
    "icon-zoom-in": """
      <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/>
      <line x1="11" y1="8" x2="11" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="8" y1="11" x2="14" y2="11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="16.5" y1="16.5" x2="21" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    """,
    "icon-zoom-out": """
      <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/>
      <line x1="8" y1="11" x2="14" y2="11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <line x1="16.5" y1="16.5" x2="21" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    """,
    "icon-home": """
      <path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
    """,
    "icon-wifi-off": """
      <line x1="2" y1="2" x2="22" y2="22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M8.5 16.5a5 5 0 0 1 7 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M4.93 12.93a10 10 0 0 1 3.57-2.36" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M12 20h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    """,
}


def clean_xml_element(elem: ET.Element) -> None:
    """Strip editor-specific namespaces, attributes, and hidden display styles."""
    attribs_to_remove = [
        k for k in elem.attrib
        if k.startswith("{") or k.startswith("sodipodi:") or k.startswith("inkscape:")
    ]
    for attr in attribs_to_remove:
        elem.attrib.pop(attr, None)

    if "style" in elem.attrib:
        style = elem.attrib["style"]
        style = re.sub(r"display\s*:\s*[^;]+;?", "", style).strip()
        style = re.sub(r"fill\s*:\s*#000000;?", "fill: currentColor;", style)
        if style:
            elem.attrib["style"] = style
        else:
            elem.attrib.pop("style", None)

    if elem.attrib.get("fill") == "#000000":
        elem.attrib["fill"] = "currentColor"

    for child in elem:
        clean_xml_element(child)


def build(source_dir: Path, target: Path, prototype_target: Path | None = None) -> None:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    extracted_symbols: dict[str, str] = {}

    # Traverse all SVG files in source directory
    svg_files = sorted(source_dir.glob("*.svg"))
    print(f"Scanning {source_dir} ({len(svg_files)} files found)...")

    for svg_path in svg_files:
        content = svg_path.read_text(encoding="utf-8")
        content_clean = re.sub(r'\sxmlns="[^"]+"', '', content, count=1)
        try:
            root = ET.fromstring(content_clean)
        except ET.ParseError as err:
            print(f"  [WARN] Skipping invalid XML {svg_path.name}: {err}")
            continue

        found_groups = False
        # 1. Check if the file has multi-icon groups (id="icon-*" or inkscape:label="icon-*")
        for group in root.findall(".//g"):
            group_id = group.attrib.get("id", "")
            label = ""
            for k, v in group.attrib.items():
                if "label" in k.lower():
                    label = v
                    break

            symbol_id = ""
            if label.startswith("icon-"):
                symbol_id = label
            elif group_id.startswith("icon-"):
                symbol_id = group_id

            if symbol_id:
                clean_xml_element(group)
                group.attrib["id"] = symbol_id
                inner_xml = ET.tostring(group, encoding="unicode").strip()
                extracted_symbols[symbol_id] = (
                    f'  <symbol id="{symbol_id}" viewBox="0 0 24 24">\n    {inner_xml}\n  </symbol>'
                )
                found_groups = True

        # 2. If no inner 'icon-*' groups found, treat the entire standalone SVG as one symbol
        if not found_groups:
            symbol_id = svg_path.stem
            if not symbol_id.startswith("icon-"):
                symbol_id = f"icon-{symbol_id}"

            clean_xml_element(root)
            inner_content = "".join(ET.tostring(child, encoding="unicode") for child in root).strip()
            viewbox = root.attrib.get("viewBox", "0 0 24 24")
            extracted_symbols[symbol_id] = (
                f'  <symbol id="{symbol_id}" viewBox="{viewbox}">\n    {inner_content}\n  </symbol>'
            )

    # 3. Add default UI symbols if not overridden
    for symbol_id, inner_xml in DEFAULT_UI_SYMBOLS.items():
        if symbol_id not in extracted_symbols:
            extracted_symbols[symbol_id] = (
                f'  <symbol id="{symbol_id}" viewBox="0 0 24 24">\n{inner_xml.strip()}\n  </symbol>'
            )

    # Compose final SVG sprite
    sprite_content = (
        '<svg xmlns="http://www.w3.org/2000/svg" style="display: none;">\n'
        '  <!--\n'
        '    DTEAM Centralized Iconography Sprite Sheet\n'
        '    Standard: DT-UI-DS-DOC-001 v1.8 (Section 6.4)\n'
        '    GENERATED FILE - Do not edit manually.\n'
        f'    Source: {source_dir.relative_to(ROOT)}/\n'
        '    Regenerate with: python3 scripts/build_icons_sprite.py\n'
        '  -->\n\n'
        + "\n\n".join(extracted_symbols.values())
        + "\n</svg>\n"
    )

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(sprite_content, encoding="utf-8")
    print(f"Generated: {target} ({len(extracted_symbols)} symbols total)")

    if prototype_target:
        prototype_target.parent.mkdir(parents=True, exist_ok=True)
        prototype_target.write_text(sprite_content, encoding="utf-8")
        print(f"Synced to prototype: {prototype_target}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--prototype-target", type=Path, default=DEFAULT_PROTOTYPE_TARGET)
    args = parser.parse_args()
    build(args.source_dir.resolve(), args.target.resolve(), args.prototype_target.resolve())


if __name__ == "__main__":
    main()
