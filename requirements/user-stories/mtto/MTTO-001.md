---
id: MTTO-001
nombre: "Preventive Maintenance Scheduling"
priority: MUST
points: 5
role: Maintenance Planner
epic: MTTO
observations: This story is strictly restricted to scheduling by calendar time intervals.
applicable_trs:
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-008]]"
---

# MTTO-001: Preventive Maintenance Scheduling

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Maintenance Planner | I want to create and schedule preventive work orders on a recurring basis, linked to specific equipment units and maintainable items, based on calendar time intervals. | So that I can ensure routine maintenance is executed on time according to the established plan, maintaining traceability in compliance with ISO standards and reducing the risk of failure due to omission. |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| Successful preventive plan creation | Given the Planner is authenticated and the equipment unit is registered with full identification. | When they select the equipment unit, define the calendar time frequency, and save the plan. | Then the system confirms the plan creation and displays it as scheduled in the operational calendar. |
| Mandatory fields validation | Given the Planner is authenticated. | When they attempt to save a plan without selecting an equipment unit or without defining the frequency. | Then the system reports the missing mandatory fields and does not generate the schedule. |
| Traceability record | Given a recurring preventive plan has been successfully created. | When the user accesses the system's audit history. | Then they view the complete record with author, date and time, affected equipment unit, frequency, and configured method. |
| Active plans list | Given there are active preventive plans. | When the Planner queries the list of plans. | Then the system presents the equipment unit, the maintainable item, the time frequency, the date of the next work order, and the status. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-001 | The system shall allow the Planner to select an equipment unit (ISO 14224 Level 6) and link one or more maintainable items (Level 8) to the preventive plan. | Functional Suitability | High | ISO 14224 taxonomy and boundaries |
| FR-002 | The plan creation form shall allow defining a preventive maintenance frequency strictly based on calendar time intervals. | Functional Suitability | High | Wireman Vol 4 - The Core CMMS Engine |
| FR-003 | The system shall automatically calculate the date of the next Work Order based on the selected frequency and the last registered closure of the plan. | Functional Suitability | High | ISO 14224 recommended data and maintenance history |
| FR-004 | The system shall block saving the plan if any mandatory technical fields are missing (equipment unit, maintainable item, and frequency). | Functional Suitability | High | ISO 14224 recommended data and validation |
| FR-005 | The system shall automatically project and generate Work Orders according to the defined time interval without manual intervention. | Functional Suitability | High | Wireman Vol 4 - The Core CMMS Engine |
| FR-006 | The system shall display a registry of active preventive plans that exposes key tracking attributes (equipment unit, maintainable item, time frequency, next estimated work order date, and status). | Functional Suitability | High | Wireman Vol 4 - The Core CMMS Engine |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-007 | The scheduling service must have fault tolerance and automatic retry mechanisms to recover from service interruptions. | Reliability | High | Offline-First Design Principles (Google Developers) |
| NFR-008 | The management interface shall respond to user interactions in under 1 second to maintain planning workflow fluidity. | Performance Efficiency | Medium | The High Performance HMI Handbook (Hollifield) |
| NFR-009 | The system shall support the continuous growth of plan volumes without perceptible performance degradation. | Performance Efficiency | Medium | ISO/IEC 25010:2023 - Performance Efficiency (Capacity) |

## Source
- Automatically generated from `user-stories.csv`, `gherkin.csv` and `srs.csv`.
