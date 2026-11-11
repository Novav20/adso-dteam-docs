---
id: UC-ADM-032
name: Consult Cryptographic Audit Trail (Audit Log)
module: adm
user_story: ADM-032
primary_actor: Auditor
secondary_actors:
  - Plant Manager
  - System Administrator
---

# UC-ADM-032: Consult Cryptographic Audit Trail (Audit Log)

## 1. Description
Enables authorized governance personnel to query, inspect, verify, and export the platform's immutable, append-only cryptographic audit trail in compliance with ISO/IEC 27001:2022 Annex A.8.15–A.8.16, ISO 55001 Clause 7.5, and ISO 9001. Reserved strictly for forensic investigations, Root Cause Analysis (RCA), and regulatory compliance across critical state-mutating operations (`CREATE`, `UPDATE`, `DELETE`, `QUERY`, `ADJUST`, and `SECURITY_ALERT`), the system provides side-by-side before-and-after state comparisons with automatic secret masking, visualizes temporal activity trends to detect operational anomalies, validates SHA-256 cryptographic hash-chain continuity from the genesis record, enforces a minimum 7-year retention lifecycle, and records all audit queries via self-referential Meta-Auditing.

## 2. Preconditions
* The Actor is authenticated in the web portal with the `Auditor`, `Plant Manager`, or `System Administrator` role possessing audit inspection privileges ([TR-006](../../../requirements/common/TR-006.md)).
* Note on Offline Access Guard: In accordance with the global navigation offline guard ([DT-UI-NAV-DOC-001 §6.1](../../../ui-ux/DT-UI-NAV-DOC-001.md#61-offline-operation-guard)), direct queries against the central immutable audit repository require active server connectivity, while verified audit packages may be exported for independent offline analysis ([NFR-359](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr)).
* The centralized append-only audit ledger ([TR-001](../../../requirements/common/TR-001.md), [ADR-003](../../../architecture/adr/ADR-003.md)) is active and enforces strict write-once immutability preventing modification or deletion by any role ([FR-347](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr)).

## 3. Main Flow
1. The Auditor accesses the Immutable Audit Log Viewer ([SCR-ADM-032](../../../ui-ux/screens/adm/SCR-ADM-032.md)) from the Web Portal Governance menu or via the `"Audit Modification"` handoff in the RBAC Matrix ([SCR-ADM-013](../../../ui-ux/screens/adm/SCR-ADM-013.md)).
2. The System presents the audit analysis dashboard visualizing technical activity volume trends and anomaly indicators ([FR-352](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr)), alongside multi-criteria filtering controls: UTC date-time range, operator identity, source IP address, operation type (`CREATE`, `UPDATE`, `DELETE`, `QUERY`, `ADJUST`, `SECURITY_ALERT`), affected domain entity type, specific entity identifier, and structured attribute path values ([FR-345](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [FR-348](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr)).
3. The Auditor configures the search criteria (such as filtering `ADJUST` and `UPDATE` operations on a specific Work Order or Equipment Unit) and executes the query.
4. The System retrieves the matching encrypted historical records with high-speed indexed performance ([NFR-355](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr), [NFR-356](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr), [NFR-357](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr)) while ensuring background operational logging never penalizes live plant transactions ([NFR-354](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr)).
5. The System renders the chronological ledger and automatically records a self-referential `QUERY` entry (Meta-Audit) in the immutable audit trail capturing the Auditor's identity, timestamp, and query filter scope ([NFR-360](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr), [TR-001](../../../requirements/common/TR-001.md)).
6. The Auditor selects a specific audit event from the ledger for forensic inspection.
7. The System displays the detailed forensic comparison pane ([FR-349](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr)), presenting the UTC timestamp, operator badge, source IP address, client user agent, and a structured diff comparing the Previous State against the New State, automatically masking sensitive credential hashes or cryptographic keys.
8. The System executes a cryptographic hash-chain verification across the inspected record and its chronological predecessors ([FR-346](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [FR-351](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [TR-003](../../../requirements/common/TR-003.md), [ADR-003](../../../architecture/adr/ADR-003.md)):
   9. Recomputes the SHA-256 digest chaining the preceding record's integrity hash (`GENESIS` sentinel on the initial ledger entry) with the current record's immutable payload.
   10. Compares the recalculated digest against the stored integrity hash.
11. Upon confirming an exact mathematical match and unbroken chain continuity, the System displays a documentary confirmation seal: *"Cryptographic Integrity Verified: Unaltered Record Chain"* ([TR-011](../../../requirements/common/TR-011.md)).
12. The Auditor optionally exports the verified audit trail subset in a structured, cryptographically signed format (`CSV` or `JSON`) for external regulatory reviews or offline forensic analysis ([FR-349](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [FR-353](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [NFR-359](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr)), while the System governs long-term 7-year archival retention ([FR-350](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [FR-358](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr)).

## 4. Alternate Flows

### AF-001: Compromised Chain Integrity Alert (Tamper-Evident Breach Detected)
In step 8 or during periodic automated background verification ([FR-346](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [FR-351](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr)), if the recalculated SHA-256 hash mismatches the stored digest or a chronological gap indicates external database row deletion:
1. The System immediately flags the exact compromised record and blocks standard compliance export for the corrupted range to prevent circulation of tampered evidence.
2. The System deploys a high-salience critical security alert using redundant shape and color coding per WCAG 2.1 AA ([TR-011](../../../requirements/common/TR-011.md)): *"CRITICAL SECURITY ALERT: Cryptographic Hash-Chain Discrepancy Detected. Possible External Database Tampering."*
3. The System automatically appends a high-priority `SECURITY_ALERT` event to the security log and dispatches an immediate incident notification to the Lead Auditor, System Administrator, and HSEQ supervision ([TR-003](../../../requirements/common/TR-003.md)).

### AF-002: Attempted Modification or Deletion of Audit Records
If any user—including a System Administrator—attempts to edit, overwrite, or delete an existing audit trail entry via the interface or API ([FR-347](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr)):
1. The System rejects the operation unconditionally under the append-only immutability policy ([TR-001](../../../requirements/common/TR-001.md)).
2. The System records the rejected attempt as a `SECURITY_ALERT` event in the audit trail ([TR-006](../../../requirements/common/TR-006.md)).

### AF-003: Query Without Matching Records
In step 4, if no historical transactions match the specified filter criteria:
1. The System records the Meta-Audit `QUERY` event ([NFR-360](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr)) and displays a neutral empty-state notice: *"No audit records match the selected filter parameters."*
2. The Auditor adjusts the filter criteria, returning to step 2.

## 5. Postconditions
* The Auditor obtains a verified, secret-masked before-and-after comparison of the target historical transactions ([FR-349](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr)).
* Cryptographic SHA-256 hash-chain continuity is mathematically verified across the inspected range ([FR-351](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [ADR-003](../../../architecture/adr/ADR-003.md)).
* The consultation or export action itself is immutably recorded via Meta-Auditing ([NFR-360](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr)).
* Historical records remain protected under encrypted 7-year regulatory retention policies ([FR-350](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [FR-358](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr), [NFR-357](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr)).

## 6. Associated Requirements
* **Functional Requirements:**
  * [FR-345](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Recording of all critical operations (`CREATE`, `UPDATE`, `DELETE`, `QUERY`, `ADJUST`, `SECURITY_ALERT`) with timestamp, actor identity, and before/after states.
  * [FR-346](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Security monitoring mechanisms preventing unauthorized alterations to the audit history.
  * [FR-347](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Strict append-only immutability preventing editing or deletion of audit records by any profile.
  * [FR-348](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Advanced query interface filtering by date periods, users, operation types, and affected entities.
  * [FR-349](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Structured visualization of before/after state changes and export for external compliance reviews.
  * [FR-350](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Automated audit data lifecycle and archival management preserving hash-chain continuity.
  * [FR-351](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Periodic and on-demand cryptographic integrity validation with immediate anomaly notification.
  * [FR-352](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Audit analysis dashboard visualizing activity trends and detecting unusual operational patterns.
  * [FR-353](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Export of the audit trail in structured formats (`CSV` and `JSON`) for external regulatory audits.
  * [FR-358](../../../requirements/user-stories/adm/ADM-032.md#functional-requirements-fr): Regulatory retention maintaining historical audit records for the statutory period (minimum 7 years).
* **Non-Functional Requirements:**
  * [NFR-354](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr): Asynchronous audit capture ensuring zero performance penalty on primary operational transactions.
  * [NFR-355](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr): High-efficiency query response times across large volumes of accumulated historical data.
  * [NFR-356](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr): Optimized persistence indexing guaranteeing data integrity and rapid retrieval.
  * [NFR-357](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr): Encryption at rest protecting sensitive state payloads within audit logs.
  * [NFR-359](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr): Portable data extraction enabling independent offline forensic analysis in external environments.
  * [NFR-360](../../../requirements/user-stories/adm/ADM-032.md#non-functional-requirements-nfr): Self-referential Meta-Auditing recording all accesses and queries made to the auditing tools.
* **Transversal Requirements:**
  * [TR-001](../../../requirements/common/TR-001.md): Immutable audit trail with 7-year retention and SHA-256 cryptographic hash chaining.
  * [TR-002](../../../requirements/common/TR-002.md): Data encryption at rest for audit log storage volumes and archives.
  * [TR-003](../../../requirements/common/TR-003.md): Cryptographic data integrity verification and tamper alerting.
  * [TR-005](../../../requirements/common/TR-005.md): Encryption in transit across all audit query and export channels.
  * [TR-006](../../../requirements/common/TR-006.md): Role-Based Access Control (RBAC) restricting audit trail access to authorized governance roles.
  * [TR-011](../../../requirements/common/TR-011.md): ANSI/ISA-101 High-Performance HMI grayscale discipline and WCAG 2.1 AA redundant coding.
* **Architectural Decision Records:**
  * [ADR-003](../../../architecture/adr/ADR-003.md): Tamper-evident cryptographic SHA-256 hash chaining (`GENESIS` sentinel and sequential payload linking).
  * [ADR-005](../../../architecture/adr/ADR-005.md): Time-sequential UUIDv7 primary key generation preventing B-Tree index fragmentation in high-velocity audit tables.