"""
Single-pass Markdown parser with exact GFM anchor slugging, frontmatter parsing,
tables, relative links, wikilinks, section numbers, Mermaid blocks, and LaTeX math spans.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote


@dataclass(frozen=True, slots=True)
class MarkdownHeading:
    level: int
    text: str
    slug: str
    line: int
    section_number: str | None = None


@dataclass(frozen=True, slots=True)
class SectionNumberEntry:
    level: int
    number: str
    parts: tuple[int, ...]
    title: str
    line: int


@dataclass(frozen=True, slots=True)
class MarkdownTable:
    heading: str
    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]
    start_line: int
    end_line: int


@dataclass(frozen=True, slots=True)
class MarkdownLink:
    label: str
    url: str
    target_path: str
    anchor: str | None
    is_image: bool
    is_external: bool
    line: int


@dataclass(frozen=True, slots=True)
class WikilinkRef:
    raw: str
    target: str
    line: int


@dataclass(frozen=True, slots=True)
class CodeBlock:
    language: str
    content: str
    start_line: int
    end_line: int


@dataclass(frozen=True, slots=True)
class MermaidBlock:
    diagram_type: str
    content: str
    start_line: int
    end_line: int


@dataclass(frozen=True, slots=True)
class LatexSpan:
    content: str
    is_display: bool
    line: int


@dataclass(frozen=True, slots=True)
class ParsedMarkdownDoc:
    rel_path: str
    abs_path: Path
    raw_text: str
    frontmatter_raw: str | None
    frontmatter: dict[str, Any]
    frontmatter_line_count: int
    headings: tuple[MarkdownHeading, ...]
    anchors: frozenset[str]
    section_numbers: tuple[SectionNumberEntry, ...]
    tables: tuple[MarkdownTable, ...]
    links: tuple[MarkdownLink, ...]
    frontmatter_wikilinks: tuple[WikilinkRef, ...]
    body_wikilinks: tuple[WikilinkRef, ...]
    code_blocks: tuple[CodeBlock, ...]
    mermaid_blocks: tuple[MermaidBlock, ...]
    latex_spans: tuple[LatexSpan, ...]


_WIKILINK_RE = re.compile(r"(!?\[\[(.*?)\]\])")
_MD_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)]+)\)")
_EXTERNAL_URL_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_SEC_NUM_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$")
_FENCE_OPEN_RE = re.compile(r"^(`{3,}|~{3,})\s*([A-Za-z0-9_+#.-]*)\s*$")
_TABLE_SEP_RE = re.compile(r"^\|?(?:\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*$")


def gfm_slug(text: str) -> str:
    """
    Generate a GitHub Flavored Markdown (GFM) anchor slug from heading text.

    Matches `scripts/verify_markdown_links.py` slug rules:
    - Strip markdown links and images keeping label/alt text
    - Protect inline backtick spans before stripping HTML tags
    - Strip asterisk bold/italics and strikethrough
    - Lowercase, strip punctuation outside [\\w\\s-], replace whitespace runs with '-'
    """
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    code_spans: list[str] = []

    def _save_code(match: re.Match[str]) -> str:
        code_spans.append(match.group(1))
        return f"__CODE_SPAN_{len(code_spans) - 1}__"

    text = re.sub(r"`([^`]+)`", _save_code, text)
    text = re.sub(r"<[^>]+>", "", text)
    for idx, val in enumerate(code_spans):
        text = text.replace(f"__CODE_SPAN_{idx}__", val)
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"~~([^~]+)~~", r"\1", text)
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text).strip()
    text = re.sub(r"[\s]+", "-", text)
    return text


def _strip_yaml_scalar(value: str) -> Any:
    v = value.strip()
    if not v:
        return ""
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    low = v.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "~"):
        return None
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        return [_strip_yaml_scalar(item) for item in inner.split(",")]
    if re.fullmatch(r"-?\d+", v):
        try:
            return int(v)
        except ValueError:
            return v
    return v


def _parse_frontmatter_yaml(fm_raw: str) -> dict[str, Any]:
    """Parse the constrained YAML frontmatter subset used in repository Markdown files."""
    result: dict[str, Any] = {}
    current_list_key: str | None = None
    current_dict_key: str | None = None

    for line in fm_raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        if stripped.startswith("- "):
            item_val = _strip_yaml_scalar(stripped[2:])
            target_key = current_list_key or current_dict_key
            if target_key is not None:
                existing = result.get(target_key)
                if isinstance(existing, list):
                    existing.append(item_val)
                else:
                    result[target_key] = [item_val]
            continue

        key_match = re.match(r"^([A-Za-z0-9_.-]+)\s*:\s*(.*)$", stripped)
        if not key_match:
            continue
        key = key_match.group(1)
        val_raw = key_match.group(2).strip()

        if indent > 0 and current_dict_key and isinstance(result.get(current_dict_key), dict):
            result[current_dict_key][key] = _strip_yaml_scalar(val_raw)
            current_list_key = None
            continue

        if val_raw == "":
            result[key] = []
            current_list_key = key
            current_dict_key = key
        else:
            result[key] = _strip_yaml_scalar(val_raw)
            current_list_key = None
            current_dict_key = None

    return result


def _split_frontmatter(raw_text: str) -> tuple[str | None, str, int]:
    """Return `(frontmatter_raw, body_text, body_start_line_1based)`."""
    if not raw_text.startswith("---"):
        return None, raw_text, 1
    lines = raw_text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, raw_text, 1
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            fm_raw = "".join(lines[1:idx])
            body_text = "".join(lines[idx + 1 :])
            return fm_raw, body_text, idx + 2
    return None, raw_text, 1


def _blank_inline_code(line: str) -> str:
    """Replace inline code spans with spaces of equal length to preserve line/col positions."""
    return re.sub(r"`[^`\n]+`", lambda m: " " * len(m.group(0)), line)


def _split_table_row(line: str) -> tuple[str, ...]:
    trimmed = line.strip()
    if trimmed.startswith("|"):
        trimmed = trimmed[1:]
    if trimmed.endswith("|"):
        trimmed = trimmed[:-1]
    return tuple(cell.strip() for cell in trimmed.split("|"))


def _detect_mermaid_type(content: str) -> str:
    for line in content.splitlines():
        s = line.strip()
        if not s or s.startswith("%%"):
            continue
        return s.split()[0]
    return "unknown"


def _extract_latex_spans(body_lines: list[str], body_start_line: int, fenced_mask: list[bool]) -> tuple[LatexSpan, ...]:
    """Extract display (`$$...$$`) and inline (`$...$`) LaTeX math spans outside code."""
    spans: list[LatexSpan] = []

    # Build a line-aligned string where fenced code lines and inline code spans are masked
    masked_lines: list[str] = []
    for i, line in enumerate(body_lines):
        if fenced_mask[i]:
            masked_lines.append("")
        else:
            masked_lines.append(_blank_inline_code(line))

    text = "\n".join(masked_lines)
    # Remove escaped dollars (`\$`) so they do not pair as math delimiters
    scan_text = re.sub(r"\\\$", "  ", text)

    # 1. Display math $$...$$
    occupied: list[tuple[int, int]] = []
    for m in re.finditer(r"\$\$(.+?)\$\$", scan_text, re.DOTALL):
        start, end = m.span()
        occupied.append((start, end))
        line_no = body_start_line + scan_text[:start].count("\n")
        spans.append(LatexSpan(content=text[start + 2 : end - 2].strip(), is_display=True, line=line_no))

    # Mask occupied display-math ranges before inline scanning
    chars = list(scan_text)
    for start, end in occupied:
        for idx in range(start, end):
            if chars[idx] != "\n":
                chars[idx] = " "
    inline_text = "".join(chars)

    # 2. Inline math $...$ (single line, no leading/trailing space right inside delimiters)
    for offset, line in enumerate(inline_text.splitlines()):
        line_no = body_start_line + offset
        for m in re.finditer(r"(?<!\$)\$(?!\s|\$)([^$\n]+?)(?<!\s)\$(?!\d|\$)", line):
            inner = m.group(1).strip()
            if inner:
                spans.append(LatexSpan(content=inner, is_display=False, line=line_no))

    return tuple(spans)


def parse_markdown_text(rel_path: str, abs_path: Path, raw_text: str) -> ParsedMarkdownDoc:
    """Parse already-loaded Markdown text into a `ParsedMarkdownDoc`."""
    fm_raw, body_text, body_start_line = _split_frontmatter(raw_text)
    frontmatter = _parse_frontmatter_yaml(fm_raw) if fm_raw is not None else {}
    fm_line_count = body_start_line - 1

    fm_wikilinks: list[WikilinkRef] = []
    if fm_raw is not None:
        for wm in _WIKILINK_RE.finditer(fm_raw):
            line_no = 2 + fm_raw[: wm.start()].count("\n")
            fm_wikilinks.append(WikilinkRef(raw=wm.group(1), target=wm.group(2).strip(), line=line_no))

    body_lines = body_text.splitlines()
    fenced_mask = [False] * len(body_lines)
    code_blocks: list[CodeBlock] = []
    mermaid_blocks: list[MermaidBlock] = []

    in_fence = False
    fence_char = ""
    fence_len = 0
    fence_lang = ""
    fence_start_idx = 0
    fence_buf: list[str] = []

    for idx, line in enumerate(body_lines):
        stripped = line.strip()
        if not in_fence:
            m_open = _FENCE_OPEN_RE.match(stripped)
            if m_open:
                in_fence = True
                fence_char = m_open.group(1)[0]
                fence_len = len(m_open.group(1))
                fence_lang = m_open.group(2).strip().lower()
                fence_start_idx = idx
                fence_buf = []
                fenced_mask[idx] = True
        else:
            fenced_mask[idx] = True
            if stripped.startswith(fence_char * fence_len) and stripped.replace(fence_char, "") == "":
                content = "\n".join(fence_buf)
                start_line = body_start_line + fence_start_idx
                end_line = body_start_line + idx
                code_blocks.append(
                    CodeBlock(
                        language=fence_lang,
                        content=content,
                        start_line=start_line,
                        end_line=end_line,
                    )
                )
                if fence_lang == "mermaid":
                    mermaid_blocks.append(
                        MermaidBlock(
                            diagram_type=_detect_mermaid_type(content),
                            content=content,
                            start_line=start_line,
                            end_line=end_line,
                        )
                    )
                in_fence = False
                fence_buf = []
            else:
                fence_buf.append(line)

    if in_fence:
        content = "\n".join(fence_buf)
        start_line = body_start_line + fence_start_idx
        end_line = body_start_line + len(body_lines) - 1
        code_blocks.append(
            CodeBlock(
                language=fence_lang,
                content=content,
                start_line=start_line,
                end_line=end_line,
            )
        )
        if fence_lang == "mermaid":
            mermaid_blocks.append(
                MermaidBlock(
                    diagram_type=_detect_mermaid_type(content),
                    content=content,
                    start_line=start_line,
                    end_line=end_line,
                )
            )

    headings: list[MarkdownHeading] = []
    anchors_ordered: list[str] = []
    slug_counts: dict[str, int] = {}
    section_numbers: list[SectionNumberEntry] = []
    tables: list[MarkdownTable] = []
    links: list[MarkdownLink] = []
    body_wikilinks: list[WikilinkRef] = []

    current_heading_title = ""
    i = 0
    total_lines = len(body_lines)
    while i < total_lines:
        if fenced_mask[i]:
            i += 1
            continue

        line = body_lines[i]
        file_line = body_start_line + i
        stripped = line.strip()

        # Headings
        hm = _HEADING_RE.match(stripped)
        if hm:
            level = len(hm.group(1))
            raw_title = hm.group(2).strip()
            current_heading_title = raw_title
            slug = gfm_slug(raw_title)
            final_slug = slug
            if slug:
                if slug in slug_counts:
                    slug_counts[slug] += 1
                    final_slug = f"{slug}-{slug_counts[slug]}"
                else:
                    slug_counts[slug] = 0
                    final_slug = slug
                anchors_ordered.append(final_slug)

            sec_num: str | None = None
            sm = _SEC_NUM_RE.match(raw_title)
            if sm:
                sec_num = sm.group(1)
                parts = tuple(int(p) for p in sec_num.split("."))
                section_numbers.append(
                    SectionNumberEntry(
                        level=level,
                        number=sec_num,
                        parts=parts,
                        title=sm.group(2).strip(),
                        line=file_line,
                    )
                )

            headings.append(
                MarkdownHeading(
                    level=level,
                    text=raw_title,
                    slug=final_slug,
                    line=file_line,
                    section_number=sec_num,
                )
            )
            i += 1
            continue

        # Markdown pipe tables
        if (
            stripped.startswith("|")
            and i + 1 < total_lines
            and not fenced_mask[i + 1]
            and _TABLE_SEP_RE.match(body_lines[i + 1].strip())
        ):
            headers = _split_table_row(stripped)
            table_start = file_line
            rows: list[tuple[str, ...]] = []
            j = i + 2
            while j < total_lines and not fenced_mask[j] and body_lines[j].strip().startswith("|"):
                rows.append(_split_table_row(body_lines[j].strip()))
                j += 1
            table_end = body_start_line + j - 1
            tables.append(
                MarkdownTable(
                    heading=current_heading_title,
                    headers=headers,
                    rows=tuple(rows),
                    start_line=table_start,
                    end_line=table_end,
                )
            )
            # Still scan table cells for links and wikilinks
            for row_idx in range(i, j):
                row_clean = _blank_inline_code(body_lines[row_idx])
                row_line_no = body_start_line + row_idx
                for wm in _WIKILINK_RE.finditer(row_clean):
                    body_wikilinks.append(
                        WikilinkRef(raw=wm.group(1), target=wm.group(2).strip(), line=row_line_no)
                    )
                for lm in _MD_LINK_RE.finditer(row_clean):
                    is_img = lm.group(1) == "!"
                    label = lm.group(2)
                    url = lm.group(3).strip()
                    is_ext = bool(
                        _EXTERNAL_URL_RE.match(url)
                        or url.startswith("mailto:")
                        or url.startswith("tel:")
                    )
                    if "#" in url and not is_ext:
                        t_path, anchor = url.split("#", 1)
                    else:
                        t_path, anchor = url, None
                    links.append(
                        MarkdownLink(
                            label=label,
                            url=url,
                            target_path=unquote(t_path),
                            anchor=anchor.lower() if anchor else None,
                            is_image=is_img,
                            is_external=is_ext,
                            line=row_line_no,
                        )
                    )
            i = j
            continue

        # Standard prose line: scan for wikilinks and markdown links outside inline code
        clean_line = _blank_inline_code(line)
        for wm in _WIKILINK_RE.finditer(clean_line):
            body_wikilinks.append(
                WikilinkRef(raw=wm.group(1), target=wm.group(2).strip(), line=file_line)
            )
        for lm in _MD_LINK_RE.finditer(clean_line):
            is_img = lm.group(1) == "!"
            label = lm.group(2)
            url = lm.group(3).strip()
            is_ext = bool(
                _EXTERNAL_URL_RE.match(url)
                or url.startswith("mailto:")
                or url.startswith("tel:")
            )
            if "#" in url and not is_ext:
                t_path, anchor = url.split("#", 1)
            else:
                t_path, anchor = url, None
            links.append(
                MarkdownLink(
                    label=label,
                    url=url,
                    target_path=unquote(t_path),
                    anchor=anchor.lower() if anchor else None,
                    is_image=is_img,
                    is_external=is_ext,
                    line=file_line,
                )
            )

        i += 1

    latex_spans = _extract_latex_spans(body_lines, body_start_line, fenced_mask)

    return ParsedMarkdownDoc(
        rel_path=rel_path,
        abs_path=abs_path,
        raw_text=raw_text,
        frontmatter_raw=fm_raw,
        frontmatter=frontmatter,
        frontmatter_line_count=fm_line_count,
        headings=tuple(headings),
        anchors=frozenset(anchors_ordered),
        section_numbers=tuple(section_numbers),
        tables=tuple(tables),
        links=tuple(links),
        frontmatter_wikilinks=tuple(fm_wikilinks),
        body_wikilinks=tuple(body_wikilinks),
        code_blocks=tuple(code_blocks),
        mermaid_blocks=tuple(mermaid_blocks),
        latex_spans=latex_spans,
    )
