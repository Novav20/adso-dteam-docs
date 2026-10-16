---
id: MTTO-026
nombre: "Backlog Management via Objective Prioritization (RIME)"
priority: MUST
points: 5
role: Maintenance Planner
epic: MTTO
observations: The system will calculate the RIME Score by delegating the operation to the configurable prioritization engine under the industrial RIME standard (according to the MVP strategy defined in ADR-002). Being a direct operation based on equipment master data and work type selection, sequential dependency with the inventory module is eliminated.
applicable_trs:
  - "[[TR-001]]"
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-008]]"
---

# MTTO-026: Backlog Management via Objective Prioritization (RIME)

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Maintenance Planner | I want the system to automatically assign a RIME priority to tasks by combining equipment criticality and the selected work class. | So that I can eliminate subjectivity in scheduling, ensure ISO 55001 compliance, and focus resources on the highest-impact interventions. |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| RIME score calculation | Given an Equipment Unit has a Criticality index of 8. | When a Work Request is created with a Work Class index of 5. | Then the system automatically assigns a RIME priority score of 40 to the task. |
| Backlog sorting | Given the programming staff queries the pending tasks board. | When the system loads the list of work orders. | Then the interventions with the highest RIME Score (scale 1 to 100) automatically appear at the top section of the backlog. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-058 | The system shall automatically retrieve the numerical value of the Equipment Unit Criticality (scale 1 to 10) statically registered in the affected equipment's record. | Functional Suitability | High | Standard EAM / RIME Methodology |
| FR-059 | The Work Request creation form shall require the mandatory selection of the Work Class, associating the corresponding standardized numerical weight (1 to 10). | Functional Suitability | High | Standard EAM / RIME Methodology |
| FR-060 | The system shall calculate the RIME score by delegating the operation to the configurable prioritization engine under the adopted RIME industrial standard (see ADR-002). | Functional Suitability | High | Standard EAM / RIME Methodology |
| FR-065 | Each request presented in the system must display its priority metadata, affected Equipment Unit, intervention type, and estimated costs. | Functional Suitability | High | Standard EAM / RIME Methodology |
| FR-066 | The system shall allow querying the technical breakdown of the priority calculation, referencing the industrial standards applicable to each factor. | Functional Suitability | Low | ISO/IEC 25010:2023 — Functional Suitability (Appropriateness) |
| FR-067 | The system shall provide advanced filtering capabilities by priority category, Functional Location, and date ranges. | Functional Suitability | High | Nielsen Norman Group (NN/g) - Information Filtering |
| FR-068 | The system shall generate grouping recommendations when it detects multiple pending priority interventions on the same physical Equipment Unit. | Functional Suitability | Medium | Reliability-Centered Maintenance (RCM) Principles |
| FR-069 | The prioritized backlog information may be exported in structured formats for analysis in external tools. | Functional Suitability | Medium | Data Portability Principles |
| FR-074 | The calculation engine must be deterministic: the same inputs for equipment criticality and work class must produce identical scores throughout the system. | Functional Suitability | High | ISO/IEC 25010:2023 — Functional Suitability (Accuracy) |
| FR-075 | The system shall automatically recalculate priorities upon changes in the criticality of master equipment to keep the backlog updated. | Functional Suitability | High | ACID Database Transaction Properties (Consistency) |
| FR-076 | Significant changes in the priority category of an intervention must automatically notify the responsible planning personnel. | Functional Suitability | Medium | Enterprise Integration Patterns (Publish-Subscribe) |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-061 | The system shall classify and visually differentiate requests into priority bands according to their score (e.g., >80: Emergency, 50-79: High, 20-49: Normal, <20: Low). | Interaction Capability | High | The High Performance HMI Handbook |
| NFR-062 | The management dashboard shall organize requests descending by RIME Score, restricting manual alteration of the order to authorized profiles (Supervisors). | Security | High | NIST SP 800-192 (RBAC Framework) |
| NFR-070 | The RIME Score calculation upon changes in the Work Class must be performed in <100ms in the user interface. | Performance Efficiency | High | ISO/IEC 25010:2023 — Performance Efficiency (Time behavior) |
| NFR-071 | The operational dashboard visualization must maintain a response of < 2 seconds with large volumes of information. | Performance Efficiency | High | ISO/IEC 25010:2023 — Performance Efficiency (Time behavior) |
| NFR-072 | The master configuration parameters of the prioritization model must be versioned and protected against unauthorized access. | Security | High | NIST SP 800-53 (Configuration Management) |
| NFR-073 | The visibility of technical priority scores shall be restricted to the roles defined in the system's governance policy. | Security | High | NIST SP 800-192 (RBAC Framework) |

## Source
- Automatically generated from [user-stories.csv](../../data/user-stories.csv), [gherkin.csv](../../data/gherkin.csv) and [srs.csv](../../data/srs.csv).
