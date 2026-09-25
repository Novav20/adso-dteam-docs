---
code: DT-ARQ-DB-DOC-001
version: 1.0
date: 2026-09-10
status: Active
author: Juan David Julio Serrano
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

| Rule / Element | Implementation Decision | Technical / Regulatory Justification |
| :--- | :--- | :--- |
| **PK Identifiers** | `UUID DEFAULT uuidv7()` | Time-sequential identifiers that prevent B-Tree page fragmentation in massive telemetry and audit insertions. |
| **FK Indexing** | Mandatory `CREATE INDEX` on each foreign key column. | PostgreSQL **does not** automatically index FKs in child tables. Prevents *Full Table Scans* during parent deletions or updates. |
| **Asset Deletion** | `ON DELETE RESTRICT` on relations with `work_orders`. | **ISO 14224 / ISO 55001:** Strict prohibition of cascade deletion on work orders and failure history. Assets are logically retired (`Decommission`). |
| **Spares Management** | Keep standard `NULLS DISTINCT` behavior in `equipment_units.functional_location_id`. | Allows multiple equipment units in the warehouse (`IN_STORAGE`) to have a `NULL` value simultaneously without violating plant slot uniqueness (Pauli Principle). |
| **Numerical Precision** | Strict `DECIMAL(18,6)` on sensors and `DECIMAL(12,2)` on costs. | Prohibition of `DOUBLE PRECISION` / `FLOAT` to avoid IEEE 754 rounding errors in deterministic Zero Energy (LOTO) validation. |
| **DDD Schemas** | Segregation into 5 schemas: `tax`, `mtto`, `inv`, `vis`, `adm`. | Isolation by *Bounded Context*, removal of prefixes in tables, and support for defense in depth via `GRANT/REVOKE` privileges. |
| **Operational Indexing** | `CREATE INDEX ... WHERE ...` (Partial) | To optimize query performance on the Backlog Board and LOTO validations without saturating RAM, the use of **Partial Indexes** on active records is required. Records in terminal states (e.g., `CLOSED`, `COMPLETE`) are excluded from the active index B-Tree. |
| **Controlled Vocabularies**| `CHECK (col IN (...))` in MVP with evolution path to *Lookup Tables*. | In the MVP, `CHECK` constraints mapped to C# `enum`s are used to maximize performance and avoid unnecessary JOINs. In later phases requiring dynamic parameterization from the UI (without code deployments), they will be migrated to dedicated catalog tables managed by Entity Framework Core (`SeedData`). |

## 3. DML Query and Performance Guidelines

### 3.1. `LEFT JOIN LATERAL` Pattern for Latest Telemetry ([[VIS-033]])
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

### 3.2. Conditional Aggregations with `FILTER` Clause ([[MTTO-026]], [[INV-006]])
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

### 3.5. ISO 14224 Hierarchy Resolution ([[INV-027]])
For navigation and validation of the asset tree (Functional Locations L1-L5), the relational model implements an Adjacency List pattern (`parent_id`). Queries requiring the reconstruction of the asset path (breadcrumbs) or validation of re-parenting cycles must be implemented using **Recursive CTEs (`WITH RECURSIVE`)**. In-memory loading of the entire table to build the tree in the application layer (.NET) is prohibited.

### 3.6. Idempotent Ingestion for Offline Queues ([[TR-007]])
To ensure resilience in synchronization from mobile clients, deferred write operations (e.g., closing orders or telemetry registration) entering via the `Background Sync Worker` must be executed as atomic *Upsert* operations. The native **`INSERT ... ON CONFLICT (id) DO UPDATE`** clause will be used to prevent duplicate key exceptions if the mobile network retransmits the same data packet.

### 3.7. Pessimistic Locking for LOTO Isolation ([[VIS-011]], [[DT-ARQ-ASR-001#2. Real-Time LOTO Security and Fail-Safe|ASR-2]])
To guarantee compliance with the Zero Energy standard (Fail-Safe), the initiation validation of critical work orders must not use dirty reads or exclusive optimistic control. The domain service must execute energy state validation wrapping queries in explicit, non-blocking database locks (`SELECT ... FOR UPDATE NOWAIT`). If the row is found locked by the asynchronous IoT telemetry injection process, the transaction must abort immediately, returning an "Indeterminate Safety" state to the user, preventing the thread from freezing (prevent thread pool starvation).

### 3.8. GIN Indexing for JSONB Immutable Audit ([[ADM-032]])
To guarantee efficient searches over the massive audit trail, the `previous_state` and `new_state` columns (`JSONB` type) of the `adm.audit_logs` table must be indexed using the **`jsonb_path_ops`** operator class (GIN Index). Historical search queries from the .NET application must be implemented using the native containment operator (`@>`) to take advantage of path structure optimization (hash paths).
