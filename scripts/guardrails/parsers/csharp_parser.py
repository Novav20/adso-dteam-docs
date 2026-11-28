"""
C# and Razor contract parser for fenced code blocks in SCR-*.md, DT-UI-CTR-001.md,
and DT-ARQ-CMP-DOC-001.md.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .markdown_parser import CodeBlock, MarkdownHeading, ParsedMarkdownDoc

_CSHARP_LANGS = frozenset({"csharp", "c#", "cs", "razor"})

_TYPE_DECL_RE = re.compile(
    r"^\s*(?P<mods>(?:public|internal|private|protected|sealed|abstract|partial|readonly|static)\s+)*"
    r"(?P<kind>record(?:\s+struct|\s+class)?|class|struct|interface)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*(?:<[^>]+>)?)"
    r"(?:\s*\((?P<pos_params>[^)]*)\))?"
    r"(?:\s*:\s*(?P<bases>[^{;]+?))?"
    r"\s*(?P<opener>\{|;)",
)

_ENUM_DECL_RE = re.compile(
    r"^\s*(?:public|internal|private|protected)?\s*enum\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\{",
)

_PROP_RE = re.compile(
    r"^(?:(?:public|internal|private|protected|new|virtual|override|abstract|sealed|static)\s+)*"
    r"(?:(?P<req>required)\s+)?"
    r"(?P<type>[A-Za-z_][A-Za-z0-9_<>,\.\?\s\[\]]+?)\s+"
    r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*"
    r"(?:\{(?P<acc>[^}]*)\}|=>\s*(?P<expr>[^;]+);)\s*"
    r"(?:=\s*(?P<default>[^;]+);)?$"
)

_RAZOR_MARKER_RE = re.compile(r"//\s*(?:CMP-\d+\s*:|[^:\n]*:)?\s*([A-Za-z0-9_]+\.razor)\b")
_HEADING_RAZOR_RE = re.compile(r"([A-Za-z0-9_]+\.razor)")
_ATTR_LINE_RE = re.compile(r"^\[([^\]]+)\]\s*(.*)$")


@dataclass(frozen=True, slots=True)
class CSharpProp:
    name: str
    type_name: str
    is_required: bool
    is_nullable: bool
    default_value: str | None = None
    attributes: tuple[str, ...] = ()
    line: int = 0


@dataclass(frozen=True, slots=True)
class CSharpRecord:
    name: str
    kind: str
    base_types: tuple[str, ...]
    properties: tuple[CSharpProp, ...]
    file: str
    line: int


@dataclass(frozen=True, slots=True)
class CSharpEnum:
    name: str
    members: tuple[str, ...]
    file: str
    line: int


@dataclass(frozen=True, slots=True)
class RazorContract:
    component_name: str | None
    parameters: tuple[CSharpProp, ...]
    file: str
    start_line: int
    heading: str | None = None


def _is_nullable_type(type_name: str) -> bool:
    return type_name.strip().endswith("?")


def _clean_type_name(type_name: str) -> str:
    return re.sub(r"\s+", " ", type_name).strip()


def _split_top_level(text: str, sep: str = ",") -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    angle = 0
    paren = 0
    bracket = 0
    in_str: str | None = None
    escape = False
    for ch in text:
        if escape:
            buf.append(ch)
            escape = False
            continue
        if ch == "\\" and in_str is not None:
            buf.append(ch)
            escape = True
            continue
        if in_str is not None:
            buf.append(ch)
            if ch == in_str:
                in_str = None
            continue
        if ch in ('"', "'"):
            in_str = ch
            buf.append(ch)
            continue
        if ch == "<":
            angle += 1
        elif ch == ">":
            angle = max(0, angle - 1)
        elif ch == "(":
            paren += 1
        elif ch == ")":
            paren = max(0, paren - 1)
        elif ch == "[":
            bracket += 1
        elif ch == "]":
            bracket = max(0, bracket - 1)
        elif ch == sep and angle == 0 and paren == 0 and bracket == 0:
            item = "".join(buf).strip()
            if item:
                parts.append(item)
            buf = []
            continue
        buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)
    return parts


def _closest_heading(headings: tuple[MarkdownHeading, ...], line_no: int) -> MarkdownHeading | None:
    best: MarkdownHeading | None = None
    for h in headings:
        if h.line <= line_no:
            best = h
        else:
            break
    return best


def _extract_razor_from_heading(heading: MarkdownHeading | None) -> str | None:
    if heading is None:
        return None
    m = _HEADING_RAZOR_RE.search(heading.text)
    return m.group(1) if m else None


def _parse_property_line(
    raw_stmt: str,
    attrs: tuple[str, ...],
    line_no: int,
) -> CSharpProp | None:
    stmt = re.sub(r"\s+", " ", raw_stmt).strip()
    if not stmt:
        return None

    m = _PROP_RE.match(stmt)
    if not m:
        return None

    type_name = _clean_type_name(m.group("type"))
    # Avoid matching method declarations or variable assignments
    if "(" in type_name:
        return None

    is_req = bool(m.group("req")) or any("EditorRequired" in a for a in attrs)
    default_val = m.group("default").strip() if m.group("default") else None
    return CSharpProp(
        name=m.group("name"),
        type_name=type_name,
        is_required=is_req,
        is_nullable=_is_nullable_type(type_name),
        default_value=default_val,
        attributes=attrs,
        line=line_no,
    )


def _parse_positional_params(pos_params: str, line_no: int) -> tuple[CSharpProp, ...]:
    props: list[CSharpProp] = []
    for raw_param in _split_top_level(pos_params):
        cleaned = re.sub(r"\[[^\]]+\]\s*", "", raw_param).strip()
        default_val: str | None = None
        if "=" in cleaned:
            left, right = cleaned.split("=", 1)
            cleaned = left.strip()
            default_val = right.strip()
        parts = cleaned.rsplit(" ", 1)
        if len(parts) != 2:
            continue
        t_name = _clean_type_name(parts[0])
        p_name = parts[1].strip()
        props.append(
            CSharpProp(
                name=p_name,
                type_name=t_name,
                is_required=(default_val is None and not _is_nullable_type(t_name)),
                is_nullable=_is_nullable_type(t_name),
                default_value=default_val,
                attributes=(),
                line=line_no,
            )
        )
    return tuple(props)


def _strip_inline_comment(line: str) -> str:
    """Strip single-line `//` comment outside string literals."""
    in_str: str | None = None
    escape = False
    for idx, ch in enumerate(line):
        if escape:
            escape = False
            continue
        if ch == "\\" and in_str is not None:
            escape = True
            continue
        if in_str is not None:
            if ch == in_str:
                in_str = None
            continue
        if ch in ('"', "'"):
            in_str = ch
            continue
        if ch == "/" and idx + 1 < len(line) and line[idx + 1] == "/":
            return line[:idx]
    return line


def _extract_brace_block(lines: list[str], start_idx: int) -> tuple[list[tuple[int, str]], int]:
    """Collect `(line_offset, text)` inside `{ ... }` starting from `start_idx`."""
    depth = 0
    started = False
    collected: list[tuple[int, str]] = []
    idx = start_idx
    while idx < len(lines):
        code = _strip_inline_comment(lines[idx])
        for ch in code:
            if ch == "{":
                depth += 1
                started = True
            elif ch == "}":
                depth -= 1
        collected.append((idx, code))
        if started and depth <= 0:
            return collected, idx + 1
        idx += 1
    return collected, idx


def parse_csharp_blocks_in_doc(
    doc: ParsedMarkdownDoc,
) -> tuple[list[CSharpRecord], list[CSharpEnum], list[RazorContract]]:
    """Parse all C# records/classes/enums and Razor parameter contracts in a Markdown doc."""
    records: list[CSharpRecord] = []
    enums: list[CSharpEnum] = []
    razor_contracts: list[RazorContract] = []

    for block in doc.code_blocks:
        if block.language not in _CSHARP_LANGS:
            continue
        rec, enm, raz = _parse_single_code_block(doc, block)
        records.extend(rec)
        enums.extend(enm)
        razor_contracts.extend(raz)

    return records, enums, razor_contracts


