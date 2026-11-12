---
id: UC-MTTO-002
name: Execute and Finalize Work Order
module: mtto
user_story: MTTO-002
primary_actor: Maintenance Technician
secondary_actors:
  - Maintenance Supervisor
  - Reliability Engineer
  - Warehouse Manager
---

# UC-MTTO-002: Execute and Finalize Work Order

## 1. Description
Governs the mobile execution workflow of an active Work Order on the plant floor. It enforces task checklist completion, material and spare parts consumption (including rotable asset swap modal handoffs), multi-evidence photographic capture with client-side cryptographic hashing, and comprehensive failure recording adhering strictly to the 7-tier ISO 14224 reliability taxonomy. Finalization enforces a composite Hard Lock completion gate and preserves de-isolation safety boundaries prior to formal Operations Handover.

## 2. Preconditions
* The Maintenance Technician is authenticated on an authorized mobile terminal ([TR-006](../../../requirements/common/TR-006.md)).
* The target Work Order is in `IN_PROGRESS` status, formally assigned to the Technician, and linked to an active Work Permit in `APPROVED` status ([FR-182](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr)).
* The Actor enters the execution interface ([SCR-MTTO-002](../../../ui-ux/screens/mtto/SCR-MTTO-002.md)) from Zero Energy LOTO verification ([SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md)), Level 3 Equipment Task Faceplate ([SCR-VIS-033](../../../ui-ux/screens/vis/SCR-VIS-033.md)), or the Mobile Assigned Work Orders list.
* Isolation points (LOTO) associated with the target Equipment Unit are physically locked, tagged, and attested, ensuring field safety throughout the intervention.

## 3. Main Flow
1. The Technician accesses the Mobile Work Order execution interface.
2. The System displays the intervention tabs: Scope Checklist, Spares Consumption, Multimedia Evidence, and ISO 14224 Failure Coding.
3. The Technician physically executes planned tasks on the target Equipment Unit (e.g., Centrifugal Pump `P-0101A` at Functional Location `TFA-CSS-P-0101A`) and attests completion of mandatory scope checklist items.
4. The Technician records actual spare parts consumed against allocated reservations, or initiates a rotable equipment swap if replacing a serialized machine (branching to AF-004).
5. The Technician navigates to the ISO 14224 Failure Coding tab; the System presents categorized dropdowns constrained by the equipment class.
6. The Technician records the complete ISO 14224 Failure Taxonomy tiers ([FR-011](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr)):
   1. Maintainable Item (ISO 14224 Level 8, e.g., Mechanical Seal `SM-02`).
   2. Failure Mode (e.g., External Leakage - Utility `ELU`).
   3. Failure Mechanism (e.g., Mechanical Wear `WEA`).
   4. Failure Cause (e.g., Lubrication Deficiency `LUB`).
   5. Detection Method (e.g., Visual Inspection `VIO`).
   6. Operational Condition (e.g., Operating `OPE`).
   7. Operational Impact (e.g., Degraded Operation `DEG`).
   8. Quantitative Downtime Hours (e.g., `1.5` hrs) and Technical Observations.
7. The Technician navigates to the Multimedia Evidence tab and captures one or more field photographs ($1..N$ evidence array); the System generates client-side SHA-256 cryptographic hashes and responsive thumbnails ([TR-003](../../../requirements/common/TR-003.md)).
8. The Technician records actual Wrench Time (positive labor hours) and clicks "Finalize Work Order".
9. The System evaluates the composite Hard Lock Completion Invariant ([NFR-015](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr)):
   $$\text{CanFinalize} = \mathcal{T}_{\text{complete}} \land \mathcal{E}_{\text{valid}} \land \mathcal{W}_{\text{valid}}$$
   Verifying that all 7 failure tiers and downtime hours are complete, at least one valid photographic evidence with SHA-256 hash exists, actual labor hours are positive, and all mandatory scope checklist items are confirmed.
10. The System records the technical closure within a single atomic transactional boundary ([TR-001](../../../requirements/common/TR-001.md)):
    1. Transitions Work Order lifecycle status from `IN_PROGRESS` to `COMPLETE` (entering pre-closure state pending supervisor administrative review).
    2. Enforces the De-Isolation Safety Boundary Invariant: Physical LOTO padlocks remain attached and the machine remains de-energized; equipment operational status is NOT freed until formal Operations De-Isolation Handover.
    3. Persists failure classification, actual material consumption, labor hours, and multimedia attachments with cryptographic hashes.
    4. Records an append-only work order history log entry and an immutable audit trail record with chained SHA-256 hash.
