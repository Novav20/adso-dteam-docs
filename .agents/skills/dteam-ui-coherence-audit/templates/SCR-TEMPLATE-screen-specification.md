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
status: Draft | In Review | Approved
---

# SCR-MOD-000: Functional Screen Title

## 1. Purpose and Operational Context
* **View Objective:** Concise definition of the operational task and cognitive goal achieved on this screen.
* **Primary Target Persona:** Target role dictating ergonomics, touch targets, and interaction density.
* **Secondary Personas:** Secondary roles with read-only, supervisory, or auditing permissions.
* **Operational Context:** Physical environment and hardware contexts (e.g., Desktop web workstation in control room, Industrial tablet in field).
* **Mode of Operation:** Nature of interaction (e.g., Supervisory monitoring, passive navigation, transactional execution, safety interlock). Explicitly state if industrial control commands (DCS/SCADA) are excluded.

> *Rule:* State operational environment and hardware context qualitatively (e.g., industrial tablet in field dead-zones, engineering desktop workstation). Never embed breakpoint tokens (`--dt-breakpoint-*`), container pixel/vh dimensions, or domain enum lists in Section 1. These belong strictly to Section 5, Section 7, and Section 8.

---

## 2. Visual Artifact

![SCR-MOD-000 Screenshot](assets/SCR-MOD-000-screenshot.png)

> *Note: Production UI prototype capture (1920x1080) illustrating the spatial layout and component placement. Standalone SVG wireframes are prohibited; the visual artifact is always a high-definition screenshot of the companion HTML prototype.*

---

## 3. Functional Component Inventory

> The base grid, typography, neutral palettes, and minimal tactile contact areas are inherited from [DT-UI-DS-DOC-001](../../DT-UI-DS-DOC-001.md). This table defines the present components, their semantic tokens, and their architectural roles. Detailed interaction rules, layout constraints, and geometric algorithms are strictly specified in Section 5.
>
> *Rule:* Table cells must strictly serve as a visual catalog of roles, semantic tokens, and pointers to Section 5. Never embed interaction algorithms, clamping math, state machine logic, raw CSS styles, hardware layout dimensions (e.g., `640px`, `45vh`), status strings, domain enum lists, or NFR citations in table cells. Column 4 ("Semantic Token") must reference explicit Design System tokens (`--dt-*`). Badges and pills are strictly reserved for dynamic state lifecycles and quantifiable counters; static invariant attributes must be modeled as plain structured text with neutral muted tokens (`--dt-color-text-muted`).

| ID | Control / Component | Visual Role / Content | Semantic Token | Architectural Role & Reference |
| :--- | :--- | :--- | :--- | :--- |
| `CMP-01` | Component Name | High-level content and visual representation | Surface: `--dt-color-surface-*`<br>Border: `--dt-color-border-*` | High-level architectural purpose and pointer to §5 for behavioral logic. |

---

## 4. Screen State Matrix

| State | Visual Modification in the Interface | Activation Condition |
| :--- | :--- | :--- |
| **Normal (Default)** | Neutral grayscale surfaces and indicators in baseline state. | Successful view initial load without active alarms or pending selections. |
| **Loading** | Visual skeleton shimmer or dimmed activity indicator. | Asynchronous data fetch or initial canvas geometry parsing in progress. |
| **Selected** | Primary entity highlighted with informational selection border. Contextual panel deployed. | Direct user tap/click on entity or command palette search match. |
| **Alarm / Alert** | Redundant coding (geometric symbol + saturated alarm color). | Safety interlock, process limit excursion, or asset trip condition. |
| **Diagnostic / Offline** | Priority 4 Diagnostic styling: muted typography, stale indicator, zero process alarm colors. | Communication disruption, stale cache fallback, or heartbeat timeout. |

---

## 5. Interaction Rules and Data Flow

### 5.1. Initial Load & Lifecycle
1. Description of initial view state, default zoom/coordinates, and unselected baseline.
2. Initial data subscriptions and local caching retrieval policies.
3. **Presentation Layer Boundary Invariant:** UI sequence diagrams (Mermaid) must model interactions strictly between the User/Technician (`Tech`), the presentation component (`UI`), external client hardware/interop (`Scanner`/`Sensor`), and the boundary Application Service API (`API`). Private backend-to-backend hops (e.g., `API ->> Worker`, `API ->> DB`, or internal `API ->> API` self-calls) are prohibited presentation leaks.

### 5.2. Spatial Navigation & Tactile Mechanics
> *Rule:* Section 5.2 is the SSoT for tactile gesture physics, drag handle hysteresis thresholds, natural drawer heights, and focal pan/zoom offsets. Container widths, breakpoint-to-device mappings, and overall layout organization belong strictly to Section 8.
1. **Desktop vs. Tablet Interaction Modality:** Explicit input disambiguation (e.g., middle-click panning vs. tactile gesture threshold).
2. **Layout Shift Invariants:** Explicit fixed dimensions (e.g., badge widths, slot heights) preventing layout thrashing.
3. **Gesture Physics & Snap Thresholds:** Tactile physics, drag handle hysteresis, natural heights, and minimize transitions.

