---
name: dteam-sdlc-deep-audit
description: Holistic end-of-milestone SDLC auditor combining deterministic repository-wide guardrails (scripts/verify_all.py --scope all) with chronological cross-layer redundancy, ADR, and semantic analysis.
---

# DTEAM Docs-as-Code — Lifecycle Auditor (SDLC Deep Audit)

## 1. General Description

This skill performs a repository-wide SDLC audit across Requirements (`srs.csv`), Domain & Use Cases (`DT-UL-DOC-001`, `DT-DM-DOC-001/002`, `UC-*`), Relational Schema (`DT-ERD-DOC-001`, `.sql`, `.dbml`), Architecture (`DT-ARQ-*`, `ADR-*`), and UI/UX (`DT-UI-*`, `DT-UI-CTR-001`, `SCR-*`).

It combines:
1. **Deterministic Full-Repo Sweep (`GRD-01`..`GRD-21`):** Automated verification across all 13 architectural scopes via `scripts/verify_all.py --scope all`.
2. **Chronological Semantic Review:** Deep inspection of `git log` history and cross-layer artifacts to catch semantic redundancies, undocumented architectural decisions lacking an ADR, and subtle drift beyond deterministic rules.

---

## 2. Deterministic Full-Repository Baseline

Always start from the repository root (`adso-dteam-docs/`) by running the deterministic suite:

```bash
# Run all 21 guardrails across all scopes and inspect console summary
python3 scripts/verify_all.py --scope all --format console

# Run strict CI gate (fail on any WARNING as well as BLOCKER)
python3 scripts/verify_all.py --scope all --strict --format console

# Persist structured baseline snapshot for the SDLC audit report
python3 scripts/verify_all.py --scope all --format markdown --output reports/audits/AUD-SDLC-GUARDRAILS.md
```

Targeted drill-down scopes: `domain`, `erd`, `contracts`, `ui`, `uc`, `nav`, `rbac`, `arch`, `api`, `links`, `ul`, `tokens`, `srs`. Exit code `2` indicates unresolved `BLOCKER` findings (or `WARNING`s under `--strict`).

---

## 3. Chronological & Semantic SDLC Workflow

1. **Reconstruct Evolution:** Inspect `git log -n 30 --oneline` to trace recent architectural and SSoT milestones.
2. **Sweep Upstream-to-Downstream Layers:**
   * *Requirements & UL:* Check `requirements/data/srs.csv`, auto-generated `TR-*.md`, and `DT-UL-DOC-001.md` dimension-agnostic parity (`GRD-18`, `GRD-21`).
   * *Domain & Schema:* Verify `DT-DM-DOC-001 §§4–5` (vocabularies, `SOD-*`, physical safety thresholds `0.0 V`, `0.5 psig`, `15 m`, `13 m`, `5 m`), `DT-DM-DOC-002`, `DT-DM-001.puml`, and `DT-ERD-DOC-001`/`.sql`/`.dbml` (`GRD-01`..`GRD-04`).
   * *Architecture & ADRs:* Verify single-SSoT ownership in `ADR-003` (WORM `H_k` hash chain, `AuditJustification >= 15` chars, `7 years` retention), `ADR-006` (offline leases & 5-step `SyncOutbox`), and `DT-ARQ-CMP-DOC-001 §§5–6` (REST/SignalR registries, `GRD-13`..`GRD-16`).
   * *UI/UX & Contracts:* Verify DRY consolidation in `DT-UI-CTR-001.md`, presentation-layer purity across `SCR-*.md`, and `--dt-*` / WCAG contrast (`GRD-05`..`GRD-11`, `GRD-19`, `GRD-20`).
3. **Report Findings:** Persist the consolidated SDLC analysis to `reports/audits/AUD-SDLC-DOCS-IN-DEPTH-ANALYSIS.md` using `[RESOLVED]`, `[PENDING: ADR]`, `[PENDING: DECISION]`, and `[BLOCKER]` statuses, highlighting inter-layer redundancies, missing ADRs, and cross-artifact contradictions.

---

## 4. Exit Codes

| Exit Code | Meaning |
| :--- | :--- |
| `0` | Passed (`0` blockers, and `0` warnings under `--strict`) |
| `1` | Execution/configuration error |
| `2` | Guardrail failure (`BLOCKER`, or `WARNING` under `--strict`) |
