---
name: dteam-screen-scaffolder
description: Scaffolds DRY, SSoT-compliant screen specifications (SCR-*.md) and interactive HTML prototypes consuming DT-UI-CTR-001.md, DT-DM-DOC-001 §§4-5, DT-ARQ-CMP-DOC-001 §§5-6, ADR-003, and ADR-006.
---

# DTEAM Screen & Prototype Scaffolder Skill

## 1. Purpose & Input Contract

Given an audited Use Case (`UC-<MOD>-<NUM>.md`), this skill scaffolds two synchronized deliverables:
1. **`ui-ux/screens/<mod>/SCR-<MOD>-<NUM>.md`** in Technical English following `.agents/skills/dteam-ui-coherence-audit/templates/SCR-TEMPLATE-screen-specification.md`.
2. **`ui-ux/prototype/scr-<mod>-<num>.html` (+ `.js`)** in Spanish operational copy using shared `--dt-*` tokens (`tokens.css`) and SVG symbols (`icons.svg`), registered in `dev-wrapper.html` with 1080p PNG captures under `ui-ux/screens/<mod>/assets/`.

Load these SSoTs before drafting:
* **Use Case & Domain:** `UC-*.md`, `DT-UL-DOC-001.md`, `DT-DM-DOC-001.md` (§4 vocabularies, §5 `SOD-*` and safety constants `0.0 V`, `0.5 psig`, `15 m`, `13 m`, `5 m`), `DT-DM-DOC-002.md`, `DT-ERD-DOC-001.md`.
* **Shared UI & Architecture SSoTs:** [DT-UI-CTR-001.md](../../ui-ux/contracts/DT-UI-CTR-001.md), [DT-ARQ-CMP-DOC-001.md](../../architecture/views/DT-ARQ-CMP-DOC-001.md) §§5–6, `DT-UI-NAV-DOC-001.md`, `DT-UI-DS-DOC-001.md`, [ADR-003.md](../../architecture/adr/ADR-003.md), and [ADR-006.md](../../architecture/adr/ADR-006.md).

---

## 2. DRY Scaffolding & Architectural Rules

1. **Verify Upstream UC First:** Run `python3 scripts/verify_all.py --scope uc --files <UC-path>` and ensure `* **Related Screens:**` in `UC-*.md §6` includes the target `SCR-*`.
2. **Consume Shared Contracts (`DT-UI-CTR-001.md` & `DT-DM-DOC-001 §4`):**
   * **Never** redeclare shared domain enums (`WorkOrderStatus`, `EquipmentLifecycleStatus`, `StandardUnitOfMeasure`, etc.), shared lookup DTOs (`PagedLookupResultDto<T>`, `EquipmentUnitLookupDto`, `PermissionGrantKeyDto`), or shared `.razor` components (`PortalSidebarNav.razor`, spatial HUD kit, maintenance form kit, `EquipmentLookupModal.razor`). Link to `DT-UI-CTR-001.md` and `DT-DM-DOC-001.md#4-controlled-vocabulary`.
3. **Type, Security & Offline Rules (`GRD-05`, `GRD-08`, `GRD-15`, `ADR-003`, `ADR-006`):**
   * Use `decimal` for quantities/hours, `DateTimeOffset`/`DateOnly` (no `DateTime`), and `uint ConcurrencyToken` (`uint?` on offline-capable commands; omit `If-Match`/`ConcurrencyToken` on WORM tables).
   * Never expose `PreviousHash` on mutating `*Command`/`*RequestDto` (`ADR-003`); audit justification requires `>= 15` chars.
   * For offline screens, link §5.3.4 error handling directly to `ADR-006.md` 5-step `SyncOutbox` protocol instead of duplicating outbox SQL/retry steps.
4. **Pure Contracts & Presentation Purity (`GRD-07`, `GRD-16`):**
   * Ban `ComponentBase`, `[Inject]`, `_privateField`, lifecycle overrides, and `namespace` in §7.2; keep §1–§5 free of DB/interceptor internals and CSS class names.
   * Enforce ordered `## 1.`–`## 9.`, `### 7.1`–`7.3`, `CLS = 0`, 90/10 grayscale, and zero static pseudo-badges.
5. **HTML Prototype Hygiene (`GRD-19`, `GRD-20`):**
   * Require `<html lang="es">`, `#icon-*` sprites, `--dt-*` tokens (`tokens.css`), neutral focus states, and authentic Spanish operational labels with zero emojis, raw uppercase enum keys in visible DOM, or `FR-*`/`AF-*` codes.

---

## 3. Mandatory Verification Gate Before Handover

Register new REST endpoints in `DT-ARQ-CMP-DOC-001 §6.1` and SignalR events in `§5`, then run:

```bash
python3 scripts/verify_all.py --scope contracts --files ui-ux/screens/<mod>/SCR-<MOD>-<NUM>.md --format console
python3 scripts/verify_all.py --scope ui --files ui-ux/screens/<mod>/SCR-<MOD>-<NUM>.md --format console
python3 scripts/verify_all.py --scope api --files ui-ux/screens/<mod>/SCR-<MOD>-<NUM>.md --format console
python3 scripts/verify_all.py --scope uc --files ui-ux/screens/<mod>/SCR-<MOD>-<NUM>.md --format console
```

Remediate all `BLOCKER` findings (exit code `2`) prior to handover.
