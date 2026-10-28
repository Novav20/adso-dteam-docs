# DTEAM: Product Engineering Roadmap & Technical Tasks

This file is the Single Source of Truth (SSoT) for engineering deliverables, architectural tasks, and implementation milestones for the DTEAM system (Asset Performance Management / Digital Twin).

All documentation and specifications referenced here reside in `adso-dteam-docs/` and are authored strictly in **100% Technical English**.

---

## 📌 Phase 1: Spatial UI/UX & HMI Viewports (Desktop & Mobile)

### Core Spatial & Supervisory Viewports (Digital Twin HMI)
- [x] **SCR-VIS-033: Level 3 Equipment Task Faceplate**
  - [x] Responsive layout on Desktop ($1440\times 900$) and Industrial Tablet Portrait ($800\times 1280$).
  - [x] Touch physics: upward drag height retention, snap hysteresis, and docked $36\text{px}$ peek tab.
  - [x] Canonical specification finalized: [`SCR-VIS-033.md`](ui-ux/screens/vis/SCR-VIS-033.md) (Stable).

- [x] **SCR-VIS-008: Level 1 General Plant Map with SIMOPS Layer**
  - [x] Redundant coding for PTW pins (Color + Geometry + Icon + Label per ANSI/ISA-101).
  - [x] Contextual popovers with viewport boundary clamping.
  - [x] Canonical specification finalized: [`SCR-VIS-008.md`](ui-ux/screens/vis/SCR-VIS-008.md) (Stable).

- [x] **SCR-VIS-011: LOTO Isolation Boundary Matrix**
  - [x] Cognitive Task Analysis (CTA): Physical Try-Out attestation primacy and negative interlock logic.
  - [x] Canonical specification finalized: [`SCR-VIS-011.md`](ui-ux/screens/vis/SCR-VIS-011.md) (Stable).

### Maintenance Management Screens (MTTO)
- [x] **SCR-MTTO-002: Work Order Technical Closure**
  - [x] Multi-evidence array ($1 : 0..N$), SHA-256 tamper verification, and discrete ISO 14224 mini-bars.
  - [x] Canonical specification finalized: [`SCR-MTTO-002.md`](ui-ux/screens/mtto/SCR-MTTO-002.md) (v1.1 Stable).

- [x] **SCR-MTTO-026: RIME Backlog Prioritization Dashboard**
  - [x] 1–100 RIME criticality matrix scoring and batching recommendation.
  - [x] Audit data pertinence, finalize desktop prototype review, capture high-res screenshot, and promote to Stable.
  - [x] Canonical specification finalized: [`SCR-MTTO-026.md`](ui-ux/screens/mtto/SCR-MTTO-026.md) (v1.2 Stable).

- [ ] **SCR-MTTO-001: Calendar-Based Maintenance Scheduling**
  - [ ] Cascading taxonomy selector (L6 $\to$ L7 $\to$ L8) and battery limit validation.
  - [ ] Complete canonical specification review, run deterministic audit, and promote to Stable: [`SCR-MTTO-001.md`](ui-ux/screens/mtto/SCR-MTTO-001.md) (DRAFT).

- [ ] **SCR-MTTO-023: Condition / Telemetry-Based Maintenance**
  - [ ] Telemetry variable binding, threshold calculations, and monotonic counter rules.
  - [ ] Complete canonical specification review, run deterministic audit, and promote to Stable: [`SCR-MTTO-023.md`](ui-ux/screens/mtto/SCR-MTTO-023.md) (DRAFT).

- [ ] **SCR-MTTO-029: Asset Boundary Limits Card (Battery Limits)**
  - [ ] Draft canonical specification with engineering limits, cost boundaries, and spatial anchoring per ISO 14224: [`SCR-MTTO-029.md`](ui-ux/screens/mtto/SCR-MTTO-029.md).
  - [ ] Execute Tier 0/1 UI audit and persist report.

### Inventory & Asset Master Data Screens (INV)
- [x] **SCR-INV-025: Rotable Asset Swap (Pauli Principle)**
  - [x] Field modal / drawer for atomic 1:1 rotable equipment exchange.
  - [x] Canonical specification finalized: [`SCR-INV-025.md`](ui-ux/screens/inv/SCR-INV-025.md) (v1.4 Stable).

