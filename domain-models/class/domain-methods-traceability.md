---
code: DT-DM-DOC-002
version: 1.1
date: 2026-07-07
status: Adición de métodos en FunctionalLocation, EquipmentUnit y MaintenancePlan
author: Juan David Julio Serrano
standard:
  - ISO 9001:2015
  - ISO 14224:2016
  - Domain-Driven Design (DDD)
---

# Trazabilidad de Comportamientos del Dominio

## 1. Propósito

Este documento establece la Única Fuente de Verdad (SSoT) para el comportamiento de las clases del modelo de dominio del Gemelo Digital. Su objetivo es mapear cada método (operación) de las entidades y raíces de agregado hacia las Historias de Usuario del MVP y los Requisitos Funcionales (FR), garantizando la trazabilidad exigida por la normativa ISO 9001.

Adicionalmente, el documento justifica la existencia de cada método bajo los principios de **Domain-Driven Design (DDD)**. Las firmas de los métodos utilizan la convención **PascalCase**, en preparación para su implementación física en C# (.NET).

---

## 2. Capa 1: Taxonomía de Activos (ISO 14224)

### 2.1. `FunctionalLocation` (`<<Aggregate Root>>`)

| Método                                             | Propósito / Regla de Negocio                                                                                                             | Origen (Historia / FR)         | Justificación Arquitectónica (DDD)                                                                                                                                                       |
| :------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AddChild(child: FunctionalLocation): void`        | Vincula jerárquicamente un nodo hijo validando que su `hierarchyLevel` sea estrictamente mayor (nivel inferior en ISO) que el del padre. | [[INV-027]]<br>FR-161          | **Encapsulamiento:** Como raíz de agregado, la ubicación debe gobernar y validar las reglas de negocio al anidar dependencias.                                                           |
| `RemoveChild(childId: UUID): void`                 | Elimina un nodo hijo, validando previamente que la ubicación no tenga activos (`EquipmentUnit`) instalados o sub-jerarquías huérfanas.   | [[INV-027]]<br>FR-163          | **Invariante de Ciclo de Vida:** Protege contra la orfandad de datos y asegura restricciones lógicas antes de permitir la eliminación.                                                   |
| `ReorganizeTree(newParentId: UUID): void`          | Cambia el nodo padre de la ubicación actual, validando que el movimiento no genere inconsistencias lógicas o ciclos infinitos.           | [[INV-027]]<br>FR-162, NFR-167 | **Comportamiento Rico:** El cambio de jerarquía es una regla de negocio compleja, no un simple _setter_. Delega a la entidad la verificación de su propia consistencia antes de moverse. |
| `InstallEquipment(equipment: EquipmentUnit): void` | Instala un activo en la posición operativa, cambiando su estado a INSTALLED y vinculándolo formalmente.                                  | [[INV-025]]<br>FR-184, FR-185  | **Invariante de Negocio:** Valida que la posición no esté ocupada y que el equipo a instalar esté en estado operativo/disponible.                                                        |
| `UninstallEquipment(): EquipmentUnit`              | Remueve el activo de la ubicación operativa, retornando la instancia del equipo para gestionar su resguardo.                             | [[INV-025]]<br>FR-183          | **Máquina de Estados:** Rompe el vínculo y habilita al equipo para su reubicación física en el almacén o taller.                                                                         |

### 2.2. `EquipmentUnit` (`<<Aggregate Root>>`)

| Método                                                               | Propósito / Regla de Negocio                                                                                               | Origen (Historia / FR)         | Justificación Arquitectónica (DDD)                                                                                                                                                                 |
| :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- | :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Activate(): void`                                                   | Formaliza el alta del equipo, cambiando su estado a `INSTALLED` y habilitándolo para planes preventivos y correctivos.     | [[INV-007]]<br>FR-139, FR-140  | **Comportamiento Rico:** Representa el concepto de negocio "Commissioning" (Puesta en marcha). No es un simple setter, es una transición de máquina de estados.                                    |
| `DefineBoundaries(boundaryStart: String, boundaryEnd: String): void` | Establece los límites físicos del activo para evitar ambigüedad en el registro de intervenciones y tiempos de inactividad. | [[MTTO-029]]<br>FR-092, FR-096 | **Regla ISO 14224:** Encapsula la obligación normativa de delimitar dónde empieza y termina el equipo físico dentro del proceso industrial.                                                        |
| `UpdateOperationalStatus(newStatus: Enum): void`                     | Transiciona la condición operativa (`UP`, `DOWN`, `STANDBY`).                                                              | [[MTTO-002]]<br>FR-014         | **Centralización de Lógica:** Evita modificaciones accidentales del estado (Primitive Obsession). Permite emitir Eventos de Dominio si la máquina pasa a `DOWN`.                                   |
| `AddSubunit(subunit: Subunit): void`                                 | Vincula un subcomponente (Nivel 7 ISO) a la jerarquía interna del equipo físico.                                           | [[MTTO-029]]<br>FR-094         | **Control de Agregado:** Como Aggregate Root, es el único responsable de agregar y gestionar la colección de sus partes internas para mantener consistencia.                                       |
| `Decommission(reason: String, disposalDate: Date): void`             | Retira permanentemente el activo del servicio operativo, marcando su fin de ciclo de vida.                                 | Soporte Transversal ISO 55000  | **Invariante de Ciclo de Vida:** Operación destructiva lógica que asegura que un equipo retirado no reciba más planes de mantenimiento.                                                            |
| `RejectCommissioning(reason: String): void`                          | Devuelve el activo durante el proceso de alta, registrando el motivo técnico del rechazo en `RejectionReason`.             | [[INV-007]]<br>FR-141          | **Máquina de Estados (Validación):** Completa el flujo de comisionamiento permitiendo rechazar activos que no cumplen la norma de completitud de datos (FR-138), exigiendo un string justificante. |
| `TransitionToStorage(warehouseId: UUID): void`                       | Cambia el estado del activo a IN_STORAGE y lo vincula al almacén seleccionado para resguardo.                              | [[INV-025]]<br>FR-183          | **Transición de Estado:** Mueve el ciclo de vida del activo serializado de regreso al inventario bajo control del almacén.                                                                         |
| `TransitionToRepair(): void`                                         | Cambia el estado del activo a UNDER_MAINTENANCE / REPAIR para envío a taller técnico.                                      | [[INV-025]]<br>FR-183          | **Ciclo de Vida:** Habilita el activo para flujos de reparación correctiva o reacondicionamiento (rebuildable).                                                                                    |

