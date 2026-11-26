---
id: UC-ADM-014
name: Manage User Lifecycle and Authentication Identity
module: adm
user_story: ADM-014
primary_actor: System Administrator
secondary_actors:
  - Auditor
  - Maintenance Supervisor
  - Maintenance Technician
---

# UC-ADM-014: Manage User Lifecycle and Authentication Identity

## 1. Description
Governs the end-to-end lifecycle of platform user accounts (onboarding provisioning, multi-role assignment under Least-Privilege Union consolidation, Root Administrator protection, brute-force lockout defense, temporary suspension, audited restoration of previously activated accounts, logical soft-deletion, and single-use token password recovery) in compliance with ISO/IEC 27001:2022 Annex A.5.16–A.5.18, ISO 55001 Clause 7.2, and NIST SP 800-63B. It preserves historical referential integrity across Work Orders, LOTO attestations, and audit logs by enforcing logical deactivation (`INACTIVE`) and immediate session token revocation while strictly prohibiting physical account deletion.

## 2. Preconditions
* The Actor is authenticated in the platform with the `System Administrator` role for identity lifecycle mutations, or `Auditor` role for user status and login activity inspection ([TR-006](../../../requirements/common/TR-006.md)).
* Note on Offline Access Guard: Centralized identity administration requires live server connectivity and is prohibited during disconnected field operation.
* The RBAC role catalog ([UC-ADM-013](UC-ADM-013.md)), including the immutable built-in Root Administrator role (`FR-250`) and configurable password complexity policies ([NFR-272](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)), is initialized.

