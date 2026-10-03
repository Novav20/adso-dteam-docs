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
        stereo = c.get('Architectural Layer / Stereotype', '')
        c_id = c.get('Component ID', '')
        
        if c_id in ["local_db", "loto_watchdog"]:
            boundaries["External System"].append(c)
        elif stereo in boundaries:
            boundaries[stereo].append(c)
        else:
            if 'Adapter' in stereo or 'External' in stereo or 'Client' in stereo or 'Persistence' in stereo:
                boundaries["External System"].append(c)
            else:
                boundaries["Domain Service"].append(c)

    dsl = []
    dsl.append("workspace \"System Component Model\" {")
    dsl.append("")
    dsl.append("    model {")
    dsl.append("        # External Systems and Clients")
    
    for c in boundaries["Client Application"]:
        c_id = c['Component ID']
        tag = "Mobile" if "mobile" in c_id.lower() else "WebBrowser" if "web" in c_id.lower() else "Client"
        dsl.append(f"        {c_id} = softwareSystem \"{c['Component or Functional Port']}\" \"{c['Technical Responsibility']}\" \"{tag}\"")
        
    for c in boundaries["External System"]:
        c_id = c['Component ID']
        tag = "Database" if "db" in c_id.lower() or "redis" in c_id.lower() else "Broker" if "iot" in c_id.lower() else "External"
        dsl.append(f"        {c_id} = softwareSystem \"{c['Component or Functional Port']}\" \"{c['Technical Responsibility']}\" \"{tag}\"")
        
    dsl.append("")
    dsl.append("        monolith = softwareSystem \"Modular Monolith\" \"Sistema Central de Mantenimiento y LOTO (.NET 10)\" {")
    
    # We map C4 Components to Components within a default Container
    dsl.append("            appContainer = container \"Backend Web API\" \"Modular Monolith Runtime\" \".NET 10\" {")
    
    dsl.append("                group \"Driving Adapters\" {")
    for c in boundaries["Driving Adapter"]:
        dsl.append(f"                    {c['Component ID']} = component \"{c['Component or Functional Port']}\" \"{c['Technical Responsibility']}\" \"{c['Port / Interface']}\" \"ComponentShape\"")
    dsl.append("                }")
    
    dsl.append("                group \"Application Core\" {")
    for c in boundaries["Primary Port (In)"]:
        dsl.append(f"                    {c['Component ID']} = component \"{c['Component or Functional Port']}\" \"{c['Technical Responsibility']}\" \"{c['Port / Interface']}\" \"ComponentShape\"")
    for c in boundaries["Domain Service"]:
        tag = "Broker" if "bus" in c['Component ID'].lower() else "ComponentShape"
        dsl.append(f"                    {c['Component ID']} = component \"{c['Component or Functional Port']}\" \"{c['Technical Responsibility']}\" \"{c['Port / Interface']}\" \"{tag}\"")
    for c in boundaries["Secondary Port (Out)"]:
        dsl.append(f"                    {c['Component ID']} = component \"{c['Component or Functional Port']}\" \"{c['Technical Responsibility']}\" \"{c['Port / Interface']}\" \"ComponentShape\"")
    dsl.append("                }")
    
    dsl.append("                group \"Driven Adapters\" {")
    for c in boundaries["Driven Adapter"]:
        dsl.append(f"                    {c['Component ID']} = component \"{c['Component or Functional Port']}\" \"{c['Technical Responsibility']}\" \"{c['Port / Interface']}\" \"ComponentShape\"")
    dsl.append("                }")
    
    dsl.append("            }")
    dsl.append("        }")
    dsl.append("")
    
    dsl.append("        # Relationships")
    for r in relationships:
        src = r['Caller ID']
        dest = r['Callee ID']
        tech = r['Protocol / Technology']
        desc = r['Technical Description']
        dsl.append(f"        {src} -> {dest} \"{desc}\" \"{tech}\"")
        
    dsl.append("    }")
    dsl.append("")
    dsl.append("    views {")
    dsl.append("        component appContainer \"ComponentDiagram\" {")
    dsl.append("            include *")
    for c in boundaries["Client Application"]:
        dsl.append(f"            include {c['Component ID']}")
    for c in boundaries["External System"]:
        dsl.append(f"            include {c['Component ID']}")
    dsl.append("            autoLayout lr")
    dsl.append("        }")
    dsl.append("        styles {")
    dsl.append("            element \"Database\" {")
    dsl.append("                shape Cylinder")
    dsl.append("            }")
    dsl.append("            element \"Mobile\" {")
    dsl.append("                shape MobileDevicePortrait")
    dsl.append("            }")
    dsl.append("            element \"WebBrowser\" {")
    dsl.append("                shape WebBrowser")
    dsl.append("            }")
    dsl.append("            element \"Broker\" {")
    dsl.append("                shape Pipe")
    dsl.append("            }")
    dsl.append("            element \"ComponentShape\" {")
    dsl.append("                shape Component")
    dsl.append("            }")
    dsl.append("            element \"Element\" {")
    dsl.append("                metadata false")
    dsl.append("            }")
    dsl.append("        }")
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
