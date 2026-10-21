---
id: UC-INV-006
name: Process Inventory Transaction (Kardex)
module: inv
user_story: INV-006
primary_actor: Inventory Manager
secondary_actors: []
---

# UC-INV-006: Process Inventory Transaction (Kardex)

## 1. Description
Executes and records all physical and logical movements of materials, spare parts, and tools in the warehouse (In, Out, Transfer, Adjustment, Reservation), ensuring atomic consistency of the available stock levels and financial cost traceability for Work Orders.

## 2. Preconditions
* The Inventory Manager is authenticated in the system [TR-006](../../../requirements/common/TR-006.md).
* The spare part or material to be transacted is registered in the master catalog.
* If the transaction is an output, the target Work Order must exist and be in a valid status (e.g. `PLANNING` or `IN_PROGRESS`).

## 3. Main Flow
1. The Inventory Manager accesses the "Inventory Operations" module and selects "New Transaction".
2. The System displays the transaction form.
3. The Manager selects the Transaction Type: "Output for Work Order" (OUT).
4. The Manager enters the reference of the target Work Order and the ID (SKU) of the item to be dispatched (e.g. "Bearing 6204-2Z").
5. The System validates the existence of the Work Order and retrieves the current stock availability of the selected item in the source warehouse.
6. The Manager specifies the quantity to dispatch (e.g. 2 units) and the source location (e.g. "Warehouse A, Bin 14").
7. The System validates that the requested quantity is less than or equal to the available stock in the specified location.
8. The Manager confirms the transaction.
9. The System executes a transactional block in the database (ACID):
   - Deducts the dispatched quantity from the physical and available stock of the item in the specified warehouse.
   - Calculates the transaction cost based on the active inventory valuation method (e.g. Average Cost).
   - Generates the transaction record in the Kardex with the transaction ID, type, item, quantity, cost, user, timestamp, and reference to the Work Order.
   - Updates the total material cost of the target Work Order.
10. The System confirms transactional persistence in the Kardex ledger. If the operation is a manual Stock Adjustment (discrepancy / inventory write-off, AF-003), the event is also recorded in the immutable audit trail [TR-001](../../../requirements/common/TR-001.md).
11. The System displays a success confirmation and the unique transaction folio number.

## 4. Alternate Flows
### AF-001: Insufficient Stock (Validation Error)
In step 7, if the requested quantity exceeds the available stock in the location:
1. The System blocks the transaction.
2. The System highlights the quantity field with an error indicator and displays the message: "Insufficient stock. The requested quantity exceeds the available stock (Current: X units)."
3. The flow returns to step 6 for the Manager to adjust the quantity.

### AF-002: Reorder Point Trigger (Automated Event)
In step 9, after the stock deduction, if the new physical stock of the item is equal to or less than its configured Reorder Point:
1. The System automatically generates a "Purchase Requisition" draft for the item.
2. The System sends a notification to the Purchasing Department: "Reorder point reached for Item [SKU]. Suggested replenishment: [Economic Order Quantity]."
3. The main flow continues normally.

### AF-003: Stock Adjustment (Physical Count)
In step 3, if the Manager selects Transaction Type: "Physical Adjustment" (ADJUST):
1. The Manager enters the item, the actual physical quantity counted, and a justification code (e.g. "Shrinkage", "Counting Error").
2. The System calculates the difference between the physical count and the logical stock.
3. The System adjusts the logical stock to match the physical count and records a financial loss/gain entry in the Kardex.
4. The System records the manual discrepancy and justification in the immutable audit trail [TR-001](../../../requirements/common/TR-001.md).
5. The flow continues to step 11.

## 5. Postconditions
* The inventory movement is immutably recorded in the transactional Kardex ledger.
* The stock levels and available stock of the spare part are updated atomically in the database.
* The cost of the associated work order is updated with the real value of the dispatched or returned materials.
* Manual stock adjustments and inventory write-offs are cryptographically audited under [TR-001](../../../requirements/common/TR-001.md).

## 6. Associated Requirements
* **Functional Requirements:** FR-125, FR-126, FR-127, FR-128, FR-129, FR-130, FR-131
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md)
