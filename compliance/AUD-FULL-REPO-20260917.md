---
code: AUD-FULL-REPO-20260917
date: 2026-09-17 15:28
scope: Repositorio completo
---

# Auditoría Completa del Repositorio — DTEAM

**Fecha:** 2026-09-17 15:28  
**Artefactos auditados:** 98  
**Total BLOCKERs:** 37

---

## 🔴 `README.md`
*1 BLOCKER | 0 WARNING | 0 INFO*

- **[BLOCKER][B-SCP01]** *(línea 49)* Caso de uso `UC-TRC-001` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.

## ⚠️ `architecture/DT-ARQ-DB-DOC-001.md`
*0 BLOCKER | 3 WARNING | 2 INFO*

- **[WARNING][W-TR01]** *(línea 76)* Requisito Arquitectónicamente Significativo `ASR-2` referenciado pero no se encontró su archivo. Verificar nombre.
- **[INFO][I-NRM01]** Estándar `ISO/IEC 42010:2011` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `PostgreSQL 18.x Documentation` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Regla / Elemento`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Justificación Técnica / Norma`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `architecture/DT-ARQ-TECH-001.md`
*0 BLOCKER | 26 WARNING | 0 INFO*

- **[WARNING][W-NRM01]** *(línea 36)* Tecnología no aprobada encontrada: EF Core en móvil (prohibido — usar sqlite-net-pcl). Verificar contra DT-ARQ-TECH-001 y ADR-004.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Cliente móvil`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Cliente administrativo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `planificación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `administración y dashboards`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Componentes de UI`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `HPHMI`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `formularios`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `tablas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `estados y navegación compartida`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Lenguaje de aplicación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Cliente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `servicios compartidos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `dominio y backend`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Backend`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `reglas de negocio DDD`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `autenticación y procesamiento`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Tiempo real`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `Persistencia móvil`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Base de datos central`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP20]** Posible rol no definido en la Matriz RBAC: `Activos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP21]** Posible rol no definido en la Matriz RBAC: `inventario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP22]** Posible rol no definido en la Matriz RBAC: `Ingesta IoT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP23]** Posible rol no definido en la Matriz RBAC: `Infraestructura`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP24]** Posible rol no definido en la Matriz RBAC: `Visualización`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP25]** Posible rol no definido en la Matriz RBAC: `Gemelo digital y contexto operacional`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `architecture/adr/ADR-001.md`
*0 BLOCKER | 1 WARNING | 3 INFO*

- **[WARNING][W-TR01]** *(línea 17)* Requisito Arquitectónicamente Significativo `ASR-1` referenciado pero no se encontró su archivo. Verificar nombre.
- **[INFO][I-NRM01]** Estándar `"[[VIS-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[VIS-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `"[[UC-VIS-033]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.

## ℹ️ `architecture/adr/ADR-002.md`
*0 BLOCKER | 0 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[MTTO-026]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[UC-MTTO-026]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.

## ℹ️ `architecture/adr/ADR-003.md`
*0 BLOCKER | 0 WARNING | 3 INFO*

- **[INFO][I-NRM01]** Estándar `"[[ADM-032]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[UC-ADM-032]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `"[[TR-001]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.

## ⚠️ `architecture/adr/ADR-004.md`
*0 BLOCKER | 3 WARNING | 3 INFO*

- **[WARNING][W-NRM01]** *(línea 8)* Tecnología no aprobada encontrada: React (frontend no aprobado — usar Blazor). Verificar contra DT-ARQ-TECH-001 y ADR-004.
- **[WARNING][W-NRM05]** *(línea 8)* Tecnología no aprobada encontrada: React Native (plataforma no aprobada — usar .NET MAUI). Verificar contra DT-ARQ-TECH-001 y ADR-004.
- **[WARNING][W-NRM07]** *(línea 26)* Tecnología no aprobada encontrada: EF Core en móvil (prohibido — usar sqlite-net-pcl). Verificar contra DT-ARQ-TECH-001 y ADR-004.
- **[INFO][I-NRM01]** Estándar `DT-ARQ-CMP-001` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `DT-ARQ-DEP-001` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `DT-ARQ-TECH-001` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.

## ℹ️ `architecture/adr/ADR-005.md`
*0 BLOCKER | 0 WARNING | 3 INFO*

- **[INFO][I-NRM01]** Estándar `"DT-ARQ-DB-DOC-001"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"ADR-003"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `"ADM-032"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.

## ℹ️ `architecture/adr/ADR-006.md`
*0 BLOCKER | 0 WARNING | 5 INFO*

- **[INFO][I-NRM01]** Estándar `"DT-ARQ-ASR-001"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"TR-007"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `"INV-006"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM04]** Estándar `"VIS-011"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM05]** Estándar `"DT-ARQ-DB-DOC-001"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.

## ℹ️ `architecture/patterns/DT-ARQ-PAT-DOC-001.md`
*0 BLOCKER | 0 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `Domain-Driven Design` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `Clean Architecture / Hexagonal Architecture` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.

## 🔴 `architecture/views/DT-ARQ-CMP-DOC-001.md`
*2 BLOCKER | 62 WARNING | 4 INFO*

