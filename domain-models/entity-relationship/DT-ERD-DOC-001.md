---
code: DT-ERD-DOC-001
version: 1.0
date: 2026-09-14
status: Vigente
author: Juan David Julio Serrano
standard:
  - ISO 9001:2015
  - ISO 14224:2016
  - PostgreSQL 18.x Documentation
linked_to:
  - DT-ERD-LOG-001
  - DT-DM-DOC-001
  - DT-ARQ-DB-DOC-001
---

# Diccionario de Datos Físico y Relacional

## 1. Alcance y Propósito

Este documento actúa como el Diccionario de Datos oficial y especificación de mapeo relacional físico para PostgreSQL 18, complementando el diagrama Entidad-Relación (DT-ERD-LOG-001). Define de manera estricta los esquemas, nombres de tablas, columnas físicas y tipos de datos nativos.

## 2. Convenciones y Estructura de Esquemas

Todas las tablas y columnas siguen el estándar de nombrado snake_case. La base de datos está organizada en 5 esquemas impulsados por el diseño (DDD) para aislar contextos:

- tax: Taxonomía y activos conforme a ISO 14224.
- mtto: Gestión de mantenimiento y confiabilidad.
- inv: Control de recursos y suministros.
- vis: Gemelo digital y capas de seguridad operativa.
- adm: Seguridad perimetral, IAM y auditoría inmutable.

## 3. Diccionario de Datos Físico por Esquema

### 3.1 Esquema tax

| Entidad | Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- | --- |
| FunctionalLocation | tag_number | VARCHAR(50) | NOT NULL | UNIQUE | Identidad del tag de la ISO 14224 y trazabilidad de la ubicación. |
| FunctionalLocation | name | VARCHAR(150) | NOT NULL |  | Nombre de la ubicación legible por humanos. |
| FunctionalLocation | description | VARCHAR(255) | NULL |  | Texto explicativo opcional. |
| FunctionalLocation | criticality | VARCHAR(30) | NOT NULL | CHECK o lookup | Vocabulario de prioridad controlado. |
| FunctionalLocation | geographic_location | VARCHAR(150) | NULL |  | Contexto físico de la ubicación. |
| FunctionalLocation | environmental_exposure | VARCHAR(150) | NULL | CHECK o lookup | Condiciones ambientales para cálculos de confiabilidad (ISO 14224). |
| FunctionalLocation | hierarchy_level | SMALLINT | NOT NULL | CHECK (1..5) | Niveles 1 al 5 de la taxonomía ISO 14224 (las Ubicaciones Funcionales gobiernan la estructura espacial de planta hasta el proceso, mientras que L6 a L8 corresponden a equipos y componentes físicos). |
| EquipmentClass | class_name | VARCHAR(120) | NOT NULL | UNIQUE | Datos maestros a nivel de clase. |
| EquipmentClass | description | VARCHAR(255) | NULL |  | Descripción de la clase. |
| EquipmentClass | manufacturer_standard | VARCHAR(120) | NULL |  | Referencia de estandarización. |
| EquipmentUnit | serial_number | VARCHAR(100) | NOT NULL | UNIQUE | Integridad de la identificación del activo. |
| EquipmentUnit | manufacturer | VARCHAR(120) | NOT NULL |  | Procedencia del activo. |
| EquipmentUnit | model | VARCHAR(120) | NOT NULL |  | Identificación del tipo de activo. |
| EquipmentUnit | purchase_date | DATE | NOT NULL |  | Cronología de adquisiciones. |
| EquipmentUnit | rejection_reason | VARCHAR(255) | NULL |  | Solo está presente cuando se rechaza la adquisición. |
| EquipmentUnit | boundary_start | VARCHAR(150) | NOT NULL |  | Punto de inicio de la definición del límite. |
| EquipmentUnit | boundary_end | VARCHAR(150) | NOT NULL |  | Punto final de la definición del límite. |
| EquipmentUnit | acquisition_date | DATE | NOT NULL |  | Trazabilidad de la adquisición del activo. |
| EquipmentUnit | installation_date | DATE | NULL |  | La instalación puede estar pendiente. |
| EquipmentUnit | operation_start_date | DATE | NULL |  | El inicio operativo puede estar pendiente. |
| EquipmentUnit | operating_hours | BIGINT | NOT NULL | DEFAULT 0 | Seguimiento de confiabilidad y uso. |
| EquipmentUnit | surveillance_hours | BIGINT | NOT NULL | DEFAULT 0 | Tiempo de vigilancia/standby para cálculo preciso de fallas (ISO 14224). |
| EquipmentUnit | disposal_date | DATE | NULL |  | Registro de fin de vida para trazabilidad de pasivos (ISO 55000). |
| EquipmentUnit | disposal_reason | VARCHAR(255) | NULL |  | Razón del retiro o desmantelamiento del activo. |
| EquipmentUnit | operational_status | VARCHAR(20) | NOT NULL | CHECK o lookup | Vocabulario de estado operativo controlado. |
| EquipmentUnit | lifecycle_status | VARCHAR(20) | NOT NULL | CHECK o lookup | Vocabulario de ciclo de vida controlado. |
| EquipmentUnit | maintenance_status | VARCHAR(30) | NOT NULL | CHECK o lookup | Vocabulario de estado de mantenimiento controlado. |
| EquipmentUnit | health_status | VARCHAR(30) | NULL | CHECK o lookup | Vocabulario de estado de salud general (ISO 13374-4). |
| EquipmentUnit | is_sce | BOOLEAN | NOT NULL | DEFAULT FALSE | Indicador de Equipo Crítico de Seguridad (Safety Critical Element). |
| Subunit | subunit_type | VARCHAR(80) | NOT NULL |  | Taxonomía del subcomponente. |
| Subunit | name | VARCHAR(120) | NOT NULL |  | Etiqueta del subcomponente. |
| MaintainableItem | component_name | VARCHAR(120) | NOT NULL |  | Identidad del ítem mantenible. |
| MaintainableItem | subunit_type | VARCHAR(80) | NOT NULL |  | Clasificación taxonómica. |
| MaintainableItem | spare_part_type | VARCHAR(80) | NULL |  | Correspondencia opcional de partes de repuesto. |
| MaintainableItem | design_attributes | JSONB | NULL |  | Propiedades estáticas de diseño estructuradas (ISO 14224 Anexo A). |
| MaintainableItem | status | VARCHAR(30) | NOT NULL | CHECK o lookup | Estado del ciclo de vida del ítem. |