### 2.3. `Subunit` (`<<Entity>>`)

| Método                                              | Propósito / Regla de Negocio                         | Origen (Historia / FR) | Justificación Arquitectónica (DDD)                                                                                                                    |
| :-------------------------------------------------- | :--------------------------------------------------- | :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AddMaintainableItem(item: MaintainableItem): void` | Vincula un ítem mantenible (Nivel 8) al sub-sistema. | [[MTTO-029]]<br>FR-094 | **Control Jerárquico:** Encapsula la adición de componentes de nivel inferior, garantizando que el árbol jerárquico se construya de forma controlada. |

### 2.4. `MaintainableItem` (`<<Entity>>`)

| Método                                | Propósito / Regla de Negocio                                                   | Origen (Historia / FR) | Justificación Arquitectónica (DDD)                                                                                                                       |
| :------------------------------------ | :----------------------------------------------------------------------------- | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `UpdateStatus(newStatus: Enum): void` | Transiciona el estado del ítem (ej. de `OPERATIONAL` a `FAILED` o `REPLACED`). | [[MTTO-002]]<br>FR-011 | **Máquina de Estados:** Protege el atributo `Status`, asegurando que los reportes de falla afecten el ciclo de vida del componente específico que falló. |

## 3. Capa 2: Operaciones de Mantenimiento (MTTO)

### 3.1. `WorkRequest` (`<<Aggregate Root>>`)

| Método                                                                                    | Propósito / Regla de Negocio                                                                                          | Origen (Historia / FR)          | Justificación Arquitectónica (DDD)                                                                                                                                      |
| :---------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PromoteToWorkOrder(): void`                                                              | Transiciona la solicitud al estado `APPROVED`, marcándola como lista para generar una OT en el backlog.               | Soporte Transversal             | **Máquina de Estados:** Protege el ciclo de vida de admisión. Un cambio a este estado suele disparar un *Domain Event* que crea la entidad `WorkOrder` correspondiente. |
| `Reject(reason: String): void`                                                            | Rechaza la solicitud (estado `REJECTED`), exigiendo un motivo técnico para evitar intervenciones falsas o duplicadas. | Soporte Transversal             | **Invariante de Negocio:** Toda cancelación o rechazo debe estar justificada para la auditoría técnica.                                                                 |
| `UpdateWorkClass(workClass: int): void`                                                   | Actualiza la clase de trabajo (Work Class) asociada a la solicitud.                                                   | [[MTTO-026]]<br>FR-059          | **Consistencia de Agregado:** El cambio de la clase de trabajo dispara la actualización atómica del RIME Score en el `BacklogItem` correspondiente.                     |

