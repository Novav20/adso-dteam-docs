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
version: 1
date: 2026-10-15
status: In Review
---

# SCR-MTTO-002: Mobile Work Order Execution, ISO 14224 Failure Coding, and Technical Closure

## 1. Purpose and Operational Context

* **View Objective:** Mobile field technical execution, taxonomy failure diagnosis, and formal technical closure of active Work Orders (ANSI/ISA-101 Level 4). Enforces strict ISO 14224 reliability coding (Maintainable Item, Failure Mode, Mechanism, Cause, Detection Method, Operational Condition, and Operational Impact), actual Wrench Time capture, immutable photographic evidence acquisition with SHA-256 cryptographic hashing ([TR-003](../../../requirements/common/TR-003.md)), and atomic status transition to `COMPLETE` ([DT-ERD-DOC-001 §3.2.6](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#326-work_orders)), with full offline-first resilience via encrypted local database ([TR-002](../../../requirements/common/TR-002.md)) and transactional outbox synchronization ([TR-007](../../../requirements/common/TR-007.md)).
* **Primary Target Persona:** Maintenance Technician (e.g., `TECH-4921 (J. Serrano)`) operating on rugged industrial tablets (`--dt-breakpoint-md`, `--dt-breakpoint-lg`) in Class I Div 2 hazardous process areas under adverse conditions (glare, noise, chemical-resistant gloves).
* **Secondary Personas:**
  * **Maintenance Supervisor:** Reviews field execution metrics, verifies Wrench Time variance, and performs administrative closure (`CLOSED`).
  * **Reliability Engineer:** Consumes structured ISO 14224 failure distributions for Weibull analysis, Bad Actor tracking, and MTBF/MTTR calculations.
  * **HSEQ Inspector:** Audits the cryptographic hash chain of field evidence and verifies de-isolation safety handover protocols.
* **Operational Context:** Deployed on portable industrial tablets and intrinsically safe handheld devices. Requires tactile targets $\ge 48\times 48\text{px}$, high-contrast typography, zero nested modal traps, and resilient persistence against unexpected power loss or radio-frequency shadowing inside tank dikes and pump battery limits.
* **Mode of Operation:** Transactional Execution & Field Technical Certification mode. Direct DCS/SCADA process control manipulation is strictly excluded; field mechanics log physical intervention data, parts consumption, and diagnostic classifications.
* **Upstream & Downstream Navigation Invariants:**
  * **Upstream Continuity:** Directly launched upon successful Zero Energy verification and work initiation in [SCR-VIS-011](../vis/SCR-VIS-011.md) (`WO-2026-0842`, `P-0101A`), automatically transitioning the Work Order lifecycle state to `IN_PROGRESS`.
  * **Downstream Transitions:** Hosts the trigger for the Rotable Asset Swap modal ([SCR-INV-025](../inv/SCR-INV-025.md)) when physical equipment replacement is required, and routes to the RIME Backlog Dashboard ([SCR-MTTO-026](./SCR-MTTO-026.md)) upon confirmed technical closure.

---

## 2. Visual Artifact

![SCR-MTTO-002 Wireframe](assets/SCR-MTTO-002-wireframe.svg)

> *Note: Vector wireframe illustrating the mobile execution header, 4-tier operational tab navigation, ISO 14224 multi-tier classification matrix, cryptographic evidence uploader, and the sticky bottom action bar with active ISO Lock.*

---

## 3. Functional Component Inventory

> The base layout, typography, and design tokens are inherited from [DT-UI-DS-DOC-001](../../DT-UI-DS-DOC-001.md) and [tokens.css](../../assets/tokens.css). This table defines the present components, semantic tokens, and their architectural roles. Detailed interaction rules, layout constraints, and geometric algorithms are strictly specified in Section 5.

| ID | Control / Component | Visual Role / Content | Semantic Token | Architectural Role & Reference |
| :--- | :--- | :--- | :--- | :--- |
| `CMP-01` | Mobile Execution Header | Work Order & Asset context strip | Surface: `--dt-color-surface-panel`<br>Border: `--dt-color-border-panel` | Anchored header displaying Work Order ID (`WO-2026-0842`), Target Equipment Unit (`P-0101A`), Functional Location (`TFA-CSS-P-0101A`), active LOTO safety badge (`[🔒 ZERO ENERGY CONFIRMED]`), and technician profile. Detailed in §5.1. |
| `CMP-02` | Operational Tabs Controller | 4-channel segmented tab bar | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle`<br>Active: `--dt-color-border-focus` | Top segmented navigation bar allowing instant switching between: `[1. Scope & Execution]`, `[2. Spares & Rotations]`, `[3. ISO 14224 Diagnosis]`, and `[4. Multimedia Evidence]`. Ergonomics and swipe physics in §5.2. |
| `CMP-03` | Scope & Checklist Panel | Step-by-step task checklist & labor timer | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle` | Displays planned task scope items with tactile completion checkboxes, actual start/finish timestamps, active Wrench Time stopwatch, and actual labor duration input (`actual_labor_hours` per [DT-ERD-DOC-001 §3.2.6](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#326-work_orders)). Rules in §5.3. |
| `CMP-04` | Materials & Spares Allocation Panel | Parts consumed & equipment rotation trigger | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle` | Lists reserved warehouse spare parts (e.g., mechanical seals, O-rings) with quantity consumed inputs. Hosts high-priority action trigger `[Rotate Dismounted Equipment]`, launching modal [SCR-INV-025](../inv/SCR-INV-025.md) when an asset swap is required. Specification in §5.3. |
| `CMP-05` | ISO 14224 Multi-Tier Taxonomy Matrix Card | 7-tier standardized failure coding matrix | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-panel`<br>Radius: `--dt-radius-md` | The core reliability data collection container. Enforces sequential multi-tier dropdowns strictly bound to [DT-ERD-DOC-001 §3.2.2](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#322-failure_records): Maintainable Item (`maintainable_item_id`), Failure Mode, Failure Mechanism, Failure Cause, Detection Method, Operational Condition, Operational Impact, and Downtime (`downtime`). Taxonomy logic in §5.3. |
| `CMP-06` | ISO 14224 Hard Lock Indicator | Quality gate completeness widget | Surface: `--dt-color-surface-raised`<br>Border: Dynamic (`--dt-color-alarm-warning` vs `--dt-color-state-success`) | Visual quality meter displaying taxonomic completeness ($0\%-100\%$). Employs redundant coding (symbol + text + contrast border) per WCAG 2.1 AA. Hard-disables finalization while any mandatory ISO field remains unclassified (`FR-012`). Logic in §5.3. |
| `CMP-07` | Cryptographic Evidence Capture Card | Tactical camera trigger & SHA-256 verifier | Surface: `--dt-color-surface-card`<br>Border: `--dt-color-border-subtle`<br>Hash: `--dt-font-family-mono` | Hosts hardware camera trigger button ($\ge 48\text{px}$), reactive thumbnail preview, file format validator (`JPG`, `PNG`, `PDF`), and asynchronous client-side SHA-256 hash calculator ([TR-003](../../../requirements/common/TR-003.md)). Automatically flags corrupt or unreadable files (`AF-003`). Protocol in §5.3. |
| `CMP-08` | Offline Outbox & Sync Banner | Connection & local queue health indicator | Surface: Dynamic (`--dt-color-surface-card` vs `rgba(245, 158, 11, 0.12)`)<br>Border: `--dt-color-alarm-warning` | Priority 4 diagnostic alert banner deployed automatically upon network loss (`AF-002`, [ASR-001](../../../architecture/asr/DT-ARQ-ASR-001.md)). Displays offline status, cached transaction count, and unencrypted-in-transit zero-leakage guarantee via SQLCipher ([TR-002](../../../requirements/common/TR-002.md)). Specification in §5.3. |
| `CMP-09` | Technical Finalization Action Bar | Sticky bottom closure controller | Surface: `--dt-color-surface-panel`<br>Elevation: `--dt-z-header-sticky` ($500$)<br>Button: Dynamic | Fixed bottom action container hosting the primary control `[Finalize Work Order]`. Hard-gated by the Boolean conjunction of `CMP-06` and `CMP-07`. Persists atomic transition to `COMPLETE` in `mtto.work_orders` and chains cryptographic audit log in `adm.audit_logs`. Execution rules in §5.3. |
| `CMP-10` | De-Isolation Safety Handover Strip | LOTO clearance acknowledgment strip | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle` | Safety acknowledgment strip reminding the technician that physical padlocks remain locked until formal de-isolation handover is executed prior to operational start-up. Detailed in §6. |on in §5.3. |
| `CMP-09` | Technical Finalization Action Bar | Sticky bottom closure controller | Surface: `--dt-color-surface-panel`<br>Elevation: `--dt-z-header-sticky` ($500$)<br>Button: Dynamic | Fixed bottom action container hosting the primary control `[Finalize Work Order]`. Hard-gated by the Boolean conjunction of `CMP-06` and `CMP-07`. Persists atomic transition to `COMPLETE` in `mtto.work_orders` and chains cryptographic audit log in `adm.audit_logs`. Execution rules in §5.3. |
| `CMP-10` | De-Isolation Safety Handover Strip | LOTO clearance acknowledgment strip | Surface: `--dt-color-surface-base`<br>Border: `--dt-color-border-subtle` | Safety acknowledgment strip reminding the technician that physical padlocks remain locked until formal de-isolation handover is executed prior to operational start-up. Detailed in §6. |

---

## 4. Screen State Matrix

| State | Visual Modification in the Interface | Activation Condition |
| :--- | :--- | :--- |
| **Normal / In Progress (Default)** | Header displays `IN_PROGRESS` in neutral blue/gray badge. Checklist editable. Wrench Time counter increments. Tab 3 shows incomplete taxonomy. `CMP-09` `[Finalize Work Order]` is hard-disabled (`disabled`, opacity 0.45). | Initial load of `SCR-MTTO-002` following work authorization from `SCR-VIS-011`. |
| **Loading / Synchronizing** | Skeleton shimmer on form fields and spares table (`--dt-color-surface-raised`). Taxonomy dropdowns show animated loading indicator while hydrating local SQLite cache. Controls locked. | Initial data hydration from local SQLCipher cache or background delta synchronization in progress. |
| **Taxonomy Incomplete / Missing Fields (AF-001)** | Missing mandatory taxonomy selectors highlighted with saturated amber borders (`--dt-color-alarm-warning`, $2\text{px}$) and warning icon `⚠️`. `CMP-06` displays completeness $< 100\%$ with message *"ISO 14224 Lock Active"*. `CMP-09` remains disabled. | Technician attempts to finalize or navigates away while any of the 7 mandatory ISO fields or downtime is empty. |
| **Evidence Capturing & Hashing** | Camera viewfinder overlay active or file upload progress bar visible. SHA-256 calculation shows animated pulsing badge *"Computing Hash..."* in monospace font. | Technician captures or selects photo evidence in `CMP-07`. |
| **Evidence Corrupt / Hash Mismatch (AF-003)** | File preview replaced by critical red border (`--dt-color-alarm-critical`) and error icon `🚫`. Banner displays: *"File integrity error. SHA-256 mismatch detected. Please recapture evidence"*. Form progression blocked. | Cryptographic verification detects corrupted binary stream or zero-byte payload (`TR-003-NFR-380`). |
| **Offline Mode (AF-002)** | Persistent amber diagnostic banner `CMP-08` pinned below header: *"[⚡ OFFLINE MODE] Local SQLCipher cache active. 1 transaction pending sync"*. Zero process alarm red used. | Device loses Wi-Fi/cellular connectivity in field process areas (`ASR-001`). |
| **Ready to Finalize (Unlocked)** | `CMP-06` badge transitions to solid Teal `[100% ISO COMPLIANT]`. Evidence thumbnail displays validated SHA-256 hash stamp. Action button `CMP-09` unlocks in solid Teal (`--dt-color-state-success`). | All 7 ISO 14224 fields selected + Downtime specified + Photo evidence captured with valid hash + Checklist attested. |
| **Technical Closure Complete** | Form transitions to read-only state. Header badge updates to `COMPLETE`. Full-screen non-disruptive success banner: *"Work Order WO-2026-0842 technically completed. Handed over for supervisory review"*. | Technician confirms `[Finalize Work Order]`. System commits atomic transaction. |

---

## 5. Interaction Rules and Data Flow (Single Source of Truth - SSoT)

### 5.1. Initial Load & Lifecycle

1. **Context Ingestion Contract:**
   * When navigated from [SCR-VIS-011](../vis/SCR-VIS-011.md), the route receives the validated parameter payload:
     $$\mathcal{P}_{\text{init}} = \langle \text{WorkOrderId}: \text{"WO-2026-0842"}, \text{EquipId}: \text{"P-0101A"}, \text{FuncLoc}: \text{"TFA-CSS-P-0101A"}, \text{TechId}: \text{"TECH-4921"}, \text{LotoStatus}: \text{"VERIFIED\_ZERO\_ENERGY"} \rangle$$
   * If `mtto.work_orders.current_status == 'SCHEDULED'`, the client immediately emits an atomic transition event to `IN_PROGRESS`, logging `actual_start = clock_timestamp()` and creating an audit record in `mtto.work_order_histories` (`old_status = 'SCHEDULED'`, `new_status = 'IN_PROGRESS'`).
2. **Local Cache Pre-Hydration (Offline Readiness):**
   * Pre-hydrates the ISO 14224 taxonomic tables (`tax.maintainable_items`, equipment class failure modes) from the local SQLite/SQLCipher encrypted database ([TR-002](../../../requirements/common/TR-002.md)), guaranteeing zero network latency when populating dropdowns in field dead-zones.

### 5.2. Mobile Ergonomics & Tactile Mechanics

1. **Gloved Touch Target Invariant (ISO 9241-110 Clause 5.3 / `--dt-touch-target-mobile`):**
   * All interactive controls (checkboxes, dropdown triggers, camera buttons, tab headers) enforce a minimal bounding box of $48\times 48\text{px}$ with $\ge 8\text{px}$ separation, ensuring error-free operation with nitrile and leather field gloves.
2. **Sticky Bottom Finalization Bar (`CMP-09`):**
   * Pinned to the bottom viewport boundary (`bottom: 0; position: fixed; z-index: var(--dt-z-header-sticky, 500); height: 72px;`), elevated via border-top `$1.5\text{px}$ solid var(--dt-color-border-panel)`.
   * Form content container enforces `padding-bottom: 96px` to prevent the sticky footer from occluding input fields or notes at maximal scroll extents.
3. **Tab Navigation Physics (`CMP-02`):**
   * Segmented bar with discrete horizontal sliding indicator. Supports horizontal touch swipe gestures with a $40\text{px}$ displacement threshold to switch between tabs without causing accidental vertical scroll disruption.

### 5.3. Domain Workflows, Taxonomy Enums, and Cryptographic Mutation

1. **ISO 14224 Multi-Tier Taxonomy Matrix (`CMP-05`):**
   * Failure classification is strictly constrained by the relational contracts defined in [DT-ERD-DOC-001 §3.2.2](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#322-failure_records) (`mtto.failure_records`):
     * **Tier 1: Maintainable Item (`maintainable_item_id`):** Filtered dynamically by the target equipment class (e.g., for Centrifugal Pump `P-0101A` per API 610: *Mechanical Seal*, *Impeller*, *Bearings*, *Shaft*, *Casing*, *Coupling*).
     * **Tier 2: Failure Mode (`failure_mode`):** Constrained by Maintainable Item (e.g., for Mechanical Seal: *External Leakage (EL)*, *Vibration Excursion (VE)*, *Overheating (OH)*).
     * **Tier 3: Failure Mechanism (`failure_mechanism`):** Observable physical degradation (e.g., *Mechanical Wear*, *Abrasive Erosion*, *Thermal Fatigue*, *Elastomer Degradation*).
     * **Tier 4: Failure Cause (`failure_cause`):** Root engineering origin (e.g., *Lubrication Deficiency*, *Shaft Misalignment*, *Cavitation Erosion*, *Operational Off-Design*).
     * **Tier 5: Detection Method (`detection_method`):** Strictly restricted by `ck_failure_records_detection_method` in `DT-ERD-DOC-001.md`:
       $$\text{detection\_method} \in \{\text{'PERIODIC\_MAINTENANCE'}, \text{'FUNCTIONAL\_TESTING'}, \text{'INSPECTION'}, \text{'PERIODIC\_CBM'}, \text{'PRESSURE\_TESTING'}, \text{'CONTINUOUS\_CBM'}, \text{'PRODUCTION\_INTERFERENCE'}, \text{'CASUAL\_OBSERVATION'}, \text{'CORRECTIVE\_MAINTENANCE'}, \text{'ON\_DEMAND'}, \text{'OTHER'}\}$$
     * **Tier 6: Operational Condition (`operational_condition`):** Strictly restricted by `ck_failure_records_operational_condition` in `DT-ERD-DOC-001.md`:
       $$\text{operational\_condition} \in \{\text{'RUNNING'}, \text{'START\_UP'}, \text{'RUN\_DOWN'}, \text{'HOT\_STANDBY'}, \text{'COLD\_STANDBY'}, \text{'IDLE'}, \text{'TESTING'}\}$$
     * **Tier 7: Operational Impact (`operational_impact`):** Strictly restricted by `ck_failure_records_operational_impact` in `DT-ERD-DOC-001.md`:
       $$\text{operational\_impact} \in \{\text{'EXTENSIVE\_STOP'}, \text{'STOP\_ABOVE\_ACCEPTABLE'}, \text{'STOP\_BELOW\_ACCEPTABLE'}, \text{'STOP\_MINOR'}\}$$
     * **Quantitative Metric: Downtime (`downtime`):** Numeric field `DECIMAL(10,2) NOT NULL` recording hours of lost operational availability.

2. **The ISO 14224 Hard Lock Formula (`CMP-06`, `FR-012`):**
   * The primary action button `CMP-09` `[Finalize Work Order]` is governed by the asymmetric Boolean lock:
     $$\text{CanFinalize} = \mathcal{T}_{\text{complete}} \land \mathcal{E}_{\text{valid}} \land \mathcal{W}_{\text{valid}}$$
     where:
     $$\mathcal{T}_{\text{complete}} = (\text{Item} \ne \varnothing) \land (\text{Mode} \ne \varnothing) \land (\text{Mech} \ne \varnothing) \land (\text{Cause} \ne \varnothing) \land (\text{Method} \ne \varnothing) \land (\text{Condition} \ne \varnothing) \land (\text{Impact} \ne \varnothing) \land (\text{Downtime} \ge 0.0)$$
     $$\mathcal{E}_{\text{valid}} = (\text{MediaAttachmentCount} \ge 1) \land (\text{SHA256HashVerified} == \text{true})$$
     $$\mathcal{W}_{\text{valid}} = (\text{ActualLaborHours} > 0.0) \land (\text{AllChecklistItemsChecked} == \text{true})$$
   * Any false term renders the button `disabled` with visual error flags on omitted fields (`AF-001`).

3. **Cryptographic Multimedia Evidence Pipeline (`CMP-07`, `TR-003`):**
   * Capturing a photograph via device camera triggers local asynchronous processing:
     1. Downsamples image to maximum $1920\times 1080$ resolution in JPEG format (quality 0.85) to optimize storage.
     2. Generates an instant thumbnail ($120\times 120\text{px}$) rendered in the UI preview slot.
     3. Computes the cryptographic checksum using the HTML5 Web Crypto API:
        $$\text{hash} = \text{SubtleCrypto.digest}(\text{"SHA-256"}, \text{ArrayBuffer})$$
     4. Stores file metadata in `mtto.media_attachments`: `file_url`, `file_type = 'JPG'`, `uploaded_at = clock_timestamp()`, and links `failure_record_id`.
     5. If file reading throws an I/O error or hash evaluation fails, the UI enters state `Evidence Corrupt` (`AF-003`), halts finalization, and forces recapture.

4. **Atomic Technical Closure Mutation & Audit Chaining (`CMP-09`, `TR-001`):**
   * Upon pressing `[Finalize Work Order]`, the application dispatches an atomic technical closure command (`SubmitTechnicalClosureCommand`) against the backend API endpoint `POST /api/v1/work-orders/{id}/technical-closure`.
   * The backend processes the closure within a single atomic database transaction governed by the physical integrity invariants of [DT-ARQ-DB-DOC-001 §2](../../../architecture/DT-ARQ-DB-DOC-001.md#2-physical-integrity-invariants-and-constraints):
     * **Step 1 (Failure Diagnosis):** Inserts diagnosis record into `mtto.failure_records` adhering to the relational constraints in [DT-ERD-DOC-001 §3.2.2](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#322-failure_records).
     * **Step 2 (Work Order Lifecycle Transition):** Updates `mtto.work_orders` (`current_status = 'COMPLETE'`, `actual_finish = clock_timestamp()`, `actual_labor_hours = :hours`) per [DT-ERD-DOC-001 §3.2.6](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#326-work_orders).
     * **Step 3 (Lifecycle Audit Record):** Appends state history record into `mtto.work_order_histories` (`old_status = 'IN_PROGRESS'`, `new_status = 'COMPLETE'`) per [DT-ERD-DOC-001 §3.2.5](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#325-work_order_histories).
     * **Step 4 (Cryptographic Audit Chaining):** Appends immutable audit entry into `adm.audit_logs` calculating cryptographic SHA-256 chain integrity per [DT-ERD-DOC-001 §3.5.1](../../../domain-models/entity-relationship/DT-ERD-DOC-001.md#351-audit_logs) and [DT-ARQ-DB-DOC-001 §3.8](../../../architecture/DT-ARQ-DB-DOC-001.md#38-gin-indexing-for-jsonb-immutable-audit-adm-032).

5. **Offline Operation Protocol (`AF-002`, `TR-002`, `TR-007`, `ADR-007`):**
   * If network connection is lost (`navigator.onLine == false` or heartbeat timeout):
     1. Banner `CMP-08` illuminates in amber warning tone (`rgba(245, 158, 11, 0.12)`).
     2. The full atomic transaction payload is serialized into JSON and written to the encrypted local SQLite table `offline_outbox` protected by SQLCipher (AES-256-CBC).
     3. Assigns a unique `idempotency_key` (UUIDv7) per `ADR-007`.
     4. Marks the local UI view as `COMPLETE (Pending Sync)`.
     5. Background synchronization worker monitors connectivity; upon restoration, drains the outbox queue via idempotent `POST /api/v1/work-orders/WO-2026-0842/technical-closure` with `X-Idempotency-Key` header.

6. **Rotable Asset Swap Branching (`CMP-04`):**
   * If the physical repair requires unmounting the pump unit, tapping `[Rotate Dismounted Equipment]` preserves the in-flight form draft in local memory and deploys the modal [SCR-INV-025](../inv/SCR-INV-025.md). Upon completing the asset swap, `SCR-INV-025` returns the new mounted equipment serial number (`P-0101B`) and stamps the replacement reference into `technician_notes`.

---

## 6. Industrial and Safety Considerations

* **High-Performance HMI (ANSI/ISA-101 / [TR-011](../../../requirements/common/TR-011.md)):**
  * Grayscale visual discipline: $90\%$ of the screen utilizes neutral dark slate tones (`--dt-color-surface-base`, `--dt-color-surface-card`, `--dt-color-border-subtle`).
  * Saturated amber (`--dt-color-alarm-warning`) is reserved exclusively for the offline diagnostic banner and missing taxonomy flags.
  * Saturated red (`--dt-color-alarm-critical`) is reserved strictly for corrupt file integrity errors or process safety emergency breaches. Green is never used for generic "active" status, only for verified completion gates (`--dt-color-state-success`).
* **Diagnostic (Priority 4) vs. Process Alarm Segregation:**
  * Network disconnection banner (`CMP-08`) is styled strictly as a Priority 4 Diagnostic indicator with muted borders and informational icons. It is strictly prohibited from masquerading as a high-priority process emergency.
* **De-Isolation / De-LOTO Safety Handover Protocol:**
  * Technical closure (`COMPLETE`) of the Work Order does **NOT** equate to plant re-energization.
  * Banner `CMP-10` explicitly enforces the safety invariant:
    > *"CAUTION: Hazardous energy isolations established in SCR-VIS-011 remain locked. Physical padlock removal and de-isolation must be executed via formal Operations Handover prior to commissioning."*

---

## 7. Frontend Component Contract (Blazor / Razor)

### 7.1. Component Hierarchy & File Mapping

```text
Pages/
└── MobileWorkOrderClosingPage.razor                 # Root View (SCR-MTTO-002)
    ├── ExecutionHeader.razor                        # CMP-01: Work Order & Asset context header
    ├── OperationalTabsBar.razor                     # CMP-02: 4-channel tab selector
    ├── ScopeExecutionTab.razor                      # CMP-03: Checklist & Wrench Time timer
    ├── SparesAllocationTab.razor                    # CMP-04: Spares logging & Asset Swap trigger
    ├── IsoTaxonomyDiagnosisTab.razor                # CMP-05: 7-tier ISO 14224 dropdown matrix
    │   └── IsoComplianceLockBadge.razor             # CMP-06: Quality gate meter & alert
    ├── MultimediaEvidenceTab.razor                  # CMP-07: Camera capture & SHA-256 verifier
    ├── OfflineOutboxBanner.razor                    # CMP-08: Diagnostic connectivity banner
    ├── TechnicalFinalizeBar.razor                   # CMP-09: Sticky bottom action bar
    └── DeIsolationHandoverStrip.razor               # CMP-10: LOTO safety acknowledgment strip
```

### 7.2. Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)

#### 7.2.1. `MobileWorkOrderClosingPage.razor` (Root View)

```csharp
public partial class MobileWorkOrderClosingPage : ComponentBase
{
    [Parameter]
    public required Guid WorkOrderId { get; set; }

    [Parameter, SupplyParameterFromQuery]
    public string? ReturnUrl { get; set; }

    private WorkOrderClosingContextDto? Context { get; set; }
    private FailureRecordInputDto FailureInput { get; set; } = new();
    private List<MediaAttachmentDto> Attachments { get; set; } = [];
    private bool IsOffline { get; set; }
    private bool IsIsoLockActive => !FailureInput.IsValidIso14224(Attachments.Count);
}
```

#### 7.2.2. Subcomponent Parameters

```csharp
public partial class IsoTaxonomyDiagnosisTab : ComponentBase
{
    [Parameter, EditorRequired]
    public required FailureRecordInputDto Model { get; set; }

    [Parameter, EditorRequired]
    public required EventCallback<FailureRecordInputDto> ModelChanged { get; set; }

    [Parameter, EditorRequired]
    public required Guid EquipmentClassId { get; set; }

    [Parameter]
    public bool IsReadOnly { get; set; }
}

public partial class TechnicalFinalizeBar : ComponentBase
{
    [Parameter, EditorRequired]
    public bool CanFinalize { get; set; }

    [Parameter, EditorRequired]
    public EventCallback OnFinalizeTriggered { get; set; }

    [Parameter]
    public bool IsSubmitting { get; set; }
}
```

#### 7.2.3. Data Transfer Objects (DTOs)

```csharp
public record WorkOrderClosingContextDto
{
    public required Guid WorkOrderId { get; init; }
    public required string WorkOrderNumber { get; init; } // e.g. "WO-2026-0842"
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
    public string? DetectionMethod { get; set; } // Enforced by ck_failure_records_detection_method
    public string? OperationalCondition { get; set; } // ck_failure_records_operational_condition
    public string? OperationalImpact { get; set; } // ck_failure_records_operational_impact
    public decimal DowntimeHours { get; set; }
    public string? TechnicianNotes { get; set; }

    public bool IsValidIso14224(int attachmentCount) =>
        MaintainableItemId.HasValue &&
        !string.IsNullOrWhiteSpace(FailureMode) &&
        !string.IsNullOrWhiteSpace(FailureMechanism) &&
        !string.IsNullOrWhiteSpace(FailureCause) &&
        !string.IsNullOrWhiteSpace(DetectionMethod) &&
        !string.IsNullOrWhiteSpace(OperationalCondition) &&
        !string.IsNullOrWhiteSpace(OperationalImpact) &&
        DowntimeHours >= 0.0m &&
        attachmentCount >= 1;
}

public record MediaAttachmentDto
{
    public required Guid Id { get; init; }
    public required string FileUrl { get; init; }
    public required string FileType { get; init; } // "JPG", "PNG", "PDF"
    public required string IntegrityHashSha256 { get; init; }
    public required DateTime UploadedAt { get; init; }
}
```

### 7.3. Client-Side DOM & Interop Bridge

1. **Hardware Camera & Image Compression Interop (`cameraInterop.js`):**
   * Uses HTML5 MediaDevices API (`navigator.mediaDevices.getUserMedia`) with fallback to standard `<input type="file" accept="image/*" capture="environment">`.
   * Downsamples and compresses bitmaps via OffscreenCanvas to guarantee file sizes $< 1.5\text{MB}$ prior to local persistence.
2. **Web Crypto SHA-256 Hashing Bridge (`cryptoInterop.js`):**
   * Computes the SHA-256 hash asynchronously via `crypto.subtle.digest('SHA-256', buffer)` in a dedicated Web Worker to prevent UI thread stuttering or frame drops on industrial tablets.
3. **Encrypted SQLite / SQLCipher Interop:**
   * Interfaces with client-side relational storage (`sqlite-net-pcl` + `SQLCipher`) for immediate transactional outbox queuing during offline partitions (`TR-002`, `TR-007`).

---

## 8. Layout and Responsive Adaptability

| Viewport / Breakpoint | Layout Organization | Ergonomic Rules |
| :--- | :--- | :--- |
| **Desktop Workstation**<br>($\ge 1400\text{px}$, `--dt-breakpoint-xl`) | Dual-column side-by-side layout ($50\% / 50\%$). Left: Scope, Spares, and Multimedia. Right: Full ISO 14224 Taxonomy Matrix and audit logs. Sticky footer spans bottom width. | Mouse click focus; keyboard numeric navigation; dense multi-tier dropdown grids; full-resolution image preview modal. |
| **Industrial Tablet Landscape**<br>($901\text{px} - 1399\text{px}$, `--dt-breakpoint-lg`) | Asymmetric dual-column layout ($45\% / 55\%$). Segmented tab bar `CMP-02` allows grouped inspection. Sticky footer `CMP-09` pinned at bottom. | Gloved touch targets $\ge 48\times 48\text{px}$; scrollable taxonomy matrix; camera trigger anchored for dual-thumb reachability. |
| **Industrial Tablet Portrait**<br>($600\text{px} - 900\text{px}$, `--dt-breakpoint-md`) | Single-column stacked layout. Segmented tab bar `CMP-02` hosts swipeable tab views. Form items span full width ($100\%$). Action bar `CMP-09` sticky at bottom ($72\text{px}$). | Large touch input fields; single-hand thumb navigation; sticky ISO lock completeness meter pinned above action button. |

---

## 9. Traceability and Requirements Matrix

| Requirement | Addressed in Component | Verification & Implementation Mechanism |
| :--- | :--- | :--- |
| [FR-010](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-03`, `CMP-09` | Registration of actual labor duration (`actual_labor_hours`) and Wrench Time tracking from mobile interface. |
| [FR-011](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-05` | Mandatory 7-tier classification strictly using ISO 14224 taxonomy tables (`tax.maintainable_items`, `mtto.failure_records`). |
| [FR-012](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-06`, `CMP-09` | **ISO 14224 Hard Lock:** Hard-disables finalization button until all mandatory taxonomy fields and downtime are complete. |
| [FR-013](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-07` | Multimedia photographic attachment capture, preview thumbnail generation, and persistent linkage to `mtto.media_attachments`. |
| [FR-014](../../../requirements/user-stories/mtto/MTTO-002.md#functional-requirements-fr) | `CMP-09` | Atomic transition of Work Order state to `COMPLETE` in `mtto.work_orders` and dispatch of event notification to Reliability Engineer. |
| [NFR-015](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr) | `CMP-08`, `CMP-09` | Offline-First persistence using encrypted SQLCipher local database with crash-resilient write-ahead logging (WAL). |
| [NFR-016](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr) | `CMP-02`, `CMP-05` | Mobile response latency $< 2\text{s}$ achieved via pre-hydrated local taxonomy caches and Web Worker SHA-256 hashing. |
| [NFR-017](../../../requirements/user-stories/mtto/MTTO-002.md#non-functional-requirements-nfr) | `CMP-01` to `CMP-10` | Cross-platform mobile suitability on Android industrial tablets and iOS/Windows devices via responsive CSS tokens. |
| [TR-001](../../../requirements/common/TR-001.md) | `CMP-09` | Append-only immutable audit trail logging in `adm.audit_logs` with SHA-256 hash chaining upon Work Order finalization. |
| [TR-002](../../../requirements/common/TR-002.md) | `CMP-08` | Local database encryption at rest using AES-256 (SQLCipher) for all cached work order and failure records. |
| [TR-003](../../../requirements/common/TR-003.md) | `CMP-07` | Client-side cryptographic SHA-256 hash evaluation of all uploaded media files stored in metadata for tamper detection. |
| [TR-006](../../../requirements/common/TR-006.md) | `CMP-01` | Device authorization and authenticated technician session validation (`TECH-4921`). |
| [TR-007](../../../requirements/common/TR-007.md) | `CMP-08` | Transactional Offline Sync Outbox: Queues completed technical closures during disconnected operation with idempotent sync. |
| [TR-010](../../../requirements/common/TR-010.md) | `CMP-01`, `CMP-08` | Real-time synchronization via WebSockets/SignalR for telemetry connection health and outbox reconciliation. |
| **ISO 9241-110** | `CMP-02`, `CMP-07`, `CMP-09` | Gloved touch targets $\ge 48\times 48\text{px}$ with $\ge 8\text{px}$ separation complying with industrial ergonomics (`--dt-touch-target-mobile`). |
| [TR-011](../../../requirements/common/TR-011.md) | `CMP-01` to `CMP-10` | ANSI/ISA-101 HPHMI: 90% neutral grayscale palette; saturated amber reserved for offline banner and missing fields; saturated red reserved for file corruption. |
| [ADR-006](../../../architecture/adr/ADR-006.md) | `CMP-01`, `CMP-08` | Integration with Cryptographic Offline Lease protocol for disconnected field operations. |
| [ADR-007](../../../architecture/adr/ADR-007.md) | `CMP-08`, `CMP-09` | Idempotency token generation (UUIDv7) attached to technical closure payloads to prevent duplicate commits. |
