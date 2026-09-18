---
code: DT-DM-DOC-001
version: 1.3
date: 2026-09-14
status: Aprobado — Especificación Conceptual de Dominio
author: Juan David Julio Serrano
standard:
  - ISO 9001:2015
  - ISO 14224:2016
  - ISO 55000-Series
  - ISO 13374-Series
  - ISO 27001:2022
---

# Especificación del Modelo de Dominio

## 1. Propósito

Este documento es el complemento de negocio para el modelo de dominio de la solución del Gemelo Digital. Actúa como la Única Fuente de Verdad (SSoT) para el significado del dominio, los límites tácticos de DDD, los vocabularios de enumeradores (enums) y las reglas preliminares de persistencia antes de generar el ERD físico.

El documento se enfoca en las reglas de negocio y la trazabilidad del almacenamiento en lugar de los detalles de implementación. El modelo UML define la estructura; este documento explica por qué existe cada elemento, cómo debe interpretarse y cómo debe restringirse en la capa de base de datos.

## 2. Decisiones Críticas de Síntesis

### 2.1 División del Estado en EquipmentUnit

El campo status se descompone en cuatro dimensiones independientes y especializadas:

- operationalStatus: captura la condición operativa real del activo, como el estado de actividad (uptime), inactividad (downtime) o espera (standby), en línea con la lógica de confiabilidad y estado operativo de la ISO 14224.
- lifecycleStatus: captura la fase contable y de negocio del activo, como almacenamiento, instalación, puesta en marcha (commissioning) o desmantelamiento (decommissioning), lo cual está más alineado con la gobernanza del ciclo de vida en la gestión de activos (ISO 55000).
- maintenanceStatus: captura el contexto actual de mantenimiento, como si el activo está operativo, bajo mantenimiento o bajo prueba.
- healthStatus: captura la salud física y mecánica consolidada (Undetermined, Good, Fair, Serious, Critical, etc.) basada en telemetría de monitoreo de condición (ISO 13374).

Esta división reduce el acoplamiento, evita sobrecargar la lógica de negocio y previene almacenar significados no relacionados en un solo campo. También facilita la validación transaccional porque cada dimensión puede restringirse de forma independiente.

### 2.2 Priorización RIME Configurable

Para cumplir con la gestión de riesgos exigida por la norma ISO 55001 y las mejores prácticas de la ingeniería de mantenimiento, el sistema adopta el estándar RIME (Ranking Index for Maintenance Expenditure).

De acuerdo con [[ADR-002]], el cálculo del puntaje de prioridad se encapsula bajo el patrón *Strategy* a través de un servicio de dominio. La arquitectura desacopla este algoritmo del la orden de trabajo, permitiendo incorporar a futuro estrategias adaptadas a factores económicos o de inventario sin alterar las entidades del núcleo.

### 2.3 Aislamiento Multi-Fuente y Extensibilidad de Seguridad

El modelo soporta intencionalmente tipos de aislamiento de seguridad más allá de la energía eléctrica o mecánica únicamente. Las intervenciones industriales pueden involucrar riesgos térmicos, químicos o gravitacionales dependiendo del activo y del alcance del trabajo. Por lo tanto, el modelo de permisos necesita valores extensibles y una alternativa controlada (fallback) como OTHER.

### 2.4 Nota de Modelado sobre el Conjunto de Estándares

El conjunto de cápsulas aprobadas proporciona una fuerte orientación para LOTO, competencias y gobernanza de seguridad, pero no incluye una cápsula dedicada a la taxonomía de permisos OSHA. Por esa razón, los vocabularios de permisos y aislamientos a continuación son vocabularios de proyecto normalizados y alineados con las referencias aprobadas en lugar de códigos literales extraídos de un solo estándar. Esto es deliberado y debe preservarse en el diseño del ERD como datos de búsqueda controlados (lookup data).

### 2.5 Nota de Modelado sobre MediaAttachment

MediaAttachment está modelado como un Value Object en la capa de dominio porque su significado de negocio es puramente evidencial. Sin embargo, una implementación relacional aún podría asignarle una llave subrogada técnica si el motor de almacenamiento requiere direccionamiento de filas independiente. Ese detalle de persistencia no cambia la clasificación en el dominio.

### 2.6 Aislamiento de Módulos mediante Esquemas de Base de Datos

Para reflejar la arquitectura de Monolito Modular en la capa de persistencia y evitar la saturación del esquema predeterminado (public), las tablas del sistema se distribuyen en esquemas dedicados correspondientes a los contextos delimitados (*Bounded Contexts*) de DDD:

