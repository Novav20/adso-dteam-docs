---
id: UC-VIS-008
name: Visualize Work Permits Overlay (Digital Twin)
module: vis
user_story: VIS-008
primary_actor: HSEQ Inspector
secondary_actors: []
---

# UC-VIS-008: Visualize Work Permits Overlay (Digital Twin)

## 1. Description
Allows the spatial mapping and real-time visualization of high-risk operational permits (e.g., Hot Work, Confined Space) directly onto the interactive 2D/3D plant schematics (Visual Layer). By overlaying logical safety contexts onto the physical layout, it enhances operational situational awareness and strictly supports Simultaneous Operations (SIMOPS) control, mitigating interference risks.

## 2. Preconditions
* The Inspector is authenticated in the platform with the authorized role of "HSEQ Inspector" [TR-006](../../../requirements/common/TR-006.md).
* There are active work permits in operational status (`APPROVED`).
* The interactive installation schematic is correctly loaded in the user's viewer.

## 3. Main Flow
1. The Inspector accesses the Digital Twin viewer and activates the "Work Permits" layer control.
2. The System retrieves the active permits and executes a referential integrity validation by crossing the asset identifiers (`TagNumber`) against the spatial metadata of the current schematic.
3. The System renders the valid permits by overlaying icons on the affected assets. It uses redundant visual coding (Color + Shape) based on the HPHMI Grayscale philosophy [TR-011](../../../requirements/common/TR-011.md) to mitigate cognitive fatigue (e.g. Hot Work: Red Square; Heights: Blue Triangle).
4. The Inspector selects or hovers the cursor over one of the rendered icons.
5. The System displays a pop-up information card showing key metadata without obstructing the schematic: Permit Type, Contractor, HSEQ Responsible, Time Window, Status (Active / Expiring Soon) and associated LOTO reference (if applicable).
6. The Inspector applies visualization filters by risk category (e.g. "Confined Space") and the System updates the view instantly.
7. The System listens to domain events in real-time [TR-010](../../../requirements/common/TR-010.md). If a permit changes status (e.g., enters the expiring soon window, is revoked, or a new one is created), the System dynamically updates the visual appearance of the icon without requiring an interface reload.

## 4. Alternate Flows
### AF-001: Broken Link Detected (SIMOPS Integrity Alert)
In step 2, if the system detects an active permit whose associated asset does not exist in the current schematic or lacks spatial coordinates:
1. The System skips rendering the icon on the schematic to avoid false spatial localizations.
2. The System triggers a prominent visual safety alert ("SIMOPS Integrity Alert") and adds the record to the "Visualization Failures" side panel.
3. The Inspector expands the panel, analyzes the orphaned permit data (ID, Contractor, Expected Tag) and selects the resolution action to request the update of spatial metadata or asset reassignment.

### AF-002: Synchronization Service Interruption (Operational Resilience)
In step 7, if the connection to the real-time propagation service is lost:
1. The System preserves general navigation of the Digital Twin without blocking the user.
2. The System displays a prominent warning banner indicating that the layer is operating with cached data and shows the timestamp of the last reliable synchronization, assuming a conservative state of operational safety.

## 5. Postconditions
* The work permits layer is visually integrated with the spatial model, improving Situational Awareness.
* Geometric inconsistencies and orphaned permits are highlighted prominently to avoid blind risks in SIMOPS.

## 6. Associated Requirements
* **Functional Requirements:** FR-182, FR-183, FR-184, FR-185, FR-186, FR-187, FR-188, FR-189
* **Non-Functional Requirements:** NFR-190, NFR-191, NFR-192, NFR-193, NFR-194, NFR-195
* **Transversal Requirements:** [TR-010](../../../requirements/common/TR-010.md), [TR-011](../../../requirements/common/TR-011.md)
