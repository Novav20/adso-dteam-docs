---
name: dteam-ui-coherence-audit
description: Audits UI/UX screen specifications against the Domain Model, ERD, Design System, and HPHMI/ISA-101 standards, supporting both Transactional (APM) and Supervisory (Digital Twin) screens.
---

# UI/UX Coherence & HMI Audit Skill

## 1. Purpose & Architectural Philosophy

This skill performs a **Three-Tier Coherence and Ergonomic Audit** on system UI/UX screen specifications (`SCR-*.md`) within the hybrid **Asset Performance Management (APM) and Digital Twin (DT)** architecture:

* **Tier 0 (Deterministic Pre-Flight Gate):** Automated script-based parsing via `.agents/skills/dteam-ui-coherence-audit/scripts/audit.py`. Evaluates AST/regex negative boundary rules: halts execution immediately on SQL/schema leaks, Blazor code-behind wrappers, private state, [Inject], raw CSS rules, hex codes, or missing canonical sections.
* **Tier 1 (Local Heuristic & Ergonomic Audit):** Executed locally by the agent against the repository's Single Sources of Truth (SSoT: `DT-ERD-DOC-001`, `DT-DM-DOC-002`, `DT-UI-DS-DOC-001`, and requirements). Validates task completeness, cardinality constraints, component boundaries, and codified HPHMI rules.
* **Tier 2 (Formal Grounded Audit Escalation):** When deep normative compliance, complex Cognitive Task Analysis (CTA), or subjective ergonomic trade-offs are identified, the skill generates a structured prompt for the user's external **Gemini Notebook (GN)**, which is grounded on authoritative, copyrighted standard corpora (ISA-101, *The High Performance HMI Handbook*, ISO 14224, ISO 11064).

---

## 2. CLI Execution & Helper Script

From the repository root (`adso-dteam-docs/`), the deterministic auditor is invoked via CLI:

```bash
# 1. Full deterministic audit + markdown report generation in sena-evidence/
uv run .agents/skills/dteam-ui-coherence-audit/scripts/audit.py audit --file ui-ux/screens/vis/SCR-VIS-008.md

# 2. Fast console linting (pre-commit / CI gate, zero report files generated)
uv run .agents/skills/dteam-ui-coherence-audit/scripts/audit.py lint --file ui-ux/screens/vis/SCR-VIS-008.md

# 3. Batch scan of all screen specifications
uv run .agents/skills/dteam-ui-coherence-audit/scripts/audit.py audit-all
```

### Exit Codes:
* `0`: Clean PASS or only WARNING/INFO observations.
* `1`: Execution error (file not found, outside repo).
* `2`: BLOCKER found (immediate rejection — document MUST NOT be approved without remediation).

---

## 3. Step-by-Step Execution Workflow

### Step 0: Deterministic Pre-Flight Gate (Tier 0)
1. Run `uv run .agents/skills/dteam-ui-coherence-audit/scripts/audit.py audit --file <relative-path>`.
2. If exit code is `2` (BLOCKER), stop immediately and report the specific syntactic/boundary violations to the user. Do NOT proceed to heuristic evaluation while deterministic blockers exist.

### Step 1: Context Gathering & Archetype Classification
1. Read the target screen specification (`SCR-*.md`) and its associated use case (`UC-*.md`).
2. Identify the screen archetype:
   * **Archetype A: Transactional / Command Screen (APM):** Forms, workflows, state mutations, permits, failure reporting, or inventory transactions (e.g., `SCR-MTTO-023`, `SCR-VIS-011`, `SCR-INV-025`).
   * **Archetype B: Supervisory / Inspection Screen (Digital Twin HMI):** Vector schematics, spatial navigation, real-time telemetry monitoring, faceplates, or alarm oversight (e.g., `SCR-VIS-033`, `SCR-VIS-008`).
3. Load corresponding project SSoTs:
   * ERD schema: `adso-dteam-docs/domain-models/entity-relationship/DT-ERD-DOC-001.md`.
   * Domain Model behaviors: `adso-dteam-docs/domain-models/class/DT-DM-DOC-002.md`.
   * Design System & tokens: `adso-dteam-docs/ui-ux/DT-UI-DS-DOC-001.md`.
   * Ubiquitous Language: `adso-dteam-docs/domain-models/ubiquitous-language/DT-UL-DOC-001.md`.
   * Canonical Screen Template: `adso-dteam-docs/.agents/skills/dteam-ui-coherence-audit/templates/SCR-TEMPLATE-screen-specification.md`.

---

### Step 2: Archetype-Specific Auditing

#### For Archetype A: Transactional / Command Screens
1. **Mandatory Field Completeness:**
   * Check physical ERD tables for `NOT NULL` columns that lack default values.
   * **Validation:** Does the UI provide explicit inputs or contextual state to supply all mandatory fields?
