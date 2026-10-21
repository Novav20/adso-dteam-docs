---
code: DT-UI-SVG-DOC-001
version: 2.1
date: 2026-10-21
status: SUBMITTED_FOR_AUDIT
author: Juan David Julio Serrano
standards:
  - ISO 13567-1/2 (Organization and naming of layers for CAD)
  - AIA CAD Layer Guidelines v5
  - ISO 14224:2016 (Collection and exchange of reliability and maintenance data for equipment)
  - ANSI/ISA-101.01-2015 (Human-Machine Interfaces for Process Automation Systems)
  - ANSI/ISA-5.1-2009 (Instrumentation Symbols and Identification)
  - NFPA 30:2024 (Flammable and Combustible Liquids Code - Spill Containment & Spacing)
  - NFPA 497:2024 (Classification of Flammable Liquids, Gases, or Vapors and Hazardous Locations)
  - OSHA 29 CFR 1910.147 (The Control of Hazardous Energy - Lockout/Tagout)
  - API Standard 650/620 (Welded Tanks for Oil Storage)
---

# DT-UI-SVG-DOC-001: SVG Ingestion, Layering, and Spatial Data Contract (Rev 2.1)

## 1. Purpose & Scope
This normative standard defines the structural, spatial, semantic, and security contract for ingesting 2D vector CAD/BIM layouts (General Arrangement Plot Plans, P&IDs, Hazardous Area Classifications) into the DTEAM Asset Performance Management (APM) and Digital Twin rendering engine.

To bridge the gap between greenfield CAD drafting conventions and High-Performance Human-Machine Interface (HPHMI) runtime execution, DTEAM enforces strict XML structures, predefined layer stacking, progressive disclosure tiers, and ISO 14224 / LOTO / ISA-5.1 data bindings. This specification ensures brownfield Management of Change (MOC) integrity, eliminates visual clutter, and guarantees deterministic client-side spatial resolution.

---

## 2. Ingestion & Sanitization Invariants

Before client-side DOM insertion or database persistence, all incoming SVG documents MUST pass the following automated server-side verification pipeline:

1. **Security Sanitization:** Complete elimination of executable `<script>` elements, `javascript:` protocol URIs, inline DOM event handlers (`onclick`, `onload`, etc.), external XML entities (`<!ENTITY>`), foreign namespaces, and proprietary CAD binary metadata manifests (e.g., Adobe XMP, C2PA, Autodesk DWF blobs).
2. **Performance Ceiling (DOM Budget):** The total parsed DOM tree count MUST NOT exceed **15,000 nodes** to ensure continuous 60 FPS vector manipulation under real-time telemetry streaming and multi-permit spatial queries.
3. **MOC Cryptographic Payload Checksum:** The root element MUST carry a SHA-256 digest (`data-checksum-sha256`) computed over the raw sanitized XML template (excluding the checksum attribute itself). The ingestion pipeline re-calculates and asserts this checksum against the active MOC registry.
4. **Coordinate System & Metric Scale:** All geometry MUST be expressed in SVG User Space coordinates normalized to a metric scale ratio defined in the root header (`data-scale-ratio` and `data-units="meters"`). Global geodesic EPSG transformations are decoupled and computed at runtime via the root calibration vector.

---

## 3. Structural Root Contract (`<svg>`)

The root `<svg>` element MUST define Management of Change (MOC) attributes, spatial bounding limits, and initial semantic zoom classification:

```xml
<svg 
  xmlns="http://www.w3.org/2000/svg" 
  viewBox="0 0 2000 1500" 
  class="dt-canvas zoom-l1"
  data-moc-id="MOC-2026-0042"
  data-rev-number="2.1"
  data-checksum-sha256="892a420e807f2f98..."
  data-scale-ratio="0.2"
  data-units="meters"
  aria-label="General Arrangement Plot Plan — Terminal Digital Twin"
>
  <defs>
    <!-- Pattern hatches for civil surfaces: gravel, concrete, asphalt -->
    <pattern id="hatch-concrete" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="var(--dt-color-border-subtle, #B9C0CC)" stroke-width="1" />
    </pattern>
  </defs>
  <style>
    /* Normative HPHMI rendering & progressive disclosure styles */
  </style>
  <!-- Seven Immutable Layer Groups in Physical Depth Stacking Order -->
</svg>
```

