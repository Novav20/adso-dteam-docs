---
id: UC-MTTO-023
name: Schedule Condition-Based Predictive Maintenance (Telemetry)
module: mtto
user_story: MTTO-023
primary_actor: Reliability Engineer
secondary_actors:
  - SCADA/Historian Module (IoT ingestion
  - automated)
  - Task Planning Service.
---

# UC-MTTO-023: Schedule Condition-Based Predictive Maintenance (Telemetry)

## 1. Description
Allows defining preventive maintenance rules based on accumulated condition triggers (e.g. running hours, cycles, wear). These rules automatically instantiate predictive Work Orders without manual intervention when field instruments report that limits have been reached, ensuring strict adherence to condition-based reliability models (CBM).

## 2. Preconditions
* The Engineer is authenticated in the platform with the "Reliability Engineer" role [TR-006](../../../requirements/common/TR-006.md).
* The asset is registered and has telemetry signals configured and mapped to its digital twin in the master catalog.
* The structure of subunits and maintainable items is formally linked to the asset [TR-008](../../../requirements/common/TR-008.md).

## 3. Main Flow
1. The Engineer accesses the Maintenance Planning menu and selects "Create Predictive Plan (Condition)".
2. The System displays the creation form with mandatory fields:
   - Target Asset (Level 6).
   - Linked Subunit (Level 7) and Maintainable Item (Level 8).
   - Type of physical measurement (Running Hours, Kilometers, Production Cycles, Starts, Wear in mm).
   - Specific triggering interval (e.g., Every 1000 hours).
   - Resource estimation (Wrench Time) and required specialty.
   - Initial threshold definition from current historical accumulation.
3. The Engineer selects the asset "Compressor C-201", links the "Bearing" item, selects "Running Hours" as the condition unit, and sets the recurring interval to "1000 hours".
4. The System evaluates the asset's current historical accumulated value (e.g. 4500 hours) and calculates the initial target limit mathematically: `Target Limit = 4500 + 1000 = 5500 hours`.
5. The Engineer adds the technical description of the task and confirms the creation of the plan.
6. The System evaluates the configured asset criticality and assigns the Work Class "Predictive Maintenance" (Weight 7).
7. The System persists the predictive plan definition in the operational database, leaving it in active "LISTENING" status waiting for data streams.
8. The System displays a confirmation in the interface indicating successful creation and the required target limit for the first trigger.

## 4. Alternate Flows
### AF-001: Automatic Work Order Trigger by Telemetry
This flow executes asynchronously and automatically every time the system ingests field data:
1. The local SCADA control station [TR-010](../../../requirements/common/TR-010.md) publishes an asset telemetry reading that equals or exceeds the target limit established in the plan (e.g., the sensor reports 5502 running hours).
2. The System processes the frame and validates that the reading is consistent with the historical accumulation.
3. The System automatically generates the Work Order in "PLANNING" status, inheriting tasks, labor estimation, LOTO parameters and calculating the dynamic RIME Score (Asset Criticality × Work Class).
4. The System calculates the next trigger limit by adding the configured interval strictly to the previous limit to avoid time drifts (Drift): `New Limit = 5500 + 1000 = 6500 hours`.
5. The System persists the generated Work Order and the updated plan target limit atomically in the operational database.

### AF-002: Reading Inconsistency (Counter Decrement)
In step 1 of AF-001, if the SCADA reports a counter value lower than the recorded historical accumulation (e.g., the sensor reports 4300 hours when the last valid record was 4500):
1. The System applies the fail-safe principle, preventively blocks the reading processing and keeps the counter at its last valid value.
2. The System generates a data inconsistency visual alarm and dispatches an alert to the Reliability Engineer to audit the field instrument.
3. The flow is interrupted and the anomalous counter reset attempt is recorded in the operational diagnostics log for engineering inspection.

### AF-003: Contingency Manual Reading Record
If the connection with the SCADA presents prolonged failures and the planner needs to force synchronization:
1. The Planner accesses the asset's data sheet in the system and manually records the reading obtained from the physical hour meter in the field.
2. The System validates that the reading is higher than the recorded historical accumulation and proceeds to step 5 of the main flow or executes the trigger in step 3 of AF-001 as appropriate.

## 5. Postconditions
* The telemetry-based predictive plan is registered and active in the system.
* The triggering of preventive work orders executes asynchronously and automatically, generating WOs with objective priority (RIME) and estimated resources (Wrench Time).
* Automated Work Order instantiations and sensor tracking are durably persisted in the operational maintenance repository.

## 6. Associated Requirements
* **Functional Requirements:** FR-583, FR-585, FR-586, FR-587
* **Non-Functional Requirements:** NFR-584, NFR-588, NFR-589, NFR-590
* **Transversal Requirements:** [TR-008](../../../requirements/common/TR-008.md), [TR-010](../../../requirements/common/TR-010.md)
