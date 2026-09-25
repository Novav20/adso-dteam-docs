---
code: DT-DM-DOC-002
version: 1.2
date: 2026-09-25
status: Behavioral audit gaps resolved (ISO 14224 / Commissioning Gate)
author: Juan David Julio Serrano
standard:
  - ISO 9001:2015
  - ISO 14224:2016
  - Domain-Driven Design (DDD)
---

# Domain Behavior Traceability

## 1. Purpose

This document establishes the Single Source of Truth (SSoT) for the behavior of the classes in the Digital Twin domain model. Its objective is to map each method (operation) of the entities and aggregate roots to the MVP User Stories and Functional Requirements (FR), guaranteeing the traceability required by the ISO 9001 standard.

Additionally, the document justifies the existence of each method under the principles of **Domain-Driven Design (DDD)**. Method signatures use the **PascalCase** convention, in preparation for physical implementation in C# (.NET).

---

## 2. Layer 1: Asset Taxonomy (ISO 14224)

### 2.1. `FunctionalLocation` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `AddChild(child: FunctionalLocation): void` | Hierarchically links a child node validating that its `hierarchyLevel` is strictly greater (lower level in ISO) than the parent's. | [[INV-027]]<br>FR-161 | **Encapsulation:** As an aggregate root, the location must govern and validate business rules when nesting dependencies. |
| `RemoveChild(childId: UUID): void` | Removes a child node, previously validating that the location has no installed assets (`EquipmentUnit`) or orphaned sub-hierarchies. | [[INV-027]]<br>FR-163 | **Lifecycle Invariant:** Protects against data orphanage and ensures logical constraints before allowing deletion. |
| `ReorganizeTree(newParentId: UUID): void` | Changes the parent node of the current location, validating that the movement does not generate logical inconsistencies or infinite cycles. | [[INV-027]]<br>FR-162, NFR-167 | **Rich Behavior:** Changing hierarchy is a complex business rule, not a simple _setter_. It delegates the verification of its own consistency to the entity before moving. |
| `InstallEquipment(equipment: EquipmentUnit): void` | Installs an asset in the operational position, changing its status to INSTALLED and formally linking it. | [[INV-025]]<br>FR-184, FR-185 | **Business Invariant:** Validates that the position is not occupied and that the equipment to be installed is in an operational/available state. |
| `UninstallEquipment(): EquipmentUnit` | Removes the asset from the operational location, returning the equipment instance to manage its storage. | [[INV-025]]<br>FR-183 | **State Machine:** Breaks the link and enables the equipment for physical relocation to the warehouse or workshop. |

### 2.2. `EquipmentUnit` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `Activate(): void` | Formalizes the equipment commissioning (Commissioning Gate), validating the mandatory presence of physical limits (Boundaries) and mapped LOTO points before transitioning to `OPERATIONAL`. | [[INV-007]]<br>FR-139, FR-140, NFR-144 | **Rich Behavior:** Represents the "Commissioning" business concept. Blocks activation if technical or safety configurations are missing. |
| `ValidateChronology(): void` | Validates that the lifecycle milestone sequence maintains logical coherence (e.g., `operationStartDate >= purchaseDate`). | [[INV-005]]<br>FR-119 | **Domain Invariant:** Protects against temporal paradoxes that would corrupt historical reliability metrics. |
| `DefineBoundaries(boundaryStart: String, boundaryEnd: String): void` | Establishes the asset's physical boundaries to avoid ambiguity when recording interventions and downtime. | [[MTTO-029]]<br>FR-092, FR-096 | **ISO 14224 Rule:** Encapsulates the normative obligation to delimit where the physical equipment begins and ends within the industrial process. |
| `UpdateOperationalStatus(newStatus: Enum): void` | Transitions the operational condition (`UP`, `DOWN`, `STANDBY`). | [[MTTO-002]]<br>FR-014 | **Logic Centralization:** Prevents accidental state modifications (Primitive Obsession). Allows emitting Domain Events if the machine goes `DOWN`. |
| `AddSubunit(subunit: Subunit): void` | Links a subcomponent (ISO Level 7) to the internal hierarchy of the physical equipment. | [[MTTO-029]]<br>FR-094 | **Aggregate Control:** As an Aggregate Root, it is solely responsible for adding and managing the collection of its internal parts to maintain consistency. |
| `Decommission(reason: String, disposalDate: Date): void` | Permanently retires the asset from operational service, marking its end of lifecycle. | ISO 55000 Transversal Support | **Lifecycle Invariant:** Logical destructive operation that ensures a retired equipment unit does not receive more maintenance plans. |
| `RejectCommissioning(reason: String): void` | Returns the asset during the commissioning process, recording the technical reason for rejection in `RejectionReason`. | [[INV-007]]<br>FR-141 | **State Machine (Validation):** Completes the commissioning flow allowing rejection of assets that do not meet the data completeness norm (FR-138), requiring a justifying string. |
| `TransitionToStorage(warehouseId: UUID): void` | Changes the asset state to IN_STORAGE and links it to the selected warehouse for safekeeping. | [[INV-025]]<br>FR-183 | **State Transition:** Moves the lifecycle of the serialized asset back to inventory under warehouse control. |
| `TransitionToRepair(): void` | Changes the asset state to UNDER_MAINTENANCE / REPAIR for shipping to the technical workshop. | [[INV-025]]<br>FR-183 | **Lifecycle:** Enables the asset for corrective repair or reconditioning flows (rebuildable). |