- **[BLOCKER][B-NRM01]** *(línea 101)* Nivel ISA-101 `L6` no válido. Solo se permiten L1, L2, L3 y L4 según DT-UI-NAV-DOC-001.
- **[BLOCKER][B-NRM02]** *(línea 103)* Nivel ISA-101 `L5` no válido. Solo se permiten L1, L2, L3 y L4 según DT-UI-NAV-DOC-001.
- **[INFO][I-NRM01]** Estándar `ISO/IEC 42010:2011` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `ISO 9001:2015` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `ISO 55001:2014` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM04]** Estándar `Domain-Driven Design / Arquitectura Hexagonal` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `ID Componente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Responsabilidad Técnica`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Mobile App`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Web Admin Portal`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Blazor Web App`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Idempotency Filter`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `IActionFilter`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `REST API Controllers`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Minimal APIs`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `SignalR Hub`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `SignalR.Hub`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Driving Adapter`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Background Sync Worker`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `IHostedService`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Taxonomy Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `ITaxonomyService`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Maintenance Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `IWorkOrderService`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Inventory Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP20]** Posible rol no definido en la Matriz RBAC: `IInventoryService`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP21]** Posible rol no definido en la Matriz RBAC: `ILotoService`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP22]** Posible rol no definido en la Matriz RBAC: `Security Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP23]** Posible rol no definido en la Matriz RBAC: `ISecurityService`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP24]** Posible rol no definido en la Matriz RBAC: `RIME Calculator`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP25]** Posible rol no definido en la Matriz RBAC: `IRimeCalculator`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP26]** Posible rol no definido en la Matriz RBAC: `Event Bus Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP27]** Posible rol no definido en la Matriz RBAC: `IEventBus`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP28]** Posible rol no definido en la Matriz RBAC: `Asset Repository Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP29]** Posible rol no definido en la Matriz RBAC: `IEquipmentRepository`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP30]** Posible rol no definido en la Matriz RBAC: `Maintenance Repository Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP31]** Posible rol no definido en la Matriz RBAC: `IWorkOrderRepository`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP32]** Posible rol no definido en la Matriz RBAC: `Inventory Repository Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP33]** Posible rol no definido en la Matriz RBAC: `IInventoryRepository`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP34]** Posible rol no definido en la Matriz RBAC: `Audit Repository Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP35]** Posible rol no definido en la Matriz RBAC: `ISecurityRepository`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP36]** Posible rol no definido en la Matriz RBAC: `Notification Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP37]** Posible rol no definido en la Matriz RBAC: `INotificationPort`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP38]** Posible rol no definido en la Matriz RBAC: `Telemetry Port`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP39]** Posible rol no definido en la Matriz RBAC: `ITelemetryPort`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP40]** Posible rol no definido en la Matriz RBAC: `EF Core PostgreSQL Adapter`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP41]** Posible rol no definido en la Matriz RBAC: `PostgresDbContext`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP42]** Posible rol no definido en la Matriz RBAC: `SignalR Broadcaster`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP43]** Posible rol no definido en la Matriz RBAC: `PostgreSQL Master`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP44]** Posible rol no definido en la Matriz RBAC: `Relational Database`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP45]** Posible rol no definido en la Matriz RBAC: `Azure IoT Hub`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP46]** Posible rol no definido en la Matriz RBAC: `Cloud Broker`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP47]** Posible rol no definido en la Matriz RBAC: `Redis Cache`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP48]** Posible rol no definido en la Matriz RBAC: `SCADA Control Station`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP49]** Posible rol no definido en la Matriz RBAC: `Edge Device`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP50]** Posible rol no definido en la Matriz RBAC: `Origen`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP51]** Posible rol no definido en la Matriz RBAC: `Protocolo / Interfaz`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP52]** Posible rol no definido en la Matriz RBAC: `HTTPS / JSON`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP54]** Posible rol no definido en la Matriz RBAC: `MQTT/AMQP`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP55]** Posible rol no definido en la Matriz RBAC: `AMQP`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP56]** Posible rol no definido en la Matriz RBAC: `Invoca autorización e IAM`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP57]** Posible rol no definido en la Matriz RBAC: `Calcula determinísticamente la prioridad RIME`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP58]** Posible rol no definido en la Matriz RBAC: `Persiste estructuras taxonómicas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP59]** Posible rol no definido en la Matriz RBAC: `Persiste movimientos de stock`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP60]** Posible rol no definido en la Matriz RBAC: `Suscribe requerimientos de energía física`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP61]** Posible rol no definido en la Matriz RBAC: `Implementa difusión vía Microsoft.AspNetCore.SignalR`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP62]** Posible rol no definido en la Matriz RBAC: `Módulo / Puerto`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP63]** Posible rol no definido en la Matriz RBAC: `Requisito / US`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `architecture/views/DT-ARQ-DEP-DOC-001.md`
*0 BLOCKER | 29 WARNING | 3 INFO*

- **[INFO][I-NRM01]** Estándar `ISO/IEC 42010:2011` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `ISO 9001:2015` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `ISO 27001:2022` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `ID Nodo Padre`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Estereotipo / Plataforma`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Nombre del Componente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Mobile Device`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Frontend App`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `LOTO Watchdog`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Local DB`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Local Control Station`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Sensor Emulator`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Workstation`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Web Admin Portal`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Blazor Web App`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Azure Cloud Platform`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Azure IoT Hub`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Azure IoT Hub Service`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `Cloud Host Server`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Docker Engine`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP20]** Posible rol no definido en la Matriz RBAC: `Docker Runtime`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP22]** Posible rol no definido en la Matriz RBAC: `Nginx Reverse Proxy`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP24]** Posible rol no definido en la Matriz RBAC: `Backend API Monolith`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP25]** Posible rol no definido en la Matriz RBAC: `Database Server`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP26]** Posible rol no definido en la Matriz RBAC: `PostgreSQL Master`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP27]** Posible rol no definido en la Matriz RBAC: `Componente Origen`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP28]** Posible rol no definido en la Matriz RBAC: `Componente Destino`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP29]** Posible rol no definido en la Matriz RBAC: `Protocolo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP30]** Posible rol no definido en la Matriz RBAC: `Cifrado / Seguridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP33]** Posible rol no definido en la Matriz RBAC: `Archivo Local`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP51]** Posible rol no definido en la Matriz RBAC: `Red Docker`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP54]** Posible rol no definido en la Matriz RBAC: `SSL / Red Privada`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/class/DT-DM-DOC-001.md`
*0 BLOCKER | 187 WARNING | 4 INFO*

- **[WARNING][W-NRM01]** *(línea 163)* Tecnología no aprobada encontrada: Angular (frontend no aprobado — usar Blazor). Verificar contra DT-ARQ-TECH-001 y ADR-004.
- **[INFO][I-NRM01]** Estándar `ISO 9001:2015` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `ISO 55000-Series` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `ISO 13374-Series` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM04]** Estándar `ISO 27001:2022` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Entidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Justificación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `FunctionalLocation`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `EquipmentClass`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `EquipmentUnit`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Subunit`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `MaintainableItem`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `WorkRequest`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `MaintenancePlan`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `WorkOrder`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Posee la ejecución`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `el historial`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `MediaAttachment`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `WorkOrderHistory`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `FailureRecord`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `BacklogItem`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `SparePart`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `InventoryTransaction`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `órdenes de trabajo y almacenes`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP20]** Posible rol no definido en la Matriz RBAC: `Warehouse`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP21]** Posible rol no definido en la Matriz RBAC: `Supplier`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP22]** Posible rol no definido en la Matriz RBAC: `Posee la identidad de adquisiciones`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP23]** Posible rol no definido en la Matriz RBAC: `MeshMapping`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP24]** Posible rol no definido en la Matriz RBAC: `TelemetrySignal`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP25]** Posible rol no definido en la Matriz RBAC: `WorkPermit`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP26]** Posible rol no definido en la Matriz RBAC: `IsolationPoint`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP27]** Posible rol no definido en la Matriz RBAC: `VisualLayer`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP28]** Posible rol no definido en la Matriz RBAC: `SpatialMetadata`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP29]** Posible rol no definido en la Matriz RBAC: `User`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP30]** Posible rol no definido en la Matriz RBAC: `WorkOrderIsolation`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP31]** Posible rol no definido en la Matriz RBAC: `Role`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP32]** Posible rol no definido en la Matriz RBAC: `Permission`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP33]** Posible rol no definido en la Matriz RBAC: `AuthToken`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP34]** Posible rol no definido en la Matriz RBAC: `uso y caducidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP35]** Posible rol no definido en la Matriz RBAC: `WorkOrderAssignment`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP36]** Posible rol no definido en la Matriz RBAC: `AuditLog`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP37]** Posible rol no definido en la Matriz RBAC: `MaterialRequirement`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP38]** Posible rol no definido en la Matriz RBAC: `DOWN`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP39]** Posible rol no definido en la Matriz RBAC: `STANDBY`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP40]** Posible rol no definido en la Matriz RBAC: `INSTALLED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP41]** Posible rol no definido en la Matriz RBAC: `COMMISSIONING`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP42]** Posible rol no definido en la Matriz RBAC: `DECOMMISSIONED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP43]** Posible rol no definido en la Matriz RBAC: `OPERATIONAL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP44]** Posible rol no definido en la Matriz RBAC: `Clase de Trabajo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP45]** Posible rol no definido en la Matriz RBAC: `Emergencia de Seguridad o Ambiental`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP46]** Posible rol no definido en la Matriz RBAC: `Mantenimiento Preventivo Sistemático`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP47]** Posible rol no definido en la Matriz RBAC: `Inspección de vibraciones`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP48]** Posible rol no definido en la Matriz RBAC: `termografía planificada`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP49]** Posible rol no definido en la Matriz RBAC: `Trabajo Correctivo No Crítico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP50]** Posible rol no definido en la Matriz RBAC: `Trabajo por Conveniencia Operativa`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP51]** Posible rol no definido en la Matriz RBAC: `CYCLES`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP52]** Posible rol no definido en la Matriz RBAC: `Norma / Concepto`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP53]** Posible rol no definido en la Matriz RBAC: `TEMPERATURE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP54]** Posible rol no definido en la Matriz RBAC: `Sensor de Temperatura`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP55]** Posible rol no definido en la Matriz RBAC: `PRESSURE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP56]** Posible rol no definido en la Matriz RBAC: `Sensor de Presión`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP57]** Posible rol no definido en la Matriz RBAC: `VIBRATION`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP58]** Posible rol no definido en la Matriz RBAC: `Análisis de Vibraciones`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP59]** Posible rol no definido en la Matriz RBAC: `Medición de caudal o flujo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP60]** Posible rol no definido en la Matriz RBAC: `VOLTAGE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP61]** Posible rol no definido en la Matriz RBAC: `Sensor de Tensión`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP62]** Posible rol no definido en la Matriz RBAC: `Tacómetro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP64]** Posible rol no definido en la Matriz RBAC: `VISIBLE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP65]** Posible rol no definido en la Matriz RBAC: `HIDDEN`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP66]** Posible rol no definido en la Matriz RBAC: `GHOSTED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP68]** Posible rol no definido en la Matriz RBAC: `ASSETS`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP69]** Posible rol no definido en la Matriz RBAC: `Dominio de Activos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP70]** Posible rol no definido en la Matriz RBAC: `MAINTENANCE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP71]** Posible rol no definido en la Matriz RBAC: `Dominio de Mantenimiento`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP72]** Posible rol no definido en la Matriz RBAC: `INVENTORY`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP73]** Posible rol no definido en la Matriz RBAC: `Dominio de Inventario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP74]** Posible rol no definido en la Matriz RBAC: `SAFETY`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP75]** Posible rol no definido en la Matriz RBAC: `Dominio de Seguridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP76]** Posible rol no definido en la Matriz RBAC: `SYSTEM`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP77]** Posible rol no definido en la Matriz RBAC: `Dominio IAM`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP78]** Posible rol no definido en la Matriz RBAC: `Norma de Referencia`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP80]** Posible rol no definido en la Matriz RBAC: `DEGRADED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP81]** Posible rol no definido en la Matriz RBAC: `FAILED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP82]** Posible rol no definido en la Matriz RBAC: `El componente está siendo mantenido`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP83]** Posible rol no definido en la Matriz RBAC: `reparado o reemplazado activamente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP84]** Posible rol no definido en la Matriz RBAC: `REPLACED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP85]** Posible rol no definido en la Matriz RBAC: `Historial de Confiabilidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP87]** Posible rol no definido en la Matriz RBAC: `Admisión básica de CMMS`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP88]** Posible rol no definido en la Matriz RBAC: `APPROVED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP89]** Posible rol no definido en la Matriz RBAC: `Transición a planificación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP90]** Posible rol no definido en la Matriz RBAC: `REJECTED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP92]** Posible rol no definido en la Matriz RBAC: `DRAFT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP93]** Posible rol no definido en la Matriz RBAC: `Control documental`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP94]** Posible rol no definido en la Matriz RBAC: `ACTIVE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP95]** Posible rol no definido en la Matriz RBAC: `Operativo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP96]** Posible rol no definido en la Matriz RBAC: `INACTIVE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP97]** Posible rol no definido en la Matriz RBAC: `Suspensión de ciclos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP98]** Posible rol no definido en la Matriz RBAC: `ARCHIVED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP100]** Posible rol no definido en la Matriz RBAC: `PREVENTIVE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP101]** Posible rol no definido en la Matriz RBAC: `PREDICTIVE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP103]** Posible rol no definido en la Matriz RBAC: `PLANNING`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP104]** Posible rol no definido en la Matriz RBAC: `SCHEDULED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP105]** Posible rol no definido en la Matriz RBAC: `COMPLETE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP106]** Posible rol no definido en la Matriz RBAC: `CLOSED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP108]** Posible rol no definido en la Matriz RBAC: `CORRECTIVE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP111]** Posible rol no definido en la Matriz RBAC: `IMPROVEMENT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP112]** Posible rol no definido en la Matriz RBAC: `Gestión de Cambios / Ingeniería`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP114]** Posible rol no definido en la Matriz RBAC: `EMERGENCY`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP115]** Posible rol no definido en la Matriz RBAC: `Criticidad Máxima`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP116]** Posible rol no definido en la Matriz RBAC: `URGENT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP117]** Posible rol no definido en la Matriz RBAC: `Prioridad Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP118]** Posible rol no definido en la Matriz RBAC: `NORMAL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP119]** Posible rol no definido en la Matriz RBAC: `Prioridad Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP120]** Posible rol no definido en la Matriz RBAC: `Prioridad Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP122]** Posible rol no definido en la Matriz RBAC: `PENDING`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP123]** Posible rol no definido en la Matriz RBAC: `Cola de planificación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP124]** Posible rol no definido en la Matriz RBAC: `READY`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP125]** Posible rol no definido en la Matriz RBAC: `Listo para programar`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP126]** Posible rol no definido en la Matriz RBAC: `DEFERRED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP127]** Posible rol no definido en la Matriz RBAC: `Suspensión en cola`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP130]** Posible rol no definido en la Matriz RBAC: `Gestión de Stock`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP131]** Posible rol no definido en la Matriz RBAC: `OBSOLETE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP132]** Posible rol no definido en la Matriz RBAC: `SUSPENDED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP133]** Posible rol no definido en la Matriz RBAC: `Control de Calidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP135]** Posible rol no definido en la Matriz RBAC: `RECEIPT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP136]** Posible rol no definido en la Matriz RBAC: `Ingesta de Stock`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP137]** Posible rol no definido en la Matriz RBAC: `ISSUE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP138]** Posible rol no definido en la Matriz RBAC: `Carga a Costos de OT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP139]** Posible rol no definido en la Matriz RBAC: `ADJUSTMENT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP140]** Posible rol no definido en la Matriz RBAC: `Conciliación de Inventario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP142]** Posible rol no definido en la Matriz RBAC: `MAPPED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP143]** Posible rol no definido en la Matriz RBAC: `Vinculación Digital`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP144]** Posible rol no definido en la Matriz RBAC: `UNMAPPED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP145]** Posible rol no definido en la Matriz RBAC: `Gemelo Incompleto`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP147]** Posible rol no definido en la Matriz RBAC: `Entrada a tanques`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP148]** Posible rol no definido en la Matriz RBAC: `ELECTRICAL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP149]** Posible rol no definido en la Matriz RBAC: `Riesgo Eléctrico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP150]** Posible rol no definido en la Matriz RBAC: `EXCAVATION`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP151]** Posible rol no definido en la Matriz RBAC: `CHEMICAL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP152]** Posible rol no definido en la Matriz RBAC: `Riesgo Químico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP155]** Posible rol no definido en la Matriz RBAC: `Ciclo de Autorización`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP159]** Posible rol no definido en la Matriz RBAC: `Permiso Activo / FSM Trigger`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP160]** Posible rol no definido en la Matriz RBAC: `EXPIRED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP161]** Posible rol no definido en la Matriz RBAC: `Control de Riesgos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP162]** Posible rol no definido en la Matriz RBAC: `REVOKED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP163]** Posible rol no definido en la Matriz RBAC: `Intervención de Emergencia`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP165]** Posible rol no definido en la Matriz RBAC: `Cierre de Operación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP168]** Posible rol no definido en la Matriz RBAC: `MECHANICAL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP169]** Posible rol no definido en la Matriz RBAC: `LOTO Mecánico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP170]** Posible rol no definido en la Matriz RBAC: `PNEUMATIC`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP171]** Posible rol no definido en la Matriz RBAC: `LOTO Neumático`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP172]** Posible rol no definido en la Matriz RBAC: `HYDRAULIC`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP173]** Posible rol no definido en la Matriz RBAC: `LOTO Hidráulico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP175]** Posible rol no definido en la Matriz RBAC: `LOTO Químico / Proceso`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP176]** Posible rol no definido en la Matriz RBAC: `THERMAL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP177]** Posible rol no definido en la Matriz RBAC: `LOTO Térmico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP178]** Posible rol no definido en la Matriz RBAC: `GRAVITATIONAL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP179]** Posible rol no definido en la Matriz RBAC: `LOTO de Gravedad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP182]** Posible rol no definido en la Matriz RBAC: `Ciclo de Vida de Cuenta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP185]** Posible rol no definido en la Matriz RBAC: `LOCKED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP186]** Posible rol no definido en la Matriz RBAC: `Mitigación de Fuerza Bruta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP188]** Posible rol no definido en la Matriz RBAC: `TECHNICIAN`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP189]** Posible rol no definido en la Matriz RBAC: `Ejecución Técnica`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP190]** Posible rol no definido en la Matriz RBAC: `Responsable de Línea`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP191]** Posible rol no definido en la Matriz RBAC: `PLANNER`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP192]** Posible rol no definido en la Matriz RBAC: `Ingeniería de Mantenimiento`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP194]** Posible rol no definido en la Matriz RBAC: `CREATE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP195]** Posible rol no definido en la Matriz RBAC: `UPDATE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP196]** Posible rol no definido en la Matriz RBAC: `DELETE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP198]** Posible rol no definido en la Matriz RBAC: `UNDETERMINED`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP199]** Posible rol no definido en la Matriz RBAC: `GOOD`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP200]** Posible rol no definido en la Matriz RBAC: `FAIR`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP201]** Posible rol no definido en la Matriz RBAC: `SERIOUS`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP202]** Posible rol no definido en la Matriz RBAC: `CRITICAL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP204]** Posible rol no definido en la Matriz RBAC: `SEVERE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP205]** Posible rol no definido en la Matriz RBAC: `MODERATE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP206]** Posible rol no definido en la Matriz RBAC: `UNKNOWN`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP208]** Posible rol no definido en la Matriz RBAC: `INSPECTION`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP209]** Posible rol no definido en la Matriz RBAC: `OTHER`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP211]** Posible rol no definido en la Matriz RBAC: `RUNNING`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP212]** Posible rol no definido en la Matriz RBAC: `IDLE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP213]** Posible rol no definido en la Matriz RBAC: `TESTING`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP215]** Posible rol no definido en la Matriz RBAC: `Referencia / Marco`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP218]** Posible rol no definido en la Matriz RBAC: `Calibración de instrumentos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP219]** Posible rol no definido en la Matriz RBAC: `lazos de control y automatización/PLCs`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP220]** Posible rol no definido en la Matriz RBAC: `LUBRICATION`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP221]** Posible rol no definido en la Matriz RBAC: `ELECTRONICS`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP222]** Posible rol no definido en la Matriz RBAC: `Soldadura`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP223]** Posible rol no definido en la Matriz RBAC: `pailería`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP224]** Posible rol no definido en la Matriz RBAC: `calderería y reparaciones estructurales`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP225]** Posible rol no definido en la Matriz RBAC: `FACILITIES`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/class/DT-DM-DOC-002.md`
*0 BLOCKER | 3 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `ISO 9001:2015` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `Domain-Driven Design` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Método`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Soporte Transversal`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Vincula un rol al usuario`. Verificar contra SCR-ADM-013 o si es un alias.

