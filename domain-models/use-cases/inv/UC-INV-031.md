---
id: UC-INV-031
name: Manage Spare Part Master Catalog (Part Master)
module: inv
user_story: INV-031
primary_actor: Warehouse Manager
secondary_actors: []
---

# UC-INV-031: Manage Spare Part Master Catalog (Part Master)

## 1. Description
Allows the standardized creation, update, and technical categorization of materials and spare parts in the master catalog (Part Master), preventing duplicates and ensuring that inventory policies (Min/Max, Reorder Point, Just in Time) and unit costs are accurately configured to automate replenishment generation and accurate valuation of Work Orders.

## 2. Preconditions
* The Warehouse Manager is authenticated in the system with the appropriate role [TR-006](../../../requirements/common/TR-006.md).
* The standard catalog of manufacturers and generic Material commodity codes is available.

## 3. Main Flow
1. The Warehouse Manager accesses the Spare Parts Catalog menu and selects the "New Spare Part" option.
2. The System displays the registration form demanding the following mandatory fields:
   - SKU / Unique Code.
   - Technical description and Commodity Code.
   - Manufacturer and reference Model.
   - Material Hierarchical Category (ISO 14224) and Standardized Equipment Class (optional).
   - Unit of Measure (UoM).
   - Special indicators: Repairable Spare (Rebuildable) and Safety Critical Equipment Spare (SCE).
   - Inventory Policy (Reorder Point, Min/Max, JIT).
   - Reorder Point (Critical trigger quantity) and Maximum Warehouse Capacity.
   - Estimated Unit Cost.
3. The Warehouse Manager enters the data of a high-precision bearing, checks the "Repairable Spare" box, and enters the SKU "SKF-6204".
4. The System executes an automatic redundancy and uniqueness analysis against the master database catalog:
   - Validates that the SKU "SKF-6204" is not exactly duplicated.
   - Executes a semantic and phonetic search filter over the descriptions of existing spares to identify potential duplicate records with alternate names.
5. The System confirms the validity of the data and configures the stock monitoring rules according to the chosen policy.
6. The Warehouse Manager confirms saving the spare part.
7. The System permanently and uniquely registers the new spare part in the database's master material catalog, recording creation attributes (user, timestamp, registered SKU, manufacturer, stock policy, and parameterized cost).
8. The System displays a confirmation message of successful registration.

## 4. Alternate Flows
### AF-001: Potential Duplicate Record Detected (Redundant Coding)
In step 4, if the system detects that a spare part with matching characteristics already exists (e.g. a description "Radial Bearing SKF 6204" with a similar SKU):
1. The System interrupts the saving and displays a warning using redundant Shape + Color coding (alert symbol + contrast indicator) according to WCAG 2.1 AA: "Potential duplicate detected: The catalog already has a spare part with similar characteristics (SKU: SKF-6204-A). Do you want to cancel the creation or justify the registration of the new SKU?"
2. If the user decides to cancel, the flow is canceled.
3. If the user justifies the technical need for the new SKU, they enter a mandatory justification and the system continues to step 6, recording the justification in the catalog change record.

### AF-002: Direct Purchase Classification (No Storage)
In step 3, if the Warehouse Manager defines the inventory type as direct purchase ("Direct Purchase / JIT"):
1. The System dynamically adapts the interface, hiding the mandatory storage fields (shelf location, maximum capacity, and reorder point).
2. The flow continues to step 6.

## 5. Postconditions
* The new spare part is registered in the Part Master uniquely and standardized, ready to be consumed in Work Orders.
* Replenishment policies and ABC classification are associated and active for the stock monitor rules.

## 6. Associated Requirements
* **Functional Requirements:** FR-170, FR-171, FR-172, FR-173, FR-174, FR-175, FR-176, FR-181
* **Non-Functional Requirements:** NFR-177, NFR-178, NFR-179, NFR-180
* **Transversal Requirements:** [TR-008](../../../requirements/common/TR-008.md)
