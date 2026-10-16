---
id: MTTO-004
nombre: "Automatic Report Data Extraction"
priority: SHOULD
points: 5
role: Maintenance Supervisor
epic: MTTO
observations: This cutting-edge functionality seeks to automate technical data ingestion through the cognitive processing of digital documents. Although extraction success is conditioned by the quality of the source reports, the system implements a mandatory human validation flow and a technical confidence indicator to ensure the integrity of the reliability database.
applicable_trs:
  - "[[TR-004]]"
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-009]]"
  - "[[TR-011]]"
---

# MTTO-004: Automatic Report Data Extraction

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Maintenance Supervisor | I want the system to automatically extract key information from digital documents (actual hours, used spare parts, work description) and present it in a summary ready for validation. | So that I can reduce the Work Order closure time and ensure traceability of technical maintenance data. |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| Successful data extraction | Given a digital report is attached to the Work Order. | When the Supervisor triggers the automatic extraction. | Then the system analyzes the document and pre-fills the real hours, materials, and description fields with a high confidence indicator. |
| Extraction with missing data | Given the attached report lacks material details. | When the system performs the automatic extraction. | Then it pre-fills the hours and description, flags the materials field as empty, and requires manual input from the Supervisor. |
| One-click approval | Given the extraction returned data with high confidence. | When the Supervisor reviews the pre-filled fields and clicks 'Approve Extraction'. | Then the data is permanently saved to the Work Order record. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-030 | The Supervisor can initiate automatic extraction via the corresponding function in the Work Order attachment management interface. | Functional Suitability | High | Nielsen Norman Group (NN/g) - AI and UI Guidelines (HITL) |
| FR-031 | The system shall analyze the digital document to extract: labor hours, bill of materials, and a technical summary of the work. | Functional Suitability | High | ISO 55000: Asset Management - Information Requirements |
| FR-032 | The processing engine shall return a dataset containing technical confidence levels for each extracted field, alongside a brief justification of the result. | Functional Suitability | High | Google Cloud AI Architecture Guidelines (Confidence Scoring) |
| FR-033 | If the technical confidence meets the configured threshold, the system shall pre-fill the Work Order fields and display visual indicators denoting data quality. | Functional Suitability | High | ISO 55000: Asset Management - Data Quality Assurance |
| FR-034 | If technical confidence is insufficient, the system shall require mandatory manual confirmation from the Supervisor before allowing the information to be saved. | Functional Suitability | High | Nielsen Norman Group (NN/g) - AI and UI Guidelines (HITL) |
| FR-035 | If a critical field is not identified in the document, the system shall notify the user of the missing information and enable the field for manual entry. | Functional Suitability | High | Nielsen Norman Group (NN/g) - 10 Usability Heuristics (Error Recovery) |
| FR-036 | The Supervisor shall have the final authority to edit or correct any automatically retrieved data prior to formalizing the Work Order closure. | Functional Suitability | Medium | Nielsen Norman Group (NN/g) - AI and UI Guidelines (HITL) |
| FR-037 | If the processing service is temporarily unavailable, the system shall implement automatic retries and ultimately notify the user to proceed manually. | Functional Suitability | Medium | ISO/IEC 25010:2023 - Reliability (Fault Tolerance) |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-038 | The extraction processing must complete in < 15 seconds to avoid degrading supervisor productivity. | Performance Efficiency | High | ISO/IEC 25010:2023 - Performance Efficiency (Time behavior) |
| NFR-039 | The processing engine parameters must guarantee deterministic and reproducible results for identical data inputs. | Reliability | High | ISO 55000: Asset Management - Data Quality Assurance |
| NFR-040 | Access credentials for external intelligence services must be managed securely and never exposed within the application logic. | Security | High | OWASP Secure Coding Practices (Credential Management) |
| NFR-041 | The system must structurally prohibit the automatic saving of data with low technical confidence, forcing human intervention as a data integrity control measure. | Security | High | Nielsen Norman Group (NN/g) - AI and UI Guidelines (HITL) |
| NFR-042 | The processing service must implement mitigation mechanisms (fallbacks) to handle potential outages of the external intelligence provider. | Reliability | Medium | ISO/IEC 25010:2023 - Reliability (Recoverability) |

## Source
- Automatically generated from `user-stories.csv`, `gherkin.csv` and `srs.csv`.
