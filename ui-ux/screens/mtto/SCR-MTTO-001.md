---
id: SCR-MTTO-001
title: Preventive Maintenance Scheduling Form (Calendar Intervals)
module: MTTO
isa101_level: L3 (Equipment Detail & Technical Form)
platform: Desktop Web
target_device: Desktop Workstation (Primary) | Industrial Tablet Landscape
roles:
  - Maintenance Planner
  - Maintenance Supervisor
  - Reliability Engineer
user_stories:
  - "[[MTTO-001]]"
use_cases:
  - "[[UC-MTTO-001]]"
version: 1.1
date: 2026-11-12
status: Stable
---

# SCR-MTTO-001: Preventive Maintenance Scheduling Form (Calendar Intervals)

## 1. Purpose and Operational Context

* **View Objective:** Centralized configuration form for creating, calibrating, and scheduling recurring preventive maintenance plans based exclusively on calendar time intervals (weeks or months). Links plans to ISO 14224 taxonomic levels (Equipment Unit Level 6, Subunit Level 7, Maintainable Item Level 8), enforces physical battery limits verification ([MTTO-029](../../../requirements/user-stories/mtto/MTTO-029.md)), estimates required labor resources (Wrench Time in Man-Hours), calculates the initial RIME priority score ($Score = \text{Criticality} \times \text{Work Class Weight}$), and automatically projects the initial Work Order into `PLANNING` status.
* **Primary Target Persona:** Maintenance Planner defining recurring preventive maintenance cadences, balancing workload hours, and assigning maintenance specialties to prevent catastrophic equipment wear (ISO 55001 §8.1).
* **Secondary Personas:**
  * **Maintenance Supervisor:** Reviews projected preventive work orders and verifies craft availability.
  * **Reliability Engineer:** Verifies taxonomic boundary compliance and receives optimization alerts when inspection cadences on high-criticality assets exceed recommended limits.
* **Operational Context:** Planning control rooms and engineering workstations and supervisory industrial tablets in landscape orientation.
* **Mode of Operation:** Supervisory Technical Configuration mode. Focuses on master plan parameterization, resource allocation, and automated work order projection. Direct DCS/SCADA process control manipulation is strictly excluded.
* **Web Portal Workspace Invariant:** Operates as a Level 3 technical form within the Blazor Web Portal shell (`Pages/Maintenance/CreatePreventivePlanPage.razor`), accessible directly from the Maintenance menu or via drill-down from the RIME Backlog Dashboard ([SCR-MTTO-026](./SCR-MTTO-026.md)).

---

## 2. Visual Artifact

### 2.1. Preventive Maintenance Scheduling Form (Dark Theme)
![SCR-MTTO-001 Screenshot](assets/SCR-MTTO-001-screenshot.png)

> *Note: Production UI prototype capture illustrating the Web Portal layout at 1280×800 in Dark Theme. Exhibits the portal navigation sidebar (CMP-01), sticky breadcrumb header (CMP-02), cascading ISO 14224 selector (CMP-03), boundary limit verification badge (CMP-04), calendar cadence controller (CMP-05), labor estimation grid (CMP-07), RIME score decomposition (CMP-09), and grounded action footer (CMP-12).*

### 2.2. Preventive Maintenance Scheduling Form (Light Theme)
![SCR-MTTO-001 Light](assets/SCR-MTTO-001-light.png)

> *Note: Production UI prototype capture illustrating the Web Portal layout at 1280×800 in Light Theme.*

---

## 3. Functional Component Inventory

> The base grid, typography, neutral palettes, and minimal tactile contact areas are inherited from [DT-UI-DS-DOC-001](../../DT-UI-DS-DOC-001.md). This inventory defines the canonical components present on the screen, their design tokens, and their architectural scope. Interaction rules and geometric algorithms are specified in Section 5; responsive container adaptations are governed by Section 8.

1. **`CMP-01`: Portal Sidebar Navigation** (`PortalSidebarNav.razor`)
   - **Visual Role:** Collapsible persistent sidebar providing access to core modules (Digital Twin, Work Orders, Maintenance Plans, Asset Inventory, Governance).
   - **Design Tokens:**
     - Width (Expanded): `--dt-layout-sidebar-width-expanded`
     - Width (Collapsed): `--dt-layout-sidebar-width-collapsed`
     - Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Active Route Indicator: `--dt-color-state-info`
   - **Architectural Scope:** Hosts shared application routing, collapsible state (`IsCollapsed`), and active route tracking (`ActiveRouteCode = "SCR-MTTO-001"`). Detailed in §8.

