---
code: DT-DM-DOC-001
version: 1.5-MVP
date: 2026-05-22
status: Draft
author: Juan David
standard: 
  - ISO 9001:2015 
  - ISO 14224:2016
  - ISO 55000-Series
---

# Modelo de Entidades del Dominio

## 1. Propósito

Este documento es el complemento de negocio para el modelo de dominio de la solución del Gemelo Digital. Actúa como la Única Fuente de Verdad (SSoT) para el significado del dominio, los límites tácticos de DDD, los vocabularios de enumeradores (enums) y las reglas preliminares de persistencia antes de generar el ERD físico.

El documento se enfoca intencionalmente en las reglas de negocio y la trazabilidad del almacenamiento en lugar de los detalles de implementación. El modelo UML define la estructura; este documento explica por qué existe cada elemento, cómo debe interpretarse y cómo debe restringirse en la capa de base de datos.

## 2. Decisiones Críticas de Síntesis

### 2.1 División del Estado en `EquipmentUnit`

El campo `status` se descompone en tres dimensiones separadas:

- `operationalStatus`: captura la condición operativa real del activo, como el estado de actividad (uptime), inactividad (downtime) o espera (standby), en línea con la lógica de confiabilidad y estado operativo de la ISO 14224.
- `lifecycleStatus`: captura la fase contable y de negocio del activo, como almacenamiento, instalación, puesta en marcha (commissioning) o desmantelamiento (decommissioning), lo cual está más alineado con la gobernanza del ciclo de vida en la gestión de activos.
- `maintenanceStatus`: captura el contexto actual de mantenimiento, como si el activo está operativo, bajo mantenimiento o bajo prueba.

Esta división reduce el acoplamiento, evita sobrecargar la lógica de negocio y previene almacenar significados no relacionados en un solo campo. También facilita la validación transaccional porque cada dimensión puede restringirse de forma independiente.

### 2.2 Factores Cualitativos RIME

Los factores RIME en `WorkRequest` son tratados como selectores cualitativos en lugar de fórmulas monetarias fijas. Esto es importante para el MVP porque el backlog de mantenimiento debe funcionar en diferentes plantas con distintas escalas financieras, diferentes costos por tiempo de inactividad y diferentes niveles de madurez operativa.

Usar `CRITICAL`, `MAJOR` y `MINOR` como los niveles base mantiene el modelo auditable y comparable mientras permite que el motor de cálculo permanezca estable. Por lo tanto, el `economyFactor` no es un rango de moneda fijo (hard-coded) en el modelo de dominio; es un nivel de priorización relativo que puede ser mapeado a bandas de costos locales en la configuración.

### 2.3 Aislamiento Multi-Fuente y Extensibilidad de Seguridad

El modelo soporta intencionalmente tipos de aislamiento de seguridad más allá de la energía eléctrica o mecánica únicamente. Las intervenciones industriales pueden involucrar riesgos térmicos, químicos o gravitacionales dependiendo del activo y del alcance del trabajo. Por lo tanto, el modelo de permisos necesita valores extensibles y una alternativa controlada (fallback) como `OTHER`.

### 2.4 Nota de Modelado sobre el Conjunto de Estándares

El conjunto de cápsulas aprobadas proporciona una fuerte orientación para LOTO, competencias y gobernanza de seguridad, pero no incluye una cápsula dedicada a la taxonomía de permisos OSHA. Por esa razón, los vocabularios de permisos y aislamientos a continuación son vocabularios de proyecto normalizados y alineados con las referencias aprobadas en lugar de códigos literales extraídos de un solo estándar. Esto es deliberado y debe preservarse en el diseño del ERD como datos de búsqueda controlados (lookup data).

### 2.5 Nota de Modelado sobre `MediaAttachment`

`MediaAttachment` está modelado como un `Value Object` en la capa de dominio porque su significado de negocio es puramente evidencial. Sin embargo, una implementación relacional aún podría asignarle una llave subrogada técnica si el motor de almacenamiento requiere direccionamiento de filas independiente. Ese detalle de persistencia no cambia la clasificación en el dominio.

## 3. Tabla de Mapeo de Estereotipos

