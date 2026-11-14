---
id: UC-MTTO-029
name: Define Asset Physical Boundaries (Boundaries)
module: mtto
user_story: MTTO-029
primary_actor: Reliability Engineer
secondary_actors:
  - Maintenance Planner
  - Maintenance Technician
  - Auditor
---

# UC-MTTO-029: Define Asset Physical Boundaries (Boundaries)

## 1. Description
Guarantees taxonomic consistency and strict physical scoping of industrial machinery following ISO 14224:2016 Section 6 and Annex A. This use case governs the definition and field consultation of the physical battery limits (upstream initial process/power interface, downstream final process/load interface, and governing Piping and Instrumentation Diagram reference metadata) of an Equipment Unit (ISO 14224 Level 6), ensuring that its Subunits (Level 7) and Maintainable Items (Level 8) are exclusively framed within that physical envelope. It prevents cross-equipment component ownership collisions, satisfies the mandatory commissioning gate precondition prior to operational activation, and establishes a tamper-evident audit baseline for maintenance cost control and failure attribution.

## 2. Preconditions
* The Actor is authenticated in the platform with the `Reliability Engineer` or `Maintenance Planner` role for boundary configuration, or with `Maintenance Technician` or `Auditor` roles for read-only consultation ([TR-006](../../../requirements/common/TR-006.md)).
* The target Equipment Unit (ISO 14224 Level 6) exists in the master catalog in `COMMISSIONING` lifecycle status awaiting boundary formalization prior to operational activation, or in `INSTALLED` or `IN_STORAGE` lifecycle status undergoing an audited boundary refinement ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)).
* Standardized ISO 14224 Equipment Class definitions, Subunit classifications, and Maintainable Item catalogs are registered in the master taxonomy.

## 3. Main Flow
1. The Reliability Engineer accesses the Asset Boundary Limits Card ([SCR-MTTO-029](../../../ui-ux/screens/mtto/SCR-MTTO-029.md)) directly from the Equipment Master Data Card ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)) or switches to another Equipment Unit via the enterprise equipment lookup filter ([FR-091](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)), entering configuration mode.
2. The System presents the boundary configuration workspace, displaying the equipment's current commissioning readiness status and requiring the following technical definitions ([FR-092](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr), [FR-096](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr), [FR-102](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)):
   * Technical description of the initial physical boundary (upstream suction flange, inlet nozzle, or power supply interface).
   * Technical description of the final physical boundary (downstream discharge flange, outlet header, or motor load terminal interface).
   * Reference metadata identifying the governing Piping and Instrumentation Diagram (P&ID) associated with the battery-limit envelope and component technical design properties.
   * Decomposition of one or more Subunits (ISO 14224 Level 7) belonging to the Equipment Unit.
   * Search, selection, and linkage of one or more Maintainable Items (ISO 14224 Level 8) nested under their respective Subunits, including static design parameters and linked MRO spare part families.
