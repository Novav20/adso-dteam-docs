---
code: DT-ARQ-DB-DOC-001
version: 1.1
date: 2026-11-07
status: Approved
author: Juan David Julio
standard:
  - ISO/IEC 42010:2011 (Software Architecture)
  - PostgreSQL 18.x Documentation
  - ISO 14224:2016 / ISO 55001:2014
---

# Technical Persistence Specification and SQL Guidelines

## 1. Scope and Purpose
This document consolidates the technical guidelines, physical constraints, and mandatory SQL query patterns for the PostgreSQL 18 engine in DTEAM. It acts as the persistence contract for the development of migrations in Entity Framework Core and DDL/DML scripts.

---

## 2. Physical Integrity Invariants and Constraints

| Rule / Element | Implementation Decision | Technical / Regulatory Justification                                                                                                                                                                                                                                                                           |
| :--- | :--- | :--- |
| **PK Identifiers** | `UUID DEFAULT uuidv7()` | Time-sequential identifiers that prevent B-Tree page fragmentation in massive telemetry and audit insertions.                                                                                                                                                                                                  |
| **FK Indexing** | Mandatory `CREATE INDEX` on each foreign key column. | PostgreSQL **does not** automatically index FKs in child tables. Prevents *Full Table Scans* during parent deletions or updates.                                                                                                                                                                               |
| **Asset Deletion** | `ON DELETE RESTRICT` on relations with `work_orders`. | **ISO 14224 / ISO 55001:** Strict prohibition of cascade deletion on work orders and failure history. Assets are logically retired (`Decommission`).                                                                                                                                                           |
| **Spares Management** | Keep standard `NULLS DISTINCT` behavior in `equipment_units.functional_location_id`. | Allows multiple equipment units in the warehouse (`IN_STORAGE`) to have a `NULL` value simultaneously without violating plant slot uniqueness.                                                                                                                                                                 |
| **Numerical Precision** | Strict `DECIMAL(18,6)` on sensors and `DECIMAL(12,2)` on costs. | Prohibition of `DOUBLE PRECISION` / `FLOAT` in all domain, telemetry, safety, financial, and inventory persistence/DTO contracts to avoid IEEE 754 rounding errors in deterministic Zero Energy (LOTO) validation. **Explicit UI Presentation Exception:** IEEE-754 `double` is strictly permitted solely in client-side 2D/3D SVG viewport presentation models (`SCR-VIS-008`, `SCR-VIS-011`, `SCR-VIS-033`) for screen-space pan/zoom transforms, pixel coordinates, and cartographic scale ratios that are never persisted as engineering measurements. |
| **DDD Schemas** | Segregation into 5 schemas: `tax`, `mtto`, `inv`, `vis`, `adm`. | Isolation by *Bounded Context*, removal of prefixes in tables, and support for defense in depth via `GRANT/REVOKE` privileges.                                                                                                                                                                                 |
| **Operational Indexing** | `CREATE INDEX ... WHERE ...` (Partial) | To optimize query performance on the Backlog Board and LOTO validations without saturating RAM, the use of **Partial Indexes** on active records is required. Records in terminal states (e.g., `CLOSED`, `COMPLETE`) are excluded from the active index B-Tree.                                               |
| **Controlled Vocabularies**| `CHECK (col IN (...))` in MVP with evolution path to *Lookup Tables*. | In the MVP, `CHECK` constraints mapped to C# `enum`s are used to maximize performance and avoid unnecessary JOINs. In later phases requiring dynamic parameterization from the UI (without code deployments), they will be migrated to dedicated catalog tables managed by Entity Framework Core (`SeedData`). |

## 3. DML Query and Performance Guidelines

### 3.1. `LEFT JOIN LATERAL` Pattern for Latest Telemetry ([VIS-033](../requirements/user-stories/vis/VIS-033.md))
To retrieve the latest sensor reading for each equipment without incurring costly aggregations (`MAX`) over massive time-series tables, canvas queries must use correlated `LATERAL` subqueries:

