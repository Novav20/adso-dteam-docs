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
| equipment_classes | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_classes | class_name | VARCHAR(120) | NOT NULL | UNIQUE | Datos maestros a nivel de clase. |
| equipment_classes | description | VARCHAR(255) | NULL |  | Descripción de la clase. |
| equipment_classes | manufacturer_standard | VARCHAR(120) | NULL |  | Referencia de estandarización. |
| equipment_units | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| equipment_units | serial_number | VARCHAR(100) | NOT NULL | UNIQUE | Integridad de la identificación del activo. |
| equipment_units | manufacturer | VARCHAR(120) | NOT NULL |  | Procedencia del activo. |
| equipment_units | model | VARCHAR(120) | NOT NULL |  | Identificación del tipo de activo. |
| equipment_units | purchase_date | DATE | NOT NULL |  | Cronología de adquisiciones. |
| equipment_units | rejection_reason | VARCHAR(255) | NULL |  | Solo está presente cuando se rechaza la adquisición. |
| equipment_units | boundary_start | VARCHAR(150) | NOT NULL |  | Punto de inicio de la definición del límite. |
| equipment_units | boundary_end | VARCHAR(150) | NOT NULL |  | Punto final de la definición del límite. |
| equipment_units | acquisition_date | DATE | NOT NULL |  | Trazabilidad de la adquisición del activo. |
| equipment_units | installation_date | DATE | NULL |  | La instalación puede estar pendiente. |
| equipment_units | operation_start_date | DATE | NULL |  | El inicio operativo puede estar pendiente. |
| equipment_units | operating_hours | BIGINT | NOT NULL |  | Seguimiento de confiabilidad y uso. |
| equipment_units | surveillance_hours | BIGINT | NOT NULL |  | Tiempo de vigilancia/standby para cálculo preciso de fallas (ISO 14224). |
| equipment_units | disposal_date | DATE | NULL |  | Registro de fin de vida para trazabilidad de pasivos (ISO 55000). |
| equipment_units | disposal_reason | VARCHAR(255) | NULL |  | Razón del retiro o desmantelamiento del activo. |
| equipment_units | operational_status | VARCHAR(20) | NOT NULL |  | Vocabulario de estado operativo controlado. |
| equipment_units | lifecycle_status | VARCHAR(20) | NOT NULL |  | Vocabulario de ciclo de vida controlado. |
| equipment_units | maintenance_status | VARCHAR(30) | NOT NULL |  | Vocabulario de estado de mantenimiento controlado. |
| equipment_units | health_status | VARCHAR(30) | NULL |  | Vocabulario de estado de salud general (ISO 13374-4). |
| equipment_units | is_sce | BOOLEAN | NOT NULL |  | Indicador de Equipo Crítico de Seguridad (Safety Critical Element). |
| equipment_units | functional_location_id | UUID | NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| equipment_units | equipment_class_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| equipment_units | warehouse_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| functional_locations | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| functional_locations | tag_number | VARCHAR(50) | NOT NULL | UNIQUE | Identidad del tag de la ISO 14224 y trazabilidad de la ubicación. |
| functional_locations | name | VARCHAR(150) | NOT NULL |  | Nombre de la ubicación legible por humanos. |
| functional_locations | description | VARCHAR(255) | NULL |  | Texto explicativo opcional. |
| functional_locations | criticality | VARCHAR(30) | NOT NULL |  | Vocabulario de prioridad controlado. |
| functional_locations | geographic_location | VARCHAR(150) | NULL |  | Contexto físico de la ubicación. |
| functional_locations | environmental_exposure | VARCHAR(150) | NULL |  | Condiciones ambientales para cálculos de confiabilidad (ISO 14224). |
| functional_locations | hierarchy_level | SMALLINT | NOT NULL |  | Niveles 1 al 5 de la taxonomía ISO 14224 (las Ubicaciones Funcionales gobiernan la estructura espacial de planta hasta el proceso, mientras que L6 a L8 corresponden a equipos y componentes físicos). |
| functional_locations | parent_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| maintainable_items | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| maintainable_items | subunit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| maintainable_items | component_name | VARCHAR(120) | NOT NULL |  | Identidad del ítem mantenible. |
| maintainable_items | subunit_type | VARCHAR(80) | NOT NULL |  | Clasificación taxonómica. |
| maintainable_items | spare_part_type | VARCHAR(80) | NULL |  | Correspondencia opcional de partes de repuesto. |
| maintainable_items | design_attributes | JSONB | NULL |  | Propiedades estáticas de diseño estructuradas (ISO 14224 Anexo A). |
| maintainable_items | status | VARCHAR(30) | NOT NULL |  | Estado del ciclo de vida del ítem. |
| subunits | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| subunits | equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| subunits | subunit_type | VARCHAR(80) | NOT NULL |  | Taxonomía del subcomponente. |
| subunits | name | VARCHAR(120) | NOT NULL |  | Etiqueta del subcomponente. |

