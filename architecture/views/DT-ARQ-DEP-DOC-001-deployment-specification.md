---
code: DT-ARQ-DEP-DOC-001
version: 1.0
date: 2026-08-05
status: Especificación Técnica de Despliegue y Topología Física — MVP
author: Juan David Julio Serrano
standard:
  - ISO/IEC 42010:2011 (Arquitectura de Software)
  - ISO 9001:2015 (Control Documental)
  - ISO 45001:2018 (Cláusula 8.1 — LOTO & Fail-Safe)
  - ISO 27001:2022 (Seguridad en Redes y Cifrado)
---

# Especificación Técnica de Despliegue y Topología Física

## Alcance y Objetivo

Este documento constituye la especificación técnica de la vista de despliegue físico (`DT-ARQ-DEP-001`) para el sistema DTEAM. Define la distribución de nodos de ejecución, contenedores, topología de red, protocolos de comunicación y el mecanismo de seguridad perimetral _Fail-Safe_ (LOTO Watchdog) en dispositivos móviles.

---

## Matriz de Nodos de Ejecución e Infraestructura

| Nodo / Entorno             | Tipo de Nodo             | Componentes Hospedados                                | Responsabilidad Técnica                                                                                                          |
| :------------------------- | :----------------------- | :---------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| **Dispositivo Móvil**      | Edge Node (Android/iOS)  | .NET MAUI Blazor Hybrid, LOTO Watchdog, SQLite  | Ejecución táctil en campo, almacenamiento cifrado offline (`TR-002`, `TR-007`) y monitoreo de _heartbeat_ de seguridad.          |
| **Estación Control Local** | Edge Node (SCADA)        | SCADA Engine (Instrument Emulator)                    | Gateway de instrumentación de planta; emula y transmite variables físicas (vibración, temperatura, presión).                     |
| **Estación de Trabajo**    | Client Node (Web SPA)    | Web Admin Portal (Blazor Web App)                              | Interfaz administrativa para supervisión HSEQ, planificación de backlog y dashboards ejecutivos de KPIs.                         |
| **Azure Cloud Platform**   | Managed Cloud Ingestion  | Azure IoT Hub                                         | Bróker de mensajería IoT para ingesta asíncrona de telemetría industrial de alta frecuencia.                                     |
| **Servidor Cloud Host**    | Host Container Engine    | Nginx (Reverse Proxy), Backend API Monolith (.NET 10) | Hospedaje del contenedor monolítico .NET 10 y servidor Nginx para enrutamiento, terminación SSL y entrega de archivos estáticos. |
| **Servidor Base Datos**    | Managed/Containerized DB | PostgreSQL 16 + TimescaleDB Extension                 | Almacenamiento relacional de activos, inventario, auditoría inmutable (`ADR-003`) y series de tiempo para telemetría.            |

---

## Especificación de Red y Protocolos de Comunicación

| Origen                  | Destino           | Protocolo | Cifrado / Seguridad | Propósito y Frecuencia                                                              |
| :---------------------- | :---------------- | :-------- | :------------------ | :---------------------------------------------------------------------------------- |
| **SCADA Node**          | Azure IoT Hub     | `MQTT`    | TLS 1.3             | Publicación continua de lecturas de sensores físicos desde planta.                  |
| **Azure IoT Hub**       | Backend Monolith  | `AMQP`    | TLS 1.3             | Consumo asíncrono y confiable de eventos de telemetría encolados.                   |
| **Mobile / Web Client** | Nginx Proxy       | `HTTPS`   | TLS 1.3 / AES-256   | Transacciones REST API (sincronización de colas localDB, consultas JSON).           |
| **Mobile / Web Client** | Backend (SignalR) | `WSS`     | WebSockets TLS 1.3  | Canal bidireccional en tiempo real para _heartbeat_ de seguridad y KPIs (`TR-010`). |
| **Backend Monolith**    | PostgreSQL DB     | `TCP/IP`  | Red Privada / SSL   | Operaciones de persistencia vía EF Core bajo patrón _Unit of Work_.                 |

---

## Mecanismo de Seguridad Perimetral: LOTO Watchdog (Fail-Safe)

Para mitigar el ruido electromagnético (EMI) de las plantas industriales que ocasiona caídas en la red móvil:

1. **Monitoreo de Heartbeat:** El hilo nativo `LOTO Watchdog` en el dispositivo móvil valida la conexión contra el servidor central enviando un _ping_ cada 2 segundos sobre WebSockets (`WSS`).
2. **Umbral de Tolerancia:** Si se registran 3 fallos consecutivos de respuesta (ventana de 6 segundos), el Watchdog interrumpe el flujo normal.
3. **Acción Fail-Safe Local:** El Watchdog escribe de forma directa un estado de **Bloqueo Preventivo de Seguridad** en la base de datos local del teléfono.
4. **Interrupción de Interfaz:** La aplicación .NET MAUI Blazor Hybrid detecta la bandera local y bloquea la pantalla de trabajo del técnico, impidiendo la transición al estado `IN_PROGRESS` hasta que la conexión se restablezca y el servidor re-confirme la Energía Cero.
