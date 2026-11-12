---
id: UC-INV-027
name: Structure Taxonomy of Functional Locations
module: inv
user_story: INV-027
primary_actor: Project Engineer
secondary_actors:
  - Reliability Engineer
  - Maintenance Planner
  - Auditor
---

# UC-INV-027: Structure Taxonomy of Functional Locations

## 1. Description
Enables defining, reorganizing, and auditing the master hierarchical structure of the industrial facility in strict accordance with ISO 14224:2016 (Levels 1 to 5: Industry, Business Category, Installation, Plant/Unit, and Section/System). By decoupling immutable operational positions (Functional Locations) from physical rotating machinery (Equipment Units), this taxonomy preserves long-term process reliability history, governs inherited operational criticality ($1..10$) and environmental exposure classifications, and guarantees a mathematically coherent tree free of orphan nodes or circular references.

## 2. Preconditions
* The Actor is authenticated in the platform with the `Project Engineer` or `Reliability Engineer` role for taxonomic mutations, or any authorized operational role for hierarchical navigation and consultation ([TR-006](../../../requirements/common/TR-006.md)).
* Standardized ISO 14224 taxonomic level definitions (Levels 1 to 5) and environmental exposure categories are registered in the system.
* The Actor accesses the Functional Locations Tree ([SCR-INV-027](../../../ui-ux/screens/inv/SCR-INV-027.md)) via the Web Portal Inventory and Taxonomy navigation menu ([DT-UI-NAV-DOC-001 §3.2](../../../ui-ux/DT-UI-NAV-DOC-001.md#32-level-2-process-supervision-and-planning-l2---unit-process)).

## 3. Main Flow
1. The Project Engineer accesses the Functional Locations Tree interface ([SCR-INV-027](../../../ui-ux/screens/inv/SCR-INV-027.md)); the System loads and renders the complete plant hierarchy in under 3 seconds ([NFR-166](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr)), providing search and multi-criteria filtering across operational positions ([FR-164](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr)).
2. The Engineer selects the action to create a root Functional Location (Level 1) or a child Functional Location under an existing parent node ([FR-160](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr)).
3. The System displays the taxonomic registration form, dynamically constraining the target ISO 14224 Hierarchy Level ($1..5$) to be strictly one level below the selected parent node ([FR-161](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr)).
4. The Engineer enters the unique alphanumeric Tag identifier, human-readable Name, technical Description, Operational Criticality index ($1..10$), Geographic Location, and Environmental Exposure classification (`SEVERE`, `MODERATE`, `LOW`, or `UNKNOWN`).
5. The System executes real-time taxonomic integrity validations in under 1 second ([TR-008](../../../requirements/common/TR-008.md), [NFR-167](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr)):
   1. Verifies that the alphanumeric Tag identifier is globally unique across the entire plant taxonomy.
   2. Verifies that the node's hierarchical level ($1..5$) maintains a strict parent-child sequence with its superior node and that a complete path from Level 1 exists ([FR-161](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr)).
6. The System confirms taxonomic validity and previews the candidate SHA-256 cryptographic integrity seal.
7. The Engineer confirms creation of the Functional Location.
8. Within a single atomic transactional boundary ([NFR-168](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr)), the System:
   1. Persists the new Functional Location node in the master taxonomic catalog.
   2. Records an append-only entry in the immutable audit trail ([TR-001](../../../requirements/common/TR-001.md)) with a chained SHA-256 cryptographic integrity hash ([ADR-003](../../../architecture/adr/ADR-003.md)).
9. The System updates the hierarchical tree view, enables the new Level 5 operational position to receive physical Equipment Unit mounting ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md), [SCR-INV-025](../../../ui-ux/screens/inv/SCR-INV-025.md)), and allows exporting the updated taxonomic architecture report ([FR-165](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr)).

## 4. Alternate Flows

### AF-001: Tag Uniqueness or Level Coherence Conflict
In step 5, if the System detects that the entered Tag identifier already exists or that the selected parent node violates the sequential ISO 14224 level order ([FR-161](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr), [TR-008](../../../requirements/common/TR-008.md)):
1. The System interrupts the save operation and blocks submission.
2. The System highlights the conflicting field applying redundant shape and color coding in compliance with WCAG 2.1 AA ([TR-011](../../../requirements/common/TR-011.md)) and displays a specific diagnostic message: *"Taxonomic Integrity Error: The entered Functional Location Tag already exists or violates the sequential ISO 14224 parent-child level hierarchy."*
3. The flow returns to step 4 for correction.

