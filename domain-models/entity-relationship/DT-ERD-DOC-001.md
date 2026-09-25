---
code: DT-ERD-DOC-001
version: 1.1
date: 2026-09-18
status: Active
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
	
# Physical Relational and Data Dictionary

## 1. Scope and Purpose

This document acts as the official Data Dictionary and physical relational mapping specification for PostgreSQL 18, complementing the Entity-Relationship diagram (DT-ERD-LOG-001). It strictly defines schemas, table names, physical columns, and native data types.

## 2. Conventions and Schema Structure

All tables and columns follow the `snake_case` naming standard. The database is organized into 5 design-driven (DDD) schemas to isolate contexts:

- `tax`: Taxonomy and assets according to ISO 14224.
- `mtto`: Maintenance and reliability management.
- `inv`: Resource and supply control.
- `vis`: Digital twin and operational safety layers.
- `adm`: Perimeter security, IAM, and immutable audit.

## 3. Physical Data Dictionary by Schema

### 3.1 Schema `tax`

#### 3.1.1 equipment_classes

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| class_name | VARCHAR(120) | NOT NULL | UNIQUE | - | Master data at the class level. |
| description | VARCHAR(255) | NULL | | NULL | Class description. |
| manufacturer_standard | VARCHAR(120) | NULL | | NULL | Standardization reference. |

#### 3.1.2 equipment_units

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| serial_number | VARCHAR(100) | NOT NULL | UNIQUE | - | Asset identification integrity. |
| manufacturer | VARCHAR(120) | NOT NULL | | - | Asset provenance. |
| model | VARCHAR(120) | NOT NULL | | - | Asset type identification. |
| purchase_date | DATE | NOT NULL | | - | Procurement chronology. |
| rejection_reason | VARCHAR(255) | NULL | | NULL | Only present when commissioning is rejected. |
| boundary_start | VARCHAR(150) | NOT NULL | | - | Starting point of the boundary definition. |
| boundary_end | VARCHAR(150) | NOT NULL | | - | Ending point of the boundary definition. |
| acquisition_date | DATE | NOT NULL | | - | Asset acquisition traceability. |
| installation_date | DATE | NULL | | NULL | Installation may be pending. |
| operation_start_date | DATE | NULL | | NULL | Operational start may be pending. |
| operating_hours | BIGINT | NOT NULL | | 0 | Reliability and usage tracking. |
| surveillance_hours | BIGINT | NOT NULL | | 0 | Surveillance/standby time for accurate failure calculation (ISO 14224). |
| disposal_date | DATE | NULL | | NULL | End-of-life record for liability traceability (ISO 55000). |
| disposal_reason | VARCHAR(255) | NULL | | NULL | Reason for asset retirement or decommissioning. |
| operational_status | VARCHAR(20) | NOT NULL | CHECK | - | Controlled operational status vocabulary. |
| lifecycle_status | VARCHAR(20) | NOT NULL | CHECK | - | Controlled lifecycle vocabulary. |
| maintenance_status | VARCHAR(30) | NOT NULL | CHECK | - | Controlled maintenance status vocabulary. |
| health_status | VARCHAR(30) | NULL | CHECK | NULL | Controlled overall health status vocabulary (ISO 13374-4). |
| is_sce | BOOLEAN | NOT NULL | | FALSE | Safety Critical Element indicator. |
| functional_location_id | UUID | NULL | FK, UNIQUE | NULL | Foreign key to the related table. |
| equipment_class_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| warehouse_id | UUID | NULL | FK | NULL | Foreign key to the related table. |