## 🔴 `domain-models/entity-relationship/DT-ERD-DOC-001.md`
*2 BLOCKER | 72 WARNING | 5 INFO*

- **[BLOCKER][B-NRM01]** *(línea 85)* Nivel ISA-101 `L6` no válido. Solo se permiten L1, L2, L3 y L4 según DT-UI-NAV-DOC-001.
- **[BLOCKER][B-NRM02]** *(línea 85)* Nivel ISA-101 `L8` no válido. Solo se permiten L1, L2, L3 y L4 según DT-UI-NAV-DOC-001.
- **[INFO][I-NRM01]** Estándar `ISO 9001:2015` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `PostgreSQL 18.x Documentation` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `DT-ERD-LOG-001` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM04]** Estándar `DT-DM-DOC-001` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM05]** Estándar `DT-ARQ-DB-DOC-001` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Campo Físico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Nulabilidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Justificación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `UUID`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `NOT NULL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `NULL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Descripción de la clase`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Referencia de estandarización`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Procedencia del activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `Identificación del tipo de activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `DATE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP20]** Posible rol no definido en la Matriz RBAC: `Cronología de adquisiciones`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP26]** Posible rol no definido en la Matriz RBAC: `La instalación puede estar pendiente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP28]** Posible rol no definido en la Matriz RBAC: `BIGINT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP29]** Posible rol no definido en la Matriz RBAC: `Seguimiento de confiabilidad y uso`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP34]** Posible rol no definido en la Matriz RBAC: `Vocabulario de estado operativo controlado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP38]** Posible rol no definido en la Matriz RBAC: `BOOLEAN`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP40]** Posible rol no definido en la Matriz RBAC: `UNIQUE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP50]** Posible rol no definido en la Matriz RBAC: `Texto explicativo opcional`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP52]** Posible rol no definido en la Matriz RBAC: `Vocabulario de prioridad controlado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP54]** Posible rol no definido en la Matriz RBAC: `Contexto físico de la ubicación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP56]** Posible rol no definido en la Matriz RBAC: `SMALLINT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP64]** Posible rol no definido en la Matriz RBAC: `Identidad del ítem mantenible`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP66]** Posible rol no definido en la Matriz RBAC: `Clasificación taxonómica`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP68]** Posible rol no definido en la Matriz RBAC: `JSONB`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP76]** Posible rol no definido en la Matriz RBAC: `Taxonomía del subcomponente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP78]** Posible rol no definido en la Matriz RBAC: `Etiqueta del subcomponente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP110]** Posible rol no definido en la Matriz RBAC: `Cadencia controlada del plan`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP124]** Posible rol no definido en la Matriz RBAC: `Ubicación de la evidencia`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP126]** Posible rol no definido en la Matriz RBAC: `Formato de archivo adjunto controlado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP127]** Posible rol no definido en la Matriz RBAC: `TIMESTAMP`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP136]** Posible rol no definido en la Matriz RBAC: `Tiempo de transición`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP151]** Posible rol no definido en la Matriz RBAC: `Inicio planeado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP153]** Posible rol no definido en la Matriz RBAC: `Inicio real de la ejecución`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP155]** Posible rol no definido en la Matriz RBAC: `Finalización real de la ejecución`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP164]** Posible rol no definido en la Matriz RBAC: `Narrativa de la solicitud`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP168]** Posible rol no definido en la Matriz RBAC: `Origen de la solicitud`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP181]** Posible rol no definido en la Matriz RBAC: `Registro temporal preciso del movimiento`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP204]** Posible rol no definido en la Matriz RBAC: `Identidad de la parte`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP207]** Posible rol no definido en la Matriz RBAC: `Identidad del proveedor/fabricante`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP209]** Posible rol no definido en la Matriz RBAC: `Código de clasificación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP215]** Posible rol no definido en la Matriz RBAC: `Cantidad actualmente en inventario físico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP217]** Posible rol no definido en la Matriz RBAC: `Stock comprometido para órdenes planificadas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP220]** Posible rol no definido en la Matriz RBAC: `Costo unitario estándar de adquisición`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP229]** Posible rol no definido en la Matriz RBAC: `Identidad comercial del proveedor`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP231]** Posible rol no definido en la Matriz RBAC: `Teléfono`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP232]** Posible rol no definido en la Matriz RBAC: `correo o dirección de contacto`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP234]** Posible rol no definido en la Matriz RBAC: `Términos estándar de garantía comercial`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP240]** Posible rol no definido en la Matriz RBAC: `Identidad del almacén`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP249]** Posible rol no definido en la Matriz RBAC: `Identidad del punto de aislamiento`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP251]** Posible rol no definido en la Matriz RBAC: `Vocabulario de aislamiento`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP262]** Posible rol no definido en la Matriz RBAC: `Tiempo de la última sincronización`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP270]** Posible rol no definido en la Matriz RBAC: `Descriptor de escala`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP279]** Posible rol no definido en la Matriz RBAC: `Unidad de medición`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP281]** Posible rol no definido en la Matriz RBAC: `Umbral de alerta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP283]** Posible rol no definido en la Matriz RBAC: `Tiempo de medición`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP285]** Posible rol no definido en la Matriz RBAC: `Bandera de clasificación de seguridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP293]** Posible rol no definido en la Matriz RBAC: `Control de renderizado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP310]** Posible rol no definido en la Matriz RBAC: `Vocabulario de permisos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP312]** Posible rol no definido en la Matriz RBAC: `Identificación del contratista`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP320]** Posible rol no definido en la Matriz RBAC: `Nombre de la tabla/entidad auditada`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP337]** Posible rol no definido en la Matriz RBAC: `Identificador del cliente/navegador para fingerprinting`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP351]** Posible rol no definido en la Matriz RBAC: `Descripción del alcance del rol`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP379]** Posible rol no definido en la Matriz RBAC: `Registro temporal de la asignación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP380]** Posible rol no definido en la Matriz RBAC: `Cardinalidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP381]** Posible rol no definido en la Matriz RBAC: `Verbo de Negocio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP382]** Posible rol no definido en la Matriz RBAC: `CASCADE`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP386]** Posible rol no definido en la Matriz RBAC: `SET NULL`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP399]** Posible rol no definido en la Matriz RBAC: `TEXT`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP401]** Posible rol no definido en la Matriz RBAC: `Ninguno`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP408]** Posible rol no definido en la Matriz RBAC: `TIMESTAMPTZ`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP414]** Posible rol no definido en la Matriz RBAC: `JSON`. Verificar contra SCR-ADM-013 o si es un alias.

## 🔴 `domain-models/use-cases/DT-UC-TRC-001.md`
*31 BLOCKER | 28 WARNING | 2 INFO*

- **[BLOCKER][B-TR01]** *(línea 35)* Caso de Uso `UC-MTTO-003` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR02]** *(línea 36)* Caso de Uso `UC-MTTO-004` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR03]** *(línea 37)* Caso de Uso `UC-MTTO-020` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR04]** *(línea 38)* Caso de Uso `UC-MTTO-028` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR05]** *(línea 39)* Caso de Uso `UC-MTTO-030` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR06]** *(línea 60)* Caso de Uso `UC-INV-021` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR07]** *(línea 78)* Caso de Uso `UC-VIS-009` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR08]** *(línea 79)* Caso de Uso `UC-VIS-010` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR09]** *(línea 80)* Caso de Uso `UC-VIS-012` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR10]** *(línea 98)* Caso de Uso `UC-ADM-015` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR11]** *(línea 99)* Caso de Uso `UC-ADM-016` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR12]** *(línea 100)* Caso de Uso `UC-ADM-017` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR13]** *(línea 101)* Caso de Uso `UC-ADM-018` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR14]** *(línea 102)* Caso de Uso `UC-ADM-019` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR15]** *(línea 103)* Caso de Uso `UC-ADM-022` referenciado pero no existe en el repositorio.
- **[BLOCKER][B-TR16]** *(línea 104)* Caso de Uso `UC-ADM-024` referenciado pero no existe en el repositorio.
- **[WARNING][W-TR01]** *(línea 71)* Requisito Arquitectónicamente Significativo `ASR-2` referenciado pero no se encontró su archivo. Verificar nombre.
- **[INFO][I-NRM01]** Estándar `ISO 9001:2015` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `ISO 55001:2014` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[BLOCKER][B-SCP01]** *(línea 2)* Caso de uso `UC-TRC-001` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP02]** *(línea 35)* Caso de uso `UC-MTTO-003` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP03]** *(línea 36)* Caso de uso `UC-MTTO-004` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP04]** *(línea 37)* Caso de uso `UC-MTTO-020` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP05]** *(línea 38)* Caso de uso `UC-MTTO-028` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP06]** *(línea 39)* Caso de uso `UC-MTTO-030` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP07]** *(línea 60)* Caso de uso `UC-INV-021` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP08]** *(línea 80)* Caso de uso `UC-VIS-012` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP09]** *(línea 98)* Caso de uso `UC-ADM-015` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP10]** *(línea 99)* Caso de uso `UC-ADM-016` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP11]** *(línea 100)* Caso de uso `UC-ADM-017` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP12]** *(línea 101)* Caso de uso `UC-ADM-018` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP13]** *(línea 102)* Caso de uso `UC-ADM-019` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP14]** *(línea 103)* Caso de uso `UC-ADM-022` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[BLOCKER][B-SCP15]** *(línea 104)* Caso de uso `UC-ADM-024` no está en el índice de UCs MVP aprobado. Si es un caso de uso nuevo, actualizar el índice con aprobación explícita.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Actor Principal`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Programar Mantenimiento Preventivo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Programar Mantenimiento por Telemetría`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Priorizar Backlog mediante RIME`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Definir Límites de Activos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Ingeniero de Confiabilidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Contratista`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Visualizar Documentación Móvil`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Gestionar Garantías de Activos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Crear Ficha Técnica de Activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Ingeniero de Proyectos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Gestionar Movimientos de Inventario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Jefe de Almacén`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Validar y Activar Activos Nuevos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `Ejecutar Rotación de Activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP20]** Posible rol no definido en la Matriz RBAC: `Crear Ubicaciones Funcionales`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP22]** Posible rol no definido en la Matriz RBAC: `Gestionar Catálogo de Repuestos Maestro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP25]** Posible rol no definido en la Matriz RBAC: `Monitorear Reabastecimiento de Stock`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP29]** Posible rol no definido en la Matriz RBAC: `Navegar Jerárquicamente con Zoom Semántico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP32]** Posible rol no definido en la Matriz RBAC: `Gestionar Roles y Permisos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP34]** Posible rol no definido en la Matriz RBAC: `Configurar Integración ERP`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP35]** Posible rol no definido en la Matriz RBAC: `Publicar Anuncios del Sistema`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP36]** Posible rol no definido en la Matriz RBAC: `Consultar Dashboard Ejecutivo de KPIs`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP37]** Posible rol no definido en la Matriz RBAC: `Generar Reportes Ejecutivos PDF`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP38]** Posible rol no definido en la Matriz RBAC: `Sincronizar Datos con Herramientas BI`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP39]** Posible rol no definido en la Matriz RBAC: `Ing. de Confiabilidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP40]** Posible rol no definido en la Matriz RBAC: `Configurar Parámetros Generales`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/adm/UC-ADM-013.md`
*0 BLOCKER | 2 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Gestionar Roles y Permisos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Ninguno`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/adm/UC-ADM-032.md`
*0 BLOCKER | 1 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Servicio de Monitoreo de Seguridad`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/inv/UC-INV-005.md`
*0 BLOCKER | 3 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Crear Ficha Técnica de Activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Ingeniero de Proyectos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Servicio de Validación Taxonómica`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/inv/UC-INV-006.md`
*0 BLOCKER | 2 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Gestionar Movimientos de Inventario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Jefe de Almacén`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/inv/UC-INV-007.md`
*0 BLOCKER | 2 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Validar y Activar Activos Nuevos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Ninguno`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/inv/UC-INV-025.md`
*0 BLOCKER | 3 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Ejecutar Rotación de Activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Ingeniero de Proyectos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Servicio de Control de Inventario`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/inv/UC-INV-027.md`
*0 BLOCKER | 3 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Crear y Estructurar Ubicaciones Funcionales`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Ingeniero de Proyectos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Servicio de Validación Taxonómica`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/inv/UC-INV-031.md`
*0 BLOCKER | 2 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Gestionar Catálogo de Repuestos Maestro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Jefe de Almacén`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/mtto/UC-MTTO-001.md`
*0 BLOCKER | 1 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Programar Mantenimiento Preventivo`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/mtto/UC-MTTO-023.md`
*0 BLOCKER | 1 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Programar Mantenimiento por Telemetría`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/mtto/UC-MTTO-026.md`
*0 BLOCKER | 1 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Priorizar Backlog mediante RIME`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `domain-models/use-cases/mtto/UC-MTTO-029.md`
*0 BLOCKER | 2 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Definir Límites Físicos de Activos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Ingeniero de Confiabilidad`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/INDEX.md`
*0 BLOCKER | 6 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Total`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Versión`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Cambios`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Senior Lead Architect`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Equipo de Análisis`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-001.md`
*0 BLOCKER | 12 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `usuario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `tipo de operacion`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-002.md`
*0 BLOCKER | 7 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-003.md`
*0 BLOCKER | 6 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-004.md`
*0 BLOCKER | 10 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `usuario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `rol y ventana de tiempo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Maintainability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-005.md`
*0 BLOCKER | 7 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `deshabilitando versiones obsoletas o vulnerables`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-006.md`
*0 BLOCKER | 7 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-007.md`
*0 BLOCKER | 9 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Usability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.