2. **Cardinality Verification:**
   * Check ERD referential relationships (`1 : 0..N` or `N : M`).
   * **Validation:** If a relationship is `1 : 0..N` (e.g., a work order with multiple failure records or LOTO points), does the UI allow dynamic multi-item additions, or does it erroneously enforce a `1 : 1` static form?
3. **Domain Method Signature Alignment:**
   * Check method signatures in `DT-DM-DOC-002.md` for triggered domain commands (e.g., `InstallEquipment`, `ReportFailure`).
   * **Validation:** Does the UI payload provide all typed parameters required by the domain method?

#### For Archetype B: Supervisory / Inspection Screens (HMI)
1. **Read-Model & SSoT Traceability:**
   * Verify displayed entities, identifiers, and statuses against `DT-ERD-DOC-001.md` and `DT-DM-DOC-002.md`.
   * **Validation:** Are status badges and criticality levels adhering strictly to canonical domain enums (e.g., `UP`, `DOWN`, `STANDBY`)?
2. **ISA-101 Display Hierarchy & Cognitive Boundaries:**
   * Validate screen classification (`isa101_level`): Level 1 (COP Overview), Level 2 (Process Area Schematic), Level 3 (Equipment Task Faceplate), Level 4 (Diagnostic / Master Detail).
   * **Validation:** Does a Level 3 Faceplate strictly isolate tactical operational data? Flag any Level 4 static master data (datasheets, purchase records, full vendor manuals, deep history) improperly polluting the faceplate.
3. **Codified HPHMI & Alarm Guardrails (`DT-UI-DS-DOC-001`):**
   * **Color Semantics:** Verify that neutral grays are used for normal operation. **[FAIL]** if green is used to indicate "normal/running".
   * **Alarm vs. Diagnostic Segregation:** Verify that communication/link failure or telemetry loss uses Priority 4 Diagnostic coding (muted text, neutral stale icon, timestamp). **[FAIL]** if amber/yellow or red is used for lost connection or stale data.
   * **Moving Analog Indicators (MAI):** Continuous process variables (pressure, temperature, flow) must be rendered in analog scale bars with defined normal operating zones (`--dt-color-mai-normal-zone`) and trip limits. **[FAIL]** if continuous variables are presented solely as naked numeric readouts.
4. **Actionable Task Content:**
   * Ensure lists (such as active Work Orders) display actionable attributes (WO ID, Type CM/PM, Status, Priority). **[FAIL]** if reduced to raw un-actionable counts ("3 active WOs").

---

### Step 3: Design System & Ergonomic Integrity (All Screens)

1. **Semantic Token Conformance:**
   * Verify that every `CMP-*` component references valid semantic tokens declared in `DT-UI-DS-DOC-001.md` (e.g., `--dt-color-*`, `--dt-radius-*`, `--dt-z-*`).
2. **Tactile Ergonomics:**
   * For controls targeted at tablets or mobile (`target_device: Industrial Tablet`), ensure action buttons and container triggers inherit `--dt-touch-target-mobile` ($\ge 48\text{px}$) to support gloved operation.
3. **Screen State Matrix Completeness:**
   * Verify coverage of necessary states: `Normal`, `Loading`, `Selected`, `Critical Alarm`, `Telemetry Loss / Diagnostic`, and `Unmapped / Offline`.

---

### Step 4: Structural Integrity, SSoT Boundary Enforcement & Anti-Redundancy Audit

All screen specifications must strictly align with the canonical standard defined in `templates/SCR-TEMPLATE-screen-specification.md`:

1. **Canonical 9-Section Hierarchy:**
   * Verify presence and exact sequencing of all 9 sections:
     * §1 Purpose and Operational Context
     * §2 Visual Artifact (Universal markdown link `![SCR-*](assets/SCR-*.svg)`)
     * §3 Functional Component Inventory
     * §4 Screen State Matrix
     * §5 Interaction Rules and Data Flow (Single Source of Truth)
     * §6 Industrial and Safety Considerations
     * §7 Frontend Component Contract (Blazor / Razor)
     * §8 Layout and Responsive Adaptability
     * §9 Traceability and Requirements Matrix
   * **[FAIL]** if sections are omitted, merged, or out of order.

