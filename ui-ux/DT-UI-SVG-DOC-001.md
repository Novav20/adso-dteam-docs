---
code: DT-UI-SVG-DOC-001
version: 2
date: 2026-10-09
status: APPROVED
author: Juan David Julio Serrano
standard:
  - ISO 13567-1/2 (Organization and naming of layers for CAD)
  - AIA CAD Layer Guidelines v5
  - ISO 14224:2016 (Collection and exchange of reliability and maintenance data for equipment)
  - ANSI/ISA-5.1-2009 (Instrumentation Symbols and Identification)
  - OSHA 29 CFR 1910.106 (Flammable Liquids)
  - API Standard 650/620
---

# DT-UI-SVG-DOC-001: SVG Ingestion, Layering, and Spatial Data Contract

## 1. Purpose
This normative standard defines the structural, spatial, semantic, and security contract for ingesting 2D vector CAD/BIM layouts into the DTEAM Digital Twin rendering engine. 

To bridge the gap between industrial CAD standards and High-Performance Human-Machine Interface (HPHMI) web rendering, DTEAM enforces strict XML structures, predefined layer groups, semantic pruning, and ISO 14224 data binding. This standard filters out greenfield CAD bloat and prioritizes brownfield Management of Change (MOC) integrities.

## 2. Ingestion & Sanitization Invariants

Before client-side DOM insertion, all SVG documents MUST pass the following automated server-side checks:

1. **Security Sanitization:** Complete removal of all executable `<script>` elements, `javascript:` URIs, inline event attributes (`onclick`, etc.), external entities (`<!ENTITY>`), and proprietary CAD manifests (e.g., Adobe XMP, C2PA).
2. **Performance Ceiling:** The parsed DOM tree MUST NOT exceed 15,000 nodes to guarantee $\ge$ 60 FPS rendering under alarm conditions.
3. **MOC Header Validation:** Verification of cryptographic signatures and MOC tracking metadata against the active plant database.

## 3. Structural Root Contract (`<svg>`)

The root `<svg>` element MUST define Management of Change (MOC) attributes, viewport scaling, and semantic zoom controllers.

```xml
<svg 
  xmlns="http://www.w3.org/2000/svg" 
  viewBox="0 0 10000 10000" 
  class="dt-canvas zoom-l1"
  data-moc-id="MOC-2026-0042"
  data-rev-number="2.0"
  data-checksum-sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  data-scale-ratio="0.1"
  data-units="meters"
>
```

*(Note: Global geodesic EPSG coordinates are deliberately omitted. Spatial mapping is handled via local metric scaling to ensure broad compatibility with standard plot plans).*

## 4. Layer Architecture

All graphics MUST be mapped into seven immutable `<g>` (group) elements. Z-index is strictly dictated by DOM order (bottom to top). Unstructured paths outside these groups will be rejected by the ingestion engine.

| SVG Group ID (`id`) | CSS Class | Scope & Governance |
| :--- | :--- | :--- |
| `L-CIVL-BOTM` | `.dt-layer-civil-botm` | Civil works, terrain, roads, concrete pads, and secondary containment dikes. |
| `L-MECH-EQPM` | `.dt-layer-mech-eqpm` | Process equipment: storage tanks, vessels, pumps. |
| `L-PIPE-PROC` | `.dt-layer-pipe-proc` | Process piping lines and manifolds. |
| `L-INSP-INST` | `.dt-layer-insp-inst` | Instrumentation nodes and control loops (ANSI/ISA-5.1). |
| `L-FIRE-PROT` | `.dt-layer-fire-prot` | Fixed fire protection: deluge rings, foam lines, hydrants (NFPA 15). |
| `L-ELEC-HAZ` | `.dt-layer-elec-haz` | Hazardous area electrical classification zones (Class I Div 1/2). |
| `L-ANNO-TEXT` | `.dt-layer-anno-text` | Static labels, grid lines, and the calibration vector. |

## 5. Process Safety Geometry

Geometry representing physical safety boundaries MUST embed structural data attributes allowing the Digital Twin engine to compute spatial interlocks dynamically.

### 5.1 Secondary Containment Dikes (`L-CIVL-BOTM`)
```xml
<polygon 
  id="DIKE-101" 
  class="dt-safety-containment"
  data-dike-vol-m3="14500.0" 
  data-dike-height-m="1.80" 
  data-submerged-vol-m3="1200.0" 
  points="..." 
/>
```

### 5.2 Storage Tank Shells (`L-MECH-EQPM`)
Tanks MUST carry their physical diameter to allow dynamic, software-driven calculation of OSHA 1910.106 $D/6$ shell-to-shell buffers. (Explicit dashed buffer paths drawn in CAD are forbidden to reduce DOM bloat).

```xml
<circle 
  cx="5000" cy="5000" r="160" 
  class="dt-equipment-unit"
  data-shell-diam-m="32.0" 
  data-tank-height-m="14.0" 
  data-design-std="API-650"
/>
```

## 6. Telemetry Binding & Identity Schema (ISO 14224)

Live SCADA telemetry and interactive UI components MUST decouple physical hardware from spatial plant slots.

- `data-func-loc`: (Level 5) The immutable Functional Location slot (e.g., `TFA-CSS-TK-0101`). This is the **primary** binding key.
- `data-equip-id`: (Level 6) The physical asset serial/ID currently occupying the slot (e.g., `EQ-TK-101-A`). Used for maintenance tracking.
- `data-isa-tag`: For instrumentation loops (e.g., `LIT-101A`).

*Example:*
```xml
<g id="TK-0101" data-func-loc="TFA-CSS-TK-0101" data-equip-id="EQ-TK-101-A" class="dt-interactive">
  <!-- Tank graphics -->
</g>
```

## 7. Element Lifecycle (AIA v5 Status)

For brownfield MOC integrity, elements MUST carry a `data-status` attribute to track as-built lifecycle states without destructive DOM deletion:

- `data-status="N"`: New Work (Scheduled installation).
- `data-status="E"`: Existing to Remain (Current as-built).
- `data-status="D"`: Demolish / Decommissioned (Visible as ghosted/dashed geometry).
- `data-status="M"`: Moved / Relocated Asset.

## 8. Web Performance & Semantic Zoom

DTEAM employs a CSS-driven Semantic Zoom approach. To prevent browser DOM thrashing and memory leaks, hidden zoom tiers MUST be stripped from the layout rendering pass using `display: none !important`. 

Using `opacity: 0` to hide dense CAD elements is strictly forbidden.

```css
/* Hard DOM Layout Pruning Rules */
.dt-zoom-l2, .dt-zoom-l3 {
  display: none !important;
}

/* Medium Zoom */
svg.zoom-l2 .dt-zoom-l2,
svg.zoom-l3 .dt-zoom-l2 {
  display: inline !important;
}

/* High Zoom */
svg.zoom-l3 .dt-zoom-l3 {
  display: inline !important;
}
```

## 9. Spatial Calibration

Layer `L-ANNO-TEXT` MUST contain a calibration vector validating the metric translation from SVG User Units to real-world dimensions.

```xml
<g id="L-ANNO-TEXT" class="dt-layer-anno-text">
  <line x1="0" y1="0" x2="1000" y2="0" id="CALIBRATION-VECTOR" data-real-meters="100.0" />
</g>
```
