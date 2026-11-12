---
id: UC-INV-007
name: Validate and Activate Master Asset (Commissioning)
module: inv
user_story: INV-007
primary_actor: Reliability Engineer
secondary_actors: []
---

# UC-INV-007: Validate and Activate Master Asset (Commissioning)

## 1. Description
Validates and formally approves the technical inclusion of a physical asset (Equipment Unit, Level 6) into the operational ecosystem. It enforces strict completeness checks (Commissioning Gate), ensuring that critical parameters such as LOTO procedures, physical boundaries, and design attributes are fully documented before the asset is exposed to the Maintenance (MTTO) and Digital Twin (VIS) modules.

## 2. Preconditions
* The Engineer is authenticated in the system with the "Reliability Engineer" role [TR-006](../../../requirements/common/TR-006.md).
* The asset is registered in the catalog in a preliminary/draft status.
* The asset has a Functional Location defined in the system.

## 3. Main Flow
1. The Engineer accesses the inventory control panel and selects the "Assets Pending Validation" view.
2. The System displays a list of equipment in preliminary status, ordered by waiting time.
3. The Engineer selects a specific asset for review.
4. The System presents the complete technical data sheet, applying redundant coding (Shape + Color) to highlight the missing mandatory attributes according to the asset class.
5. The Engineer enters or edits the required technical parameters (e.g., class design attributes, technical manuals association).
6. The Engineer selects the "Authorize Activation" action.
7. The System executes a strict gate validation (Commissioning Gate), verifying that the asset complies with:
   - Valid link to a Functional Location.
   - Criticality and Safety Critical Equipment (SCE) flag defined.
   - Physical boundaries and logical components (Level 8) structured.
   - Isolation points (LOTO) mapped to guarantee safe operations.
8. Upon passing validation, the System:
   - Invokes domain logic to transition the asset status to operational and automatically stamps the current "Start of operation date" for MTBF calculations.
   - Atomically persists the change in the database, enabling the asset for maintenance planning and visualization in the Digital Twin.
   - Records the transaction in the immutable audit trail [TR-001](../../../requirements/common/TR-001.md) via an append-only log with its chained cryptographic integrity hash.
9. The System displays a success confirmation and removes the asset from the review queue.

## 4. Alternate Flows
### AF-001: Technical Rejection due to Inconsistencies
In step 6, if the Engineer determines that the engineering data is incorrect or the physical installation presents unrecoverable deviations:
1. The Engineer selects the "Reject Asset" action.
2. The System requires the mandatory input of a technical reason justifying the return.
3. The Engineer enters the reason and confirms the rejection.
4. The System invokes domain logic to transition the asset to rejected status, permanently blocking its exposure in the Digital Twin views and persisting the entered reason.
5. The System generates the entry in the immutable audit [TR-001](../../../requirements/common/TR-001.md) and dispatches an asynchronous notification to the user responsible for the initial entry for correction.
6. The flow ends and the System returns to the pending list.

### AF-002: Activation Block due to Incomplete Data (Gate Failure)
In step 7, if the System detects that mandatory fields or security configurations are still missing (e.g., LOTO not defined):
1. The System blocks the transition to operational status applying the completeness regulatory restriction of ISO 14224 / ISO 45001.
2. The System alerts the user detailing exactly which engineering or security parameters are missing, using warning iconography and high contrast colors (WCAG 2.1 AA).
3. The flow returns to step 5 so the Engineer can complete the required technical information.

## 5. Postconditions
* The asset is formally activated, with its service date stamped, and exposed to the platform's functional modules (MTTO, VIS).
* It is guaranteed that no asset operates without LOTO configuration and defined physical boundaries.
* The immutability of the decision (approval or rejection) is preserved through the cryptographic log.

## 6. Associated Requirements
* **Functional Requirements:** FR-137, FR-138, FR-139, FR-140, FR-141
* **Non-Functional Requirements:** NFR-144, NFR-145
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-008](../../../requirements/common/TR-008.md), [TR-011](../../../requirements/common/TR-011.md)
