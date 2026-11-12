---
code: DT-UC-TRC-001
version: 1.4
date: 2026-10-05
status: Active — Segmented MVP Scope and Standardized Use Cases
author: Juan David Julio Serrano
standard:
  - ISO 9001:2015
  - ISO 14224:2016
  - ISO 45001:2018
  - ISO 55001:2014
---
# Use Case Specification and Traceability Matrix

This document constitutes the **Single Source of Truth (SSoT)** for the specification and traceability of the EAM Digital Twin (DTEAM) system Use Cases.

---

## Maintenance Operations Module (MTTO)

### MVP Scope

| Use Case (ID)       | Use Case Name (Action / Objective)              | User Story (ID) | Primary Actor              | Regulatory Support / Business Invariant                                                                                                    |
| :------------------ | :---------------------------------------------- | :----------------------- | :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| **[UC-MTTO-001](mtto/UC-MTTO-001.md)** | Schedule Preventive Maintenance                 | [MTTO-001](../../requirements/user-stories/mtto/MTTO-001.md)             | Maintenance Planner        | **ISO 55001 (8.1):** Systematic scheduling to avoid accelerated wear and catastrophic failures.                                            |
| **[UC-MTTO-002](mtto/UC-MTTO-002.md)** | Close Work Order with ISO 14224 Taxonomy        | [MTTO-002](../../requirements/user-stories/mtto/MTTO-002.md)             | Maintenance Technician     | **ISO 14224 (Section 5):** Mandatory capture of failure data (mode, cause, and mechanism) for reliability indicators (MTBF).               |
| **[UC-MTTO-023](mtto/UC-MTTO-023.md)** | Schedule Telemetry-based Maintenance            | [MTTO-023](../../requirements/user-stories/mtto/MTTO-023.md)             | Maintenance Planner        | **ISO 13374 / CBM:** Dynamic planning based on mechanical wear and actual accumulated usage (hour meters).                                 |
| **[UC-MTTO-026](mtto/UC-MTTO-026.md)** | Prioritize Backlog via RIME                     | [MTTO-026](../../requirements/user-stories/mtto/MTTO-026.md)             | Maintenance Planner        | **ISO 55001 (6.2.2) / ADR-002:** Objective prioritization of critical resources delegated to configurable RIME strategy.                   |
| **[UC-MTTO-029](mtto/UC-MTTO-029.md)** | Define Asset Boundaries                         | [MTTO-029](../../requirements/user-stories/mtto/MTTO-029.md)             | Reliability Engineer       | **ISO 14224 (Section 5.6):** Mandatory specification of equipment boundaries to avoid duplication of maintenance costs.                      |

### Use Cases Planned for Later Phases (Out of MVP Scope)

| Use Case (ID) | Use Case Name (Action / Objective)         | User Story (ID) | Primary Actor              | Regulatory Support / Business Invariant                                                                                                    |
| :--------------- | :----------------------------------------- | :----------------------- | :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| UC-MTTO-003      | Upload Contractor Report (PDF)             | [MTTO-003](../../requirements/user-stories/mtto/MTTO-003.md)             | Contractor                 | **ISO 55001 (8.3 - Outsourcing):** Control and documentary integrity of services executed by third parties.                                |
| UC-MTTO-004      | Extract Report Data with AI                | [MTTO-004](../../requirements/user-stories/mtto/MTTO-004.md)             | Maintenance Supervisor     | **ISO 55001 (7.5 - Information Requirements):** Asynchronous ingestion and validation of reports to guarantee master data quality.         |
| UC-MTTO-020      | View Mobile Documentation                  | [MTTO-020](../../requirements/user-stories/mtto/MTTO-020.md)             | Maintenance Technician     | **ISO 55001 (7.5):** Offline availability of manufacturer manuals and technical schematics at the point of work.                           |
| UC-MTTO-028      | Consult Technical RAG Chatbot              | [MTTO-028](../../requirements/user-stories/mtto/MTTO-028.md)             | Maintenance Technician     | **ISO 55001 (7.2 - Competence):** Interactive safety assistance to avoid human interpretation errors during repairs.                       |
| UC-MTTO-030      | Manage Asset Warranties                    | [MTTO-030](../../requirements/user-stories/mtto/MTTO-030.md)             | Maintenance Planner        | **ISO 55001 (8.1 - Controls):** Validation of supplier coverage prior to the execution of internal maintenance expenditures.               |

---

## Resource Control Module (`INV`)

### MVP Scope