## 🔴 `requirements/common/TR-008.md`
*1 BLOCKER | 9 WARNING | 0 INFO*

- **[BLOCKER][B-NRM01]** *(línea 17)* Nivel ISA-101 `L6` no válido. Solo se permiten L1, L2, L3 y L4 según DT-UI-NAV-DOC-001.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `criticidad y estado operativo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-009.md`
*0 BLOCKER | 9 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `control de costos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-010.md`
*0 BLOCKER | 8 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `con deteccion automatica de desconexiones`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/common/TR-011.md`
*0 BLOCKER | 6 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Descripción general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Referencias normativas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Usability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-013.md`
*0 BLOCKER | 12 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Definición de un Rol Personalizado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Protección de Roles del Sistema`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `permitiendo definir el nombre`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-014.md`
*0 BLOCKER | 10 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Cuando falla el cuarto intento`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `OWASP Session Management Cheat Sheet`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP22]** Posible rol no definido en la Matriz RBAC: `Usability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-015.md`
*0 BLOCKER | 11 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `Se mantiene como COULD para el MVP enfocándose en el cumplimiento de la norma ISO 27001 y el estándar de intercambio MIMOSA.` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prueba de conexión API exitosa`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Prueba de conexión API fallida`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `permitiendo modos de operación manual`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-016.md`
*0 BLOCKER | 8 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-001]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-006]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-017.md`
*0 BLOCKER | 13 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-010]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Visualización de KPIs Globales`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Compatibility`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Usability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP21]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-018.md`
*0 BLOCKER | 12 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Reporte descargado correctamente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `permitiendo seleccionar los activos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `áreas y periodos de interés`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-019.md`
*0 BLOCKER | 12 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `Se mantiene como COULD priorizando el diseño bajo especificación OpenAPI y el aseguramiento ISO 27001.` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Exportación de Datos para BI`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Conexión de Datos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-022.md`
*0 BLOCKER | 10 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `La implementación de IA predictiva` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Usability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-024.md`
*0 BLOCKER | 9 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `La parametrización dinámica de la interfaz gráfica` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Cambio de Logo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Cambio de Zona Horaria`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/adm/ADM-032.md`
*0 BLOCKER | 14 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Cuando guarda los cambios`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Consulta de Historial por Activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Cuando confirma la acción`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `incluso para perfiles administrativos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `usuarios`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP22]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP23]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/inv/INV-005.md`
*0 BLOCKER | 13 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Ingeniero de Proyectos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Creación Exitosa con Campos Mínimos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prevención de Tag Duplicado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Validación de campos obligatorios`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Validación de Coherencia de Fechas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/inv/INV-006.md`
*0 BLOCKER | 11 WARNING | 0 INFO*

- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Jefe de Almacen`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `deduce las cantidades del inventario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Validación de Stock Insuficiente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Alerta de Sobrestock por Devolución`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `capturando el repuesto`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `la cantidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/inv/INV-007.md`
*0 BLOCKER | 12 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Ingeniero de Proyectos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Validación y Activación de Activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Rechazo de Activo Incompleto`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Tras la aprobación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Tras la activación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/inv/INV-021.md`
*0 BLOCKER | 11 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-010]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Jefe de Almacen`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Resolución de Alerta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `permitiendo el filtrado por prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/inv/INV-025.md`
*0 BLOCKER | 8 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Ingeniero de Proyectos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Registro de Trazabilidad Histórica`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/inv/INV-027.md`
*0 BLOCKER | 12 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Ingeniero de Proyectos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Validación de Tag Único`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prevención de Ciclos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/inv/INV-031.md`
*0 BLOCKER | 12 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Jefe de Almacen`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Creación Exitosa de Repuesto Stock`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Distinción Stock vs. Direct Purchase`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Selección de Commodity Code Jerárquico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-001.md`
*0 BLOCKER | 11 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Cuando selecciona el activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Validación de campos obligatorios`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Registro de trazabilidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Listado de planes activos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-002.md`
*0 BLOCKER | 12 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-007]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Cierre Exitoso con Clasificación ISO`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Adjuntar Evidencia Multimedia`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Operación sin Conexión`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Filtrado Dinámico de Taxonomía`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Compatibility`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Estándares de Arquitectura Web Móvil`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-003.md`
*0 BLOCKER | 12 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-007]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Contratista`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Carga exitosa de informe digital`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Validación de tamaño de archivo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `manteniendo la consistencia visual`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-004.md`
*0 BLOCKER | 10 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-009]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Extracción de datos exitosa`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Extracción con datos faltantes`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Aprobación con un solo clic`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-020.md`
*0 BLOCKER | 11 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-007]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Descarga voluntaria para uso Offline`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `priorizando los resultados disponibles localmente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-023.md`
*0 BLOCKER | 12 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-010]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Creación de plan por horómetro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Disparo de OT por telemetría`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Alerta por lectura inconsistente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Compatibility`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-026.md`
*0 BLOCKER | 13 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Cálculo automático de RIME`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Ordenamiento del Backlog`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Standard EAM / RIME Methodology`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `activo afectado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP23]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-028.md`
*0 BLOCKER | 11 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-009]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Pregunta fuera de contexto`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Consulta offline con contingencia`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `En ausencia de conectividad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-029.md`
*0 BLOCKER | 11 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Ingeniero de Confiabilidad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Validación de Unicidad de Componentes`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Visualización de Límites`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/mtto/MTTO-030.md`
*0 BLOCKER | 10 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Alerta de Garantía Vigente`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Conversión a Reclamo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Bypass Justificado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/vis/VIS-008.md`
*0 BLOCKER | 9 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `agregará nuevos permisos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Usability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Compatibility`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/vis/VIS-009.md`
*0 BLOCKER | 8 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Límites de Navegación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/vis/VIS-010.md`
*0 BLOCKER | 13 WARNING | 1 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Activación de Despiece`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Selección de Componente Interno`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `código de parte`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Baja`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP20]** Posible rol no definido en la Matriz RBAC: `Usability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP21]** Posible rol no definido en la Matriz RBAC: `Compatibility`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/vis/VIS-011.md`
*0 BLOCKER | 14 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-010]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `previniendo accidentes laborales`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Visualización de Puntos de Corte`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Validación de Conexión`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Validación de Energía Cero`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Reliability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP21]** Posible rol no definido en la Matriz RBAC: `inconsistente o fuera de rango`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP23]** Posible rol no definido en la Matriz RBAC: `Security`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/vis/VIS-012.md`
*0 BLOCKER | 9 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Como Ingeniero de Proyectos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Navegación jerárquica`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Media`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `requirements/user-stories/vis/VIS-033.md`
*0 BLOCKER | 12 WARNING | 2 INFO*

