---
name: dteam-usecase-audit
description: Audits domain use cases (UC-*.md) against ERD, Domain Models, Ubiquitous Language, RBAC, and Navigation SSoTs via scripts/verify_all.py while enforcing strict black-box behavioral boundaries.
---

# Use Case Coherence & Domain Model Alignment Skill

## 1. Purpose & Three-Tier Architecture

This skill audits `domain-models/use-cases/<mod>/UC-<MOD>-<NUM>.md` before screen scaffolding:

1. **Tier 0 (Deterministic Guardrails):** `scripts/verify_all.py` checks 6-section structure & YAML keys (`GRD-09`), alternate-flow coverage & routes (`GRD-10`), canonical RBAC actors & `SOD-*` codes (`GRD-11`), black-box purity (`GRD-12`), and UL purity (`GRD-18`).
2. **Tier 1 (Heuristic & Domain Invariant Audit):** Validates conceptual parity with `DT-ERD-DOC-001.md` (`NOT NULL`, `1:N` cardinalities), `DT-DM-DOC-002.md` preconditions/atomic boundaries, `DT-DM-DOC-001 §5` physical safety constants, and `ADR-006` offline lease rules.
3. **Tier 2 (Grounded Escalation Gate — Gemini Notebook):** Evaluates Triggers G1–G4 with explicit SSoT-backed technical justification.

---

## 2. Deterministic CLI Execution (Tier 0)

Run from repository root (`adso-dteam-docs/`):

```bash
# Audit target Use Case structure, traceability, RBAC, black-box purity, and UL
python3 scripts/verify_all.py --scope uc --files domain-models/use-cases/inv/UC-INV-005.md --format console
python3 scripts/verify_all.py --scope rbac --files domain-models/use-cases/inv/UC-INV-005.md --format console
python3 scripts/verify_all.py --scope ul --files domain-models/use-cases/inv/UC-INV-005.md --format console

# Verify underlying domain model and ERD parity
python3 scripts/verify_all.py --scope domain --format console
```

Exit codes: `0` pass, `1` runtime/config error, `2` BLOCKER (halt heuristic audit and remediate first).

---

## 3. Authoritative SSoT Inputs & 5 Verification Axes

* **SSoT Inputs:** [DT-UL-DOC-001.md](../../domain-models/ubiquitous-language/DT-UL-DOC-001.md), [DT-DM-DOC-001.md](../../domain-models/class/DT-DM-DOC-001.md) (§4 vocabularies, §5 `SOD-*` codes & safety constants `0.0 V`, `0.5 psig`, `15 m`, `13 m`, `5 m`), [DT-DM-DOC-002.md](../../domain-models/class/DT-DM-DOC-002.md), [DT-ERD-DOC-001.md](../../domain-models/entity-relationship/DT-ERD-DOC-001.md), [DT-UI-NAV-DOC-001.md](../../ui-ux/DT-UI-NAV-DOC-001.md), [DT-UI-CTR-001.md](../../ui-ux/contracts/DT-UI-CTR-001.md), [ADR-003.md](../../architecture/adr/ADR-003.md), and [ADR-006.md](../../architecture/adr/ADR-006.md).
* **Axis 1 — UL & Hygiene (`GRD-18`):** Ban rendering-coupled terms (`2D`, `3D`, `WebGL`, `SVG`, `CanvasViewport2D`), drafting aliases (`Asset A / Asset B`), monolithic 2-column HTML tables, and body `[[wikilinks]]`.
* **Axis 2 — Black-Box Purity & Conceptual Parity (`GRD-12`):** Ban PostgreSQL schema qualifiers (`tax.*`, `mtto.*`, `inv.*`, `vis.*`, `adm.*`), snake_case tables/columns, SQL DDL/DML, `Class.Method()`, `/api/v1/*`, `--dt-*`, `CMP-*`, HTML tags, and `UUIDv7` implementation terms inside flows (use *unique client-generated correlation identifiers*).
* **Axis 3 — Domain Boundaries & Structure (`GRD-09`):** Require YAML keys (`id`, `name`, `module`, `user_story`, `primary_actor`, `secondary_actors`), ordered `## 1.`–`## 6.` headings, atomic transaction boundaries, and `* **Related Screens:**` in `§6` linking at least one owning `SCR-*.md`.
* **Axis 4 — Actors & Navigation (`GRD-11`):** Match canonical RBAC roles (`SCR-ADM-013`) or approved system actors (`SCADA / Historian`, `Audit Log Service`, etc.), and align upstream/downstream handoffs with `DT-UI-NAV-DOC-001.md`.
* **Axis 5 — Safety & Offline (`ADR-003`, `ADR-006`):** Mandate alternate flows (`AF-*`) for safety interlocks (`SOD-*`, telemetry loss, tamper alerts), WORM audit rules (`AuditJustification >= 15` chars, `7 years` retention), and cryptographic offline leases.

---

## 4. Tier 2 Escalation Gate (G1–G4) & Report Persistence

Evaluate all four triggers explicitly before finalizing:
* **G1:** Hazardous energy isolation / LOTO / hot-work safety risk.
* **G2:** Concurrent multi-permit SIMOPS cognitive overload.
* **G3:** ISO 14224 L6–L9 taxonomy conflicts unresolved by local SSoTs.
* **G4:** Unprecedented operational interaction pattern.

Persist audit evidence to `reports/audits/use-cases/AUD-UC-<UC_ID>-<YYYYMMDD-HHMMSS>.md` containing Executive Summary, 5-Axis Evaluation, Detailed Findings Table, Corrective Action Plan (`CAP-*`), and G1–G4 Escalation Gate table.
