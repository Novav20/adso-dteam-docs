---
id: UC-VIS-011
name: Verify Zero Energy Condition (LOTO-TryOut)
module: vis
user_story: VIS-011
primary_actor: Maintenance Technician
secondary_actors:
  - Maintenance Supervisor
  - HSEQ Inspector
  - Plant Operations Manager
---

# UC-VIS-011: Verify Zero Energy Condition (LOTO-TryOut)

## 1. Description
Governs the life-critical safety verification workflow required before physical maintenance intervention on plant Equipment Units. It validates Lockout/Tagout (LOTO) isolation by synthesizing physical padlocks and tags, formal Try-Out attestations, and real-time telemetry sensing into an infallible Negative Interlock. This guarantees a confirmed Zero Energy state, guards against unapproved permits or residual hazardous energy, and provides automated full-screen emergency evacuation alerts in the event of unscheduled line re-energization.

## 2. Preconditions
* The Maintenance Technician is authenticated on an authorized mobile device ([TR-006](../../../requirements/common/TR-006.md)).
* The target Work Order is in `SCHEDULED` status ([FR-225](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr)).
* The target Work Order is linked to an active Work Permit in `APPROVED` status ([FR-182](../../../requirements/user-stories/vis/VIS-008.md#functional-requirements-fr)).
* The Actor invokes the LOTO verification interface ([SCR-VIS-011](../../../ui-ux/screens/vis/SCR-VIS-011.md)) from the Level 3 Equipment Task Faceplate ([SCR-VIS-033](../../../ui-ux/screens/vis/SCR-VIS-033.md)) via "Verify LOTO Isolation" or from the Level 1 Plant Overview ([SCR-VIS-008](../../../ui-ux/screens/vis/SCR-VIS-008.md)) via LOTO layer selection.
* Physical cutoff points and active telemetry sensors are mapped in the 2D plot plan vector overlay.

## 3. Main Flow
1. The Technician opens the LOTO verification interface for the scheduled Work Order.
2. The System renders the 2D plot plan vector overlay with focal island de-emphasis, attenuating non-relevant plant areas while visually tracing the electrical/piping feeder lines and highlighting all sequential isolation cutoff points.
3. The System displays the safety header detailing mandatory Personal Protective Equipment (PPE), the applicable Standard Operating Procedure (SOP), active SIMOPS awareness notices, and the sequential isolation checklist.
4. The Technician inspects each cutoff point in the field, attaches physical padlocks and safety tags, and inputs or scans each Padlock Tag ID; the System validates and confirms each cutoff point sequentially.
5. The Technician executes the formal Try-Out Attestation:
   1. Selects the physical verification method (`MULTIMETER_PROBE`, `ATMOSPHERIC_VENT_BLEED`, or `LOCAL_PUSHBUTTON_ATTEMPT`).
   2. Records the observed residual energy readings ($0.00\text{ V}$, $0.0\text{ psig}$).
   3. Submits their digital signature hash confirming physical absence of tension or pressure.
6. The System requests a telemetry verification snapshot across boundary sensors at all isolation cutoff points.
7. The System evaluates the Negative Interlock Principle ([TR-011](../../../requirements/common/TR-011.md)):
   1. Telemetry acts strictly as a negative interlock (veto mechanism). If sensors detect zero residual energy ($V < 1.0\text{ V}$, $P < 0.1\text{ psig}$), the veto is lifted.
   2. The System unlocks the asymmetric "Start Work" control only when all preconditions are conjunctively satisfied: all physical padlocks verified, Try-Out attestation digitally signed, telemetry veto lifted, and associated Work Permit confirmed in `APPROVED` status.
8. The Technician engages the asymmetric slider control to confirm work commencement.
9. The System executes the execution transition within a single atomic transactional boundary ([TR-001](../../../requirements/common/TR-001.md)):
   1. Transitions Work Order lifecycle status to `IN_PROGRESS`.
   2. Persists the isolation attestation records (padlock IDs, Try-Out method, observed readings, digital signature hash, and telemetry snapshot).
   3. Records an immutable append-only audit trail entry with chained SHA-256 cryptographic hash.
   4. Routes the technician's mobile interface to Mobile Work Order Execution ([SCR-MTTO-002](../../../ui-ux/screens/mtto/SCR-MTTO-002.md)).

## 4. Alternate Flows

### AF-001: Active Residual Energy Detected / Sensor Health Fault (Fail-Safe Invariant)
In step 6, if telemetry sensors report residual energy above safety thresholds, or if sensor telemetry encounters communication timeout or health fault:
1. The System activates the negative interlock, hard-disabling the work start action. Under the Fail-Safe Invariant (Safety over Availability), telemetry uncertainty is treated as active hazardous energy.
2. The System issues a critical safety alert visualizing the anomalous reading: *"Safety Interlock Engaged: Active residual energy detected or telemetry unverified. Work start prohibited."*
3. The flow returns to step 4, awaiting physical energy dissipation, bleed-off, or instrument inspection.

### AF-002: Field Network Partition & Cryptographic Offline Lease Fallback
Prior to step 8, if wireless connectivity drops in shielded or remote plant zones ([TR-007](../../../requirements/common/TR-007.md)):
1. The mobile client detects network disconnection and verifies the presence of an active Cryptographic Offline Lease ([ADR-006](../../../architecture/adr/ADR-006.md)).
2. If the lease is active and unexpired:
   1. The System applies Fail-Safe Zero-Energy Telemetry Masking, rendering a neutral diagnostic stale notice (`wifi-off`) per ISA-101.
   2. The System prompts for mandatory manual attestation: the Technician re-confirms physical lock placement and signs the physical Try-Out attestation locally.
   3. The System unlocks the asymmetric slider under "Offline Verified Safety Mode".
   4. In step 9, the System persists the transaction in local encrypted storage ([TR-002](../../../requirements/common/TR-002.md)) and queues the command payload into the local offline synchronization queue ([ADR-006](../../../architecture/adr/ADR-006.md)) using client-side UUIDv7 identifiers ([ADR-005](../../../architecture/adr/ADR-005.md)).
   5. Upon network recovery, the background synchronization service dispatches the transaction to the central server using idempotency keys.
3. If the lease is expired or absent:
   1. The System enforces the fail-safe lockout, disabling the work start interface.
   2. The System displays: *"Offline Safety Lease Expired. Re-establish network connectivity or provide Supervisor Cryptographic Override to proceed."*
   3. The operation remains locked until reconnection renews the lease or an authorized supervisor override is entered.

### AF-003: Unscheduled Re-Energization During Work Execution (Emergency Evacuation Beacon)
After step 9, while the Work Order is `IN_PROGRESS`, if continuous telemetry monitoring detects unexpected voltage, current, or fluid pressure:
1. The System immediately deploys the full-screen passive emergency evacuation overlay.
2. The System enforces complete touchscreen input lockout (strictly zero dismiss or cancel buttons per ISO 11064-5, preventing cognitive hesitation during acute life-safety emergencies).
3. The System initiates a high-visibility diagonal hazard strobe ($2\text{Hz}$) and triggers an acoustic alarm sweep ($800\text{Hz} - 1200\text{Hz}$ via Web Audio API).
4. The System automatically transitions the Work Order status to `SUSPENDED` and broadcasts emergency evacuation alerts to central HSEQ and Operations consoles.

### AF-004: Unapproved or Expired Work Permit (Regulatory Safety Guard)
In step 1 or step 7, if the associated Work Permit is expired, revoked, or not in `APPROVED` status:
1. The System engages the regulatory safety interlock, preventing LOTO execution.
2. The System displays a regulatory error banner: *"Permit Safety Guard: Field work cannot proceed without an active, approved Work Permit. Contact HSEQ Inspector."*
3. The workflow is aborted.

## 5. Postconditions
* The Work Order transitions to `IN_PROGRESS` strictly under proven Zero Energy conditions, physical padlock placement, and signed Try-Out attestation.
* Isolation records, measured parameters, and cryptographic digital signatures are durably persisted in the audit trail.
* Control smoothly routes to Mobile Work Order Execution ([SCR-MTTO-002](../../../ui-ux/screens/mtto/SCR-MTTO-002.md)) with isolation status preserved.
* Continuous background telemetry monitoring remains active, ready to trigger emergency evacuation beacons if unexpected re-energization occurs.

## 6. Associated Requirements
* **Functional Requirements:** [FR-225](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr), [FR-226](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr), [FR-227](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr), [FR-228](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr), [FR-230](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr), [FR-231](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr), [FR-232](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr)
* **Non-Functional Requirements:** [NFR-229](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr), [NFR-233](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr), [NFR-234](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr), [NFR-235](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr), [NFR-236](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr), [NFR-237](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr), [NFR-238](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr)
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-002](../../../requirements/common/TR-002.md), [TR-005](../../../requirements/common/TR-005.md), [TR-006](../../../requirements/common/TR-006.md), [TR-007](../../../requirements/common/TR-007.md), [TR-010](../../../requirements/common/TR-010.md), [TR-011](../../../requirements/common/TR-011.md)
* **Architectural Decisions:** [ADR-005](../../../architecture/adr/ADR-005.md), [ADR-006](../../../architecture/adr/ADR-006.md)
