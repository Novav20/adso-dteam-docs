import re
import os

md_file = 'domain-models/entity-relationship/DT-ERD-DOC-001.md'
dbml_file = 'domain-models/entity-relationship/DT-ERD-LOG-001-logical-model.dbml'

with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

schemas = {}
table_to_schema = {}
sec3_start = md_content.find('## 3. Diccionario de Datos')
sec4_start = md_content.find('## 4. Matriz de Relaciones')

if sec3_start != -1 and sec4_start != -1:
    sec3_content = md_content[sec3_start:sec4_start]
    
    current_schema = None
    current_table = None
    
    for line in sec3_content.split('\n'):
        m_schema = re.match(r'^### 3\.\d+ Esquema \**`?(\w+)`?\**', line)
        if m_schema:
            current_schema = m_schema.group(1)
            schemas[current_schema] = {}
            continue
            
        m_table = re.match(r'^#### 3\.\d+\.\d+ (\w+)', line)
        if m_table:
            current_table = m_table.group(1)
            if current_schema:
                schemas[current_schema][current_table] = []
                table_to_schema[current_table] = current_schema
            continue
            
        if line.startswith('|') and not line.startswith('| Campo') and not line.startswith('| ---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                col = parts[1]
                typ = parts[2]
                not_null = parts[3]
                constraints = parts[4]
                default_val = parts[5]
                just = parts[6]
                
                if current_schema and current_table:
                    schemas[current_schema][current_table].append({
                        'col': col,
                        'typ': typ,
                        'not_null': not_null,
                        'constraints': constraints,
                        'default_val': default_val,
                        'just': just
                    })

relationships = []
sec4_end = md_content.find('## 5. Matriz de Correspondencia')
if sec4_start != -1 and sec4_end != -1:
    sec4_content = md_content[sec4_start:sec4_end]
    for line in sec4_content.split('\n'):
        if line.startswith('|') and not line.startswith('| Entidad Origen') and not line.startswith('| ---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 6:
                parent = parts[1]
                card = parts[2]
                child = parts[3]
                verb = parts[4]
                del_rule = parts[5]
                update_rule = parts[6]
                
                relationships.append({
                    'parent': parent,
                    'card': card,
                    'child': child,
                    'verb': verb,
                    'del_rule': del_rule,
                    'update_rule': update_rule
                })

dbml_output = "Project DT_ERD {\n"
dbml_output += "  database_type: 'PostgreSQL'\n"
dbml_output += "  Note: 'Diccionario de Datos Físico y Relacional (Auto-generado desde Markdown)'\n"
dbml_output += "}\n\n"

for schema, tables in schemas.items():
    dbml_output += f"TableGroup {schema} {{\n"
    for table in tables:
        dbml_output += f"  \"{table}\"\n"
    dbml_output += "}\n\n"

for schema, tables in schemas.items():
    for table, cols in tables.items():
        dbml_output += f"Table \"{table}\" {{\n"
        for c in cols:
            props = []
            if 'PK' in c['constraints']: props.append("pk")
            if 'UNIQUE' in c['constraints']: props.append("unique")
            if c['not_null'] == 'NOT NULL': props.append("not null")
            if c.get('default_val') and c['default_val'] not in ['-', 'NULL']:
                if c['default_val'] == 'FALSE':
                    props.append("default: false")
                elif c['default_val'] == 'TRUE':
                    props.append("default: true")
                elif c['default_val'] in ['0', '1']:
                    props.append(f"default: {c['default_val']}")
                else:
                    props.append(f"default: `{c['default_val']}`")
            
            note_text = c['just'].replace("'", "\\'")
            if note_text: props.append(f"note: '{note_text}'")
            
            props_str = f" [{', '.join(props)}]" if props else ""
            dbml_output += f"  \"{c['col']}\" \"{c['typ']}\"{props_str}\n"
        dbml_output += "}\n\n"

def get_child_fk_col(parent, child, schema_data):
    if parent == child:
        return 'parent_id'
        
    expected_fk = parent
    if expected_fk.endswith('ies'): expected_fk = expected_fk[:-3] + 'y_id'
    elif expected_fk.endswith('es') and not expected_fk.endswith('ses'): expected_fk = expected_fk[:-2] + '_id'
    elif expected_fk.endswith('s') and not expected_fk.endswith('ss'): expected_fk = expected_fk[:-1] + '_id'
    else: expected_fk = expected_fk + '_id'
    
    if expected_fk == 'equipment_classe_id': expected_fk = 'equipment_class_id'
    if expected_fk == 'rol_id': expected_fk = 'role_id'
    if expected_fk == 'work_order_historie_id': expected_fk = 'work_order_history_id'
    
    schema_of_child = table_to_schema.get(child)
    if schema_of_child and child in schema_data[schema_of_child]:
        for c in schema_data[schema_of_child][child]:
            if c['col'] == expected_fk:
                return expected_fk
            elif c['col'] == parent + '_id':
                return parent + '_id'
                
    return expected_fk

dbml_output += "// --- RELACIONES ---\n"
for r in relationships:
    parent = r['parent']
    child = r['child']
    card = r['card']
    
    parent_pk = 'id'
    child_fk = get_child_fk_col(parent, child, schemas)
    
    if card in ['1 : 0..N', '1 : 1..N']: symbol = '<'
    elif card in ['0..1 : 0..1', '1 : 1', '1 : 0..1']: symbol = '-'
    else: symbol = '<'
    
    actions = []
    if r['del_rule']:
        actions.append(f"delete: {r['del_rule'].lower()}")
    if r['update_rule']:
        actions.append(f"update: {r['update_rule'].lower()}")
        
    settings = ""
    if actions:
        settings = f" [{', '.join(actions)}]"
        
    dbml_output += f"Ref: \"{parent}\".\"{parent_pk}\" {symbol} \"{child}\".\"{child_fk}\"{settings}\n"

with open(dbml_file, 'w', encoding='utf-8') as f:
    f.write(dbml_output)

print("DBML Diagram generated successfully.")