### 3.2. `MaintenancePlan` (`<<Aggregate Root>>`)

| Método                                                     | Propósito / Regla de Negocio                                                                                | Origen (Historia / FR)   | Justificación Arquitectónica (DDD)                                                                                                                                  |
| :--------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- | :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `CalculateNextDueDate(lastCompletionDate: DateTime): void` | Calcula y actualiza la propiedad `NextWorkOrderDate` sumando la cadencia (`Frequency`) al último cierre.    | [[MTTO-001]]<br>FR-003   | **Lógica de Dominio:** El cálculo de la próxima iteración es conocimiento exclusivo del plan, dependiendo de si es basado en calendario, horas operativas o ciclos. |
| `GenerateWorkOrder(): WorkOrder`                           | Factory Method que instancia una nueva OT preventiva heredando los datos del plan.                          | [[MTTO-001]]<br>FR-005   | **Comportamiento Rico:** El plan actúa como fábrica de sus propias ejecuciones, asegurando que la OT nazca vinculada a él.                                          |
| `Activate(): void`                                         | Pasa el plan de `DRAFT` a `ACTIVE`, permitiendo que el motor de programación (Cron) lo evalúe.              | [[MTTO-001]]<br>FR-006   | **Transición de Estado:** Evita que se generen OTs desde planes que aún están en diseño o revisión técnica.                                                         |
| `Suspend(reason: String): void`                            | Pasa el plan a estado `INACTIVE`, deteniendo temporalmente la generación de nuevas OTs.                     | [[MTTO-001]] (Implícito) | **Máquina de Estados:** Útil durante paradas generales de planta o cambios operativos.                                                                              |
| `Archive(): void`                                          | Pasa el plan a estado `ARCHIVED` marcándolo como obsoleto, preservando el historial.                        | Soporte Transversal      | **Retención Documental:** Cumplimiento de ISO 55000 sobre retención de registros obsoletos sin eliminación física.                                                  |
| `CalculateNextTriggerLimit(currentUsage: Decimal): void`   | Calcula el siguiente umbral de disparo de telemetría sumando el `IntervalValue` a la lectura actual de uso. | [[MTTO-023]]<br>FR-584   | **Telemetría (Uso):** Define el objetivo de la próxima OT basado en acumulación de variables físicas (horómetros/ciclos).                                           |


### 3.3. `WorkOrder` (`<<Aggregate Root>>`)

