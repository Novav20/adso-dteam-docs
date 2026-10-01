import os
import re
import argparse

def parse_enums(dm_doc_path):
    enums = {}
    if not os.path.exists(dm_doc_path): return enums
    with open(dm_doc_path, 'r', encoding='utf-8') as f: lines = f.readlines()
        
    current_entity = None
    current_field = None
    
    for line in lines:
        match = re.match(r'^#### \d+\.\d+ (\w+)\.(\w+)', line)
        if match:
            current_entity = match.group(1)
            current_field = match.group(2)
            
            snake_entity = re.sub(r'(?<!^)(?=[A-Z])', '_', current_entity).lower()
            plural_snake_entity = pluralize(snake_entity)
            snake_field = re.sub(r'(?<!^)(?=[A-Z])', '_', current_field).lower()
            
            key = f"{plural_snake_entity}.{snake_field}"
            if key not in enums: enums[key] = []
            if snake_field not in enums: enums[snake_field] = []
            continue
            
        if current_entity and line.startswith('|') and not line.startswith('| ---') and not line.startswith('| Value') and not line.startswith('| Code'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3 and parts[1]:
                val = parts[1]
                snake_entity = re.sub(r'(?<!^)(?=[A-Z])', '_', current_entity).lower()
                plural_snake_entity = pluralize(snake_entity)
                snake_field = re.sub(r'(?<!^)(?=[A-Z])', '_', current_field).lower()
                key = f"{plural_snake_entity}.{snake_field}"
                
                if val not in enums[key]: enums[key].append(val)
                if val not in enums[snake_field]: enums[snake_field].append(val)
    return enums

def parse_ul(ul_doc_path):
    ul_glossary = {}
    if not os.path.exists(ul_doc_path): return ul_glossary
    with open(ul_doc_path, 'r', encoding='utf-8') as f: lines = f.readlines()
    for line in lines:
        if line.startswith('|') and not line.startswith('| ---') and not line.startswith('| :---') and not line.startswith('| English'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                term = parts[1].replace('**', '').split('(')[0].strip()
                definition = parts[2].replace("'", "''")
                
                snake_term = term.lower().replace(' ', '_')
                ul_glossary[snake_term] = definition
                ul_glossary[pluralize(snake_term)] = definition
    return ul_glossary

def pluralize(word):
    if word.endswith('y'): return word[:-1] + 'ies'
    elif word.endswith('s'): return word + 'es'
    return word + 's'

def parse_referential_actions(erd_doc_path):
    actions = {}
    with open(erd_doc_path, 'r', encoding='utf-8') as f: lines = f.readlines()
    in_ref_table = False
    for line in lines:
        if line.startswith('## 4. Referential Relationships'): in_ref_table = True; continue
        if line.startswith('## 5.'): break
        if in_ref_table and line.startswith('|') and not line.startswith('| ---') and not line.startswith('| Parent Table') and not line.startswith('| :---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                parent, child, on_delete, on_update = parts[1], parts[3], parts[5], parts[6]
                actions[f"{child}->{parent}"] = {'delete': on_delete, 'update': on_update}
    return actions

def parse_erd(erd_doc_path, enums, ref_actions, ul_glossary, include_comments):
    with open(erd_doc_path, 'r', encoding='utf-8') as f: lines = f.readlines()

    schemas = []
    schema_set = set()
    tables = {}
    current_schema = current_table = None

    for line in lines:
        if line.startswith('## '):
            current_table = None
            continue
            
        schema_match = re.match(r'^### \d+\.\d+ Schema `(\w+)`', line)
        if schema_match:
            current_schema = schema_match.group(1)
            if current_schema not in schema_set:
                schemas.append(current_schema)
                schema_set.add(current_schema)
            current_table = None
            continue

        table_match = re.match(r'^#### \d+\.\d+\.\d+ (\w+)', line)
        if table_match and current_schema:
            current_table = table_match.group(1)
            tables[f"{current_schema}.{current_table}"] = []
            continue

        if current_table and line.startswith('|') and not line.startswith('| ---') and not line.startswith('| Physical Field'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                tables[f"{current_schema}.{current_table}"].append({
                    'field': parts[1], 'type': parts[2], 'nullability': parts[3],
                    'constraints': parts[4], 'default': parts[5], 'comment': parts[6]
                })

    sql = "-- ==========================================\n"
    sql += "-- AUTO-GENERATED DDL SCRIPT\n"
    sql += "-- ==========================================\n\n"

    for schema in schemas: sql += f"CREATE SCHEMA IF NOT EXISTS {schema};\n"
    sql += "\n"

    foreign_keys = []
    indexes = []

    for schema in schemas:
        schema_tables = [t for t in tables.keys() if t.startswith(f"{schema}.")]
        if schema_tables:
            sql += f"-- ==========================================\n"
            sql += f"-- SCHEMA: {schema.upper()}\n"
            sql += f"-- ==========================================\n\n"

        for table_name in schema_tables:
            columns = tables[table_name]
            raw_table = table_name.split('.')[1]
            sql += f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
            
            col_defs, constraints, comments = [], [], []
            table_comment = ul_glossary.get(raw_table, 'Auto-generated from documentation')
            comments.append(f"COMMENT ON TABLE {table_name} IS '{table_comment}';")
            
            for c in columns:
                col_def = f"    {c['field'].ljust(25)} {c['type']}"
                if 'NOT NULL' in c['nullability']: col_def += " NOT NULL"
                if c['default'] and c['default'] not in ['-', 'NULL']: col_def += f" DEFAULT {c['default']}"
                col_defs.append(col_def)
                
                if include_comments and c['comment'] and c['comment'] != '-':
                    clean_comment = c['comment'].replace("'", "''")
                    comments.append(f"COMMENT ON COLUMN {table_name}.{c['field']} IS '{clean_comment}';")
                    
                if 'UNIQUE' in c['constraints']:
                    constraints.append(f"    CONSTRAINT uq_{raw_table}_{c['field']} UNIQUE ({c['field']})")
                if 'CHECK' in c['constraints']:
                    enum_key_specific = f"{raw_table}.{c['field']}"
                    
                    target_enum = None
                    if enum_key_specific in enums and enums[enum_key_specific]:
                        target_enum = enums[enum_key_specific]
                        
                    if target_enum:
                        enum_vals = ", ".join([f"'{v}'" for v in target_enum])
                        constraints.append(f"    CONSTRAINT ck_{raw_table}_{c['field']} CHECK ({c['field']} IN ({enum_vals}))")
                    else:
                        constraints.append(f"    -- CONSTRAINT ck_{raw_table}_{c['field']} CHECK (...) /* Missing explicit enum for {enum_key_specific} */")

                if 'FK' in c['constraints']:
                    indexes.append(f"CREATE INDEX IF NOT EXISTS idx_{raw_table}_{c['field']} ON {table_name} ({c['field']});")
                    
                    parent_base = c['field'].replace('_id', '')
                    parent_table = pluralize(parent_base)
                    
                    if parent_table == 'parents': parent_table = raw_table
                    elif c['field'] == 'subunit_id' and raw_table == 'maintainable_items': parent_table = 'subunits'
                    elif c['field'] == 'equipment_class_id': parent_table = 'equipment_classes'
                    
                    parent_schema = next((t.split('.')[0] for t in tables.keys() if t.split('.')[1] == parent_table), None)
                    
                    if parent_schema:
                        action_key = f"{raw_table}->{parent_table}"
                        on_delete, on_update = "RESTRICT", "CASCADE"
                        if action_key in ref_actions:
                            on_delete, on_update = ref_actions[action_key]['delete'], ref_actions[action_key]['update']
                            
                        fk_name = f"fk_{raw_table}_{parent_base}"
                        foreign_keys.append(
                            f"ALTER TABLE {table_name}\n    ADD CONSTRAINT {fk_name} FOREIGN KEY ({c['field']}) "
                            f"REFERENCES {parent_schema}.{parent_table} (id)\n    ON DELETE {on_delete} ON UPDATE {on_update};"
                        )

                if 'JSONB' in c['type'].upper():
                    indexes.append(f"CREATE INDEX IF NOT EXISTS idx_{raw_table}_{c['field']} ON {table_name} USING GIN ({c['field']} jsonb_path_ops);")

            pk_cols = [c['field'] for c in columns if 'PK' in c['constraints']]
            if pk_cols: constraints.append(f"    CONSTRAINT pk_{raw_table} PRIMARY KEY ({', '.join(pk_cols)})")

            sql += ",\n".join(col_defs)
            if constraints: sql += ",\n\n" + ",\n".join(constraints)
            sql += "\n);\n\n"
            if include_comments: sql += "\n".join(comments) + "\n\n"

    sql += "-- ==========================================\n"
    sql += "-- INDEXES (AUTO-GENERATED HEURISTICS)\n"
    sql += "-- ==========================================\n\n"
    sql += "\n".join(indexes) + "\n\n"

    sql += "-- ==========================================\n"
    sql += "-- FOREIGN KEY CONSTRAINTS (CROSS-SCHEMA)\n"
    sql += "-- ==========================================\n\n"
    sql += "\n\n".join(foreign_keys) + "\n\n"

    return sql

def main():
    parser = argparse.ArgumentParser(description="Generate SQL DDL from Markdown Docs-as-Code.")
    parser.add_argument("--comments", action="store_true", help="Include COMMENT ON statements in the SQL.")
    args = parser.parse_args()

    erd_doc_path = os.path.join(os.path.dirname(__file__), "..", "domain-models", "entity-relationship", "DT-ERD-DOC-001.md")
    dm_doc_path = os.path.join(os.path.dirname(__file__), "..", "domain-models", "class", "DT-DM-DOC-001.md")
    ul_doc_path = os.path.join(os.path.dirname(__file__), "..", "domain-models", "ubiquitous-language", "DT-UL-DOC-001.md")
    output_path = os.path.join(os.path.dirname(__file__), "..", "domain-models", "entity-relationship", "DT-ERD-DOC-001.sql")
    
    enums = parse_enums(dm_doc_path)
    ref_actions = parse_referential_actions(erd_doc_path)
    ul_glossary = parse_ul(ul_doc_path)
    
    sql_output = parse_erd(erd_doc_path, enums, ref_actions, ul_glossary, args.comments)
    
    with open(output_path, 'w', encoding='utf-8') as f: 
        f.write(sql_output)
        
    print(f"✅ Generated {output_path} successfully. (Comments: {args.comments})")

if __name__ == "__main__": main()
