---
id: SCR-MTTO-026
title: RIME Backlog Prioritization Dashboard
module: MTTO
isa101_level: L2 (Process Supervision and Planning)
platform: Desktop Web
target_device: Desktop Workstation
roles:
  - Maintenance Planner
  - Maintenance Supervisor
  - Reliability Engineer
user_stories:
  - "[[MTTO-026]]"
use_cases:
  - "[[UC-MTTO-026]]"
version: 1.4
date: 2026-11-03
status: Stable
---

# SCR-MTTO-026: RIME Backlog Prioritization Dashboard

## 1. Purpose and Operational Context

* **View Objective:** Centralized supervisory dashboard for objective, quantitative prioritization of work requests in the maintenance backlog. Automatically assigns a standardized priority score by delegating calculation to the industrial RIME (Ranking Index for Maintenance Expenditure) prioritization strategy engine ([ADR-002](../../../architecture/adr/ADR-002.md)), combining static Asset Criticality ($1..10$) and Work Class weight ($1..10$) into an audited score ($1..100$). Eliminates subjective bias, enforces compliance with ISO 55001 (§6.2.2), and consolidates resource availability (labor hours and materials) to streamline weekly workload scheduling.
* **Primary Target Persona:** Maintenance Planner executing weekly workload distribution, reviewing incoming requests, adjusting work class classifications when operational conditions shift, and promoting prioritized backlog items into scheduled work orders.
* **Secondary Personas:**
  * **Maintenance Supervisor:** Reviews prioritized backlog, verifies labor availability, and approves emergency work overrides.
  * **Reliability Engineer:** Receives fail-safe notifications for assets lacking configured criticality, updates master data catalogs, and evaluates equipment failure grouping opportunities.
* **Operational Context:** Deployed in central maintenance engineering and planning control offices on high-resolution desktop workstations. Also accessible from portable industrial tablets in supervisory and reliability office environments.
* **Mode of Operation:** Supervisory Prioritization and Governance mode. Direct DCS/SCADA process control manipulation is strictly excluded. Actions focus on multi-criteria backlog sorting, work class adjustment with cryptographic audit trails, fail-safe mitigation, grouping recommendations, work order promotion ([SCR-MTTO-001](SCR-MTTO-001.md)), and sensor-based telemetry scheduling ([SCR-MTTO-023](SCR-MTTO-023.md)).
* **Web Portal Workspace Invariant:** Operates as a Level 2 supervisory portal view (ANSI/ISA-101 Level 2 per [DT-UI-NAV-DOC-001](../../DT-UI-NAV-DOC-001.md)) within the unified Blazor Web Portal shell. Features collapsible navigation, breadcrumb navigation, dense multi-column tabular data grids with column-level sorting, sticky KPI summary cards, and persistent right dock inspection panels (`CMP-13` hosting `CMP-09` and `CMP-11`).

---

## 2. Visual Artifact

![SCR-MTTO-026 RIME Backlog Prioritization Screenshot](assets/SCR-MTTO-026-screenshot.png)

> *Note: Production UI prototype capture illustrating the Archetype C desktop workstation layout, collapsible navigation sidebar, interactive KPI summary cards, flat multi-criteria filter toolbar with inline grouping trigger, dense prioritized data grid with locked column dimensions, persistent right dock with Blender N-panel-inspired vertical tabs, and sticky workload confirmation footer.*

---

## 3. Functional Component Inventory

> The base layout, typography, and design tokens are inherited from [DT-UI-DS-DOC-001](../../DT-UI-DS-DOC-001.md). This table defines the present components, semantic tokens, and architectural roles. Detailed interaction rules, layout constraints, and responsive resolutions are strictly specified in Section 5 and Section 8.