### 2.3. `Subunit` (`<<Entity>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `AddMaintainableItem(item: MaintainableItem): void` | Links a maintainable item (Level 8) to the subsystem. | [[MTTO-029]]<br>FR-094 | **Hierarchical Control:** Encapsulates the addition of lower-level components, ensuring the hierarchical tree is built in a controlled manner. |

### 2.4. `MaintainableItem` (`<<Entity>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `UpdateStatus(newStatus: Enum): void` | Transitions the status of the item (e.g., from `OPERATIONAL` to `FAILED` or `REPLACED`). | [[MTTO-002]]<br>FR-011 | **State Machine:** Protects the `Status` attribute, ensuring that failure reports affect the lifecycle of the specific component that failed. |

---

## 3. Layer 2: Maintenance Management (MTTO)

### 3.1. `WorkRequest` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `ApproveAsWorkOrder(): WorkOrder` | Evaluates the request and, if valid, promotes it by returning a newly instantiated Work Order. | [[MTTO-028]]<br>FR-078, FR-081 | **Factory Method:** The request acts as a factory for the work order, maintaining the traceability of the origin of the work. |
| `Reject(reason: String): void` | Marks the request as `REJECTED`, capturing the reason (duplicate, false alarm, out of scope). | [[MTTO-028]] (Implicit) | **Auditability:** Retains the record of why an intake flow was discarded without deleting it from the database. |

### 3.2. `MaintenancePlan` (`<<Aggregate Root>>`)

| Method                                                   | Purpose / Business Rule                                                                                              | Origin (Story / FR)     | Architectural Justification (DDD)                                                                                                        |
| :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- | :---------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| `GenerateWorkOrder(targetDate: DateTime): WorkOrder`     | Acts as a Factory to instantiate a new `WorkOrder` inheriting the tasks, spare parts, and specialties from the plan. | [[MTTO-001]]<br>FR-004  | **Factory Method:** Centralizes the recurring logic. The plan knows exactly how to clone its specifications into an executable instance. |
| `Suspend(reason: String): void`                          | Changes the plan to an `INACTIVE` state, temporarily stopping the generation of new WOs.                             | [[MTTO-001]] (Implicit) | **State Machine:** Useful during general plant shutdowns or operational changes.                                                         |
| `Archive(): void`                                        | Changes the plan to an `ARCHIVED` state marking it as obsolete, preserving the history.                              | Transversal Support     | **Document Retention:** ISO 55000 compliance regarding the retention of obsolete records without physical deletion.                      |
| `CalculateNextTriggerLimit(currentUsage: Decimal): void` | Calculates the next telemetry trigger threshold by adding the `IntervalValue` to the current usage reading.          | [[MTTO-023]]<br>FR-584  | **Telemetry (Usage):** Defines the target of the next WO based on physical variable accumulation (hour meters/cycles).                   |