### 3.2 Esquema mtto

| Entidad | Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- | --- |
| backlog_items | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| backlog_items | equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| backlog_items | work_request_id | UUID | NOT NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| backlog_items | priority_score | INT | NOT NULL |  | Puntaje del backlog derivado de RIME (Calculado). |
| backlog_items | status | VARCHAR(20) | NOT NULL |  | Estado del ciclo de vida del backlog (priorización). |
| failure_records | id | UUID | NOT NULL | PK | Identidad del evento de falla. |
| failure_records | work_order_id | UUID | NOT NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| failure_records | maintainable_item_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| failure_records | failure_mode | VARCHAR(120) | NOT NULL |  | Codificación de fallas de la ISO 14224. |
| failure_records | failure_mechanism | VARCHAR(120) | NOT NULL |  | Codificación de fallas de la ISO 14224. |
| failure_records | failure_cause | VARCHAR(120) | NOT NULL |  | Codificación de fallas de la ISO 14224. |
| failure_records | detection_method | VARCHAR(120) | NOT NULL |  | Método de detección de la falla (ISO 14224). |
| failure_records | operational_condition | VARCHAR(120) | NOT NULL |  | Condición operativa al momento de la falla (ISO 14224). |
| failure_records | operational_impact | VARCHAR(120) | NOT NULL |  | Impacto operacional de la falla (ISO 14224). |
| failure_records | downtime | DECIMAL(10,2) | NOT NULL |  | Métrica de análisis de confiabilidad (Calculada). |
| failure_records | status | VARCHAR(20) | NOT NULL |  | Estado del registro de fallas. |
| maintenance_plans | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| maintenance_plans | equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| maintenance_plans | maintenance_method | VARCHAR(80) | NOT NULL |  | Estrategia de mantenimiento (PM, PdM, CBM). |
| maintenance_plans | frequency | VARCHAR(50) | NOT NULL |  | Descripción de la frecuencia legible por humanos. |
| maintenance_plans | frequency_type | VARCHAR(20) | NOT NULL |  | Cadencia controlada del plan. |
| maintenance_plans | next_work_order_date | DATE | NULL |  | Fecha de ejecución programada (Calculada). |
| maintenance_plans | interval_value | DECIMAL(12,2) | NULL |  | Valor numérico del intervalo para telemetría (ej. 500 horas). |
| maintenance_plans | next_trigger_limit | DECIMAL(12,2) | NULL |  | Límite acumulado calculado para el próximo disparo. |
| maintenance_plans | estimated_labor_hours | DECIMAL(10,2) | NOT NULL |  | Horas-Hombre estimadas (Wrench Time) para planificación. |
| maintenance_plans | required_specialty | VARCHAR(80) | NOT NULL |  | Especialidad técnica requerida (ej. Mecánica, Eléctrica). |
| maintenance_plans | technical_description | VARCHAR(255) | NOT NULL |  | Descripción técnica del alcance de las tareas. |
| maintenance_plans | status | VARCHAR(20) | NOT NULL |  | Estado del ciclo de vida del plan (documento). |
| media_attachments | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| media_attachments | work_order_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| media_attachments | file_url | VARCHAR(255) | NOT NULL |  | Ubicación de la evidencia. |
| media_attachments | file_type | VARCHAR(20) | NOT NULL |  | Formato de archivo adjunto controlado. |
| media_attachments | uploaded_at | TIMESTAMP | NOT NULL |  | Tiempo de subida/ingesta de la evidencia. |
| work_order_histories | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| work_order_histories | work_order_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_order_histories | old_status | VARCHAR(20) | NULL |  | Estado anterior del ciclo de vida (NULL si es primer estado). |
| work_order_histories | new_status | VARCHAR(20) | NOT NULL |  | Nuevo estado del ciclo de vida. |
| work_order_histories | timestamp | TIMESTAMP | NOT NULL |  | Tiempo de transición. |
| work_order_histories | duration_seconds | BIGINT | NULL |  | Tiempo empleado en el estado (Calculado al transicionar). |
| work_orders | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| work_orders | equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_orders | maintenance_plan_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_orders | work_request_id | UUID | NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| work_orders | work_permit_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_orders | current_status | VARCHAR(20) | NOT NULL |  | Estado del ciclo de vida de ejecución (FSM). |
| work_orders | maintenance_method | VARCHAR(80) | NOT NULL |  | Método de mantenimiento (Correctivo, Preventivo, etc.). |
| work_orders | creation_date | TIMESTAMP | NOT NULL |  | Marca de tiempo (timestamp) de creación de la orden. |
| work_orders | scheduled_date | TIMESTAMP | NULL |  | Inicio planeado. |
| work_orders | actual_start | TIMESTAMP | NULL |  | Inicio real de la ejecución. |
| work_orders | actual_finish | TIMESTAMP | NULL |  | Finalización real de la ejecución. |
| work_orders | actual_labor_hours | DECIMAL(10,2) | NULL |  | Duración laboral real (Calculada). |
| work_orders | criticality | VARCHAR(20) | NOT NULL |  | Etiqueta de criticidad / prioridad de la OT. |
| work_requests | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| work_requests | equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_requests | description | VARCHAR(255) | NOT NULL |  | Narrativa de la solicitud. |
| work_requests | priority | VARCHAR(20) | NOT NULL |  | Etiqueta de prioridad de la solicitud. |
| work_requests | request_date | TIMESTAMP | NOT NULL |  | Línea de tiempo para auditoría. |
| work_requests | request_source | VARCHAR(80) | NOT NULL |  | Origen de la solicitud. |
| work_requests | status | VARCHAR(20) | NOT NULL |  | Estado del ciclo de vida de la solicitud. |
| work_requests | work_class_code | SMALLINT | NOT NULL |  | Peso numérico de la clase de trabajo seleccionada para el RIME. |

