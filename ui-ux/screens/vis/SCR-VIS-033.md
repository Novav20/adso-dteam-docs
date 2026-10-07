---
id: SCR-VIS-033
title: Asset Inspection on the 2D Base Map
module: VIS
isa101_level: L2 (Process Area Schematic) | L3 (Equipment Task Faceplate)
platform: Shared Component
target_device: Industrial Tablet | Desktop
roles:
  - Maintenance Technician
  - Maintenance Supervisor
  - HSEQ Inspector
  - Reliability Engineer
user_stories:
  - "[[VIS-033]]"
use_cases:
  - "[[UC-VIS-033]]"
requirements:
  - FR-598
  - FR-599
  - FR-600
  - FR-601
  - FR-602
  - NFR-603
  - NFR-604
  - NFR-605
  - "[[TR-010]]"
  - "[[TR-011]]"
version: 1.5
date: 2026-10-06
status: In Review
---

# SCR-VIS-033: Asset Inspection on the 2D Base Map

## 1. Purpose and Operational Context
* **View Objective:** Interactive spatial visualization of a plant functional location in 2D (ISA-101 Level 2), enabling equipment localization, real-time operating condition assessment, and deployment of the Level 3 Equipment Task Faceplate.
* **Primary Target Persona:** **Maintenance Technician** (dictates operational ergonomics, `--dt-touch-target-mobile` compliance for gloved operation, and pre-attentive tactical scanning).
* **Secondary Personas:** Maintenance Supervisor, HSEQ Inspector, and Reliability Engineer (authorized read/inspection access for spatial situational awareness; specialized workflows drill down into their dedicated modules).
* **Operational Context:** Deployed on desktop web consoles (Light Theme) and on industrial field tablets (Dark Theme with tactile ergonomics suitable for field conditions).
* **Mode of Operation:** Supervision, visual diagnosis, and passive contextual navigation. The interface does not issue industrial control commands (start/stop), does not alter process variables, and does not execute remote maneuvers on the SCADA.

---

## 2. Visual Artifact

![[SCR-VIS-033-asset-inspection-card.svg]]

---

## 3. Functional Component Inventory

> The base grid, typography, neutral palettes, and minimal tactile contact areas are inherited from [[DT-UI-DS-DOC-001]]. This table exclusively defines the present components, their semantic tokens, and the link with the model.