- **[INFO][I-NRM01]** Estándar `"[[TR-010]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Beneficio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Para consultar su estado operativo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Escenario`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Carga del Plano Base`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Inspección de Activo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Monitoreo de Telemetría`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Activo sin Mapeo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Prioridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Functional Suitability`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `garantizando una correspondencia bidireccional`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Alta`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Performance Efficiency`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `ui-ux/DT-UI-DS-DOC-001.md`
*0 BLOCKER | 56 WARNING | 1 INFO*

- **[WARNING][W-NRM01]** *(línea 94)* Color `#AAB1BD` no está en la paleta aprobada de DT-UI-DS-DOC-001 v1.2.
- **[INFO][I-NRM01]** Estándar `The High Performance HMI Handbook` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Reseteo de márgenes y paddings`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Plataforma Objetivo / Justificación`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Relación de Aspecto`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Disposición de Layout y Contenedores`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Tablet vertical / Colector industrial`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Familia / Uso Base`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Gris deshabilitado para fondo oscuro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Borde y elemento interactivo neutro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Texto secundario y atenuado general`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Bordes en fondo claro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Rojo industrial de alarma`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP12]** Posible rol no definido en la Matriz RBAC: `Ámbar / Advertencia base`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP13]** Posible rol no definido en la Matriz RBAC: `Azul informativo en fondo claro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP14]** Posible rol no definido en la Matriz RBAC: `Azul informativo base`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP15]** Posible rol no definido en la Matriz RBAC: `Confirmación documental base`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP16]** Posible rol no definido en la Matriz RBAC: `Confirmación documental en fondo oscuro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP17]** Posible rol no definido en la Matriz RBAC: `Modales / Paneles flotantes`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP18]** Posible rol no definido en la Matriz RBAC: `Líneas divisorias / Separadores`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP19]** Posible rol no definido en la Matriz RBAC: `Títulos / Valores críticos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP20]** Posible rol no definido en la Matriz RBAC: `Puntero de valor actual MAI`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP21]** Posible rol no definido en la Matriz RBAC: `Cuadrado / Octágono`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP22]** Posible rol no definido en la Matriz RBAC: `Borde punteado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP23]** Posible rol no definido en la Matriz RBAC: `Rol Tipográfico`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP24]** Posible rol no definido en la Matriz RBAC: `Inter`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP25]** Posible rol no definido en la Matriz RBAC: `Títulos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP26]** Posible rol no definido en la Matriz RBAC: `etiquetas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP27]** Posible rol no definido en la Matriz RBAC: `descripciones y controles`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP28]** Posible rol no definido en la Matriz RBAC: `Monoespaciada`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP29]** Posible rol no definido en la Matriz RBAC: `Cascadia Code`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP30]** Posible rol no definido en la Matriz RBAC: `SF Mono`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP31]** Posible rol no definido en la Matriz RBAC: `Consolas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP32]** Posible rol no definido en la Matriz RBAC: `monospace`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP33]** Posible rol no definido en la Matriz RBAC: `Encabezados de tarjetas`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP34]** Posible rol no definido en la Matriz RBAC: `lectura principal de OTs`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP35]** Posible rol no definido en la Matriz RBAC: `Texto de celdas de tabla`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP36]** Posible rol no definido en la Matriz RBAC: `descripciones técnicas y menús`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP37]** Posible rol no definido en la Matriz RBAC: `Etiquetas flotantes de formularios`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP38]** Posible rol no definido en la Matriz RBAC: `metadatos`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP39]** Posible rol no definido en la Matriz RBAC: `autoría de logs`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP40]** Posible rol no definido en la Matriz RBAC: `Badges de estado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP41]** Posible rol no definido en la Matriz RBAC: `tags de clase de equipo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP42]** Posible rol no definido en la Matriz RBAC: `checkboxes`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP43]** Posible rol no definido en la Matriz RBAC: `Ventanas modales`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP44]** Posible rol no definido en la Matriz RBAC: `diálogos de bloqueo LOTO`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP45]** Posible rol no definido en la Matriz RBAC: `Panel lateral de navegación desplegable`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP46]** Posible rol no definido en la Matriz RBAC: `Elemento Gráfico del MAI`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP47]** Posible rol no definido en la Matriz RBAC: `Concepto de Seguridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP48]** Posible rol no definido en la Matriz RBAC: `Forma Geométrica`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP49]** Posible rol no definido en la Matriz RBAC: `Texto Obligatorio`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP50]** Posible rol no definido en la Matriz RBAC: `HOT WORK`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP51]** Posible rol no definido en la Matriz RBAC: `Escalera / Arnés`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP52]** Posible rol no definido en la Matriz RBAC: `Silueta / Tanque`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP53]** Posible rol no definido en la Matriz RBAC: `Candado cerrado`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP54]** Posible rol no definido en la Matriz RBAC: `Candado abierto con halo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP55]** Posible rol no definido en la Matriz RBAC: `Rombo`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `ui-ux/DT-UI-NAV-DOC-001.md`
*0 BLOCKER | 11 WARNING | 0 INFO*

- **[WARNING][W-TR01]** *(línea 204)* Requisito Arquitectónicamente Significativo `ASR-002` referenciado pero no se encontró su archivo. Verificar nombre.
- **[WARNING][W-NRM01]** *(línea 39)* Color `#E8F1FF` no está en la paleta aprobada de DT-UI-DS-DOC-001 v1.2.
- **[WARNING][W-NRM02]** *(línea 39)* Color `#0F172A` no está en la paleta aprobada de DT-UI-DS-DOC-001 v1.2.
- **[WARNING][W-NRM03]** *(línea 40)* Color `#ECFDF5` no está en la paleta aprobada de DT-UI-DS-DOC-001 v1.2.
- **[WARNING][W-NRM04]** *(línea 40)* Color `#059669` no está en la paleta aprobada de DT-UI-DS-DOC-001 v1.2.
- **[WARNING][W-NRM05]** *(línea 40)* Color `#064E3B` no está en la paleta aprobada de DT-UI-DS-DOC-001 v1.2.
- **[WARNING][W-NRM06]** *(línea 41)* Color `#FFF7ED` no está en la paleta aprobada de DT-UI-DS-DOC-001 v1.2.
- **[WARNING][W-NRM07]** *(línea 41)* Color `#EA580C` no está en la paleta aprobada de DT-UI-DS-DOC-001 v1.2.
- **[WARNING][W-NRM08]** *(línea 41)* Color `#7C2D12` no está en la paleta aprobada de DT-UI-DS-DOC-001 v1.2.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Roles Autorizados`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Selección de Nodo de Ubicación`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `ui-ux/screens/vis/SCR-VIS-008.md`
*0 BLOCKER | 11 WARNING | 16 INFO*

