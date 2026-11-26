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
Provides real-time spatial mapping and situational awareness of high-risk operational permits (e.g., Hot Work, Confined Space, Work at Heights) directly onto interactive plant layout spatial representations. By projecting regulatory and safety contexts onto physical Equipment Units and Functional Locations, the system visualizes dynamic hazard clearance buffers, automates Simultaneous Operations (SIMOPS) proximity conflict detection, and establishes direct operational handoffs to tactical equipment inspection and Lockout/Tagout (LOTO) isolation packages.

## 2. Preconditions
* The Actor is authenticated in the platform with the role of `HSEQ Inspector` or `Maintenance Supervisor` ([TR-006](../../../requirements/common/TR-006.md)).
* The Actor accesses the Digital Twin plant spatial overview in an authorized web or mobile operational session.
* Active work permits exist in operational status `APPROVED` ([FR-182](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr)).
* The active plant spatial representation is loaded with calibrated spatial mappings linking Equipment Units to geometric coordinates.

## 3. Main Flow
1. The Inspector opens the Digital Twin spatial overview and activates the Work Permits visibility scope.
2. The System retrieves the active permits in `APPROVED` status and executes spatial referential resolution, linking each permit through its target Equipment Unit to the spatial metadata and geometric centroid on the active spatial representation.
3. The System renders the permits governed by the Semantic Zoom Clustering Invariant (ANSI/ISA-101 / Hollifield):
   1. At macro plant-overview zoom scale, individual equipment markers are suppressed to preserve the 90/10 grayscale rule ([TR-011](../../../requirements/common/TR-011.md)), presenting consolidated functional-zone permit clusters at Functional Location centroids summarizing permit counts and risk types.
   2. At process-area zoom scale, zone clusters expand into discrete equipment permit indicators positioned at the corresponding Equipment Units.
   3. Indicators enforce 4-channel redundant coding (Geometric Shape + Vector Icon + Saturated Indicator + Alphanumeric Label: `HOT WORK`, `HEIGHTS`, `CONFINED`) per WCAG 2.1 AA.
4. The System evaluates dynamic spatial hazard clearance buffers ($15\text{m}$ for Hot Work, $13\text{m}$ for Confined Space, and $5\text{m}$ default) and computes automated Euclidean proximity checks ($D_{AB} < R_A + R_B$) in real time to detect SIMOPS interference risks ([FR-188](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr)).
5. The Inspector selects or focuses a displayed equipment permit indicator.
6. The System presents a non-occlusive contextual permit summary disclosing: Permit Number, Permit Type, Contractor Name, Responsible Supervisor, Validity Time Window, Lifecycle Status (`APPROVED`), Transient Expiration Indicator (highlighted amber if remaining validity $< 60\text{ min}$), and associated LOTO isolation reference.
7. From the contextual permit summary, the Inspector may trigger operational drill-downs:
   1. Inspecting equipment condition and task telemetry transitions the Inspector to the Level 3 Equipment Task inspection context ([UC-VIS-033](UC-VIS-033.md)).
   2. Inspecting LOTO isolation barriers transitions the Inspector to the Level 4 LOTO Route Verification workflow ([UC-VIS-011](UC-VIS-011.md)).
8. The Inspector applies filters by risk category, contractor, or validity window, and the System updates the spatial view dynamically without reloading.
9. The System listens to real-time domain events ([TR-010](../../../requirements/common/TR-010.md)), dynamically updating permit indicator states, zone cluster counts, and hazard buffers when permits transition (`WorkPermitApproved`, `WorkPermitRevoked`, `WorkPermitClosed`, `WorkPermitExpired`).

## 4. Alternate Flows

### AF-001: Orphaned Permit Detected (SIMOPS Negative Interlock)
In step 2, if the System detects an approved permit whose associated Equipment Unit lacks calibrated spatial coordinates or does not exist on the active spatial representation:
1. The System activates the negative interlock, strictly suppressing the permit indicator from arbitrary spatial origin placement (e.g., $(0,0)$) to prevent false situational awareness.
2. The System increments the orphaned-permit exception count and records the unmapped permit in the SIMOPS integrity reconciliation list.
3. The Inspector opens the integrity reconciliation list, reviews the unmapped permit attributes (Permit ID, Contractor, Target Tag), and initiates a spatial-mapping reconciliation request without interrupting active spatial navigation.

### AF-002: Real-Time Synchronization Interruption (Diagnostic State)
In step 9, if the connection to the real-time event distribution service is disrupted:
1. The System maintains full pan and zoom navigation across the plant spatial representation without blocking user interaction.
2. The System displays a Priority 4 Diagnostic status notice using neutral slate/gray visual coding and muted typography (strictly avoiding amber or red process alarm colors per ANSI/ISA-101 and [TR-011](../../../requirements/common/TR-011.md)), indicating cached data mode and displaying the timestamp of the last verified synchronization snapshot ([NFR-194](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr)).
3. Upon link recovery, dynamic real-time subscription is re-established automatically.

### AF-003: SIMOPS Spatial Conflict / Proximity Violation Breach
In step 4, if the automated proximity calculation detects overlapping hazard clearance buffers between incompatible concurrent permits ($D_{AB} < R_A + R_B$):
1. The System renders high-salience diagonal hazard indicators across the overlapping intersection zone and highlights the affected equipment permit indicators.
2. The System flags a SIMOPS conflict condition and presents a non-blocking safety notification detailing the conflicting permits and distance breach.
3. The Inspector selects the conflict alert to focus the spatial conflict zone, review environmental safety interlocks, and coordinate operational de-confliction or work postponement with area supervisors.

## 5. Postconditions
* Active work permits are spatially integrated onto the plant layout with dynamic hazard clearance buffers, delivering Level 3 Situational Awareness.
* Visual density is dynamically regulated across zoom scales, preserving the 90/10 grayscale design philosophy for critical process alarms.
* Spatial collisions and orphaned permits are surfaced via non-blocking interlocks and integrity reconciliation records, eliminating undetected SIMOPS operational hazards.
* Actionable operational handoffs connect the spatial plant overview to Level 3 equipment inspection ([UC-VIS-033](UC-VIS-033.md)) and Level 4 LOTO route verification ([UC-VIS-011](UC-VIS-011.md)).

## 6. Associated Requirements
* **Functional Requirements:** [FR-182](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-183](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-184](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-185](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-186](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-187](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-188](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr), [FR-189](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr)
* **Non-Functional Requirements:** [NFR-190](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-191](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-192](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-193](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-194](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr), [NFR-195](../../../requirements/user-stories/vis/VIS-008.md#non-functional-requirements-nfr)
* **Transversal Requirements:** [TR-005](../../../requirements/common/TR-005.md), [TR-006](../../../requirements/common/TR-006.md), [TR-010](../../../requirements/common/TR-010.md), [TR-011](../../../requirements/common/TR-011.md)
* **Related Screens:** [SCR-VIS-008](../../../ui-ux/screens/vis/SCR-VIS-008.md), [SCR-VIS-033](../../../ui-ux/screens/vis/SCR-VIS-033.md), [SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md)