---

## 4. Layer Architecture & Physical Stacking Order

In SVG 1.1 and 2.0 specifications, rendering order is governed strictly by the **Painter's Algorithm** (DOM document tree order from top to bottom). All graphics MUST be grouped into exactly seven immutable `<g>` elements.

To prevent sub-surface conduits and spatial boundary envelopes from visually slicing across physical machinery, layers MUST follow this normative physical depth sequence:

```
[Top View Overlay]       7. L-ANNO-TEXT   (Labels, tags, metric calibration)
                         6. L-INSP-INST   (ISA-5.1 bubbles, impulse leads)
                         5. L-PIPE-PROC   (Above-ground process piping, valves)
                         4. L-MECH-EQPM   (Opaque equipment: tanks, pumps, skids)
                         3. L-FIRE-PROT   (Firewater ring mains, hydrants)
                         2. L-ELEC-HAZ    (Underground feeders, NFPA 497 zones)
[Bottom Foundation]      1. L-CIVL-BOTM   (Terrain, roads, basin, dike walls)
```

| Order | SVG Group ID (`id`) | CSS Class | Scope, Governance & Occlusion Behavior |
| :---: | :--- | :--- | :--- |
| **1** | `L-CIVL-BOTM` | `.dt-layer-civil-botm` | **Sub-surface Ground & Civil Baseline:** Terrain plot limits, access roads, retention/OWS basins, foundation slab footprints, secondary containment dikes, and reference coordinate grids. |
| **2** | `L-ELEC-HAZ` | `.dt-layer-elec-haz` | **Underground Electrical & Spatial Envelopes:** Underground MV/LV power feeder duct banks (`FDR-*`) and virtual NFPA 497 Class I, Div 1/2 hazardous area boundary classification envelopes (`HAZ-ZONE-*`). Sits *under* physical equipment. |
| **3** | `L-FIRE-PROT` | `.dt-layer-fire-prot` | **Emergency Fire Protection Network:** Fire-water tank suction/discharge headers, underground looped perimeter ring mains (`RINGM`), road branch loops, addressable hydrants (`FH-*`), and monitor towers (`FM-*`). |
| **4** | `L-MECH-EQPM` | `.dt-layer-mech-eqpm` | **Physical Maintainable Equipment:** Primary process machinery (API 650 storage tanks, API 610 transfer pump skids, NFPA 20 fire pumps, custody transfer LACT skids, crossover manifolds, truck loading bays, and substation buildings). Opaque fills mask underlying conduits. |
| **5** | `L-PIPE-PROC` | `.dt-layer-pipe-proc` | **Above-Ground Process Piping Corridors:** Product sleeperways (`SN`, `SA`, `SB`, `SR`), multi-headers (Header A/B), expansion loops, tank suction/discharge stubs, and mechanical LOTO isolation valves (`CMP-ISO-VALVE`). Sits *on top* of equipment nozzles. |
| **6** | `L-INSP-INST` | `.dt-layer-insp-inst` | **Instrumentation & Control Loops:** ANSI/ISA-5.1 field instrumentation bubbles (`CMP-INST-NODE`), stanchions, and physical sensor/impulse lead lines (`L-INSP-LEADS`). |
| **7** | `L-ANNO-TEXT` | `.dt-layer-anno-text` | **Annotation Callouts & Metric Reference:** Equipment primary tags, road markers, gate operational roles, title blocks, and the metric calibration vector (`CALIBRATION-VECTOR`). |

*Rules:*
1. Unstructured vector elements outside these seven groups will be rejected by the ingestion engine.
2. Group IDs are case-sensitive and immutable.
3. Solid equipment bodies in `L-MECH-EQPM` MUST use opaque fills (`var(--dt-color-canvas-equip-shell)`) to naturally occlude sub-surface conduits (`L-ELEC-HAZ`) running directly beneath machinery foundation pads.

---

## 5. Process Safety & Spatial Containment Geometry

### 5.1 Secondary Containment Dikes (`L-CIVL-BOTM`)
Secondary containment bund walls MUST be modeled as closed `<polygon>` elements embedding NFPA 30 structural containment attributes:

