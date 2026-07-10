---
code: DT-ARQ-CMP-DOC-001
version: 1
date: 2026-07-08
status: Especificación Técnica de Componentes — MVP
author: Juan David Julio Serrano
standard:
  - ISO/IEC 42010:2011 (Arquitectura — Vistas C4 Nivel 3)
  - ISO 9001:2015 (Control Documental)
  - ISO 14224:2016
  - ISO 45001:2018 (Cláusula 8.1 — LOTO)
  - ISO 55001:2014
  - Domain-Driven Design / Arquitectura Hexagonal
---

# Especificación Técnica de Interfaces y Puertos

## Alcance y Objetivo

Este documento constituye la especificación de diseño detallado (C4 Nivel 3) que complementa al diagrama de componentes (`DT-ARQ-CMP-001`). Su propósito es servir como la única fuente de verdad (SSoT) para el equipo de desarrollo, traduciendo las fronteras y puertos funcionales del diagrama a interfaces físicas de código en C# (.NET 10) y esquemas de almacenamiento relacional en PostgreSQL.

La especificación se acota estrictamente al alcance del **Producto Mínimo Viable (MVP)**, consolidando la lógica de inmutabilidad de logs sin colisiones, la priorización automática del backlog basada en el estándar industrial RIME, la sincronización de telemetría reactiva para seguridad y el control de inventario físico para rotación de activos (Asset Swap).

---

## Matriz de Especificación de Componentes y Puertos

| Componente o Puerto Funcional   | Estereotipo / Clasificación | Puerto / Interfaz                              | Responsabilidad Técnica                                                                                                                                                                     |
| ------------------------------- | --------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Idempotency Filter**          | Driving Adapter             | `IActionFilter` + `IDistributedCache`          | Intercepta solicitudes con el encabezado `Idempotency-Key` en la caché de Redis; evita reprocesar inserciones o transiciones críticas reenviadas por el móvil tras reconexión ([[TR-007]]). |
| **REST API Controllers**        | Driving Adapter             | `Minimal APIs` / `Controllers`                 | Expone los endpoints HTTPS públicos; maneja el control de concurrencia optimista utilizando marcas de versión de fila (`RowVersion`/`ETag`) en `WorkOrder` y `EquipmentUnit`.               |
| **SignalR Hub**                 | Driving Adapter             | `Microsoft.AspNetCore.SignalR.Hub`             | Canal bidireccional persistente sobre WebSockets (WSS); degrada a consultas periódicas (polling) de forma transparente si la conexión de red industrial falla.                              |
| **Telemetry Listener (IoT)**    | Driving Adapter             | `IHostedService` (Background Task)             | Consumidor asíncrono (AMQP) del bróker Azure IoT Hub; captura la telemetría enviada por la estación de control del SCADA (Edge Node) y la inyecta al puerto de LOTO.                        |
| **Taxonomy Port (PTax)**        | Primary Port (In)           | `ITaxonomyService`                             | Define los casos de uso para administrar la jerarquía ISO 14224 (alta de activos, desincorporación, re-parenting y validación de ciclos).                                                   |
| **Maintenance Port (PMtto)**    | Primary Port (In)           | `IWorkOrderService`                            | Define los casos de uso para la administración del backlog, cálculos de prioridad, programación de preventivos y reporte de fallas.                                                         |
| **Inventory Port (PInv)**       | Primary Port (In)           | `IInventoryService`                            | Define los casos de uso para transacciones de almacén (egresos/ingresos), control de stock crítico y rotación física de equipos (Asset Swap).                                               |
| **Safety & LOTO Port (PLoto)**  | Primary Port (In)           | `ILotoService`                                 | Define los casos de uso para la autorización segura de trabajos: aprobación de permisos, verificación de bloqueos físicos e aseguramiento de la condición de Energía Cero.                                      |
| **Security Port (PSec)**        | Primary Port (In)           | `ISecurityService`                             | Define los casos de uso para la gobernanza IAM: autenticación, renovación de sesiones (8h), validaciones de roles RBAC y control de logs de auditoría.                                      |
| **IRimeCalculator**             | Domain Service              | `IRimeCalculator`                              | Encapsula el cálculo determinístico del RIME ($Score = \text{Criticidad} \times \text{Clase de Trabajo}$) mediante el patrón _Strategy_, desacoplándolo de la entidad del backlog.          |
| **Asset Repo Port (RAsset)**    | Secondary Port (Out)        | `IEquipmentRepository`                         | Interfaz de persistencia para el resguardo de la estructura del catálogo maestro (`FunctionalLocation`, `EquipmentUnit`).                                                                   |
| **Mtto Repo Port (RMtto)**      | Secondary Port (Out)        | `IWorkOrderRepository`                         | Interfaz de persistencia para las entidades transaccionales del flujo de mantenimiento (`WorkOrder`, `FailureRecord`).                                                                      |
| **Inventory Repo Port (RInv)**  | Secondary Port (Out)        | `IInventoryRepository`                         | Interfaz de persistencia para el control de materiales e inventarios de seguridad (`SparePart`, `MaterialRequirement`).                                                                     |
| **Audit Repo Port (RSec)**      | Secondary Port (Out)        | `ISecurityRepository`                          | Interfaz de persistencia para datos de cuentas de usuario, roles de seguridad, sesiones activas e `AuditLog`.                                                                               |
| **Notification Port (PNotify)** | Secondary Port (Out)        | `INotificationPort`                            | Interfaz para la difusión síncrona de alertas de seguridad y estado de LOTO hacia el exterior del hexágono.                                                                                 |
| **Event Bus Port (PEventBus)**  | Secondary Port (Out)        | `IEventBus`                                    | Desacopla la lógica interna entre módulos del monolito mediante eventos de dominio en memoria (`MediatR` / Pub-Sub).                                                                        |
| **EF Core PostgreSQL Adapter**  | Driven Adapter              | `PostgresDbContext` + `SaveChangesInterceptor` | Implementa los puertos secundarios de persistencia mediante Unit of Work; persiste el `AuditLog` a una tabla append-only controlada por Row-Level Security.                                   |
| **SignalR Broadcaster**         | Driven Adapter              | `IHubContext<T>`                               | Implementa el puerto de notificación; realiza el broadcast de datos hacia los canales SignalR filtrando los destinatarios por rol autorizado.                                               |

