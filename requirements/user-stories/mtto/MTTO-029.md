---
id: MTTO-029
nombre: "Equipment Physical Boundaries Definition"
priority: MUST
points: 3
role: Reliability Engineer
epic: MTTO
observations: This functionality is a mandatory ISO 14224 requirement for reliability data integrity. The precise definition of Boundaries ensures the equipment hierarchy is unique and consistent, eliminating ambiguities in the allocation of costs and technical responsibilities between adjacent equipment units.
applicable_trs:
  - "[[TR-001]]"
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-008]]"
---

# MTTO-029: Equipment Physical Boundaries Definition

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Reliability Engineer | I want to define and validate the physical boundaries of each master equipment unit, specifying its start, end points, and integrated internal components. | So that I can ensure each equipment unit has clear physical boundaries (start/end + included components), preventing duplication of maintenance or incorrect failure allocation. |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| Boundaries registration in Equipment Record | Given the Reliability Engineer is configuring the technical parameters of a Level 6 equipment unit. | When they record the physical boundary points and select the Level 8 components belonging to the equipment. | Then the system confirms the successful boundary registration and the selected components are officially integrated into the equipment's technical record. |
| Component uniqueness validation | Given a technical component is already assigned to the boundaries of an operational equipment unit. | When the technical staff attempts to link that same component to a different equipment unit in the hierarchy. | Then the system issues a hierarchical conflict notification and blocks the operation to prevent inconsistencies in the equipment database. |
| Boundaries visualization | Given a user queries the technical record of an equipment unit in the operational app. | When they access the boundaries and included components section. | Then they view the technical description of the physical boundaries and the complete list of components that make up the operational unit. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-091 | The system shall allow the Reliability Engineer to access the technical boundaries configuration from the Level 6 master Equipment Unit management. | Functional Suitability | High | ISO 14224:2016, Section 6 — Taxonomy |
| FR-092 | The definition form shall include fields to describe the initial boundary, the final boundary, and the multiple selection of associated Level 8 Maintainable Items. | Functional Suitability | High | ISO 14224:2016, Section 6 — Taxonomy |
| FR-096 | The system shall force the input of boundary fields before allowing the technical formalization of the Equipment Unit in the master catalog. | Functional Suitability | High | ISO 14224:2016, Section 6 — Taxonomy |
| FR-098 | The system shall provide a chronological history of adjustments made in the boundaries definition for engineering audits. | Functional Suitability | High | ISO/IEC 27001:2022, Annex A.8.15 (Logging) |
| FR-102 | Technical boundary descriptions must support the necessary length to detail complex physical specifications. | Functional Suitability | High | Database Schema Design Best Practices |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-093 | The system shall validate that a technical component CANNOT be assigned to multiple Equipment Units simultaneously to ensure hierarchy integrity. | Security | High | ACID Database Transaction Properties (Referential Integrity) |
| NFR-094 | The system shall detect inconsistencies in the deep hierarchy of components, ensuring that parent-child relationships remain coherent across all technical levels. | Security | High | ACID Database Transaction Properties (Referential Integrity) |
| NFR-095 | The system shall guarantee that saving technical boundaries does not generate partial or inconsistent records upon any process interruption. | Reliability | High | ACID Database Transaction Properties (Atomicity) |
| NFR-097 | Boundary information shall be accessible in read-only mode for technical personnel during the consultation of the equipment record in the field. | Security | High | NIST SP 800-192 (RBAC Framework) |
| NFR-099 | The validation of component duplication must complete in < 1 second to avoid affecting administrative workflows. | Performance Efficiency | High | ISO/IEC 25010:2023 — Performance Efficiency (Time behavior) |
| NFR-100 | The validation of hierarchical consistency in high-volume catalogs shall not degrade system response. | Performance Efficiency | High | ISO/IEC 25010:2023 — Performance Efficiency (Capacity) |
| NFR-101 | The boundaries definition interface must preserve the form's progress against session losses or unexpected browser closures. | Reliability | Medium | Offline-First Design Principles |
| NFR-103 | The system shall feature data integrity verification routines to detect and report any historical hierarchical anomalies. | Reliability | High | ACID Database Transaction Properties (Integrity) |

## Source
- Automatically generated from [user-stories.csv](../../data/user-stories.csv), [gherkin.csv](../../data/gherkin.csv) and [srs.csv](../../data/srs.csv).
