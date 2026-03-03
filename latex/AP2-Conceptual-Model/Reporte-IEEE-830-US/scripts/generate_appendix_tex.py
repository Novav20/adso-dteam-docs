import os
import re
import csv
from pathlib import Path

# Configuración de rutas relativas
SCRIPT_DIR = Path(__file__).parent
BASE_SENA_DIR = SCRIPT_DIR / "../../../../../sena-evidence/01-Analysis/AP2-Conceptual-Model/GA2-220501093-AA1"
US_DIR = BASE_SENA_DIR / "EV03-User-Stories"
OUTPUT_DIR = SCRIPT_DIR.parent / "sections/appendices"
SRS_CSV = SCRIPT_DIR.parent.parent.parent.parent / "assets/docs/databases/srs.csv"

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

def collect_requirements():
    epic_data = {"MTTO": [], "INV": [], "VIS": [], "ADM": [], "COMMON": []}

    if SRS_CSV.exists():
        with open(SRS_CSV, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                req_id = (row.get('Req ID') or "").strip().upper()
                if re.match(r'^TR-\d+-(FR|NFR)-\d+$', req_id):
                    desc = (row.get('Descripción') or "").strip()
                    desc = re.sub(r'^TR-\d+-(FR|NFR)-\d+:\s*', '', desc)
                    epic_data["COMMON"].append({
                        'id': req_id,
                        'desc': desc,
                        'prio': (row.get('Prioridad') or "Media").strip(),
                    })
                    continue

                if not re.match(r'^(FR|NFR)-\d+$', req_id):
                    continue

                related_story = (row.get('Historia Relacionada') or "").strip().upper()
                epic_match = re.match(r'^(MTTO|INV|VIS|ADM)-\d+', related_story)
                if not epic_match:
                    continue
                epic = epic_match.group(1)

                desc = (row.get('Descripción') or "").strip()
                desc = re.sub(r'^(FR|NFR)-\d+:\s*', '', desc)

                epic_data[epic].append({
                    'id': req_id,
                    'desc': desc,
                    'cat': (row.get('Categoría ISO 25010') or "Functional Suitability").strip(),
                    'prio': (row.get('Prioridad') or "Media").strip(),
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
        "MTTO": "Requisitos del Módulo de Gestión de Mantenimiento", 
        "INV": "Requisitos del Módulo de Gestión de Inventario", 
        "VIS": "Requisitos del Módulo de Visualización Digital", 
        "ADM": "Requisitos del Módulo de Administración",
        "COMMON": "Requisitos Transversales"
    }
    
    for epic, name in epic_names.items():
        if data[epic]:
            generate_epic_tex(epic, data[epic], name)
            print(f"✅ {epic}.tex generado para jerarquía A.X.Y.")

if __name__ == "__main__":
    generate_all()