| Use Case (ID)       | Use Case Name (Action / Objective)         | User Story (ID) | Primary Actor              | Regulatory Support / Business Invariant                                                                                                                    |
| :------------------ | :----------------------------------------- | :----------------------- | :------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[UC-INV-005](inv/UC-INV-005.md)**  | Register Physical Asset Master             | [INV-005](../../requirements/user-stories/inv/INV-005.md)              | Project Engineer           | **ISO 14224 (9.1a):** Master data registration for unambiguous physical identification of equipment units (Level 6).                                       |
| **[UC-INV-006](inv/UC-INV-006.md)**  | Process Inventory Transactions (Kardex)    | [INV-006](../../requirements/user-stories/inv/INV-006.md)              | Warehouse Manager          | **ISO 55001 (8.1 - Control):** Transactional integrity (receipts, issues, and returns) for true stock control and WO costing.                              |
| **[UC-INV-007](inv/UC-INV-007.md)**  | Validate and Activate Master Asset         | [INV-007](../../requirements/user-stories/inv/INV-007.md)              | Reliability Engineer       | **ISO 14224 (Section 6) / ISO 45001:** Strict gate (Commissioning) for safety metadata and isolation points prior to operation.                            |
| **[UC-INV-025](inv/UC-INV-025.md)**  | Register Rotable Asset Swap                | [INV-025](../../requirements/user-stories/inv/INV-025.md)              | Reliability Engineer       | **ISO 14224 (Section 5):** Physical replacement tracking retaining reliability MTBF history per functional location.                                       |
| **[UC-INV-027](inv/UC-INV-027.md)**  | Structure Taxonomy of Functional Locations | [INV-027](../../requirements/user-stories/inv/INV-027.md)              | Project Engineer           | **ISO 14224 (Section 6):** Modeling of the taxonomic tree (levels 1-5) to retain process position history.                                                 |
| **[UC-INV-031](inv/UC-INV-031.md)**  | Manage Spare Part Master Catalog           | [INV-031](../../requirements/user-stories/inv/INV-031.md)              | Warehouse Manager          | **ISO 55001 (8.1):** Technical centralization of the Part Master using commoditized codes (SKUs) to avoid catalog duplicates.                              |

### Use Cases Planned for Later Phases (Out of MVP Scope)

| Use Case (ID) | Use Case Name (Action / Objective)         | User Story (ID) | Primary Actor     | Regulatory Support / Business Invariant                                                                                          |
| :--------------- | :----------------------------------------- | :----------------------- | :---------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| UC-INV-021       | Monitor Stock Replenishment                | [INV-021](../../requirements/user-stories/inv/INV-021.md)             | Warehouse Manager | **ISO 55001 (7.5 - Planning):** Management of automated technical purchases based on criticality and Class A, B, or C spares.    |

---

## Digital Twin Convergence Module (`VIS`)

### MVP Scope

| Use Case (ID)      | Use Case Name (Action / Objective)                | User Story (ID) | Primary Actor          | Regulatory Support / Business Invariant                                                                                                         |
| :----------------- | :------------------------------------------------ | :-------------- | :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| **[UC-VIS-008](vis/UC-VIS-008.md)** | Visualize Work Permits Overlay                    | [VIS-008](../../requirements/user-stories/vis/VIS-008.md)     | HSEQ Inspector         | **ISO 45001 (8.1):** Visual control of simultaneous operations (SIMOPS) to mitigate high-risk interference.                                     |
| **[UC-VIS-011](vis/UC-VIS-011.md)** | Verify Isolation Routes (LOTO) and Active Lockout | [VIS-011](../../requirements/user-stories/vis/VIS-011.md)     | Maintenance Technician | **ISO 45001 (8.1) / ASR-2:** Software block (fail-safe) preventing execution start if active energy is in the field or network heartbeat fails. |
| **[UC-VIS-033](vis/UC-VIS-033.md)** | Inspect Assets on the 2D Base Schematic           | [VIS-033](../../requirements/user-stories/vis/VIS-033.md)     | Maintenance Technician | **ISO 55001 (7.5) / ISA-101.01 / ADR-001:** Base canvas for situational awareness and real-time contextual inspection.                          |

### Use Cases Planned for Later Phases (Out of MVP Scope)