| Entidad | Estereotipo DDD | Justificación | Estándar de Referencia |
|---|---|---|---|
| `FunctionalLocation` | `Aggregate Root` | Posee la jerarquía de ubicación del activo y la definición del límite. | ISO 14224 Capítulos 8.1 y 8.2 |
| `EquipmentClass` | `Aggregate Root` | Posee la taxonomía de la clase del activo y la semántica de los límites específicos de la clase. | ISO 14224 Anexo A |
| `EquipmentUnit` | `Aggregate Root` | Posee el registro de inventario y la división de estado de tres vías para un activo físico. | ISO 14224 Capítulo 9.1 y Tabla 5 |
| `Subunit` | `Entity` | Depende del ciclo de vida del activo padre y del contexto de la taxonomía. | ISO 14224 Taxonomía Niveles 6–9 |
| `MaintainableItem` | `Entity` | Representa el nivel reparable más bajo utilizado para mantenimiento y análisis de fallas. | ISO 14224 Taxonomía Niveles 8–9 |
| `WorkRequest` | `Aggregate Root` | Inicia el flujo de admisión de mantenimiento y posee los factores de priorización RIME. | ISO 55000 orientación de riesgos y decisiones; ADR 002 |
| `MaintenancePlan` | `Aggregate Root` | Posee un cronograma de mantenimiento planificado y su cadencia. | ISO 14224 orientación de datos de mantenimiento |
| `WorkOrder` | `Aggregate Root` | Posee la ejecución, el historial, los adjuntos y los registros de trabajo descendentes. | ISO 14224 datos de eventos; ISO 9000 control de registros |
| `MediaAttachment` | `Value Object` | Carga útil (payload) de evidencia pura sin identidad de negocio independiente. | ISO 9000 información documentada y registros |
| `WorkOrderHistory` | `Entity` | Registro de transición del ciclo de vida de solo adición (append-only) para una orden de trabajo. | ISO 9000 inmutabilidad de registros |
| `FailureRecord` | `Entity` | Evento de falla histórico vinculado al historial del equipo y mantenimiento. | ISO 14224 lógica de fallas |
| `BacklogItem` | `Entity` | Registro de priorización derivado vinculado a la admisión de mantenimiento y al contexto del activo. | ISO 55000 orientación de clasificación de riesgos |
| `SparePart` | `Aggregate Root` | Registro maestro de inventario para una familia de partes con política de stock y datos de costos. | ISO 14224 datos de inventario; ISO 55000 orientación de planificación |
| `InventoryTransaction` | `Entity` | Registro de movimiento rastreable vinculado a partes, órdenes de trabajo y almacenes. | ISO 14224 datos de transacciones; ISO 9000 trazabilidad |
| `Warehouse` | `Aggregate Root` | Representa un límite de ubicación de stock con reglas de capacidad. | ISO 55000 orientación de planificación de recursos |
| `Supplier` | `Aggregate Root` | Posee la identidad de adquisiciones, el contexto comercial y la lógica de garantías. | ISO 9000 información documentada |
| `MeshMapping` | `Entity` | Registro de mapeo persistente entre el activo físico y la visualización digital. | ISO 9000 separación de datos vs. información |
| `TelemetrySignal` | `Entity` | Registro de medición cruda con marca de tiempo utilizado para trazabilidad y analítica de seguridad. | ISO 9000 seguimiento y medición |
| `WorkPermit` | `Aggregate Root` | Límite de autorización de seguridad para una intervención en campo. | ISO 55000 orientación de competencias y LOTO |
| `IsolationPoint` | `Entity` | Registro de aislamiento controlado ejecutado bajo un permiso o alcance de trabajo. | ISO 55000 orientación LOTO; ISO 14224 gobernanza de seguridad |
| `VisualLayer` | `Entity` | Registro de presentación asociado con una orden de trabajo y estado visual. | ISO 9000 comportamiento de registros |
| `SpatialMetadata` | `Value Object` | Descriptor inmutable de ubicación y geometría para un artefacto visual. | ISO 9000 separación de datos vs. información |
| `User` | `Aggregate Root` | Raíz del ciclo de vida de cuenta, contraseña, bloqueo (lockout) y token. | ISO 55000 gobernanza de auditorías; ISO 9000 control de auditorías |
| `Role` | `Aggregate Root` | Raíz de la semántica de autorización y agrupación de permisos. | ISO 55000 orientación de competencias y roles |
| `Permission` | `Value Object` | Regla de autorización atómica sin ciclo de vida independiente. | ISO 9000 flujo de trabajo controlado |
| `AuthToken` | `Entity` | Tiene ciclo de vida de emisión, uso y caducidad, y debe permanecer rastreable hasta su propietario. | ISO 9000 trazabilidad |
| `WorkOrderAssignment` | `Entity` | Relación auditable entre un usuario/rol y una orden de trabajo. | ISO 55000 control de competencias |
| `AuditLog` | `Entity` | Registro de auditoría de solo adición que contiene el estado antes y después (before/after). | ISO 9000 evidencia de auditoría e inmutabilidad de registros |

## 4. Vocabulario Controlado

### 4.1 `EquipmentUnit.operationalStatus`

| Valor | Significado |
|---|---|
| `UP` | El activo está en funcionamiento o listo en un sentido operativo. |
| `DOWN` | El activo no está disponible debido a una falla o interrupción. |
| `STANDBY` | El activo está listo pero no está produciendo activamente. |

### 4.2 `EquipmentUnit.lifecycleStatus`

| Valor | Significado |
|---|---|
| `IN_STORAGE` | El activo existe como inventario pero no está instalado. |
| `INSTALLED` | El activo está instalado físicamente en su ubicación funcional. |
| `COMMISSIONING` | El activo está siendo puesto en servicio. |
| `DECOMMISSIONED` | El activo ha sido retirado permanentemente del servicio. |

### 4.3 `EquipmentUnit.maintenanceStatus`

| Valor | Significado |
|---|---|
| `OPERATIONAL` | El activo no se encuentra actualmente bajo intervención de mantenimiento. |
| `UNDER_MAINTENANCE` | El activo está siendo reparado o atendido activamente. |
| `UNDER_TEST` | El activo está bajo verificación o prueba funcional. |

### 4.4 Vocabularios de factores RIME

Los cuatro factores de `WorkRequest` utilizan los mismos niveles controlados.

| Valor | Peso | Significado |
|---|---|---|
| `CRITICAL` | 3 | Prioridad más alta / exposición máxima. |
| `MAJOR` | 2 | Prioridad media / exposición material. |
| `MINOR` | 1 | Prioridad más baja / exposición limitada. |