3. The Engineer records the governing P&ID drawing reference (`PID-TFA-1045-REV3`), enters the initial physical boundary (*"DN200 ANSI 300# suction flange downstream of isolation valve MOV-0101A"*), enters the final physical boundary (*"DN150 ANSI 600# discharge flange and main motor terminal box M-0101A"*), structures the Subunit (*"Primary Sealing System"*), searches and links one or more Maintainable Items (*"Cartridge Mechanical Seal Plan 53A"*), and enters a mandatory technical audit justification.
4. The System executes an automated uniqueness and hierarchical integrity verification in under 1 second ([TR-008](../../../requirements/common/TR-008.md), [NFR-093](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [NFR-094](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [NFR-099](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [NFR-100](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr)):
   * Verifies that none of the selected Level 8 Maintainable Items are currently assigned to the physical boundaries of another Equipment Unit in the catalog.
   * Verifies that all parent-child relationships (Equipment Unit $\to$ Subunit $\to$ Maintainable Item) remain coherently structured without orphaned nodes or taxonomic mismatches ([NFR-103](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr)).
5. The System confirms that the physical boundaries and component hierarchy are free of ownership collisions and previews the candidate SHA-256 cryptographic integrity seal alongside the updated 2D boundary envelope schematic.
6. The Engineer confirms saving the boundary configuration.
7. Within a single atomic transactional boundary ([NFR-095](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr)), the System:
   * Persists the initial and final physical battery limits, Subunit definitions, Maintainable Item associations, and P&ID boundary metadata on the Equipment Unit master hierarchy.
   * Records the modification in the chronological boundary audit history ([FR-098](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)) and appends an immutable audit trail entry ([TR-001](../../../requirements/common/TR-001.md)) sealed with a chained SHA-256 cryptographic hash ([ADR-003](../../../architecture/adr/ADR-003.md)).
8. The System clears any temporary local draft, marks the physical boundary requirement of the Equipment Unit commissioning gate as satisfied ([FR-096](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)), and transitions the view to read-only consultation mode.

## 4. Alternate Flows

### AF-001: Component Ownership Collision (Duplicate Maintainable Item Assignment)
In step 4 of the Main Flow, if the uniqueness validation detects that a selected Maintainable Item (such as *"Mechanical Seal SM-02"*) is already assigned to the physical boundaries of another registered Equipment Unit ([NFR-093](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [TR-008](../../../requirements/common/TR-008.md)):
1. The System interrupts the save operation and hard-blocks submission.
2. The System highlights the conflicting component applying redundant shape and color coding in compliance with WCAG 2.1 AA ([TR-011](../../../requirements/common/TR-011.md)), identifies the conflicting Equipment Unit tag, and displays an integrity alert: *"ISO 14224 Consistency Error: The selected Maintainable Item already belongs to the physical boundaries of another Equipment Unit. Unlink the component from the source machine before saving."*
3. The flow returns to step 3 of the Main Flow so the Engineer can unlink the conflicting component or select an unassigned Maintainable Item.

### AF-002: Session Interruption and Progress Preservation
During boundary configuration in step 3 of the Main Flow, if the client experiences an unexpected session interruption, temporary network drop, or browser closure ([NFR-101](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr)):
1. The System preserves the in-progress boundary descriptions and temporary Subunit and Maintainable Item hierarchy locally in encrypted storage ([TR-002](../../../requirements/common/TR-002.md)).
2. Upon restoring the session and reopening the Asset Boundary Limits Card, the System prompts the Engineer to restore or discard the uncommitted draft and resumes the workflow at step 3 without data loss.

### AF-003: Read-Only Boundary Consultation on Field Mobile Terminal
When a Maintenance Technician inspects an Equipment Unit's battery limits in the field from an industrial tablet ([NFR-097](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [TR-007](../../../requirements/common/TR-007.md)):
1. The Technician opens the Asset Boundary Limits Card ([SCR-MTTO-029](../../../ui-ux/screens/mtto/SCR-MTTO-029.md)) from the mobile navigation drawer or Equipment Master Data Card.
2. The System presents the governing P&ID reference, upstream and downstream physical boundary descriptions, the 2D boundary envelope schematic, and the expandable Subunit and Maintainable Item hierarchy (with bottom-sheet detail inspection on portrait viewports) strictly in read-only consultation mode, suppressing all editing controls.

### AF-004: Incomplete Mandatory Boundary Definition or Audit Justification
In step 6 of the Main Flow, if the Engineer attempts to commit the configuration while the initial boundary, final boundary, at least one Subunit with a linked Maintainable Item, or the mandatory technical audit justification is missing ([FR-096](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)):
1. The System blocks submission, highlights omitted mandatory fields with redundant warning indicators, and displays inline validation guidance specifying the missing elements required to formalize the Equipment Unit.
2. The flow returns to step 3 of the Main Flow until all mandatory boundary criteria are completed.

## 5. Postconditions
* The Equipment Unit (ISO 14224 Level 6) has its initial and final physical battery limits, governing P&ID boundary metadata, Subunits (Level 7), and Maintainable Items (Level 8) atomically persisted and verified free of cross-equipment ownership collisions.
* The physical boundary precondition of the Equipment Unit commissioning gate ([FR-096](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)) is satisfied, enabling subsequent operational activation in [SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md) and preventive or condition-based scheduling in [SCR-MTTO-001](../../../ui-ux/screens/mtto/SCR-MTTO-001.md) and [SCR-MTTO-023](../../../ui-ux/screens/mtto/SCR-MTTO-023.md).
* All structural boundary adjustments are permanently recorded in the chronological engineering audit history with an unbroken SHA-256 cryptographic hash chain ([FR-098](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr), [TR-001](../../../requirements/common/TR-001.md)).

## 6. Associated Requirements
* **Functional Requirements:**
  * [FR-091](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr): Access to technical boundary configuration from Level 6 Equipment Unit management.
  * [FR-092](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr): Initial boundary, final boundary, and multi-selection of Level 8 Maintainable Items.
  * [FR-096](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr): Mandatory boundary definition prior to Equipment Unit formalization.
  * [FR-098](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr): Chronological history of boundary adjustments for engineering audits.
  * [FR-102](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr): Support for complex technical boundary descriptions.
* **Non-Functional Requirements:**
  * [NFR-093](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr): Single-asset exclusivity preventing a component from belonging to multiple Equipment Units simultaneously.
  * [NFR-094](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr): Deep hierarchical parent-child consistency across Levels 6, 7, and 8.
  * [NFR-095](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr): Atomic transaction guarantee preventing partial or inconsistent boundary records.
  * [NFR-097](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr): Read-only boundary consultation access for field technical personnel.
  * [NFR-099](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr): Component duplication validation response time under 1 second.
  * [NFR-100](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr): High-volume catalog hierarchy validation without performance degradation.
  * [NFR-101](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr): Local form progress preservation against session losses or unexpected browser closures.
  * [NFR-103](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr): Data integrity verification routines to detect historical hierarchical anomalies.
* **Transversal Requirements:**
  * [TR-001](../../../requirements/common/TR-001.md): Immutable audit trail with SHA-256 cryptographic hash chaining.
  * [TR-002](../../../requirements/common/TR-002.md): Data encryption at rest for locally preserved configuration drafts and offline boundary caches.
  * [TR-005](../../../requirements/common/TR-005.md): Encryption in transit across all boundary queries and validation requests.
  * [TR-006](../../../requirements/common/TR-006.md): Role-Based Access Control (RBAC) enforcement.
  * [TR-007](../../../requirements/common/TR-007.md): Offline-first synchronization and field equipment boundary consultation.
  * [TR-008](../../../requirements/common/TR-008.md): ISO 14224 hierarchy management, component uniqueness, and cycle prevention.
  * [TR-011](../../../requirements/common/TR-011.md): ANSI/ISA-101 High-Performance HMI grayscale discipline and WCAG 2.1 AA redundant coding.
* **Architectural Decision Records:**
  * [ADR-003](../../../architecture/adr/ADR-003.md): Tamper-evident cryptographic SHA-256 hash chaining for audit logs.
  * [ADR-005](../../../architecture/adr/ADR-005.md): Sequential UUIDv7 identifier generation for taxonomic entities.