### 3.2 Esquema mtto

| Entidad | Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- | --- |
| WorkRequest | description | VARCHAR(255) | NOT NULL |  | Narrativa de la solicitud. |
| WorkRequest | priority | VARCHAR(20) | NOT NULL | CHECK o lookup | Etiqueta de prioridad de la solicitud. |
| WorkRequest | request_date | TIMESTAMPTZ | NOT NULL |  | Línea de tiempo para auditoría. |
| WorkRequest | request_source | VARCHAR(80) | NOT NULL |  | Origen de la solicitud. |
| WorkRequest | status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado del ciclo de vida de la solicitud. |
| WorkRequest | work_class | INT | NOT NULL | CHECK (1..10) o lookup | Peso numérico de la clase de trabajo seleccionada para el RIME. |
| MaintenancePlan | maintenance_method | VARCHAR(80) | NOT NULL | CHECK o lookup | Estrategia de mantenimiento (PM, PdM, CBM). |
| MaintenancePlan | frequency | VARCHAR(80) | NOT NULL |  | Descripción de la frecuencia legible por humanos. |
| MaintenancePlan | frequency_type | VARCHAR(20) | NOT NULL | CHECK o lookup | Cadencia controlada del plan. |
| MaintenancePlan | next_work_order_date | DATE | NULL |  | Fecha de ejecución programada (Calculada). |
| MaintenancePlan | interval_value | DECIMAL(12,2) | NULL |  | Valor numérico del intervalo para telemetría (ej. 500 horas). |
| MaintenancePlan | next_trigger_limit | DECIMAL(12,2) | NULL |  | Límite acumulado calculado para el próximo disparo. |
| MaintenancePlan | estimated_labor_hours | DECIMAL(10,2) | NOT NULL |  | Horas-Hombre estimadas (Wrench Time) para planificación. |
| MaintenancePlan | required_specialty | VARCHAR(80) | NOT NULL | CHECK o lookup | Especialidad técnica requerida (ej. Mecánica, Eléctrica). |
| MaintenancePlan | technical_description | VARCHAR(255) | NOT NULL |  | Descripción técnica del alcance de las tareas. |
| MaintenancePlan | status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado del ciclo de vida del plan (documento). |
| WorkOrder | current_status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado del ciclo de vida de ejecución (FSM). |
| WorkOrder | maintenance_method | VARCHAR(80) | NOT NULL | CHECK o lookup | Método de mantenimiento (Correctivo, Preventivo, etc.). |
| WorkOrder | creation_date | TIMESTAMPTZ | NOT NULL |  | Marca de tiempo (timestamp) de creación de la orden. |
| WorkOrder | scheduled_date | TIMESTAMPTZ | NULL |  | Inicio planeado. |
| WorkOrder | actual_start | TIMESTAMPTZ | NULL |  | Inicio real de la ejecución. |
| WorkOrder | actual_finish | TIMESTAMPTZ | NULL |  | Finalización real de la ejecución. |
| WorkOrder | actual_labor_hours | DECIMAL(10,2) | NULL |  | Duración laboral real (Calculada). |
| WorkOrder | criticality | VARCHAR(20) | NOT NULL | CHECK o lookup | Etiqueta de criticidad / prioridad de la OT. |
| MediaAttachment | file_url | VARCHAR(255) | NOT NULL |  | Ubicación de la evidencia. |
| MediaAttachment | file_type | VARCHAR(10) | NOT NULL | CHECK o lookup | Formato de archivo adjunto controlado. |
| MediaAttachment | uploaded_at | TIMESTAMPTZ | NOT NULL |  | Tiempo de subida/ingesta de la evidencia. |
| WorkOrderHistory | old_status | VARCHAR(20) | NULL |  | Estado anterior del ciclo de vida (NULL si es primer estado). |
| WorkOrderHistory | new_status | VARCHAR(20) | NOT NULL |  | Nuevo estado del ciclo de vida. |
| WorkOrderHistory | timestamp | TIMESTAMPTZ | NOT NULL |  | Tiempo de transición. |
| WorkOrderHistory | duration_seconds | BIGINT | NULL |  | Tiempo empleado en el estado (Calculado al transicionar). |
| FailureRecord | failure_id | UUID | NOT NULL | PK | Identidad del evento de falla. |
| FailureRecord | failure_mode | VARCHAR(120) | NOT NULL | CHECK o lookup | Codificación de fallas de la ISO 14224. |
| FailureRecord | failure_mechanism | VARCHAR(120) | NOT NULL | CHECK o lookup | Codificación de fallas de la ISO 14224. |
| FailureRecord | failure_cause | VARCHAR(120) | NOT NULL | CHECK o lookup | Codificación de fallas de la ISO 14224. |
| FailureRecord | detection_method | VARCHAR(120) | NOT NULL | CHECK o lookup | Método de detección de la falla (ISO 14224). |
| FailureRecord | operational_condition | VARCHAR(120) | NOT NULL | CHECK o lookup | Condición operativa al momento de la falla (ISO 14224). |
| FailureRecord | operational_impact | VARCHAR(120) | NOT NULL | CHECK o lookup | Impacto operacional de la falla (ISO 14224). |
| FailureRecord | downtime | DECIMAL(10,2) | NOT NULL |  | Métrica de análisis de confiabilidad (Calculada). |
| FailureRecord | status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado del registro de fallas. |
| BacklogItem | priority_score | INT | NOT NULL |  | Puntaje del backlog derivado de RIME (Calculado). |
| BacklogItem | status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado del ciclo de vida del backlog (priorización). |

