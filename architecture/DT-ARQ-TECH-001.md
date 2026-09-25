---
code: DT-ARQ-TECH-001
version: 1.2
date: 2026-09-25
status: Active
author: Juan David Julio Serrano
---

# Technology Stack Traceability Matrix

## Purpose

This document is the consolidated source for identifying the target technology stack of DTEAM and linking it to the decisions, architecture views, and requirements that justify it. Active views must remain consistent with this matrix.

## Target Stack

| Layer | Target Technology | Main Use | Traceability |
| :--- | :--- | :--- | :--- |
| Mobile Client | .NET MAUI Blazor Hybrid | Field Android/iOS operation and offline-first experience | ADR-004, `TR-002`, `TR-007`, DT-ARQ-DEP-001 |
| Administrative Client | Blazor Web App | HSEQ supervision, planning, administration, and dashboards | ADR-004, DT-ARQ-CMP-001, DT-ARQ-DEP-001 |
| UI Components | Razor Components / Blazor (RCL) | HPHMI, forms, tables, shared states, and navigation | ADR-004, `TR-011` |
| Application Language | C# (.NET 10) | Client, shared services, domain, and backend | ADR-004 |
| Backend | .NET 10 / ASP.NET Core | API, DDD business rules, authentication, and processing | DT-ARQ-DEP-001 |
| Real-Time | SignalR over WSS | LOTO Heartbeat (2s), KPIs, and authorized notifications | `TR-010`, DT-ARQ-DEP-001 |
| API | HTTPS/JSON | Synchronization and client-server operations | `TR-005`, `TR-007`, DT-ARQ-DEP-001 |
| Mobile Persistence | `sqlite-net-pcl` + SQLCipher | Local state, offline queue (`TR-007`), and preventive block | `TR-002`, `TR-007`, ADR-004 |
| Distributed Cache | Redis 7.x | Fast-path idempotency caching for offline-sync retry storms | ADR-007, `TR-007`, DT-ARQ-DEP-001 |
| Central Database | PostgreSQL 18 + TimescaleDB | Assets, inventory, immutable audit, and time series | ADR-003, DT-ARQ-DEP-001 |
| IoT Ingestion | Azure IoT Hub | Industrial telemetry (MQTT from SCADA / AMQP to Backend) | DT-ARQ-DEP-001 |
| Infrastructure | Docker, Nginx, and Azure Cloud Services | Containers, reverse proxy, TLS 1.3, and deployment | DT-ARQ-DEP-001 |
| Visualization | 2D First model (SVG), 3D Evolutionary | Digital twin and operational context | ADR-001 |

## Consistency Rules

1. Active artifacts must use .NET MAUI Blazor Hybrid for the mobile client and Blazor Web App for the administrative client, sharing components via Razor Class Library (RCL).
2. Previous frontend technologies can only appear in historical records or superseded decisions, clearly identified as inactive.
3. Mobile persistence is formalized under `sqlite-net-pcl` with SQLCipher encryption; the use of Entity Framework Core on the mobile client is not allowed.
4. Stack changes must be recorded via a new ADR or an approved new version of ADR-004.
5. Draw.io diagram labels must match this matrix; diagram file names and view codes do not change due to the stack.

## Related Artifacts

- [[ADR-004|ADR-004: Frontend Client with .NET MAUI Blazor Hybrid]]
- [Component Model](views/DT-ARQ-CMP-001-component-model.drawio)
- [[DT-ARQ-CMP-DOC-001|Component Specification]]
- [Deployment Model](views/DT-ARQ-DEP-001-deployment-model.drawio)
- [[DT-ARQ-DEP-DOC-001|Deployment Specification]]
