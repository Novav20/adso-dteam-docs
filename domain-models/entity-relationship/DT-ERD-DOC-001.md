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

#### 3.1.1 equipment_classes

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| class_name | VARCHAR(120) | NOT NULL | UNIQUE | Datos maestros a nivel de clase. |
| description | VARCHAR(255) | NULL |  | Descripción de la clase. |
| manufacturer_standard | VARCHAR(120) | NULL |  | Referencia de estandarización. |

#### 3.1.2 equipment_units

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| serial_number | VARCHAR(100) | NOT NULL | UNIQUE | Integridad de la identificación del activo. |
| manufacturer | VARCHAR(120) | NOT NULL |  | Procedencia del activo. |
| model | VARCHAR(120) | NOT NULL |  | Identificación del tipo de activo. |
| purchase_date | DATE | NOT NULL |  | Cronología de adquisiciones. |
| rejection_reason | VARCHAR(255) | NULL |  | Solo está presente cuando se rechaza la adquisición. |
| boundary_start | VARCHAR(150) | NOT NULL |  | Punto de inicio de la definición del límite. |
| boundary_end | VARCHAR(150) | NOT NULL |  | Punto final de la definición del límite. |
| acquisition_date | DATE | NOT NULL |  | Trazabilidad de la adquisición del activo. |
| installation_date | DATE | NULL |  | La instalación puede estar pendiente. |
| operation_start_date | DATE | NULL |  | El inicio operativo puede estar pendiente. |
| operating_hours | BIGINT | NOT NULL |  | Seguimiento de confiabilidad y uso. |
| surveillance_hours | BIGINT | NOT NULL |  | Tiempo de vigilancia/standby para cálculo preciso de fallas (ISO 14224). |
| disposal_date | DATE | NULL |  | Registro de fin de vida para trazabilidad de pasivos (ISO 55000). |
| disposal_reason | VARCHAR(255) | NULL |  | Razón del retiro o desmantelamiento del activo. |
| operational_status | VARCHAR(20) | NOT NULL | CHECK | Vocabulario de estado operativo controlado. |
| lifecycle_status | VARCHAR(20) | NOT NULL | CHECK | Vocabulario de ciclo de vida controlado. |
| maintenance_status | VARCHAR(30) | NOT NULL | CHECK | Vocabulario de estado de mantenimiento controlado. |
| health_status | VARCHAR(30) | NULL | CHECK | Vocabulario de estado de salud general (ISO 13374-4). |
| is_sce | BOOLEAN | NOT NULL |  | Indicador de Equipo Crítico de Seguridad (Safety Critical Element). |
| functional_location_id | UUID | NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| equipment_class_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| warehouse_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |

#### 3.1.3 functional_locations

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| tag_number | VARCHAR(50) | NOT NULL | UNIQUE | Identidad del tag de la ISO 14224 y trazabilidad de la ubicación. |
| name | VARCHAR(150) | NOT NULL |  | Nombre de la ubicación legible por humanos. |
| description | VARCHAR(255) | NULL |  | Texto explicativo opcional. |
| criticality | VARCHAR(30) | NOT NULL |  | Vocabulario de prioridad controlado. |
| geographic_location | VARCHAR(150) | NULL |  | Contexto físico de la ubicación. |
| environmental_exposure | VARCHAR(150) | NULL | CHECK | Condiciones ambientales para cálculos de confiabilidad (ISO 14224). |
| hierarchy_level | SMALLINT | NOT NULL |  | Niveles 1 al 5 de la taxonomía ISO 14224 (las Ubicaciones Funcionales gobiernan la estructura espacial de planta hasta el proceso, mientras que L6 a L8 corresponden a equipos y componentes físicos). |
| parent_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |

#### 3.1.4 maintainable_items

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| subunit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| component_name | VARCHAR(120) | NOT NULL |  | Identidad del ítem mantenible. |
| subunit_type | VARCHAR(80) | NOT NULL |  | Clasificación taxonómica. |
| spare_part_type | VARCHAR(80) | NULL |  | Correspondencia opcional de partes de repuesto. |
| design_attributes | JSONB | NULL |  | Propiedades estáticas de diseño estructuradas (ISO 14224 Anexo A). |
| status | VARCHAR(30) | NOT NULL | CHECK | Estado del ciclo de vida del ítem. |

