---
id: UC-ADM-013
name: Manage Role-Based Access Control (RBAC) and Security
module: adm
user_story: ADM-013
primary_actor: System Administrator
secondary_actors: []
---

# UC-ADM-013: Manage Role-Based Access Control (RBAC) and Security

## 1. Description
Provides the core administration interface to create, modify, and define the granular access limits of user roles across the platform. It strictly enforces Segregation of Duties (SoD) to prevent operational conflicts and ensures that all authorization changes are immutably logged for ISO 27001 compliance.

## 2. Preconditions
* The Administrator is authenticated in the web console with valid credentials and authorized role for access management [TR-006](../../../requirements/common/TR-006.md).
* The master matrix of system modules (MTTO, INV, VIS, ADM) is available and parameterized.

## 3. Main Flow
1. The Administrator accesses the Security Configuration menu and selects "Manage Roles and Permissions".
2. The Administrator selects the "Create New Role" option and enters the mandatory basic data: role name (e.g., "Maintenance Planner") and responsibility description.
3. The System presents the granular permissions matrix divided by functional modules.
4. The Administrator configures the authorized actions for the role, specifically marking the privileges: Create, Read, Edit, Delete, Approve, Audit, and Execute.
5. Upon processing the selection, the System evaluates the business rules to guarantee Segregation of Duties (SoD):
   - Verifies that the assigned permissions do not violate critical risk control policies (e.g., preventing the same role from having creation and final approval privileges over the same process).
6. The Administrator confirms the role creation.
7. The System:
   - Atomically persists the structure of the new role and its associated permissions in the security catalog.
   - Records the operation in the immutable audit trail [TR-001](../../../requirements/common/TR-001.md), generating an append-only record with its chained cryptographic hash (SHA-256).
   - Asynchronously dispatches an update notification to propagate the new permissions to all active sessions within a maximum time of 2 seconds.
8. The System displays a confirmation on screen: "Role created successfully."

## 4. Alternate Flows
### AF-001: Strict Block due to Segregation of Duties (SoD)
In step 5, if the System detects that the combination of permissions generates a direct operational risk (e.g., allowing the "Technician" role to autonomously sign their own LOTO closure):
1. The System **strictly blocks** the save operation.
2. The System highlights the conflicting permissions in red and displays a regulatory error notice: "Security Block (ISO 27001 A.5.3): The selected combination of permissions violates the Segregation of Duties policy. You must uncheck one of the conflicting actions to continue."
3. The Administrator unchecks the incompatible action and the flow returns to step 5.

### AF-002: Attempt to Modify Root Role (Super Admin)
In the management menu, if the Administrator attempts to edit or delete the system's master administration role:
1. The System denies the operation, blocks the modification controls in the interface, and displays a critical error message: "Action Denied: The integrity of the root system role is immutable and cannot be altered or deleted."
2. The flow ends, returning to the role list.

## 5. Postconditions
* The new user role is consolidated and immediately available for assignment.
* The permissions matrix is propagated to the system's authorization layer to evaluate incoming access requests with minimal latency.
* The permission alteration transaction is unalterably recorded in the audit log.

## 6. Associated Requirements
* **Functional Requirements:** FR-247, FR-248, FR-249, FR-250, FR-251, FR-252, FR-253, FR-254
* **Non-Functional Requirements:** NFR-255, NFR-256, NFR-257
* **Transversal Requirements:** [TR-001](../../../requirements/common/TR-001.md), [TR-006](../../../requirements/common/TR-006.md)