- tax: Taxonomía y activos conforme a ISO 14224 (functional_locations, equipment_units, subunits, maintainable_items, equipment_classes).
- mtto: Gestión de mantenimiento y confiabilidad (work_requests, work_orders, maintenance_plans, failure_records, backlog_items).
- inv: Control de recursos y suministros (spare_parts, inventory_transactions, material_requirements, warehouses, suppliers).
- vis: Gemelo digital y capas de seguridad operativa (mesh_mappings, spatial_metadata, telemetry_signals, work_permits, isolation_points).
- adm: Seguridad perimetral, IAM y auditoría inmutable (users, roles, role_permissions, auth_tokens, audit_logs).

Esta segregación permite:
1. **Defensa en profundidad:** Asignación granular de privilegios SQL (GRANT/REVOKE) por módulo para prevenir accesos cruzados no autorizados.
2. **Claridad de consultas:** Eliminación de prefijos redundantes en nombres de tablas (ej. mtto.work_orders en lugar de public.mtto_work_orders).
3. **Mantenibilidad y evolución:** Facilita la futura extracción de un módulo hacia su propio microservicio o base de datos independiente si los requisitos de escalabilidad lo demandan.

## 3. Tabla de Mapeo de Estereotipos

| Entidad                | Estereotipo DDD  | Justificación                                                                                                                                                                                                        | Estándar de Referencia                                                |
| ---------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| FunctionalLocation   | Aggregate Root | Posee la jerarquía de ubicación del activo y la definición del límite.                                                                                                                                               | ISO 14224 Capítulos 8.1 y 8.2                                         |
| EquipmentClass       | Aggregate Root | Posee la taxonomía de la clase del activo y la semántica de los límites específicos de la clase.                                                                                                                     | ISO 14224 Anexo A                                                     |
| EquipmentUnit        | Aggregate Root | Posee el registro de inventario y la división de estado de tres vías para un activo físico.                                                                                                                          | ISO 14224 Capítulo 9.1 y Tabla 5                                      |
| Subunit              | Entity         | Depende del ciclo de vida del activo padre y del contexto de la taxonomía.                                                                                                                                           | ISO 14224 Taxonomía Niveles 6–9                                       |
| MaintainableItem     | Entity         | Representa el nivel reparable más bajo utilizado para mantenimiento y análisis de fallas.                                                                                                                            | ISO 14224 Taxonomía Niveles 8–9                                       |
| WorkRequest          | Aggregate Root | Inicia el flujo de admisión de mantenimiento y posee los factores de priorización RIME.                                                                                                                              | ISO 55000 orientación de riesgos y decisiones; ADR 002                |
| MaintenancePlan      | Aggregate Root | Posee un cronograma de mantenimiento planificado y su cadencia.                                                                                                                                                      | ISO 14224 orientación de datos de mantenimiento                       |
| WorkOrder            | Aggregate Root | Posee la ejecución, el historial, los adjuntos y los registros de trabajo descendentes.                                                                                                                              | ISO 14224 datos de eventos; ISO 9000 control de registros             |
| MediaAttachment      | Value Object   | Carga útil (payload) de evidencia pura sin identidad de negocio independiente.                                                                                                                                       | ISO 9000 información documentada y registros                          |
| WorkOrderHistory     | Entity         | Registro de transición del ciclo de vida de solo adición (append-only) para una orden de trabajo.                                                                                                                    | ISO 9000 inmutabilidad de registros                                   |
| FailureRecord        | Entity           | Evento de falla histórico vinculado directamente al ítem mantenible (MaintainableItem) que lo experimenta.                                                                                                         | ISO 14224 lógica de fallas                                            |
| BacklogItem          | Entity         | Registro de priorización derivado vinculado a la admisión de mantenimiento y al contexto del activo.                                                                                                                 | ISO 55000 orientación de clasificación de riesgos                     |
| SparePart            | Aggregate Root | Registro maestro de inventario para una familia de partes con política de stock y datos de costos.                                                                                                                   | ISO 14224 datos de inventario; ISO 55000 orientación de planificación |
| InventoryTransaction | Entity         | Registro de movimiento rastreable vinculado a partes, órdenes de trabajo y almacenes.                                                                                                                                | ISO 14224 datos de transacciones; ISO 9000 trazabilidad               |
| Warehouse            | Aggregate Root | Representa un límite de ubicación de stock con reglas de capacidad.                                                                                                                                                  | ISO 55000 orientación de planificación de recursos                    |
| Supplier             | Aggregate Root | Posee la identidad de adquisiciones, el contexto comercial y la lógica de garantías.                                                                                                                                 | ISO 9000 información documentada                                      |
| MeshMapping          | Entity         | Proyección gráfica del patrón Sidecar que vincula unívocamente la geometría (SVG o malla 3D) con el Nivel 6 (EquipmentUnit). Los niveles 7 y 8 no poseen coordenadas geométricas individuales en el plano general. | ISO 9000 separación de datos vs. información                          |
| TelemetrySignal      | Entity         | Registro de medición cruda con marca de tiempo utilizado para trazabilidad y analítica de seguridad.                                                                                                                 | ISO 9000 seguimiento y medición                                       |
| WorkPermit           | Aggregate Root   | Límite de autorización de seguridad que valida la ejecución de órdenes de trabajo específicas en campo.                                                                                                              | ISO 55000 orientación de competencias y LOTO                          |
| IsolationPoint       | Entity           | Punto de bloqueo permanente perteneciente a un equipo (EquipmentUnit), requerido aislar en órdenes de trabajo.                                                                                                     | ISO 55000 orientación LOTO; ISO 14224 gobernanza                      |
| VisualLayer          | Entity         | Registro de presentación asociado con una orden de trabajo y estado visual.                                                                                                                                          | ISO 9000 comportamiento de registros                                  |
| SpatialMetadata      | Value Object   | Descriptor inmutable de ubicación y geometría para un artefacto visual.                                                                                                                                              | ISO 9000 separación de datos vs. información                          |
| User                 | Aggregate Root | Raíz del ciclo de vida de cuenta, contraseña, bloqueo (lockout) y token.                                                                                                                                             | ISO 55000 gobernanza de auditorías; ISO 9000 control de auditorías    |
| WorkOrderIsolation   | Entity         | Representa el estado y registro temporal del bloqueo de seguridad de un punto de aislamiento para una OT.                                                                                                            | ISO 55000 orientación LOTO; ISO 14224                                 |
| Role                 | Aggregate Root | Raíz de la semántica de autorización y agrupación de permisos.                                                                                                                                                       | ISO 55000 orientación de competencias y roles                         |
| Permission           | Value Object   | Regla de autorización atómica sin ciclo de vida independiente.                                                                                                                                                       | ISO 9000 flujo de trabajo controlado                                  |
| AuthToken            | Entity         | Tiene ciclo de vida de emisión, uso y caducidad, y debe permanecer rastreable hasta su propietario.                                                                                                                  | ISO 9000 trazabilidad                                                 |
| WorkOrderAssignment  | Entity         | Relación auditable entre un usuario/rol y una orden de trabajo.                                                                                                                                                      | ISO 55000 control de competencias                                     |
| AuditLog             | Entity         | Registro de auditoría de solo adición que contiene el estado antes y después (before/after).                                                                                                                         | ISO 9000 evidencia de auditoría e inmutabilidad de registros          |
| MaterialRequirement  | Entity           | Representa la planificación futura y reserva de consumo de un repuesto para una orden de trabajo específica.                                                                                                         | ISO 55000 planificación de recursos                                   |

