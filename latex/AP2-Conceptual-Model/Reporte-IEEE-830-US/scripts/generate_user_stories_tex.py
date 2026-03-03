import os
import re
import csv

def escape_latex(text):
    """Escapa caracteres especiales de LaTeX y maneja comillas/unicode."""
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
    
    text = text.replace("≥", r"$\ge$").replace("≤", r"$\le$").replace("∞", r"$\infty$").replace("➡", r"$\rightarrow$").replace("→", r"$\rightarrow$")
    text = text.replace("\uFE0F", "")
    text = re.sub(r"[\U0001F300-\U0001FAFF]", "", text) 
    text = re.sub(r"[\u2600-\u27BF]", "", text)         
    
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'^\s*[-•]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    
    return text.strip()

def format_us_description(desc_text):
    """Extrae las 3 partes de la US de forma robusta y las devuelve como lista LaTeX."""
    if not desc_text: return "N/A"
    
    # Normalizar: quitar negritas y citaciones de Markdown
    clean = re.sub(r'\*\*', '', desc_text)
    clean = re.sub(r'^\s*>\s*', '', clean, flags=re.MULTILINE)
    
    # Dividir por líneas para evitar que palabras como "como" dentro de un paréntesis activen la regex
    lines = clean.split('\n')
    como = ""
    quiero = ""
    para = ""
    
    for line in lines:
        line = line.strip()
        # Solo capturar si la línea EMPIEZA con la palabra clave
        if re.match(r'^como\b', line, re.I):
            como = re.sub(r'^como\s*(?::)?\s*', '', line, flags=re.I)
        elif re.match(r'^quiero\b', line, re.I):
            quiero = re.sub(r'^quiero\s*(?::)?\s*', '', line, flags=re.I)
        elif re.match(r'^para\b', line, re.I):
            para = re.sub(r'^para\s*(?::)?\s*', '', line, flags=re.I)
            
    if not (como or quiero or para):
        return escape_latex(' '.join(clean.split()))
    
    parts = []
    if como: parts.append(f"\\item \\textbf{{Como}} {escape_latex(como)}")
    if quiero: parts.append(f"\\item \\textbf{{Quiero}} {escape_latex(quiero)}")
    if para: parts.append(f"\\item \\textbf{{Para}} {escape_latex(para)}")
    
    res = [r"\parbox[t]{\linewidth}{\vspace{2pt}\begin{itemize}[leftmargin=1.5em, nosep, topsep=0pt]"]
    res.extend(parts)
    res.append(r"\end{itemize}\vspace{2pt}}")
    return "\n".join(res)

def load_gherkin_csv(csv_path):
    scenarios_by_us = {}
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                us_id = row.get('US ID', '').strip().upper()
                if not us_id: continue
                if us_id not in scenarios_by_us: scenarios_by_us[us_id] = []
                scenarios_by_us[us_id].append({
                    'Dado': row.get('Contexto', '').strip(),
                    'Cuando': row.get('Acción', '').strip(),
                    'Entonces': row.get('Resultado', '').strip()
                })
    except Exception as e: print(f"❌ Error CSV: {e}")
    return scenarios_by_us

def parse_us_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    meta = {}
    meta_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if meta_match:
        for line in meta_match.group(1).split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip().lower()] = v.strip().strip('"').strip("'")
    
    desc_match = re.search(r'##\s+(?:📋\s*)?Descripción de la Historia\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    description = desc_match.group(1).strip() if desc_match else ""
    
    observations = meta.get('observaciones', '')
    if not observations:
        obs_match = re.search(r'##\s+(?:📝\s*)?Observaciones\s*\n(.*?)(?=\n##|\n---|\Z)', content, re.DOTALL | re.IGNORECASE)
        observations = obs_match.group(1).strip() if obs_match else "N/A"
    
    return meta, description, observations

def generate_tex():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_dir = os.path.dirname(script_dir)
    base_path = os.path.normpath(os.path.join(
        script_dir,
        "..", "..", "..", "..", "..",
        "sena-evidence", "01-Analysis", "AP2-Conceptual-Model", "GA2-220501093-AA1", "EV03-User-Stories"
    ))
    output_dir = os.path.join(report_dir, "sections", "user_stories")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    gherkin_csv = os.path.join(report_dir, "..", "..", "..", "assets", "docs", "databases", "gherkin.csv")
    scenarios_by_us = load_gherkin_csv(os.path.normpath(gherkin_csv))
    
    epic_names = {"MTTO": "Gestión de Operaciones de Mantenimiento", "INV": "Gestión de Recursos e Inventario",
                  "VIS": "Visualización y Gemelo Digital", "ADM": "Administración e Inteligencia de Negocio"}

    for epic in ["MTTO", "INV", "VIS", "ADM"]:
        epic_dir = os.path.join(base_path, epic)
        if not os.path.exists(epic_dir): continue
        
        epic_tex = [f"\\subsection{{Módulo de {epic_names[epic]} ({epic})}}"]
        files = sorted([f for f in os.listdir(epic_dir) if f.endswith(".md")], 
                      key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
        
        for file in files:
            meta, desc, obs = parse_us_file(os.path.join(epic_dir, file))
            us_id = meta.get('id', file.replace('.md', '')).upper()
            
            epic_tex.append(r"\noindent\textbf{Ficha Técnica: " + us_id + " - " + escape_latex(meta.get('nombre', '')) + "}")
            epic_tex.append(r"\footnotesize\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.2}")
            epic_tex.append(r"\rowcolors{2}{tableBlue}{white}\begin{longtable}{|p{0.21\textwidth}|p{0.74\textwidth}|}\hline")
            epic_tex.append(f"\\textbf{{Número}} & {us_id} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Usuario}} & {escape_latex(meta.get('rol', 'N/A'))} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Prioridad}} & {escape_latex(meta.get('prioridad', 'N/A'))} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Puntos Estimados de Esfuerzo}} & {meta.get('puntos', 'N/A')} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Descripción}} & {format_us_description(desc)} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Observaciones}} & {escape_latex(obs)} \\\\ \\hline")
            epic_tex.append(r"\end{longtable}\normalsize")
            
            scenarios = scenarios_by_us.get(us_id, [])
            if scenarios:
                epic_tex.append(r"\noindent\textit{Criterios de Aceptación:}")
                epic_tex.append(r"\footnotesize\begin{longtable}{|p{0.28\textwidth}|p{0.32\textwidth}|p{0.34\textwidth}|}\hline")
                epic_tex.append(r"\textbf{Contexto} & \textbf{Acción} & \textbf{Resultado} \\ \hline")
                for s in scenarios:
                    epic_tex.append(f"\\parbox[t]{{\\linewidth}}{{{escape_latex(s['Dado'])}}} & \\parbox[t]{{\\linewidth}}{{{escape_latex(s['Cuando'])}}} & \\parbox[t]{{\\linewidth}}{{{escape_latex(s['Entonces'])}}} \\\\ \\hline")
                epic_tex.append(r"\end{longtable}\normalsize")
            epic_tex.append(r"\vspace{1em}")
            
        with open(os.path.join(output_dir, f"{epic}.tex"), 'w') as f: f.write("\n".join(epic_tex))
    print("✅ LaTeX regenerado corrigiendo cortes de texto.")

if __name__ == "__main__":
    generate_tex()