### 4.5 `MaintenancePlan.frequencyType`

| Valor | Significado |
|---|---|
| `CALENDAR_TIME` | El plan es impulsado por el tiempo calendario transcurrido. |
| `OPERATING_HOURS` | El plan es impulsado por las horas de funcionamiento acumuladas. |
| `CYCLES` | El plan es impulsado por ciclos o arranques. |

### 4.6 `WorkPermit.permitType`

| Valor | Significado |
|---|---|
| `HOT_WORK` | Trabajo que involucra llama, chispas, soldadura o corte. |
| `CONFINED_SPACE` | Trabajo dentro de un área confinada o de acceso restringido. |
| `ELECTRICAL_WORK` | Trabajo en o cerca de sistemas eléctricos energizados. |
| `WORK_AT_HEIGHT` | Trabajo en altura con riesgo de caída. |
| `EXCAVATION` | Trabajo que expone riesgos del subsuelo o trincheras. |
| `CHEMICAL` | Trabajo que involucra químicos peligrosos o riesgo de exposición. |
| `THERMAL` | Trabajo que involucra riesgos de alta temperatura. |
| `OTHER` | Tipo de permiso específico del sitio no cubierto por la lista estándar. |

### 4.7 `WorkPermit.status`

| Valor | Significado |
|---|---|
| `DRAFT` | Permiso preparado pero aún no emitido. |
| `ISSUED` | Permiso aprobado y liberado. |
| `ACTIVE` | El permiso está actualmente en vigor. |
| `SUSPENDED` | El permiso está pausado temporalmente. |
| `CLOSED` | El permiso ha sido cerrado formalmente. |
| `EXPIRED` | La ventana de validez del permiso ha expirado. |

### 4.8 `IsolationPoint.isolationType`

| Valor | Significado |
|---|---|
| `ELECTRICAL` | Aislamiento de energía eléctrica. |
| `MECHANICAL` | Aislamiento de energía mecánica. |
| `HYDRAULIC` | Aislamiento de energía hidráulica. |
| `PNEUMATIC` | Aislamiento de energía neumática. |
| `THERMAL` | Aislamiento de energía térmica. |
| `CHEMICAL` | Aislamiento químico. |
| `GRAVITATIONAL` | Riesgo de gravedad / energía potencial almacenada. |
| `OTHER` | Tipo de aislamiento específico del sitio no cubierto por la lista estándar. |

### 4.9 `SparePart.stockPolicy`

| Valor | Significado |
|---|---|
| `REORDER_POINT` | Reabastecer cuando el inventario alcance un umbral de activación (trigger). |
| `MIN_MAX` | Mantener el stock entre niveles mínimo y máximo. |
| `JUST_IN_TIME` | Reabastecer solo cuando se espere demanda. |

### 4.10 `MediaAttachment.fileType`

| Valor | Significado |
|---|---|
| `PDF` | Portable Document Format (Formato de Documento Portátil). |
| `JPG` | Archivo de imagen JPEG. |
| `PNG` | Archivo de imagen Portable Network Graphics. |

### 4.11 `MaintainableItem.status`

| Valor | Significado | Norma de Referencia |
|---|---|---|
| `OPERATIONAL` | Saludable y operando dentro de los parámetros de diseño. | ISO 13374 (Normal) |
| `DEGRADED` | Falla parcial o advertencia de condición; requiere monitoreo o intervención planificada. | ISO 14224 (Partial Failure) / ISO 13374 (Alert) |
| `FAILED` | Falla funcional completa; el ítem ya no puede realizar su función requerida. | ISO 14224 (Complete Failure) |
| `UNDER_REPAIR` | El componente está siendo mantenido, reparado o reemplazado activamente. | Estado transaccional EAM |
| `REPLACED` | Fin del ciclo de vida del componente en esa ubicación; conservado para historial de MTBF. | Historial de Confiabilidad |

### 4.12 `WorkRequest.status`

| Valor | Significado | Norma / Concepto |
|---|---|---|
| `NEW` | Solicitud recién creada y pendiente de evaluación. | Admisión básica de CMMS |
| `APPROVED` | Aprobada y promovida a Orden de Trabajo (`WorkOrder`). | Transición a planificación |
| `REJECTED` | Rechazada por ser inválida, duplicada o falsa alarma. | Trazabilidad de falsos positivos |

### 4.13 `MaintenancePlan.status`

| Valor | Significado | Norma / Concepto |
|---|---|---|
| `DRAFT` | Plan en fase de diseño o revisión técnica, inactivo. | Control documental |
| `ACTIVE` | Activo y disparando órdenes de trabajo según su ciclo. | Operativo |
| `INACTIVE` | Desactivado temporalmente por parada o cambio operativo. | Suspensión de ciclos |
| `ARCHIVED` | Obsoleto o reemplazado; conservado para historial de auditoría. | ISO 55001 Ciclo de Vida |

### 4.14 `MaintenancePlan.maintenanceMethod`

| Valor | Significado | Norma / Concepto |
|---|---|---|
| `PREVENTIVE` | Mantenimiento preventivo sistemático (basado en tiempo/uso). | ISO 14224 (Preventative) |
| `PREDICTIVE` | Monitoreo predictivo (análisis de vibraciones, termografía, etc.). | ISO 14224 (Condition-based) |
| `CONDITION_BASED` | Acciones directas disparadas por límites de sensores en telemetría. | ISO 13374 / CBM |

