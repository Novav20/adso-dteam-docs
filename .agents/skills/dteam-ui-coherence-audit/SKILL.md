---
name: dteam-ui-coherence-audit
description: Audits UI/UX screen specifications (SCR-*.md) and companion prototypes against the Domain Model, ERD, Shared UI Contracts, ADRs, Design System tokens, and ANSI/ISA-101 HPHMI standards.
---

# UI/UX Coherence & HMI Audit Skill

## 1. Purpose & Three-Tier Architecture

This skill audits `ui-ux/screens/<mod>/SCR-<MOD>-<NUM>.md` and companion prototypes (`scr-*.html`, `scr-*.js`) across three tiers:

1. **Tier 0 (Deterministic Guardrails):** `scripts/verify_all.py` enforces DRY contracts (`DT-UI-CTR-001.md`), enum parity (`DT-DM-DOC-001 §4`), `ADR-003`/`ADR-006` SSoTs, REST/SignalR parity (`DT-ARQ-CMP-DOC-001`), `--dt-*` token/WCAG 2.1 AA contrast, and prototype hygiene.
2. **Tier 1 (Heuristic & Ergonomic Audit):** Cross-checks mandatory ERD `NOT NULL` fields (`DT-ERD-DOC-001.md`), domain behaviors (`DT-DM-DOC-002.md`), safety invariants (`DT-DM-DOC-001 §5`), ISA-101 display hierarchy, and Spanish operational prototype copy.
3. **Tier 2 (Grounded Escalation Gate — Gemini Notebook):** Evaluates Triggers G1–G4 with a mandatory technical justification referencing local SSoTs when escalation is not triggered.

---

## 2. Deterministic CLI Execution (Tier 0)

Run from repository root (`adso-dteam-docs/`). Zero external packages required (`Python >= 3.11` stdlib):

```bash
# Audit target screen contracts, UI rules, and API/SignalR parity
python3 scripts/verify_all.py --scope ui --files ui-ux/screens/vis/SCR-VIS-008.md --format console
python3 scripts/verify_all.py --scope contracts --files ui-ux/screens/vis/SCR-VIS-008.md --format console
python3 scripts/verify_all.py --scope api --files ui-ux/screens/vis/SCR-VIS-008.md --format console

# Verify Design System tokens, WCAG contrast, and navigation guards
python3 scripts/verify_all.py --scope tokens --format console
python3 scripts/verify_all.py --scope nav --format console
```

Exit codes: `0` pass, `1` runtime/config error, `2` BLOCKER (or WARNING under `--strict`). Halt Tier 1 review whenever exit code `2` occurs.

---

## 3. Authoritative SSoT References & Audit Checklist

* **Shared UI Contracts:** [DT-UI-CTR-001.md](../../ui-ux/contracts/DT-UI-CTR-001.md) — shared lookup DTOs, Razor shell/HUD/planning/lookup parameters, `PermissionGrantKeyDto`, `StandardUnitOfMeasure`. Any DTO, enum, or `.razor` block duplicated across $\ge 2$ screens or redeclared inline is a `BLOCKER` (`GRD-06`).
* **Domain Vocabularies & Safety Constants:** [DT-DM-DOC-001.md](../../domain-models/class/DT-DM-DOC-001.md) — §4 enums (`DT-DM-DOC-001 §4` link required; no inline shared enums) and §5 constants (`SOD-*`, `0.0 V`, `0.5 psig`, `15 m`, `13 m`, `5 m`).
* **API & SignalR Registry:** [DT-ARQ-CMP-DOC-001.md](../../architecture/views/DT-ARQ-CMP-DOC-001.md) §§5–6 — every `VERB /api/v1/...`, `/hubs/*`, and SignalR event must match bidirectionally (`GRD-13`/`GRD-14`).
* **Audit & Offline ADRs:** [ADR-003.md](../../architecture/adr/ADR-003.md) (no `PreviousHash` on mutating commands/requests; `AuditJustification >= 15` chars; client preview digest only; `7 years` WORM retention) and [ADR-006.md](../../architecture/adr/ADR-006.md) (point §5.3.4 errors to canonical 5-step `SyncOutbox`; offline commands use `uint? ConcurrencyToken`).
* **Type & Contract Purity (`GRD-05`/`GRD-07`):** Use `decimal` (quantities/hours), `DateTimeOffset`/`DateOnly` (no `DateTime`), `uint`/`uint?` for `ConcurrencyToken`, and declarative Razor parameters only (ban `ComponentBase`, `[Inject]`, `_privateField`, `namespace`).
* **Structure & HPHMI:** Verify ordered `## 1.`–`## 9.` and `### 7.1`–`7.3` per `templates/SCR-TEMPLATE-screen-specification.md`; 90/10 grayscale, redundant shape+color alarms, Priority 4 diagnostic separation, `CLS = 0`, `#icon-*` symbols, and `<html lang="es">` prototypes free of emojis or SRS codes (`FR-*`/`AF-*`).

---

## 4. Tier 2 Escalation Gate (G1–G4) & Report Persistence

Evaluate all four triggers explicitly before concluding:
* **G1 (Life Safety & LOTO):** Hazardous energy isolation, live energy overrides, hot work interlocks.
* **G2 (Cognitive Overload):** $>30$ concurrent dynamic objects or multi-priority alarm floods.
* **G3 (Normative Taxonomy):** ISO 14224 Levels 6–9 boundary or failure mode conflicts unresolved by SSoT.
* **G4 (Novel Interaction):** Unprecedented spatial gestures or control modalities outside Archetypes A–C.

Persist reports to `reports/audits/ui/AUD-UI-<SCREEN_ID>-<YYYYMMDD-HHMMSS>.md`:

```yaml
---
id: AUD-UI-<SCREEN_ID>-<YYYYMMDD-HHMMSS>
screen_audited: <SCREEN_ID>
date: <YYYY-MM-DD HH:MM:SS>
verdict: PASSED | PASSED_WITH_OBSERVATIONS | BLOCKED
auditor: dteam-ui-coherence-audit
---
```

Present a concise chat summary with the verdict, blockers/warnings, G1–G4 justifications, and report link.
