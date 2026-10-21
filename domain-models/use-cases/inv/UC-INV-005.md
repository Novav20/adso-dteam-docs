---
id: UC-INV-005
name: Register Physical Asset Master (Catalog)
module: inv
user_story: INV-005
primary_actor: Reliability Engineer
secondary_actors: []
---

# UC-INV-005: Register Physical Asset Master (Catalog)

## 1. Description
Allows the formal registration of a new physical asset (Equipment Unit, Level 6) in the master catalog, establishing its initial taxonomic hierarchy according to ISO 14224, defining its technical boundaries, functional location, and operational criticality to support failure analysis and RIME prioritization.

## 2. Preconditions
* The Engineer is authenticated in the system with the "Reliability Engineer" role [TR-006](../../../requirements/common/TR-006.md).
* The master plant taxonomy (Functional Locations) is previously configured in the system.
* The standard Equipment Classes are defined in the reference dictionary.

## 3. Main Flow
1. The Engineer accesses the Asset Catalog module and selects "Register New Equipment".
2. The System displays the registration form requesting technical attributes and chronological milestones.
3. The Engineer enters the identification data (Industrial Tag, Serial Number), design and operation attributes (Equipment Class, Manufacturer, Model, Normal Operating Mode, Initial Criticality, Safety Critical Equipment - SCE indicator) and lifecycle dates (Purchase, Installation, Start of Operation).
4. The Engineer selects the Functional Location from the hierarchical tree to which the asset will be linked.
5. The Engineer confirms the action to save the record.
6. The System validates that all critical attributes declared by the ISO 14224 standard are filled out.
7. The System validates that the industrial tag and serial number of the equipment are globally unique in the master catalog.
8. The System validates the logical coherence of the entered dates (e.g. the start of operation date must be equal to or later than the purchase date).
9. The System:
   - Atomically persists the new asset data sheet in the database in initial lifecycle status.
   - Generates an entry in the immutable audit trail [TR-001](../../../requirements/common/TR-001.md) via an append-only record with its corresponding chained cryptographic integrity hash (SHA-256), capturing: user, timestamp, Equipment Tag, class, criticality and associated functional location.
10. The System displays a success confirmation message and redirects to the detailed view of the new technical data sheet.

## 4. Alternate Flows
### AF-001: Incomplete Mandatory Fields (Redundant Coding)
In step 6, if the Engineer omitted any critical attribute (e.g. Equipment Class or Criticality):
1. The System interrupts the saving transaction.
2. The System highlights the missing fields applying redundant Shape + Color coding (warning symbol and contrast indicator) according to WCAG 2.1 AA and displays a notification: "ISO 14224 Inconsistency: Mandatory technical data is missing to formalize the asset registration."
3. The flow returns to step 3 for correction.

### AF-002: Identifier Conflict (Duplicate Tag)
In step 7, if the identifier or serial number already exists in the database:
1. The System blocks the persistence to protect the catalog's uniqueness.
2. The System issues an integrity warning: "The entered Identifier/Tag is already assigned to an existing asset. Review the inventory or enter a valid identifier."
3. The flow returns to step 3.

### AF-003: Chronological Inconsistency of Dates
In step 8, if a temporal paradox is detected (e.g. operation prior to acquisition):
1. The System interrupts the saving.
2. The System alerts about the logical error: "Chronological inconsistency: The start of operation date cannot be prior to the asset's purchase date."
3. The flow returns to step 3 so the Engineer can adjust the equipment's schedule.

## 5. Postconditions
* The new physical asset (Equipment Unit) is formalized and uniquely available in the master catalog with its initial criticality for the RIME engine.
* The plant's hierarchical structure is updated reflecting the equipment in its corresponding functional location.
* The creation transaction is protected under the immutable audit trail.

## 6. Associated Requirements
* **Functional Requirements:** FR-116, FR-117, FR-118, FR-119, FR-120
* **Non-Functional Requirements:** NFR-121, NFR-122
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-008](../../../requirements/common/TR-008.md)
