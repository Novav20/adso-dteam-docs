import re
import os

def snake_to_pascal(snake_str):
    if not snake_str: return ""
    components = snake_str.split('_')
    # Special rules: id -> Id, but if table name equipment_units -> EquipmentUnit
    return "".join(x.capitalize() for x in components)

def singularize(word):
    if word.endswith('ies'): return word[:-3] + 'y'
    if word.endswith('sses'): return word[:-2]
    if word.endswith('s'): return word[:-1]
    return word

def map_pg_type_to_csharp(pg_type):
    pg_type = pg_type.upper()
    if 'UUID' in pg_type: return 'Guid'
    if 'VARCHAR' in pg_type or 'TEXT' in pg_type: return 'string'
    if 'INT' in pg_type or 'SERIAL' in pg_type: return 'int'
    if 'DECIMAL' in pg_type or 'NUMERIC' in pg_type: return 'decimal'
    if 'BOOL' in pg_type: return 'bool'
    if 'DATE' in pg_type or 'TIMESTAMP' in pg_type: return 'DateTime'
    if 'JSON' in pg_type: return 'string'
    return 'string'

def generate_domain_puml():
    erd_md = "domain-models/entity-relationship/DT-ERD-DOC-001.md"
    dm_md = "domain-models/class/DT-DM-DOC-002.md"
    out_puml = "domain-models/class/DT-DM-001-domain-model.puml"
    
    classes = {}
    
    # Parse ERD for properties
    with open(erd_md, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    in_table = False
    for line in lines:
        line = line.strip()
        if line.startswith("| Entidad |"):
            in_table = True
            continue
        if line.startswith("| ---"):
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 6:
                table_name = parts[0]
                column_name = parts[1]
                pg_type = parts[2]
                nullable = parts[3]
                
                class_name = singularize(snake_to_pascal(table_name))
                prop_name = snake_to_pascal(column_name)
                csharp_type = map_pg_type_to_csharp(pg_type)
                if nullable == "NULL" and csharp_type != "string":
                    csharp_type += "?"
                    
                if class_name not in classes:
                    classes[class_name] = {"props": [], "methods": [], "deps": []}
                    
                classes[class_name]["props"].append(f"+ {csharp_type} {prop_name} {{get; set;}}")
                
                # Try to infer relationship
                if column_name.endswith("_id") and column_name != "id":
                    target_table = column_name[:-3]
                    target_class = singularize(snake_to_pascal(target_table))
                    if target_class != class_name:
                        classes[class_name]["deps"].append(target_class)
                        
        elif not line.strip():
            in_table = False
            
    # Parse DM for methods
    try:
        with open(dm_md, "r", encoding="utf-8") as f:
            dm_content = f.read()
            
        # Regex to find sections like ### 2.1. `FunctionalLocation` (`<<Aggregate Root>>`)
        # and then the table below it
        sections = re.split(r'###\s+\d+\.\d+\.\s+`([^`]+)`', dm_content)
        
        for i in range(1, len(sections), 2):
            class_name = sections[i]
            content = sections[i+1]
            
            # Find the table in this content
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
                        method_signature = parts[0]
                        # Remove backticks from method signature if any
                        method_signature = method_signature.replace('`', '')
                        if class_name not in classes:
                            classes[class_name] = {"props": [], "methods": [], "deps": []}
                        classes[class_name]["methods"].append(f"+ {method_signature}")
                elif not line.strip() and in_table:
                    in_table = False
    except Exception as e:
        print(f"Could not parse DM doc fully: {e}")

    # Generate PlantUML
    puml = []
    puml.append("@startuml DT-DM-001-domain-model")
    puml.append("skinparam classAttributeIconSize 0")
    puml.append("skinparam monochrome true")
    puml.append("hide circle")
    puml.append("")
    
    # Ensure classes with methods are printed even if they don't have props
    for class_name, data in classes.items():
        puml.append(f"class {class_name} {{")
        for prop in data["props"]:
            puml.append(f"    {prop}")
        if data["methods"]:
            puml.append("    --")
        for meth in data["methods"]:
            puml.append(f"    {meth}")
        puml.append("}")
        puml.append("")
        
    puml.append("' Relationships")
    for class_name, data in classes.items():
        for dep in set(data["deps"]):
            if dep in classes:
                puml.append(f"{class_name} --> {dep}")
                
    puml.append("")
    puml.append("@enduml")
    
    with open(out_puml, "w", encoding="utf-8") as f:
        f.write("\n".join(puml))
        
    print(f"Generated {out_puml}")

if __name__ == '__main__':
    generate_domain_puml()
