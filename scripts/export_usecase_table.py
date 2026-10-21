#!/usr/bin/env python3
"""
export_usecase_table.py
-----------------------
Utility to export a modern docs-as-code Use Case (YAML frontmatter + Markdown headings)
into the legacy 2-column Markdown table format required for SENA academic evidence deliverables.

Usage:
    python3 export_usecase_table.py --file domain-models/use-cases/inv/UC-INV-025.md
    python3 export_usecase_table.py --file domain-models/use-cases/inv/UC-INV-025.md --output /tmp/UC-INV-025-table.md
"""

import argparse
import os
import re
import sys
import yaml

def parse_usecase(content: str) -> dict:
    """Parses a modern docs-as-code Use Case into structured elements."""
    frontmatter = {}
    body = content

    # Extract YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if fm_match:
        frontmatter_str = fm_match.group(1)
        body = fm_match.group(2)
        try:
            frontmatter = yaml.safe_load(frontmatter_str) or {}
        except Exception as e:
            print(f"[WARN] Failed to parse YAML frontmatter: {e}", file=sys.stderr)

    # Extract sections by heading
    sections = {}
    current_section = None
    current_lines = []

    for line in body.splitlines():
        h2_match = re.match(r"^##\s+(\d+\.\s*)?([A-Za-z0-9\s_-]+)$", line)
        if h2_match:
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = h2_match.group(2).strip()
            current_lines = []
        elif current_section is not None:
            current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    return {
        "frontmatter": frontmatter,
        "sections": sections
    }

def format_cell_markdown_to_table(text: str) -> str:
    """Converts multi-line Markdown text into a single-line table cell representation with <br>."""
    if not text:
        return ""
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    return "<br>".join(lines)

def format_bullet_list_to_html(text: str) -> str:
    """Converts Markdown bullet list to <ul><li>...</li></ul>."""
    items = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("* ") or stripped.startswith("- "):
            items.append(f"<li>{stripped[2:].strip()}</li>")
        elif stripped and items:
            # continuation of previous item
            items[-1] = items[-1][:-5] + " " + stripped + "</li>"
    if items:
        return f"<ul>{''.join(items)}</ul>"
    return format_cell_markdown_to_table(text)

def generate_table_markdown(parsed: dict) -> str:
    """Generates the legacy 2-column SENA Markdown table."""
    fm = parsed["frontmatter"]
    sec = parsed["sections"]

    uc_id = fm.get("id", "UC-UNKNOWN")
    uc_name = fm.get("name", "Unnamed Use Case")
    primary_actor = fm.get("primary_actor", "Unknown Actor")
    secondary_actors = fm.get("secondary_actors", [])
    if isinstance(secondary_actors, list):
        sec_actors_str = ", ".join(secondary_actors)
    else:
        sec_actors_str = str(secondary_actors)

    description = format_cell_markdown_to_table(sec.get("Description", ""))
    preconditions = format_bullet_list_to_html(sec.get("Preconditions", ""))
    main_flow = format_cell_markdown_to_table(sec.get("Main Flow", ""))
    alt_flows = format_cell_markdown_to_table(sec.get("Alternate Flows", ""))
    postconditions = format_bullet_list_to_html(sec.get("Postconditions", ""))
    assoc_reqs = format_cell_markdown_to_table(sec.get("Associated Requirements", ""))

    out = []
    out.append(f"# {uc_id}: {uc_name}\n")
    out.append("## Use Case Template\n")
    out.append("| **Element** | **Detail** |")
    out.append("| :--- | :--- |")
    out.append(f"| **ID** | {uc_id} |")
    out.append(f"| **Name** | {uc_name} |")
    out.append(f"| **Primary Actor** | {primary_actor} |")
    out.append(f"| **Secondary Actors** | {sec_actors_str} |")
    out.append(f"| **Description** | {description} |")
    out.append(f"| **Preconditions** | {preconditions} |")
    out.append(f"| **Main Flow** | {main_flow} |")
    out.append(f"| **Alternate Flows** | {alt_flows} |")
    out.append(f"| **Postconditions** | {postconditions} |")
    out.append(f"| **Associated Requirements** | {assoc_reqs} |")
    out.append("")

    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(description="Export modern Use Case to SENA legacy table format.")
    parser.add_argument("--file", required=True, help="Path to modern UC Markdown file")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        content = f.read()

    parsed = parse_usecase(content)
    table_md = generate_table_markdown(parsed)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(table_md)
        print(f"[OK] Table export written to {args.output}")
    else:
        print(table_md)

if __name__ == "__main__":
    main()