```sql
SELECT a.tag_number, tel.value AS current_vibration, tel.timestamp
FROM tax.equipment_units a
LEFT JOIN LATERAL (
    SELECT s.value, s.timestamp
    FROM vis.telemetry_signals s
    WHERE s.equipment_unit_id = a.id
    ORDER BY s.timestamp DESC
    LIMIT 1
) tel ON TRUE;
```

### 3.2. Conditional Aggregations with `FILTER` Clause ([MTTO-026](../requirements/user-stories/mtto/MTTO-026.md), [INV-006](../requirements/user-stories/inv/INV-006.md))
For consolidated metrics in a single table read, the use of `SUM(CASE ...)` is prohibited in favor of the standard `FILTER (WHERE ...)` clause:

```sql
-- Example: RIME Backlog consolidation by severity bands in a single pass
SELECT 
    COUNT(*) AS total_requests,
    COUNT(*) FILTER (WHERE priority_score >= 80) AS do_first_emergency,
    COUNT(*) FILTER (WHERE priority_score BETWEEN 50 AND 79) AS schedule_high
FROM mtto.backlog_items;
```

### 3.3. Prohibition of `NOT IN` with Subqueries
To prevent the presence of a `NULL` value from invalidating the entire result due to three-valued logic (3VL), `NOT IN (SELECT ...)` is prohibited in domain queries. It must be used exclusively:
* `NOT EXISTS (SELECT 1 FROM ... WHERE ...)`
* `LEFT JOIN ... WHERE <right_table>.id IS NULL`

### 3.4. Safe Evaluation in `WHERE` Clauses
Because PostgreSQL does not guarantee strict left-to-right short-circuiting in the `WHERE` clause, any calculation prone to division by zero or arithmetic error must be encapsulated in a `CASE WHEN <divisor> != 0 THEN ... ELSE NULL END` expression.

### 3.5. ISO 14224 Hierarchy Resolution ([INV-027](../requirements/user-stories/inv/INV-027.md))
For navigation and validation of the asset tree (Functional Locations L1-L5), the relational model implements an Adjacency List pattern (`parent_id`). Queries requiring the reconstruction of the asset path (breadcrumbs) or validation of re-parenting cycles must be implemented using **Recursive CTEs (`WITH RECURSIVE`)**. In-memory loading of the entire table to build the tree in the application layer (.NET) is prohibited.

### 3.6. Idempotent Ingestion for Offline Queues ([TR-007](../requirements/common/TR-007.md))
To ensure resilience in synchronization from mobile clients, deferred write operations (e.g., closing orders or telemetry registration) entering via the `Background Sync Worker` must be executed as atomic *Upsert* operations. The native **`INSERT ... ON CONFLICT (id) DO UPDATE`** clause will be used to prevent duplicate key exceptions if the mobile network retransmits the same data packet.

### 3.7. Pessimistic Locking vs. Distributed Offline Leases for LOTO Isolation ([VIS-011](../requirements/user-stories/vis/VIS-011.md), [ASR-002](./asr/DT-ARQ-ASR-001.md#2-real-time-loto-security-and-fail-safe), [ADR-006](./adr/ADR-006.md))
To guarantee compliance with the Zero Energy standard (Fail-Safe), the initiation validation of critical work orders operates under two distinct architectural boundaries:
1. **Online Synchronous Scope:** When an intervention is initiated directly against the central API, dirty reads and naive optimistic controls are strictly prohibited. The domain service executes energy state validation wrapped in explicit, non-blocking database locks (`SELECT ... FOR UPDATE NOWAIT`) on the asset isolation record. If the row is found locked by the asynchronous IoT telemetry ingestion worker, the transaction aborts immediately, returning an "Indeterminate Safety" state to prevent thread pool starvation.
2. **Offline Distributed Scope (Lease Delegation):** Mobile clients operating in disconnected environments cannot execute synchronous PostgreSQL row locks. As specified in [ADR-006](./adr/ADR-006.md), when a client acquires a cryptographically signed *Offline Lease* before entering a disconnected zone, the central server transitions the asset isolation state to `LEASED_OFFLINE` for a bounded time window (e.g., 60 minutes). During this window, the cryptographic lease acts as a distributed lock, delegating operational authority to the mobile device's local SQLite database without requiring live PostgreSQL locks. Synchronous database locking is deferred until reconnection reconciliation by the `Background Sync Worker`.