## 4. Vocabulario Controlado

### Esquema: TAX

#### 4.1 EquipmentUnit.healthStatus

| Valor                 | Significado                                               | Norma / Concepto              |
| --------------------- | --------------------------------------------------------- | ----------------------------- |
| UNDETERMINED        | Estado de salud desconocido.                              | ISO 13374-4 Health Assessment |
| GOOD                | Todos los indicadores dentro de límites normales.         | ISO 13374-4 Health Assessment |
| FAIR                | Algunas anomalías leves detectadas, sin riesgo inmediato. | ISO 13374-4 Health Assessment |
| SERIOUS_BUT_STABLE  | Anomalías serias pero sin empeoramiento progresivo.       | ISO 13374-4 Health Assessment |
| SERIOUS             | Anomalías serias en deterioro.                            | ISO 13374-4 Health Assessment |
| CRITICAL_BUT_STABLE | Condición crítica que no empeora a corto plazo.           | ISO 13374-4 Health Assessment |
| CRITICAL            | Falla inminente, intervención inmediata requerida.        | ISO 13374-4 Health Assessment |

#### 4.2 EquipmentUnit.lifecycleStatus

| Valor          | Significado                                                     |
| -------------- | --------------------------------------------------------------- |
| IN_STORAGE     | El activo existe como inventario pero no está instalado.        |
| INSTALLED      | El activo está instalado físicamente en su ubicación funcional. |
| COMMISSIONING  | El activo está siendo puesto en servicio.                       |
| DECOMMISSIONED | El activo ha sido retirado permanentemente del servicio.        |

#### 4.3 EquipmentUnit.maintenanceStatus

| Valor               | Significado                                                               |
| ------------------- | ------------------------------------------------------------------------- |
| OPERATIONAL       | El activo no se encuentra actualmente bajo intervención de mantenimiento. |
| UNDER_MAINTENANCE | El activo está siendo reparado o atendido activamente.                    |
| UNDER_TEST        | El activo está bajo verificación o prueba funcional.                      |

#### 4.4 EquipmentUnit.operationalStatus

