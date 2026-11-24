---
code: DT-UI-SVG-DOC-001
version: 2.3
date: 2026-11-24
status: In Review
author: Juan David Julio
standards:
  - ISO 13567-1/2 (Organization and naming of layers for CAD)
  - ISO 128-20 (Technical drawings — General principles of presentation — Basic conventions for lines)
  - AIA CAD Layer Guidelines v5
  - ISO 14224:2016 (Collection and exchange of reliability and maintenance data for equipment)
  - ANSI/ISA-101.01-2015 (Human-Machine Interfaces for Process Automation Systems)
  - ANSI/ISA-5.1-2009 (Instrumentation Symbols and Identification)
  - NFPA 30:2024 (Flammable and Combustible Liquids Code - Spill Containment & Spacing)
  - NFPA 497:2024 (Classification of Flammable Liquids, Gases, or Vapors and Hazardous Locations)
  - OSHA 29 CFR 1910.147 (The Control of Hazardous Energy - Lockout/Tagout)
  - API Standard 650/620 (Welded Tanks for Oil Storage)
---

# DT-UI-SVG-DOC-001: SVG Ingestion, Layering, and Spatial Data Contract

## 1. Purpose & Scope
This normative standard defines the structural, spatial, semantic, and security contract for ingesting 2D vector CAD/BIM layouts (General Arrangement Plot Plans, P&IDs, Hazardous Area Classifications) into the DTEAM Asset Performance Management (APM) and Digital Twin rendering engine.

To bridge the gap between greenfield CAD drafting conventions and High-Performance Human-Machine Interface (HPHMI) runtime execution, DTEAM enforces strict XML structures, predefined ISO 13567 layer stacking, ISO 128 hierarchical lineweights, hybrid progressive disclosure tiers, and ISO 14224 / LOTO / ISA-5.1 data bindings. In accordance with the Single Responsibility Principle (SRP), the SVG DOM functions strictly as a spatial projection and identity-binding target—not as an EAM master database or SCADA setpoint cache. This specification ensures brownfield Management of Change (MOC) integrity, eliminates visual clutter, and guarantees deterministic client-side spatial resolution across facilities of arbitrary scale.

---

## 2. Ingestion & Sanitization Invariants

Before client-side DOM insertion or database persistence, all incoming SVG documents MUST pass the following automated server-side verification pipeline:

1. **Security Sanitization:** Complete elimination of executable `<script>` elements, `javascript:` protocol URIs, inline DOM event handlers (`onclick`, `onload`, etc.), external XML entities (`<!ENTITY>`), foreign namespaces, and proprietary CAD binary metadata manifests (e.g., Adobe XMP, C2PA, Autodesk DWF blobs).
2. **Performance Ceiling (DOM Budget):**
   * **Operational Design Target:** Normalized plot plans SHOULD target **$\le 6,000$ DOM nodes** to guarantee smooth 60 FPS interaction on mid-tier industrial tablets without GPU fill-rate exhaustion.
   * **Hard Ingestion Rejection Ceiling:** Total parsed SVG DOM tree count MUST NOT exceed **15,000 nodes**. Documents exceeding 15,000 nodes MUST fail ingestion deterministically with an explicit micro-geometry stripping diagnostic.
3. **MOC Cryptographic Payload Checksum:** The root element MUST carry a SHA-256 digest (`data-checksum-sha256`) computed over the raw sanitized XML template (excluding the checksum attribute itself). The ingestion pipeline re-calculates and asserts this checksum against the active MOC registry.
4. **Coordinate System & Metric Scale:** All geometry MUST be expressed in SVG User Space coordinates normalized to a metric scale ratio defined in the root header (`data-scale-ratio` and `data-units="meters"`). Global geodesic EPSG transformations are decoupled and computed at runtime via the root calibration metadata (§11).
5. **Zero Unresolved Asset Placement & Physical Hit-Target Boundary:** Unmapped database equipment records (`UNMAPPED`) MUST NOT be injected at synthetic coordinates such as $(0, 0)$. Direct pointer hover and click interaction on the canvas targets strictly physical equipment hotspots (`class="dt-interactive"`, ISO 14224 Level 6 `EquipmentUnit` entities); logical Functional Locations (`ZONE-*`, `DIKE-*`) are navigated via the breadcrumb selector, L1 summary pills (`CMP-09`), or the `Space` / `Ctrl+K` intent-search bar.

---

## 3. Structural Root Contract (`<svg>`)

