---
id: UC-VIS-033
name: Inspect Assets on the 2D Base Schematic
module: vis
user_story: VIS-033
primary_actor: Maintenance Technician
secondary_actors:
  - Telemetry Service (IoT)
  - CMMS/EAM Service
---

# UC-VIS-033: Inspect Assets on the 2D Base Schematic

## 1. Description
Provides spatial navigation across plant functional locations using an HPHMI Level 2 canvas (combining Geometric and Semantic Zoom). Selecting an asset deploys an ISA-101 compliant Level 3 Equipment Task Faceplate disclosing operational health with analog limit context, active LOTO/PTW safety boundaries, actionable CMMS Work Orders, and live telemetry, with on-demand drill-down to Level 4 diagnostics.

## 2. Preconditions
* The Maintenance Technician is authenticated with authorized field execution permissions on the visualization module [TR-006](../../../requirements/common/TR-006.md).
* The selected functional location (ISO 14224 Level 5) has an interactive schematic and spatial mapping configured in the system.

## 3. Main Flow
1. The technician accesses the Digital Twin module and selects a functional location (ISO 14224 Level 5) from the plant hierarchy.
2. The System retrieves the spatial configuration and renders the base Level 2 Process Area schematic using the neutral HPHMI palette [TR-011](../../../requirements/common/TR-011.md). The canvas supports dual navigation combining **Geometric Zoom** (fluid SVG viewport scaling via mouse wheel or touch gestures) and **Semantic Zoom** (automatic information density switching based on scale thresholds: the zoomed-out view shows equipment silhouettes and critical alarms; the zoomed-in view reveals TagNumber identifiers, connection ports, and process variables).
3. The technician navigates the schematic (via panning and zooming) and selects the graphical representation of a specific equipment unit (ISO 14224 Level 6).
4. The System deploys a contextual **Level 3 Equipment Task Faceplate** containing:
   * Equipment identification: TagNumber, technical description, operational status, and criticality rating.
   * Safety context summary: Active PTW number and verified LOTO isolation tags (e.g., locked boundary valves or breakers).
   * Actionable Work Orders: Active work orders displaying WO ID, Type (Preventive/Corrective), Status (e.g., In Progress, Ready), and Priority.
5. The System requests a subscription to the asset's real-time physical telemetry channel [TR-010](../../../requirements/common/TR-010.md).
6. The Telemetry Service publishes the equipment's sensor readings.
7. The System processes the asynchronous update and refreshes the values in the Level 3 faceplate, presenting readings contextualized with normal operating ranges and alarm limits without interrupting canvas navigation.
8. (Optional) The technician triggers a drill-down action to consult Level 4 Diagnostics (complete equipment master catalog, technical datasheets, and full CMMS maintenance history).

## 4. Alternate Flows
### AF-001: Inspection of Asset without Spatial Mapping
If the technician locates the asset through the textual search directory instead of the interactive schematic:
1. The System checks if the asset has spatial metadata linked to the current schematic.
2. Upon detecting the absence of mapping, the System deploys the Level 3 faceplate in unmapped mode and disables the "Locate on Schematic" control.
3. The System displays an informative neutral badge: "Spatial Mapping Pending for this asset (ISO 14224 Level 6 unlinked)".

### AF-002: Telemetry Signal Loss (Diagnostic State)
In step 6, if the connection to the telemetry data stream is interrupted:
1. The System detects the drop in the real-time subscription [TR-010](../../../requirements/common/TR-010.md).
2. The System freezes the last received readings, applies Priority 4 Diagnostic coding (neutral/magenta diagnostic indicator and warning symbol per ISA-101/HPHMI, avoiding process alarm colors), and displays the disconnection timestamp: "Stale Data. Connection Lost at [timestamp]".
3. The System automatically resumes dynamic updates once the link is restored.

## 5. Postconditions
* The technician gains centralized Level 3 situational awareness of the asset's operational state, safety boundaries, task readiness, and telemetry with operational limits.
* Direct navigation paths are enabled for on-demand Level 4 diagnostics or CMMS Work Order execution.
* The base canvas is initialized and ready to support the overlay of advanced security layers (Work Permits and LOTO).

## 6. Associated Requirements
* **Functional Requirements:** FR-598, FR-599, FR-600, FR-601, FR-602
* **Non-Functional Requirements:** NFR-603, NFR-604, NFR-605
* **Transversal Requirements:** [TR-010](../../../requirements/common/TR-010.md), [TR-011](../../../requirements/common/TR-011.md)