| Use Case (ID)    | Use Case Name (Action / Objective)             | User Story (ID) | Primary Actor          | Regulatory Support / Business Invariant                                                                                         |
| :--------------- | :--------------------------------------------- | :----------------------- | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| UC-VIS-009       | Navigate Hierarchically with Semantic Zoom     | [VIS-009](../../requirements/user-stories/vis/VIS-009.md)              | Maintenance Supervisor | **HPHMI (Hollifield):** Hierarchical navigation structure by levels (1-3) to mitigate data fatigue (UX).                        |
| UC-VIS-010       | Visualize 3D Exploded View (Teardown)          | [VIS-010](../../requirements/user-stories/vis/VIS-010.md)              | Maintenance Technician | **ISO 55001 (7.5 - Accessibility) / ADR-001 (3D Phase):** 3D exploded view for spatial recognition prior to physical teardown.  |
| UC-VIS-012       | Configure 3D Component Hierarchy               | [VIS-012](../../requirements/user-stories/vis/VIS-012.md)              | Project Engineer       | **ISO 55001 (7.5) / ADR-001 (3D Phase):** Technical administration of the mapping between 3D meshes (`.glb`) and the tree.      |

---

## Security and Governance Module (`ADM`)

### MVP Scope

| Use Case (ID)      | Use Case Name (Action / Objective)         | User Story (ID) | Primary Actor        | Regulatory Support / Business Invariant                                                                                                  |
| :----------------- | :----------------------------------------- | :----------------------- | :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **[UC-ADM-013](adm/UC-ADM-013.md)** | Manage Roles and Permissions               | [ADM-013](../../requirements/user-stories/adm/ADM-013.md)              | System Administrator | **ISO 55001 (5.3 - Roles):** Definition of authority and Segregation of Duties (SoD) to avoid conflicts.                                 |
| **[UC-ADM-014](adm/UC-ADM-014.md)** | Manage User Lifecycle                      | [ADM-014](../../requirements/user-stories/adm/ADM-014.md)              | System Administrator | **ISO 27001 (A.8.2 - IAM):** Secure cycle: brute force inactivity, PBKDF2 encryption, and logical deletion (soft-delete).                |
| **[UC-ADM-032](adm/UC-ADM-032.md)** | Consult Immutable Audit Trail              | [ADM-032](../../requirements/user-stories/adm/ADM-032.md)              | Plant Manager        | **ISO 27001 (A.8.15 - Logging) / ADR-003:** Chained SHA-256 cryptographic traceability to ensure log unalterability.                     |

### Use Cases Planned for Later Phases (Out of MVP Scope)

| Use Case (ID)    | Use Case Name (Action / Objective)         | User Story (ID) | Primary Actor          | Regulatory Support / Business Invariant                                                                                                  |
| :--------------- | :----------------------------------------- | :----------------------- | :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| UC-ADM-015       | Configure ERP Integration                  | [ADM-015](../../requirements/user-stories/adm/ADM-015.md)              | System Administrator   | **ISO 55001 (8.3 - Third Parties):** Industrial interoperability (MIMOSA) for inventory flows with Odoo/ERP.                             |
| UC-ADM-016       | Publish System Announcements               | [ADM-016](../../requirements/user-stories/adm/ADM-016.md)              | System Administrator   | **ISO 55001 (7.3 - Awareness):** Mass communication of maintenance windows to mitigate operational risks.                                |
| UC-ADM-017       | Consult Executive KPI Dashboard            | [ADM-017](../../requirements/user-stories/adm/ADM-017.md)              | Plant Manager          | **ISO 14224 (Annex C):** Mathematical consolidation of MTBF, MTTR, and unavailability to identify "problem assets" (Pareto).             |
| UC-ADM-018       | Generate Executive PDF Reports             | [ADM-018](../../requirements/user-stories/adm/ADM-018.md)              | Plant Manager          | **ISO 55001 (7.5 - Traceability):** Immutable and compliant export for offline analysis in executive committees.                         |
| UC-ADM-019       | Synchronize Data with BI Tools             | [ADM-019](../../requirements/user-stories/adm/ADM-019.md)              | Plant Manager          | **ISO 27001 (A.8.24 - Exchange):** Controlled exposure (OAuth 2.0 API / rate-limiting) of reliability datasets for analytics.            |
| UC-ADM-022       | Evaluate Optimization Suggestions (PMO)    | [ADM-022](../../requirements/user-stories/adm/ADM-022.md)              | Reliability Engineer   | **ISO 55001 (10.2 - Continuous Improvement):** Historical failure analysis to avoid over-maintenance (CAPEX/OPEX).                       |
| UC-ADM-024       | Configure General Parameters               | [ADM-024](../../requirements/user-stories/adm/ADM-024.md)              | System Administrator   | **ISO 55001 (7.5):** Parameterization of time zones and units of measure (ISO 80000) without altering the codebase.                      |
