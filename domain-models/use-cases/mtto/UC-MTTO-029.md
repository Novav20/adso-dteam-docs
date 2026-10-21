---
id: UC-MTTO-029
name: Define Asset Physical Boundaries (Boundaries)
module: mtto
user_story: MTTO-029
primary_actor: Reliability Engineer
secondary_actors: []
---

# UC-MTTO-029: Define Asset Physical Boundaries (Boundaries)

## 1. Description
Guarantees taxonomic consistency and strict physical scoping of assets following the principles of ISO 14224. This use case defines the logical and physical boundary (P&ID reference, start/end) of an equipment unit (Level 6), ensuring that its subunits (Level 7) and maintainable items (Level 8) are exclusively framed within said limit, preventing overlapping assignments and generating a solid baseline for failure analysis.

## 2. Preconditions
* The Engineer is authenticated in the web system with the "Reliability Engineer" role [TR-006](../../../requirements/common/TR-006.md).
* The asset (Equipment Unit, Level 6) exists in the master catalog in "DRAFT" status.
* The master components (Subunits and Maintainable Items) that will be associated are available in the master reference tables.

## 3. Main Flow
1. The Reliability Engineer accesses the technical data sheet of an asset in draft status and selects the option "Configure Physical Boundaries".
2. The System displays the configuration form, making the following fields mandatory:
   - Reference to the Piping and Instrumentation Diagram (P&ID).
   - Physical description of the initial boundary (process start point).
   - Physical description of the final boundary (process end point).
   - Structuring of Subunits (Level 7) associated with the equipment.
   - Selection of one or more logical components (Maintainable Items, Level 8) linked to their respective subunits.
3. The Engineer enters the diagram "PID-1045", the initial boundary ("4-inch suction flange"), the final boundary ("3-inch discharge flange"), defines the subunit "Sealing System" and associates the component "Mechanical Seal" to it.
4. The System executes an automatic validation of uniqueness and hierarchical integrity [TR-008](../../../requirements/common/TR-008.md):
   - It verifies at runtime that none of the selected components currently belong to the boundaries of another operational master asset in the catalog.
   - It verifies that the parent-child relationships (Equipment $\to$ Subunit $\to$ Item) remain coherently structured.
5. The System confirms that the boundaries and selected components are free of collisions and are taxonomically consistent.
6. The Engineer confirms saving the configuration.
7. The System:
   - Atomically persists the physical boundary, P&ID reference and logical component association in the database.
   - Records the transaction in the immutable audit [TR-001](../../../requirements/common/TR-001.md) via an append-only log with its corresponding chained cryptographic integrity hash.
8. The System updates the technical status of the asset's data sheet, enabling it for the final validation and commissioning flow.

## 4. Alternate Flows
### AF-001: Assignment Collision (Duplicate Component)
In step 4, if the system validation detects that one of the selected components (e.g., "Mechanical Seal SM-02") is already assigned to the boundaries of another registered equipment unit:
1. The System interrupts the saving process.
2. The System highlights the conflicting component in the interface applying redundant Shape + Color coding (warning icon and contrast) according to WCAG 2.1 AA, and displays an error message: "ISO 14224 consistency error: The selected component already belongs to the physical boundaries of another asset. Unlink the component from the source asset before saving."
3. The flow returns to step 3.

### AF-002: Connection Loss (Progress Preservation)
During field configuration, if the client experiences an unexpected crash or temporary connection loss:
1. The System locally preserves the progress and the temporary hierarchical structure built in the form.
2. Upon restoring the session or reopening the boundaries form, the System recovers the screen state and allows continuing with the normal flow from step 3.

### AF-003: Read-Only Boundary Consultation (Mobile in Field)
If a Maintenance Technician is consulting an asset's data sheet in the field from their mobile device:
1. The Technician selects the option "View Technical Boundaries".
2. The System displays the asset's technical information in read-only mode, showing the P&ID reference, process physical descriptions (start/end) and the relationship of subunits and components in a hierarchical dropdown format.

## 5. Postconditions
* The draft asset has its physical boundaries, engineering references (P&ID) and logical components (Levels 7 and 8) safely defined in the database.
* The asset is mandatorily enabled for technical validation and subsequent operational activation.
* Structural changes to the hierarchy are recorded in the cryptographic audit trail.

## 6. Associated Requirements
* **Functional Requirements:** FR-091, FR-092, FR-093, FR-094, FR-095, FR-096, FR-097, FR-098
* **Non-Functional Requirements:** NFR-099, NFR-100, NFR-101, NFR-102, NFR-103
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-006](../../../requirements/common/TR-006.md), [TR-008](../../../requirements/common/TR-008.md)
