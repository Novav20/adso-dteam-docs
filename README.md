# DTEAM — Digital Twin Enterprise Asset Management

[![.NET 10](https://img.shields.io/badge/.NET-10-512BD4?style=flat-square&logo=dotnet&logoColor=white)](architecture/DT-ARQ-TECH-001.md)
[![.NET Aspire](https://img.shields.io/badge/.NET_Aspire-Local_Orchestration-512BD4?style=flat-square&logo=dotnet&logoColor=white)](architecture/adr/ADR-011.md)
[![Blazor & MAUI](https://img.shields.io/badge/UI-Blazor_%2B_MAUI_Hybrid-512BD4?style=flat-square&logo=blazor&logoColor=white)](architecture/adr/ADR-004.md)
[![PostgreSQL 18](https://img.shields.io/badge/PostgreSQL-18_%2B_TimescaleDB-4169E1?style=flat-square&logo=postgresql&logoColor=white)](architecture/DT-ARQ-DB-DOC-001.md)
[![ISO 14224](https://img.shields.io/badge/Standard-ISO_14224_%7C_55001-0B857A?style=flat-square)](compliance/)
[![ANSI/ISA-101](https://img.shields.io/badge/HMI-ANSI%2FISA--101-2563EB?style=flat-square)](ui-ux/DT-UI-DS-DOC-001.md)

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

In accordance with architecture decision **[ADR-004](architecture/adr/ADR-004.md)** and traceability matrix **[DT-ARQ-TECH-001](architecture/DT-ARQ-TECH-001.md)**, the software is implemented under a unified **.NET** ecosystem:

* **Backend:** Modular Monolith on .NET 10 structured with Hexagonal Architecture (*Ports & Adapters*) and Domain-Driven Design (DDD).
* **Central Database:** PostgreSQL 18 + TimescaleDB extension (time series for telemetry). ISO 14224 taxonomic tree resolution is handled natively via recursive CTEs.
* **Mobile Field Client:** .NET MAUI Blazor Hybrid (Android/iOS) with encrypted local relational persistence via `sqlite-net-pcl` with SQLCipher (Offline-First).
* **Web Administrative Client:** Blazor Web App for HSEQ supervision, backlog planning, and control dashboards on desktop workstations.
* **Component Library:** Shared Razor components in a Razor Class Library (RCL) consuming Design System tokens.
* **Real-Time:** SignalR over WebSockets (WSS TLS 1.3) for LOTO safety heartbeat (2s) and process telemetry streaming.
* **IoT Ingestion:** Azure IoT Hub consuming industrial telemetry via MQTT from SCADA and exposing it to the backend via AMQP.
* **Local Orchestration & Testing:** .NET Aspire (`Dteam.AppHost`, `Dteam.ServiceDefaults`, `Aspire.Hosting.Testing`) for local development, OpenTelemetry tracing, and container-backed integration tests ([ADR-011](architecture/adr/ADR-011.md)).
* **Graphic Canvas:** 2D-First strategy based on interactive SVG vector floor plans ([ADR-001](architecture/adr/ADR-001.md)) with a roadmap towards 3D models.

---

## 3. Repository Structure

```text
adso-dteam-docs/
├── .agents/              # Agent skills for SDLC deep audits, UI coherence, and Use Case auditing
├── architecture/         # C4 views (Components & Deployment), ASRs, ADRs, DB guidelines, and Tech Stack Matrix
│   ├── adr/              # Architecture Decision Records (ADR-001 to ADR-011)
│   ├── asr/              # Architecturally Significant Requirements (ASR-001, ASR-002)
│   └── views/            # C4 Component (CMP) and Physical Deployment (DEP) Structurizr DSL models & specs
├── business-processes/   # BPMN 2.0 operational process flows (Draw.io)
├── compliance/           # Normative shield and ISO 14224 / ISO 55001 compliance justifications
├── domain-models/        # Tactical DDD modelling, ERD/DDL, Ubiquitous Language, and Use Cases
│   ├── class/            # Domain model specifications (DT-DM-DOC-001/002) and PlantUML class diagram
│   ├── entity-relationship/ # Physical data dictionary (DT-ERD-DOC-001), DBML, and PostgreSQL 18 DDL
│   ├── ubiquitous-language/ # Ubiquitous Language glossary (DT-UL-DOC-001)
│   └── use-cases/        # Formal use cases (17 MVP UC-*.md) and Master Traceability Matrix (DT-UC-TRC-001)
├── reports/              # Persisted screen, use-case, and repository audit reports
├── requirements/         # Software requirements and master sources
│   ├── common/           # Transversal Domain and Platform Requirements (TR-001 to TR-011)
│   ├── data/             # Master catalogs synchronized as CSVs (actors, SRS, stories, gherkin)
│   └── user-stories/     # Detailed user stories by module (ADM, INV, MTTO, VIS)
├── scripts/              # Generators (DDL, DBML, Structurizr, Tokens, Requirements), Notion importer, verifiers & plot_plan_generator/
├── TODO.md               # Engineering roadmap, milestone log, and pre-implementation backlog
└── ui-ux/                # User interface design and information architecture
    ├── assets/           # Generated tokens.css, MAI figures, icons-src/ SVGs & Affinity design sources
    ├── screens/          # 16 canonical screen specification blueprints (SCR-*.md)
    ├── DT-UI-DS-DOC-001  # Design Tokens, HPHMI principles, and Visual Style Guide
    ├── DT-UI-NAV-DOC-001 # Global Navigation Specification, Transition Matrix, and Safety Guards
    └── DT-UI-SVG-DOC-001 # Normative 7-Layer SVG Plot Plan Ingestion Contract (Rev 2.0)
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
