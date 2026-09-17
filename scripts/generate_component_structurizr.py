import re

def extract_tables(md_text):
    tables = []
    lines = md_text.split('\n')
    current_table = []
    in_table = False
    
    for line in lines:
        if line.strip().startswith('|'):
            in_table = True
            current_table.append(line)
        elif in_table:
            tables.append(current_table)
            current_table = []
            in_table = False
            
    if in_table:
        tables.append(current_table)
        
    return tables

def parse_table(table_lines):
    if not table_lines or len(table_lines) < 3:
        return []
    
    headers = [col.strip() for col in table_lines[0].split('|')[1:-1]]
    rows = []
    
    for line in table_lines[2:]:
        cols = [col.strip() for col in line.split('|')[1:-1]]
        # Remove markdown bold formatting from IDs and text
        cols = [c.replace('**', '').strip() for c in cols]
        rows.append(dict(zip(headers, cols)))
        
    return rows

def generate_structurizr_dsl(md_path, out_dsl_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
        
    tables = extract_tables(md_text)
    
    components = parse_table(tables[0])
    relationships = parse_table(tables[1])
    
    # Categorize nodes
    boundaries = {
        "Client Application": [],
        "External System": [],
        "Driving Adapter": [],
        "Primary Port (In)": [],
        "Domain Service": [],
        "Secondary Port (Out)": [],
        "Driven Adapter": []
    }
    
    for c in components:
        stereo = c.get('Capa Arquitectónica / Estereotipo')
        if stereo in boundaries:
            boundaries[stereo].append(c)
        else:
            if 'Adapter' in stereo or 'External' in stereo or 'Client' in stereo:
                boundaries["External System"].append(c)
            else:
                boundaries["Domain Service"].append(c)

    dsl = []
    dsl.append("workspace \"SENA-Career Component Model\" {")
    dsl.append("")
    dsl.append("    model {")
    dsl.append("        # External Systems and Clients")
    
    for c in boundaries["Client Application"]:
        dsl.append(f"        {c['ID Componente']} = softwareSystem \"{c['Componente o Puerto Funcional']}\" \"{c['Responsabilidad Técnica']}\" \"Client\"")
        
    for c in boundaries["External System"]:
        dsl.append(f"        {c['ID Componente']} = softwareSystem \"{c['Componente o Puerto Funcional']}\" \"{c['Responsabilidad Técnica']}\" \"External\"")
        
    dsl.append("")
    dsl.append("        monolith = softwareSystem \"SENA-Career Monolith\" \"Modular Monolith (.NET 10)\" {")
    
    # We map C4 Components to Components within a default Container
    dsl.append("            appContainer = container \"Application Core\" \"Core services and adapters\" \".NET 10\" {")
    
    dsl.append("                group \"Driving Adapters\" {")
    for c in boundaries["Driving Adapter"]:
        dsl.append(f"                    {c['ID Componente']} = component \"{c['Componente o Puerto Funcional']}\" \"{c['Responsabilidad Técnica']}\" \"{c['Puerto / Interfaz']}\"")
    dsl.append("                }")
    
    dsl.append("                group \"Application Core\" {")
    for c in boundaries["Primary Port (In)"]:
        dsl.append(f"                    {c['ID Componente']} = component \"{c['Componente o Puerto Funcional']}\" \"{c['Responsabilidad Técnica']}\" \"{c['Puerto / Interfaz']}\"")
    for c in boundaries["Domain Service"]:
        dsl.append(f"                    {c['ID Componente']} = component \"{c['Componente o Puerto Funcional']}\" \"{c['Responsabilidad Técnica']}\" \"{c['Puerto / Interfaz']}\"")
    for c in boundaries["Secondary Port (Out)"]:
        dsl.append(f"                    {c['ID Componente']} = component \"{c['Componente o Puerto Funcional']}\" \"{c['Responsabilidad Técnica']}\" \"{c['Puerto / Interfaz']}\"")
    dsl.append("                }")
    
    dsl.append("                group \"Driven Adapters\" {")
    for c in boundaries["Driven Adapter"]:
        dsl.append(f"                    {c['ID Componente']} = component \"{c['Componente o Puerto Funcional']}\" \"{c['Responsabilidad Técnica']}\" \"{c['Puerto / Interfaz']}\"")
    dsl.append("                }")
    
    dsl.append("            }")
    dsl.append("        }")
    dsl.append("")
    
    dsl.append("        # Relationships")
    for r in relationships:
        src = r['Origen']
        dest = r['Destino']
        tech = r['Protocolo / Interfaz']
        desc = r['Propósito y Descripción']
        dsl.append(f"        {src} -> {dest} \"{desc}\" \"{tech}\"")
        
    dsl.append("    }")
    dsl.append("")
    dsl.append("    views {")
    dsl.append("        component appContainer \"ComponentDiagram\" {")
    dsl.append("            include *")
    dsl.append("            autoLayout tb")
    dsl.append("        }")
    dsl.append("        ")
    dsl.append("        theme default")
    dsl.append("    }")
    dsl.append("}")
    
    with open(out_dsl_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(dsl))

if __name__ == '__main__':
    md = 'architecture/views/DT-ARQ-CMP-DOC-001.md'
    dsl = 'architecture/views/DT-ARQ-CMP-001-component-model.dsl'
    generate_structurizr_dsl(md, dsl)
    print(f"Generated {dsl}")