### 4.15 `WorkOrder.currentStatus`

| Valor | Significado | Norma / Concepto |
|---|---|---|
| `PLANNING` | Definición de repuestos, permisos LOTO y recursos. | FSM - Planificación |
| `WAITING_PARTS` | Espera activa de repuestos en almacén/compras. | FSM - Cuello de botella logístico |
| `SCHEDULED` | Asignado con técnico y fecha de ejecución programada. | FSM - Programación |
| `IN_PROGRESS` | El técnico está ejecutando la labor (clock-in activo). | FSM - Ejecución ("Wrench Time") |
| `COMPLETE` | Trabajo técnico finalizado, en espera de revisión. | FSM - Pre-cierre técnico |
| `CLOSED` | Cerrada administrativamente e ingresados los códigos de falla. | FSM - QA / Auditoría ISO 14224 |

### 4.16 `WorkOrder.maintenanceMethod`

| Valor | Significado | Norma / Concepto |
|---|---|---|
| `CORRECTIVE` | Mantenimiento correctivo reactivo (reparación tras falla). | ISO 14224 (Corrective) |
| `PREVENTIVE` | Preventivo sistemático programado (derivado de plan). | ISO 14224 (Preventative) |
| `PREDICTIVE` | Monitoreo o inspección predictiva programada. | ISO 14224 (Condition-based) |
| `IMPROVEMENT` | Modificación, rediseño o mejora técnica (CAPEX/OPEX). | Gestión de Cambios / Ingeniería |

### 4.17 `WorkOrder.criticality`

| Valor | Significado | Norma / Concepto |
|---|---|---|
| `EMERGENCY` | Detención total de planta, riesgo de seguridad o ambiental inminente. | Criticidad Máxima |
| `URGENT` | Falla con impacto operativo inmediato; reparar en menos de 24-48h. | Prioridad Alta |
| `NORMAL` | Planificable dentro de los ciclos y ventanas semanales. | Prioridad Media |
| `LOW` | Tareas estéticas o menores de conveniencia operativa. | Prioridad Baja |

### 4.18 `BacklogItem.status`

| Valor | Significado | Norma / Concepto |
|---|---|---|
| `PENDING` | En espera de análisis técnico o definición de materiales. | Cola de planificación |
| `READY` | Planificado completamente y listo para ser calendarizado. | Listo para programar |
| `DEFERRED` | Aplazado intencionalmente (falta de presupuesto o parada general). | Suspensión en cola |

### 4.19 `SparePart.status`

| Valor | Significado | Norma / Concepto |
|---|---|---|
| `ACTIVE` | Activo y disponible para consumo y compras. | Gestión de Stock |
| `OBSOLETE` | Obsoleto, no se permite nueva compra (se mantiene para historial). | ISO 55001 Ciclo de Vida |
| `SUSPENDED` | Temporalmente bloqueado por control de calidad o problemas del proveedor. | Control de Calidad |

### 4.20 `InventoryTransaction.transactionType`

| Valor | Significado | Norma / Concepto |
|---|---|---|
| `RECEIPT` | Entrada de inventario (compra, devolución, transferencia). | Ingesta de Stock |
| `ISSUE` | Salida de inventario (consumo en Orden de Trabajo). | Carga a Costos de OT |
| `ADJUSTMENT` | Ajuste manual/automático por discrepancia en conteo físico. | Conciliación de Inventario |

## 5. Tabla de Trazabilidad de Columnas Físicas

**Nota:** Las llaves foráneas (Foreign Keys) derivadas de las asociaciones se omiten en la lista de campos a continuación para mayor legibilidad, pero deben agregarse en el ERD físico. El siguiente mapeo se centra en los campos lógicos que ya están presentes en el modelo de PlantUML.

### 5.1 Capa de Taxonomía

