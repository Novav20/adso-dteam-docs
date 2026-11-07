---
id: SCR-MTTO-002
title: Mobile Work Order Execution, ISO 14224 Failure Coding, and Technical Closure
module: MTTO
isa101_level: L4 (Diagnostic / Master Detail / Field Execution)
platform: Shared Component
target_device: Industrial Tablet (Primary) | Mobile Data Collector
roles:
  - Maintenance Technician
  - Maintenance Supervisor
  - Reliability Engineer
user_stories:
  - "[[MTTO-002]]"
use_cases:
  - "[[UC-MTTO-002]]"
version: 1.5
date: 2026-11-06
status: Stable
---

# SCR-MTTO-002: Mobile Work Order Execution, ISO 14224 Failure Coding, and Technical Closure

## 1. Purpose and Operational Context

* **View Objective:** Mobile field technical execution, taxonomy failure diagnosis, and formal technical closure of active Work Orders (ANSI/ISA-101 Level 4). Enforces strict ISO 14224 reliability coding (Maintainable Item, Failure Mode, Mechanism, Cause, Detection Method, Operational Condition, and Operational Impact), actual Wrench Time capture, immutable photographic evidence acquisition with SHA-256 cryptographic hashing ([TR-003](../../../requirements/common/TR-003.md)), and atomic status transition to `COMPLETE` ([DT-ERD-DOC-001 §3.2.6](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#326-work_orders)), with full offline-first resilience via encrypted local database ([TR-002](../../../requirements/common/TR-002.md)) and transactional outbox synchronization ([TR-007](../../../requirements/common/TR-007.md)).
* **Primary Target Persona:** Maintenance Technician operating on rugged industrial tablets in Class I Div 2 hazardous process areas under adverse conditions (glare, noise, chemical-resistant gloves). Detailed responsive profiles and breakpoints are specified in Section 8.
* **Secondary Personas:**
  * **Maintenance Supervisor:** Reviews field execution metrics, verifies Wrench Time variance, and performs administrative closure (`CLOSED`).
  * **Reliability Engineer:** Consumes structured ISO 14224 failure distributions for Weibull analysis, Bad Actor tracking, and MTBF/MTTR calculations.
  * **HSEQ Inspector:** Audits the cryptographic hash chain of field evidence and verifies de-isolation safety handover protocols.
* **Operational Context:** Deployed on portable industrial tablets and intrinsically safe handheld devices. Requires tactile targets, high-contrast typography, zero nested modal traps, and resilient persistence against unexpected power loss or radio-frequency shadowing inside tank dikes and pump battery limits. Tactile dimensions are specified in §5.2 and §8.
* **Mode of Operation:** Transactional Execution & Field Technical Certification mode. Direct DCS/SCADA process control manipulation is strictly excluded; field mechanics log physical intervention data, parts consumption, and diagnostic classifications.
* **Upstream & Downstream Navigation Invariants:**
  * **Upstream Continuity:** Directly launched upon successful Zero Energy verification and work initiation in [SCR-VIS-011](../vis/SCR-VIS-011.md), automatically transitioning the Work Order lifecycle state to `IN_PROGRESS`.
  * **Downstream Transitions:** Hosts the trigger for the Rotable Asset Swap modal ([SCR-INV-025](../inv/SCR-INV-025.md)) when physical equipment replacement is required, and routes to the RIME Backlog Dashboard ([SCR-MTTO-026](./SCR-MTTO-026.md)) upon confirmed technical closure.

---

## 2. Visual Artifact

### 2.1. Tab 1: Scope & Timing (Light Theme)
![SCR-MTTO-002 Scope & Timing](assets/SCR-MTTO-002-tab1-light.png)

> *Note: Production UI prototype capture illustrating the mobile execution header, frameless task checklist with monochromatic completion checks, decoupled timing master card with dual telemetry gauges, and sticky action bar.*

### 2.2. Tab 2: Materials & Spares Allocation (Light Theme)
![SCR-MTTO-002 Materials & Spares](assets/SCR-MTTO-002-tab2-light.png)

> *Note: Production UI prototype capture illustrating allocated warehouse spares with tactile quantity steppers and contextual rotable asset swap launch pane.*

### 2.3. Tab 3: ISO 14224 Diagnosis (Dark Theme)
![SCR-MTTO-002 ISO 14224 Diagnosis](assets/SCR-MTTO-002-tab3-dark.png)

> *Note: Production UI prototype capture illustrating the 7-node sequential quality gate stepper and cascading taxonomy classification matrix in Dark Theme.*

### 2.4. Tab 4: Photographic Evidence (Dark Theme)
![SCR-MTTO-002 Photographic Evidence](assets/SCR-MTTO-002-tab4-dark.png)

> *Note: Production UI prototype capture illustrating cryptographic evidence acquisition, verified photo attachment cards with SHA-256 seal, and unlocked technical closure button.*

---

## 3. Functional Component Inventory

> The base layout, typography, and design tokens are inherited from [DT-UI-DS-DOC-001](../../DT-UI-DS-DOC-001.md). This table defines the present components, semantic tokens, and their architectural roles. Detailed interaction rules, layout constraints, and geometric algorithms are strictly specified in Section 5.

| ID | Control / Component | Visual Role / Content | Semantic Token | Architectural Role & Reference |
| :--- | :--- | :--- | :--- | :--- |
| `CMP-01` | Mobile Execution Header | Work Order & Asset context strip | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle` | Anchored header displaying Work Order ID, Target Equipment Name and Tag, Functional Location, active technician session, operational status badge, neutral de-energized LOTO status capsule, integrated telemetry chip, and queued outbox badge. Detailed in §5.1 and §5.3.5. |
| `CMP-02` | Operational Tabs Controller | 4-channel flush tab bar | Surface: `--dt-color-surface-base`<br>Active Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle`<br>Active Indicator: `--dt-color-text-primary` | Edge-to-edge flush navigation bar allowing instant switching between: `[1. Scope]`, `[2. Spares]`, `[3. ISO Diagnosis]`, and `[4. Evidence]`. Active tab merges visually with the main workspace (`--dt-color-surface-card`) and displays a high-contrast bottom indicator (`--dt-color-text-primary`). Detailed in §5.2. |
| `CMP-03` | Scope & Timing Panel | Frameless step checklist & unified timing cockpit master card | Surface: `--dt-color-surface-card`<br>Divider: `--dt-color-border-subtle` | Displays planned task scope items directly on the continuous workspace surface with tactile completion checkboxes, separated by a full-height vertical divider (`--dt-color-border-subtle`) from the right-hand timing cockpit master card: Inset telemetry widgets section with dual circular gauges, `FieldStopwatchSubcard` with subtle fill, and `ActualLaborHoursSection` with circular steppers, recessed hours display, quick preset pills, and full-width CTA pill. Detailed in §5.2 and §5.3.1. |
| `CMP-04` | Materials & Spares Allocation Panel | Frameless parts consumed list & equipment rotation pane | Surface: `--dt-color-surface-card`<br>Divider: `--dt-color-border-subtle` | Lists reserved warehouse spare parts directly on the continuous workspace surface with tactile quantity steppers and plain-text warehouse metadata, separated by a full-height vertical divider from the right-hand equipment rotation pane hosting the trigger for modal [SCR-INV-025](../inv/SCR-INV-025.md) when an equipment swap is required. Detailed in §5.2 and §5.3. |
| `CMP-05` | ISO 14224 Multi-Tier Taxonomy Matrix | Frameless 7-tier sequential failure coding matrix | Surface: `--dt-color-surface-card`<br>Divider: `--dt-color-border-subtle`<br>Control Border: `--dt-color-border-panel`<br>Popover Border: `--dt-color-border-hairline` | Core reliability data collection section separated from the quality gate stepper by a subtle top divider (`--dt-color-border-subtle`). Enforces sequential cascading custom popover dropdowns ($1 \to 7$) where each tier remains disabled until its predecessor is classified, resetting downstream selections upon upstream mutation: Maintainable Item, Failure Mode, Failure Mechanism, Failure Cause, Detection Method, Operational Condition, Operational Impact, Downtime Hours, and full-width Technical Observations. Detailed in §5.3.1. |
| `CMP-06` | ISO 14224 Hard Lock Indicator | Sequential 7-node quality gate stepper | Surface: `--dt-color-surface-card`<br>Node Border: `--dt-color-border-panel`<br>Link: `--dt-color-border-subtle` | Frameless sequential 7-node horizontal stepper unified with the `SCR-INV-005` progression architecture. Enforces strict ANSI/ISA-101.01 §6.2 grayscale discipline: active step displays high-contrast ring and inner pulse dot (`--dt-color-text-primary`), completed steps render neutral checkmarks, and pending steps remain muted without redundant lock pills or helper text. In portrait mode, nodes stack concise labels underneath circular step indicators while omitting subtitles and centering horizontal links through the indicators. Detailed in §5.3.2 and §8. |
| `CMP-07` | Cryptographic Evidence Capture Section | Frameless multi-evidence array uploader ($1 : 0..N$) & SHA-256 verifier | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle`<br>Hash: `--dt-font-mono-data` | Frameless multi-evidence container supporting $0..N$ attachments directly on the workspace surface. Displays dashed dropzone placeholder solely when empty ($0$ items); once $\ge 1$ attachment is captured, the dropzone is replaced by verified attachment cards while the action toolbar (`Capture Evidence` / `Select File`) remains accessible for additional captures. Detailed in §5.3.3. |
| `CMP-08` | Integrated Telemetry & Outbox Indicator | Zero-shift connection & local queue health indicator | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle` | Zero-shift diagnostic telemetry chip integrated into execution header (`CMP-01`), eliminating intrusive sticky banners (CLS = 0). Displays offline status, queued transaction count, and offline persistence status. Detailed in §5.3.5. |
| `CMP-09` | Technical Finalization Action Bar | Sticky bottom closure controller with arrow navigation | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle`<br>Elevation: `--dt-z-header-sticky`<br>Primary Button: `--dt-color-text-primary` | Fixed bottom action container sharing the workspace surface (`--dt-color-surface-card`), hosting progressive navigation arrow buttons and neutral high-contrast primary control `[Finalize Work Order]`. Hard-gated by the Boolean conjunction of `CMP-06` and `CMP-07`. Detailed in §5.2 and §5.3.4. |
| `CMP-10` | De-Isolation Safety Handover Strip | LOTO clearance acknowledgment strip | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle` | Flush safety acknowledgment strip reminding the technician that physical padlocks remain locked until formal de-isolation handover is executed prior to operational start-up. Detailed in §6. |

---

## 4. Screen State Matrix

| State | Visual Modification in the Interface | Activation Condition |
| :--- | :--- | :--- |
| **Normal / In Progress (Default)** | Header displays `IN_PROGRESS` in neutral high-contrast capsule badge (`--dt-color-surface-base`, `--dt-color-border-subtle`, `--dt-color-text-primary`). Checklist editable. Stopwatch counter increments. Tab 3 shows incomplete taxonomy. `CMP-09` `[Finalize Work Order]` is hard-disabled via the ISO Lock. | Initial load of `SCR-MTTO-002` following work authorization from `SCR-VIS-011`. |
| **Loading / Synchronizing** | Skeleton shimmer on form fields and spares table (`--dt-color-surface-raised`). Taxonomy dropdowns show animated loading indicator while hydrating local SQLite cache. Controls locked. | Initial data hydration from local SQLCipher cache or background delta synchronization in progress. |
| **Taxonomy Incomplete / Missing Fields (AF-001)** | Missing mandatory taxonomy selectors highlighted with dynamic asterisk (`*`). Sequential stepper `CMP-06` highlights the active next step with a neutral pulse indicator while keeping downstream dropdowns locked (`disabled`) per ISO 14224 causal hierarchy. Action button `CMP-09` remains disabled. | Technician attempts to finalize or navigates away while any of the 7 mandatory ISO fields or downtime is empty. |
| **Evidence Capturing & Hashing** | Camera viewfinder overlay active or file upload progress bar visible. Monospace hash chip displays animated status *"Computing SHA-256..."*. Validated photos replace the empty-state dashed dropzone with verified gallery cards ($1..N$) displaying thumbnail, file metadata, and tamper-resistant digital stamp (`SHA-256: [hash]`). Action toolbar remains active for additional captures. | Technician captures or selects photo evidence in `CMP-07`. |
| **Evidence Corrupt / Hash Mismatch (AF-003)** | File preview replaced by critical red border (`--dt-color-alarm-critical`) and error glyph (`#icon-ban`). Banner displays: *"File integrity error. SHA-256 discrepancy detected. Please recapture evidence"*. Form progression blocked. | Cryptographic verification detects corrupted binary stream or zero-byte payload (`TR-003-NFR-380`). |
| **Offline Mode (AF-002)** | Zero layout shift (CLS = 0). Header telemetry chip updates to `OFFLINE · [HH:MM]`, `[1 PENDING SYNC]` amber badge illuminates, and `[DE-ENERGIZED EQUIPMENT]` capsule is automatically hidden to avoid false certainty of unverified live telemetry. Local SQLCipher cache active. | Device loses Wi-Fi/cellular connectivity in field process areas (`ASR-001`). |
| **Ready to Finalize (Unlocked)** | `CMP-06` sequential 7-node stepper marks all 7 circular nodes as completed (`#icon-check`) with completed connecting links, updating the Tab 3 header badge to `[7/7]`. All media attachments display validated cryptographic seal. Action button `CMP-09` unlocks in high-contrast neutral primary styling (`--dt-color-text-primary`). | All 7 ISO 14224 fields selected + Downtime specified + Photo evidence captured with valid hash + Checklist attested. |
| **Technical Closure Complete** | Form transitions to read-only state. Header badge updates to `COMPLETE`. Standardized completion certificate modal (header with close `X`, body with structured key-value certificate rows and SHA-256 seal, footer with primary action `[Return to Work Orders]`) confirms closure and redirects to `SCR-MTTO-026`. | Technician confirms `[Finalize Work Order]`. System commits atomic transaction. |

---

## 5. Interaction Rules and Data Flow

### 5.1. Initial Load & Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Tech as Maintenance Technician
    participant VIS as SCR-VIS-011 LOTO
    participant UI as SCR-MTTO-002 Execution View
    participant Store as IOfflineStorage / SQLCipher
    participant Crypto as ICryptoInterop (Web Worker)
    participant API as Work Order Application Service

    Tech->>VIS: Confirms Zero Energy & Try-Out
    VIS->>UI: Navigates with Execution Context (WorkOrderId, TechnicianId)
    UI->>Store: Pre-hydrate ISO 14224 taxonomy & cached WO details
    Store-->>UI: Return taxonomies & checklist items
    Tech->>UI: Attests checklist tasks & captures wrench time (CMP-03)
    Tech->>UI: Confirms consumed spares (CMP-04)
    Tech->>UI: Classifies 7-tier ISO failure taxonomy (CMP-05)
    UI->>UI: Validates 7/7 completeness & unlocks ISO Lock meter (CMP-06)
    Tech->>UI: Captures photographic evidence (CMP-07)
    UI->>Crypto: Compute client-side SHA-256 hash asynchronously
    Crypto-->>UI: Return validated SHA-256 hash stamp
    Tech->>UI: Clicks [Finalize Work Order] (CMP-09)
    alt Network Connected
        UI->>API: POST /api/v1/work-orders/{id}/technical-closure (SubmitTechnicalClosureCommand + X-Idempotency-Key)
        API-->>UI: HTTP 200 OK (WorkOrderTechnicallyCompletedEvent)
        UI-->>Tech: Display completion certificate modal & navigate to SCR-MTTO-026
    else Disconnected / Offline Outbox (AF-002)
        UI->>Store: Enqueue SubmitTechnicalClosureCommand into encrypted outbox
        Store-->>UI: Offline lease queued confirmation
        UI-->>Tech: Display offline sync badge & return to backlog
    end
```

1. **Context Ingestion Contract:**
   * When navigated from [SCR-VIS-011](../vis/SCR-VIS-011.md), the route receives the initial execution context payload:
     $$\mathcal{P}_{\text{init}} = \langle \text{WorkOrderId}: \text{Guid}, \text{EquipmentTag}: \text{string}, \text{FunctionalLocation}: \text{string}, \text{TechnicianId}: \text{Guid}, \text{LotoStatus}: \text{LotoLockoutState} \rangle$$
   * If the initial Work Order status is `SCHEDULED`, the client dispatches an execution start command, transitioning the Work Order status to `IN_PROGRESS` with server-side audit timestamp logging.
2. **Local Cache Pre-Hydration (Offline Readiness):**
   * Pre-hydrates the ISO 14224 taxonomic datasets (maintainable items catalog, equipment class failure modes) from the local encrypted database ([TR-002](../../../requirements/common/TR-002.md)), guaranteeing zero network latency when populating dropdowns in field dead-zones.

### 5.2. Mobile Ergonomics & Tactile Mechanics

1. **Gloved Touch Target Invariant (ISO 9241-110 Clause 5.3 / `--dt-touch-target-mobile`):**
   * All interactive controls (checkboxes, dropdown triggers, camera buttons, tab headers, spare parts quantity steppers) enforce a minimal bounding box governed by `--dt-touch-target-mobile` with `--dt-space-2` separation, ensuring error-free operation with nitrile and leather field gloves.
   * Step navigation directional arrow buttons enforce an enlarged footprint governed by `--dt-control-width-nav-step` $\times$ `--dt-control-height-nav-step` (and `--dt-control-width-nav-step-mobile` $\times$ `--dt-control-height-nav-step-mobile` on mobile) with subtle neutral secondary surface fill (`--dt-color-surface-btn-secondary`), subtle perimeter ring (`--dt-color-border-subtle`), standard curvature (`--dt-radius-md`), and explicit SVG chevrons (`#icon-chevron-left`, `#icon-chevron-right`).
   * Custom scope checklist implements a frameless list layout with tactile circular check indicators (`--dt-control-size-checkbox`, `--dt-radius-full`): unselected items render a neutral hairline perimeter ring, while verified items fill with high-contrast monochromatic fill (`--dt-color-text-primary`) and an embedded checkmark in surface color. Individual item bounding boxes are purged in favor of subtle baseline dividers (`--dt-color-border-subtle`) and full-width touch hit rows.
2. **Asymmetric Layout Grids & Continuous Workspace Dividers (`CMP-03` & `CMP-04`):**
   * **Continuous Data Architecture (Zero Card Plague):** Mirrors the frameless section discipline established in `SCR-INV-005`. Primary content sections render directly on the workspace surface (`--dt-color-surface-card`) without redundant outer card wrappers. Initial sections within a tab have no top border, while subsequent stacked sections are separated by a subtle top divider (`--dt-color-border-subtle`).
   * **Scope & Timing Grid (`CMP-03`):** Enforces an asymmetric two-column desktop/landscape grid expanding across the full vertical workspace height: The primary left column provides expansive breadth for frameless procedural task checklist items, while the secondary right column (`--dt-color-border-subtle`) hosts the enclosed timing cockpit master card. In portrait mode, the vertical divider transitions into an edge-to-edge full-width horizontal divider (`--dt-color-border-subtle` with zero side gaps).
   * **Spares & Rotable Asset Grid (`CMP-04`):** Mirrors the exact asymmetric two-column full-height stretch rhythm: The primary left column hosts allocated warehouse parts (Allocated Materials & Spares) with circular tactile quantity steppers, while the secondary right column (`--dt-color-border-subtle`) hosts the frameless equipment rotation pane with natural flow spacing and a dedicated rotable swap trigger bound to `--dt-color-surface-btn-secondary`.
   * Encapsulates real-time diagnostic field timing and formal CMMS accounting entry into a single structured master card with edge-to-edge flush headers:
     * **Telemetry Widgets Section (`ScopeWidgetsSection`):** High-contrast inset instrument bezel with darker recessed background (`--dt-color-surface-base`) extending flush to the master container borders, hosting dual circular SVG gauges for field stopwatch and labor progress, center bridge percentage pill, and Work Order telemetry reference without redundant analytical rows.
     * **Field Intervention Stopwatch Section (`FieldStopwatchSection`):** Frameless section directly on the controls body, hosting field intervention timer, tactile pill toggle (`[Pause]` / `[Resume]` with permanent capsule curvature `--dt-radius-full` and monochromatic high-contrast active fill), discrete bump pill (`[+15 min]`), tactile circular reset button, and a bottom divider line separating it from labor accounting.
     * **Actual Labor Hours Section (`ActualLaborHoursSection`):** Hosts the official CMMS accounting field featuring circular steppers (`−` / `+`), recessed numeric display sharing the identical surface treatment as the steppers, monochromatic left-aligned quick preset pills with content-fit widths (`2.0h`, `2.5h`, `3.0h`, `3.5h (Planned)`), horizontal divider line, and full-width CTA pill (`[Log Time to Record]`) bound to `--dt-color-state-info`.
3. **Sticky Bottom Finalization Bar (`CMP-09`):**
   * Pinned to the bottom viewport boundary with height `--dt-layout-footer-height` and elevation `--dt-z-header-sticky`, separated via `--dt-color-border-subtle`.
   * Workspace container uses standard internal padding (`--dt-space-5`) without artificial bottom scroll padding, allowing checklist items to scroll naturally with `--dt-layout-footer-clearance`.
   * Guided workflow: Progressive navigation (`← Previous` and `Next →`) guides the technician sequentially; primary action `[Finalize Work Order]` unlocks strictly on Step 4 (Evidence) once quality gates are satisfied.
4. **Flush Tab Navigation Physics (`CMP-02`):**
   * Edge-to-edge flush tab bar with zero inter-tab gap or rounded corners, sitting directly adjacent to the LOTO handover strip and workspace bounds.
   * Supports horizontal touch swipe gestures across touch viewports. Badges are strictly reserved for quantifiable counters (`[5/7]`, `[3 items]`, `[0/7]`, `[0/1]`), purging decorative pseudo-badges per ANSI/ISA-101.01 §6.2.

### 5.3. Domain Workflows, Taxonomy Enums, and Cryptographic Mutation

1. **ISO 14224 Multi-Tier Taxonomy Matrix & Sequential Cascade (`CMP-05`):**
   * Failure classification is strictly constrained by ISO 14224 reliability standards and domain model contracts ([DT-ERD-DOC-001 §3.2.2](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#322-failure_records)), enforcing a strict causal top-down cascade ($1 \to 7$) where each dropdown remains locked (`disabled`) until its immediate predecessor is populated, and mutating an upstream tier resets all downstream tiers:
     * **Tier 1: Maintainable Item:** Filtered dynamically by the target equipment class (e.g., for Centrifugal Pump `P-0101A` per API 610: *Mechanical Seal*, *Impeller*, *Bearings*, *Shaft*, *Casing*, *Coupling*).
     * **Tier 2: Failure Mode:** Constrained by Maintainable Item (e.g., for Mechanical Seal: *External Leakage (EL)*, *Vibration Excursion (VE)*, *Overheating (OH)*).
     * **Tier 3: Failure Mechanism:** Observable physical degradation (e.g., *Mechanical Wear*, *Abrasive Erosion*, *Thermal Fatigue*, *Elastomer Degradation*).
     * **Tier 4: Failure Cause:** Root engineering origin (e.g., *Lubrication Deficiency*, *Shaft Misalignment*, *Cavitation Erosion*, *Operational Off-Design*).
     * **Tier 5: Detection Method:** Controlled vocabulary mapped to enum `DetectionMethod` (§7.2.3).
     * **Tier 6: Operational Condition:** Controlled vocabulary mapped to enum `OperationalCondition` (§7.2.3).
     * **Tier 7: Operational Impact:** Controlled vocabulary mapped to enum `OperationalImpact` (§7.2.3).
     * **Quantitative Metric: Downtime Hours:** Numeric field recording hours of lost operational availability ($\ge 0.0\text{h}$).
     * **Technical Observations:** Full-width field capturing empirical observations and diagnostic notes directly tied to the failure record.

2. **The ISO 14224 Hard Lock Formula & Sequential Stepper (`CMP-06`, `FR-012`):**
   * Visualized via a 7-node sequential horizontal stepper sharing the exact monochromatic progression grammar of `SCR-INV-005` (circular step indicator nodes joined by horizontal connector bars, without redundant lock pills or helper text).
   * The primary action button `CMP-09` `[Finalize Work Order]` is governed by the asymmetric Boolean lock:
     $$\text{CanFinalize} = \mathcal{T}_{\text{complete}} \land \mathcal{E}_{\text{valid}} \land \mathcal{W}_{\text{valid}}$$
     where:
     $$\mathcal{T}_{\text{complete}} = (\text{Item} \ne \varnothing) \land (\text{Mode} \ne \varnothing) \land (\text{Mech} \ne \varnothing) \land (\text{Cause} \ne \varnothing) \land (\text{Method} \ne \varnothing) \land (\text{Condition} \ne \varnothing) \land (\text{Impact} \ne \varnothing) \land (\text{Downtime} \ge 0.0)$$
     $$\mathcal{E}_{\text{valid}} = (\text{MediaAttachmentCount} \ge 1) \land (\forall e \in \text{Attachments}, e.\text{SHA256HashVerified} == \text{true})$$
     $$\mathcal{W}_{\text{valid}} = (\text{ActualLaborHours} > 0.0) \land (\text{AllChecklistItemsChecked} == \text{true})$$
   * Any false term renders the button `disabled` with dynamic visual indicator (`*`) on omitted fields (`AF-001`).

3. **Multi-Evidence Photographic Capture & Cryptographic Hashing Pipeline (`CMP-07`, `TR-003`):**
   * Supports an array of $0..N$ attachments (`List<MediaAttachmentDto>` per [DT-ERD-DOC-001 §3.2.4](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#324-media_attachments)):
     1. Displays a reserved dashed dropzone container as empty-state placeholder with direct camera trigger.
     2. Capturing photo via hardware camera or file picker downsamples image to maximum $1920\times 1080$ JPEG format (quality 0.85) to optimize offline storage footprint.
     3. Computes cryptographic checksum asynchronously in a Web Worker via ICryptoInterop (SHA-256).
     4. Renders individual gallery cards displaying image thumbnail (--dt-layout-thumbnail-size), metadata, delete trigger, and verified monospace hash stamp (`SHA-256: [hash]`).
     5. Packages validated media items into `MediaAttachmentDto` records linking image URI, file format, timestamp, and hash string to the failure record context.
     6. If file reading throws an I/O error or hash evaluation fails, the UI enters state `Evidence Corrupt` (`AF-003`), halts finalization, and forces recapture.

4. **Atomic Technical Closure Command Dispatch (`CMP-09`, `TR-001`):**
   * Upon pressing `[Finalize Work Order]`, the application dispatches an atomic technical closure command (`SubmitTechnicalClosureCommand`) against the backend API endpoint `POST /api/v1/work-orders/{id}/technical-closure`.
   * **Client Command Contract:**
     * **Request Headers:** Includes `X-Idempotency-Key: {uuidv7}` ([ADR-007](../../../architecture/adr/ADR-007.md)) to guarantee exactly-once processing during network reconnection retries.
     * **Command Payload:** Serializes `FailureRecordInputDto` (7-tier ISO 14224 classifications, downtime, technician notes), `ActualLaborHours`, and `List<MediaAttachmentDto>` (evidence attachments with computed SHA-256 signatures).
     * **Backend Persistence Invariant:** Backend orchestrates the atomic transaction (failure record insertion, Work Order status update to `COMPLETE`, history logging, and cryptographic audit chaining) governed by [DT-ARQ-DB-DOC-001 §2](../../../architecture/DT-ARQ-DB-DOC-001.md#2-physical-integrity-invariants-and-constraints) and [DT-ERD-DOC-001 §3.2.6](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#326-work_orders).
     * **Success Handling (HTTP 200 OK):** Transitions UI state to `COMPLETE`, displays non-disruptive completion modal, and navigates downstream to the RIME Backlog Dashboard ([SCR-MTTO-026](./SCR-MTTO-026.md)).
     * **Failure / Disconnected Handling:** On network timeout or HTTP 5xx error, transitions to the Zero-Shift Offline Outbox Protocol (§5.3.5, [TR-007](../../../requirements/common/TR-007.md)).

5. **Zero-Shift Offline Telemetry and Outbox Protocol (`AF-002`, `TR-002`, `TR-007`, `ADR-007`):**
   * If network connection is lost or heartbeat timeout occurs:
     1. Telemetry indicator in header transitions from `ONLINE · [HH:MM]` to `OFFLINE · [HH:MM]` with disconnected network glyph.
     2. Amber badge `[1 PENDING SYNC]` illuminates directly in the header context.
     3. **Fail-Safe Zero-Energy Masking:** The safety badge `[🔒 ZERO ENERGY CONFIRMED]` is automatically suppressed from the UI during offline operation. While mechanical padlocks remain locked, real-time electrical zero-voltage and zero-current attestation cannot be confirmed via disconnected DCS telemetry; displaying a stale positive safety confirmation during telemetry blackout violates process safety integrity principles.
     4. Zero layout shift is incurred (CLS = 0), preventing disorienting viewport jumps or content displacement on tablet screens.
     5. The full atomic command payload is serialized into JSON and written to the encrypted local outbox protected by database encryption at rest ([TR-002](../../../requirements/common/TR-002.md)).
     6. Assigns a unique `IdempotencyKey` (UUIDv7) per `ADR-007`.
     7. Marks the local UI view as `COMPLETE (Pending Sync)`.
     8. Background synchronization worker monitors connectivity; upon restoration, drains the outbox queue via idempotent `POST /api/v1/work-orders/{id}/technical-closure` with `X-Idempotency-Key` header.

6. **Rotable Asset Swap Branching (`CMP-04`):**
   * If the physical repair requires unmounting the pump unit, tapping `[Rotate Dismounted Equipment]` preserves the in-flight form draft in local memory and deploys the in-situ overlay modal [SCR-INV-025](../inv/SCR-INV-025.md). Upon completing the asset swap, `SCR-INV-025` returns the new mounted equipment serial number (`P-0101B`) and stamps the replacement reference into technical observations.

---

## 6. Industrial and Safety Considerations

* **High-Performance HMI (ANSI/ISA-101 / [TR-011](../../../requirements/common/TR-011.md)):**
   * Grayscale visual discipline: $90\%$ of the screen utilizes neutral dark slate tones (`--dt-color-surface-base`, `--dt-color-surface-card`, `--dt-color-border-subtle`).
   * Saturated amber (`--dt-color-alarm-warning`) is reserved exclusively for the offline sync indicator badge (`[1 PENDING SYNC]`) and missing required fields.
   * Saturated red (`--dt-color-alarm-critical`) is reserved strictly for corrupt file integrity errors or process safety emergency breaches. Industrial green is strictly prohibited; Muted Teal (`--dt-color-state-success`) is reserved exclusively for verified completion gates.
* **Diagnostic (Priority 4) vs. Process Alarm Segregation:**
   * Network disconnection chip (`CMP-08`) in the header is styled strictly as a Priority 4 Diagnostic indicator with muted borders and informational icons. It is strictly prohibited from masquerading as a high-priority process emergency.
* **De-Isolation / De-LOTO Safety Handover Protocol:**
   * Technical closure (`COMPLETE`) of the Work Order does **NOT** equate to plant re-energization.
   * Flush banner `CMP-10` explicitly enforces the safety invariant:
    > *"CAUTION: Hazardous energy isolations established in SCR-VIS-011 remain locked. Physical padlock removal and de-isolation must be executed via formal Operations Handover prior to commissioning."*

---

## 7. Frontend Component Contract (Blazor / Razor)

### 7.1. Component Hierarchy & File Mapping

```text
Pages/
└── MobileWorkOrderClosingPage.razor                 # Root View (SCR-MTTO-002)
    ├── ExecutionHeader.razor                        # CMP-01: Header with fail-safe LOTO & telemetry
    ├── OperationalTabsBar.razor                     # CMP-02: Flush 4-channel tab selector
    ├── ScopeExecutionTab.razor                      # CMP-03: Scope & Decoupled timing container
    │   ├── TaskChecklistCard.razor                  # Step-by-step checklist with tactile checks (--dt-control-size-checkbox)
    │   ├── FieldStopwatchCard.razor                 # Field intervention stopwatch & transfer hero action
    │   └── ActualLaborHoursCard.razor               # Actual labor input with tactile steppers (--dt-touch-target-mobile) & presets
    ├── SparesAllocationTab.razor                    # CMP-04: Spares card list & Asset Swap trigger
    ├── IsoTaxonomyDiagnosisTab.razor                # CMP-05: 7-tier ISO 14224 matrix & observations
    │   └── IsoComplianceStepper.razor               # CMP-06: 7-node sequential quality gate stepper (INV-005 style)
    ├── MultimediaEvidenceTab.razor                  # CMP-07: Multi-evidence array uploader & SHA-256 verifier
    │   ├── EvidenceDropzone.razor                   # Reserved dashed empty-state container
    │   └── EvidenceCard.razor                       # Reactive photo card with thumbnail & hash stamp
    ├── OfflineTelemetryIndicator.razor              # CMP-08: Zero-shift header telemetry & outbox badge
    ├── TechnicalFinalizeBar.razor                   # CMP-09: Sticky bottom bar with nav arrows (--dt-control-height-nav-step)
    └── DeIsolationHandoverStrip.razor               # CMP-10: Flush LOTO safety acknowledgment strip
```

### 7.2. Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)

#### 7.2.1. `MobileWorkOrderClosingPage.razor` (Root View)

```csharp
[Parameter]
public required Guid WorkOrderId { get; set; }

[Parameter, SupplyParameterFromQuery]
public string? ReturnUrl { get; set; }
```

#### 7.2.2. Subcomponent Parameters

```csharp
// CMP-01: ExecutionHeader.razor
[Parameter, EditorRequired]
public required WorkOrderClosingContextDto Context { get; set; }

[Parameter]
public bool IsOffline { get; set; }

[Parameter]
public int PendingSyncCount { get; set; }

// CMP-02: OperationalTabsBar.razor
[Parameter, EditorRequired]
public required int ActiveTabIndex { get; set; }

[Parameter, EditorRequired]
public EventCallback<int> ActiveTabIndexChanged { get; set; }

[Parameter]
public int CompletedScopeItems { get; set; }

[Parameter]
public int TotalScopeItems { get; set; }

[Parameter]
public int CompletedIsoTiers { get; set; }

[Parameter]
public int AttachmentCount { get; set; }

// CMP-03: ScopeExecutionTab.razor
[Parameter, EditorRequired]
public required IReadOnlyList<ScopeTaskItemDto> Tasks { get; set; }

[Parameter, EditorRequired]
public EventCallback<Guid> OnTaskToggled { get; set; }

[Parameter, EditorRequired]
public decimal ActualLaborHours { get; set; }

[Parameter, EditorRequired]
public EventCallback<decimal> ActualLaborHoursChanged { get; set; }

[Parameter]
public decimal PlannedLaborHours { get; set; }

// CMP-04: SparesAllocationTab.razor
[Parameter, EditorRequired]
public required IReadOnlyList<SparePartAllocationDto> SpareParts { get; set; }

[Parameter, EditorRequired]
public EventCallback<SparePartAllocationDto> OnQuantityChanged { get; set; }

[Parameter]
public EventCallback OnRotateEquipmentRequested { get; set; }

// CMP-05: IsoTaxonomyDiagnosisTab.razor
[Parameter, EditorRequired]
public required FailureRecordInputDto Model { get; set; }

[Parameter, EditorRequired]
public EventCallback<FailureRecordInputDto> ModelChanged { get; set; }

[Parameter, EditorRequired]
public required Guid EquipmentClassId { get; set; }

[Parameter]
public bool IsReadOnly { get; set; }

// CMP-06: IsoComplianceStepper.razor
[Parameter, EditorRequired]
public int CompletedTierCount { get; set; }

[Parameter]
public int TotalTiers { get; set; } = 7;

[Parameter]
public bool IsLocked { get; set; }

// CMP-07: MultimediaEvidenceTab.razor
[Parameter, EditorRequired]
public required IReadOnlyList<MediaAttachmentDto> Attachments { get; set; }

[Parameter, EditorRequired]
public EventCallback<MediaAttachmentDto> OnAttachmentAdded { get; set; }

[Parameter, EditorRequired]
public EventCallback<Guid> OnAttachmentRemoved { get; set; }

[Parameter]
public bool IsCapturing { get; set; }

// CMP-08: OfflineTelemetryIndicator.razor
[Parameter]
public bool IsOffline { get; set; }

[Parameter]
public int PendingSyncCount { get; set; }

[Parameter]
public DateTimeOffset? LastSyncTime { get; set; }

// CMP-09: TechnicalFinalizeBar.razor
[Parameter, EditorRequired]
public int CurrentStep { get; set; }

[Parameter, EditorRequired]
public int TotalSteps { get; set; } = 4;

[Parameter]
public bool CanFinalize { get; set; }

[Parameter]
public bool IsSubmitting { get; set; }

[Parameter]
public EventCallback OnPreviousStep { get; set; }

[Parameter]
public EventCallback OnNextStep { get; set; }

[Parameter]
public EventCallback OnFinalizeTriggered { get; set; }

// CMP-10: DeIsolationHandoverStrip.razor
[Parameter]
public bool IsLotoNeutralized { get; set; }

[Parameter]
public string? LotoTagReference { get; set; }
```

#### 7.2.3. Data Transfer Objects (DTOs) and Enums

```csharp
public enum DetectionMethod
{
    PERIODIC_MAINTENANCE,
    FUNCTIONAL_TESTING,
    INSPECTION,
    PERIODIC_CBM,
    PRESSURE_TESTING,
    CONTINUOUS_CBM,
    PRODUCTION_INTERFERENCE,
    CASUAL_OBSERVATION,
    CORRECTIVE_MAINTENANCE,
    ON_DEMAND,
    OTHER
}

public enum OperationalCondition
{
    RUNNING,
    START_UP,
    RUN_DOWN,
    HOT_STANDBY,
    COLD_STANDBY,
    IDLE,
    TESTING
}

public enum OperationalImpact
{
    EXTENSIVE_STOP,
    STOP_ABOVE_ACCEPTABLE,
    STOP_BELOW_ACCEPTABLE,
    STOP_MINOR
}

public record WorkOrderClosingContextDto
{
    public required Guid WorkOrderId { get; init; }
    public required string WorkOrderNumber { get; init; } // e.g. "WO-2026-0842"
    public required Guid TechnicianId { get; init; }
    public required Guid EquipmentUnitId { get; init; }
    public required string EquipmentTag { get; init; }     // e.g. "P-0101A"
    public required string FunctionalLocation { get; init; } // e.g. "TFA-CSS-P-0101A"
    public required string CurrentStatus { get; init; }    // "IN_PROGRESS"
    public required bool IsLotoNeutralized { get; init; }   // true
    public required decimal EstimatedHours { get; init; }
    public decimal? ActualLaborHours { get; init; }
}

public record FailureRecordInputDto
{
    public Guid? MaintainableItemId { get; set; }
    public string? FailureMode { get; set; }
    public string? FailureMechanism { get; set; }
    public string? FailureCause { get; set; }
    public DetectionMethod? DetectionMethod { get; set; }
    public OperationalCondition? OperationalCondition { get; set; }
    public OperationalImpact? OperationalImpact { get; set; }
    public decimal DowntimeHours { get; set; }
    public string? TechnicianNotes { get; set; }
}

public record ScopeTaskItemDto
{
    public required Guid TaskId { get; init; }
    public required string Description { get; init; }
    public required bool IsCompleted { get; init; }
}

public record SparePartAllocationDto
{
    public required Guid PartId { get; init; }
    public required string PartNumber { get; init; }
    public required string Description { get; init; }
    public required decimal QuantityReserved { get; init; }
    public decimal QuantityConsumed { get; init; }
    public required string WarehouseLocation { get; init; }
}

public record MediaAttachmentDto
{
    public required Guid Id { get; init; }
    public required string FileUrl { get; init; }
    public required string FileType { get; init; } // "JPG", "PNG", "PDF"
    public required string IntegrityHashSha256 { get; init; }
    public bool CapturedOffline { get; init; }
    public required DateTimeOffset UploadedAt { get; init; }
}

public record SubmitTechnicalClosureCommand(
    Guid WorkOrderId,
    Guid TechnicianId,
    decimal ActualLaborHours,
    FailureRecordInputDto FailureRecord,
    IReadOnlyList<SparePartAllocationDto> ConsumedSpares,
    IReadOnlyList<MediaAttachmentDto> EvidenceAttachments,
    string PreviousHash
);
```

### 7.3. Client-Side DOM & Interop Bridge

1. **Hardware Camera & Image Compression Interop (`ICameraInterop`):**
   * Encapsulates device media capture capabilities with fallback to native OS camera file picker.
   * Performs client-side image downsampling and JPEG compression asynchronously off the main UI thread to guarantee media payloads $< 1.5\text{MB}$ prior to local persistence.
2. **Web Crypto SHA-256 Hashing Bridge (`ICryptoInterop`):**
   * Dispatches cryptographic SHA-256 checksum computation asynchronously to a dedicated Web Worker to prevent UI thread stuttering or frame drops on industrial tablets during binary processing.
3. **Encrypted Offline Storage Interop (`IOfflineStorage`):**
   * Interfaces with client-side encrypted relational storage (AES-256 via SQLCipher) for immediate transactional outbox queuing during disconnected field operations ([TR-002](../../../requirements/common/TR-002.md), [TR-007](../../../requirements/common/TR-007.md)).

---

## 8. Layout and Responsive Adaptability

| Viewport / Breakpoint | Layout Organization | Ergonomic Rules |
| :--- | :--- | :--- |
| **Desktop Workstation**<br>($\ge 1920\text{px}$, `--dt-breakpoint-xl`) | Flush 4-tab execution workspace (`CMP-02`) with multi-column internal tab grids (Tab 1 & Tab 2 pair a frameless primary section on the left with a full-height vertical divider `--dt-color-border-subtle` and the secondary operational column on the right; Tab 3 renders the 7-node horizontal stepper above the 2-column ISO 14224 matrix separated by a top divider). Sticky footer `CMP-09` (`--dt-layout-footer-height`) spans bottom width. | Mouse click focus; keyboard numeric navigation; dense multi-tier custom popover dropdowns; full-resolution image preview modal. |
| **Industrial Tablet Landscape**<br>($1280\text{px} - 1919\text{px}$, `--dt-breakpoint-lg`) | Flush 4-tab execution workspace (`CMP-02`) with asymmetric two-column internal tab grids stretching across the full workspace height. The primary checklist and parts tables flow naturally with standard clearance (`--dt-layout-footer-clearance`), scrolling vertically as items exceed viewport height without artificial padding. Sticky footer `CMP-09` pinned at bottom (`--dt-layout-footer-height`). | Gloved touch targets governed by `--dt-touch-target-mobile` with `--dt-space-2` separation; camera trigger anchored for dual-thumb reachability. |
| **Industrial Tablet Portrait**<br>($768\text{px} - 1279\text{px}$, `--dt-breakpoint-md`) | Single-column vertical stack inside each swipeable tab view (`CMP-02`). In Tabs 1 & 2, the vertical column divider transitions into an edge-to-edge full-width horizontal divider (`--dt-color-border-subtle`). In Tab 3, the ISO 14224 matrix collapses to a single column, and the 7-node stepper (`CMP-06`) stacks concise tier labels directly underneath the circular indicators with centered horizontal connector links so all 7 nodes fit without horizontal scrolling. Sticky footer `CMP-09` pinned at bottom. | Gloved operation ergonomics (`--dt-touch-target-mobile`, `--dt-space-2` gap); single-hand thumb navigation; zero horizontal scrollbars inside the ISO quality gate stepper (`CMP-06`). |

---

## 9. Traceability and Requirements Matrix

| Requirement | Addressed in Component | Verification & Implementation Mechanism |
| :--- | :--- | :--- |
| [FR-010](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-03`, `CMP-09` | Registration of actual labor duration and Wrench Time tracking from mobile interface. |
| [FR-011](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-05` | Mandatory 7-tier classification strictly using ISO 14224 maintainable item catalog and failure record entities. |
| [FR-012](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-06`, `CMP-09` | **ISO 14224 Hard Lock:** Hard-disables finalization button until all mandatory taxonomy fields and downtime are complete. |
| [FR-013](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-07` | Multimedia photographic attachment capture, preview thumbnail generation, and persistent linkage to media attachment records. |
| [FR-014](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-09` | Atomic transition of Work Order state to `COMPLETE` and dispatch of domain event notification to Reliability Engineer. |
| [NFR-015](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr) | `CMP-08`, `CMP-09` | Offline-First persistence using encrypted SQLCipher local storage with crash-resilient transactional journaling. |
| [NFR-016](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr) | `CMP-02`, `CMP-05` | Mobile response latency $< 2\text{s}$ achieved via pre-hydrated local taxonomy caches and Web Worker SHA-256 hashing. |
| [NFR-017](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr) | `CMP-01` to `CMP-10` | Cross-platform mobile suitability on Android industrial tablets and iOS/Windows devices via responsive CSS tokens. |
| [TR-001](../../../requirements/common/TR-001.md) | `CMP-09` | Append-only immutable audit trail logging with SHA-256 hash chaining upon Work Order finalization. |
| [TR-002](../../../requirements/common/TR-002.md) | `CMP-08` | Local database encryption at rest using AES-256 (SQLCipher) for all cached work order and failure records. |
| [TR-003](../../../requirements/common/TR-003.md) | `CMP-07` | Client-side cryptographic SHA-256 hash evaluation of all uploaded media files stored in metadata for tamper detection. |
| [TR-006](../../../requirements/common/TR-006.md) | `CMP-01` | Device authorization and authenticated technician session validation (`TECH-4921`). |
| [TR-007](../../../requirements/common/TR-007.md) | `CMP-08` | Transactional Offline Sync Outbox: Queues completed technical closures during disconnected operation with idempotent sync. |
| [TR-010](../../../requirements/common/TR-010.md) | `CMP-01`, `CMP-08` | Real-time synchronization via WebSockets/SignalR for telemetry connection health and outbox reconciliation. |
| **ISO 9241-110** | `CMP-02`, `CMP-07`, `CMP-09` | Gloved touch targets governed by `--dt-touch-target-mobile` with `--dt-space-2` separation complying with industrial ergonomics. |
| [TR-011](../../../requirements/common/TR-011.md) | `CMP-01` to `CMP-10` | ANSI/ISA-101 HPHMI: 90% neutral grayscale palette; saturated amber reserved for offline banner and missing fields; saturated red reserved for file corruption. |
| [ADR-006](../../../architecture/adr/ADR-006.md) | `CMP-01`, `CMP-08` | Integration with Cryptographic Offline Lease protocol for disconnected field operations. |
| [ADR-007](../../../architecture/adr/ADR-007.md) | `CMP-08`, `CMP-09` | Idempotency token generation (UUIDv7) attached to technical closure payloads to prevent duplicate commits. |

