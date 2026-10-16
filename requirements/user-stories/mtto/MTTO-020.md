---
id: MTTO-020
nombre: "Mobile Manuals Consultation"
priority: SHOULD
points: 3
role: Maintenance Technician
epic: MTTO
observations: This functionality seeks to decentralize access to technical information, allowing operational personnel to consult manuals and blueprints directly at the point of work. Although it is a significant productivity improvement for the conceptual prototype, its production implementation requires a robust document management strategy and an integrated document viewer with offline operation capabilities.
applicable_trs:
  - "[[TR-002]]"
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-007]]"
  - "[[TR-008]]"
  - "[[TR-011]]"
---

# MTTO-020: Mobile Manuals Consultation

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Maintenance Technician | I want to search and consult technical manuals and blueprints linked to the equipment hierarchy directly from the operational application. | So that I can consult the necessary information at the repair site without having to travel to the office or look for physical folders, ensuring the documentation is relevant to the component I am intervening on. |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| Usage-based WO generation | Given a preventive plan is set to trigger every 500 operating hours. | When the equipment unit's telemetry counter crosses the 500-hour threshold. | Then the system automatically generates the Work Order and resets the cycle counter. |
| Counter reset tracking | Given a preventive Work Order triggered by usage has been closed. | When the Technician confirms the replacement of the component. | Then the system records the reset of the cycle counter and logs the zero-point for the next iteration. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-043 | On the detail screen of an Equipment Unit or component, the system shall display a documentation section with the list of manuals, blueprints, and guides associated with that hierarchical level. | Functional Suitability | High | ISO 14224:2016, Section 6 — Taxonomy |
| FR-044 | Each document must present descriptive metadata: title, version, update date, and local availability status. | Functional Suitability | High | ISO 9001 — Documented Information Control |
| FR-045 | The system shall allow the visualization of technical documents via an integrated viewer, without requiring the user to be redirected to an external application. | Functional Suitability | High | Interaction Design Best Practices |
| FR-047 | The system shall allow the Technician to individually mark documents for offline consultation. The system shall visually confirm when the document is available locally. | Functional Suitability | High | Offline-First Design Principles |
| FR-048 | The system shall allow searching by technical terms within the list of documents associated with an Equipment Unit, prioritizing locally available results. | Functional Suitability | High | Nielsen Norman Group (NN/g) - Search & Discovery |
| FR-050 | The system shall verify the validity of the document version whenever connectivity exists, notifying if an update is available in the central repository. | Functional Suitability | High | Offline-First Design Principles (Delta Sync) |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-046 | The document viewer must support basic navigation functions: scale adjustment (zoom), panning between pages, and term search. | Interaction Capability | High | W3C Web Content Accessibility Guidelines (WCAG) |
| NFR-049 | The system shall inform the user when the local storage of downloaded documents reaches the capacity limit defined for the application. | Performance Efficiency | Medium | Nielsen Norman Group (NN/g) - Visibility of System Status |
| NFR-051 | If a document is withdrawn from the central repository, the system shall maintain the local version indicating its outdated or withdrawn status to avoid leaving the technician without reference. | Reliability | Medium | Graceful Degradation Patterns |
| NFR-052 | The opening of locally stored documents must complete in < 2 seconds to guarantee operational fluidity. | Performance Efficiency | High | ISO/IEC 25010:2023 — Performance Efficiency (Time behavior) |
| NFR-053 | The local search engine must return results in < 1 second for the end user. | Performance Efficiency | High | ISO/IEC 25010:2023 — Performance Efficiency (Time behavior) |
| NFR-054 | The verification of document versions must be performed in the background without impacting the interface's interactivity. | Performance Efficiency | High | Asynchronous Worker Patterns |
| NFR-055 | The document viewer must maintain the reading state (current page, zoom level) upon device orientation changes. | Interaction Capability | Low | Web Rendering Optimization Standards |
| NFR-056 | The system must support the automatic resumption of downloads in the event of network connectivity interruptions. | Reliability | High | Enterprise Integration Patterns (Retry Mechanisms) |
| NFR-057 | The query interface must be compatible with the mobile devices and operating systems defined in the plant's standards. | Flexibility | High | Responsive Web Design Standards |

## Source
- Automatically generated from [user-stories.csv](../../data/user-stories.csv), [gherkin.csv](../../data/gherkin.csv) and [srs.csv](../../data/srs.csv).
