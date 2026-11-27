---
code: DT-UI-CTR-001
version: 1.0
date: 2026-11-27
status: Approved
author: Juan David Julio
standard:
  - ISO/IEC 25010:2023 (Maintainability — Modularity & Reusability)
  - ISA-101.01-2015 (Human Machine Interfaces for Process Automation Systems)
  - ISO 14224:2016 (Equipment Taxonomy & Boundary Limits)
  - WCAG 2.1 Level AA
---

# Shared UI Contracts & Component Parameter Catalog

## 1. Scope and Purpose

This document is the **Single Source of Truth (SSoT)** for reusable Blazor / Razor Class Library (RCL) component parameter contracts and shared lookup Data Transfer Objects (DTOs) referenced across the `SCR-*.md` screen specifications. Individual screen specifications define only screen-local view models, commands, and screen-specific widget contracts while linking here for shared shell, spatial HUD, lookup modal, and maintenance-planning kit interfaces.

* **Shared Domain Enums:** see [DT-DM-DOC-001 §4](../../domain-models/class/DT-DM-DOC-001.md#4-controlled-vocabulary).
* **Design Tokens & Visual Patterns:** see [DT-UI-DS-DOC-001](../DT-UI-DS-DOC-001.md) and [DT-UI-NAV-DOC-001](../DT-UI-NAV-DOC-001.md).
* **REST API & SignalR Contracts:** see [DT-ARQ-CMP-DOC-001 §5–§6](../../architecture/views/DT-ARQ-CMP-DOC-001.md#5-signalr-hub-and-real-time-event-contract-registry-tr-010).

---

## 2. Shared Lookup DTOs

All shared pagination, taxonomy, and catalog lookup DTOs below use canonical C# `record` types and fixed-point `decimal` precision where applicable ([DT-ARQ-CMP-DOC-001 §6](../../architecture/views/DT-ARQ-CMP-DOC-001.md#6-rest-api-prefix-concurrency-numeric-precision-conventions)).

```csharp
// Consumed by: SCR-MTTO-001, SCR-MTTO-023, SCR-MTTO-029
public record PagedLookupResultDto<T>
{
    public required IReadOnlyList<T> Items { get; init; }
    public required int TotalCount { get; init; }
    public required int PageNumber { get; init; }
    public required int PageSize { get; init; }
}

// Consumed by: SCR-MTTO-001, SCR-MTTO-023, SCR-MTTO-029
public record EquipmentUnitLookupQueryDto
{
    public string? SearchTerm { get; init; }
    public Guid? FunctionalLocationId { get; init; }
    public Guid? EquipmentClassId { get; init; }
    public int? MinCriticality { get; init; }
    public int? MaxCriticality { get; init; }
    public bool? HasBoundariesFilter { get; init; }
    public int PageNumber { get; init; } = 1;
    public int PageSize { get; init; } = 25;
}

// Consumed by: SCR-MTTO-001, SCR-MTTO-023, SCR-MTTO-029
public record EquipmentUnitLookupDto
{
    public required Guid EquipmentUnitId { get; init; }
    public required string TagNumber { get; init; }
    public required string Name { get; init; }
    public required string SerialNumber { get; init; }
    public required string Model { get; init; }
    public string? FunctionalLocationTag { get; init; }
    public required string EquipmentClassName { get; init; }
    public int? Criticality { get; init; }
    public required EquipmentLifecycleStatus LifecycleStatus { get; init; }
    public int MappedSignalCount { get; init; }
    public required bool HasBoundaries { get; init; }
    public string? BoundaryStart { get; init; }
    public string? BoundaryEnd { get; init; }
    public required int SubunitCount { get; init; }
    public required int MaintainableItemCount { get; init; }
}

// Consumed by: SCR-MTTO-029
/// <summary>
/// Paged query for Subunit-scoped Maintainable Items. Because <c>maintainable_items.subunit_id</c> is <c>NOT NULL</c>
/// (DT-ERD-001.sql), items are always created and managed under a parent <c>Subunit</c> (never an unassigned pool).
/// </summary>
public record MaintainableItemLookupQueryDto
{
    public string? SearchTerm { get; init; }
    public string? SparePartType { get; init; }
    public Guid? EquipmentUnitId { get; init; }
    public Guid? SubunitId { get; init; }
    public int PageNumber { get; init; } = 1;
    public int PageSize { get; init; } = 25;
}

// Consumed by: SCR-MTTO-001, SCR-MTTO-023, SCR-MTTO-029
/// <summary>
/// Level 8 Maintainable Item lookup projection. Because <c>maintainable_items.subunit_id</c> is <c>NOT NULL</c>
/// (DT-ERD-001.sql) and <c>subunits.equipment_unit_id</c> is <c>NOT NULL</c>, every item always belongs to a parent
/// <c>Subunit</c> and owning <c>EquipmentUnit</c> (<see cref="AssignedEquipmentUnitId"/> is non-null).
/// </summary>
public record MaintainableItemLookupDto
{
    public required Guid MaintainableItemId { get; init; }
    public required Guid SubunitId { get; init; }
    public required string ComponentName { get; init; }
    public required string SubunitType { get; init; }
    public string? SparePartType { get; init; }
    public required MaintainableItemStatus Status { get; init; }
    public required Guid AssignedEquipmentUnitId { get; init; }
    public string? AssignedEquipmentTag { get; init; }
    public IReadOnlyDictionary<string, string> DesignAttributes { get; init; } = new Dictionary<string, string>();
    public IReadOnlyList<LinkedSparePartSummaryDto> LinkedSpareParts { get; init; } = [];
}

// Consumed by: SCR-MTTO-001, SCR-MTTO-023, SCR-MTTO-029
public record LinkedSparePartSummaryDto
{
    public required Guid SparePartId { get; init; }
    public required string Sku { get; init; }
    public required string Description { get; init; }
    public required string UnitOfMeasure { get; init; }
}

// Consumed by: SCR-INV-005, SCR-INV-031
public record EquipmentClassLookupDto
{
    public required Guid EquipmentClassId { get; init; }
    public required string ClassName { get; init; }
    public string? Description { get; init; }
    public string? ManufacturerStandard { get; init; }
}

// Consumed by: SCR-MTTO-001, SCR-MTTO-023
public record SubunitLookupDto
{
    public required Guid SubunitId { get; init; }
    public required Guid EquipmentUnitId { get; init; }
    public required string SubunitName { get; init; }
}
```

---

## 3. Shared Razor Component Parameter Contracts

### 3.1. Application Shell Navigation

#### `PortalSidebarNav.razor`
* **Consumed by:** `SCR-ADM-013`, `SCR-ADM-014`, `SCR-ADM-032`, `SCR-INV-005`, `SCR-INV-006`, `SCR-INV-027`, `SCR-INV-031`, `SCR-MTTO-001`, `SCR-MTTO-023`, `SCR-MTTO-026`, `SCR-MTTO-029`.

```csharp
[Parameter]
public bool IsCollapsed { get; set; }

[Parameter]
public bool IsMobileDrawerOpen { get; set; }

[Parameter]
public string? ActiveRouteCode { get; set; }

[Parameter]
public EventCallback<bool> OnCollapseToggled { get; set; }

[Parameter]
public EventCallback<bool> OnMobileDrawerToggled { get; set; }
```

---

### 3.2. Spatial Viewport & HUD Kit

#### `CanvasViewport2D.razor`
* **Consumed by:** `SCR-VIS-011`, `SCR-VIS-033`.

```csharp
[Parameter]
public required string SvgContent { get; set; }

[Parameter]
public double ZoomScale { get; set; } = 1.0;

[Parameter]
public string? FunctionalLocationCode { get; set; }

[Parameter]
public IReadOnlyList<EquipmentHotspotDto>? Hotspots { get; set; }

[Parameter]
public string? SelectedEquipmentTag { get; set; }

[Parameter]
public EventCallback<string> OnEquipmentSelected { get; set; }

[Parameter]
public EventCallback OnEmptyCanvasClicked { get; set; }

[Parameter]
public string? TargetEquipmentTag { get; set; }

[Parameter]
public IReadOnlyList<CutoffPointStatusDto>? CutoffPoints { get; set; }

[Parameter]
public string? SelectedCutoffNodeId { get; set; }

[Parameter]
public bool IsFocalDeemphasisActive { get; set; } = true;

[Parameter]
public EventCallback<string> OnCutoffNodeSelected { get; set; }
```

#### `ViewportToolbar.razor`
* **Consumed by:** `SCR-VIS-008`, `SCR-VIS-011`, `SCR-VIS-033`.

```csharp
[Parameter]
public string? SearchQuery { get; set; }

[Parameter]
public EventCallback<string?> OnSearchQueryChanged { get; set; }

[Parameter]
public double ZoomScale { get; set; } = 1.0;

[Parameter]
public bool? IsLayersActive { get; set; }

[Parameter]
public EventCallback<bool> OnLayersToggled { get; set; }

[Parameter]
public bool? IsPtwLayerActive { get; set; }

[Parameter]
public int? SimopsConflictCount { get; set; }

[Parameter]
public int? OrphanPermitsCount { get; set; }

[Parameter]
public bool? IsIntegrityDrawerOpen { get; set; }

[Parameter]
public EventCallback OnZoomInRequested { get; set; }

[Parameter]
public EventCallback OnZoomOutRequested { get; set; }

[Parameter]
public EventCallback OnResetViewRequested { get; set; }

[Parameter]
public EventCallback<bool> OnPtwLayerToggled { get; set; }

[Parameter]
public EventCallback OnSimopsConflictBadgeClicked { get; set; }

[Parameter]
public EventCallback OnOrphanBadgeClicked { get; set; }
```

#### `UserProfileButton.razor`
* **Consumed by:** `SCR-VIS-008`, `SCR-VIS-011`, `SCR-VIS-033`.

```csharp
[Parameter]
public required string UserInitials { get; set; }

[Parameter]
public EventCallback OnProfileMenuRequested { get; set; }
```

#### `CartographicHud.razor`
* **Consumed by:** `SCR-VIS-008`, `SCR-VIS-011`, `SCR-VIS-033`.

```csharp
[Parameter]
public double ZoomScale { get; set; } = 1.0;

[Parameter]
public double ScaleRatioMetersPerUnit { get; set; } = 0.2;
```

---

### 3.3. Shared Maintenance Planning Form Kit

#### `FormBreadcrumbHeader.razor`
* **Consumed by:** `SCR-MTTO-001`, `SCR-MTTO-023`.

```csharp
[Parameter]
public required string OperatorBadgeCode { get; set; }

[Parameter]
public required string OperatorDisplayName { get; set; }

[Parameter]
public string? ActiveAssetTag { get; set; }

[Parameter]
public string? ActiveSignalTag { get; set; }

[Parameter]
public decimal? InitialTargetLimit { get; set; }

[Parameter]
public MaintenancePlanStatus PlanStatus { get; set; } = MaintenancePlanStatus.DRAFT;

[Parameter]
public EventCallback OnBackToBacklogClicked { get; set; }
```

#### `IsoHierarchyCascadingSelector.razor`
* **Consumed by:** `SCR-MTTO-001`, `SCR-MTTO-023`.

```csharp
[Parameter]
public IReadOnlyList<EquipmentUnitLookupDto>? AvailableEquipment { get; set; }

[Parameter]
public Guid? SelectedEquipmentUnitId { get; set; }

[Parameter]
public EventCallback<Guid?> SelectedEquipmentUnitIdChanged { get; set; }

[Parameter]
public EquipmentUnitLookupDto? SelectedEquipmentUnit { get; set; }

[Parameter]
public EventCallback OnOpenEquipmentLookupModal { get; set; }

[Parameter]
public required IReadOnlyList<SubunitLookupDto> AvailableSubunits { get; set; }

[Parameter]
public required IReadOnlyList<MaintainableItemLookupDto> AvailableMaintainableItems { get; set; }

[Parameter]
public Guid? SelectedSubunitId { get; set; }

[Parameter]
public EventCallback<Guid?> SelectedSubunitIdChanged { get; set; }

[Parameter]
public Guid? SelectedMaintainableItemId { get; set; }

[Parameter]
public EventCallback<Guid?> SelectedMaintainableItemIdChanged { get; set; }

[Parameter]
public bool HasDefinedBoundaries { get; set; }

[Parameter]
public string? BoundaryDescription { get; set; }

[Parameter]
public EventCallback OnInspectBoundariesRequested { get; set; }
```

#### `LaborEstimationCard.razor`
* **Consumed by:** `SCR-MTTO-001` (defaults: `4.0m`, `[MaintenanceCraft.MECHANICAL]`), `SCR-MTTO-023` (defaults: `6.0m`, `[MaintenanceCraft.CONDITION_MONITORING]`).

```csharp
[Parameter]
public decimal EstimatedLaborHours { get; set; }

[Parameter]
public EventCallback<decimal> EstimatedLaborHoursChanged { get; set; }

[Parameter]
public IReadOnlyList<MaintenanceCraft> RequiredCrafts { get; set; } = [];

[Parameter]
public EventCallback<IReadOnlyList<MaintenanceCraft>> RequiredCraftsChanged { get; set; }
```

#### `PlanScopeEditor.razor`
* **Consumed by:** `SCR-MTTO-001`, `SCR-MTTO-023`.

```csharp
[Parameter]
public string TechnicalDescription { get; set; } = string.Empty;

[Parameter]
public EventCallback<string> TechnicalDescriptionChanged { get; set; }
```

#### `RimePriorityPreview.razor`
* **Consumed by:** `SCR-MTTO-001` (default `WorkClassWeight = 6`), `SCR-MTTO-023` (default `WorkClassWeight = 5`).

```csharp
[Parameter]
public int AssetCriticality { get; set; }

[Parameter]
public int WorkClassWeight { get; set; }

[Parameter]
public int CalculatedRimeScore { get; set; }
```

#### `ProjectedWorkOrderCard.razor`
* **Consumed by:** `SCR-MTTO-001` (`TPreview = CalendarWorkOrderPreviewDto`), `SCR-MTTO-023` (`TPreview = CbmWorkOrderPreviewDto`).

```csharp
// Typed generic parameter TPreview bound to CalendarWorkOrderPreviewDto (SCR-MTTO-001)
// or CbmWorkOrderPreviewDto (SCR-MTTO-023)
[Parameter]
public required TPreview ProjectedWorkOrder { get; set; }

[Parameter]
public EventCallback OnVerifySparePartsRequested { get; set; }
```

#### `FormActionFooter.razor`
* **Consumed by:** `SCR-MTTO-001`, `SCR-MTTO-023`.

```csharp
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

---

### 3.4. Enterprise Relational Entity Lookup Modal (`DT-UI-DS-DOC-001 §6.7`)

#### `EquipmentLookupModal.razor`
* **Consumed by:** `SCR-MTTO-023`, `SCR-MTTO-029` (Tier A Reference Contract per [DT-UI-DS-DOC-001 §6.7](../DT-UI-DS-DOC-001.md#67-relational-entity-lookup-modal-pattern-lov-list-of-values)).

```csharp
[Parameter]
public bool IsOpen { get; set; }

[Parameter]
public required EquipmentUnitLookupQueryDto Query { get; set; }

[Parameter]
public EventCallback<EquipmentUnitLookupQueryDto> OnQueryChanged { get; set; }

[Parameter]
public required IReadOnlyList<EquipmentUnitLookupDto> SearchResults { get; set; }

[Parameter]
public int TotalCount { get; set; }

[Parameter]
public Guid? SelectedEquipmentUnitId { get; set; }

[Parameter]
public EventCallback<EquipmentUnitLookupDto> OnEquipmentUnitSelected { get; set; }

[Parameter]
public EventCallback OnCloseRequested { get; set; }
```