2. **`CMP-02`: Form Breadcrumbs & Header** (`FormBreadcrumbHeader.razor`)
   - **Visual Role:** Sticky top bar presenting hierarchical breadcrumb path (*"Maintenance › Preventive Plans › Calendar Scheduling"*), active asset tag pill, and backlink to [SCR-MTTO-026](./SCR-MTTO-026.md).
   - **Design Tokens:**
     - Surface: `--dt-color-surface-base`
     - Border: `--dt-color-border-subtle`
     - Typography: `--dt-font-body-md`, `--dt-font-mono-data`
     - Height: `--dt-control-height-lg`
   - **Architectural Scope:** Establishes spatial orientation and session metadata (`OperatorBadgeCode`, `OperatorDisplayName`).

3. **`CMP-03`: Cascading ISO 14224 Selector** (`IsoHierarchyCascadingSelector.razor`)
   - **Visual Role:** Three-tier taxonomic dropdown hierarchy: Equipment Unit L6 (`P-0101A`), Subunit L7 (`Sealing System`), and Maintainable Item L8 (`Mechanical Seal`).
   - **Design Tokens:**
     - Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Control Height: `--dt-control-height-lg`
     - Radius: `--dt-radius-md`
   - **Architectural Scope:** Enforces ISO 14224 taxonomic constraints (`FR-001`, `TR-008`), dynamically filtering child units upon parent selection and managing cascading state resets.

4. **`CMP-04`: Boundary Limits Verification Badge** (`BoundaryComplianceBadge.razor`)
   - **Visual Role:** Real-time compliance badge verifying whether the selected asset has defined physical battery limits (`BoundaryStart`, `BoundaryEnd` per [MTTO-029](../../../requirements/user-stories/mtto/MTTO-029.md)).
   - **Design Tokens:**
     - Radius: `--dt-radius-full`
     - Valid Surface: `--dt-color-state-success`
     - Warning Surface: `--dt-color-alarm-warning`
   - **Architectural Scope:** Hard-blocks plan registration if battery limits are undefined (`AF-002`), guaranteeing cost and downtime attribution accuracy.

5. **`CMP-05`: Calendar Cadence Controller** (`CalendarCadenceController.razor`)
   - **Visual Role:** Numeric interval stepper ($1..104$) paired with time unit selector (`Weeks`, `Months`, `Days`, `Years`) and quick-select industrial cadence chips.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Typography: `--dt-font-mono-data`
     - Control Height: `--dt-control-height-lg`
   - **Architectural Scope:** Captures calendar frequency parameters (`FR-002`) and triggers instantaneous execution date calculation (`CMP-06`).

6. **`CMP-06`: Next Work Order Date Indicator** (`NextExecutionDatePreview.razor`)
   - **Visual Role:** Real-time projected execution date preview calculated from current baseline date and cadence parameters.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-raised`
     - Font: `--dt-font-mono-data`
     - Border: `--dt-color-border-subtle`
   - **Architectural Scope:** Previews `NextWorkOrderDate` (`FR-003`) client-side in $< 50\text{ms}$ without server roundtrips.

7. **`CMP-07`: Labor & Resource Estimation Grid** (`LaborEstimationCard.razor`)
   - **Visual Role:** Numeric input for Estimated Active Wrench Time ($1.0..120.0\text{ Man-Hours}$) and craft specialty selector (`Mechanical`, `Electrical`, `Instrumentation`).
   - **Design Tokens:**
     - Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Control Height: `--dt-control-height-lg`
   - **Architectural Scope:** Captures craft specialty and wrench time allocations, validating positive non-zero values (`AF-001`).

8. **`CMP-08`: Plan Scope & SOP Linkage Textarea** (`PlanScopeEditor.razor`)
   - **Visual Role:** Multiline input capturing technical narrative, standard operating procedure (SOP) references, and safety isolation requirements.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Typography: `--dt-font-body-md`
   - **Architectural Scope:** Stores detailed technical scope dispatched to projected Work Orders.

9. **`CMP-09`: RIME Priority Preview Card** (`RimePriorityPreview.razor`)
   - **Visual Role:** Real-time decomposition of asset criticality ($1..10$), Work Class weight (default 6 for Systematic PM, 7 for Regulated PM), and calculated RIME Score ($C \times W$) with redundant priority badge.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-card`
     - Border: `--dt-color-border-subtle`
     - Typography: `--dt-font-mono-data`
   - **Architectural Scope:** Computes initial RIME triage priority per ISO 55001 planning standards and passes priority rating to the instantiated Work Order.

