#!/usr/bin/env python3
import os
import glob

def build_epic(epic_name, output_filename):
    print(f"Compilando épica: {epic_name}...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    epic_dir = os.path.join(base_dir, epic_name)
    
    index_path = os.path.join(epic_dir, "index.md")
    
    if not os.path.exists(index_path):
        print(f"Error: No se encontró el archivo index.md en {epic_dir}")
        return

    # 1. Leer el index.md
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    # Separar el frontmatter y el cuerpo del index (Changelog)
    parts = index_content.split("---")
    if len(parts) >= 3:
        # parts[1] es el contenido del frontmatter
        frontmatter = "---" + parts[1] + "---\n\n"
        index_body = "---".join(parts[2:]).strip()
    else:
        # Fallback de seguridad si no hay delimitadores válidos
        frontmatter = ""
        index_body = index_content.strip()

    # Inicializar las líneas de salida con el Frontmatter
    output_lines = [frontmatter, "\n"]

    # 2. Buscar y concatenar todos los UC-*.md ordenados alfabéticamente
    uc_files = sorted(glob.glob(os.path.join(epic_dir, "UC-*.md")))
    
    if not uc_files:
        print(f"Advertencia: No se encontraron archivos UC-*.md en {epic_dir}")

    for uc_file in uc_files:
        print(f" -> Añadiendo: {os.path.basename(uc_file)}")
        with open(uc_file, "r", encoding="utf-8") as f:
            output_lines.append(f.read())
            output_lines.append("\n\n---\n\n")

    # 3. Añadir el cuerpo del index.md (Changelog y referencias) al final
    output_lines.append(index_body + "\n")

    # 4. Definir ruta de salida (hacia sena-evidence)
    output_path = os.path.abspath(os.path.join(base_dir, "../../../../SENA-Career/sena-evidence/01-Analysis/AP2-Conceptual-Model/GA2-220501093/AA1/EV02-Use-Cases", output_filename))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(output_lines)
        
    print(f"¡Éxito! Archivo generado en: {output_path}\n")

if __name__ == "__main__":
    build_epic("mtto", "Casos-Uso-MTTO.md")
    build_epic("inv", "Casos-Uso-INV.md")
    build_epic("vis", "Casos-Uso-VIS.md")
    build_epic("adm", "Casos-Uso-ADM.md")