| Valor     | Significado                                                       |
| --------- | ----------------------------------------------------------------- |
| UP      | El activo está en funcionamiento o listo en un sentido operativo. |
| DOWN    | El activo no está disponible debido a una falla o interrupción.   |
| STANDBY | El activo está listo pero no está produciendo activamente.        |

#### 4.5 FunctionalLocation.environmentalExposure

| Valor      | Significado                                                                                 | Norma de Referencia       |
| ---------- | ------------------------------------------------------------------------------------------- | ------------------------- |
| SEVERE   | Instalaciones no cerradas o a la intemperie; expuestas a vibración, calor, polvo o salitre. | ISO 14224:2016 Tabla A.70 |
| MODERATE | Instalaciones parcialmente cerradas o moderadamente expuestas; ventilación natural.         | ISO 14224:2016 Tabla A.70 |
| LOW      | Instalaciones cerradas o en interiores (indoor); exposición mínima; ventilación mecánica.   | ISO 14224:2016 Tabla A.70 |
| UNKNOWN  | No se dispone de información sobre la exposición ambiental.                                 | ISO 14224:2016 Tabla A.70 |

#### 4.6 MaintainableItem.status

| Valor          | Significado                                                                               | Norma de Referencia                             |
| -------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------- |
| OPERATIONAL  | Saludable y operando dentro de los parámetros de diseño.                                  | ISO 13374 (Normal)                              |
| DEGRADED     | Falla parcial o advertencia de condición; requiere monitoreo o intervención planificada.  | ISO 14224 (Partial Failure) / ISO 13374 (Alert) |
| FAILED       | Falla funcional completa; el ítem ya no puede realizar su función requerida.              | ISO 14224 (Complete Failure)                    |
| UNDER_REPAIR | El componente está siendo mantenido, reparado o reemplazado activamente.                  | Estado transaccional EAM                        |
| REPLACED     | Fin del ciclo de vida del componente en esa ubicación; conservado para historial de MTBF. | Historial de Confiabilidad                      |

### Esquema: MTTO

#### 4.7 BacklogItem.status

| Valor      | Significado                                                        | Norma / Concepto      |
| ---------- | ------------------------------------------------------------------ | --------------------- |
| PENDING  | En espera de análisis técnico o definición de materiales.          | Cola de planificación |
| READY    | Planificado completamente y listo para ser calendarizado.          | Listo para programar  |
| DEFERRED | Aplazado intencionalmente (falta de presupuesto o parada general). | Suspensión en cola    |

#### 4.8 FailureRecord.detectionMethod

| Valor                     | Significado                                                                             | Norma de Referencia      |
| ------------------------- | --------------------------------------------------------------------------------------- | ------------------------ |
| PERIODIC_MAINTENANCE    | Descubierto durante actividades programadas del plan preventivo.                        | ISO 14224:2016 Tabla B.4 |
| FUNCTIONAL_TESTING      | Descubierto al activar una función y comparar contra estándar.                          | ISO 14224:2016 Tabla B.4 |
| INSPECTION              | Descubierto durante inspección visual planificada o ensayos NDT.                        | ISO 14224:2016 Tabla B.4 |
| PERIODIC_CBM            | Revelado durante rondas de medición programadas (vibración, termografía offline).       | ISO 14224:2016 Tabla B.4 |
| PRESSURE_TESTING        | Observado específicamente durante ensayo de presión.                                    | ISO 14224:2016 Tabla B.4 |
| CONTINUOUS_CBM          | Revelado por alarmas o lecturas de instrumentos en línea (SCADA).                       | ISO 14224:2016 Tabla B.4 |
| PRODUCTION_INTERFERENCE | Descubierto por interrupción o reducción inesperada de producción.                      | ISO 14224:2016 Tabla B.4 |
| CASUAL_OBSERVATION      | Descubierto por los sentidos (ruido, olor, fuga) en rutinas normales.                   | ISO 14224:2016 Tabla B.4 |
| CORRECTIVE_MAINTENANCE  | Observado mientras se reparaba otra falla distinta.                                     | ISO 14224:2016 Tabla B.4 |
| ON_DEMAND               | Descubierto durante un intento real de activación (ej. falla de cierre de válvula ESD). | ISO 14224:2016 Tabla B.4 |
| OTHER                   | Otro método de detección no clasificado.                                                | ISO 14224:2016 Tabla B.4 |

#### 4.9 FailureRecord.operationalCondition

