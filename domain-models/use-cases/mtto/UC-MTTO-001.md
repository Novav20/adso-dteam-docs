---
id: UC-MTTO-001
name: Schedule Preventive Maintenance
module: mtto
user_story: MTTO-001
primary_actor: Maintenance Planner
secondary_actors:
  - Task Planning Service
  - Reliability Engineer (notified)
---

# UC-MTTO-001: Schedule Preventive Maintenance

## 1. Description
Allows creating and scheduling recurrent preventive maintenance plans based exclusively on calendar time intervals, linked to equipment units (ISO 14224 Level 6), subunits (Level 7) and maintainable items (Level 8), capturing resource estimation (Wrench Time) and criticality for Work Order generation.

## 2. Preconditions
* The Planner is authenticated in the platform with the "Maintenance Planner" role [TR-006](../../../requirements/common/TR-006.md).
* The asset is registered in the master catalog with its complete identification Tag (Level 6) and its assigned criticality.
* The structure of subunits (Level 7) and maintainable items (Level 8) is defined and linked to the asset [TR-008](../../../requirements/common/TR-008.md).
* The physical limits of the asset (boundaries) are defined in the technical data sheet [MTTO-029](../../../requirements/user-stories/mtto/MTTO-029.md).

## 3. Main Flow
1. The Planner accesses the Maintenance Planning menu and selects "Create Preventive Plan".
2. The System displays the creation form requiring the following mandatory fields:
   - Asset selection (Level 6) through Tag search.
   - Selection of associated Subunit (Level 7) and Maintainable Item (Level 8).
   - Time frequency in weeks or months (Calendar frequency).
   - Estimated Man-Hours (Wrench Time) and Required Specialty (Mechanical, Electrical, Instrumentation).
   - Technical description of task scope.
3. The Planner selects the asset "Pump P-101", links the subunit "Sealing System" and the item "Mechanical Seal", defines a frequency of "12 weeks", estimates "4.0 Man-Hours" of mechanical specialty and enters the technical description.
4. The System evaluates the configured asset criticality and assigns the Work Class "Preventive Maintenance" (Weight 6) to calculate the initial RIME prioritization score ($Score = \text{Criticality} \times 6$).
   - If the criticality is high (greater than 8) and the entered time interval is greater than 8 weeks:
   - The System displays an optimization warning: "For high criticality assets, it is recommended to schedule preventive plans with intervals less than or equal to 8 weeks. Do you want to proceed with the current frequency?"
   - The Planner confirms the 12-week frequency by entering a technical justification or adjusts it to 8 weeks.
5. The Planner confirms the creation of the preventive plan.
6. The System:
   - Invokes the domain method to calculate the date of the first calendar Work Order based on the parameterized frequency.
   - Automatically generates the first preventive Work Order in "PLANNING" status, inheriting plan data, estimated Man-Hours, associated LOTO points and the calculated RIME Score.
   - Persists the preventive plan and the generated Work Order atomically in the database.
7. The System displays a confirmation in the interface indicating successful creation and the estimated date of the next execution.

## 4. Alternate Flows
### AF-001: Empty Mandatory Fields (Redundant Coding)
In step 3, if the Planner attempts to confirm the plan by omitting mandatory fields (e.g. Estimated Man-Hours or Asset):
1. The System interrupts the process.
2. The System highlights the missing fields applying redundant Shape + Color coding (warning symbol and contrast indicator) according to WCAG 2.1 AA and displays a message: "Mandatory fields required: Asset, Time Frequency, Estimated Man-Hours and Description."
3. The flow returns to step 3.

### AF-002: Asset without Defined Physical Boundaries
In step 3, if the selected asset lacks physical boundaries in its technical data sheet [MTTO-029](../../../requirements/user-stories/mtto/MTTO-029.md):
1. The System blocks plan creation and displays an error warning: "It is not possible to schedule preventive maintenance on an asset without defined physical boundaries (ISO 14224). Request boundary configuration from the Reliability Engineer."
2. The flow is canceled and returns to the module's home screen.

### AF-003: Frequency Adjustment after Warning
In step 4, if the Planner decides to adjust the interval to a recommended range (≤ 8 weeks):
1. The Planner changes the frequency to "8 weeks" in the form.
2. The System validates the new frequency and continues to step 5.

## 5. Postconditions
* The preventive maintenance plan is registered and active in the system with its labor estimates (Wrench Time).
* The first Work Order is instantiated in planning status with its inherited RIME Score.

## 6. Associated Requirements
* **Functional Requirements:** FR-001, FR-002, FR-003, FR-004, FR-005, FR-006
* **Non-Functional Requirements:** NFR-007, NFR-008, NFR-009
* **Transversal Requirements:** [TR-008](../../../requirements/common/TR-008.md)