### 3.3 Esquema inv

| Entidad | Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- | --- |
| inventory_transactions | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| inventory_transactions | spare_part_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| inventory_transactions | warehouse_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| inventory_transactions | work_order_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| inventory_transactions | quantity | DECIMAL(12,4) | NOT NULL |  | Cantidad transada (positiva para entradas, negativa para salidas). |
| inventory_transactions | transaction_type | VARCHAR(20) | NOT NULL |  | Tipo de movimiento (RECEIPT, ISSUE, ADJUSTMENT). |
| inventory_transactions | timestamp | TIMESTAMP | NOT NULL |  | Registro temporal preciso del movimiento. |
| inventory_transactions | reason | VARCHAR(255) | NOT NULL |  | Razón del movimiento o referencia a documentos externos. |
| inventory_transactions | total_cost | DECIMAL(12,2) | NOT NULL |  | Costo total de la transacción (Cantidad \* Costo). |
| inventory_transactions | aisle_shelf_location | VARCHAR(150) | NULL |  | Ubicación física específica de la transacción (pasillo/estante). |
| inventory_transactions | serial_number | VARCHAR(100) | NULL |  | Número de serie o Tag del equipo rotativo (Asset Swap). |
| maintainable_item_spare_parts | maintainable_item_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| maintainable_item_spare_parts | spare_part_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| material_requirements | work_order_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| material_requirements | spare_part_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| material_requirements | planned_quantity | DECIMAL(12,4) | NOT NULL |  | Repuestos planificados antes de la ejecución de la OT. |
| material_requirements | actual_quantity | DECIMAL(12,4) | NULL |  | Repuestos realmente consumidos durante la ejecución de la OT. |
| material_requirements | is_reserved | BOOLEAN | NOT NULL |  | Bandera que indica si el stock ya fue apartado en almacén. |
| spare_parts | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| spare_parts | sku | VARCHAR(80) | NOT NULL | UNIQUE | Identidad de la parte. |
| spare_parts | description | VARCHAR(255) | NOT NULL |  | Descripción de la parte legible por humanos. |
| spare_parts | manufacturer | VARCHAR(120) | NOT NULL |  | Identidad del proveedor/fabricante. |
| spare_parts | commodity_code | VARCHAR(80) | NULL |  | Código de clasificación. |
| spare_parts | reorder_point | DECIMAL(12,4) | NOT NULL |  | Umbral mínimo de activación de compra. |
| spare_parts | unit_of_measure | VARCHAR(20) | NOT NULL |  | Unidad de medida estándar (UoM). |
| spare_parts | stock_policy | VARCHAR(20) | NOT NULL |  | Política de reabastecimiento (Min/Max, Reorder Point, JIT). |
| spare_parts | is_rebuildable | BOOLEAN | NOT NULL |  | Indica si la parte se desecha o se envía a taller para reparación. |
| spare_parts | quantity_on_hand | DECIMAL(12,4) | NOT NULL |  | Cantidad actualmente en inventario físico. |
| spare_parts | reserved_quantity | DECIMAL(12,4) | NOT NULL |  | Stock comprometido para órdenes planificadas. |
| spare_parts | max_capacity | DECIMAL(12,4) | NOT NULL |  | Límite físico del almacén para la parte. |
| spare_parts | unit_cost | DECIMAL(12,2) | NOT NULL |  | Costo unitario estándar de adquisición. |
| spare_parts | status | VARCHAR(20) | NOT NULL |  | Estado de disponibilidad del repuesto. |
| spare_parts | supplier_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| spare_parts | equipment_class_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| suppliers | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| suppliers | name | VARCHAR(120) | NOT NULL |  | Identidad comercial del proveedor. |
| suppliers | contact_info | VARCHAR(255) | NOT NULL |  | Teléfono, correo o dirección de contacto. |
| suppliers | warranty_terms | VARCHAR(255) | NOT NULL |  | Términos estándar de garantía comercial. |
| warehouses | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| warehouses | name | VARCHAR(80) | NOT NULL |  | Identidad del almacén. |
| warehouses | location | VARCHAR(255) | NOT NULL |  | Dirección o ubicación física del almacén. |
| warehouses | capacity | DECIMAL(12,4) | NOT NULL |  | Capacidad máxima volumétrica o de carga del almacén. |

