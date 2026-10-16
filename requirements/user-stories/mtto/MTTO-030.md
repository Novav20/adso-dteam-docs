---
id: MTTO-030
nombre: "Equipment Warranty Management"
priority: SHOULD
points: 3
role: Maintenance Planner
epic: MTTO
observations: This functionality optimizes equipment return on investment (ROI) by automating the detection of active coverages. By integrating warranty dates with the work order creation flow, the system prevents unnecessary expenditure of internal resources and ensures compliance with external provider support contracts.
applicable_trs:
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-008]]"
  - "[[TR-011]]"
---

# MTTO-030: Equipment Warranty Management

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Maintenance Planner | I want to receive automatic notifications when an intervention is managed on an equipment unit with an active warranty. | So that I can leverage warranty coverage before performing internal maintenance, optimizing costs and avoiding redundant work on equipment still under warranty. |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| Active warranty alert | Given an operational equipment unit has valid warranty coverage according to system records. | When the technical staff attempts to initiate the registration of a corrective intervention for that equipment. | Then the system interrupts the operational flow with a warning notification, informing about the active warranty and suggesting initiating a claim. |
| Conversion to claim | Given an active warranty notification was issued during work order management. | When the responsible user chooses to formalize a technical claim with the provider. | Then the system adapts the operational interface, hiding internal cost fields and presenting the manufacturer's contact info and coverage terms. |
| Justified bypass | Given an active warranty notification was issued. | When the responsible user decides to proceed with internal maintenance despite the active coverage. | Then the system demands the entry of a mandatory technical justification before allowing the formalization of the work order. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-104 | The system shall automatically validate the validity of the Equipment Unit's warranty at the time of registering a corrective intervention. | Functional Suitability | High | Enterprise Asset Management (EAM) Best Practices |
| FR-105 | The warranty management interface shall present the provider's contact data and the specific terms of the available technical coverage. | Functional Suitability | High | Enterprise Asset Management (EAM) Best Practices |
| FR-106 | The system shall allow the transition of a standard work order toward a warranty claim status, notifying responsible personnel regarding the initiation of the external process. | Functional Suitability | Medium | Enterprise Integration Patterns |
| FR-107 | The system shall require selecting or entering a categorized technical justification when opting to proceed with internal maintenance on an Equipment Unit with an active warranty. | Functional Suitability | High | Compliance / Audit Trail Best Practices |
| FR-109 | The system shall not present warranty alerts when the coverage has expired according to the Equipment Unit's master records. | Functional Suitability | High | Enterprise Asset Management (EAM) Best Practices |
| FR-114 | The system shall validate the presence of a justification for the voluntary omission of external coverages, blocking flow advancement if the mandatory field is empty. | Functional Suitability | High | ISO 14224:2016 / EAM Data Quality |
| FR-115 | The system may present comparative intervention cost information when historical data permits such estimation. | Functional Suitability | Low | Enterprise Asset Management (EAM) Best Practices |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-108 | Every decision of internal maintenance on warranted Equipment Units shall be recorded with its respective technical justification and timestamp. | Security | High | ISO/IEC 27001:2022, Annex A.8.15 (Logging) |
| NFR-110 | Authorized personnel may manage and update warranty parameters from the Equipment Unit's technical record in the master catalog. | Security | High | NIST SP 800-192 (RBAC Framework) |
| NFR-111 | The validation of warranty validity must be performed in < 2 seconds to avoid interrupting the operational flow in the field. | Performance Efficiency | High | ISO/IEC 25010:2023 — Performance Efficiency (Time behavior) |
| NFR-112 | Warranty alerts must be presented clearly and prominently, ensuring the user perceives the warning before proceeding. | Interaction Capability | High | Nielsen Norman Group (NN/g) - Visibility of System Status |
| NFR-113 | The Equipment Unit's warranty data must be available during the consultation of the technical record in the field. | Flexibility | High | Offline-First Design Principles |

## Source
- Automatically generated from `user-stories.csv`, `gherkin.csv` and `srs.csv`.
