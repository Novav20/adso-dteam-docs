---
id: UC-MTTO-026
name: Calculate RIME Priority of Work Requests (Backlog)
module: mtto
user_story: MTTO-026
primary_actor: Maintenance Planner
secondary_actors:
  - Reliability Engineer
  - Maintenance Supervisor
---

# UC-MTTO-026: Calculate RIME Priority of Work Requests (Backlog)

## 1. Description
Automatically calculates and assigns an objective, quantitative priority score to each work request in the maintenance backlog. The system delegates priority evaluation to the industrial RIME (Ranking Index for Maintenance Expenditure) strategy engine ([ADR-002](../../../architecture/adr/ADR-002.md)), combining static asset criticality ($1..10$) with the operational weight of the selected work class ($1..10$) into a normalized score ($1..100$). The system consolidates resource availability (material inventory reservations and wrench hours), supports algorithmic work-order clustering on identical equipment units, and enforces tamper-evident cryptographic audit trails for all manual work-class adjustments.

## 2. Preconditions
* The Maintenance Planner is authenticated in the web portal with the authorized "Maintenance Planner" role ([TR-006](../../../requirements/common/TR-006.md)).
* One or more work requests exist in intake `NEW` status awaiting supervisory planning and scheduling.
* Target assets associated with pending work requests possess a configured numerical criticality index ($1..10$) defined in their ISO 14224 Functional Location and Equipment Unit master records ([FR-058](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)).
* The Actor enters the supervisory interface ([SCR-MTTO-026](../../../ui-ux/screens/mtto/SCR-MTTO-026.md)) via the Web Portal navigation tree under Level 2 Process Supervision and Planning ([DT-UI-NAV-DOC-001 §3.2](../../../ui-ux/DT-UI-NAV-DOC-001.md#32-level-2-process-supervision-and-planning-l2---unit-process)).

## 3. Main Flow
1. The Planner accesses the Backlog Prioritization module in the web portal shell ([SCR-MTTO-026](../../../ui-ux/screens/mtto/SCR-MTTO-026.md)).
2. The System queries all active work requests in `NEW` status and constructs or updates the corresponding backlog prioritization item projections.
3. The System automatically evaluates the priority score for each backlog item by delegating calculation to the industrial RIME prioritization engine ([FR-060](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr), [ADR-002](../../../architecture/adr/ADR-002.md)):
   1. Retrieves the static asset criticality index ($C \in [1, 10]$) from the master record of the associated ISO 14224 Equipment Unit or Functional Location ([FR-058](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)).
   2. Retrieves the standardized numerical weight ($W \in [1, 10]$) corresponding to the assigned Work Class ([FR-059](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr), [DT-DM-DOC-001 §4.20](../../../domain-models/class/DT-DM-DOC-001.md#420-workrequestworkclasscode-work-class-rime)).
   3. Computes the deterministic RIME priority score:
      $$\text{Score} = C \times W \quad (\text{Range: } 1..100)$$
      guaranteeing that identical criticality and work-class inputs produce identical scores across the enterprise ([FR-074](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)).
4. The System classifies and visually categorizes each backlog item into four standardized RIME priority bands featuring redundant shape and color coding per ANSI/ISA-101 ([NFR-061](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr), [TR-011](../../../requirements/common/TR-011.md)):
   * **Do First** ($80..100$): Octagon symbol, emergency and immediate safety/production priority band.
   * **Schedule** ($50..79$): Triangle symbol, high operational priority band.
   * **Plan** ($20..49$): Square symbol, standard preventive and corrective routine band.
   * **Wish** ($1..19$): Circle symbol, low-urgency deferrable cosmetic band.
5. The System sorts the backlog descendingly by RIME score ([NFR-062](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr)), enriching each tabular row with key operational metadata: affected Equipment Unit tag and description, ISO 14224 Maintainable Item, estimated wrench hours, and material availability status ([FR-065](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)).
6. The System displays advanced multi-criteria filtering controls (by priority band, functional location hierarchy, and date range per [FR-067](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)) and provides structured data export in CSV and JSON formats ([FR-069](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)).
7. The Planner reviews the objective prioritized list, validates resource allocations, and promotes prioritized items into scheduled maintenance plans or formal Work Orders.

## 4. Alternate Flows
### AF-001: Work Class Modification (Priority Adjustment)
If operational conditions shift and the Planner determines that a pending request requires an altered urgency classification:
1. The Planner selects the target backlog item and initiates a work-class adjustment dialog.
2. The Planner selects an updated canonical Work Class from the standardized taxonomy ([DT-DM-DOC-001 §4.20](../../../domain-models/class/DT-DM-DOC-001.md#420-workrequestworkclasscode-work-class-rime)), such as escalating from Code 6 (*Systematic Preventive Maintenance*, weight 6) to Code 8 (*High Priority Process Work*, weight 8) or Code 10 (*Safety and Environmental Emergency*, weight 10), and provides a mandatory technical justification text.
3. The System calculates the candidate RIME score in real-time ($< 100\text{ms}$ per [NFR-070](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr)) and displays the updated priority band.
4. The Planner confirms the adjustment.
5. The System persists the change within a single atomic transactional boundary:
   1. Mutates the work-class classification and associated numerical weight on the work request.
   2. Updates the calculated priority score and status on the backlog item projection, instantaneously re-ranking the backlog order.
   3. Records an append-only audit trail record with chained SHA-256 cryptographic integrity hashing ([TR-001](../../../requirements/common/TR-001.md)), capturing: timestamp, user identifier, request identifier, previous work class, new work class, resulting score, technical justification, and previous record hash.
6. If the score adjustment causes the item to transition across a major priority category (e.g., entering the *Do First* band), the System issues an asynchronous event notification to the responsible planning and supervisory personnel ([FR-076](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)).

### AF-002: Asset without Defined Criticality (Fail-Safe Default)
If a work request targets an asset whose master technical record lacks a configured numerical criticality index:
1. The System enforces the industrial fail-safe principle ([ADR-002](../../../architecture/adr/ADR-002.md)): to prevent an unconfigured asset from being buried at the bottom of the backlog due to missing multiplier data, the RIME calculation engine applies a pessimistic priority floor:
   $$\text{Score}_{\text{fail-safe}} = \max(C_{\text{default}} \times W, 75)$$
   forcing the item into the *Schedule* (High) priority band regardless of a low work-class weight.
2. The System renders a prominent diagnostic warning banner on the backlog item: *"Asset criticality unconfigured in master catalog. Fail-safe priority floor applied preventively."*
3. The System dispatches an automated notification to the Reliability Engineer requesting immediate calibration of the asset's criticality index in the master equipment registry.
4. The workflow resumes at Main Flow Step 5.

### AF-003: Multi-Work-Order Batching / Grouping Recommendation
When multiple independent work requests target the same physical equipment unit:
1. The System's grouping engine scans pending backlog items and detects that $\ge 2$ requests reference the identical Level 6 Equipment Unit ([FR-068](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)).
2. The System generates a prominent contextual grouping recommendation banner above the data grid, highlighting the clustered equipment unit tag, the count of pending interventions, and the consolidated wrench-time estimate.
3. The Planner clicks "Filter Clustered Requests"; the System filters the data grid to isolate all pending requests targeting that specific machine.
4. The Planner evaluates the batch and bundles the requests into a unified planned maintenance window or shutdown package, optimizing overall plant downtime and technician mobilization.
5. The workflow resumes at Main Flow Step 7.

### AF-004: Master Equipment Criticality Update (Automated Backlog Rescore)
When a Reliability Engineer updates the master criticality index of an equipment unit or functional location in the asset catalog:
1. The asset catalog service publishes an asset criticality modified event ([FR-075](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)).
2. The System executes an automated background transaction querying all active backlog items linked to that equipment unit.
3. The System recalculates the RIME score for each affected backlog item using the updated criticality value and instantaneously updates their position in the backlog ranking.
4. If any affected backlog item transitions across a priority threshold (e.g., from *Schedule* to *Do First*), the System publishes a priority shift notification to the Planner ([FR-076](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)).

## 5. Postconditions
* All pending work requests possess an audited, deterministic RIME priority score ($1..100$) and are mapped to an ANSI/ISA-101 visual priority band.
* The maintenance backlog is objectively ranked in descending order, displaying consolidated labor wrench hours and material availability status.
* Any manual adjustment of work class or priority parameters is immutably recorded in the SHA-256 chained audit trail ([TR-001](../../../requirements/common/TR-001.md)).
* Approved and prioritized backlog items are operationalized and handed off downstream to the Preventive Maintenance Scheduling Form ([SCR-MTTO-001](../../../ui-ux/screens/mtto/SCR-MTTO-001.md)) or Condition-Based Predictive Form ([SCR-MTTO-023](../../../ui-ux/screens/mtto/SCR-MTTO-023.md)) for calendar or telemetry execution.

## 6. Associated Requirements
* **Functional Requirements:**
  * [FR-058](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Asset Criticality retrieval from master records ($1..10$).
  * [FR-059](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Mandatory Work Class selection with numerical weights ($1..10$).
  * [FR-060](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): RIME score calculation via strategy engine.
  * [FR-065](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Backlog row operational metadata display.
  * [FR-066](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Technical breakdown query of RIME calculation factors.
  * [FR-067](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Multi-criteria filtering by priority band, functional location, and date.
  * [FR-068](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Automated multi-request grouping recommendations on identical equipment.
  * [FR-069](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Structured backlog data export in CSV and JSON formats.
  * [FR-074](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Deterministic calculation engine invariant.
  * [FR-075](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Automated backlog rescoring upon master asset criticality modification.
  * [FR-076](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr): Notification dispatch upon significant priority category shifts.
* **Non-Functional Requirements:**
  * [NFR-061](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr): Visual classification into 4 redundant priority bands (Do First, Schedule, Plan, Wish).
  * [NFR-062](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr): Descending RIME sort with authorization restrictions on manual overrides.
  * [NFR-070](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr): UI calculation response time $< 100\text{ms}$ on work class change.
  * [NFR-071](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr): Dashboard rendering performance $< 2\text{s}$ under high request volumes.
  * [NFR-072](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr): Versioned prioritization strategy parameters and anti-tampering protection.
  * [NFR-073](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr): Visibility of technical priority scores restricted to authorized roles.
* **Transversal Requirements:**
  * [TR-001](../../../requirements/common/TR-001.md): Immutable audit trail with SHA-256 chained hashing for work class adjustments.
  * [TR-005](../../../requirements/common/TR-005.md): Comprehensive system auditing and traceability.
  * [TR-006](../../../requirements/common/TR-006.md): Role-Based Access Control (RBAC) enforcement.
  * [TR-008](../../../requirements/common/TR-008.md): Centralized logging and operational monitoring.
  * [TR-011](../../../requirements/common/TR-011.md): ANSI/ISA-101 High Performance HMI grayscale discipline with redundant visual encoding.
