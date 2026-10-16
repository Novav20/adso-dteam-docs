-- ==========================================
-- AUTO-GENERATED DDL SCRIPT
-- ==========================================

CREATE SCHEMA IF NOT EXISTS tax;
CREATE SCHEMA IF NOT EXISTS mtto;
CREATE SCHEMA IF NOT EXISTS inv;
CREATE SCHEMA IF NOT EXISTS vis;
CREATE SCHEMA IF NOT EXISTS adm;

-- ==========================================
-- SCHEMA: TAX
-- ==========================================

CREATE TABLE IF NOT EXISTS tax.equipment_classes (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    class_name                VARCHAR(120) NOT NULL,
    description               VARCHAR(255),
    manufacturer_standard     VARCHAR(120),

    CONSTRAINT uq_equipment_classes_class_name UNIQUE (class_name),
    CONSTRAINT pk_equipment_classes PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tax.equipment_units (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    serial_number             VARCHAR(100) NOT NULL,
    manufacturer              VARCHAR(120) NOT NULL,
    model                     VARCHAR(120) NOT NULL,
    purchase_date             DATE NOT NULL,
    rejection_reason          VARCHAR(255),
    boundary_start            VARCHAR(150) NOT NULL,
    boundary_end              VARCHAR(150) NOT NULL,
    acquisition_date          DATE NOT NULL,
    installation_date         DATE,
    operation_start_date      DATE,
    operating_hours           BIGINT NOT NULL DEFAULT 0,
    surveillance_hours        BIGINT NOT NULL DEFAULT 0,
    disposal_date             DATE,
    disposal_reason           VARCHAR(255),
    operational_status        VARCHAR(20) NOT NULL,
    lifecycle_status          VARCHAR(20) NOT NULL,
    maintenance_status        VARCHAR(30) NOT NULL,
    health_status             VARCHAR(30),
    is_sce                    BOOLEAN NOT NULL DEFAULT FALSE,
    functional_location_id    UUID,
    equipment_class_id        UUID NOT NULL,
    warehouse_id              UUID,

    CONSTRAINT uq_equipment_units_serial_number UNIQUE (serial_number),
    CONSTRAINT ck_equipment_units_operational_status CHECK (operational_status IN ('UP', 'DOWN', 'STANDBY')),
    CONSTRAINT ck_equipment_units_lifecycle_status CHECK (lifecycle_status IN ('IN_STORAGE', 'INSTALLED', 'COMMISSIONING', 'DECOMMISSIONED')),
    CONSTRAINT ck_equipment_units_maintenance_status CHECK (maintenance_status IN ('OPERATIONAL', 'UNDER_MAINTENANCE', 'UNDER_TEST')),
    CONSTRAINT ck_equipment_units_health_status CHECK (health_status IN ('UNDETERMINED', 'GOOD', 'FAIR', 'SERIOUS_BUT_STABLE', 'SERIOUS', 'CRITICAL_BUT_STABLE', 'CRITICAL')),
    CONSTRAINT uq_equipment_units_functional_location_id UNIQUE (functional_location_id),
    CONSTRAINT pk_equipment_units PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tax.functional_locations (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    tag_number                VARCHAR(50) NOT NULL,
    name                      VARCHAR(150) NOT NULL,
    description               VARCHAR(255),
    criticality               VARCHAR(30) NOT NULL,
    geographic_location       VARCHAR(150),
    environmental_exposure    VARCHAR(150),
    hierarchy_level           SMALLINT NOT NULL,
    parent_id                 UUID,

    CONSTRAINT uq_functional_locations_tag_number UNIQUE (tag_number),
    CONSTRAINT ck_functional_locations_environmental_exposure CHECK (environmental_exposure IN ('SEVERE', 'MODERATE', 'LOW', 'UNKNOWN')),
    CONSTRAINT pk_functional_locations PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tax.maintainable_items (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    subunit_id                UUID NOT NULL,
    component_name            VARCHAR(120) NOT NULL,
    subunit_type              VARCHAR(80) NOT NULL,
    spare_part_type           VARCHAR(80),
    design_attributes         JSONB,
    status                    VARCHAR(30) NOT NULL,

    CONSTRAINT ck_maintainable_items_status CHECK (status IN ('OPERATIONAL', 'DEGRADED', 'FAILED', 'UNDER_REPAIR', 'REPLACED')),
    CONSTRAINT pk_maintainable_items PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tax.subunits (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    equipment_unit_id         UUID NOT NULL,
    subunit_type              VARCHAR(80) NOT NULL,
    name                      VARCHAR(120) NOT NULL,

    CONSTRAINT pk_subunits PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tax.asset_installations (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    functional_location_id    UUID NOT NULL,
    equipment_unit_id         UUID NOT NULL,
    installed_at              TIMESTAMP NOT NULL DEFAULT now(),
    removed_at                TIMESTAMP,

    CONSTRAINT uq_asset_installations_removed_at UNIQUE (removed_at),
    CONSTRAINT pk_asset_installations PRIMARY KEY (id)
);

-- ==========================================
-- SCHEMA: MTTO
-- ==========================================

CREATE TABLE IF NOT EXISTS mtto.backlog_items (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    equipment_unit_id         UUID NOT NULL,
    work_request_id           UUID NOT NULL,
    priority_score            INT NOT NULL,
    status                    VARCHAR(20) NOT NULL,

    CONSTRAINT ck_backlog_items_status CHECK (status IN ('PENDING', 'READY', 'DEFERRED')),
    CONSTRAINT pk_backlog_items PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mtto.failure_records (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    work_order_id             UUID NOT NULL,
    maintainable_item_id      UUID,
    failure_mode              VARCHAR(120) NOT NULL,
    failure_mechanism         VARCHAR(120) NOT NULL,
    failure_cause             VARCHAR(120) NOT NULL,
    detection_method          VARCHAR(120) NOT NULL,
    operational_condition     VARCHAR(120) NOT NULL,
    operational_impact        VARCHAR(120) NOT NULL,
    technician_notes          TEXT,
    downtime                  DECIMAL(10,2) NOT NULL,
    status                    VARCHAR(20) NOT NULL,

    CONSTRAINT ck_failure_records_detection_method CHECK (detection_method IN ('PERIODIC_MAINTENANCE', 'FUNCTIONAL_TESTING', 'INSPECTION', 'PERIODIC_CBM', 'PRESSURE_TESTING', 'CONTINUOUS_CBM', 'PRODUCTION_INTERFERENCE', 'CASUAL_OBSERVATION', 'CORRECTIVE_MAINTENANCE', 'ON_DEMAND', 'OTHER')),
    CONSTRAINT ck_failure_records_operational_condition CHECK (operational_condition IN ('RUNNING', 'START_UP', 'RUN_DOWN', 'HOT_STANDBY', 'COLD_STANDBY', 'IDLE', 'TESTING')),
    CONSTRAINT ck_failure_records_operational_impact CHECK (operational_impact IN ('EXTENSIVE_STOP', 'STOP_ABOVE_ACCEPTABLE', 'STOP_BELOW_ACCEPTABLE', 'STOP_MINOR')),
    CONSTRAINT pk_failure_records PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mtto.maintenance_plans (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    equipment_unit_id         UUID NOT NULL,
    maintenance_method        VARCHAR(80) NOT NULL,
    frequency                 VARCHAR(50) NOT NULL,
    frequency_type            VARCHAR(20) NOT NULL,
    next_work_order_date      DATE,
    interval_value            DECIMAL(12,2),
    next_trigger_limit        DECIMAL(12,2),
    estimated_labor_hours     DECIMAL(10,2) NOT NULL,
    required_specialty        VARCHAR(80) NOT NULL,
    technical_description     VARCHAR(255) NOT NULL,
    status                    VARCHAR(20) NOT NULL,

    CONSTRAINT ck_maintenance_plans_maintenance_method CHECK (maintenance_method IN ('PREVENTIVE', 'PREDICTIVE', 'CONDITION_BASED')),
    CONSTRAINT ck_maintenance_plans_frequency_type CHECK (frequency_type IN ('CALENDAR_TIME', 'OPERATING_HOURS', 'CYCLES')),
    CONSTRAINT ck_maintenance_plans_required_specialty CHECK (required_specialty IN ('MECHANICAL', 'ELECTRICAL', 'INSTRUMENTATION_AND_CONTROL', 'LUBRICATION', 'CONDITION_MONITORING', 'ELECTRONICS', 'WELDING_FABRICATION', 'FACILITIES')),
    CONSTRAINT ck_maintenance_plans_status CHECK (status IN ('DRAFT', 'ACTIVE', 'INACTIVE', 'ARCHIVED')),
    CONSTRAINT pk_maintenance_plans PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mtto.media_attachments (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    work_order_id             UUID NOT NULL,
    failure_record_id         UUID,
    file_url                  VARCHAR(255) NOT NULL,
    file_type                 VARCHAR(20) NOT NULL,
    uploaded_at               TIMESTAMP NOT NULL,

    CONSTRAINT ck_media_attachments_file_type CHECK (file_type IN ('PDF', 'JPG', 'PNG')),
    CONSTRAINT pk_media_attachments PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mtto.work_order_histories (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    work_order_id             UUID NOT NULL,
    old_status                VARCHAR(20),
    new_status                VARCHAR(20) NOT NULL,
    timestamp                 TIMESTAMP NOT NULL DEFAULT clock_timestamp(),
    duration_seconds          BIGINT,

    CONSTRAINT pk_work_order_histories PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mtto.work_orders (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    equipment_unit_id         UUID NOT NULL,
    maintenance_plan_id       UUID,
    work_request_id           UUID,
    work_permit_id            UUID,
    current_status            VARCHAR(20) NOT NULL,
    maintenance_method        VARCHAR(80) NOT NULL,
    creation_date             TIMESTAMP NOT NULL,
    scheduled_date            TIMESTAMP,
    actual_start              TIMESTAMP,
    actual_finish             TIMESTAMP,
    actual_labor_hours        DECIMAL(10,2),
    criticality               VARCHAR(20) NOT NULL,

    CONSTRAINT ck_work_orders_current_status CHECK (current_status IN ('PLANNING', 'WAITING_PARTS', 'SCHEDULED', 'IN_PROGRESS', 'SUSPENDED', 'COMPLETE', 'CLOSED')),
    CONSTRAINT ck_work_orders_maintenance_method CHECK (maintenance_method IN ('CORRECTIVE', 'PREVENTIVE', 'PREDICTIVE', 'IMPROVEMENT')),
    CONSTRAINT ck_work_orders_criticality CHECK (criticality IN ('EMERGENCY', 'URGENT', 'NORMAL', 'LOW')),
    CONSTRAINT pk_work_orders PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS mtto.work_requests (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    equipment_unit_id         UUID NOT NULL,
    description               VARCHAR(255) NOT NULL,
    priority                  VARCHAR(20) NOT NULL,
    request_date              TIMESTAMP NOT NULL,
    request_source            VARCHAR(80) NOT NULL,
    status                    VARCHAR(20) NOT NULL,
    work_class                SMALLINT NOT NULL,

    CONSTRAINT ck_work_requests_status CHECK (status IN ('NEW', 'APPROVED', 'REJECTED')),
    -- CONSTRAINT ck_work_requests_work_class CHECK (...) /* Missing explicit enum for work_requests.work_class */,
    CONSTRAINT pk_work_requests PRIMARY KEY (id)
);

-- ==========================================
-- SCHEMA: INV
-- ==========================================

CREATE TABLE IF NOT EXISTS inv.inventory_transactions (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    spare_part_id             UUID NOT NULL,
    warehouse_id              UUID NOT NULL,
    work_order_id             UUID,
    quantity                  DECIMAL(12,4) NOT NULL DEFAULT 1,
    transaction_type          VARCHAR(20) NOT NULL,
    timestamp                 TIMESTAMP NOT NULL DEFAULT clock_timestamp(),
    reason                    VARCHAR(255) NOT NULL,
    total_cost                DECIMAL(12,2) NOT NULL,
    locator_id                UUID,
    serial_number             VARCHAR(100),

    CONSTRAINT ck_inventory_transactions_transaction_type CHECK (transaction_type IN ('RECEIPT', 'ISSUE', 'ADJUSTMENT')),
    CONSTRAINT pk_inventory_transactions PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS inv.maintainable_item_spare_parts (
    maintainable_item_id      UUID NOT NULL,
    spare_part_id             UUID NOT NULL,

    CONSTRAINT pk_maintainable_item_spare_parts PRIMARY KEY (maintainable_item_id, spare_part_id)
);

CREATE TABLE IF NOT EXISTS inv.material_requirements (
    work_order_id             UUID NOT NULL,
    spare_part_id             UUID NOT NULL,
    planned_quantity          DECIMAL(12,4) NOT NULL DEFAULT 1,
    actual_quantity           DECIMAL(12,4),
    is_reserved               BOOLEAN NOT NULL,

    CONSTRAINT pk_material_requirements PRIMARY KEY (work_order_id, spare_part_id)
);

CREATE TABLE IF NOT EXISTS inv.spare_parts (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    sku                       VARCHAR(80) NOT NULL,
    description               VARCHAR(255) NOT NULL,
    manufacturer              VARCHAR(120) NOT NULL,
    commodity_code            VARCHAR(80),
    reorder_point             DECIMAL(12,4) NOT NULL,
    unit_of_measure           VARCHAR(20) NOT NULL,
    stock_policy              VARCHAR(20) NOT NULL,
    is_rebuildable            BOOLEAN NOT NULL DEFAULT FALSE,
    quantity_on_hand          DECIMAL(12,4) NOT NULL,
    reserved_quantity         DECIMAL(12,4) NOT NULL,
    max_capacity              DECIMAL(12,4) NOT NULL,
    unit_cost                 DECIMAL(12,2) NOT NULL,
    status                    VARCHAR(20) NOT NULL,
    supplier_id               UUID NOT NULL,
    equipment_class_id        UUID,

    CONSTRAINT uq_spare_parts_sku UNIQUE (sku),
    CONSTRAINT ck_spare_parts_stock_policy CHECK (stock_policy IN ('REORDER_POINT', 'MIN_MAX', 'JUST_IN_TIME')),
    CONSTRAINT ck_spare_parts_status CHECK (status IN ('ACTIVE', 'OBSOLETE', 'SUSPENDED')),
    CONSTRAINT pk_spare_parts PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS inv.suppliers (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    name                      VARCHAR(120) NOT NULL,
    contact_info              VARCHAR(255) NOT NULL,
    warranty_terms            VARCHAR(255) NOT NULL,

    CONSTRAINT pk_suppliers PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS inv.locators (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    warehouse_id              UUID NOT NULL,
    aisle                     VARCHAR(50) NOT NULL,
    rack                      VARCHAR(50),
    shelf                     VARCHAR(50),
    barcode                   VARCHAR(100),
    is_active                 BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_locators_barcode UNIQUE (barcode),
    CONSTRAINT pk_locators PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS inv.warehouses (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    name                      VARCHAR(80) NOT NULL,
    location                  VARCHAR(255) NOT NULL,
    capacity                  DECIMAL(12,4) NOT NULL,

    CONSTRAINT pk_warehouses PRIMARY KEY (id)
);

-- ==========================================
-- SCHEMA: VIS
-- ==========================================

CREATE TABLE IF NOT EXISTS vis.isolation_points (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    equipment_unit_id         UUID NOT NULL,
    isolation_tag             VARCHAR(80) NOT NULL,
    isolation_type            VARCHAR(20) NOT NULL,
    is_verified               BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT uq_isolation_points_isolation_tag UNIQUE (isolation_tag),
    CONSTRAINT ck_isolation_points_isolation_type CHECK (isolation_type IN ('ELECTRICAL', 'MECHANICAL', 'PNEUMATIC', 'HYDRAULIC', 'CHEMICAL', 'THERMAL', 'GRAVITATIONAL')),
    CONSTRAINT pk_isolation_points PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS vis.mesh_mappings (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    equipment_unit_id         UUID NOT NULL,
    mesh_uuid                 VARCHAR(80) NOT NULL,
    mapping_status            VARCHAR(20) NOT NULL,
    last_sync_time            TIMESTAMP,

    CONSTRAINT uq_mesh_mappings_equipment_unit_id UNIQUE (equipment_unit_id),
    CONSTRAINT uq_mesh_mappings_mesh_uuid UNIQUE (mesh_uuid),
    CONSTRAINT ck_mesh_mappings_mapping_status CHECK (mapping_status IN ('MAPPED', 'UNMAPPED', 'SYNC_ERROR')),
    CONSTRAINT pk_mesh_mappings PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS vis.spatial_metadata (
    mesh_mapping_id           UUID NOT NULL,
    position                  JSONB NOT NULL,
    rotation                  JSONB,
    scale                     JSONB,

    CONSTRAINT pk_spatial_metadata PRIMARY KEY (mesh_mapping_id)
);

CREATE TABLE IF NOT EXISTS vis.telemetry_signals (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    equipment_unit_id         UUID NOT NULL,
    signal_type               VARCHAR(80) NOT NULL,
    value                     DECIMAL(18,6) NOT NULL,
    unit                      VARCHAR(20) NOT NULL,
    threshold                 DECIMAL(18,6),
    timestamp                 TIMESTAMP NOT NULL DEFAULT clock_timestamp(),
    is_safety_critical        BOOLEAN NOT NULL,

    CONSTRAINT ck_telemetry_signals_signal_type CHECK (signal_type IN ('TEMPERATURE', 'PRESSURE', 'VIBRATION', 'FLOW_RATE', 'VOLTAGE', 'RPM')),
    CONSTRAINT pk_telemetry_signals PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS vis.visual_layers (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    work_order_id             UUID NOT NULL,
    layer_type                VARCHAR(80) NOT NULL,
    opacity_level             DECIMAL(5,2) NOT NULL,
    status                    VARCHAR(20) NOT NULL,

    CONSTRAINT ck_visual_layers_status CHECK (status IN ('VISIBLE', 'HIDDEN', 'GHOSTED')),
    CONSTRAINT pk_visual_layers PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS vis.work_order_isolations (
    work_order_id             UUID NOT NULL,
    isolation_point_id        UUID NOT NULL,
    is_isolated               BOOLEAN NOT NULL DEFAULT FALSE,
    isolated_at               TIMESTAMP,
    padlock_tag_id            VARCHAR(80),
    try_out_confirmed         BOOLEAN NOT NULL DEFAULT FALSE,
    try_out_at                TIMESTAMP,
    try_out_method            VARCHAR(40),
    try_out_reading           VARCHAR(80),
    telemetry_snapshot        JSONB,
    signature_hash            VARCHAR(64),

    CONSTRAINT ck_work_order_isolations_try_out_method CHECK (try_out_method IN ('MULTIMETER_PROBE', 'ATMOSPHERIC_VENT_BLEED', 'LOCAL_PUSHBUTTON_ATTEMPT')),
    CONSTRAINT pk_work_order_isolations PRIMARY KEY (work_order_id, isolation_point_id)
);

CREATE TABLE IF NOT EXISTS vis.work_permits (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    equipment_unit_id         UUID NOT NULL,
    permit_identifier         VARCHAR(80) NOT NULL,
    permit_type               VARCHAR(50) NOT NULL,
    contractor                VARCHAR(120) NOT NULL,
    issuer_user_id            UUID NOT NULL,
    valid_from                TIMESTAMP NOT NULL DEFAULT clock_timestamp(),
    valid_to                  TIMESTAMP NOT NULL,
    status                    VARCHAR(20) NOT NULL,

    CONSTRAINT uq_work_permits_permit_identifier UNIQUE (permit_identifier),
    CONSTRAINT ck_work_permits_permit_type CHECK (permit_type IN ('HOT_WORK', 'COLD_WORK', 'CONFINED_SPACE', 'ELECTRICAL', 'WORK_AT_HEIGHT', 'EXCAVATION', 'CHEMICAL')),
    CONSTRAINT ck_work_permits_status CHECK (status IN ('DRAFT', 'PENDING', 'APPROVED', 'EXPIRED', 'REVOKED', 'CLOSED')),
    CONSTRAINT pk_work_permits PRIMARY KEY (id)
);

-- ==========================================
-- SCHEMA: ADM
-- ==========================================

CREATE TABLE IF NOT EXISTS adm.audit_logs (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    user_id                   UUID,
    event_type                VARCHAR(80) NOT NULL,
    entity_type               VARCHAR(80) NOT NULL,
    entity_id                 UUID NOT NULL,
    timestamp                 TIMESTAMP NOT NULL DEFAULT clock_timestamp(),
    previous_state            JSONB,
    new_state                 JSONB,
    ip_address                VARCHAR(45),
    user_agent                VARCHAR(255),
    integrity_hash            VARCHAR(255) NOT NULL,

    CONSTRAINT pk_audit_logs PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS adm.auth_tokens (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    user_id                   UUID NOT NULL,
    token_hash                VARCHAR(255) NOT NULL,
    expires_at                TIMESTAMP NOT NULL,
    is_revoked                BOOLEAN NOT NULL DEFAULT FALSE,
    purpose                   VARCHAR(20) NOT NULL,

    CONSTRAINT uq_auth_tokens_token_hash UNIQUE (token_hash),
    -- CONSTRAINT ck_auth_tokens_purpose CHECK (...) /* Missing explicit enum for auth_tokens.purpose */,
    CONSTRAINT pk_auth_tokens PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS adm.role_permissions (
    role_id                   UUID NOT NULL,
    module                    VARCHAR(80) NOT NULL,
    action                    VARCHAR(80) NOT NULL,

    CONSTRAINT pk_role_permissions PRIMARY KEY (role_id, module, action)
);

CREATE TABLE IF NOT EXISTS adm.roles (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    name                      VARCHAR(80) NOT NULL,
    description               VARCHAR(255),

    CONSTRAINT uq_roles_name UNIQUE (name),
    CONSTRAINT pk_roles PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS adm.user_roles (
    user_id                   UUID NOT NULL,
    role_id                   UUID NOT NULL,

    CONSTRAINT pk_user_roles PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS adm.users (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    username                  VARCHAR(80) NOT NULL,
    email                     VARCHAR(120) NOT NULL,
    password_hash             VARCHAR(255) NOT NULL,
    full_name                 VARCHAR(150) NOT NULL,
    is_active                 BOOLEAN NOT NULL DEFAULT TRUE,
    failed_login_attempts     INT NOT NULL DEFAULT 0,
    lockout_until             TIMESTAMP,
    last_login_at             TIMESTAMP,

    CONSTRAINT uq_users_username UNIQUE (username),
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT pk_users PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS adm.work_order_assignments (
    work_order_id             UUID NOT NULL,
    user_id                   UUID NOT NULL,
    assigned_role             VARCHAR(80) NOT NULL,
    assigned_at               TIMESTAMP NOT NULL DEFAULT clock_timestamp(),

    -- CONSTRAINT ck_work_order_assignments_assigned_role CHECK (...) /* Missing explicit enum for work_order_assignments.assigned_role */,
    CONSTRAINT pk_work_order_assignments PRIMARY KEY (work_order_id, user_id)
);

CREATE TABLE IF NOT EXISTS adm.idempotency_logs (
    id                        UUID NOT NULL DEFAULT uuidv7(),
    idempotency_key           VARCHAR(128) NOT NULL,
    tenant_id                 UUID NOT NULL,
    request_hash              VARCHAR(64) NOT NULL,
    status                    VARCHAR(20) NOT NULL,
    created_at                TIMESTAMP NOT NULL DEFAULT clock_timestamp(),

    CONSTRAINT uq_idempotency_logs_idempotency_key UNIQUE (idempotency_key),
    CONSTRAINT pk_idempotency_logs PRIMARY KEY (id)
);

-- ==========================================
-- INDEXES (AUTO-GENERATED HEURISTICS)
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_equipment_units_functional_location_id ON tax.equipment_units (functional_location_id);
CREATE INDEX IF NOT EXISTS idx_equipment_units_equipment_class_id ON tax.equipment_units (equipment_class_id);
CREATE INDEX IF NOT EXISTS idx_equipment_units_warehouse_id ON tax.equipment_units (warehouse_id);
CREATE INDEX IF NOT EXISTS idx_functional_locations_parent_id ON tax.functional_locations (parent_id);
CREATE INDEX IF NOT EXISTS idx_maintainable_items_subunit_id ON tax.maintainable_items (subunit_id);
CREATE INDEX IF NOT EXISTS idx_maintainable_items_design_attributes ON tax.maintainable_items USING GIN (design_attributes jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_subunits_equipment_unit_id ON tax.subunits (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_asset_installations_functional_location_id ON tax.asset_installations (functional_location_id);
CREATE INDEX IF NOT EXISTS idx_asset_installations_equipment_unit_id ON tax.asset_installations (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_backlog_items_equipment_unit_id ON mtto.backlog_items (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_backlog_items_work_request_id ON mtto.backlog_items (work_request_id);
CREATE INDEX IF NOT EXISTS idx_failure_records_work_order_id ON mtto.failure_records (work_order_id);
CREATE INDEX IF NOT EXISTS idx_failure_records_maintainable_item_id ON mtto.failure_records (maintainable_item_id);
CREATE INDEX IF NOT EXISTS idx_maintenance_plans_equipment_unit_id ON mtto.maintenance_plans (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_media_attachments_work_order_id ON mtto.media_attachments (work_order_id);
CREATE INDEX IF NOT EXISTS idx_media_attachments_failure_record_id ON mtto.media_attachments (failure_record_id);
CREATE INDEX IF NOT EXISTS idx_work_order_histories_work_order_id ON mtto.work_order_histories (work_order_id);
CREATE INDEX IF NOT EXISTS idx_work_orders_equipment_unit_id ON mtto.work_orders (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_work_orders_maintenance_plan_id ON mtto.work_orders (maintenance_plan_id);
CREATE INDEX IF NOT EXISTS idx_work_orders_work_request_id ON mtto.work_orders (work_request_id);
CREATE INDEX IF NOT EXISTS idx_work_orders_work_permit_id ON mtto.work_orders (work_permit_id);
CREATE INDEX IF NOT EXISTS idx_work_requests_equipment_unit_id ON mtto.work_requests (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_spare_part_id ON inv.inventory_transactions (spare_part_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_warehouse_id ON inv.inventory_transactions (warehouse_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_work_order_id ON inv.inventory_transactions (work_order_id);
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_locator_id ON inv.inventory_transactions (locator_id);
CREATE INDEX IF NOT EXISTS idx_maintainable_item_spare_parts_maintainable_item_id ON inv.maintainable_item_spare_parts (maintainable_item_id);
CREATE INDEX IF NOT EXISTS idx_maintainable_item_spare_parts_spare_part_id ON inv.maintainable_item_spare_parts (spare_part_id);
CREATE INDEX IF NOT EXISTS idx_material_requirements_work_order_id ON inv.material_requirements (work_order_id);
CREATE INDEX IF NOT EXISTS idx_material_requirements_spare_part_id ON inv.material_requirements (spare_part_id);
CREATE INDEX IF NOT EXISTS idx_spare_parts_supplier_id ON inv.spare_parts (supplier_id);
CREATE INDEX IF NOT EXISTS idx_spare_parts_equipment_class_id ON inv.spare_parts (equipment_class_id);
CREATE INDEX IF NOT EXISTS idx_locators_warehouse_id ON inv.locators (warehouse_id);
CREATE INDEX IF NOT EXISTS idx_isolation_points_equipment_unit_id ON vis.isolation_points (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_mesh_mappings_equipment_unit_id ON vis.mesh_mappings (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_spatial_metadata_mesh_mapping_id ON vis.spatial_metadata (mesh_mapping_id);
CREATE INDEX IF NOT EXISTS idx_spatial_metadata_position ON vis.spatial_metadata USING GIN (position jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_spatial_metadata_rotation ON vis.spatial_metadata USING GIN (rotation jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_spatial_metadata_scale ON vis.spatial_metadata USING GIN (scale jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_telemetry_signals_equipment_unit_id ON vis.telemetry_signals (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_visual_layers_work_order_id ON vis.visual_layers (work_order_id);
CREATE INDEX IF NOT EXISTS idx_work_order_isolations_work_order_id ON vis.work_order_isolations (work_order_id);
CREATE INDEX IF NOT EXISTS idx_work_order_isolations_isolation_point_id ON vis.work_order_isolations (isolation_point_id);
CREATE INDEX IF NOT EXISTS idx_work_order_isolations_telemetry_snapshot ON vis.work_order_isolations USING GIN (telemetry_snapshot jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_work_permits_equipment_unit_id ON vis.work_permits (equipment_unit_id);
CREATE INDEX IF NOT EXISTS idx_work_permits_issuer_user_id ON vis.work_permits (issuer_user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON adm.audit_logs (user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_previous_state ON adm.audit_logs USING GIN (previous_state jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_audit_logs_new_state ON adm.audit_logs USING GIN (new_state jsonb_path_ops);
CREATE INDEX IF NOT EXISTS idx_auth_tokens_user_id ON adm.auth_tokens (user_id);
CREATE INDEX IF NOT EXISTS idx_role_permissions_role_id ON adm.role_permissions (role_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON adm.user_roles (user_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_role_id ON adm.user_roles (role_id);
CREATE INDEX IF NOT EXISTS idx_work_order_assignments_work_order_id ON adm.work_order_assignments (work_order_id);
CREATE INDEX IF NOT EXISTS idx_work_order_assignments_user_id ON adm.work_order_assignments (user_id);

-- ==========================================
-- FOREIGN KEY CONSTRAINTS (CROSS-SCHEMA)
-- ==========================================

ALTER TABLE tax.equipment_units
    ADD CONSTRAINT fk_equipment_units_functional_location FOREIGN KEY (functional_location_id) REFERENCES tax.functional_locations (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE tax.equipment_units
    ADD CONSTRAINT fk_equipment_units_equipment_class FOREIGN KEY (equipment_class_id) REFERENCES tax.equipment_classes (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE tax.equipment_units
    ADD CONSTRAINT fk_equipment_units_warehouse FOREIGN KEY (warehouse_id) REFERENCES inv.warehouses (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE tax.functional_locations
    ADD CONSTRAINT fk_functional_locations_parent FOREIGN KEY (parent_id) REFERENCES tax.functional_locations (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE tax.maintainable_items
    ADD CONSTRAINT fk_maintainable_items_subunit FOREIGN KEY (subunit_id) REFERENCES tax.subunits (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE tax.subunits
    ADD CONSTRAINT fk_subunits_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE tax.asset_installations
    ADD CONSTRAINT fk_asset_installations_functional_location FOREIGN KEY (functional_location_id) REFERENCES tax.functional_locations (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE tax.asset_installations
    ADD CONSTRAINT fk_asset_installations_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE mtto.backlog_items
    ADD CONSTRAINT fk_backlog_items_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE mtto.backlog_items
    ADD CONSTRAINT fk_backlog_items_work_request FOREIGN KEY (work_request_id) REFERENCES mtto.work_requests (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE mtto.failure_records
    ADD CONSTRAINT fk_failure_records_work_order FOREIGN KEY (work_order_id) REFERENCES mtto.work_orders (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE mtto.failure_records
    ADD CONSTRAINT fk_failure_records_maintainable_item FOREIGN KEY (maintainable_item_id) REFERENCES tax.maintainable_items (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE mtto.maintenance_plans
    ADD CONSTRAINT fk_maintenance_plans_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE mtto.media_attachments
    ADD CONSTRAINT fk_media_attachments_work_order FOREIGN KEY (work_order_id) REFERENCES mtto.work_orders (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE mtto.media_attachments
    ADD CONSTRAINT fk_media_attachments_failure_record FOREIGN KEY (failure_record_id) REFERENCES mtto.failure_records (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE mtto.work_order_histories
    ADD CONSTRAINT fk_work_order_histories_work_order FOREIGN KEY (work_order_id) REFERENCES mtto.work_orders (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE mtto.work_orders
    ADD CONSTRAINT fk_work_orders_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE mtto.work_orders
    ADD CONSTRAINT fk_work_orders_maintenance_plan FOREIGN KEY (maintenance_plan_id) REFERENCES mtto.maintenance_plans (id)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE mtto.work_orders
    ADD CONSTRAINT fk_work_orders_work_request FOREIGN KEY (work_request_id) REFERENCES mtto.work_requests (id)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE mtto.work_orders
    ADD CONSTRAINT fk_work_orders_work_permit FOREIGN KEY (work_permit_id) REFERENCES vis.work_permits (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE mtto.work_requests
    ADD CONSTRAINT fk_work_requests_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE inv.inventory_transactions
    ADD CONSTRAINT fk_inventory_transactions_spare_part FOREIGN KEY (spare_part_id) REFERENCES inv.spare_parts (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE inv.inventory_transactions
    ADD CONSTRAINT fk_inventory_transactions_warehouse FOREIGN KEY (warehouse_id) REFERENCES inv.warehouses (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE inv.inventory_transactions
    ADD CONSTRAINT fk_inventory_transactions_work_order FOREIGN KEY (work_order_id) REFERENCES mtto.work_orders (id)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE inv.inventory_transactions
    ADD CONSTRAINT fk_inventory_transactions_locator FOREIGN KEY (locator_id) REFERENCES inv.locators (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE inv.maintainable_item_spare_parts
    ADD CONSTRAINT fk_maintainable_item_spare_parts_maintainable_item FOREIGN KEY (maintainable_item_id) REFERENCES tax.maintainable_items (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE inv.maintainable_item_spare_parts
    ADD CONSTRAINT fk_maintainable_item_spare_parts_spare_part FOREIGN KEY (spare_part_id) REFERENCES inv.spare_parts (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE inv.material_requirements
    ADD CONSTRAINT fk_material_requirements_work_order FOREIGN KEY (work_order_id) REFERENCES mtto.work_orders (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE inv.material_requirements
    ADD CONSTRAINT fk_material_requirements_spare_part FOREIGN KEY (spare_part_id) REFERENCES inv.spare_parts (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE inv.spare_parts
    ADD CONSTRAINT fk_spare_parts_supplier FOREIGN KEY (supplier_id) REFERENCES inv.suppliers (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE inv.spare_parts
    ADD CONSTRAINT fk_spare_parts_equipment_class FOREIGN KEY (equipment_class_id) REFERENCES tax.equipment_classes (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE inv.locators
    ADD CONSTRAINT fk_locators_warehouse FOREIGN KEY (warehouse_id) REFERENCES inv.warehouses (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vis.isolation_points
    ADD CONSTRAINT fk_isolation_points_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE vis.mesh_mappings
    ADD CONSTRAINT fk_mesh_mappings_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vis.spatial_metadata
    ADD CONSTRAINT fk_spatial_metadata_mesh_mapping FOREIGN KEY (mesh_mapping_id) REFERENCES vis.mesh_mappings (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vis.telemetry_signals
    ADD CONSTRAINT fk_telemetry_signals_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vis.visual_layers
    ADD CONSTRAINT fk_visual_layers_work_order FOREIGN KEY (work_order_id) REFERENCES mtto.work_orders (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vis.work_order_isolations
    ADD CONSTRAINT fk_work_order_isolations_work_order FOREIGN KEY (work_order_id) REFERENCES mtto.work_orders (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE vis.work_order_isolations
    ADD CONSTRAINT fk_work_order_isolations_isolation_point FOREIGN KEY (isolation_point_id) REFERENCES vis.isolation_points (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE vis.work_permits
    ADD CONSTRAINT fk_work_permits_equipment_unit FOREIGN KEY (equipment_unit_id) REFERENCES tax.equipment_units (id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE adm.audit_logs
    ADD CONSTRAINT fk_audit_logs_user FOREIGN KEY (user_id) REFERENCES adm.users (id)
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE adm.auth_tokens
    ADD CONSTRAINT fk_auth_tokens_user FOREIGN KEY (user_id) REFERENCES adm.users (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE adm.role_permissions
    ADD CONSTRAINT fk_role_permissions_role FOREIGN KEY (role_id) REFERENCES adm.roles (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE adm.user_roles
    ADD CONSTRAINT fk_user_roles_user FOREIGN KEY (user_id) REFERENCES adm.users (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE adm.user_roles
    ADD CONSTRAINT fk_user_roles_role FOREIGN KEY (role_id) REFERENCES adm.roles (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE adm.work_order_assignments
    ADD CONSTRAINT fk_work_order_assignments_work_order FOREIGN KEY (work_order_id) REFERENCES mtto.work_orders (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE adm.work_order_assignments
    ADD CONSTRAINT fk_work_order_assignments_user FOREIGN KEY (user_id) REFERENCES adm.users (id)
    ON DELETE CASCADE ON UPDATE CASCADE;