| Entidad | Campo Lógico | Tipo Físico (Estándar SQL) | Nulabilidad | Restricciones / Llaves | Justificación |
|---|---|---|---|---|---|
| `FunctionalLocation` | `tagNumber` | `VARCHAR(50)` | NOT NULL | UNIQUE | Identidad del tag de la ISO 14224 y trazabilidad de la ubicación. |
| `FunctionalLocation` | `name` | `VARCHAR(150)` | NOT NULL |  | Nombre de la ubicación legible por humanos. |
| `FunctionalLocation` | `description` | `VARCHAR(255)` | NULL |  | Texto explicativo opcional. |
| `FunctionalLocation` | `criticality` | `VARCHAR(30)` | NOT NULL | CHECK o lookup | Vocabulario de prioridad controlado. |
| `FunctionalLocation` | `geographicLocation` | `VARCHAR(150)` | NULL |  | Contexto físico de la ubicación. |
| `FunctionalLocation` | `hierarchyLevel` | `SMALLINT` | NOT NULL | CHECK (1..9) | Nivel de taxonomía ISO 14224. |
| `EquipmentClass` | `className` | `VARCHAR(120)` | NOT NULL | UNIQUE | Datos maestros a nivel de clase. |
| `EquipmentClass` | `description` | `VARCHAR(255)` | NULL |  | Descripción de la clase. |
| `EquipmentClass` | `manufacturerStandard` | `VARCHAR(120)` | NULL |  | Referencia de estandarización. |
| `EquipmentUnit` | `serialNumber` | `VARCHAR(100)` | NOT NULL | UNIQUE | Integridad de la identificación del activo. |
| `EquipmentUnit` | `manufacturer` | `VARCHAR(120)` | NOT NULL |  | Procedencia del activo. |
| `EquipmentUnit` | `model` | `VARCHAR(120)` | NOT NULL |  | Identificación del tipo de activo. |
| `EquipmentUnit` | `purchaseDate` | `DATE` | NOT NULL |  | Cronología de adquisiciones. |
| `EquipmentUnit` | `rejectionReason` | `VARCHAR(255)` | NULL |  | Solo está presente cuando se rechaza la adquisición. |
| `EquipmentUnit` | `boundaryStart` | `VARCHAR(150)` | NOT NULL |  | Punto de inicio de la definición del límite. |
| `EquipmentUnit` | `boundaryEnd` | `VARCHAR(150)` | NOT NULL |  | Punto final de la definición del límite. |
| `EquipmentUnit` | `acquisitionDate` | `DATE` | NOT NULL |  | Trazabilidad de la adquisición del activo. |
| `EquipmentUnit` | `installationDate` | `DATE` | NULL |  | La instalación puede estar pendiente. |
| `EquipmentUnit` | `operationStartDate` | `DATE` | NULL |  | El inicio operativo puede estar pendiente. |
| `EquipmentUnit` | `operatingHours` | `BIGINT` | NOT NULL | DEFAULT 0 | Seguimiento de confiabilidad y uso. |
| `EquipmentUnit` | `operationalStatus` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Vocabulario de estado operativo controlado. |
| `EquipmentUnit` | `lifecycleStatus` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Vocabulario de ciclo de vida controlado. |
| `EquipmentUnit` | `maintenanceStatus` | `VARCHAR(30)` | NOT NULL | CHECK o lookup | Vocabulario de estado de mantenimiento controlado. |
| `Subunit` | `subunitType` | `VARCHAR(80)` | NOT NULL |  | Taxonomía del subcomponente. |
| `Subunit` | `name` | `VARCHAR(120)` | NOT NULL |  | Etiqueta del subcomponente. |
| `MaintainableItem` | `componentName` | `VARCHAR(120)` | NOT NULL |  | Identidad del ítem mantenible. |
| `MaintainableItem` | `subunitType` | `VARCHAR(80)` | NOT NULL |  | Clasificación taxonómica. |
| `MaintainableItem` | `sparePartType` | `VARCHAR(80)` | NULL |  | Correspondencia opcional de partes de repuesto. |
| `MaintainableItem` | `designAttributes` | `VARCHAR(255)` | NULL |  | Propiedades estáticas de diseño. |
| `MaintainableItem` | `status` | `VARCHAR(30)` | NOT NULL | CHECK o lookup | Estado del ciclo de vida del ítem. |

### 5.2 Mantenimiento y Gestión de Trabajo

| Entidad | Campo Lógico | Tipo Físico (Estándar SQL) | Nulabilidad | Restricciones / Llaves | Justificación |
|---|---|---|---|---|---|
| `WorkRequest` | `description` | `VARCHAR(255)` | NOT NULL |  | Narrativa de la solicitud. |
| `WorkRequest` | `priority` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Etiqueta de prioridad de la solicitud. |
| `WorkRequest` | `requestDate` | `TIMESTAMP` | NOT NULL |  | Línea de tiempo para auditoría. |
| `WorkRequest` | `requestSource` | `VARCHAR(80)` | NOT NULL |  | Origen de la solicitud. |
| `WorkRequest` | `status` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Estado del ciclo de vida de la solicitud. |
| `WorkRequest` | `riskFactor` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Vocabulario controlado RIME. |
| `WorkRequest` | `impactFactor` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Vocabulario controlado RIME. |
| `WorkRequest` | `maintainabilityFactor` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Vocabulario controlado RIME. |
| `WorkRequest` | `economyFactor` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Vocabulario controlado RIME. |
| `MaintenancePlan` | `maintenanceMethod` | `VARCHAR(80)` | NOT NULL | CHECK o lookup | Estrategia de mantenimiento (PM, PdM, CBM). |
| `MaintenancePlan` | `frequency` | `VARCHAR(80)` | NOT NULL |  | Descripción de la frecuencia legible por humanos. |
| `MaintenancePlan` | `frequencyType` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Cadencia controlada del plan. |
| `MaintenancePlan` | `nextWorkOrderDate` | `DATE` | NULL |  | Fecha de ejecución programada (Calculada). |
| `MaintenancePlan` | `status` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Estado del ciclo de vida del plan (documento). |
| `WorkOrder` | `currentStatus` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Estado del ciclo de vida de ejecución (FSM). |
| `WorkOrder` | `maintenanceMethod` | `VARCHAR(80)` | NOT NULL | CHECK o lookup | Método de mantenimiento (Correctivo, Preventivo, etc.). |
| `WorkOrder` | `creationDate` | `TIMESTAMP` | NOT NULL |  | Marca de tiempo (timestamp) de creación de la orden. |
| `WorkOrder` | `scheduledDate` | `TIMESTAMP` | NULL |  | Inicio planeado. |
| `WorkOrder` | `actualStart` | `TIMESTAMP` | NULL |  | Inicio real de la ejecución. |
| `WorkOrder` | `actualFinish` | `TIMESTAMP` | NULL |  | Finalización real de la ejecución. |
| `WorkOrder` | `actualLaborHours` | `DECIMAL(10,2)` | NULL |  | Duración laboral real (Calculada). |
| `WorkOrder` | `criticality` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Etiqueta de criticidad / prioridad de la OT. |
| `MediaAttachment` | `fileUrl` | `VARCHAR(255)` | NOT NULL |  | Ubicación de la evidencia. |
| `MediaAttachment` | `fileType` | `VARCHAR(10)` | NOT NULL | CHECK o lookup | Formato de archivo adjunto controlado. |
| `MediaAttachment` | `uploadedAt` | `TIMESTAMP` | NOT NULL |  | Tiempo de subida/ingesta de la evidencia. |
| `WorkOrderHistory` | `oldStatus` | `VARCHAR(20)` | NULL |  | Estado anterior del ciclo de vida (NULL si es primer estado). |
| `WorkOrderHistory` | `newStatus` | `VARCHAR(20)` | NOT NULL |  | Nuevo estado del ciclo de vida. |
| `WorkOrderHistory` | `timestamp` | `TIMESTAMP` | NOT NULL |  | Tiempo de transición. |
| `WorkOrderHistory` | `durationSeconds` | `BIGINT` | NULL |  | Tiempo empleado en el estado (Calculado al transicionar). |
| `FailureRecord` | `failureId` | `UUID` | NOT NULL | PK | Identidad del evento de falla. |
| `FailureRecord` | `failureMode` | `VARCHAR(120)` | NOT NULL | CHECK o lookup | Codificación de fallas de la ISO 14224. |
| `FailureRecord` | `failureMechanism` | `VARCHAR(120)` | NOT NULL | CHECK o lookup | Codificación de fallas de la ISO 14224. |
| `FailureRecord` | `failureCause` | `VARCHAR(120)` | NOT NULL | CHECK o lookup | Codificación de fallas de la ISO 14224. |
| `FailureRecord` | `downtime` | `DECIMAL(10,2)` | NOT NULL |  | Métrica de análisis de confiabilidad (Calculada). |
| `FailureRecord` | `status` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Estado del registro de fallas. |
| `BacklogItem` | `priorityScore` | `INT` | NOT NULL |  | Puntaje del backlog derivado de RIME (Calculado). |
| `BacklogItem` | `status` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Estado del ciclo de vida del backlog (priorización). |