### 3.3. `WorkOrder` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `Schedule(scheduledDate: DateTime): void` | Transitions the WO to a `SCHEDULED` state, assigning a time window for execution. | Transversal Support | **State Machine:** First step of formal planning. |
| `RequireIsolation(isolationPointId: UUID): void` | Links a physical LOTO point (`IsolationPoint`) that must be mandatorily locked out before work. | [[VIS-011]]<br>FR-228, FR-230 | **Safety Precondition:** Builds the required safety matrix for the safe execution of maintenance. |
| `StartExecution(): void` | Transitions to `IN_PROGRESS`. Internally validates that an approved `WorkPermit` exists and that all LOTO isolations are in a safe state (Zero Energy). | [[VIS-011]]<br>NFR-229 (Critical) | **Critical Invariant (Fail-Safe):** Prevents the start of hazardous work. The behavior encapsulates life and safety validations. |
| `CompleteExecution(actualLaborHours: Decimal): void` | Transitions to `COMPLETE`. Records the wrench time by the technician in the field. | [[MTTO-002]]<br>FR-010, FR-014 | **State Machine:** Separates physical completion (technician) from administrative closure (audit). |
| `CloseAdministratively(): void` | Transitions to `CLOSED`. Validates that failure codes (ISO 14224) and actual consumptions are correctly filled out. | [[MTTO-002]]<br>FR-012 | **Quality Control:** Guarantees the completeness of the maintenance record for reliability KPIs before its final immutability. |
| `ReportFailure(maintainableItemId: UUID, mode: Enum, mechanism: Enum, cause: Enum, detectionMethod: Enum, operationalCondition: Enum, operationalImpact: Enum, technicianNotes: String): void` | Creates and links a complete `FailureRecord` to the WO, applying the ISO 14224 taxonomy (mode, cause, mechanism, detection method, and impacts). | [[MTTO-002]]<br>FR-011 | **Rich Behavior:** The WO governs the failure reporting by capturing the entirety of the dimensions required by ISO 14224. |
| `AddMediaAttachment(fileUrl: String, fileType: Enum): void` | Attaches multimedia evidence to the technical closure. | [[MTTO-002]]<br>FR-013 | **Traceability:** Adds Value Objects (`MediaAttachment`) for auditing. |
| `SuspendExecution(reason: String): void` | Immediately stops the work order (transitions to suspended/blocked state) if unsafe conditions are detected. | [[VIS-011]]<br>FR-232, NFR-234 | **Critical Invariant (LOTO):** If IoT telemetry detects active energy during execution, the WO must protect the worker's life by immediately suspending the normative flow. |

### 3.4. `BacklogItem` (`<<Entity>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `UpdatePriorityScore(score: int): void` | Updates the consolidated score. The calculation is injected by a domain service (`IRimeCalculator`). | [[MTTO-026]]<br>ADR 002 | **Inversion of Control:** Allows the RIME calculation strategy to change (from static to dynamic) without modifying the entity. |
| `Defer(reason: String): void` | Changes the status to `DEFERRED`, intentionally postponing the work. | [[MTTO-026]]<br>FR-064 | **State Machine:** Represents a managerial decision regarding the operational backlog. |
### 3.5. `FailureRecord` (`<<Entity>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `UpdateClassification(mode: Enum, mechanism: Enum, cause: Enum): void` | Allows correcting or updating the taxonomy of the recorded failure. | [[MTTO-002]]<br>FR-011 | **Controlled Mutation:** Allows QA audit (supervisor) before the final closure of the WO. |

## 4. Layer 3: Resource Control (INV)

### 4.1. `SparePart` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `UpdateStockPolicy(policy: Enum, reorderPoint: Decimal, maxCapacity: Decimal): void` | Modifies the replenishment rules for the spare part. | [[INV-031]]<br>FR-173 | **Business Configuration:** Encapsulates the logic of how and when the system should generate stock alerts (INV-021). |
| `ReserveStock(quantity: Decimal): void` | Increases the reserved quantity (`ReservedQuantity`). Fails if it exceeds the available physical quantity. | [[INV-006]]<br>FR-126 | **Critical Invariant:** Protects inventory ensuring that materials planned for future WOs are not accidentally consumed. |
| `ReleaseReservation(quantity: Decimal): void` | Decreases the reserved quantity when a WO is canceled or finished. | [[INV-006]] (Implicit) | **State Consistency:** Frees committed stock so it becomes available again. |
| `ReceiveStock(quantity: Decimal): void` | Increases the quantity on hand (`QuantityOnHand`) after entering the warehouse. | [[INV-006]]<br>FR-125 | **Inventory Transaction:** Single point of mutation for material entries, preventing direct manual assignments to the attribute. |
| `IssueStock(quantity: Decimal): void` | Decreases the quantity on hand and the reserved quantity (if applicable), recording the actual consumption. | [[INV-006]]<br>FR-127 | **Inventory Transaction:** Guarantees that more stock is not issued than physically exists. |

