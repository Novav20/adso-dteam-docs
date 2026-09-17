---
code: DT-ARQ-CMP-DOC-001
version: 1.3
date: 2026-09-17
status: Vigente
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

## 1. Alcance y Objetivo

Este documento constituye la especificación de diseño detallado (C4 Nivel 3) que complementa al diagrama de componentes (`DT-ARQ-CMP-001-component-model.puml`). Su propósito es servir como la única fuente de verdad (SSoT) para el equipo de desarrollo, traduciendo las fronteras y puertos funcionales del diagrama a interfaces físicas de código en C# (.NET 10) y esquemas de almacenamiento relacional en PostgreSQL.

La especificación se acota estrictamente al alcance del **Producto Mínimo Viable (MVP)**, consolidando la lógica de inmutabilidad de logs sin colisiones, la priorización automática del backlog basada en el estándar industrial RIME, la sincronización de telemetría reactiva para seguridad y el control de inventario físico para rotación de activos (Asset Swap).

---

## 2. Matriz de Especificación de Componentes y Puertos

| ID Componente | Componente o Puerto Funcional | Capa Arquitectónica / Estereotipo | Puerto / Interfaz | Responsabilidad Técnica |
| :--- | :--- | :--- | :--- | :--- |
| **mobile_app** | Mobile App | Client Application | .NET MAUI Blazor | Cliente de campo offline-first para ejecución táctil. |
| **web_admin** | Web Admin Portal | Client Application | Blazor Web App | Supervisión HSEQ, planificación y dashboards. |
| **idempotency_filter** | Idempotency Filter | Driving Adapter | IActionFilter | Intercepta solicitudes con el encabezado Idempotency-Key; evita reprocesar transiciones críticas reenviadas tras reconexión (TR-007). |
| **api_controllers** | REST API Controllers | Driving Adapter | Minimal APIs | Expone endpoints HTTPS; maneja control de concurrencia optimista utilizando marcas de versión de fila (RowVersion/ETag). |
| **signalr_hub** | SignalR Hub | Driving Adapter | SignalR.Hub | Canal bidireccional persistente sobre WebSockets (WSS); degrada a polling si la red industrial falla. |
| **telemetry_listener** | Telemetry Listener (IoT) | Driving Adapter | IHostedService | Consumidor asíncrono (AMQP) del bróker Azure IoT Hub; inyecta telemetría al puerto de LOTO. |
| **sync_worker** | Background Sync Worker | Driving Adapter | IHostedService | Procesa de forma asíncrona e idempotente colas offline transmitidas desde clientes móviles tras recuperar conexión (TR-007). |
| **tax_port** | Taxonomy Port | Primary Port (In) | ITaxonomyService | Administra la jerarquía ISO 14224 (alta de activos, desincorporación, re-parenting y validación de ciclos). |
| **mtto_port** | Maintenance Port | Primary Port (In) | IWorkOrderService | Administración del backlog, cálculos de prioridad, programación de preventivos y reporte de fallas. |
| **inv_port** | Inventory Port | Primary Port (In) | IInventoryService | Transacciones de almacén, control de stock crítico y rotación física de equipos (Asset Swap). |
| **loto_port** | Safety & LOTO Port | Primary Port (In) | ILotoService | Autorización segura de trabajos: aprobación de permisos, bloqueos físicos y condición de Energía Cero. |
| **sec_port** | Security Port | Primary Port (In) | ISecurityService | Gobernanza IAM: autenticación, renovación de sesiones, validaciones RBAC y auditoría inmutable. |
| **rime_calc** | RIME Calculator | Domain Service | IRimeCalculator | Encapsula el cálculo de priorización RIME mediante el patrón Strategy (ADR-002). |
| **event_bus** | Event Bus Port | Domain Service | IEventBus | Desacopla la lógica interna entre módulos del monolito mediante eventos de dominio en memoria. |
| **asset_repo** | Asset Repository Port | Secondary Port (Out) | IEquipmentRepository | Interfaz de persistencia para el catálogo maestro (FunctionalLocation, EquipmentUnit). |
| **mtto_repo** | Maintenance Repository Port | Secondary Port (Out) | IWorkOrderRepository | Interfaz de persistencia para entidades transaccionales (WorkOrder, FailureRecord). |
| **inv_repo** | Inventory Repository Port | Secondary Port (Out) | IInventoryRepository | Interfaz de persistencia para control de materiales e inventarios de seguridad. |
| **sec_repo** | Audit Repository Port | Secondary Port (Out) | ISecurityRepository | Interfaz de persistencia para cuentas de usuario, roles de seguridad, sesiones y AuditLog. |
| **notify_port** | Notification Port | Secondary Port (Out) | INotificationPort | Difusión síncrona de alertas de seguridad y estado de LOTO hacia el exterior. |
| **telemetry_port** | Telemetry Port | Secondary Port (Out) | ITelemetryPort | Interfaz para suscripción a flujos de telemetría física de seguridad de forma asíncrona. |
| **ef_adapter** | EF Core PostgreSQL Adapter | Driven Adapter | PostgresDbContext | Unit of Work; persiste el AuditLog a tabla append-only con Row-Level Security. |
| **signalr_broadcaster**| SignalR Broadcaster | Driven Adapter | IHubContext<T> | Realiza el broadcast de datos hacia canales SignalR filtrando por rol autorizado. |
| **db_postgres** | PostgreSQL Master | External System | Relational Database | Almacén relacional maestro (PostgreSQL 18 + TimescaleDB). |
| **azure_iot** | Azure IoT Hub | External System | Cloud Broker | Bróker administrado para ingesta asíncrona de telemetría. |
| **redis_cache** | Redis Cache | External System | In-Memory Datastore | Caché distribuida para claves de idempotencia. |

