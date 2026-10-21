---
id: UC-MTTO-026
name: Calculate RIME Priority of Work Requests (Backlog)
module: mtto
user_story: MTTO-026
primary_actor: Maintenance Planner
secondary_actors:
  - Reliability Engineer (notified)
---

# UC-MTTO-026: Calculate RIME Priority of Work Requests (Backlog)

## 1. Description
Automatically calculates and assigns an objective priority score to each work request in the backlog, delegating the calculation to the RIME (Ranking Index for Maintenance Expenditure) prioritization engine implemented under the *Strategy* pattern (`IRimeCalculator`, [ADR-002](../../../architecture/adr/ADR-002.md)). In the MVP strategy, the score is calculated deterministically from Asset Criticality (1-10) and Work Class weight (1-10). The system consolidates resource availability (materials and time) to facilitate decision-making.

## 2. Preconditions
* The Planner is authenticated in the web system with the "Maintenance Planner" role [TR-006](../../../requirements/common/TR-006.md).
* There are pending work requests in `NEW` status to be planned.
* The affected assets have a numerical Criticality value (1 to 10) configured in their technical data sheets.

## 3. Main Flow
1. The Planner accesses the "Backlog Management" module in the web portal and selects "View Pending Requests".
2. The System retrieves all pending work requests.
3. The System automatically calculates the priority index for each request by invoking the active strategy of the `IRimeCalculator` service ([ADR-002](../../../architecture/adr/ADR-002.md)):
   - In the standard MVP strategy, it obtains the asset criticality from the master catalog and the weight of the selected Work Class, multiplying both factors to generate the resulting score (Range: 1 to 100).
4. The System classifies and groups the request into a high-contrast visual category based on the obtained score:
   - **Do First** (80-100): Emergency Category.
   - **Schedule** (50-79): High Category.
   - **Plan** (20-49): Normal Category.
   - **Wish** (1-19): Low Category.
5. The System sorts the backlog descendingly by RIME score, enriching each row with key operational metadata: Equipment Serial Number, Maintainable Item (Level 8), Estimated Man-Hours (Wrench Time) and Material Availability Status.
6. The Planner visualizes the prioritized list and confirms the distribution of the weekly workload.

## 4. Alternate Flows
### AF-001: Work Class Modification (Priority Adjustment)
If the Planner detects that a request requires greater or lesser urgency due to operational conditions:
1. The Planner edits the "Work Class" field, changing (for example) from "Preventive Maintenance" to "High Process Priority".
2. The System immediately recalculates the RIME score and automatically reorders the backlog list.
3. The System records the transaction in the immutable audit trail [TR-001](../../../requirements/common/TR-001.md) generating an append-only record with its corresponding chained cryptographic integrity hash, capturing: user, request identifier, old value, new value, new calculated score and technical justification.

### AF-002: Asset without Defined Criticality (Fail-Safe)
If the work request is associated with an asset that lacks criticality classification in its technical data sheet:
1. The System applies the fail-safe principle. To prevent the purely multiplicative calculation from burying the request, the final RIME score is forced to a minimum floor of 75 (High Category), regardless of a low Work Class weight.
2. The System highlights the request with a prominent visual warning: "Criticality not configured on the asset. Maximum temporary priority assigned preventively."
3. The flow continues to step 4, sending a notification to the Reliability Engineer to configure the actual criticality in the catalog.

## 5. Postconditions
* All pending work requests have a RIME score calculated and audited at runtime.
* The backlog is objectively sorted with estimated resources (labor and materials) visible for scheduling.
* Any alteration of priority parameters is cryptographically recorded.

## 6. Associated Requirements
* **Functional Requirements:** FR-058, FR-059, FR-060, FR-061, FR-062, FR-065, FR-066, FR-067, FR-068, FR-069
* **Non-Functional Requirements:** NFR-070, NFR-071, NFR-072, NFR-073, NFR-074, NFR-075, NFR-076
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-006](../../../requirements/common/TR-006.md)