11. The System displays a confirmation notice: *"Work Order successfully completed and pending supervisory review"*, and returns the Technician to the Work Orders Backlog ([SCR-MTTO-026](../../../ui-ux/screens/mtto/SCR-MTTO-026.md)).

## 4. Alternate Flows

### AF-001: Incomplete Closure Gate (Hard Lock Enforcement)
In step 9, if any mandatory taxonomic tier, Downtime Hours, positive labor hours, scope checklist item, or photographic evidence is missing or invalid:
1. The System interrupts the state transition, enforcing the Hard Lock gate.
2. The System highlights the missing or invalid fields using redundant Shape + Color indicators (amber contrast warning) per WCAG 2.1 AA and displays a specific validation error notice.
3. The flow returns to the corresponding tab for correction.

### AF-002: Field Network Partition & Deferred Synchronization (Offline-First)
In step 1, if operating in plant zones lacking wireless connectivity ([TR-007](../../../requirements/common/TR-007.md)):
1. The System displays the offline indicator ("OFFLINE · LOCALLY QUEUED").
2. The System applies Fail-Safe Zero-Energy Telemetry Masking, rendering neutral diagnostic status banners.
3. The Technician executes steps 1 through 8 normally; data, photos, and failure classifications are persisted in encrypted local storage ([TR-002](../../../requirements/common/TR-002.md)).
4. In step 10, the System marks the order as locally completed, queues the command payload using client-side UUIDv7 identifiers ([ADR-005](../../../architecture/adr/ADR-005.md)), and displays: *"Work locally completed. Synchronization pending."*
5. Upon network recovery, the background synchronization service dispatches the transaction queue to the central server using idempotency verification ([ADR-007](../../../architecture/adr/ADR-007.md)).

### AF-003: Corrupt Evidence File or Cryptographic Hash Mismatch
In step 7, if cryptographic integrity verification ([TR-003](../../../requirements/common/TR-003.md)) fails or detects an unreadable file:
1. The System rejects the file attachment and blocks form progression.
2. The System alerts: *"File integrity verification failed. Re-capture photographic evidence."*
3. The flow returns to step 7.

### AF-004: Rotable Equipment Replacement (Asset Swap Branching)
In step 4, if the Technician determines that a serialized rotable equipment unit must be physically replaced with a warehouse spare:
1. The Technician clicks "Rotate Dismounted Equipment" on the Spares tab.
2. The System deploys the contextual modal dialog for Asset Swap ([SCR-INV-025](../../../ui-ux/screens/inv/SCR-INV-025.md) / [UC-INV-025](../../../domain-models/use-cases/inv/UC-INV-025.md)).
3. The Technician executes the asset swap workflow: selects dismount destination, scans replacement unit, and confirms rotation.
4. Upon modal completion, control returns to the active Work Order execution view with the replacement serial number reflected in the active session.
5. The Technician resumes the main workflow at step 5.

### AF-005: Safety Interlock Breach / Active Hazardous Energy Detected
During active field execution, if plant telemetry or boundary sensors detect residual pressure, electrical voltage, or an unverified barrier breach:
1. The System immediately engages the safety interlock, sounding a critical warning.
2. The System automatically suspends execution, transitioning the Work Order status to `SUSPENDED`.
3. The System directs the technician to evacuate the immediate area and broadcasts high-priority alerts to the HSEQ Inspector and Maintenance Supervisor.

## 5. Postconditions
* The Work Order transitions to `COMPLETE`, becoming available for administrative review and closure by the Maintenance Supervisor.
* Complete 7-tier ISO 14224 failure classifications and downtime metrics are permanently linked to the equipment reliability history.
* The De-Isolation Safety Boundary Invariant is upheld: equipment remains physically locked and de-energized until formal Operations Handover.
* Multimedia evidence and immutable cryptographic audit records are permanently anchored in the central repository.

## 6. Associated Requirements
* **Functional Requirements:** [FR-010](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr), [FR-011](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr), [FR-012](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr), [FR-013](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr), [FR-014](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr)
* **Non-Functional Requirements:** [NFR-015](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr), [NFR-016](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr), [NFR-017](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr)
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-002](../../../requirements/common/TR-002.md), [TR-003](../../../requirements/common/TR-003.md), [TR-005](../../../requirements/common/TR-005.md), [TR-006](../../../requirements/common/TR-006.md), [TR-007](../../../requirements/common/TR-007.md), [TR-008](../../../requirements/common/TR-008.md), [TR-010](../../../requirements/common/TR-010.md), [TR-011](../../../requirements/common/TR-011.md)
* **Architectural Decisions:** [ADR-005](../../../architecture/adr/ADR-005.md), [ADR-006](../../../architecture/adr/ADR-006.md), [ADR-007](../../../architecture/adr/ADR-007.md)
