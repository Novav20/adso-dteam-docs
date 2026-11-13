---
id: UC-MTTO-023
name: Schedule Condition-Based Predictive Maintenance (Telemetry)
module: mtto
user_story: MTTO-023
primary_actor: Reliability Engineer
secondary_actors:
  - Maintenance Planner
  - SCADA / Historian Module (Automated IoT Ingestion)
---

# UC-MTTO-023: Schedule Condition-Based Predictive Maintenance (Telemetry)

## 1. Description
Allows defining preventive and condition-based maintenance (CBM) rules governed by accumulated usage or telemetry counters (operating hours, cycles, distance, or wear depth). These rules automatically instantiate Work Orders in `PLANNING` status without manual intervention when field instruments report that accumulated usage has reached or exceeded the configured target threshold, eliminating schedule drift while preserving strict counter monotonicity.

## 2. Preconditions
* The actor is authenticated in the platform with the `Reliability Engineer` or `Maintenance Planner` role ([TR-006](../../../requirements/common/TR-006.md)).
* The target Level 6 Equipment Unit is registered in the master catalog with formalized physical battery limits (upstream and downstream physical battery limits per [MTTO-029](../../../requirements/user-stories/mtto/MTTO-029.md)).
* The Equipment Unit's Level 7 Subunits and Level 8 Maintainable Items are formally linked in the ISO 14224 hierarchy ([TR-008](../../../requirements/common/TR-008.md)).
* At least one cumulative telemetry signal is mapped to the Equipment Unit's digital twin and active in the SCADA/Historian stream ([TR-010](../../../requirements/common/TR-010.md)).

## 3. Main Flow
1. The Reliability Engineer accesses the Maintenance Planning workspace from the RIME Backlog Dashboard or navigation menu and selects "Create Condition-Based Plan (Telemetry)".
2. The System displays the condition-based scheduling form with the mandatory configuration fields:
   - Target Equipment Unit (ISO 14224 Level 6), whose physical battery limits are automatically verified.
   - Linked Subunit (Level 7) and Maintainable Item (Level 8).
   - Mapped cumulative telemetry signal (`OPERATING_HOURS`, `CYCLES`, or equivalent physical usage stream).
   - Physical measurement unit (`OPERATING_HOURS`, `CYCLES`, `KILOMETERS`, `WEAR_DEPTH_MM`).
   - Triggering recurrence interval delta ($\Delta$) with high-precision decimal retention.
   - Estimated active wrench time (Man-Hours) and required maintenance craft specialties.
   - Technical task scope, diagnostic procedure, and isolation guidance.
3. The Reliability Engineer selects Equipment Unit `"Compressor C-201"`, links `"Bearing Assembly"` and `"Drive-End Journal Bearing"`, selects mapped signal `C201_RUN_HOURS` with measurement unit `OPERATING_HOURS`, and sets the triggering interval delta to `1,000.00` operating hours alongside `6.0` Man-Hours and required crafts.
4. The System retrieves the signal's current historical accumulated reading (e.g., `4,500.00` operating hours) and mathematically computes the initial activation threshold: `Target Limit = 4,500.00 + 1,000.00 = 5,500.00 operating hours`.
5. The Reliability Engineer enters the technical task scope and confirms plan activation.
6. The System evaluates the Equipment Unit's criticality (`8`) and assigns the Predictive Maintenance Work Class (`Weight 5` per `DT-DM-DOC-001 §4.24` and [ADR-002](../../../architecture/adr/ADR-002.md)), calculating `RIME Score = 8 × 5 = 40`.
7. The System atomically persists the predictive Maintenance Plan in **`ACTIVE`** lifecycle status with `CONDITION_BASED` method, initial activation threshold (`5,500.00`), and immutable audit record ([TR-001](../../../requirements/common/TR-001.md)).
8. The System displays documentary confirmation showing the created plan identifier, `ACTIVE` monitoring state, and target threshold for the first automated trigger.

## 4. Alternate Flows
### AF-001: Automatic Work Order Trigger by Telemetry
This flow executes asynchronously whenever the telemetry ingestion channel receives an authorized, TLS 1.3-encrypted counter update:
1. The plant SCADA/Historian publishes a monotonic reading for the monitored signal that meets or exceeds the active plan's target limit (e.g., `5,502.50` operating hours) and the System evaluates the trigger rule within `< 3 seconds`.
2. The System validates that the incoming reading is monotonically non-decreasing (`Received Reading >= Historical Accumulation`).
3. The System atomically instantiates a new `WorkOrder` in `PLANNING` status inheriting task scope, wrench time, required craft specialties, LOTO requirements, and dynamic RIME priority score (`Asset Criticality × 5`).
4. To prevent positive schedule drift across delayed SCADA arrivals, the System advances the next target limit strictly from the previous target limit rather than the received reading: `New Limit = 5,500.00 + 1,000.00 = 6,500.00 operating hours`.
5. The System atomically persists the generated Work Order, backlog prioritization entry, and updated Maintenance Plan target limit, broadcasting the event over real-time transport ([TR-010](../../../requirements/common/TR-010.md)).

