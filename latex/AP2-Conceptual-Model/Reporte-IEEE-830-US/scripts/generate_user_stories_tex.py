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

def format_us_description(como, quiero, para):
    """Construye la descripción de US (Como/Quiero/Para) como lista LaTeX."""
    como = re.sub(r'^\s*como\s*', '', (como or "").strip(), flags=re.IGNORECASE)
    quiero = re.sub(r'^\s*quiero\s*', '', (quiero or "").strip(), flags=re.IGNORECASE)
    para = re.sub(r'^\s*para\s*', '', (para or "").strip(), flags=re.IGNORECASE)

    if not (como or quiero or para):
        return "N/A"

    parts = []
    if como: parts.append(f"\\item \\textbf{{Como}} {escape_latex(como)}")
    if quiero: parts.append(f"\\item \\textbf{{Quiero}} {escape_latex(quiero)}")
    if para: parts.append(f"\\item \\textbf{{Para}} {escape_latex(para)}")
    
    res = [r"\parbox[t]{\linewidth}{\vspace{2pt}\begin{itemize}[leftmargin=1.5em, nosep, topsep=0pt]"]
    res.extend(parts)
    res.append(r"\end{itemize}\vspace{2pt}}")
    return "\n".join(res)

def clean_role(role_text):
    if not role_text:
        return "N/A"
    role = re.sub(r'\s*\(https?://[^)]*\)', '', role_text).strip()
    return role if role else "N/A"

def clean_story_title(us_id, title_text):
    title = (title_text or "").strip()
    if not title:
        return us_id
    pattern = rf'^\s*{re.escape(us_id)}\s*[:\-–—]\s*'
    return re.sub(pattern, '', title, flags=re.IGNORECASE).strip()

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

def load_user_stories_csv(csv_path):
    stories_by_epic = {"MTTO": [], "INV": [], "VIS": [], "ADM": []}

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            epic = (row.get('Epic') or "").strip().upper()
            us_id = (row.get('US ID') or "").strip().upper()
            if epic not in stories_by_epic or not us_id:
                continue

            story = {
                'us_id': us_id,
                'nombre': clean_story_title(us_id, (row.get('Nombre') or "").strip()),
                'usuario': clean_role((row.get('Rol (Como ...)') or row.get('Como') or "").strip()),
                'prioridad': (row.get('MoSCoW') or "N/A").strip(),
                'puntos': (row.get('Puntos Fibonacci') or "N/A").strip(),
                'como': (row.get('Como') or "").strip(),
                'quiero': (row.get('Quiero') or row.get('Acción') or "").strip(),
                'para': (row.get('Para') or row.get('Beneficio') or "").strip(),
                'observaciones': (row.get('Observaciones') or "N/A").strip(),
            }
            stories_by_epic[epic].append(story)

    def us_sort_key(item):
        match = re.search(r'-(\d+)$', item['us_id'])
        return int(match.group(1)) if match else 999999

    for epic in stories_by_epic:
        stories_by_epic[epic].sort(key=us_sort_key)

    return stories_by_epic

def generate_tex():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_dir = os.path.dirname(script_dir)
    user_stories_csv = os.path.join(report_dir, "..", "..", "..", "assets", "docs", "databases", "user_stories.csv")
    user_stories_csv = os.path.normpath(user_stories_csv)
    output_dir = os.path.join(report_dir, "sections", "user_stories")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    gherkin_csv = os.path.join(report_dir, "..", "..", "..", "assets", "docs", "databases", "gherkin.csv")
    scenarios_by_us = load_gherkin_csv(os.path.normpath(gherkin_csv))
    stories_by_epic = load_user_stories_csv(user_stories_csv)
    
    epic_names = {"MTTO": "Gestión de Operaciones de Mantenimiento", "INV": "Gestión de Recursos e Inventario",
                  "VIS": "Visualización y Gemelo Digital", "ADM": "Administración e Inteligencia de Negocio"}

    for epic in ["MTTO", "INV", "VIS", "ADM"]:
        stories = stories_by_epic.get(epic, [])
        if not stories:
            continue
        
        epic_tex = [f"\\subsection{{Módulo de {epic_names[epic]} ({epic})}}"]
        
        for story in stories:
            us_id = story['us_id']
            
            epic_tex.append(r"\noindent\textbf{Ficha Técnica: " + us_id + " - " + escape_latex(story.get('nombre', '')) + "}")
            epic_tex.append(r"\footnotesize\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.2}")
            epic_tex.append(r"\rowcolors{2}{tableBlue}{white}\begin{longtable}{|p{0.21\textwidth}|p{0.74\textwidth}|}\hline")
            epic_tex.append(f"\\textbf{{Número}} & {us_id} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Usuario}} & {escape_latex(story.get('usuario', 'N/A'))} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Prioridad}} & {escape_latex(story.get('prioridad', 'N/A'))} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Puntos Estimados de Esfuerzo}} & {escape_latex(story.get('puntos', 'N/A'))} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Descripción}} & {format_us_description(story.get('como', ''), story.get('quiero', ''), story.get('para', ''))} \\\\ \\hline")
            epic_tex.append(f"\\textbf{{Observaciones}} & {escape_latex(story.get('observaciones', 'N/A'))} \\\\ \\hline")
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
