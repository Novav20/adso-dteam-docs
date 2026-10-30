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
DEFAULT_PROTOTYPE_DIR = ROOT / "ui-ux" / "prototype" / "assets"
DEFAULT_PROTOTYPE_TARGET = DEFAULT_PROTOTYPE_DIR / "icons.svg"
DEFAULT_PROTOTYPE_DATA_JS = DEFAULT_PROTOTYPE_DIR / "icons-data.js"

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
    "icon-close": """
      <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="currentColor"/>
    """,
    "icon-chevron-left": """
      <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" fill="currentColor"/>
    """,
    "icon-chevron-right": """
      <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" fill="currentColor"/>
    """,
    "icon-chevron-down": """
      <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z" fill="currentColor"/>
    """,
    "icon-chevron-up": """
      <path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z" fill="currentColor"/>
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
        style = re.sub(r"fill\s*:\s*(?:#000000|#000|black);?", "fill: currentColor;", style)
        style = re.sub(r"stroke\s*:\s*(?:#000000|#000|black);?", "stroke: currentColor;", style)
        if style:
            elem.attrib["style"] = style
        else:
            elem.attrib.pop("style", None)

    if elem.attrib.get("fill") in ("#000000", "#000", "black"):
        elem.attrib["fill"] = "currentColor"

    if elem.attrib.get("stroke") in ("#000000", "#000", "black"):
        elem.attrib["stroke"] = "currentColor"

    # Default SVG shapes without explicit fill or stroke to currentColor (inherits parent CSS)
    tag_clean = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
    if tag_clean in ("path", "polygon", "rect", "circle", "ellipse"):
        style_str = elem.attrib.get("style", "")
        has_fill = ("fill" in elem.attrib) or bool(re.search(r"(?<!-)\bfill\s*:", style_str))
        has_stroke = ("stroke" in elem.attrib) or bool(re.search(r"(?<!-)\bstroke\s*:", style_str))
        if not has_fill and not has_stroke:
            elem.attrib["fill"] = "currentColor"

    for child in elem:
        clean_xml_element(child)


def build(source_dir: Path, target: Path, prototype_target: Path | None = None, prototype_data_js: Path | None = None) -> None:
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

    if prototype_data_js:
        import json
        js_content = (
            "/**\n"
            " * ICONS-DATA.JS\n"
            " * Inlines SVG icons sprite into document body.\n"
            " * Enables zero-CORS SVG icon rendering on local file:// URLs.\n"
            " * GENERATED FILE - Do not edit manually.\n"
            f" * Source: ui-ux/assets/icons-src/\n"
            " * Regenerate with: python3 scripts/build_icons_sprite.py\n"
            " */\n"
            "(function(global) {\n"
            '    "use strict";\n'
            f"    const spriteContent = {json.dumps(sprite_content)};\n\n"
            "    function injectSprite() {\n"
            "        if (document.getElementById('__dteam_inlined_sprite')) return;\n"
            "        const div = document.createElement('div');\n"
            "        div.id = '__dteam_inlined_sprite';\n"
            "        div.style.display = 'none';\n"
            "        div.innerHTML = spriteContent;\n"
            "        if (document.body) {\n"
            "            document.body.insertBefore(div, document.body.firstChild);\n"
            "        }\n"
            "    }\n\n"
            "    function remapUses() {\n"
            "        document.querySelectorAll('use').forEach(useEl => {\n"
            "            const href = useEl.getAttribute('href') || useEl.getAttribute('xlink:href');\n"
            "            if (href && href.startsWith('assets/icons.svg#')) {\n"
            "                useEl.setAttribute('href', href.replace('assets/icons.svg', ''));\n"
            "            }\n"
            "        });\n"
            "    }\n\n"
            "    if (document.readyState === 'loading') {\n"
            "        document.addEventListener('DOMContentLoaded', () => {\n"
            "            injectSprite();\n"
            "            remapUses();\n"
            "        });\n"
            "    }\n"
            "    injectSprite();\n"
            "})(typeof window !== 'undefined' ? window : this);\n"
        )
        prototype_data_js.parent.mkdir(parents=True, exist_ok=True)
        prototype_data_js.write_text(js_content, encoding="utf-8")
        print(f"Synced to prototype data JS: {prototype_data_js}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--target", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--prototype-target", type=Path, default=DEFAULT_PROTOTYPE_TARGET)
    parser.add_argument("--prototype-data-js", type=Path, default=DEFAULT_PROTOTYPE_DATA_JS)
    parser.add_argument(
        "--target-prototype-dir",
        type=Path,
        default=None,
        help="Directory receiving the prototype icons.svg and icons-data.js outputs.",
    )
    args = parser.parse_args()
    prototype_target = args.prototype_target
    prototype_data_js = args.prototype_data_js
    if args.target_prototype_dir is not None:
        prototype_dir = args.target_prototype_dir.resolve()
        prototype_target = prototype_dir / "icons.svg"
        prototype_data_js = prototype_dir / "icons-data.js"
    build(args.source_dir.resolve(), args.target.resolve(), prototype_target.resolve(), prototype_data_js.resolve())


if __name__ == "__main__":
    main()
