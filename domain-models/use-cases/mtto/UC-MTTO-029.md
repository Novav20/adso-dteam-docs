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
Guarantees taxonomic consistency and strict physical scoping of machinery following ISO 14224:2016 Section 6 and Annex A. This use case defines the logical and physical battery limits (Piping and Instrumentation Diagram reference, initial process boundary, and final process boundary) of an Equipment Unit (ISO 14224 Level 6), ensuring that its Subunits (Level 7) and Maintainable Items (Level 8) are exclusively framed within that boundary. It prevents cross-equipment component ownership collisions, satisfies the mandatory commissioning gate precondition prior to operational activation, and establishes an auditable baseline for maintenance cost control and failure attribution.

## 2. Preconditions
* The Actor is authenticated in the platform with the `Reliability Engineer` or `Maintenance Planner` role for boundary configuration, or `Maintenance Technician` and `Auditor` roles for read-only consultation ([TR-006](../../../requirements/common/TR-006.md)).
* The target Equipment Unit (ISO 14224 Level 6) exists in the master catalog in `COMMISSIONING` lifecycle status awaiting boundary formalization prior to operational activation, or in `INSTALLED` or `IN_STORAGE` lifecycle status undergoing an audited boundary refinement ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)).
* Standardized ISO 14224 Equipment Class definitions, Subunit classifications, and Maintainable Item catalogs are registered in the master taxonomy.

## 3. Main Flow
1. The Reliability Engineer accesses the Equipment Master Data Card ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)) and selects the action to define physical boundaries, opening the Asset Boundary Limits Card ([SCR-MTTO-029](../../../ui-ux/screens/mtto/SCR-MTTO-029.md)) in configuration mode ([FR-091](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)).
2. The System presents the boundary configuration workspace, requiring the following mandatory technical definitions ([FR-092](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr), [FR-096](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr), [FR-102](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)):
   3. Reference to the governing Piping and Instrumentation Diagram (P&ID).
   4. Technical description of the initial physical boundary (upstream suction or power supply interface).
   5. Technical description of the final physical boundary (downstream discharge or load terminal interface).
   6. Decomposition of one or more Subunits (ISO 14224 Level 7) belonging to the Equipment Unit.
   7. Selection and linkage of one or more Maintainable Items (ISO 14224 Level 8) nested under their respective Subunits, including static design parameters and associated spare part families.
8. The Engineer records the P&ID reference (`PID-TFA-1045-REV3`), the initial physical boundary (*"DN200 ANSI 300# suction flange downstream of isolation valve MOV-0101A"*), the final physical boundary (*"DN150 ANSI 600# discharge flange and main motor terminal box M-0101A"*), structures the Level 7 Subunit (*"Primary Sealing System"*), links the Level 8 Maintainable Item (*"Cartridge Mechanical Seal Plan 53A"*), and enters the technical audit justification.
9. The System executes an automated uniqueness and hierarchical integrity verification in under 1 second ([TR-008](../../../requirements/common/TR-008.md), [NFR-093](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [NFR-094](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [NFR-099](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [NFR-100](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr)):
   10. Verifies that none of the selected Level 8 Maintainable Items are currently assigned to the physical boundaries of another Equipment Unit in the catalog.
   11. Verifies that all parent-child relationships (Equipment Unit $\to$ Subunit $\to$ Maintainable Item) remain coherently structured without orphaned nodes or circular references ([NFR-103](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr)).
12. The System confirms that the physical boundaries and component hierarchy are free of ownership collisions and previews the candidate SHA-256 cryptographic integrity seal.
13. The Engineer confirms saving the boundary configuration.
14. Within a single atomic transactional boundary ([NFR-095](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr)), the System:
   15. Persists the physical battery limits, P&ID reference, Level 7 Subunits, and Level 8 Maintainable Item associations on the Equipment Unit master record.
   16. Records the modification in the chronological boundary audit history ([FR-098](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)) and appends an immutable audit trail entry ([TR-001](../../../requirements/common/TR-001.md)) sealed with a chained SHA-256 cryptographic hash ([ADR-003](../../../architecture/adr/ADR-003.md)).
17. The System marks the physical boundary requirement of the Equipment Unit commissioning gate as satisfied ([FR-096](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)) and transitions the view to read-only consultation mode.

## 4. Alternate Flows

### AF-001: Component Ownership Collision (Duplicate Maintainable Item Assignment)
In step 4, if the uniqueness validation detects that a selected Level 8 Maintainable Item (such as *"Mechanical Seal SM-02"*) is already assigned to the physical boundaries of another registered Equipment Unit ([NFR-093](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [TR-008](../../../requirements/common/TR-008.md)):
1. The System interrupts the save operation and blocks form submission.
2. The System highlights the conflicting component applying redundant shape and color coding in compliance with WCAG 2.1 AA ([TR-011](../../../requirements/common/TR-011.md)), identifies the conflicting Equipment Unit tag, and displays an integrity alert: *"ISO 14224 Consistency Error: The selected Maintainable Item already belongs to the physical boundaries of another Equipment Unit. Unlink the component from the source machine before saving."*
3. The flow returns to step 3 so the Engineer can unlink the conflicting component or select an unassigned Maintainable Item.

### AF-002: Session Interruption and Progress Preservation
During boundary configuration in step 3, if the client experiences an unexpected session interruption, temporary network drop, or browser closure ([NFR-101](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr)):
1. The System preserves the in-progress boundary descriptions and temporary Level 7 and Level 8 hierarchy locally in encrypted storage ([TR-002](../../../requirements/common/TR-002.md)).
2. Upon restoring the session and reopening the Asset Boundary Limits Card, the System prompts the Engineer to restore the uncommitted draft and resumes the workflow at step 3 without data loss.

### AF-003: Read-Only Boundary Consultation on Field Mobile Terminal
When a Maintenance Technician inspects an Equipment Unit's battery limits in the field from an industrial tablet ([NFR-097](../../../requirements/user-stories/mtto/MTTO-029.md#non-functional-requirements-nfr), [TR-007](../../../requirements/common/TR-007.md)):
1. The Technician opens the Asset Boundary Limits Card ([SCR-MTTO-029](../../../ui-ux/screens/mtto/SCR-MTTO-029.md)) from the mobile navigation drawer or Equipment Master Data Card.
2. The System presents the P&ID reference, upstream and downstream physical boundary descriptions, the 2D boundary envelope schematic, and the Level 7 Subunit and Level 8 Maintainable Item hierarchy in read-only consultation mode, suppressing all editing controls.

## 5. Postconditions
* The Equipment Unit (ISO 14224 Level 6) has its physical battery limits, P&ID reference, Level 7 Subunits, and Level 8 Maintainable Items atomically persisted and verified free of cross-equipment ownership collisions.
* The physical boundary precondition of the Equipment Unit commissioning gate ([FR-096](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)) is satisfied, enabling subsequent operational activation.
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