### 3.4 Esquema vis

| Entidad | Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- | --- |
| isolation_points | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| isolation_points | equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| isolation_points | isolation_tag | VARCHAR(80) | NOT NULL | UNIQUE | Identidad del punto de aislamiento. |
| isolation_points | isolation_type | VARCHAR(20) | NOT NULL |  | Vocabulario de aislamiento. |
| isolation_points | is_verified | BOOLEAN | NOT NULL |  | Estado de verificación. |
| mesh_mappings | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| mesh_mappings | equipment_unit_id | UUID | NOT NULL | FK, UNIQUE | Llave foránea hacia la tabla relacionada. |
| mesh_mappings | mesh_uuid | VARCHAR(80) | NOT NULL | UNIQUE | Identidad o ruta del modelo 3D del activo. |
| mesh_mappings | mapping_status | VARCHAR(20) | NOT NULL |  | Estado de vinculación del gemelo digital. |
| mesh_mappings | last_sync_time | TIMESTAMP | NULL |  | Tiempo de la última sincronización. |
| spatial_metadata | mesh_mapping_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| spatial_metadata | position | JSONB | NOT NULL |  | Coordenada espacial vectorial (ej. x,y,z). |
| spatial_metadata | rotation | JSONB | NULL |  | Descriptor de orientación (ej. cuaternión). |
| spatial_metadata | scale | JSONB | NULL |  | Descriptor de escala. |
| telemetry_signals | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| telemetry_signals | equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| telemetry_signals | signal_type | VARCHAR(80) | NOT NULL |  | Etiqueta de la señal del sensor. |
| telemetry_signals | value | DECIMAL(18,6) | NOT NULL |  | Valor de la medición cruda. |
| telemetry_signals | unit | VARCHAR(20) | NOT NULL |  | Unidad de medición. |
| telemetry_signals | threshold | DECIMAL(18,6) | NULL |  | Umbral de alerta. |
| telemetry_signals | timestamp | TIMESTAMP | NOT NULL |  | Tiempo de medición. |
| telemetry_signals | is_safety_critical | BOOLEAN | NOT NULL |  | Bandera de clasificación de seguridad. |
| visual_layers | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| visual_layers | work_order_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| visual_layers | layer_type | VARCHAR(80) | NOT NULL |  | Tipo de representación visual. |
| visual_layers | opacity_level | DECIMAL(5,2) | NOT NULL |  | Control de renderizado. |
| visual_layers | status | VARCHAR(20) | NOT NULL |  | Estado de la capa visual. |
| work_order_isolations | work_order_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| work_order_isolations | isolation_point_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| work_order_isolations | is_isolated | BOOLEAN | NOT NULL |  | Estado de bloqueo verificado para el trabajo específico. |
| work_order_isolations | isolated_at | TIMESTAMP | NULL |  | Marca de tiempo en que se ejecutó el bloqueo. |
| work_order_isolations | padlock_tag_id | VARCHAR(80) | NULL |  | Identificador del candado o etiqueta física (Try-Out). |
| work_permits | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| work_permits | equipment_unit_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_permits | permit_identifier | VARCHAR(80) | NOT NULL | UNIQUE | Trazabilidad del permiso. |
| work_permits | permit_type | VARCHAR(30) | NOT NULL |  | Vocabulario de permisos. |
| work_permits | contractor_name | VARCHAR(150) | NOT NULL |  | Identificación del contratista. |
| work_permits | status | VARCHAR(20) | NOT NULL |  | Estado del ciclo de vida del permiso. |

