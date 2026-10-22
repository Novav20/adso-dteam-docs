---
id: UC-VIS-008
name: Visualize Work Permits Overlay (Digital Twin)
module: vis
user_story: VIS-008
primary_actor: HSEQ Inspector
secondary_actors:
  - Maintenance Supervisor
  - Reliability Engineer
  - Plant Operations Manager
---

# UC-VIS-008: Visualize Work Permits Overlay (Digital Twin)

## 1. Description
Provides real-time spatial mapping and situational awareness of high-risk operational permits (e.g., Hot Work, Confined Space, Work at Heights) directly onto interactive 2D and 3D plant layout schematics. By projecting regulatory and safety contexts onto physical Equipment Units and Functional Locations, the system visualizes dynamic hazard clearance buffers, automates Simultaneous Operations (SIMOPS) proximity conflict detection, and establishes direct navigation drill-downs to tactical equipment faceplates and Lockout/Tagout (LOTO) isolation packages.

## 2. Preconditions
* The Actor is authenticated in the platform with the role of `HSEQ Inspector` or `Maintenance Supervisor` ([TR-006](../../../requirements/common/TR-006.md)).
* The Actor accesses the Digital Twin viewer from the Web Portal (`1.0 Digital Twin -> 2D Plant Map`) or Mobile Client (`1.0 Plant`) per [DT-UI-NAV-DOC-001](../../../ui-ux/DT-UI-NAV-DOC-001.md).
* Active work permits exist in operational status `APPROVED` ([FR-182](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr)).
* The interactive plant installation schematic is loaded with calibrated spatial mesh mappings linking equipment units to geometric coordinates.

## 3. Main Flow
1. The Inspector accesses the Digital Twin viewer and activates the "Work Permits" layer control in the layer toolbar.
2. The System retrieves the active permits in `APPROVED` status and executes spatial referential resolution, linking each permit through its target Equipment Unit to the spatial metadata and geometric centroid on the active schematic.
3. The System renders the permits governed by the Semantic Zoom Clustering Invariant (ANSI/ISA-101 / Hollifield):
   1. At macro scale ($Z < \text{--dt-zoom-scale-l1-max}$), discrete badges are suppressed to preserve the 90/10 grayscale rule ([TR-011](../../../requirements/common/TR-011.md)), rendering consolidated Zone Cluster Pills at Functional Location centroids summarizing permit counts and types.
   2. At process area scale ($\text{--dt-zoom-scale-l1-max} \le Z < \text{--dt-zoom-scale-l2-max}$), cluster pills expand into Discrete Equipment Badges positioned directly over the corresponding Equipment Units.
   3. Badges enforce 4-channel redundant coding (Geometric Shape + Vector Icon + Saturated Indicator + Alphanumeric Label: `HOT WORK`, `HEIGHTS`, `CONFINED`) per WCAG 2.1 AA.
4. The System evaluates dynamic spatial hazard clearance buffers ($15\text{m}$ for Hot Work, $10\text{m}$ for Confined Space, and $5\text{m}$ default) and computes automated Euclidean proximity checks ($D_{AB} < R_A + R_B$) in real time to detect SIMOPS interference risks ([FR-188](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr)).
5. The Inspector hovers over or taps a rendered equipment badge.
6. The System displays the non-occlusive Context Popover Card: Permit Number, Permit Type, Contractor Name, Responsible Supervisor, Validity Time Window, Lifecycle Status (`APPROVED`), Transient Expiration Indicator (highlighted amber if remaining validity $< 60\text{ min}$), and associated LOTO isolation reference.
7. The Inspector can trigger contextual drill-down navigation from the popover card:
   1. Selecting "View Faceplate" transitions to the Level 3 Equipment Task Faceplate ([SCR-VIS-033](../../../ui-ux/screens/vis/SCR-VIS-033.md)).
   2. Selecting "Inspect Isolation" transitions to the Level 4 LOTO Route Inspection view ([SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md)).
8. The Inspector applies visualization filters by risk category, contractor, or validity window, and the System updates the canvas dynamically without reloading.
9. The System listens to real-time domain events ([TR-010](../../../requirements/common/TR-010.md)), dynamically updating badge states, cluster counters, and hazard buffers when permits transition (`WorkPermitApproved`, `WorkPermitRevoked`, `WorkPermitClosed`, `WorkPermitExpired`).

## 4. Alternate Flows

### AF-001: Orphaned Permit Detected (SIMOPS Negative Interlock)
In step 2, if the System detects an approved permit whose associated equipment unit lacks calibrated spatial coordinates or does not exist on the active schematic:
1. The System activates the negative interlock, strictly suppressing the permit badge from arbitrary canvas placement (e.g., $(0,0)$) to prevent false situational awareness.
2. The System increments the warning counter in the layer toolbar and logs the record in the SIMOPS Integrity Drawer.
3. The Inspector opens the integrity drawer, reviews the unmapped permit attributes (Permit ID, Contractor, Target Tag), and initiates a data reconciliation request without interrupting active canvas navigation.

### AF-002: Real-Time Synchronization Interruption (Diagnostic State)
In step 9, if the connection to the real-time event distribution service is disrupted:
1. The System maintains full pan and zoom navigation of the Digital Twin without blocking user interaction.
2. The System displays a Priority 4 Diagnostic status banner using neutral slate/gray tokens and muted typography (strictly avoiding amber or red process alarm colors per ANSI/ISA-101 and [TR-011](../../../requirements/common/TR-011.md)), indicating cached data mode and displaying the timestamp of the last verified synchronization snapshot ([NFR-194](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr)).
3. If WebGL hardware acceleration is unavailable, the viewer seamlessly degrades to 2D vector SVG rendering ([NFR-195](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr)).
4. Upon link recovery, dynamic real-time subscription is re-established automatically.

### AF-003: SIMOPS Spatial Conflict / Proximity Violation Breach
In step 4, if the automated proximity calculation detects overlapping hazard clearance buffers between incompatible concurrent permits ($D_{AB} < R_A + R_B$):
1. The System renders visual diagonal hazard hatching across the overlapping intersection zone and applies pulsing alarm halos to the affected equipment badges.
2. The System displays an emergency SIMOPS conflict pill in the layer toolbar and presents a non-modal warning notification detailing the conflicting permits and distance breach.
3. The Inspector clicks the conflict pill to highlight the spatial conflict zone, review environmental safety interlocks, and coordinate operational de-confliction or work postponement with area supervisors.

## 5. Postconditions
* Active work permits are spatially integrated onto the plant layout with dynamic hazard clearance buffers, delivering Level 3 Situational Awareness.
* Visual density is dynamically regulated across zoom scales, preserving the 90/10 grayscale design philosophy for critical process alarms.
* Spatial collisions and orphaned permits are highlighted via non-modal interlocks and integrity drawers, eliminating undetected SIMOPS operational hazards.
* Actionable navigation handoffs are established connecting the spatial map to tactical Level 3 equipment faceplates ([SCR-VIS-033](../../../ui-ux/screens/vis/SCR-VIS-033.md)) and Level 4 LOTO route verification ([SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md)).

## 6. Associated Requirements
* **Functional Requirements:** [FR-182](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-183](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-184](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-185](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-186](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-187](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-188](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-189](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr)
* **Non-Functional Requirements:** [NFR-190](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-191](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-192](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-193](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-194](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-195](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr)
* **Transversal Requirements:** [TR-005](../../../requirements/common/TR-005.md), [TR-006](../../../requirements/common/TR-006.md), [TR-010](../../../requirements/common/TR-010.md), [TR-011](../../../requirements/common/TR-011.md)
