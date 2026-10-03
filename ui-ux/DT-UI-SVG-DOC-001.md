---
code: DT-UI-SVG-DOC-001
version: 0.1
date: 2026-09-29
status: DRAFT
author: Juan David Julio Serrano
standard:
  - ISO 9001:2015 (Documented Information Control)
  - ANSI/ISA-101.01-2015 (Human Machine Interfaces for Process Automation Systems)
  - AIA CAD Layer Guidelines v5 / ISO 13567
  - ISO 14224:2016 (Equipment Taxonomy and Functional Locations)
---

# DT-UI-SVG-DOC-001: SVG Ingestion & Layering Contract

## 1. Purpose
This document defines the strict structural contract for standardizing and ingesting raw 2D vector layouts (exported from CAD, Illustrator, Inkscape, etc.) into the DTEAM Digital Twin rendering engine. 

To bridge the gap between traditional industrial CAD standards (AIA CAD Layer Guidelines / ISO 13567) and web-native rendering, DTEAM enforces a specific XML structure, grouping (`<g>`), and data-attribute schema.

## 2. The Hybrid Workflow
Our asset creation workflow is:
1. **Drafting:** The domain expert draws the physical layout in any vector tool (e.g., Penpot, Inkscape, Vectorizer).
2. **Export:** The file is exported as a raw, unstructured SVG.
3. **Normalization (The Contract):** The raw SVG is structurally refactored (often via automated tooling or AI) to strictly adhere to the rules below.
4. **Ingestion:** The frontend consumes the normalized SVG, applying CSS-driven Semantic Zoom and SignalR telemetry bindings.

## 3. Structural Contract

### 3.1 Document Root
The root `<svg>` MUST contain the base spatial definitions and semantic zoom controllers.

```xml
<svg 
  xmlns="http://www.w3.org/2000/svg" 
  viewBox="0 0 2000 1500" 
  class="dt-canvas zoom-l1" <!-- zoom-l1, zoom-l2, zoom-l3 dynamically applied by JS -->
>
```

### 3.2 Layering Architecture (AIA / ISO 13567 Mapping)
Raw CAD layers must be mapped to specific SVG `<g>` (group) elements. These base layers dictate Z-index and rendering order (bottom to top).

| CAD Standard (AIA) | SVG Group ID | CSS Class | Description |
| :--- | :--- | :--- | :--- |
| `C-ROAD`, `C-TOPO` | `g#L-CIVIL` | `.dt-layer-civil` | Roads, concrete pads, terrain, containment dikes. |
| `S-GRID`, `S-COLS` | `g#L-STRUCT` | `.dt-layer-struct`| Structural supports, pipe racks, stairs. |
| `M-EQPM` | `g#L-MECH` | `.dt-layer-mech` | Tanks, pumps, compressors, vessels. |
| `P-PIPE` | `g#L-PIPE` | `.dt-layer-pipe` | Process piping, valves, manifolds. |
| `E-POWR`, `I-INST` | `g#L-ELEC` | `.dt-layer-elec` | Cable trays, major instrumentation nodes. |
| `A-ANNO` | `g#L-ANNO` | `.dt-layer-anno` | Static text labels, grids. |

*Example:*
```xml
<!-- Base layer for civil engineering / concrete -->
<g id="L-CIVIL" class="dt-layer-civil">
   ...
</g>
```

### 3.3 Semantic Zoom Classes
Elements within layers must dictate *when* they appear based on the current zoom level (ISA-101 spatial context).

- **No zoom class:** Always visible (e.g., major tank outlines).
- **`.dt-zoom-l2`:** Appears at medium zoom (e.g., secondary piping, platforms).
- **`.dt-zoom-l3`:** Appears at maximum zoom (e.g., individual flanges, small pumps, stairs).

*Example:*
```xml
<g id="L-STRUCT">
  <!-- Stairs only visible when zoomed in -->
  <path class="dt-zoom-l3" d="..." /> 
</g>
```

### 3.4 Data Binding & Telemetry (The Digital Twin Link)
For an SVG element to receive live telemetry or respond to user interactions (Contextual Drawers), it MUST contain the following data attributes:

- `data-cmp-id`: The Component ID mapping to the UI Design System (e.g., `CMP-EQP-TANK`).
- `data-tag`: The exact `EquipmentUnit` or `FunctionalLocation` tag from the ISO 14224 domain model (e.g., `TK-101`).

*Example:*
```xml
<g id="L-MECH">
  <!-- An interactive Tank mapped to backend data -->
  <g data-cmp-id="CMP-EQP-TANK" data-tag="TK-101" class="dt-interactive">
    <circle cx="500" cy="500" r="100" />
  </g>
</g>
```

## 4. CSS Interactions
The CSS file uses the parent `.zoom-l*` class on the root SVG to cascade visibility down to the layers.

```css
/* Hide L2 and L3 elements by default */
.dt-zoom-l2, .dt-zoom-l3 {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Reveal L2 elements when canvas is zoomed to L2 or L3 */
svg.zoom-l2 .dt-zoom-l2,
svg.zoom-l3 .dt-zoom-l2 {
  opacity: 1;
  pointer-events: auto;
}

/* Reveal L3 elements only when canvas is zoomed to L3 */
svg.zoom-l3 .dt-zoom-l3 {
  opacity: 1;
  pointer-events: auto;
}
```