| ID | Control / Component | Visual Role / Content | Semantic Token | Architectural Role & Reference |
| :--- | :--- | :--- | :--- | :--- |
| `CMP-01` | Web Portal Shell & Sidebar | Collapsible navigation sidebar | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle` | Hosts global module navigation (Digital Twin, Maintenance, Inventory, Governance per [DT-UI-NAV-DOC-001](../../DT-UI-NAV-DOC-001.md)). Highlights "Backlog Prioritization" as the active route. Responsive widths governed in Section 8. |
| `CMP-02` | Top Workstation Header | Breadcrumb trail, search, governance notifications, and user badge | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle` | Sticky header hosting breadcrumbs, quick search trigger (`Ctrl + K`), unconfigured criticality alert button (`CMP-06`), and standardized operator session badge. |
| `CMP-03` | KPI Summary Metric Cards | 5-card interactive filter & summary bar | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle`<br>Radius: `--dt-radius-md` | Displays aggregate counters across the 4 RIME priority bands plus total pending count. Serves as the sole interactive priority band filter for the data grid, preventing redundant filter chip rows. Detailed in §5.1. |
| `CMP-04` | Multi-Criteria Filter Toolbar | Flat canvas toolbar with dropdowns, search input, and inline grouping pill | Surface: `--dt-color-surface-base`<br>Controls: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle` | Hosts Functional Location hierarchy dropdown, Work Class selector, live text search, and the inline equipment grouping suggestion pill (`CMP-05`) directly on the canvas without outer box nesting or vertical layout shift. Specification in §5.2. |
| `CMP-05` | Inline Grouping Suggestion Pill | Compact inline batching indicator | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle`<br>Radius: `--dt-radius-md` | Compact pill embedded inside `CMP-04` deployed when multiple pending work requests target the same Level 6 Equipment Unit. Uses flat inline text dividers (`|`) without nested button boxes to display affected asset tag, request count, combined wrench time, and batch filter action. Workflow in §5.3.3. |
| `CMP-06` | Criticality Governance Alert Modal | Unconfigured asset notification & dispatch modal | Surface: `--dt-color-surface-overlay`<br>Border: `--dt-color-border-panel`<br>Elevation: `--dt-z-modal` | Triggered via the header warning indicator when work requests reference assets lacking configured criticality in the catalog. Informs that a preventive floor score was assigned, provides a "View Affected Request" filter action, and dispatches a calibration request to the Reliability Engineer. Workflow in §5.3.2. |
| `CMP-07` | Dense Prioritized Data Grid | Multi-column sortable table | Header: `--dt-color-surface-base`<br>Rows: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle` | Virtualized tabular grid rendering prioritized backlog requests descending by RIME score. Nine operational columns governed by proportional CSS grid tokens (Priority Category & Score, Request ID, Technical Location, Physical Asset, Maintainable Item L8, Technical Description, Work Class, Asset Criticality, and Estimated Hours / Material Availability) calibrated to fit the desktop workspace alongside the open right dock. Column actions are removed in favor of the header action in `CMP-09`. Clicking any point of a row selects and inspects it in `CMP-09`. |
| `CMP-08` | Priority Category Badges | High-contrast redundant capsule pills | Surface: `--dt-color-surface-base`<br>Radius: `--dt-radius-full`<br>Accents: `--dt-color-alarm-critical`, `--dt-color-alarm-warning`, `--dt-color-text-body`, `--dt-color-text-muted` | Four-tier visual categorization implementing ANSI/ISA-101 redundant coding (Shape + Color + Score + Label) using capsule pill geometry (`--dt-radius-full`) morphologically distinct from rectangular row buttons (`--dt-radius-sm`) per [DT-UI-DS-DOC-001 §6.5.1](../../DT-UI-DS-DOC-001.md#651-morphological-differentiation-status-badges-vs-interactive-buttons). Details in §5.1. |
| `CMP-09` | Contextual Request Inspection & Calibration Rail | Collapsible lateral inspection rail in workspace dock | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle` | Lateral inspection pane hosted within the workspace dock (`CMP-13`). Features a sticky header with request identifier, asset tag, primary promotion action ("Plan Request"), and close button; technical facts breakdown; embedded RIME decomposition (`CMP-10`); Work Class recalibration selector with dynamic score preview; mandatory justification textarea; and SHA-256 seal. Operates alongside the table canvas without modal blindness. |
| `CMP-10` | RIME Factor Decomposition Panel | Inline technical factor breakdown card | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle` | Technical card hosted inside `CMP-09`, displaying the exact multiplicative Criticality $\times$ Work Class formula, ISO 55001 (§6.2.2) compliance note, and fail-safe floor indicator (Floor 75). |
| `CMP-11` | Chained Cryptographic Audit Pane | Integrated immutable audit log tab pane | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle` | Tab pane hosted inside the workspace dock (`CMP-13`), displaying the immutable append-only chronological trail of priority calibrations: timestamps, planner user ID, old vs. new work class and score, justification text, previous hash, and current SHA-256 integrity seal. |
| `CMP-12` | Workload Confirmation & Export Bar | Bottom sticky action bar | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle` | Bottom bar consolidating weekly selected man-hours vs. team capacity, centralizing data export options (`CSV` / `JSON` / `Selected`) and hosting the primary "Confirm Weekly Workload" action button. Workflow in §5.3.4. |
| `CMP-13` | Persistent Workspace Dock & Tab Strip | Right dock container with vertical pill tabs | Track: `--dt-color-surface-base`<br>Panel: `--dt-color-surface-card`<br>Active Tab: `--dt-color-surface-raised`<br>Indicator: `--dt-color-state-info` | Blender N-panel-inspired persistent lateral dock. Hosts `CMP-09` (*Request Detail*) and `CMP-11` (*SHA-256 Audit*) as persistent vertical pill tabs oriented along the lateral edge. Active tab click remains open; row selection is preserved across tab switches without horizontal layout shift. Responsive widths and layout rules governed in §5.2 and §8. |

---

## 4. Screen State Matrix

| State | Visual Modification in the Interface | Activation Condition |
| :--- | :--- | :--- |
| **Normal (Default)** | Neutral grayscale surfaces. Full prioritized data grid populated descending by RIME score. Routine `Plan` ($20-49$) and `Wish` ($1-19$) bands and normal material availability states (`In Stock`, `Reserved`) rendered in neutral grayscale without chromatic fills. | Successful data fetch of pending work requests and asset master catalogs. |
| **Loading** | Table rows and KPI summary cards display animated skeleton shimmer (`--dt-color-surface-raised`). Action buttons disabled. | Initial page load or asynchronous execution of bulk filter / sort operations. |
| **Selected Row** | Target table row renders a high-contrast left selection indicator bar (`--dt-color-state-info`) and subtle selection tint background. Right dock vertical tab strip (`CMP-13`) remains accessible. | Planner selects the row checkbox or uses keyboard navigation (`ArrowUp`/`ArrowDown`) on a table row. |
| **Detail Inspection State** | `CMP-09` pane opens inside the persistent right dock container (`--dt-layout-drawer-width-desktop`) alongside the prioritized grid. Main canvas body reserves dock padding dynamically, preventing horizontal layout shift. Selected row receives inspection outline; embedded `CMP-10` and Work Class calibration remain visible. | Planner clicks any point of a backlog row or uses `ArrowUp` / `ArrowDown` after an item is inspected. |
| **Cryptographic Audit State** | Planner clicks the vertical tab *SHA-256 Audit*. The dock panel switches to `CMP-11`, rendering the chained SHA-256 ledger without closing the dock or clearing selected rows. | Planner clicks the *SHA-256 Audit* tab in `CMP-13`. |
| **Priority Recalculation (AF-001)** | The open inspection rail recalculates the candidate RIME score in real-time ($<100\text{ms}$). The confirmation action remains disabled until valid justification is entered ($\ge 15$ characters). | Planner changes Work Class in `CMP-09`. |
| **Fail-Safe Active (AF-002)** | Header notification button in `CMP-02` displays amber warning indicator (`--dt-color-alarm-warning`) with counter badge. Affected row displays amber warning icon with tooltip: *"Criticality not configured on asset. Preventive priority floor applied (Score: 75)"*. | One or more pending work requests are linked to assets lacking criticality in the master catalog. |
| **Grouping Recommendation (FR-068)** | Compact inline pill `CMP-05` rendered inside the filter toolbar `CMP-04` with `#icon-layers`. Affected rows highlight with subtle accent border. Zero vertical displacement of the data grid. | Algorithmic detection of $\ge 2$ pending requests sharing the same Level 6 equipment unit. |
| **Filtered / Search Active** | Data grid displays matching subset with the active KPI filter card highlighted via `--dt-color-state-info` focus border. | Planner clicks an interactive KPI card, selects a Functional Location filter, or types in the search field. |
| **Empty Backlog** | Data grid displays centered neutral empty state illustration (`#icon-check-circle`), title *"No Pending Work Requests"*, and subtitle *"All backlog items have been prioritized and promoted into scheduled work orders."* | Zero work requests in status `NEW` in the database. |

---

## 5. Interaction Rules and Data Flow

### 5.1. Initial Load & Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Planner as Maintenance Planner
    participant UI as SCR-MTTO-026 (Backlog Dashboard)
    participant API as Backlog API Gateway

    Planner->>UI: Navigates to "Backlog Management" (L2)
    UI->>UI: Displays skeleton loading state
    UI->>API: GET /api/v1/maintenance/backlog-items?status=NEW
    API-->>UI: Returns BacklogItemsListDto (enriched projections)
    UI->>UI: Aggregates KPI summary counters (CMP-03)
    UI->>UI: Evaluates equipment grouping clusters (CMP-05)
    UI->>UI: Sorts rows descending by RIME score (CMP-07)
    UI-->>Planner: Renders prioritized interactive data grid (< 2s latency)
```

1. **Initial Query:** On page initialization, the client dispatches a query to retrieve active backlog item projections for all work requests in `NEW` status, enriched with ISO 14224 Equipment Unit, Functional Location, and Maintainable Item metadata.
2. **Deterministic Calculation:** The system verifies that each backlog item reflects the deterministic calculation governed by the active strategy of the RIME prioritization engine ([ADR-002](../../../architecture/adr/ADR-002.md)). The default MVP two-factor formula computes:
   $$\text{Score} = C_{\text{asset}} \times W_{\text{class}}$$
   where $C_{\text{asset}} \in [1, 10]$ is retrieved from the asset catalog, and $W_{\text{class}} \in [1, 10]$ is the standardized weight of the selected Work Class.
3. **Priority Band Categorization:** Every row is mapped to its categorical band according to [NFR-061](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr):
   * **Do First** ($80 \le \text{Score} \le 100$): Emergency Category. Redundant indicator: Red diamond ($\blacklozenge$, `--dt-color-alarm-critical`).
   * **Schedule** ($50 \le \text{Score} \le 79$): High Category. Redundant indicator: Amber triangle ($\blacktriangle$, `--dt-color-alarm-warning`).
   * **Plan** ($20 \le \text{Score} \le 49$): Normal Category. Redundant indicator: Neutral steel square ($\blacksquare$, `--dt-color-text-body`, border `--dt-color-border-panel`).
   * **Wish** ($1 \le \text{Score} \le 19$): Low Category. Redundant indicator: Subdued slate circle ($\bullet$, `--dt-color-text-muted`, border `--dt-color-border-subtle`).
4. **Initial Ordering:** The data grid is deterministically sorted descending by `PriorityScore`. If two items share identical scores, tie-breaking sorts ascending by `RequestDate` (FIFO order).

---

### 5.2. Table Mechanics & Desktop Ergonomics

1. **Sorting Mechanics:** Clicking any column header toggles sorting: `Descending` $\to$ `Ascending` $\to$ `Reset to Default RIME Order`. Column headers retain neutral primary text (`--dt-color-text-primary`) and indicate sort direction via the neutral chevron glyph (`#icon-chevron-up`, `#icon-chevron-down`), preventing non-functional chromatic noise.
2. **Multi-Criteria Filtering:**
   * **Priority Band:** Interactive KPI summary cards (`CMP-03`) act directly as one-click band filters in-memory without server round-trip, eliminating duplicate filter chip rows in `CMP-04`.
   * **Functional Location Filter:** Hierarchical dropdown supporting filtering by Plant Level 3 (Installation), Level 4 (Plant/Area), or Level 5 (System).
   * **Work Class Filter:** Dropdown filtering by specific work classes (e.g., "Safety Emergency", "Predictive Maintenance").
   * **Fuzzy Text Search:** Debounced input ($300\text{ms}$) searching across `TagNumber`, `SerialNumber`, `Description`, and `MaintainableItem`.
3. **Master-Detail Inspection:** Clicking any point within a row selects and inspects the request in the right dock (`CMP-09`). The primary "Plan Request" promotion action is situated in the inspection rail header, removing the redundant "Actions" column from the table grid and keeping the 9-column technical data canvas clear and uncluttered.
4. **Keyboard Navigation:**
   * `ArrowUp` / `ArrowDown`: Moves row selection through the table without mouse interaction.
   * `Enter`: Selects and inspects the focused backlog row in the right dock (`CMP-09`).
   * `Ctrl + K`: Globally focuses the search input.
   * `Escape`: Closes the active dock panel or open governance alert modal.
5. **Asymmetric Workstation Split & Zero Layout Shift:** At desktop widths, the prioritized backlog canvas is paired with the persistent right dock container (`CMP-13`, governed by `--dt-layout-drawer-width-desktop`). To prevent horizontal layout shift or table width collapse, the canvas body reserves dock padding, ensuring seamless inspection without modal blindness or horizontal scrollbars.
6. **Persistent Vertical Tab Dock (Blender N-panel Pattern):** The right dock features vertical pill tabs oriented along the lateral spine with left-rounded geometry (`--dt-radius-md`). The surface hierarchy follows a three-tier depth: dark track canvas (`--dt-color-surface-base`), intermediate dock panel (`--dt-color-surface-card`), and elevated active pill tab (`--dt-color-surface-raised`) with an inset active indicator bar (`--dt-color-state-info`). Tab state is persistent: clicking the active tab keeps the panel open without accidental collapse; switching between *Request Detail* (`CMP-09`) and *SHA-256 Audit* (`CMP-11`) swaps the pane content instantaneously while preserving selected rows in the table.
7. **Data Virtualization & Performance:** For backlog volumes exceeding $100$ items, the Blazor data grid employs UI virtualization (`Virtualize<BacklogItemDto>`), maintaining DOM node count $< 60$ and guaranteeing response times $< 2\text{s}$ for datasets up to $1,000$ items ([NFR-071](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr)).

---

### 5.3. Domain Workflows & Prioritization Engine

#### 5.3.1. Work Class Modification & Dynamic Recalculation (AF-001)

When the Planner identifies that operational conditions warrant an adjusted priority:

```mermaid
sequenceDiagram
    autonumber
    actor Planner as Maintenance Planner
    participant Rail as BacklogItemInspectionRail (CMP-09)
    participant Interop as Client Crypto Interop
    participant API as Backlog API Gateway

    Planner->>Rail: Selects updated Work Class (e.g., Code 8: High Priority Process Work)
    Rail->>Rail: Recalculates candidate RIME score in real-time (< 100ms)
    Rail->>Rail: Updates preview score and priority band indicator
    Planner->>Rail: Enters mandatory technical justification (min 15 chars)
    Planner->>Rail: Clicks "Sign Cryptographic Calibration"
    Rail->>Interop: ComputeSha256Digest(PreviousHash, AuditPayload)
    Interop-->>Rail: Returns candidate PayloadHash
    Rail->>API: POST /api/v1/maintenance/backlog-items/{id}/adjust-work-class
    API-->>Rail: 200 OK (AdjustWorkClassResultDto with chained hash)
    Rail-->>Planner: Re-sorts backlog grid and updates KPI summary cards
```

1. **Trigger:** The Planner clicks a backlog row; the right dock opens with `CMP-09` displaying the selected request.
2. **Latency Requirement:** The UI recalculates the new RIME score in $< 100\text{ms}$ ([NFR-070](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr)), dynamically updating the preview badge.
3. **Mandatory Justification:** The confirmation button remains disabled until the Planner enters a technical justification containing at least $15$ non-whitespace characters.
4. **Cryptographic Integrity Hash ([TR-001](../../../requirements/common/TR-001.md), [ADR-003](../../../architecture/adr/ADR-003.md)):** Upon confirmation, the client dispatches an `AdjustWorkClassCommand`. The backend system atomically commits the work class change, rescores the backlog item, and appends an immutable record into the audit trail:
   $$\text{PayloadHash} = \text{SHA-256}(\text{PreviousHash} \parallel \text{PlannerUserId} \parallel \text{WorkRequestId} \parallel \text{PreviousScore} \parallel \text{CalculatedScore} \parallel \text{TechnicalJustification} \parallel \text{TimestampUtc})$$
5. **Re-sorting:** The backlog grid automatically re-sorts descending, moving the modified request to its new objective position without page reload.

---

#### 5.3.2. Asset without Defined Criticality Fail-Safe Workflow (AF-002)

To prevent unconfigured equipment criticality from artificially burying a critical maintenance intervention:

1. **Fail-Safe Trigger:** When a work request references an equipment unit whose `AssetCriticality` is unconfigured in the master catalog.
2. **Pessimistic Floor Assignment:** The system overrides the multiplicative calculation and assigns a **minimum floor score of 75** (placing the item in the *Schedule / High Category* band), regardless of how low the selected Work Class weight is.
3. **Visual Highlighting:** The request row renders with an amber warning indicator in the criticality column (`Unconfigured / Floor: 75`), and the top header notification button (`CMP-02`) displays an active warning badge without shifting the vertical layout of the data grid.
4. **Reliability Notification (`CMP-06`):** Clicking the header notification badge opens the Criticality Governance Dialog (`CMP-06`). From this dialog, the Planner can either click *"Filter Affected Request"* to isolate the unconfigured equipment row in the grid or click *"Dispatch Reliability Notification"* to send an automated governance task to the Reliability Engineer responsible for populating the asset's technical sheet.

---

#### 5.3.3. Equipment Grouping Recommendations (FR-068)

1. **Clustering Algorithm:** On data load, the system groups all pending requests by `EquipmentUnitId`.
2. **Threshold Rule:** When $\text{Count}(\text{requests}) \ge 2$ for the same physical equipment:
   * The Inline Grouping Pill `CMP-05` renders inside the right zone of the Filter Toolbar (`CMP-04`), preserving full vertical viewport height for the backlog grid.
   * Text specifies: *"Suggested Batch: {Count} in {TagNumber} ({TotalHours} HH)"*.
   * Action link *"Filter Batch"* filters the data grid strictly to the affected asset, enabling the Planner to bundle interventions into a single planned shutdown or maintenance window.

---

#### 5.3.4. Workload Distribution Confirmation & Export (FR-069)

1. **Workload Confirmation ([UC-MTTO-026](../../../domain-models/use-cases/mtto/UC-MTTO-026.md) Step 7):** The bottom bar `CMP-12` tracks the cumulative estimated wrench hours of selected backlog items against the weekly team capacity. Clicking "Confirm Weekly Distribution" approves the selected items for scheduling, updating their status to `APPROVED` and transitioning authorized requests to Preventive Scheduling ([SCR-MTTO-001](SCR-MTTO-001.md)) or Predictive Scheduling ([SCR-MTTO-023](SCR-MTTO-023.md)).
2. **Data Portability ([FR-069](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr)):** Clicking the unified "Export Data" dropdown menu in `CMP-12` generates structured export packages (`CSV` or `JSON` for the full view or current selection) containing all prioritized metadata, factor breakdowns, asset serial numbers, and material availability flags for external reporting.

---

## 6. Industrial and Safety Considerations

* **ANSI/ISA-101 HPHMI Grayscale 90/10 Rule ([TR-011](../../../requirements/common/TR-011.md)):** The backlog dashboard utilizes a neutral, subdued grayscale background (`--dt-color-surface-base`, `--dt-color-surface-card`) to prevent cognitive fatigue during extended planning sessions. Saturated colors are strictly reserved for priority and shortage indicators:
  * Red (`--dt-color-alarm-critical`) is allocated exclusively to emergency **Do First** items ($80 - 100$) and out-of-stock material shortages (`OutOfStock`).
  * Amber (`--dt-color-alarm-warning`) is allocated to **Schedule** items ($50 - 79$), partial material availability (`PartiallyAvailable`), and fail-safe governance warnings.
  * Routine maintenance bands (**Plan** $20-49$ and **Wish** $1-19$) and normal operational states (`InStock` and `ReservedInWarehouse` material availability) render strictly in neutral grayscale (`--dt-color-text-body`, `--dt-color-text-muted`) with zero chromatic fills, reserving blue (`--dt-color-state-info`) exclusively for active selection states and the primary confirmation button.
* **Redundant Visual Coding:** In strict compliance with accessibility and high-performance HMI principles, priority bands never rely solely on color. Every priority badge (`CMP-08`) combines:
  1. A distinctive geometric symbol ($\blacklozenge$, $\blacktriangle$, $\blacksquare$, $\bullet$).
  2. High-contrast semantic token color.
  3. Explicit numeric score ($1..100$) and text category label.
* **Status Badge & Counter Discipline (Anti-Badge-Inflation Principle per [DT-UI-DS-DOC-001 §6.5](../../DT-UI-DS-DOC-001.md#65-status-badge-counter-discipline-anti-badge-inflation-principle)):** Interactive status badges are strictly reserved for dynamic state lifecycle containers (`CMP-08`), shortage alerts, and interactive quantitative counters (`CMP-03`). Static metadata (such as user roles, work class descriptions, or equipment serials) and normal material availability states render strictly as structured plain text using subdued metadata typography (`--dt-color-text-muted`), preventing visual clutter and alarm desensitization.
* **Typography Hierarchy:** Primary asset tags and request identifiers use monospace data and primary text tokens (`--dt-font-mono-data`, `--dt-color-text-primary`), while technical descriptions and secondary metadata use body and caption tokens (`--dt-font-body-md`, `--dt-font-caption`) in muted slate (`--dt-color-text-muted`) to prevent visual crowding.
* **Fail-Safe Principle ([ASR-002](../../../architecture/asr/DT-ARQ-ASR-001.md#2-real-time-loto-security-and-fail-safe), AF-002):** Lack of asset metadata is treated conservatively. Setting unconfigured assets to a priority floor of 75 ensures that missing technical data cannot lead to deferred maintenance on potentially hazardous or production-critical equipment.
* **Cryptographic Integrity & Segregation of Duties ([TR-001](../../../requirements/common/TR-001.md), [TR-006](../../../requirements/common/TR-006.md)):** Manual adjustment of priority parameters directly impacts equipment reliability and operational safety. All adjustments mandate technical justifications and are sealed in the immutable SHA-256 audit chain. The ability to modify priority order manually without changing Work Class is strictly restricted to authorized Maintenance Supervisors ([NFR-062](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr)).

---

## 7. Frontend Component Contract (Blazor / Razor)

### 7.1. Component Hierarchy & File Mapping

```text
Pages/
└── RimeBacklogDashboardPage.razor                     # Root View (SCR-MTTO-026)
    ├── PortalSidebarNav.razor                         # CMP-01: Collapsible desktop navigation sidebar
    ├── BacklogHeaderBar.razor                         # CMP-02: Top breadcrumb, alert trigger, and user badge
    ├── BacklogSummaryCards.razor                      # CMP-03: 5-card interactive KPI filter summary
    ├── BacklogFilterToolbar.razor                     # CMP-04: Dropdowns, search, and inline grouping pill
    │   └── GroupingRecommendationPill.razor           # CMP-05: Inline equipment batching trigger
    ├── CriticalityGovernanceModal.razor               # CMP-06: AF-002 Unconfigured asset governance modal
    ├── PrioritizedBacklogGrid.razor                   # CMP-07: Dense virtualized tabular data grid (9 columns)
    │   ├── PriorityBandBadge.razor                    # CMP-08: Redundant category badge
    │   └── MaterialAvailabilityIndicator.razor        # HPHMI material availability text/shortage pill
    ├── BacklogWorkspaceDock.razor                     # CMP-13: Workspace dock container with vertical tab strip
    │   ├── BacklogItemInspectionRail.razor            # CMP-09: Contextual request inspection, promotion & calibration rail
    │   │   └── RimeBreakdownCard.razor                # CMP-10: FR-066 embedded factor decomposition
    │   └── ChainedAuditLogPane.razor                  # CMP-11: Integrated cryptographic audit trail tab pane
    └── WorkloadConfirmationFooter.razor               # CMP-12: Sticky capacity footer and unified export menu
```

---

### 7.2. Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)

#### 7.2.1. `RimeBacklogDashboardPage.razor` (Root View Parameter Contract)

```csharp
// Route & Query Parameters for RimeBacklogDashboardPage.razor (SCR-MTTO-026)
[Parameter, SupplyParameterFromQuery(Name = "loc")]
public string? SelectedFunctionalLocationTag { get; set; }

[Parameter, SupplyParameterFromQuery(Name = "band")]
public string? InitialBandFilter { get; set; }
```

#### 7.2.2. Subcomponent Parameter Contracts (`CMP-01` – `CMP-13`)

```csharp
// CMP-01: PortalSidebarNav.razor
[Parameter] public bool IsCollapsed { get; set; }
[Parameter] public string ActiveRouteCode { get; set; } = "SCR-MTTO-026";
[Parameter] public EventCallback<bool> OnCollapseToggled { get; set; }

// CMP-02: BacklogHeaderBar.razor
[Parameter, EditorRequired] public string OperatorBadgeCode { get; set; } = default!;
[Parameter, EditorRequired] public string OperatorDisplayName { get; set; } = default!;
[Parameter] public int ActiveGovernanceAlertCount { get; set; }
[Parameter] public EventCallback OnOpenGovernanceAlertModal { get; set; }

// CMP-03: BacklogSummaryCards.razor
[Parameter, EditorRequired] public BacklogSummaryMetricsDto Metrics { get; set; } = default!;
[Parameter] public RimePriorityBand? ActiveBandFilter { get; set; }
[Parameter] public EventCallback<RimePriorityBand?> OnBandFilterSelected { get; set; }

// CMP-04 & CMP-05: BacklogFilterToolbar.razor & GroupingRecommendationPill.razor
[Parameter] public string? SelectedLocationFilter { get; set; }
[Parameter] public WorkClassCode? SelectedWorkClassFilter { get; set; }
[Parameter] public string? SearchQuery { get; set; }
[Parameter] public EquipmentGroupingSuggestionDto? GroupingSuggestion { get; set; }
[Parameter] public EventCallback<string?> OnLocationFilterChanged { get; set; }
[Parameter] public EventCallback<WorkClassCode?> OnWorkClassFilterChanged { get; set; }
[Parameter] public EventCallback<string?> OnSearchQueryChanged { get; set; }
[Parameter] public EventCallback<string> OnApplyGroupingCluster { get; set; }
[Parameter] public EventCallback OnResetFilters { get; set; }

// CMP-06: CriticalityGovernanceModal.razor
[Parameter] public bool IsVisible { get; set; }
[Parameter] public BacklogItemDto? UnconfiguredItem { get; set; }
[Parameter] public EventCallback<string> OnFilterAffectedEquipment { get; set; }
[Parameter] public EventCallback<Guid> OnDispatchReliabilityNotification { get; set; }
[Parameter] public EventCallback OnClose { get; set; }

// CMP-07 & CMP-08: PrioritizedBacklogGrid.razor & PriorityBandBadge.razor
[Parameter, EditorRequired] public IReadOnlyList<BacklogItemDto> BacklogItems { get; set; } = [];
[Parameter] public IReadOnlySet<Guid> SelectedItemIds { get; set; } = new HashSet<Guid>();
[Parameter] public Guid? InspectedItemId { get; set; }
[Parameter] public EventCallback<Guid> OnToggleRowSelection { get; set; }
[Parameter] public EventCallback<BacklogItemDto> OnInspectRowRequested { get; set; }

// CMP-13: BacklogWorkspaceDock.razor
[Parameter] public bool IsOpen { get; set; }
[Parameter] public BacklogDockTab ActiveTab { get; set; } = BacklogDockTab.Detail;
[Parameter] public EventCallback<BacklogDockTab> OnTabChanged { get; set; }
[Parameter] public EventCallback OnClosed { get; set; }

// CMP-09: BacklogItemInspectionRail.razor hosted inside CMP-13
[Parameter] public BacklogItemDto? TargetItem { get; set; }
[Parameter] public EventCallback<AdjustWorkClassCommand> OnConfirmed { get; set; }
[Parameter] public EventCallback<Guid> OnPromoteToWorkOrder { get; set; }

// CMP-10: RimeBreakdownCard.razor hosted inside CMP-09
[Parameter] public RimeCalculationBreakdownDto? Breakdown { get; set; }

// CMP-11: ChainedAuditLogPane.razor hosted inside CMP-13
[Parameter, EditorRequired] public IReadOnlyList<ChainedAuditEntryDto> AuditEntries { get; set; } = [];

// CMP-12: WorkloadConfirmationFooter.razor
[Parameter] public int SelectedCount { get; set; }
[Parameter] public decimal SelectedWrenchHours { get; set; }
[Parameter] public decimal WeeklyCapacityHours { get; set; } = 40.0m;
[Parameter] public EventCallback OnConfirmWeeklyDistribution { get; set; }
[Parameter] public EventCallback<BacklogExportFormat> OnExportRequested { get; set; }
```

#### 7.2.3. Data Transfer Objects (DTOs) & Commands

```csharp
public record BacklogItemDto(
    Guid Id,
    Guid WorkRequestId,
    Guid EquipmentUnitId,
    Guid FunctionalLocationId,
    string WorkRequestNumber,
    string Description,
    string FunctionalLocationTag,
    string FunctionalLocationName,
    string EquipmentTag,
    string EquipmentSerialNumber,
    string EquipmentModel,
    string MaintainableItemName,
    WorkClassCode WorkClass,
    int? AssetCriticality,
    int PriorityScore,
    RimePriorityBand PriorityBand,
    bool IsFailSafeApplied,
    decimal EstimatedWrenchHours,
    MaterialAvailabilityStatus MaterialStatus,
    DateTimeOffset RequestDate,
    string Status
);

public record BacklogSummaryMetricsDto(
    int TotalBacklogCount,
    decimal TotalEstimatedHours,
    int DoFirstCount,
    int ScheduleCount,
    int PlanCount,
    int WishCount
);

public record EquipmentGroupingSuggestionDto(
    Guid EquipmentUnitId,
    Guid FunctionalLocationId,
    string FunctionalLocationTag,
    string EquipmentTag,
    string EquipmentSerialNumber,
    int PendingRequestCount,
    decimal TotalEstimatedHours
);

public record ChainedAuditEntryDto(
    Guid AuditEntryId,
    DateTimeOffset TimestampUtc,
    string WorkRequestNumber,
    string FunctionalLocationTag,
    string OperatorBadgeCode,
    int PreviousScore,
    int NewScore,
    string TechnicalJustification,
    string PreviousHash,
    string PayloadHash
);

public enum RimePriorityBand
{
    DoFirst,    // 80 - 100
    Schedule,   // 50 - 79
    Plan,       // 20 - 49
    Wish        // 1 - 19
}

public enum WorkClassCode
{
    SafetyEnvironmentalEmergency = 10,
    ProductionShutdown = 9,
    HighPriorityProcess = 8,
    RegulatedPreventive = 7,
    SystematicPreventive = 6,
    PredictiveMaintenance = 5,
    NonCriticalCorrective = 4,
    EngineeringModification = 3,
    AestheticOrderCleanliness = 2,
    OperationalConvenience = 1
}

public enum MaterialAvailabilityStatus
{
    InStock,
    PartiallyAvailable,
    ReservedInWarehouse,
    OutOfStock
}

public enum BacklogExportFormat
{
    FullViewCsv,
    FullViewJson,
    SelectedItemsJson
}

public enum BacklogDockTab
{
    Detail,
    Audit
}

public record AdjustWorkClassCommand(
    Guid WorkRequestId,
    WorkClassCode NewWorkClass,
    int CalculatedScore,
    string TechnicalJustification,
    Guid PlannerUserId,
    string PreviousHash
);

public record RimeCalculationBreakdownDto(
    Guid WorkRequestId,
    string ActiveStrategyName,
    int AssetCriticality,
    int WorkClassWeight,
    int RawScore,
    int FinalScore,
    bool IsFailSafeApplied,
    string ApplicableStandardReference
);
```

---

### 7.3. Client-Side DOM & Interop Bridge

1. **Virtualization Interop (`IVirtualizationInterop`):** Client-side viewport scroll measurement capability that lazily renders only visible table rows within the scrollable grid container, keeping UI response times under $100\text{ms}$ during high-density backlog scrolling.
2. **Real-Time Recalculation Bridge:** Client-side evaluation within the Work Class Inspection & Calibration Rail (`CMP-09`) that computes the candidate score instantaneously in WebAssembly without dispatching server roundtrips until final confirmation.
3. **Keyboard Shortcut Interop (`IKeyboardShortcutInterop`):** Focus and keybinding capability capturing `ArrowUp`, `ArrowDown`, `Ctrl+K`, and `Escape` events to support mouse-free desktop workstation operation.
4. **Cryptographic Digest Preview Interop (`ICryptoInterop`):** Client-side SHA-256 digest capability that computes the candidate `PayloadHash` in real time as the Planner enters the technical justification, providing immediate visual verification of the chained audit signature.

---

## 8. Layout and Responsive Adaptability

| Viewport / Breakpoint | Layout Organization | Ergonomic Rules |
| :--- | :--- | :--- |
| **Desktop Workstation**<br>($\ge 1920\text{px}$, `--dt-breakpoint-xl`) | Asymmetric workstation split: prioritized 9-column data grid canvas paired with the persistent `CMP-13` right dock container (`--dt-layout-drawer-width-desktop`); navigation sidebar expanded; 5 summary KPI cards in one row; zero horizontal layout shift. | Optimized for mouse and keyboard navigation; row height `--dt-layout-table-row-height`; single-click row inspection and side-by-side comparison without modal blindness; persistent vertical pill tabs. |
| **Tablet Landscape**<br>($1280\text{px} - 1919\text{px}$, `--dt-breakpoint-lg`) | Navigation sidebar collapses to icon-only rail; `CMP-13` becomes a collapsible slide-over dock (`--dt-layout-drawer-width-tablet`); KPI cards remain fluid; grouping pill wraps when required. | Touch and pointer targets comply with `--dt-control-height-sm`; dock panel overlays without darkening the workspace; horizontal scroll reserved for wide table columns. |
| **Tablet Portrait / Secondary Terminal**<br>($768\text{px} - 1279\text{px}$, `--dt-breakpoint-md`) | Sidebar becomes off-canvas; KPI cards wrap; `CMP-13` transitions to a collapsible bottom sheet using `--dt-layout-bottom-sheet-height-expanded` with tab switcher in header; data grid prioritizes core operational columns. | Touch targets $\ge 48\times 48\text{px}$ with `--dt-space-2` spacing; row inspection remains non-blocking and keyboard-independent. |

---

## 9. Traceability and Requirements Matrix

| Requirement | Addressed in Component | Verification & Implementation Mechanism |
| :--- | :--- | :--- |
| [FR-058](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-07`, `CMP-10` | Retrieves numerical asset criticality ($1..10$) from ISO 14224 Functional Location and Equipment Unit master records. |
| [FR-059](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-07`, `CMP-09` | Mandates Work Class selection associating standardized numerical weight ($1..10$) per [DT-DM-DOC-001 §4.24](../../../domain-models/class/DT-DM-DOC-001.md#424-workrequestworkclasscode-work-class-rime). |
| [FR-060](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-07`, `CMP-10` | Priority score calculated deterministically by delegating to active strategy of RIME prioritization engine ([ADR-002](../../../architecture/adr/ADR-002.md)). |
| [FR-065](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-07` | Each row renders priority metadata, affected equipment unit, intervention type, estimated costs, and wrench hours. |
| [FR-066](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-10` | RIME factor breakdown card in `CMP-09` displays exact factor decomposition and cites ISO 55001 (§6.2.2) standards. |
| [FR-067](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-04` | Advanced filtering capabilities by Priority Category, Functional Location hierarchy, Work Class, and dates. |
| [FR-068](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-05` | Generates smart grouping recommendations when detecting $\ge 2$ pending interventions on the same physical equipment. |
| [FR-069](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-12` | Export button outputs prioritized backlog in structured formats (`CSV` and `JSON`) for external analytics. |
| [FR-074](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-07`, `CMP-10` | Deterministic calculation engine: identical criticality and work class inputs produce identical scores across the system. |
| [FR-075](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-07` | Event-driven background recalculation upon changes to master asset criticality in catalog. |
| [FR-076](../../../requirements/user-stories/mtto/MTTO-026.md#functional-requirements-fr) | `CMP-02`, `CMP-09` | Significant category shifts (e.g., transition into "Do First") trigger event-driven pub-sub notifications to planners. |
| [NFR-061](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr) | `CMP-03`, `CMP-08` | Classifies and visually differentiates requests into 4 priority bands with redundant shape and color coding. |
| [NFR-062](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr) | `CMP-07` | Backlog organized strictly descending by RIME score; manual alteration restricted to authorized Supervisor roles. |
| [NFR-070](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr) | `CMP-09` | Work Class priority recalculation in `CMP-09` executes in $< 100\text{ms}$ in the user interface. |
| [NFR-071](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr) | `CMP-07` | Virtualized data grid maintains response times $< 2\text{s}$ for datasets exceeding $500$ rows. |
| [NFR-072](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr) | `CMP-10` | Prioritization strategy parameters versioned and protected against unauthorized tampering ([ADR-002](../../../architecture/adr/ADR-002.md)). |
| [NFR-073](../../../requirements/user-stories/mtto/MTTO-026.md#non-functional-requirements-nfr) | `CMP-07`, `CMP-08` | Visibility of technical priority scores restricted to authorized planning and reliability governance roles. |
| [TR-001](../../../requirements/common/TR-001.md) | `CMP-09`, `CMP-11` | Immutable append-only audit trail logging with SHA-256 hash chaining for all priority adjustments. |
| [TR-006](../../../requirements/common/TR-006.md) | `CMP-01`, `CMP-02` | Enforces RBAC permissions (`Maintenance Planner`, `Maintenance Supervisor`, `Reliability Engineer`). |
| [TR-011](../../../requirements/common/TR-011.md) | `CMP-01`..`CMP-13` | Strict adherence to ANSI/ISA-101 HPHMI: 90/10 neutral grayscale canvas, saturated color reserved for alarms/bands. |
| [ADR-002](../../../architecture/adr/ADR-002.md) | `CMP-07`, `CMP-10` | Encapsulates RIME calculation under Strategy Pattern (`IRimeCalculator`), decoupling domain entities. |
