# DTEAM: Product Engineering Roadmap & Technical Tasks

This file is the Single Source of Truth (SSoT) for engineering deliverables, architectural tasks, and implementation milestones for the DTEAM system (Asset Performance Management / Digital Twin).

All documentation and specifications referenced here reside in `adso-dteam-docs/` and are authored strictly in **100% Technical English**.

---

## 📌 Phase 1: Spatial UI/UX & HMI Viewports (Desktop & Mobile)

### Core Spatial & Supervisory Viewports (Digital Twin HMI)
- [x] **SCR-VIS-033: Level 3 Equipment Task Faceplate**
  - [x] Responsive layout on Desktop ($1920\times 1080$), Tablet Landscape ($1280\times 800$), and Industrial Tablet Portrait ($800\times 1280$).
  - [x] Touch physics: upward drag height retention, snap hysteresis, Google Maps light-dismiss (zero peek tab), and discrete single-tap handle dismiss.
  - [x] Spatial Engine Calibration: neutral HPHMI spatial palette (`--dt-color-canvas-*`), zoom-adaptive ISO 128 hierarchical lineweights, pure `viewBox` site-boundary clamping, unified `> 4px` primary/middle-click pan, hybrid LOD ramps, `Space` / `Ctrl + K` intent framing, L3 ISO 14224 spatial breadcrumb, and screen-space clamped ANSI/ISA-5.1 plates.
  - [x] Canonical specification finalized and locked as Gold Standard Baseline: [`SCR-VIS-033.md`](ui-ux/screens/vis/SCR-VIS-033.md) (v2.3 Stable).

- [x] **SCR-VIS-008: Level 1 General Plant Map with SIMOPS Layer**
  - [x] Redundant coding for PTW pins (`#sym-icon-ptw-*`, `48 × 48` two-tone spatial profile, Color + Shape Silhouette + Icon + Label per ANSI/ISA-101).
  - [x] IOGP 459 / API 2015 3-state SIMOPS matrix (`A` / `R` / `X`), shape-aware buffers with intersection-only diagonal hatching (`A ∩ B`), concurrency fan-out trays, auto-enabled `L-ELEC-HAZ`, programmatic L1 zone summary pills, and contextual popovers with viewport boundary clamping.
  - [x] Modernized frosted HUD elevation (`--dt-shadow-glass`), unified `> 4px` pan ergonomics, borderless discrete risk filters, and flat unmapped permits list: [`SCR-VIS-008.md`](ui-ux/screens/vis/SCR-VIS-008.md) (v2.2 Stable).

- [x] **SCR-VIS-011: LOTO Isolation Boundary Matrix**
  - [x] Cognitive Task Analysis (CTA): Physical Try-Out attestation primacy and negative interlock logic.
  - [x] Spatial Isolation Precision: Oblique `H/V + 45 deg` MCC electrical routes, edge-anchored mechanical boundary lines, translucent `--dt-color-loto-disc` cutoff discs (`#sym-icon-loto-isolated` / `#sym-icon-eloto-energized` / `#sym-icon-mloto-energized`), pure SVG `<mask>` Focal Island aperture, full-circuit initial framing, and inward-clustered off-screen directional edge beacons.
  - [x] Canonical specification finalized and locked as Gold Standard Baseline: [`SCR-VIS-011.md`](ui-ux/screens/vis/SCR-VIS-011.md) (v2.2 Stable).

