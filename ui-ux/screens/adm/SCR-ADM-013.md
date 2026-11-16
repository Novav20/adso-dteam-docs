---
id: SCR-ADM-013
title: Industrial RBAC Roles and Segregation of Duties (SoD) Permissions Matrix
module: ADM
isa101_level: L2 (Governance & Security Supervision)
platform: Desktop Web
target_device: Desktop Workstation
roles:
  - System Administrator
  - Auditor
user_stories:
  - "[[ADM-013]]"
use_cases:
  - "[[UC-ADM-013]]"
version: 1.1
date: 2026-11-16
status: Stable
---

# SCR-ADM-013: Industrial RBAC Roles and Segregation of Duties (SoD) Permissions Matrix

## 1. Purpose and Operational Context

* **View Objective:** Centralized Level 2 security governance workspace for defining custom and operational roles (`RoleSummaryDto`), configuring the 2D module-by-action permissions matrix (`RoleMatrixDetailDto`), enforcing automated Segregation of Duties (SoD) interlocks (`Role.ValidateSoD()` per [DT-DM-DOC-002 §6.2](../../../domain-models/class/DT-DM-DOC-002.md#62-role-aggregate-root)), and broadcasting real-time permission revocations to active sessions in $< 2\text{s}$ (`NFR-257`).
* **Primary Target Persona:** System Administrator creating custom roles, configuring domain privileges across `ASSETS`, `MAINTENANCE`, `INVENTORY`, `SAFETY`, and `SYSTEM`, resolving SoD conflicts (`AF-001`), and logically deactivating obsolete roles (`FR-254`).
* **Secondary Personas:**
  * **Auditor:** Inspects the global RBAC matrix in read-only mode, verifies Segregation of Duties enforcement under ISO/IEC 27001:2022 Annex A.5.3 and ISO 55001 Clause 5.3, exports compliance reports (`FR-252`), and drills down to the Immutable Audit Log Viewer ([SCR-ADM-032](SCR-ADM-032.md)).
* **Operational Context:** Deployed exclusively on high-resolution Desktop Workstations inside IT/OT security governance and compliance offices ([DT-UI-NAV-DOC-001 §4.2](../../DT-UI-NAV-DOC-001.md#42-navigation-structure--web-portal-client)). Per [DT-UI-NAV-DOC-001 §4.1](../../DT-UI-NAV-DOC-001.md#41-navigation-structure--mobile-client) and [§6.1](../../DT-UI-NAV-DOC-001.md#61-offline-operation-guard), mobile/tablet field clients and offline execution are strictly outside scope. Compact desktop workstation adaptations are governed in Section 8.
* **Mode of Operation:** Security Governance & Compliance Audit mode. Direct DCS/SCADA process control manipulation is strictly excluded. The Root Administrator role (`ROOT_ADMINISTRATOR`) is hardware/software-locked against deletion or privilege reduction (`FR-250`, `AF-002`). Multi-role user assignment and Least-Privilege Union conflict validation (`FR-251`) reside exclusively in User Management ([SCR-ADM-014](SCR-ADM-014.md)).
* **Web Portal Workspace Invariant:** Operates within the unified Blazor Web Portal shell alongside an **on-demand, closed-by-default** right-hand workspace dock (`CMP-12` hosting `CMP-07`/`CMP-08` and `CMP-11`) using the vertical tab spine pattern (`CLS = 0`). The dock opens on vertical spine tab selection or via the `[Role Detail]` toolbar trigger, and closes cleanly on outside click, close trigger, or `Escape`.
* **Upstream & Downstream Navigation Invariants ([DT-UI-NAV-DOC-001 §5](../../DT-UI-NAV-DOC-001.md#5-transition-matrix-and-access-control-rbac)):**
  * **Upstream Continuity:** Launched from the Web Portal Governance sidebar or via `"Edit Privileges"` (`L2` $\to$ `L2`) in User Management ([SCR-ADM-014](SCR-ADM-014.md)).
  * **Downstream Transitions:** Routes to the Immutable SHA-256 Audit Log Viewer ([SCR-ADM-032](SCR-ADM-032.md)) via `"Audit Modification"` (`L2` $\to$ `L2`) or returns to [SCR-ADM-014](SCR-ADM-014.md) to assign roles to user accounts and validate multi-role permission unions (`FR-251`).

---

## 2. Visual Artifact

### 2.1. Desktop Workstation — Baseline Matrix (Dark Theme, Closed Dock by Default)
![SCR-ADM-013 Desktop Baseline Closed Dock](assets/SCR-ADM-013-screenshot.png)

> *Note: Baseline desktop workstation (Dark Theme) illustrating the collapsible sidebar (`CMP-01`), consolidated header with `[Export]` dropdown and single primary `[+ Create Custom Role]` CTA (`CMP-02`), 5-card neutral security posture KPI strip (`CMP-03`), rounded role selector tabs paired with module/lifecycle filters and `[Role Detail]` trigger (`CMP-04`), monochromatic 2D permissions matrix grid with circular checkboxes (`CMP-05`, `CMP-06`), closed-by-default right dock spine (`CMP-12`), and consolidated sticky governance footer with neutral pre-commit status slot, justification input, and L2 handoffs (`CMP-13`).*

### 2.2. Desktop Workstation — On-Demand Role Detail & Segregation Rules Dock
![SCR-ADM-013 Role Detail and Segregation Rules Dock](assets/SCR-ADM-013-dock-detail.png)

> *Note: Activating `[Role Detail]` or vertical spine tabs opens `CMP-12` to `CMP-07` (`Role Detail`) and `CMP-08` (`Segregation Rules`), inspecting role authority metadata, per-rule segregation compliance (`#icon-check` / `#icon-ban`), and the candidate SHA-256 integrity seal preview without duplicating commit controls.*

### 2.3. Desktop Light Theme — `AF-001` Segregation of Duties Conflict Interlock
![SCR-ADM-013 Light Theme AF-001 SoD Conflict](assets/SCR-ADM-013-light.png)

> *Note: Light Theme rendering during `AF-001`, escalating KPI #4 (`Evaluated SoD Rules`), conflicting matrix cells (`SAFETY.EXECUTE` and `SAFETY.APPROVE`), the violated `SOD-SAF-01` rule card, and the sticky footer block slot to redundant critical visual channels (`#icon-ban` and critical red accent) while hard-locking `[Save Permission Matrix]`.*

### 2.4. Desktop Workstation — Create Custom Role Modal (`CMP-09`, Dark Theme)
![SCR-ADM-013 Create Custom Role Modal](assets/SCR-ADM-013-create-modal.png)

> *Note: Centered Level 4 custom role creation dialog (`CMP-09`) capturing role name uniqueness, operational authority scope, optional template cloning, authorized domain modules, and strictly neutral Principle of Least Privilege (PoLP) readiness notice.*

---

## 3. Functional Component Inventory

> The base grid, typography (`--dt-font-caption` minimum floor), neutral HPHMI palettes, and tactile contact areas are inherited from [DT-UI-DS-DOC-001](../../DT-UI-DS-DOC-001.md). This inventory defines the canonical components present on the screen, their design tokens, and their architectural scope. Interaction rules and geometric algorithms are specified in Section 5; responsive container adaptations are governed by Section 8.

1. **`CMP-01`: Web Portal Shell & Sidebar**
   - **Visual Role:** Collapsible desktop navigation sidebar hosting global modules, module hierarchy, and route markers.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-base`
     - Border: `--dt-color-border-subtle`
     - Width: `--dt-layout-sidebar-width-expanded` (Desktop) / `--dt-layout-sidebar-width-collapsed` (Compact Desktop Rail)
   - **Architectural Scope:** Hosts global module navigation per [DT-UI-NAV-DOC-001 §4](../../DT-UI-NAV-DOC-001.md#4-information-architecture-tree), highlighting "Roles & Permissions (RBAC)" under Governance & Security. Layout rules governed in Section 8.

2. **`CMP-02`: RBAC Governance Header & Action Bar**
   - **Visual Role:** Sticky top header hosting breadcrumbs, live session propagation status chip (`NFR-257`), `[Export]` compliance dropdown (`CSV` / `JSON`, `FR-252`), sole primary CTA `[+ Create Custom Role]` (`FR-247`), and operator session badge.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Elevation: `--dt-z-header-sticky`
     - Primary Button: `--dt-color-state-info`
   - **Architectural Scope:** Enforces single primary CTA discipline, triggers custom role creation (`CMP-09`), exports global ISO 27001 RBAC posture reports (`FR-252`), and displays real-time SignalR session invalidation broadcasts (`< 2s`). Detailed in §5.1 and §5.3.4.

3. **`CMP-03`: Security Posture KPI Strip**
   - **Visual Role:** 5-card interactive summary strip displaying `Total Roles`, `Protected System Roles`, `Operational Roles`, `Segregation Rules`, and `Elevated Privileges` (`FR-253`). Both `Segregation Rules` and `Elevated Privileges` remain strictly neutral grayscale at `0` conflicts/warnings, escalating to critical red or amber warning borders and glyphs only when active exceptions occur.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Radius: `--dt-radius-md`
     - Active Filter Ring: `--dt-color-state-info`
     - Critical Escalation (Conflict): `--dt-color-alarm-critical`
     - Warning Accent (Elevated Privilege): `--dt-color-alarm-warning`
   - **Architectural Scope:** Provides one-click role category filtering (`ALL`, `ROOT`, `CUSTOM`) and non-alarmist baseline posture telemetry without duplicate status pills or specification acronym bloat in user-facing labels. Detailed in §5.1.

4. **`CMP-04`: Role Directory & Module Filter Toolbar**
   - **Visual Role:** Horizontal **rounded tactile role selector tab bar** (`--dt-radius-full`, matching compact low-cardinality role selection) paired with a `RbacModule` dropdown, a role lifecycle status dropdown (`ACTIVE` / `INACTIVE` / `ALL`), a debounced search input (`Ctrl+K`), `[Role Detail]` dock toggle, and `[Reset]` action.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-btn-secondary`
     - Border: `--dt-color-border-subtle`
     - Active Role Tab: `--dt-primitive-gray-980` (Light) / `--dt-primitive-gray-10` (Dark)
     - Inactive Role Tab: `--dt-color-border-subtle` (dashed outline)
     - Control Height: `--dt-control-height-sm`
     - Radius: `--dt-radius-full` (Role Selector Tabs) / `--dt-radius-sm` (Dropdowns & Action Controls)
   - **Architectural Scope:** Switches the active role inspected in `CMP-05` and `CMP-07` in $< 50\text{ms}$ without page reload across low-cardinality plant role catalogs while reserving high-saturation fills exclusively for critical or warning states ([DT-UI-DS-DOC-001 §6.5](../../DT-UI-DS-DOC-001.md#65-status-badge--counter-discipline-anti-badge-inflation-principle)). Detailed in §5.2.

5. **`CMP-05`: Interactive 2D Module-by-Action Permissions Matrix Grid**
   - **Visual Role:** Single-table 2D matrix crossing the 5 localized domain modules (`Assets & Taxonomy`, `Maintenance`, `Inventory (MRO)`, `Industrial Safety & LOTO`, `Governance & System` mapped to `RbacModule`) against the 7 localized permission actions (`Create`, `Read`, `Edit`, `Delete`, `Approve`, `Audit`, `Execute` mapped to `RbacAction` per `FR-248`), plus a row-level grant count summary (`N / 7`).
   - **Design Tokens:**
     - Header Surface: `--dt-color-surface-base`
     - Row Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Row Height: `--dt-layout-table-row-height`
     - Typography: `--dt-font-body-md`, `--dt-font-mono-data`
   - **Architectural Scope:** Core RBAC matrix editor binding `Role.AddPermission(module, action)` and `Role.RemovePermission(module, action)` ([DT-DM-DOC-002 §6.2](../../../domain-models/class/DT-DM-DOC-002.md#62-role-aggregate-root)). Detailed in §5.2 and §5.3.1.

6. **`CMP-06`: Permission Matrix Circular Checkbox Cell & SoD Interlock Indicator**
   - **Visual Role:** Tactile **circular** checkbox cell (`--dt-radius-full` within a `--dt-control-size-checkbox` hit region) rendering a monochromatic high-contrast fill and checkmark when granted, a critical red outline + `#icon-ban` badge when part of an active Segregation of Duties violation (`AF-001`), an amber `#icon-warning` indicator on PoLP advisories (`AF-003`), or a disabled padlock `#icon-loto-locked` on the immutable Root Administrator role (`AF-002`).
   - **Design Tokens:**
     - Checkbox Hit Region: `--dt-control-size-checkbox`
     - Radius: `--dt-radius-full`
     - Granted Fill: `--dt-color-text-primary`
     - Unchecked Border: `--dt-color-border-panel`
     - SoD Conflict (`AF-001`): `--dt-color-alarm-critical`
     - PoLP Advisory (`AF-003`): `--dt-color-alarm-warning`
     - Root Immutable Lock (`AF-002`): `--dt-color-state-disabled`
   - **Architectural Scope:** Enforces 4-channel WCAG 2.1 AA redundant coding on toxic permission pairs in $< 500\text{ms}$ (`NFR-255`) while avoiding green checkbox clutter on normal grants ([DT-UI-DS-DOC-001 §1](../../DT-UI-DS-DOC-001.md#1-scope)). Detailed in §5.3.1.

7. **`CMP-07`: Role Detail & Lifecycle Inspection Rail**
   - **Visual Role:** Read/Inspect master-detail rail hosted inside dock `CMP-12` displaying the selected role's name and borderless monospace category tag, metadata facts (`Description`, `AssignedUsersCount`, `ProtectionState`), the `Segregation Rules Card` (`CMP-08`), a read-only candidate SHA-256 integrity seal preview, and the contextual `[Deactivate]` trigger (`FR-254`). Commit controls (`AuditJustification`, `[Discard Changes]`, `[Save Permission Matrix]`) reside exclusively in the consolidated sticky footer `CMP-13`.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Typography: `--dt-font-caption`, `--dt-font-body-md`, `--dt-font-mono-data`
   - **Architectural Scope:** Provides authoritative role metadata, duty-segregation rule diagnostics, pre-commit cryptographic digest inspection, and lifecycle deactivation governance (`FR-254`) without duplicating matrix edit controls. Multi-role union evaluation (`FR-251`) is governed exclusively when assigning roles to accounts in [SCR-ADM-014](SCR-ADM-014.md). Detailed in §5.3.3 and §5.3.4.

8. **`CMP-08`: Segregation of Duties Rule Breakdown Card**
   - **Visual Role:** Nested governance card inside `CMP-07` listing the 4 active duty-segregation rules (`SOD-SAF-01`, `SOD-INV-01`, `SOD-MTTO-01`, `SOD-SYS-01`) evaluated against the current matrix using monochromatic SVG glyphs (`#icon-check` when compliant, escalating to `#icon-ban` and `--dt-color-alarm-critical` when violated) with plain operational descriptions free of regulatory clause citations in the UI.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-base`
     - Border: `--dt-color-border-subtle`, `--dt-color-alarm-critical` (Violated)
     - Radius: `--dt-radius-md`
   - **Architectural Scope:** Explains the exact conflicting `(Module, Action A) <-> (Module, Action B)` pair blocking commit in `AF-001`. Detailed in §5.3.1.

9. **`CMP-09`: Create Custom Role Modal (`FR-247`)**
   - **Visual Role:** Centered transactional modal dialog (`--dt-layout-modal-width`, `--dt-layout-modal-max-height`) for creating a new custom role, capturing `RoleName` (with live uniqueness validation), `Description`, optional base role template to clone, authorized `RbacModule` scope checkboxes, and a strictly neutral Principle of Least Privilege (PoLP) summary box.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-card`
     - Backdrop: `--dt-color-surface-overlay`
     - Width & Max-Height: `--dt-layout-modal-width`, `--dt-layout-modal-max-height`
     - Radius: `--dt-radius-xl`
     - Elevation: `--dt-z-modal`
     - Primary CTA: `--dt-color-state-info`
   - **Architectural Scope:** Validates role name uniqueness, scopes cloned permissions strictly to checked `AuthorizedModules`, and initializes the custom role in the matrix editor. Detailed in §5.1.

10. **`CMP-10`: Logical Role Deactivation & Session Revocation Modal (`FR-254`)**
    - **Visual Role:** Centered confirmation modal displaying the count of active assigned users who will immediately lose privileges (`< 2s`, `NFR-257`) upon deactivating the custom role, requiring a mandatory security justification ($\ge 15$ characters).
    - **Design Tokens:**
      - Surface: `--dt-color-surface-card`
      - Width: `--dt-layout-modal-width`
      - Radius: `--dt-radius-xl`
      - Elevation: `--dt-z-modal`
      - Alert Box: `--dt-color-alarm-critical`
    - **Architectural Scope:** Executes logical role deactivation while preserving historical audit trail and user-role attribution integrity (`FR-254`, `AF-004`). Detailed in §5.3.4.

11. **`CMP-11`: Chained Cryptographic RBAC Audit Pane**
    - **Visual Role:** Append-only cryptographic audit tab hosted in dock `CMP-12` displaying chronological role creations, permission matrix commits, logical deactivations, operator identity, audit justification quotes, and SHA-256 integrity hashes.
    - **Design Tokens:**
      - Surface: `--dt-color-surface-card`
      - Border: `--dt-color-border-subtle`
      - Hash Typography: `--dt-font-mono-data`
    - **Architectural Scope:** Satisfies [TR-001](../../../requirements/common/TR-001.md) and [ADR-003](../../../architecture/adr/ADR-003.md). Detailed in §5.3.3.

12. **`CMP-12`: On-Demand Workspace Dock & Vertical Tab Strip (`CLS = 0`)**
    - **Visual Role:** Closed-by-default right-hand desktop workspace dock with vertical spine tabs (`ROLE DETAIL` | `SHA-256 AUDIT`) hosting `CMP-07`/`CMP-08` and `CMP-11`.
    - **Design Tokens:**
      - Track Surface: `--dt-color-surface-base`
      - Panel Surface: `--dt-color-surface-card`
      - Active Tab: `--dt-color-surface-raised`
      - Elevation: `--dt-shadow-panel`
      - Active Indicator: `--dt-color-state-info`
    - **Architectural Scope:** Initializes closed on initial load to maximize 2D matrix width (`CLS = 0`), opens via `[Role Detail]` (`CMP-04`) or vertical spine tab click, and dismisses cleanly on outside click, close trigger, or `Escape`. Detailed in §5.2 and Section 8.

13. **`CMP-13`: Sticky Governance, Justification & Handoff Footer**
    - **Visual Role:** Permanent consolidated sticky bottom bar hosting the `CLS = 0` status alert slot (strictly neutral grayscale pre-commit; `--dt-color-state-success` teal reserved strictly for post-commit save confirmation, role deactivation, or global matrix export), L2 navigation handoffs (`[Manage Users]`, `[Forensic Audit]`), mandatory `AuditJustification` input ($\ge 15$ characters), `[Discard Changes]`, and `[Save Permission Matrix]`.
    - **Design Tokens:**
      - Surface: `--dt-color-surface-card`
      - Border: `--dt-color-border-hairline`
      - Height: `--dt-layout-footer-height`
      - Elevation: `--dt-z-header-sticky`
      - Primary CTA: `--dt-color-state-info`
      - Secondary Button: `--dt-color-surface-btn-secondary`
      - Post-Commit Success Slot: `--dt-color-state-success`
    - **Architectural Scope:** Single authoritative commit gateway hard-gated by `HasUnsavedChanges && SodEvaluation.IsCompliant && AuditJustification.Length >= 15`; routes directly to [SCR-ADM-014](SCR-ADM-014.md) or [SCR-ADM-032](SCR-ADM-032.md) ([DT-UI-NAV-DOC-001 §5](../../DT-UI-NAV-DOC-001.md#5-transition-matrix-and-access-control-rbac)). Detailed in §5.3.3.

---

## 4. Screen State Catalog

1. **Matrix Inspection & Configuration Mode (Default)**
   - **Activation Condition:** System Administrator or Auditor navigates to `SCR-ADM-013`.
   - **Visual Modification:** Neutral grayscale 90/10 baseline (`--dt-color-surface-card`) with `CMP-12` workspace dock closed by default (`CLS = 0`). Active operational role (e.g., `Maintenance Planner`) is selected via rounded tabs in `CMP-04`. Granted cells in `CMP-05` render as circular checkboxes with monochromatic high-contrast fills (`--dt-color-text-primary`) without green backgrounds. Footer status slot in `CMP-13` renders strictly neutral grayscale (*"Matrix evaluated: no duty-segregation conflicts."*).

2. **Loading / Evaluating Matrix**
   - **Activation Condition:** Initial role catalog load or server-side catalog refresh.
   - **Visual Modification:** Skeleton shimmer (`--dt-color-surface-raised`) across `CMP-03` KPI cards and `CMP-05` matrix rows; commit controls locked.

3. **Segregation of Duties Conflict Blocked (`AF-001` / `FR-249` / `NFR-255`)**
   - **Activation Condition:** Administrator checks a permission cell in `CMP-05` that conflicts with an incompatible privilege on the edited role (evaluated in $< 500\text{ms}$).
   - **Visual Modification:** Both conflicting cells in `CMP-05` highlight with a critical red outline (`--dt-color-alarm-critical`) and `#icon-ban` badge. KPI #4 (`Segregation Rules`) escalates to `--dt-color-alarm-critical`. `CMP-08` highlights the violated rule. Footer status slot in `CMP-13` renders a critical block alert (`#icon-ban`): *"Segregation of duties block: Industrial Safety and LOTO (Execute and Approve) cannot coexist on the same role."* `[Save Permission Matrix]` is hard-disabled (`CLS = 0`).

4. **Root Administrator Role Immutable Lock (`AF-002` / `FR-250`)**
   - **Activation Condition:** Administrator selects the `Root Administrator` role in `CMP-04`.
   - **Visual Modification:** All matrix cells in `CMP-05` render locked with `#icon-loto-locked` (`--dt-color-state-disabled`) and `[Deactivate]` in `CMP-07` is hidden. Footer `CMP-13` displays neutral protection notice: *"Protected Root Role: Root Administrator privileges are immutable to prevent administrative lockout."*

5. **Elevated Privilege Advisory Warning (`AF-003` / `FR-253`)**
   - **Activation Condition:** Administrator grants broad destructive privileges (such as `DELETE` on `ASSETS` or `INVENTORY` to a non-administrative role) that do not violate a hard segregation rule but exceed least-privilege baselines.
   - **Visual Modification:** Affected cell in `CMP-05` displays an amber caution border (`--dt-color-alarm-warning`) and `#icon-warning` glyph; KPI #5 (`Elevated Privileges`) escalates to `--dt-color-alarm-warning`. Footer status slot in `CMP-13` prompts for mandatory `AuditJustification` ($\ge 15$ characters) before enabling `[Save Permission Matrix]`.

6. **Creating Custom Role (`FR-247`) or Deactivating Role (`AF-004` / `FR-254`)**
   - **Activation Condition:** Administrator clicks `[+ Create Custom Role]` (`CMP-09`) or `[Deactivate]` inside `CMP-07` (`CMP-10`).
   - **Visual Modification:** Centered modal deploys over `--dt-color-surface-overlay` backdrop with keyboard focus trapping and `Escape` dismissal. Deactivated roles remain inspectable in read-only mode when filtered via `INACTIVE` or `ALL`.

7. **Documentary Confirmation & Live Session Broadcast (`NFR-257`)**
   - **Activation Condition:** Atomic permission matrix save, custom role creation/deactivation, or global compliance matrix export (`FR-252`) commits cleanly.
   - **Visual Modification:** Footer slot in `CMP-13` renders a Teal documentary confirmation (`--dt-color-state-success`, `#icon-check`) displaying the truncated SHA-256 digest or export summary, while header chip in `CMP-02` confirms: *"SESSIONS INVALIDATED (< 2s)"*.

---

## 5. Interaction Rules and Data Flow

### 5.1. Initial Load & Sub-500ms SoD Validation Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor Admin as System Administrator
    participant UI as SCR-ADM-013 (RBAC Matrix)
    participant SoD as ISodValidationEngine (< 500ms)
    participant Crypto as ICryptoInterop (SHA-256)
    participant API as Security & IAM API Gateway

    Admin->>UI: Navigates to "Roles & Permissions Matrix" (L2)
    UI->>API: GET /api/v1/security/roles/matrix
    API-->>UI: Returns RbacMatrixWorkspaceDto (Roles, Modules, SoDRules, Metrics)
    UI-->>Admin: Renders 5 KPI cards (CMP-03), Role Tabs (CMP-04), Matrix (CMP-05), Dock closed (CMP-12)
    Admin->>UI: Toggles cell (Module: SAFETY, Action: APPROVE) on "Maintenance Technician"
    UI->>SoD: EvaluateMatrix(RolePermissions, ActiveSodRules) (< 500ms, NFR-255)
    alt Segregation of Duties Conflict Detected (AF-001)
        SoD-->>UI: Returns SodEvaluationResultDto (IsCompliant = false, ViolatedRule = "SOD-SAF-01")
        UI-->>Admin: Highlights conflicting cells in Red (#icon-ban) & hard-locks [Save]
        Admin->>UI: Unchecks conflicting action (SAFETY.APPROVE) or clicks [Discard]
    end
    SoD-->>UI: Returns SodEvaluationResultDto (IsCompliant = true)
    UI->>Crypto: ComputeSha256Digest(PreviousHash, RoleMatrixPayload)
    Crypto-->>UI: Updates read-only candidate SHA-256 preview in CMP-07
    Admin->>UI: Enters AuditJustification (>= 15 chars) & clicks [Save Permission Matrix] (CMP-13)
    UI->>API: PUT /api/v1/security/roles/{id}/permissions (UpdateRolePermissionsCommand + X-Idempotency-Key)
    API-->>UI: HTTP 200 OK (Broadcasts SignalR PermissionRevocationEvent in < 2s, NFR-257)
    UI-->>Admin: Displays Teal confirmation in CMP-13, sync chip in CMP-02 & updates CMP-11 Audit Pane
```

1. **Canonical Domain Module & Action Matrix (`FR-248`, [DT-DM-DOC-001 §4.39](../../../domain-models/class/DT-DM-DOC-001.md#439-rolepermissionmodule), [§4.42](../../../domain-models/class/DT-DM-DOC-001.md#442-rolepermissionaction)):**
   * The matrix rows bind strictly to the 5 canonical `RbacModule` enum values (`ASSETS`, `MAINTENANCE`, `INVENTORY`, `SAFETY`, `SYSTEM`), and the columns bind to the 7 canonical `RbacAction` enum values (`CREATE`, `READ`, `EDIT`, `DELETE`, `APPROVE`, `AUDIT`, `EXECUTE`).
2. **Imperceptible Authorization Cache Architecture (`NFR-256`, `NFR-257`, `TR-010`):**
   * Committed matrix changes invalidate distributed memory/JWT permission claims and push a real-time SignalR `PermissionsUpdatedEvent` to connected clients in $< 2\text{s}$ (`NFR-257`, `TR-010-NFR-432`), enabling runtime endpoint authorization checks to execute in $< 5\text{ms}$–$10\text{ms}$ (`NFR-256`, `TR-006-NFR-401`).
3. **Audit Justification Payload Mapping ([DT-ERD-DOC-001 §6.7](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#67-admaudit_logsprevious_state-and-new_state)):**
   * Mandatory `AuditJustification` text captured in `CMP-13`, `CMP-09`, and `CMP-10` ($\ge 15$ characters) persists inside the `AuditLog` post-mutation `JSONB` envelope (`NewState`) under the transversal justification contract defined in [DT-ERD-DOC-001 §6.7](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#67-admaudit_logsprevious_state-and-new_state) and is sealed within the chained SHA-256 `IntegrityHash` (`ADR-003`).

---

### 5.2. Matrix Ergonomics, Dock Lifecycle & Keyboard Accessibility

1. **Grid Navigation & Keyboard Ergonomics (`CMP-05`, `CMP-06`):**
   * Supports 2D arrow-key navigation (`ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`) across matrix cells (`role="grid"`) and `Space` / `Enter` to toggle permission checkboxes.
   * Each matrix checkbox renders inside a high-clarity desktop hit region sized by `--dt-control-size-checkbox`.
2. **Closed-by-Default Dock Lifecycle (`CMP-12`):**
   * On initial render, `RbacWorkspaceDock.IsOpen == false` (`CLS = 0`). Clicking `[Role Detail]` (`CMP-04`) or either vertical spine tab (`ROLE DETAIL` | `SHA-256 AUDIT`) expands the panel at `--dt-layout-drawer-width-desktop` (`--dt-layout-drawer-width-tablet` in compact desktop viewports) without resizing surrounding controls; pressing `Escape` or clicking outside interactive matrix/toolbar regions dismisses the dock.
3. **Cross-Screen Governance Handoffs ([DT-UI-NAV-DOC-001 §5](../../DT-UI-NAV-DOC-001.md#5-transition-matrix-and-access-control-rbac)):**
   * Clicking `[Manage Users]` in `CMP-13` routes to User Management ([SCR-ADM-014](SCR-ADM-014.md)).
   * Clicking `[Forensic Audit]` in `CMP-13` routes to the Immutable SHA-256 Audit Log Viewer ([SCR-ADM-032](SCR-ADM-032.md)) pre-filtered by `EntityType = "Role"`.

---

### 5.3. Domain Workflows & Security Interlock Rules

#### 5.3.1. Segregation of Duties (SoD) Matrix Evaluation (`FR-249`, `NFR-255`, `AF-001`)
1. **Deterministic SoD Rule Set (`Role.ValidateSoD()`):** Let $P_r \subseteq \text{RbacModule} \times \text{RbacAction}$ be the permission set assigned to role $r$, and let $\mathcal{C}_{\text{SoD}}$ be the set of prohibited toxic pairs $((m_1, a_1), (m_2, a_2))$:
   * **Rule `SOD-SAF-01` (LOTO & Permit Self-Approval):** $(\text{SAFETY}, \text{CREATE/EXECUTE}) \land (\text{SAFETY}, \text{APPROVE})$ — prevents a technician or contractor from autonomously approving their own high-risk Work Permit or LOTO override.
   * **Rule `SOD-INV-01` (Inventory Fraud Prevention):** $(\text{INVENTORY}, \text{CREATE/EXECUTE}) \land (\text{INVENTORY}, \text{APPROVE/AUDIT})$ — prevents a warehouse operator from both executing and auditing/approving physical stock write-offs.
   * **Rule `SOD-MTTO-01` (Work Order Closure Governance):** $(\text{MAINTENANCE}, \text{EXECUTE}) \land (\text{MAINTENANCE}, \text{APPROVE})$ — enforces separation between field technical completion (`COMPLETE`) and supervisory administrative closure (`CLOSED`).
   * **Rule `SOD-SYS-01` (Audit Trail Independence):** $(\text{SYSTEM}, \text{CREATE/EDIT/DELETE}) \land (\text{SYSTEM}, \text{AUDIT})$ on non-root roles — separates IAM administration from independent compliance auditing.
2. **Sub-500ms Veto Execution (`NFR-255`, `AF-001`):** Whenever $\exists (p_1, p_2) \in \mathcal{C}_{\text{SoD}}$ such that $p_1 \in P_r \land p_2 \in P_r$, client-side `Role.ValidateSoD()` trips in $< 50\text{ms}$ (well within the $500\text{ms}$ ceiling), highlighting both cells in `--dt-color-alarm-critical` (`#icon-ban`) and hard-disabling `[Save Permission Matrix]`. Any attempt to bypass the UI is rejected by the backend domain aggregate, which logs a `SECURITY_ALERT` entry in the immutable audit ledger (`DT-DM-DOC-001 §4.36`).

#### 5.3.2. Principle of Least Privilege (PoLP) Advisory Warnings (`FR-253`, `AF-003`)
1. **Elevated Privilege Supervision:** When a non-root operational role is granted high-impact destructive privileges (`ASSETS.DELETE` or `INVENTORY.DELETE`), `ISodValidationEngine` raises a non-blocking amber PoLP advisory in `CMP-03` and `CMP-06` and requires explicit `AuditJustification` ($\ge 15$ characters) before `[Save Permission Matrix]` activates. Multi-role Least-Privilege Union checks ($P_{\text{effective}}(u) = \bigcup_{r \in R_u} P_r$, `FR-251`) are enforced directly during user role assignment in [SCR-ADM-014](SCR-ADM-014.md).

#### 5.3.3. Root Administrator Immutability & Chained SHA-256 Audit (`FR-250`, `AF-002`, `TR-001`, `ADR-003`)
1. **Root Role Guard (`FR-250`, `AF-002`):** When `SelectedRole.IsSystemRootRole == true`, all checkbox inputs in `CMP-05` and `Role.RemovePermission` calls are hard-blocked on both client and server.
2. **Chained SHA-256 Digest (`TR-001`, `ADR-003`):** Every role creation, permission matrix update, or logical deactivation requires a mandatory `AuditJustification` ($\ge 15$ characters) entered in `CMP-13` (or `CMP-10` for deactivations) and appends a tamper-evident record to `CMP-11`:
   $$\text{IntegrityHash} = \text{SHA-256}(\text{PreviousHash} \parallel \text{AdminUserId} \parallel \text{RoleId} \parallel \text{PreviousPermissionsJson} \parallel \text{NewPermissionsJson} \parallel \text{AuditJustification} \parallel \text{TimestampUtc})$$
3. **Discard Baseline Reversion (`CMP-13`):** Clicking `[Discard Changes]` restores the active role's working matrix cleanly to its persisted server baseline and clears pending justification text.

#### 5.3.4. Logical Role Deactivation, Export & Immediate Session Revocation (`FR-252`, `FR-254`, `NFR-257`, `AF-004`)
1. Confirming logical deactivation in `CMP-10` sets `IsActive = false` on the custom role, revokes active bearer/refresh tokens (`AuthToken.Revoke()` per `DT-DM-DOC-002 §6.4`) or pushes a SignalR permission refresh to affected sessions within $< 2\text{s}$ (`NFR-257`), and retains all historical user-role assignments and cryptographic audit entries.
2. Selecting `CSV` or `JSON` in `[Export]` (`CMP-02`) exports the complete multi-role authorization matrix and SoD evaluation ledger for ISO/IEC 27001 external audits (`FR-252`).

---

## 6. Industrial and Safety Considerations

* **Life-Safety Segregation of Duties (ISO 45001 §8.1 / ISO 55001 §5.3 / ISO 27001 A.5.3):** In industrial environments, allowing the same role to both execute field work and approve LOTO/Work Permit authorizations creates a catastrophic single-point human-factor failure mode. `CMP-05` and `CMP-08` elevate Segregation of Duties from a passive policy document to an un-bypassable software interlock (`AF-001`).
* **Root Account Anti-Lockout Protection (`FR-250`):** Preventing deletion or privilege stripping of the `Root Administrator` role guarantees that the plant platform can never enter an unrecoverable administrative lockout state during emergency governance interventions.
* **HPHMI Grayscale & Anti-Badge-Inflation Governance ([TR-011](../../../requirements/common/TR-011.md)):** In accordance with [DT-UI-DS-DOC-001 §1](../../DT-UI-DS-DOC-001.md#1-scope) and [§6.5](../../DT-UI-DS-DOC-001.md#65-status-badge--counter-discipline-anti-badge-inflation-principle), granted circular permission checkboxes render in neutral high-contrast monochromatic fill (`--dt-color-text-primary`), low-cardinality role selector tabs use tactile rounded geometry (`--dt-radius-full`), pre-commit status indicators avoid decorative green, and `--dt-color-alarm-critical` (`AF-001` SoD blocks) / `--dt-color-alarm-warning` (`AF-003` PoLP advisories) are reserved strictly for security exceptions.

---

## 7. Frontend Component Contract (Blazor / Razor)

### 7.1. Component Hierarchy & File Mapping

```text
Pages/Governance/
└── RolesAndPermissionsMatrixPage.razor                # Root View (SCR-ADM-013)
    ├── PortalSidebarNav.razor                         # CMP-01: Collapsible desktop navigation sidebar
    ├── RbacHeaderBar.razor                            # CMP-02: Breadcrumbs, [Export], [+ Create Role] & sync chip
    ├── RbacSummaryCards.razor                         # CMP-03: 5-card security posture & SoD KPI strip
    ├── RbacFilterToolbar.razor                        # CMP-04: Rounded role selector tabs, lifecycle filter & inspector trigger
    ├── PermissionsMatrixGrid.razor                    # CMP-05: 2D Module-by-Action permissions matrix table
    │   └── PermissionMatrixCell.razor                 # CMP-06: Circular checkbox cell with SoD/PoLP/Root states
    ├── RbacWorkspaceDock.razor                        # CMP-12: Closed-by-default desktop workspace dock
    │   ├── RoleInspectionRail.razor                   # CMP-07: Role metadata, SHA-256 preview & deactivate action
    │   │   └── SodConflictBreakdownCard.razor         # CMP-08: Role segregation rule evaluation card
    │   └── RbacAuditLogPane.razor                     # CMP-11: Chained SHA-256 RBAC audit trail pane
    ├── CreateCustomRoleModal.razor                    # CMP-09: Custom role creation modal (FR-247)
    ├── DeactivateRoleModal.razor                      # CMP-10: Logical role deactivation & session revocation modal (FR-254)
    └── RbacActionFooter.razor                         # CMP-13: Sticky footer, SoD slot, justification, Discard/Save & handoffs
```

---

### 7.2. Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)

#### 7.2.1. `RolesAndPermissionsMatrixPage.razor` (Root View)

```csharp
[Parameter, SupplyParameterFromQuery(Name = "roleId")]
public Guid? InitialRoleId { get; set; }
```

#### 7.2.2. Subcomponent Parameter Contracts (`CMP-01` to `CMP-13`)

```csharp
// CMP-01: PortalSidebarNav.razor
[Parameter]
public bool IsCollapsed { get; set; }

[Parameter]
public string ActiveRouteCode { get; set; } = "SCR-ADM-013";

[Parameter]
public EventCallback<bool> OnCollapseToggled { get; set; }

// CMP-02: RbacHeaderBar.razor
[Parameter]
public required string OperatorBadgeCode { get; set; }

[Parameter]
public required string OperatorDisplayName { get; set; }

[Parameter]
public bool CanEditRbac { get; set; }

[Parameter]
public DateTimeOffset? LastSessionBroadcastAtUtc { get; set; }

[Parameter]
public EventCallback OnOpenCreateRoleModal { get; set; }

[Parameter]
public EventCallback<RbacMatrixExportFormat> OnExportMatrixRequested { get; set; }

// CMP-03: RbacSummaryCards.razor
[Parameter]
public required RbacSummaryMetricsDto Metrics { get; set; }

[Parameter]
public RbacRoleFilterCategory? ActiveCategoryFilter { get; set; }

[Parameter]
public EventCallback<RbacRoleFilterCategory?> OnCategoryFilterSelected { get; set; }

// CMP-04: RbacFilterToolbar.razor
[Parameter]
public required IReadOnlyList<RoleSummaryDto> Roles { get; set; }

[Parameter]
public required Guid SelectedRoleId { get; set; }

[Parameter]
public RbacModule? SelectedModuleFilter { get; set; }

[Parameter]
public RbacRoleLifecycleFilter RoleLifecycleFilter { get; set; } = RbacRoleLifecycleFilter.ACTIVE;

[Parameter]
public string? SearchQuery { get; set; }

[Parameter]
public EventCallback<Guid> OnRoleSelected { get; set; }

[Parameter]
public EventCallback<RbacModule?> OnModuleFilterChanged { get; set; }

[Parameter]
public EventCallback<RbacRoleLifecycleFilter> OnRoleLifecycleFilterChanged { get; set; }

[Parameter]
public EventCallback<string?> OnSearchQueryChanged { get; set; }

[Parameter]
public EventCallback OnInspectRoleRequested { get; set; }

[Parameter]
public EventCallback OnResetFiltersRequested { get; set; }

// CMP-05: PermissionsMatrixGrid.razor
[Parameter]
public required RoleMatrixDetailDto ActiveRoleMatrix { get; set; }

[Parameter]
public required SodEvaluationResultDto SodEvaluation { get; set; }

[Parameter]
public bool IsReadOnly { get; set; }

[Parameter]
public EventCallback<PermissionToggleRequestDto> OnPermissionCellToggled { get; set; }

// CMP-06: PermissionMatrixCell.razor
[Parameter]
public required RbacModule Module { get; set; }

[Parameter]
public required RbacAction Action { get; set; }

[Parameter]
public bool IsGranted { get; set; }

[Parameter]
public bool IsRootLocked { get; set; }

[Parameter]
public bool HasSodConflict { get; set; }

[Parameter]
public bool HasPolpAdvisory { get; set; }

[Parameter]
public EventCallback<PermissionToggleRequestDto> OnCellToggled { get; set; }

// CMP-12: RbacWorkspaceDock.razor (Closed by default: IsOpen = false)
[Parameter]
public bool IsOpen { get; set; }

[Parameter]
public RbacDockTab ActiveTab { get; set; } = RbacDockTab.ROLE_INSPECTOR;

[Parameter]
public EventCallback<RbacDockTab> OnTabChanged { get; set; }

[Parameter]
public EventCallback OnClosed { get; set; }

// CMP-07: RoleInspectionRail.razor
[Parameter]
public required RoleMatrixDetailDto ActiveRole { get; set; }

[Parameter]
public required SodEvaluationResultDto SodEvaluation { get; set; }

[Parameter]
public required string CandidateIntegrityHashPreview { get; set; }

[Parameter]
public bool CanEditRbac { get; set; }

[Parameter]
public EventCallback<Guid> OnOpenDeactivateRoleModal { get; set; }

// CMP-08: SodConflictBreakdownCard.razor
[Parameter]
public required IReadOnlyList<SodRuleEvaluationItemDto> EvaluatedRules { get; set; }

// CMP-09: CreateCustomRoleModal.razor (FR-247)
[Parameter]
public bool IsVisible { get; set; }

[Parameter]
public required IReadOnlyList<RoleSummaryDto> TemplateRoles { get; set; }

[Parameter]
public bool IsRoleNameUnique { get; set; } = true;

[Parameter]
public EventCallback<CreateCustomRoleCommand> OnRoleCreated { get; set; }

[Parameter]
public EventCallback OnCloseRequested { get; set; }

// CMP-10: DeactivateRoleModal.razor (FR-254)
[Parameter]
public bool IsVisible { get; set; }

[Parameter]
public RoleSummaryDto? TargetRole { get; set; }

[Parameter]
public EventCallback<DeactivateCustomRoleCommand> OnDeactivateConfirmed { get; set; }

[Parameter]
public EventCallback OnCloseRequested { get; set; }

// CMP-11: RbacAuditLogPane.razor
[Parameter]
public required IReadOnlyList<RbacAuditEntryDto> AuditEntries { get; set; }

// CMP-13: RbacActionFooter.razor
[Parameter]
public required RoleMatrixDetailDto ActiveRole { get; set; }

[Parameter]
public required SodEvaluationResultDto SodEvaluation { get; set; }

[Parameter]
public bool HasUnsavedChanges { get; set; }

[Parameter]
public bool CanCommit { get; set; }

[Parameter]
public bool IsSubmitting { get; set; }

[Parameter]
public string AuditJustification { get; set; } = string.Empty;

[Parameter]
public EventCallback<string> AuditJustificationChanged { get; set; }

[Parameter]
public EventCallback OnNavigateToUserManagement { get; set; }

[Parameter]
public EventCallback<Guid> OnNavigateToAuditViewer { get; set; }

[Parameter]
public EventCallback OnDiscardChangesClicked { get; set; }

[Parameter]
public EventCallback OnSaveMatrixClicked { get; set; }
```

#### 7.2.3. Data Transfer Objects (DTOs) and Enums

```csharp
/// <summary>
/// Controlled application subdomain module vocabulary per DT-DM-DOC-001 §4.39.
/// </summary>
public enum RbacModule
{
    ASSETS,
    MAINTENANCE,
    INVENTORY,
    SAFETY,
    SYSTEM
}

/// <summary>
/// Controlled granular RBAC action vocabulary per FR-248, DT-DM-DOC-001 §4.42 & DT-ERD-DOC-001 §3.5.3.
/// </summary>
public enum RbacAction
{
    CREATE,
    READ,
    EDIT,
    DELETE,
    APPROVE,
    AUDIT,
    EXECUTE
}

public enum RbacRoleFilterCategory
{
    ALL_ROLES,
    SYSTEM_PROTECTED,
    CUSTOM_OPERATIONAL,
    SOD_RULES_ACTIVE,
    POLP_ADVISORIES
}

public enum RbacRoleLifecycleFilter
{
    ACTIVE,
    INACTIVE,
    ALL
}

public enum RbacDockTab
{
    ROLE_INSPECTOR,
    SHA256_AUDIT
}

public enum RbacMatrixExportFormat
{
    GLOBAL_MATRIX_CSV,
    GLOBAL_MATRIX_JSON
}

public readonly record struct PermissionGrantKeyDto(
    RbacModule Module,
    RbacAction Action
);

public record PermissionToggleRequestDto
{
    public required RbacModule Module { get; init; }
    public required RbacAction Action { get; init; }
    public required bool NewGrantedState { get; init; }
}

public record RbacSummaryMetricsDto
{
    public required int TotalRolesCount { get; init; }
    public required int SystemProtectedRolesCount { get; init; }
    public required int CustomRolesCount { get; init; }
    public required int ActiveSodRulesCount { get; init; }
    public required int PolpAdvisoryWarningsCount { get; init; }
}

public record RoleSummaryDto
{
    public required Guid RoleId { get; init; }
    public required string Name { get; init; }
    public string? Description { get; init; }
    public required bool IsSystemRootRole { get; init; }
    public required bool IsCustomRole { get; init; }
    public required bool IsActive { get; init; }
    public required int AssignedUsersCount { get; init; }
}

public record RoleMatrixDetailDto
{
    public required Guid RoleId { get; init; }
    public required string Name { get; init; }
    public string? Description { get; init; }
    public required bool IsSystemRootRole { get; init; }
    public required bool IsCustomRole { get; init; }
    public required bool IsActive { get; init; }
    public required int AssignedUsersCount { get; init; }
    public required IReadOnlySet<PermissionGrantKeyDto> GrantedPermissions { get; init; }
    public required string LatestIntegrityHash { get; init; }
}

public record SodEvaluationResultDto
{
    public required bool IsCompliant { get; init; }
    public required int SodViolationCount { get; init; }
    public required int PolpAdvisoryCount { get; init; }
    public IReadOnlySet<PermissionGrantKeyDto> ConflictingCells { get; init; } = new HashSet<PermissionGrantKeyDto>();
    public IReadOnlySet<PermissionGrantKeyDto> PolpAdvisoryCells { get; init; } = new HashSet<PermissionGrantKeyDto>();
    public IReadOnlyList<SodRuleEvaluationItemDto> RuleEvaluations { get; init; } = [];
    public string? PrimaryDiagnosticMessage { get; init; }
}

public record SodRuleEvaluationItemDto
{
    public required string RuleCode { get; init; }
    public required string RuleTitle { get; init; }
    public required string IsoStandardReference { get; init; }
    public required PermissionGrantKeyDto LeftPrivilege { get; init; }
    public required PermissionGrantKeyDto RightPrivilege { get; init; }
    public required bool IsViolated { get; init; }
}

public record CreateCustomRoleCommand
{
    public required string Name { get; init; }
    public required string Description { get; init; }
    public Guid? CloneFromRoleId { get; init; }
    public required IReadOnlySet<RbacModule> AuthorizedModules { get; init; }
    public required string AuditJustification { get; init; }
    public required Guid AdminUserId { get; init; }
    public required string PreviousHash { get; init; }
}

/// <summary>
/// Permission matrix mutation payload; AuditJustification persists within the AuditLog NewState JSONB envelope per DT-ERD-DOC-001 §6.7.
/// </summary>
public record UpdateRolePermissionsCommand
{
    public required Guid RoleId { get; init; }
    public required IReadOnlySet<PermissionGrantKeyDto> GrantedPermissions { get; init; }
    public required string AuditJustification { get; init; }
    public required Guid AdminUserId { get; init; }
    public required string PreviousHash { get; init; }
}

public record DeactivateCustomRoleCommand
{
    public required Guid RoleId { get; init; }
    public required string AuditJustification { get; init; }
    public required Guid AdminUserId { get; init; }
    public required string PreviousHash { get; init; }
}

/// <summary>
/// Audited RBAC timeline row hydrated from the immutable AuditLog ledger per DT-ERD-DOC-001 §3.5.1 and §6.7.
/// </summary>
public record RbacAuditEntryDto
{
    public required Guid AuditLogId { get; init; }
    public required DateTimeOffset TimestampUtc { get; init; }
    public required string OperatorBadgeCode { get; init; }
    public required string EventType { get; init; }
    public required string RoleName { get; init; }
    public required string ChangeSummary { get; init; }
    public required string AuditJustification { get; init; }
    public required string PreviousHash { get; init; }
    public required string IntegrityHash { get; init; }
}
```

---

### 7.3. Client-Side DOM & Interop Bridge

1. **In-Memory Segregation of Duties & PoLP Validator (`ISodValidationEngine`):**
   * Evaluates `Role.ValidateSoD()` and Principle of Least Privilege advisories synchronously in WebAssembly on every checkbox toggle (completing in $< 10\text{ms}$, well below the $500\text{ms}$ `NFR-255` ceiling).
2. **Real-Time Session Permission Revocation Hub (`IPermissionBroadcastHub` / `TR-010`):**
   * Subscribes to and dispatches SignalR permission invalidation events upon role matrix commits or custom role deactivations, propagating privilege changes to active client sessions in $< 2\text{s}$ (`NFR-257`, `TR-010-NFR-432`).
3. **Web Cryptography SHA-256 Digest Bridge (`ICryptoInterop`):**
   * Computes candidate `IntegrityHash` digests asynchronously in a Web Worker across canonicalized role permission sets (`TR-001`, `ADR-003`).

---

## 8. Layout and Responsive Adaptability

### 8.1. Desktop Workstation (`--dt-breakpoint-xl`, Primary Scope)
* **Layout Organization:** Asymmetric Desktop Web Portal workstation split ([DT-UI-DS-DOC-001 §2.3](../../DT-UI-DS-DOC-001.md#23-responsive-breakpoints-and-reference-frames), [DT-UI-NAV-DOC-001 §4.2](../../DT-UI-NAV-DOC-001.md#42-navigation-structure--web-portal-client)): left navigation sidebar `CMP-01` expanded at `--dt-layout-sidebar-width-expanded`, central RBAC workspace hosting the 5 summary KPI cards `CMP-03`, rounded role selector toolbar `CMP-04`, and 2D permissions matrix grid `CMP-05`, paired with the on-demand closed-by-default right workspace dock `CMP-12` sized by `--dt-layout-drawer-width-desktop` (`--dt-shadow-panel`). Modals `CMP-09` and `CMP-10` center at `--dt-layout-modal-width-desktop` bounded by `--dt-layout-modal-max-height`. Consolidated sticky footer `CMP-13` (`--dt-layout-footer-height`) spans the bottom workspace.
* **Ergonomic Rules:** Enforces strict `--dt-font-caption` minimum font size and Medium static label weighting per [DT-UI-DS-DOC-001 §4.2](../../DT-UI-DS-DOC-001.md#42-typographic-scale) (Anti-Visual-Shouting Principle); optimized for mouse and 2D keyboard arrow navigation (`Ctrl + K` search focus, `Escape` modal/dock dismissal); matrix row height governed by `--dt-layout-table-row-height`; circular checkbox cells bounded within `--dt-control-size-checkbox`; zero horizontal layout shift (`CLS = 0`).

### 8.2. Compact Desktop Workstation (`--dt-breakpoint-lg`)
* **Layout Organization:** On compact desktop and laptop monitors (`--dt-breakpoint-lg`), navigation sidebar `CMP-01` collapses to `--dt-layout-sidebar-width-collapsed`, KPI cards `CMP-03` adopt an orphan-free 3-column grid (`Total Roles` spanning 2 columns on row 1), filter controls in `CMP-04` wrap cleanly across lines to prevent selector truncation when `CMP-12` is open, workspace dock `CMP-12` operates at `--dt-layout-drawer-width-tablet`, and modals `CMP-09` and `CMP-10` size to `--dt-layout-modal-width-tablet`. Per [DT-UI-NAV-DOC-001 §4.1–§4.2](../../DT-UI-NAV-DOC-001.md#42-navigation-structure--web-portal-client), Tablet Landscape and Tablet Portrait field client breakpoints are outside the operational scope of centralized RBAC governance administration.
* **Ergonomic Rules:** Matrix rows maintain `--dt-layout-table-row-height`; consolidated sticky footer `CMP-13` (`--dt-layout-footer-height`) remains permanently pinned with L2 governance handoffs (`CLS = 0`).

---

## 9. Traceability and Requirements Matrix

| Requirement                                                                                  | Addressed in Component                 | Verification & Implementation Mechanism                                                                                                         |
| :------------------------------------------------------------------------------------------- | :------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| [FR-247](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)       | `CMP-02`, `CMP-04`, `CMP-09`           | Creates custom roles defining unique `Name`, `Description`, and authorized `RbacModule` scope.                                                  |
| [FR-248](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)       | `CMP-05`, `CMP-06`                     | Displays 2D permissions matrix configuring `CREATE`, `READ`, `EDIT`, `DELETE`, `APPROVE`, `AUDIT`, and `EXECUTE` across the 5 platform modules. |
| [FR-249](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)       | `CMP-05`, `CMP-06`, `CMP-08`, `CMP-13` | Enforces Segregation of Duties (`Role.ValidateSoD()`) blocking conflicting safety, inventory, and maintenance privilege pairs (`AF-001`).       |
| [FR-250](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)       | `CMP-05`, `CMP-06`, `CMP-07`           | Hard-locks the `Root Administrator` role (`IsSystemRootRole`) against deletion or privilege reduction (`AF-002`).                               |
| [FR-252](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)       | `CMP-02`                               | Exports the global permissions matrix and SoD compliance posture in structured formats (`CSV` and `JSON`) for ISO 27001 audits.                 |
| [FR-253](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)       | `CMP-03`, `CMP-06`, `CMP-13`           | Issues Principle of Least Privilege (PoLP) advisory warnings (`AF-003`) when destructive privileges are granted to non-supervisory roles.       |
| [FR-254](../../../requirements/user-stories/adm/ADM-013.md#functional-requirements-fr)       | `CMP-07`, `CMP-10`                     | Logically deactivates custom roles (`AF-004`), revoking active user access immediately while preserving historical audit records.               |
| [NFR-255](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr) | `CMP-05`, `CMP-06`, `CMP-08`           | In-memory `ISodValidationEngine` evaluates structural SoD conflicts in $< 500\text{ms}$ on every checkbox toggle.                               |
| [NFR-256](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr) | `CMP-05`                               | Pre-compiled claim sets and distributed authorization caches guarantee runtime permission checks execute in $< 10\text{ms}$.                    |
| [NFR-257](../../../requirements/user-stories/adm/ADM-013.md#non-functional-requirements-nfr) | `CMP-02`, `CMP-10`, `CMP-13`           | SignalR permission invalidation broadcast propagates matrix updates and role deactivations to active sessions within $< 2\text{s}$.             |
| [TR-001](../../../requirements/common/TR-001.md)                                             | `CMP-11`, `CMP-13`                     | Immutable append-only audit trail logging with SHA-256 hash chaining for all RBAC mutations and SoD security alerts.                            |
| [TR-002](../../../requirements/common/TR-002.md)                                             | `CMP-05`, `CMP-11`                     | Encrypts persisted RBAC role matrices, token hashes, and audit logs at rest.                                                                    |
| [TR-005](../../../requirements/common/TR-005.md)                                             | `CMP-02`, `CMP-05`, `CMP-13`           | Enforces TLS/HTTPS and WSS encryption in transit across all RBAC configuration requests and session revocation broadcasts.                      |
| [TR-006](../../../requirements/common/TR-006.md)                                             | `CMP-01` to `CMP-13`                   | Implements the core RBAC permissions matrix, ownership controls, and `< 5ms`–`10ms` authorization verification.                                 |
| [TR-010](../../../requirements/common/TR-010.md)                                             | `CMP-02`, `CMP-13`                     | Real-time SignalR synchronization propagating permission revocations to active user sessions (`TR-010-NFR-432`).                                |
| [TR-011](../../../requirements/common/TR-011.md)                                             | `CMP-01` to `CMP-13`                   | ANSI/ISA-101 HPHMI 90/10 neutral grayscale matrix, rounded role selector tabs, circular checkboxes, zero pre-commit green, WCAG 2.1 AA coding.  |
| [ADR-003](../../../architecture/adr/ADR-003.md)                                              | `CMP-11`, `CMP-13`                     | Tamper-evident cryptographic SHA-256 hash chaining (`PreviousHash` $\to$ `IntegrityHash`) on RBAC audit records.                                |
| [ADR-005](../../../architecture/adr/ADR-005.md)                                              | `CMP-09`                               | Time-sequential UUIDv7 identifier generation for newly created `Role` entities.                                                                 |
