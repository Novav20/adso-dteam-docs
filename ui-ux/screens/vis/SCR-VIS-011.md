---
id: SCR-VIS-011
title: LOTO Isolation Boundary Matrix and Zero Energy Verification (LOTO-TryOut)
module: VIS
isa101_level: L4 (Diagnostic, Detail & Task Execution) | Spatial L2/L3 Context
platform: Shared Component
target_device: Industrial Tablet (Primary) | Desktop Workstation
roles:
  - Maintenance Technician
  - Maintenance Supervisor
  - HSEQ Inspector
user_stories:
  - "[[VIS-011]]"
use_cases:
  - "[[UC-VIS-011]]"
version: 2.2
date: 2026-11-24
status: Stable
---

# SCR-VIS-011: LOTO Isolation Boundary Matrix and Zero Energy Verification (LOTO-TryOut)

## 1. Purpose and Operational Context

* **View Objective:** Spatial and procedural verification of hazardous energy isolation boundaries (LOTO) over the plant 2D plot plan (ANSI/ISA-101 Level 4 Task Execution with Level 2/3 spatial context). Corroborates physical field lockouts and absence-of-energy tests with real-time IoT telemetry, enforcing active software interlocking to guarantee a proven Zero Energy State prior to Equipment Unit intervention (OSHA 1910.147, ISO 45001).
* **Primary Target Persona:** Maintenance Technician executing field cutoffs, registering physical padlocks, performing Try-Out tests, and requesting work authorization.
* **Secondary Personas:**
  * **HSEQ Inspector:** Audits isolation boundaries, verifies cryptographic compliance trails, and monitors SIMOPS interactions.
  * **Maintenance Supervisor:** Oversees active isolations and provides emergency supervisory overrides.
* **Operational Context:** Deployed on rugged industrial tablets in the field and central maintenance workstations.
* **Mode of Operation:** Hybrid Safety Interlock & Supervisory Inspection mode. Real-time telemetry monitoring and field safety interlock authorization. Direct DCS/SCADA process control manipulation is strictly excluded; field mechanics rely on physical manual cutoff points, padlocks, and local Try-Out tests.
* **Single-Canvas Workspace Invariant:** Operates strictly as a contextual operational mode within the unified application shell, not as an independent web page with browser history. Activated contextually when selecting *"LOTO Route"* from [SCR-VIS-033](./SCR-VIS-033.md) or a Work Order panel, projecting the LOTO vector layer over the shared plot plan and opening the isolation drawer in-place.

---

## 2. Visual Artifact

![SCR-VIS-011 LOTO Isolation Matrix Screenshot](assets/SCR-VIS-011-screenshot.png)

> *Figure 2.1 — Level 4 LOTO Isolation Boundary Matrix (Dark Theme): Illustrates the 2D plot plan with LOTO vector overlay (`CMP-01`), isolation cutoff nodes (`CMP-04`), and lateral contextual isolation drawer (`CMP-05`).*

---

## 3. Functional Component Inventory

> The base grid, typography, neutral palettes, and minimal tactile contact areas are inherited from [DT-UI-DS-DOC-001](../../DT-UI-DS-DOC-001.md) and [DT-UI-SVG-DOC-001](../../DT-UI-SVG-DOC-001.md). This inventory defines the canonical components present on the screen, their design tokens, and their architectural scope. Interaction rules and geometric algorithms are specified in Section 5; responsive container adaptations are governed by Section 8.

