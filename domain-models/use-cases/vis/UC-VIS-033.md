---
id: UC-VIS-033
name: Inspect Equipment Units on the 2D Base Schematic
module: vis
user_story: VIS-033
primary_actor: Maintenance Technician
secondary_actors:
  - Maintenance Supervisor
  - HSEQ Inspector
  - Reliability Engineer
---

# UC-VIS-033: Inspect Equipment Units on the 2D Base Schematic

## 1. Description
Provides spatial plant navigation and situational awareness across Functional Locations and Equipment Units using an HPHMI Level 2 canvas combining Geometric and Semantic Zoom. Selecting an equipment unit deploys an ISA-101 compliant Level 3 Equipment Task Faceplate disclosing operational condition, Moving Analog Indicators (MAI) with trip limits, active LOTO/PTW safety boundaries, and prioritized CMMS Work Orders, establishing secure navigation paths to Level 3 technical data sheets, Level 4 LOTO verification, and field Work Order execution.

## 2. Preconditions
* The Maintenance Technician is authenticated on an authorized workstation or mobile terminal ([TR-006](../../../requirements/common/TR-006.md)).
* The Actor accesses the visualization canvas from the Level 1 Plant Overview ([SCR-VIS-008](../../../ui-ux/screens/vis/SCR-VIS-008.md)), the Functional Location Hierarchy ([SCR-INV-027](../../../ui-ux/screens/inv/SCR-INV-027.md)), or the Command Palette search directory (`CMP-03`).
* The selected Functional Location (ISO 14224 Level 5) has spatial mesh mappings and vector schematics configured in the system.

## 3. Main Flow
1. The Technician accesses the Digital Twin module and selects a Functional Location (ISO 14224 Level 5) or navigates via the plant layout.
2. The System retrieves the spatial configuration and renders the base Level 2 Process Area schematic using the neutral HPHMI palette ([TR-011](../../../requirements/common/TR-011.md)). Viewport scaling supports dual navigation combining Geometric Zoom (smooth coordinate-preserving scaling) and Semantic Zoom governed by canonical design tokens (`--dt-zoom-scale-l1-max`, `--dt-zoom-scale-l2-max`, `--dt-zoom-scale-tactical`).
3. The Technician navigates the canvas (panning/zooming) and selects the graphical representation of a specific Equipment Unit (ISO 14224 Level 6) or locates it via search directory (`CMP-03`); the System smoothly centers the viewport to tactical scale (`--dt-zoom-scale-tactical`) and displays an active highlight halo.
4. The System deploys the contextual Level 3 Equipment Task Faceplate as an absolute overlay guaranteeing zero layout shift on the canvas:
   1. Equipment Identification: Functional Location Tag Number, physical Equipment Unit Serial Number, Equipment Class, Manufacturer, Model, and Operational Status (`UP`, `DOWN`, `STANDBY`).
   2. Safety Context Summary: Active Work Permit number in `APPROVED` status and verified LOTO isolation boundaries (applied padlocks and confirmed zero-energy attestation).
   3. Actionable Work Orders: Active work orders displaying WO ID, Type (Preventive/Corrective), Lifecycle Status (`PLANNING`, `WAITING_PARTS`, `SCHEDULED`, `IN_PROGRESS`), and RIME prioritization score.
   4. Moving Analog Indicators (MAI): Real-time telemetry gauges displaying process variables contextualized with normal operating bands and high/low alarm limits.
5. The System requests a real-time physical telemetry stream for the selected Equipment Unit ([TR-010](../../../requirements/common/TR-010.md)).
6. The Telemetry Service streams live sensor readings (e.g., vibration, winding temperature, discharge pressure).
7. The System updates the MAI indicators dynamically within normal operating limits without causing viewport re-renders or layout shifts.
8. The Technician initiates an actionable tactical handoff:
   1. Selecting "Verify LOTO" routes to LOTO Route Verification ([SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md)).
   2. Selecting "Start Execution" on a scheduled Work Order validates the safety interlock and routes to Mobile Work Order Execution ([SCR-MTTO-002](../../../ui-ux/screens/mtto/SCR-MTTO-002.md)).
   3. Selecting "View Technical Data Sheet" routes to Equipment Master Detail ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)).

## 4. Alternate Flows

### AF-001: Unmapped Equipment Unit Selected (Negative Interlock)
In step 3, if the Technician locates an Equipment Unit via textual directory that lacks spatial coordinates on the active schematic:
1. The System deploys the Level 3 Faceplate in unmapped mode.
2. The System engages the negative interlock, disabling the "Locate on Schematic" control and strictly suppressing arbitrary rendering at $(0,0)$ to prevent false situational awareness.
3. The System displays a neutral badge: *"Spatial Mapping Pending for this Equipment Unit (ISO 14224 Level 6 unlinked)"*.

