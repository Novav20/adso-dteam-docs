---
code: DT-ARQ-CMP-DOC-001
version: 1.4
date: 2026-09-25
status: Active
author: Juan David Julio Serrano
standard:
  - ISO/IEC 42010:2011 (Architecture — C4 Level 3 Views)
  - ISO 9001:2015 (Document Control)
  - ISO 14224:2016
  - ISO 45001:2018 (Clause 8.1 — LOTO)
  - ISO 55001:2014
  - Domain-Driven Design / Hexagonal Architecture
---

# Technical Interface and Port Specification

## 1. Scope and Objective

This document constitutes the detailed design specification (C4 Level 3) that complements the component diagram (`DT-ARQ-CMP-001-component-model.puml`). Its purpose is to serve as the single source of truth (SSoT) for the development team, translating the boundaries and functional ports of the diagram into physical C# (.NET 10) code interfaces and PostgreSQL relational storage schemas.

The specification is strictly limited to the scope of the **Minimum Viable Product (MVP)**, consolidating the logic of immutable logs without collisions, automatic backlog prioritization based on the RIME industrial standard, reactive telemetry synchronization for safety, and physical inventory control for Asset Swaps.

---

## 2. Component and Port Specification Matrix

| Component ID | Component or Functional Port | Architectural Layer / Stereotype | Port / Interface | Technical Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **mobile_app** | Mobile App | Client Application | .NET MAUI Blazor | Offline-first field client for touch execution. |
| **local_db** | SQLite Offline DB | Persistence | sqlite-net-pcl | Offline-first relational store (SQLCipher encrypted). |
| **loto_watchdog** | LOTO Safety Watchdog | Component | C# Background Service | Real-time verification of Zero Energy thresholds on the mobile client. |
| **web_admin** | Web Admin Portal | Client Application | Blazor Web App | HSEQ supervision, planning, and dashboards. |
| **idempotency_filter** | Idempotency Filter | Driving Adapter | IActionFilter | Intercepts requests with the Idempotency-Key header; prevents reprocessing critical transitions resent after reconnection (TR-007). |
| **api_controllers** | REST API Controllers | Driving Adapter | Minimal APIs | Exposes HTTPS endpoints; handles optimistic concurrency control using row version marks (RowVersion/ETag). |
| **signalr_hub** | SignalR Hub | Driving Adapter | SignalR.Hub | Persistent bidirectional channel over WebSockets (WSS); degrades to polling if the industrial network fails. |
| **telemetry_listener** | Telemetry Listener (IoT) | Driving Adapter | IHostedService | Asynchronous consumer (AMQP) of the Azure IoT Hub broker; injects telemetry to the LOTO port. |
| **sync_worker** | Background Sync Worker | Driving Adapter | IHostedService | Asynchronously and idempotently processes offline queues transmitted from mobile clients after recovering connection (TR-007). |
| **tax_port** | Taxonomy Port | Primary Port (In) | ITaxonomyService | Manages the ISO 14224 hierarchy (asset registration, decommissioning, re-parenting, and cycle validation). |
| **mtto_port** | Maintenance Port | Primary Port (In) | IWorkOrderService | Backlog administration, priority calculations, preventive scheduling, and failure reporting. |
| **inv_port** | Inventory Port | Primary Port (In) | IInventoryService | Warehouse transactions, critical stock control, and physical equipment rotation (Asset Swap). |
| **loto_port** | Safety & LOTO Port | Primary Port (In) | ILotoService | Secure job authorization: permit approval, physical lockouts, and Zero Energy condition. |
| **sec_port** | Security Port | Primary Port (In) | ISecurityService | IAM governance: authentication, session renewal, RBAC validations, and immutable auditing. |
| **rime_calc** | RIME Calculator | Domain Service | IRimeCalculator | Encapsulates the RIME prioritization calculation using the Strategy pattern (ADR-002). |
| **event_bus** | Event Bus Port | Domain Service | IEventBus | Decouples internal logic between monolith modules via in-memory domain events. |
| **asset_repo** | Asset Repository Port | Secondary Port (Out) | IEquipmentRepository | Persistence interface for the master catalog (FunctionalLocation, EquipmentUnit). |
| **mtto_repo** | Maintenance Repository Port | Secondary Port (Out) | IWorkOrderRepository | Persistence interface for transactional entities (WorkOrder, FailureRecord). |
| **inv_repo** | Inventory Repository Port | Secondary Port (Out) | IInventoryRepository | Persistence interface for material control and safety inventories. |
| **sec_repo** | Audit Repository Port | Secondary Port (Out) | ISecurityRepository | Persistence interface for user accounts, security roles, sessions, and AuditLog. |
| **notify_port** | Notification Port | Secondary Port (Out) | INotificationPort | Synchronous broadcast of safety alerts and LOTO status to the outside. |
| **telemetry_bus** | Telemetry Stream Bus | Domain Service | ITelemetryBus | Internal pub/sub channel for high-frequency safety telemetry streams. |
| **telemetry_repo** | Telemetry Repository Port | Secondary Port (Out) | ITelemetryRepository | Persistence interface for historical time-series data. |
| **telemetry_ef_adapter**| Telemetry EF Adapter | Driven Adapter | TelemetryDbContext | Unit of Work; optimized bulk-inserts into TimescaleDB. |
| **tax_ef_adapter** | Taxonomy EF Adapter | Driven Adapter | TaxonomyDbContext | Unit of Work for Taxonomy domain schema. |
| **mtto_ef_adapter** | Maintenance EF Adapter | Driven Adapter | MaintenanceDbContext | Unit of Work for Maintenance domain schema. |
| **inv_ef_adapter** | Inventory EF Adapter | Driven Adapter | InventoryDbContext | Unit of Work for Inventory domain schema. |
| **sec_ef_adapter** | Security EF Adapter | Driven Adapter | SecurityDbContext | Unit of Work; persists AuditLog to append-only table. |
| **signalr_broadcaster**| SignalR Broadcaster | Driven Adapter | IHubContext<T> | Broadcasts data to SignalR channels filtering by authorized role. |
| **db_postgres** | PostgreSQL Master | External System | Relational Database | Master relational store (PostgreSQL 18 + TimescaleDB). |
| **azure_iot** | Azure IoT Hub | External System | Cloud Broker | Managed broker for asynchronous telemetry ingestion. |
| **redis_cache** | Redis Cache | External System | In-Memory Datastore | Distributed cache for idempotency keys. |
| **scada_node** | SCADA Control Station | External System | Edge Device | Local control station (Edge Node) sending industrial telemetry to Azure IoT. |