### 5.3. Domain Workflows & Telemetry
1. Real-time subscription, debouncing, and payload mapping rules.
2. State validation, business rule evaluation, and fail-safe handling.
3. Command dispatch contracts (API endpoint, typed DTO payload, idempotency headers, and HTTP response handling). Formulate data mutations strictly as command dispatch invocations via typed DTO payloads, HTTP endpoints, and idempotent queuing.
4. **Controlled Vocabulary & Enum Hygiene:** Reference domain enums directly by their strongly-typed C# enum name defined in §7.2.3 (e.g., "Controlled vocabulary mapped to enum `DetectionMethod` (§7.2.3)"). Prohibit exhaustive string literals in prose or LaTeX set equations.
5. **Offline Protocol Referencing:** When an offline protocol is formalized in §5.3.5, command dispatch error handling in §5.3.4 must point directly to it rather than duplicating outbox persistence steps.

---

## 6. Industrial and Safety Considerations

* **HPHMI Philosophy ([TR-011](../../../requirements/common/TR-011.md)):** Grayscale baseline; color reserved strictly for alarms with redundant shape coding.
* **Alarm vs. Diagnostic Segregation (ISA-101):** Diagnostic failures must never masquerade as process alarms.
* **Fail-Safe Integrity:** Pessimistic default states on communication loss or ambiguous data.
* **Typography Hierarchy:** Primary asset tags and identifiers use monospace data and primary text tokens (`--dt-font-mono-data`, `--dt-color-text-primary`), while technical descriptions and secondary metadata use body and caption tokens (`--dt-font-body-md`, `--dt-font-caption`) in muted slate (`--dt-color-text-muted`). Prohibit raw numeric CSS font-weights (`400..700`) or literal pixel/rem sizes.
* **Interactive Control Neutrality:** Active sort chevrons, selection indicators, and focus outlines must bind to neutral tokens (`--dt-color-border-focus`, `--dt-color-text-muted`), never uncodified saturated accents.

---

## 7. Frontend Component Contract (Blazor / Razor)

### 7.1. Component Hierarchy & File Mapping

```text
Pages/
└── ScreenNamePage.razor                       # Root View (SCR-MOD-000)
    ├── CanvasOrContainer.razor                # CMP-01: Main container
    └── ContextPanel.razor                     # CMP-02: Auxiliary panel
```

### 7.2. Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)

#### 7.2.1. `ScreenNamePage.razor` (Root View)
```csharp
[Parameter]
public required string EntityId { get; set; }
```

#### 7.2.2. Subcomponent Parameters (`CMP-01` to `CMP-XX`)
```csharp
// Pure [Parameter] properties for child razor components
```

#### 7.2.3. Data Transfer Objects (DTOs)
```csharp
public record ScreenDataDto
{
    public required string Id { get; init; }
}
```

### 7.3. Client-Side DOM & Interop Bridge
1. **Pointer & Viewport Tracking (`IPointerInterop`):** Architectural boundary for client-side JavaScript interop handling performance-critical gestures and matrix transforms.
2. **Event Throttling & Debouncing:** Policies preventing network saturation during continuous manipulations.
3. **Encrypted Offline Storage (`IOfflineStorage`):** Interop interface for local encrypted cache and transactional outbox queuing.

---

## 8. Layout and Responsive Adaptability

> *Rule:* Section 8 is the SSoT for responsive breakpoint ranges, container widths, and layout stacking across viewports. Ergonomic interaction physics, drag thresholds, and mathematical centering offsets belong to §5.2 and must be referenced, not duplicated. Prohibit raw CSS `calc()` expressions in table cells; use descriptive architectural offsets.

| Viewport / Breakpoint | Layout Organization | Ergonomic Rules |
| :--- | :--- | :--- |
| **Desktop Workstation**<br>($\ge 1920\text{px}$, `--dt-breakpoint-xl`) | Full horizontal layout; lateral docked panels (`--dt-layout-drawer-width-desktop`). | Mouse wheel focal zoom; middle-click pan; dense dual-column data inspection. |
| **Industrial Tablet Landscape**<br>($1280\text{px} - 1919\text{px}$, `--dt-breakpoint-lg` / $1280\times 800\text{px}$) | Split canvas and side panel layout (`--dt-layout-drawer-width-tablet`). | Touch pan threshold ($4\text{px}$); gloved touch targets $\ge 48\text{px}$. |
| **Industrial Tablet Portrait**<br>($768\text{px} - 1279\text{px}$, `--dt-breakpoint-md` / $800\times 1280\text{px}$) | Vertical stacked layout; bottom sheet drawer (`--dt-layout-bottom-sheet-height-initial`). | Drag handle gesture mechanics; sticky action buttons. |

---

## 9. Traceability and Requirements Matrix

| Requirement | Addressed in Component | Verification & Implementation Mechanism |
| :--- | :--- | :--- |
| **FR-XXX** | `CMP-XX` | Concrete functional verification and technical mechanism. |
| **NFR-XXX** | `CMP-XX` | Quantitative performance or reliability threshold verification. |
| **TR-XXX** | `CMP-XX` | Transversal architecture or design system compliance rule. |