## 3. Main Flow
1. The System Administrator opens the User Management workspace, which presents the administrative control summary of all platform users, their lifecycle status (`ACTIVE`, `INACTIVE`, or `LOCKED`), assigned roles, and recent authentication activity ([FR-265](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [NFR-268](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).
2. The Administrator selects the action to provision a new user account ([FR-258](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr)).
3. The System presents the identity provisioning form requiring the unique Username (operator badge code), Full Name, institutional Email address, and one or more authorized RBAC Roles.
4. The Administrator enters the corporate identity attributes, assigns the appropriate operational roles, and enters an onboarding justification.
5. The System validates that both the Username and institutional Email address are globally unique across the identity directory and evaluates the assigned multi-role combination under Least-Privilege Union Consolidation and Segregation of Duties rules ([FR-251](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)).
6. The Administrator confirms account provisioning.
7. Within a single atomic transactional boundary, the System:
   * Creates the user account initialized in `INACTIVE` pre-activation state (with a pending onboarding registration state) and links the assigned RBAC roles.
   * Generates a single-use cryptographic registration token with bounded temporal validity ([NFR-269](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)) and stores its salted cryptographic hash ([TR-002](../../../requirements/common/TR-002.md), [NFR-267](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).
   * Records an append-only entry in the immutable audit trail ([TR-001](../../../requirements/common/TR-001.md)) with a chained SHA-256 cryptographic integrity hash ([ADR-003](../../../architecture/adr/ADR-003.md)).
   * Asynchronously dispatches the onboarding activation link to the user's institutional email ([FR-258](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [NFR-270](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).
8. The newly provisioned user opens the activation link via an accessible interface compatible with assistive technologies ([NFR-273](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)) and establishes a personal password complying with the configured NIST SP 800-63B complexity rules ([FR-259](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [NFR-272](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).
9. The System verifies the password policy, hashes and salts the credential ([NFR-267](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)), marks the single-use registration token as consumed, transitions the account status to `ACTIVE`, and logs the activation in the audit trail ([TR-001](../../../requirements/common/TR-001.md)). When activated users subsequently authenticate with valid credentials, the System records the latest login timestamp, clears transient failed-attempt counters, and redirects to their role-authorized workspace ([TR-006](../../../requirements/common/TR-006.md), [NFR-268](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).
10. From the identity console, the Administrator or Auditor may transition directly to Role-Based Access Control ([UC-ADM-013](UC-ADM-013.md)) to edit role privileges or to Cryptographic Audit Trail inspection ([UC-ADM-032](UC-ADM-032.md)) to inspect identity forensic events.

## 4. Alternate Flows

### AF-001: Account Suspension and Logical Soft-Deletion
When an employee's contract concludes, role duties change, or a security risk requires immediate access withdrawal ([FR-262](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [FR-264](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr)):
1. The System Administrator selects a non-root target user account, initiates suspension or logical deactivation, and enters a mandatory administrative justification.
2. Within a single atomic transaction, the System transitions the user account status to `INACTIVE` (strictly prohibiting physical row deletion so historical Work Orders, LOTO signatures, and audit logs remain intact per [FR-264](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr)), immediately revokes all active access, refresh, and offline LOTO lease tokens ([NFR-269](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr), [TR-010](../../../requirements/common/TR-010.md)), and seals the deactivation in the SHA-256 audit trail ([TR-001](../../../requirements/common/TR-001.md)).

### AF-002: Brute-Force Mitigation and Automatic Account Lockout
During authentication, if repeated invalid password attempts occur against an account ([FR-260](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [NFR-268](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)):
1. The System records each failed login attempt in the forensic access log ([NFR-268](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)) and increments the account's failure counter.
2. Upon reaching the configured maximum failure threshold (5 consecutive failed attempts), the System automatically transitions the account to `LOCKED` status with a bounded temporal lockout window.
3. The System records a critical security alert in the immutable audit trail ([TR-001](../../../requirements/common/TR-001.md)) and asynchronously dispatches an immediate security notification email to both the affected user and the System Administrator ([NFR-270](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr), [NFR-271](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).

### AF-003: Single-Use Token Password Reset and Credential Rotation
When an account requires password recovery or periodic credential rotation ([FR-261](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [FR-266](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr)):
1. The Administrator triggers a password reset (or the user initiates self-service recovery or periodic rotation).
2. The System verifies that the account is not logically deactivated, issues a single-use password reset token with strict temporal expiration ([FR-261](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [NFR-269](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)), and dispatches the recovery link asynchronously ([NFR-270](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).
3. The user submits a new password via the WCAG 2.1 AA accessible recovery interface ([NFR-273](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)); the System validates complexity rules and enforces the credential history policy preventing reuse of previous passwords ([FR-259](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [FR-266](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [NFR-272](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).
4. Upon validation, the System updates the salted password hash ([NFR-267](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)), invalidates the single-use recovery token and any prior session tokens, notifies the user of the credential change ([NFR-271](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)), and logs the event in the audit trail ([TR-001](../../../requirements/common/TR-001.md)).

### AF-004: Audited Restoration of Suspended or Locked Accounts
When the System Administrator rehabilitates a previously activated account that is suspended (`INACTIVE`) or brute-force locked (`LOCKED`) ([FR-263](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr)):
1. The System verifies that the target account does not have an unconsumed first-access registration link; accounts awaiting initial password establishment ([FR-259](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr)) cannot bypass onboarding via administrative restoration.
2. The Administrator initiates account restoration and enters a mandatory security justification documenting the reason for reactivation.
3. Within a single atomic transaction, the System restores the account status to `ACTIVE`, resets the failed login attempt counter to zero, clears the lockout window, re-establishes the user's role privileges, and records the reactivation justification in the SHA-256 chained audit trail ([TR-001](../../../requirements/common/TR-001.md)).

### AF-005: Cross-Role Segregation of Duties (SoD) Block on Role Assignment
In step 5 (or during subsequent multi-role assignment updates), if combining the selected roles on a single user grants incompatible privileges violating Segregation of Duties policies ([FR-251](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr), [FR-249](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)):
1. The System immediately engages the cross-role security interlock, blocking account provisioning or role assignment confirmation.
2. The System highlights the conflicting roles using redundant shape and color coding per WCAG 2.1 AA ([TR-011](../../../requirements/common/TR-011.md)) and identifies the violated duty-segregation rule; any server-side bypass attempt is rejected and recorded as a security alert ([TR-001](../../../requirements/common/TR-001.md)).
3. The Administrator adjusts the role assignment to remove the conflicting duty combination, and validation resumes cleanly.

### AF-006: Duplicate Username or Institutional Email Rejection
In step 5, if the entered Username or institutional Email matches an existing active or historically soft-deleted account in the identity directory ([FR-258](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [FR-264](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr)):
1. The System keeps account provisioning disabled and displays inline uniqueness conflict feedback identifying the duplicate attribute.
2. The Administrator supplies a unique Username and Email address, and provisioning validation resumes.

### AF-007: Root Administrator Account Protection
If an Administrator selects or attempts to suspend, soft-delete, or strip the Root Administrator role from the protected built-in Root Administrator account ([FR-250](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)):
1. The System locks account suspension and root role assignment controls for that account.
2. The System displays a root-account protection notice indicating that the administrative root account cannot be deactivated or stripped of system privileges, preventing unrecoverable administrative lockout.

### AF-008: Unauthorized Route or Governance Access Rejection
At any point, if an authenticated user lacking identity governance authorization attempts direct access to restricted routes or action execution ([TR-006](../../../requirements/common/TR-006.md)):
1. The System rejects the request prior to loading protected identity directory records and presents an access-denied (`403 Forbidden`) response.
2. The System appends an immutable security alert entry to the SHA-256 audit trail identifying the actor, timestamp, and attempted restricted target ([TR-001](../../../requirements/common/TR-001.md)).

## 5. Postconditions
* User accounts are governed across their complete lifecycle (`ACTIVE`, `INACTIVE`, `LOCKED`) with zero physical deletions, preserving 100% of historical operational and audit references ([FR-264](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr)), while successful logins accurately refresh activity telemetry and clear transient failure counters ([NFR-268](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).
* Suspended or locked accounts have all active session and offline lease tokens immediately invalidated ([FR-262](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr), [NFR-269](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)), and Root Administrator continuity remains preserved ([FR-250](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)).
* All provisioning events, multi-role assignments, policy changes, login attempts, brute-force lockouts, password resets, and account restorations are immutably traced in the SHA-256 cryptographic audit ledger ([TR-001](../../../requirements/common/TR-001.md), [NFR-268](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr)).

## 6. Associated Requirements
* **Functional Requirements:**
  * [FR-249](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Segregation of Duties (SoD) validations preventing conflicting operational or safety privileges.
  * [FR-250](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Protection of the Root Administrator role and built-in root administrative continuity against deactivation or lockout.
  * [FR-251](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr): Multi-role assignment consolidation under the Principle of Least Privilege union.
  * [FR-258](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr): User creation interface with automated dispatch of a secure activation link to institutional email.
  * [FR-259](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr): Mandatory establishment of a robust personal password complying with complexity policies prior to first access.
  * [FR-260](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr): Brute-force attack protection temporarily locking accounts after reaching the failed login threshold.
  * [FR-261](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr): Password resets using single-use tokens with limited temporal validity.
  * [FR-262](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr): Temporary suspension of users immediately revoking active access while preserving historical records.
  * [FR-263](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr): Restoration of suspended or locked accounts with documented reactivation justification.
  * [FR-264](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr): Logical soft-deletion of users preserving historical action traceability for technical audits.
  * [FR-265](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr): Administrative control dashboard visualizing user status, roles, and recent authentication activity.
  * [FR-266](../../../requirements/user-stories/adm/ADM-014.md#functional-requirements-fr): Self-service periodic password rotation enforcing non-reuse of previous credentials.
* **Non-Functional Requirements:**
  * [NFR-267](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr): High-resistance cryptographic hashing and salting for stored credentials and tokens.
  * [NFR-268](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr): Detailed forensic logging of all authentication attempts and security anomalies.
  * [NFR-269](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr): Strict temporal expiration policies for session and recovery tokens.
  * [NFR-270](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr): Asynchronous dispatch of activation and security alert emails.
  * [NFR-271](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr): Immediate user and administrator notification upon critical account security events.
  * [NFR-272](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr): Administrator-configurable password complexity and lockout policy parameters.
  * [NFR-273](../../../requirements/user-stories/adm/ADM-014.md#non-functional-requirements-nfr): WCAG 2.1 AA accessibility compliance across account activation and recovery workflows.
* **Transversal Requirements:**
  * [TR-001](../../../requirements/common/TR-001.md): Immutable audit trail with SHA-256 cryptographic hash chaining.
  * [TR-002](../../../requirements/common/TR-002.md): Data encryption at rest for credential hashes and security tokens.
  * [TR-005](../../../requirements/common/TR-005.md): Encryption in transit across all authentication and identity administration endpoints.
  * [TR-006](../../../requirements/common/TR-006.md): Role-Based Access Control (RBAC) authentication and token lifecycle governance.
  * [TR-010](../../../requirements/common/TR-010.md): Real-time session revocation and permission synchronization.
  * [TR-011](../../../requirements/common/TR-011.md): ANSI/ISA-101 High-Performance HMI grayscale discipline and WCAG 2.1 AA redundant coding.
* **Architectural Decision Records:**
  * [ADR-003](../../../architecture/adr/ADR-003.md): Tamper-evident cryptographic SHA-256 hash chaining for audit logs.
  * [ADR-005](../../../architecture/adr/ADR-005.md): Sequential UUIDv7 primary key generation for user and token entities.
* **Related Screens:** [SCR-ADM-014](../../../ui-ux/screens/adm/SCR-ADM-014.md), [SCR-ADM-013](../../../ui-ux/screens/adm/SCR-ADM-013.md), [SCR-ADM-032](../../../ui-ux/screens/adm/SCR-ADM-032.md)
