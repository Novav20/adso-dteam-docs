---
code: DT-ARQ-DEP-DOC-001
version: 1.5
date: 2026-09-17
status: Vigente
author: Juan David Julio Serrano
standard:
  - ISO/IEC 42010:2011 (Arquitectura de Software)
  - ISO 9001:2015 (Control Documental)
  - ISO 45001:2018 (Cláusula 8.1 — LOTO & Fail-Safe)
  - ISO 27001:2022 (Seguridad en Redes y Cifrado)
---

# Especificación Técnica de Despliegue y Topología Física

## 1. Alcance y Objetivo

Este documento constituye la especificación técnica de la vista de despliegue físico (DT-ARQ-DEP-001) para el sistema DTEAM. Define la distribución jerárquica de nodos de ejecución, contenedores, topología de red, protocolos de comunicación y el mecanismo de seguridad perimetral Fail-Safe (LOTO Watchdog) en dispositivos móviles.

> **Nota:** La estación de control local (SCADA) se implementa como una Prueba de Concepto (PoC) interna para emular instrumentación industrial de campo y validar la ingesta asíncrona de telemetría hacia Azure IoT Hub.

---

## 2. Matriz Jerárquica de Nodos y Componentes Hospedados

Esta matriz desglosa la infraestructura física y los artefactos de software desplegados en cada entorno de ejecución conforme al estándar ISO/IEC 42010 (C4 Nivel 4 - Despliegue).

