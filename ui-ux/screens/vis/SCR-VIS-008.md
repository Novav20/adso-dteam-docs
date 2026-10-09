---
id: SCR-VIS-008
title: General Plant Map with Work Permits Layer (SIMOPS)
module: VIS
isa101_level: L1 (COP - Overview)
platform: Shared Component
target_device: Industrial Tablet | Desktop
roles:
  - HSEQ Inspector
  - Maintenance Supervisor
user_stories:
  - "[[VIS-008]]"
use_cases:
  - "[[UC-VIS-008]]"
requirements:
  - FR-182
  - FR-183
  - FR-184
  - FR-185
  - FR-186
  - FR-187
  - FR-188
  - FR-189
  - NFR-190
  - NFR-191
  - NFR-192
  - NFR-193
  - NFR-194
  - NFR-195
  - "[[TR-010]]"
  - "[[TR-011]]"
version: 1.2
date: 2026-10-09
status: In Review
---

# SCR-VIS-008: General Plant Map with Work Permits Layer (SIMOPS)

## 1. Purpose and Operational Context
* **View Objective:** Provide a macro-spatial overview (Plot Plan / Common Operational Picture) of the Functional Locations of the industrial plant (ANSI/ISA-101 Level 1). It enables safety inspectors and maintenance supervisors to toggle a dynamic Work Permits (PTW) safety layer to detect dangerous operational intersections (Simultaneous Operations - SIMOPS) and orphan permits lacking spatial mapping.
* **Primary Target Persona:** **HSEQ Inspector** (dictates safety compliance, redundant visual coding, pre-attentive hazard salience, and gloved tactile ergonomics on field tablets).
* **Secondary Persona:** **Maintenance Supervisor** (spatial situational awareness, contractor activity scheduling, and escalation into Level 3 equipment inspection).
* **Operational Context:** Field audits with industrial tablets (`1280 x 800 px` landscape / `800 x 1280 px` portrait, `--dt-breakpoint-lg`) under harsh ambient lighting, or central permit office oversight on desktop workstations (`1920 x 1080 px`, `--dt-breakpoint-xl`).
* **Mode of Operation:** Spatial supervision, safety audit, and passive contextual navigation. The interface does not issue industrial control maneuvers (start/stop) or manipulate process setpoints on the SCADA system.

---

## 2. Visual Artifact

![[SCR-VIS-008-simops-layer.svg]]

---

## 3. Functional Component Inventory

> The base grid, typography, neutral palettes, and minimal tactile contact areas are inherited from [[DT-UI-DS-DOC-001]]. This table defines the present components, their semantic tokens, and the link with the domain model.

