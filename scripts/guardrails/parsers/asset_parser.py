"""
Parsers for UI tokens (`tokens.css`), SVG icon sprites (`icons.svg`),
prototype `.html`/`.css`/`.js` files, and requirements CSV tables (`requirements/data/*.csv`).
"""

from __future__ import annotations

import csv
import io
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TokensModel:
    light_tokens: dict[str, str]
    dark_tokens: dict[str, str]
    all_tokens: frozenset[str]
    duplicate_light: tuple[str, ...]
    duplicate_dark: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class IconsModel:
    symbol_ids: frozenset[str]
    duplicate_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PrototypeAsset:
    rel_path: str
    kind: str  # "html" | "css" | "js"
    content: str
    referenced_tokens: tuple[str, ...]
    referenced_icons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CsvTable:
    rel_path: str
    headers: tuple[str, ...]
    rows: tuple[dict[str, str], ...]


_CSS_DECL_RE = re.compile(r"(--dt-[a-z0-9-]+)\s*:\s*([^;]+);")
_TOKEN_REF_RE = re.compile(r"--dt-[a-z0-9-]+")
_ICON_REF_RE = re.compile(r"#(icon-[a-z0-9-]+)\b")


def parse_tokens_css(css_text: str) -> TokensModel:
    """Parse `:root` (light/shared) and `[data-theme="dark"]` tokens from `tokens.css`."""
    light_tokens: dict[str, str] = {}
    dark_tokens: dict[str, str] = {}
    dup_light: list[str] = []
    dup_dark: list[str] = []

    # Remove CSS block comments before block scanning
    clean_css = re.sub(r"/\*.*?\*/", "", css_text, flags=re.DOTALL)

    # Track selector scopes while recognizing @media responsive overrides
    # Primary base blocks: top-level `:root { ... }` and `[data-theme="dark"] { ... }`
    in_media = False
    media_depth = 0
    current_target: str | None = None  # "light" | "dark"
    target_depth = 0
    brace_depth = 0

    for raw_line in clean_css.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("@media") and "{" in line:
            in_media = True
            media_depth = brace_depth + line.count("{") - line.count("}")
            brace_depth = media_depth
            continue

        if current_target is None:
            if line.startswith(":root") and "{" in line:
                current_target = "light"
                brace_depth += line.count("{") - line.count("}")
                target_depth = brace_depth
                continue
            if '[data-theme="dark"]' in line and "{" in line:
                current_target = "dark"
                brace_depth += line.count("{") - line.count("}")
                target_depth = brace_depth
                continue

        brace_depth += line.count("{") - line.count("}")

        if current_target is not None:
            for m in _CSS_DECL_RE.finditer(line):
                key, val = m.group(1), m.group(2).strip()
                if current_target == "light":
                    if key in light_tokens and not in_media and key not in dup_light:
                        dup_light.append(key)
                    light_tokens[key] = val
                else:
                    if key in dark_tokens and not in_media and key not in dup_dark:
                        dup_dark.append(key)
                    dark_tokens[key] = val

            if brace_depth < target_depth:
                current_target = None

        if in_media and brace_depth < media_depth:
            in_media = False

    # Fallback regex pass if custom formatting bypassed line scanner
    if not light_tokens and not dark_tokens:
        for m in _CSS_DECL_RE.finditer(clean_css):
            light_tokens[m.group(1)] = m.group(2).strip()

    all_tokens = frozenset(light_tokens.keys()) | frozenset(dark_tokens.keys())
    return TokensModel(
        light_tokens=light_tokens,
        dark_tokens=dark_tokens,
        all_tokens=all_tokens,
        duplicate_light=tuple(dup_light),
        duplicate_dark=tuple(dup_dark),
    )


def parse_icons_svg(svg_text: str) -> IconsModel:
    """Parse `<symbol id="icon-...">` definitions from `ui-ux/assets/icons.svg`."""
    ids: list[str] = []
    seen: set[str] = set()
    dups: list[str] = []

    try:
        root = ET.fromstring(svg_text)
        for elem in root.iter():
            local_tag = elem.tag.rsplit("}", 1)[-1]
            if local_tag == "symbol":
                sym_id = elem.attrib.get("id", "").strip()
                if sym_id:
                    if sym_id in seen and sym_id not in dups:
                        dups.append(sym_id)
                    seen.add(sym_id)
                    ids.append(sym_id)
    except ET.ParseError:
        for sym_id in re.findall(r'<symbol[^>]*\bid=["\']([^"\']+)["\']', svg_text):
            if sym_id in seen and sym_id not in dups:
                dups.append(sym_id)
            seen.add(sym_id)
            ids.append(sym_id)

    return IconsModel(symbol_ids=frozenset(ids), duplicate_ids=tuple(dups))


def parse_prototype_asset(rel_path: str, text: str) -> PrototypeAsset:
    """Parse a `.html`, `.css`, or `.js` prototype asset."""
    ext = rel_path.rsplit(".", 1)[-1].lower()
    kind = ext if ext in ("html", "css", "js") else "other"
    tokens = tuple(dict.fromkeys(_TOKEN_REF_RE.findall(text)))
    icons = tuple(dict.fromkeys(_ICON_REF_RE.findall(text)))
    return PrototypeAsset(
        rel_path=rel_path,
        kind=kind,
        content=text,
        referenced_tokens=tokens,
        referenced_icons=icons,
    )


def parse_csv_table(rel_path: str, text: str) -> CsvTable:
    """Parse a UTF-8 CSV file using Python stdlib `csv.DictReader`."""
    stream = io.StringIO(text.lstrip("\ufeff"), newline="")
    reader = csv.DictReader(stream)
    headers = tuple(reader.fieldnames or ())
    rows = tuple(dict(row) for row in reader)
    return CsvTable(rel_path=rel_path, headers=headers, rows=rows)
