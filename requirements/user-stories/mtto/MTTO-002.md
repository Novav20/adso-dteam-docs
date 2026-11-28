---
id: MTTO-002
nombre: "Digital WO Closure with ISO 14224 Taxonomy"
priority: MUST
points: 8
role: Maintenance Technician
epic: MTTO
observations: This process is critical to guarantee information quality according to ISO 14224 requirements. The implementation prioritizes an optimized user experience for mobile devices in the field, ensuring the capture of failure data (mode, mechanism, cause) even in low-connectivity conditions.
applicable_trs:
  - "[[TR-001]]"
  - "[[TR-002]]"
  - "[[TR-003]]"
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-007]]"
  - "[[TR-008]]"
  - "[[TR-010]]"
  - "[[TR-011]]"
---

# MTTO-002: Digital WO Closure with ISO 14224 Taxonomy

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Maintenance Technician | I want to record the closure of a work order from my mobile device, classifying the failure according to the ISO 14224 taxonomy and attaching multimedia evidence. | So that I can ensure technical traceability, comply with industry standards, and allow accurate calculation of reliability indicators (MTBF/MTTR). |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| Successful closure with ISO classification | Given the Technician has completed the physical work and the Corrective Work Order is in 'IN_PROGRESS' status. | When they fill out the closure form specifying the Maintainable Item, Failure Mode, Failure Mechanism, and Failure Cause according to ISO 14224, and submit the closure. | Then the system transitions the Work Order status to 'COMPLETE' and records the immutable ISO 14224 technical reliability data. |
| Attach multimedia evidence | Given the Technician is filling out the WO closure form. | When they capture or attach a photograph of the repaired equipment unit. | Then the system associates the image with the closure record and makes it visible for future technical audits. |
| Data integrity validation (ISO 14224 Lock) | Given the Technician attempts to close a corrective Work Order. | When they omit the Failure Cause or any mandatory ISO 14224 taxonomic field. | Then the system blocks the closure, alerts about the missing technical data, and prevents the state transition. |
| Offline operation | Given the Technician is in a plant area without network coverage. | When they register the WO closure with ISO 14224 classification. | Then the system saves the record locally and automatically synchronizes it with the server once connectivity is restored. |
| Dynamic taxonomy filtering | Given the Technician is classifying a failure. | When they select the Maintainable Item. | Then the system dynamically filters the available Failure Modes to show only those applicable to that specific item class. |
| Preventive and Predictive closure omitting FailureRecord | Given a PREVENTIVE or PREDICTIVE WorkOrder is in 'IN_PROGRESS' status. | When the Technician invokes CompleteTechnically() without filling failure taxonomy fields. | Then the system allows technical completion to 'COMPLETE' without requiring an ISO 14224 FailureRecord, unlike CORRECTIVE WorkOrders. |
| Corrective Work Order two-stage closure under SOD-MTTO-01 | Given a CORRECTIVE WorkOrder is in 'IN_PROGRESS' status with MaintainableItem, FailureMode, FailureMechanism, and FailureCause recorded. | When the assigned Technician submits technical completion and subsequently an independent Maintenance Supervisor closes it administratively. | Then CompleteTechnically() transitions the WorkOrder to 'COMPLETE', self-approval by the same Technician is blocked under SOD-MTTO-01, and an independent Supervisor invoking CloseAdministratively() transitions it to 'CLOSED' with a chained AuditLog entry. |
| Corrupt multimedia evidence SHA-256 quarantine | Given a Technician uploads multimedia evidence alongside its SHA-256 hash during Work Order closure. | When the computed SHA-256 hash does not match the uploaded payload. | Then the system quarantines the corrupt file, rejects attachment binding, and logs a warning. |
| Rotable swap branching and LOTO re-energization abort | Given a Work Order involves a rotable EquipmentUnit swap or still has an active LOTO lockout. | When the Technician attempts to close the Work Order. | Then the system routes rotable swaps through the Equipment Swap flow and aborts closure if active LOTO re-energization clearance is incomplete. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-010 | The system shall allow a Technician to register the closure of a Work Order from a mobile device, including Actual Man-Hours. | Functional Suitability | High | Wireman Vol 4 - The Core CMMS Engine |
| FR-011 | The closure form shall allow selecting and saving the Maintainable Item (Level 8), Failure Mode, Failure Mechanism, and Failure Cause, strictly using the ISO 14224 taxonomy. | Functional Suitability | High | ISO 14224 failure data and taxonomies |
| FR-012 | The system shall block the Work Order status transition until mandatory taxonomy fields are completed; it shall display a specific error message if fields are missing to enforce ISO 14224 compliance. | Functional Suitability | High | ISO 14224 mandatory data constraints |
| FR-013 | The system shall allow attaching multimedia (photo/video); files must be linked to the Work Order and remain visible to the Supervisor and Reliability Engineer. | Functional Suitability | Medium | SMRP Best Practices (CMMS Data Quality) |
| FR-014 | Upon form submission, the Work Order status shall transition to 'COMPLETE' (pending administrative closure by an independent Supervisor under SOD-MTTO-01), and an event notification shall be triggered for the Maintenance Supervisor and Reliability Engineer. | Functional Suitability | High | Wireman Vol 4 - The Core CMMS Engine |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-015 | The local persistent storage must guarantee data integrity against unexpected shutdowns and support retry mechanisms. | Reliability | High | Offline-First Design Principles (Google Developers) |
| NFR-016 | The system shall process operations on the mobile interface in under 2 seconds to prevent disrupting field workflow. | Performance Efficiency | Medium | The High Performance HMI Handbook (Hollifield) |
| NFR-017 | The system must be compatible with standard mobile operating systems used in the industrial environment. | Flexibility | Medium | W3C Mobile Web Application Best Practices / PWA Core Criteria |

## Source
- Automatically generated from [user-stories.csv](../../data/user-stories.csv), [gherkin.csv](../../data/gherkin.csv) and [srs.csv](../../data/srs.csv).
