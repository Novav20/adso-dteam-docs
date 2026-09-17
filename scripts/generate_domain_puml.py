import re

def snake_to_pascal(snake_str):
    if not snake_str: return ""
    components = snake_str.split('_')
    return "".join(x.capitalize() for x in components)

def singularize(word):
    if word.endswith('ies'): return word[:-3] + 'y'
    if word.endswith('sses'): return word[:-2]
    if word.endswith('s') and not word.endswith('ss'): return word[:-1]
    return word

def map_pg_type_to_agnostic(pg_type):
    pg_type = pg_type.upper()
    if 'UUID' in pg_type: return 'UUID'
    if 'VARCHAR' in pg_type or 'TEXT' in pg_type: return 'String'
    if 'INT' in pg_type or 'SERIAL' in pg_type: return 'Integer'
    if 'DECIMAL' in pg_type or 'NUMERIC' in pg_type: return 'Decimal'
    if 'BOOL' in pg_type: return 'Boolean'
    if 'DATE' in pg_type or 'TIMESTAMP' in pg_type: return 'DateTime'
    if 'JSON' in pg_type: return 'JSON'
    return 'String'

def generate_domain_puml():
    erd_md = "domain-models/entity-relationship/DT-ERD-DOC-001.md"
    dm_md = "domain-models/class/DT-DM-DOC-002.md"
    out_puml = "domain-models/class/DT-DM-001-domain-model.puml"
    
    classes = {}
    schemas = {}
    current_schema = "Common"
    
    # 1. Parse ERD for properties and schemas
    with open(erd_md, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    in_table = False
    in_relations = False
    relations = []
    
    for line in lines:
        line = line.strip()
        
        # Schema Detection
        if line.startswith("### ") and "Esquema" in line:
            current_schema = line.split("Esquema")[-1].strip()
            continue
            
        if line.startswith("## 4. Matriz de Relaciones"):
            in_relations = True
            in_table = False
            continue
            
        if line.startswith("| Entidad |") or line.startswith("| Entidad Origen"):
            in_table = True
            continue
            
        if line.startswith("| ---"):
            continue
            
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if not in_relations and len(parts) >= 6:
                table_name = parts[0]
                column_name = parts[1]
                pg_type = parts[2]
                nullable = parts[3]
                
                class_name = singularize(snake_to_pascal(table_name))
                prop_name = snake_to_pascal(column_name)
                agnostic_type = map_pg_type_to_agnostic(pg_type)
                
                # C# nullability equivalent for UML representation
                if nullable == "NULL" and agnostic_type not in ["String", "JSON"]:
                    agnostic_type += "?"
                    
                if class_name not in classes:
                    classes[class_name] = {"props": [], "methods": [], "schema": current_schema}
                    
                classes[class_name]["props"].append(f"+ {prop_name}: {agnostic_type}")
                
            elif in_relations and len(parts) >= 5:
                parent_table = parts[0]
                card = parts[1]
                child_table = parts[2]
                verb = parts[3]
                cascade = parts[4]
                
                parent_class = singularize(snake_to_pascal(parent_table))
                child_class = singularize(snake_to_pascal(child_table))
                
                c_parts = card.split(" : ")
                card_parent = f'"{c_parts[0].strip()}"' if len(c_parts) > 1 else '""'
                card_child = f'"{c_parts[1].strip()}"' if len(c_parts) > 1 else '""'
                
                arrow = "*--" if cascade == "CASCADE" else "o--" if cascade == "SET NULL" else "-->"
                relations.append(f"{parent_class} {card_parent} {arrow} {card_child} {child_class} : {verb}")
                
        elif not line.strip():
            in_table = False
            
    # 2. Parse DM for methods
    try:
        with open(dm_md, "r", encoding="utf-8") as f:
            dm_content = f.read()
            
        sections = re.split(r'###\s+\d+\.\d+\.\s+`([^`]+)`', dm_content)
        for i in range(1, len(sections), 2):
            class_name = sections[i]
            content = sections[i+1]
            
            lines = content.split('\n')
            in_table = False
            for line in lines:
                line = line.strip()
                if line.startswith("| Método"):
                    in_table = True
                    continue
                if line.startswith("| :---"):
                    continue
                if in_table and line.startswith("|"):
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 1:
                        method_signature = parts[0].replace('`', '')
                        if class_name not in classes:
                            classes[class_name] = {"props": [], "methods": [], "schema": "Common"}
                        classes[class_name]["methods"].append(f"+ {method_signature}")
                elif not line.strip() and in_table:
                    in_table = False
    except Exception as e:
        pass

    # 3. Generate PlantUML
    puml = []
    puml.append("@startuml DT-DM-001-domain-model")
    puml.append("skinparam classAttributeIconSize 0")
    puml.append("skinparam packageStyle rectangle")
    puml.append("hide circle")
    puml.append("")
    
    # Colors for schemas
    schema_colors = {
        "tax": "#E8F4F8",
        "mtto": "#FFF0E6",
        "inv": "#E6F4EA",
        "vis": "#F3E5F5",
        "adm": "#FFF3CD"
    }
    
    schemas_group = {}
    for c_name, data in classes.items():
        s = data["schema"]
        if s not in schemas_group: schemas_group[s] = []
        schemas_group[s].append((c_name, data))
        
    for schema, cls_list in schemas_group.items():
        color = schema_colors.get(schema, "#FFFFFF")
        puml.append(f'package "{schema}" <<Folder>> {color} {{')
        for class_name, data in cls_list:
            puml.append(f"    class {class_name} {{")
            for prop in data["props"]:
                puml.append(f"        {prop}")
            if data["methods"]:
                puml.append("        --")
            for meth in data["methods"]:
                puml.append(f"        {meth}")
            puml.append("    }")
        puml.append("}")
        puml.append("")
        
    puml.append("' Relationships")
    for rel in relations:
        puml.append(rel)
                
    puml.append("")
    puml.append("@enduml")
    
    with open(out_puml, "w", encoding="utf-8") as f:
        f.write("\n".join(puml))
        
if __name__ == '__main__':
    generate_domain_puml()
