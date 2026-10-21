---
id: UC-ADM-032
name: Consult Cryptographic Audit Trail (Audit Log)
module: adm
user_story: ADM-032
primary_actor: Plant Manager / Lead Auditor
secondary_actors: []
---

# UC-ADM-032: Consult Cryptographic Audit Trail (Audit Log)

## 1. Description
Allows authorized personnel to consult the immutable cryptographic transaction history of the platform. Strictly reserved for forensic investigations, Root Cause Analysis (RCA), and ISO 9001 / ISO 27001 / ISO 55001 regulatory compliance on critical state-mutating operations (Safety, LOTO, Security, and Asset Governance). Routine operational queries (e.g., MTBF calculations, asset movement timelines, and inventory kardex balances) are strictly decoupled from this ledger and served by normalized domain history registries.

## 2. Preconditions
* The Manager/Auditor is authenticated in the system with maximum audit privileges [TR-006](../../../requirements/common/TR-006.md).
* The centralized immutable audit registry is active and available.
* The query targets critical operations audited under [TR-001](../../../requirements/common/TR-001.md) and [ADR-003](../../../architecture/adr/ADR-003.md).

## 3. Main Flow
1. The Manager accesses the "Security and Audit" panel and selects "Consult Change Log".
2. The System presents the advanced filtering parameters: date range, responsible user, source IP address, operation type (create, modify, delete), and affected entity.
3. The Manager configures a specific filter (e.g., audit changes on a particular Work Order) and requests the query.
4. The System retrieves the historical records that match the search criteria.
5. The System presents the results in a structured timeline. The Manager selects a specific event for detailed inspection.
6. The System deploys the transaction detail, showing the source IP address, the timestamp, and the visual comparison between the Previous State and the New State of the record. The System automatically masks any sensitive attributes (such as credential hashes or access keys) to prevent accidental exposure of secrets.
7. The System transparently executes a cryptographic integrity validation routine on the record:
   - Recalculates the signature (SHA-256 hash) validating the mathematical concatenation against the chronologically previous record.
8. Upon confirming the exact match and chain integrity, the System displays a visual trust mark: "Cryptographic Integrity Verified: Unaltered Record".
9. The System records this query in the audit log itself as an administrative read action (Meta-Audit) [TR-001](../../../requirements/common/TR-001.md).

## 4. Alternate Flows
### AF-001: Compromised Integrity Alert (Tamper-Evident Activation)
In step 7, if the cryptographic chain verification fails (evidencing that underlying records were modified, deleted, or corrupted externally to the system):
1. The System interrupts the detail visualization and immediately blocks any data export for the affected date range.
2. The System deploys a prominent critical safety alert: "WARNING: Inconsistency detected in the audit chain. Possible data tampering."
3. The System automatically generates an emergency event, notifying the Lead Auditor and the HSEQ area with the identifier of the compromised record.
4. The System isolates the event in the server's security log for forensic analysis.

### AF-002: Query without Results
In step 4, if there are no records matching the entered filters:
1. The System displays a descriptive message: "No transactions found in the selected range."
2. The flow returns to step 2.

## 5. Postconditions
* The auditor obtains the unalterable data trail and the exact transaction comparison securely and masked.
* Historical integrity is algorithmically re-validated during the query.
* Any external alteration of the database is detected, isolated, and reported instantly.

## 6. Associated Requirements
* **Functional Requirements:** FR-345, FR-346, FR-347, FR-348, FR-349, FR-350, FR-351, FR-352, FR-353
* **Non-Functional Requirements:** NFR-354, NFR-355, NFR-356, NFR-357, NFR-358, NFR-359, NFR-360
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-002](../../../requirements/common/TR-002.md), [TR-003](../../../requirements/common/TR-003.md), [TR-006](../../../requirements/common/TR-006.md)