### 3.3 Esquema inv

| Entidad | Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- | --- |
| SparePart | sku | VARCHAR(80) | NOT NULL | UNIQUE | Identidad de la parte. |
| SparePart | description | VARCHAR(255) | NOT NULL |  | Descripción de la parte legible por humanos. |
| SparePart | manufacturer | VARCHAR(120) | NOT NULL |  | Identidad del proveedor/fabricante. |
| SparePart | commodity_code | VARCHAR(80) | NULL |  | Código de clasificación. |
| SparePart | reorder_point | DECIMAL(12,4) | NOT NULL |  | Umbral mínimo de activación de compra. |
| SparePart | unit_of_measure | VARCHAR(20) | NOT NULL |  | Unidad de medida estándar (UoM). |
| SparePart | stock_policy | VARCHAR(20) | NOT NULL | CHECK o lookup | Política de reabastecimiento (Min/Max, Reorder Point, JIT). |
| SparePart | is_rebuildable | BOOLEAN | NOT NULL | DEFAULT false | Indica si la parte se desecha o se envía a taller para reparación. |
| SparePart | quantity_on_hand | DECIMAL(12,4) | NOT NULL |  | Cantidad actualmente en inventario físico. |
| SparePart | reserved_quantity | DECIMAL(12,4) | NOT NULL | DEFAULT 0 | Stock comprometido para órdenes planificadas. |
| SparePart | max_capacity | DECIMAL(12,4) | NULL |  | Límite físico del almacén para la parte. |
| SparePart | unit_cost | DECIMAL(12,2) | NOT NULL |  | Costo unitario estándar de adquisición. |
| SparePart | status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado de disponibilidad del repuesto. |
| InventoryTransaction | quantity | DECIMAL(12,4) | NOT NULL |  | Cantidad transada (positiva para entradas, negativa para salidas). |
| InventoryTransaction | transaction_type | VARCHAR(20) | NOT NULL | CHECK o lookup | Tipo de movimiento (RECEIPT, ISSUE, ADJUSTMENT). |
| InventoryTransaction | timestamp | TIMESTAMPTZ | NOT NULL |  | Registro temporal preciso del movimiento. |
| InventoryTransaction | reason | VARCHAR(255) | NOT NULL |  | Razón del movimiento o referencia a documentos externos. |
| InventoryTransaction | total_cost | DECIMAL(12,2) | NOT NULL |  | Costo total de la transacción (Cantidad \* Costo). |
| InventoryTransaction | aisle_shelf_location | VARCHAR(150) | NULL |  | Ubicación física específica de la transacción (pasillo/estante). |
| InventoryTransaction | serial_number | VARCHAR(100) | NULL |  | Número de serie o Tag del equipo rotativo (Asset Swap). |
| Warehouse | name | VARCHAR(80) | NOT NULL | UNIQUE | Identidad del almacén. |
| Warehouse | location | VARCHAR(255) | NOT NULL |  | Dirección o ubicación física del almacén. |
| Warehouse | capacity | DECIMAL(12,4) | NOT NULL |  | Capacidad máxima volumétrica o de carga del almacén. |
| Supplier | name | VARCHAR(120) | NOT NULL | UNIQUE | Identidad comercial del proveedor. |
| Supplier | contact_info | VARCHAR(255) | NOT NULL |  | Teléfono, correo o dirección de contacto. |
| Supplier | warranty_terms | VARCHAR(255) | NOT NULL |  | Términos estándar de garantía comercial. |
| MaterialRequirement | planned_quantity | DECIMAL(12,4) | NOT NULL |  | Repuestos planificados antes de la ejecución de la OT. |
| MaterialRequirement | actual_quantity | DECIMAL(12,4) | NULL |  | Repuestos realmente consumidos durante la ejecución de la OT. |
| MaterialRequirement | is_reserved | BOOLEAN | NOT NULL | DEFAULT false | Bandera que indica si el stock ya fue apartado en almacén. |

