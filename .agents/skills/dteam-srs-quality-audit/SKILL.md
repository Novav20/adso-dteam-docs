---
name: dteam-srs-quality-audit
description: Quality, ISO 25010:2023, TR-* sync, and dimension-agnostic Ubiquitous Language auditor for requirements/data/srs.csv and generated TR-*.md artifacts via scripts/verify_all.py.
---

# DTEAM Docs-as-Code — SRS Quality Auditor

## 1. General Description

This skill audits `requirements/data/srs.csv` and generated `requirements/common/TR-*.md` artifacts against repository SSoTs:

1. **SRS Integrity & `TR-*` Synchronization (`GRD-21`):** Validates required columns (`Req ID`, `Global ID`, `Description`, `Type`, `Status`, `TR ID`), uniqueness, `total_requirements` parity, and bidirectional `srs.csv` <-> `TR-*.md` consistency.
2. **ISO 25010:2023 & Normative Citations:** Flags deprecated quality categories (*Usability*, *Portability* -> use *Interaction Capability*, *Flexibility*) and vague standards citations instead of actionable ISO/NIST/OSHA/ISA/ACID references.
3. **Domain-Driven Ubiquitous Language Purity (`GRD-18`):** Detects rendering-coupled terms (`2D`, `3D`, `WebGL`, `SVG`, `CanvasViewport2D`) and generic asset phrasing across `srs.csv`, `DT-UL-DOC-001.md`, `DT-DM-DOC-001 §5`, and `UC-*.md`.

---

## 2. Deterministic CLI Execution

Run from the repository root (`adso-dteam-docs/`). Standard library `Python >= 3.11` only:

```bash
# Audit srs.csv integrity, TR-* sync, framework bans, and MVP index alignment
python3 scripts/verify_all.py --scope srs --format console

# Check dimension-agnostic Ubiquitous Language findings on srs.csv
python3 scripts/verify_all.py --scope ul --files requirements/data/srs.csv --format console

# Check domain constants and safety invariants (SOD-*, 0.0 V, 0.5 psig, 15 m, 13 m, 5 m)
python3 scripts/verify_all.py --scope domain --format console

# Strict gate (treat WARNING findings in srs.csv as exit code 2)
python3 scripts/verify_all.py --scope srs --strict --format console
```

---

## 3. Workflow & SSoT Governance

1. Run `python3 scripts/verify_all.py --scope srs` and inspect findings grouped by `BLOCKER` and `WARNING`.
2. Verify ISO 25010:2023 category names, actionable normative standards, and alignment with `ADR-003` (7-year audit retention / `TR-001`) and `ADR-006` (offline sync / `TR-007`).
3. **Never edit `requirements/common/TR-*.md` manually:** Remediate findings directly in `requirements/data/srs.csv` (and source CSVs) and regenerate `TR-*.md` before re-running `verify_all.py`.

---

## 4. Exit Codes

| Exit Code | Meaning |
| :--- | :--- |
| `0` | Passed (`0` blockers, and `0` warnings under `--strict`) |
| `1` | Execution/configuration error (missing CSV or invalid path) |
| `2` | Guardrail failure (`BLOCKER`, or `WARNING` under `--strict`) |
