# 🛠️ Docs-as-Code Automation and Generators

This directory contains the support scripts for synchronization and automated generation of Markdown documents from tabular master data (`requirements/data/`).

## `generate_design_tokens.py`

Generates `ui-ux/assets/tokens.css` and `ui-ux/assets/tokens_penpot.json` from
the tables and definitions in `ui-ux/DT-UI-DS-DOC-001.md`. Both are generated
artifacts; changes must be made in the Markdown source document and then
regenerated:

```bash
python3 scripts/generate_design_tokens.py
```

The JSON file uses the DTCG/Design Tokens format compatible with Penpot, with
semantic references such as `{Primitives.gray-900}`.

It also accepts explicit paths for validations or alternative sources:

```bash
python3 scripts/generate_design_tokens.py \
	--source ui-ux/DT-UI-DS-DOC-001.md \
	--target ui-ux/assets/tokens.css \
	--penpot-target ui-ux/assets/tokens_penpot.json
```

---

## 📌 `generate_requirements_docs.py`

Unified script responsible for compiling:
1. **Transversal Requirements (`TR-001` to `TR-011` and `INDEX.md`):** Generated in `requirements/common/`.
2. **User Stories:** Grouped by module/epic (`adm/`, `inv/`, `mtto/`, `vis/`) in `requirements/user-stories/`.

### 🛡️ Safe by Default (Dry-Run)

The script **never overwrites files by default**. If executed without parameters, it operates in simulation mode (*dry-run*), printing to the console what files would be created or modified.

---

## 🚀 Usage Examples

### 1. Simulation (Check what would change)
```bash
python scripts/generate_requirements_docs.py
```

### 2. View Exact Line-by-Line Differences (Diff)
```bash
python scripts/generate_requirements_docs.py --diff
```

### 3. Apply Changes to Disk (Real Write)
```bash
python scripts/generate_requirements_docs.py --write
```

### 4. Generate and Update the Transversal Requirements `INDEX.md`
```bash
python scripts/generate_requirements_docs.py --write --write-index
```

### 5. Filter by Specific Module (e.g., only Maintenance and Inventory)
```bash
python scripts/generate_requirements_docs.py --modules MTTO INV --write
```

### 6. Filter by Specific ID (e.g., a single User Story or a single TR)
```bash
python scripts/generate_requirements_docs.py --ids MTTO-001 TR-003 --write
```

### 7. Generate Only User Stories or Only Transversal Requirements
```bash
# Only User Stories
python scripts/generate_requirements_docs.py --only-us --write

# Only Transversal Requirements (COMMON)
python scripts/generate_requirements_docs.py --only-tr --write
```

---

## 📂 Default Path Mapping

| Source (Master CSV) | Generated Destination (Markdown) | Format / Content |
| :--- | :--- | :--- |
| `requirements/data/srs.csv` + `transversal-requirements.csv` | `requirements/common/TR-xxx.md` | Transversal context, FR/NFR tables, and normative references. |
| `requirements/data/srs.csv` + `user-stories.csv` + `gherkin.csv` | `requirements/user-stories/{epic}/{US-ID}.md` | As/I want/So that, Gherkin acceptance criteria, FR/NFR tables, and traceability. |