#### 3.1.5 subunits

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| subunit_type | VARCHAR(80) | NOT NULL |  | Taxonomía del subcomponente. |
| name | VARCHAR(120) | NOT NULL |  | Etiqueta del subcomponente. |

### 3.2 Esquema mtto

#### 3.2.1 backlog_items

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_request_id | UUID | NOT NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| priority_score | INT | NOT NULL |  | Puntaje del backlog derivado de RIME (Calculado). |
| status | VARCHAR(20) | NOT NULL | CHECK | Estado del ciclo de vida del backlog (priorización). |

#### 3.2.2 failure_records

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identidad del evento de falla. |
| work_order_id | UUID | NOT NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| maintainable_item_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| failure_mode | VARCHAR(120) | NOT NULL |  | Codificación de fallas de la ISO 14224. |
| failure_mechanism | VARCHAR(120) | NOT NULL |  | Codificación de fallas de la ISO 14224. |
| failure_cause | VARCHAR(120) | NOT NULL |  | Codificación de fallas de la ISO 14224. |
| detection_method | VARCHAR(120) | NOT NULL | CHECK | Método de detección de la falla (ISO 14224). |
| operational_condition | VARCHAR(120) | NOT NULL | CHECK | Condición operativa al momento de la falla (ISO 14224). |
| operational_impact | VARCHAR(120) | NOT NULL | CHECK | Impacto operacional de la falla (ISO 14224). |
| downtime | DECIMAL(10,2) | NOT NULL |  | Métrica de análisis de confiabilidad (Calculada). |
| status | VARCHAR(20) | NOT NULL |  | Estado del registro de fallas. |

#### 3.2.3 maintenance_plans

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| maintenance_method | VARCHAR(80) | NOT NULL | CHECK | Estrategia de mantenimiento (PM, PdM, CBM). |
| frequency | VARCHAR(50) | NOT NULL |  | Descripción de la frecuencia legible por humanos. |
| frequency_type | VARCHAR(20) | NOT NULL | CHECK | Cadencia controlada del plan. |
| next_work_order_date | DATE | NULL |  | Fecha de ejecución programada (Calculada). |
| interval_value | DECIMAL(12,2) | NULL |  | Valor numérico del intervalo para telemetría (ej. 500 horas). |
| next_trigger_limit | DECIMAL(12,2) | NULL |  | Límite acumulado calculado para el próximo disparo. |
| estimated_labor_hours | DECIMAL(10,2) | NOT NULL |  | Horas-Hombre estimadas (Wrench Time) para planificación. |
| required_specialty | VARCHAR(80) | NOT NULL | CHECK | Especialidad técnica requerida (ej. Mecánica, Eléctrica). |
| technical_description | VARCHAR(255) | NOT NULL |  | Descripción técnica del alcance de las tareas. |
| status | VARCHAR(20) | NOT NULL | CHECK | Estado del ciclo de vida del plan (documento). |

#### 3.2.4 media_attachments

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| work_order_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| file_url | VARCHAR(255) | NOT NULL |  | Ubicación de la evidencia. |
| file_type | VARCHAR(20) | NOT NULL | CHECK | Formato de archivo adjunto controlado. |
| uploaded_at | TIMESTAMP | NOT NULL |  | Tiempo de subida/ingesta de la evidencia. |

#### 3.2.5 work_order_histories

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| work_order_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| old_status | VARCHAR(20) | NULL |  | Estado anterior del ciclo de vida (NULL si es primer estado). |
| new_status | VARCHAR(20) | NOT NULL |  | Nuevo estado del ciclo de vida. |
| timestamp | TIMESTAMP | NOT NULL |  | Tiempo de transición. |
| duration_seconds | BIGINT | NULL |  | Tiempo empleado en el estado (Calculado al transicionar). |