| ID Nodo Padre    | Nodo / Entorno de Ejecución | Estereotipo / Plataforma               | ID Componente | Nombre del Componente | Tipo C4     | Tecnología / Runtime        | Responsabilidad Técnica                                                       |
| :--------------- | :-------------------------- | :------------------------------------- | :------------ | :-------------------- | :---------- | :-------------------------- | :---------------------------------------------------------------------------- |
| mobile_node      | Mobile Device               | Edge Node (Android / iOS Device)       | mobile_app    | Frontend App          | Container   | .NET MAUI Blazor Hybrid     | Ejecución táctil en campo y sincronización offline (TR-002, TR-007).          |
| mobile_node      | Mobile Device               | Edge Node (Android / iOS Device)       | loto_watchdog | LOTO Watchdog         | Component   | Background Thread (C#)      | Monitoreo continuo de heartbeat de seguridad (TR-010).                        |
| mobile_node      | Mobile Device               | Edge Node (Android / iOS Device)       | local_db      | Local DB              | ContainerDb | SQLite (sqlite-net-pcl)     | Persistencia local cifrada offline en dispositivo móvil.                      |
| scada_node       | Local Control Station       | Edge Gateway (Industrial PC / SCADA)   | scada_engine  | Sensor Emulator       | Component   | SCADA Engine (C# / Python)  | Gateway de instrumentación; emula y transmite lecturas de sensores vía MQTT.  |
| workstation_node | Workstation                 | Client Node (Desktop PC / Web Browser) | admin_portal  | Web Admin Portal      | Container   | Blazor Web App              | Interfaz web administrativa para supervisión HSEQ, OTs y dashboards KPIs.     |
| azure_cloud      | Azure Cloud Platform        | Managed Cloud Service (Azure Tenant)   | iot_hub       | Azure IoT Hub         | Container   | Azure IoT Hub Service       | Bróker administrado para ingesta asíncrona de telemetría de alta frecuencia.  |
| cloud_host       | Cloud Host Server           | Execution Environment (Linux VPS)      | docker_engine | Docker Engine         | Node        | Docker Runtime              | Hospeda los contenedores del backend y proxy inverso con aislamiento.         |
| docker_engine    | Docker Engine               | Container Runtime (Linux VPS)          | nginx_proxy   | Nginx Reverse Proxy   | Container   | Nginx (Alpine Linux)        | Terminación TLS 1.3, enrutamiento inverso y entrega de estáticos web.         |
| docker_engine    | Docker Engine               | Container Runtime (Linux VPS)          | backend_api   | Backend API Monolith  | Container   | .NET 10 Web API Monolith    | Monolito modular con lógica de negocio DDD y servicios de dominio.            |
| db_server        | Database Server             | Database Node (Managed DB / Container) | postgres_db   | PostgreSQL Master     | ContainerDb | PostgreSQL 18 + TimescaleDB | Almacén maestro relacional, auditoría inmutable (ADR-003) y series de tiempo. |

---

## 3. Matriz de Conectividad y Protocolos de Red

Esta matriz especifica los canales de comunicación punto a punto entre los componentes de software a través de los límites de red.

| Componente Origen | Nodo Origen           | Componente Destino | Nodo Destino         | Protocolo  | Puerto / Canal | Cifrado / Seguridad | Propósito y Frecuencia                                                         |
| :---------------- | :-------------------- | :----------------- | :------------------- | :--------- | :------------- | :------------------ | :----------------------------------------------------------------------------- |
| mobile_app        | Mobile Device         | local_db           | Mobile Device        | Direct IPC | Archivo Local  | AES-256             | Lectura y escritura transaccional local offline (TR-002, TR-007).              |
| loto_watchdog     | Mobile Device         | local_db           | Mobile Device        | Direct IPC | Archivo Local  | AES-256             | Escritura de estado de Bloqueo Preventivo de Seguridad Fail-Safe.              |
| mobile_app        | Mobile Device         | nginx_proxy        | Cloud Host Server    | HTTPS      | Puerto 443     | TLS 1.3 / AES-256   | Transacciones de sincronización API REST (colas locales, datos JSON).          |
| loto_watchdog     | Mobile Device         | nginx_proxy        | Cloud Host Server    | WSS        | Puerto 443     | WebSockets TLS 1.3  | Canal persistente de Heartbeat de seguridad (ping cada 2s) para LOTO (TR-010). |
| scada_engine      | Local Control Station | iot_hub            | Azure Cloud Platform | MQTT       | Puerto 8883    | TLS 1.3             | Publicación continua de telemetría de proceso real desde planta.               |
| iot_hub           | Azure Cloud Platform  | backend_api        | Cloud Host Server    | AMQP       | Puerto 5671    | TLS 1.3             | Consumo asíncrono y confiable de telemetría industrial encolada.               |
| admin_portal      | Workstation           | nginx_proxy        | Cloud Host Server    | HTTPS      | Puerto 443     | TLS 1.3             | Descarga de recursos estáticos Blazor/.NET y peticiones API JSON.              |
| admin_portal      | Workstation           | nginx_proxy        | Cloud Host Server    | WSS        | Puerto 443     | WebSockets TLS 1.3  | Canal en tiempo real para actualización de telemetría y Dashboard de KPIs.     |
| nginx_proxy       | Cloud Host Server     | backend_api        | Cloud Host Server    | HTTP       | Red Docker     | Red Interna Aislada | Enrutamiento interno de peticiones API y tráfico WebSocket terminado.          |
| backend_api       | Cloud Host Server     | postgres_db        | Database Server      | TCP/IP     | Puerto 5432    | SSL / Red Privada   | Operaciones de persistencia vía EF Core bajo patrón Unit of Work.              |

---

## 4. Mecanismo de Seguridad Perimetral: LOTO Watchdog (Fail-Safe)

Para mitigar el ruido electromagnético (EMI) de las plantas industriales que ocasiona caídas en la red móvil:

1. **Monitoreo de Heartbeat:** El hilo nativo LOTO Watchdog en el dispositivo móvil valida la conexión contra el servidor central enviando un ping periódico sobre WebSockets (WSS).
2. **Umbral de Tolerancia y Ventana de Gracia:** Para tolerar la atenuación por radiofrecuencia (RF Shadowing) y los retardos de itinerancia (AP Roaming) característicos de estructuras metálicas en refinerías sin generar falsos positivos, se establece un umbral de tolerancia de **30 segundos** (ventana de gracia).
3. **Acción Fail-Safe Local:** Si se agota la ventana de 30 segundos sin recepción de latido:
   * Si el dispositivo cuenta con un Arrendamiento Criptográfico LOTO (Offline Lease conforme a ADR-006) vigente, transiciona a modo seguro fuera de línea permitiendo verificaciones locales paso a paso.
   * Si no existe un arrendamiento válido o ha expirado, el Watchdog escribe de forma directa un estado de **Bloqueo Preventivo de Seguridad** en la base de datos local SQLite, congelando la pantalla del técnico mediante el modal crítico no descartable (--dt-z-modal-fail-safe: 1500).
4. **Interrupción de Interfaz:** La aplicación móvil detecta la bandera local y bloquea la pantalla de trabajo del técnico, impidiendo la transición al estado IN_PROGRESS hasta que la conexión se restablezca y el servidor re-confirme la Energía Cero.