def _parse_single_code_block(
    doc: ParsedMarkdownDoc,
    block: CodeBlock,
) -> tuple[list[CSharpRecord], list[CSharpEnum], list[RazorContract]]:
    records: list[CSharpRecord] = []
    enums: list[CSharpEnum] = []
    razor_contracts: list[RazorContract] = []

    lines = block.content.splitlines()
    block_content_start_line = block.start_line + 1
    enclosing_heading = _closest_heading(doc.headings, block.start_line)
    heading_text = enclosing_heading.text if enclosing_heading else None

    # Track active Razor component grouping inside the block
    current_razor_name: str | None = _extract_razor_from_heading(enclosing_heading)
    current_razor_start = block_content_start_line
    current_razor_params: list[CSharpProp] = []

    def _flush_razor() -> None:
        nonlocal current_razor_params
        if current_razor_params:
            razor_contracts.append(
                RazorContract(
                    component_name=current_razor_name,
                    parameters=tuple(current_razor_params),
                    file=doc.rel_path,
                    start_line=current_razor_start,
                    heading=heading_text,
                )
            )
            current_razor_params = []

    pending_attrs: list[str] = []
    idx = 0
    in_block_comment = False

    while idx < len(lines):
        raw_line = lines[idx]
        line_no = block_content_start_line + idx
        stripped_raw = raw_line.strip()

        if in_block_comment:
            if "*/" in stripped_raw:
                in_block_comment = False
            idx += 1
            continue

        if stripped_raw.startswith("/*"):
            if "*/" not in stripped_raw[2:]:
                in_block_comment = True
            idx += 1
            continue

        # Check Razor component marker comments (`// CMP-04: ComponentName.razor`)
        if stripped_raw.startswith("//"):
            rm = _RAZOR_MARKER_RE.match(stripped_raw)
            if rm:
                _flush_razor()
                current_razor_name = rm.group(1)
                current_razor_start = line_no
            idx += 1
            continue

        code_line = _strip_inline_comment(raw_line).strip()
        if not code_line:
            idx += 1
            continue

        # Collect attributes (`[Parameter]`, `[Parameter, SupplyParameterFromQuery(...)]`, etc.)
        while code_line.startswith("["):
            am = _ATTR_LINE_RE.match(code_line)
            if not am:
                break
            pending_attrs.append(am.group(1).strip())
            code_line = am.group(2).strip()

        if not code_line:
            idx += 1
            continue

        # Accumulate multi-line header if this line opens an enum or record/class/struct/interface
        # declaration whose `{` or `;` appears on a following line.
        header_line = code_line
        header_end_idx = idx
        if re.match(
            r"^(?:public|internal|private|protected|sealed|abstract|partial|readonly|static|\s)*"
            r"(?:enum|record(?:\s+struct|\s+class)?|class|struct|interface)\b",
            header_line,
        ):
            while (
                "{" not in header_line
                and ";" not in header_line
                and header_end_idx + 1 < len(lines)
            ):
                next_code = _strip_inline_comment(lines[header_end_idx + 1]).strip()
                if not next_code:
                    header_end_idx += 1
                    continue
                if next_code.startswith("[") or next_code.startswith("public ") or next_code.startswith("internal "):
                    break
                header_end_idx += 1
                header_line = f"{header_line} {next_code}".strip()

        # 1. Enum declaration
        em = _ENUM_DECL_RE.match(header_line)
        if em:
            _flush_razor()
            pending_attrs.clear()
            enum_name = em.group("name")
            brace_start = idx
            while brace_start <= header_end_idx and "{" not in _strip_inline_comment(lines[brace_start]):
                brace_start += 1
            body_lines, next_idx = _extract_brace_block(lines, brace_start)
            joined = "\n".join(text for _, text in body_lines)
            inner_m = re.search(r"\{(.*)\}", joined, re.DOTALL)
            members: list[str] = []
            if inner_m:
                for token in inner_m.group(1).split(","):
                    clean_tok = token.split("=", 1)[0].strip()
                    if clean_tok:
                        members.append(clean_tok)
            enums.append(
                CSharpEnum(
                    name=enum_name,
                    members=tuple(members),
                    file=doc.rel_path,
                    line=line_no,
                )
            )
            idx = next_idx
            continue

        # 2. Record / Class / Struct / Interface declaration
        tm = _TYPE_DECL_RE.match(header_line)
        if tm:
            _flush_razor()
            pending_attrs.clear()
            kind = re.sub(r"\s+", " ", tm.group("kind")).strip()
            name = tm.group("name").strip()
            pos_params = tm.group("pos_params")
            bases_raw = tm.group("bases")
            bases = tuple(b.strip() for b in _split_top_level(bases_raw)) if bases_raw else ()
            props: list[CSharpProp] = []
            if pos_params:
                props.extend(_parse_positional_params(pos_params, line_no))

            if tm.group("opener") == "{":
                brace_start = idx
                while brace_start <= header_end_idx and "{" not in _strip_inline_comment(lines[brace_start]):
                    brace_start += 1
                body_lines, next_idx = _extract_brace_block(lines, brace_start)
                # Strip first line up to '{' and final '}'
                inner_pairs: list[tuple[int, str]] = []
                for b_pos, (b_idx, b_text) in enumerate(body_lines):
                    txt = b_text
                    if b_pos == 0 and "{" in txt:
                        txt = txt.split("{", 1)[1]
                    if b_pos == len(body_lines) - 1 and "}" in txt:
                        txt = txt.rsplit("}", 1)[0]
                    inner_pairs.append((block_content_start_line + b_idx, txt))

                prop_attrs: list[str] = []
                for p_line_no, p_raw in inner_pairs:
                    p_str = p_raw.strip()
                    if not p_str:
                        continue
                    while p_str.startswith("["):
                        pam = _ATTR_LINE_RE.match(p_str)
                        if not pam:
                            break
                        prop_attrs.append(pam.group(1).strip())
                        p_str = pam.group(2).strip()
                    if not p_str:
                        continue
                    parsed_prop = _parse_property_line(p_str, tuple(prop_attrs), p_line_no)
                    prop_attrs.clear()
                    if parsed_prop is not None:
                        props.append(parsed_prop)
                idx = next_idx
            else:
                idx = header_end_idx + 1

            records.append(
                CSharpRecord(
                    name=name,
                    kind=kind,
                    base_types=bases,
                    properties=tuple(props),
                    file=doc.rel_path,
                    line=line_no,
                )
            )
            continue

        # 3. Top-level Razor [Parameter] / [SupplyParameterFromQuery] property inside component block
        if any("Parameter" in a for a in pending_attrs):
            stmt = code_line
            stmt_line = line_no
            # Handle multi-line property declaration if `{` / `;` hasn't closed yet
            while "{" not in stmt and ";" not in stmt and idx + 1 < len(lines):
                idx += 1
                stmt += " " + _strip_inline_comment(lines[idx]).strip()
            prop = _parse_property_line(stmt, tuple(pending_attrs), stmt_line)
            pending_attrs.clear()
            if prop is not None:
                current_razor_params.append(prop)
            idx += 1
            continue

        pending_attrs.clear()
        idx += 1

    _flush_razor()
    return records, enums, razor_contracts