### Maintenance Management Screens (MTTO)
- [x] **SCR-MTTO-002: Work Order Technical Closure**
  - [x] Multi-evidence array ($1 : 0..N$), SHA-256 tamper verification, and discrete ISO 14224 mini-bars.
  - [x] Canonical specification finalized and locked as Gold Standard Baseline: [`SCR-MTTO-002.md`](ui-ux/screens/mtto/SCR-MTTO-002.md) (v1.7 Stable — Screen #4, Field Execution Form Archetype, `ScopeChecklist`, `IsolationStatus`, `ClosureCertificateModal.razor`, 100% C# 14 / .NET 10 contracts, `TR-001`–`ADR-007` traceability).

- [x] **SCR-MTTO-026: RIME Backlog Prioritization Dashboard**
  - [x] 1–100 RIME criticality matrix scoring and batching recommendation.
  - [x] Audit data pertinence, finalize desktop prototype review, capture high-res screenshot, and promote to Stable.
  - [x] Canonical specification finalized and locked as Gold Standard Baseline: [`SCR-MTTO-026.md`](ui-ux/screens/mtto/SCR-MTTO-026.md) (v1.5 Stable — Screen #5, Supervisory Desktop Web Portal Archetype, `BacklogItemStatus`, `EstimatedCost`, 100% C# 14 / .NET 10 contracts, `TR-001`–`TR-011`, `ADR-002`, `ADR-003` traceability).

- [x] **SCR-MTTO-001: Calendar-Based Maintenance Scheduling**
  - [x] Cascading taxonomy selector (L6 $\to$ L7 $\to$ L8) and battery limit validation.
  - [x] Canonical specification finalized and promoted to Stable: [`SCR-MTTO-001.md`](ui-ux/screens/mtto/SCR-MTTO-001.md) (v1.2 Stable).

- [x] **SCR-MTTO-023: Condition / Telemetry-Based Maintenance**
  - [x] Telemetry variable binding, threshold calculations, and monotonic counter rules.
  - [x] Canonical specification finalized and promoted to Stable: [`SCR-MTTO-023.md`](ui-ux/screens/mtto/SCR-MTTO-023.md) (v1.2 Stable).

- [x] **SCR-MTTO-029: Asset Boundary Limits Card (Battery Limits)**
  - [x] Canonical specification finalized with engineering limits, cost boundaries, and ISO 14224 sub-tree decomposition: [`SCR-MTTO-029.md`](ui-ux/screens/mtto/SCR-MTTO-029.md) (v1.2 Stable).
  - [x] Execute Tier 0/1 UI audit and promote to Stable.

### Inventory & Asset Master Data Screens (INV)
- [x] **SCR-INV-025: Rotable Asset Swap**
  - [x] Field modal / drawer for atomic 1:1 rotable equipment exchange.
  - [x] Canonical specification finalized: [`SCR-INV-025.md`](ui-ux/screens/inv/SCR-INV-025.md) (v1.5 Stable — Screen #7, Level 4 Transactional Modal Dialog Archetype, 100% C# 14 / .NET 10 contracts, `TaxonomicCompatibilityBadge.razor` `CMP-06` nested in `ModalActionFooter.razor` `CMP-09`, `TR-001`–`TR-011`, `ADR-003`/`005`/`007`/`010` traceability).
  - [x] Visual prototype modern continuous redesign & dual-theme captures updated (Dark/Light).

- [x] **SCR-INV-005: Equipment Master Data Card (Technical Data Sheet)**
  - [x] Pre-flight Use Case Audit and CAP execution: [`UC-INV-005.md`](domain-models/use-cases/inv/UC-INV-005.md) (v1.1 Stable / PASSED).
  - [x] Canonical specification finalized: [`SCR-INV-005.md`](ui-ux/screens/inv/SCR-INV-005.md) (v1.3 Stable — Screen #6, Level 3 Master Datasheet & Audited Governance Archetype, `EquipmentTechnicalSchematicCard.razor` `CMP-13`, 100% C# 14 / .NET 10 contracts, `TR-001`–`TR-011`, `ADR-003`/`ADR-005`/`ADR-010` traceability).
  - [x] Execute Tier 0/1/2 UI audit, capture 1080p screenshot, and persist report (`PASSED`).
  - [x] Modernize visual ergonomics & tablet landscape responsiveness, extract shared [`portal-shell.css`](ui-ux/assets/portal-shell.css), and update high-res visual artifact.

- [x] **SCR-INV-027: Functional Locations Hierarchy Tree**
  - [x] Canonical specification finalized for ISO 14224 Level 1 to Level 5 navigation tree: [`SCR-INV-027.md`](ui-ux/screens/inv/SCR-INV-027.md) (v1.1 Stable).
  - [x] Execute Tier 0/1 UI audit and promote to Stable.

- [x] **SCR-INV-031: Spare Parts Master Catalog**
  - [x] Canonical specification finalized for spare parts inventory, stock policies, and interchangeability: [`SCR-INV-031.md`](ui-ux/screens/inv/SCR-INV-031.md) (v1.2 Stable).
  - [x] Execute Tier 0/1 UI audit and promote to Stable.

- [x] **SCR-INV-006: Movements and Kardex History**
  - [x] Canonical specification finalized for transactional spare parts ledger and equipment movement history: [`SCR-INV-006.md`](ui-ux/screens/inv/SCR-INV-006.md) (v1.1 Stable).
  - [x] Execute Tier 0/1 UI audit and promote to Stable.

### Administration & Security Screens (ADM)
- [x] **SCR-ADM-013: Roles and Permissions Matrix (RBAC)**
  - [x] Canonical specification finalized for role privileges, Segregation of Duties (`Role.ValidateSoD()`), and 2D security matrix: [`SCR-ADM-013.md`](ui-ux/screens/adm/SCR-ADM-013.md) (v1.1 Stable — 4 desktop captures, `AuditActionType`, `RolePermissionAction`).
  - [x] Execute Tier 0/1 UI audit and promote to Stable.

- [x] **SCR-ADM-014: User Lifecycle Management & Security Lockout**
  - [x] Canonical specification finalized for credential lifecycle, brute-force lockout control, and `FR-251` multi-role union governance: [`SCR-ADM-014.md`](ui-ux/screens/adm/SCR-ADM-014.md) (v1.1 Stable — 4 desktop captures).
  - [x] Execute Tier 0/1 UI audit and promote to Stable.

- [x] **SCR-ADM-032: Immutable Audit Log Viewer**
  - [x] Canonical specification finalized for WORM SHA-256 chained transaction logs, secret-masked JSONB diffs, Meta-Auditing, and 7-year dynamic quarterly retention partitions: [`SCR-ADM-032.md`](ui-ux/screens/adm/SCR-ADM-032.md) (v1.1 Stable — 4 desktop captures, Cross-Cutting 37-table/43-enum parity verified).
  - [x] Execute Tier 0/1 UI audit and promote to Stable.

### Architectural Viewport Shell & Cross-Cutting Gates (Deferred until Screen Specs are Stable)
- [x] **Prototype asset modularization and Design System alignment**
  - [x] Extract screen-specific CSS and JavaScript from the seven catalogued prototype screens without changing screen routes, IDs, or alternate-flow message listeners.
  - [x] Apply canonical `tokens.css` and `portal-shell.css` to portal workstation screens and preserve archetype-specific modal, canvas, and mobile layouts.
  - [x] Validate local `file:///` asset references, JavaScript syntax, HTML parsing, and `dev-wrapper.html` catalog integrity.

- [x] **Unified Spatial Application Shell & Dual Icon Profile**
  - [x] Formalized single-canvas viewport kinematics, normalized zoom tokens (`--dt-zoom-scale-*`, `--dt-cad-stroke-floor`), site-boundary clamping, and hybrid LOD cross-fades across `SCR-VIS-008`, `SCR-VIS-033`, and `SCR-VIS-011` ([`DT-UI-DS-DOC-001.md`](ui-ux/DT-UI-DS-DOC-001.md) v2.3, [`DT-UI-NAV-DOC-001.md`](ui-ux/DT-UI-NAV-DOC-001.md)).
  - [x] Reconciled dual SVG icon profile: `24 × 24` monochromatic UI glyphs (`#icon-*`) + `48 × 48` two-tone spatial markers (`#sym-icon-*`) in [`ui-ux/assets/icons.svg`](ui-ux/assets/icons.svg) with WCAG 2.1 AA verification across HPHMI spatial surfaces.

- [ ] **Known Spatial HMI & Product Backlog Gaps (MVP / Post-MVP Triage)**
  - [ ] **`LIM-UI-002` (Telemetry Quality Token):** Introduce a dedicated Magenta ANSI/ISA-101 "Bad Quality" diagnostic token (`--dt-color-quality-bad`) in [`DT-UI-DS-DOC-001.md`](ui-ux/DT-UI-DS-DOC-001.md) §3.3 to decouple SCADA communication loss (`Priority 4` slate) from active sensor hardware/signal quality faults.
  - [ ] **Gap 1 — Dedicated 2D Plot Plan MOC Ingestion & Piping Promotion:** Define an operational Management of Change (MOC) SVG upload, validation, and coordinate diff workflow in MVP/Phase 2 alongside progressive promotion of static piping corridors (`L-PIPE-PROC`) into discrete addressable `EquipmentUnit` records without disrupting base coordinates.
  - [ ] **Gap 2 — HSEQ Role-Specific Map Layer Toggle Policy:** Formalize RBAC-governed map layer visibility toggles (`L-ELEC-HAZ`, `L-FIRE-PROT`, diagnostic overlays) in production operational profiles across operational profiles (`HSEQ Inspector`, `Maintenance Supervisor`, `Maintenance Technician`).
  - [ ] **`LIM-VIS-003` (Post-MVP — Multi-Plant & 3D Isometric Islands):** Multi-facility terminal switcher and WebGL/3D isometric facility island viewports scoped strictly for Post-MVP evolution.

---

## 📌 Phase 2: Ingestion Contracts & Digital Twin Spatial Tooling

- [x] **DT-UI-SVG-DOC-001: SVG Ingestion Contract (v2.3 Approved)**
  - [x] Normative 7-layer standard (`L-CIVL-BOTM`, `L-CIVL-PROP`, `L-CIVL-PUBROAD`, `L-MECH-EQPM`, `L-PIPE-PROC`, `L-INSP-INST`, `L-FIRE-PROT`, `L-ELEC-HAZ`, `L-ANNO-TEXT`).
  - [x] ISO 14224 binding attributes (`data-func-loc`, `data-equip-id`, `data-status`) and generalizable `CALIBRATION-VECTOR` (`data-nominal-span="0.65"`).
  - [x] MOC audit header metadata (`data-moc-id`, `data-rev-number`, `data-checksum-sha256`), `$6,000$-node` operational target (`15,000` hard cap), ISO 128 4-tier zoom-adaptive scaling, dynamic `3.0 px` text halos, and spatial clearance Rules 4–6 (`DT-UI-SVG-DOC-001.md`).

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

- [x] **Pre-Implementation Persistence & Domain Contract Remediation (Batch 1 & Batch 2)**
  - [x] Enforce `TIMESTAMPTZ` across all temporal columns in [`DT-ERD-DOC-001.md`](domain-models/entity-relationship/DT-ERD-DOC-001.md) and [`DT-ERD-001.sql`](domain-models/entity-relationship/DT-ERD-001.sql) for Npgsql 10 UTC compliance.
  - [x] Replace broken `UNIQUE (removed_at)` on `tax.asset_installations` with partial unique indexes (`WHERE removed_at IS NULL`) and configure TimescaleDB hypertable composite PK `(timestamp, id)` on `vis.telemetry_signals`.
  - [x] Add missing persistence fields required by stable screen contracts (`adm.audit_logs.previous_hash`, `mtto.media_attachments.integrity_hash_sha256` & `captured_offline`, `mtto.work_orders.scope_checklist`, `vis.work_order_isolations` offline lease columns, `mtto.maintenance_plans` ISO 14224 Level 7/8 (`subunit_id`, `maintainable_item_id`) & CBM fields, `tax.functional_locations` integer criticality `1..10`).
  - [x] Resolve all missing `CHECK` enums and explicit FK mappings (`issuer_user_id`, `lease_holder_user_id`, `subunit_id`, `maintainable_item_id`) in [`scripts/generate_ddl.py`](scripts/generate_ddl.py) with strict fail-fast validation.
  - [x] Reconcile 4-dimensional `EquipmentUnit` state transitions in [`DT-DM-DOC-002.md`](domain-models/class/DT-DM-DOC-002.md) and promote [`DT-UL-DOC-001.md`](domain-models/ubiquitous-language/DT-UL-DOC-001.md) to `APPROVED`.

- [ ] **Pre-Implementation Architecture & Contract Alignment (Batch 3)**
  - [x] Resolve `ITaxonomyService` vs. `IInventoryService` ownership of `INV-025` (`SwapAssetAsync`) in [`DT-ARQ-CMP-DOC-001.md`](architecture/views/DT-ARQ-CMP-DOC-001.md).
  - [x] Document the Cross-DbContext Unit of Work / Shared `DbConnection` transaction pattern in [`DT-ARQ-DB-DOC-001.md`](architecture/DT-ARQ-DB-DOC-001.md).
  - [ ] Define the canonical multi-project `.sln` structure (`Dteam.Contracts`, shared `Dteam.Ui` Razor Class Library, `Dteam.Web`, `Dteam.Mobile`) in [`DT-ARQ-TECH-001.md`](architecture/DT-ARQ-TECH-001.md).

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