| ID | Control / Component | Visual Role / Content | Semantic Token | Data Link / Behavior Rule |
| :------- | :---------------------- | :------------------------------- | :-------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CMP-01` | Canvas Viewport 2D      | Interactive SVG vector canvas | `--dt-color-bg-canvas`                                                                              | Renders the SVG map of the functional area (ISA-101 Level 2). Supports continuous panning and dual zoom (geometric and semantic) per [[UC-VIS-033]]. |
| `CMP-02` | Viewport Toolbar        | Spatial navigation bar | Surface: `--dt-color-surface-card`<br>Radius: `--dt-radius-full`                                    | Unified floating pill toolbar centered over `CMP-01`. Integrates `CMP-03`, level badge, and viewer controls: Reset view, zoom levels, and layer selector. |
| `CMP-03` | Command Palette Trigger | Quick search access | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle`<br>Radius: `--dt-radius-full`    | Embedded pill search input within `CMP-02` (`Ctrl + K` / `/`). Supports fuzzy equipment tag search. |
| `CMP-04` | Equipment Hotspot       | Equipment symbol in SVG | Border: `--dt-primitive-gray-500`<br>Background: `--dt-color-bg-canvas` | Level 6 geometry linked by `TagNumber`. In normal condition, it operates with neutral outlining; in alarm, it acquires a halo and severity shape per [[DT-UI-DS-DOC-001]]. |
| `CMP-05` | Context Container       | Level 3 Equipment Task Faceplate | Surface: `--dt-color-surface-card` | Adaptable container (Collapsible lateral panel or *Bottom Sheet*). Desktop Elevation: `--dt-z-overlay-card`. Mobile Elevation: `--dt-z-drawer-sidebar`. **Boundary rule:** Strictly limited to Level 3 operational data. Excludes Level 4 static master data (datasheets, purchase records, full manuals). |
| `CMP-06` | Asset Header Block      | Identification and status | Surface: `--dt-color-surface-card` | Presents `TagNumber` (with `--dt-font-mono-data` typography), technical description, criticality rating, and operational status (`EquipmentUnit.operationalStatus`). |
| `CMP-07` | Live Telemetry Block    | MAI analog indicators | `--dt-color-mai-*`                                                                                  | Moving Analog Indicators (MAI) contextualizing process variables within calibrated normal operating zones (`--dt-color-mai-normal-zone`) and trip limits ([[DT-UI-DS-DOC-001#6.1]]). Dynamically updated via SignalR ([[TR-010]]). Raw numbers without analog scale context are prohibited. |
| `CMP-08` | Safety Context Summary  | Safety boundaries summary | [[DT-UI-DS-DOC-001#6.2. Redundant Coding Matrix for Permits and LOTO\| DT-UI-DS-DOC-001]] | Summary badges of active PTW permit number and verified LOTO isolation tags (e.g., locked boundary valves or electrical disconnects) applying mandatory redundant coding. |
| `CMP-09` | Quick Action Buttons    | Primary actions button panel | Surface: `--dt-color-surface-base`<br>Text: `--dt-color-text-primary`                           | Direct drill-down actions: `[Locate on Map]`, `[View LOTO Route]` $\to$ SCR-VIS-011, `[Full WO History]` $\to$ SCR-MTTO-026, `[Level 4 Master Catalog / Datasheet]` $\to$ SCR-INV-005. |
| `CMP-10` | Actionable Work Orders  | Active maintenance tasks list | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle`                            | Compact list of active work orders showing WO ID, Type (PM/CM), Status (e.g., Ready, In Progress), and Priority. Replaces un-actionable raw counters ("3 WOs"). |

---

## 4. Screen State Matrix

| State | Visual Modification in the Interface | Activation Condition |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **Normal (Default)** | Surfaces and assets in neutral grayscale palette. Telemetry within normal operating ranges. | Successful area load and active data stream without alarms. |
| **Loading** | Dimmed activity indicator over the canvas; visual skeleton (*shimmer*) in the contextual panel. | Functional area transition or initial SVG map retrieval. |
| **Selected Asset** | The active equipment highlights with an informational selection border (`--dt-color-state-info`). `CMP-05` is deployed. | Click / Tap on `CMP-04` or selection via `CMP-03`. |
| **Critical Asset Alarm** | `CMP-04` acquires a border and square symbol in `--dt-color-alarm-critical`. In `CMP-07`, the MAI shows a P1 severity marker. | Physical variable exceeding safety thresholds or equipment in `DOWN` condition. |
| **Telemetry Loss** | Numeric values in `CMP-07` freeze; indicator applies Priority 4 Diagnostic coding: value switches to `--dt-color-text-muted`, the pointer/track is dimmed, and a neutral diagnostic icon (`wifi-off` / stale symbol) with disconnection timestamp is shown ("Stale Data. Connection Lost at [timestamp]"). The amber process alarm color is strictly prohibited. | Interruption of the real-time connection with the SCADA source or heartbeat timeout ([[UC-VIS-033]], `AF-002`). |
| **Pending Mapping** | `CMP-05` presents the tabular information of the asset but disables the spatial localization action with an informational badge. | Query of a master catalog equipment that lacks associated geometry in the current SVG ([[UC-VIS-033]], `AF-001`). |

---

## 5. Interaction Rules and Data Flow

### 5.1. Initial Load
1. The system retrieves the vector map corresponding to the functional location and renders the base canvas.
2. Interactive graphic nodes are bidirectionally linked with the registered equipment entities (FR-599).
3. The map is initialized centered on its macro view.

### 5.2. Spatial Navigation and Mobile Ergonomics
1. **Panning and Zoom:** Dual navigation (Geometric and Semantic) per [[UC-VIS-033]].
2. **Tactile Controllability:** The `CMP-05` container toggles its states via an upper graphic trigger that inherits the tactile size of `--dt-touch-target-mobile`.
3. **Responsive Layout:** The transformation of the `CMP-05` container (Bottom Sheet $\leftrightarrow$ Lateral Panel) is delegated to the device orientation rules defined in [[DT-UI-NAV-DOC-001]].
4. **Collapsible Drawer and Viewport Centering:** In landscape tablet mode, `CMP-05` can be collapsed via a dedicated tactile trigger. When collapsed or expanded, `CMP-01` smoothly resizes, and the unified floating toolbar (`CMP-02` / `CMP-03`) automatically recalibrates its horizontal position to remain strictly centered over the active visible canvas.
  
### 5.3. Inspection and Telemetry
1. Selecting an asset on the map invokes the opening of `CMP-05` and real-time subscription to the equipment's telemetry channel.
2. `CMP-05` renders strictly tactical Level 3 data: Asset Header (`CMP-06`), Analog Telemetry (`CMP-07`), Safety Boundaries (`CMP-08`), and Actionable Work Orders (`CMP-10`).
3. **SignalR Subscription Management:** Subject to global *debouncing* policies to prevent network collisions due to rapid multiple selection ([[DT-ARQ-CMP-DOC-001]]).
4. **Diagnostic Connection Resilience:** If the component detects a violation of the *Heartbeat* threshold or receives a packet with "Bad" quality ([[DT-ARQ-DEP-DOC-001]]), it immediately transitions to the "Telemetry Loss" state using Priority 4 Diagnostic coding, preventing the generation of misleading process alarms.
5. **Level 4 Drill-Down:** Deep master data (catalogs, specifications) and historical work order archives are deferred to full-screen views triggered via `CMP-09`.

---

## 6. Industrial and Safety Considerations

* **HPHMI Philosophy ([[TR-011]]):** The use of the color green to denote normal operation is prohibited. The interface remains strictly in neutral grayscale; saturated colors are reserved for alarm and warning conditions with redundant shape coding.
* **Alarm vs. Diagnostic Segregation (ISA-101):** Communication failures, sensor disconnects, and stale data streams are categorized as Priority 4 Diagnostics. They must never use amber (`--dt-color-alarm-warning`) or red (`--dt-color-alarm-critical`), preventing operator cognitive distraction during real process upsets.
* **Pre-Attentive Telemetry Scanning:** Telemetry must never be presented as disconnected numerical text alone. Moving Analog Indicators (MAI) provide immediate spatial assessment relative to high/low limits within <2 seconds.
* **Level 3 Cognitive Boundary:** The contextual faceplate (`CMP-05`) is strictly an operational bridge. Overloading the faceplate with Level 4 static master catalog data or extensive CMMS logs is prohibited to prevent field operational errors.
* **Telemetry Resilience:** No variable without a confirmed timestamp can be presented as a live reading. The interface explicitly distinguishes between a real zero-value reading and instrument disconnection.