---

## 3. Índice de Trazabilidad de Puertos, Interfaces y Requisitos

| Módulo / Puerto               | Firma de Método en C# e Parámetros                                                                        | Requisito / US                    | Invariante de Seguridad / Regla de Negocio a Validar                                                                                                                      |
| ----------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PTax / ITaxonomyService**   | `Task InstallEquipment(Guid locationId, Guid equipmentId);`                                               | [[INV-025]]<br>FR-184, FR-185     | Valida que la ubicación funcional no tenga un activo instalado (máximo 1 slot - 1 activo) y que el equipo de reemplazo esté en estado `IN_STORAGE` (INV-025).             |
| **PTax / ITaxonomyService**   | `Task<EquipmentUnit> UninstallEquipment(Guid locationId, string reason);`                                 | [[INV-025]]<br>FR-591, FR-592     | Desvincula el equipo de su posición operativa; actualiza su estado físico a "En Reparación" o "Stock" en una transacción de base de datos de único commit (NFR-596).      |
| **PTax / ITaxonomyService**   | `Task ReorganizeTree(Guid locationId, Guid newParentId);`                                                 | [[INV-027]]<br>FR-162, NFR-167    | Valida que el movimiento no genere ciclos infinitos (un nodo no puede ser ancestro de sí mismo, TR-008-FR-417) ni rompa la restricción de 9 niveles taxonómicos.          |
| **PMtto / IWorkOrderService** | `Task<Guid> CreateWorkRequest(CreateWorkRequestDto request);`                                             | [[MTTO-026]]<br>FR-059            | Exige de forma obligatoria el ingreso de la Clase de Trabajo (`workClassCode`) y el identificador del activo para poder admitir la solicitud en el backlog.               |
| **PMtto / IWorkOrderService** | `Task UpdatePriorityScore(Guid workRequestId);`                                                           | [[MTTO-026]]<br>FR-060, NFR-074   | Invoca `IRimeCalculator.Calculate(asset.Criticality, request.WorkClass)`; el cálculo es determinístico e inmutable ante factores de inventario externos.                  |
| **PMtto / IWorkOrderService** | `Task CalculateNextTriggerLimit(Guid planId, decimal currentUsage);`                                      | [[MTTO-023]]<br>FR-583, FR-584    | Rechaza lecturas de telemetría inferiores al acumulado histórico (contadores); mantiene el último valor válido y genera alerta por posible alteración de sensor.          |
| **PMtto / IWorkOrderService** | `Task StartExecution(Guid workOrderId);`                                                                  | [[VIS-011]]<br>NFR-229, NFR-238   | **FAIL-SAFE:** Bloquea la transición si el permiso asociado no está `APPROVED` o si algún `WorkOrderIsolation.isIsolated` es falso. Bloquea si hay pérdida de telemetría. |
| **PMtto / IWorkOrderService** | `Task CloseAdministratively(Guid workOrderId);`                                                           | [[MTTO-002]]<br>FR-012            | Valida el diligenciamiento de los códigos de falla de la ISO 14224 (`FailureRecord`) y el consumo real de repuestos antes de marcar la OT como `CLOSED`.                  |
| **PInv / IInventoryService**  | `Task ReserveStock(Guid sparePartId, decimal quantity);`                                                  | [[INV-006]]<br>FR-126             | Decrementa el stock disponible virtual (`QuantityOnHand - ReservedQuantity`); rechaza la reserva si el valor resultante es inferior a cero.                               |
| **PInv / IInventoryService**  | `Task RecordConsumption(Guid workOrderId, Guid sparePartId, decimal quantity);`                           | [[INV-006]]<br>FR-127             | Cruza el consumo de repuestos con `SparePart.IssueStock()`; actualiza la tabla de costos de mantenimiento de la OT de forma atómica en la DB.                             |
| **PLoto / ILotoService**      | `Task RequireIsolation(Guid workOrderId, Guid isolationPointId);`                                         | [[VIS-011]]<br>FR-228, FR-230     | Inserta la tupla en la tabla intermedia `work_order_isolations`; no permite autorizar el aislamiento general si quedan ítems del checklist sin confirmar.                 |
| **PLoto / ILotoService**      | `Task EvaluateEnergyState(Guid isolationPointId, decimal telemetryValue);`                                | [[VIS-011]]<br>NFR-229, NFR-237   | Si el valor de lectura del sensor supera los límites seguros de Energía Cero, fuerza estado de peligro; el bloqueo físico no puede superarse desde la UI del técnico.     |
| **PSec / ISecurityService**   | `Task<AuthToken> Authenticate(string username, string password);`                                         | TR-006-FR-394                     | Genera token JWT inmutable con vigencia máxima de 8 horas; incrementa el contador de fallos de login en `User` si la contraseña no coincide.                              |
| **PSec / ISecurityService**   | `Task AppendAuditEntry(string entityType, string entityId, string action, object previous, object next);` | [[ADM-032]]<br>FR-346, [[TR-001]] | Persiste en formato JSONB de PostgreSQL mediante interceptor asíncrono; la tabla de destino deniega comandos `UPDATE`/`DELETE` a nivel de motor SQL.                      |
| **PSec / ISecurityService**   | `Task<bool> VerifyAuditIntegrity(Guid logId);`                                                            | [[ADM-032]]<br>FR-351             | Recalcula el hash SHA-256 encadenado criptográficamente con el registro anterior y valida la coincidencia; notifica de inmediato al HSEQ si hay discrepancia.             |