| Método                                                                          | Propósito / Regla de Negocio                                                                                                                                  | Origen (Historia / FR)           | Justificación Arquitectónica (DDD)                                                                                                                                                        |
| :---------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Schedule(scheduledDate: DateTime): void`                                                 | Transiciona la OT a estado `SCHEDULED`, asignando una ventana temporal de ejecución.                                                                          | Soporte Transversal              | **Máquina de Estados:** Primer paso de planificación formal.                                                                                                                              |
| `RequireIsolation(isolationPointId: UUID): void`                                          | Vincula un punto físico LOTO (`IsolationPoint`) que debe ser bloqueado obligatoriamente antes del trabajo.                                                    | [[VIS-011]]<br>FR-228, FR-230    | **Precondición de Seguridad:** Construye la matriz de seguridad requerida para la ejecución segura del mantenimiento.                                                                     |
| `StartExecution(): void`                                                                  | Transiciona a `IN_PROGRESS`. Valida internamente que exista un `WorkPermit` aprobado y que todos los aislamientos LOTO estén en estado seguro (Energía Cero). | [[VIS-011]]<br>NFR-229 (Crítico) | **Invariante Crítico (Fail-Safe):** Evita el inicio de trabajos peligrosos. El comportamiento encapsula las validaciones de vida y seguridad.                                             |
| `CompleteExecution(actualLaborHours: Decimal): void`                                      | Transiciona a `COMPLETE`. Registra el tiempo de llave (*wrench time*) por parte del técnico en campo.                                                         | [[MTTO-002]]<br>FR-010, FR-014   | **Máquina de Estados:** Separa la terminación física (técnico) del cierre administrativo (auditoría).                                                                                     |
| `CloseAdministratively(): void`                                                           | Transiciona a `CLOSED`. Valida que los códigos de falla (ISO 14224) y los consumos reales estén diligenciados correctamente.                                  | [[MTTO-002]]<br>FR-012           | **Control de Calidad:** Garantiza la completitud de la ficha de mantenimiento para los KPIs de confiabilidad antes de su inmutabilidad final.                                             |
| `ReportFailure(maintainableItemId: UUID, mode: Enum, mechanism: Enum, cause: Enum): void` | Crea y vincula un `FailureRecord` a la OT, aplicando la taxonomía ISO 14224 al componente específico que falló.                                               | [[MTTO-002]]<br>FR-011           | **Comportamiento Rico:** La OT gobierna el reporte del fallo en lugar de crear la entidad de forma aislada.                                                                               |
| `AddMediaAttachment(fileUrl: String, fileType: Enum): void`                               | Adjunta evidencia multimedia al cierre técnico.                                                                                                               | [[MTTO-002]]<br>FR-013           | **Trazabilidad:** Agrega Value Objects (`MediaAttachment`) para auditoría.                                                                                                                |
| `SuspendExecution(reason: String): void`                                                  | Detiene inmediatamente la orden de trabajo (pasa a estado de suspensión/bloqueo) si se detectan condiciones inseguras.                                        | [[VIS-011]]<br>FR-232, NFR-234   | **Invariante Crítico (LOTO):** Si la telemetría IoT detecta energía activa durante la ejecución, la OT debe proteger la vida del trabajador suspendiendo el flujo normativo de inmediato. |
### 3.4. `BacklogItem` (`<<Entity>>`)

| Método  | Propósito / Regla de Negocio | Origen (Historia / FR) | Justificación Arquitectónica (DDD) |
| :--- | :--- | :--- | :--- |
| `UpdatePriorityScore(score: int): void` | Actualiza el puntaje consolidado. El cálculo es inyectado por un servicio de dominio (`IRimeCalculator`). | [[MTTO-026]]<br>ADR 002 | **Inversión de Control:** Permite que la estrategia de cálculo RIME cambie (de estática a dinámica) sin modificar la entidad. |
| `Defer(reason: String): void` | Cambia el estado a `DEFERRED`, posponiendo intencionalmente el trabajo. | [[MTTO-026]]<br>FR-064 | **Máquina de Estados:** Representa una decisión gerencial frente al backlog operativo. |

### 3.5. `FailureRecord` (`<<Entity>>`)

| Método  | Propósito / Regla de Negocio | Origen (Historia / FR) | Justificación Arquitectónica (DDD) |
| :--- | :--- | :--- | :--- |
| `UpdateClassification(mode: Enum, mechanism: Enum, cause: Enum): void` | Permite corregir o actualizar la taxonomía de la falla registrada. | [[MTTO-002]]<br>FR-011 | **Mutación Controlada:** Permite auditoría de QA (supervisor) antes del cierre final de la OT. |
## 4. Capa 3: Control de Recursos (INV)

### 4.1. `SparePart` (`<<Aggregate Root>>`)

| Método                                                                     | Propósito / Regla de Negocio                                                                          | Origen (Historia / FR)  | Justificación Arquitectónica (DDD)                                                                                                            |
| :----------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- | :---------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `UpdateStockPolicy(policy: Enum, reorderPoint: Decimal, maxCapacity: Decimal): void` | Modifica las reglas de reabastecimiento del repuesto.                                                 | [[INV-031]]<br>FR-173   | **Configuración de Negocio:** Encapsula la lógica de cómo y cuándo el sistema debe generar alertas de stock (INV-021).                        |
| `ReserveStock(quantity: Decimal): void`                                              | Incrementa la cantidad reservada (`ReservedQuantity`). Falla si excede la cantidad física disponible. | [[INV-006]]<br>FR-126   | **Invariante Crítico:** Protege el inventario asegurando que los materiales planeados para OTs futuras no se consuman accidentalmente.        |
| `ReleaseReservation(quantity: Decimal): void`                                        | Decrementa la cantidad reservada cuando una OT se cancela o finaliza.                                 | [[INV-006]] (Implícito) | **Consistencia de Estado:** Libera el stock comprometido para que vuelva a estar disponible.                                                  |
| `ReceiveStock(quantity: Decimal): void`                                              | Incrementa la cantidad en mano (`QuantityOnHand`) tras el ingreso al almacén.                         | [[INV-006]]<br>FR-125   | **Transacción de Inventario:** Único punto de mutación para las entradas de material, previniendo asignaciones manuales directas al atributo. |
| `IssueStock(quantity: Decimal): void`                                                | Decrementa la cantidad en mano y la cantidad reservada (si aplicaba), registrando el consumo real.    | [[INV-006]]<br>FR-127   | **Transacción de Inventario:** Garantiza que no se extraiga más stock del físicamente existente.                                              |

### 4.2. `MaterialRequirement` (`<<Entity>>`)

| Método  | Propósito / Regla de Negocio | Origen (Historia / FR) | Justificación Arquitectónica (DDD) |
| :--- | :--- | :--- | :--- |
| `MarkAsReserved(): void` | Cambia la bandera `IsReserved` a `true` una vez que el inventario central confirma la disponibilidad del material. | [[INV-006]]<br>FR-126 | **Integridad Transaccional:** Coordina el estado de la planificación en la OT con la reserva física real en el `SparePart`. |
| `RecordConsumption(actualQuantity: Decimal): void` | Registra la cantidad final de repuestos utilizados durante la ejecución de la Orden de Trabajo. | [[INV-006]]<br>FR-127 | **Cierre Técnico:** Permite capturar la diferencia entre la cantidad planificada y la consumida para ajustar inventarios y costos (KPIs). |

## 5. Capa 4: Convergencia Gemelo Digital (VIS)

### 5.1. `WorkPermit` (`<<Aggregate Root>>`)

| Método  | Propósito / Regla de Negocio | Origen (Historia / FR) | Justificación Arquitectónica (DDD) |
| :--- | :--- | :--- | :--- |
| `Approve(): void` | Transiciona el permiso al estado `APPROVED`, habilitándolo operativamente. | [[VIS-011]]<br>FR-225 | **Precondición Operativa:** Las OTs dependen de este estado para permitir la transición a "En Ejecución" (Fail-Safe). |
| `Revoke(reason: String): void` | Transiciona a `REVOKED` de forma inmediata por condiciones inseguras. | [[VIS-011]] (Implícito) | **Invariante de Seguridad:** Requiere justificación (reason). Altera de inmediato la autorización de trabajo en campo. |
| `Expire(): void` | Transiciona a `EXPIRED` automáticamente cuando se agota la ventana temporal. | Regla de Negocio (HSEQ) | **Máquina de Estados:** Representa el vencimiento natural del permiso (Límite temporal). |
| `Close(): void` | Transiciona a `CLOSED` una vez se finaliza la intervención y se retira el LOTO. | [[VIS-011]]<br>FR-231 | **Transición de Estado:** Cierre formal y documental del permiso. |

### 5.2. `IsolationPoint` (`<<Entity>>`)

| Método  | Propósito / Regla de Negocio | Origen (Historia / FR) | Justificación Arquitectónica (DDD) |
| :--- | :--- | :--- | :--- |
| `MarkAsVerified(): void` | Cambia la bandera `IsVerified` a `true` tras inspección de ingeniería. | [[VIS-011]] (Implícito) | **Dato Maestro (Safety):** Certifica que el punto físico identificado (ej. breaker) aísla efectivamente la energía del equipo. |

## 6. Capa 5: Seguridad y Gobernanza (ADM)

### 6.1. `User` (`<<Aggregate Root>>`)

| Método                                | Propósito / Regla de Negocio                                                                                                           | Origen (Historia / FR)        | Justificación Arquitectónica (DDD)                                                                                                                             |
| :---------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AssignRole(roleId: UUID): void`                | Vincula un rol al usuario, otorgándole el paquete de permisos asociado.                                                                | [[ADM-013]]<br>FR-251         | **Control de Acceso:** Gestiona la relación Many-to-Many entre usuarios y roles a través de la raíz de agregado.                                               |
| `RemoveRole(roleId: UUID): void`                | Revoca un rol previamente asignado al usuario.                                                                                         | [[ADM-013]] (Implícito)       | **Principio de Mínimo Privilegio:** Permite retirar accesos dinámicamente.                                                                                     |
| `RecordFailedLogin(): void`                     | Incrementa el contador de intentos fallidos. Si supera el umbral, cambia el estado a `LOCKED` y establece el tiempo de `LockoutUntil`. | [[ADM-014]]<br>FR-260         | **Protección Fuerza Bruta:** Encapsula la lógica de bloqueo de cuenta en el propio objeto usuario, evitando que el servicio de aplicación corrompa las reglas. |
| `RegisterSuccessfulLogin(): void`               | Reinicia a 0 el contador de intentos fallidos y limpia bloqueos.                                                                       | [[ADM-014]] (Implícito)       | **Ciclo de Seguridad:** Restaura el estado de confianza del usuario tras autenticación válida.                                                                 |
| `UpdatePassword(newPasswordHash: String): void` | Actualiza la credencial de acceso del usuario.                                                                                         | [[ADM-014]]<br>FR-261         | **Seguridad de Estado:** Asegura que la mutación del hash esté centralizada y pueda auditarse.                                                                 |
| `Deactivate(reason: String): void`              | Cambia el estado a `INACTIVE` (Soft-delete).                                                                                           | [[ADM-014]]<br>FR-262, FR-264 | **Retención de Auditoría:** Impide el inicio de sesión sin destruir las referencias históricas del usuario en otras tablas.                                    |
| `Activate(): void`                              | Restaura una cuenta inactiva o bloqueada al estado `ACTIVE`.                                                                           | [[ADM-014]]<br>FR-263         | **Recuperación de Estado:** Permite que recursos humanos o TI rehabiliten accesos.                                                                             |

