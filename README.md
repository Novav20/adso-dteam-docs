# DTEAM — Digital Twin Enterprise Asset Management

Canonical repository of technical documentation and architecture for the **DTEAM** platform, targeting the industrial Oil & Gas sector.

---

## 1. System Vision

DTEAM is a high-criticality asset management platform that integrates industrial maintenance governance, physical resource control, passive IoT condition monitoring, and spatial schematic visualization.

The system is designed under strict compliance with international standards:
* **ISO 55001:2014:** Strategic asset management, risk prioritization, and decision-making.
* **ISO 14224:2016:** 9-level taxonomy, equipment boundaries, and standardized failure capture for reliability (MTBF/MTTR).
* **ISO 45001:2018 / OSHA:** Operational safety, Simultaneous Operations control (SIMOPS), and Zero-Energy assurance (LOTO Fail-Safe).
* **ISO 27001:2022:** Granular access control (RBAC/SoD) and immutable audit logging via SHA-256 cryptographic chaining (ADR-003).
* **ANSI/ISA-101.01-2015 / IEC 63303:** High-Performance Human-Machine Interfaces (HPHMI) in neutral grayscale and hierarchical L1–L4 display.

---

## 2. Technology Stack

In accordance with architecture decision **[[ADR-004]]** and traceability matrix **[[DT-ARQ-TECH-001]]**, the software is implemented under a unified **.NET** ecosystem:

* **Backend:** Modular Monolith on .NET 10 structured with Hexagonal Architecture (*Ports & Adapters*) and Domain-Driven Design (DDD).
* **Central Database:** PostgreSQL 18 + TimescaleDB extension (time series for telemetry). ISO 14224 taxonomic tree resolution is handled natively via recursive CTEs.
* **Mobile Field Client:** .NET MAUI Blazor Hybrid (Android/iOS) with encrypted local relational persistence via `sqlite-net-pcl` with SQLCipher (Offline-First).
* **Web Administrative Client:** Blazor Web App for HSEQ supervision, backlog planning, and control dashboards on desktop workstations.
* **Component Library:** Shared Razor components in a Razor Class Library (RCL) consuming Design System tokens.
* **Real-Time:** SignalR over WebSockets (WSS TLS 1.3) for LOTO safety heartbeat (2s) and process telemetry streaming.
* **IoT Ingestion:** Azure IoT Hub consuming industrial telemetry via MQTT from SCADA and exposing it to the backend via AMQP.
* **Graphic Canvas:** 2D-First strategy based on interactive SVG vector floor plans ([[ADR-001]]) with a roadmap towards 3D models.

---

## 3. Repository Structure

```text
adso-dteam-docs/
├── .agents/              # Agent skills for coherence auditing and SDLC analysis
├── architecture/         # C4 views (Components & Deployment), ASRs, ADRs, and Tech Stack Matrix
│   ├── adr/              # Architecture Decision Records (ADR-001 to ADR-006)
│   ├── asr/              # Architecturally Significant Requirements (ASR-001)
│   ├── patterns/         # Catalogue of applied GoF patterns and DDD tactics
│   └── views/            # C4 Component (CMP) and Physical Deployment (DEP) models
├── business-processes/   # BPMN 2.0 operational process flows (Draw.io)
├── compliance/           # Normative shield and ISO 14224 / ISO 55001 compliance justifications
├── domain-models/        # Tactical DDD modelling, activity diagrams, and Use Cases
│   ├── activity/         # UML activity diagrams for critical flows (LOTO, Preventive)
│   ├── class/            # Domain model specification, DDD entities and methods
│   ├── entity-relationship/ # Conceptual and logical relational database models
│   ├── ubiquitous-language/ # Ubiquitous Language glossary (DT-UL-DOC-001)
│   └── use-cases/        # Formal use cases and Master Traceability Matrix (DT-UC-TRC-001)
├── requirements/         # Software requirements and master sources
│   ├── common/           # Transversal Domain and Platform Requirements (TR-001 to TR-011)
│   ├── data/             # Master catalogs synchronized as CSVs (actors, SRS, stories, gherkin)
│   ├── interviews/       # Elicitation transcripts and field interviews
│   └── user-stories/     # Detailed user stories by module (ADM, INV, MTTO, VIS)
├── scripts/              # Documentation generation tools and coherence audit helpers
└── ui-ux/                # User interface design and information architecture
    ├── assets/           # CSS token files (tokens.css), MAI graphics (SVG), and wireframes
    ├── screens/          # Technical screen specification blueprints (SCR-*.md)
    ├── DT-UI-DS-DOC-001  # Design Tokens, HPHMI principles, and Visual Style Guide
    └── DT-UI-NAV-DOC-001 # Global Navigation Specification and Safety Guards
```

---

## 4. Development Ecosystem

The project operates under two complementary repositories:
1. **`adso-dteam-docs` (This repository):** Design specifications, formal models, interface contracts, and normative compliance shield.
2. **`adso-dteam-code` (In preparation):** Source code, unit/integration tests, and CI/CD pipelines.

---

## 5. Document Control

All technical artifacts are version-controlled under **ISO 9001:2015**. Architectural changes require approval from the Software Architect and must be formalized via a new ADR record or a justified update to the traceability matrices.


---
