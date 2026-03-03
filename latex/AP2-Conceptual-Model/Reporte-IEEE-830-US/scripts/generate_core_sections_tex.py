import argparse
import difflib
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
TEX_DIR = (SCRIPT_DIR.parent / "sections").resolve()

MD_DIR_CANDIDATES = [
    (SCRIPT_DIR / "../../../../../sena-evidence/01-Analysis/AP2-Conceptual-Model/GA2-220501093-AA1/Draft-Report").resolve(),
    (SCRIPT_DIR / "../../../../../sena-evidence/01-Analysis/AP2-Conceptual-Model/GA2-220501093-AA1/Report-Draft").resolve(),
]

FILE_MAP = {
    "1-Introduccion.md": "intro.tex",
    "2-Descripcion-General.md": "general_desc.tex",
    "3-Requerimientos-Especificos.md": "specific_reqs.tex",
    "4-Conclusiones.md": "conclusiones.tex",
}


def resolve_md_dir() -> Path:
    for path in MD_DIR_CANDIDATES:
        if path.exists():
            return path
    return MD_DIR_CANDIDATES[0]


def escape_latex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("≥", r"$\ge$")
    text = text.replace("≤", r"$\le$")
    text = re.sub(r"(?<=\s)<(?=\s|\d)", r"$<$", text)
    text = re.sub(r"(?<=\s)>(?=\s|\d)", r"$>$", text)

    url_pattern = re.compile(r"https?://[^\s]+")
    urls = []

    def hold_url(match):
        urls.append(match.group(0))
        return f"__URL_{len(urls)-1}__"

    text = url_pattern.sub(hold_url, text)

    quote_toggle = True
    out = []
    for ch in text:
        if ch in ('"', '“', '”'):
            out.append("``" if quote_toggle else "''")
            quote_toggle = not quote_toggle
        else:
            out.append(ch)
    text = "".join(out)

    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\\textit{\1}", text)

    text = text.replace(
        "electrical/electronic/programmable",
        r"electrical\slash electronic\slash programmable",
    )

    for i, url in enumerate(urls):
        text = text.replace(f"__URL_{i}__", rf"\url{{{url}}}")

    return text


def close_lists(tex_lines: list[str], list_stack: list[str]) -> None:
    while list_stack:
        tex_lines.append(f"\\end{{{list_stack.pop()}}}")


def heading_to_latex(level: int, text: str) -> str:
    text = escape_latex(text.strip())
    if level == 1:
        return f"\\section{{{text}}}"
    if level == 2:
        return f"\\subsection{{{text}}}"
    return f"\\subsubsection{{{text}}}"


def markdown_to_tex(md_text: str) -> str:
    tex_lines: list[str] = []
    list_stack: list[str] = []
    in_sloppypar = False

    lines = md_text.splitlines()

    for raw_line in lines:
        if not raw_line.strip():
            if not list_stack:
                tex_lines.append("")
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", raw_line)
        if heading_match:
            close_lists(tex_lines, list_stack)
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()

            if in_sloppypar:
                tex_lines.append(r"\end{sloppypar}")
                in_sloppypar = False

            tex_lines.append(heading_to_latex(level, heading_text))

            if heading_text.lower() == "referencias":
                tex_lines.append(r"\begin{sloppypar}")
                in_sloppypar = True
            continue

        num_match = re.match(r"^\s*\d+\.\s+(.*)$", raw_line)
        if num_match:
            if list_stack != ["enumerate"]:
                close_lists(tex_lines, list_stack)
                tex_lines.append(r"\begin{enumerate}")
                list_stack.append("enumerate")
            tex_lines.append(rf"    \item {escape_latex(num_match.group(1).strip())}")
            continue

        bullet_match = re.match(r"^(\s*)-\s+(.*)$", raw_line)
        if bullet_match:
            indent_spaces = len(bullet_match.group(1).replace("\t", "    "))
            depth = 1 + (indent_spaces // 2)

            if any(env != "itemize" for env in list_stack):
                close_lists(tex_lines, list_stack)

            while len(list_stack) < depth:
                tex_lines.append(r"\begin{itemize}")
                list_stack.append("itemize")
            while len(list_stack) > depth:
                tex_lines.append(f"\\end{{{list_stack.pop()}}}")

            tex_lines.append(rf"    \item {escape_latex(bullet_match.group(2).strip())}")
            continue

        close_lists(tex_lines, list_stack)
        tex_lines.append(escape_latex(raw_line.strip()))

    close_lists(tex_lines, list_stack)

    if in_sloppypar:
        tex_lines.append(r"\end{sloppypar}")

    return "\n".join(tex_lines).strip() + "\n"


def normalize_content(text: str) -> str:
    text = re.sub(r"\\(section|subsection|subsubsection)\{([^}]*)\}", r" \2 ", text)
    text = re.sub(r"\\begin\{[^}]*\}|\\end\{[^}]*\}", " ", text)
    text = re.sub(r"\\item", " ", text)
    text = text.replace(r"\textbf{", "").replace(r"\textit{", "")
    text = text.replace("{", " ").replace("}", " ")
    text = text.replace(r"$\ge$", "≥").replace(r"$\le$", "≤").replace(r"$<$", "<").replace(r"$>$", ">")
    text = text.replace("``", '"').replace("''", '"')
    text = re.sub(r"\\url\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    text = re.sub(r"[#*_\-|]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def generate_sections(write: bool) -> int:
    md_dir = resolve_md_dir()
    print(f"📁 Fuente Markdown: {md_dir}")

    missing = [name for name in FILE_MAP if not (md_dir / name).exists()]
    if missing:
        print("❌ Faltan archivos Markdown:")
        for name in missing:
            print(f"   - {md_dir / name}")
        return 1

    exit_code = 0
    for md_name, tex_name in FILE_MAP.items():
        md_path = md_dir / md_name
        tex_path = TEX_DIR / tex_name

        generated = markdown_to_tex(md_path.read_text(encoding="utf-8"))
        current = tex_path.read_text(encoding="utf-8") if tex_path.exists() else ""

        if generated == current:
            print(f"✅ Sin cambios: {tex_name}")
            continue

        same_content = normalize_content(generated) == normalize_content(current)
        if same_content:
            print(f"🟢 Contenido equivalente (solo diferencias de formato): {tex_name}")
            if not write:
                continue

        print(f"🟡 Diferencias detectadas: {tex_name}")
        diff = difflib.unified_diff(
            current.splitlines(),
            generated.splitlines(),
            fromfile=f"actual/{tex_name}",
            tofile=f"generated/{tex_name}",
            lineterm="",
            n=2,
        )
        for line in list(diff)[:80]:
            print(line)

        if write:
            tex_path.write_text(generated, encoding="utf-8")
            print(f"✍️  Actualizado: {tex_path}")
        else:
            exit_code = 2

    return exit_code


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera secciones TEX (intro/general/specific/conclusiones) a partir de Markdown."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Escribe los .tex cuando existan diferencias (sin este flag solo muestra diff).",
    )
    args = parser.parse_args()

    code = generate_sections(write=args.write)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