---

## 3. Matriz de Interacciones y Flujo de Datos

| Origen | Destino | Protocolo / Interfaz | Propósito y Descripción |
| :--- | :--- | :--- | :--- |
| **mobile_app** | **idempotency_filter** | HTTPS / JSON | Envía transacciones sincrónicas o colas offline a la API. |
| **mobile_app** | **signalr_hub** | WSS | Conexión persistente para telemetría y LOTO Heartbeat. |
| **web_admin** | **api_controllers** | HTTPS / JSON | Consumo de API REST administrativa. |
| **web_admin** | **signalr_hub** | WSS | Conexión en tiempo real para dashboards. |
| **azure_iot** | **telemetry_listener** | AMQP | Consumo asíncrono de eventos de planta. |
| **idempotency_filter** | **redis_cache** | TCP/IP (Redis) | Consulta y guarda claves para prevenir reintentos. |
| **idempotency_filter** | **api_controllers** | Pipeline in-memory | Permite el paso de solicitudes HTTP seguras e idempotentes. |
| **api_controllers** | **tax_port** | C# Interface | Invoca casos de uso de taxonomía ISO 14224. |
| **api_controllers** | **mtto_port** | C# Interface | Invoca casos de uso de órdenes de trabajo. |
| **api_controllers** | **inv_port** | C# Interface | Invoca casos de uso de inventario. |
| **api_controllers** | **sec_port** | C# Interface | Invoca autorización e IAM. |
| **signalr_hub** | **sec_port** | C# Interface | Valida tokens y autoriza canales WSS. |
| **telemetry_listener**| **loto_port** | C# Interface | Inyecta datos de telemetría para evaluar Energía Cero. |
| **sync_worker** | **mtto_port** | C# Interface | Vacía colas de órdenes offline procesándolas en background. |
| **mtto_port** | **rime_calc** | C# Interface | Calcula determinísticamente la prioridad RIME. |
| **tax_port** | **event_bus** | C# Interface | Dispara eventos de dominio (Ej. AssetInstalled). |
| **mtto_port** | **event_bus** | C# Interface | Dispara eventos de dominio (Ej. WorkOrderClosed). |
| **tax_port** | **asset_repo** | C# Interface | Persiste estructuras taxonómicas. |
| **mtto_port** | **mtto_repo** | C# Interface | Persiste órdenes de trabajo y backlog. |
| **inv_port** | **inv_repo** | C# Interface | Persiste movimientos de stock. |
| **sec_port** | **sec_repo** | C# Interface | Persiste logs de auditoría inmutables. |
| **loto_port** | **notify_port** | C# Interface | Envía alertas de cambio de estado de aislamiento físico. |
| **loto_port** | **telemetry_port**| C# Interface | Suscribe requerimientos de energía física. |
| **asset_repo** | **ef_adapter** | C# Class Inheritance | Implementa persistencia vía EF Core DbContext. |
| **mtto_repo** | **ef_adapter** | C# Class Inheritance | Implementa persistencia vía EF Core DbContext. |
| **inv_repo** | **ef_adapter** | C# Class Inheritance | Implementa persistencia vía EF Core DbContext. |
| **sec_repo** | **ef_adapter** | C# Class Inheritance | Implementa persistencia vía EF Core DbContext. |
| **notify_port** | **signalr_broadcaster**| C# Class Inheritance | Implementa difusión vía Microsoft.AspNetCore.SignalR. |
| **ef_adapter** | **db_postgres** | TCP/IP (SQL) | Ejecuta comandos relacionales transaccionales bajo Unit of Work. |