10. **`CMP-10`: High-Criticality Interval Alert Modal & Advisory Pill** (`HighCriticalityAlertBanner.razor`)
    - **Visual Role:** Subtle inline advisory indicator on the main canvas (`#cadenceSoftBadge`) deployed when Asset Criticality $\ge 8$ and selected interval $> 8\text{ weeks}$, complemented by a modal dialog (`#cadenceModalBackdrop`) intercepted prior to persistence requiring mandatory technical justification or one-click adjustment to $\le 8\text{ weeks}$.
    - **Design Tokens:**
      - Modal Backdrop: `rgba(15, 23, 42, 0.55)` with backdrop blur `--dt-space-1`
      - Modal Surface: `--dt-color-surface-card`
      - Border: `--dt-color-border-subtle`
      - Advisory Pill: `rgba(217, 119, 6, 0.08)` with border `--dt-color-alarm-warning`
      - Radius: `--dt-radius-xl`
    - **Architectural Scope:** Implements RCM optimization governance (`AF-003`), enforcing justified exceptions on critical infrastructure without causing layout shift (`CLS = 0`) on the primary form.

11. **`CMP-11`: Projected Work Order Preview Card** (`ProjectedWorkOrderCard.razor`)
    - **Visual Role:** Read-only preview card displaying the first Work Order to be automatically created in `PLANNING` status upon plan confirmation.
    - **Design Tokens:**
      - Surface: `--dt-color-surface-card`
      - Border: `--dt-color-state-info`
      - Typography: `--dt-font-caption`, `--dt-font-mono-data`
    - **Architectural Scope:** Previews initial work order attributes (`ScheduledDate`, `WorkClass`, `Status`, `EstimatedCost`) prior to atomic commit (`FR-005`).

12. **`CMP-12`: Plan Confirmation & Action Bar** (`FormActionFooter.razor`)
    - **Visual Role:** Grounded footer action bar hosting *"Cancel"* and *"Save & Instantiate Plan"* primary action buttons paired with inline validation pill.
    - **Design Tokens:**
      - Surface: `--dt-color-surface-card`
      - Border: `--dt-color-border-subtle`
      - Primary CTA: `--dt-color-state-info`
      - Height: `--dt-layout-footer-height`
    - **Architectural Scope:** Enforces single-commit atomic creation of `MaintenancePlan` and initial `WorkOrder` (`NFR-007`); hard-disabled until all mandatory fields and boundary checks are satisfied.

---

## 4. Screen State Catalog

1. **Normal / Empty Form**
   - **Activation Condition:** Planner accesses "Create Preventive Plan" prior to asset selection.
   - **Visual Modification:** Form fields render empty or with default prompts. `CMP-04` renders neutral placeholder badge. Primary commit CTA `CMP-12` is disabled (`--dt-color-state-disabled`).
2. **Asset Selected & Validated**
   - **Activation Condition:** Planner selects a valid Level 6 Equipment Unit with defined battery limits.
   - **Visual Modification:** `CMP-04` displays Teal badge (`--dt-color-state-success`): *"Physical Boundaries Verified (ISO 14224)"*. Subunit and Maintainable Item dropdowns become active. RIME score card populates with asset criticality.
3. **Boundary Missing Blocked (`AF-002`)**
   - **Activation Condition:** Selected asset has `BoundaryStart` or `BoundaryEnd` as null or empty (`AF-002`).
   - **Visual Modification:** `CMP-04` displays red status pill (`--dt-color-alarm-critical`): *"Physical Boundaries Missing"*. Bottom action footer displays contextual feedback banner: *"Action blocked: Define physical battery limits in asset catalog prior to scheduling."* Primary CTA `CMP-12` is completely disabled with muted grayscale styling and informative tooltip. Form submission is hard-blocked.
4. **High Criticality Alert & Governance Modal (`AF-003`)**
   - **Activation Condition:** Asset Criticality $\ge 8$ and selected interval $> 8\text{ weeks}$ (`AF-003`).
   - **Visual Modification:** Subtle warning pill `CMP-10` activates beneath cadence preset chips: *"Requires technical justification upon save (> 8 weeks on critical asset)"*. When the user clicks *"Save and Schedule Preventive Plan"*, an L4 modal dialog intercepts the workflow, requiring $\ge 15$ characters of technical justification or offering a one-click *"Adjust to 8 Weeks"* remediation action.
