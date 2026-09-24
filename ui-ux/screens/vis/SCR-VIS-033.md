---
id: SCR-VIS-033
title: Asset Inspection on the 2D Base Map
module: VIS
isa101_level: L1 (COP) | L3 (Asset Detail)
platform: Shared Component
target_device: Industrial Tablet | Desktop
roles:
  - Maintenance Supervisor
  - Maintenance Technician
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
version: 1.3
date: 2026-09-04
status: In Review
---

# SCR-VIS-033: Asset Inspection on the 2D Base Map

## 1. Purpose and Operational Context
* **View Objective:** Interactive spatial visualization of the plant or subsystem in 2D, allowing equipment localization, real-time condition querying, and deployment of the operations contextual card.
* **Operational Context:** Deployed on desktop web consoles (Light Theme) and on industrial field tablets (Dark Theme with tactile ergonomics suitable for use with gloves).
* **Mode of Operation:** Supervision, visual diagnosis, and passive contextual navigation. The interface does not issue industrial control commands (start/stop), does not alter process variables, and does not execute remote maneuvers on the SCADA.

---

## 2. Visual Artifact

![[SCR-VIS-033-asset-inspection-card.svg]]

---

## 3. Functional Component Inventory

> The base grid, typography, neutral palettes, and minimal tactile contact areas are inherited from [[DT-UI-DS-DOC-001]]. This table exclusively defines the present components, their semantic tokens, and the link with the model.

| ID | Control / Component | Visual Role / Content | Semantic Token | Data Link / Behavior Rule |
| :------- | :---------------------- | :------------------------------- | :-------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CMP-01` | Canvas Viewport 2D      | Interactive SVG vector canvas | `--dt-color-bg-canvas`                                                                              | Renders the SVG map of the area. Supports continuous panning and dual zoom (geometric and semantic) per [[UC-VIS-033]]. |
| `CMP-02` | Viewport Toolbar        | Spatial navigation bar | `--dt-color-surface-card`                                                                           | Viewer controls: Reset view, zoom levels, layer selector, and contextual level badge. |
| `CMP-03` | Command Palette Trigger | Quick search access | `--dt-color-border-subtle`<br>`--dt-color-text-muted`                                               | Global fuzzy search trigger (`Ctrl + K` / `/`) on desktop. On mobile, it renders as a tactile action button with a magnifying glass icon. |
| `CMP-04` | Equipment Hotspot       | Equipment symbol in SVG | Border: `--dt-primitive-gray-500`<br>Background: `--dt-color-bg-canvas` | Level 6 geometry linked by `TagNumber`. In normal condition, it operates with neutral outlining; in alarm, it acquires a halo and severity shape per [[DT-UI-DS-DOC-001]]. |
| `CMP-05` | Context Container       | Asset contextual panel | Surface: `--dt-color-surface-card` | Adaptable container (Side panel or *Bottom Sheet*). Desktop Elevation: `--dt-z-overlay-card`. Mobile Elevation: `--dt-z-drawer-sidebar`. |
| `CMP-06` | Asset Header Block      | Identification and status | Surface: `--dt-color-surface-card` | Presents `TagNumber` (with `--dt-font-mono-data` typography), criticality, and operational status (`EquipmentUnit.operationalStatus`). |
| `CMP-07` | Live Telemetry Block    | MAI analog indicators | `--dt-color-mai-*`                                                                                  | Analog bars for critical process variables ([[DT-UI-DS-DOC-001]]). Dynamically updated via SignalR ([[TR-010]]). |
| `CMP-08` | Safety & Work Badges    | Work and risk indicators | [[DT-UI-DS-DOC-001#6.2. Redundant Coding Matrix for Permits and LOTO\| DT-UI-DS-DOC-001]] | Consumes Permit and LOTO data applying mandatory redundant coding. |
| `CMP-09` | Quick Action Buttons    | Primary actions button panel | Surface: `--dt-color-surface-base`<br>Text: `--dt-color-text-primary`                           | Quick links: `[Locate on Map]`, `[View LOTO Route]` $\to$ SCR-VIS-011, `[View WOs]` $\to$ SCR-MTTO-026, `[Master Card]` $\to$ SCR-INV-005. |


---

## 4. Screen State Matrix

| State | Visual Modification in the Interface | Activation Condition |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **Normal (Default)** | Surfaces and assets in neutral grayscale palette. Telemetry within normal operating ranges. | Successful area load and active data stream without alarms. |
| **Loading** | Dimmed activity indicator over the canvas; visual skeleton (*shimmer*) in the contextual panel. | Functional area transition or initial SVG map retrieval. |
| **Selected Asset** | The active equipment highlights with an informational selection border (`--dt-color-state-info`). `CMP-05` is deployed. | Click / Tap on `CMP-04` or selection via `CMP-03`. |
| **Critical Asset Alarm** | `CMP-04` acquires a border and square symbol in `--dt-color-alarm-critical`. In `CMP-07`, the MAI shows a P1 severity marker. | Physical variable exceeding safety thresholds or equipment in `DOWN` condition. |
| **Telemetry Loss** | Numeric values in `CMP-07` freeze and switch to `--dt-color-state-disabled`; an amber warning icon (`--dt-color-alarm-warning`) and disconnection timestamp are shown. | Interruption of the real-time connection with the SCADA source ([[UC-VIS-033]], `AF-002`). |
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
  
### 5.3. Inspection and Telemetry
1. Selecting an asset on the map invokes the opening of `CMP-05` and real-time subscription to the equipment's telemetry channel.
2. **SignalR Subscription Management:** Subject to global *debouncing* policies to prevent network collisions due to rapid multiple selection ([[DT-ARQ-CMP-DOC-001]]).
3. **Connection Resilience:** If the component detects a violation of the *Heartbeat* threshold or receives a packet with "Bad" quality ([[DT-ARQ-DEP-DOC-001]]), it immediately transitions to the "Telemetry Loss" display.
---

## 6. Industrial and Safety Considerations

* **HPHMI Philosophy ([[TR-011]]):** The use of the color green to denote normal operation is prohibited. The interface remains strictly in neutral grayscale; saturated colors are reserved for alarm and warning conditions with redundant shape coding.
* **Telemetry Resilience:** No variable without a confirmed timestamp can be presented as a live reading. The interface explicitly distinguishes between a real zero-value reading and instrument disconnection.