#### 3.2.6 work_orders

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| maintenance_plan_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_request_id | UUID | NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| work_permit_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| current_status | VARCHAR(20) | NOT NULL | CHECK | Estado del ciclo de vida de ejecución (FSM). |
| maintenance_method | VARCHAR(80) | NOT NULL | CHECK | Método de mantenimiento (Correctivo, Preventivo, etc.). |
| creation_date | TIMESTAMP | NOT NULL |  | Marca de tiempo (timestamp) de creación de la orden. |
| scheduled_date | TIMESTAMP | NULL |  | Inicio planeado. |
| actual_start | TIMESTAMP | NULL |  | Inicio real de la ejecución. |
| actual_finish | TIMESTAMP | NULL |  | Finalización real de la ejecución. |
| actual_labor_hours | DECIMAL(10,2) | NULL |  | Duración laboral real (Calculada). |
| criticality | VARCHAR(20) | NOT NULL | CHECK | Etiqueta de criticidad / prioridad de la OT. |

#### 3.2.7 work_requests

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| description | VARCHAR(255) | NOT NULL |  | Narrativa de la solicitud. |
| priority | VARCHAR(20) | NOT NULL |  | Etiqueta de prioridad de la solicitud. |
| request_date | TIMESTAMP | NOT NULL |  | Línea de tiempo para auditoría. |
| request_source | VARCHAR(80) | NOT NULL |  | Origen de la solicitud. |
| status | VARCHAR(20) | NOT NULL | CHECK | Estado del ciclo de vida de la solicitud. |
| work_class_code | SMALLINT | NOT NULL | CHECK | Peso numérico de la clase de trabajo seleccionada para el RIME. |

### 3.3 Esquema inv

#### 3.3.1 inventory_transactions

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| spare_part_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| warehouse_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_order_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| quantity | DECIMAL(12,4) | NOT NULL |  | Cantidad transada (positiva para entradas, negativa para salidas). |
| transaction_type | VARCHAR(20) | NOT NULL | CHECK | Tipo de movimiento (RECEIPT, ISSUE, ADJUSTMENT). |
| timestamp | TIMESTAMP | NOT NULL |  | Registro temporal preciso del movimiento. |
| reason | VARCHAR(255) | NOT NULL |  | Razón del movimiento o referencia a documentos externos. |
| total_cost | DECIMAL(12,2) | NOT NULL |  | Costo total de la transacción (Cantidad \* Costo). |
| aisle_shelf_location | VARCHAR(150) | NULL |  | Ubicación física específica de la transacción (pasillo/estante). |
| serial_number | VARCHAR(100) | NULL |  | Número de serie o Tag del equipo rotativo (Asset Swap). |

#### 3.3.2 maintainable_item_spare_parts

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| maintainable_item_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| spare_part_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |

#### 3.3.3 material_requirements

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| work_order_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| spare_part_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| planned_quantity | DECIMAL(12,4) | NOT NULL |  | Repuestos planificados antes de la ejecución de la OT. |
| actual_quantity | DECIMAL(12,4) | NULL |  | Repuestos realmente consumidos durante la ejecución de la OT. |
| is_reserved | BOOLEAN | NOT NULL |  | Bandera que indica si el stock ya fue apartado en almacén. |

#### 3.3.4 spare_parts

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| sku | VARCHAR(80) | NOT NULL | UNIQUE | Identidad de la parte. |
| description | VARCHAR(255) | NOT NULL |  | Descripción de la parte legible por humanos. |
| manufacturer | VARCHAR(120) | NOT NULL |  | Identidad del proveedor/fabricante. |
| commodity_code | VARCHAR(80) | NULL |  | Código de clasificación. |
| reorder_point | DECIMAL(12,4) | NOT NULL |  | Umbral mínimo de activación de compra. |
| unit_of_measure | VARCHAR(20) | NOT NULL |  | Unidad de medida estándar (UoM). |
| stock_policy | VARCHAR(20) | NOT NULL | CHECK | Política de reabastecimiento (Min/Max, Reorder Point, JIT). |
| is_rebuildable | BOOLEAN | NOT NULL |  | Indica si la parte se desecha o se envía a taller para reparación. |
| quantity_on_hand | DECIMAL(12,4) | NOT NULL |  | Cantidad actualmente en inventario físico. |
| reserved_quantity | DECIMAL(12,4) | NOT NULL |  | Stock comprometido para órdenes planificadas. |
| max_capacity | DECIMAL(12,4) | NOT NULL |  | Límite físico del almacén para la parte. |
| unit_cost | DECIMAL(12,2) | NOT NULL |  | Costo unitario estándar de adquisición. |
| status | VARCHAR(20) | NOT NULL | CHECK | Estado de disponibilidad del repuesto. |
| supplier_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| equipment_class_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |

#### 3.3.5 suppliers

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| name | VARCHAR(120) | NOT NULL |  | Identidad comercial del proveedor. |
| contact_info | VARCHAR(255) | NOT NULL |  | Teléfono, correo o dirección de contacto. |
| warranty_terms | VARCHAR(255) | NOT NULL |  | Términos estándar de garantía comercial. |

#### 3.3.6 warehouses

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| name | VARCHAR(80) | NOT NULL |  | Identidad del almacén. |
| location | VARCHAR(255) | NOT NULL |  | Dirección o ubicación física del almacén. |
| capacity | DECIMAL(12,4) | NOT NULL |  | Capacidad máxima volumétrica o de carga del almacén. |

### 3.4 Esquema vis

#### 3.4.1 isolation_points

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| isolation_tag | VARCHAR(80) | NOT NULL | UNIQUE | Identidad del punto de aislamiento. |
| isolation_type | VARCHAR(20) | NOT NULL | CHECK | Vocabulario de aislamiento. |
| is_verified | BOOLEAN | NOT NULL |  | Estado de verificación. |

#### 3.4.2 mesh_mappings

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_unit_id | UUID | NOT NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| mesh_uuid | VARCHAR(80) | NOT NULL | UNIQUE | Identidad o ruta del modelo 3D del activo. |
| mapping_status | VARCHAR(20) | NOT NULL | CHECK | Estado de vinculación del gemelo digital. |
| last_sync_time | TIMESTAMP | NULL |  | Tiempo de la última sincronización. |

#### 3.4.3 spatial_metadata

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| mesh_mapping_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| position | JSONB | NOT NULL |  | Coordenada espacial vectorial (ej. x,y,z). |
| rotation | JSONB | NULL |  | Descriptor de orientación (ej. cuaternión). |
| scale | JSONB | NULL |  | Descriptor de escala. |

#### 3.4.4 telemetry_signals

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| signal_type | VARCHAR(80) | NOT NULL | CHECK | Etiqueta de la señal del sensor. |
| value | DECIMAL(18,6) | NOT NULL |  | Valor de la medición cruda. |
| unit | VARCHAR(20) | NOT NULL |  | Unidad de medición. |
| threshold | DECIMAL(18,6) | NULL |  | Umbral de alerta. |
| timestamp | TIMESTAMP | NOT NULL |  | Tiempo de medición. |
| is_safety_critical | BOOLEAN | NOT NULL |  | Bandera de clasificación de seguridad. |

#### 3.4.5 visual_layers

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| work_order_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| layer_type | VARCHAR(80) | NOT NULL |  | Tipo de representación visual. |
| opacity_level | DECIMAL(5,2) | NOT NULL |  | Control de renderizado. |
| status | VARCHAR(20) | NOT NULL | CHECK | Estado de la capa visual. |

#### 3.4.6 work_order_isolations

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| work_order_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| isolation_point_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| is_isolated | BOOLEAN | NOT NULL |  | Estado de bloqueo verificado para el trabajo específico. |
| isolated_at | TIMESTAMP | NULL |  | Marca de tiempo en que se ejecutó el bloqueo. |
| padlock_tag_id | VARCHAR(80) | NULL |  | Identificador del candado o etiqueta física (Try-Out). |