The root `<svg>` element MUST define Management of Change (MOC) attributes, spatial bounding limits, initial semantic zoom classification, and optional calibration metadata for generalized plants:

```xml
<svg 
  xmlns="http://www.w3.org/2000/svg" 
  viewBox="0 0 2000 1500" 
  class="dt-canvas zoom-l1"
  data-moc-id="MOC-2026-0042"
  data-rev-number="2.3"
  data-checksum-sha256="892a420e807f2f98..."
  data-scale-ratio="0.2"
  data-units="meters"
  aria-label="General Arrangement Plot Plan — Terminal Digital Twin"
>
  <defs>
    <!-- Pattern hatches for civil surfaces and SIMOPS conflict intersections -->
    <pattern id="hatch-concrete" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="var(--dt-color-border-subtle)" stroke-width="1" />
    </pattern>
  </defs>
  <!-- Seven Immutable Layer Groups in Physical Depth Stacking Order -->
</svg>
```

---

## 4. Layer Architecture & Physical Stacking Order

In SVG 1.1 and 2.0 specifications, rendering order is governed strictly by the **Painter's Algorithm** (DOM document tree order from top to bottom). All graphics MUST be grouped into exactly seven immutable `<g>` elements.

To prevent sub-surface conduits and spatial boundary envelopes from visually slicing across physical machinery, layers MUST follow this normative physical depth sequence:

```text
[Top View Overlay]       7. L-ANNO-TEXT   (Labels, tags, metric calibration, L1 summary pills)
                         6. L-INSP-INST   (ISA-5.1 bubbles, impulse leads)
                         5. L-PIPE-PROC   (Above-ground process piping corridors & valves)
                         4. L-MECH-EQPM   (Opaque equipment: tanks, pumps, skids)
                         3. L-FIRE-PROT   (Firewater ring mains, hydrants, monitors)
                         2. L-ELEC-HAZ    (Underground feeders, NFPA 497 zones)
[Bottom Foundation]      1. L-CIVL-BOTM   (Property boundary, public/internal roads, basin, dike walls)
```

| Order | SVG Group ID (`id`) | CSS Class | Scope, Governance & Occlusion Behavior |
| :---: | :--- | :--- | :--- |
| **1** | `L-CIVL-BOTM` | `.dt-layer-civil-botm` | **Sub-surface Ground & Civil Baseline:** Legal property limit polygon (`L-CIVL-PROP`), public perimeter highway (`L-CIVL-PUBROAD` with open-end alpha mask dissolve), internal access roads with tangential intersection fillets, retention/OWS basins, foundation slabs, and secondary containment dikes (`DIKE-*`). |
| **2** | `L-ELEC-HAZ` | `.dt-layer-elec-haz` | **Underground Electrical & Spatial Envelopes:** Underground MV/LV power feeder duct banks (`FDR-*`) and virtual NFPA 497 Class I, Div 1/2 hazardous area boundary envelopes (`HAZ-ZONE-*`). Hidden by default during normal supervisory inspection and automatically enabled in SIMOPS operational mode (`SCR-VIS-008`). |
| **3** | `L-FIRE-PROT` | `.dt-layer-fire-prot` | **Emergency Fire Protection Network:** Aerial firewater skids, addressable hydrants (`FH-*`), and foam monitor towers (`FM-*`) disclosed from Level 2 (`dt-zoom-l2`); underground looped perimeter fire-water ring mains (`RINGM`) routed strictly outside paved roadway curbs (`> roadHalfWidth`) and disclosed from Level 3 (`dt-zoom-l3`) to preserve crisp road edges. |
| **4** | `L-MECH-EQPM` | `.dt-layer-mech-eqpm` | **Physical Maintainable Equipment:** Primary process machinery (API 650 storage tanks, API 610 transfer pump skids, NFPA 20 fire pumps, custody transfer LACT skids, crossover manifolds, truck loading bays, and substation buildings). Opaque fills mask underlying conduits. |
| **5** | `L-PIPE-PROC` | `.dt-layer-pipe-proc` | **Above-Ground Process Piping Corridors:** Primary headers, secondary sleeperway pipes (`--dt-color-canvas-pipe-sec`), expansion loops, tank suction/discharge stubs, blind flange CAD terminations, and mechanical LOTO isolation valves (`CMP-ISO-VALVE`). Sits *on top* of equipment nozzles. Longitudinal sleeperway pipes suppress at L1 (`dt-zoom-l2`) and exclude pipe geometry inside paved road zones. |
| **6** | `L-INSP-INST` | `.dt-layer-insp-inst` | **Instrumentation & Control Loops:** ANSI/ISA-5.1 field instrumentation bubbles (`CMP-INST-NODE`), stanchions, and physical sensor/impulse lead lines (`L-INSP-LEADS`). Progressive disclosure governed from `--dt-zoom-scale-tactical`. |
| **7** | `L-ANNO-TEXT` | `.dt-layer-anno-text` | **Annotation Callouts & Metric Reference:** Equipment primary tags with dynamic screen-space vector halos, road/gate markers, programmatic L1 zone summary pills, and the metric calibration vector (`CALIBRATION-VECTOR`). |

