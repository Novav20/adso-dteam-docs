---
id: UC-ADM-014
name: Manage User Lifecycle and Authentication Identity
module: adm
user_story: ADM-014
primary_actor: System Administrator
secondary_actors:
  - End User (in recovery flows)
---

# UC-ADM-014: Manage User Lifecycle and Authentication Identity

## 1. Description
Manages the complete lifecycle of corporate user accounts (provisioning, updates, logical deletion) and enforces the technical configuration of secure identity policies (password complexity algorithms, expiration, session limits, and anti-brute force mechanisms). It guarantees the referential integrity of transactional records by prioritizing logical deactivation over physical deletion.

## 2. Preconditions
* The Administrator is authenticated in the web console with an authorized identity management role [TR-006](../../../requirements/common/TR-006.md).
* The role matrix is fully configured and available for assignment.

## 3. Main Flow
1. The Administrator accesses the User Management directory and selects "Create New Account".
2. The System presents the identity form requiring basic corporate data (Name, Surname, Corporate Email, Technical ID/Employee Code).
3. The Administrator completes the data and assigns one or more configured Roles to the user.
4. The Administrator selects the account provisioning mode (e.g., sending an activation link to the user's email).
5. The Administrator confirms the registration.
6. The System executes uniqueness validations, ensuring that the corporate email and Technical ID do not exist in the database.
7. The System invokes the persistence service:
   - Registers the user securely, initializing their status as "Pending Activation".
   - Links the assigned roles via an associative data structure.
   - Generates the immutable audit record [TR-001](../../../requirements/common/TR-001.md) detailing the provisioning action and the assigning Administrator.
8. The System generates a single-use cryptographic token, embeds it in an activation email, and dispatches it to the new user.
9. The user receives the email, accesses the secure link, and establishes their initial password, which is evaluated against strict length and complexity policies.
10. The System completes the activation and updates the user's status to "Active".

## 4. Alternate Flows
### AF-001: Secure Deactivation (Logical Deletion)
If the Administrator needs to remove a user (e.g., contract termination):
1. The Administrator selects the active account and executes the "Deactivate User" action.
2. The System requires an administrative justification.
3. The Administrator confirms the action.
4. The System applies a logical deletion (changes status to INACTIVE) keeping the user's historical relations intact in work orders and audit logs.
5. The System immediately revokes and invalidates all active sessions and access tokens for that user.
6. The System records the deactivation in the immutable audit [TR-001](../../../requirements/common/TR-001.md).

### AF-002: Brute Force Mitigation (Automatic Intervention)
During any user's authentication process:
1. The System detects multiple consecutive login attempts with invalid credentials.
2. Upon exceeding the configured maximum failure threshold, the System automatically blocks the account for a specific period of time (e.g., 15 minutes).
3. The System dispatches a security alert to the user's email notifying them of the preventive block.
4. The System isolates the event by recording it as a security anomaly in the immutable log.

### AF-003: Password Recovery and Complexity Validation
If an unauthenticated user requests to restore their access:
1. The User enters their email in the portal and requests recovery.
2. The System validates that the account exists and is not logically deactivated.
3. The System generates a single-use token with temporal validity and sends it via email.
4. The User accesses the link and enters their new password.
5. The System evaluates the credential. If it does not meet the minimum length (12 characters) or violates the non-reuse policy, the System stops the process and indicates the specific reasons for rejection.
6. After a successful validation, the System securely updates the credential, invalidates the recovery token, and notifies the user of the update.

## 5. Postconditions
* The user's lifecycle (creation, block, or deactivation) is updated, guaranteeing the protection of system resources.
* Access revocation takes immediate effect on any active session.
* All identity mutations, breach attempts, and blocks are cryptographically traced for forensic audits.

## 6. Associated Requirements
* **Functional Requirements:** FR-258, FR-259, FR-260, FR-261, FR-262, FR-263, FR-264, FR-265, FR-266
* **Non-Functional Requirements:** NFR-267, NFR-268, NFR-269, NFR-270, NFR-271, NFR-272, NFR-273
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-006](../../../requirements/common/TR-006.md)
