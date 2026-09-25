---
code: DT-ARQ-PAT-DOC-001
version: 1
date: 2026-08-05
status: Architectural and Code Design Patterns Specification
author: Juan David Julio Serrano
standard:
  - GoF (Gang of Four Design Patterns)
  - Domain-Driven Design (DDD)
  - Clean Architecture / Hexagonal Architecture
---

# DTEAM Solution Design Patterns Catalog

## 1. Creational Patterns

### Factory Method
* **Location:** `MaintenancePlan` aggregate root (`GenerateWorkOrder()`).
* **Purpose:** Centralizes the instantiation of the preventive maintenance `WorkOrder` entity. The maintenance plan encapsulates all necessary rules and invariants (work class, asset criticality, Wrench Time estimation, and LOTO point inherence), preventing the application layer from creating incomplete orders.

---

## 2. Structural Patterns

### Adapter
* **Location:** Periphery of the infrastructure layer (Secondary Ports). Examples: `EFCorePostgresAdapter`, `SignalRBroadcaster`.
* **Purpose:** Applies the Dependency Inversion Principle (DIP). The domain core defines abstract interfaces (ports). The infrastructure implements concrete adapters, allowing database engines or network connectors to be changed without altering ISO 14224 business rules.

### Composite
* **Location:** `FunctionalLocation` entity.
* **Purpose:** Allows treating both individual locations (tree leaves) and grouping locations (tree branches) under the same 9-level hierarchical interface (ISO 14224). Simplifies recursive navigation operations and cycle prevention validations (`ReorganizeTree`).

---

## 3. Behavioral Patterns

### Strategy
* **Location:** `IRimeCalculator` contract and `RimeCalculatorService` implementation ([[ADR-002]]).
* **Purpose:** Encapsulates the RIME prioritization algorithm. Allows replacing or extending the calculation in the future with one based on financial risk or inventory availability without modifying the `WorkRequest` entity or the aggregator rules.

### State
* **Location:** Work order execution flow (`WorkOrder.currentStatus`).
* **Purpose:** Encapsulates state transitions (`PLANNING` $\to$ `WAITING_PARTS` $\to$ `SCHEDULED` $\to$ `IN_PROGRESS` $\to$ `COMPLETE` $\to$ `CLOSED`). Encapsulates safety preconditions (such as blocking `IN_PROGRESS` if LOTO or PTW are not verified) within dedicated state classes, eliminating nested `switch/if-else`.

### Observer
* **Location:** Reactive Zero Energy monitoring (`IsolationPoint` as subject, `WorkOrder` as observer).
* **Purpose:** If the IoT adapter detects active energy during the execution of maintenance, the subject notifies the observer, immediately invoking `SuspendExecution()` on the work order to protect the operator.

### Mediator (Native Dispatcher)
* **Location:** `IEventBus` port and `Native Event Dispatcher` implementation.
* **Purpose:** Decouples inter-module asynchronous communication. Allows the Maintenance module (`MTTO`) to emit the `WorkOrderStatusChanged` event and the Inventory module (`INV`) to capture it to execute `RecordConsumption` without sharing direct runtime dependencies.