| Valor          | Significado                                                | Norma de Referencia    |
| -------------- | ---------------------------------------------------------- | ---------------------- |
| RUNNING      | En operación normal de proceso al momento del evento.      | ISO 14224:2016 Tabla 6 |
| START_UP     | Ocurrido durante el proceso de puesta en marcha.           | ISO 14224:2016 Tabla 6 |
| RUN_DOWN     | Ocurrido durante el proceso de parada/salida de servicio.  | ISO 14224:2016 Tabla 6 |
| HOT_STANDBY  | En reserva activa (listo para operar de inmediato).        | ISO 14224:2016 Tabla 6 |
| COLD_STANDBY | En reserva pasiva (requiere acciones previas para operar). | ISO 14224:2016 Tabla 6 |
| IDLE         | Disponible pero no requerido por el proceso.               | ISO 14224:2016 Tabla 6 |
| TESTING      | Ocurrido durante la ejecución de una prueba funcional.     | ISO 14224:2016 Tabla 6 |

#### 4.10 FailureRecord.operationalImpact

| Valor                   | Significado                                                     | Norma de Referencia      |
| ----------------------- | --------------------------------------------------------------- | ------------------------ |
| EXTENSIVE_STOP        | Parada extensa catastrófica de la producción o instalación.     | ISO 14224:2016 Tabla C.2 |
| STOP_ABOVE_ACCEPTABLE | Parada de producción por encima del límite aceptable de planta. | ISO 14224:2016 Tabla C.2 |
| STOP_BELOW_ACCEPTABLE | Parada de producción por debajo del límite aceptable.           | ISO 14224:2016 Tabla C.2 |
| STOP_MINOR            | Impacto de producción menor o despreciable.                     | ISO 14224:2016 Tabla C.2 |

#### 4.11 MaintenancePlan.frequencyType

| Valor             | Significado                                                      |
| ----------------- | ---------------------------------------------------------------- |
| CALENDAR_TIME   | El plan es impulsado por el tiempo calendario transcurrido.      |
| OPERATING_HOURS | El plan es impulsado por las horas de funcionamiento acumuladas. |
| CYCLES          | El plan es impulsado por ciclos o arranques.                     |

#### 4.12 MaintenancePlan.maintenanceMethod

| Valor             | Significado                                                         | Norma / Concepto            |
| ----------------- | ------------------------------------------------------------------- | --------------------------- |
| PREVENTIVE      | Mantenimiento preventivo sistemático (basado en tiempo/uso).        | ISO 14224 (Preventative)    |
| PREDICTIVE      | Monitoreo predictivo (análisis de vibraciones, termografía, etc.).  | ISO 14224 (Condition-based) |
| CONDITION_BASED | Acciones directas disparadas por límites de sensores en telemetría. | ISO 13374 / CBM             |

#### 4.13 MaintenancePlan.requiredSpecialty

| Valor                         | Significado                                                              | Referencia / Marco                       |
| ----------------------------- | ------------------------------------------------------------------------ | ---------------------------------------- |
| MECHANICAL                  | Intervenciones mecánicas, ajuste de transmisión, alineación y bombas.    | Vocabulario Interno (Prácticas SMRP)     |
| ELECTRICAL                  | Sistemas de potencia, motores eléctricos, tableros y subestaciones.      | Vocabulario Interno (Prácticas SMRP)     |
| INSTRUMENTATION_AND_CONTROL | Calibración de instrumentos, lazos de control y automatización/PLCs.     | Vocabulario Interno (Prácticas SMRP)     |
| LUBRICATION                 | Rutas de lubricación, cambio de aceites y engrase especializado.         | Vocabulario Interno (ISO 18436-4 / SMRP) |
| CONDITION_MONITORING        | Rutas de monitoreo predictivo (vibraciones, termografía, ultrasonido).   | Vocabulario Interno (ISO 18436-2 / SMRP) |
| ELECTRONICS                 | Tarjetas electrónicas, variadores de frecuencia y componentes digitales. | Vocabulario Interno (Prácticas SMRP)     |
| WELDING_FABRICATION         | Soldadura, pailería, calderería y reparaciones estructurales.            | Vocabulario Interno (Prácticas SMRP)     |
| FACILITIES                  | Infraestructura civil, estructuras, iluminación y servicios generales.   | Vocabulario Interno (Prácticas EAM)      |

#### 4.14 MaintenancePlan.status

| Valor      | Significado                                                     | Norma / Concepto        |
| ---------- | --------------------------------------------------------------- | ----------------------- |
| DRAFT    | Plan en fase de diseño o revisión técnica, inactivo.            | Control documental      |
| ACTIVE   | Activo y disparando órdenes de trabajo según su ciclo.          | Operativo               |
| INACTIVE | Desactivado temporalmente por parada o cambio operativo.        | Suspensión de ciclos    |
| ARCHIVED | Obsoleto o reemplazado; conservado para historial de auditoría. | ISO 55001 Ciclo de Vida |

#### 4.15 MediaAttachment.fileType

| Valor | Significado                                               |
| ----- | --------------------------------------------------------- |
| PDF | Portable Document Format (Formato de Documento Portátil). |
| JPG | Archivo de imagen JPEG.                                   |
| PNG | Archivo de imagen Portable Network Graphics.              |