#### 3.4.7 work_permits

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| permit_identifier | VARCHAR(80) | NOT NULL | UNIQUE | Trazabilidad del permiso. |
| permit_type | VARCHAR(30) | NOT NULL | CHECK | Vocabulario de permisos. |
| contractor_name | VARCHAR(150) | NOT NULL |  | Identificación del contratista. |
| status | VARCHAR(20) | NOT NULL | CHECK | Estado del ciclo de vida del permiso. |

### 3.5 Esquema adm

#### 3.5.1 audit_logs

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| user_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| entity_type | VARCHAR(80) | NOT NULL |  | Nombre de la tabla/entidad auditada. |
| entity_identifier | VARCHAR(80) | NOT NULL |  | Identificador UUID de la fila modificada. |
| action_type | VARCHAR(20) | NOT NULL | CHECK | Tipo de operación DML (CREATE, UPDATE, DELETE). |
| timestamp | TIMESTAMP | NOT NULL |  | Registro temporal preciso del evento de cambio. |
| previous_state | JSONB | NULL |  | Representación JSON descompuesta binaria antes de la acción. |
| new_state | JSONB | NULL |  | Representación JSON descompuesta binaria después de la acción. |
| integrity_hash | VARCHAR(255) | NOT NULL |  | Hash SHA-256 encadenado para detectar manipulación del log. |

#### 3.5.2 auth_tokens

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| user_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| token_hash | VARCHAR(255) | NOT NULL | UNIQUE | Hash del token de autenticación API / sesión. |
| expires_at | TIMESTAMP | NOT NULL |  | Fecha y hora de expiración del token. |
| is_used | BOOLEAN | NOT NULL |  | Indica si el token ya fue consumido (uso único). |
| ip_address | VARCHAR(45) | NULL |  | Dirección IP desde la que se emitió el token (IPv4/IPv6). |
| user_agent | VARCHAR(255) | NULL |  | Identificador del cliente/navegador para fingerprinting. |

#### 3.5.3 role_permissions

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| role_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| module | VARCHAR(80) | NOT NULL | CHECK | Módulo del sistema (ej. MTTO, INV, VIS). |
| action | VARCHAR(80) | NOT NULL |  | Acción permitida (ej. READ, CREATE, UPDATE, SIGN_OFF). |

#### 3.5.4 roles

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| role_name | VARCHAR(80) | NOT NULL | UNIQUE | Identificador del rol de usuario (ej. Planner, Technician). |
| description | VARCHAR(255) | NULL |  | Descripción del alcance del rol. |
| is_system_role | BOOLEAN | NOT NULL |  | Bandera para roles inmutables del sistema. |

#### 3.5.5 user_roles

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| user_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| role_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |

#### 3.5.6 users

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| username | VARCHAR(80) | NOT NULL | UNIQUE | Identidad de la cuenta de usuario. |
| full_name | VARCHAR(150) | NOT NULL |  | Nombre completo o institucional del usuario. |
| email | VARCHAR(150) | NOT NULL | UNIQUE | Correo electrónico institucional y de contacto. |
| status | VARCHAR(20) | NOT NULL | CHECK | Estado de la cuenta (ACTIVE, INACTIVE, LOCKED). |
| password_hash | VARCHAR(255) | NOT NULL |  | Hash de la contraseña de acceso (PBKDF2/BCrypt). |
| failed_login_attempts | INT | NOT NULL |  | Contador de intentos fallidos de autenticación. |
| lockout_until | TIMESTAMP | NULL |  | Fin del periodo de bloqueo temporal. |
| mfa_enabled | BOOLEAN | NOT NULL |  | Bandera que indica si la autenticación multifactor está activa. |
| totp_secret | VARCHAR(255) | NULL |  | Secreto compartido para autenticación TOTP (Autenticador). |
| deactivation_reason | VARCHAR(255) | NULL |  | Justificación administrativa para el borrado lógico (ISO 27001). |

#### 3.5.7 work_order_assignments

| Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| work_order_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| user_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| role_in_work | VARCHAR(50) | NOT NULL | CHECK | Rol funcional en la orden de trabajo (TECHNICIAN, SUPERVISOR). |
| assigned_at | TIMESTAMP | NOT NULL |  | Registro temporal de la asignación. |

