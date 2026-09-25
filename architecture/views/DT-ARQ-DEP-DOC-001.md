---
code: DT-ARQ-DEP-DOC-001
version: 1.3
date: 2026-09-25
status: Active
author: Juan David Julio Serrano
standard:
  - ISO/IEC 42010:2011 (Architecture — C4 Level 4 Views)
  - ISO 27001:2013 (Information Security)
---

# Deployment View Specification

## 1. Scope and Objective

This document defines the deployment topology for the Digital Twin MVP. It acts as the source of truth for the auto-generated Structurizr diagram (compiled to `DT-ARQ-DEP-001-deployment-model.dsl` using `scripts/generate_deployment_structurizr.py`), specifying the mapping of software containers to execution environments, network protocols, and cryptographic security boundaries.

> **Note:** The local control station (SCADA) is implemented as an internal Proof of Concept (PoC) to emulate industrial field instrumentation and validate asynchronous telemetry ingestion into Azure IoT Hub.

---

## 2. Hierarchical Node and Hosted Component Matrix

This matrix breaks down the physical infrastructure and software artifacts deployed in each execution environment according to the ISO/IEC 42010 standard (C4 Level 4 - Deployment).

| Parent Node ID | Node / Execution Environment | Stereotype / Platform | Component ID | Component Name | C4 Type | Technology / Runtime | Technical Responsibility |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| mobile_node | Mobile Device | Edge Node (Android / iOS Device) | mobile_app | Frontend App | Container | .NET MAUI Blazor Hybrid | Field touch execution and offline synchronization (TR-002, TR-007). |
| mobile_node | Mobile Device | Edge Node (Android / iOS Device) | loto_watchdog | LOTO Watchdog | Component | Background Thread (C#) | Continuous safety heartbeat monitoring (TR-010). |
| mobile_node | Mobile Device | Edge Node (Android / iOS Device) | local_db | Local DB | ContainerDb | SQLite (sqlite-net-pcl) | Local encrypted offline persistence on mobile device. |
| scada_node | Local Control Station | Edge Gateway (Industrial PC / SCADA) | scada_engine | Sensor Emulator | Component | SCADA Engine (C# / Python) | Instrumentation gateway; emulates and transmits sensor readings via MQTT. |
| workstation_node| Workstation | Client Node (Desktop PC / Web Browser) | admin_portal | Web Admin Portal | Container | Blazor Web App | Web administrative interface for HSEQ supervision, WOs, and KPI dashboards. |
| azure_cloud | Azure Cloud Platform | Managed Cloud Service (Azure Tenant) | iot_hub | Azure IoT Hub | Container | Azure IoT Hub Service | Managed broker for asynchronous high-frequency telemetry ingestion. |
| cloud_host | Cloud Host Server | Execution Environment (Linux VPS) | docker_engine | Docker Engine | Node | Docker Runtime | Hosts the backend containers and reverse proxy with isolation. |
| docker_engine | Docker Engine | Container Runtime (Linux VPS) | nginx_proxy | Nginx Reverse Proxy | Container | Nginx (Alpine Linux) | TLS 1.3 termination, reverse routing, and static web delivery. |
| docker_engine | Docker Engine | Container Runtime (Linux VPS) | backend_api | Backend API Monolith | Container | .NET 10 Web API Monolith | Modular monolith with DDD business logic and domain services. |
| db_server | Database Server | Database Node (Managed DB / Container) | postgres_db | PostgreSQL Master | ContainerDb | PostgreSQL 18 + TimescaleDB | Relational master store, immutable audit (ADR-003), and time series. |
| cache_server | Cache Server | In-Memory Node | redis_cache | Redis Cache | ContainerDb | Redis 7.x | Distributed in-memory datastore for idempotency caching keys (ADR-007). |

---

## 3. Connectivity and Network Protocol Matrix

This matrix specifies the point-to-point communication channels between software components across network boundaries.

| Source Component | Source Node | Destination Component | Destination Node | Protocol | Port / Channel | Encryption / Security | Purpose and Frequency |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| mobile_app | Mobile Device | local_db | Mobile Device | Direct IPC | Local File | AES-256 | Local offline transactional read and write (TR-002, TR-007). |
| loto_watchdog | Mobile Device | local_db | Mobile Device | Direct IPC | Local File | AES-256 | Write of Fail-Safe Preventive Security Lockout status. |
| mobile_app | Mobile Device | nginx_proxy | Cloud Host Server | HTTPS | Port 443 | TLS 1.3 / AES-256 | REST API synchronization transactions (local queues, JSON data). |
| loto_watchdog | Mobile Device | nginx_proxy | Cloud Host Server | WSS | Port 443 | WebSockets TLS 1.3 | Persistent safety Heartbeat channel (ping every 2s) for LOTO (TR-010). |
| scada_engine | Local Control Station| iot_hub | Azure Cloud Platform | MQTT | Port 8883 | TLS 1.3 | Continuous publication of real process telemetry from the plant. |
| iot_hub | Azure Cloud Platform | backend_api | Cloud Host Server | AMQP | Port 5671 | TLS 1.3 | Asynchronous and reliable consumption of queued industrial telemetry. |
| admin_portal | Workstation | nginx_proxy | Cloud Host Server | HTTPS | Port 443 | TLS 1.3 | Download of Blazor/.NET static resources and JSON API requests. |
| admin_portal | Workstation | nginx_proxy | Cloud Host Server | WSS | Port 443 | WebSockets TLS 1.3 | Real-time channel for telemetry updates and KPI Dashboard. |
| nginx_proxy | Cloud Host Server | backend_api | Cloud Host Server | HTTP | Docker Net | Isolated Internal Net | Internal routing of API requests and terminated WebSocket traffic. |
| backend_api | Cloud Host Server | postgres_db | Database Server | TCP/IP | Port 5432 | SSL / Private Net | Persistence operations via EF Core under Unit of Work pattern. |

---

## 4. Perimeter Security Mechanism: LOTO Watchdog (Fail-Safe)

To mitigate electromagnetic interference (EMI) in industrial plants that causes mobile network dropouts:

1. **Heartbeat Monitoring:** The native LOTO Watchdog thread on the mobile device validates the connection against the central server by sending a periodic ping over WebSockets (WSS).
2. **Tolerance Threshold and Grace Window:** To tolerate radio frequency attenuation (RF Shadowing) and roaming delays (AP Roaming) characteristic of metallic structures in refineries without generating false positives, a tolerance threshold of **30 seconds** (grace window) is established.
3. **Local Fail-Safe Action:** If the 30-second window expires without receiving a heartbeat:
   * If the device has an active Cryptographic LOTO Lease (Offline Lease according to ADR-006), it transitions to offline safe mode allowing step-by-step local verifications.
   * If there is no valid lease or it has expired, the Watchdog directly writes a **Preventive Security Lockout** status in the local SQLite database, freezing the technician's screen via the non-dismissible critical modal (--dt-z-modal-fail-safe: 1500).
4. **Interface Interruption:** The mobile application detects the local flag and locks the technician's work screen, preventing the transition to the IN_PROGRESS state until the connection is restored and the server re-confirms Zero Energy.