#### 4.16 WorkOrder.criticality

| Valor       | Significado                                                           | Norma / Concepto  |
| ----------- | --------------------------------------------------------------------- | ----------------- |
| EMERGENCY | Detención total de planta, riesgo de seguridad o ambiental inminente. | Criticidad Máxima |
| URGENT    | Falla con impacto operativo inmediato; reparar en menos de 24-48h.    | Prioridad Alta    |
| NORMAL    | Planificable dentro de los ciclos y ventanas semanales.               | Prioridad Media   |
| LOW       | Tareas estéticas o menores de conveniencia operativa.                 | Prioridad Baja    |

#### 4.17 WorkOrder.currentStatus

| Valor           | Significado                                                    | Norma / Concepto                  |
| --------------- | -------------------------------------------------------------- | --------------------------------- |
| PLANNING      | Definición de repuestos, permisos LOTO y recursos.             | FSM - Planificación               |
| WAITING_PARTS | Espera activa de repuestos en almacén/compras.                 | FSM - Cuello de botella logístico |
| SCHEDULED     | Asignado con técnico y fecha de ejecución programada.          | FSM - Programación                |
| IN_PROGRESS   | El técnico está ejecutando la labor (clock-in activo).         | FSM - Ejecución ("Wrench Time")   |
| COMPLETE      | Trabajo técnico finalizado, en espera de revisión.             | FSM - Pre-cierre técnico          |
| CLOSED        | Cerrada administrativamente e ingresados los códigos de falla. | FSM - QA / Auditoría ISO 14224    |

**Restricciones de Transición FSM (Seguridad Industrial & LOTO):**

- Para transicionar de cualquier estado previo (PLANNING, SCHEDULED, WAITING_PARTS) a **IN_PROGRESS**, el sistema debe verificar programáticamente las siguientes precondiciones:
  1.  **Permiso de Trabajo (WorkPermit):** Debe existir un permiso de trabajo asociado y su estado (status) debe ser estrictamente APPROVED.
  2.  **Bloqueo y Etiquetado (LOTO):** Todos los puntos de aislamiento declarados para la orden de trabajo en la tabla intermedia work_order_isolations deben tener su estado de bloqueo verificado (is_isolated = TRUE e isolated_at no nulo).

#### 4.18 WorkOrder.maintenanceMethod

| Valor         | Significado                                                | Norma / Concepto                |
| ------------- | ---------------------------------------------------------- | ------------------------------- |
| CORRECTIVE  | Mantenimiento correctivo reactivo (reparación tras falla). | ISO 14224 (Corrective)          |
| PREVENTIVE  | Preventivo sistemático programado (derivado de plan).      | ISO 14224 (Preventative)        |
| PREDICTIVE  | Monitoreo o inspección predictiva programada.              | ISO 14224 (Condition-based)     |
| IMPROVEMENT | Modificación, rediseño o mejora técnica (CAPEX/OPEX).      | Gestión de Cambios / Ingeniería |

#### 4.19 WorkRequest.status

| Valor      | Significado                                            | Norma / Concepto                 |
| ---------- | ------------------------------------------------------ | -------------------------------- |
| NEW      | Solicitud recién creada y pendiente de evaluación.     | Admisión básica de CMMS          |
| APPROVED | Aprobada y promovida a Orden de Trabajo (WorkOrder). | Transición a planificación       |
| REJECTED | Rechazada por ser inválida, duplicada o falsa alarma.  | Trazabilidad de falsos positivos |

#### 4.20 WorkRequest.workClassCode (Work Class RIME)

| Código (Peso) | Clase de Trabajo                           | Ejemplo Industrial                                                 |
| ------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| 10            | Emergencia de Seguridad o Ambiental        | Fuga de hidrocarburos, falla de aislamiento de seguridad crítica.  |
| 9             | Parada de Producción (Downtime Directo)    | Falla funcional catastrófica en un activo crítico (Bomba Nivel 6). |
| 8             | Trabajo de Alta Prioridad de Proceso       | Degradación de rendimiento con riesgo inminente de detención.      |
| 7             | Mantenimiento Preventivo (PM) Regulado     | Calibraciones de seguridad instrumentada exigidas por ley.         |
| 6             | Mantenimiento Preventivo Sistemático       | Planes cíclicos calendario o por telemetría.                       |
| 5             | Mantenimiento Predictivo (Análisis / Ruta) | Inspección de vibraciones, termografía planificada.                |
| 4             | Trabajo Correctivo No Crítico              | Reparación de fallas con redundancia activa en el sistema.         |
| 3             | Modificaciones de Ingeniería (Mejoras)     | Proyectos de optimización CAPEX (No urgentes).                     |
| 2             | Trabajos Estéticos / Orden y Aseo          | Pintura de estructuras, barandas, limpieza general.                |
| 1             | Trabajo por Conveniencia Operativa         | Ajustes menores de confort o soporte administrativo.               |