### 6.2. `Role` (`<<Aggregate Root>>`)

| Método  | Propósito / Regla de Negocio | Origen (Historia / FR) | Justificación Arquitectónica (DDD) |
| :--- | :--- | :--- | :--- |
| `AddPermission(module: String, action: String): void` | Agrega una regla de autorización atómica al rol. | [[ADM-013]]<br>FR-248 | **Gestión RBAC:** El rol, como raíz de agregado, encapsula y protege su lista de permisos (Value Objects). |
| `RemovePermission(module: String, action: String): void` | Elimina una regla de autorización del rol. | [[ADM-013]] (Implícito) | **Gestión RBAC:** Permite restringir privilegios configurados erróneamente. |
| `ValidateSoD(): void` | Revisa la matriz interna de permisos para garantizar que no existan conflictos de Segregación de Funciones (ej. creador vs aprobador). | [[ADM-013]]<br>FR-249 | **Invariante Crítico:** Cumplimiento normativo ISO 55001/27001 para evitar fraudes internos o manipulaciones no auditadas. |

### 6.3. `AuditLog` (`<<Entity>>`)

| Método  | Propósito / Regla de Negocio | Origen (Historia / FR) | Justificación Arquitectónica (DDD) |
| :--- | :--- | :--- | :--- |
| `VerifyIntegrity(): boolean` | Recalcula el hash de los datos internos y lo compara con el `IntegrityHash` almacenado para confirmar que el registro no fue alterado físicamente en la BD. | [[ADM-032]]<br>FR-346, FR-351 | **Seguridad Inmutable:** Permite que el sistema valide criptográficamente la pureza de la trazabilidad durante auditorías o exportaciones. |

