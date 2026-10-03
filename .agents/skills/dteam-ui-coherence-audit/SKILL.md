---
name: dteam-ui-coherence-audit
description: Audits UI/UX screen specifications against the Domain Model and ERD to ensure data and cardinality coherence.
---

# UI/UX Coherence Audit Skill

## Purpose
This skill validates that a User Interface (UI) mockup or screen specification accurately reflects the physical database schema (ERD) and Domain Model behavior. It prevents "Impedance Mismatches" where the UI fails to capture required data or restricts cardinality incorrectly.

## Execution Steps

When invoked by the user to audit a specific screen (e.g., `SCR-VIS-011` or `Technical Closure`):

1. **Context Gathering:**
   - Read the UI specification markdown provided by the user.
   - Identify the primary entities and aggregates being manipulated on this screen (e.g., `WorkOrder`, `FailureRecord`, `Locator`).
   - Read the corresponding sections of the ERD (`adso-dteam-docs/domain-models/entity-relationship/DT-ERD-DOC-001.md`).
   - Read the corresponding sections of the Domain Model (`adso-dteam-docs/domain-models/class/DT-DM-DOC-002.md`).

2. **Data Completeness Audit:**
   - Check the physical ERD table for `NOT NULL` fields that do not have a `Default Value`.
   - **Validation:** Does the UI specification provide inputs, hidden fields, or context to supply *all* mandatory fields?
   - **Validation:** Are newly introduced domain fields (e.g., `technician_notes` in `failure_records`) represented in the UI if applicable?

3. **Cardinality Audit:**
   - Check Section 4 of the ERD (Referential Relationships) for the relevant entities.
   - **Validation:** If the ERD defines a `1 : 0..N` relationship (e.g., `work_orders` to `failure_records`), does the UI design allow the user to add multiple instances (e.g., a dynamic list or "Add Another" button)? Or does the UI wrongly assume a `1 : 1` static form?

4. **Behavioral Audit:**
   - Check the Domain Model (`DT-DM-DOC-002.md`).
   - **Validation:** If the UI triggers a domain method (e.g., `ReportFailure`), does the UI collect all the parameters defined in the method signature?

5. **Output Generation:**
   - Present a clear, structured Audit Report to the user containing:
     - **[PASS]** items that are correctly aligned.
     - **[WARNING]** items that are ambiguous.
     - **[FAIL]** items where the UI restricts the database or misses mandatory data. Provide explicit recommendations for fixing the UI.