5. **Missing Mandatory Fields (`AF-001`)**
   - **Activation Condition:** Planner attempts to submit form without satisfying mandatory constraints (e.g., zero labor hours, unselected item, empty scope) (`AF-001`).
   - **Visual Modification:** Omitted inputs highlight with amber outline (`--dt-color-alarm-warning`, $2\text{px}$) and warning icon `#icon-warning`. Inline footer pill indicates: *"Mandatory fields required: Asset, Subunit, Item, Frequency, Man-Hours, Description."*
6. **Saving / Instantiating**
   - **Activation Condition:** Planner activates *"Save & Instantiate Plan"*.
   - **Visual Modification:** Primary CTA `CMP-12` renders skeleton shimmer and loading indicator (*"Saving Plan and Instantiating WO..."*). Form inputs are locked.
7. **Plan Created (Success)**
   - **Activation Condition:** Atomic persistence of plan and initial work order completes in $< 1\text{s}$ (`NFR-008`).
   - **Visual Modification:** Form displays green success alert banner (`--dt-color-state-success`), shows generated Work Order ID (`WO-2026-PLAN-XXXX`), and provides navigation links to *"View Active Plans"* or *"Create Another Plan"*.

---

## 5. Interaction Rules and Data Flow

### 5.1. Initial Load & Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Planner as Maintenance Planner
    participant UI as SCR-MTTO-001 Form
    participant TAX as Asset Taxonomy Service (tax)
    participant MTTO as Maintenance Planning Service (mtto)

    Planner->>UI: Accesses "Create Preventive Plan"
    UI->>TAX: Query Equipment Units (Level 6) & Master Classes
    TAX-->>UI: Returns active asset catalog
    Planner->>UI: Selects Equipment Unit (P-0101A)
    UI->>TAX: Check boundary_start & boundary_end (MTTO-029)
    alt Boundaries Configured
        TAX-->>UI: Boundaries Validated (CMP-03 Teal)
        UI->>TAX: Load Subunits (L7) & Maintainable Items (L8)
        TAX-->>UI: Populates cascading selectors (CMP-02)
    else Boundaries Missing (AF-002)
        TAX-->>UI: Boundaries NULL
        UI->>UI: Blocks submission & deploys AF-002 error alert
    end
    Planner->>UI: Selects Subunit, Item, Frequency (12 Weeks), Man-Hours (4.0 HH)
    UI->>UI: Evaluates Criticality (9) vs. Interval (12 Wks) -> Deploys AF-003 Warning
    Planner->>UI: Confirms 8 Weeks or enters justification
    Planner->>UI: Clicks "Save & Instantiate Plan"
    UI->>MTTO: CreateMaintenancePlanCommand
    MTTO-->>UI: Returns PlanId & WorkOrderId
    UI-->>Planner: Renders success confirmation & projected execution date