2. **Section 1 & Section 3 Anti-Redundancy (Clean Cataloging & Scoping):**
   * Section 1 must state operational and environmental contexts qualitatively. **[FAIL]** if Section 1 embeds breakpoint tokens (`--dt-breakpoint-*`), container pixel/vh dimensions, or domain enum lists.
   * Table cells in §3 must strictly serve as a catalog of visual roles, semantic tokens, and pointers to Section 5.
   * **[FAIL]** if table cells in §3 contain detailed algorithms, mathematical formulas (e.g., coordinate calculations, clamping bounds), multi-step interaction workflows, hardware layout dimensions (e.g., `640px`, `45vh`), domain enum string lists, status strings, or NFR citations.
   * Column 4 ("Semantic Token") must reference explicit Design System tokens (`--dt-*`). **[FAIL]** if placeholder text (e.g., `Color: Security Matrix Tokens`) is used.

3. **Section 4 DOM/Visual-Only Delta Integrity:**
   * State descriptions in §4 must define observable visual modifications in the DOM (e.g., muted typography, halo additions, container transitions).
   * **[FAIL]** if §4 cells duplicate backend business rules, state machine transitions, or detailed interaction logic.

4. **Section 5 Single Source of Truth (SSoT) & Presentation Boundary Integrity:**
   * Section 5 is the sole SSoT for interaction mechanics, gesture physics, and calculations:
     * Viewport math, focal zooming, bounding box clamping, and coordinate transformations.
     * Layout shift invariants (e.g., fixed badge widths, fixed slot heights).
     * Tactile mechanics: touch thresholds (e.g., $4\text{px}$ pan threshold), sheet snap heights, drag handle hysteresis, and minimize transitions.
     * Real-time subscription policies, debouncing thresholds, and fail-safe diagnostic fallbacks.
   * **[FAIL] Presentation Layer Sequence Diagram Leaks:** UI sequence diagrams in §5.1 must model interactions strictly between `Tech`, `UI`, `Interop`, and the boundary `API` Gateway. Flag any backend worker hops (e.g., `API ->> Worker`, `API ->> DB`) or internal backend self-calls (`API ->> API`).
   * **[FAIL] Exhaustive Enum Duplication:** §5.3 must reference strongly-typed C# enums in §7.2.3. Flag exhaustive string literals in prose or LaTeX set equations enumerating enum literals.
   * **[FAIL] Duplicate Outbox Flows:** If §5.3.5 exists, §5.3.4 command dispatch must point directly to §5.3.5 instead of repeating local outbox serialization and sync retry steps.
   * **[FAIL] Parenthetical Type Contradictions:** Flag parenthetical fixtures in prose (e.g., `*(e.g., WorkOrderId = "WO-...")*`) that contradict strongly-typed DTOs (`Guid` vs `string`).

5. **Section 7 Tripartite Contract Conformance:**
   * Section 7 must follow the structured tripartite hierarchy:
     * `7.1 Component Hierarchy & File Mapping` (ASCII tree of `.razor` components).
     * `7.2 Physical Component Parameters & DTO Contracts (.NET 10 / C# 14)` (cleanly subdivided: 7.2.1 Root View, 7.2.2 Subcomponents, 7.2.3 DTO records).
     * `7.3 Client-Side DOM & Interop Bridge` (JavaScript Interop, pointer tracking, SVG DOM manipulation, or touch gesture bridge).
   * **Decoupled Namespaces:** Snippets define UI contracts, parameters, and DTO signatures without premature C# `namespace` declarations.
   * **[FAIL]** if Section 7 dumps unstructured monolithic code, hardcodes speculative namespaces, or omits the client-side bridge (`7.3`).

6. **Sections 8 & 9 Completeness & Consistency:**
   * **Section 8 (Layout & Responsive Adaptability):** Must tabulate layout organization and ergonomic rules across all 3 standard viewports:
     * Desktop Workstation ($\ge 1920\text{px}$, `--dt-breakpoint-xl`)
     * Industrial Tablet Landscape ($1280\text{px} - 1919\text{px}$, `--dt-breakpoint-lg` / $1280\times 800\text{px}$)
     * Industrial Tablet Portrait ($768\text{px} - 1279\text{px}$, `--dt-breakpoint-md` / $800\times 1280\text{px}$)
   * **[FAIL] Component Responsibility Mismatch:** Verify that `CMP-XX` references in Section 8 match their cataloged roles in Section 3 (e.g., toolbar vs floating filter bar).
   * **[FAIL] Raw CSS Expressions:** Section 8 must not contain raw CSS `calc()` expressions; use descriptive architectural offsets.
   * **Section 9 (Traceability and Requirements Matrix):** Serves as the Single Source of Truth (SSoT) for screen-level requirements mapping. Must tabulate all functional and non-functional requirements associated with the screen's user story (sourced from Notion/backups: `srs.csv` / `transversal-requirements.csv`), mapping each requirement (`FR-*`, `NFR-*`, `TR-*`, `ADR-*`) to its implementing `CMP-*` component and concrete verification mechanism. The YAML frontmatter excludes raw requirement arrays to prevent duplicate bookkeeping.

