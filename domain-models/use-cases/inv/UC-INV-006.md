---
id: UC-INV-006
name: Process Inventory Transaction (Kardex)
module: inv
user_story: INV-006
primary_actor: Warehouse Manager
secondary_actors:
  - Maintenance Planner
  - Maintenance Technician
  - Auditor
---

# UC-INV-006: Process Inventory Transaction (Kardex)

## 1. Description
Executes, reconciles, and audits all physical and logical movements of spare parts and materials across plant warehouses and storage bin locators (inbound receipts, Work Order consumption issues, unused material returns, and physical count adjustments). It dynamically calculates net available stock by deducting active maintenance reservations from physical stock on hand, enforces exact financial cost attribution to Work Orders and intervened Equipment Units, triggers automated replenishment alerts upon crossing reorder thresholds, and seals manual inventory adjustments in the immutable cryptographic audit trail.

## 2. Preconditions
* The Actor is authenticated in the platform with the `Warehouse Manager` role for registering inventory movements, or `Maintenance Planner`, `Maintenance Technician`, and `Auditor` roles for Kardex history consultation and reconciliation ([TR-006](../../../requirements/common/TR-006.md)).
* The target Spare Part (identified by its Stock Keeping Unit, SKU), Warehouse, and physical storage Locator (aisle, rack, and shelf bin) are registered in the master catalog ([SCR-INV-031](../../../ui-ux/screens/inv/SCR-INV-031.md)).
* For material issues or unused material returns, the target Work Order exists in an active execution or pre-closure lifecycle state (`SCHEDULED`, `IN_PROGRESS`, or `COMPLETE`).