```

1. **Taxonomic Hierarchy Loading:** When an Equipment Unit (Level 6) is selected, the system filters Subunits where `EquipmentUnitId` matches the selected asset. Selecting a Subunit dynamically loads Maintainable Items associated with the selected `SubunitId` (`FR-001`).
2. **Deterministic Next Date Calculation (`FR-003`):** The system calculates:
   $$\text{next\_work\_order\_date} = \text{CurrentDate} + (\text{IntervalValue} \times \text{UnitMultiplier})$$
   where $\text{UnitMultiplier} = 7\text{ days}$ for weeks, or $30.4375\text{ days}$ for months.
3. **Automatic Work Order Instantiation (`FR-005`):** On plan confirmation, the system persists the active `MaintenancePlan` (`status = 'ACTIVE'`, `interval_value`, `interval_unit`, `estimated_labor_hours`, `next_work_order_date`) and automatically instantiates the first preventative `WorkOrder` alongside its prioritized backlog triage entry:
   * `current_status = 'PLANNING'`
   * `maintenance_method = 'PREVENTIVE'`
   * `scheduled_date = :next_work_order_date`
   * `work_class = 6` (or `7` if Regulated PM is checked, persisted in the associated `WorkRequest` / `BacklogItem` triage context)
   * `priority_score = :asset_criticality * :work_class` (driving the work order `criticality` tier)

---

### 5.2. Form Mechanics & Cascading Selectors

1. **Cascading Reset Policy:** Modifying the Level 6 Equipment Unit automatically clears and resets Subunit and Maintainable Item selections. Modifying Subunit clears Maintainable Item.
2. **Frequency Presets:** The form provides quick-select chips for common industrial cadences: `1 Week` (Weekly lubrication), `4 Weeks` (Monthly inspection), `12 Weeks` (Quarterly seal check), `26 Weeks` (Semi-annual overhaul), `52 Weeks` (Annual turnaround).
3. **Spare Parts Verification (`CMP-11`):** Clicking "Verify Spare Parts" transitions the user to [SCR-INV-031](../inv/SCR-INV-031.md) with the context of the selected Maintainable Item pre-filtered, allowing the planner to confirm stock levels before finalizing the recurring schedule.

---

### 5.3. Domain Workflows & Validation Rules

#### 5.3.1. Physical Boundaries Validation (AF-002)
1. Per ISO 14224 (Section 5.6) and [MTTO-029](../../../requirements/user-stories/mtto/MTTO-029.md), maintenance costs and scopes cannot be ambiguously assigned.
2. The form checks `BoundaryStart` and `BoundaryEnd` on the selected Equipment Unit DTO. If either is null or whitespace:
   * The form displays `AF-002` error warning: *"Cannot schedule preventive maintenance on an asset without defined physical boundaries (ISO 14224). Request boundary configuration from the Reliability Engineer."*
   * The save button is completely disabled.

#### 5.3.2. High-Criticality Interval Warning (AF-003)
1. If $\text{AssetCriticality} \ge 8$ and the entered interval is $> 8\text{ weeks}$:
   * The banner `CMP-09` appears: *"For high criticality assets, it is recommended to schedule preventive plans with intervals less than or equal to 8 weeks. Do you want to proceed with the current frequency?"*
   * The Planner can click *"Adjust to 8 Weeks"* to automatically re-parameterize the cadence, or enter a technical justification in an override field to preserve the longer interval.

---

## 6. Industrial and Safety Considerations

* **ANSI/ISA-101 HPHMI Compliance ([TR-011](../../../requirements/common/TR-011.md)):** Form uses neutral grayscale surfaces (`--dt-color-surface-base`, `--dt-color-surface-card`). Color is strictly functional:
  * Green (`--dt-color-state-success`) for verified boundaries and successful plan creation.
  * Amber (`--dt-color-alarm-warning`) for missing mandatory fields (`AF-001`) and cadence optimization alerts (`AF-003`).
* **Taxonomic Data Hygiene ([TR-008](../../../requirements/common/TR-008.md)):** Prevents generic "free-text" maintenance planning. By enforcing ISO 14224 Levels 6, 7, and 8, maintenance history is cleanly attributed to maintainable items, enabling accurate MTBF and Pareto failure analytics.
* **Wrench Time Estimation:** Labor hours are captured as pure active wrench time, adhering to modern EAM/CMMS engineering best practices.

---

## 7. Frontend Component Contract (Blazor / Razor)

### 7.1. Component Hierarchy & File Mapping

```text
Pages/Maintenance/
└── CreatePreventivePlanPage.razor                     # Root View (SCR-MTTO-001)
    ├── PortalSidebarNav.razor                         # CMP-01: Shared navigation sidebar
    ├── FormBreadcrumbHeader.razor                     # CMP-02: Header, breadcrumb, and backlink
    ├── IsoHierarchyCascadingSelector.razor            # CMP-03: L6 / L7 / L8 cascading dropdowns
    ├── BoundaryComplianceBadge.razor                 # CMP-04: Battery limits verification status
    ├── CalendarCadenceController.razor                # CMP-05: Cadence numeric stepper and unit picker
    ├── NextExecutionDatePreview.razor                 # CMP-06: Dynamic next execution date preview
    ├── LaborEstimationCard.razor                      # CMP-07: Active wrench time and craft specialty
    ├── PlanScopeEditor.razor                          # CMP-08: Scope narrative and SOP reference
    ├── RimePriorityPreview.razor                      # CMP-09: Real-time RIME score breakdown
    ├── HighCriticalityAlertBanner.razor               # CMP-10: Cadence optimization alert
    ├── ProjectedWorkOrderCard.razor                   # CMP-11: Instantiated WO preview
    └── FormActionFooter.razor                         # CMP-12: Grounded footer commit bar
