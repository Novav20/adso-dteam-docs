---
id: UC-INV-027
name: Structure Taxonomy of Functional Locations
module: inv
user_story: INV-027
primary_actor: Reliability Engineer
secondary_actors: []
---

# UC-INV-027: Structure Taxonomy of Functional Locations

## 1. Description
Allows defining and modifying the master hierarchical structure of the plant according to ISO 14224 (Levels 1 to 5: Industry, Business, Installation, Plant, Section). This taxonomy provides the logical and geographical context where physical assets (Equipment Units) operate, accumulating operational costs and maintaining structural consistency without cycles or orphan nodes.

## 2. Preconditions
* The Engineer is authenticated in the system with the "Reliability Engineer" role [TR-006](../../../requirements/common/TR-006.md).
* The master configuration of ISO 14224 taxonomic levels is defined.

## 3. Main Flow
1. The Engineer accesses the Taxonomy module and selects the "Add Functional Location" option.
2. The System displays the registration form and dynamically adjusts the required fields according to the selected ISO Hierarchical Level (Levels 1 to 5).
3. The Engineer enters the Technical Identifier (Tag), Name, Operational Criticality, Geographical Location / Environmental Exposure and the engineering blueprint reference (P&ID). Optionally, selects the parent node in the hierarchy.
4. The System executes the domain taxonomic validations [TR-008](../../../requirements/common/TR-008.md):
   - Validates that the Tag is globally unique in the system.
   - Validates that the hierarchical level of the new node is strictly coherent with its parent node (e.g., a Level 4 must be a child of a Level 3).
5. The Engineer confirms the node creation.
6. The System:
   - Atomically persists the new node in the database's taxonomic catalog.
   - Records the operation in the immutable audit trail [TR-001](../../../requirements/common/TR-001.md) via an append-only record with its corresponding chained cryptographic integrity hash (SHA-256).
7. The System updates the taxonomic tree view and confirms the success of the operation.

## 4. Alternate Flows
### AF-001: Uniqueness Conflict (Duplicate Tag)
In step 4, if the System detects that the Tag is already in use:
1. The System interrupts the transaction.
2. The System highlights the conflicting field applying redundant Shape + Color coding (warning symbol and contrast indicator) according to WCAG 2.1 AA and alerts: "The entered location Tag already exists. Identifiers must be unique across the entire taxonomy."
3. The flow returns to step 3.

### AF-002: Tree Reorganization (Cycle Prevention)
If the Engineer decides to move an existing functional location to a new parent node:
1. The Engineer selects the location and defines its new destination node (Re-parenting).
2. The System invokes the structural integrity domain validation.
3. If the System detects that the destination node is a direct or indirect descendant of the node being moved, it blocks the action immediately.
4. The System issues a critical alert: "Integrity violation: The operation would generate an infinite cycle in the hierarchy."
5. If the validation is successful, the System applies the movement atomically and records the structural change in the immutable audit [TR-001](../../../requirements/common/TR-001.md).

### AF-003: Attempt to Delete Occupied Node
If the Engineer attempts to delete an existing functional location:
1. The System validates the node's dependencies.
2. If the location has child locations or possesses a physical asset (Equipment Unit) currently installed, the System rejects the deletion.
3. The System notifies: "Action denied: The functional location contains installed assets or hierarchical dependencies. Relocate the elements before proceeding."

## 5. Postconditions
* The taxonomic tree is updated and mathematically consistent, without orphan nodes or closed cycles.
* The new functional locations are enabled to receive physical asset installation (Asset Swap).
* The structural evolution of the plant is permanently recorded for audits.

## 6. Associated Requirements
* **Functional Requirements:** FR-160, FR-161, FR-162, FR-163, FR-164, FR-165
* **Non-Functional Requirements:** NFR-166, NFR-167, NFR-168, NFR-169
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-006](../../../requirements/common/TR-006.md), [TR-008](../../../requirements/common/TR-008.md)