## 3. Main Flow
1. The Warehouse Manager accesses the Movements and Kardex History interface ([SCR-INV-006](../../../ui-ux/screens/inv/SCR-INV-006.md)) directly from the Inventory menu or via drill-down from the Equipment Master Data Card ([SCR-INV-005](../../../ui-ux/screens/inv/SCR-INV-005.md)), viewing the chronological movement ledger and multi-criteria filtering controls ([FR-130](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)).
2. The Warehouse Manager selects the action to register a new inventory movement.
3. The System presents the transactional movement form supporting inbound receipts (`RECEIPT` per [FR-125](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)), Work Order consumption issues (`ISSUE` per [FR-127](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)), unused material returns (`RECEIPT` with Work Order cost reversal per [FR-128](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)), and physical count reconciliations (`ADJUSTMENT`).
4. The Manager selects the movement classification (`ISSUE` for Work Order consumption), scans or selects the Spare Part SKU and physical Warehouse Locator bin, and links the target Work Order reference.
5. The System validates the Work Order and retrieves the real-time stock balance for the selected Spare Part with minimal latency ([NFR-133](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr)), displaying physical stock on hand, quantity reserved for planned interventions, and net available stock ([FR-126](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)).
6. The Manager enters the quantity to issue and the transaction reason.
7. The System verifies that the requested issue quantity does not exceed the net available stock (or the Work Order's reserved allocation) in the selected Warehouse Locator ([FR-126](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)).
8. The Manager confirms the inventory movement.
9. Within a single atomic transactional boundary ([NFR-132](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr), [NFR-134](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr)), the System:
   10. Updates the physical quantity on hand and reserved quantity on the Spare Part record.
   11. Computes the exact financial transaction cost from the Spare Part unit cost and transacted quantity without rounding discrepancies ([NFR-134](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr)).
   12. Appends an immutable movement record to the chronological Kardex ledger linking the Spare Part, Warehouse, Locator bin, Work Order, intervened Equipment Unit, quantity, total cost, and UTC timestamp ([FR-127](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)).
   13. Updates the consumed material quantity and accumulated material cost on the associated Work Order.
   14. Records an append-only entry in the immutable audit trail ([TR-001](../../../requirements/common/TR-001.md)) with a chained SHA-256 cryptographic integrity hash ([ADR-003](../../../architecture/adr/ADR-003.md)).
15. The System generates a printable and exportable technical receipt voucher containing the transaction folio and movement metadata ([FR-131](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)) and refreshes the Kardex ledger view.

## 4. Alternate Flows

### AF-001: Insufficient Available Stock or Unallocated Over-Issue
In step 7, if the requested issue quantity exceeds the net available stock in the specified Warehouse Locator ([FR-126](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)):
1. The System blocks the movement submission to prevent negative inventory balances.
2. The System highlights the quantity field using redundant shape and color coding in compliance with WCAG 2.1 AA ([TR-011](../../../requirements/common/TR-011.md)) and displays: *"Insufficient Available Stock: The requested quantity exceeds the net available balance after deducting active Work Order reservations."*
3. The flow returns to step 6 so the Manager can adjust the quantity or select an alternative Warehouse Locator.

### AF-002: Replenishment Threshold or Capacity Limit Alert
In step 9, if the updated physical stock on hand falls at or below the Spare Part's configured Reorder Point (or if an inbound receipt causes stock to approach or exceed Maximum Warehouse Capacity) ([FR-129](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)):
1. The System completes the atomic Kardex movement and immediately triggers a stock policy alert (`BELOW_REORDER_POINT` or `CAPACITY_EXCEEDED`).
2. The System displays a non-modal replenishment warning in the Kardex summary strip and dispatches an automated replenishment notification to procurement and planning personnel ([FR-129](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)).
3. The workflow continues to step 10.

### AF-003: Physical Count Discrepancy Adjustment or Unused Material Return
In step 3, if the Manager selects a Physical Count Adjustment (`ADJUSTMENT`) or an Unused Material Return from a Work Order ([FR-128](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)):
1. For an Unused Material Return, the Manager selects the originating Work Order and returned quantity; the System restores the quantity to warehouse stock and reverses the corresponding material cost charge on the Work Order ([FR-128](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)).
2. For a Physical Count Adjustment, the Manager enters the verified physical count and a mandatory reconciliation reason (such as shrinkage, damage, or cycle-count variance); the System computes the net delta, reconciles the logical stock balance, and seals the before-and-after states and justification in the SHA-256 cryptographic audit trail ([TR-001](../../../requirements/common/TR-001.md)).
3. The workflow continues to step 10.

### AF-004: Temporary Connectivity Loss and Background Retry
In step 8, if the warehouse terminal experiences a temporary wireless network interruption while submitting a movement ([NFR-136](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr), [TR-007](../../../requirements/common/TR-007.md)):
1. The System encrypts and persists the pending inventory movement locally ([TR-002](../../../requirements/common/TR-002.md)) with a unique client-generated idempotency token ([ADR-005](../../../architecture/adr/ADR-005.md), [ADR-007](../../../architecture/adr/ADR-007.md)).
2. The System displays a pending synchronization indicator in the header without blocking warehouse operations.
3. Upon connectivity restoration, the background synchronization worker automatically retries and commits the queued movement in strict chronological order ([NFR-136](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr)).

## 5. Postconditions
* The inventory movement is permanently recorded in the chronological Kardex ledger with exact quantity and financial valuation parity ([NFR-134](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr)).
* Physical stock on hand, reserved stock, and net available stock are atomically updated across the Spare Part and Warehouse Locator records ([FR-126](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr), [NFR-132](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr)).
* Work Order material consumption and equipment maintenance costs accurately reflect all issues and returns ([FR-127](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr), [FR-128](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)).
* A technical receipt voucher is available for the completed operation ([FR-131](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr)), and all mutations are sealed in the SHA-256 chained audit trail ([TR-001](../../../requirements/common/TR-001.md)).

## 6. Associated Requirements
* **Functional Requirements:**
  * [FR-125](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr): Formal registration of material receipts with spare part, quantity, physical locator, and audit linkage.
  * [FR-126](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr): Dynamic calculation of net available stock accounting for physical quantities and pending maintenance reservations.
  * [FR-127](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr): Material issues linked to Work Orders with full traceability to the intervened Equipment Unit.
  * [FR-128](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr): Return of unused materials to inventory with automatic cost reversal on the corresponding Work Order.
  * [FR-129](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr): Automated notifications for low stock (reorder point) or excess inventory conditions.
  * [FR-130](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr): Querying and multi-criteria filtering on the chronological Kardex movement history.
  * [FR-131](../../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr): Generation of a technical receipt voucher containing transaction metadata upon completion.
* **Non-Functional Requirements:**
  * [NFR-132](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr): Atomic transaction guarantee preventing partial or inconsistent inventory states upon interruption.
  * [NFR-133](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr): Low-latency stock availability validation to prevent warehouse dispatch delays.
  * [NFR-134](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr): Exact mathematical consistency between inventory balances and Work Order material costs.
  * [NFR-135](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr): Sustained system responsiveness during peak warehouse transaction volume.
  * [NFR-136](../../../requirements/user-stories/inv/INV-006.md#non-functional-requirements-nfr): Background retry persistence mechanism preventing loss of movements during temporary connectivity drops.
* **Transversal Requirements:**
  * [TR-001](../../../requirements/common/TR-001.md): Immutable audit trail with SHA-256 cryptographic hash chaining.
  * [TR-002](../../../requirements/common/TR-002.md): Encryption at rest for locally queued offline warehouse movements.
  * [TR-005](../../../requirements/common/TR-005.md): Encryption in transit across all inventory APIs and synchronization channels.
  * [TR-006](../../../requirements/common/TR-006.md): Role-Based Access Control (RBAC) enforcement.
  * [TR-007](../../../requirements/common/TR-007.md): Offline-first outbox synchronization with idempotent retry.
  * [TR-011](../../../requirements/common/TR-011.md): ANSI/ISA-101 High-Performance HMI grayscale discipline and WCAG 2.1 AA redundant coding.
* **Architectural Decision Records:**
  * [ADR-003](../../../architecture/adr/ADR-003.md): Tamper-evident cryptographic SHA-256 hash chaining for audit logs.
  * [ADR-005](../../../architecture/adr/ADR-005.md): Sequential UUIDv7 identifier generation for inventory transactions.
  * [ADR-007](../../../architecture/adr/ADR-007.md): Idempotent command processing via client-generated idempotency keys.