*Rules:*
1. Unstructured vector elements outside these seven groups MUST be rejected by the ingestion engine.
2. Group IDs are case-sensitive and immutable.
3. Solid equipment bodies in `L-MECH-EQPM` MUST use opaque fills (`var(--dt-color-canvas-equip-shell)`) to naturally occlude sub-surface conduits (`L-ELEC-HAZ`) running directly beneath machinery foundation pads.
4. Runtime visibility toggles (e.g., `L-ELEC-HAZ`, `L-FIRE-PROT`, `L-INSP-INST`) MUST operate on canonical layer/entity groups rather than brittle single-element DOM IDs.

---

## 5. Process Safety & Spatial Containment Geometry

### 5.1 Secondary Containment Dikes (`L-CIVL-BOTM`)
Secondary containment bund walls MUST be modeled as closed `<polygon>` elements embedding spatial identity keys for backend binding:

```xml
<polygon 
  id="DIKE-SW" 
  class="dt-safety-containment"
  data-cmp-id="CMP-EQP-CIVIL"
  data-func-loc="TFA-TKF-SW"
  data-zone-id="SW"
  points="320.5,140.2 680.1,140.2 680.1,480.6 320.5,480.6"
/>
```

*Binding Invariant:*
Volumetric engineering calculations (net liquid capacity, submerged foundation deduction, and NFPA 30 statutory $110\%$ containment margin) are strictly maintained within backend EAM domain services and surfaced via DTOs. The SVG node preserves only spatial containment geometry and logical foreign keys (`data-cmp-id`, `data-func-loc`, `data-zone-id`). Direct pointer click targeting on the canvas remains scoped to `.dt-interactive` equipment units (§2.5), while logical containment zones are inspectable via breadcrumb or zone lists.

### 5.2 Hazardous Area Classification Envelopes (`L-ELEC-HAZ`)
Virtual safety boundaries representing flammable gas or vapor release envelopes MUST be modeled as closed polygonal or radial paths per NFPA 497:

```xml
<polygon 
  id="HAZ-ZONE-PMP" 
  class="dt-haz-envelope dt-zoom-l2"
  data-zone-id="PMP"
  data-division="DIV_2"
  stroke="var(--dt-color-canvas-steel)"
  stroke-width="1.4"
  stroke-dasharray="14 5 3 5"
  fill="none"
  points="..."
/>
```

*Rules:*
* Envelopes reside in `L-ELEC-HAZ`, remain hidden during standard asset inspection (`SCR-VIS-033`) to satisfy 90/10 visual calm, and auto-activate when toggling SIMOPS / Permit supervision (`SCR-VIS-008`).
* Boundary strokes MUST consume neutral spatial tokens (`var(--dt-color-canvas-steel)`) to prevent perceptual collision with active alarm indicators.
* Detailed atmospheric properties (gas groups, temperature classifications, and ventilation ratings) reside in the backend safety model linked by `data-zone-id`.

---

## 6. EAM Telemetry Binding & Identity Schema (ISO 14224)

Every maintainable, addressable, or interactive plant entity MUST decouple its physical hardware serial number from its immutable functional location slot per ISO 14224 §A.2:

```xml
<g 
  id="tag-P-0101A"
  data-cmp-id="CMP-EQP-PUMP"
  data-func-loc="TFA-CSS-P-0101A"
  data-equip-id="EQ-P-0101A-A"
  data-tag="P-0101A"
  class="dt-interactive equipment-hotspot"
>
  <!-- Opaque foundation, casing, impeller circle, motor body -->
</g>
```

*Required Spatial Attributes:*
* `id="tag-{TagNumber}"`: Authoritative DOM identifier matching the equipment functional tag.
* `data-cmp-id`: Standardized component archetype classification.
* `data-func-loc`: Canonical ISO 14224 Functional Location code.
* `data-equip-id`: Unique physical asset identifier in EAM Master Catalog.
* `data-tag`: Alphanumeric functional tag number matching `SCR-VIS-008` §7.3 and `SCR-VIS-033` §7.3.