### 4.2. `MaterialRequirement` (`<<Entity>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `MarkAsReserved(): void` | Changes the `IsReserved` flag to `true` once the central inventory confirms material availability. | [[INV-006]]<br>FR-126 | **Transactional Integrity:** Coordinates the status of the WO planning with the actual physical reservation in the `SparePart`. |
| `RecordConsumption(actualQuantity: Decimal): void` | Records the final quantity of spare parts used during the Work Order execution. | [[INV-006]]<br>FR-127 | **Technical Closure:** Allows capturing the difference between the planned and consumed quantity to adjust inventories and costs (KPIs). |

### 4.3. `Supplier` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `UpdateContactInfo(phone: String, email: String, address: String): void` | Updates the operational contact data for the supplier. | Master Data CRUD | **Administrative Consistency:** Master Data requires mutation. If a supplier changes address, the entity must be updated to avoid breaking historical foreign keys. |
| `Deactivate(): void` | Changes the supplier status to INACTIVE. | Master Data CRUD | **Audit Retention:** Prevents new purchase orders without destroying historical references. |

### 4.4. `Warehouse` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `UpdateCapacity(newMaxWeight: Decimal, newMaxVolume: Decimal): void` | Updates the physical storage constraints of the facility. | Master Data CRUD | **Physical Reality Sync:** Warehouses can be expanded or remodeled; the system model must mutate to reflect physical reality. |
| `AddLocator(aisle: String, rack: String, shelf: String, barcode: String): UUID` | Spawns a physical sub-location within the warehouse boundaries. | Master Data CRUD | **Aggregate Root Factory:** The Warehouse controls the creation and validation of its internal physical spaces. |
| `SetStatus(newStatus: Enum): void` | Changes operational status (e.g., OPERATIONAL, UNDER_MAINTENANCE). | Master Data CRUD | **Operational Control:** Allows temporarily blocking material receptions. |

### 4.5. `Locator` (`<<Entity>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `UpdateBarcode(newCode: String): void` | Assigns or updates the physical scanning tag for the bin. | Master Data CRUD | **Physical Tracking:** Allows integration with mobile scanning devices. |
| `Deactivate(): void` | Changes status to INACTIVE. | Master Data CRUD | **State Control:** Disables a bin (e.g. if damaged) preventing new stock placements without deleting history. |

## 5. Layer 4: Digital Twin Convergence (VIS)

### 5.1. `WorkPermit` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `Approve(): void` | Transitions the permit to the `APPROVED` state, enabling it operationally. | [[VIS-011]]<br>FR-225 | **Operational Precondition:** WOs depend on this state to allow the transition to "In Progress" (Fail-Safe). |
| `Revoke(reason: String): void` | Transitions to `REVOKED` immediately due to unsafe conditions. | [[VIS-011]] (Implicit) | **Safety Invariant:** Requires justification (`reason`). Immediately alters the field work authorization. |
| `Expire(): void` | Transitions to `EXPIRED` automatically when the time window runs out. | Business Rule (HSEQ) | **State Machine:** Represents the natural expiration of the permit (Time limit). |
| `Close(): void` | Transitions to `CLOSED` once the intervention is finished and the LOTO is removed. | [[VIS-011]]<br>FR-231 | **State Transition:** Formal and documental closure of the permit. |

### 5.2. `IsolationPoint` (`<<Entity>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `MarkAsVerified(): void` | Changes the `IsVerified` flag to `true` after engineering inspection. | [[VIS-011]] (Implicit) | **Master Data (Safety):** Certifies that the identified physical point (e.g., breaker) effectively isolates the equipment's energy. |