### 3.4 Esquema vis

| Entidad | Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- | --- |
| MeshMapping | mesh_uuid | VARCHAR(80) | NOT NULL | UNIQUE | Identidad o ruta del modelo 3D del activo. |
| MeshMapping | mapping_status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado de vinculación del gemelo digital. |
| MeshMapping | last_sync_time | TIMESTAMPTZ | NULL |  | Tiempo de la última sincronización. |
| TelemetrySignal | signal_type | VARCHAR(80) | NOT NULL |  | Etiqueta de la señal del sensor. |
| TelemetrySignal | value | DECIMAL(18,6) | NOT NULL |  | Valor de la medición cruda. |
| TelemetrySignal | unit | VARCHAR(20) | NOT NULL |  | Unidad de medición. |
| TelemetrySignal | threshold | DECIMAL(18,6) | NULL |  | Umbral de alerta. |
| TelemetrySignal | timestamp | TIMESTAMPTZ | NOT NULL |  | Tiempo de medición. |
| TelemetrySignal | is_safety_critical | BOOLEAN | NOT NULL | DEFAULT FALSE | Bandera de clasificación de seguridad. |
| WorkPermit | permit_identifier | VARCHAR(80) | NOT NULL | UNIQUE | Trazabilidad del permiso. |
| WorkPermit | permit_type | VARCHAR(30) | NOT NULL | CHECK o lookup | Vocabulario de permisos. |
| WorkPermit | contractor_name | VARCHAR(150) | NOT NULL |  | Identificación del contratista. |
| WorkPermit | status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado del ciclo de vida del permiso. |
| IsolationPoint | isolation_tag | VARCHAR(80) | NOT NULL | UNIQUE | Identidad del punto de aislamiento. |
| IsolationPoint | isolation_type | VARCHAR(20) | NOT NULL | CHECK o lookup | Vocabulario de aislamiento. |
| IsolationPoint | is_verified | BOOLEAN | NOT NULL | DEFAULT FALSE | Estado de verificación. |
| WorkOrderIsolation | is_isolated | BOOLEAN | NOT NULL | DEFAULT FALSE | Estado de bloqueo verificado para el trabajo específico. |
| WorkOrderIsolation | isolated_at | TIMESTAMPTZ | NULL |  | Marca de tiempo en que se ejecutó el bloqueo. |
| WorkOrderIsolation | padlock_tag_id | VARCHAR(80) | NULL |  | Identificador del candado o etiqueta física (Try-Out). |
| VisualLayer | layer_type | VARCHAR(80) | NOT NULL |  | Tipo de representación visual. |
| VisualLayer | opacity_level | DECIMAL(5,2) | NOT NULL | CHECK (0..1) | Control de renderizado. |
| VisualLayer | status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado de la capa visual. |
| SpatialMetadata | position | JSONB | NOT NULL |  | Coordenada espacial vectorial (ej. x,y,z). |
| SpatialMetadata | rotation | JSONB | NULL |  | Descriptor de orientación (ej. cuaternión). |
| SpatialMetadata | scale | JSONB | NULL |  | Descriptor de escala. |