### Esquema: INV

#### 4.21 InventoryTransaction.transactionType

| Valor        | Significado                                                 | Norma / Concepto           |
| ------------ | ----------------------------------------------------------- | -------------------------- |
| RECEIPT    | Entrada de inventario (compra, devolución, transferencia).  | Ingesta de Stock           |
| ISSUE      | Salida de inventario (consumo en Orden de Trabajo).         | Carga a Costos de OT       |
| ADJUSTMENT | Ajuste manual/automático por discrepancia en conteo físico. | Conciliación de Inventario |

#### 4.22 SparePart.status

| Valor       | Significado                                                               | Norma / Concepto        |
| ----------- | ------------------------------------------------------------------------- | ----------------------- |
| ACTIVE    | Activo y disponible para consumo y compras.                               | Gestión de Stock        |
| OBSOLETE  | Obsoleto, no se permite nueva compra (se mantiene para historial).        | ISO 55001 Ciclo de Vida |
| SUSPENDED | Temporalmente bloqueado por control de calidad o problemas del proveedor. | Control de Calidad      |

#### 4.23 SparePart.stockPolicy

| Valor           | Significado                                                                 |
| --------------- | --------------------------------------------------------------------------- |
| REORDER_POINT | Reabastecer cuando el inventario alcance un umbral de activación (trigger). |
| MIN_MAX       | Mantener el stock entre niveles mínimo y máximo.                            |
| JUST_IN_TIME  | Reabastecer solo cuando se espere demanda.                                  |

### Esquema: VIS

#### 4.24 IsolationPoint.isolationType

| Valor           | Significado                                                 | Norma / Concepto       |
| --------------- | ----------------------------------------------------------- | ---------------------- |
| ELECTRICAL    | Apertura de disyuntores, breakers o desconexión física.     | LOTO Eléctrico (OSHA)  |
| MECHANICAL    | Bloqueos mecánicos, pasadores o trabas físicas.             | LOTO Mecánico          |
| PNEUMATIC     | Purga y bloqueo de líneas de aire o gases comprimidos.      | LOTO Neumático         |
| HYDRAULIC     | Cierre de válvulas de fluido y purga de acumuladores.       | LOTO Hidráulico        |
| CHEMICAL      | Cierre de doble válvula y purga (Double Block and Bleed).   | LOTO Químico / Proceso |
| THERMAL       | Aislamiento térmico de superficies calientes o criogénicas. | LOTO Térmico           |
| GRAVITATIONAL | Bloques físicos para prevenir caída de masas suspendidas.   | LOTO de Gravedad       |

#### 4.25 MeshMapping.mappingStatus

| Valor        | Significado                                                                 | Norma / Concepto        |
| ------------ | --------------------------------------------------------------------------- | ----------------------- |
| MAPPED     | El activo está correctamente vinculado a su representación 3D en el gemelo. | Vinculación Digital     |
| UNMAPPED   | Falta cargar o posicionar la malla 3D del activo.                           | Gemelo Incompleto       |
| SYNC_ERROR | Error de consistencia o carga entre el motor gráfico y la DB.               | Error de Sincronización |

#### 4.26 TelemetrySignal.signalType

| Valor         | Significado                           | Norma / Concepto        |
| ------------- | ------------------------------------- | ----------------------- |
| TEMPERATURE | Medición térmica.                     | Sensor de Temperatura   |
| PRESSURE    | Medición de presión de fluidos/gases. | Sensor de Presión       |
| VIBRATION   | Medición de oscilaciones mecánicas.   | Análisis de Vibraciones |
| FLOW_RATE   | Medición de caudal o flujo.           | Caudalímetro            |
| VOLTAGE     | Medición de tensión eléctrica.        | Sensor de Tensión       |
| RPM         | Medición de velocidad angular.        | Tacómetro               |

#### 4.27 VisualLayer.status

| Valor     | Significado                                             | Norma / Concepto   |
| --------- | ------------------------------------------------------- | ------------------ |
| VISIBLE | Capa visualizada activamente en el visor 3D.            | Estado Renderizado |
| HIDDEN  | Capa oculta temporalmente.                              | Estado Renderizado |
| GHOSTED | Capa visible con transparencia para revelar interiores. | Estado Renderizado |

#### 4.28 WorkPermit.permitType