## 6. Layer 5: Safety and Governance (ADM)

### 6.1. `User` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `AssignRole(roleId: UUID): void` | Links a role to the user, granting the associated permission package. | [[ADM-013]]<br>FR-251 | **Access Control:** Manages the Many-to-Many relationship between users and roles through the aggregate root. |
| `RemoveRole(roleId: UUID): void` | Revokes a role previously assigned to the user. | [[ADM-013]] (Implicit) | **Principle of Least Privilege:** Allows access to be withdrawn dynamically. |
| `RecordFailedLogin(): void` | Increments the failed login attempt counter. If it exceeds the threshold, changes the status to `LOCKED` and sets the `LockoutUntil` time. | [[ADM-014]]<br>FR-260 | **Brute Force Protection:** Encapsulates the account lockout logic within the user object itself, preventing the application service from corrupting the rules. |
| `RegisterSuccessfulLogin(): void` | Resets the failed login counter to 0 and clears lockouts. | [[ADM-014]] (Implicit) | **Security Cycle:** Restores the user's trust state after valid authentication. |
| `UpdatePassword(newPasswordHash: String): void` | Updates the user's access credential. | [[ADM-014]]<br>FR-261 | **State Security:** Ensures that the hash mutation is centralized and can be audited. |
| `Deactivate(reason: String): void` | Changes the status to `INACTIVE` (Soft-delete). | [[ADM-014]]<br>FR-262, FR-264 | **Audit Retention:** Prevents login without destroying the user's historical references in other tables. |
| `Activate(): void` | Restores an inactive or locked account to the `ACTIVE` state. | [[ADM-014]]<br>FR-263 | **State Recovery:** Allows human resources or IT to rehabilitate access. |

### 6.2. `Role` (`<<Aggregate Root>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `AddPermission(module: String, action: String): void` | Adds an atomic authorization rule to the role. | [[ADM-013]]<br>FR-248 | **RBAC Management:** The role, as an aggregate root, encapsulates and protects its permission list (Value Objects). |
| `RemovePermission(module: String, action: String): void` | Removes an authorization rule from the role. | [[ADM-013]] (Implicit) | **RBAC Management:** Allows restricting erroneously configured privileges. |
| `ValidateSoD(): void` | Reviews the internal permission matrix to guarantee that no Segregation of Duties conflicts exist (e.g., creator vs. approver). | [[ADM-013]]<br>FR-249 | **Critical Invariant:** ISO 55001/27001 regulatory compliance to prevent internal fraud or unaudited manipulations. |

### 6.3. `AuditLog` (`<<Entity>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `VerifyIntegrity(): boolean` | Recalculates the internal data hash and compares it with the stored `IntegrityHash` to confirm that the record was not physically altered in the DB. | [[ADM-032]]<br>FR-346, FR-351 | **Immutable Security:** Allows the system to cryptographically validate the purity of traceability during audits or exports. |

### 6.4. `AuthToken` (`<<Entity>>`)

| Method | Purpose / Business Rule | Origin (Story / FR) | Architectural Justification (DDD) |
| :--- | :--- | :--- | :--- |
| `Revoke(): void` | Forcibly invalidates the token before its natural expiration. | [[ADM-014]]<br>FR-262 | **Access Control:** Fundamental for instantly killing active sessions when an account is suspended due to security risk. |
| `MarkAsUsed(): void` | Invalidates the token by marking it as used. | [[ADM-014]]<br>FR-261 | **Single-Use Rule:** Prevents replay attacks on sensitive tokens such as password reset links. |

---

## **Architectural Notes**

- The `EquipmentClass` and `InventoryTransaction` classes do not expose mutation methods in this model, as they act as immutable historical records (Ledger) and strict taxonomy catalogs respectively.
- The `MeshMapping`, `TelemetrySignal`, `VisualLayer`, and `SpatialMetadata` classes function as read projections, immutable telemetry reception, or frontend graphical metadata, so they do not expose complex mutating behavior in this MVP model.
- The `WorkOrderAssignment` class does not expose mutating behavior, as it acts purely as an immutable associative entity that captures the moment and role in which a user was linked to a work order.
