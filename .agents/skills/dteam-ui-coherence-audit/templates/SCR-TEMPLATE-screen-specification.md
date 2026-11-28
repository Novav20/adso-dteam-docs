---
id: SCR-MOD-000
title: Functional Screen Title
module: VIS | MTTO | INV | ADM
isa101_level: N/A | L1 (COP - Overview) | L2 (Process Area Schematic) | L3 (Equipment Task Faceplate) | L4 (Diagnostic / Master Detail)
platform: Shared Component | Desktop Web | Mobile
target_device: Industrial Tablet | Desktop
roles:
  - Primary Persona Role
  - Secondary Persona Role
user_stories:
  - "[[US-ID]]"
use_cases:
  - "[[UC-ID]]"
version: 1.0
date: YYYY-MM-DD
status: Draft | In Review | Stable
---

# SCR-MOD-000: Functional Screen Title

## 1. Purpose and Operational Context
* **View Objective:** Concise operational goal and cognitive task achieved on this screen.
* **Primary Target Persona:** Target role dictating ergonomics, touch targets, and density.
* **Secondary Personas:** Secondary roles with supervisory, read-only, or auditing access.
* **Operational Context:** Physical environment and device form factor qualitatively (no `--dt-breakpoint-*`, pixel/vh dimensions, or enum lists).
* **Mode of Operation:** Supervisory monitoring, passive inspection, transactional execution, or safety interlock (explicitly exclude DCS/SCADA control).

---

## 2. Visual Artifact

![SCR-MOD-000 Screenshot](assets/SCR-MOD-000-screenshot.png)

> *High-resolution PNG capture of the companion HTML prototype (`scr-mod-000.html`). Standalone SVG wireframes are prohibited.*

---

## 3. Functional Component Inventory

> Base grid, palette, typography, and touch targets inherit from [DT-UI-DS-DOC-001](../../DT-UI-DS-DOC-001.md). Keep cells limited to visual role, semantic `--dt-*` tokens, and architectural pointers to §5/§8 (no algorithms, math, status lists, or NFR IDs; no static pseudo-badges).

| ID | Control / Component | Visual Role / Content | Semantic Token | Architectural Role & Reference |
| :--- | :--- | :--- | :--- | :--- |
| `CMP-01` | `PortalSidebarNav` | Persistent collapsible module navigation rail. | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle` | Shared shell contract in [DT-UI-CTR-001 §3.1](../../contracts/DT-UI-CTR-001.md#31-application-shell-navigation). |
| `CMP-02` | Screen-Specific Component | Primary workspace container or form card. | Surface: `--dt-color-surface-base`<br>Focus: `--dt-color-border-focus` | Interaction mechanics in §5; responsive rules in §8. |

---

## 4. Screen State Matrix

| State | Visual Modification in the Interface | Activation Condition |
| :--- | :--- | :--- |
| **Normal (Default)** | Neutral grayscale surfaces and neutral controls in baseline state. | Initial view load with valid data and zero active alarms. |
| **Loading** | Shimmer skeleton or subdued progress bar inside fixed containers (`CLS = 0`). | Asynchronous fetch or spatial model initialization in progress. |
| **Selected** | Target entity highlighted with neutral selection ring; detail panel active. | User click/tap on entity row, spatial hotspot, or search match. |
| **Alarm / Alert** | Redundant coding (ANSI/ISA-101 geometric icon `#icon-*` + alarm token). | Safety interlock (`SOD-*`), limit excursion, or threshold trip. |
| **Diagnostic / Offline** | Priority 4 muted slate badge/banner (`#icon-*` stale icon + UTC timestamp). | Telemetry heartbeat loss or network partition ([ADR-006](../../../architecture/adr/ADR-006.md)). |

---

## 5. Interaction Rules and Data Flow

