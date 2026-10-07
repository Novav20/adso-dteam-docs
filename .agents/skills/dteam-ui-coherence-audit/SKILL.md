---
name: dteam-ui-coherence-audit
description: Audits UI/UX screen specifications against the Domain Model, ERD, Design System, and HPHMI/ISA-101 standards, supporting both Transactional (APM) and Supervisory (Digital Twin) screens.
---

# UI/UX Coherence & HMI Audit Skill

## 1. Purpose & Architectural Philosophy

This skill performs a **Two-Tier Coherence and Ergonomic Audit** on system UI/UX screen specifications (`SCR-*.md`) within the hybrid **Asset Performance Management (APM) and Digital Twin (DT)** architecture:

* **Tier 1 (Local Deterministic & Heuristic Audit):** Executed locally by the agent against the repository's Single Sources of Truth (SSoT: `DT-ERD-DOC-001`, `DT-DM-DOC-002`, `DT-UI-DS-DOC-001`, and requirements). Validates structural data integrity, token conformance, component boundaries, and codified HPHMI rules.
* **Tier 2 (Formal Grounded Audit Escalation):** When deep normative compliance, complex Cognitive Task Analysis (CTA), or subjective ergonomic trade-offs are identified, the skill generates a structured prompt for the user's external **Gemini Notebook (GN)**, which is grounded on authoritative, copyrighted standard corpora (ISA-101, *The High Performance HMI Handbook*, ISO 14224, ISO 11064).

---

## 2. Execution Steps

When invoked to audit a specific screen (e.g., `SCR-VIS-033`, `SCR-VIS-011`, or `SCR-MTTO-023`):

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

### Step 4: Audit Report Generation & Persistence

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
   * **[FAIL]:** Missing mandatory database fields, cardinality violations, or breaches of HPHMI/ISA-101 rules (color overloading, naked numbers, level boundary violations).
4. **Tier 2 Escalation (If Required):**
   * If the audit uncovers non-trivial ergonomic trade-offs, disputed HMI density, or complex CTA questions, format a dedicated prompt ready to be saved into `sena-evidence/00-Overview/Deep-in/Prompts/P<XX>-*.md` for formal verification in Gemini Notebook.
5. **Chat Presentation:** Present a concise summary in the chat with the overall verdict and a markdown link to the persisted report file in `sena-evidence/00-Overview/Audits/UI/`.