### 5.3 Inventario y Suministro

| Entidad | Campo Lógico | Tipo Físico (Estándar SQL) | Nulabilidad | Restricciones / Llaves | Justificación |
|---|---|---|---|---|---|
| `SparePart` | `sku` | `VARCHAR(80)` | NOT NULL | UNIQUE | Identidad de la parte. |
| `SparePart` | `description` | `VARCHAR(255)` | NOT NULL |  | Descripción de la parte legible por humanos. |
| `SparePart` | `manufacturer` | `VARCHAR(120)` | NOT NULL |  | Identidad del proveedor/fabricante. |
| `SparePart` | `commodityCode` | `VARCHAR(80)` | NULL |  | Código de clasificación. |
| `SparePart` | `reorderPoint` | `DECIMAL(12,4)` | NOT NULL |  | Umbral mínimo de activación de compra. |
| `SparePart` | `unitOfMeasure` | `VARCHAR(20)` | NOT NULL |  | Unidad de medida estándar (UoM). |
| `SparePart` | `stockPolicy` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Política de reabastecimiento (Min/Max, Reorder Point, JIT). |
| `SparePart` | `quantityOnHand` | `DECIMAL(12,4)` | NOT NULL |  | Cantidad actualmente en inventario físico. |
| `SparePart` | `reservedQuantity` | `DECIMAL(12,4)` | NOT NULL | DEFAULT 0 | Stock comprometido para órdenes planificadas. |
| `SparePart` | `maxCapacity` | `DECIMAL(12,4)` | NULL |  | Límite físico del almacén para la parte. |
| `SparePart` | `unitCost` | `DECIMAL(12,2)` | NOT NULL |  | Costo unitario estándar de adquisición. |
| `SparePart` | `status` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Estado de disponibilidad del repuesto. |
| `InventoryTransaction` | `quantity` | `DECIMAL(12,4)` | NOT NULL |  | Cantidad transada (positiva para entradas, negativa para salidas). |
| `InventoryTransaction` | `transactionType` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Tipo de movimiento (RECEIPT, ISSUE, ADJUSTMENT). |
| `InventoryTransaction` | `timestamp` | `TIMESTAMP` | NOT NULL |  | Registro temporal preciso del movimiento. |
| `InventoryTransaction` | `reason` | `VARCHAR(255)` | NOT NULL |  | Razón del movimiento o referencia a documentos externos. |
| `InventoryTransaction` | `totalCost` | `DECIMAL(12,2)` | NOT NULL |  | Costo total de la transacción (Cantidad * Costo). |
| `Warehouse` | `name` | `VARCHAR(80)` | NOT NULL | UNIQUE | Identidad del almacén. |
| `Warehouse` | `location` | `VARCHAR(255)` | NOT NULL |  | Dirección o ubicación física del almacén. |
| `Warehouse` | `capacity` | `DECIMAL(12,4)` | NOT NULL |  | Capacidad máxima volumétrica o de carga del almacén. |
| `Supplier` | `name` | `VARCHAR(120)` | NOT NULL | UNIQUE | Identidad comercial del proveedor. |
| `Supplier` | `contactInfo` | `VARCHAR(255)` | NOT NULL |  | Teléfono, correo o dirección de contacto. |
| `Supplier` | `warrantyTerms` | `VARCHAR(255)` | NOT NULL |  | Términos estándar de garantía comercial. |
| `WorkOrderSparePart` | `plannedQuantity` | `DECIMAL(12,4)` | NOT NULL |  | Repuestos planificados antes de la ejecución de la OT. |
| `WorkOrderSparePart` | `actualQuantity` | `DECIMAL(12,4)` | NULL |  | Repuestos realmente consumidos durante la ejecución de la OT. |