### AF-002: Telemetry Data Staleness & Diagnostic State (ISA-101)
In step 6, if the connection to the telemetry data stream is interrupted:
1. The System detects the loss of the real-time subscription ([TR-010](../../../requirements/common/TR-010.md)).
2. The System freezes the last received readings and applies Priority 4 Diagnostic coding: renders slate grayish-blue diagnostic indicators with muted typography (`--dt-color-mai-stale-zone`), strictly avoiding amber or red process alarm colors per ANSI/ISA-101.
3. The System displays the disconnection timestamp: *"Stale Data. Connection Lost at [timestamp]"*.
4. Dynamic streaming automatically resumes once the link is restored.

### AF-003: Field Wireless Dropout & Offline Operation
During mobile plant inspection, if wireless network connectivity is completely lost ([TR-007](../../../requirements/common/TR-007.md)):
1. The mobile client preserves active 2D vector plot plan navigation using encrypted local storage.
2. The System displays a persistent diagnostic banner: *"OFFLINE MODE · CACHED SCHEMATIC"*.
3. The faceplate presents cached equipment metadata and freezes telemetry readings with an offline notice.
4. Navigation to field execution workflows ([SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md) or [SCR-MTTO-002](../../../ui-ux/screens/mtto/SCR-MTTO-002.md)) is gated by local cryptographic leases ([ADR-006](../../../architecture/adr/ADR-006.md)).

### AF-004: Critical Process Alarm / Safety Threshold Breach
In step 7, if sensor readings breach high/low safety trip thresholds, or if the unit transitions to `DOWN`:
1. The System immediately highlights the equipment hotspot on the schematic with a high-salience red alarm border and square symbol (`--dt-color-alarm-critical`).
2. The MAI gauge highlights the P1 critical alarm marker, displaying the breach magnitude.
3. The faceplate presents emergency contextual actions, enabling the technician to inspect safety permits or initiate emergency corrective dispatch.

### AF-005: LOTO Safety Guard Interlock on Work Order Start
In step 8, if the Technician attempts to start execution on a Work Order from the faceplate, but the associated isolation points are unverified or active residual energy is detected:
1. The System blocks the state transition and execution navigation.
2. The System deploys a non-dismissible safety interlock modal: *"Safety Guard Interlock: Work Order cannot be initiated. Energy isolation unverified or residual energy detected. Execute LOTO route first."*
3. The System directs the user to "Verify LOTO" ([SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md)).

## 5. Postconditions
* Centralized Level 3 situational awareness is established disclosing operational condition, safety boundaries, and prioritized Work Orders.
* Viewport stability and 90/10 grayscale hygiene are preserved with zero layout shift on the spatial canvas.
* Actionable, secure navigation handoffs connect the spatial canvas to Level 3 technical data sheets ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)), Level 4 LOTO verification ([SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md)), and Level 4 Work Order closure ([SCR-MTTO-002](../../../ui-ux/screens/mtto/SCR-MTTO-002.md)).

## 6. Associated Requirements
* **Functional Requirements:** [FR-598](../../../requirements/user-stories/vis/VIS-033.md#functional-requirements-fr), [FR-599](../../../requirements/user-stories/vis/VIS-033.md#functional-requirements-fr), [FR-600](../../../requirements/user-stories/vis/VIS-033.md#functional-requirements-fr), [FR-601](../../../requirements/user-stories/vis/VIS-033.md#functional-requirements-fr), [FR-602](../../../requirements/user-stories/vis/VIS-033.md#functional-requirements-fr)
* **Non-Functional Requirements:** [NFR-603](../../../requirements/user-stories/vis/VIS-033.md#non-functional-requirements-nfr), [NFR-604](../../../requirements/user-stories/vis/VIS-033.md#non-functional-requirements-nfr), [NFR-605](../../../requirements/user-stories/vis/VIS-033.md#non-functional-requirements-nfr)
* **Transversal Requirements:** [TR-005](../../../requirements/common/TR-005.md), [TR-006](../../../requirements/common/TR-006.md), [TR-007](../../../requirements/common/TR-007.md), [TR-008](../../../requirements/common/TR-008.md), [TR-010](../../../requirements/common/TR-010.md), [TR-011](../../../requirements/common/TR-011.md)
* **Architectural Decisions:** [ADR-006](../../../architecture/adr/ADR-006.md)