```

---

### 7.2. Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)

#### 7.2.1. `CreatePreventivePlanPage.razor` (Root View)

```csharp
[Parameter]
public Guid? PreselectedEquipmentUnitId { get; set; }

[Parameter]
public string? PreselectedTagNumber { get; set; }
```

#### 7.2.2. Subcomponent Parameter Contracts (`CMP-01` to `CMP-12`)

```csharp
// CMP-01: PortalSidebarNav.razor
[Parameter]
public bool IsCollapsed { get; set; }

[Parameter]
public required string ActiveRouteCode { get; set; } = "SCR-MTTO-001";

[Parameter]
public EventCallback<bool> OnCollapseToggled { get; set; }

// CMP-02: FormBreadcrumbHeader.razor
[Parameter]
public required string OperatorBadgeCode { get; set; }

[Parameter]
public required string OperatorDisplayName { get; set; }

[Parameter]
public string? ActiveAssetTag { get; set; }

// CMP-03: IsoHierarchyCascadingSelector.razor
[Parameter]
public required IReadOnlyList<EquipmentUnitLookupDto> AvailableEquipment { get; set; }

[Parameter]
public Guid? SelectedEquipmentUnitId { get; set; }

[Parameter]
public EventCallback<Guid?> SelectedEquipmentUnitIdChanged { get; set; }

[Parameter]
public Guid? SelectedSubunitId { get; set; }

[Parameter]
public EventCallback<Guid?> SelectedSubunitIdChanged { get; set; }

[Parameter]
public Guid? SelectedMaintainableItemId { get; set; }

[Parameter]
public EventCallback<Guid?> SelectedMaintainableItemIdChanged { get; set; }

// CMP-04: BoundaryComplianceBadge.razor
[Parameter]
public bool HasDefinedBoundaries { get; set; }

[Parameter]
public string? BoundaryDescription { get; set; }

// CMP-05: CalendarCadenceController.razor
[Parameter]
public int IntervalValue { get; set; } = 12;

[Parameter]
public EventCallback<int> IntervalValueChanged { get; set; }

[Parameter]
public CalendarIntervalUnit IntervalUnit { get; set; } = CalendarIntervalUnit.WEEKS;

[Parameter]
public EventCallback<CalendarIntervalUnit> IntervalUnitChanged { get; set; }

// CMP-06: NextExecutionDatePreview.razor
[Parameter]
public DateOnly CalculatedNextDate { get; set; }

// CMP-07: LaborEstimationCard.razor
[Parameter]
public decimal EstimatedLaborHours { get; set; } = 4.0m;

[Parameter]
public EventCallback<decimal> EstimatedLaborHoursChanged { get; set; }

[Parameter]
public IReadOnlyList<MaintenanceCraft> RequiredCrafts { get; set; } = [MaintenanceCraft.MECHANICAL];

[Parameter]
public EventCallback<IReadOnlyList<MaintenanceCraft>> RequiredCraftsChanged { get; set; }

// CMP-08: PlanScopeEditor.razor
[Parameter]
public string TechnicalDescription { get; set; } = string.Empty;

[Parameter]
public EventCallback<string> TechnicalDescriptionChanged { get; set; }

// CMP-09: RimePriorityPreview.razor
[Parameter]
public int AssetCriticality { get; set; }

[Parameter]
public int WorkClassWeight { get; set; } = 6;

[Parameter]
public int CalculatedRimeScore { get; set; }

// CMP-10: HighCriticalityAlertBanner.razor
[Parameter]
public bool IsVisible { get; set; }

[Parameter]
public string? OverrideJustification { get; set; }

[Parameter]
public EventCallback<string?> OverrideJustificationChanged { get; set; }

[Parameter]
public EventCallback OnAdjustToRecommendedCadence { get; set; }

// CMP-11: ProjectedWorkOrderCard.razor
[Parameter]
public required ProjectedWorkOrderPreviewDto ProjectedWorkOrder { get; set; }

// CMP-12: FormActionFooter.razor
[Parameter]
public bool CanSubmit { get; set; }

[Parameter]
public bool IsSubmitting { get; set; }

[Parameter]
public string? ValidationMessage { get; set; }

[Parameter]
public EventCallback OnSavePlanConfirmed { get; set; }

[Parameter]
public EventCallback OnCancelClicked { get; set; }
```

#### 7.2.3. Data Transfer Objects (DTOs) and Enums

```csharp
public enum CalendarIntervalUnit
{
    DAYS,
    WEEKS,
    MONTHS,
    YEARS
}

