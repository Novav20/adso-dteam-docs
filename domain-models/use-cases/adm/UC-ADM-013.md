---
id: UC-ADM-013
name: Manage Role-Based Access Control (RBAC) and Security
module: adm
user_story: ADM-013
primary_actor: System Administrator
secondary_actors:
  - Auditor
---

# UC-ADM-013: Manage Role-Based Access Control (RBAC) and Security

## 1. Description
Provides the governance interface to create, configure, audit, and logically deactivate user roles and granular permission matrices across the platform's five functional domains (`ASSETS`, `MAINTENANCE`, `INVENTORY`, `SAFETY`, and `SYSTEM`). It enforces Segregation of Duties (SoD) in compliance with ISO/IEC 27001:2022 Annex A.5.3 and ISO 55001 Clause 5.3, protects the immutable Root Administrator role, evaluates multi-role assignments under the Principle of Least Privilege (PoLP), propagates permission revocations to active sessions in under 2 seconds, and seals all authorization mutations in the SHA-256 cryptographic audit trail.

## 2. Preconditions
* The Actor is authenticated in the web portal with the `System Administrator` role for RBAC configuration, or `Auditor` role for compliance matrix inspection and export ([TR-006](../../../requirements/common/TR-006.md)).
* Note on Offline Access Guard: In accordance with the global navigation offline guard ([DT-UI-NAV-DOC-001 §6.1](../../../ui-ux/DT-UI-NAV-DOC-001.md#61-offline-operation-guard)), centralized security administration screens require active server connectivity and are blocked during disconnected field operation.
* The master catalog of platform functional domains (`ASSETS`, `MAINTENANCE`, `INVENTORY`, `SAFETY`, `SYSTEM`), atomic actions (`CREATE`, `READ`, `EDIT`, `DELETE`, `APPROVE`, `AUDIT`, `EXECUTE`), and Segregation of Duties conflict rules is initialized.

## 3. Main Flow
1. The System Administrator accesses the Roles and Permissions Matrix interface ([SCR-ADM-013](../../../ui-ux/screens/adm/SCR-ADM-013.md)) from the Governance navigation menu or via the `"Edit Privileges"` handoff in User Management ([SCR-ADM-014](../../../ui-ux/screens/adm/SCR-ADM-014.md)).
2. The Administrator selects the action to create a custom role ([FR-247](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)) or selects an existing custom or operational role from the role directory.
3. The Administrator enters or updates the role's unique Name, operational responsibility Description, and target functional domains ([FR-247](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)).
4. The System displays the 2D permissions matrix crossing the five functional domains (`ASSETS`, `MAINTENANCE`, `INVENTORY`, `SAFETY`, `SYSTEM`) against the seven granular actions (`CREATE`, `READ`, `EDIT`, `DELETE`, `APPROVE`, `AUDIT`, `EXECUTE`) ([FR-248](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)), alongside the multi-role Least-Privilege Union simulator ([FR-251](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)).
5. The Administrator toggles the desired permission cells for the role and enters a mandatory security audit justification.
6. Upon every cell selection, the System evaluates structural Segregation of Duties (SoD) and Principle of Least Privilege rules in under 500 milliseconds ([FR-249](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr), [FR-253](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr), [NFR-255](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr)):
   7. Verifies that the role does not combine mutually exclusive toxic privilege pairs (such as granting both `CREATE`/`EXECUTE` and final `APPROVE` authority over `SAFETY` Work Permits or `INVENTORY` physical count adjustments).
   8. Evaluates effective permission unions for users holding multiple roles ([FR-251](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)).
9. The System confirms that no Segregation of Duties conflicts exist and previews the candidate SHA-256 cryptographic integrity seal.
10. The Administrator confirms saving the role and permission matrix.
11. Within a single atomic transactional boundary, the System:
   12. Persists the role definition and its granted domain-action permission set in the security catalog ([TR-002](../../../requirements/common/TR-002.md), [TR-005](../../../requirements/common/TR-005.md)).
   13. Appends an immutable record to the audit trail ([TR-001](../../../requirements/common/TR-001.md)) with a chained SHA-256 cryptographic hash ([ADR-003](../../../architecture/adr/ADR-003.md)).
   14. Broadcasts a real-time authorization cache invalidation event, propagating the updated permissions to all active user sessions in under 2 seconds ([NFR-257](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr), [TR-010](../../../requirements/common/TR-010.md)) so subsequent request evaluations execute in under 10 milliseconds ([NFR-256](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr)).
15. The System displays a documentary confirmation notice and enables exporting the global permissions matrix for external compliance audits ([FR-252](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)) or transitioning to the Immutable Audit Log Viewer ([SCR-ADM-032](../../../ui-ux/screens/adm/SCR-ADM-032.md)).

## 4. Alternate Flows

### AF-001: Strict Block Due to Segregation of Duties (SoD) Violation
In step 6, if the Administrator selects a combination of permissions that violates Segregation of Duties policies ([FR-249](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr), [NFR-255](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr)):
1. The System immediately engages the security interlock, hard-disabling the save action.
2. The System highlights the conflicting matrix cells using redundant shape and color coding per WCAG 2.1 AA ([TR-011](../../../requirements/common/TR-011.md)), logs a security alert event, and displays a regulatory block notice: *"Segregation of Duties Block (ISO/IEC 27001 Annex A.5.3): A single role cannot hold both Execution/Creation and Approval authority over the same critical domain. Deselect one of the conflicting privileges to proceed."*
3. The Administrator deselects one of the incompatible actions, and the workflow resumes at step 6.

### AF-002: Attempt to Modify or Delete the Root Administrator Role
In step 2, if the Administrator attempts to delete the Root Administrator role or restrict its core governance privileges ([FR-250](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)):
1. The System locks all mutation checkboxes and deletion controls on the Root Administrator role.
2. The System displays an immutability notice: *"Protected System Role: The Root Administrator role is immutable and cannot be deleted or restricted to prevent administrative lockout."*
3. The workflow remains in read-only inspection mode for that role.

### AF-003: Principle of Least Privilege (PoLP) Advisory Warning
In step 6, if the Administrator grants broad destructive or cross-domain privileges (such as `DELETE` across operational modules on a non-supervisory role) that do not trigger a hard SoD block but exceed standard least-privilege baselines ([FR-253](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)):
1. The System displays a non-blocking advisory warning with redundant coding (`#icon-warning`), identifying the elevated privilege cells.
2. The System requires the Administrator to document a specific business justification before proceeding to step 8.

### AF-004: Logical Deactivation of a Custom Role and Immediate Session Revocation
When the Administrator deactivates an obsolete or compromised custom role ([FR-254](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)):
1. The Administrator selects the custom role, initiates logical deactivation, reviews the count of affected users, and enters a mandatory security justification.
2. Within a single atomic transaction, the System marks the role as logically inactive while preserving its historical audit references, records the SHA-256 audit entry ([TR-001](../../../requirements/common/TR-001.md)), and immediately revokes the role's privileges across all active user sessions in under 2 seconds ([NFR-257](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr)).

## 5. Postconditions
* Custom and operational roles are persisted with a verified, Segregation-of-Duties-compliant permission matrix across all five platform domains.
* Updated privileges are actively enforced across all connected client sessions within 2 seconds ([NFR-257](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr)) with authorization checks executing in under 10 milliseconds ([NFR-256](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr)).
* All role creations, permission changes, SoD violation blocks, and logical deactivations are sealed in the append-only SHA-256 audit ledger ([TR-001](../../../requirements/common/TR-001.md)).

## 6. Associated Requirements
* **Functional Requirements:**
  * [FR-247](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Creation of custom roles defining name, description, and authorized functional modules.
  * [FR-248](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Granular permissions matrix configuring allowed actions (`CREATE`, `READ`, `EDIT`, `DELETE`, `APPROVE`, `AUDIT`, `EXECUTE`) per module.
  * [FR-249](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Segregation of Duties (SoD) validations preventing conflicting financial or safety privileges.
  * [FR-250](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Protection of the Root Administrator role against deletion or restrictive editing.
  * [FR-251](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Multi-role assignment consolidation under the Principle of Least Privilege union.
  * [FR-252](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Generation and export of the global permissions matrix for regulatory compliance audits.
  * [FR-253](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Informative warnings when role configurations deviate from the Principle of Least Privilege.
  * [FR-254](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Logical deactivation of custom roles with immediate access revocation and historical preservation.
* **Non-Functional Requirements:**
  * [NFR-255](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr): Segregation of Duties conflict verification completing in under 500 milliseconds.
  * [NFR-256](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr): Imperceptible runtime permission authorization latency under 10 milliseconds.
  * [NFR-257](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr): Propagation of permission matrix updates to active sessions within 2 seconds.
* **Transversal Requirements:**
  * [TR-001](../../../requirements/common/TR-001.md): Immutable audit trail with SHA-256 cryptographic hash chaining.
  * [TR-002](../../../requirements/common/TR-002.md): Data encryption at rest for security configurations and credential stores.
  * [TR-005](../../../requirements/common/TR-005.md): Encryption in transit across all IAM administration and session revocation channels.
  * [TR-006](../../../requirements/common/TR-006.md): Role-Based Access Control (RBAC) authentication and authorization framework.
  * [TR-010](../../../requirements/common/TR-010.md): Real-time session permission synchronization across connected clients.
  * [TR-011](../../../requirements/common/TR-011.md): ANSI/ISA-101 High-Performance HMI grayscale discipline and WCAG 2.1 AA redundant coding.
* **Architectural Decision Records:**
  * [ADR-003](../../../architecture/adr/ADR-003.md): Tamper-evident cryptographic SHA-256 hash chaining for audit logs.
  * [ADR-005](../../../architecture/adr/ADR-005.md): Sequential UUIDv7 primary key generation for role entities.