- **[INFO][I-NRM01]** Estándar `Visión General)` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `Inspector HSEQ` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `Supervisor de Mantenimiento` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM04]** Estándar `"[[VIS-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM05]** Estándar `"[[UC-VIS-008]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM06]** Estándar `FR-182` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM07]** Estándar `FR-183` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM08]** Estándar `FR-184` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM09]** Estándar `FR-185` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM10]** Estándar `FR-186` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM11]** Estándar `FR-187` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM12]** Estándar `FR-188` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM13]** Estándar `NFR-190` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM14]** Estándar `NFR-193` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM15]** Estándar `"[[TR-010]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM16]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Rol Visual / Contenido`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Lienzo SVG de planta macro`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Viewport Toolbar`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `User Avatar Widget`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Functional Zone Polygon`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `PTW Overlay Badges`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Matriz de Seguridad`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Popover / Tooltip`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `SIMOPS Integrity Panel`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Filter Chips`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Condición de Activación`. Verificar contra SCR-ADM-013 o si es un alias.

## ⚠️ `ui-ux/screens/vis/SCR-VIS-033.md`
*0 BLOCKER | 11 WARNING | 16 INFO*

- **[INFO][I-NRM01]** Estándar `Supervisor de Mantenimiento` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM02]** Estándar `Técnico de Mantenimiento` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM03]** Estándar `Inspector HSEQ` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM04]** Estándar `Ingeniero de Confiabilidad` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM05]** Estándar `"[[VIS-033]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM06]** Estándar `"[[UC-VIS-033]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM07]** Estándar `FR-598` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM08]** Estándar `FR-599` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM09]** Estándar `FR-600` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM10]** Estándar `FR-601` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM11]** Estándar `FR-602` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM12]** Estándar `NFR-603` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM13]** Estándar `NFR-604` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM14]** Estándar `NFR-605` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM15]** Estándar `"[[TR-010]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[INFO][I-NRM16]** Estándar `"[[TR-011]]"` en frontmatter no está en el catálogo reconocido. Verificar pertinencia y agregar al catálogo si es válido.
- **[WARNING][W-SCP01]** Posible rol no definido en la Matriz RBAC: `Rol Visual / Contenido`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP02]** Posible rol no definido en la Matriz RBAC: `Lienzo vectorial SVG interactivo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP03]** Posible rol no definido en la Matriz RBAC: `Viewport Toolbar`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP04]** Posible rol no definido en la Matriz RBAC: `Command Palette Trigger`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP05]** Posible rol no definido en la Matriz RBAC: `Equipment Hotspot`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP06]** Posible rol no definido en la Matriz RBAC: `Context Container`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP07]** Posible rol no definido en la Matriz RBAC: `Asset Header Block`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP08]** Posible rol no definido en la Matriz RBAC: `Live Telemetry Block`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP09]** Posible rol no definido en la Matriz RBAC: `Indicadores de trabajo y riesgo`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP10]** Posible rol no definido en la Matriz RBAC: `Quick Action Buttons`. Verificar contra SCR-ADM-013 o si es un alias.
- **[WARNING][W-SCP11]** Posible rol no definido en la Matriz RBAC: `Condición de Activación`. Verificar contra SCR-ADM-013 o si es un alias.