### 3.5 Esquema adm

| Entidad | Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- | --- |
| User | username | VARCHAR(80) | NOT NULL | UNIQUE | Identidad de la cuenta de usuario. |
| User | full_name | VARCHAR(150) | NOT NULL |  | Nombre completo o institucional del usuario. |
| User | email | VARCHAR(150) | NOT NULL | UNIQUE | Correo electrónico institucional y de contacto. |
| User | status | VARCHAR(20) | NOT NULL | CHECK o lookup | Estado de la cuenta (ACTIVE, INACTIVE, LOCKED). |
| User | password_hash | VARCHAR(255) | NOT NULL |  | Hash de la contraseña de acceso (PBKDF2/BCrypt). |
| User | failed_login_attempts | INT | NOT NULL | DEFAULT 0 | Contador de intentos fallidos de autenticación. |
| User | lockout_until | TIMESTAMPTZ | NULL |  | Fin del periodo de bloqueo temporal. |
| User | mfa_enabled | BOOLEAN | NOT NULL | DEFAULT FALSE | Bandera que indica si la autenticación multifactor está activa. |
| User | totp_secret | VARCHAR(255) | NULL |  | Secreto compartido para autenticación TOTP (Autenticador). |
| User | deactivation_reason | VARCHAR(255) | NULL |  | Justificación administrativa para el borrado lógico (ISO 27001). |
| Role | role_name | VARCHAR(80) | NOT NULL | UNIQUE | Identificador del rol de usuario (ej. Planner, Technician). |
| Role | description | VARCHAR(255) | NULL |  | Descripción del alcance del rol. |
| Role | is_system_role | BOOLEAN | NOT NULL | DEFAULT FALSE | Bandera para roles inmutables del sistema. |
| RolePermission | module | VARCHAR(80) | NOT NULL |  | Módulo del sistema (ej. MTTO, INV, VIS). |
| RolePermission | action | VARCHAR(80) | NOT NULL |  | Acción permitida (ej. READ, CREATE, UPDATE, SIGN_OFF). |
| AuthToken | token_hash | VARCHAR(255) | NOT NULL | UNIQUE | Hash del token de autenticación API / sesión. |
| AuthToken | expires_at | TIMESTAMPTZ | NOT NULL |  | Fecha y hora de expiración del token. |
| AuthToken | is_used | BOOLEAN | NOT NULL | DEFAULT FALSE | Indica si el token ya fue consumido (uso único). |
| AuthToken | ip_address | VARCHAR(45) | NULL |  | Dirección IP desde la que se emitió el token (IPv4/IPv6). |
| AuthToken | user_agent | VARCHAR(255) | NULL |  | Identificador del cliente/navegador para fingerprinting. |
| WorkOrderAssignment | role_in_work | VARCHAR(50) | NOT NULL |  | Rol funcional en la orden de trabajo (TECHNICIAN, SUPERVISOR). |
| WorkOrderAssignment | assigned_at | TIMESTAMPTZ | NOT NULL |  | Registro temporal de la asignación. |
| AuditLog | entity_type | VARCHAR(80) | NOT NULL |  | Nombre de la tabla/entidad auditada. |
| AuditLog | entity_identifier | VARCHAR(80) | NOT NULL |  | Identificador UUID de la fila modificada. |
| AuditLog | action_type | VARCHAR(20) | NOT NULL | CHECK o lookup | Tipo de operación DML (CREATE, UPDATE, DELETE). |
| AuditLog | timestamp | TIMESTAMPTZ | NOT NULL |  | Registro temporal preciso del evento de cambio. |
| AuditLog | previous_state | JSONB | NULL |  | Representación JSON descompuesta binaria antes de la acción. |
| AuditLog | new_state | JSONB | NULL |  | Representación JSON descompuesta binaria después de la acción. |
| AuditLog | integrity_hash | VARCHAR(255) | NOT NULL |  | Hash SHA-256 encadenado para detectar manipulación del log. |

