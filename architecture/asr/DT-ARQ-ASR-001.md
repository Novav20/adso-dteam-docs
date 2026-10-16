---
code: DT-ARQ-ASR-001
version: 1.2
date: 2026-09-10
status: Approved
author: Juan David Julio Serrano
---

# Architecturally Significant Requirements (ASRs)

## 1. Offline-First Operation and Partition Tolerance
*   **Source:** [TR-007](../../requirements/common/TR-007.md), [MTTO-002](../../requirements/user-stories/mtto/MTTO-002.md), [INV-006](../../requirements/user-stories/inv/INV-006.md), [ADR-006](../adr/ADR-006.md).
*   **Quality Attribute:** Fault Tolerance / Availability / Transactional Integrity.
*   **Architectural Impact:** Forces a distributed topology with local storage on the mobile client. Blind overwrite conflict resolution via timestamps (*Last-Write-Wins*) is prohibited. Reconciliation is implemented via a queueing pipeline of operational intents (*Command-Sourced Synchronization*) processed sequentially and idempotently on the .NET backend, backed by an immutable ledger (Kardex). For critical safety interventions (LOTO), offline risk is mitigated via cryptographically signed *Offline Leases*.

## 2. Real-Time LOTO Security and Fail-Safe
*   **Source:** [TR-010](../../requirements/common/TR-010.md), [VIS-011](../../requirements/user-stories/vis/VIS-011.md), [NFR-229](../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr), [NFR-238](../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr).
*   **Quality Attribute:** Functional Safety / Real-Time.
*   **Architectural Impact:** Demands a persistent communication layer (WebSockets/PubSub) independent of standard HTTP requests, to propagate telemetry readings and permission revocations in sub-seconds. It includes the "Cryptographic Manual Override" exception for areas without network coverage, guaranteeing the fail-safe principle without blocking critical operations that have already been physically validated.

## 3. Immutable Audit Trail
*   **Source:** [TR-001](../../requirements/common/TR-001.md), [ADM-032](../../requirements/user-stories/adm/ADM-032.md), [FR-347](../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [FR-351](../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr).
*   **Quality Attribute:** Non-Repudiation / Auditability.
*   **Architectural Impact:** Prevents storing audit logs in standard transactional tables with full write permissions. Forces the establishment of an append-only storage boundary, implemented in the MVP with role isolation in PostgreSQL via Row-Level Security (RLS) and integrity validation via chained cryptographic hashing (SHA-256).

## 4. Taxonomic Transactional Core
*   **Source:** [TR-008](../../requirements/common/TR-008.md), [INV-027](../../requirements/user-stories/inv/INV-027.md), [MTTO-029](../../requirements/user-stories/mtto/MTTO-029.md), [FR-414](../../requirements/common/TR-008.md#functional-requirements-fr), [NFR-417](../../requirements/common/TR-008.md#non-functional-requirements-nfr).
*   **Quality Attribute:** Structural Consistency.
*   **Architectural Impact:** The ISO 14224 hierarchy spans 9 levels distributed across the domain model: Functional Locations govern Levels 1 to 5, Equipment Units Level 6, Subunits and Maintainable Items Levels 7 and 8, and the Spare Part Master Level 9. This distribution requires graph validations (cycle prevention and hierarchical nesting control) in under 500 ms. This forces the centralization of taxonomy logic into a strict bounded context, delegating graph validation and cycle prevention to the relational engine via native hierarchical queries (Recursive CTEs), thus preventing massive in-memory loading and complex business rules from scattering across the application layer.
