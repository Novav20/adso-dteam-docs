import os
import re

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
    
    # Limpiar restos de markdown y HTML decorativo
    text = text.replace("&nbsp;", " ")
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    
    return text.strip()

def format_cell_content(text):
    """Convierte el contenido de una celda en formato LaTeX profesional con soporte de sub-listas."""
    if not text: return "N/A"
    # Normalizar espacios invisibles desde el inicio
    text = text.replace("\u00A0", " ")
    text = re.sub(r"[\ufeff\u200b\u200c\u200d]", "", text)
    # Eliminar negritas markdown y marcadores sueltos
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = text.replace("**", "")
    # Quitar negritas markdown alrededor de encabezados AF/FA
    text = re.sub(r"\*\*\s*((?:AF|FA)-\d+:[^*]+?)\s*\*\*", r"\1", text)
    
    # 1. Normalización inicial: tratar <ul>/<li> como marcadores si existen
    text = re.sub(r"<ul>", "\n[START_ITEMIZE]\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</ul>", "\n[END_ITEMIZE]\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li>", "\n[ITEM] ", text, flags=re.IGNORECASE)
    text = re.sub(r"</li>", "\n", text, flags=re.IGNORECASE)
    # Detectar guiones usados inline como separadores de viñetas (p.ej. ": - item1 - item2")
    # Reemplazamos las secuencias " - " (con espacios) por un token de item en su propia línea.
    # También manejamos guiones largos/mediados (–, —) con espacios a ambos lados.
    text = re.sub(r"\s+[\-–—]\s+", "\n[ITEM] ", text)
    # Separar títulos de flujos alternativos cuando aparecen en la misma línea
    # Insertar un salto de línea justo antes de cualquier "AF-###" o "FA-###" que no esté ya al inicio de línea.
    text = re.sub(r'(?<!\n)(?=(?:AF|FA)-\d+\b)', '\n', text, flags=re.IGNORECASE)
    # Asegurar salto de línea antes de cualquier " AF-###:" que esté en medio de una línea
    text = re.sub(r'\s+(?=(?:AF|FA)-\d+:)', '\n', text, flags=re.IGNORECASE)
    # Marcar encabezados de flujos alternativos para procesamiento seguro
    # Convertimos líneas que empiezan con AF-###:... en un token [ALT_HEADER] seguido del texto
    text = re.sub(r'(?m)^\s*(?:AF|FA)-\d+:.*', lambda m: '[ALT_HEADER]' + m.group(0).strip(), text)
    
    # 2. Dividir por saltos de línea físicos o lógicos
    raw_lines = re.split(r'<br>|\n', text)
    # Normalizar líneas: quitar prefijos de espacio/ZWSP que puedan quedar después del split
    raw_lines = [re.sub(r'^[\s\ufeff\u200b\u200c\u200d]+', '', rl) for rl in raw_lines]
    
    formatted_lines = []
    stack = [] # Pila para manejar entornos anidados: 'enumerate' o 'itemize'

    def close_all():
        res = []
        while stack:
            res.append(f"\\end{{{stack.pop()}}}")
        return res

    for line in raw_lines:
        # Normalizar espacios no separables, eliminar espacios/zwsp iniciales y recortar
        line = line.replace("\u00A0", " ").replace("&nbsp;", " ")
        line = re.sub(r'^[\s\ufeff\u200b\u200c\u200d]+', '', line).strip()
        if not line:
            continue
        if line.strip() == "**":
            continue
        
        # Caso A: Títulos de flujos alternativos (AF-XXX) — permitir espacios iniciales
        if line.startswith('[ALT_HEADER]'):
            title = line.replace('[ALT_HEADER]', '').replace('**', '').strip()
            formatted_lines.extend(close_all())
            formatted_lines.append(f"\\vspace{{4pt}}\\noindent\\textbf{{{escape_latex(title)}}}")
            formatted_lines.append(r"\newline")
            continue
        if re.match(r'^\s*(?:AF|FA)-\d+', line, re.IGNORECASE):
            formatted_lines.extend(close_all())
            formatted_lines.append(f"\\vspace{{4pt}}\\noindent\\textbf{{{escape_latex(line.strip())}}}")
            formatted_lines.append(r"\newline")
            
        # Caso B: Ítems numerados (Flujo Principal)
        elif re.match(r'^\d+\.', line):
            if not stack or stack[-1] != 'enumerate':
                if stack and stack[-1] == 'itemize': # Si venía de una viñeta, cerramos esa viñeta
                    formatted_lines.append(r"\end{itemize}")
                    stack.pop()
                if not stack:
                    formatted_lines.append(r"\begin{enumerate}[leftmargin=1.5em, nosep, topsep=0pt]")
                    stack.append('enumerate')
            
            # Extraer texto después del número
            item_text = re.sub(r'^\d+\.\s*', '', line)
            # Detectar sub-ítems unidos con guiones dentro de la misma línea, p.ej.
            # "... campos obligatorios: - A - B - C"
            parts = re.split(r"\s+[\-–—]\s+", item_text)
            first = parts[0].strip()
            formatted_lines.append(f"\\item {escape_latex(first)}")
            if len(parts) > 1:
                # Abrir itemize anidado
                formatted_lines.append(r"\begin{itemize}[leftmargin=1.2em, nosep, topsep=0pt]")
                stack.append('itemize')
                for sub in parts[1:]:
                    sub = sub.strip()
                    if sub:
                        formatted_lines.append(f"\\item {escape_latex(sub)}")

        # Caso C: Viñetas (Sub-pasos o listas simples)
        elif re.match(r'^[\-–—•*]\s+', line) or "[ITEM]" in line:
            # Si estamos en un enumerate, abrimos un itemize anidado
            if stack and stack[-1] == 'enumerate':
                formatted_lines.append(r"\begin{itemize}[leftmargin=1.2em, nosep, topsep=0pt]")
                stack.append('itemize')
            elif not stack:
                formatted_lines.append(r"\begin{itemize}[leftmargin=1.5em, nosep, topsep=0pt]")
                stack.append('itemize')
            
            item_text = re.sub(r'^[-•*]\s*|\[ITEM\]\s*', '', line)
            formatted_lines.append(f"\\item {escape_latex(item_text)}")

        # Caso D: Marcadores HTML explícitos
        elif "[START_ITEMIZE]" in line:
            formatted_lines.append(r"\begin{itemize}[leftmargin=1.5em, nosep, topsep=0pt]")
            stack.append('itemize')
        elif "[END_ITEMIZE]" in line:
            if stack: formatted_lines.append(f"\\end{{{stack.pop()}}}")

        # Caso E: Texto plano o continuación
        else:
            # Si la línea contiene encabezados AF/FA, procesarlos primero (aunque haya listas abiertas)
            if re.search(r'(?:AF|FA)-\d+:', line, re.IGNORECASE):
                parts = re.split(r'(?=(?:AF|FA)-\d+:)', line)
                for p in parts:
                    p = p.strip()
                    if not p:
                        continue
                    if re.match(r'^(?:AF|FA)-\d+:', p, re.IGNORECASE):
                        formatted_lines.extend(close_all())
                        formatted_lines.append(f"\\vspace{{4pt}}\\noindent\\textbf{{{escape_latex(p.replace('**',''))}}}")
                        formatted_lines.append(r"\newline")
                    else:
                        formatted_lines.append(escape_latex(p))
            else:
                # Si hay una lista abierta, cerramos los niveles de viñetas para volver al texto o lo tratamos como item
                if stack:
                    formatted_lines.append(f" {escape_latex(line)}") # Continuación en la misma línea
                else:
                    formatted_lines.append(escape_latex(line))
            
    formatted_lines.extend(close_all())
        
    res = r"\parbox[t]{\linewidth}{\vspace{2pt} " + "\n".join(formatted_lines) + r" \vspace{2pt}}"
    return res

