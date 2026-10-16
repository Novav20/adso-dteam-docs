---
id: MTTO-028
nombre: "AI Documentation Consultation Assistant (RAG)"
priority: COULD
points: 5
role: Maintenance Technician
epic: MTTO
observations: This innovation functionality seeks to reduce technical information search time by using RAG (Retrieval Augmented Generation) architecture. By indexing the equipment's technical manuals, the system allows the technician to make contextual queries, ensuring each technical answer is backed by a direct reference to the manufacturer's documentation, thus minimizing operational risk due to interpretation errors.
applicable_trs:
  - "[[TR-002]]"
  - "[[TR-004]]"
  - "[[TR-005]]"
  - "[[TR-006]]"
  - "[[TR-009]]"
---

# MTTO-028: AI Documentation Consultation Assistant (RAG)

## Story Description

| Role | Action | Benefit |
|---|---|---|
| Maintenance Technician | I want to make natural language queries about technical procedures and manuals integrated into the system. | So that I can get fast answers with explicit references to a specific page/section of the manual, ensuring I confirm the information at the source before acting. |

## Acceptance Criteria
| Scenario | Given (Context) | When (Action) | Then (Result) |
|---|---|---|---|
| Question answered with source reference | Given the Technician is performing a technical intervention and opens the intelligence assistant interface. | When they ask about a specific technical specification contained in the equipment manuals. | Then the engine responds with the retrieved technical information and provides the exact reference (document, page, and section) for manual validation. |
| Out of context question | Given the Technician requests information unrelated to the available technical knowledge base. | When they perform a general or out-of-domain query. | Then the assistant communicates that it does not have reliable information in current manuals and suggests consulting the supervisor or reviewing physical documentation. |
| Offline query fallback | Given the operational staff is in an area without network connectivity. | When they attempt to use the intelligence assistant. | Then the system informs that the assistant is unavailable offline and presents the local search interface to query downloaded manuals. |
| Query audit log | Given a query to the intelligence assistant was made during an intervention. | When the supervisor reviews the work order history. | Then they view the query log including the timestamp, technical question, and document sources referenced by the engine. |

## Functional Requirements (FR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| FR-077 | The system shall allow access to the technical assistance interface from the Work Orders, maintaining the active session's query history. | Functional Suitability | High | Conversational UI Patterns |
| FR-078 | The system shall process natural language queries, searching for related concepts within the Equipment Unit's documentary base. | Functional Suitability | High | Retrieval-Augmented Generation (RAG) Architecture |
| FR-081 | The assistant shall detect queries outside the maintenance domain, redirecting the user to the corresponding technical support channels. | Functional Suitability | High | Domain-Driven Design / AI Guardrails |
| FR-084 | The system shall allow technical personnel to rate the utility of the received responses to feed the engine's continuous improvement processes. | Functional Suitability | Medium | RLHF (Reinforcement Learning from Human Feedback) |

## Non-Functional Requirements (NFR)
| ID | Description | ISO 25010 Category | Priority | Source |
|---|---|---|---|---|
| NFR-079 | The intelligence engine shall generate technical responses based exclusively on the recovered support documents, including mandatory citations to the original source. | Security | High | NIST AI Risk Management Framework (RMF) - Accountability |
| NFR-080 | The system shall evaluate the relevance level of the found information; if confidence is insufficient, it shall restrict the generation of the response to avoid erroneous interpretations. | Reliability | High | NIST AI Risk Management Framework (RMF) - Explainability |
| NFR-082 | In the absence of connectivity, the assistant shall be unavailable, and the system shall present local keyword search over persisted documents as an alternative. | Reliability | High | Offline-First Design Principles (Graceful Degradation) |
| NFR-083 | The assistant interface shall include a function to directly open the technical documentation in the section referenced by the intelligence engine. | Interaction Capability | High | Retrieval-Augmented Generation (RAG) Architecture |
| NFR-085 | The system shall provide an administrative dashboard to supervise executed queries and manage possible inconsistencies detected in responses. | Maintainability | High | NIST AI Risk Management Framework (RMF) - Accountability |
| NFR-086 | The processing of the query and the generation of the technical response must complete in < 15 seconds to guarantee field fluidity. | Performance Efficiency | High | ISO/IEC 25010:2023 — Performance Efficiency (Time behavior) |
| NFR-087 | The system must feature retry mechanisms against transient failures in communication with the intelligence service. | Reliability | High | Enterprise Integration Patterns (Retry Mechanisms) |
| NFR-088 | The engine shall guarantee consistent and objective results for the same query, minimizing the variability of the generated responses. | Reliability | High | AI Model Determinism / Temperature Control |
| NFR-089 | The system shall apply data minimization policies, storing only the summaries and metadata necessary for operational traceability. | Security | High | GDPR / Data Minimization Principles |
| NFR-090 | The system shall maintain response latency as the available documentary repository grows. | Performance Efficiency | Medium | ISO/IEC 25010:2023 — Performance Efficiency (Capacity) |

## Source
- Automatically generated from `user-stories.csv`, `gherkin.csv` and `srs.csv`.