### Component Archetypes (`data-cmp-id`)
The ingestion engine validates vector entities against standardized APM/EAM component classes:

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

Isolation points representing mechanical energy dissipation or electrical de-energization for hazardous work permits (OSHA 29 CFR 1910.147 / VIS-011) MUST adhere to the following schema:

### 7.1 Mechanical Valves (`CMP-ISO-VALVE`)
```xml
<g 
  id="cutoff-V-0101A-IN"
  data-cmp-id="CMP-ISO-VALVE"
  data-cutoff-id="V-0101A-IN"
  data-equip-id="EQ-P-0101A-A"
  data-func-loc="TFA-CSS-P-0101A"
  data-isolation-type="MECHANICAL"
  class="dt-interactive dt-isolation-point dt-zoom-l2"
  transform="translate(1088.5 765.4) rotate(-41)"
>
  <path d="M-3.6,-2.5 L3.6,2.5 L3.6,-2.5 L-3.6,2.5 Z" fill="var(--dt-color-canvas-equip-shell)" stroke="var(--dt-color-canvas-pipe-proc)" stroke-width="0.9" />
</g>
```

### 7.2 Electrical MCC Breakers (`CMP-ISO-BREAKER`)
```xml
<g 
  id="cutoff-MCC-P0101A"
  data-cmp-id="CMP-ISO-BREAKER"
  data-cutoff-id="MCC-P0101A"
  data-equip-id="EQ-P-0101A-A"
  data-func-loc="TFA-CSS-P-0101A"
  data-isolation-type="ELECTRICAL"
  class="dt-interactive dt-isolation-point dt-zoom-l3"
  transform="translate(1420.2 510.8)"
>
  <!-- Breaker graphic -->
</g>
```

*Cartographic Placement & Routing Invariant:*
* Bleed valves, instrument taps, and secondary cutoff symbols MUST be positioned with clear spatial offset from primary equipment bounding hit targets, ensuring independent pointer target disambiguation.
* Runtime LOTO overlays (`SCR-VIS-011`) project **electrical energy routes** along orthogonal `H/V + 45°` conduits from the parent Substation/MCC origin to the target motor/equipment centroid, and project **mechanical boundary lines** directly to edge-anchored nozzle/valve contact points (`boxBorderPoint`), never penetrating tank cores.

---

## 8. Instrumentation & Control Loops (ANSI/ISA-5.1-2009)

Field instrumentation nodes in layer `L-INSP-INST` represent real-time SCADA/DCS/SIS telemetry tags and are projected at runtime as **screen-space clamped opaque plates** (`36–46 px` target diameter, opaque `--dt-color-marker-surface` fill even at lowered hover opacity) to avoid ink collision with crossing piping:

```xml
<g 
  id="inst-PIT-0101A"
  data-cmp-id="CMP-INST-NODE"
  data-isa-tag="PIT-0101A"
  data-equip-id="EQ-P-0101A-A"
  data-func-loc="TFA-CSS-P-0101A"
  data-safety-critical="true"
  class="dt-interactive dt-instrument dt-zoom-l2"
>
  <!-- SIS dual-shape: Neutral outer rounded square with 1.2 radial clearance beyond inner circle -->
  <rect x="1164.0" y="801.2" width="11.6" height="11.6" rx="1.2" fill="var(--dt-color-marker-surface)" stroke="var(--dt-color-marker-border)" stroke-width="0.9" />
  <circle cx="1169.8" cy="807.0" r="4.6" fill="var(--dt-color-marker-surface)" stroke="var(--dt-color-canvas-pipe-proc)" stroke-width="1.0" />
  <line x1="1165.2" y1="807.0" x2="1174.4" y2="807.0" stroke="var(--dt-color-canvas-pipe-proc)" stroke-width="0.6" />
  <text x="1169.8" y="806.2" font-size="3.0" text-anchor="middle" font-weight="bold" fill="var(--dt-color-text-primary)">PIT</text>
  <g class="dt-zoom-l3">
    <text x="1169.8" y="810.1" font-size="2.3" text-anchor="middle" fill="var(--dt-color-text-primary)">0101A</text>
  </g>
</g>
```