### 3.8. GIN Indexing for JSONB Immutable Audit ([ADM-032](../requirements/user-stories/adm/ADM-032.md))
To guarantee efficient searches over the massive audit trail, the `previous_state` and `new_state` columns (`JSONB` type) of the `adm.audit_logs` table—along with all domain `JSONB` payload columns governed by [DT-ERD-DOC-001 §6](../domain-models/entity-relationship/DT-ERD-DOC-001.md#6-jsonb-payload-contracts)—must be indexed using the **`jsonb_path_ops`** operator class (GIN Index). Historical search queries from the .NET application (including transversal governance and meta-audit attributes standardized in [DT-ERD-DOC-001 §6.7](../domain-models/entity-relationship/DT-ERD-DOC-001.md#67-admaudit_logsprevious_state-and-new_state)) must be implemented using the native containment operator (`@>`) to take advantage of path structure optimization (hash paths).

### 3.9. Cross-DbContext Atomic Transactions (`IDbContextTransaction` Sharing) ([TR-001](../requirements/common/TR-001.md), [TR-005](../requirements/common/TR-005.md), [INV-025](../requirements/user-stories/inv/INV-025.md))
Each Bounded Context schema (`tax`, `mtto`, `inv`, `vis`, `adm`) is mapped to an isolated Entity Framework Core `DbContext` (`TaxonomyDbContext`, `MaintenanceDbContext`, `InventoryDbContext`, `TelemetryDbContext`, `SecurityDbContext`). Direct ORM navigation properties across `DbContext` boundaries are strictly prohibited.

When an Application Command must mutate state across multiple schemas atomically (for example, `INV-025` Atomic Asset Swap mutating `tax.equipment_units`, `tax.asset_installations`, `inv.inventory_transactions`, and appending a SHA-256 hash-chained record in `adm.audit_logs`), **wrapping multiple independent connections in `System.Transactions.TransactionScope` is prohibited** to avoid Npgsql distributed transaction promotion errors. Instead:
1. **Shared Connection & Explicit Transaction Coordinator:** All scoped `DbContext` instances within the request lifetime share the same underlying physical `NpgsqlConnection`. The orchestrating use case opens a single `DbTransaction` (`await dbContext.Database.BeginTransactionAsync(ct)`) and binds every participating `DbContext` via `await secondaryDbContext.Database.UseTransactionAsync(dbTransaction.GetDbTransaction(), ct)`.
2. **Audit Log Chaining Within the Same Transaction:** The `AuditSaveChangesInterceptor` (or `ISecurityRepository.AppendAuditEntry`) executes on the active shared `DbConnection` and `DbTransaction` before `await dbTransaction.CommitAsync(ct)` is invoked, guaranteeing that domain state mutations and cryptographic audit log records (`previous_hash` $\to$ `integrity_hash`) succeed or roll back as a single ACID unit.

### 3.10. In-Process Domain Event Dispatch Semantics (`IEventBus`)
Domain events published via `IEventBus` (`WorkOrderStatusChanged`, `AssetSwapCompletedEvent`, `EquipmentDecommissioned`) execute **in-process and pre-commit** within the active shared `DbTransaction` whenever the subscriber enforces a synchronous domain invariant (such as deducting reserved stock in `inv` upon Work Order technical closure in `mtto`). Side-effect handlers that communicate with external I/O (such as `INotificationPort` SignalR broadcasts) are dispatched **post-commit** only after `dbTransaction.CommitAsync()` succeeds.

### 3.11. 7-Year Declarative Range Partitioning and Cold-Archive Anchoring ([ADM-032](../requirements/user-stories/adm/ADM-032.md), [FR-350](../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [FR-358](../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr))
To sustain sub-second forensic queries (`NFR-355`) and enforce the mandatory 7-year regulatory retention window (`TR-001-FR-367`, ISO 55001 Clause 7.5), `adm.audit_logs` is partitioned declaratively in PostgreSQL 18 by quarterly UTC ranges (`PARTITION BY RANGE (timestamp)`), enforcing composite uniqueness `(id, timestamp)` and `(integrity_hash, timestamp)` across all child partitions alongside defense-in-depth WORM hardening (`ENABLE` + `FORCE ROW LEVEL SECURITY` and `REVOKE UPDATE, DELETE, TRUNCATE ON adm.audit_logs` and child partitions from `PUBLIC` for non-superuser `NOBYPASSRLS` application roles). Instead of static hardcoded dates, baseline DDL deployment executes an idempotent dynamic PL/pgSQL bootstrap (`DO $$`) deriving quarterly UTC boundaries (`date_trunc('year', timezone('UTC', now()))`) to pre-provision all four quarters of the current calendar year (`Q1`–`Q4`) plus a next-year `Q1` lookahead (`adm.part_audit_<YYYY>_q<N>`), paired with a mandatory catch-all default partition (`adm.part_audit_default`, `PARTITION OF adm.audit_logs DEFAULT`) so `INSERT` transactions never fail before scheduled quarterly rotation; ongoing future quarters are provisioned ahead of boundary rollover by `pg_cron` or the .NET `AuditPartitionProvisioningJob`. As quarterly windows age out of the active hot tier, background archival seals each segment into encrypted cold WORM storage (`TR-002`) and records boundary metadata (`partition_name`, `period_start`, `period_end`, `record_count`, `partition_anchor_hash`, `is_cold_archived`, `integrity_status`, `sealed_at`) in `adm.audit_retention_partitions`—indexed via the descending composite B-Tree index `idx_audit_retention_partitions_period (period_start DESC, period_end DESC)` for sub-millisecond active/sealed window resolution—preserving unbroken SHA-256 chain verification (`ADR-003`) across hot and cold partitions.

### 3.12. Optimistic Concurrency Control via PostgreSQL `xmin` System Column ([INV-027](../requirements/user-stories/inv/INV-027.md), [NFR-169](../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr))
To prevent silent lost updates across concurrent engineering, maintenance, inventory, and RBAC mutations without adding synthetic `row_version` columns to the physical DDL, DTEAM standardizes on PostgreSQL 18's native **`xmin`** system transaction-ID column across all mutable aggregate roots (`tax.functional_locations`, `tax.equipment_units`, `mtto.work_orders`, `mtto.maintenance_plans`, `mtto.backlog_items`, `inv.spare_parts`, `vis.work_order_isolations`, `vis.mesh_mappings`, `adm.roles`, `adm.users`, `adm.password_policies`):
1. **EF Core Mapping (Npgsql 10):** Every mutable entity configuration binds the native system column via `builder.Property<uint>("ConcurrencyToken").IsRowVersion();` (which Npgsql automatically maps to the PostgreSQL `xmin` `xid` system column and appends `WHERE id = @p0 AND xmin = @p1` to every `UPDATE` / `DELETE` statement).
2. **HTTP Wire Contract (`ETag` / `If-Match` + DTO Token):** Read endpoints return the `uint ConcurrencyToken` inside the response DTO and emit a strong HTTP header `ETag: "{xmin}"`. Mutating `PUT`/`PATCH`/`POST` state-transition requests MUST supply the matching `If-Match: "{xmin}"` header (and/or `uint ConcurrencyToken` in the command payload).
3. **Conflict Semantics:** Whenever `DbUpdateConcurrencyException` is thrown by Npgsql (zero rows affected due to a stale `xmin`) or `If-Match` fails validation against the persisted `xmin`, the ASP.NET Core exception handler rolls back the shared `DbTransaction` and returns `HTTP 409 Conflict` with RFC 7807 `ProblemDetails` prompting the client to refresh state before retrying. Append-only / WORM tables (`adm.audit_logs`, `inv.inventory_transactions`, `vis.telemetry_signals`) are exempt from `xmin` update checks because `UPDATE` is structurally prohibited.
