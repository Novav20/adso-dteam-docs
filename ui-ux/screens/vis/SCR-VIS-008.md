---
id: SCR-VIS-008
title: General Plant Map with Work Permits Layer (SIMOPS)
module: VIS
isa101_level: L1 (COP - Overview)
platform: Shared Component
target_device: Industrial Tablet | Desktop
roles:
  - HSEQ Inspector
  - Maintenance Supervisor
user_stories:
  - "[[VIS-008]]"
use_cases:
  - "[[UC-VIS-008]]"
requirements:
  - FR-182
  - FR-183
  - FR-184
  - FR-185
  - FR-186
  - FR-187
  - FR-188
  - NFR-190
  - NFR-193
  - "[[TR-010]]"
  - "[[TR-011]]"
version: 1.0
date: 2026-09-05
status: DRAFT
---

# SCR-VIS-008: General Plant Map with Work Permits Layer (SIMOPS)

## 1. Purpose and Operational Context
* **View Objective:** Provide a macro-spatial view (Plot Plan) of the Functional Locations of the industrial plant. It allows safety inspectors to activate a visual Work Permits (PTW) layer to detect dangerous operational crossings (SIMOPS) and orphan permits.
* **Operational Context:** Critical field use by HSEQ personnel with industrial tablets for contractor audit rounds, or in the central permit office for desktop approval.

---

## 2. Visual Artifact

![[SCR-VIS-008-simops-layer.svg]]

---

## 3. Functional Component Inventory

> Inherits styles, elevations, and alarm coding from [[DT-UI-DS-DOC-001]].

| ID       | Control / Component | Visual Role / Content | Semantic Token | Data Link / Behavior Rule |
| :------- | :---------------------- | :------------------------- | :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CMP-01` | L1 Plot Plan Canvas     | Macro plant SVG canvas | `--dt-color-bg-canvas`      | Renders polygons representing Functional Locations (ISO 14224 Levels 1 to 4), not individual pipelines. |
| `CMP-02` | Viewport Toolbar        | Navigation bar | `--dt-color-surface-card`   | Viewer controls. The `[≡ Layers]` button is active and highlighted (`--dt-color-state-info`). |
| `CMP-03` | User Avatar Widget      | Profile control | `--dt-color-surface-card`   | Floating circular button (top right corner). Displays the active user's contextual menu. |
| `CMP-04` | Functional Zone Polygon | Zone in the SVG | `--dt-color-border-subtle`  | Represents an area (e.g., *Crude Tanks*). In normal state, it has a subtle border and transparent background. |
| `CMP-05` | PTW Overlay Badges      | Active permit icons | Security Matrix | Superimposed over `CMP-04` polygons. They apply mandatory redundant coding. |
| `CMP-06` | Popover / Tooltip       | PTW pop-up card | `--dt-color-surface-raised` | Deployed upon clicking on a `CMP-05`. Shows: Type, Contractor, HSEQ, Schedule, and Status (`FR-184`). Elevation: `--dt-z-overlay-card`. |
| `CMP-07` | SIMOPS Integrity Panel  | Orphan alerts panel | `--dt-color-surface-card`   | Side panel/Bottom Sheet. Activated only if there are approved permits whose Tags do not exist on the graphic canvas (`FR-185`). |
| `CMP-08` | Filter Chips            | PTW filter button panel | `--dt-color-surface-base`   | Row of floating chips at the canvas base: `[Hot]`, `[Heights]`, `[Confined]`, `[Electrical]`. Allows visual isolation of permit types (`FR-188`). |

---

## 4. Screen State Matrix

| State | Visual Modification in the Interface | Activation Condition |
| :--- | :--- | :--- |
| **Normal (Inactive Layer)** | The canvas shows the zones in neutral grayscale without superimposed badges. | The user deactivates the "PTW Layer" switch/button. |
| **Active PTW Layer** | The `CMP-05` icons appear over their respective geographical zones. | Activation of the Layers button in `CMP-02`. |
| **Selected Permit** | The `CMP-05` icon highlights its outline and the floating card `CMP-06` opens next to the icon, without obscuring the rest of the plant. | Click/Tap on a permit icon on the canvas. |
| **Detected Orphanhood (SIMOPS Alert)** | Panel `CMP-07` is forcibly opened, highlighting in red (`--dt-color-alarm-critical`) the number of broken permits. | Initial load detects referential inconsistency or SignalR sends a permit without coordinates. |
| **Loss of Synchronization** | Amber banner (`--dt-color-alarm-warning`) indicates "Operating with cached data". The PTW icons remain visible but dimmed. | Loss of connection with SignalR / Server. |

---

## 5. Interaction Rules and Data Flow

### 5.1. Spatial Layer Rendering
1. Upon loading the L1 view, the system draws the Functional Locations.
2. If the PTW Layer selector is active, the system queries the `WorkPermits` in the `APPROVED` state.
3. The system cross-references the `EquipmentUnitId` of each permit with the drawn polygons to position the safety icons (`FR-185`).

### 5.2. Integrity Panel (Visualization Failures)
1. If a `WorkPermit` points to an asset that does not have `MeshMapping` on this map, the permit is classified as Orphan.
2. The icon is NOT drawn arbitrarily on the map. Instead, it is injected into the side panel `CMP-07` ("Visualization Failures").
3. The HSEQ Inspector must process the list in panel `CMP-07` to reassign or resolve the geometric inconsistencies (`FR-186`).

### 5.3. Real-Time Synchronization
1. The view subscribes to Work Permits domain events via SignalR (`TR-010`).
2. When a contractor revokes or finalizes a permit, the `CMP-05` icon disappears from the map in $< 5\text{s}$ without requiring the inspector to refresh the page (`FR-187`).

---

## 6. Industrial and Safety Considerations

* **SIMOPS Situational Awareness:** The design of the `CMP-06` popover is restricted in size so that, when inspecting a Hot Work Permit, the inspector continues to see if there is a Confined Space Permit a few meters away on the background canvas.
* **Filtering Ergonomics:** The `Filter Chips` panel (`CMP-08`) does not require navigation through dropdown menus; operators with gloves can toggle risk categories with a single direct touch at the base of the screen.