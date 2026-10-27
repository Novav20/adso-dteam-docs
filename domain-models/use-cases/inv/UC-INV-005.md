---
id: UC-INV-005
name: Register Equipment Unit Master Record
module: inv
user_story: INV-005
primary_actor: Project Engineer
secondary_actors:
  - Reliability Engineer
---

# UC-INV-005: Register Equipment Unit Master Record

## 1. Description
Allows the formal onboarding and digital registration of a new physical machinery item (Equipment Unit, ISO 14224 Level 6) into the master technical catalog. The process establishes its technical boundary limits, links it to an active Functional Location (ISO 14224 Level 5) from which it inherits process Tag Number and operational criticality, defines Safety Critical Element (SCE) designations, and validates chronological milestone integrity within an atomic, cryptographically audited transaction.

## 2. Preconditions
* The Project Engineer (or authorized Reliability Engineer) is authenticated in the system with asset onboarding permissions ([TR-006](../../../requirements/common/TR-006.md)).
* The master plant taxonomy of Functional Locations (ISO 14224 Level 1 to Level 5) is configured in the system ([SCR-INV-027](../../../ui-ux/screens/inv/SCR-INV-027.md)).
* Standard Equipment Classes are defined in the reference taxonomy dictionary.
* The Engineer accesses the creation workflow from the Equipment Master Catalog ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)) or via node context action in the Functional Locations Tree ([SCR-INV-027](../../../ui-ux/screens/inv/SCR-INV-027.md)).

## 3. Main Flow
1. The Engineer accesses the Equipment Master Catalog interface ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)) and triggers the "Register New Equipment Unit" action.
2. The System renders the onboarding form requesting physical identification, physical boundary limits, technical classification, safety flags, and chronological milestones.
3. The Engineer enters physical machinery identification attributes (Serial Number, Manufacturer, Model), physical battery limits (Boundary Start and Boundary End describing upstream and downstream connection interfaces), technical classification (Equipment Class), Safety Critical Element (SCE) boolean flag, and lifecycle chronological milestones (Purchase Date, Acquisition Date, Installation Date, and Planned Start of Operation Date).
4. The Engineer selects the target Functional Location from the hierarchical plant taxonomy tree to which the equipment unit will be mounted. The System presents the inherited process Tag Number and operational criticality assigned to that position.
5. The Engineer submits the registration request.
6. The System validates that all mandatory ISO 14224 Level 6 attributes are present (Serial Number, Manufacturer, Model, Equipment Class, physical battery limits, and lifecycle milestones).
7. The System validates that the Serial Number is globally unique across all equipment units in the master catalog.
8. The System verifies that the target Functional Location does not currently host an active mounted equipment unit.
9. The System validates the chronological sequence integrity: Purchase Date $\le$ Acquisition Date $\le$ Installation Date $\le$ Start of Operation Date.
10. The System executes an atomic transaction that:
    - Formalizes the new Equipment Unit record with initial lifecycle state (`lifecycle_status: COMMISSIONING`, `operational_status: STANDBY`, `maintenance_status: OPERATIONAL`, `health_status: UNDETERMINED`), linking it to the designated Functional Location.
    - Initiates the active installation timeline record marking the equipment unit as mounted at the selected Functional Location with the current timestamp.
    - Records an append-only entry in the immutable audit trail ([TR-001](../../../requirements/common/TR-001.md)) with a chained cryptographic integrity hash (SHA-256), capturing user identity, timestamp, Serial Number, inherited Tag Number, Equipment Class, SCE flag, and associated Functional Location.
11. The System presents a confirmation notification and transitions the view to the detailed Equipment Master Data Card ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)) in view mode, exposing operational actions for boundary definition ([SCR-MTTO-029](../../../ui-ux/screens/mtto/SCR-MTTO-029.md)), spare parts Kardex history ([SCR-INV-006](../../../ui-ux/screens/inv/SCR-INV-006.md)), and rotable equipment swap ([SCR-INV-025](../../../ui-ux/screens/inv/SCR-INV-025.md)).

## 4. Alternate Flows
### AF-001: Incomplete Mandatory Technical Data (Redundant Coding)
In step 6, if mandatory attributes (Serial Number, Manufacturer, Model, Equipment Class, or physical battery limits) are missing:
1. The System prevents registration finalization.
2. The System highlights the missing inputs applying redundant Shape + Color encoding (warning icon and high-contrast outline) conforming to WCAG 2.1 AA ([TR-011](../../../requirements/common/TR-011.md)) and displays a notification: "ISO 14224 Validation Error: Mandatory technical identification and physical boundary attributes are required to formalize the equipment unit."
3. The flow returns to step 3.