*Rules:*
1. **Loop Decoupling:** General BPCS transmitters use standard circular bubbles. Safety-Critical SIS loops (e.g., API 2350 overfill switches `LSHH`, hazardous gas detectors `AIT`) MUST enclose the bubble within a neutral bounding square box (`--dt-color-marker-border`, preserving red strictly for active alarms).
2. **Impulse Lead Lines (`L-INSP-LEADS`):** Instruments mounted on stanchions off equipment skids MUST carry fine dashed lead lines (`stroke-dasharray="3 2"`, width `0.7px`) linking the process physical tap point to the instrument bubble centroid.
3. **Telemetry Boundary (Zero Live Numeric Values on SVG):** Process variable units, live engineering readings, and trip setpoints reside strictly within the C# telemetry DTO contracts (`SCR-VIS-033` §7.2.3); embedding live telemetry values on SVG instrument plates or DOM attributes is strictly prohibited.
4. **Client-Driven Criticality & Screen-Space Decluttering:** Criticality is authoritatively driven by backend `is_safety_critical` metadata. At `--dt-zoom-scale-tactical` and above (`L2`), the viewport engine applies screen-space collision culling keeping priority order: **selected/hovered asset instruments $\to$ SIS safety-critical loops $\to$ BPCS process loops**, revealing loop sub-numbers (`0101A`) progressively at Level 3 (`--dt-zoom-scale-l2-max`).
5. **Rule 5 — Geometric Enclosure Separation (SIS Box Clearance):** When rendering safety-critical SIS loops (`is_safety_critical="TRUE"`), the enclosing rounded rectangular box (`rx = 1.2`) MUST maintain an outer radial clearance of at least **$1.2\text{ px}$** beyond the circular instrument bubble ($r_{\text{box}} = r_{\text{bubble}} + 1.2$). Tangential or intersecting corner spikes are prohibited.
6. **Rule 6 — 4-Character Functional Tag Scaling:** Instrument functional identifiers comprising 4 alphanumeric characters (e.g., `LSHH`, `PSHH`, `FSHH`) MUST scale proportionally ($\le 2.4\text{ px}$ base font unit inside $\varnothing 10.4$ SVG bubble, or equivalent in screen-space clamped plate) to guarantee $\ge 1.5\text{ px}$ lateral chord clearance from the inner circle edge.

---

## 9. High-Performance HMI (HPHMI), ISO 128 Lineweights & Adaptive Typography