## 4. Matriz de Relaciones y Cardinalidad (Foreign Keys)

Esta matriz especifica cómo interactúan las entidades entre sí, definiendo explícitamente las reglas de integridad referencial para autogenerar el diagrama.

| Entidad Origen (Parent) | Cardinalidad | Entidad Destino (Child) | Verbo de Negocio | Regla de Borrado en Cascada |
| --- | --- | --- | --- | --- |
| functional_locations | 1 : 0..N | functional_locations | contiene jerárquicamente a |  |
| functional_locations | 1 : 0..1 | equipment_units | instala |  |
| equipment_classes | 1 : 0..N | equipment_units | categoriza |  |
| equipment_units | 1 : 1..N | subunits | se compone de | CASCADE |
| subunits | 1 : 1..N | maintainable_items | contiene | CASCADE |
| equipment_units | 1 : 0..N | work_requests | genera |  |
| equipment_units | 1 : 0..N | maintenance_plans | posee |  |
| equipment_units | 1 : 0..N | work_orders | mantenido por |  |
| equipment_units | 1 : 0..N | backlog_items | está listado en |  |
| work_requests | 0..1 : 0..1 | work_orders | se convierte en |  |
| maintenance_plans | 1 : 0..N | work_orders | dispara |  |
| work_orders | 1 : 0..N | work_order_histories | registra cambios en | CASCADE |
| work_orders | 1 : 0..1 | failure_records | reporta |  |
| maintainable_items | 1 : 0..N | failure_records | experimenta |  |
| work_orders | 1 : 0..N | media_attachments | adjunta | CASCADE |
| work_requests | 1 : 0..1 | backlog_items | prioriza |  |
| suppliers | 1 : 0..N | spare_parts | suministra |  |
| equipment_classes | 1 : 0..N | spare_parts | estandariza |  |
| spare_parts | 1 : 0..N | inventory_transactions | involucrado en |  |
| warehouses | 1 : 0..N | inventory_transactions | almacena |  |
| warehouses | 1 : 0..N | equipment_units | resguarda en stock | SET NULL |
| work_orders | 1 : 0..N | inventory_transactions | genera |  |
| work_orders | 1 : 1..N | material_requirements | planifica | CASCADE |
| spare_parts | 1 : 1..N | material_requirements | es consumido en |  |
| maintainable_items | 1 : 1..N | maintainable_item_spare_parts | requiere | CASCADE |
| spare_parts | 1 : 1..N | maintainable_item_spare_parts | es repuesto para |  |
| equipment_units | 1 : 0..1 | mesh_mappings | representado por |  |
| mesh_mappings | 1 : 1 | spatial_metadata | ubicado en | CASCADE |
| equipment_units | 1 : 0..N | telemetry_signals | monitoreado por |  |
| equipment_units | 1 : 0..N | work_permits | autoriza intervención en |  |
| equipment_units | 1 : 0..N | isolation_points | contiene |  |
| work_permits | 1 : 0..N | work_orders | valida ejecución de |  |
| work_orders | 1 : 0..N | visual_layers | visualizada en | CASCADE |
| work_orders | 1 : 1..N | work_order_isolations | requiere | CASCADE |
| isolation_points | 1 : 1..N | work_order_isolations | bloqueado por |  |
| users | 1 : 1..N | user_roles | asociado a | CASCADE |
| roles | 1 : 1..N | user_roles | concedido a | CASCADE |
| roles | 1 : 0..N | role_permissions | contiene | CASCADE |
| users | 1 : 0..N | auth_tokens | autenticado con | CASCADE |
| users | 1 : 0..N | work_order_assignments | se le asigna | CASCADE |
| work_orders | 1 : 0..N | work_order_assignments | asigna personal | CASCADE |
| users | 1 : 0..N | audit_logs | genera | SET NULL |

## 5. Matriz de Correspondencia de Tipos de Datos (SQL Estándar vs. PostgreSQL)

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