public enum MaintenanceCraft
{
    MECHANICAL,
    ELECTRICAL,
    INSTRUMENTATION_AND_CONTROL,
    LUBRICATION,
    CONDITION_MONITORING,
    ELECTRONICS,
    WELDING_FABRICATION,
    FACILITIES
}

public record EquipmentUnitLookupDto
{
    public required Guid EquipmentUnitId { get; init; }
    public required string TagNumber { get; init; }
    public required string Name { get; init; }
    public required string EquipmentClassName { get; init; }
    public int Criticality { get; init; }
    public bool HasBoundaries { get; init; }
    public string? BoundaryStart { get; init; }
    public string? BoundaryEnd { get; init; }
}

public record SubunitLookupDto
{
    public required Guid SubunitId { get; init; }
    public required Guid EquipmentUnitId { get; init; }
    public required string SubunitName { get; init; }
}

public record MaintainableItemLookupDto
{
    public required Guid MaintainableItemId { get; init; }
    public required Guid SubunitId { get; init; }
    public required string ItemName { get; init; }
}

public record ProjectedWorkOrderPreviewDto
{
    public required string ProjectedWorkOrderNumber { get; init; }
    public required DateOnly ScheduledDate { get; init; }
    public required string Status { get; init; }
    public required int RimeScore { get; init; }
    public decimal EstimatedLaborCost { get; init; }
}

public record CreateMaintenancePlanCommand
{
    public required Guid EquipmentUnitId { get; init; }
    public required Guid SubunitId { get; init; }
    public required Guid MaintainableItemId { get; init; }
    public required int IntervalValue { get; init; }
    public required CalendarIntervalUnit IntervalUnit { get; init; }
    public required decimal EstimatedLaborHours { get; init; }
    public required IReadOnlyList<MaintenanceCraft> RequiredCrafts { get; init; }
    public required string TechnicalDescription { get; init; }
    public string? CadenceOverrideJustification { get; init; }
    public required string PlannerUserId { get; init; }
}