### 9.1 Palette Governance & Alarm Reservation (`CAD Calibrado`)
In strict compliance with ANSI/ISA-101.01 §6.2, steady-state digital twin layouts MUST employ the calibrated neutral **`CAD Calibrado`** material palette ([DT-UI-DS-DOC-001 §3.4](DT-UI-DS-DOC-001.md#34-spatial-and-physical-material-tokens-digital-twin-canvas)). Pure red (`#FF0000` / `#EF4444`) and warning amber (`#FFA500` / `#F59E0B`) are **strictly prohibited** on static piping, equipment fills, or civil boundaries; saturated hues are reserved exclusively for active alarm states, PTW hazard shapes, and LOTO energy vectors.

**Absolute pure white (`#FFFFFF`) and absolute pure black (`#000000`) are strictly forbidden** across both Light and Dark CAD themes. In Dark Theme, civil and process entities follow a strictly monotonic elevation luminance ladder (`--dt-color-bg-canvas` $\to$ `--dt-color-canvas-bund-floor` $\to$ `--dt-color-canvas-asphalt` $\to$ `--dt-color-canvas-concrete` $\to$ `--dt-color-canvas-equip-shell` $\to$ `--dt-color-canvas-steel` $\to$ `--dt-color-canvas-pipe-sec` $\to$ `--dt-color-canvas-pipe-proc`).

*Contrast Rule:*
Text labels MUST achieve a minimum WCAG 2.1 AA relative luminance contrast ratio of $\ge 4.5:1$ against their immediate background (`--dt-color-label-halo` / `--dt-color-canvas-equip-shell`). Graphical line elements MUST achieve $\ge 3.0:1$.

### 9.2 ISO 128 Hierarchical Lineweights & `CAD Adaptativo`
To eliminate muddy silhouette overlapping across plant scales, CAD strokes follow a 4-tier **ISO 128** hierarchy modulated at runtime by the **CAD Adaptativo** zoom factor (`vector-effect: non-scaling-stroke`):

| ISO 128 Tier | Base Screen Stroke (px) | Target Cartographic Elements |
| :---: | :---: | :--- |
| **Tier 1 (Primary Contours & Headers)** | `2.2` | Property boundary perimeter (`L-CIVL-PROP`), primary hydrocarbon headers (`pipe-proc`), tank shell perimeters, LOTO active paths. |
| **Tier 2 (Equipment & Secondary Headers)** | `1.5` | Secondary piping (`--dt-color-canvas-pipe-sec`), concrete dike walls, pump skids, valve bodies, fire-water ring mains. |
| **Tier 3 (Auxiliary Civil & Structures)** | `1.0` | Sleeperway steel bents (`--dt-color-canvas-steel`), canopy columns, hazard dashed envelopes, apron joints. |
| **Tier 4 (Micro Detail & Grids)** | `0.65` | Stairs, bolt rings, radial tank seams, impulse leads, coordinate grid lines (`--dt-color-canvas-grid`). |

*`CAD Adaptativo` Attenuation Formula:*
$$\text{StrokeWidth}_{\text{effective}} = \text{BaseTierPx} \times \text{clamp}\left(\frac{\text{NominalWidth}}{\text{CurrentViewBoxWidth}},\ \text{--dt-cad-stroke-floor},\ 1.0\right)$$
* Physical roadway lane markings (`.dt-road-marking`, physical painted line width `0.18 m` in User Space) are **explicitly exempted** from `vector-effect: non-scaling-stroke` so lane paint scales proportionally with pavement geometry rather than bloating into thick white bands at site-fit zoom.

### 9.3 Dynamic Screen-Space Text Halos & Anti-Drop-Shadow Rule
Raster `drop-shadow` filters on `<text>` elements and static `1.2px non-scaling-stroke` CSS strokes on `<text>` (which suffer font-dilation clipping across Chromium Skia pipelines) are prohibited. Legibility across dense piping racks is guaranteed via dynamically updated SVG user-unit halo strokes matching the underlying canvas ground (`--dt-color-label-halo` / `--dt-color-canvas-equip-shell`):

$$\text{HaloStroke}_{\text{userUnits}} = \max\left(0.05,\ \frac{3.0}{\max(\text{pxPerUnit},\ 0.05)}\right)$$

* For screen-space clamped label groups (`.smart-label` normalized to target $9.5\text{–}14\text{ px}$ on screen), divide `3.0 px` by the effective group scale (`pxPerUnit * markerScale`) so every label retains an exact **$3.0\text{ px}$** protective knock-out halo (`paint-order: stroke fill; stroke-linejoin: round;`) at every zoom level.
* Elevation shadows (`--dt-shadow-marker`) are permitted strictly on floating marker plate silhouettes ($Z \ge 50$) per [DT-UI-DS-DOC-001 §5.1](DT-UI-DS-DOC-001.md#51-hphmi-shadow-discipline-canvas-vs-hud-chrome-separation), never on `<text>`.

### 9.4 Adaptive Multi-Scale Coordinate Grid & SDF Boundary Dissolve
* **Multi-Scale Metric Grid:** Minor/major grid intervals select deterministically from `[0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 200]` meters so major coordinate lines maintain $\ge 72\text{ px}$ visual separation on screen.
* **Zero-Grain SDF Property Fade (`#dt-Grid-Fade`):** Beyond the legal site boundary (`L-CIVL-PROP`), the exterior canvas field fades smoothly to `--dt-color-bg-canvas` using a signed-distance-field (SDF) quintic smoothstep radial alpha ramp (`0%` fade inside `L-CIVL-PROP`) paired with $4 \times 4$ ordered Bayer dithering to prevent dark-theme 8-bit banding.
* **Open Highway Edge Dissolve (`#L-CIVL-PUBROAD`):** Public perimeter highways entering and exiting the canvas dissolve cleanly at both longitudinal open ends via linear alpha-mask gradients into the background ground without clipped rectangle edges.

---

## 10. Progressive Disclosure & Viewport Kinematics

### 10.1 Hybrid ISA-101 Semantic Zoom Model
Progressive disclosure combines discrete cross-faded swaps (for mutually exclusive L1 summary pills vs. L2 discrete markers) with smoothstep opacity ramps (for additive CAD piping/detail layers) keyed to normalized zoom tokens ([DT-UI-DS-DOC-001 §2.5](DT-UI-DS-DOC-001.md#25-spatial-navigation-and-semantic-zoom-tokens-ansiisa-10101-viewports)):

```text
Level 1: Macro Terminal Overview  (Scale < var(--dt-zoom-scale-l1-max))
  ├── Legal property perimeter (L-CIVL-PROP), perimeter roads, retention basins
  ├── Diked tank farm envelopes (DIKE-*) and gross equipment footprints
  ├── Programmatic L1 Functional Zone Summary Pills (CMP-09)
  └── Primary macro asset tags (TK-*, BLD-*)

Level 2: Subsystem & Units         (var(--dt-zoom-scale-l1-max) <= Scale < var(--dt-zoom-scale-l2-max))
  ├── Smoothstep additive ramp (l2-start .. l2-end): secondary pipe racks, sleeperway steel
  ├── L2 Fire protection hydrants/monitors (L-FIRE-PROT) & tank stairs/ramps
  ├── Mechanical LOTO isolation valves (CMP-ISO-VALVE) & PTW overlays (CMP-05)
  └── ANSI/ISA-5.1 field instrument plates disclosed at Scale >= var(--dt-zoom-scale-tactical)

Level 3: Micro Equipment Detail   (Scale >= var(--dt-zoom-scale-l2-max))
  ├── Smoothstep additive ramp (l3-start .. l3-end): underground fire ring outside curb, minor grid
  ├── Casing bleeders, drain hubs, blind flange terminations, check valves
  ├── ISA-5.1 loop sub-numbers (0101A) and impulse lead lines
  └── Electrical MCC circuit breaker nodes (CMP-ISO-BREAKER) & ISO 14224 breadcrumb target
```

### 10.2 Pure `viewBox` Camera, `PAN_BOUNDS` & Transition Rules
1. **Pure `viewBox` Geometry (Zero CSS `transform: scale`):** All pan and zoom operations mutate the `<svg>` `viewBox` attribute directly in double-precision floating point so vector crispness, hit testing, and screen-space clamped plates remain exact at $0.65\times$ through $15\times$ magnification.
2. **`PAN_BOUNDS` Center Clamping:** Pan clamping bounds the viewport center $(cx, cy)$ within the facility bounding box extents (`[siteBox.minX .. siteBox.maxX, siteBox.minY .. siteBox.maxY]`), allowing any corner of the property boundary to reach the screen center while preventing panning into infinite empty void.
3. **Instant Focal Wheel vs. Smooth Programmatic Fly-To:**
   * Mouse wheel zoom (`exp(-delta * 0.0014)`) and drag panning apply immediately per frame without inertia lag around the pointer focal coordinate.
   * Programmatic transitions (double-click `1.7x` focus, `Reset View` fit, `Space` / `Ctrl+K` intent zoom framing, LOTO full-circuit framing) execute smooth delta-time interpolation (`requestAnimationFrame`), braking cleanly on user input.
   * Desktop panning supports a unified **$> 4\text{ px}$ drag threshold** on primary or middle mouse button (stationary clicks $\le 4\text{ px}$ select `.dt-interactive` equipment), matching tablet single-finger touch disambiguation.
4. **Hybrid Cross-Fade & Hit-Test Guard:** Mutual-exclusion swaps (L1 pills $\leftrightarrow$ L2 pins) transition over **$180\text{ ms}$** using `opacity` interpolation; suppressed layers enforce `pointer-events: none` (never abrupt `visibility: hidden` mid-transition that snaps cross-fades).
5. **Focus+Context De-Emphasis (`<mask>` Clipping):** When isolating a zone or executing LOTO (`SCR-VIS-011`), non-target plant regions attenuate cleanly (`opacity: 0.24`) while preserving full opacity exclusively on the isolated circuit or SVG `<mask>` hole around the target zone/dike.
6. **Screen-Space Marker Clamping:** Floating cartographic overlays rescale inversely against `pxPerUnit` within strict pixel bounds: smart labels (`9.5–14 px`), ISA-5.1 plates (`36–46 px`), LOTO cutoff discs (`32–40 px`), SIMOPS pins (`26–36 px`), and small tap dots (`5–8 px`).
7. **Programmatic L1 Zone Summary Pills:** L1 zone pills aggregate counts dynamically from relational catalog joins (`tax.functional_locations` + `tax.equipment_units` + `vis.mesh_mappings` via API DTOs) rather than requiring separate database geometry tables or hardcoded label coordinates.

---

## 11. Spatial Metric Calibration

Layer `L-ANNO-TEXT` MUST contain a hidden metric calibration vector. To ensure the camera, LOD thresholds, and grid scale generalize cleanly across micro-skids ($20\text{ m}$), pump houses, and full bulk terminals ($300\text{ m}+$), the root SVG or `CALIBRATION-VECTOR` exposes facility scale anchors with deterministic fallback defaults:

```xml
<g id="L-ANNO-TEXT" class="dt-layer-anno-text">
  <line 
    x1="0" y1="0" x2="1000" y2="0" 
    id="CALIBRATION-VECTOR" 
    data-real-meters="200.0" 
    data-nominal-span="0.65"
    stroke="none" 
    fill="none" 
    style="display:none;" 
  />
  <!-- Annotation labels & L1 summary pills -->
</g>
```

$$\text{Scale Ratio } K = \frac{\text{data-real-meters}}{\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}} = \frac{200.0}{1000} = 0.20 \text{ m/unit}$$

* If `data-nominal-span` or calibration hint attributes are omitted on third-party imported SVGs, the engine deterministically falls back to `L-CIVL-PROP` bounding box extents (or full `<svg>` `viewBox` extents) with nominal span `0.65`.

---

## 12. Automated Ingestion Pipeline (AutoCAD Normalization)

When importing raw industrial CAD models (AutoCAD Model Space DXF/DWG/SVG exports), the DTEAM server ingestion pipeline applies the following deterministic transformations:

1. **Layer Canonicalization:** Maps legacy AutoCAD layers into the 7 standard groups according to ISO 13567 naming rules.
2. **ACI Color Normalization:** Converts legacy AutoCAD Color Index primaries (ACI 1 Red, ACI 2 Yellow, ACI 4 Cyan, ACI 6 Magenta) and CAD dark backgrounds into semantic `CAD Calibrado` tokens (`--dt-color-canvas-*`), stripping saturated static hues.
3. **Polyline Closure, Tangential Road Fillets & Blind Flange Terminations:** Closes open boundary polygons, replaces sharp corners at road intersections with **tangential fillets** ($R \ge 4.4\text{ m}$), eliminates stray pipe overhangs across roadway curbs, and terminates stub/manifold ends with canonical blind flanges.
4. **Data Schedule Re-synchronization:** Binds incoming equipment and instrumentation graphics to authoritative architectural catalogs (EAM Master Catalog, Spatial MeshMapping Repository, and LOTO Isolation Registry), supporting progressive MOC promotion of static piping corridors into discrete `EquipmentUnit` records without breaking base plot coordinates.
5. **Cartographic Abstraction & Micro-Geometry Stripping:** EPC CAD models frequently include manufacturing-level detail (individual spiral stair treads, radial roof rafters, motor cooling fins, baseplate anchor bolt pitch circles) that introduces excessive visual clutter and exhausts mobile GPU fill-rates. The ingestion pipeline strips non-interactive structural micro-lines to satisfy the **$6,000$-node operational target** ($\le 15,000$ hard cap), preserving primary equipment envelopes, nozzle stubs, and walkways.

### 12.5 Cartographic Spatial Clearance Invariants
1. **Roadway & Underground Fire Main Decoupling:** Underground fire-water ring mains (`L-FIRE-PROT`) MUST run outside paved roadway curbs (`> roadHalfWidth`) rather than slicing inside traffic aprons; above-ground pipe racks MUST cross roads only over designated sleeperway bridges (`dt-zoom-l2`).
2. **Tank Roof vs. Manifold Isolation:** Tank stairways, roof gauges, and perimeter walkways MUST maintain unobstructed clearance around dike access stairs and suction manifolds.
3. **Zero Longitudinal Sleeperway Pipes in L1:** Auxiliary longitudinal pipe runs inside sleeperways declare `.dt-zoom-l2` to suppress line density during Level 1 macro supervision.
4. **Rule 4 — Nozzle vs. Instrument Decoupling:** On atmospheric storage tanks (API 650), tank roof telemetry instruments (e.g., Radar Level Transmitters `LIT`) MUST be angularly decoupled from base process nozzles and root isolation valves (`MOV`) by an arc separation **$\ge 90^\circ$** ($\Delta \theta \ge 90^\circ$) to eliminate interactive bounding box collisions.
5. **Rule 5 — Civil Roadway Setback Clearance:** In accordance with NFPA 30 §22.5.2 and OSHA 1910.106 fire response requirements, secondary containment bund wall toes and crowns MUST maintain a minimum clear setback distance of **$1.2\text{ m}$** from internal perimeter road curb lines. Sharp acute bund vertices projecting into curved roadway turning radii MUST be chamfered.
6. **Integrity Sealing:** Re-computes and embeds the SHA-256 payload digest in `data-checksum-sha256`. Documents failing hash validation or the $15,000$-node DOM hard ceiling are rejected with an explicit ingestion diagnostic log.