| ID | Control / Component | Visual Role / Content | Semantic Token | Data Link / Behavior Rule |
| :------- | :---------------------- | :------------------------------- | :-------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CMP-01` | L1 Plot Plan Canvas | Macro plant SVG vector canvas | Surface: `--dt-color-bg-canvas`<br>Elevation: `--dt-canvas` | Renders macro polygons representing Functional Locations (ISO 14224 Levels 1 to 4) and Level 6 equipment nodes. Implements **Semantic Zoom Clustering** (ANSI/ISA-101 Cl. 6.3.1): aggregates into `CMP-09` Zone Cluster Pills at $Z < 1.15$ and expands to discrete `CMP-05` badges at $1.15 \le Z < 2.30$ per [[UC-VIS-008]] and [[UC-VIS-033]]. |
| `CMP-02` | Viewport Toolbar | Spatial navigation toolbar | Surface: `--dt-color-surface-raised`<br>Border: `--dt-color-border-subtle`<br>Radius: `--dt-radius-full` | Floating navigation toolbar centered strictly over the viewable canvas (accounting for open lateral drawers on tablet landscape). Hosts level badge (`L1: PLOT PLAN`), reset view (1:1), zoom (+ / −), and layer selector (`[≡ Layers]`). Non-modal alert badges for SIMOPS conflicts (`[⚠️ SIMOPS CONFLICT]`) and orphan permits are decoupled from the toolbar's core geometry and anchored to its right flank with vertical margin clearance, ensuring zero layout shift when toggling the PTW layer. **Adaptive Orphan Label Condensation:** On Industrial Tablet Landscape ($901\text{px} - 1399\text{px}$), opening `CMP-07` condenses the orphan badge to icon-only `[⚠️ 3]` format. On Desktop Workstations ($\ge 1400\text{px}$), in tablet portrait, and whenever `CMP-07` is closed, the badge retains its full alphanumeric label `[⚠️ 3 Unmapped]`. All buttons enforce `--dt-touch-target-mobile` ($48 \times 48\text{ px}$). Shared component with [[SCR-VIS-033]]. |
| `CMP-03` | User Profile Indicator | Active user session control | Surface: `--dt-color-surface-raised`<br>Border: `--dt-color-border-panel`<br>Radius: `--dt-radius-full` | Independent circular floating button anchored at the top-left of the viewport (`left: 16px; top: 16px;`). Displays user initials (e.g., "JS"). Minimum touch target $48 \times 48\text{ px}$ (`--dt-touch-target-mobile`). Aligned with `CMP-11` in [[SCR-VIS-033]]. |
| `CMP-04` | Functional Zone Polygon | Plant zone boundaries in SVG | Border: `--dt-color-border-subtle`<br>Fill: transparent / neutral | Vector boundary representing a Functional Location (e.g., *Crude Tanks*, *Pumping Station*). Operates in neutral grayscale without decorative fills to preserve the 90% background rule. Hosts `CMP-09` Zone Cluster Pills at geometric centroids when zoomed out ($Z < 1.15$). |
| `CMP-05` | PTW Overlay Badges | Active permit safety markers | Color: Security Matrix Tokens<br>Elevation: `--dt-z-layer-ptw` ($10$) | Positioned dynamically over affected Equipment Units at area zoom ($1.15 \le Z < 2.30$). Enforces mandatory **4-Channel Redundant Coding** (Color + Geometric Shape + Icon + Alphanumeric Text) per [[DT-UI-DS-DOC-001#6.2]] mapped to [[DT-DM-DOC-001#4.28]]:<br>• **HOT_WORK:** `--dt-color-alarm-critical` + Square ($20\times 20\text{px}$) + `#icon-hot-work` + `HOT WORK`<br>• **WORK_AT_HEIGHT:** `--dt-color-state-info` + Triangle ($20\times 18\text{px}$) + `#icon-heights` + `HEIGHTS`<br>• **CONFINED_SPACE:** `--dt-color-alarm-warning` + Circle ($\varnothing 20\text{px}$) + `#icon-confined-space` + `CONFINED`<br>• **ELECTRICAL:** `--dt-color-alarm-critical` + Hexagon ($20\times 20\text{px}$) + `#icon-electrical` + `ELECTRICAL`<br>• **CHEMICAL:** `--dt-color-alarm-warning` + Diamond ($20\times 20\text{px}$) + `#icon-chemical` + `CHEMICAL`<br>• **COLD_WORK:** `--dt-color-state-info` + Rounded Rectangle ($20\times 16\text{px}$) + `#icon-cold-work` + `COLD WORK`<br>Renders dynamic semi-transparent spatial hazard buffers (15m Hot Work, 10m Confined Space, 5m default). If Euclidean distance $D_{AB} < R_A + R_B$, displays a pulsing red conflict halo ($4\text{px}$) and overlapping hatch pattern. Buffer circles, halos, and hatch patterns are rendered with `pointer-events: none` to guarantee continuous pan drag gestures across permit zones. Includes an invisible $48 \times 48\text{ px}$ tactile hit-box for gloved operation and an expiring warning cue ($< 60\text{ min}$). |
| `CMP-06` | Context Popover Card | Permit detail contextual card | Surface: `--dt-color-surface-raised`<br>Border: `--dt-color-border-subtle`<br>Elevation: `--dt-z-overlay-card` ($100$) | Deployed upon tap/click on a `CMP-05` badge. Displays: `Permit Identifier`, `Permit Type` ([[DT-DM-DOC-001#4.28]]), `Contractor`, `Responsible Authority (Issuer)`, `Schedule (valid_from - valid_to)`, `Status` ([[DT-DM-DOC-001#4.29]]), read-only `Associated LOTO` reference, and the mandatory `'View Details'` action button (`FR-184`). **Adaptive Viewport Clamping & Collision Flipping:** Dynamically calculates bounding box and flips leftward when colliding with the right viewport margin ($X + W > \text{Viewport}_W - 16\text{px}$); clamps vertically within safe boundaries ($[70\text{px}, \text{Viewport}_H - H - 16\text{px}]$) respecting top toolbar clearance. **Transient Light-Dismiss:** Automatically dismisses upon continuous pan or zoom gestures per ANSI/ISA-101, but allows immediate reopening upon subsequent badge taps without gesture locking. Dimensioned to prevent occluding adjacent equipment units for SIMOPS situational awareness. |
| `CMP-07` | SIMOPS Integrity Panel | Visualization Failures drawer | Surface: `--dt-color-surface-drawer`<br>Border: `--dt-color-border-panel`<br>Elevation: `--dt-z-drawer-sidebar` ($800$) | Collapsible drawer (lateral panel in landscape constrained to $\le 320\text{px}$ width; bottom sheet in portrait occupying $\le 40\%$ height) activated when active permits reference Equipment Units lacking spatial `MeshMapping` (`AF-001` / `FR-185`). Triggered non-modally via toolbar alert badge or top toast banner (`--dt-color-alarm-critical`). Contains actionable list with Permit ID, Contractor, Expected Tag, and 48px `[Resolve Inconsistency]` button (`FR-186`). Incorporates touch handle with discrete tap toggle per [[DT-UI-DS-DOC-001#6.3]] and ISO 9241-110 §5.5. |
| `CMP-08` | Filter Chips Panel | Risk category filter panel | Surface: `--dt-color-surface-raised`<br>Border: `--dt-color-border-subtle`<br>Radius: `--dt-radius-full` | Floating bar at the screen bottom with direct-touch filter chips for active permit types ([[DT-DM-DOC-001#4.28]]): `[ALL (N)]`, `[HOT WORK (N)]`, `[HEIGHTS (N)]`, `[CONFINED (N)]`, `[ELECTRICAL (N)]`, `[CHEMICAL (N)]` (`FR-188`). All chips enforce `--dt-control-height-lg` / `--dt-touch-target-mobile` ($\ge 48\text{px}$) for gloved use. Supports direct swipe scrolling on touch devices and horizontal mouse-wheel scrolling via Shift + Wheel on desktop. Active chip reflects solid high-contrast visual state. |
| `CMP-09` | Zone Cluster Pill | Macro SIMOPS density aggregation | Surface: `--dt-color-surface-raised`<br>Border: `--dt-color-border-subtle`<br>Radius: `--dt-radius-full` | Rendered at Functional Location centroids when zoomed out ($Z < 1.15$). Consolidates tactical permits into high-salience overview pills (e.g., `Zone A: 5 PTWs [🔥1 \| 🧗2 \| 🛢️2]`). Tapping zooms into the zone ($Z = 1.30$), smoothly expanding the pill into discrete `CMP-05` badges. Enforces $48\text{px}$ touch target. |

---

## 4. Screen State Matrix

| State | Visual Modification in the Interface | Activation Condition |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **Normal (Inactive Layer)** | Canvas renders Functional Locations in neutral grayscale palette (`--dt-color-bg-canvas`). No superimposed safety badges. | User deactivates the "Work Permits" layer in `CMP-02` or default initial state. |
| **Loading** | Dimmed activity indicator / spinner centered over canvas; skeleton shimmer on panel containers. | Initial SVG plot plan retrieval or spatial query transition. |
| **Active PTW Layer** | Renders `CMP-09` Zone Cluster Pills at $Z < 1.15$, or discrete `CMP-05` badges with spatial hazard buffers at $1.15 \le Z < 2.30$. Layer button in `CMP-02` highlights with `--dt-color-state-info`. | Activation of the "Work Permits" layer switch in `CMP-02` (`FR-182`). |
| **Selected Permit (Popover Active)** | Target `CMP-05` badge highlights with informational halo (`--dt-color-state-info`). Compact card `CMP-06` deploys adjacent to the badge without occluding surrounding assets. Clamps inside viewport margins and dismisses upon pan/zoom. | Tap / Click on `CMP-05` badge on the canvas (`FR-184`). |
| **SIMOPS Spatial Conflict Active** | Overlapping hazard buffers render a high-contrast pulsing hatch pattern. Conflicting `CMP-05` badges display a $4\text{px}$ pulsing red conflict halo (`--dt-color-alarm-critical`). Viewport toolbar `CMP-02` displays a non-modal badge `[⚠️ SIMOPS CONFLICT: PTW-XXXX / PTW-YYYY]`. Top toast banner slides down non-modally. | Automated Spatial Integrity Engine detects Euclidean distance $D_{AB} < R_A + R_B$ between incompatible permits (e.g. Hot Work vs. Confined Space). |
| **Expiring Soon Warning** | Target `CMP-05` badge displays a distinct border pulse or warning indicator; status in `CMP-06` displays "EXPIRING SOON" in `--dt-color-alarm-warning`. | System detects permit time window has $< 60\text{ min}$ remaining until `valid_to`. |
| **Detected Orphanhood (SIMOPS Alert)** | Non-modal alert indicator on `CMP-02` toolbar highlights in `--dt-color-alarm-critical` with broken permit count badge (e.g., `[⚠️ 3]`). A single-line non-modal toast banner ($\le 40\text{px}$) notifies the operator with `[Review]` action. Explicit tap opens `CMP-07` without involuntary viewport hijacking. | System detects approved `WorkPermits` referencing Equipment Units lacking SVG `MeshMapping` (`FR-185`, `AF-001`). |
| **Loss of Synchronization** | Priority 4 Diagnostic banner at screen top (`--dt-color-surface-raised`, `--dt-color-text-muted`) with neutral stale icon (`wifi-off`) and last sync timestamp: *"Operating with cached data. Last sync: HH:mm:ss UTC"*. Badges remain visible in cached state. Process alarm colors (amber/red) are strictly prohibited. | Interruption of the real-time SignalR connection or heartbeat timeout (`FR-187`, `NFR-194`, `AF-002`). |

---

## 5. Interaction Rules and Data Flow

### 5.1. Spatial Resolution, Proximity Engine, and Layer Rendering
1. Upon loading the view, the system retrieves the vector layout representing the facility's Functional Locations (ISO 14224 Levels 1 to 4).
2. When the Work Permits layer is active, the system queries all `WorkPermits` in the `APPROVED` lifecycle state.
3. **Referential Resolution Path:**
   $$\text{WorkPermit} \xrightarrow{\text{equipment\_unit\_id}} \text{EquipmentUnit} \xrightarrow{\text{MeshMapping}} \text{SVG Coordinates / Centroid}$$
   * If the Equipment Unit has an explicit `MeshMapping` node in the SVG, the `CMP-05` badge is centered over that equipment hotspot.
   * If the Equipment Unit is mapped to a parent Functional Location without discrete geometry, the badge is placed in the designated zone cluster header (`CMP-04`).
4. **Automated SIMOPS Proximity & Collision Detection Engine (ISO 45001 §8.1 / Endsley SA Level 3):**
   * The spatial engine computes Euclidean distances between all active permit locations:
     $$D_{AB} = \sqrt{(X_B - X_A)^2 + (Y_B - Y_A)^2}$$
   * **Dynamic Spatial Hazard Buffers (`--dt-z-layer-ptw`):**
     * **HOT_WORK:** $15\text{m}$ physical radius rendered as a semi-transparent circle (`--dt-primitive-red-600` at $15\%$ opacity).
     * **CONFINED_SPACE:** $10\text{m}$ physical radius rendered as an amber semi-transparent circle (`--dt-primitive-amber-400` at $15\%$ opacity).
     * **Other Types:** Configurable safe operational clearance buffer ($5\text{m}$ default).
   * **Collision Trigger:** When $D_{AB} < R_A + R_B$, a SIMOPS conflict is automatically triggered:
     * Overlapping intersection zone renders a high-contrast pulsing diagonal hatch pattern.
     * Both affected `CMP-05` badges display a pulsing $4\text{px}$ conflict halo in `--dt-color-alarm-critical`.
     * `CMP-02` Toolbar activates a dedicated conflict pill: `[⚠️ SIMOPS CONFLICT: PTW-XXXX / PTW-YYYY]`. Tapping the pill centers the viewport over the conflict site and opens the conflict detail card.

### 5.2. Integrity Panel Governance & Non-Modal Escalation (Orphan Detection — `AF-001`)
1. If an approved `WorkPermit` references an `EquipmentUnitId` that has no geometric representation or spatial metadata in the loaded layout, the permit is classified as **Orphan**.
2. **Safety Rule:** The permit is **never** drawn at an arbitrary coordinate on the map to prevent misleading spatial situational awareness.
3. **Strict Non-Modal Escalation (ISO 9241-110 §5.5 Controllability & ISO 11064-5):**
   * Detecting unmapped permits shall **never** automatically deploy or expand `CMP-07`, preventing viewport hijacking.
   * The alert counter on `CMP-02` Toolbar transitions to `--dt-color-alarm-critical` with the unread orphan count badge (e.g., `[⚠️ 3]`).
   * A single-line non-modal toast banner ($\le 40\text{px}$ height, `--dt-z-toast-alert`) slides down at the top viewport edge:
     `"SIMOPS Alert: 3 Permits lack spatial mapping. [View List] [Dismiss]"`
4. **Explicit Operator Deployment & Tablet Physical Constraints:**
   * Tapping `[View List]` or the toolbar badge expands `CMP-07`.
   * **Tablet Landscape ($1280 \times 800\text{ px}$):** `CMP-07` is constrained to a maximum width of **$\le 320\text{ px}$** (leaving $\ge 75\%$ of the map canvas visible).
   * **Tablet Portrait ($800 \times 1280\text{ px}$):** `CMP-07` renders as a **Bottom Sheet** occupying **$\le 40\%$** vertical screen height.
   * Container toggling operates exclusively via **discrete single taps** on dedicated $48 \times 48\text{ px}$ handles (`--dt-touch-target-mobile` per [[DT-UI-DS-DOC-001#6.3]]). Continuous drag gestures are optional and never mandatory.
5. Each orphan record presents: `Permit Identifier`, `Contractor`, `Expected TagNumber`, and the $48\text{px}$ `[Resolve Inconsistency]` button (`FR-186`), enabling the inspector to assign geometry or request spatial metadata updates.

### 5.3. Real-Time Synchronization (`TR-010`)
1. The client subscribes to the SignalR hub for work permit domain events:
   * `WorkPermitApproved`: Injects a new `CMP-05` badge (or updates `CMP-09` cluster count) within $< 5\text{s}$ (`FR-187`, `NFR-192`).
   * `WorkPermitRevoked` / `WorkPermitClosed`: Removes the badge with a fluid fade transition in $< 5\text{s}$.
   * `WorkPermitExpiringSoon`: Transitions the badge to the expiring warning state.
2. **Operational Resilience (`AF-002`):** If the real-time link drops, the client transitions to the "Loss of Synchronization" diagnostic state without blocking canvas navigation, preserving the last known snapshot with explicit timestamp traceability (`NFR-194`).

### 5.4. Dual Navigation, Tactile Controllability, and Semantic Zoom Clustering
1. **Semantic Zoom Clustering (ANSI/ISA-101.01 §6.3.1 / Hollifield Ch. 8):** The viewport supports continuous pan/zoom. Progressive disclosure thresholds govern density:
   * **Scale $Z < 1.15$ (Level 1 Plant Overview / COP):** Discrete equipment badges are **suppressed**. Functional Locations render consolidated **Zone Cluster Pills** (`CMP-09`) at centroids (e.g., `Zone A: 5 PTWs [🔥1 \| 🧗2 \| 🛢️2]`), preserving the 90/10 grayscale rule and preventing visual clutter (`NFR-190`).
   * **Scale $1.15 \le Z < 2.30$ (Level 2 Process Area Layout):** Cluster pills expand into individual **Discrete Equipment Badges** (`CMP-05`) positioned over ISO 14224 Level 6 Equipment Units with dynamic spatial hazard buffers.
   * **Scale $Z \ge 2.30$ (Level 3 Equipment Detail Faceplate):** Micro tactical detail disclosing nozzles, valves, local instrument numbers, and active LOTO lock numbers.
2. **Dual-Mode Canvas Pan Ergonomics:**
   * **Desktop Workstations:** Continuous canvas panning strictly requires **middle-click (mouse wheel drag)** with pointer capture. Primary left-click is exclusively reserved for selecting equipment, toggling toolbar controls, and inspecting safety badges.
   * **Touch Tablets:** Supports direct 1-finger canvas dragging with a strict **$4\text{px}$ movement threshold** to cleanly differentiate intentional pan gestures from stationary taps on equipment badges.
3. **Transient Popover Card Dismissal & Re-opening:**
   * Moving the canvas via pan drag or adjusting zoom immediately dismisses `CMP-06` to maintain unobstructed visual scanning.
   * Ending a pan gesture must immediately unblock input handling, ensuring subsequent stationary clicks or taps on equipment badges deploy `CMP-06` without gesture-lock.
4. **Horizontal Filter Chips Ergonomics (`CMP-08`):**
   * Supports direct touch swipe on field tablets.
   * Supports horizontal scrolling on desktop via mouse wheel combined with the `Shift` key (`Shift + Wheel`).
5. **Tactile Ergonomics:** On touch devices (`Industrial Tablet`), all interactive triggers (`CMP-02`, `CMP-03`, `CMP-07`, `CMP-08`, `CMP-09`) maintain a minimum contact area of $48 \times 48\text{ px}$ (`--dt-touch-target-mobile`).
6. **Hover vs. Tap Bifurcation:** Desktop pointers display a compact hover tooltip (`FR-189`). Touch devices deploy the persistent `CMP-06` card upon direct tap (`FR-184`), dismissible via tap-away, pan/zoom motion, or close ('X') button.

### 5.5. Hierarchical Escalation (L1 $\to$ L3 Transition)
1. Clicking on `'View Details'` within `CMP-06` initiates an operational drill-down, transitioning the inspector directly into the Level 3 Equipment Task Faceplate ([[SCR-VIS-033]]) for the target equipment unit.
2. Direct selection of an Equipment Unit on the canvas (outside a PTW badge) seamlessly deploys the [[SCR-VIS-033]] contextual drawer without changing screens.

---

## 6. Industrial and Safety Considerations

* **90/10 HPHMI Philosophy ([[TR-011]]):** The plant layout operates in a neutral grayscale palette (`--dt-color-bg-canvas`). Saturated color is strictly quarantined to active safety permits, orphan alerts, and process anomalies. By clustering badges at $Z < 1.15$, pre-attentive salience for process alarms is strictly maintained. The use of industrial green for normal operation is strictly prohibited.
* **Redundant Coding for Accessibility (WCAG 2.1 AA):** No hazard or permit class is communicated solely through color. Every `CMP-05` badge combines **Geometric Shape + Vector Icon + Saturated Token + Mandatory Alphanumeric Text** (`HOT WORK`, `HEIGHTS`, `CONFINED`) per [[DT-UI-DS-DOC-001#6.2]].
* **Level 3 Situation Awareness & Automated Risk Control (Endsley & ISO 45001 §8.1):** Relying on passive human visual scanning to detect SIMOPS interferences fails cognitive projection. Automated buffer calculations ($D_{AB} < R_A + R_B$) enforce systematic OH&S operational controls.
* **Alarm vs. Diagnostic Segregation (ISA-101):** Signal loss and data staleness are Priority 4 Diagnostics. They are represented with neutral slate styling and muted typography, strictly preventing the use of amber (`--dt-color-alarm-warning`) or red (`--dt-color-alarm-critical`) to avoid distracting operators during actual plant emergencies.
* **SIMOPS Situational Awareness:** The `CMP-06` popover is dimensionally constrained so that inspecting a Hot Work permit never occludes nearby Confined Space or Height Work badges, preserving peripheral hazard visibility.

---

## 7. Frontend Component Contract (Blazor / Razor)

### 7.1. Component Hierarchy & File Mapping

```text
Pages/
└── GeneralPlantMapPage.razor                 # Root View (SCR-VIS-008)
    ├── PlotPlanCanvas2D.razor                # CMP-01: Macro SVG canvas with pan/zoom
    │   ├── FunctionalZonePolygon.razor       # CMP-04: Functional Location vector polygon
    │   ├── ZoneClusterPill.razor             # CMP-09: Macro density aggregation pill (Z < 1.15)
    │   ├── PtwOverlayBadge.razor             # CMP-05: Redundant coding safety badge (Z >= 1.15)
    │   └── SimopsHazardBuffer.razor          # Dynamic spatial buffer circle & conflict hatch
    ├── ViewportToolbar.razor                 # CMP-02: Floating navigation & layer bar
    ├── UserProfileButton.razor               # CMP-03: Top-left user profile indicator
    ├── PtwContextPopover.razor               # CMP-06: Compact permit popover card
    ├── SimopsIntegrityDrawer.razor           # CMP-07: Visualization failures side drawer (<= 320px)
    ├── PtwFilterChips.razor                  # CMP-08: Bottom floating risk filter chips
    └── StaleCacheBanner.razor                # Diagnostic stale cache banner (AF-002)
```

### 7.2. Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)

#### 7.2.1. `GeneralPlantMapPage.razor` (Root View)
```csharp
namespace DTeam.DigitalTwin.Pages;

public partial class GeneralPlantMapPage : ComponentBase
{
    [Inject]
    public required IPtwSubscriptionService PtwService { get; set; }

    [Inject]
    public required IPlotPlanSpatialService SpatialService { get; set; }

    // State properties
    public PlantPlotPlanDto? PlotPlanData { get; private set; }
    public IReadOnlyList<PtwOverlayDto> ActivePermits { get; private set; } = [];
    public IReadOnlyList<ZoneClusterPillDto> ZoneClusters { get; private set; } = [];
    public IReadOnlyList<SimopsConflictDto> ActiveConflicts { get; private set; } = [];
    public IReadOnlyList<OrphanPermitDto> OrphanPermits { get; private set; } = [];
    public PtwOverlayDto? SelectedPermit { get; private set; }
    public PermitType? ActiveFilter { get; private set; }
    public double CurrentZoomScale { get; private set; } = 1.0;
    public bool IsPtwLayerActive { get; private set; } = true;
    public bool IsIntegrityDrawerOpen { get; private set; }
    public bool IsSyncLost { get; private set; }
    public DateTimeOffset? LastSyncTimestamp { get; private set; }
}
```

#### 7.2.2. Subcomponent Parameter Contracts

```csharp
// CMP-01: PlotPlanCanvas2D.razor
[Parameter]
public required string SvgRawContent { get; set; }

[Parameter]
public required IReadOnlyList<PtwOverlayDto> Permits { get; set; }

[Parameter]
public required IReadOnlyList<ZoneClusterPillDto> Clusters { get; set; }

[Parameter]
public required IReadOnlyList<SimopsConflictDto> Conflicts { get; set; }

[Parameter]
public double ZoomScale { get; set; } = 1.0;

[Parameter]
public EventCallback<string> OnEquipmentSelected { get; set; }

[Parameter]
public EventCallback<Guid> OnPermitBadgeClicked { get; set; }

[Parameter]
public EventCallback<string> OnZoneClusterClicked { get; set; }

// CMP-09: ZoneClusterPill.razor
[Parameter]
public required ZoneClusterPillDto Cluster { get; set; }

[Parameter]
public EventCallback<string> OnClusterClicked { get; set; }

// CMP-05: PtwOverlayBadge.razor
[Parameter]
public required PtwOverlayDto Permit { get; set; }

[Parameter]
public bool IsSelected { get; set; }

[Parameter]
public bool HasSimopsConflict { get; set; }

[Parameter]
public EventCallback<Guid> OnBadgeClicked { get; set; }

// SimopsHazardBuffer.razor
[Parameter]
public required PtwOverlayDto Permit { get; set; }

[Parameter]
public bool HasConflict { get; set; }

// CMP-06: PtwContextPopover.razor
[Parameter]
public required PtwOverlayDto Permit { get; set; }

[Parameter]
public EventCallback OnCloseRequested { get; set; }

[Parameter]
public EventCallback<string> OnViewDetailsRequested { get; set; }

// CMP-07: SimopsIntegrityDrawer.razor
[Parameter]
public required IReadOnlyList<OrphanPermitDto> OrphanPermits { get; set; }

[Parameter]
public bool IsOpen { get; set; }

[Parameter]
public EventCallback<bool> OnOpenChanged { get; set; }

[Parameter]
public EventCallback<Guid> OnResolveInconsistencyRequested { get; set; }

// CMP-08: PtwFilterChips.razor
[Parameter]
public PermitType? SelectedFilter { get; set; }

[Parameter]
public required IReadOnlyDictionary<PermitType?, int> PermitCounts { get; set; }

[Parameter]
public EventCallback<PermitType?> OnFilterChanged { get; set; }
```

#### 7.2.3. Data Transfer Objects (DTOs)

```csharp
namespace DTeam.DigitalTwin.Contracts.Safety;

/// <summary>
/// Controlled permit risk classification vocabulary per DT-DM-DOC-001 §4.28.
/// </summary>
public enum PermitType
{
    HOT_WORK,
    COLD_WORK,
    CONFINED_SPACE,
    ELECTRICAL,
    WORK_AT_HEIGHT,
    EXCAVATION,
    CHEMICAL
}

/// <summary>
/// Controlled permit lifecycle status vocabulary per DT-DM-DOC-001 §4.29.
/// </summary>
public enum WorkPermitStatus
{
    DRAFT,
    PENDING,
    APPROVED,
    EXPIRED,
    REVOKED,
    CLOSED
}

public record PtwOverlayDto
{
    public required Guid Id { get; init; }
    public required string PermitIdentifier { get; init; } // e.g. "PTW-1042"
    public required PermitType Type { get; init; }
    public required string Contractor { get; init; }
    public required Guid IssuerUserId { get; init; }
    public required string IssuerFullName { get; init; }
    public required Guid EquipmentUnitId { get; init; }
    public required string EquipmentTag { get; init; }
    public required double CoordinateX { get; init; }
    public required double CoordinateY { get; init; }
    public required DateTimeOffset ValidFrom { get; init; }
    public required DateTimeOffset ValidTo { get; init; }
    public required WorkPermitStatus Status { get; init; }
    public bool IsExpiringSoon { get; init; }
    public string? AssociatedLotoNumber { get; init; }
    public double BufferRadiusMeters { get; init; } = 5.0; // 15m Hot Work, 10m Confined Space
    public bool HasSimopsConflict { get; init; }
    public IReadOnlyList<Guid> ConflictingPermitIds { get; init; } = [];
}

public record ZoneClusterPillDto
{
    public required string FunctionalLocationCode { get; init; }
    public required string ZoneName { get; init; }
    public required double CentroidX { get; init; }
    public required double CentroidY { get; init; }
    public required int TotalPermitsCount { get; init; }
    public required int HotWorkCount { get; init; }
    public required int HeightsCount { get; init; }
    public required int ConfinedSpaceCount { get; init; }
    public required int OtherPermitsCount { get; init; }
}

public record SimopsConflictRule
{
    public required PermitType TriggerType { get; init; }   // e.g. HOT_WORK
    public required PermitType TargetType { get; init; }    // e.g. CONFINED_SPACE
    public required double MinimumSafeRadiusMeters { get; init; } // e.g. 15.0 meters
    public required string EscalationSeverity { get; init; } // e.g. "CRITICAL"
}

public record SimopsConflictDto
{
    public required Guid Id { get; init; }
    public required Guid PermitAId { get; init; }
    public required Guid PermitBId { get; init; }
    public required string PermitAIdentifier { get; init; }
    public required string PermitBIdentifier { get; init; }
    public required PermitType PermitAType { get; init; }
    public required PermitType PermitBType { get; init; }
    public required double DistanceMeters { get; init; }
    public required double SafeDistanceMeters { get; init; }
    public required string ConflictDescription { get; init; }
}

public record OrphanPermitDto
{
    public required Guid Id { get; init; }
    public required string PermitIdentifier { get; init; }
    public required PermitType Type { get; init; }
    public required string Contractor { get; init; }
    public required string ExpectedEquipmentTag { get; init; }
    public required DateTimeOffset ValidTo { get; init; }
}

public record PlantPlotPlanDto
{
    public required string FacilityCode { get; init; }
    public required string FacilityName { get; init; }
    public required string SvgContent { get; init; }
    public IReadOnlyList<PlantZoneDto> Zones { get; init; } = [];
}

public record PlantZoneDto
{
    public required string FunctionalLocationCode { get; init; }
    public required string ZoneName { get; init; }
    public required int IsoHierarchyLevel { get; init; }
}
```

### 7.3. SVG DOM Interaction Bridge
1. **Geometric Viewport Navigation:** Panning, dragging, and wheel zooming are handled client-side via SVG `viewBox` coordinates or a high-performance JavaScript interop wrapper ([[ADR-001]]), maintaining $\ge 30\text{ FPS}$ on tablets and $\ge 60\text{ FPS}$ on desktop (`NFR-190`).
2. **Semantic Event Dispatching:** Hotspot groups in the SVG declare data attributes (`data-tag="P-101"`, `data-permit-id="uuid"`). Clicks on permit badges trigger the `OnPermitBadgeClicked(permitId)` callback. Clicks on equipment geometry outside active badges trigger `OnEquipmentSelected(tagNumber)`, invoking the [[SCR-VIS-033]] Level 3 faceplate.