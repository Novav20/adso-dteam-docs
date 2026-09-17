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

def generate_c4_component_puml(md_path, out_puml_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
        
    tables = extract_tables(md_text)
    
    components = parse_table(tables[0])
    relationships = parse_table(tables[1])
    
    puml = []
    puml.append("@startuml DT-ARQ-CMP-001-component-model")
    puml.append("!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml")
    puml.append("")
    puml.append("LAYOUT_WITH_LEGEND()")
    puml.append("title Component Diagram for SENA-Career Monolith")
    puml.append("")
    
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
            # Fallback
            if 'Adapter' in stereo or 'External' in stereo or 'Client' in stereo:
                boundaries["External System"].append(c)
            else:
                boundaries["Domain Service"].append(c)
                
    # Client Applications
    for c in boundaries["Client Application"]:
        puml.append(f"Container({c['ID Componente']}, \"{c['Componente o Puerto Funcional']}\", \"{c['Puerto / Interfaz']}\", \"{c['Responsabilidad Técnica']}\")")
    puml.append("")
        
    puml.append('System_Boundary(monolith, "Modular Monolith (.NET 10)") {')
    
    # Driving Adapters
    puml.append('  Container_Boundary(driving, "Driving Adapters") {')
    for c in boundaries["Driving Adapter"]:
        puml.append(f"    Component({c['ID Componente']}, \"{c['Componente o Puerto Funcional']}\", \"{c['Puerto / Interfaz']}\", \"{c['Responsabilidad Técnica']}\")")
    puml.append('  }')
    puml.append("")
    
    # Application Core
    puml.append('  Container_Boundary(core, "Application Core") {')
    for c in boundaries["Primary Port (In)"]:
        puml.append(f"    Component({c['ID Componente']}, \"{c['Componente o Puerto Funcional']}\", \"{c['Puerto / Interfaz']}\", \"{c['Responsabilidad Técnica']}\")")
    for c in boundaries["Domain Service"]:
        puml.append(f"    Component({c['ID Componente']}, \"{c['Componente o Puerto Funcional']}\", \"{c['Puerto / Interfaz']}\", \"{c['Responsabilidad Técnica']}\")")
    for c in boundaries["Secondary Port (Out)"]:
        puml.append(f"    Component({c['ID Componente']}, \"{c['Componente o Puerto Funcional']}\", \"{c['Puerto / Interfaz']}\", \"{c['Responsabilidad Técnica']}\")")
    puml.append('  }')
    puml.append("")
    
    # Driven Adapters
    puml.append('  Container_Boundary(driven, "Driven Adapters") {')
    for c in boundaries["Driven Adapter"]:
        puml.append(f"    Component({c['ID Componente']}, \"{c['Componente o Puerto Funcional']}\", \"{c['Puerto / Interfaz']}\", \"{c['Responsabilidad Técnica']}\")")
    puml.append('  }')
    
    puml.append('}')
    puml.append("")
    
    # External Systems
    for c in boundaries["External System"]:
        puml.append(f"System_Ext({c['ID Componente']}, \"{c['Componente o Puerto Funcional']}\", \"{c['Puerto / Interfaz']}\")")
    puml.append("")
    
    # Relationships
    for r in relationships:
        src = r['Origen']
        dest = r['Destino']
        tech = r['Protocolo / Interfaz']
        desc = r['Propósito y Descripción']
        puml.append(f"Rel({src}, {dest}, \"{desc}\", \"{tech}\")")
        
    puml.append("")
    puml.append("@enduml")
    
    with open(out_puml_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(puml))
        
if __name__ == '__main__':
    md = 'architecture/views/DT-ARQ-CMP-DOC-001.md'
    puml = 'architecture/views/DT-ARQ-CMP-001-component-model.puml'
    generate_c4_component_puml(md, puml)
    print(f"Generated {puml}")