### 3.5 Esquema adm

| Entidad | Campo Físico | Tipo PostgreSQL | Nulabilidad | Restricciones / Llaves | Justificación |
| --- | --- | --- | --- | --- | --- |
| audit_logs | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| audit_logs | user_id | UUID | NULL | FK | Llave foránea hacia la tabla relacionada. |
| audit_logs | entity_type | VARCHAR(80) | NOT NULL |  | Nombre de la tabla/entidad auditada. |
| audit_logs | entity_identifier | VARCHAR(80) | NOT NULL |  | Identificador UUID de la fila modificada. |
| audit_logs | action_type | VARCHAR(20) | NOT NULL |  | Tipo de operación DML (CREATE, UPDATE, DELETE). |
| audit_logs | timestamp | TIMESTAMP | NOT NULL |  | Registro temporal preciso del evento de cambio. |
| audit_logs | previous_state | JSONB | NULL |  | Representación JSON descompuesta binaria antes de la acción. |
| audit_logs | new_state | JSONB | NULL |  | Representación JSON descompuesta binaria después de la acción. |
| audit_logs | integrity_hash | VARCHAR(255) | NOT NULL |  | Hash SHA-256 encadenado para detectar manipulación del log. |
| auth_tokens | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| auth_tokens | user_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| auth_tokens | token_hash | VARCHAR(255) | NOT NULL | UNIQUE | Hash del token de autenticación API / sesión. |
| auth_tokens | expires_at | TIMESTAMP | NOT NULL |  | Fecha y hora de expiración del token. |
| auth_tokens | is_used | BOOLEAN | NOT NULL |  | Indica si el token ya fue consumido (uso único). |
| auth_tokens | ip_address | VARCHAR(45) | NULL |  | Dirección IP desde la que se emitió el token (IPv4/IPv6). |
| auth_tokens | user_agent | VARCHAR(255) | NULL |  | Identificador del cliente/navegador para fingerprinting. |
| role_permissions | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| role_permissions | role_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| role_permissions | module | VARCHAR(80) | NOT NULL |  | Módulo del sistema (ej. MTTO, INV, VIS). |
| role_permissions | action | VARCHAR(80) | NOT NULL |  | Acción permitida (ej. READ, CREATE, UPDATE, SIGN_OFF). |
| roles | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| roles | role_name | VARCHAR(80) | NOT NULL | UNIQUE | Identificador del rol de usuario (ej. Planner, Technician). |
| roles | description | VARCHAR(255) | NULL |  | Descripción del alcance del rol. |
| roles | is_system_role | BOOLEAN | NOT NULL |  | Bandera para roles inmutables del sistema. |
| user_roles | user_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| user_roles | role_id | UUID | NOT NULL | PK, FK | Llave foránea hacia la tabla relacionada. |
| users | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| users | username | VARCHAR(80) | NOT NULL | UNIQUE | Identidad de la cuenta de usuario. |
| users | full_name | VARCHAR(150) | NOT NULL |  | Nombre completo o institucional del usuario. |
| users | email | VARCHAR(150) | NOT NULL | UNIQUE | Correo electrónico institucional y de contacto. |
| users | status | VARCHAR(20) | NOT NULL |  | Estado de la cuenta (ACTIVE, INACTIVE, LOCKED). |
| users | password_hash | VARCHAR(255) | NOT NULL |  | Hash de la contraseña de acceso (PBKDF2/BCrypt). |
| users | failed_login_attempts | INT | NOT NULL |  | Contador de intentos fallidos de autenticación. |
| users | lockout_until | TIMESTAMP | NULL |  | Fin del periodo de bloqueo temporal. |
| users | mfa_enabled | BOOLEAN | NOT NULL |  | Bandera que indica si la autenticación multifactor está activa. |
| users | totp_secret | VARCHAR(255) | NULL |  | Secreto compartido para autenticación TOTP (Autenticador). |
| users | deactivation_reason | VARCHAR(255) | NULL |  | Justificación administrativa para el borrado lógico (ISO 27001). |
| work_order_assignments | id | UUID | NOT NULL | PK | Identificador único de la entidad (PK). |
| work_order_assignments | work_order_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_order_assignments | user_id | UUID | NOT NULL | FK | Llave foránea hacia la tabla relacionada. |
| work_order_assignments | role_in_work | VARCHAR(50) | NOT NULL |  | Rol funcional en la orden de trabajo (TECHNICIAN, SUPERVISOR). |
| work_order_assignments | assigned_at | TIMESTAMP | NOT NULL |  | Registro temporal de la asignación. |

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