---

## 4. Índice de Trazabilidad de Puertos, Interfaces y Requisitos

| Módulo / Puerto | Firma de Método en C# y Parámetros | Requisito / US | Invariante de Seguridad / Regla de Negocio a Validar |
| :--- | :--- | :--- | :--- |
| **ITelemetryPort** | `IDisposable SubscribeToSafetyChannel(Guid equipmentUnitId, Action<TelemetryReading> onReading);` | [[VIS-011]]<br>TR-010-FR-431 | **Sincronización en Tiempo Real:** Propaga revocaciones de permisos y picos de energía en sub-segundos. **Control de concurrencia:** El cliente debe aplicar un *debounce* de $300\text{ ms}$ en la selección de activos para evitar condiciones de carrera por suscripciones múltiples simultáneas. |
| **ITaxonomyService** | `Task InstallEquipment(Guid locationId, Guid equipmentId);` | [[INV-025]]<br>FR-593, FR-594 | Valida que la ubicación funcional no tenga un activo instalado (cardinalidad 1 slot = 1 activo L6) y que el equipo de reemplazo esté en estado `IN_STORAGE` (INV-025). |
| **ITaxonomyService** | `Task<EquipmentUnit> UninstallEquipment(Guid locationId, string reason);` | [[INV-025]]<br>FR-591, FR-592 | Desvincula el equipo de su posición operativa; actualiza su estado físico a "En Reparación" o "Stock" en una transacción de base de datos de único commit (NFR-596). |
| **ITaxonomyService** | `Task ReorganizeTree(Guid locationId, Guid newParentId);` | [[INV-027]]<br>FR-162, NFR-167 | Valida que el movimiento no genere ciclos infinitos (un nodo no puede ser ancestro de sí mismo, TR-008-FR-417) y que se mantenga dentro de los límites de Ubicaciones Funcionales (L1 a L5 de la taxonomía ISO 14224). |
| **IWorkOrderService** | `Task<Guid> CreateWorkRequest(CreateWorkRequestDto request);` | [[MTTO-026]]<br>FR-059 | Exige de forma obligatoria el ingreso de la Clase de Trabajo (`workClassCode`) y el identificador del activo para poder admitir la solicitud en el backlog. |
| **IWorkOrderService** | `Task UpdatePriorityScore(Guid workRequestId);` | [[MTTO-026]]<br>FR-060, NFR-074 | Invoca `IRimeCalculator.Calculate(asset.Criticality, request.WorkClass)`; el cálculo es determinístico e inmutable ante factores de inventario externos. |
| **IWorkOrderService** | `Task CalculateNextTriggerLimit(Guid planId, decimal currentUsage);` | [[MTTO-023]]<br>FR-583, FR-584 | Rechaza lecturas de telemetría inferiores al acumulado histórico (contadores); mantiene el último valor válido y genera alerta por posible alteración de sensor. |
| **IWorkOrderService** | `Task StartExecution(Guid workOrderId);` | [[VIS-011]]<br>NFR-229, NFR-238 | **FAIL-SAFE:** Bloquea la transición si el permiso asociado no está `APPROVED` o si algún `WorkOrderIsolation.isIsolated` es falso. Bloquea si hay pérdida de telemetría. |
| **IWorkOrderService** | `Task CloseAdministratively(Guid workOrderId);` | [[MTTO-002]]<br>FR-012 | Valida el diligenciamiento de los códigos de falla de la ISO 14224 (`FailureRecord`) y el consumo real de repuestos antes de marcar la OT como `CLOSED`. |
| **IWorkOrderService** | `Task CompleteExecution(Guid workOrderId, decimal actualLaborHours);` | [[MTTO-002]]<br>FR-010 | **Cierre Técnico:** Transiciona el estado de la OT a `COMPLETE` y registra el tiempo real de labor en campo (*wrench time*) reportado por el técnico. |
| **IWorkOrderService** | `Task<Guid> PromoteToWorkOrderAsync(Guid workRequestId);` | Soporte Transversal (WorkRequest) | **Admisión del Backlog:** Calcula el `RIME Score` mediante el servicio `IRimeCalculator` previo a la creación de la OT; rechaza si `workClassCode` no está parametrizado. |
| **IInventoryService** | `Task ReserveStock(Guid sparePartId, decimal quantity);` | [[INV-006]]<br>FR-126 | Decrementa el stock disponible virtual (`QuantityOnHand - ReservedQuantity`); rechaza la reserva si el valor resultante es inferior a cero. |
| **IInventoryService** | `Task RecordConsumption(Guid workOrderId, Guid sparePartId, decimal quantity);` | [[INV-006]]<br>FR-127 | Cruza el consumo de repuestos con `SparePart.IssueStock()`; actualiza la tabla de costos de mantenimiento de la OT de forma atómica en la DB. |
| **IInventoryService** | `Task SwapAssetAsync(Guid locationId, Guid replacementId, Guid workOrderId);` | [[INV-025]]<br>FR-591 a FR-595 | **Rotación (Asset Swap):** Desvincula de forma atómica el activo dañado de su ubicación funcional, actualiza su estado a "En Reparación" o "Stock", e instala la unidad de reemplazo (NFR-596). |
| **ILotoService** | `Task RequireIsolation(Guid workOrderId, Guid isolationPointId);` | [[VIS-011]]<br>FR-228, FR-230 | Inserta la tupla en la tabla intermedia `work_order_isolations`; no permite autorizar el aislamiento general si quedan ítems del checklist sin confirmar. |
| **ILotoService** | `Task EvaluateEnergyState(Guid isolationPointId, decimal telemetryValue);` | [[VIS-011]]<br>NFR-229, NFR-237 | Si el valor de lectura del sensor supera los límites seguros de Energía Cero, fuerza estado de peligro; el bloqueo físico no puede superarse desde la UI del técnico. |
| **ILotoService** | `Task ConfirmZeroEnergyAsync(Guid workOrderId);` | [[VIS-011]]<br>FR-230, NFR-233 | **Bloqueo Activo:** Habilita la confirmación de Energía Cero únicamente cuando la telemetría del puerto confirma que no hay flujo activo en los puntos de aislamiento; latencia <1s. |
| **ISecurityService** | `Task<AuthToken> Authenticate(string username, string password);` | TR-006-FR-394 | Genera token JWT inmutable con vigencia máxima de 8 horas; incrementa el contador de fallos de login en `User` si la contraseña no coincide. |
| **ISecurityService** | `Task AppendAuditEntry(string entityType, string entityId, string action, object previous, object next);` | [[ADM-032]]<br>FR-346, [[TR-001]] | Persiste en formato JSONB de PostgreSQL mediante interceptor asíncrono; la tabla de destino deniega comandos `UPDATE`/`DELETE` a nivel de motor SQL. |
| **ISecurityService** | `Task<bool> VerifyAuditIntegrity(Guid logId);` | [[ADM-032]]<br>FR-351 | Recalcula el hash SHA-256 encadenado criptográficamente con el registro anterior y valida la coincidencia; notifica de inmediato al HSEQ si hay discrepancia. |
| **ISecurityService** | `Task<bool> AuthorizeAsync(Guid userId, string module, string action);` | TR-006-FR-396<br>TR-006-NFR-401 | **Seguridad RBAC:** Evalúa la matriz de permisos del rol asignado en <5ms de latencia; registra las denegaciones de acceso como eventos sospechosos en `audit_logs` (TR-006-FR-397). |
| **IEquipmentRepository** | `Task<IReadOnlyList<FunctionalLocation>> GetHierarchyPathAsync(Guid assetId);` | [[TR-008]], FR-416 | **Consistencia Taxonómica:** Debe garantizar un camino jerárquico ininterrumpido desde Nivel 1 hasta el activo consultado; con respuesta de carga en <500ms (TR-008-NFR-419). |
| **ISecurityRepository** | `Task<IReadOnlyList<AuthToken>> GetActiveSessionsAsync(Guid userId);` | TR-006-NFR-402 | **Revocación de Accesos:** Permite consultar e invalidar de forma inmediata las sesiones activas (quema de tokens JWT) cuando el estado del usuario cambia a inactivo por riesgo. |
| **IWorkOrderRepository** | `Task SaveWithHistoryAsync(WorkOrder workOrder, string oldStatus);` | Soporte Transversal (`WorkOrderHistory`) | **Trazabilidad:** Cada transición de estado debe generar de forma atómica una fila en la tabla de historial `work_order_histories` en una transacción de único commit de base de datos. |
| **IInventoryRepository** | `Task<StockSnapshot> GetAvailabilityAsync(Guid sparePartId);` | TR-008 (consistencia estructural conexa) | **Integridad de Almacén:** Retorna el inventario físico (`QuantityOnHand`) y el comprometido (`ReservedQuantity`) sin lecturas sucias, asegurando consistencia transaccional. |