### 5.4 Convergencia Digital y Visualización de Seguridad

| Entidad | Campo Lógico | Tipo Físico (Estándar SQL) | Nulabilidad | Restricciones / Llaves | Justificación |
|---|---|---|---|---|---|
| `MeshMapping` | `meshUuid` | `UUID` | NOT NULL | UNIQUE | Identidad del mapeo del gemelo digital. |
| `MeshMapping` | `mappingStatus` | `VARCHAR(30)` | NOT NULL | CHECK o lookup | Estado del ciclo de vida del mapeo. |
| `MeshMapping` | `lastSyncTime` | `TIMESTAMP` | NULL |  | Tiempo de la última sincronización. |
| `TelemetrySignal` | `signalType` | `VARCHAR(80)` | NOT NULL |  | Etiqueta de la señal del sensor. |
| `TelemetrySignal` | `value` | `DECIMAL(18,6)` | NOT NULL |  | Valor de la medición cruda. |
| `TelemetrySignal` | `unit` | `VARCHAR(20)` | NOT NULL |  | Unidad de medición. |
| `TelemetrySignal` | `threshold` | `DECIMAL(18,6)` | NULL |  | Umbral de alerta. |
| `TelemetrySignal` | `timestamp` | `TIMESTAMP` | NOT NULL |  | Tiempo de medición. |
| `TelemetrySignal` | `isSafetyCritical` | `BOOLEAN` | NOT NULL | DEFAULT FALSE | Bandera de clasificación de seguridad. |
| `WorkPermit` | `permitIdentifier` | `VARCHAR(80)` | NOT NULL | UNIQUE | Trazabilidad del permiso. |
| `WorkPermit` | `permitType` | `VARCHAR(30)` | NOT NULL | CHECK o lookup | Vocabulario de permisos. |
| `WorkPermit` | `contractorName` | `VARCHAR(150)` | NOT NULL |  | Identificación del contratista. |
| `WorkPermit` | `status` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Estado del ciclo de vida del permiso. |
| `IsolationPoint` | `isolationTag` | `VARCHAR(80)` | NOT NULL | UNIQUE | Identidad del punto de aislamiento. |
| `IsolationPoint` | `isolationType` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Vocabulario de aislamiento. |
| `IsolationPoint` | `isVerified` | `BOOLEAN` | NOT NULL | DEFAULT FALSE | Estado de verificación. |
| `VisualLayer` | `layerType` | `VARCHAR(80)` | NOT NULL |  | Tipo de representación visual. |
| `VisualLayer` | `opacityLevel` | `DECIMAL(5,2)` | NOT NULL | CHECK (0..1) | Control de renderizado. |
| `VisualLayer` | `status` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Estado de la capa visual. |
| `SpatialMetadata` | `position` | `VARCHAR(120)` | NOT NULL |  | Coordenada espacial o descriptor. |
| `SpatialMetadata` | `rotation` | `VARCHAR(120)` | NULL |  | Descriptor de orientación. |
| `SpatialMetadata` | `scale` | `VARCHAR(120)` | NULL |  | Descriptor de escala. |

### 5.5 Gobernanza y Seguridad

| Entidad | Campo Lógico | Tipo Físico (Estándar SQL) | Nulabilidad | Restricciones / Llaves | Justificación |
|---|---|---|---|---|---|
| `User` | `username` | `VARCHAR(80)` | NOT NULL | UNIQUE | Identidad de la cuenta. |
| `User` | `email` | `VARCHAR(150)` | NOT NULL | UNIQUE | Identidad de contacto e inicio de sesión. |
| `User` | `status` | `VARCHAR(20)` | NOT NULL | CHECK o lookup | Estado del ciclo de vida de la cuenta. |
| `User` | `passwordHash` | `VARCHAR(255)` | NOT NULL |  | Seguridad de la credencial. |
| `User` | `failedLoginAttempts` | `INT` | NOT NULL | DEFAULT 0 | Control de bloqueos. |
| `User` | `lockoutUntil` | `TIMESTAMP` | NULL |  | Ventana de bloqueo (lockout) de cuenta. |
| `Role` | `roleName` | `VARCHAR(80)` | NOT NULL | UNIQUE | Nombre del rol de autorización. |
| `Role` | `description` | `VARCHAR(255)` | NULL |  | Significado del rol. |
| `Role` | `isSystemRole` | `BOOLEAN` | NOT NULL | DEFAULT FALSE | Protección de rol raíz/administrador. |
| `Permission` | `module` | `VARCHAR(80)` | NOT NULL |  | Alcance (scope) de autorización. |
| `Permission` | `action` | `VARCHAR(80)` | NOT NULL |  | Acción de autorización. |
| `AuthToken` | `tokenHash` | `VARCHAR(255)` | NOT NULL | UNIQUE | Seguridad del token. |
| `AuthToken` | `expiresAt` | `TIMESTAMP` | NOT NULL |  | Control de caducidad. |
| `AuthToken` | `isUsed` | `BOOLEAN` | NOT NULL | DEFAULT FALSE | Estado de uso único (one-time-use). |
| `WorkOrderAssignment` | `roleInWork` | `VARCHAR(80)` | NOT NULL |  | Rol asignado en la ejecución. |
| `WorkOrderAssignment` | `assignedAt` | `TIMESTAMP` | NOT NULL |  | Tiempo de asignación. |
| `AuditLog` | `entityType` | `VARCHAR(80)` | NOT NULL |  | Tipo de entidad auditada. |
| `AuditLog` | `actionType` | `VARCHAR(80)` | NOT NULL |  | Acción auditada. |
| `AuditLog` | `timestamp` | `TIMESTAMP` | NOT NULL |  | Tiempo del evento de auditoría. |
| `AuditLog` | `integrityHash` | `VARCHAR(255)` | NOT NULL |  | Evidencia de manipulación (tamper evidence). |
| `AuditLog` | `entityIdentifier` | `VARCHAR(120)` | NOT NULL |  | Correlaciona el registro con el objeto de negocio. |
| `AuditLog` | `previousState` | `JSON` | NULL |  | Imagen previa (before-image) para trazabilidad de auditoría. |
| `AuditLog` | `newState` | `JSON` | NULL |  | Imagen posterior (after-image) para trazabilidad de auditoría. |

