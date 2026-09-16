import re
import os

md_file = 'domain-models/entity-relationship/DT-ERD-DOC-001.md'
puml_file = 'domain-models/entity-relationship/DT-ERD-LOG-001-logical-model.puml'

with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

# 1. Parse schemas and tables
schemas = {}
# Find Section 3
sec3_start = md_content.find('## 3. Diccionario de Datos')
sec4_start = md_content.find('## 4. Matriz de Relaciones')

if sec3_start != -1 and sec4_start != -1:
    sec3_content = md_content[sec3_start:sec4_start]
    
    current_schema = None
    for line in sec3_content.split('\n'):
        m_schema = re.match(r'^### 3\.\d+ Esquema (\w+)', line)
        if m_schema:
            current_schema = m_schema.group(1)
            schemas[current_schema] = {}
            continue
            
        if line.startswith('|') and not line.startswith('| Entidad') and not line.startswith('| ---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 6:
                table = parts[1]
                col = parts[2]
                typ = parts[3]
                not_null = parts[4]
                constraints = parts[5]
                
                if current_schema:
                    if table not in schemas[current_schema]:
                        schemas[current_schema][table] = []
                    schemas[current_schema][table].append({
                        'col': col,
                        'typ': typ,
                        'not_null': not_null,
                        'constraints': constraints
                    })

# 2. Parse relationships
relationships = []
sec4_end = md_content.find('## 5. Matriz de Correspondencia')
if sec4_start != -1 and sec4_end != -1:
    sec4_content = md_content[sec4_start:sec4_end]
    for line in sec4_content.split('\n'):
        if line.startswith('|') and not line.startswith('| Entidad Origen') and not line.startswith('| ---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 5:
                parent = parts[1]
                card = parts[2]
                child = parts[3]
                verb = parts[4]
                del_rule = parts[5]
                
                # Map card back to PUML
                if card == '1 : 0..N': rel = '||--o{'
                elif card == '1 : 1..N': rel = '||--|{'
                elif card == '0..1 : 0..1': rel = '|o--o|'
                elif card == '1 : 0..1': rel = '||--o|'
                elif card == '1 : 1': rel = '||--||'
                else: rel = '||--o{' # default
                
                full_verb = verb
                if del_rule:
                    full_verb += f" (ON DELETE {del_rule})"
                    
                relationships.append(f"{parent} {rel} {child} : \"{full_verb}\"")

# 3. Generate PUML
puml_output = "@startuml LogicalModel\n"
puml_output += "!include theme.puml\n\n"

# Packages
schema_names = {
    'tax': 'Taxonomía de Activos (ISO 14224)',
    'mtto': 'Operaciones de Mantenimiento (MTTO)',
    'inv': 'Control de Recursos (INV)',
    'vis': 'Convergencia Gemelo Digital (VIS)',
    'adm': 'Seguridad y Gobernanza (ADM)'
}

for schema, tables in schemas.items():
    pkg_name = schema_names.get(schema, schema.upper())
    puml_output += f"package \"{pkg_name}\" as {schema}_module {{\n"
    for table, cols in tables.items():
        puml_output += f"    entity \"{table}\" as {table} {{\n"
        for c in cols:
            prefix = "* " if c['not_null'] == 'NOT NULL' else ""
            constr = f" <<{c['constraints'].lower()}>>" if c['constraints'] else ""
            puml_output += f"        {prefix}{c['col']} : {c['typ']}{constr}\n"
        puml_output += "    }\n\n"
    puml_output += "}\n\n"

puml_output += "' --- RELACIONES LINEALES ---\n"
for r in relationships:
    puml_output += r + "\n"

puml_output += "\n@enduml\n"

with open(puml_file, 'w', encoding='utf-8') as f:
    f.write(puml_output)

print("Diagram generated successfully.")