```xml
<polygon 
  id="DIKE-SW" 
  class="dt-interactive dt-safety-containment"
  data-zone-id="SW"
  data-dike-id="DIKE-SW"
  data-largest-tank="TK-0101"
  data-largest-vol-m3="3758.0"
  data-dike-req-110pct-m3="4133.8"
  data-dike-vol-m3="8374.3"
  data-dike-height-m="2.40"
  data-submerged-vol-m3="285.5"
  data-status="E"
  points="320.5,140.2 680.1,140.2 680.1,480.6 320.5,480.6"
/>
```

*Required Attributes:*
* `data-largest-tank`: Tag of the largest single tank enclosed within the bund.
* `data-largest-vol-m3`: Net liquid volume ($V$) of the largest tank in cubic meters ($m^3$).
* `data-dike-req-110pct-m3`: Statutory minimum containment volume ($1.10 \times V$).
* `data-dike-vol-m3`: Effective net containment volume after deducting common submerged foundations.
* `data-dike-height-m`: Design dike wall height in meters ($m$).

### 5.2 Hazardous Area Classification Envelopes (`L-ELEC-HAZ`)
Virtual safety boundaries representing flammable gas or vapor release envelopes MUST be modeled as closed polygonal or radial paths per NFPA 497:

```xml
<polygon 
  id="HAZ-ZONE-PMP" 
  class="dt-haz-envelope dt-zoom-l2"
  data-zone-id="PMP"
  data-standard="NFPA-497"
  data-division="DIV_2"
  data-gas-group="GROUP_D"
  data-temp-class="T3"
  stroke="var(--dt-color-canvas-steel, #5C677D)"
  stroke-width="1.4"
  stroke-dasharray="14 5 3 5"
  fill="none"
  points="..."
/>
```

*Rules:*
* Envelopes are tagged with `class="dt-zoom-l2"` to avoid cluttering Level 1 macro terminal views.
* Dashed lines must use subdued neutral tones (`var(--dt-color-canvas-steel)`) to avoid conflicting with active alarm graphics.

---

## 6. EAM Telemetry Binding & Identity Schema (ISO 14224)

Every maintainable, addressable, or interactive plant entity MUST decouple its physical hardware serial number from its immutable functional location slot per ISO 14224 §A.2:

```xml
<g 
  id="tag-P-0101A"
  data-cmp-id="CMP-EQP-PUMP"
  data-func-loc="TFA-CSS-P-0101A"
  data-equip-id="EQ-P-0101A-A"
  data-service-fluid="Hydrocarbon Transfer"
  data-power-mcc="MCC-2"
  data-design-std="API-610"
  data-status="E"
  class="dt-interactive equipment-hotspot"
>
  <!-- Opaque foundation, casing, impeller circle, motor body -->
</g>
```

### Component Hierarchy (`data-cmp-id`)
The ingestion engine maps vector entities into standardized APM/EAM component classes:

| `data-cmp-id` | Category | Target Physical Entity |
| :--- | :--- | :--- |
| `CMP-EQP-TANK` | Mechanical | Atmospheric storage tank (API 650/620, Cone/Floating Roof). |
| `CMP-EQP-PUMP` | Mechanical | Process centrifugal hydrocarbon transfer pump skid (API 610). |
| `CMP-EQP-FWP` | Mechanical / Fire | High-pressure diesel/electric firewater pump (NFPA 20). |
| `CMP-EQP-MANIFOLD` | Mechanical / Piping | Header distribution and crossover manifold block. |
| `CMP-EQP-SKID` | Process Unit | Custody transfer metering LACT skid, VRU, or compressor skid. |
| `CMP-EQP-BAY` | Loading / Civil | High-volume bottom-loading road tanker bay or gantry island. |
| `CMP-EQP-BLDG` | Civil / Electrical | Substation (SUB), Motor Control Center (MCC), FAR, or MCR. |
| `CMP-EQP-CIVIL` | Civil / Safety | Retention / Oily Water Sewer (OWS) basin, secondary containment dike. |
| `CMP-EQP-FIRE` | Fire Protection | Addressable hydrant (`FH-*`), foam monitor (`FM-*`), deluge valve. |
| `CMP-ISO-VALVE` | Isolation Point | Manual OS&Y gate, globe, or ball block valve used in LOTO boundary. |
| `CMP-ISO-BREAKER` | Isolation Point | 480V/4.16kV electrical MCC circuit breaker racked-out for LOTO. |
| `CMP-INST-NODE` | Instrumentation | Field transmitter, switch, or analyzer loop node (ANSI/ISA-5.1). |