### 5.1. Initial Load & Lifecycle
1. Initial route parameters, baseline zoom/unselected state, and SignalR subscriptions registered in [DT-ARQ-CMP-DOC-001 §5](../../../architecture/views/DT-ARQ-CMP-DOC-001.md#5-signalr-hub-and-real-time-event-contract-registry-tr-010).
2. Mermaid sequence diagrams model `Actor -> UI -> ClientInterop -> API` only (no backend DB/Worker hops).

### 5.2. Spatial Navigation & Tactile Mechanics
1. Input disambiguation (wheel zoom/middle-click pan vs. $4\text{px}$ touch pan threshold) and snap hysteresis.
2. Layout shift invariants (`CLS = 0`, fixed control widths `--dt-control-width-*`, sticky footer `--dt-layout-footer-height`).

### 5.3. Domain Workflows & Data Mutation
1. Bind inputs to screen-local DTOs (§7.2.3) and shared enums in [DT-DM-DOC-001 §4](../../../domain-models/class/DT-DM-DOC-001.md#4-controlled-vocabulary). Do not enumerate enum string sets in prose or LaTeX.
2. Command dispatch references registered routes in [DT-ARQ-CMP-DOC-001 §6.1](../../../architecture/views/DT-ARQ-CMP-DOC-001.md#61-canonical-rest-endpoint-catalog), `X-Idempotency-Key` (`ADR-007`), and `If-Match` / `ConcurrencyToken` (`xmin`) on mutable roots (never on WORM ledgers).
3. Audit-logged actions follow [ADR-003](../../../architecture/adr/ADR-003.md) (`AuditJustification >= 15` chars; optional client preview digest only — never transmit `PreviousHash` in commands).
4. **Offline Synchronization Protocol:** When offline writes apply, point directly to the 5-step `SyncOutbox` protocol in [ADR-006](../../../architecture/adr/ADR-006.md#2-canonical-offline-synchronization-outbox-protocol-5-steps) rather than duplicating outbox SQL/retry steps.

---

## 6. Industrial and Safety Considerations

* **HPHMI & Alarm Discipline ([TR-011](../../../requirements/common/TR-011.md)):** 90/10 grayscale baseline; Priority 4 diagnostic loss uses neutral slate, never process alarm colors.
* **Safety Constants & SoD ([DT-DM-DOC-001 §5](../../../domain-models/class/DT-DM-DOC-001.md#5-domain-invariants-and-physical-safety-constants)):** Reference canonical thresholds (`0.0 V`, `0.5 psig`, `15 m`, `13 m`, `5 m`) and `SOD-*` rules (`SOD-SAF-01`, `SOD-INV-01`, `SOD-MTTO-01`, `SOD-SYS-01`).
* **Typography & Neutrality:** Use `--dt-font-mono-data`, `--dt-font-body-md`, `--dt-font-caption`, and neutral focus tokens (`--dt-color-border-focus`, `--dt-color-text-muted`).

---

## 7. Frontend Component Contract (Blazor / Razor)

### 7.1. Component Hierarchy & File Mapping

```text
Pages/
└── ScreenNamePage.razor                       # Root View (SCR-MOD-000)
    ├── PortalSidebarNav.razor                 # CMP-01: Shared shell (DT-UI-CTR-001 §3.1)
    └── ScreenLocalWidget.razor                # CMP-02: Screen-local subcomponent
```

### 7.2. Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)

#### 7.2.1. `ScreenNamePage.razor` (Root View)
```csharp
[Parameter, SupplyParameterFromQuery(Name = "entityId")]
public Guid? EntityId { get; set; }
```

#### 7.2.2. Subcomponent Parameters (`CMP-01` to `CMP-XX`)
Shared component contracts (`PortalSidebarNav.razor`, spatial HUD, maintenance form kit, `EquipmentLookupModal.razor`): see [DT-UI-CTR-001 §3](../../contracts/DT-UI-CTR-001.md#3-shared-razor-component-parameter-contracts).

```csharp
// ScreenLocalWidget.razor — pure [Parameter] signatures only (no ComponentBase, [Inject], or _fields)
[Parameter]
public EventCallback OnRefreshRequested { get; set; }
```

#### 7.2.3. Data Transfer Objects (DTOs) and Enums
Shared Domain Enums: see [DT-DM-DOC-001 §4](../../../domain-models/class/DT-DM-DOC-001.md#4-controlled-vocabulary).

Shared Lookup DTOs & Value Types: see [DT-UI-CTR-001 §§2 & 4](../../contracts/DT-UI-CTR-001.md#2-shared-lookup-dtos).

```csharp
// Screen-local DTOs/Commands only; use decimal, DateTimeOffset/DateOnly, and uint? ConcurrencyToken (offline commands)
public record ScreenLocalCommand
{
    public required Guid CorrelationId { get; init; }
    public required DateTimeOffset SubmittedAtUtc { get; init; }
    public uint? ConcurrencyToken { get; init; }
}
```

### 7.3. Client-Side DOM & Interop Bridge
1. **Capability Interfaces:** Define pure interfaces (`IPointerInterop`, `ICryptoInterop`, `IOfflineStorage`) without `window.`/`document.` or concrete storage drivers.
2. **Event Throttling:** Debounce search/pointer updates to avoid UI jitter or API saturation.

---

## 8. Layout and Responsive Adaptability

| Viewport / Breakpoint | Layout Organization | Ergonomic Rules |
| :--- | :--- | :--- |
| **Desktop Workstation**<br>($\ge 1920\text{px}$, `--dt-breakpoint-xl`) | Full horizontal workspace + sidebar (`--dt-layout-sidebar-width-expanded`) or max-width form (`--dt-layout-form-max-width`). | Dense tabular/spatial inspection; keyboard + pointer shortcuts; sticky action footer (`--dt-layout-footer-height`). |
| **Industrial Tablet Landscape**<br>($1280\text{px} - 1919\text{px}$, `--dt-breakpoint-lg` / $1280\times 800\text{px}$) | Collapsed sidebar (`--dt-layout-sidebar-width-collapsed`) or split lateral drawer (`--dt-layout-drawer-width-tablet`). | Touch pan threshold ($4\text{px}$); gloved touch targets (`--dt-touch-target-mobile`). |
| **Industrial Tablet Portrait**<br>($768\text{px} - 1279\text{px}$, `--dt-breakpoint-md` / $800\times 1280\text{px}$) | Mobile overlay drawer or stacked layout / bottom sheet (`--dt-layout-bottom-sheet-height-initial`). | Drag handle snap hysteresis per §5.2; sticky action bar. |

---

## 9. Traceability and Requirements Matrix

| Requirement | Addressed in Component | Verification & Implementation Mechanism |
| :--- | :--- | :--- |
| **FR-XXX** | `CMP-XX` | Functional verification tied to registered API/UI contract. |
| **NFR-XXX** | `CMP-XX` | Quantitative latency, precision, or concurrency verification. |
| **TR-XXX** / **ADR-XXX** | `CMP-XX` | Compliance with `TR-001`..`TR-011` and `ADR-003` / `ADR-006`. |