- [x] **SCR-INV-005: Equipment Master Data Card (Technical Data Sheet)**
  - [x] Pre-flight Use Case Audit and CAP execution: [`UC-INV-005.md`](domain-models/use-cases/inv/UC-INV-005.md) (v1.1 Stable / PASSED).
  - [x] Canonical specification finalized: [`SCR-INV-005.md`](ui-ux/screens/inv/SCR-INV-005.md) (v1.1 Stable).
  - [x] Execute Tier 0/1/2 UI audit, capture 1080p screenshot, and persist report (`PASSED`).
  - [x] Modernize visual ergonomics & tablet landscape responsiveness, extract shared [`portal-shell.css`](ui-ux/assets/portal-shell.css), and update high-res visual artifact.

- [ ] **SCR-INV-027: Functional Locations Hierarchy Tree**
  - [ ] Draft canonical specification for ISO 14224 Level 1 to Level 5 navigation tree: [`SCR-INV-027.md`](ui-ux/screens/inv/SCR-INV-027.md).
  - [ ] Execute Tier 0/1 UI audit and persist report.

- [ ] **SCR-INV-031: Spare Parts Master Catalog**
  - [ ] Draft canonical specification for spare parts inventory, stock policies, and interchangeability: [`SCR-INV-031.md`](ui-ux/screens/inv/SCR-INV-031.md).
  - [ ] Execute Tier 0/1 UI audit and persist report.

- [ ] **SCR-INV-006: Movements and Kardex History**
  - [ ] Draft canonical specification for transactional spare parts ledger and equipment movement history: [`SCR-INV-006.md`](ui-ux/screens/inv/SCR-INV-006.md).
  - [ ] Execute Tier 0/1 UI audit and persist report.

### Administration & Security Screens (ADM)
- [ ] **SCR-ADM-013: Roles and Permissions Matrix (RBAC)**
  - [ ] Draft canonical specification for role privileges, segregation of duties, and security matrix: [`SCR-ADM-013.md`](ui-ux/screens/adm/SCR-ADM-013.md).
  - [ ] Execute Tier 0/1 UI audit and persist report.

- [ ] **SCR-ADM-014: User Lifecycle Management & Security Lockout**
  - [ ] Draft canonical specification for credential management, lockout states, and role assignments: [`SCR-ADM-014.md`](ui-ux/screens/adm/SCR-ADM-014.md).
  - [ ] Execute Tier 0/1 UI audit and persist report.

- [ ] **SCR-ADM-032: Immutable Audit Log Viewer**
  - [ ] Draft canonical specification for SHA-256 chained transaction logs and tamper verification: [`SCR-ADM-032.md`](ui-ux/screens/adm/SCR-ADM-032.md).
  - [ ] Execute Tier 0/1 UI audit and persist report.

### Architectural Viewport Shell & Cross-Cutting Gates (Deferred until Screen Specs are Stable)
- [ ] **Unified Spatial Application Shell (Single-Canvas Workspace)**
  - [ ] Formalize single-canvas viewport contract across `SCR-VIS-008`, `SCR-VIS-033`, and `SCR-VIS-011` (drawer/overlay activation vs. standard browser page navigation).
  - [ ] Evaluate focal spatial hierarchy / semantic zoom culling (Focal Island De-emphasis at L2/L3 thresholds).

- [ ] **Vector Iconography Fill & Stroke Dynamic Contrast Audit (Deferred)**
  - [ ] Audit filled vector paths (e.g., gear and package symbols) for contrast across dark/light themes.

---

## 📌 Phase 2: Ingestion Contracts & Digital Twin Spatial Tooling

- [x] **DT-UI-SVG-DOC-001: SVG Ingestion Contract (Rev 2.0 Approved)**
  - [x] Normative 7-layer standard (`L-CIVL-BOTM`, `L-MECH-EQPM`, `L-PIPE-PROC`, `L-INSP-INST`, `L-FIRE-PROT`, `L-ELEC-HAZ`, `L-ANNO-TEXT`).
  - [x] ISO 14224 binding attributes (`data-func-loc`, `data-equip-id`, `data-status`).
  - [x] MOC audit header metadata (`data-moc-id`, `data-rev-number`, `data-checksum-sha256`).