---

## 7. Lockout / Tagout (LOTO) Isolation Point Contract

Isolation points representing mechanical energy dissipation or electrical de-energization for hazardous work permits (OSHA 1910.147 / VIS-011) MUST adhere to the following schema:

### 7.1 Mechanical Valves (`CMP-ISO-VALVE`)
```xml
<g 
  id="iso-V-0101A-IN"
  data-cmp-id="CMP-ISO-VALVE"
  data-isolation-tag="V-0101A-IN"
  data-isolation-type="MECHANICAL_VALVE"
  data-role="SUCTION_BLOCK"
  data-target-equip="P-0101A"
  data-func-loc="TFA-CSS-P-0101A"
  data-source-bldg="BLD-MCC-02"
  data-normal-pos="OPEN"
  data-loto-pos="CLOSED_CHAIN_LOCKED"
  data-try-out-method="CASING_BLEED_ZERO_PRESSURE"
  data-status="E"
  class="dt-interactive dt-isolation-point dt-zoom-l2"
  transform="translate(1088.5 765.4) rotate(-41)"
>
  <path d="M-3.6,-2.5 L3.6,2.5 L3.6,-2.5 L-3.6,2.5 Z" fill="#FFFFFF" stroke="#2B2D42" stroke-width="0.9" />
</g>
```

### 7.2 Electrical MCC Breakers (`CMP-ISO-BREAKER`)
```xml
<g 
  id="iso-MCC-P0101A"
  data-cmp-id="CMP-ISO-BREAKER"
  data-isolation-tag="MCC-P0101A"
  data-isolation-type="ELECTRICAL_BREAKER"
  data-role="MCC_BREAKER"
  data-target-equip="P-0101A"
  data-func-loc="TFA-CSS-P-0101A"
  data-source-bldg="BLD-MCC-02"
  data-normal-pos="ENERGIZED"
  data-loto-pos="RACKED_OUT_LOCKED"
  data-try-out-method="LOCAL_START_PUSHBUTTON_DEAD_TEST"
  data-status="E"
  class="dt-interactive dt-isolation-point dt-zoom-l3"
  transform="translate(1420.2 510.8)"
>
  <!-- Breaker graphic -->
</g>
```

*Spatial Rule:*
Casing drain/bleed valves (`V-XXXX-BLD`) used for zero-energy verification MUST be piped into the clear operator walkway away from moving shaft couplings and motor housings.

---

## 8. Instrumentation & Control Loops (ANSI/ISA-5.1-2009)

Field instrumentation nodes in layer `L-INSP-INST` represent real-time SCADA/DCS/SIS telemetry tags:

```xml
<g 
  id="inst-PIT-0101A"
  data-cmp-id="CMP-INST-NODE"
  data-isa-tag="PIT-0101A"
  data-target-equip="P-0101A"
  data-func-loc="TFA-CSS-P-0101A"
  data-equip-id="EQ-P-0101A-A"
  data-signal-type="DISCHARGE_PRESSURE"
  data-unit="psig"
  data-normal-val="118.5"
  data-alarm-hh="145.0"
  data-safety-critical="TRUE"
  data-status="E"
  class="dt-interactive dt-instrument dt-zoom-l2"
>
  <!-- SIS dual-shape: Outer square for safety critical SIS, inner circle with divider -->
  <rect x="1165.2" y="802.4" width="9.2" height="9.2" fill="#E8EAED" stroke="#2B2D42" stroke-width="1.0" />
  <circle cx="1169.8" cy="807.0" r="4.6" fill="#FFFFFF" stroke="#2B2D42" stroke-width="1.0" />
  <line x1="1165.2" y1="807.0" x2="1174.4" y2="807.0" stroke="#2B2D42" stroke-width="0.6" />
  <text x="1169.8" y="806.2" font-size="3.0" text-anchor="middle" font-weight="bold" fill="#2B2D42">PIT</text>
  <g class="dt-zoom-l3">
    <text x="1169.8" y="810.1" font-size="2.5" text-anchor="middle" fill="#2B2D42">0101A</text>
  </g>
</g>
```

