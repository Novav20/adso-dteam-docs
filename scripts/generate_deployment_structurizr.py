import re

def extract_tables(md_text):
    sec2_start = md_text.find("## 2. Matriz Jerárquica de Nodos")
    sec3_start = md_text.find("## 3. Matriz de Conectividad")
    sec4_start = md_text.find("## 4. Mecanismo de Seguridad")
    
    sec2_text = md_text[sec2_start:sec3_start]
    sec3_text = md_text[sec3_start:sec4_start]
    
    return sec2_text, sec3_text

def parse_deployment_structurizr(md_path, out_dsl_path):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    sec2_text, sec3_text = extract_tables(content)
    
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
                
                if c4_type == "Node":
                    if comp_id not in nodes:
                        nodes[comp_id] = {
                            "id": comp_id, "name": comp_name, "tech": tech,
                            "parent": parent_id, "components": [], "children": []
                        }
                    else:
                        nodes[comp_id]["name"] = comp_name
                        nodes[comp_id]["tech"] = tech
                        nodes[comp_id]["parent"] = parent_id
                        
                    if parent_id not in nodes:
                        nodes[parent_id] = {
                            "id": parent_id, "name": node_name, "tech": node_platform,
                            "parent": None, "components": [], "children": []
                        }
                    if comp_id not in nodes[parent_id]["children"]:
                        nodes[parent_id]["children"].append(comp_id)
                    continue

                if parent_id not in nodes:
                    nodes[parent_id] = {
                        "id": parent_id, "name": node_name, "tech": node_platform,
                        "parent": None, "components": [], "children": []
                    }
                else:
                    if not nodes[parent_id].get("name"):
                        nodes[parent_id]["name"] = node_name
                    if not nodes[parent_id].get("tech"):
                        nodes[parent_id]["tech"] = node_platform

                comp_obj = {
                    "id": comp_id,
                    "name": comp_name,
                    "tech": tech,
                    "desc": resp
                }
                nodes[parent_id]["components"].append(comp_obj)
                components[comp_id] = comp_obj

    connections = []
    for line in sec3_text.split("\n"):
        line = line.strip()
        if line.startswith("|") and not line.startswith("| Componente Origen") and not line.startswith("| :---"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 8:
                src_comp = parts[0]
                dst_comp = parts[2]
                protocol = parts[4]
                port = parts[5]
                security = parts[6]
                purpose = parts[7]

                tech_str = f"{protocol}"
                if port: tech_str += f" ({port})"
                if security and security != "Ninguno (Interno)": tech_str += f" - {security}"
                connections.append({"src": src_comp, "dst": dst_comp, "desc": purpose, "tech": tech_str})

    dsl = []
    dsl.append('workspace "System Deployment Model" {')
    dsl.append('    model {')
    dsl.append('        sys = softwareSystem "System Software" {')
    for c_id, c in components.items():
        dsl.append(f'            {c_id} = container "{c["name"]}" "{c["desc"]}" "{c["tech"]}"')
    dsl.append('        }')
    dsl.append('')
    dsl.append('        # Relationships')
    for conn in connections:
        dsl.append(f'        {conn["src"]} -> {conn["dst"]} "{conn["desc"]}" "{conn["tech"]}"')
    dsl.append('')
    dsl.append('        # Deployment Environment')
    dsl.append('        production = deploymentEnvironment "Production" {')
    
    def render_deployment_node(node_id, indent=0):
        node = nodes[node_id]
        sp = "            " + ("    " * indent)
        lines = []
        lines.append(f'{sp}deploymentNode "{node["name"]}" "{node["tech"]}" {node["id"]} {{')
        for child_id in node["children"]:
            lines.extend(render_deployment_node(child_id, indent + 1))
        for comp in node["components"]:
            lines.append(f'{sp}    containerInstance {comp["id"]}')
        lines.append(f'{sp}}}')
        return lines

    root_nodes = [n_id for n_id, n in nodes.items() if n["parent"] is None]
    for r_id in root_nodes:
        dsl.extend(render_deployment_node(r_id))
    
    dsl.append('        }')
    dsl.append('    }')
    dsl.append('')
    dsl.append('    views {')
    dsl.append('        deployment sys "Production" "DeploymentDiagram" {')
    dsl.append('            include *')
    dsl.append('            autoLayout tb')
    dsl.append('        }')
    dsl.append('        theme default')
    dsl.append('    }')
    dsl.append('}')

    with open(out_dsl_path, "w", encoding="utf-8") as f:
        f.write("\n".join(dsl))
        
if __name__ == '__main__':
    md = 'architecture/views/DT-ARQ-DEP-DOC-001.md'
    dsl = 'architecture/views/DT-ARQ-DEP-001-deployment-model.dsl'
    parse_deployment_structurizr(md, dsl)
    print(f"Generated {dsl}")
