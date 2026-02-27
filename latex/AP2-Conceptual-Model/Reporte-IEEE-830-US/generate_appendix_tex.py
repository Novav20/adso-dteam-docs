import os
import re
from pathlib import Path

# Configuración de rutas
BASE_DIR = Path("/home/novillus/Documents/vscode/SENA-Career")
US_DIR = BASE_DIR / "sena-evidence/01-Analysis/AP2-Conceptual-Model/GA2-220501093-AA1/EV03-User-Stories"
TR_FILE = BASE_DIR / "sena-evidence/01-Analysis/AP2-Conceptual-Model/GA2-220501093-AA1/EV02-Common-Requirements.md"
OUTPUT_DIR = BASE_DIR / "sena-evidence/01-Analysis/AP2-Conceptual-Model/GA2-220501093-AA1/IEEE-830-US-Report/sections/appendices"

def escape_latex(text):
    if not text: return ""
    text = text.replace("\\", r"\textbackslash{}")
    text = text.replace("&", r"\&").replace("%", r"\%").replace("$", r"\$").replace("#", r"\#").replace("_", r"\_")
    text = text.replace("{", r"\{").replace("}", r"\}").replace("~", r"\textasciitilde{}").replace("^", r"\textasciicircum{}")
    
    quote_toggle = True
    out = []
    for ch in text:
        if ch in ('"', '“', '”'):
            out.append('``' if quote_toggle else "''")
            quote_toggle = not quote_toggle
        else: out.append(ch)
    text = "".join(out)
    
    text = text.replace("≥", r"$\ge$").replace("≤", r"$\le$").replace("∞", r"$\infty$").replace("➡", r"$\rightarrow$")
    text = re.sub(r"[\U0001F300-\U0001FAFF]", "", text)
    text = re.sub(r"[\u2600-\u27BF]", "", text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    return text.strip()

def parse_md_table(content):
    rows = []
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('|') and not re.match(r'^[|\s:-]+$', line.strip()):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                parts[1] = re.sub(r'\*+', '', parts[1])
                rows.append(parts[1:-1])
    return rows

def collect_requirements():
    trs = []
    if TR_FILE.exists():
        tr_content = TR_FILE.read_text(encoding='utf-8')
        tr_rows = parse_md_table(tr_content)
        for r in tr_rows:
            if re.search(r'TR-\d+-(FR|NFR)-\d+', r[0]):
                trs.append({
                    'id': r[0], 
                    'desc': r[2] if len(r) > 2 else "", 
                    'prio': r[1] if len(r) > 1 else "High"
                })

    epic_data = {"MTTO": [], "INV": [], "VIS": [], "ADM": [], "COMMON": trs}
    for epic in ["MTTO", "INV", "VIS", "ADM"]:
        epic_dir = US_DIR / epic
        if not epic_dir.exists(): continue
        files = sorted(list(epic_dir.glob("*.md")))
        for f in files:
            content = f.read_text(encoding='utf-8')
            tables = re.findall(r'## (?:Requisitos|Criterios).*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
            for table_text in tables:
                rows = parse_md_table(table_text)
                for r in rows:
                    if re.match(r'^(FR|NFR)-\d+', r[0]):
                        epic_data[epic].append({
                            'id': r[0], 
                            'desc': r[1], 
                            'cat': r[2] if len(r) > 2 else "Functional", 
                            'prio': r[3] if len(r) > 3 else "High"
                        })
    return epic_data

def generate_epic_tex(epic, reqs, name):
    is_common = (epic == "COMMON")
    
    if is_common:
        col_def = r">{\raggedright\arraybackslash}p{0.15\textwidth} >{\raggedright\arraybackslash}p{0.68\textwidth} >{\raggedright\arraybackslash}p{0.12\textwidth}"
        header = r"\rowcolor{gray!15}\textbf{ID} & \textbf{Descripción} & \textbf{Prioridad} \\ \midrule"
    else:
        col_def = r">{\raggedright\arraybackslash}p{0.12\textwidth} >{\raggedright\arraybackslash}p{0.50\textwidth} >{\raggedright\arraybackslash}p{0.18\textwidth} >{\raggedright\arraybackslash}p{0.12\textwidth}"
        header = r"\rowcolor{gray!15}\textbf{ID} & \textbf{Descripción} & \textbf{Categoría} & \textbf{Prioridad} \\ \midrule"

    # Cambiado a \subsubsection para que sea A.X.Y (ej: A.1)
    tex = [
        f"\\subsubsection{{{name}}}",
        r"\footnotesize",
        f"\\begin{{longtable}}{{{col_def}}}",
        r"\toprule",
        header,
        r"\endhead",
    ]
    
    def sort_key(req):
        m = re.match(r'([A-Z]+)-(\d+)', req['id'])
        if m:
            m2 = re.match(r'TR-(\d+)-(FR|NFR)-(\d+)', req['id'])
            if m2: return ("TR", int(m2.group(1)), m2.group(2), int(m2.group(3)))
            return (m.group(1), int(m.group(2)), "", 0)
        return (req['id'], 0, "", 0)
    
    sorted_reqs = sorted(reqs, key=sort_key)
    
    for r in sorted_reqs:
        if is_common:
            row = f"{escape_latex(r['id'])} & {escape_latex(r['desc'])} & {escape_latex(r['prio'])} \\\\"
        else:
            row = f"{escape_latex(r['id'])} & {escape_latex(r['desc'])} & {escape_latex(r['cat'])} & {escape_latex(r['prio'])} \\\\"
        tex.append(row)
        
    tex.append(r"\bottomrule")
    tex.append(r"\end{longtable}")
    tex.append(r"\normalsize")
    
    (OUTPUT_DIR / f"{epic}.tex").write_text("\n".join(tex), encoding='utf-8')

def generate_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    data = collect_requirements()
    
    epic_names = {
        "COMMON": "Requisitos Transversales",
        "MTTO": "Requisitos del Módulo de Gestión de Mantenimiento", 
        "INV": "Requisitos del Módulo de Gestión de Inventario", 
        "VIS": "Requisitos del Módulo de Visualización Digital", 
        "ADM": "Requisitos del Módulo de Administración"
    }
    
    for epic, name in epic_names.items():
        if data[epic]:
            generate_epic_tex(epic, data[epic], name)
            print(f"✅ {epic}.tex generado para jerarquía A.X.Y.")

if __name__ == "__main__":
    generate_all()
