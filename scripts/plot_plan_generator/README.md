# Plot Plan Generator (`plot_plan_generator`)

Modular Python engine for automated generation of General Arrangement (GA) spatial plot plans and Digital Twin schematics, compliant with industrial standard **`DT-UI-SVG-DOC-001` Rev 2.0** and **High-Performance HMI (ANSI/ISA-101 / Hollifield)** guidelines.

---

## Execution Guide

The generator is structured as an executable Python package (`python3 -m scripts.plot_plan_generator`).

### 1. Basic Command (Standard Prototype Generation)

From the root of the `adso-dteam-docs` repository:

```bash
# Generates the clean L1 plot plan with automatic validation
python3 -m scripts.plot_plan_generator.cli ui-ux/prototype/assets/tfa_terminal_plot_plan.svg --validate
```

### 2. Multi-Zoom Generation (`--all-zooms`)

Concurrently generates macro, intermediate, and micro files (`tfa_terminal_plot_plan.svg`, `_l2.svg`, `_l3.svg`):

```bash
python3 -m scripts.plot_plan_generator.cli ui-ux/prototype/assets/tfa_terminal_plot_plan.svg --all-zooms --validate
```

### 3. HPHMI Dark Mode (`--theme=dark`)

Generates the plot plan using the high-performance night/tablet palette:

```bash
python3 -m scripts.plot_plan_generator.cli assets/tfa_terminal_dark.svg --theme=dark --validate
```

### 4. Engineering CAD Tables Inclusion (`--include-cad-tables`)

By default, Digital Twin plot plans omit static paper-drawing tables. If debugging or printed documentation is required:

```bash
python3 -m scripts.plot_plan_generator.cli assets/tfa_terminal_cad.svg --include-cad-tables --validate
```

### 5. External Theme File Usage (`--theme-file`)

Decouples color tokens from Python code using an external JSON file:

```bash
python3 -m scripts.plot_plan_generator.cli assets/tfa_terminal_custom.svg --theme-file=scripts/plot_plan_generator/themes.json --theme=dark
```

---

## CLI Arguments

| Argument | Type | Default | Description |
| :--- | :---: | :---: | :--- |
| `output_path` | Positional | *(Required)* | Target path for the SVG file (or directory). |
| `--theme` | Option | `light` | Color palette selector (`light` or `dark`). |
| `--theme-file` | Path | `themes.json` | Path to JSON file with theme specification and design tokens. |
| `--include-cad-tables` | Flag | `False` | Includes title block, NFPA 30 bund capacity tables, and static legend. |
| `--validate` | Flag | `False` | Executes topological validation, NFPA 30 spacing, and XML schema conformance. |
| `--all-zooms` | Flag | `False` | Automatically emits semantic `_l2.svg` and `_l3.svg` variants. |

---

## Package Structure

```
plot_plan_generator/
├── __init__.py          # Package metadata.
├── __main__.py          # Entry point for module execution (`python -m`).
├── cli.py               # Command-line argument orchestration.
├── config.py            # Physical constants (0.2 m/unit, 2000x1500), rotation (49 deg), and theme loading.
├── themes.json          # Single Source of Truth for color tokens and mapping to DT-UI-DS-DOC-001.
├── builder.py           # Layer coordinator, XML defs, MOC metadata injection, and CSS styles.
├── core/
│   ├── geometry.py      # UV grid transformations, vector projections, clipping, and miter offsets.
│   └── svg_primitives.py# XML element builders (rect, circle, line, path, text, G).
├── domain/
│   ├── plant_data.py    # Tank Farm Alpha entities (tanks, roads, pipe sleepers, pumps, buildings).
│   ├── process_safety.py# Process rules: NFPA 30 bund capacity (110%) and D/6 separation.
│   └── validation.py    # Geometric assertion suite, pipe connectivity, and XML schema.
└── layers/
    ├── civil.py         # L-CIVL-BOTM: Roads, property boundaries, bunds, pipe sleepers, buildings.
    ├── mechanical.py    # L-MECH-EQPM: API 650 tanks, pump skids, loading bays, stairs.
    ├── piping.py        # L-PIPE-PROC: Main headers with loops, collectors, manifolds, valves.
    ├── fire.py          # L-FIRE-PROT: Firewater ring, FH hydrants, and FM monitor towers.
    └── annotation.py    # L-ANNO-TEXT: 40m grid, equipment tags, dimensions, calibration vector, and CAD tables.
```

---

## Design Token Integration (`themes.json`)

To avoid the fragility of hardcoded hexadecimal colors in code, themes are loaded dynamically from `themes.json`:

1. **Alignment with `DT-UI-DS-DOC-001`:**
   - Every color references the Design System primitive grays (`--dt-primitive-gray-*`).
   - **HPHMI 90/10 Rule:** 100% of static plot plan elements use neutral tones, reserving saturated color exclusively for live operational alarm states.
2. **Physical Materials:**
   - `ASPH`: Asphalt surfaces for roads and maneuvering aprons.
   - `CONC`: Reinforced concrete for bund walls and foundations.
   - `STEEL`: Structural steel for pipe sleepers and gantry beams.
   - `BUNDFILL`: Secondary containment floor.

---

## Ingestion & Quality Contract (`DT-UI-SVG-DOC-001`)

Every SVG emitted by this tool strictly complies with:
- **7 Normative Layers:** `L-CIVL-BOTM`, `L-MECH-EQPM`, `L-INSP-INST`, `L-PIPE-PROC`, `L-FIRE-PROT`, `L-ELEC-HAZ`, `L-ANNO-TEXT`.
- **ISO 14224 Data Binding:** `data-cmp-id`, `data-func-loc`, `data-equip-id`, and `data-status` attributes on all interactive hotspots.
- **MOC Audit:** `<svg>` headers with `data-moc-id`, `data-rev-number`, and `data-checksum-sha256`.
- **Calibration Vector:** Hidden `CALIBRATION-VECTOR` line with `data-real-meters="200.0"` for native client metric scaling.
