---
id: UC-INV-031
name: Manage Spare Part Master Catalog (Part Master)
module: inv
user_story: INV-031
primary_actor: Warehouse Manager
secondary_actors:
  - Maintenance Planner
  - Reliability Engineer
  - Auditor
---

# UC-INV-031: Manage Spare Part Master Catalog (Part Master)

## 1. Description
Governs the standardized creation, technical classification, supplier linkage, and replenishment policy administration of materials and spare parts in the centralized Part Master catalog. It enforces sub-second Stock Keeping Unit (SKU) uniqueness, executes automated similarity analysis to prevent redundant catalog entries, validates standardized Units of Measure (ISO 80000), dynamically adapts storage parameters for Just-In-Time direct purchases, supports consolidated CSV/JSON catalog exports for cyclical audits, and audits all technical attribute and stock policy modifications under cryptographic version control.

## 2. Preconditions
* The Actor is authenticated in the platform with the `Warehouse Manager` role for catalog creation and policy administration, or `Maintenance Planner`, `Reliability Engineer`, and `Auditor` roles for technical search, spare part verification, and audit inspection ([TR-006](../../../requirements/common/TR-006.md)).
* Standardized ISO 14224 Equipment Classes, hierarchical Commodity Codes, ISO 80000 Units of Measure, and approved Suppliers (with contact details and commercial warranty terms) are registered in the master reference catalogs.
* The Actor accesses the Spare Parts Master Catalog ([SCR-INV-031](../../../ui-ux/screens/inv/SCR-INV-031.md)) from the Web Portal Inventory menu or via the `"Verify Spare Parts"` handoff in the Preventive Maintenance Scheduling Form ([SCR-MTTO-001](../../../ui-ux/screens/mtto/SCR-MTTO-001.md)).

## 3. Main Flow
1. The Warehouse Manager accesses the Spare Parts Master Catalog ([SCR-INV-031](../../../ui-ux/screens/inv/SCR-INV-031.md)), which renders summary health cards (`ACTIVE`, below-reorder/stockout alerts, rebuildable rotables, direct JIT items, suspended/obsolete items), multi-criteria technical search (`Sku`, `Description`, `Manufacturer`, `Supplier`, `Status`), and cascading category navigation across the material catalog ([FR-172](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr), [FR-175](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr), [NFR-180](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr)).
2. The Warehouse Manager selects the header registration action (`[+ Register Spare Part]`) to onboard a new spare part ([FR-170](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr)).
3. The System presents the centered Part Master registration modal requiring the following standardized parameters:
   * Unique Stock Keeping Unit identifier (`Sku`).
   * Technical Description and Original Equipment Manufacturer (`Manufacturer`) name.
   * Hierarchical Commodity Code and compatible ISO 14224 Equipment Class ([FR-172](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr)).
   * Standardized Unit of Measure (`UnitOfMeasure`) validated against ISO 80000 conventions ([FR-181](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr)).
   * Primary authorized `Supplier` association (linking commercial contact details and warranty terms).
   * Rebuildable / Rotable indicator (`IsRebuildable`, specifying whether dismounted units are sent to workshop overhaul rather than discarded).
   * Replenishment Stock Policy (`REORDER_POINT`, `MIN_MAX`, or `JUST_IN_TIME`), dynamically configuring storage threshold inputs ([FR-173](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr)).
   * `ReorderPoint` threshold, `MaxCapacity` warehouse ceiling, Standard `UnitCost`, and initial catalog lifecycle status (`ACTIVE`, `SUSPENDED`, or `OBSOLETE`).
4. The Warehouse Manager enters the technical parameters for a cartridge mechanical seal, selects the hierarchical Commodity Code in under 1 second ([NFR-179](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr)), marks the rebuildable indicator, selects the `REORDER_POINT` policy, and enters SKU `"SKU-SEAL-API682"`.
5. The System executes automated uniqueness and duplicate redundancy validations:
   * Verifies in under 1 second that the SKU identifier is globally unique in the Part Master ([NFR-177](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr)).
   * Executes a similarity comparison across existing technical descriptions, manufacturers, and commodity codes in under 2 seconds to detect potential duplicate records ([FR-171](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr), [NFR-178](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr)).
6. The System confirms that no exact or semantic duplicates exist, validates the Unit of Measure and stock policy thresholds, and prepares the candidate SHA-256 cryptographic integrity seal.
7. The Warehouse Manager confirms saving the spare part record.
8. Within a single atomic transactional boundary, the System:
   * Persists the new Spare Part record in the Part Master catalog in `ACTIVE` status with its configured replenishment policy and supplier link.
   * Records an append-only entry in the immutable audit trail ([TR-001](../../../requirements/common/TR-001.md)) with a chained SHA-256 cryptographic integrity hash ([ADR-003](../../../architecture/adr/ADR-003.md)).
9. The System displays a documentary confirmation notice in the governance footer, updates the catalog grid and summary metrics, and enables consolidated CSV/JSON catalog report exports for cyclical inventory audits ([FR-176](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr)).

## 4. Alternate Flows