| Valor            | Significado                                                          | Norma / Concepto                |
| ---------------- | -------------------------------------------------------------------- | ------------------------------- |
| HOT_WORK       | Trabajo con fuentes de ignición o llama abierta (requiere extintor). | Seguridad Industrial (OSHA)     |
| COLD_WORK      | Trabajo estándar sin peligro de chispa (mecánico, limpieza).         | Seguridad Industrial (OSHA)     |
| CONFINED_SPACE | Entrada a tanques, ductos o áreas con ventilación limitada.          | Espacio Confinado (Alto Riesgo) |
| ELECTRICAL     | Intervención en líneas de alta o media tensión (requiere LOTO).      | Riesgo Eléctrico                |
| WORK_AT_HEIGHT | Trabajo a más de 1.5m de altura con riesgo de caída.                 | Alturas (OSHA / Res. 4272)      |
| EXCAVATION     | Excavaciones, zanjas o movimientos de tierra profundos.              | Excavación (OSHA)               |
| CHEMICAL       | Manejo o exposición a químicos peligrosos o gases nocivos.           | Riesgo Químico                  |

#### 4.29 WorkPermit.status

| Valor      | Significado                                                          | Norma / Concepto             |
| ---------- | -------------------------------------------------------------------- | ---------------------------- |
| DRAFT    | Permiso preparado por el ejecutor pero aún no radicado.              | Ciclo de Autorización        |
| PENDING  | Radicado y en proceso de evaluación y firma por el supervisor.       | Ciclo de Autorización        |
| APPROVED | Autorizado formalmente (habilita la orden de trabajo).               | Permiso Activo / FSM Trigger |
| EXPIRED  | Vencido automáticamente (se superó la ventana horaria de vigencia).  | Control de Riesgos           |
| REVOKED  | Cancelado inmediatamente por condiciones inseguras en campo.         | Intervención de Emergencia   |
| CLOSED   | Finalizado formalmente tras concluir la intervención y retirar LOTO. | Cierre de Operación          |

### Esquema: ADM

#### 4.30 AuditLog.actionType

| Valor    | Significado                                                | Norma / Concepto   |
| -------- | ---------------------------------------------------------- | ------------------ |
| CREATE | Registro inicial de un nuevo objeto en el sistema.         | Auditoría ISO 9001 |
| UPDATE | Modificación de campos existentes (rastrea estado previo). | Auditoría ISO 9001 |
| DELETE | Eliminación lógica o física de una entidad crítica.        | Auditoría ISO 9001 |

#### 4.31 RolePermission.module

| Valor         | Significado                                          | Norma / Concepto         |
| ------------- | ---------------------------------------------------- | ------------------------ |
| ASSETS      | Gestión de taxonomía, equipos y planes.              | Dominio de Activos       |
| MAINTENANCE | Gestión de solicitudes, backlog e historial.         | Dominio de Mantenimiento |
| INVENTORY   | Gestión de repuestos, almacenes y movimientos.       | Dominio de Inventario    |
| SAFETY      | Gestión de telemetría, permisos LOTO y aislamientos. | Dominio de Seguridad     |
| SYSTEM      | Gobernanza, usuarios, roles y logs de auditoría.     | Dominio IAM              |

#### 4.32 User.status

| Valor      | Significado                                                           | Norma / Concepto           |
| ---------- | --------------------------------------------------------------------- | -------------------------- |
| ACTIVE   | Cuenta activa y autorizada para interactuar con la plataforma.        | Ciclo de Vida de Cuenta    |
| INACTIVE | Cuenta desactivada temporal o permanentemente (historial preservado). | Ciclo de Vida de Cuenta    |
| LOCKED   | Bloqueada automáticamente tras exceder intentos fallidos de login.    | Mitigación de Fuerza Bruta |

#### 4.33 WorkOrderAssignment.roleInWork

| Valor        | Significado                                                   | Norma / Concepto            |
| ------------ | ------------------------------------------------------------- | --------------------------- |
| TECHNICIAN | Técnico ejecutor que realiza la labor y registra wrench time. | Ejecución Técnica           |
| SUPERVISOR | Supervisor que firma el cierre técnico y aprueba LOTO.        | Responsable de Línea        |
| PLANNER    | Planificador que diseña la orden, asigna repuestos y tiempos. | Ingeniería de Mantenimiento |

## 5. Mapeo Físico y Diccionario de Datos

Para detalles sobre el mapeo físico y el esquema relacional consulte [[DT-ERD-DOC-001]]. 

## 6. Notas Finales

- El modelo de dominio debe seguir siendo la fuente de verdad del negocio hasta que se genere el ERD físico.
- Los vocabularios controlados que son estables y de baja cardinalidad pueden hacerse cumplir mediante restricciones CHECK.
- Los vocabularios que probablemente cambiarán o crecerán deben trasladarse a tablas de búsqueda (lookup tables).
- Los registros de fallas y auditorías deben permanecer de solo adición (append-only) y rastreables.
- El vocabulario relacionado con la seguridad para permisos y puntos de aislamiento debe tratarse como datos de cumplimiento controlados, no como texto libre.