### 6.4. `AuthToken` (`<<Entity>>`)

| Método  | Propósito / Regla de Negocio | Origen (Historia / FR) | Justificación Arquitectónica (DDD) |
| :--- | :--- | :--- | :--- |
| `Revoke(): void` | Invalida el token forzosamente antes de su expiración natural. | [[ADM-014]]<br>FR-262 | **Control de Acceso:** Fundamental para matar sesiones activas instantáneamente cuando una cuenta es suspendida por riesgo de seguridad. |
| `MarkAsUsed(): void` | Invalida el token marcándolo como utilizado. | [[ADM-014]]<br>FR-261 | **Regla de Uso Único:** Evita ataques de replay en tokens sensibles como los enlaces de restablecimiento de contraseña. |



---


## **Notas Arquitectónicas**

- Las clases `EquipmentClass` ,`InventoryTransaction`, `Warehouse` y `Supplier` no exponen métodos de mutación en este modelo, ya que actúan como registros históricos inmutables (Ledger) y catálogos de Datos Maestros (Reference Data) respectivamente.
- Las clases `MeshMapping`, `TelemetrySignal`, `VisualLayer` y `SpatialMetadata` funcionan como proyecciones de lectura, recepción de telemetría inmutable o metadatos gráficos del frontend, por lo que no exponen comportamiento mutador complejo en este modelo MVP.
- La clase `WorkOrderAssignment` no expone comportamiento mutador, ya que actúa puramente como una entidad asociativa inmutable que captura el momento y rol en el que un usuario fue vinculado a una orden de trabajo