---

## 3. Interaction and Data Flow Matrix

| Caller ID | Callee ID | Protocol / Technology | Technical Description |
| :--- | :--- | :--- | :--- |
| **mobile_app** | **api_controllers** | HTTPS / JSON | Transmits offline mutation queue upon recovering network connection. |
| **web_admin** | **signalr_hub** | WSS (WebSockets) | Subscribes to real-time events for KPIs and LOTO status. |
| **telemetry_listener** | **loto_port** | In-Process Method Call | Routes incoming IoT readings to evaluate Zero Energy thresholds. |
| **api_controllers** | **tax_port** | In-Process Method Call | Invokes asset structure registration and graph validations. |
| **api_controllers** | **mtto_port** | In-Process Method Call | Routes backlog admission and work order status transition requests. |
| **api_controllers** | **inv_port** | In-Process Method Call | Routes warehouse transactions and physical asset rotation operations. |
| **api_controllers** | **loto_port** | In-Process Method Call | Routes safety validations and physical lockout confirmations. |
| **api_controllers** | **sec_port** | In-Process Method Call | Validates JWT token and RBAC matrix before processing requests. |
| **mtto_port** | **rime_calc** | In-Process Method Call | Computes deterministic backlog priority scoring via Strategy pattern. |
| **tax_port** | **asset_repo** | C# Interface (DI) | Abstraction for taxonomy graph persistence operations. |
| **mtto_port** | **mtto_repo** | C# Interface (DI) | Abstraction for work order and failure record persistence. |
| **inv_port** | **inv_repo** | C# Interface (DI) | Abstraction for inventory transactions and stock levels. |
| **sec_port** | **sec_repo** | C# Interface (DI) | Abstraction for identity management and chained hash audit logging. |
| **loto_port** | **notify_port** | C# Interface (DI) | Abstraction for broadcasting critical safety alerts. |
| **asset_repo** | **tax_ef_adapter** | C# Class Inheritance | Implements persistence via TaxonomyDbContext. |
| **mtto_repo** | **mtto_ef_adapter** | C# Class Inheritance | Implements persistence via MaintenanceDbContext. |
| **inv_repo** | **inv_ef_adapter** | C# Class Inheritance | Implements persistence via InventoryDbContext. |
| **sec_repo** | **sec_ef_adapter** | C# Class Inheritance | Implements persistence via SecurityDbContext. |
| **notify_port** | **signalr_broadcaster**| C# Class Inheritance | Implements broadcast via Microsoft.AspNetCore.SignalR. |
| **tax_ef_adapter** | **db_postgres** | TCP/IP (SQL) | Executes transactional relational commands. |
| **mtto_ef_adapter** | **db_postgres** | TCP/IP (SQL) | Executes transactional relational commands. |
| **inv_ef_adapter** | **db_postgres** | TCP/IP (SQL) | Executes transactional relational commands. |
| **sec_ef_adapter** | **db_postgres** | TCP/IP (SQL) | Executes transactional relational commands. |
| **scada_node** | **azure_iot** | MQTT / AMQP | Transmits raw industrial telemetry to the cloud broker. |
| **azure_iot** | **telemetry_listener** | AMQP | Pushes high-frequency telemetry events to the backend consumer. |
| **mobile_app** | **idempotency_filter** | HTTPS | Sends sync payloads containing idempotency keys in headers. |
| **idempotency_filter** | **redis_cache** | TCP (RESP) | Queries and sets idempotency keys (SETNX) to prevent duplicate transactions. |
| **sync_worker** | **mtto_port** | In-Process Method Call | Routes dequeued offline work orders to the maintenance domain. |
| **mtto_port** | **event_bus** | In-Process Method Call | Publishes domain events (e.g., WorkOrderClosed) for cross-module orchestration. |
| **loto_port** | **telemetry_bus** | In-Process Method Call | Subscribes to real-time safety condition streams. |
| **telemetry_listener** | **telemetry_bus** | In-Process Method Call | Publishes live sensor readings to the hot path bus. |
| **telemetry_listener** | **telemetry_repo** | C# Interface (DI) | Dispatches historical sensor readings to the cold path. |
| **telemetry_repo** | **telemetry_ef_adapter**| C# Class Inheritance | Implements time-series persistence via EF Core. |
| **telemetry_ef_adapter**| **db_postgres** | TCP/IP (SQL) | Executes optimized bulk inserts into TimescaleDB chunks. |
| **mobile_app** | **local_db** | SQLite P/Invoke | Persists transactional queue and master data for offline-first execution. |
| **loto_watchdog** | **local_db** | SQLite P/Invoke | Writes emergency lockout states directly to local storage upon connection loss. |
| **loto_watchdog** | **signalr_hub** | WSS (WebSockets) | Maintains continuous heartbeat to verify safety perimeter integrity. |
| **web_admin** | **api_controllers** | HTTPS / JSON | Executes administrative commands and fetches master data. |

