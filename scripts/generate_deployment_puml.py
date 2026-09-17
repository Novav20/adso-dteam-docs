import re
import os

md_path = "architecture/views/DT-ARQ-DEP-DOC-001.md"
puml_path = "architecture/views/DT-ARQ-DEP-001-deployment-model.puml"

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract tables
sec2_start = content.find("## 2. Matriz Jerárquica de Nodos")
sec3_start = content.find("## 3. Matriz de Conectividad")
sec4_start = content.find("## 4. Mecanismo de Seguridad")

sec2_text = content[sec2_start:sec3_start]
sec3_text = content[sec3_start:sec4_start]

# Parse Nodes & Components
# Structure:
# nodes[node_id] = { 'label': ..., 'type': ..., 'parent': ..., 'components': [], 'children_nodes': [] }
nodes = {}
components = {}

for line in sec2_text.split("\n"):
    line = line.strip()
    if line.startswith("|") and not line.startswith("| ID Nodo") and not line.startswith("| :---"):
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) >= 8:
            parent_id = parts[0]
            node_name = parts[1]
            node_platform = parts[2]
            comp_id = parts[3]
            comp_name = parts[4]
            c4_type = parts[5]
            tech = parts[6]
            resp = parts[7]

            # If the component is marked as a nested Node
            if c4_type == "Node":
                if comp_id not in nodes:
                    nodes[comp_id] = {
                        "id": comp_id,
                        "label": comp_name,
                        "platform": tech,
                        "parent": parent_id,
                        "components": [],
                        "children_nodes": []
                    }
                else:
                    nodes[comp_id]["label"] = comp_name
                    nodes[comp_id]["platform"] = tech
                    nodes[comp_id]["parent"] = parent_id

                if parent_id not in nodes:
                    nodes[parent_id] = {
                        "id": parent_id,
                        "label": node_name,
                        "platform": node_platform,
                        "parent": None,
                        "components": [],
                        "children_nodes": []
                    }
                if comp_id not in nodes[parent_id]["children_nodes"]:
                    nodes[parent_id]["children_nodes"].append(comp_id)
                continue

            # Standard node registration
            if parent_id not in nodes:
                nodes[parent_id] = {
                    "id": parent_id,
                    "label": node_name,
                    "platform": node_platform,
                    "parent": None,
                    "components": [],
                    "children_nodes": []
                }
            else:
                if not nodes[parent_id]["label"]:
                    nodes[parent_id]["label"] = node_name
                if not nodes[parent_id]["platform"]:
                    nodes[parent_id]["platform"] = node_platform

            comp_obj = {
                "id": comp_id,
                "name": comp_name,
                "type": c4_type,
                "tech": tech,
                "desc": resp,
                "node_id": parent_id
            }
            nodes[parent_id]["components"].append(comp_obj)
            components[comp_id] = comp_obj

# Parse Connections
connections = []
for line in sec3_text.split("\n"):
    line = line.strip()
    if line.startswith("|") and not line.startswith("| Componente Origen") and not line.startswith("| :---"):
        parts = [p.strip() for p in line.split("|")[1:-1]]
        if len(parts) >= 8:
            src_comp = parts[0]
            src_node = parts[1]
            dst_comp = parts[2]
            dst_node = parts[3]
            protocol = parts[4]
            port = parts[5]
            security = parts[6]
            purpose = parts[7]

            tech_str = f"{protocol} ({port})" if port else protocol
            if security and security != "Ninguno (Interno)":
                tech_str += f" - {security}"

            connections.append({
                "src": src_comp,
                "dst": dst_comp,
                "desc": purpose,
                "tech": tech_str
            })

# Generate C4-PlantUML
puml = []
puml.append("@startuml DT-ARQ-DEP-001-deployment-model")
puml.append("!include <C4/C4_Deployment>")
puml.append("")
puml.append("' Visual configurations")
puml.append("skinparam defaultFontName \"Segoe UI\"")
puml.append("skinparam wrapWidth 250")
puml.append("skinparam maxMessageSize 180")
puml.append("LAYOUT_WITH_LEGEND()")
puml.append("")
puml.append("title Vista de Despliegue Físico y Topología de Red - DTEAM (ISO/IEC 42010)")
puml.append("")

def render_node(node_id, indent=0):
    node = nodes[node_id]
    sp = "    " * indent
    lines = []
    lines.append(f'{sp}Deployment_Node({node["id"]}, "{node["label"]}", "{node["platform"]}") {{')
    
    # Render child nodes first
    for ch_id in node["children_nodes"]:
        lines.extend(render_node(ch_id, indent + 1))
        
    # Render components
    for c in node["components"]:
        csp = "    " * (indent + 1)
        macro = "ContainerDb" if c["type"] == "ContainerDb" else "Container"
        lines.append(f'{csp}{macro}({c["id"]}, "{c["name"]}", "{c["tech"]}", "{c["desc"]}")')
        
    lines.append(f'{sp}}}')
    return lines

# Root nodes (parent is None or not in nodes)
root_nodes = [n_id for n_id, n in nodes.items() if n["parent"] is None]

for r_id in root_nodes:
    puml.extend(render_node(r_id))
    puml.append("")

puml.append("' Relaciones y Canales de Comunicación")
for conn in connections:
    puml.append(f'Rel({conn["src"]}, {conn["dst"]}, "{conn["desc"]}", "{conn["tech"]}")')

puml.append("")
puml.append("@enduml")

with open(puml_path, "w", encoding="utf-8") as f:
    f.write("\n".join(puml))

print("Diagram generated successfully at:", puml_path)