- [x] **Universal Markdown Relative Links Migration**
  - [x] 100% universal Markdown relative links across all specifications and architectural docs.
  - [x] Automated link and anchor auditor: [`scripts/verify_markdown_links.py`](scripts/verify_markdown_links.py).

- [x] **Parametric Plot Plan Generator (`scripts/plot_plan_generator/`)**
  - [x] Modular Python CLI package with NFPA 30 / API 650 process safety geometry and theme token injection (`themes.json`).

- [ ] **Tabular Master Data Ingestion Contract (SaaS Onboarding)**
  - [ ] Author formal ingestion specification: `DT-DATA-INGEST-DOC-001.md`.
  - [ ] Structured CSV template for ISO 14224 hierarchy (L1 to L8) in `requirements/data/asset_onboarding_template.csv`.
  - [ ] Backend validation rules (parent node resolution, tag uniqueness, catalog mapping for `EquipmentClass` and `Subunit`).

---

## 📌 Phase 3: Data Architecture & Domain Model

- [x] **Try-Out Attestation & Verification Methods in ERD/DM**
  - [x] Relational schema extension in [`DT-ERD-DOC-001.md`](domain-models/entity-relationship/DT-ERD-DOC-001.md) (`vis.work_order_isolations`).
  - [x] Domain model alignment in [`DT-DM-DOC-001.md`](domain-models/class/DT-DM-DOC-001.md) and [`DT-DM-DOC-002.md`](domain-models/class/DT-DM-DOC-002.md).
  - [x] DDL script compilation via [`scripts/generate_ddl.py`](scripts/generate_ddl.py).

- [ ] **MOC Layout Revision Entity (`vis.plant_layout_revisions`)**
  - [ ] Add relational entity to `DT-ERD-DOC-001.md`: UUIDv7, FK to Level 4 Functional Location, revision code, Blob Storage URI, SHA-256 checksum, lifecycle status (`DRAFT`, `ACTIVE`, `SUPERSEDED`), and approver ID.
  - [ ] Document MOC audit trail for spatial additions/deletions.

- [ ] **C4 Component Model Update (`DT-ARQ-CMP-DOC-001.md`)**
  - [ ] Formalize spatial ingestion port (`ISpatialIngestionService` / `SpatialIngestionWorker`).

---

## 📌 Phase 4: Frontend Implementation (.NET 10 / C# 14 / Blazor Hybrid)

- [ ] **Pre-Phase 4 Architectural Governance Gate**
  - [ ] Implement master repository verifier script: `scripts/verify_all.py`.
  - [ ] Codify Offline-First & Outbox guard skill: `.agents/skills/dteam-offline-sync-guard/` ([ADR-006](architecture/adr/ADR-006.md)).
  - [ ] Build automated C# SSoT contract verifier (`verify_csharp_contracts.py` / ArchUnitNET).
  - [ ] Execute `.NET 10 MAUI Blazor Hybrid + SQLCipher` Walking Skeleton spike.

- [ ] **Razor Components Migration**
  - [ ] `CanvasViewport2D.razor`: Pan and focal zoom SVG engine with optimized JSInterop.
  - [ ] `ViewportToolbar.razor`: Floating navigation and tag search toolbar.
  - [ ] `AssetTaskFaceplate.razor`: Adaptable container (Desktop lateral sidebar / Tablet bottom sheet).
  - [ ] Subcomponents: `MovingAnalogIndicator.razor`, `ActiveWorkOrdersList.razor`, `SafetyContextSummary.razor`.

- [ ] **SignalR Telemetry & Offline Store**
  - [ ] Real-time subscription by `TagNumber` with debouncing on rapid selections.
  - [ ] Priority 4 diagnostic fallback upon heartbeat timeout or connection loss.
  - [ ] SQLCipher encrypted local database with outbox command queue and SHA-256 evidence sealing.
