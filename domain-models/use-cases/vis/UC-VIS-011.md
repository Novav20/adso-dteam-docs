---
id: UC-VIS-011
name: Verify Zero Energy Condition (LOTO-TryOut)
module: vis
user_story: VIS-011
primary_actor: Maintenance Technician
secondary_actors:
  - Telemetry Service (IoT)
  - HSEQ Inspector (notified on breach)
---

# UC-VIS-011: Verify Zero Energy Condition (LOTO-TryOut)

## 1. Description
Critical security workflow that dictates the final verification step before initiating a physical intervention on an asset. The system validates Lockout/Tagout (LOTO) isolation by crossing manual checks (checklists, physical padlock IDs, Try-Out) with telemetry sensor data in real-time, ensuring a strict "Zero Energy" state to prevent severe accidents.

## 2. Preconditions
* The Maintenance Technician is authenticated in the system on an authorized mobile device [TR-006](../../../requirements/common/TR-006.md).
* The target Work Order is in `PLANNING` or `SCHEDULED` status.
* The asset's isolation points (LOTO) and active telemetry sensors are properly mapped in the digital twin.

## 3. Main Flow
1. The Technician accesses the Work Order on their mobile terminal and requests to visualize the LOTO route.
2. The System renders the asset schematic, highlights the energy flow and identifies the physical cutoff points.
3. The System displays the safety header indicating the applicable standard operating procedure (SOP), mandatory personal protective equipment (PPE), an informative notice about other active permits on the asset (SIMOPS awareness) and the sequential isolation checklist.
4. The Technician moves to the field, places the physical padlocks/tags on each cutoff point and enters or verifies the applied Padlock Tag IDs in the list.
5. The Technician executes the physical absence of tension test (Try-Out test) on the asset and marks the confirmation of the test on the checklist.
6. The System requests a synchronous verification from the Telemetry Service to validate the sensor readings at the cutoff points.
7. The Telemetry Service confirms the Zero Energy condition. The System enables the control to start the work.
8. The Technician confirms the start of the intervention.
9. The System:
   - Updates the Work Order status to execution (`IN_PROGRESS`).
   - Records the physical padlock identifiers, Zero Energy telemetry readings, and isolation signatures directly in the dedicated Work Order Isolation registry to support fast safety compliance querying.
   - Records the execution state transition in the immutable audit trail [TR-001](../../../requirements/common/TR-001.md) via an append-only log, capturing the user, timestamp, and action hash.
   - Enables the order execution interface for the technician in the field.

## 4. Alternate Flows
### AF-001: Active Energy Detected
In step 6 (or through continuous monitoring prior to start), if telemetry reports energy levels above the safety threshold:
1. The System interrupts the status transition and blocks work enablement.
2. The System issues a critical alert visualizing the anomalous reading: "DANGER: Active energy detected. Intervention blocked."
3. The flow returns to step 4, waiting for the residual energy to dissipate or the physical isolation to be corrected.

### AF-002: Field Connection Loss (Offline Lease Safety Fallback)
At any time before step 8, if the mobile terminal loses communication with the central server (e.g. in shielded environments or confined spaces):
1. The mobile terminal detects network partition and verifies the presence of an active Cryptographic Offline Lease [ADR-006](../../../architecture/adr/ADR-006.md).
2. If the Offline Lease is active and unexpired:
a. The System prompts for mandatory local confirmation of physical isolation: the Technician must manually re-verify and confirm the physical Try-Out test (absence of energy) and lock placement.
b. The System unlocks the work start control under "Offline Verified Safety Mode" and queues the execution start command in the local offline outbox [TR-007](../../../requirements/common/TR-007.md).
c. Upon reconnecting, the sync worker reconciles the offline safety execution with the central system.
3. If the Offline Lease is expired or absent:
a. The System enforces the fail-safe lock, disabling the work start interface.
b. The System notifies: "Connection Lost and Offline Safety Lease expired. Re-establish connection or provide authorized Supervisor Cryptographic Override to proceed."
4. The operation remains locked until reconnection renews the lease or the override is validated.

### AF-003: Re-energization During Execution
After step 9, while the order is in progress:
1. Continuous background monitoring detects an accidental energy flow in the isolated line.
2. The System automatically and immediately forces the suspension of the Work Order.
3. The System issues maximum evacuation alerts on the Technician's terminal and dispatches emergency notifications to the HSEQ supervision consoles.

## 5. Postconditions
* The Work Order transitions to execution only under proven guarantee of Zero Energy and physical Try-Out verification.
* Operational safety conditions (sensor readings and padlock identifiers) are durably preserved in the transactional Work Order Isolation registry for immediate OSHA compliance reporting, while the state transitions remain cryptographically audited.
* The system remains in a continuous monitoring state to react to energy contingencies.

## 6. Associated Requirements
* **Functional Requirements:** FR-225, FR-226, FR-227, FR-228, FR-230, FR-231, FR-232
* **Non-Functional Requirements:** NFR-229, NFR-233, NFR-234, NFR-235, NFR-236, NFR-237, NFR-238
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-007](../../../requirements/common/TR-007.md), [TR-010](../../../requirements/common/TR-010.md), [TR-011](../../../requirements/common/TR-011.md)
* **Architectural Decisions:** [ADR-006](../../../architecture/adr/ADR-006.md)
