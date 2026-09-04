---
code: DT-ARQ-DEP-DOC-001
version: 1.3
date: 2026-09-04
status: Vigente
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

> **Nota:** La estación de control local (*Local Control Station / SCADA*) se implementa como una Prueba de Concepto (PoC) interna para emular instrumentación industrial de campo y validar la ingesta asíncrona de telemetría hacia Azure IoT Hub.

---

## Matriz de Nodos de Ejecución e Infraestructura

| Nodo / Entorno            | Tipo de Nodo / Estereotipo                           | Componentes Hospedados (Diagrama)                                                                                              | Responsabilidad Técnica                                                                                                                |
| :------------------------ | :--------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| **Mobile Device**         | «Edge Node»<br>[Android / iOS Device]                | • Frontend App (.NET MAUI Blazor Hybrid)<br>• LOTO Watchdog (Background Thread)<br>• Local DB (SQLite vía `sqlite-net-pcl`)    | Ejecución táctil en campo, persistencia local cifrada offline (`TR-002`, `TR-007`) y monitoreo de _heartbeat_ de seguridad.            |
| **Local Control Station** | «Edge Gateway»<br>[Industrial PC / SCADA Node]       | • Instrument/Sensor Emulator (SCADA Engine)                                                                                    | Gateway de instrumentación; emula y transmite lecturas de sensores físicos (vibración, presión, temperatura) vía MQTT.                 |
| **Workstation**           | «Client Node»<br>[Desktop PC / Web Browser]          | • Web Admin Portal (Blazor Web App)                                                                                            | Interfaz web administrativa para supervisión HSEQ, planificación de órdenes de trabajo y dashboards de KPIs.                           |
| **Azure Cloud Platform**  | «Managed Cloud Service»<br>[Azure Tenant]            | • Azure IoT Hub                                                                                                                | Bróker administrado para ingesta asíncrona y confiable de telemetría industrial de alta frecuencia.                                    |
| **Cloud Host Server**     | «Execution Environment»<br>[Linux VPS / Docker Host] | • Docker Engine<br>&nbsp;&nbsp;├─ Reverse Proxy & Static Files Server (Nginx)<br>&nbsp;&nbsp;└─ Backend API Monolith (.NET 10) | Hospeda los contenedores del monolito .NET 10 y Nginx para terminación TLS 1.3, enrutamiento inverso y entrega de estáticos Web.       |
| **Database Server**       | «Database Node»<br>[Managed DB / Container]          | • PostgreSQL 18 + TimescaleDB Extension                                                                                        | Almacén relacional maestro de activos, inventario, auditoría inmutable de solo inserción (`ADR-003`) y series de tiempo de telemetría. |

---

## Especificación de Red y Protocolos de Comunicación

| Origen                    | Destino           | Protocolo | Cifrado / Seguridad | Propósito y Frecuencia                                                                             |
| :------------------------ | :---------------- | :-------- | :------------------ | :------------------------------------------------------------------------------------------------- |
| **Local Control Station** | Azure IoT Hub     | `MQTT`    | TLS 1.3             | Publicación continua de telemetría de proceso real desde planta.                                   |
| **Azure IoT Hub**         | Backend Monolith  | `AMQP`    | TLS 1.3             | Consumo asíncrono y confiable de telemetría industrial encolada.                                   |
| **Mobile Device**         | Nginx Proxy       | `HTTPS`   | TLS 1.3 / AES-256   | Transacciones de sincronización API REST (colas locales, datos JSON).                              |
| **Mobile Device**         | Backend via Nginx | `WSS`     | WebSockets TLS 1.3  | Canal persistente para _Heartbeat_ bidireccional de seguridad (ping cada 2s) para LOTO (`TR-010`). |
| **Workstation**           | Nginx Proxy       | `HTTPS`   | TLS 1.3             | Descarga de recursos estáticos Blazor/.NET y peticiones API JSON.                                  |
| **Workstation**           | Backend via Nginx | `WSS`     | WebSockets TLS 1.3  | Canal en tiempo real para actualización de telemetría y Dashboard de KPIs.                         |
| **Nginx Proxy**           | Backend Monolith  | `HTTP`    | Red Interna Docker  | Enrutamiento interno de peticiones API y tráfico WebSocket.                                        |
| **Backend Monolith**      | Database Server   | `TCP/IP`  | Red Privada / SSL   | Operaciones de persistencia vía EF Core bajo patrón _Unit of Work_.                                |

---

## Mecanismo de Seguridad Perimetral: LOTO Watchdog (Fail-Safe)

Para mitigar el ruido electromagnético (EMI) de las plantas industriales que ocasiona caídas en la red móvil:

1. **Monitoreo de Heartbeat:** El hilo nativo `LOTO Watchdog` en el dispositivo móvil valida la conexión contra el servidor central enviando un _ping_ cada 2 segundos sobre WebSockets (`WSS`).
2. **Umbral de Tolerancia y Calidad de Señal:** Si se registran 3 fallos consecutivos de respuesta (ventana de $>6.0\text{ segundos}$), o si la trama de telemetría entrante reporta explícitamente una calidad de señal *"Bad/Failure"* desde el instrumento, el Watchdog interrumpe inmediatamente el flujo normal, asumiendo un estado de peligro preventivo.
3. **Acción Fail-Safe Local:** El Watchdog escribe de forma directa un estado de **Bloqueo Preventivo de Seguridad** en la base de datos local SQLite del dispositivo, garantizando inmutabilidad local de la interrupción.
4. **Interrupción de Interfaz:** La aplicación .NET MAUI Blazor Hybrid detecta la bandera local y bloquea la pantalla de trabajo del técnico, impidiendo la transición al estado `IN_PROGRESS` hasta que la conexión se restablezca y el servidor re-confirme la Energía Cero.