## 4. Matriz de Correspondencia de Tipos de Datos (SQL Estándar vs. PostgreSQL)

Para garantizar la viabilidad física del modelo lógico y su correcta implementación en el motor de base de datos seleccionado (**PostgreSQL**), se ha validado y mapeado formalmente cada tipo de datos físico propuesto:

| Tipo Físico (Estándar SQL) | Tipo Nativo en PostgreSQL             | Equivalente Técnico Alternativo | Impacto Técnico / Justificación en PostgreSQL                                                                                                                                                                                                                                                                                                                                                                  |
| :------------------------- | :------------------------------------ | :------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VARCHAR(N)               | VARCHAR(N) o CHARACTER VARYING(N) | TEXT                          | PostgreSQL maneja cadenas de longitud variable eficientemente. TEXT no tiene penalización de rendimiento y se prefiere cuando no se requiere un límite estricto de longitud de caracteres.                                                                                                                                                                                                                   |
| SMALLINT                 | SMALLINT o INT2                   | Ninguno                         | Entero con signo de 2 bytes (rango -32,768 a 32,767). Óptimo para cardinalidades y niveles taxonómicos (como hierarchyLevel).                                                                                                                                                                                                                                                                                |
| INT                      | INTEGER o INT4                    | Ninguno                         | Entero con signo de 4 bytes (rango -2,147,483,648 a 2,147,483,647). Estándar para contadores simples (como failedLoginAttempts).                                                                                                                                                                                                                                                                             |
| BIGINT                   | BIGINT o INT8                     | Ninguno                         | Entero con signo de 8 bytes. Usado para métricas acumuladas grandes como horas operativas (operatingHours) y duraciones de transición.                                                                                                                                                                                                                                                                       |
| DATE                     | DATE                                | Ninguno                         | Tipo de datos de 4 bytes para almacenar fechas de calendario sin zona horaria (año, mes, día).                                                                                                                                                                                                                                                                                                                 |
| TIMESTAMP                | TIMESTAMP                           | TIMESTAMPTZ                   | TIMESTAMP almacena fecha y hora sin zona horaria. Se recomienda TIMESTAMPTZ (Timestamp con zona horaria) para logs de auditoría, marcas de creación e inicio de órdenes de trabajo para evitar discrepancias por husos horarios.                                                                                                                                                                           |
| DECIMAL(P,S)             | DECIMAL(P,S) o NUMERIC(P,S)       | Ninguno                         | Tipo de precisión exacta con escala de usuario. Esencial para valores monetarios (unitCost), dimensiones de sensores (value, threshold) y porcentajes exactos (opacityLevel).                                                                                                                                                                                                                          |
| UUID                     | UUID                                | Ninguno                         | Tipo de datos nativo de 128 bits. En PostgreSQL 18 se utilizará la función nativa uuidv7() como valor por defecto para llaves primarias. A diferencia de UUIDv4 (aleatorio), UUIDv7 incluye un prefijo temporal de 48 bits ordenado cronológicamente, lo que previene la fragmentación de páginas en los índices B-Tree y maximiza el rendimiento de inserción en series de tiempo y registros de auditoría. |
| BOOLEAN                  | BOOLEAN o BOOL                    | Ninguno                         | Tipo lógico que almacena TRUE o FALSE.                                                                                                                                                                                                                                                                                                                                                                     |
| JSON                     | JSON                                | JSONB                         | JSON almacena el texto literal, lo cual requiere parseo en cada consulta. Se recomienda usar JSONB (JSON Binario Descompuesto) porque almacena el contenido en formato binario, soporta indexación rápida (índices GIN) y es mucho más eficiente para consultas de auditoría (previousState y newState).                                                                                               |

