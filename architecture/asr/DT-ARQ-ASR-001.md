---
code: DT-ARQ-ASR-001
version: 1.2
date: 2026-09-10
status: Approved
author: Juan David Julio Serrano
---

# Architecturally Significant Requirements (ASRs)

## 1. Offline-First Operation and Partition Tolerance
*   **Source:** [[TR-007]], [[MTTO-002]], [[INV-006]], [[ADR-006]].
*   **Quality Attribute:** Fault Tolerance / Availability / Transactional Integrity.
*   **Architectural Impact:** Forces a distributed topology with local storage on the mobile client. Blind overwrite conflict resolution via timestamps (*Last-Write-Wins*) is prohibited. Reconciliation is implemented via a queueing pipeline of operational intents (*Command-Sourced Synchronization*) processed sequentially and idempotently on the .NET backend, backed by an immutable ledger (Kardex). For critical safety interventions (LOTO), offline risk is mitigated via cryptographically signed *Offline Leases*.

## 2. Real-Time LOTO Security and Fail-Safe
*   **Source:** [[TR-010]], [[VIS-011]], NFR-229, NFR-238.
*   **Quality Attribute:** Functional Safety / Real-Time.
*   **Architectural Impact:** Demands a persistent communication layer (WebSockets/PubSub) independent of standard HTTP requests, to propagate telemetry readings and permission revocations in sub-seconds. It includes the "Cryptographic Manual Override" exception for areas without network coverage, guaranteeing the fail-safe principle without blocking critical operations that have already been physically validated.

## 3. Immutable Audit Trail
*   **Source:** [[TR-001]], [[ADM-032]], FR-347, FR-351.
*   **Quality Attribute:** Non-Repudiation / Auditability.
*   **Architectural Impact:** Prevents storing audit logs in standard transactional tables with full write permissions. Forces the establishment of an append-only storage boundary, implemented in the MVP with role isolation in PostgreSQL via Row-Level Security (RLS) and integrity validation via chained cryptographic hashing (SHA-256).

## 4. Taxonomic Transactional Core
*   **Source:** [[TR-008]], [[INV-027]], [[MTTO-029]], FR-414, FR-417.
*   **Quality Attribute:** Structural Consistency.
*   **Architectural Impact:** The ISO 14224 hierarchy spans 9 levels distributed across the domain model: Functional Locations govern Levels 1 to 5, Equipment Units Level 6, Subunits and Maintainable Items Levels 7 and 8, and the Spare Part Master Level 9. This distribution requires graph validations (cycle prevention and hierarchical nesting control) in under 500 ms. This forces the centralization of taxonomy logic into a strict bounded context, delegating graph validation and cycle prevention to the relational engine via native hierarchical queries (Recursive CTEs), thus preventing massive in-memory loading and complex business rules from scattering across the application layer.