*Rules:*
1. **Loop Decoupling:** General BPCS transmitters use standard circular bubbles ($\varnothing 9.2$). Safety-Critical SIS loops (e.g., API 2350 overfill switches `LSHH`, hazardous gas detectors `AIT`) MUST enclose the bubble within a bounding square.
2. **Impulse Lead Lines (`L-INSP-LEADS`):** Instruments mounted on stanchions off equipment skids MUST carry fine dashed lead lines (`stroke-dasharray="3 2"`, width `0.7px`) linking the process physical tap point to the instrument bubble centroid.

---

## 9. High-Performance HMI (HPHMI) & Typography (ANSI/ISA-101.01)

### 9.1 Palette Governance & Alarm Reservation
In strict compliance with ANSI/ISA-101.01 §6.2, steady-state digital twin layouts MUST employ neutral, low-contrast canvas palettes. The use of pure red (`#FF0000` / `#EF4444`) and warning amber (`#FFA500` / `#F59E0B`) for static piping, equipment fills, or civil boundaries is **strictly prohibited**; these hues are reserved exclusively for active, unacknowledged alarm states.

| Token | Light Canvas (`#EDF2F4`) | Dark Canvas (`#0F172A`) | Role & Conformance Threshold |
| :--- | :--- | :--- | :--- |
| `INK` | `#2B2D42` (11.97:1 AAA) | `#FAFBFC` (16.2:1 AAA) | Primary text labels, structural equipment outlines, major headers. |
| `STEEL` | `#5C677D` (4.79:1 AA) | `#94A3B8` (7.14:1 AAA) | Secondary headers, civil curbs, fire mains, instrument impulse leads. |
| `MID` | `#8D99AE` (2.39:1 Aux) | `#64748B` (3.92:1 AA) | Auxiliary grid lines, concrete hatch dividers, inactive zone bounds. |
| `SHELL` | `#FAFBFC` | `#1E293B` | Opaque equipment body fills (tanks, pump bodies, building roofs). |

*Contrast Rule:*
Text labels MUST achieve a minimum WCAG 2.1 AA relative luminance contrast ratio of $\ge 4.5:1$ against their immediate background. Graphical line elements MUST achieve $\ge 3.0:1$.

### 9.2 Non-Scaling Vector Stroke Halos
Raster drop-shadow filters (`filter: drop-shadow(...)`) cause excessive GPU fill-rate penalties and are forbidden. When text must cross dense underlying geometry (such as tank radial rafters or sleeperway pipe clusters), legibility is guaranteed via **Non-Scaling Vector Stroke Halos**:

```css
/* Micro vector stroke halos for dense background isolation */
.dt-halo-text {
  paint-order: stroke fill;
  stroke: var(--dt-color-canvas-equip-shell, #FAFBFC);
  stroke-width: 1.2px;
  vector-effect: non-scaling-stroke;
  stroke-linejoin: round;
}

.dt-corridor-text {
  paint-order: stroke fill;
  stroke: var(--dt-color-bg-canvas, #EDF2F4);
  stroke-width: 1.2px;
  vector-effect: non-scaling-stroke;
  stroke-linejoin: round;
}
```

*Invariants:*
* Global text strokes on `.dt-canvas text` are prohibited; halos MUST be scoped explicitly via `.dt-halo-text` or `.dt-corridor-text`.
* `vector-effect: non-scaling-stroke` MUST be specified so the mask remains a constant 1.2 screen pixels at any zoom scale ($1\times$ to $15\times$).

---

## 10. Progressive Disclosure & Viewport Kinematics

### 10.1 ISA-101 Semantic Zoom Tiers
To prevent operator visual overload, elements MUST declare semantic visibility tiers:

