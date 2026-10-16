---
id: MTTO-003
nombre: "Contractor Report Upload"
priority: SHOULD
points: 3
role: Contractor
epic: MTTO
observations: This component digitizes the delivery of third-party reports, unifying technical documentation in a single repository linked to the Work Order. The system must validate the integrity and format of the uploaded documents to ensure the information is actionable and secure, facilitating immediate review by the supervisor.
applicable_trs:
  - "[[TR-002]]"
  - "[[TR-003]]"
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-007]]"
---

# MTTO-003: Contractor Report Upload

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Contractor | I want to upload my work report in digital format to the assigned work order. | So that I can fulfill the client's delivery requirement quickly and digitally. |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| Successful digital report upload | Given the Contractor is authenticated and assigned to the Work Order. | When they upload a PDF report and select the corresponding Maintainable Item. | Then the system attaches the document, records the timestamp, and notifies the Supervisor. |
| Upload attempt with incorrect format | Given the Contractor is attaching a report. | When they attempt to upload a file with an unauthorized extension (e.g., .exe or .zip). | Then the system rejects the file, displays an invalid format error, and prevents the upload. |
| File size validation | Given the Contractor is attaching a report. | When they attempt to upload a PDF file exceeding 50 MB. | Then the system rejects the file and displays an error indicating the maximum allowed size has been exceeded. |
| Attachment viewing for Supervisor | Given a Contractor has uploaded a report. | When the Supervisor reviews the Work Order details. | Then they can view, download, and approve/reject the attached document directly from the interface. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-018 | The system shall allow a Contractor to upload work reports in PDF or image format linked to a specific Work Order. | Functional Suitability | High | Wireman Vol 4 - The Core CMMS Engine |
| FR-019 | Upon file upload, the system shall require the selection of the Maintainable Item (Level 8) to which the report belongs, ensuring ISO 14224 hierarchical traceability. | Functional Suitability | High | ISO 14224 failure data and taxonomies |
| FR-020 | The system shall validate file formats against an authorized whitelist (e.g., PDF, JPG, PNG) and reject unauthorized extensions to prevent malicious payloads. | Functional Suitability | High | OWASP Secure Coding Practices (File Upload Validation) |
| FR-021 | The system shall send an automated notification to the assigned Supervisor when a new report is uploaded to a Work Order under their purview. | Functional Suitability | Medium | Wireman Vol 4 - The Core CMMS Engine |
| FR-022 | The system shall allow the Supervisor to view, download, and approve/reject uploaded reports directly from the Work Order review interface. | Functional Suitability | High | Wireman Vol 4 - The Core CMMS Engine |
| FR-023 | The system shall allow users to filter attached documents by Maintainable Item within the Work Order view. | Functional Suitability | Low | Nielsen Norman Group (NN/g) - Information Filtering |
| FR-024 | The system shall allow the Contractor to delete an erroneously uploaded file PROVIDED THAT the Work Order has not yet been submitted for review. | Functional Suitability | Medium | Nielsen Norman Group (NN/g) - 10 Usability Heuristics (User Control and Freedom) |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-025 | The system shall support files up to 50 MB per individual upload. | Performance Efficiency | Medium | ISO/IEC 25010:2023 - Performance Efficiency (Capacity) |
| NFR-026 | The upload processing and confirmation time must be < 5 seconds under normal network conditions. | Performance Efficiency | Medium | ISO/IEC 25010:2023 - Performance Efficiency (Time behavior) |
| NFR-027 | The document storage infrastructure must feature redundancy to prevent the loss of critical technical evidence. | Reliability | High | ISO/IEC 25010:2023 - Reliability (Recoverability) |
| NFR-028 | The upload interface shall be fully functional and maintain visual consistency across both desktop browsers and mobile devices. | Interaction Capability | Medium | W3C Responsive Web Design (RWD) Guidelines |
| NFR-029 | The system shall perform automated malware scanning on all uploaded files before allowing them to be viewed or downloaded by other users. | Security | Low | OWASP Application Security Verification Standard (V12) |

## Source
- Automatically generated from [user-stories.csv](../../data/user-stories.csv), [gherkin.csv](../../data/gherkin.csv) and [srs.csv](../../data/srs.csv).