1. **`CMP-01`: Canvas Viewport 2D & LOTO Layer**
   - **Visual Role:** Interactive 2D vector plot plan canvas rendering dynamic LOTO energy routes (`H/V + 45 deg` oblique electrical MCC paths and edge-anchored mechanical boundary lines) over the target Equipment Unit (`data-equip-id`), applying SVG mask-based Focal Island De-emphasis to attenuate non-isolated plant sectors.
   - **Design Tokens:**
     - Surface: `--dt-color-bg-canvas`
     - Elevation: `--dt-z-canvas` (Base Canvas) / `--dt-z-layer-loto` (LOTO Route Overlay)
     - Energized Route: `--dt-color-alarm-critical`
     - Isolated Route: `--dt-color-loto-isolated-path`
     - Spatial Materials: `--dt-color-canvas-bund-floor`, `--dt-color-canvas-equip-shell`, `--dt-color-canvas-pipe-proc`
   - **Architectural Scope:** Strictly flat $Z = 0$ base vector layer ([DT-UI-DS-DOC-001 §5.1](../../DT-UI-DS-DOC-001.md#51-hphmi-shadow-discipline-canvas-vs-hud-chrome-separation)) with superimposed LOTO vector paths and pure SVG mask-clipped de-emphasis. Spatial kinematics, full-circuit framing, site-boundary clamping, and unified pan ergonomics specified in §5.1 and §5.2.

2. **`CMP-02`: Viewport Toolbar**
   - **Visual Role:** Frosted floating capsule toolbar integrating inline equipment tag search (`Space` / `Ctrl + K`), fixed-width hierarchical level indicator (`L3: LOTO Matrix`), view reset, zoom controls (`+` / `-`), and LOTO focal de-emphasis layer toggle (`#icon-layers`).
   - **Design Tokens:**
     - Surface: `--dt-color-float-bg`
     - Border: `--dt-color-float-border`
     - Elevation: `--dt-shadow-glass`
     - Radius: `--dt-radius-full`
     - Stacking: `--dt-z-overlay-card`
     - Level Badge Width: `--dt-layout-toolbar-badge-width`
   - **Architectural Scope:** Floating borderless HUD chrome per [DT-UI-DS-DOC-001 §5.2](../../DT-UI-DS-DOC-001.md#52-elevation-shadows), dynamically centering over the unoccluded canvas workspace when `CMP-05` is deployed. Detailed in §5.2 and §8.

3. **`CMP-03`: User Profile Button**
   - **Visual Role:** Circular floating operator session button anchored at the top-left viewport margin displaying active technician initials and a static session presence dot.
   - **Design Tokens:**
     - Surface: `--dt-color-float-bg`
     - Border: `--dt-color-float-border`
     - Elevation: `--dt-shadow-glass`
     - Radius: `--dt-radius-full`
     - Stacking: `--dt-z-overlay-card`
     - Touch Target: `--dt-touch-target-mobile`
     - Session Dot: `--dt-color-state-success`
   - **Architectural Scope:** Anchored at top-left viewport margin per [DT-UI-DS-DOC-001 §5.2](../../DT-UI-DS-DOC-001.md#52-elevation-shadows). Triggers operator session and theme menu.

4. **`CMP-04`: Isolation Cutoff Nodes & Directional Edge Beacons**
   - **Visual Role:** Addressable translucent circular vector discs (`--dt-color-loto-disc` with double slate rim `--dt-color-marker-border`, `--dt-shadow-marker` silhouette elevation) positioned over physical energy cutoff points (`#icon-loto-locked`, `#icon-loto-energized`), paired with off-screen frosted directional edge beacons during Level 3 zoom inspection.
   - **Design Tokens:**
     - Disc Surface: `--dt-color-loto-disc`
     - Rim & Focus: `--dt-color-marker-border`, `--dt-color-border-focus`
     - Energized Halo: `--dt-color-alarm-critical`
     - Isolated State: `--dt-color-state-success`, `--dt-color-loto-isolated-path`
     - Beacon Surface: `--dt-color-float-bg-strong`
     - Marker Elevation: `--dt-shadow-marker`
     - Stacking: `--dt-z-layer-markers`
     - Touch Target: `--dt-touch-target-mobile`
   - **Architectural Scope:** Bound via `data-cutoff-id` and `data-equip-id` ([DT-UI-SVG-DOC-001 §7](../../DT-UI-SVG-DOC-001.md#7-lockout-tagout-loto-isolation-point-contract)) with 4-channel redundant spatial symbology ([DT-UI-DS-DOC-001 §6.4](../../DT-UI-DS-DOC-001.md#64-iconography-and-redundant-symbology-standards)). Screen-space clamping, obstacle collision avoidance, and edge beacon clustering in §5.2; bidirectional checklist synchronization in §5.3.

5. **`CMP-05`: LOTO Isolation Drawer**
   - **Visual Role:** Adaptable contextual safety panel (docked lateral drawer in landscape/desktop; sliding bottom sheet in portrait) hosting the minimize (`>`) and close (`×`) controls, Equipment Unit tag badge, dynamic safety status pill, Work Order badge, SOP link, and subcomponents `CMP-06` through `CMP-11`.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-drawer` (container) / `--dt-color-surface-card` (elevated slots)
     - Border: `--dt-color-border-panel`
     - Elevation: `--dt-shadow-panel`
     - Stacking: `--dt-z-drawer-sidebar`
     - Bottom Sheet Radius: `--dt-radius-2xl`
     - Status Pill: `--dt-color-alarm-critical` (Energized) / `--dt-color-state-success` (Zero Energy Verified)
   - **Architectural Scope:** Overlaid container with permanent scrollbar gutter reservation. Lifecycle, minimize peek tab (`--dt-layout-bottom-sheet-peek-height`), snap physics, and layout rules in §5.2 and §8.

6. **`CMP-06`: Sequential Isolation Checklist**
   - **Visual Role:** Ordered step-by-step physical lockout list enforcing sequential Padlock Tag ID input, optical barcode/NFC scan trigger, and step confirmation (`[Lock]`).
   - **Design Tokens:**
     - Surface: `--dt-color-surface-base` / `--dt-color-surface-card` (Active Step)
     - Border: `--dt-color-border-subtle` / `--dt-color-border-focus` (Active Step)
     - Confirmed State: `--dt-color-state-success`
     - Primary Step Action: `--dt-color-state-info`
     - Radius: `--dt-radius-lg`
   - **Architectural Scope:** Enforces thermodynamic isolation sequencing (`FR-228`). Validation rules in §5.3.

7. **`CMP-07`: Telemetry Verification Matrix**
   - **Visual Role:** Real-time multi-sensor Moving Analog Indicators (MAI) contextualizing continuous boundary variables ($V, I, P, Q$) against calibrated scale bars and zero-energy trip limits ([DT-UI-DS-DOC-001 §6.1](../../DT-UI-DS-DOC-001.md#61-moving-analog-indicator-mai-specification)).
   - **Design Tokens:**
     - Track & Zone: `--dt-color-mai-track`, `--dt-color-mai-normal-zone`
     - Pointer & Interlock: `--dt-color-mai-pointer`, `--dt-color-mai-interlock`
     - Breach Alert: `--dt-color-alarm-critical`
     - Stale Zone: `--dt-color-mai-stale-zone`
   - **Architectural Scope:** Evaluates negative interlock sensor thresholds in $< 1\text{s}$ (`NFR-233`). Mathematical mapping and threshold rules in §5.3.

8. **`CMP-08`: Physical Try-Out Verification Card**
   - **Visual Role:** Mandatory absence-of-energy attestation card (OSHA 1910.147 §(d)(6)) hosting the physical verification method selector, observed reading input, and technician cryptographic sign-off trigger.
   - **Design Tokens:**
     - Surface: `--dt-color-surface-base`
     - Border: `--dt-color-border-subtle` / `--dt-color-border-focus` (Actionable)
     - Radius: `--dt-radius-lg`
   - **Architectural Scope:** Captures `TryOutAttestationDto` and instantaneous `TelemetrySnapshot` for immutable SHA-256 audit persistence (`TR-001`). Detailed in §5.3 and §7.2.

9. **`CMP-09`: Active Safety Interlock Button**
   - **Visual Role:** Pinned footer primary execution control (`[Active Lock: Sequence Incomplete]` when locked; `[Start Work]` when unlocked).
   - **Design Tokens:**
     - Locked Surface: `--dt-color-surface-raised`, `--dt-color-state-disabled`
     - Unlocked Surface: `--dt-color-state-success`
     - Breach Surface: `--dt-color-alarm-critical`
     - Height: `--dt-control-height-xl`
     - Radius: `--dt-radius-md`
   - **Architectural Scope:** Enforces active hardware/software negative interlocking (`NFR-229`). Governing Boolean conjunction in §5.3.

10. **`CMP-10`: SIMOPS Awareness Ribbon**
    - **Visual Role:** Compact non-modal alert strip inside `CMP-05` displaying active concurrent Work Permits within the proximity zone.
    - **Design Tokens:**
      - Surface: `--dt-color-surface-card`
      - Border: `--dt-color-border-subtle`
      - Icon Accent: `--dt-color-alarm-warning`
      - Radius: `--dt-radius-md`
    - **Architectural Scope:** Provides peripheral co-activity awareness without obstructing the sequential LOTO workflow. Detailed in §5.3.

11. **`CMP-11`: Fail-Safe Diagnostic Banner**
    - **Visual Role:** Diagnostic status strip inside `CMP-05` indicating live telemetry stream health (`Live Telemetry Connected`) or Priority 4 disconnected status and Cryptographic Offline Lease countdown (`AF-002`).
    - **Design Tokens:**
      - Surface: `--dt-color-surface-card`
      - Border: `--dt-color-border-subtle`
      - Connected Dot: `--dt-color-state-success`
      - Disconnected Text: `--dt-color-text-muted`
      - Height: `--dt-layout-banner-diagnostic-height`
    - **Architectural Scope:** Segregates network/lease diagnostics from process alarms ([ADR-006](../../../architecture/adr/ADR-006.md)). Detailed in §5.3.

12. **`CMP-12`: Evacuation Beacon Overlay**
    - **Visual Role:** Full-screen non-interactive passive emergency evacuation beacon deployed autonomously upon unexpected re-energization during active work (`AF-003`).
    - **Design Tokens:**
      - Surface: `--dt-color-alarm-critical` / `--dt-color-bg-canvas` (Diagonal hazard strobe)
      - Text: `--dt-color-alarm-text-critical`
      - Stacking: `--dt-z-modal-fail-safe`
    - **Architectural Scope:** Completely locks out touchscreen and pointer input per ISO 11064-5 and triggers an acoustic sweep (`IEvacuationAudioInterop`). Detailed in §5.3.

13. **`CMP-13`: Cartographic Compass & Metric Scale HUD**
    - **Visual Role:** Fixed bottom-left frosted spatial HUD combining a circular north-orientation compass indicator (`--dt-control-size-hud`) and a dynamic metric scale bar.
    - **Design Tokens:**
      - Surface: `--dt-color-float-bg`, `--dt-color-scale-bg`
      - Border: `--dt-color-float-border`
      - Elevation: `--dt-shadow-glass`
      - Compass Footprint: `--dt-control-size-hud`
      - Radius: `--dt-radius-full` (Compass)
    - **Architectural Scope:** Decoupled HTML overlay anchored at the bottom-left margin per [DT-UI-DS-DOC-001 §2.2](../../DT-UI-DS-DOC-001.md#22-dimensions-of-controls-and-touch-areas) and [§5.2](../../DT-UI-DS-DOC-001.md#52-elevation-shadows), calibrated via SVG `CALIBRATION-VECTOR` ([DT-UI-SVG-DOC-001 §11](../../DT-UI-SVG-DOC-001.md#11-spatial-metric-calibration)).

---

## 4. Screen State Catalog

1. **Normal / Energized (Default Baseline)**
   - **Activation Condition:** Initial opening of LOTO mode for a scheduled Work Order prior to field cutoff.
   - **Visual Modification:** Energy routes render as oblique `H/V + 45 deg` electrical paths and edge-anchored mechanical boundary segments in solid `--dt-color-alarm-critical`. Cutoff discs (`CMP-04`) display translucent `--dt-color-loto-disc` interiors with critical energized halos and `#icon-loto-energized`. Undocumented dotted halos around target equipment casings are prohibited. Sequential checklist `CMP-06` shows `0 / N LOCKED` with Step 1 active. Primary action control `CMP-09` is hard-disabled (`[#icon-loto-locked] Active Lock: Sequence Incomplete`). Status pill in `CMP-05` header displays `[HAZARDOUS ENERGY DETECTED]` in `--dt-color-alarm-critical`.

2. **Loading**
   - **Activation Condition:** Initial view load, asynchronous SVG layer parsing, or SignalR duplex WebSocket connection handshake in progress.
   - **Visual Modification:** Canvas vector overlays and drawer content display animated skeleton shimmer (`--dt-color-surface-raised`). Telemetry MAIs render neutral placeholder tracks without pointers. Action controls remain disabled.

3. **Selected Cutoff Node**
   - **Activation Condition:** Technician taps or clicks a cutoff node (`CMP-04`), taps an off-screen directional edge beacon, or selects a step in `CMP-06`.
   - **Visual Modification:** Target cutoff disc in `CMP-04` renders a high-contrast focus ring (`--dt-color-border-focus`), smoothly framing the node if off-screen. Corresponding checklist item in `CMP-06` and MAI card in `CMP-07` smoothly scroll into view with elevated background (`--dt-color-surface-raised`).

4. **Field Cutoff in Progress**
   - **Activation Condition:** Technician applies physical padlocks and enters Tag IDs sequentially in `CMP-06`.
   - **Visual Modification:** Confirmed energy branches transition from crimson energized vectors to dashed slate isolated paths (`--dt-color-loto-isolated-path`). Confirmed cutoff discs display `#icon-loto-locked` in Teal (`--dt-color-state-success`). Telemetry MAIs show pointers moving toward the zero-energy zone. `CMP-09` remains hard-disabled.

5. **Active Energy Detected (`AF-001`)**
   - **Activation Condition:** Telemetry reports energy above safe threshold ($V > 0.0\text{ V}$ or $P > 0.5\text{ psig}$) after cutoff attempt or backfeed (`AF-001`, `FR-232`).
   - **Visual Modification:** Critical alert banner deploys across `CMP-05` header (`--dt-color-alarm-critical`). Offending cutoff disc pulses with an animated critical halo (`--dt-color-alarm-critical`). Interlock marker on MAI scale bar highlights critical red (`--dt-color-mai-interlock`). `CMP-09` remains hard-disabled.

6. **Zero Energy Verified (Pre-Start)**
   - **Activation Condition:** Telemetry confirms all points within safe zero thresholds ($0.0\text{ V}$, $\le 0.5\text{ psig}$) AND all checklist padlocks in `CMP-06` are validated.
   - **Visual Modification:** All cutoff discs display `#icon-loto-locked` in Teal (`--dt-color-state-success`). Energy boundary lines render exclusively as isolated dashed slate vectors (`--dt-color-loto-isolated-path`). MAI pointers rest inside the safe zero-energy zone. Status pill in `CMP-05` header displays `[#icon-loto-locked TELEMETRY ZERO STATE · TRY-OUT REQUIRED]`. Try-Out card `CMP-08` becomes actionable (`--dt-color-border-focus`). `CMP-09` remains disabled until Try-Out signature submission.

7. **Ready to Execute (Unlocked)**
   - **Activation Condition:** Zero Energy corroborated by telemetry + Checklist 100% complete + Physical Try-Out attested and cryptographically signed (`FR-230`).
   - **Visual Modification:** Primary action control `CMP-09` (`[Start Work]`) unlocks with solid Teal fill (`--dt-color-state-success`). Status pill in `CMP-05` header transitions to `[#icon-loto-locked ZERO ENERGY VERIFIED · READY TO START]`.

8. **Work Order In Progress**
   - **Activation Condition:** Technician activates `[Start Work]` (`CMP-09`).
   - **Visual Modification:** `CMP-05` header status reflects active execution (`IN_PROGRESS`). Primary action button `CMP-09` transitions to `[Complete Work & De-isolate]` (`--dt-color-surface-raised`). Boundary route remains locked in slate dashed.

9. **Re-energization Emergency (`AF-003`)**
   - **Activation Condition:** Continuous telemetry monitoring detects hazardous energy flow ($V > 0.0\text{ V}$ or $P > 0.5\text{ psig}$) during active execution and broadcasts an emergency alert (`FR-232`, `AF-003`).
   - **Visual Modification:** Full-screen non-interactive passive evacuation overlay deployed via `CMP-12` (`--dt-z-modal-fail-safe`). Touchscreen input is completely locked out (zero dismiss controls per ISO 11064-5). Display flashes high-contrast diagonal hazard stripes (`--dt-color-alarm-critical` at $2\text{Hz}$) with imperative banner: `"[#icon-loto-energized] DANGER: HAZARDOUS ENERGY BREACH — EVACUATE AREA IMMEDIATELY"`, accompanied by a pulsed acoustic sweep (`IEvacuationAudioInterop`).

10. **Disconnectivity / Fail-Safe (`AF-002`)**
    - **Activation Condition:** Telemetry communication lost prior to work start ([ADR-006](../../../architecture/adr/ADR-006.md), `NFR-238`).
    - **Visual Modification:** Diagnostic banner `CMP-11` transitions to Priority 4 disconnected mode (`--dt-color-surface-card`, `--dt-color-text-muted`, `#icon-wifi-off`). If a valid Cryptographic Offline Lease exists, displays remaining lease countdown; if expired or absent, `CMP-09` locks in fail-safe state blocking initiation.

11. **Unmapped Cutoff Node (Geometry Unresolved)**
    - **Activation Condition:** Cutoff point defined in the work order isolation plan lacks valid coordinate mapping in `MeshMapping` (`UNMAPPED` or `SYNC_ERROR`).
    - **Visual Modification:** Drawer step in `CMP-06` displays a neutral diagnostic pill `[Coordinates Pending CAD Ingestion]` (`--dt-color-text-muted`) and disables spatial pan-to-node for that cutoff point without rendering arbitrary $(0, 0)$ canvas markers.

---

## 5. Interaction Rules and Data Flow

### 5.1. Initial Load & Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor Tech as Maintenance Technician
    participant UI as SCR-VIS-011 Interface
    participant IoT as Telemetry Service (IoT)
    participant SEC as Active Safety Interlock
    participant API as Safety Application Service

    Tech->>UI: Opens "LOTO Route" from Work Order
    UI->>API: GET /api/v1/safety/loto-plans/work-orders/{workOrderId}
    API-->>UI: Returns LotoIsolationPlanDto
    UI->>UI: Renders isolation boundary on SVG and initializes drawer (CMP-05)
    UI->>IoT: Subscribes to /hubs/telemetry (ReceiveTelemetryReading, LotoHeartbeatAck, EmergencyEvacuationBroadcast) & /hubs/operations (PermitStatusChanged, WorkOrderStatusChanged)
    IoT-->>UI: Live sensor readings pushed (< 1s latency)
    UI->>UI: Maps readings to MAI scale bars (CMP-07)

    opt Pre-Fetch Offline Lease for RF-Shadowed Area (ADR-006)
        UI->>API: POST /api/v1/safety/loto-plans/{workOrderId}/offline-lease (X-Idempotency-Key)
        API-->>UI: Returns CryptographicOfflineLeaseDto (MaxTtlMinutes = 60, HmacSignature)
    end
    
    Tech->>UI: Inputs Padlock Tag IDs sequentially into CMP-06
    UI->>API: POST /api/v1/safety/loto-plans/{planId}/cutoffs/{isolationPointId}/confirm (ConfirmCutoffStepRequestDto + X-Idempotency-Key)
    API-->>UI: Isolation step confirmed under SELECT ... FOR UPDATE NOWAIT
    
    Tech->>UI: Selects verification method, enters reading, signs Try-Out (CMP-08)
    UI->>API: POST /api/v1/safety/loto-plans/{planId}/try-out (TryOutAttestationDto + X-Idempotency-Key)
    API-->>UI: Attestation & hardware-bound signature registered (TR-001 audit logged)
    
    alt Hazardous Energy Detected (> threshold)
        API-->>UI: Safety Interlock Denied (Energy Detected / Uncertain)
        UI->>SEC: Maintains HARD LOCK (interlock active)
        UI->>Tech: Deploys Critical Alert "Hazardous Energy Detected"
    else Zero Energy Corroborated & Try-Out Attested
        API-->>UI: Safety Interlock Authorized (Zero State Proven)
        UI->>SEC: Enables [Start Work] control (CMP-09)
        Tech->>UI: Presses [Start Work]
        UI->>API: POST /api/v1/maintenance/work-orders/{id}/start-execution (StartWorkOrderExecutionCommand + X-Idempotency-Key)
        API-->>UI: Execution confirmed (WorkOrder IN_PROGRESS, TR-001 audit logged)
    end

    opt Re-energization Breach during Execution (AF-003)
        API-->>UI: High-priority /hubs/telemetry push: EmergencyEvacuationBroadcast (WorkOrder SUSPENDED)
        UI->>UI: Deploys non-interactive local emergency beacon (touch locked out)
        UI->>Tech: Emits high-urgency audio sweep & visual strobe warning (AF-003)
    end
```

1. **Initial Full-Circuit Framing & Pure SVG `<mask>` Focus+Context:**
   * Upon activation from a Work Order or [SCR-VIS-033](./SCR-VIS-033.md), the viewport executes a smooth fly-to transition framing the **complete isolation circuit** (`target EquipmentUnit` plus all linked upstream MCC breakers and mechanical isolation cutoff nodes) centered within the unoccluded canvas workspace left of `CMP-05`.
   * Under Focal Island De-emphasis, non-isolated plant equipment is attenuated cleanly outside a pure SVG `<mask>` aperture framing the target equipment and isolation zone while keeping full contrast exclusively inside the mask.
   * Electrical energy routes trace oblique orthogonal-plus-45-degree (`H/V + 45 deg`) paths from the remote MCC breaker core to the motor terminal, while mechanical process isolation boundaries anchor strictly to the exterior shell boundary perimeter (never cutting through tank interiors). Undocumented dotted perimeter halos around equipment casings are strictly prohibited.
   * Cutoff discs (`CMP-04`) project screen-space clamped scales (`32–40 px`) with obstacle collision avoidance against ANSI/ISA-5.1 instrument plates.
   * Drawer `CMP-05` initializes in baseline state with checklist step 1 highlighted and Try-Out card disabled.

2. **Data Subscriptions, API Idempotency & Concurrency/Lease Protocol:**
   * Establishes real-time duplex WebSocket streams per [DT-ARQ-CMP-DOC-001 §5](../../../architecture/views/DT-ARQ-CMP-DOC-001.md#5-signalr-hub-and-real-time-event-contract-registry-tr-010): `/hubs/telemetry` (`ITelemetryClient`: `ReceiveTelemetryReading`, `LotoHeartbeatAck` on a mandatory **2-second heartbeat cadence**, `EmergencyEvacuationBroadcast`) and `/hubs/operations` (`IOperationsClient`: `PermitStatusChanged`, `WorkOrderStatusChanged`).
   * Every mutating isolation and execution command (`POST /api/v1/safety/loto-plans/{planId}/cutoffs/{isolationPointId}/confirm`, `POST /api/v1/safety/loto-plans/{planId}/try-out`, `POST /api/v1/maintenance/work-orders/{id}/start-execution`, and `POST /api/v1/safety/loto-plans/{workOrderId}/offline-lease`) mandates `X-Idempotency-Key: {uuidv7}` ([ADR-007](../../../architecture/adr/ADR-007.md)) to guarantee idempotent execution across retries.
   * **Online Pessimistic Locking (`SELECT ... FOR UPDATE NOWAIT`):** Rather than client-supplied `If-Match` / PostgreSQL `xmin` optimistic concurrency on `confirm`, `try-out`, and `start-execution`, online submissions enforce server-side pessimistic locking (`SELECT ... FOR UPDATE NOWAIT`) on the isolation record per [DT-ARQ-DB-DOC-001 §3.7](../../../architecture/DT-ARQ-DB-DOC-001.md#37-pessimistic-locking-vs-distributed-offline-leases-for-loto-isolation-vis-011-asr-002-adr-006), aborting immediately as an indeterminate-safety lock conflict if concurrently locked by telemetry ingestion.
   * **Offline Lease Delegation (`ADR-006`):** Prior to entering disconnected field zones, the client requests a bounded lease via `POST /api/v1/safety/loto-plans/{workOrderId}/offline-lease`, persisting the signed `CryptographicOfflineLeaseDto` (`LeaseToken`, `WorkOrderId`, `IssuedToUserId`, `ExpiresAtUtc`, `MaxTtlMinutes = 60`, `HmacSignature`) in local secure storage (`ISecureStorage` / `IOfflineStorage`, `TR-006`), bounded to a **60-minute max TTL** validated against the **hardware monotonic clock**. Offline commands execute against the active lease and replay with `CryptographicOfflineLeaseDto` (`LeaseToken`) + `X-Idempotency-Key` upon reconnection.

### 5.2. Spatial Navigation, Edge Beacons & Tactile Mechanics

1. **Viewport Pan, Zoom & LOTO Framing:** Shared pure-`viewBox` camera, site-boundary clamping, instant focal wheel zoom, and unified `> 4px` drag-threshold panning follow [DT-UI-SVG-DOC-001 §10.2](../../DT-UI-SVG-DOC-001.md#102-pure-viewbox-camera-site-boundary-clamping-transition-rules). Stationary clicks ($\le 4\text{px}$) select cutoff hotspot discs (`CMP-04`), while programmatic navigation (`CMP-06` step jump, edge beacon tap, view reset) interpolates smoothly.

2. **Off-Screen Directional Edge Beacons (Level 3 Zoom Awareness):**
   * When zooming deeply into the target unit (`Scale >= --dt-zoom-scale-l2-max`), upstream MCC breakers or distant isolation valves located outside the visible `viewBox` remain tracked via frosted directional edge beacons (`--dt-color-float-bg-strong`, `--dt-shadow-glass`) docked along the unoccluded viewport boundary edge (offset inward from `CMP-05` and HUD margins).
   * Nearby off-screen nodes along the same edge cluster cleanly into directional badges (`<< 2 MCC`), showing aggregate energized/isolated status; tapping any beacon smoothly pans and frames that isolation node.

3. **Layout Shift Invariants & Dimension Enforcements:**
   * Toolbar `CMP-02`: Level indicator badge enforces a rigid fixed width (`--dt-layout-toolbar-badge-width`), preventing horizontal control jitter across zoom transitions.
   * Drawer `CMP-05`: Sized by normative layout token `--dt-layout-drawer-width` with permanent scrollbar gutter reservation, strictly preserving canvas visibility. Breakpoint mappings are detailed in Section 8.

4. **Bottom Sheet Snap Physics & Discrete Switching (`CMP-05`):**
   * In portrait tablet orientation, `CMP-05` operates as an ergonomic bottom sheet transitioning between natural collapsed height and expanded height (exact viewport percentages detailed in Section 8).
   * **Gesture Snap Physics:** Dragging past velocity threshold $> 0.5\text{px/ms}$ or displacement $> 25\%$ distance snaps to destination state via spring animation.
   * **Discrete Switching Invariant (ISO 9241-110 Clause 5.5 / [DT-UI-DS-DOC-001 §6.3](../../DT-UI-DS-DOC-001.md#63-sliding-containers-pattern-bottom-sheets-and-drawers)):** To guarantee usability under adverse field conditions (e.g., rain droplets, gloved operation), container deployment is NEVER conditioned exclusively to drag gestures. A single discrete tap on the touch drag handle immediately toggles sheet elevation between natural collapsed height and expanded height via standard cubic-bezier sheet transition.

5. **Overlay Drawer Lifecycle (Minimize vs. Deselect / Close Contract):**
   * Per [DT-UI-DS-DOC-001 §2.4](../../DT-UI-DS-DOC-001.md#24-structural-layout-and-dimensional-tokens) and [DT-UI-NAV-DOC-001](../../DT-UI-NAV-DOC-001.md):
     * **Minimization (Chevron Trigger `>` / Tactical Pull-Down):** Retracts `CMP-05` to the viewport edge while preserving an exposed peek tab (`--dt-layout-bottom-sheet-peek-height`) for immediate re-expansion during spatial route tracing. The active equipment selection halo, checklist cursor, and real-time SignalR telemetry subscriptions are retained in memory.
     * **Explicit Dismissal / Exit (Close `×` Button):** Closes `CMP-05`, suppresses the peek trigger, and clears cutoff focus on the SVG canvas, returning the viewport to the supervisory baseline.

### 5.3. Domain Workflows, Interlocks, and Telemetry

1. **Sequential Padlock Verification Rule (`FR-228`):**
   * Checklist `CMP-06` enforces strict thermodynamic and procedural sequencing:
     $$\text{Electrical Cutoff} \longrightarrow \text{Mechanical Upstream Isolation} \longrightarrow \text{Mechanical Downstream Isolation} \longrightarrow \text{Bleed / Venting}$$
   * Physical Padlock Tag IDs must conform to configured facility nomenclature (e.g., regex mask `^PAD-[A-Z0-9]{4,8}$`) or be captured directly via NFC / 2D barcode scan.
   * Step $N+1$ cannot be confirmed until Step $N$ is marked and verified. Upon step verification, the client dispatches `ConfirmCutoffStepRequestDto` (§7.2.3, encapsulating `SequenceOrder`, `IsolationPointId`, and `AppliedPadlockTagId`) with `X-Idempotency-Key` to `POST /api/v1/safety/loto-plans/{planId}/cutoffs/{isolationPointId}/confirm` (locked online via `SELECT ... FOR UPDATE NOWAIT` per [DT-ARQ-DB-DOC-001 §3.7](../../../architecture/DT-ARQ-DB-DOC-001.md#37-pessimistic-locking-vs-distributed-offline-leases-for-loto-isolation-vis-011-asr-002-adr-006)).

2. **Moving Analog Indicator (MAI) Zero-Energy Verification (`CMP-07`):**
   * Continuous telemetry variables ($V, I, P, Q$) are rendered using Moving Analog Indicators (MAI) per [DT-UI-DS-DOC-001 §6.1](../../DT-UI-DS-DOC-001.md#61-moving-analog-indicator-mai-specification) and ISA-101.
   * Pointer position on the normalized scale track ($[0\%, 100\%]$) is evaluated as:
     $$\text{PointerPos} = \text{clamp}\left(\frac{\text{MeasuredValue} - \text{ScaleMin}}{\text{ScaleMax} - \text{ScaleMin}}, 0.0, 1.0\right) \times 100\%$$
   * **Safe Normal Zone (`--dt-color-mai-normal-zone`):** Spans the verified zero energy range ($[0.0, 0.0]\text{V}$ for electrical voltage; $[0.0, 0.5]\text{A}$ for electrical current; $[0.0, 0.5]\text{psig}$ for pressure; $[0.0, 1.0]\text{gpm}$ for flow).
   * **Trip Interlock Marker (`--dt-color-mai-interlock`):** Fixed tick at the maximum permissible safe threshold ($0.0\text{V}$, $0.5\text{A}$, $0.5\text{psig}$, $1.0\text{gpm}$). If `MeasuredValue > TripThreshold`, the interlock tick and Method 3 `[■ 1]` breach marker highlight in `--dt-color-alarm-critical` and trip the software interlock.

3. **Physical Try-Out Verification & Cryptographic Persistence (`CMP-08`, `FR-230`, `TR-001`):**
   * Mandates physical absence-of-energy test (OSHA 1910.147 §(d)(6)). The technician must physically execute and record the test in `CMP-08`.
   * **Verification Input Controls:**
     * **Method Selector:** Bound to the `TryOutMethod` enum (§7.2.3), capturing direct electrical dead-test (`MULTIMETER_PROBE`), atmospheric vent opening (`ATMOSPHERIC_VENT_BLEED`), or local start attempt (`LOCAL_PUSHBUTTON_ATTEMPT`).
     * **Observed Value / State Field:** Recorded field metric (e.g., `0.00 V`, `0.0 psig`, or `Zero Motion Confirmed`).
     * **Technician Attestation Signature:** Mandatory field technician cryptographic sign-off.
   * Upon attestation submission, the client captures:
     * Cryptographic attestation token: Digital signature generated via the device's hardware-bound security module (`TR-006`, `ADR-006`), binding technician identity, timestamp, and verification payload without exposing raw private keys in client memory.
     * Telemetry verification snapshot: Structured payload capturing instantaneous sensor values across all cutoff points at attestation time per [DT-ERD-DOC-001 §6.6](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#66-viswork_order_isolationstelemetry_snapshot).
   * Encapsulated into `TryOutAttestationDto` (§7.2.3, containing `IsolationPointId`, `Method`, `ObservedPhysicalReading`, `TechnicianSignatureHash`, `TelemetrySnapshot`, and `AttestedAtUtc`) and dispatched with `X-Idempotency-Key` to `POST /api/v1/safety/loto-plans/{planId}/try-out`. The application service acquires a pessimistic `SELECT ... FOR UPDATE NOWAIT` lock online ([DT-ARQ-DB-DOC-001 §3.7](../../../architecture/DT-ARQ-DB-DOC-001.md#37-pessimistic-locking-vs-distributed-offline-leases-for-loto-isolation-vis-011-asr-002-adr-006)), updates isolation state, and appends an immutable audit record with SHA-256 hash chaining (`TR-001`).

4. **Active Safety Interlock Logic (`NFR-229`, `FR-230`):**
   * Work initiation button `CMP-09` `[Start Work]` reflects the server-authoritative safety gate. The backend application service permits work execution strictly when the following Boolean invariant evaluates to true:
     $$\text{CanStartWork} = \text{ChecklistCompleted} \land \text{TryOutAttested} \land \text{TelemetryNotEnergized} \land (\text{IsOnline} \lor \text{ValidOfflineLease})$$
   * **Normative Asymmetry (Negative Interlock Primacy):** IoT telemetry operates strictly as a **negative interlock**, never as a positive authorization enabler. The presence of detected energy ($V > 0.0\text{V}$ or $P > 0.5\text{psig}$) or telemetry uncertainty/sensor fault immediately and unconditionally forces $\text{CanStartWork} = \text{false}$. Conversely, telemetry showing zero energy is insufficient on its own to enable work: affirmative authorization is gated strictly by 100% physical checklist completion and verified manual Try-Out attestation.
   * **Client Presentation Contract:** The UI reflects this rule via an optimistic state calculation (`CanStartWork`) that sets the disabled state (`--dt-color-state-disabled`) on `CMP-09`. However, client DOM manipulation cannot bypass the interlock: activating `[Start Work]` dispatches `StartWorkOrderExecutionCommand` (§7.2.3) with `X-Idempotency-Key` to `POST /api/v1/maintenance/work-orders/{id}/start-execution`, which is authoritatively validated under `SELECT ... FOR UPDATE NOWAIT` online (or against `CryptographicOfflineLeaseDto` in offline lease mode per [DT-ARQ-DB-DOC-001 §3.7](../../../architecture/DT-ARQ-DB-DOC-001.md#37-pessimistic-locking-vs-distributed-offline-leases-for-loto-isolation-vis-011-asr-002-adr-006)) before transitioning the Work Order to `IN_PROGRESS`.
   * In offline disconnected operations with a valid lease (`ADR-006`), live telemetry evaluation is bypassed in favor of mandatory physical Try-Out attestation verified against the hardware keystore.

5. **Continuous In-Execution Monitoring & Emergency Broadcast Handling (`FR-232`, `AF-003`):**
   * While the Work Order is `IN_PROGRESS`, backend surveillance monitors isolation cutoff telemetry.
   * Upon intercepting the high-priority `EmergencyEvacuationBroadcast` SignalR push alert (dispatched by the backend when hazardous energy flow $V > 0.0\text{V}$ or $P > 0.5\text{psig}$ is detected, autonomously suspending the Work Order per `AF-003`), the client interface executes the emergency protocol:
     1. **Local Supplementary Warning Overlay (`CMP-12`):** Immediately deploys the non-interactive passive evacuation overlay. All touchscreen and pointer interactions are locked out (zero confirmation buttons or dismiss controls) to eliminate cognitive friction, panic freezing, or dangerous attempts to interact with the device under acute life-threatening stress (ISO 11064-5).
     2. **Multimodal Strobe & Warning Sweep:** The tablet screen strobes high-contrast diagonal safety hazard stripes (alternating `--dt-color-alarm-critical` and `--dt-color-bg-canvas` at $2\text{Hz}$) displaying large-format typography: `"[#icon-loto-energized] DANGER: HAZARDOUS ENERGY BREACH — EVACUATE AREA IMMEDIATELY"`. Concurrently, client interop triggers an autonomous pulsed audio frequency sweep ($800\text{Hz} - 1200\text{Hz}$) at maximum device volume as a local supplemental cue alongside plant evacuation sirens.

6. **LOTO Watchdog Heartbeat & Cryptographic Offline Lease Protocol (`ADR-006`, `NFR-238`, `AF-002`, `TR-006`, `TR-007`, `TR-010`):**
   * **Mandatory 2-Second Heartbeat & 30-Second Grace Window ([DT-ARQ-DEP-DOC-001 §4](../../../architecture/views/DT-ARQ-DEP-DOC-001.md#4-perimeter-security-mechanism-loto-watchdog-fail-safe), [DT-UI-NAV-DOC-001 §6.2](../../DT-UI-NAV-DOC-001.md#62-loto-lockout-and-fail-safe-guard)):** The background LOTO Watchdog (`loto_watchdog`) validates WebSocket connectivity over `/hubs/telemetry` by sending a heartbeat ping on a mandatory **2-second cadence** and tracking `LotoHeartbeatAck` acknowledgments. To tolerate industrial RF shadowing and AP roaming without false positives, a **30-second Grace Window** applies before declaring telemetry disconnection and evaluating fail-safe lockout on `CMP-09`.
   * **Lease Acquisition & Monotonic Clock Evaluation (`ADR-006`):** Prior to offline entry, the client acquires an HMAC-SHA256-signed `CryptographicOfflineLeaseDto` via `POST /api/v1/safety/loto-plans/{workOrderId}/offline-lease` (`X-Idempotency-Key`), transitioning the server isolation record to `LEASED_OFFLINE` ([DT-ARQ-DB-DOC-001 §3.7](../../../architecture/DT-ARQ-DB-DOC-001.md#37-pessimistic-locking-vs-distributed-offline-leases-for-loto-isolation-vis-011-asr-002-adr-006)). If the **30-second Grace Window** expires without `LotoHeartbeatAck`, the client validates the cached `CryptographicOfflineLeaseDto` (`LeaseToken`, `WorkOrderId`, `IssuedToUserId`, `ExpiresAtUtc`, `MaxTtlMinutes = 60`, `HmacSignature`). `RemainingLeaseSeconds` is strictly bounded to a **60-minute max TTL** ($\le 3600\text{ s}$) and evaluated against the device's **hardware monotonic clock** (mitigating OS wall-clock tampering or NTP skew).
   * **Active Lease Present:** Transitions to bounded offline safe mode, deploying `CMP-11` in informational mode (*"Offline Safety Mode Active (Lease expires: HH:mm UTC)"* with `RemainingLeaseSeconds` countdown). Mandates physical Try-Out re-verification (`CMP-08`) and queues `ConfirmCutoffStepRequestDto`, `TryOutAttestationDto`, and `StartWorkOrderExecutionCommand` into the encrypted offline outbox (`TR-007`) paired with `CryptographicOfflineLeaseDto` (`LeaseToken`) + `X-Idempotency-Key` for deferred reconciliation upon reconnection ([DT-ARQ-DB-DOC-001 §3.7](../../../architecture/DT-ARQ-DB-DOC-001.md#37-pessimistic-locking-vs-distributed-offline-leases-for-loto-isolation-vis-011-asr-002-adr-006)).
   * **Expired or Absent Lease:** Writes a Preventive Security Lockout flag to encrypted local storage (`DT-ARQ-DEP-DOC-001 §4`) and triggers an immediate fail-safe lock on `CMP-09`, displaying *"Danger: Telemetry communication lost. Intervention blocked by fail-safe design"*. Initiation requires connectivity restoration (and fresh Zero-Energy confirmation) or dual-supervisor cryptographic override.

---

## 6. Industrial and Safety Considerations

* **Try-Out Primacy & Negative Interlock Asymmetry (OSHA 1910.147 §(d)(6) / ISO 45001 §8.1):** Physical lockout and manual Try-Out attestation constitute the mandatory legal authorization for equipment intervention. Real-time IoT telemetry acts strictly as a subordinate **negative interlock** (fail-safe veto) that blocks execution upon detecting residual energy or sensor uncertainty (`NFR-229`, `NFR-234`), preventing cognitive over-reliance on instrumentation (§5.3).
* **Passive Emergency Ergonomics & SIS Boundary (ISO 11064-5 / IEC 61508):** Under unscheduled re-energization during active execution (`AF-003`), `CMP-12` converts the tablet into a non-interactive passive evacuation beacon (zero dismiss buttons) to eliminate panic-induced cognitive latency. Because commercial mobile runtimes are not SIL-certified Safety Instrumented Systems (SIS), `CMP-12` serves strictly as a supplementary local warning alongside certified plant evacuation sirens.
* **Fail-Safe Disconnectivity & HPHMI Governance ([TR-011](../../../requirements/common/TR-011.md)):** Telemetry dropouts default to a hazardous locked state unless authorized by an unexpired hardware-bound Cryptographic Offline Lease ([ADR-006](../../../architecture/adr/ADR-006.md)). Visual coding, MAI zero-energy tracks, Teal documentary confirmation (`--dt-color-state-success`), and gloved tactile ergonomics (`--dt-touch-target-mobile`) adhere strictly to [DT-UI-DS-DOC-001 §1](../../DT-UI-DS-DOC-001.md#1-scope), [§6.1](../../DT-UI-DS-DOC-001.md#61-moving-analog-indicator-mai-specification), [§6.2](../../DT-UI-DS-DOC-001.md#62-redundant-coding-matrix-for-permits-and-loto), and [§6.3](../../DT-UI-DS-DOC-001.md#63-sliding-containers-pattern-bottom-sheets-and-drawers).

---

## 7. Frontend Component Contract (Blazor / Razor)

### 7.1. Component Hierarchy & File Mapping

```text
Pages/
└── LotoIsolationMatrixPage.razor              # Root Operational View (SCR-VIS-011)
    ├── CanvasViewport2D.razor                 # CMP-01: Shared SVG canvas with LOTO layer
    │   ├── LotoBoundaryRoute.razor            # Vector energy path and boundary polygon
    │   └── IsolationCutoffNode.razor          # CMP-04: Breaker / Valve cutoff hotspot symbols
    ├── ViewportToolbar.razor                  # CMP-02: Floating navigation & focal de-emphasis bar
    ├── UserProfileButton.razor                # CMP-03: Top-left user profile indicator
    ├── CartographicHud.razor                  # CMP-13: Bottom-left compass & metric scale HUD
    ├── LotoIsolationDrawer.razor              # CMP-05: Main contextual safety container
    │   ├── LotoHeaderInfo.razor               # Equipment Unit info, status pill & SOP link
    │   ├── SimopsAwarenessRibbon.razor        # CMP-10: Concurrent proximity permits alert strip
    │   ├── FailSafeDiagnosticBanner.razor     # CMP-11: Telemetry connection & Offline Lease banner
    │   ├── SequentialChecklist.razor          # CMP-06: Step-by-step physical padlock list
    │   ├── TelemetryVerificationMatrix.razor  # CMP-07: Live multi-sensor MAI scale bar cards
    │   ├── PhysicalTryOutCard.razor           # CMP-08: Absence-of-energy verification card
    │   └── ActiveSafetyInterlockButton.razor  # CMP-09: Interlocked [Start Work] action button
    └── EvacuationBeaconOverlay.razor          # CMP-12: Non-interactive passive emergency evacuation beacon
```

### 7.2. Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)

#### 7.2.1. `LotoIsolationMatrixPage.razor` (Root View)
```csharp
[Parameter, SupplyParameterFromQuery(Name = "workOrderId")]
public Guid? WorkOrderId { get; set; }

[Parameter, SupplyParameterFromQuery(Name = "equipId")]
public Guid? EquipmentUnitId { get; set; }

[Parameter]
public string? WorkOrderNumber { get; set; }
```

#### 7.2.2. Subcomponent Parameter Contracts (`CMP-01` to `CMP-13`)
```csharp
// CMP-01: CanvasViewport2D.razor
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

// LotoBoundaryRoute.razor
[Parameter]
public required string TargetEquipmentTag { get; set; }

[Parameter]
public required ZeroEnergyState OverallEnergyState { get; set; }

[Parameter]
public required IReadOnlyList<CutoffPointStatusDto> CutoffPoints { get; set; }

// CMP-04: IsolationCutoffNode.razor
[Parameter]
public required CutoffPointStatusDto CutoffPoint { get; set; }

[Parameter]
public bool IsSelected { get; set; }

[Parameter]
public EventCallback<string> OnNodeSelected { get; set; }

// CMP-02: ViewportToolbar.razor
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

// CMP-03: UserProfileButton.razor
[Parameter]
public required string UserInitials { get; set; }

[Parameter]
public EventCallback OnProfileMenuRequested { get; set; }

// CMP-13: CartographicHud.razor
[Parameter]
public double ZoomScale { get; set; } = 1.0;

[Parameter]
public double ScaleRatioMetersPerUnit { get; set; } = 0.2;

// CMP-05: LotoIsolationDrawer.razor
[Parameter]
public required LotoIsolationPlanDto Plan { get; set; }

[Parameter]
public required ZeroEnergyState OverallEnergyState { get; set; }

[Parameter]
public bool IsMinimized { get; set; }

[Parameter]
public EventCallback<bool> OnMinimizeToggled { get; set; }

[Parameter]
public EventCallback OnCloseRequested { get; set; }

// LotoHeaderInfo.razor
[Parameter]
public required LotoIsolationPlanDto Plan { get; set; }

[Parameter]
public required ZeroEnergyState OverallEnergyState { get; set; }

[Parameter]
public EventCallback OnMinimizeClicked { get; set; }

[Parameter]
public EventCallback OnCloseClicked { get; set; }

// CMP-10: SimopsAwarenessRibbon.razor
[Parameter]
public required IReadOnlyList<SimopsPermitSummaryDto> ActiveSimopsPermits { get; set; }

// CMP-11: FailSafeDiagnosticBanner.razor
// Monitors the 2s LotoHeartbeatAck cadence; triggers IsOffline after the 30s Grace Window expires
// (enforcing immediate fail-safe lock on CMP-09 if no valid lease exists per DT-ARQ-DEP-DOC-001 §4 & DT-UI-NAV-DOC-001 §6.2).
// RemainingLeaseSeconds is bounded to a 60-minute max TTL (0..3600s) validated against the hardware monotonic clock (ADR-006).
[Parameter]
public bool IsOffline { get; set; }

[Parameter]
public bool HasValidOfflineLease { get; set; }

/// <summary>
/// Remaining lease lifetime in seconds (bounded to [0, 3600] — 60-minute max TTL — derived from hardware monotonic clock elapsed ticks per ADR-006).
/// </summary>
[Parameter]
public int RemainingLeaseSeconds { get; set; }

// CMP-06: SequentialChecklist.razor
[Parameter]
public required IReadOnlyList<ChecklistStepDto> Steps { get; set; }

[Parameter]
public EventCallback<ConfirmCutoffStepRequestDto> OnStepVerified { get; set; }

// CMP-07: TelemetryVerificationMatrix.razor (MAI Display)
[Parameter]
public required IReadOnlyList<CutoffPointStatusDto> CutoffPoints { get; set; }

[Parameter]
public required ZeroEnergyState OverallEnergyState { get; set; }

// CMP-08: PhysicalTryOutCard.razor
[Parameter]
public bool IsActionable { get; set; }

[Parameter]
public bool IsAttested { get; set; }

[Parameter]
public TryOutMethod SelectedMethod { get; set; } = TryOutMethod.MULTIMETER_PROBE;

[Parameter]
public string ObservedValue { get; set; } = string.Empty;

[Parameter]
public EventCallback<TryOutAttestationDto> OnTryOutAttested { get; set; }

// CMP-09: ActiveSafetyInterlockButton.razor
[Parameter]
public bool CanStartWork { get; set; }

[Parameter]
public WorkOrderStatus CurrentWorkOrderStatus { get; set; } = WorkOrderStatus.SCHEDULED;

[Parameter]
public EventCallback OnStartWorkInitiated { get; set; }

// CMP-12: EvacuationBeaconOverlay.razor
[Parameter]
public bool IsActive { get; set; }

[Parameter]
public string OffendingNodeTag { get; set; } = string.Empty;

[Parameter]
public decimal DetectedEnergyValue { get; set; }

[Parameter]
public string EngineeringUnit { get; set; } = string.Empty;
```

#### 7.2.3. Data Transfer Objects (DTOs)
```csharp
public record LotoIsolationPlanDto
{
    public required Guid PlanId { get; init; }
    public required Guid WorkOrderId { get; init; }
    public required string WorkOrderNumber { get; init; }
    public required WorkOrderStatus WorkOrderStatus { get; init; }
    public required Guid EquipmentUnitId { get; init; }
    public required string TargetEquipmentTag { get; init; }
    public required string TargetEquipmentDescription { get; init; }
    public required string FunctionalLocationName { get; init; }
    public WorkPermitStatus? LinkedPermitStatus { get; init; }
    public required string StandardOperatingProcedureCode { get; init; }
    public required string StandardOperatingProcedureUrl { get; init; }
    public IReadOnlyList<string> RequiredPpeCodes { get; init; } = [];
    public IReadOnlyList<CutoffPointStatusDto> CutoffPoints { get; init; } = [];
    public IReadOnlyList<ChecklistStepDto> ChecklistSteps { get; init; } = [];
    public IReadOnlyList<SimopsPermitSummaryDto> ActiveSimopsPermits { get; init; } = [];
    public required uint ConcurrencyToken { get; init; }
}

public record CutoffPointStatusDto
{
    public required Guid IsolationPointId { get; init; }
    public required string CutoffNodeId { get; init; }
    public required string PhysicalTag { get; init; }
    public required IsolationType Type { get; init; }
    public required IsolationStatus IsolationStatus { get; init; }
    public required string VariableName { get; init; }
    public required TelemetrySignalType SignalType { get; init; }
    public required decimal MeasuredValue { get; init; }
    public required string EngineeringUnit { get; init; }
    public required decimal ScaleMin { get; init; }
    public required decimal ScaleMax { get; init; }
    public required decimal SafeZeroThreshold { get; init; }
    public required decimal TripThreshold { get; init; }
    public bool IsSensorZeroEnergy { get; init; }
    public bool IsLocationMapped { get; init; } = true;
    public required string SensorHealthCode { get; init; }
    public required DateTimeOffset LastReadingUtc { get; init; }
}

public record ChecklistStepDto
{
    public required int SequenceOrder { get; init; }
    public required Guid IsolationPointId { get; init; }
    public required string CutoffNodeId { get; init; }
    public required string ActionDescription { get; init; }
    public required string ExpectedPadlockTagId { get; init; }
    public string? AppliedPadlockTagId { get; init; }
    public bool IsVerified { get; init; }
    public DateTimeOffset? VerifiedAtUtc { get; init; }
}

public record ConfirmCutoffStepRequestDto
{
    public required int SequenceOrder { get; init; }
    public required Guid IsolationPointId { get; init; }
    public required string AppliedPadlockTagId { get; init; }
    public string? OfflineLeaseToken { get; init; }
}

public record SimopsPermitSummaryDto
{
    public required string PermitIdentifier { get; init; }
    public required PermitType PermitType { get; init; }
    public required string TargetEquipmentTag { get; init; }
    public required decimal DistanceMeters { get; init; }
}

/// <summary>
/// Physical Try-Out attestation DTO; TelemetrySnapshot maps to the WorkOrderIsolation JSONB contract per DT-ERD-DOC-001 §6.6.
/// Online execution locks the (work_order_id, isolation_point_id) WorkOrderIsolation row via SELECT ... FOR UPDATE NOWAIT (DT-ARQ-DB-DOC-001 §3.7).
/// </summary>
public record TryOutAttestationDto
{
    public required Guid IsolationPointId { get; init; }
    public required TryOutMethod Method { get; init; }
    public required string ObservedPhysicalReading { get; init; }
    public required string TechnicianSignatureHash { get; init; }
    public required IReadOnlyDictionary<string, decimal> TelemetrySnapshot { get; init; }
    public required DateTimeOffset AttestedAtUtc { get; init; }
    public string? OfflineLeaseToken { get; init; }
}

/// <summary>
/// Device-bound HMAC-SHA256 offline LOTO lease token issued by POST /api/v1/safety/loto-plans/{workOrderId}/offline-lease and persisted in encrypted local storage (ADR-006).
/// MaxTtlMinutes is capped at 60 (60-minute max TTL); RemainingLeaseSeconds (0..3600) is computed strictly from the hardware monotonic clock
/// after the 30-second Grace Window expires without a 2-second LotoHeartbeatAck heartbeat (DT-ARQ-DEP-DOC-001 §4, DT-UI-NAV-DOC-001 §6.2).
/// </summary>
public record CryptographicOfflineLeaseDto
{
    public required string LeaseToken { get; init; }
    public required Guid WorkOrderId { get; init; }
    public required Guid IssuedToUserId { get; init; }
    public required DateTimeOffset ExpiresAtUtc { get; init; }
    public int MaxTtlMinutes { get; init; } = 60;
    public required string HmacSignature { get; init; }
    public required int RemainingLeaseSeconds { get; init; }
    public required long MonotonicIssuedTimestampMs { get; init; }
}

/// <summary>
/// Authoritative execution start command dispatched to POST /api/v1/maintenance/work-orders/{id}/start-execution.
/// Online execution enforces server-side SELECT ... FOR UPDATE NOWAIT (DT-ARQ-DB-DOC-001 §3.7);
/// offline lease execution pairs OfflineLeaseToken (from CryptographicOfflineLeaseDto) with X-Idempotency-Key (ADR-006, ADR-007).
/// </summary>
public record StartWorkOrderExecutionCommand
{
    public required Guid WorkOrderId { get; init; }
    public required Guid LotoPlanId { get; init; }
    public required Guid TechnicianUserId { get; init; }
    public string? OfflineLeaseToken { get; init; }
    public required DateTimeOffset RequestedAtUtc { get; init; }
}

/// <summary>
/// Controlled physical energy isolation vocabulary per DT-DM-DOC-001 §4.28.
/// </summary>
public enum IsolationType
{
    ELECTRICAL,
    MECHANICAL,
    PNEUMATIC,
    HYDRAULIC,
    CHEMICAL,
    THERMAL,
    GRAVITATIONAL
}

/// <summary>
/// Controlled work order isolation lifecycle vocabulary per DT-DM-DOC-001 §4.32.
/// </summary>
public enum IsolationStatus
{
    PENDING_ISOLATION,
    ISOLATED,
    VERIFIED_ZERO_ENERGY,
    LEASED_OFFLINE,
    RELEASED
}

/// <summary>
/// Consolidated negative-interlock energy state evaluation.
/// </summary>
public enum ZeroEnergyState
{
    ENERGIZED,
    UNCERTAIN,
    ZERO_ENERGY_VERIFIED
}

/// <summary>
/// Controlled physical Try-Out verification method vocabulary per DT-DM-DOC-001 §4.33.
/// </summary>
public enum TryOutMethod
{
    MULTIMETER_PROBE,
    ATMOSPHERIC_VENT_BLEED,
    LOCAL_PUSHBUTTON_ATTEMPT
}

/// <summary>
/// Controlled sensor signal classification vocabulary per DT-DM-DOC-001 §4.30.
/// </summary>
public enum TelemetrySignalType
{
    TEMPERATURE,
    PRESSURE,
    VIBRATION,
    FLOW_RATE,
    VOLTAGE,
    CURRENT,
    RPM,
    OPERATING_HOURS,
    CYCLES
}

/// <summary>
/// Controlled permit risk classification vocabulary per DT-DM-DOC-001 §4.34.
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
/// Controlled permit lifecycle status vocabulary per DT-DM-DOC-001 §4.35.
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

/// <summary>
/// Controlled work order execution status vocabulary per DT-DM-DOC-001 §4.21.
/// </summary>
public enum WorkOrderStatus
{
    PLANNING,
    WAITING_PARTS,
    SCHEDULED,
    IN_PROGRESS,
    SUSPENDED,
    COMPLETE,
    CLOSED
}
```

### 7.3. Client-Side DOM & Interop Bridge

1. **SVG Viewport & LOTO Route Interop (`ILotoCanvasInterop`):**
   * Manipulates SVG path stroke attributes (crimson solid oblique `H/V + 45 deg` and edge-anchored paths for active hazardous energy vs. `--dt-color-loto-isolated-path` dashed paths for confirmed isolated lines) and pure `<mask>` Focal Island apertures in real time without triggering full SVG re-parsing.
   * Tracks PointerEvents for pure `viewBox` panning (site-boundary center clamping), unified primary/middle-click and tablet $4\text{px}$ drag thresholding, instant focal wheel zoom, smooth full-circuit fly-to transitions, and directional off-screen edge beacon projection.
2. **Cutoff Node Hotspot Binding:**
   * Standardized SVG data attribute binding (`data-cutoff-id`, `data-equip-id`). Disambiguates $> 4\text{px}$ pan drags from discrete stationary taps ($\le 4\text{px}$) on cutoff discs (`CMP-04`), enforces screen-space clamping (`32–40 px`) with ANSI/ISA-5.1 obstacle avoidance, and dispatches selection to highlight corresponding checklist steps in `CMP-06` and MAI cards in `CMP-07`.
3. **Encrypted Offline Storage & Lease Interop (`IOfflineStorage`):**
   * Interfaces with client-side encrypted local storage (`TR-002`, `TR-006`, `TR-007`) for offline cryptographic lease evaluation against the **hardware monotonic clock** (60-minute max TTL per `ADR-006`), Preventive Security Lockout persistence after expiration of the **30-second Grace Window** without **2-second `LotoHeartbeatAck` heartbeats** (`DT-ARQ-DEP-DOC-001 §4`), and transactional outbox queuing of verification commands during network disconnections.
4. **Emergency Evacuation Interop (`IEvacuationAudioInterop`):**
   * Encapsulates client-side acoustic sweep generation ($800\text{Hz} - 1200\text{Hz}$ at $2\text{Hz}$ modulation) calibrated to $\approx 85\text{ dBA}$ alongside full viewport pointer and keyboard event trapping, guaranteeing complete non-interactive passivity during life-safety evacuation (`CMP-12`, `AF-003`).

---

## 8. Layout and Responsive Adaptability

### 8.1. Desktop Workstation (`--dt-breakpoint-xl`)
* **Layout Organization:** Canvas `CMP-01` occupies the full viewport (`--dt-z-canvas`) with user profile indicator `CMP-03` anchored at top-left and cartographic HUD `CMP-13` anchored at bottom-left. LOTO Drawer `CMP-05` docks as a full-height lateral panel sized by `--dt-layout-drawer-width-desktop` (`--dt-z-drawer-sidebar`, `--dt-shadow-panel`) on the right flank. Viewport toolbar `CMP-02` centers over the unoccluded canvas workspace.
* **Ergonomic Rules:** Instant mouse wheel focal zoom around pointer $(cx, cy)$; unified primary and middle-click pan above the $4\text{px}$ drag threshold; smooth fly-to circuit/beacon framing; 2x2 grid presentation for the telemetry verification matrix (`CMP-07`).

### 8.2. Industrial Tablet Landscape (`--dt-breakpoint-lg`)
* **Layout Organization:** Canvas `CMP-01` occupies the left workspace; LOTO Drawer `CMP-05` docks as a right-hand lateral panel sized by `--dt-layout-drawer-width-tablet`, strictly preserving $\ge 70\%$ canvas visibility per [DT-UI-DS-DOC-001 §2.4](../../DT-UI-DS-DOC-001.md#24-structural-layout-and-dimensional-tokens). Viewport toolbar `CMP-02` auto-centers over the viewable canvas area, with `CMP-13` anchored at bottom-left.
* **Ergonomic Rules:** Touch pan dead-zone threshold (§5.2); gloved touch targets governed by `--dt-touch-target-mobile`; drawer minimizes via chevron trigger (`>`) to an edge peek tab (`--dt-layout-bottom-sheet-peek-height`).

### 8.3. Industrial Tablet Portrait (`--dt-breakpoint-md`)
* **Layout Organization:** Canvas `CMP-01` occupies full viewport width; LOTO Drawer `CMP-05` operates as an adaptive **Bottom Sheet** (`--dt-radius-2xl` upper curvature) docked at the bottom edge, initializing at natural content height (`--dt-layout-bottom-sheet-height-initial`) with the capsule drag handle nested inside the drawer header, expandable up to `--dt-layout-bottom-sheet-height-expanded`.
* **Ergonomic Rules:** Drag handle gesture support with snap hysteresis (§5.2); mandatory discrete single-tap toggling between resting, expanded, and peek (`--dt-layout-bottom-sheet-peek-height`) states ([DT-UI-DS-DOC-001 §6.3](../../DT-UI-DS-DOC-001.md#63-sliding-containers-pattern-bottom-sheets-and-drawers)); sticky `CMP-09` interlock action bar (`--dt-layout-footer-height`) remains pinned at the bottom of `CMP-05`.

---

## 9. Traceability and Requirements Matrix

| Requirement | Addressed in Component | Verification & Implementation Mechanism |
| :--- | :--- | :--- |
| [FR-225](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr) | `CMP-01`, `CMP-05` | "LOTO Route" overlay renders energy paths over SVG plot plan upon request. |
| [FR-226](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr) | `CMP-01` | Energy lines dynamically styled based on live IoT telemetry (red energized, slate dashed isolated). |
| [FR-227](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr) | `CMP-04` | Cutoff points rendered with standardized industrial symbology (`#icon-loto-locked`, `#icon-loto-energized`). |
| [FR-228](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr) | `CMP-06` | Mandatory sequential checklist with strict order and physical Padlock Tag ID validation. |
| [FR-230](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr) | `CMP-08`, `CMP-09` | Start work control enables ONLY AFTER physical checklist completion, rich Try-Out attestation with signature hash, and corroborative telemetry zero state. |
| [FR-231](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr) | `CMP-08`, `CMP-09` | Audit trail logging of technician signature hash, padlock IDs, timestamps, and sensor telemetry snapshot upon start. |
| [FR-232](../../../requirements/user-stories/vis/VIS-011.md#functional-requirements-fr) | `CMP-01`, `CMP-09`, `CMP-12` | Continuous in-execution telemetry monitoring; automated server-side Work Order suspension to `SUSPENDED` and deployment of non-interactive passive evacuation beacon on re-energization breach. |
| [NFR-229](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | `CMP-09` | ACTIVE LOCK: interface disables work initiation on active energy; cannot be bypassed on client. |
| [NFR-233](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | `CMP-07` | Telemetry processing and UI update latency $< 1\text{s}$ via SignalR WebSocket stream. |
| [NFR-234](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | `CMP-09` | Fail-safe design: uncertain energy status assumes hazardous condition and maintains lock. |
| [NFR-235](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | `CMP-05`, `CMP-09` | Transactional synchronization via `ConfirmCutoffStepRequestDto` upon isolation confirmation under `SELECT ... FOR UPDATE NOWAIT` ([DT-ARQ-DB-DOC-001 §3.7](../../../architecture/DT-ARQ-DB-DOC-001.md#37-pessimistic-locking-vs-distributed-offline-leases-for-loto-isolation-vis-011-asr-002-adr-006)). |
| [NFR-236](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | `CMP-01` | Fluid SVG rendering $\ge 30\text{ FPS}$ on tablets, $\ge 60\text{ FPS}$ on desktop workstations. |
| [NFR-237](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | `CMP-07` | Out-of-range sensor readings trigger automated pessimistic hazardous energy lock. |
| [NFR-238](../../../requirements/user-stories/vis/VIS-011.md#non-functional-requirements-nfr) | `CMP-09`, `CMP-11` | Disconnectivity fail-safe: 2-second `LotoHeartbeatAck` watchdog with 30-second Grace Window locks `CMP-09` unless an unexpired Cryptographic Offline Lease ($\le 60$-minute max TTL on hardware monotonic clock) exists ([ADR-006](../../../architecture/adr/ADR-006.md), [DT-ARQ-DEP-DOC-001 §4](../../../architecture/views/DT-ARQ-DEP-DOC-001.md#4-perimeter-security-mechanism-loto-watchdog-fail-safe)). |
| [TR-001](../../../requirements/common/TR-001.md) | `CMP-08`, `CMP-09` | Immutable append-only audit trail logging of padlock tags, Try-Out signature hash, and sensor snapshot with SHA-256 hash chaining. |
| [TR-002](../../../requirements/common/TR-002.md) | `CMP-08`, `CMP-11` | Encrypts cached LOTO isolation plans, Cryptographic Offline Leases, and queued Try-Out attestations at rest in local device storage (`IOfflineStorage`). |
| [TR-005](../../../requirements/common/TR-005.md) | `CMP-01`, `CMP-07`, `CMP-12` | Enforces TLS/HTTPS and WSS encryption across all isolation command dispatches and real-time SignalR telemetry/evacuation streams. |
| [TR-006](../../../requirements/common/TR-006.md) | `CMP-08`, `CMP-09`, `CMP-11` | Enforces RBAC role authorization and hardware-keystore verification for Try-Out signing and offline safety lease validation. |
| [TR-007](../../../requirements/common/TR-007.md) | `CMP-05`, `CMP-06`, `CMP-08`, `CMP-11` | Offline Sync Outbox persists sequential padlock confirmations (`ConfirmCutoffStepRequestDto`), signed `TryOutAttestationDto`, and `StartWorkOrderExecutionCommand` using UUIDv7 idempotency keys during field disconnections. |
| [TR-010](../../../requirements/common/TR-010.md) | `CMP-01`, `CMP-07`, `CMP-09`, `CMP-11`, `CMP-12` | Persistent real-time SignalR streams on `/hubs/telemetry` (`ReceiveTelemetryReading`, **2s** `LotoHeartbeatAck` with **30s Grace Window**, `EmergencyEvacuationBroadcast`) and `/hubs/operations` (`PermitStatusChanged`, `WorkOrderStatusChanged`) with $< 1\text{s}$ latency and automatic disconnect fail-safe detection. |
| [TR-011](../../../requirements/common/TR-011.md) | `CMP-01`, `CMP-04`, `CMP-07`, `CMP-13` | ANSI/ISA-101 HPHMI: 90/10 grayscale baseline with focal island de-emphasis, MAI zero-energy scales, Teal confirmation tokens, and `--dt-touch-target-mobile` gloved ergonomics. |
| [ADR-006](../../../architecture/adr/ADR-006.md) | `CMP-08`, `CMP-09`, `CMP-11` | Cryptographic Offline Lease protocol (`POST /api/v1/safety/loto-plans/{workOrderId}/offline-lease`, bounded to 60-minute max TTL on hardware monotonic clock) for disconnected zero-energy field verification. |
| [ADR-007](../../../architecture/adr/ADR-007.md) | `CMP-06`, `CMP-08`, `CMP-09` | Mandatory `X-Idempotency-Key: {uuidv7}` header across `confirm`, `try-out`, `start-execution`, and `offline-lease` commands (online execution uses server-side `SELECT ... FOR UPDATE NOWAIT`; offline mode pairs with `CryptographicOfflineLeaseDto` per [DT-ARQ-DB-DOC-001 §3.7](../../../architecture/DT-ARQ-DB-DOC-001.md#37-pessimistic-locking-vs-distributed-offline-leases-for-loto-isolation-vis-011-asr-002-adr-006)). |