### AF-001: Exact SKU Collision or Potential Duplicate Spare Part Detected
In step 5, if the System detects an exact SKU collision or identifies an existing catalog item with matching technical characteristics ([FR-171](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr), [NFR-177](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr), [NFR-178](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr)):
1. If the SKU already exists, the System hard-blocks registration, highlights the SKU input using redundant ban shape and critical color coding per WCAG 2.1 AA ([TR-011](../../../requirements/common/TR-011.md)), and requires a unique SKU.
2. If the SKU is unique but the similarity engine detects a potential duplicate record (such as an existing part with matching manufacturer and description), the System pauses submission and displays a redundant warning card inside the registration modal requiring either cancellation to reuse the existing SKU or a mandatory engineering override justification ($\ge 15$ characters).
3. If the Manager enters a valid technical justification and confirms override, the System proceeds to step 8 and seals the duplicate override justification in the SHA-256 audit trail ([TR-001](../../../requirements/common/TR-001.md)).

### AF-002: Direct Purchase / Just-In-Time Policy Selection (No Warehouse Storage)
In step 3, if the Warehouse Manager classifies the spare part under the `JUST_IN_TIME` (direct purchase) replenishment policy ([FR-173](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr)):
1. The System dynamically adapts the registration modal or lateral `Policy` tab, hiding physical warehouse storage thresholds (`ReorderPoint` and `MaxCapacity`) and setting them to zero.
2. The System marks the item with a direct-procurement replenishment indicator while retaining its standard `ACTIVE` catalog lifecycle state so maintenance planners know the part is procured on demand against scheduled Work Orders.
3. The workflow continues to step 5 (or policy commit in `AF-003`).

### AF-003: Versioned Stock Policy or Lifecycle Status Update
When the Warehouse Manager updates the replenishment policy, reorder thresholds, supplier warranty terms, or lifecycle status (`ACTIVE`, `SUSPENDED`, or `OBSOLETE`) of an existing Spare Part ([FR-174](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr)):
1. The Manager selects the Spare Part row in the catalog (opening the on-demand inspection dock and switching to the dedicated `Policy` tab), modifies the policy parameters or status (such as transitioning a discontinued part to `OBSOLETE` to block new purchases while preserving historical reliability records), and enters a mandatory audit justification ($\ge 15$ characters).
2. The System validates that `ReorderPoint` does not exceed `MaxCapacity` and commits the update atomically via the lateral `Policy` commit action, incrementing the revision number and recording the before-and-after version states in the SHA-256 chained audit trail ([TR-001](../../../requirements/common/TR-001.md)).

## 5. Postconditions
* The Spare Part is uniquely standardized in the Part Master catalog, linked to its ISO 14224 Equipment Class, Commodity Code, ISO 80000 Unit of Measure, and approved Supplier.
* Replenishment policies (`REORDER_POINT`, `MIN_MAX`, or `JUST_IN_TIME`) are active for automated stock threshold monitoring (`STOCKOUT` / `BELOW_REORDER_POINT`) in the Kardex ([SCR-INV-006](../../../ui-ux/screens/inv/SCR-INV-006.md)).
* All catalog creations, duplicate override justifications, and versioned policy updates are immutably recorded in the SHA-256 audit trail ([TR-001](../../../requirements/common/TR-001.md)).

## 6. Associated Requirements
* **Functional Requirements:**
  * [FR-170](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr): Creation of spare parts capturing unique SKU, technical description, manufacturer, and industrial classification.
  * [FR-171](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr): Automated detection of potential duplicate records by comparing technical attributes during registration.
  * [FR-172](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr): Hierarchical selector for material classification across ISO 14224 classes, families, and commodity groups.
  * [FR-173](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr): Dynamic configuration of inventory management fields based on the selected replenishment policy.
  * [FR-174](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr): Audited update of technical attributes and stock policies under version control.
  * [FR-175](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr): Multi-criteria technical search optimizing spare part lookup for Equipment Units.
  * [FR-176](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr): Generation of consolidated Part Master catalog reports for cyclical inventory and technical audits.
  * [FR-181](../../../requirements/user-stories/inv/INV-031.md#functional-requirements-fr): Automatic validation and standardization of Units of Measure (ISO 80000).
* **Non-Functional Requirements:**
  * [NFR-177](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr): Immediate SKU uniqueness validation executing in under 1 second.
  * [NFR-178](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr): Redundancy analysis for potential duplicate detection completing in under 2 seconds.
  * [NFR-179](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr): Taxonomic validation and hierarchical category navigation executing in under 1 second.
  * [NFR-180](../../../requirements/user-stories/inv/INV-031.md#non-functional-requirements-nfr): Consistent multi-criteria search performance across extensive industrial material catalogs.
* **Transversal Requirements:**
  * [TR-001](../../../requirements/common/TR-001.md): Immutable audit trail with SHA-256 cryptographic hash chaining.
  * [TR-005](../../../requirements/common/TR-005.md): Encryption in transit across all catalog queries and policy mutation commands.
  * [TR-006](../../../requirements/common/TR-006.md): Role-Based Access Control (RBAC) enforcement.
  * [TR-008](../../../requirements/common/TR-008.md): ISO 14224 taxonomic hierarchy management and equipment class compatibility validation.
  * [TR-011](../../../requirements/common/TR-011.md): ANSI/ISA-101 High-Performance HMI grayscale discipline and WCAG 2.1 AA redundant coding.
* **Architectural Decision Records:**
  * [ADR-003](../../../architecture/adr/ADR-003.md): Tamper-evident cryptographic SHA-256 hash chaining for audit logs.
  * [ADR-005](../../../architecture/adr/ADR-005.md): Sequential UUIDv7 primary key generation for catalog entities.
