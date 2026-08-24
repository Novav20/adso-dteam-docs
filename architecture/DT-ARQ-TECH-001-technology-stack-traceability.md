---
code: DT-ARQ-TECH-001
version: 1.0
date: 2026-08-24
status: Vigente
author: Juan David Julio Serrano
---

# Matriz de Trazabilidad del Stack Tecnológico

## Propósito

Este documento es la fuente consolidada para identificar el stack tecnológico objetivo de DTEAM y relacionarlo con las decisiones, vistas de arquitectura y requisitos que lo justifican. Las vistas vigentes deben mantenerse consistentes con esta matriz.

## Stack objetivo

| Capa | Tecnología objetivo | Uso principal | Trazabilidad |
| :--- | :--- | :--- | :--- |
| Cliente móvil | .NET MAUI Blazor Hybrid | Operación Android/iOS en campo y experiencia offline-first | ADR-004, `TR-002`, `TR-007`, DT-ARQ-DEP-001 |
| Cliente administrativo | Blazor Web App | Supervisión HSEQ, planificación, administración y dashboards | ADR-004, DT-ARQ-CMP-001, DT-ARQ-DEP-001 |
| Componentes de UI | Razor Components / Blazor | HPHMI, formularios, tablas, estados y navegación | ADR-004, `TR-011` |
| Lenguaje de aplicación | C# | Cliente, servicios compartidos y backend | ADR-004 |
| Backend | .NET 10 / ASP.NET Core | API, reglas de negocio, autenticación y procesamiento | DT-ARQ-DEP-001 |
| Tiempo real | SignalR sobre WSS | Heartbeat LOTO, KPIs y notificaciones autorizadas | `TR-010`, DT-ARQ-DEP-001 |
| API | HTTPS/JSON | Sincronización y operaciones cliente-servidor | `TR-005`, `TR-007`, DT-ARQ-DEP-001 |
| Persistencia móvil | SQLite compatible con .NET MAUI | Estado local, cola offline y bloqueo preventivo | `TR-002`, `TR-007`, ADR-004 |
| Base de datos central | PostgreSQL 16 + TimescaleDB | Activos, inventario, auditoría y series temporales | ADR-003, DT-ARQ-DEP-001 |
| Ingesta IoT | Azure IoT Hub | Telemetría industrial | DT-ARQ-DEP-001 |
| Infraestructura | Docker, Nginx y Azure Cloud Services | Contenedores, proxy, TLS y despliegue | DT-ARQ-DEP-001 |
| Visualización | Modelo 2D primero, 3D evolutivo | Gemelo digital y contexto operacional | ADR-001 |

## Reglas de consistencia

1. Los artefactos vigentes deben usar .NET MAUI Blazor Hybrid para el cliente móvil y Blazor Web App para el cliente administrativo.
2. Las tecnologías frontend anteriores solo pueden aparecer en registros históricos o decisiones superseded, identificadas claramente como no vigentes.
3. La solución concreta de SQLite debe actualizarse en esta matriz y en ADR-004 cuando se seleccione durante la implementación.
4. Los cambios del stack deben registrarse mediante un nuevo ADR o una nueva versión aprobada de ADR-004.
5. Las etiquetas de los diagramas Draw.io deben coincidir con esta matriz; los nombres de archivos de diagramas y códigos de vista no cambian por el stack.

## Artefactos relacionados

- [ADR-004: Cliente Frontend con .NET MAUI Blazor Hybrid](adr/ADR-004-DotNet-MAUI-Blazor-Hybrid.md)
- [Modelo de componentes](views/DT-ARQ-CMP-001-component-model.drawio)
- [Especificación de interfaces](views/DT-ARQ-CMP-DOC-001-architecture-interfaces-specification.md)
- [Modelo de despliegue](views/DT-ARQ-DEP-001-deployment-model.drawio)
- [Especificación de despliegue](views/DT-ARQ-DEP-DOC-001-deployment-specification.md)