---

## 4. Port, Interface, and Requirements Traceability Index

| Module / Port | C# Method Signature and Parameters | Requirement / US | Safety Invariant / Business Rule to Validate |
| :--- | :--- | :--- | :--- |
| **ITelemetryBus** | `IDisposable SubscribeToSafetyChannel(Guid equipmentUnitId, Action<TelemetryReading> onReading);` | [[VIS-011]]<br>TR-010-FR-431 | **Real-Time Synchronization:** Propagates permit revocations and energy spikes in sub-seconds. **Concurrency Control:** The client must apply a $300	ext{ ms}$ debounce on asset selection to prevent race conditions due to simultaneous multiple subscriptions. |
| **ITaxonomyService** | `Task InstallEquipment(Guid locationId, Guid equipmentId);` | [[INV-025]]<br>FR-593, FR-594 | Validates that the functional location has no installed asset (cardinality 1 slot = 1 L6 asset) and that the replacement equipment is in `IN_STORAGE` status (INV-025). |
| **ITaxonomyService** | `Task<EquipmentUnit> UninstallEquipment(Guid locationId, string reason);` | [[INV-025]]<br>FR-591, FR-592 | Unlinks the equipment from its operational position; updates its physical status to "In Repair" or "Stock" in a single-commit database transaction (NFR-596). |
| **ITaxonomyService** | `Task ReorganizeTree(Guid locationId, Guid newParentId);` | [[INV-027]]<br>FR-162, NFR-167 | Validates that the movement does not generate infinite cycles (a node cannot be its own ancestor, TR-008-FR-417) and remains within the boundaries of Functional Locations (L1 to L5 of the ISO 14224 taxonomy). |
| **IWorkOrderService** | `Task<Guid> CreateWorkRequest(CreateWorkRequestDto request);` | [[MTTO-026]]<br>FR-059 | Mandates the entry of the Work Class (`workClassCode`) and the asset identifier to admit the request into the backlog. |
| **IWorkOrderService** | `Task UpdatePriorityScore(Guid workRequestId);` | [[MTTO-026]]<br>FR-060, NFR-074 | Invokes `IRimeCalculator.Calculate(asset.Criticality, request.WorkClass)`; the calculation is deterministic and immutable to external inventory factors. |
| **IWorkOrderService** | `Task CalculateNextTriggerLimit(Guid planId, decimal currentUsage);` | [[MTTO-023]]<br>FR-583, FR-584 | Rejects telemetry readings lower than the historical accumulated (counters); maintains the last valid value and generates an alert for possible sensor tampering. |
| **IWorkOrderService** | `Task StartExecution(Guid workOrderId);` | [[VIS-011]]<br>NFR-229, NFR-238 | **FAIL-SAFE:** Blocks the transition if the associated permit is not `APPROVED` or if any `WorkOrderIsolation.isIsolated` is false. Blocks if there is telemetry loss. |
| **IWorkOrderService** | `Task CloseAdministratively(Guid workOrderId);` | [[MTTO-002]]<br>FR-012 | Validates the filling of ISO 14224 failure codes (`FailureRecord`) and actual spare parts consumption before marking the WO as `CLOSED`. |
| **IWorkOrderService** | `Task CompleteExecution(Guid workOrderId, decimal actualLaborHours);` | [[MTTO-002]]<br>FR-010 | **Technical Closure:** Transitions the WO status to `COMPLETE` and records the actual field labor time (*wrench time*) reported by the technician. |
| **IWorkOrderService** | `Task<Guid> PromoteToWorkOrderAsync(Guid workRequestId);` | Cross-cutting (WorkRequest) | **Backlog Admission:** Calculates the `RIME Score` via the `IRimeCalculator` service prior to creating the WO; rejects if `workClassCode` is not parameterized. |
| **IInventoryService** | `Task ReserveStock(Guid sparePartId, decimal quantity);` | [[INV-006]]<br>FR-126 | Decrements available virtual stock (`QuantityOnHand - ReservedQuantity`); rejects reservation if the resulting value is below zero. |
| **IInventoryService** | `Task RecordConsumption(Guid workOrderId, Guid sparePartId, decimal quantity);` | [[INV-006]]<br>FR-127 | Crosses parts consumption with `SparePart.IssueStock()`; atomically updates the WO maintenance cost table in the DB. |
| **IInventoryService** | `Task SwapAssetAsync(Guid locationId, Guid replacementId, Guid workOrderId);` | [[INV-025]]<br>FR-591 to FR-595 | **Asset Swap:** Atomically unlinks the damaged asset from its functional location, updates its status to "In Repair" or "Stock", and installs the replacement unit (NFR-596). |
| **ILotoService** | `Task RequireIsolation(Guid workOrderId, Guid isolationPointId);` | [[VIS-011]]<br>FR-228, FR-230 | Inserts the tuple into the intermediate `work_order_isolations` table; prevents authorizing general isolation if checklist items remain unconfirmed. |
| **ILotoService** | `Task EvaluateEnergyState(Guid isolationPointId, decimal telemetryValue);` | [[VIS-011]]<br>NFR-229, NFR-237 | If the sensor reading value exceeds the safe Zero Energy limits, forces danger state; physical lockout cannot be bypassed from the technician's UI. |
| **ILotoService** | `Task ConfirmZeroEnergyAsync(Guid workOrderId);` | [[VIS-011]]<br>FR-230, NFR-233 | **Active Lockout:** Enables Zero Energy confirmation only when port telemetry confirms there is no active flow at the isolation points; latency <1s. |
| **ISecurityService** | `Task<AuthToken> Authenticate(string username, string password);` | TR-006-FR-394 | Generates an immutable JWT token with a maximum validity of 8 hours; increments the login failure counter in `User` if the password does not match. |
| **ISecurityService** | `Task AppendAuditEntry(string entityType, string entityId, string action, object previous, object next);` | [[ADM-032]]<br>FR-346, [[TR-001]] | Persists in PostgreSQL JSONB format via an asynchronous interceptor; the destination table denies `UPDATE`/`DELETE` commands at the SQL engine level. |
| **ISecurityService** | `Task<bool> VerifyAuditIntegrity(Guid logId);` | [[ADM-032]]<br>FR-351 | Recalculates the cryptographically chained SHA-256 hash with the previous record and validates the match; immediately notifies HSEQ if there is a discrepancy. |
| **ISecurityService** | `Task<bool> AuthorizeAsync(Guid userId, string module, string action);` | TR-006-FR-396<br>TR-006-NFR-401 | **RBAC Security:** Evaluates the assigned role's permission matrix in <5ms latency; records access denials as suspicious events in `audit_logs` (TR-006-FR-397). |
| **IEquipmentRepository** | `Task<IReadOnlyList<FunctionalLocation>> GetHierarchyPathAsync(Guid assetId);` | [[TR-008]], FR-416 | **Taxonomic Consistency:** Must guarantee an uninterrupted hierarchical path from Level 1 to the queried asset; with a load response in <500ms (TR-008-NFR-419). |
| **ISecurityRepository** | `Task<IReadOnlyList<AuthToken>> GetActiveSessionsAsync(Guid userId);` | TR-006-NFR-402 | **Access Revocation:** Allows querying and immediately invalidating active sessions (burning JWT tokens) when a user's status changes to inactive due to risk. |
| **IWorkOrderRepository** | `Task SaveWithHistoryAsync(WorkOrder workOrder, string oldStatus);` | Cross-cutting (`WorkOrderHistory`) | **Traceability:** Each state transition must atomically generate a row in the `work_order_histories` history table in a single-commit database transaction. |
| **IInventoryRepository** | `Task<StockSnapshot> GetAvailabilityAsync(Guid sparePartId);` | TR-008 (connected structural consistency) | **Warehouse Integrity:** Returns the physical inventory (`QuantityOnHand`) and committed (`ReservedQuantity`) without dirty reads, ensuring transactional consistency. |
