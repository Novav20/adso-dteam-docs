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
    dm_doc1 = "domain-models/class/DT-DM-DOC-001.md"
    dm_doc2 = "domain-models/class/DT-DM-DOC-002.md"
    out_puml = "domain-models/class/DT-DM-DOC-001.puml"
    
    classes = {}
    current_schema = "Common"
    current_table = None
    
    # 0. Parse DM-DOC-001 for stereotypes
    try:
        with open(dm_doc1, "r", encoding="utf-8") as f:
            dm1_lines = f.readlines()
        in_table = False
        for line in dm1_lines:
            line = line.strip()
            if "| Entidad" in line and "| Estereotipo DDD" in line:
                in_table = True
                continue
            if line.startswith("| ---") or line.startswith("| -") or line.startswith("| :---") or line.startswith("| :"):
                continue
            if in_table and line.startswith("|"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 2:
                    cls_name = parts[0]
                    # Fix manual mismatches between DM concepts and physical ERD entities
                    if cls_name == "Permission":
                        cls_name = "RolePermission"
                    stereotype = parts[1]
                    if cls_name not in classes:
                        classes[cls_name] = {"props": [], "methods": [], "schema": "Common", "stereotype": stereotype}
                    else:
                        classes[cls_name]["stereotype"] = stereotype
            elif not line.strip() and in_table:
                in_table = False
    except Exception as e:
        pass
    
    # 1. Parse ERD for properties and schemas
    with open(erd_md, "r", encoding="utf-8") as f:
        erd_lines = f.readlines()
        
    in_table = False
    in_relations = False
    relations = []
    
    for line in erd_lines:
        line = line.strip()
        
        # Schema Detection
        if line.startswith("### ") and "Schema" in line:
            current_schema = line.split("Schema")[-1].strip().replace("`", "")
            continue
            
        # Table Detection
        m_table = re.match(r'^#### 3\.\d+\.\d+ (\w+)', line)
        if m_table:
            current_table = m_table.group(1)
            continue
            
        if line.startswith("## 4. Referential Relationships and Cascading (FKs)"):
            in_relations = True
            in_table = False
            continue
            
        if line.startswith("| Physical Field |") or line.startswith("| Parent Table"):
            in_table = True
            continue
            
        if line.startswith("| ---") or line.startswith("| :---") or line.startswith("| :"):
            continue
            
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if not in_relations and len(parts) >= 5:
                table_name = current_table
                column_name = parts[0]
                pg_type = parts[1]
                nullable = parts[2]
                
                class_name = singularize(snake_to_pascal(table_name))
                prop_name = snake_to_pascal(column_name)
                agnostic_type = map_pg_type_to_agnostic(pg_type)
                
                # C# nullability equivalent for UML representation
                if nullable == "NULL" and agnostic_type not in ["String", "JSON"]:
                    agnostic_type += "?"
                    
                if class_name not in classes:
                    classes[class_name] = {"props": [], "methods": [], "schema": current_schema, "stereotype": "Entity"}
                else:
                    classes[class_name]["schema"] = current_schema
                    
                classes[class_name]["props"].append(f"- {prop_name}: {agnostic_type}")
                
            elif in_relations and len(parts) >= 6:
                parent_table = parts[0]
                card = parts[1]
                child_table = parts[2]
                verb = parts[3]
                cascade = parts[4] # on delete action
                on_update = parts[5]
                
                parent_class = singularize(snake_to_pascal(parent_table))
                child_class = singularize(snake_to_pascal(child_table))
                
                # Convert N to * for UML standard
                card = card.replace("N", "*")
                c_parts = card.split(" : ")
                card_parent = f'"{c_parts[0].strip()}"' if len(c_parts) > 1 else '""'
                card_child = f'"{c_parts[1].strip()}"' if len(c_parts) > 1 else '""'
                
                arrow = "*--" if cascade == "CASCADE" else "o--" if cascade == "SET NULL" else "-->"
                relations.append(f"{parent_class} {card_parent} {arrow} {card_child} {child_class} : {verb}")
                
        elif not line.strip():
            in_table = False
            
    # 2. Parse DM for methods
    try:
        with open(dm_doc2, "r", encoding="utf-8") as f:
            dm_content = f.read()
            
        sections = re.split(r'###\s+\d+\.\d+\.\s+`([^`]+)`', dm_content)
        for i in range(1, len(sections), 2):
            class_name = sections[i]
            content = sections[i+1]
            
            lines = content.split('\n')
            in_table = False
            for line in lines:
                line = line.strip()
                if line.startswith("| Method |"):
                    in_table = True
                    continue
                if line.startswith("| :---"):
                    continue
                if in_table and line.startswith("|"):
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 1:
                        method_signature = parts[0].replace('`', '')
                        if class_name not in classes:
                            classes[class_name] = {"props": [], "methods": [], "schema": "Common", "stereotype": "Entity"}
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
    
    # Layout and routing improvements
    puml.append("skinparam linetype ortho")
    puml.append("skinparam nodesep 80")
    puml.append("skinparam ranksep 80")
    puml.append("")
    
    puml.append("skinparam class {")
    puml.append("    BackgroundColor #E3F2FD")
    puml.append("    BorderColor #1565C0")
    puml.append("    ArrowColor #1565C0")
    puml.append("    FontName Arial")
    puml.append("    HeaderFontStyle bold")
    puml.append("}")
    puml.append("")
    
    schema_titles = {
        "tax": "Asset Taxonomy (ISO 14224)",
        "mtto": "Maintenance Management (MTTO)",
        "inv": "Resource Control (INV)",
        "vis": "Digital Twin Convergence (VIS)",
        "adm": "Safety and Governance (ADM)"
    }
    
    schemas_group = {}
    for c_name, data in classes.items():
        s = data["schema"]
        
        # Don't render phantom classes from DM docs that weren't physically mapped in ERD
        if s == "Common" and len(data["props"]) == 0 and len(data["methods"]) == 0:
            continue
            
        if s not in schemas_group: schemas_group[s] = []
        schemas_group[s].append((c_name, data))
        
    for schema, cls_list in schemas_group.items():
        title = schema_titles.get(schema, schema)
        puml.append(f'package "{title}" <<Folder>> #F0F0F0 {{')
        for class_name, data in cls_list:
            stereotype = f' <<{data["stereotype"]}>>' if data.get("stereotype") else ""
            puml.append(f"    class {class_name}{stereotype} {{")
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