### AF-002: Tree Reorganization and Circular Reference Prevention
When the Engineer reorganizes the hierarchy by moving an existing Functional Location subtree to a new parent node ([FR-162](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr)):
1. The Engineer selects the target Functional Location node, initiates the re-parenting dialog, selects the candidate parent node, and enters an audit justification.
2. The System evaluates structural integrity and cycle prevention in under 1 second ([NFR-167](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr), [TR-008](../../../requirements/common/TR-008.md)).
3. If the candidate parent node is a direct or indirect descendant of the node being moved, or if the move would violate ISO 14224 level depth ($1..5$), the System immediately blocks the operation and issues a critical alert: *"Hierarchy Integrity Violation: Moving this Functional Location to the selected target would create a circular reference or invalid level depth."*
4. If the validation succeeds, the System applies the reorganization atomically ([NFR-168](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr)) and seals the structural mutation in the immutable SHA-256 audit trail ([TR-001](../../../requirements/common/TR-001.md)).

### AF-003: Attempt to Delete Occupied or Parent Functional Location
When the Engineer attempts to remove a Functional Location node ([FR-163](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr)):
1. The System inspects the node's active dependencies across the taxonomy and equipment registries ([TR-008](../../../requirements/common/TR-008.md)).
2. If the Functional Location contains dependent child locations or hosts an active mounted Equipment Unit, the System rejects the deletion to prevent data orphanage.
3. The System displays a blocking alert with redundant coding: *"Deletion Denied: This Functional Location contains dependent child nodes or an actively mounted Equipment Unit. Dismount the equipment via Rotable Asset Swap or relocate child nodes before removing this position."*

### AF-004: Concurrent Structure Modification Conflict
In step 8 or during tree reorganization, if another engineer has modified the same parent or target Functional Location branch concurrently ([NFR-169](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr)):
1. The System detects the concurrency version mismatch within the isolated transaction boundary and aborts the stale write without overwriting the concurrent changes.
2. The System refreshes the affected taxonomy branch and alerts the Engineer: *"Concurrent Modification Detected: The target hierarchy branch was updated by another user. Review the refreshed tree structure before re-applying your change."*

## 5. Postconditions
* The ISO 14224 Functional Location tree (Levels 1 to 5) is updated and mathematically consistent, with zero orphan nodes, level inversions, or circular references.
* Level 5 Functional Locations are available for physical Equipment Unit onboarding ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)) and Rotable Asset Swaps ([SCR-INV-025](../../../ui-ux/screens/inv/SCR-INV-025.md)).
* All taxonomic creations, re-parenting movements, and criticality updates are permanently recorded in the SHA-256 chained audit trail ([TR-001](../../../requirements/common/TR-001.md)).

## 6. Associated Requirements
* **Functional Requirements:**
  * [FR-160](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr): Creation of root and child nodes complying with ISO 14224 hierarchical levels.
  * [FR-161](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr): Coherent parent-child level validation preventing disordered levels.
  * [FR-162](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr): Dynamic tree reorganization with structural relationship integrity validation.
  * [FR-163](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr): Restriction against deleting locations with installed Equipment Units or child dependencies.
  * [FR-164](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr): Technical search and filtering across complex organizational structures.
  * [FR-165](../../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr): Generation and export of complete Functional Location architecture reports.
* **Non-Functional Requirements:**
  * [NFR-166](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr): Fluid visualization and navigation of extensive hierarchies with load response under 3 seconds.
  * [NFR-167](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr): Integrity validation and cycle detection execution in under 1 second.
  * [NFR-168](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr): Atomic all-or-nothing execution of tree restructuring operations.
  * [NFR-169](../../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr): Concurrency isolation preventing simultaneous edits from overwriting structural changes.
* **Transversal Requirements:**
  * [TR-001](../../../requirements/common/TR-001.md): Immutable audit trail with SHA-256 cryptographic hash chaining.
  * [TR-005](../../../requirements/common/TR-005.md): Encryption in transit across all taxonomic queries and mutations.
  * [TR-006](../../../requirements/common/TR-006.md): Role-Based Access Control (RBAC) enforcement.
  * [TR-008](../../../requirements/common/TR-008.md): ISO 14224 hierarchy management, uniqueness validation, and cycle prevention.
  * [TR-011](../../../requirements/common/TR-011.md): ANSI/ISA-101 High-Performance HMI grayscale discipline and WCAG 2.1 AA redundant coding.
* **Architectural Decision Records:**
  * [ADR-003](../../../architecture/adr/ADR-003.md): Tamper-evident cryptographic SHA-256 hash chaining for audit logs.
  * [ADR-005](../../../architecture/adr/ADR-005.md): Sequential UUIDv7 primary key generation for taxonomic entities.
  * [ADR-008](../../../architecture/adr/ADR-008.md): Chronological installation history decoupling Functional Locations from physical Equipment Units.