7. **Language and Persona Tone Guardrails:**
   * Must be written in 100% Technical English. **[FAIL]** if Spanish words, accents, or untranslated domain phrases are present.
   * Must maintain concise, senior engineering tone without parenthetical filler, conversational fluff, or premature design rationales.

8. **Implementation Leak Prevention (Architectural Abstraction):**
   * Screen specifications govern presentation behavior, ergonomic targets, client quality gates, and data contracts. They must remain strictly decoupled from backend persistence internals and transient frontend prototype artifacts:
     * **[FAIL] Prototype CSS Artifacts:** Specification text (especially in §3, §5, and §6) must not reference HTML/CSS prototype class names (e.g., `.scope-timing-cards-grid`, `.btn-evidence-primary`, `.evidence-dropzone`, `.labor-timing-grid`). Layout and styling must be expressed strictly in terms of Blazor subcomponents and Design System semantic tokens (`tokens.css`).
     * **[FAIL] Backend Database Transaction Orchestration:** In §5.3, the specification must declare the client command dispatch contract (`SubmitCommand`, endpoint, payload DTO, `X-Idempotency-Key`, HTTP 200 vs. offline/error handling). It is strictly forbidden from detailing backend SQL transactions, multi-table insert/update sequences (e.g., `INSERT INTO failure_records... UPDATE work_orders...`), or database index mechanics (e.g., GIN indexing in `adm.audit_logs`), which belong exclusively to `DT-ARQ-DB-DOC-001`.
     * **[FAIL] Direct DB Writes in UI Workflows:** Workflows must describe data encapsulation into typed DTOs/commands, not direct database column mutations (e.g., *"stores metadata in `mtto.media_attachments: file_url, ...`"*).
     * **[FAIL] Low-Level Runtime & Package Coupling:** Section 7.3 must define capability interfaces (`ICameraInterop`, `ICryptoInterop`, `IOfflineStorage`) rather than concrete JavaScript API call snippets (e.g., `SubtleCrypto.digest(...)`) or third-party NuGet package names (e.g., `sqlite-net-pcl`).

9. **Domain Nomenclature & Anti-Meta-Text Guard (`TXT-001`):**
   * Screen specifications, wireframes, and component catalogs must use authentic operational domain terminology from `DT-UL-DOC-001.md` and ISO 14224 (e.g., `Dismounted Asset`, `Replacement Asset`).
   * **[FAIL] Drafting Variable Placeholders (`TXT-001`):** Generic variable aliases (`Asset A / Asset B`, `Activo A / Activo B`, `Entity X / Y`, `Record 1 / 2`) or software pipeline jargon are strictly prohibited in component names, wireframes, interaction workflows, and state matrices.

---

### Step 5: Audit Report Generation & Persistence

The agent **must persist** the complete audit report to the evidence repository at:
`/home/novillus/Documents/vscode/SENA-Career/sena-evidence/00-Overview/Audits/UI/AUD-UI-<SCREEN_ID>-<YYYYMMDD-HHMMSS>.md`

*(Note: `<YYYYMMDD-HHMMSS>` represents the execution timestamp, e.g., `20261007-153520`, ensuring multiple audit runs and fix iterations are preserved without overwriting history).*

The generated report must include the following structure:
1. **Frontmatter:**
   ```yaml
   ---
   id: AUD-UI-<SCREEN_ID>-<YYYYMMDD-HHMMSS>
   screen_audited: <SCREEN_ID>
   date: <YYYY-MM-DD HH:MM:SS>
   verdict: PASSED | PASSED_WITH_OBSERVATIONS | BLOCKED
   auditor: dteam-ui-coherence-audit
   ---
   ```
2. **Screen Classification:** Detected Archetype (A or B), ISA-101 Level, Target Devices, and Primary Persona.
3. **Audit Findings & Evaluation:**
   * **[PASS]:** Elements compliant with ERD, Domain Model, and Design System tokens.
   * **[WARNING]:** Potential cognitive overload, missing ergonomic affordances, or ambiguous parameters.
   * **[FAIL]:** Missing mandatory database fields, cardinality violations, structural/SSoT boundary violations, or breaches of HPHMI/ISA-101 rules.
4. **Tier 2 Escalation (If Required):**
   * If the audit uncovers non-trivial ergonomic trade-offs, disputed HMI density, or complex CTA questions, format a dedicated prompt ready to be saved into `sena-evidence/00-Overview/Deep-in/Prompts/P<XX>-*.md` for formal verification in Gemini Notebook.
5. **Chat Presentation:** Present a concise summary in the chat with the overall verdict and a markdown link to the persisted report file in `sena-evidence/00-Overview/Audits/UI/`.