public record MaintenancePlanSummaryDto
{
    public required Guid PlanId { get; init; }
    public required string EquipmentTag { get; init; }
    public required string MaintainableItemName { get; init; }
    public required string FrequencyDescription { get; init; }
    public required DateOnly NextWorkOrderDate { get; init; }
    public required string Status { get; init; }
    public required Guid InitialWorkOrderId { get; init; }
    public required int RimeScore { get; init; }
}
```

---

### 7.3. Client-Side DOM & Interop Bridge

1. **Debounced Execution Date Bridge (`ICadenceDateInterop`):**
   - Recalculates `NextWorkOrderDate` instantaneously on the client thread ($< 50\text{ms}$) as interval numbers or units change, preventing UI blocking.
2. **Keyboard Focus & Form Progression (`IFormKeyNavigationInterop`):**
   - Supports natural `Tab` key cycling across inputs, `Enter` to submit when valid, and `Escape` to cancel.

---

## 8. Layout and Responsive Adaptability

### 8.1. Desktop Workstation (`--dt-breakpoint-xl`)
* **Layout Organization:** Full Web Portal shell with expanded navigation sidebar (`--dt-layout-sidebar-width-expanded`); workspace organizes into an asymmetric two-column technical configuration layout within `--dt-layout-form-max-width`. The primary technical canvas ($65\%$ width) hosts the sequential setup cards: Cascading ISO 14224 selector (`CMP-03`), Cadence controller (`CMP-05`), and Labor estimation (`CMP-07`). The right-hand governance rail ($35\%$ width) hosts Boundary verification badge (`CMP-04`), RIME score preview (`CMP-09`), and Projected Work Order card (`CMP-11`). Sticky action footer `CMP-12` (`--dt-layout-footer-height`) remains grounded at bottom.
* **Ergonomic Rules:** Mouse and keyboard navigation; form controls adhere to `--dt-control-height-lg`; dense legible technical typography (`--dt-font-body-md`, `--dt-font-mono-data`); zero horizontal scroll; zero layout shift (`CLS = 0`).

### 8.2. Industrial Tablet Landscape (`--dt-breakpoint-lg`)
* **Layout Organization:** Navigation sidebar collapses to an icon-only rail (`--dt-layout-sidebar-width-collapsed`); workspace organizes into a fluid dual-column layout or compact single-column stacked card sequence; cadence chips wrap naturally; technical cards preserve stacked key-value pairs; permanent sticky action footer (`--dt-layout-footer-height`) remains docked.
* **Ergonomic Rules:** Touch targets governed by `--dt-touch-target-mobile` with `--dt-space-2` separation for gloved operation; prominent numeric steppers and cadence preset chips.

### 8.3. Industrial Tablet Portrait (`--dt-breakpoint-md`)
* **Layout Organization:** Single-column vertical stack with full-width touch targets within `--dt-layout-form-max-width`; off-canvas navigation drawer triggered via top brand mark button in `CMP-02`; governance cards flow sequentially beneath configuration cards; bottom scroll clearance enforced via `--dt-layout-footer-clearance`. Sticky action footer `CMP-12` remains thumb-reachable.
* **Ergonomic Rules:** Gloved operation ergonomics with touch targets governed by `--dt-touch-target-mobile`; sticky bottom action footer (`CMP-12`) prevents thumb strain.

---

## 9. Traceability and Requirements Matrix

| Requirement | Addressed in Component | Verification & Implementation Mechanism |
| :--- | :--- | :--- |
| [FR-001](../../../requirements/user-stories/mtto/MTTO-001.md#functional-requirements-fr) | `CMP-03` | Cascading selection of Level 6 equipment unit, Level 7 subunit, and Level 8 maintainable item. |
| [FR-002](../../../requirements/user-stories/mtto/MTTO-001.md#functional-requirements-fr) | `CMP-05` | Plan creation form defines frequency strictly based on calendar time intervals (weeks/months). |
| [FR-003](../../../requirements/user-stories/mtto/MTTO-001.md#functional-requirements-fr) | `CMP-06` | Automatically calculates next Work Order date based on selected frequency and baseline. |
| [FR-004](../../../requirements/user-stories/mtto/MTTO-001.md#functional-requirements-fr) | `CMP-04`, `CMP-12` | Blocks saving plan if mandatory fields (equipment, item, frequency, labor hours, boundaries) are missing. |
| [FR-005](../../../requirements/user-stories/mtto/MTTO-001.md#functional-requirements-fr) | `CMP-11`, `CMP-12` | Automatically projects and instantiates first Work Order in `PLANNING` status upon confirmation. |
| [FR-006](../../../requirements/user-stories/mtto/MTTO-001.md#functional-requirements-fr) | `CMP-02`, `CMP-11` | Displays summary of plan tracking attributes (asset, item, frequency, next date, status). |
| [NFR-007](../../../requirements/user-stories/mtto/MTTO-001.md#non-functional-requirements-nfr) | `CMP-12` | Fault tolerance and offline queuing resilience for planning actions. |
| [NFR-008](../../../requirements/user-stories/mtto/MTTO-001.md#non-functional-requirements-nfr) | `CMP-03`, `CMP-05`, `CMP-06` | Interface responds to user interactions (cascading selection, date calc) in under 1 second. |
| [NFR-009](../../../requirements/user-stories/mtto/MTTO-001.md#non-functional-requirements-nfr) | `CMP-03` | Virtualized catalog loading supporting extensive taxonomy catalogs without UI lag. |
| [TR-005](../../../requirements/common/TR-005.md) | `CMP-01`, `CMP-03` | Encryption in Transit: Transport layer security (TLS/HTTPS) for all RESTful DTO transmissions and API calls. |
| [TR-006](../../../requirements/common/TR-006.md) | `CMP-02`, `CMP-12` | Role-Based Access Control (RBAC): Enforces permissions (`Maintenance Planner`, `Maintenance Supervisor`). |
| [TR-008](../../../requirements/common/TR-008.md) | `CMP-03`, `CMP-04` | ISO 14224 Hierarchy Management and Validation: Enforces taxonomic hierarchy and physical battery limits ([MTTO-029](../../../requirements/user-stories/mtto/MTTO-029.md)). |
| [TR-010](../../../requirements/common/TR-010.md) | `CMP-11`, `CMP-12` | Real-time synchronization: broadcasts generated preventive work order events to connected clients via WebSockets (< 1s). |
| [TR-011](../../../requirements/common/TR-011.md) | `CMP-01`..`CMP-12` | ANSI/ISA-101 HPHMI: 90/10 grayscale palette, functional alert color, and redundant coding. |
| [ADR-005](../../../architecture/adr/ADR-005.md) | `CMP-03`, `CMP-11` | Time-sequential UUIDv7 generation for plan and work order entities. |
