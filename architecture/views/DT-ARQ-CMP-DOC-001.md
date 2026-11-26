---
code: DT-ARQ-CMP-DOC-001
version: 1.6
date: 2026-11-07
status: Approved
author: Juan David Julio
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

This document constitutes the detailed design specification (C4 Level 3) that complements the component diagram (`DT-ARQ-CMP-001-component-model.dsl`). Its purpose is to serve as the single source of truth (SSoT) for the development team, translating the boundaries and functional ports of the diagram into physical C# (.NET 10) code interfaces and PostgreSQL relational storage schemas.

The specification is strictly limited to the scope of the **Minimum Viable Product (MVP)**, consolidating the logic of immutable logs without collisions, automatic backlog prioritization based on the RIME industrial standard, reactive telemetry synchronization for safety, and physical inventory control for Asset Swaps.

---

## 2. Component and Port Specification Matrix

| Component ID | Component or Functional Port | Architectural Layer / Stereotype | Port / Interface | Technical Responsibility |
| :--- | :--- | :--- | :--- | :--- |
| **mobile_app** | Mobile App | Client Application | .NET MAUI Blazor | Offline-first field client for touch execution. |
| **local_db** | SQLite Offline DB | Persistence | sqlite-net-pcl | Offline-first relational store (SQLCipher encrypted). |
| **loto_watchdog** | LOTO Safety Watchdog | Component | C# Background Service | Real-time verification of Zero Energy thresholds on the mobile client. |
| **object_storage** | Azure Blob Storage | External System | Storage Account | Binary evidence persistence for ISO 14224 photographs. |
| **web_admin** | Web Admin Portal | Client Application | Blazor Web App | HSEQ supervision, planning, and dashboards. |
| **idempotency_filter** | Idempotency Filter | Driving Adapter | IEndpointFilter | Intercepts Minimal API mutating requests with the canonical `X-Idempotency-Key` header; prevents reprocessing critical transitions resent after reconnection (TR-007, ADR-007). |
| **idempotency_repo** | Idempotency Repository | Secondary Port (Out) | IIdempotencyRepository | Abstracts relational persistence of the IdempotencyLog to join the Domain's Unit of Work (ADR-007). |
| **media_repo** | Media Repository | Secondary Port (Out) | IMediaRepository | Manages SAS token issuance for external evidence storage (ADR-008). |
| **api_controllers** | REST API Controllers | Driving Adapter | Minimal APIs | Exposes HTTPS `/api/v1/...` endpoints; enforces optimistic concurrency control using PostgreSQL `xmin` mapped to EF Core `ConcurrencyToken` (`ETag` / `If-Match`, `DT-ARQ-DB-DOC-001 §3.12`). |
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
| **inv_port** | **asset_repo** | C# Interface (DI) | Coordinates taxonomic slot uninstallation/installation during atomic rotable swaps. |
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
| **idempotency_filter** | **idempotency_repo** | In-Process Method Call | Delegates durable logging (Stage 2) into the domain transaction. |
| **idempotency_repo** | **db_postgres** | TCP/IP (SQL) | Executes ACID transaction inserting the IdempotencyLog record. |
| **mobile_app** | **object_storage** | HTTPS / REST | Uploads binary failure evidence directly via Valet Key (pre-signed SAS token). |
| **mtto_port** | **media_repo** | In-Process Method Call | Requests SAS tokens for multimedia persistence. |
| **media_repo** | **object_storage** | HTTPS / Azure SDK | Authenticates via Managed Identity to generate and issue SAS tokens. |
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
| **ITelemetryBus** | `IDisposable SubscribeToSafetyChannel(Guid equipmentUnitId, Action<TelemetryReading> onReading);` | [VIS-011](../../requirements/user-stories/vis/VIS-011.md)<br>[TR-010-NFR-431](../../requirements/common/TR-010.md#non-functional-requirements-nfr) | **Real-Time Synchronization:** Propagates permit revocations and energy spikes in sub-seconds. **Concurrency Control:** The client must apply a $300\text{ ms}$ debounce on asset selection to prevent race conditions due to simultaneous multiple subscriptions. |
| **ITaxonomyService** | `Task<Guid> RegisterEquipmentAsync(RegisterEquipmentCommand command);` | [INV-005](../../requirements/user-stories/inv/INV-005.md)<br>[FR-119](../../requirements/user-stories/inv/INV-005.md#functional-requirements-fr) | Validates chronological milestone coherence (`ValidateChronology`) and ISO 14224 L6-L8 taxonomic placement before persisting a new serialized `EquipmentUnit`. |
| **ITaxonomyService** | `Task ActivateEquipmentAsync(Guid equipmentUnitId);` | [INV-007](../../requirements/user-stories/inv/INV-007.md)<br>[FR-139](../../requirements/user-stories/inv/INV-007.md#functional-requirements-fr), [FR-140](../../requirements/user-stories/inv/INV-007.md#functional-requirements-fr) | **Commissioning Gate:** Validates mandatory physical boundaries (`boundary_start`, `boundary_end`) and mapped LOTO isolation points before transitioning `lifecycle_status` from `COMMISSIONING` to `INSTALLED`. |
| **ITaxonomyService** | `Task ReorganizeTree(Guid locationId, Guid newParentId);` | [INV-027](../../requirements/user-stories/inv/INV-027.md)<br>[FR-162](../../requirements/user-stories/inv/INV-027.md#functional-requirements-fr), [NFR-167](../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr) | Validates that the movement does not generate infinite cycles (a node cannot be its own ancestor, [TR-008-NFR-417](../../requirements/common/TR-008.md#non-functional-requirements-nfr)) and remains within the boundaries of Functional Locations (L1 to L5 of the ISO 14224 taxonomy). |
| **IWorkOrderService** | `Task<Guid> CreateWorkRequest(CreateWorkRequestDto request);` | [MTTO-026](../../requirements/user-stories/mtto/MTTO-026.md)<br>[FR-059](../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | Mandates the entry of the Work Class (`workClassCode`) and the asset identifier to admit the request into the backlog. |
| **IWorkOrderService** | `Task UpdatePriorityScore(Guid workRequestId);` | [MTTO-026](../../requirements/user-stories/mtto/MTTO-026.md)<br>[FR-060](../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr), [NFR-074](../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr) | Invokes `IRimeCalculator.Calculate(functionalLocation.Criticality, workRequest.WorkClassCode)`; the calculation is deterministic and immutable to external inventory factors. |
| **IWorkOrderService** | `Task CalculateNextTriggerLimit(Guid planId, decimal currentUsage);` | [MTTO-023](../../requirements/user-stories/mtto/MTTO-023.md)<br>[FR-583](../../requirements/user-stories/mtto/MTTO-023.md#functional-requirements-fr), [FR-584](../../requirements/user-stories/mtto/MTTO-023.md#functional-requirements-fr) | Rejects telemetry readings lower than the historical accumulated (counters); maintains the last valid value and generates an alert for possible sensor tampering. |
| **IWorkOrderService** | `Task StartExecution(Guid workOrderId);` | [VIS-011](../../requirements/user-stories/vis/VIS-011.md)<br>[NFR-229](../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr), [NFR-238](../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | **FAIL-SAFE:** Blocks the transition if the associated permit is not `APPROVED` or if any `WorkOrderIsolation.isIsolated` is false. Blocks if there is telemetry loss. |
| **IWorkOrderService** | `Task CloseAdministratively(Guid workOrderId);` | [MTTO-002](../../requirements/user-stories/mtto/MTTO-002.md)<br>[FR-012](../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | Validates the filling of ISO 14224 failure codes (`FailureRecord`) and actual spare parts consumption before marking the WO as `CLOSED`. |
| **IWorkOrderService** | `Task CompleteExecution(Guid workOrderId, decimal actualLaborHours);` | [MTTO-002](../../requirements/user-stories/mtto/MTTO-002.md)<br>[FR-010](../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | **Technical Closure:** Transitions the WO status to `COMPLETE` and records the actual field labor time (*wrench time*) reported by the technician. |
| **IWorkOrderService** | `Task<Guid> PromoteToWorkOrderAsync(Guid workRequestId);` | Cross-cutting (WorkRequest) | **Backlog Admission:** Calculates the `RIME Score` via the `IRimeCalculator` service prior to creating the WO; rejects if `workClassCode` is not parameterized. |
| **IInventoryService** | `Task ReserveStock(Guid sparePartId, decimal quantity);` | [INV-006](../../requirements/user-stories/inv/INV-006.md)<br>[FR-126](../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr) | Decrements available virtual stock (`QuantityOnHand - ReservedQuantity`); rejects reservation if the resulting value is below zero. |
| **IInventoryService** | `Task RecordConsumption(Guid workOrderId, Guid sparePartId, decimal quantity);` | [INV-006](../../requirements/user-stories/inv/INV-006.md)<br>[FR-127](../../requirements/user-stories/inv/INV-006.md#functional-requirements-fr) | Crosses parts consumption with `SparePart.IssueStock()`; atomically updates the WO maintenance cost table in the DB. |
| **IInventoryService** | `Task<AssetSwapCompletedEvent> SwapAssetAsync(ExecuteAssetSwapCommand command);` | [INV-025](../../requirements/user-stories/inv/INV-025.md)<br>[FR-591 to FR-595](../../requirements/user-stories/inv/INV-025.md#functional-requirements-fr), [NFR-596](../../requirements/user-stories/inv/INV-025.md#non-functional-requirements-nfr) | **Atomic Asset Swap (Single Orchestrator):** Coordinates `FunctionalLocation.UninstallEquipment()`, `EquipmentUnit.TransitionToStorage/Repair/Damaged()`, and `FunctionalLocation.InstallEquipment()` across `TaxonomyDbContext`, `InventoryDbContext`, and `SecurityDbContext` over a single shared `DbTransaction` ([DT-ARQ-DB-DOC-001 §3.9](../DT-ARQ-DB-DOC-001.md#39-cross-dbcontext-atomic-transactions-idbcontexttransaction-sharing-tr-001-tr-005-inv-025)). |
| **ILotoService** | `Task RequireIsolation(Guid workOrderId, Guid isolationPointId);` | [VIS-011](../../requirements/user-stories/vis/VIS-011.md)<br>[FR-228](../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr), [FR-230](../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr) | Inserts the tuple into the intermediate `work_order_isolations` table; prevents authorizing general isolation if checklist items remain unconfirmed. |
| **ILotoService** | `Task EvaluateEnergyState(Guid isolationPointId, decimal telemetryValue);` | [VIS-011](../../requirements/user-stories/vis/VIS-011.md)<br>[NFR-229](../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr), [NFR-237](../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | If the sensor reading value exceeds the safe Zero Energy limits, forces danger state; physical lockout cannot be bypassed from the technician's UI. |
| **ILotoService** | `Task ConfirmZeroEnergyAsync(Guid workOrderId);` | [VIS-011](../../requirements/user-stories/vis/VIS-011.md)<br>[FR-230](../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr), [NFR-233](../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | **Active Lockout:** Enables Zero Energy confirmation only when port telemetry confirms there is no active flow at the isolation points; latency <1s. |
| **ISecurityService** | `Task<AuthToken> Authenticate(string username, string password);` | [TR-006-NFR-394](../../requirements/common/TR-006.md#non-functional-requirements-nfr) | Issues a short-lived Access JWT (15-minute TTL) paired with a rotating Session Refresh Token (maximum 8-hour shift validity stored in `adm.auth_tokens`); increments the login failure counter in `User` if the password does not match. |
| **ISecurityService** | `Task AppendAuditEntry(string entityType, Guid entityId, AuditActionType action, object? previous, object? next);` | [ADM-032](../../requirements/user-stories/adm/ADM-032.md)<br>[FR-346](../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [TR-001](../../requirements/common/TR-001.md) | Persists in PostgreSQL `JSONB` format conforming to [DT-ERD-DOC-001 §6.7](../../domain-models/entity-relationship/DT-ERD-DOC-001.md#67-admaudit_logsprevious_state-and-new_state) synchronously inside the active shared `DbTransaction` via `AuditSaveChangesInterceptor` pre-commit ([DT-ARQ-DB-DOC-001 §3.9](../DT-ARQ-DB-DOC-001.md#39-cross-dbcontext-atomic-transactions-idbcontexttransaction-sharing-tr-001-tr-005-inv-025)); the destination table denies `UPDATE`/`DELETE` commands at the SQL engine level. |
| **ISecurityService** | `Task<bool> VerifyAuditIntegrity(Guid logId);` | [ADM-032](../../requirements/user-stories/adm/ADM-032.md)<br>[FR-351](../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr) | Recalculates the cryptographically chained SHA-256 hash with the previous record and validates the match; immediately notifies HSEQ if there is a discrepancy. |
| **ISecurityService** | `Task<bool> AuthorizeAsync(Guid userId, string module, string action);` | [TR-006-NFR-396](../../requirements/common/TR-006.md#non-functional-requirements-nfr)<br>[TR-006-NFR-401](../../requirements/common/TR-006.md#non-functional-requirements-nfr) | **RBAC Security:** Evaluates the assigned role's permission matrix in <5ms latency; records access denials as suspicious events in `audit_logs` ([TR-006-NFR-397](../../requirements/common/TR-006.md#non-functional-requirements-nfr)). |
| **IEquipmentRepository** | `Task<IReadOnlyList<FunctionalLocation>> GetHierarchyPathAsync(Guid assetId);` | [TR-008](../../requirements/common/TR-008.md), [TR-008-FR-416](../../requirements/common/TR-008.md#functional-requirements-fr) | **Taxonomic Consistency:** Must guarantee an uninterrupted hierarchical path from Level 1 to the queried asset; with a load response in <500ms (TR-008-NFR-419). |
| **ISecurityRepository** | `Task<IReadOnlyList<AuthToken>> GetActiveSessionsAsync(Guid userId);` | [TR-006-NFR-402](../../requirements/common/TR-006.md#non-functional-requirements-nfr) | **Access Revocation:** Allows querying and immediately invalidating active sessions (revoking refresh tokens and pushing `SessionRevoked` over `/hubs/security`) when a user's status changes to inactive due to risk. |
| **IWorkOrderRepository** | `Task SaveWithHistoryAsync(WorkOrder workOrder, string oldStatus);` | Cross-cutting (`WorkOrderHistory`) | **Traceability:** Each state transition must atomically generate a row in the `work_order_histories` history table in a single-commit database transaction. |
| **IInventoryRepository** | `Task<StockSnapshot> GetAvailabilityAsync(Guid sparePartId);` | [TR-008](../../requirements/common/TR-008.md) (connected structural consistency) | **Warehouse Integrity:** Returns the physical inventory (`QuantityOnHand`) and committed (`ReservedQuantity`) without dirty reads, ensuring transactional consistency. |

---

## 5. SignalR Hub and Real-Time Event Contract Registry (`TR-010`)

To prevent event-name drift across Blazor Web App and .NET MAUI Blazor Hybrid clients, all server-to-client WebSocket broadcasts via `signalr_broadcaster` MUST bind strictly to the three canonical SignalR hubs and strongly typed client contracts below:

| Hub Endpoint | Typed Client Interface | Canonical Server-to-Client Event Signature | Producers | Authorized Subscribers & Consuming Screens |
| :--- | :--- | :--- | :--- | :--- |
| **`/hubs/telemetry`** | `ITelemetryClient` | `ReceiveTelemetryReading(TelemetryReadingDto reading)` | `telemetry_listener` (Azure IoT Hub / SCADA), `SCR-MTTO-023` (manual readings) | `SCR-VIS-033`, `SCR-VIS-011`, `SCR-MTTO-023` (live sensor updates & Zero Energy monitoring). |
| **`/hubs/telemetry`** | `ITelemetryClient` | `EmergencyEvacuationBroadcast(EvacuationAlertDto alert)` | `telemetry_listener`, `loto_port`, `SCR-VIS-011` (Zero Energy breach / fail-safe interrupt) | `SCR-VIS-008`, `SCR-VIS-011`, `SCR-VIS-033`, `SCR-MTTO-002` (plant-wide red priority alert & fail-safe interrupt). |
| **`/hubs/telemetry`** | `ITelemetryClient` | `CbmReadingRecorded(CbmTriggerEventDto triggerEvent)` | `telemetry_listener`, `mtto_port`, `SCR-MTTO-023` (CBM counter ingestion) | `SCR-MTTO-023` (live condition-based trigger recalculation & counter tamper alerts). |
| **`/hubs/telemetry`** | `ITelemetryClient` | `LotoHeartbeatAck(DateTimeOffset utcTimestamp)` | `signalr_hub`, `loto_port` (watchdog heartbeat ack) | `SCR-VIS-011`, `SCR-MTTO-002`, `loto_watchdog` (2-second cadence; 30-second Grace Window before fail-safe lockout). |
| **`/hubs/security`** | `ISecuritySessionClient` | `PermissionsUpdated(RolePermissionsUpdatedEvent evt)` | `SCR-ADM-013` (role matrix), `SCR-ADM-014` (user role assignments) | `SCR-ADM-013`, `SCR-ADM-014`, all authenticated Blazor sessions (real-time RBAC matrix cache refresh). |
| **`/hubs/security`** | `ISecuritySessionClient` | `SessionRevoked(SessionRevocationEvent evt)` | `SCR-ADM-013` (role deactivation), `SCR-ADM-014` (user suspension / token revocation) | `SCR-ADM-014`, all active sessions for revoked/locked user (immediate forced logout & local cache wipe). |
| **`/hubs/operations`** | `IOperationsClient` | `PermitStatusChanged(WorkPermitStatusEvent evt)` | `loto_port`, `SCR-VIS-008`, `SCR-VIS-011` (PTW lifecycle transitions) | `SCR-VIS-008`, `SCR-VIS-011` (unified PTW lifecycle transitions: `APPROVED`, `REVOKED`, `CLOSED`, `EXPIRING_SOON`). |
| **`/hubs/operations`** | `IOperationsClient` | `WorkOrderStatusChanged(WorkOrderTransitionEvent evt)` | `SCR-MTTO-001`, `SCR-MTTO-023`, `SCR-MTTO-026`, `SCR-VIS-011`, `SCR-MTTO-002` | `SCR-MTTO-026`, `SCR-MTTO-002`, `SCR-VIS-011`, `SCR-VIS-033` (RIME backlog board refresh and work-order FSM sync). |
| **`/hubs/operations`** | `IOperationsClient` | `AssetSwapCompleted(AssetSwapCompletedEvent evt)` | `SCR-INV-025` (`IInventoryService.SwapAssetAsync`) | `SCR-INV-025`, `SCR-INV-005`, `SCR-VIS-033` (rotable slot re-mount notification across connected viewports). |

### 5.1. Canonical SignalR Event Payload Contracts

The 8 typed SignalR event records (`LotoHeartbeatAck` emits a scalar `DateTimeOffset utcTimestamp`) expose the following canonical fields:

| Event Record | Canonical Payload Fields |
| :--- | :--- |
| **`TelemetryReadingDto`** | `SignalId` (`Guid`), `EquipmentUnitId` (`Guid`), `SignalType` (`TelemetrySignalType`), `Value` (`decimal`), `Unit` (`string`), `Threshold` (`decimal?`), `IsSafetyCritical` (`bool`), `TimestampUtc` (`DateTimeOffset`). |
| **`EvacuationAlertDto`** | `AlertId` (`Guid`), `EquipmentUnitId` (`Guid`), `FunctionalLocationTag` (`string`), `WorkOrderId` (`Guid?`), `SignalType` (`TelemetrySignalType`), `MeasuredValue` (`decimal`), `ThresholdValue` (`decimal`), `EngineeringUnit` (`string`), `Reason` (`string`), `TriggeredAtUtc` (`DateTimeOffset`). |
| **`CbmTriggerEventDto`** | `MaintenancePlanId` (`Guid`), `EquipmentUnitId` (`Guid`), `SignalType` (`TelemetrySignalType`), `ReadingValue` (`decimal`), `NextTriggerLimit` (`decimal?`), `IsMonotonicityViolation` (`bool`), `TriggeredWorkOrderId` (`Guid?`), `RecordedAtUtc` (`DateTimeOffset`). |
| **`RolePermissionsUpdatedEvent`** | `RoleId` (`Guid`), `RoleName` (`string`), `AffectedUserIds` (`IReadOnlyList<Guid>`), `UpdatedByUserId` (`Guid`), `UpdatedAtUtc` (`DateTimeOffset`). |
| **`SessionRevocationEvent`** | `TargetUserId` (`Guid`), `RevokedTokenId` (`Guid?`), `Reason` (`string`), `RevokedByUserId` (`Guid`), `RevokedAtUtc` (`DateTimeOffset`). |
| **`WorkPermitStatusEvent`** | `WorkPermitId` (`Guid`), `PermitIdentifier` (`string`), `EquipmentUnitId` (`Guid`), `PreviousStatus` (`WorkPermitStatus`), `NewStatus` (`WorkPermitStatus`), `IsExpiringSoon` (`bool`), `OccurredAtUtc` (`DateTimeOffset`). |
| **`WorkOrderTransitionEvent`** | `WorkOrderId` (`Guid`), `WorkOrderNumber` (`string`), `EquipmentUnitId` (`Guid`), `OldStatus` (`WorkOrderStatus`), `NewStatus` (`WorkOrderStatus`), `TriggeredByUserId` (`Guid`), `OccurredAtUtc` (`DateTimeOffset`). |
| **`AssetSwapCompletedEvent`** | `InstallationId` (`Guid`), `FunctionalLocationTag` (`string`), `DismountedSerialNumber` (`string`), `InstalledSerialNumber` (`string`), `CryptographicHash` (`string`), `Timestamp` (`DateTimeOffset`). |

---

## 6. REST API Prefix, Concurrency & Numeric Precision Conventions

1. **Bounded-Context REST Prefixes:** All HTTPS endpoints exposed by `api_controllers` follow the canonical prefix `/api/v1/{context}/...` mapped cleanly by domain bounded context:
   * `/api/v1/taxonomy/...` — ISO 14224 Functional Locations, Equipment Units, Commissioning Gate, Boundaries, Subunits (`SCR-INV-005`, `SCR-INV-027`, `SCR-MTTO-029`, `SCR-MTTO-001`, `SCR-MTTO-023`).
   * `/api/v1/maintenance/...` — Maintenance Plans (Time-Based & CBM), Work Requests, RIME Backlog, Work Orders (`SCR-MTTO-001`, `SCR-MTTO-002`, `SCR-MTTO-023`, `SCR-MTTO-026`, `SCR-VIS-011`, `SCR-VIS-033`).
   * `/api/v1/inventory/...` — Spare Parts Catalog, Inventory Movements / Kardex, Atomic Rotable Swaps (`SCR-INV-006`, `SCR-INV-025`, `SCR-INV-031`).
   * `/api/v1/safety/...` — Work Permits (PTW) and LOTO Isolation Plans / Try-Out Verification (`SCR-VIS-008`, `SCR-VIS-011`).
   * `/api/v1/visualization/...` — 2D Plot Plan SVG revisions, Mesh Mappings, and Spatial Faceplate projections (`SCR-VIS-008`, `SCR-VIS-033`).
   * `/api/v1/telemetry/...` — Telemetry Signal lookups and Manual Counter Readings (`SCR-MTTO-023`; SignalR-only for `SCR-VIS-033`).
   * `/api/v1/security/...` — RBAC Roles, User Lifecycle, Active Sessions, and WORM Audit Logs (`SCR-ADM-013`, `SCR-ADM-014`, `SCR-ADM-032`).
2. **Idempotency & Optimistic Concurrency Headers:** Every mutating `POST`/`PUT`/`PATCH`/`DELETE` command MUST include `X-Idempotency-Key` (`ADR-007`), whereas read-only query/validation `POST` routes (such as `POST /api/v1/taxonomy/maintainable-items/validate-exclusivity` and `POST /api/v1/security/audit-logs/query`) are exempt from `idempotency_filter`. Every update or state-transition on a mutable entity MUST enforce PostgreSQL `xmin` optimistic concurrency via `ETag` / `If-Match` headers and `uint ConcurrencyToken` (`DT-ARQ-DB-DOC-001 §3.12`).
3. **Numeric Precision Boundary:** All domain, telemetry, engineering, financial, and inventory quantities MUST use C# `decimal` (mapped to PostgreSQL `DECIMAL`). IEEE-754 `double` is strictly permitted only in non-persisted 2D/3D SVG presentation viewport DTOs/view-models (`SCR-VIS-008`, `SCR-VIS-011`, `SCR-VIS-033`) for screen pan/zoom transforms, pixel coordinates, and cartographic scale factors (`DT-ARQ-DB-DOC-001 §2`).

### 6.1. Canonical REST Endpoint Catalog

The catalog below consolidates all **72 normalized Minimal API endpoints** (**74 verbatim `VERB /api/v1/...` route references** across the 16 `SCR-*.md` screen contracts, accounting for the optional `?from={isoDate}&to={isoDate}` query parameters on `commissioning-report` and the `?serial={sn}` / `?serial={serialNumber}` parameter alias on `verify-uniqueness`) grouped by bounded context:

#### 6.1.1. `taxonomy` Context (21 Normalized / 23 Verbatim Routes)

| Method + Route | Command / Response DTO | Idempotency / Concurrency | Consuming Screens |
| :--- | :--- | :--- | :--- |
| `POST /api/v1/taxonomy/functional-locations` | `CreateFunctionalLocationCommand` $\to$ `FunctionalLocationCreatedEvent` | `X-Idempotency-Key` | `SCR-INV-027` |
| `GET /api/v1/taxonomy/functional-locations/tree` | `FunctionalLocationTreeResponseDto` | Read-only (`GET`) | `SCR-INV-027` |
| `GET /api/v1/taxonomy/functional-locations/verify-tag?tag={tag}` | `TagUniquenessResultDto` | Read-only (`GET`) | `SCR-INV-027` |
| `PUT /api/v1/taxonomy/functional-locations/{id}` | `UpdateFunctionalLocationCommand` $\to$ `FunctionalLocationTreeNodeDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-INV-027` |
| `PATCH /api/v1/taxonomy/functional-locations/{id}/reorganize` | `ReorganizeFunctionalLocationCommand` $\to$ `FunctionalLocationTreeNodeDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-INV-027` |
| `DELETE /api/v1/taxonomy/functional-locations/{id}` | `TaxonomyAuditEntryDto` / `204 No Content` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-INV-027` |
| `GET /api/v1/taxonomy/functional-locations/export` | `TaxonomyExportFormat` (`CSV` / `JSON` stream) | Read-only (`GET`) | `SCR-INV-027` |
| `GET /api/v1/taxonomy/functional-locations/{locId}/installed-asset` | `InstalledAssetDetailsDto` | Read-only (`GET`) | `SCR-INV-025` |
| `POST /api/v1/taxonomy/equipment-units` | `RegisterEquipmentUnitCommand` $\to$ `EquipmentUnitMasterCardDto` | `X-Idempotency-Key` | `SCR-INV-005` |
| `GET /api/v1/taxonomy/equipment-units/{id}` | `EquipmentUnitMasterCardDto` | Read-only (`GET`) | `SCR-INV-005` |
| `PUT /api/v1/taxonomy/equipment-units/{id}` | `UpdateEquipmentMasterRecordCommand` $\to$ `EquipmentUnitMasterCardDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-INV-005` |
| `GET /api/v1/taxonomy/equipment-units/lookup` | `EquipmentUnitLookupQueryDto` $\to$ `PagedLookupResultDto<EquipmentUnitLookupDto>` | Read-only (`GET`) | `SCR-MTTO-001`, `SCR-MTTO-023`, `SCR-MTTO-029` |
| `GET /api/v1/taxonomy/equipment-units/verify-uniqueness?serial={serialNumber}` (alias `?serial={sn}`) | `SerialUniquenessResultDto` | Read-only (`GET`) | `SCR-INV-005` |
| `GET /api/v1/taxonomy/equipment-units/pending-commissioning` | `IReadOnlyList<PendingCommissioningItemDto>` | Read-only (`GET`) | `SCR-INV-005` |
| `POST /api/v1/taxonomy/equipment-units/{id}/commission` | `CommissionEquipmentUnitCommand` $\to$ `EquipmentUnitMasterCardDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-INV-005` |
| `POST /api/v1/taxonomy/equipment-units/{id}/reject-commissioning` | `RejectEquipmentCommissioningCommand` $\to$ `EquipmentUnitMasterCardDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-INV-005` |
| `GET /api/v1/taxonomy/equipment-units/commissioning-report` (`?from={isoDate}&to={isoDate}`) | Structured `CSV` / `JSON` compliance report | Read-only (`GET`) | `SCR-INV-005` |
| `GET /api/v1/taxonomy/equipment-units/{id}/boundaries` | `EquipmentBoundaryCardDto` | Read-only (`GET`) | `SCR-MTTO-001`, `SCR-MTTO-023`, `SCR-MTTO-029` |
| `PUT /api/v1/taxonomy/equipment-units/{id}/boundaries` | `SaveEquipmentBoundariesCommand` $\to$ `EquipmentBoundaryCardDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-MTTO-029` |
| `GET /api/v1/taxonomy/equipment-units/{id}/subunits` | `IReadOnlyList<SubunitLookupDto>` / `SubunitNodeDto` | Read-only (`GET`) | `SCR-MTTO-001`, `SCR-MTTO-023` |
| `POST /api/v1/taxonomy/maintainable-items/validate-exclusivity` | `MaintainableItemLookupQueryDto` $\to$ `ComponentExclusivityValidationResultDto` | Exempt (`POST` read-only validation) | `SCR-MTTO-029` |

#### 6.1.2. `maintenance` Context (13 Routes)

| Method + Route | Command / Response DTO | Idempotency / Concurrency | Consuming Screens |
| :--- | :--- | :--- | :--- |
| `POST /api/v1/maintenance/plans` | `CreateMaintenancePlanCommand` $\to$ `MaintenancePlanSummaryDto` | `X-Idempotency-Key` | `SCR-MTTO-001` |
| `PUT /api/v1/maintenance/plans/{id}` | `UpdateMaintenancePlanCommand` $\to$ `MaintenancePlanSummaryDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-MTTO-001` |
| `POST /api/v1/maintenance/plans/cbm` | `CreateCbmPlanCommand` $\to$ `CbmTriggerEventDto` | `X-Idempotency-Key` | `SCR-MTTO-023` |
| `GET /api/v1/maintenance/backlog-items?status=NEW` | `IReadOnlyList<BacklogItemDto>` (`BacklogSummaryMetricsDto`) | Read-only (`GET`) | `SCR-MTTO-026` |
| `POST /api/v1/maintenance/backlog-items/{id}/adjust-work-class` | `AdjustWorkClassCommand` $\to$ `BacklogItemDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-MTTO-026` |
| `POST /api/v1/maintenance/backlog-items/{id}/notify-reliability` | `DispatchReliabilityNotificationCommand` | `X-Idempotency-Key` | `SCR-MTTO-026` |
| `POST /api/v1/maintenance/backlog-items/weekly-distribution` | `ConfirmWeeklyDistributionCommand` | `X-Idempotency-Key` | `SCR-MTTO-026` |
| `GET /api/v1/maintenance/backlog-items/export` | `BacklogExportFormat` (`CSV` / `JSON` stream) | Read-only (`GET`) | `SCR-MTTO-026` |
| `GET /api/v1/maintenance/work-orders?equipmentUnitId={id}&status=ACTIVE` | `IReadOnlyList<ActiveWorkOrderSummaryDto>` | Read-only (`GET`) | `SCR-VIS-033` |
| `GET /api/v1/maintenance/work-orders/{id}/closing-context` | `WorkOrderClosingContextDto` | Read-only (`GET`) | `SCR-MTTO-002` |
| `POST /api/v1/maintenance/work-orders/{id}/start-execution` | `StartWorkOrderExecutionCommand` $\to$ `WorkOrderTransitionEvent` | `X-Idempotency-Key` + `SELECT ... FOR UPDATE NOWAIT` (online) / `CryptographicOfflineLeaseDto` (offline) | `SCR-VIS-011`, `SCR-MTTO-002` |
| `POST /api/v1/maintenance/work-orders/{id}/media-upload-sas` | `RequestMediaUploadSasCommand` $\to$ `MediaUploadSasResponseDto` | Valet Key SAS issuance ([ADR-008](../adr/ADR-008.md)) | `SCR-MTTO-002` |
| `POST /api/v1/maintenance/work-orders/{id}/technical-closure` | `SubmitTechnicalClosureCommand` $\to$ `WorkOrderTransitionEvent` | `X-Idempotency-Key` + `If-Match` (`xmin` online; omitted on offline FIFO replay per [ADR-006](../adr/ADR-006.md)) | `SCR-MTTO-002` |

#### 6.1.3. `inventory` Context (9 Routes)

| Method + Route | Command / Response DTO | Idempotency / Concurrency | Consuming Screens |
| :--- | :--- | :--- | :--- |
| `GET /api/v1/inventory/spare-parts?page=1&pageSize=100` | `IReadOnlyList<SparePartMasterItemDto>` (`PartMasterSummaryMetricsDto`) | Read-only (`GET`) | `SCR-INV-031` |
| `GET /api/v1/inventory/spare-parts/verify-sku?sku={sku}` | `SkuUniquenessResultDto` | Read-only (`GET`) | `SCR-INV-031` |
| `POST /api/v1/inventory/spare-parts` | `RegisterSparePartCommand` $\to$ `SparePartMasterItemDto` | `X-Idempotency-Key` | `SCR-INV-031` |
| `PUT /api/v1/inventory/spare-parts/{id}/policy` | `UpdateSparePartPolicyCommand` $\to$ `SparePartMasterItemDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-INV-031` |
| `GET /api/v1/inventory/spare-parts/rotables` | `IReadOnlyList<RotableSpareSummaryDto>` | Read-only (`GET`) | `SCR-INV-025` |
| `GET /api/v1/inventory/spare-parts/{id}/availability?warehouseId={wh}` | `SparePartAvailabilityDto` | Read-only (`GET`) | `SCR-INV-006` |
| `GET /api/v1/inventory/kardex?equipmentUnitId={id}&sparePartId={partId}` | `KardexSummaryMetricsDto` + `IReadOnlyList<KardexTransactionRowDto>` | Read-only (`GET`) | `SCR-INV-006` |
| `POST /api/v1/inventory/transactions` | `RegisterInventoryTransactionCommand` $\to$ `InventoryTransactionVoucherDto` | `X-Idempotency-Key` + `If-Match` (`xmin` online; omitted on offline FIFO replay) | `SCR-INV-006` |
| `POST /api/v1/inventory/rotable-swaps` | `ExecuteAssetSwapCommand` $\to$ `AssetSwapCompletedEvent` | `X-Idempotency-Key` + `If-Match` (`xmin` dual-unit online; omitted on offline replay) | `SCR-INV-025` |

#### 6.1.4. `safety` Context (7 Routes)

| Method + Route | Command / Response DTO | Idempotency / Concurrency | Consuming Screens |
| :--- | :--- | :--- | :--- |
| `GET /api/v1/safety/work-permits?status=APPROVED` | `IReadOnlyList<PtwOverlayDto>` | Read-only (`GET`) | `SCR-VIS-008` |
| `GET /api/v1/safety/work-permits/orphans` | `IReadOnlyList<OrphanPermitDto>` | Read-only (`GET`) | `SCR-VIS-008` |
| `GET /api/v1/safety/loto-plans/work-orders/{workOrderId}` | `LotoIsolationPlanDto` | Read-only (`GET`) | `SCR-VIS-011` |
| `POST /api/v1/safety/loto-plans/{workOrderId}/offline-lease` | `CryptographicOfflineLeaseDto` | `X-Idempotency-Key` | `SCR-VIS-011` |
| `POST /api/v1/safety/loto-plans/{workOrderId}/cutoffs/{isolationPointId}/confirm` | `ConfirmCutoffStepRequestDto` $\to$ `CutoffPointStatusDto` | `X-Idempotency-Key` + `SELECT ... FOR UPDATE NOWAIT` (online) / `CryptographicOfflineLeaseDto` (offline) | `SCR-VIS-011` |
| `POST /api/v1/safety/loto-plans/{workOrderId}/try-out` | `TryOutAttestationDto` $\to$ `LotoIsolationPlanDto` | `X-Idempotency-Key` + `SELECT ... FOR UPDATE NOWAIT` (online) / `CryptographicOfflineLeaseDto` (offline) | `SCR-VIS-011` |
| `POST /api/v1/safety/loto-plans/{workOrderId}/supervisor-override` | `SupervisorLotoOverrideCommand` $\to$ `LotoIsolationPlanDto` | `X-Idempotency-Key` | `SCR-VIS-011` |

#### 6.1.5. `visualization` Context (4 Routes)

| Method + Route | Command / Response DTO | Idempotency / Concurrency | Consuming Screens |
| :--- | :--- | :--- | :--- |
| `GET /api/v1/visualization/plot-plans/{facilityCode}` | `PlantPlotPlanDto` | Read-only (`GET`) | `SCR-VIS-008` |
| `GET /api/v1/visualization/plot-plans/{functionalLocationCode}` | `PlantPlotPlanDto` | Read-only (`GET`) | `SCR-VIS-033` |
| `GET /api/v1/visualization/equipment-units/{tagNumber}/faceplate` | `EquipmentFaceplateDto` | Read-only (`GET`) | `SCR-VIS-033` |
| `PUT /api/v1/visualization/mesh-mappings/{equipmentUnitId}` | `UpsertMeshMappingCommand` | `X-Idempotency-Key` + conditional `If-Match` (`xmin` on update; omitted on create) | `SCR-VIS-008` |

#### 6.1.6. `telemetry` Context (2 Routes)

| Method + Route | Command / Response DTO | Idempotency / Concurrency | Consuming Screens |
| :--- | :--- | :--- | :--- |
| `GET /api/v1/telemetry/equipment-units/{id}/signals` | `IReadOnlyList<TelemetrySignalDto>` | Read-only (`GET`) | `SCR-MTTO-023` |
| `POST /api/v1/telemetry/signals/{id}/manual-readings` | `RecordManualReadingCommand` $\to$ `CbmTriggerEventDto` | `X-Idempotency-Key` (no `If-Match`; append-only hypertable) | `SCR-MTTO-023` |

#### 6.1.7. `security` Context (16 Routes)

| Method + Route | Command / Response DTO | Idempotency / Concurrency | Consuming Screens |
| :--- | :--- | :--- | :--- |
| `GET /api/v1/security/roles/matrix` | `RoleMatrixDetailDto` + `RbacSummaryMetricsDto` | Read-only (`GET`) | `SCR-ADM-013` |
| `GET /api/v1/security/roles/export` | RBAC matrix & SoD export (`CSV` / `JSON`) | Read-only (`GET`) | `SCR-ADM-013` |
| `POST /api/v1/security/roles` | `CreateCustomRoleCommand` $\to$ `RoleSummaryDto` | `X-Idempotency-Key` | `SCR-ADM-013` |
| `PUT /api/v1/security/roles/{id}/permissions` | `UpdateRolePermissionsCommand` $\to$ `RoleMatrixDetailDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-ADM-013` |
| `POST /api/v1/security/roles/{id}/deactivate` | `DeactivateCustomRoleCommand` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-ADM-013` |
| `GET /api/v1/security/users` | `UserDirectoryMetricsDto` + `IReadOnlyList<UserDirectoryRowDto>` | Read-only (`GET`) | `SCR-ADM-014` |
| `GET /api/v1/security/users/verify-identity?username={u}&email={e}` | `IdentityUniquenessResultDto` | Read-only (`GET`) | `SCR-ADM-014` |
| `POST /api/v1/security/users` | `ProvisionUserAccountCommand` $\to$ `UserDetailProfileDto` | `X-Idempotency-Key` | `SCR-ADM-014` |
| `PUT /api/v1/security/users/{id}/roles` | `AssignUserRolesCommand` $\to$ `RoleUnionEvaluationDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-ADM-014` |
| `POST /api/v1/security/users/{id}/lifecycle` | `ExecuteUserLifecycleTransitionCommand` $\to$ `UserDetailProfileDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-ADM-014` |
| `POST /api/v1/security/users/{id}/password-reset` | `IssuePasswordResetCommand` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-ADM-014` |
| `POST /api/v1/security/users/{id}/tokens/revoke` | `RevokeUserTokensCommand` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-ADM-014` |
| `PUT /api/v1/security/password-policy` | `UpdatePasswordSecurityPolicyCommand` $\to$ `PasswordSecurityPolicyDto` | `X-Idempotency-Key` + `If-Match` (`xmin`) | `SCR-ADM-014` |
| `GET /api/v1/security/audit-logs` | `AuditLogWorkspaceDto` | Read-only (`GET`; logs `QUERY` Meta-Audit) | `SCR-ADM-032` |
| `POST /api/v1/security/audit-logs/query` | `AuditLogQueryFilterDto` $\to$ `IReadOnlyList<AuditLogEntryDto>` | Exempt (`POST` read-only GIN `@>` query; logs `QUERY` Meta-Audit) | `SCR-ADM-032` |
| `POST /api/v1/security/audit-logs/report-tamper-breach` | `ChainTamperBreachDetailsDto` | `X-Idempotency-Key` | `SCR-ADM-032` |