#### 3.1.3 functional_locations

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| tag_number | VARCHAR(50) | NOT NULL | UNIQUE | - | ISO 14224 tag identity and location traceability. |
| name | VARCHAR(150) | NOT NULL | | - | Human-readable location name. |
| description | VARCHAR(255) | NULL | | NULL | Optional explanatory text. |
| criticality | VARCHAR(30) | NOT NULL | | - | Controlled priority vocabulary. |
| geographic_location | VARCHAR(150) | NULL | | NULL | Physical context of the location. |
| environmental_exposure | VARCHAR(150) | NULL | CHECK | NULL | Environmental conditions for reliability calculations (ISO 14224). |
| hierarchy_level | SMALLINT | NOT NULL | | - | Levels 1 to 5 of the ISO 14224 taxonomy (Functional Locations govern the plant's spatial structure down to the process, while L6 to L8 correspond to physical equipment and components). |
| parent_id | UUID | NULL | FK | NULL | Foreign key to the related table. |

#### 3.1.4 maintainable_items

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| subunit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| component_name | VARCHAR(120) | NOT NULL | | - | Identity of the maintainable item. |
| subunit_type | VARCHAR(80) | NOT NULL | | - | Taxonomic classification. |
| spare_part_type | VARCHAR(80) | NULL | | NULL | Optional spare parts correspondence. |
| design_attributes | JSONB | NULL | | NULL | Structured static design properties (ISO 14224 Annex A). |
| status | VARCHAR(30) | NOT NULL | CHECK | - | Item's lifecycle status. |

#### 3.1.5 subunits

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| subunit_type | VARCHAR(80) | NOT NULL | | - | Subcomponent taxonomy. |
| name | VARCHAR(120) | NOT NULL | | - | Subcomponent label. |

### 3.2 Schema `mtto`

#### 3.2.1 backlog_items

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| work_request_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| priority_score | INT | NOT NULL | | - | Backlog score derived from RIME (Calculated). |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Backlog lifecycle status (prioritization). |

#### 3.2.2 failure_records

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Identity of the failure event. |
| work_order_id | UUID | NOT NULL | FK, UNIQUE | - | Foreign key to the related table. |
| maintainable_item_id | UUID | NULL | FK | NULL | Foreign key to the related table. |
| failure_mode | VARCHAR(120) | NOT NULL | | - | ISO 14224 failure coding. |
| failure_mechanism | VARCHAR(120) | NOT NULL | | - | ISO 14224 failure coding. |
| failure_cause | VARCHAR(120) | NOT NULL | | - | ISO 14224 failure coding. |
| detection_method | VARCHAR(120) | NOT NULL | CHECK | - | Failure detection method (ISO 14224). |
| operational_condition | VARCHAR(120) | NOT NULL | CHECK | - | Operational condition at the time of failure (ISO 14224). |
| operational_impact | VARCHAR(120) | NOT NULL | CHECK | - | Operational impact of the failure (ISO 14224). |
| technician_notes | TEXT | NULL | | NULL | Qualitative field diagnosis and observations from the technician. |
| downtime | DECIMAL(10,2) | NOT NULL | | - | Reliability analysis metric (Calculated). |
| status | VARCHAR(20) | NOT NULL | | - | Status of the failure record. |

#### 3.2.3 maintenance_plans

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| maintenance_method | VARCHAR(80) | NOT NULL | CHECK | - | Maintenance strategy (PM, PdM, CBM). |
| frequency | VARCHAR(50) | NOT NULL | | - | Human-readable frequency description. |
| frequency_type | VARCHAR(20) | NOT NULL | CHECK | - | Controlled cadence of the plan. |
| next_work_order_date | DATE | NULL | | NULL | Scheduled execution date (Calculated). |
| interval_value | DECIMAL(12,2) | NULL | | NULL | Numeric value of the interval for telemetry (e.g., 500 hours). |
| next_trigger_limit | DECIMAL(12,2) | NULL | | NULL | Accumulated limit calculated for the next trigger. |
| estimated_labor_hours | DECIMAL(10,2) | NOT NULL | | - | Estimated Man-Hours (Wrench Time) for planning. |
| required_specialty | VARCHAR(80) | NOT NULL | CHECK | - | Required technical specialty (e.g., Mechanical, Electrical). |
| technical_description | VARCHAR(255) | NOT NULL | | - | Technical description of the task scope. |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Plan (document) lifecycle status. |

#### 3.2.4 media_attachments

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| work_order_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| file_url | VARCHAR(255) | NOT NULL | | - | Evidence location. |
| file_type | VARCHAR(20) | NOT NULL | CHECK | - | Controlled attachment file format. |
| uploaded_at | TIMESTAMP | NOT NULL | | - | Upload/ingestion time of the evidence. |

#### 3.2.5 work_order_histories

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| work_order_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| old_status | VARCHAR(20) | NULL | | NULL | Previous lifecycle status (NULL if first status). |
| new_status | VARCHAR(20) | NOT NULL | | - | New lifecycle status. |
| timestamp | TIMESTAMP | NOT NULL | | clock_timestamp() | Transition time. |
| duration_seconds | BIGINT | NULL | | NULL | Time spent in the state (Calculated upon transition). |

#### 3.2.6 work_orders

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| maintenance_plan_id | UUID | NULL | FK | NULL | Foreign key to the related table. |
| work_request_id | UUID | NULL | FK | NULL | Foreign key to the related table. |
| work_permit_id | UUID | NULL | FK | NULL | Foreign key to the related table. |
| current_status | VARCHAR(20) | NOT NULL | CHECK | - | Execution lifecycle status (FSM). |
| maintenance_method | VARCHAR(80) | NOT NULL | CHECK | - | Maintenance method (Corrective, Preventive, etc.). |
| creation_date | TIMESTAMP | NOT NULL | | - | Timestamp of order creation. |
| scheduled_date | TIMESTAMP | NULL | | NULL | Planned start. |
| actual_start | TIMESTAMP | NULL | | NULL | Actual execution start. |
| actual_finish | TIMESTAMP | NULL | | NULL | Actual execution finish. |
| actual_labor_hours | DECIMAL(10,2) | NULL | | NULL | Actual labor duration (Calculated). |
| criticality | VARCHAR(20) | NOT NULL | CHECK | - | WO criticality / priority label. |

#### 3.2.7 work_requests

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| description | VARCHAR(255) | NOT NULL | | - | Request narrative. |
| priority | VARCHAR(20) | NOT NULL | | - | Request priority label. |
| request_date | TIMESTAMP | NOT NULL | | - | Timeline for audit. |
| request_source | VARCHAR(80) | NOT NULL | | - | Origin of the request. |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Request lifecycle status. |
| work_class | SMALLINT | NOT NULL | CHECK | - | Numeric weight of the selected work class for RIME. |

### 3.3 Schema `inv`

#### 3.3.1 inventory_transactions

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| spare_part_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| warehouse_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| work_order_id | UUID | NULL | FK | NULL | Foreign key to the related table. |
| quantity | DECIMAL(12,4) | NOT NULL | | 1 | Transacted quantity (positive for receipts, negative for issues). |
| transaction_type | VARCHAR(20) | NOT NULL | CHECK | - | Movement type (RECEIPT, ISSUE, ADJUSTMENT). |
| timestamp | TIMESTAMP | NOT NULL | | clock_timestamp() | Precise temporal record of the movement. |
| reason | VARCHAR(255) | NOT NULL | | - | Reason for movement or reference to external documents. |
| total_cost | DECIMAL(12,2) | NOT NULL | | - | Total cost of the transaction (Quantity \* Cost). |
| aisle_shelf_location | VARCHAR(150) | NULL | | NULL | Specific physical location of the transaction (aisle/shelf). |
| serial_number | VARCHAR(100) | NULL | | NULL | Serial number or Tag of the rotating equipment (Asset Swap). |

#### 3.3.2 maintainable_item_spare_parts

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| maintainable_item_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| spare_part_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |

#### 3.3.3 material_requirements

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| work_order_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| spare_part_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| planned_quantity | DECIMAL(12,4) | NOT NULL | | 1 | Planned spare parts before WO execution. |
| actual_quantity | DECIMAL(12,4) | NULL | | NULL | Spare parts actually consumed during WO execution. |
| is_reserved | BOOLEAN | NOT NULL | | - | Flag indicating if stock was already set aside in warehouse. |

#### 3.3.4 spare_parts

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| sku | VARCHAR(80) | NOT NULL | UNIQUE | - | Part identity. |
| description | VARCHAR(255) | NOT NULL | | - | Human-readable part description. |
| manufacturer | VARCHAR(120) | NOT NULL | | - | Supplier/manufacturer identity. |
| commodity_code | VARCHAR(80) | NULL | | NULL | Classification code. |
| reorder_point | DECIMAL(12,4) | NOT NULL | | - | Minimum purchase activation threshold. |
| unit_of_measure | VARCHAR(20) | NOT NULL | | - | Standard Unit of Measure (UoM). |
| stock_policy | VARCHAR(20) | NOT NULL | CHECK | - | Replenishment policy (Min/Max, Reorder Point, JIT). |
| is_rebuildable | BOOLEAN | NOT NULL | | FALSE | Indicates whether the part is discarded or sent to the workshop for repair. |
| quantity_on_hand | DECIMAL(12,4) | NOT NULL | | - | Quantity currently in physical inventory. |
| reserved_quantity | DECIMAL(12,4) | NOT NULL | | - | Committed stock for planned orders. |
| max_capacity | DECIMAL(12,4) | NOT NULL | | - | Physical warehouse limit for the part. |
| unit_cost | DECIMAL(12,2) | NOT NULL | | - | Standard unit acquisition cost. |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Spare part availability status. |
| supplier_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| equipment_class_id | UUID | NULL | FK | NULL | Foreign key to the related table. |

#### 3.3.5 suppliers

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| name | VARCHAR(120) | NOT NULL | | - | Supplier commercial identity. |
| contact_info | VARCHAR(255) | NOT NULL | | - | Phone, email, or contact address. |
| warranty_terms | VARCHAR(255) | NOT NULL | | - | Standard commercial warranty terms. |

#### 3.3.6 warehouses

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| name | VARCHAR(80) | NOT NULL | | - | Warehouse identity. |
| location | VARCHAR(255) | NOT NULL | | - | Warehouse address or physical location. |
| capacity | DECIMAL(12,4) | NOT NULL | | - | Maximum volumetric or load capacity of the warehouse. |

### 3.4 Schema `vis`

#### 3.4.1 isolation_points

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| isolation_tag | VARCHAR(80) | NOT NULL | UNIQUE | - | Identity of the isolation point. |
| isolation_type | VARCHAR(20) | NOT NULL | CHECK | - | Isolation vocabulary. |
| is_verified | BOOLEAN | NOT NULL | | FALSE | Verification status. |

#### 3.4.2 mesh_mappings

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK, UNIQUE | - | Foreign key to the related table. |
| mesh_uuid | VARCHAR(80) | NOT NULL | UNIQUE | - | Identity or path of the asset's 3D model. |
| mapping_status | VARCHAR(20) | NOT NULL | CHECK | - | Digital twin mapping status. |
| last_sync_time | TIMESTAMP | NULL | | NULL | Last synchronization time. |

#### 3.4.3 spatial_metadata

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| mesh_mapping_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| position | JSONB | NOT NULL | | - | Spatial vector coordinate (e.g., x,y,z). |
| rotation | JSONB | NULL | | NULL | Orientation descriptor (e.g., quaternion). |
| scale | JSONB | NULL | | NULL | Scale descriptor. |

#### 3.4.4 telemetry_signals

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| signal_type | VARCHAR(80) | NOT NULL | CHECK | - | Sensor signal label. |
| value | DECIMAL(18,6) | NOT NULL | | - | Raw measurement value. |
| unit | VARCHAR(20) | NOT NULL | | - | Measurement unit. |
| threshold | DECIMAL(18,6) | NULL | | NULL | Alert threshold. |
| timestamp | TIMESTAMP | NOT NULL | | clock_timestamp() | Measurement time. |
| is_safety_critical | BOOLEAN | NOT NULL | | - | Safety classification flag. |

#### 3.4.5 visual_layers

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| work_order_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| layer_type | VARCHAR(80) | NOT NULL | | - | Visual representation type. |
| opacity_level | DECIMAL(5,2) | NOT NULL | | - | Rendering control. |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Visual layer status. |

#### 3.4.6 work_order_isolations

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| work_order_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| isolation_point_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| is_isolated | BOOLEAN | NOT NULL | | FALSE | Verified lockout state for the specific work. |
| isolated_at | TIMESTAMP | NULL | | NULL | Timestamp when the lockout was executed. |
| padlock_tag_id | VARCHAR(80) | NULL | | NULL | Identifier of the physical padlock or tag (Try-Out). |

#### 3.4.7 work_permits

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| permit_identifier | VARCHAR(80) | NOT NULL | UNIQUE | - | Permit traceability. |
| valid_from | TIMESTAMP | NOT NULL | | clock_timestamp() | Timeline start. |
| valid_to | TIMESTAMP | NOT NULL | | - | Timeline end. |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Permit status (Active, Revoked, Expired). |

### 3.5 Schema `adm`

#### 3.5.1 audit_logs

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| user_id | UUID | NULL | FK | NULL | Foreign key to the related table. |
| event_type | VARCHAR(80) | NOT NULL | | - | Action executed (e.g., CREATE, UPDATE, DELETE). |
| entity_type | VARCHAR(80) | NOT NULL | | - | Affected table or domain entity. |
| entity_id | UUID | NOT NULL | | - | Identifier of the affected record. |
| timestamp | TIMESTAMP | NOT NULL | | clock_timestamp() | Exact moment of the mutation. |
| previous_state | JSONB | NULL | | NULL | Snapshot of the data before the change. |
| new_state | JSONB | NULL | | NULL | Snapshot of the data after the change. |
| ip_address | VARCHAR(45) | NULL | | NULL | Network traceability (IPv4 or IPv6). |
| user_agent | VARCHAR(255) | NULL | | NULL | Client traceability. |
| integrity_hash | VARCHAR(255) | NOT NULL | | - | Cryptographic hash for immutability verification. |

#### 3.5.2 auth_tokens

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| user_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| token_hash | VARCHAR(255) | NOT NULL | UNIQUE | - | Cryptographic representation of the token. |
| expires_at | TIMESTAMP | NOT NULL | | - | Temporal validity limit. |
| is_revoked | BOOLEAN | NOT NULL | | FALSE | Pre-expiration manual revocation flag. |
| purpose | VARCHAR(20) | NOT NULL | CHECK | - | Context of use (e.g., ACCESS, REFRESH, RESET). |

#### 3.5.3 role_permissions

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| role_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| module | VARCHAR(80) | NOT NULL | PK | - | Application subdomain or module. |
| action | VARCHAR(80) | NOT NULL | PK | - | Granted behavior (e.g., READ, WRITE, APPROVE). |

#### 3.5.4 roles

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| name | VARCHAR(80) | NOT NULL | UNIQUE | - | Human-readable role identity. |
| description | VARCHAR(255) | NULL | | NULL | Description of the RBAC role. |

#### 3.5.5 user_roles

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| user_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| role_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |

#### 3.5.6 users

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| username | VARCHAR(80) | NOT NULL | UNIQUE | - | Access identity. |
| email | VARCHAR(120) | NOT NULL | UNIQUE | - | Communication identity. |
| password_hash | VARCHAR(255) | NOT NULL | | - | Secure credential. |
| full_name | VARCHAR(150) | NOT NULL | | - | Real identity. |
| is_active | BOOLEAN | NOT NULL | | TRUE | Access control flag. |
| failed_login_attempts | INT | NOT NULL | | 0 | Brute force defense counter. |
| lockout_until | TIMESTAMP | NULL | | NULL | Temporary block time window. |
| last_login_at | TIMESTAMP | NULL | | NULL | Activity traceability. |

#### 3.5.7 work_order_assignments

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| work_order_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| user_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| assigned_role | VARCHAR(80) | NOT NULL | CHECK | - | Operational role of the technician in the specific WO. |
| assigned_at | TIMESTAMP | NOT NULL | | clock_timestamp() | Moment of assignment. |

#### 3.5.8 idempotency_logs

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| idempotency_key | VARCHAR(128) | NOT NULL | UNIQUE | - | Client-provided uniqueness token (ADR-007). |
| tenant_id | UUID | NOT NULL | | - | Multi-tenant isolation boundary. |
| request_hash | VARCHAR(64) | NOT NULL | | - | SHA-256 fingerprint to prevent payload mutation. |
| status | VARCHAR(20) | NOT NULL | | - | State of the transaction (e.g., COMPLETED). |
| created_at | TIMESTAMP | NOT NULL | | clock_timestamp() | Partitioning key for MVCC cleanup. |

## 4. Referential Relationships and Cascading (FKs)

| Parent Table | Cardinality | Child Table | Verb / Meaning | ON DELETE | ON UPDATE |
| :--- | :--- | :--- | :--- | :--- | :--- |
| equipment_classes | 1 : 0..N | equipment_units | classifies | RESTRICT | CASCADE |
| functional_locations| 1 : 0..N | functional_locations | contains (Self) | RESTRICT | CASCADE |
| functional_locations| 1 : 0..N | equipment_units | installs | RESTRICT | CASCADE |
| equipment_units | 1 : 0..N | subunits | broken down into | CASCADE | CASCADE |
| subunits | 1 : 0..N | maintainable_items | built by | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | maintenance_plans | governed by | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | work_orders | generates | CASCADE | CASCADE |
| maintenance_plans | 1 : 0..N | work_orders | instantiates | SET NULL | CASCADE |
| work_requests | 1 : 0..N | work_orders | originates | SET NULL | CASCADE |
| equipment_units | 1 : 0..N | work_requests | requires | CASCADE | CASCADE |
| work_requests | 1 : 0..N | backlog_items | prioritized as | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | backlog_items | pending for | CASCADE | CASCADE |
| work_orders | 1 : 0..1 | failure_records | diagnoses | CASCADE | CASCADE |
| maintainable_items | 1 : 0..N | failure_records | affected by | SET NULL | CASCADE |
| work_orders | 1 : 0..N | media_attachments | evidenced by | CASCADE | CASCADE |
| work_orders | 1 : 0..N | work_order_histories| audited via | CASCADE | CASCADE |
| warehouses | 1 : 0..N | inventory_transactions| transacts | RESTRICT | CASCADE |
| spare_parts | 1 : 0..N | inventory_transactions| moves | RESTRICT | CASCADE |
| work_orders | 1 : 0..N | inventory_transactions| consumes | SET NULL | CASCADE |
| maintainable_items | 1 : 0..N | maintainable_item_spare_parts | repaired with | CASCADE | CASCADE |
| spare_parts | 1 : 0..N | maintainable_item_spare_parts | replaces | CASCADE | CASCADE |
| work_orders | 1 : 0..N | material_requirements | plans | CASCADE | CASCADE |
| spare_parts | 1 : 0..N | material_requirements | fulfills | CASCADE | CASCADE |
| suppliers | 1 : 0..N | spare_parts | supplies | RESTRICT | CASCADE |
| equipment_classes | 1 : 0..N | spare_parts | compatible with | RESTRICT | CASCADE |
| equipment_units | 1 : 0..1 | mesh_mappings | visualized as | CASCADE | CASCADE |
| mesh_mappings | 1 : 0..N | spatial_metadata | located via | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | telemetry_signals | monitored by | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | isolation_points | contains | RESTRICT | CASCADE |
| work_permits | 1 : 0..N | work_orders | validates execution of | RESTRICT | CASCADE |
| work_orders | 1 : 0..N | visual_layers | visualized in | CASCADE | CASCADE |
| work_orders | 1 : 1..N | work_order_isolations | requires | CASCADE | CASCADE |
| isolation_points | 1 : 1..N | work_order_isolations | locked by | RESTRICT | CASCADE |
| users | 1 : 1..N | user_roles | associated to | CASCADE | CASCADE |
| roles | 1 : 1..N | user_roles | granted to | CASCADE | CASCADE |
| roles | 1 : 0..N | role_permissions | contains | CASCADE | CASCADE |
| users | 1 : 0..N | auth_tokens | authenticated with | CASCADE | CASCADE |
| users | 1 : 0..N | work_order_assignments| assigned to | CASCADE | CASCADE |
| work_orders | 1 : 0..N | work_order_assignments| assigns personnel | CASCADE | CASCADE |
| users | 1 : 0..N | audit_logs | generates | SET NULL | CASCADE |

## 5. Data Type Correspondence Matrix (Standard SQL vs. PostgreSQL)

To guarantee the physical viability of the logical model and its correct implementation in the selected database engine (**PostgreSQL**), each proposed physical data type has been formally validated and mapped:

| Physical Type (SQL Standard) | Native Type in PostgreSQL | Alternative Technical Equivalent | Technical Impact / Justification in PostgreSQL |
| :--- | :--- | :--- | :--- |
| VARCHAR(N) | VARCHAR(N) or CHARACTER VARYING(N) | TEXT | PostgreSQL handles variable-length strings efficiently. TEXT has no performance penalty and is preferred when a strict character length limit is not required. |
| SMALLINT | SMALLINT or INT2 | None | 2-byte signed integer (range -32,768 to 32,767). Optimal for cardinalities and taxonomic levels (like hierarchyLevel). |
| INT | INTEGER or INT4 | None | 4-byte signed integer (range -2,147,483,648 to 2,147,483,647). Standard for simple counters (like failedLoginAttempts). |
| BIGINT | BIGINT or INT8 | None | 8-byte signed integer. Used for large accumulated metrics like operational hours (operatingHours) and transition durations. |
| DATE | DATE | None | 4-byte data type for storing calendar dates without time zone (year, month, day). |
| TIMESTAMP | TIMESTAMP | TIMESTAMPTZ | TIMESTAMP stores date and time without time zone. TIMESTAMPTZ (Timestamp with time zone) is recommended for audit logs, creation marks, and work order starts to avoid discrepancies due to time zones. |
| DECIMAL(P,S) | DECIMAL(P,S) or NUMERIC(P,S) | None | Exact precision type with user scale. Essential for monetary values (unitCost), sensor dimensions (value, threshold), and exact percentages (opacityLevel). |
| UUID | UUID | None | Native 128-bit data type. In PostgreSQL 18, the native function uuidv7() will be used as the default value for primary keys. Unlike UUIDv4 (random), UUIDv7 includes a 48-bit chronologically ordered time prefix, which prevents page fragmentation in B-Tree indexes and maximizes insertion performance in time series and audit logs. |
| BOOLEAN | BOOLEAN or BOOL | None | Logical type that stores TRUE or FALSE. |
| JSON | JSON | JSONB | JSON stores the literal text, which requires parsing on each query. It is recommended to use JSONB (Binary Decomposed JSON) because it stores the content in binary format, supports fast indexing (GIN indexes), and is much more efficient for audit queries (previousState and newState). |