```
Level 1: Macro Terminal Overview  (Scale < 1.60x)
  ├── Site plot boundaries, perimeter roads, retention basin
  ├── Diked tank farm envelopes (DIKE-*) and gross capacities
  └── Primary equipment tags (TK-0101, BLD-SUB-01)

Level 2: Subsystem & Units         (1.60x <= Scale < 2.80x)
  ├── Sleeperway multi-headers (Header A/B, expansion loops)
  ├── Tank dimensions (Ø18m FLOATING ROOF) and stair treads
  ├── Mechanical LOTO isolation valves (CMP-ISO-VALVE)
  └── Primary field instrumentation nodes (PIT, LIT, LSHH)

Level 3: Micro Equipment Detail   (Scale >= 2.80x)
  ├── Casing bleeders, drain hubs, flange pairs, check valves
  ├── ISA-5.1 loop sub-numbers (0101A) and impulse lead lines
  ├── Electrical MCC circuit breaker nodes (CMP-ISO-BREAKER)
  └── Motor terminal wiring, bearing lube points, bolt pitches
```

### 10.2 Smooth Opacity Transitions
Abrupt visual popping via `display: none` is forbidden during continuous zooming. Progressive disclosure MUST transition smoothly using CSS opacity and visibility:

```css
/* Progressive disclosure with smooth opacity interpolation */
.dt-zoom-l2, .dt-zoom-l3 {
  transition: opacity 0.28s cubic-bezier(0.4, 0, 0.2, 1), visibility 0.28s;
}

.zoom-l1 .dt-zoom-l2,
.zoom-l1 .dt-zoom-l3 {
  opacity: 0 !important;
  visibility: hidden !important;
  pointer-events: none !important;
}

.zoom-l2 .dt-zoom-l3 {
  opacity: 0 !important;
  visibility: hidden !important;
  pointer-events: none !important;
}

.zoom-l2 .dt-zoom-l2 {
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
}

.zoom-l3 .dt-zoom-l2,
.zoom-l3 .dt-zoom-l3 {
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
}
```

---

## 11. Spatial Metric Calibration

Layer `L-ANNO-TEXT` MUST contain a hidden metric calibration vector. The client-side spatial resolution engine measures this vector's length in SVG user units to calculate the precise real-world meter-to-pixel ratio:

```xml
<g id="L-ANNO-TEXT" class="dt-layer-anno-text">
  <line 
    x1="0" y1="0" x2="1000" y2="0" 
    id="CALIBRATION-VECTOR" 
    data-real-meters="200.0" 
    stroke="none" 
    fill="none" 
    style="display:none;" 
  />
  <!-- Annotation labels -->
</g>
```

$$\text{Scale Ratio } K = \frac{\text{data-real-meters}}{\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}} = \frac{200.0}{1000} = 0.20 \text{ m/unit}$$

---

## 12. Automated Ingestion Pipeline (AutoCAD Normalization)

When importing raw industrial CAD models (AutoCAD Model Space DXF/DWG/SVG exports), the DTEAM server ingestion pipeline applies the following deterministic transformations:

1. **Layer Canonicalization:** Maps legacy AutoCAD layers (e.g., `0`, `CIVIL-ROADS`, `EQUIP-TANK`, `INST-TXT`) into the 7 standard groups according to ISO 13567 naming rules.
2. **ACI Color Mapping:** Converts legacy AutoCAD Color Index (ACI) primaries (ACI 1 Red, ACI 4 Cyan, ACI 6 Magenta) into HPHMI tokens (`STEEL`, `INK`, `MID`), stripping bright static hues.
3. **Polyline Closure & Miter Normalization:** Closes open boundary polygons and replaces zero-radius sharp corners with standard corner fillets ($R \ge 4.4\text{ m}$) at road junctions.
4. **Data Schedule Re-synchronization:** Binds incoming equipment graphics to canonical external schedules (`1_functional_zones.csv`, `2_equipment_master.csv`, `3_loto_isolation_points.csv`, `4_instruments_isa51.csv`).
5. **Integrity Sealing:** Re-computes and embeds the SHA-256 payload digest in `data-checksum-sha256`. Documents failing hash validation or DOM node budget ($\le 15,000$) are rejected with an explicit ingestion diagnostic log.