### AF-002: Reading Inconsistency (Counter Decrement)
In step 2 of `AF-001` (or during manual contingency submission in `AF-003`), if a received reading is strictly lower than the recorded historical accumulation (e.g., `4,300.00 < 4,500.00`):
1. The System applies the fail-safe monotonicity guard, rejects the decremented reading, and preserves the cumulative counter at its last valid historical value (`4,500.00`).
2. The System deploys a critical inconsistency alert on the SCADA status panel and dispatches a diagnostic notification to the Reliability Engineer for field sensor calibration or rollover audit.
3. Automated Work Order instantiation for that signal is suspended until the anomaly is inspected and resolved, and the rejected attempt is appended to the immutable operational audit log ([TR-001](../../../requirements/common/TR-001.md)).

### AF-003: Contingency Manual Reading Record
If the SCADA/IoT link experiences prolonged communication loss and the Maintenance Planner or Reliability Engineer must synchronize field usage manually:
1. The Maintenance Planner opens the Contingency Manual Reading dialog from the telemetry status panel.
2. The Planner enters the physical field counter value (must satisfy monotonic non-decreasing validation `>= 4,500.00`), reading timestamp (UTC/local not in the future), authenticated inspector identifier, and optional gauge photograph evidence URL.
3. The System validates monotonicity, updates the historical baseline accumulation, marks the link state as manual contingency active, and automatically executes `AF-001` Work Order instantiation if the entered value meets or exceeds the target limit.

### AF-004: Missing Physical Battery Limits or Mandatory Configuration Data
If the selected Level 6 Equipment Unit lacks formalized physical battery limits ([MTTO-029](../../../requirements/user-stories/mtto/MTTO-029.md)) or mandatory parameters (Maintainable Item, mapped signal, positive interval delta, positive wrench time, at least one craft specialty, or technical scope) are omitted:
1. The System hard-blocks plan confirmation and renders contextual feedback indicating the missing prerequisite or offering navigation to boundary configuration.
2. No Maintenance Plan or Work Order is persisted until all mandatory invariants are satisfied.

## 5. Postconditions
* The telemetry-governed Maintenance Plan is durably persisted in `ACTIVE` status with a high-precision initial target limit.
* Automated non-drifting Work Order instantiation and fail-safe monotonicity protection are armed against incoming SCADA/IoT telemetry frames.
* Any generated Work Orders enter the RIME Backlog in `PLANNING` status with objective RIME scoring (`Criticality × 5`) and wrench time allocations, backed by an immutable audit trail.

## 6. Associated Requirements
* **Functional Requirements:** [FR-583](../../../requirements/user-stories/mtto/MTTO-023.md#functional-requirements-fr), [FR-584](../../../requirements/user-stories/mtto/MTTO-023.md#functional-requirements-fr), [FR-585](../../../requirements/user-stories/mtto/MTTO-023.md#functional-requirements-fr), [FR-586](../../../requirements/user-stories/mtto/MTTO-023.md#functional-requirements-fr), [FR-587](../../../requirements/user-stories/mtto/MTTO-023.md#functional-requirements-fr), [FR-590](../../../requirements/user-stories/mtto/MTTO-023.md#functional-requirements-fr), [FR-096](../../../requirements/user-stories/mtto/MTTO-029.md#functional-requirements-fr)
* **Non-Functional Requirements:** [NFR-588](../../../requirements/user-stories/mtto/MTTO-023.md#non-functional-requirements-nfr), [NFR-589](../../../requirements/user-stories/mtto/MTTO-023.md#non-functional-requirements-nfr)
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-005](../../../requirements/common/TR-005.md), [TR-006](../../../requirements/common/TR-006.md), [TR-008](../../../requirements/common/TR-008.md), [TR-010](../../../requirements/common/TR-010.md), [TR-011](../../../requirements/common/TR-011.md)
* **Architectural Decisions:** [ADR-002](../../../architecture/adr/ADR-002.md), [ADR-005](../../../architecture/adr/ADR-005.md)
