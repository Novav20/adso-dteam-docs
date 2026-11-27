---
name: dteam-coherence-audit
description: Cross-seam coherence auditor for the DTEAM docs-as-code repository verifying relative links, GFM anchors, ERD/SQL/DBML parity, REST/SignalR catalogs, navigation guards, and MVP scope via scripts/verify_all.py.
---

# DTEAM Docs-as-Code — Coherence Auditor

## 1. General Description

This skill validates cross-seam integrity across all artifacts in `adso-dteam-docs/` without mutating target files:

1. **Traceability & Hygiene (`GRD-17`..`GRD-21`):** Relative links, GFM section anchors, 4-segment `DT-*` IDs, zero body wikilinks, dimension-agnostic UL purity, token/WCAG 2.1 AA parity, Technical English, LaTeX, Mermaid, and MVP scope.
2. **Domain & Schema Parity (`GRD-01`..`GRD-04`):** `DT-DM-DOC-001 §§4–5` (`SOD-*`, physical constants `0.0 V`, `0.5 psig`, `15 m`, `13 m`, `5 m`), `DT-DM-DOC-002`, `DT-DM-001.puml`, `DT-ERD-DOC-001.md`, `DT-ERD-001.sql`, and `DT-ERD-001.dbml`.
3. **Contracts, Navigation, Architecture & APIs (`GRD-05`..`GRD-16`):** Shared UI contracts (`DT-UI-CTR-001.md`), RBAC/navigation (`DT-UI-NAV-DOC-001`), REST/SignalR registries (`DT-ARQ-CMP-DOC-001 §§5–6`), WORM rules (`ADR-003`), and offline outbox rules (`ADR-006`).

---

## 2. Deterministic CLI Execution

Run from the repository root (`adso-dteam-docs/`). Standard library `Python >= 3.11` only:

```bash
# Single-file coherence audit across relevant seams
python3 scripts/verify_all.py --scope links --files <relative-path> --format console
python3 scripts/verify_all.py --scope nav --files <relative-path> --format console
python3 scripts/verify_all.py --scope arch --files <relative-path> --format console

# Domain / ERD / Contract parity checks
python3 scripts/verify_all.py --scope erd --format console
python3 scripts/verify_all.py --scope contracts --format console

# Full repository CI gate (all 21 rules; add --strict to fail on warnings)
python3 scripts/verify_all.py --scope all --format console
```

Available `--scope` values: `all`, `domain`, `erd`, `contracts`, `ui`, `uc`, `nav`, `rbac`, `arch`, `api`, `links`, `ul`, `tokens`, `srs`.

---

## 3. Workflow & Reporting

1. **Identify Artifact:** Resolve the repository-relative path of the candidate document or target the full repository (`--scope all`).
2. **List or Filter Rules (Optional):** Use `--list-rules --scope <scope>` or `--rules GRD-13,GRD-17` for focused triage.
3. **Execute Guardrails:** Run `python3 scripts/verify_all.py` (optionally `--format markdown --output reports/audits/compliance/AUD-FULL-REPO.md` to persist compliance evidence; `reports/` is excluded from rule noise).
4. **Present Findings:** List `BLOCKER` findings first (file, line, rule ID, and remediation), followed by `WARNING` and `INFO`. Ask the user before editing cross-file artifacts.

---

## 4. Exit Codes & Common Resolutions

| Exit Code | Meaning | Action |
| :--- | :--- | :--- |
| `0` | Verification passed (`0` blockers; warnings allowed unless `--strict`) | Approve with any logged observations |
| `1` | Execution/configuration error (invalid path, unknown scope/rule) | Verify CWD is `adso-dteam-docs/` and check `--scope` |
| `2` | Guardrail failure (`BLOCKER`, or `WARNING` under `--strict`) | Remediate cited SSoT mismatch before committing |