def parse_use_cases_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    use_cases = []
    pattern = r'###\s+(UC-\w+-\d+):\s*(.*?)\n\n(.*?)(?=\n###|\Z)'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        uc_id = match.group(1)
        uc_name = match.group(2).strip()
        table_content = match.group(3)
        uc_data = {'id': uc_id, 'nombre': uc_name}
        
        rows = re.findall(r'\|\s*\*\*(.*?)\*\*\s*\|\s*(.*?)\s*\|', table_content)
        for field, value in rows:
            f_key = field.lower().strip()
            if 'actor principal' in f_key: uc_data['actor'] = value.strip()
            elif 'secundarios' in f_key: uc_data['secundarios'] = value.strip()
            elif 'descripción' in f_key: uc_data['desc'] = value.strip()
            elif 'precondiciones' in f_key: uc_data['pre'] = value.strip()
            elif 'flujo principal' in f_key: uc_data['flow'] = value.strip()
            elif 'flujos alternativos' in f_key: uc_data['alt'] = value.strip()
            elif 'postcondiciones' in f_key: uc_data['post'] = value.strip()
            elif 'requisitos' in f_key: uc_data['reqs'] = value.strip()
            
        use_cases.append(uc_data)
    return use_cases

def generate_tex():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.normpath(os.path.join(
        script_dir, "..", "01-Analysis", "AP2-Conceptual-Model",
        "GA2-220501093-AA1", "EV02-Use-Cases"
    ))
    output_dir = os.path.normpath(os.path.join(
        script_dir, "..", "01-Analysis", "AP2-Conceptual-Model",
        "GA2-220501093-AA1", "IEEE-830-US-Report", "sections", "use_cases"
    ))
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    epic_names = {"MTTO": "Gestión de Operaciones de Mantenimiento", "INV": "Gestión de Recursos e Inventario", 
                  "VIS": "Visualización y Gemelo Digital", "ADM": "Administración e Inteligencia de Negocio"}
    
    for epic in ["MTTO", "INV", "VIS", "ADM"]:
        file_path = os.path.join(base_path, f"Casos-Uso-{epic}.md")
        if not os.path.exists(file_path): continue
        
        ucs = parse_use_cases_file(file_path)
        epic_tex = [f"\\subsection{{Módulo de {epic_names[epic]} ({epic})}}\n"]
        
        pdf_diag = f"assets/Diagrama-UC-{epic}.pdf"
        epic_tex.append(r"\begin{figure}[H]\centering")
        epic_tex.append(f"\\includegraphics[width=0.85\\textwidth]{{{pdf_diag}}}")
        epic_tex.append(f"\\caption{{Diagrama de Casos de Uso - {epic_names[epic]}}}\\end{{figure}}\n")

        for uc in ucs:
            epic_tex.append(r"\noindent\textbf{Ficha de Caso de Uso: " + uc['id'] + " - " + escape_latex(uc['nombre']) + "}")
            epic_tex.append(r"\footnotesize\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.2}")
            epic_tex.append(r"\rowcolors{2}{tableBlue}{white}\begin{longtable}{>{\raggedright\arraybackslash}p{0.21\textwidth} >{\raggedright\arraybackslash}p{0.74\textwidth}} \toprule")
            epic_tex.append(f"\\textbf{{Actor Principal}} & {escape_latex(uc.get('actor', 'N/A'))} \\\\")
            epic_tex.append(f"\\textbf{{Actores Secundarios}} & {escape_latex(uc.get('secundarios', 'N/A'))} \\\\")
            epic_tex.append(f"\\textbf{{Descripción}} & {escape_latex(uc.get('desc', 'N/A'))} \\\\")
            epic_tex.append(f"\\textbf{{Precondiciones}} & {format_cell_content(uc.get('pre', ''))} \\\\")
            epic_tex.append(f"\\textbf{{Flujo Principal}} & {format_cell_content(uc.get('flow', ''))} \\\\")
            epic_tex.append(f"\\textbf{{Flujos Alternativos}} & {format_cell_content(uc.get('alt', ''))} \\\\")
            epic_tex.append(f"\\textbf{{Postcondiciones}} & {format_cell_content(uc.get('post', ''))} \\\\")
            epic_tex.append(f"\\textbf{{Requisitos}} & {escape_latex(uc.get('reqs', 'N/A'))} \\\\ \\bottomrule")
            epic_tex.append(r"\end{longtable}\normalsize\vspace{1em}")
            
        with open(os.path.join(output_dir, f"{epic}.tex"), 'w', encoding='utf-8') as f: f.write("\n".join(epic_tex))
    print("✅ Casos de Uso regenerados con éxito.")

if __name__ == "__main__":
    generate_tex()