### AF-002: Serial Number Conflict (Duplicate Physical Machinery)
In step 7, if the entered Serial Number already exists in the master equipment catalog:
1. The System halts registration to preserve catalog uniqueness.
2. The System issues an integrity warning: "Duplicate Equipment Conflict: An equipment unit with this Serial Number is already registered in the master catalog. Verify physical nameplate data."
3. The flow returns to step 3.

### AF-003: Chronological Milestone Sequence Violation
In step 9, if the chronological milestones violate the sequence invariant (Purchase Date $\le$ Acquisition Date $\le$ Installation Date $\le$ Start of Operation Date):
1. The System interrupts the submission.
2. The System highlights the conflicting dates and issues a temporal consistency alert: "Chronological Sequence Inconsistency: Milestone dates must follow the logical progression (Purchase $\le$ Acquisition $\le$ Installation $\le$ Operation Start)."
3. The flow returns to step 3 for date adjustment.

### AF-004: Occupied Functional Location Conflict
In step 8, if the selected Functional Location currently hosts an active mounted equipment unit:
1. The System blocks the assignment to enforce the single-equipment occupancy rule per functional location.
2. The System issues an allocation alert: "Location Occupied: The selected Functional Location currently has an active equipment unit installed. Dismount the existing unit via Rotable Asset Swap ([UC-INV-025](UC-INV-025.md)) before mounting a new unit, or select an unoccupied location."
3. The flow returns to step 4 so the Engineer can select an alternative location or abort the mounting association.

### AF-005: Safety Critical Element (SCE) Attestation Guard
In step 3, if the Engineer designates the equipment unit as a Safety Critical Element (`is_sce: true`):
1. The System displays a safety confirmation prompt requiring the Engineer to acknowledge that this equipment unit governs critical barrier protection under ISO 45001.
2. The System marks the technical record with high-priority safety inspection flags and prompts for verification of isolation points and LOTO route readiness ([SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md)).
3. The flow resumes at step 4.

## 5. Postconditions
* The new Equipment Unit (ISO 14224 Level 6) is formalized in the master catalog in `COMMISSIONING` lifecycle status, uniquely identified by Serial Number.
* The active installation timeline record is instantiated, establishing the operational link between the physical equipment unit and its assigned Functional Location (inheriting process Tag Number and operational criticality).
* The atomic creation transaction is sealed within the immutable append-only audit trail with an unbroken SHA-256 cryptographic hash chain ([TR-001](../../../requirements/common/TR-001.md)).
* Downstream maintenance planning, reliability analysis (RIME), and Digital Twin spatial tracking can reference the equipment unit.

## 6. Associated Requirements
* **Functional Requirements:**
  - [FR-116](../../../requirements/user-stories/inv/INV-005.md): Hierarchical Functional Location linkage.
  - [FR-117](../../../requirements/user-stories/inv/INV-005.md): Global uniqueness of equipment identification.
  - [FR-118](../../../requirements/user-stories/inv/INV-005.md): Mandatory ISO 14224 technical data validation.
  - [FR-119](../../../requirements/user-stories/inv/INV-005.md): Chronological sequence coherence validation.
  - [FR-120](../../../requirements/user-stories/inv/INV-005.md): Consolidated technical record presentation and audited updates.
* **Non-Functional Requirements:**
  - [NFR-121](../../../requirements/user-stories/inv/INV-005.md): Near real-time validation response without interface blocking.
  - [NFR-122](../../../requirements/user-stories/inv/INV-005.md): Multi-aggregate atomic ACID transaction guarantee.
  - [NFR-123](../../../requirements/user-stories/inv/INV-005.md): Historical reliability preservation and prohibition of hard-deletes.
  - [NFR-124](../../../requirements/user-stories/inv/INV-005.md): Creation and registration response time < 2 seconds.
* **Transversal Requirements:**
  - [TR-001](../../../requirements/common/TR-001.md): Immutable audit trail with cryptographic hash chaining (SHA-256).
  - [TR-005](../../../requirements/common/TR-005.md): Relational integrity and foreign key constraints.
  - [TR-006](../../../requirements/common/TR-006.md): Role-Based Access Control (RBAC) authorization.
  - [TR-008](../../../requirements/common/TR-008.md): Audit logging and governance traceability.
  - [TR-011](../../../requirements/common/TR-011.md): High-Performance HMI (HPHMI) redundant coding.
* **Architectural Decision Records:**
  - [ADR-005](../../../architecture/adr/ADR-005.md): Cryptographic audit trail and hash chaining.