## 6. Matriz de Correspondencia de Tipos de Datos (SQL Estándar vs. PostgreSQL)

Para garantizar la viabilidad física del modelo lógico y su correcta implementación en el motor de base de datos seleccionado (**PostgreSQL**), se ha validado y mapeado formalmente cada tipo de datos físico propuesto:

| Tipo Físico (Estándar SQL) | Tipo Nativo en PostgreSQL | Equivalente Técnico Alternativo | Impacto Técnico / Justificación en PostgreSQL |
| :--- | :--- | :--- | :--- |
| `VARCHAR(N)` | `VARCHAR(N)` o `CHARACTER VARYING(N)` | `TEXT` | PostgreSQL maneja cadenas de longitud variable eficientemente. `TEXT` no tiene penalización de rendimiento y se prefiere cuando no se requiere un límite estricto de longitud de caracteres. |
| `SMALLINT` | `SMALLINT` o `INT2` | Ninguno | Entero con signo de 2 bytes (rango -32,768 a 32,767). Óptimo para cardinalidades y niveles taxonómicos (como `hierarchyLevel`). |
| `INT` | `INTEGER` o `INT4` | Ninguno | Entero con signo de 4 bytes (rango -2,147,483,648 a 2,147,483,647). Estándar para contadores simples (como `failedLoginAttempts`). |
| `BIGINT` | `BIGINT` o `INT8` | Ninguno | Entero con signo de 8 bytes. Usado para métricas acumuladas grandes como horas operativas (`operatingHours`) y duraciones de transición. |
| `DATE` | `DATE` | Ninguno | Tipo de datos de 4 bytes para almacenar fechas de calendario sin zona horaria (año, mes, día). |
| `TIMESTAMP` | `TIMESTAMP` | `TIMESTAMPTZ` (Recomendado) | `TIMESTAMP` almacena fecha y hora sin zona horaria. Se recomienda `TIMESTAMPTZ` (Timestamp con zona horaria) para logs de auditoría, marcas de creación e inicio de órdenes de trabajo para evitar discrepancias por husos horarios. |
| `DECIMAL(P,S)` | `DECIMAL(P,S)` o `NUMERIC(P,S)` | Ninguno | Tipo de precisión exacta con escala de usuario. Esencial para valores monetarios (`unitCost`), dimensiones de sensores (`value`, `threshold`) y porcentajes exactos (`opacityLevel`). |
| `UUID` | `UUID` | Ninguno | Tipo de datos nativo de 128 bits para Identificadores Únicos Universales (UUID). Mucho más eficiente que almacenar UUID como `VARCHAR(36)`. Requiere cargar la extensión `uuid-ossp` o usar la función nativa `gen_random_uuid()` para generación de llaves en la base de datos. |
| `BOOLEAN` | `BOOLEAN` o `BOOL` | Ninguno | Tipo lógico que almacena `TRUE` o `FALSE`. |
| `JSON` | `JSON` | `JSONB` (Recomendado) | `JSON` almacena el texto literal, lo cual requiere parseo en cada consulta. Se recomienda usar `JSONB` (JSON Binario Descompuesto) porque almacena el contenido en formato binario, soporta indexación rápida (índices GIN) y es mucho más eficiente para consultas de auditoría (`previousState` y `newState`). |

## 7. Notas Finales

- El modelo de dominio debe seguir siendo la fuente de verdad del negocio hasta que se genere el ERD físico.
- Los vocabularios controlados que son estables y de baja cardinalidad pueden hacerse cumplir mediante restricciones `CHECK`.
- Los vocabularios que probablemente cambiarán o crecerán deben trasladarse a tablas de búsqueda (lookup tables).
- Los registros de fallas y auditorías deben permanecer de solo adición (append-only) y rastreables.
- El vocabulario relacionado con la seguridad para permisos y puntos de aislamiento debe tratarse como datos de cumplimiento controlados, no como texto libre.
