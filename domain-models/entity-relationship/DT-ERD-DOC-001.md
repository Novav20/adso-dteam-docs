---
code: DT-ERD-DOC-001
version: 1.6
date: 2026-11-13
status: Approved
author: Juan David Julio
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

**Optimistic Concurrency Standard (PostgreSQL `xmin`):** Physical tables do **not** declare synthetic `row_version` columns. Instead, all mutable aggregate roots leverage PostgreSQL 18's native `xmin` system column mapped in Entity Framework Core via `.Property<uint>("ConcurrencyToken").IsRowVersion()` and serialized as HTTP `ETag` / `If-Match` headers ([DT-ARQ-DB-DOC-001 §3.12](../../architecture/DT-ARQ-DB-DOC-001.md#312-optimistic-concurrency-control-via-postgresql-xmin-system-column)).

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
| boundary_start | VARCHAR(150) | NULL | | NULL | Starting point of the boundary definition (validated as required at `Activate()` / `DefineBoundaries()`). |
| boundary_end | VARCHAR(150) | NULL | | NULL | Ending point of the boundary definition (validated as required at `Activate()` / `DefineBoundaries()`). |
| acquisition_date | DATE | NOT NULL | | - | Asset acquisition traceability. |
| installation_date | DATE | NULL | | NULL | Installation may be pending. |
| operation_start_date | DATE | NULL | | NULL | Operational start may be pending. |
| operating_hours | DECIMAL(12,2) | NOT NULL | | 0 | Reliability and usage tracking. |
| surveillance_hours | DECIMAL(12,2) | NOT NULL | | 0 | Surveillance/standby time for accurate failure calculation (ISO 14224). |
| disposal_date | DATE | NULL | | NULL | End-of-life record for liability traceability (ISO 55000). |
| disposal_reason | VARCHAR(255) | NULL | | NULL | Reason for asset retirement or decommissioning. |
| operational_status | VARCHAR(20) | NOT NULL | CHECK | - | Controlled operational status vocabulary. |
| lifecycle_status | VARCHAR(20) | NOT NULL | CHECK | - | Controlled lifecycle vocabulary. |
| maintenance_status | VARCHAR(30) | NOT NULL | CHECK | - | Controlled maintenance status vocabulary. |
| health_status | VARCHAR(30) | NOT NULL | CHECK | 'UNDETERMINED' | Controlled overall health status vocabulary (ISO 13374-4). |
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
| criticality | SMALLINT | NULL | CHECK | NULL | Numeric asset criticality index (1..10) for RIME; NULL triggers AF-002 fail-safe floor (75). |
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
| design_attributes | JSONB | NULL | | NULL | Structured static design properties per ISO 14224 Annex A ([§6.1](#61-taxmaintainable_itemsdesign_attributes)). |
| status | VARCHAR(30) | NOT NULL | CHECK | - | Item's lifecycle status. |

#### 3.1.5 subunits

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| subunit_type | VARCHAR(80) | NOT NULL | | - | Subcomponent taxonomy. |
| name | VARCHAR(120) | NOT NULL | | - | Subcomponent label. |

#### 3.1.6 asset_installations

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the installation record. |
| functional_location_id | UUID | NOT NULL | FK | - | The physical position (slot) where the asset is installed. |
| equipment_unit_id | UUID | NOT NULL | FK | - | The specific serialized asset installed. |
| installed_at | TIMESTAMPTZ | NOT NULL | | now() | UTC timestamp of physical installation. |
| removed_at | TIMESTAMPTZ | NULL | | NULL | UTC timestamp of physical removal. Partial unique indexes WHERE removed_at IS NULL enforce 1:1 active occupancy. |

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
| work_order_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| maintainable_item_id | UUID | NOT NULL | FK | - | Foreign key to the related table (mandatory ISO 14224 Level 8 failure target). |
| failure_mode | VARCHAR(120) | NOT NULL | | - | ISO 14224 failure coding. |
| failure_mechanism | VARCHAR(120) | NOT NULL | | - | ISO 14224 failure coding. |
| failure_cause | VARCHAR(120) | NOT NULL | | - | ISO 14224 failure coding. |
| detection_method | VARCHAR(120) | NOT NULL | CHECK | - | Failure detection method (ISO 14224). |
| operational_condition | VARCHAR(120) | NOT NULL | CHECK | - | Operational condition at the time of failure (ISO 14224). |
| operational_impact | VARCHAR(120) | NOT NULL | CHECK | - | Operational impact of the failure (ISO 14224). |
| technician_notes | TEXT | NULL | | NULL | Qualitative field diagnosis and observations from the technician. |
| downtime | DECIMAL(10,2) | NOT NULL | | - | Reliability analysis metric (Calculated). |
| status | VARCHAR(20) | NOT NULL | CHECK | 'REPORTED' | Controlled lifecycle status of the failure record. |

#### 3.2.3 maintenance_plans

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the target Level 6 Equipment Unit. |
| subunit_id | UUID | NULL | FK | NULL | Optional ISO 14224 Level 7 Subunit target (MTTO-001, MTTO-023). |
| maintainable_item_id | UUID | NULL | FK | NULL | Optional ISO 14224 Level 8 Maintainable Item target (MTTO-001, MTTO-023). |
| maintenance_method | VARCHAR(80) | NOT NULL | CHECK | - | Maintenance strategy (PM, PdM, CBM). |
| frequency | VARCHAR(50) | NOT NULL | | - | Human-readable frequency description. |
| frequency_type | VARCHAR(20) | NOT NULL | CHECK | - | Controlled cadence driver of the plan. |
| interval_value | DECIMAL(12,2) | NULL | | NULL | Numeric value of the calendar or telemetry interval (e.g., 4 weeks, 500 hours). |
| interval_unit | VARCHAR(30) | NULL | CHECK | NULL | Controlled unit of the interval (WEEKS, MONTHS, OPERATING_HOURS, CYCLES, etc.). |
| monitored_signal_type | VARCHAR(80) | NULL | CHECK | NULL | Monitored telemetry signal type on the Equipment Unit for CBM plans (MTTO-023). |
| next_work_order_date | DATE | NULL | | NULL | Scheduled execution date (Calculated). |
| next_trigger_limit | DECIMAL(12,2) | NULL | | NULL | Accumulated limit calculated for the next trigger. |
| estimated_labor_hours | DECIMAL(10,2) | NOT NULL | | - | Estimated Man-Hours (Wrench Time) for planning. |
| technical_description | VARCHAR(255) | NOT NULL | | - | Technical description of the task scope. |
| cadence_override_justification | VARCHAR(255) | NULL | | NULL | Mandatory audit justification when overriding recommended cadence on critical assets (MTTO-001). |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Plan (document) lifecycle status. |

#### 3.2.4 media_attachments

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| work_order_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| failure_record_id | UUID | NULL | FK | NULL | Foreign key to the specific failure occurrence. |
| file_url | VARCHAR(255) | NOT NULL | | - | Evidence location. |
| file_type | VARCHAR(20) | NOT NULL | CHECK | - | Controlled attachment file format. |
| integrity_hash_sha256 | VARCHAR(64) | NOT NULL | | - | SHA-256 cryptographic digest calculated at capture for tamper detection (TR-003). |
| captured_offline | BOOLEAN | NOT NULL | | FALSE | Flag indicating whether evidence was acquired during disconnected field execution (MTTO-002). |
| uploaded_at | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | UTC upload/ingestion time of the evidence. |

#### 3.2.5 work_order_histories

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| work_order_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| old_status | VARCHAR(20) | NULL | | NULL | Previous lifecycle status (NULL if first status). |
| new_status | VARCHAR(20) | NOT NULL | | - | New lifecycle status. |
| timestamp | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | UTC transition time. |
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
| creation_date | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | UTC timestamp of order creation. |
| scheduled_date | TIMESTAMPTZ | NULL | | NULL | Planned start (UTC). |
| actual_start | TIMESTAMPTZ | NULL | | NULL | Actual execution start (UTC). |
| actual_finish | TIMESTAMPTZ | NULL | | NULL | Actual execution finish (UTC). |
| actual_labor_hours | DECIMAL(10,2) | NULL | | NULL | Actual labor duration (Calculated). |
| scope_checklist | JSONB | NULL | | NULL | Structured task checklist item array for field execution ([§6.2](#62-mttowork_ordersscope_checklist), MTTO-002). |
| criticality | VARCHAR(20) | NOT NULL | CHECK | - | WO criticality / priority label. |

#### 3.2.7 work_requests

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| description | VARCHAR(255) | NOT NULL | | - | Request narrative. |
| priority | VARCHAR(20) | NOT NULL | | - | Request priority label. |
| request_date | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | UTC timeline for audit. |
| request_source | VARCHAR(80) | NOT NULL | | - | Origin of the request. |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Request lifecycle status. |
| work_class_code | SMALLINT | NOT NULL | CHECK | - | Numeric weight (1..10) of the selected work class for RIME (`WorkRequest.workClassCode`, DT-DM-DOC-001 §4.24). |

#### 3.2.8 maintenance_plan_crafts

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| maintenance_plan_id | UUID | NOT NULL | PK, FK | - | Foreign key to the parent maintenance plan. |
| craft | VARCHAR(80) | NOT NULL | PK, CHECK | - | Controlled technical specialty vocabulary (DT-DM-DOC-001 §4.17). |

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
| timestamp | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | Precise UTC temporal record of the movement. |
| reason | VARCHAR(255) | NOT NULL | | - | Reason for movement or reference to external documents. |
| total_cost | DECIMAL(12,2) | NOT NULL | | - | Total cost of the transaction (Quantity \* Cost). |
| locator_id | UUID | NULL | FK | NULL | Specific physical storage bin of the transaction. |
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

#### 3.3.6 locators

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| warehouse_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| aisle | VARCHAR(50) | NOT NULL | | - | Physical aisle identifier. |
| rack | VARCHAR(50) | NULL | | NULL | Physical rack identifier. |
| shelf | VARCHAR(50) | NULL | | NULL | Physical shelf identifier. |
| barcode | VARCHAR(100) | NULL | UNIQUE | NULL | Scannable code for mobile operations. |
| is_active | BOOLEAN | NOT NULL | | TRUE | Active status for storage. |

#### 3.3.7 warehouses

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
| last_sync_time | TIMESTAMPTZ | NULL | | NULL | Last synchronization time (UTC). |

#### 3.4.3 spatial_metadata

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| mesh_mapping_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| position | JSONB | NOT NULL | | - | 3D Cartesian translation vector `{x, y, z}` in meters ([§6.3](#63-visspatial_metadataposition)). |
| rotation | JSONB | NULL | | NULL | Normalized 3D orientation quaternion `{x, y, z, w}` ([§6.4](#64-visspatial_metadatarotation)). |
| scale | JSONB | NULL | | NULL | 3D scale multiplier vector `{x, y, z}` ([§6.5](#65-visspatial_metadatascale)). |

#### 3.4.4 telemetry_signals

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| timestamp | TIMESTAMPTZ | NOT NULL | PK | clock_timestamp() | UTC measurement time and TimescaleDB hypertable partitioning column. |
| id | UUID | NOT NULL | PK | uuidv7() | Unique reading identifier paired with `timestamp` in composite hypertable PK. |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| signal_type | VARCHAR(80) | NOT NULL | CHECK | - | Sensor signal label. |
| value | DECIMAL(18,6) | NOT NULL | | - | Raw measurement value. |
| unit | VARCHAR(20) | NOT NULL | | - | Measurement unit. |
| threshold | DECIMAL(18,6) | NULL | | NULL | Alert threshold. |
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
| isolation_status | VARCHAR(30) | NOT NULL | CHECK | 'PENDING_ISOLATION' | LOTO isolation lifecycle state including `LEASED_OFFLINE` (`ADR-006`). |
| is_isolated | BOOLEAN | NOT NULL | | FALSE | Verified lockout state for the specific work. |
| isolated_at | TIMESTAMPTZ | NULL | | NULL | UTC timestamp when the lockout was executed. |
| padlock_tag_id | VARCHAR(80) | NULL | | NULL | Identifier of the physical padlock or tag (Try-Out). |
| try_out_confirmed | BOOLEAN | NOT NULL | | FALSE | Verified zero-energy Try-Out confirmation. |
| try_out_at | TIMESTAMPTZ | NULL | | NULL | UTC timestamp when physical Try-Out was performed. |
| try_out_method | VARCHAR(40) | NULL | CHECK | NULL | Controlled Try-Out verification method (DT-DM-DOC-001 §4.33). |
| try_out_reading | VARCHAR(80) | NULL | | NULL | Physical observed metric or confirmation text (e.g. 0.00 V, 0.0 psig). |
| telemetry_snapshot | JSONB | NULL | | NULL | Instantaneous sensor readings snapshot captured at zero-energy Try-Out verification ([§6.6](#66-viswork_order_isolationstelemetry_snapshot)). |
| signature_hash | VARCHAR(64) | NULL | | NULL | SHA-256 technician digital signature hash. |
| lease_holder_user_id | UUID | NULL | FK | NULL | Foreign key to `adm.users(id)` holding an active offline safety lease (`ADR-006`). |
| leased_until | TIMESTAMPTZ | NULL | | NULL | UTC expiration timestamp of the bounded offline LOTO safety lease (`ADR-006`). |

#### 3.4.7 work_permits

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| equipment_unit_id | UUID | NOT NULL | FK | - | Foreign key to the related table (`equipment_units`). |
| permit_identifier | VARCHAR(80) | NOT NULL | UNIQUE | - | Permit traceability natural code (e.g. PTW-1042). |
| permit_type | VARCHAR(50) | NOT NULL | CHECK | - | Controlled permit risk classification vocabulary (DT-DM-DOC-001 §4.34). |
| contractor | VARCHAR(120) | NOT NULL | | - | Executing contractor or internal company team name. |
| issuer_user_id | UUID | NOT NULL | FK | - | Foreign key to `adm.users(id)` for authorizing authority. |
| valid_from | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | Permit validity start (UTC). |
| valid_to | TIMESTAMPTZ | NOT NULL | | - | Permit validity end (UTC). |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Controlled permit lifecycle status vocabulary (DT-DM-DOC-001 §4.35). |

#### 3.4.8 plant_layout_revisions

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| functional_location_id | UUID | NOT NULL | FK | - | Foreign key to the Level 4 Functional Location (`functional_locations`). |
| revision_code | VARCHAR(40) | NOT NULL | UNIQUE | - | Management of Change (MOC) layout revision identifier (e.g. MOC-2026-REV01). |
| blob_storage_uri | VARCHAR(512) | NOT NULL | | - | Immutable Object Storage URI of the spatial layout artifact (`DT-UI-SVG-DOC-001`). |
| checksum_sha256 | VARCHAR(64) | NOT NULL | | - | Hex-encoded SHA-256 integrity digest verifying layout artifact immutability. |
| status | VARCHAR(20) | NOT NULL | CHECK | 'DRAFT' | Controlled MOC layout revision status vocabulary (DT-DM-DOC-001 §4.44). |
| approved_by_user_id | UUID | NULL | FK | - | Foreign key to `adm.users(id)` for the MOC approver (`NULL` while in `DRAFT`). |
| approved_at | TIMESTAMPTZ | NULL | | - | UTC timestamp when the revision was approved and activated. |
| created_at | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | UTC creation timestamp of the layout revision record. |

### 3.5 Schema `adm`

#### 3.5.1 audit_logs

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (composite PK `(id, timestamp)` for PostgreSQL 18 declarative range partitioning per FR-350). |
| user_id | UUID | NULL | FK | NULL | Foreign key to the related table. |
| action_type | VARCHAR(80) | NOT NULL | CHECK | - | Controlled audit operation type (`AuditLog.actionType`, DT-DM-DOC-001 §4.36: CREATE, UPDATE, DELETE, QUERY, ADJUST, SECURITY_ALERT). |
| entity_type | VARCHAR(80) | NOT NULL | | - | Affected table or domain entity. |
| entity_id | UUID | NOT NULL | | - | Identifier of the affected record. |
| timestamp | TIMESTAMPTZ | NOT NULL | PK | clock_timestamp() | Exact UTC moment of the mutation and range-partitioning key (composite PK `(id, timestamp)`, FR-350). |
| previous_state | JSONB | NULL | | NULL | Pre-mutation entity state snapshot captured via `RETURNING old.*` ([§6.7](#67-admaudit_logsprevious_state-and-new_state), ADR-003). |
| new_state | JSONB | NULL | | NULL | Post-mutation state snapshot, `QUERY` meta-audit payload, or `SECURITY_ALERT` context including transversal `justification` ([§6.7](#67-admaudit_logsprevious_state-and-new_state), ADR-003). |
| ip_address | VARCHAR(45) | NULL | | NULL | Network traceability (IPv4 or IPv6). |
| user_agent | VARCHAR(255) | NULL | | NULL | Client traceability. |
| previous_hash | VARCHAR(64) | NOT NULL | | - | SHA-256 integrity hash of the preceding audit record (`GENESIS` sentinel on first entry, ADR-003). |
| integrity_hash | VARCHAR(64) | NOT NULL | UNIQUE | - | SHA-256 cryptographic hash chaining `previous_hash` and current payload (ADR-003; composite unique `(integrity_hash, timestamp)` on partitioned table). |

#### 3.5.2 auth_tokens

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| user_id | UUID | NOT NULL | FK | - | Foreign key to the related table. |
| token_hash | VARCHAR(255) | NOT NULL | UNIQUE | - | Cryptographic representation of the token. |
| expires_at | TIMESTAMPTZ | NOT NULL | | - | UTC temporal validity limit. |
| is_revoked | BOOLEAN | NOT NULL | | FALSE | Pre-expiration manual revocation flag (`Revoke()`). |
| is_used | BOOLEAN | NOT NULL | | FALSE | Single-use token consumption flag (`MarkAsUsed()`, distinct from `Revoke()`). |
| used_at | TIMESTAMPTZ | NULL | | NULL | UTC timestamp recorded when a single-use token is consumed via `MarkAsUsed()`. |
| purpose | VARCHAR(30) | NOT NULL | CHECK | - | Controlled token purpose (ACCESS, SESSION_REFRESH, REGISTRATION, PASSWORD_RESET, OFFLINE_LOTO_LEASE). |

#### 3.5.3 role_permissions

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| role_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| module | VARCHAR(80) | NOT NULL | PK, CHECK | - | Controlled application subdomain or module vocabulary (DT-DM-DOC-001 §4.39). |
| action | VARCHAR(80) | NOT NULL | PK, CHECK | - | Controlled granular RBAC action vocabulary (CREATE, READ, EDIT, DELETE, APPROVE, AUDIT, EXECUTE per FR-248 & DT-DM-DOC-001 §4.42). |

#### 3.5.4 roles

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| name | VARCHAR(80) | NOT NULL | UNIQUE | - | Human-readable role identity. |
| description | VARCHAR(255) | NULL | | NULL | Description of the RBAC role. |
| is_active | BOOLEAN | NOT NULL | | TRUE | Logical lifecycle status flag allowing role deactivation while preserving historical audit traceability (FR-254). |
| is_system_root | BOOLEAN | NOT NULL | | FALSE | Immutable protection flag identifying built-in System Root roles guarded against privilege reduction or lockout (FR-250). |

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
| lockout_until | TIMESTAMPTZ | NULL | | NULL | UTC temporary block time window. |
| last_login_at | TIMESTAMPTZ | NULL | | NULL | UTC activity traceability. |

#### 3.5.7 work_order_assignments

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| work_order_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| user_id | UUID | NOT NULL | PK, FK | - | Foreign key to the related table. |
| role_in_work | VARCHAR(80) | NOT NULL | CHECK | - | Operational role of the technician in the specific WO (`WorkOrderAssignment.roleInWork`, DT-DM-DOC-001 §4.41). |
| assigned_at | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | UTC moment of assignment. |

#### 3.5.8 idempotency_logs

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| idempotency_key | VARCHAR(128) | NOT NULL | UNIQUE | - | Client-provided uniqueness token (ADR-007). |
| request_hash | VARCHAR(64) | NOT NULL | | - | SHA-256 fingerprint to prevent payload mutation. |
| status | VARCHAR(20) | NOT NULL | CHECK | - | Controlled state of the transaction (PROCESSING, COMPLETED, FAILED). |
| response_status_code | INT | NULL | | NULL | Cached HTTP status code replayed on duplicate requests during PostgreSQL idempotency fallback (ADR-007). |
| response_payload | JSONB | NULL | | NULL | Cached JSON response payload replayed on duplicate requests during PostgreSQL idempotency fallback (ADR-007). |
| created_at | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | UTC timestamp indexed for scheduled batched 24-hour TTL purge on the unpartitioned table (ADR-007). |

#### 3.5.9 audit_retention_partitions

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| partition_name | VARCHAR(80) | NOT NULL | UNIQUE | - | Physical PostgreSQL range partition identifier (e.g., `part_audit_2026_q4`, FR-350). |
| period_start | DATE | NOT NULL | | - | Inclusive UTC start date of the quarterly retention window (FR-358). |
| period_end | DATE | NOT NULL | | - | Inclusive UTC end date of the quarterly retention window (FR-358). |
| record_count | BIGINT | NOT NULL | | 0 | Total immutable audit records sealed inside the retention partition. |
| partition_anchor_hash | VARCHAR(64) | NULL | | NULL | Final SHA-256 `integrity_hash` anchoring continuity across archived partition boundaries (`NULL` while `is_cold_archived = FALSE`; ADR-003, FR-350). |
| is_cold_archived | BOOLEAN | NOT NULL | | FALSE | Flag indicating whether the quarterly partition is sealed in 7-year cold storage (FR-350, FR-358). |
| integrity_status | VARCHAR(30) | NOT NULL | CHECK | 'VERIFIED_INTACT' | Controlled partition integrity status vocabulary (DT-DM-DOC-001 §4.43). |
| sealed_at | TIMESTAMPTZ | NULL | | NULL | UTC timestamp when the partition was sealed for cold archival (`NULL` while hot/active). |

#### 3.5.10 password_policies

> Singleton security configuration table supporting PostgreSQL `xmin` optimistic concurrency (`PUT /api/v1/security/password-policy`, `NFR-272`).

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the singleton policy record (PK). |
| min_length | INT | NOT NULL | | 12 | Minimum required password length enforced under NIST SP 800-63B (`FR-259`, `NFR-272`). |
| require_uppercase | BOOLEAN | NOT NULL | | TRUE | Requires at least one uppercase alphabetical character (`NFR-272`). |
| require_digit | BOOLEAN | NOT NULL | | TRUE | Requires at least one numeric digit (`NFR-272`). |
| require_special_char | BOOLEAN | NOT NULL | | TRUE | Requires at least one special symbol (`NFR-272`). |
| max_age_days | INT | NOT NULL | | 90 | Maximum credential validity window in days triggering periodic password rotation (`FR-266`). |
| history_non_reuse_count | INT | NOT NULL | | 5 | Number of prior credential hashes blocked from reuse (`FR-266`, `NFR-272`). |
| lockout_threshold | INT | NOT NULL | | 5 | Maximum consecutive failed login attempts before brute-force lockout (`FR-260`). |
| lockout_duration_minutes | INT | NOT NULL | | 15 | Duration in minutes for temporary account lockout (`FR-260`). |
| updated_at | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | UTC timestamp of last policy update; singleton configuration aggregate guarded by PostgreSQL `xmin` optimistic concurrency (`PUT /api/v1/security/password-policy`). |

#### 3.5.11 user_password_histories

| Physical Field | PostgreSQL Type | Nullability | Constraints / Keys | Default Value | Justification |
| --- | --- | --- | --- | --- | --- |
| id | UUID | NOT NULL | PK | uuidv7() | Unique identifier of the entity (PK). |
| user_id | UUID | NOT NULL | FK | - | Foreign key to `adm.users(id)` (`ON DELETE CASCADE`) enforcing password non-reuse (`FR-266`). |
| password_hash | VARCHAR(255) | NOT NULL | | - | Salted cryptographic digest (`Argon2id`) of historical credential retained to prevent password reuse (`FR-266`, `NFR-267`). |
| created_at | TIMESTAMPTZ | NOT NULL | | clock_timestamp() | UTC timestamp when the rotated credential hash was recorded. |

## 4. Referential Relationships and Cascading (FKs)

| Parent Table | Cardinality | Child Table | Verb / Meaning | ON DELETE | ON UPDATE |
| :--- | :--- | :--- | :--- | :--- | :--- |
| equipment_classes | 1 : 0..N | equipment_units | classifies | RESTRICT | CASCADE |
| functional_locations| 1 : 0..N | functional_locations | contains (Self) | RESTRICT | CASCADE |
| functional_locations| 1 : 0..N | equipment_units | installs | RESTRICT | CASCADE |
| warehouses | 1 : 0..N | equipment_units | stores | SET NULL | CASCADE |
| functional_locations | 1 : 0..N | asset_installations | tracked via | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | asset_installations | mounted at | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | subunits | broken down into | CASCADE | CASCADE |
| subunits | 1 : 0..N | maintainable_items | built by | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | maintenance_plans | governed by | CASCADE | CASCADE |
| subunits | 1 : 0..N | maintenance_plans | targeted by | SET NULL | CASCADE |
| maintainable_items | 1 : 0..N | maintenance_plans | maintained via | SET NULL | CASCADE |
| maintenance_plans | 1 : 1..N | maintenance_plan_crafts | requires | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | work_orders | generates | RESTRICT | CASCADE |
| maintenance_plans | 1 : 0..N | work_orders | instantiates | SET NULL | CASCADE |
| work_requests | 1 : 0..N | work_orders | originates | SET NULL | CASCADE |
| equipment_units | 1 : 0..N | work_requests | requires | CASCADE | CASCADE |
| work_requests | 1 : 0..N | backlog_items | prioritized as | CASCADE | CASCADE |
| equipment_units | 1 : 0..N | backlog_items | pending for | CASCADE | CASCADE |
| work_orders | 1 : 0..N | failure_records | diagnoses | CASCADE | CASCADE |
| maintainable_items | 1 : 0..N | failure_records | affected by | RESTRICT | CASCADE |
| work_orders | 1 : 0..N | media_attachments | evidenced by | CASCADE | CASCADE |
| failure_records | 1 : 0..N | media_attachments | detailed by | CASCADE | CASCADE |
| work_orders | 1 : 0..N | work_order_histories| audited via | CASCADE | CASCADE |
| locators | 1 : 0..N | inventory_transactions| transacts | RESTRICT | CASCADE |
| warehouses | 1 : 0..N | locators | contains | CASCADE | CASCADE |
| warehouses | 1 : 0..N | inventory_transactions | records | RESTRICT | CASCADE |
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
| equipment_units | 1 : 0..N | work_permits | targets | RESTRICT | CASCADE |
| users | 1 : 0..N | work_permits | authorizes / issues | RESTRICT | CASCADE |
| work_permits | 1 : 0..N | work_orders | validates execution of | RESTRICT | CASCADE |
| work_orders | 1 : 0..N | visual_layers | visualized in | CASCADE | CASCADE |
| work_orders | 1 : 1..N | work_order_isolations | requires | CASCADE | CASCADE |
| isolation_points | 1 : 1..N | work_order_isolations | locked by | RESTRICT | CASCADE |
| users | 1 : 0..N | work_order_isolations | leases offline | SET NULL | CASCADE |
| functional_locations | 1 : 0..N | plant_layout_revisions | versioned by | RESTRICT | CASCADE |
| users | 1 : 0..N | plant_layout_revisions | approves | SET NULL | CASCADE |
| users | 1 : 1..N | user_roles | associated to | CASCADE | CASCADE |
| roles | 1 : 1..N | user_roles | granted to | CASCADE | CASCADE |
| roles | 1 : 0..N | role_permissions | contains | CASCADE | CASCADE |
| users | 1 : 0..N | auth_tokens | authenticated with | CASCADE | CASCADE |
| users | 1 : 0..N | work_order_assignments| assigned to | CASCADE | CASCADE |
| work_orders | 1 : 0..N | work_order_assignments| assigns personnel | CASCADE | CASCADE |
| users | 1 : 0..N | audit_logs | generates | RESTRICT | RESTRICT |
| users | 1 : 0..N | user_password_histories | retains password history | CASCADE | CASCADE |

## 5. Data Type Correspondence Matrix (Standard SQL vs. PostgreSQL)

To guarantee the physical viability of the logical model and its correct implementation in the selected database engine (**PostgreSQL**), each proposed physical data type has been formally validated and mapped:

| Physical Type (SQL Standard) | Native Type in PostgreSQL | Alternative Technical Equivalent | Technical Impact / Justification in PostgreSQL |
| :--- | :--- | :--- | :--- |
| VARCHAR(N) | VARCHAR(N) or CHARACTER VARYING(N) | TEXT | PostgreSQL handles variable-length strings efficiently. TEXT has no performance penalty and is preferred when a strict character length limit is not required. |
| SMALLINT | SMALLINT or INT2 | None | 2-byte signed integer (range -32,768 to 32,767). Optimal for cardinalities and taxonomic levels (like hierarchyLevel). |
| INT | INTEGER or INT4 | None | 4-byte signed integer (range -2,147,483,648 to 2,147,483,647). Standard for simple counters (like failedLoginAttempts). |
| BIGINT | BIGINT or INT8 | None | 8-byte signed integer. Used for large accumulated metrics like operational hours (operatingHours) and transition durations. |
| DATE | DATE | None | 4-byte data type for storing calendar dates without time zone (year, month, day). |
| TIMESTAMP WITH TIME ZONE | TIMESTAMPTZ | TIMESTAMP | Enforced across all event, audit, and operational timestamps so Npgsql 10 (`DateTimeOffset` / UTC) persists strictly in UTC without `InvalidCastException` or time-zone skew. |
| DECIMAL(P,S) | DECIMAL(P,S) or NUMERIC(P,S) | None | Exact precision type with user scale. Essential for monetary values (unitCost), sensor dimensions (value, threshold), and exact percentages (opacityLevel). |
| UUID | UUID | None | Native 128-bit data type. In PostgreSQL 18, the native function uuidv7() will be used as the default value for primary keys. Unlike UUIDv4 (random), UUIDv7 includes a 48-bit chronologically ordered time prefix, which prevents page fragmentation in B-Tree indexes and maximizes insertion performance in time series and audit logs. |
| BOOLEAN | BOOLEAN or BOOL | None | Logical type that stores TRUE or FALSE. |
| JSON | JSON | JSONB | JSON stores the literal text, which requires parsing on each query. It is recommended to use JSONB (Binary Decomposed JSON) because it stores the content in binary format, supports fast indexing (GIN indexes), and is much more efficient for audit queries (previousState and newState). |

## 6. JSONB Payload Contracts

This section serves as the **Single Source of Truth (SSoT)** for the internal JSON structure of all 8 `JSONB` columns defined in §3. Every column follows one of three architectural contract patterns:

- **Strict Schema:** Fixed property keys, deterministic types, and required validation boundaries (e.g., `scope_checklist`, `spatial_metadata` vectors).
- **Extensible Typed Dictionary:** Open domain-specific keys constrained to a homogeneous value type and canonical key naming style (e.g., `design_attributes`, `telemetry_snapshot`).
- **Polymorphic Envelope:** Shared structural conventions and transversal governance keys paired with entity- or event-specific payloads (e.g., `audit_logs.previous_state` and `audit_logs.new_state`).

All `JSONB` columns are indexed in PostgreSQL using `GIN (... jsonb_path_ops)` to support sub-second containment queries (`@>`) per [DT-ARQ-DB-DOC-001 §3.8](../../architecture/DT-ARQ-DB-DOC-001.md#38-gin-indexing-for-jsonb-immutable-audit). Upstream domain projections and application services bind strictly to the physical payload contracts below.

### 6.1 `tax.maintainable_items.design_attributes`

- **Contract Pattern:** Extensible Typed Dictionary (*String Key-Value Map*).
- **Domain Entity & Traceability:** `MaintainableItem` (`tax.maintainable_items`, [DT-DM-DOC-001 §3](../class/DT-DM-DOC-001.md#3-stereotype-mapping-table)) — ISO 14224 Level 8 component boundary decomposition ([MTTO-029](../../requirements/user-stories/mtto/MTTO-029.md), `FR-102`).
- **Storage & Query Rules:** Keys use lower `snake_case` engineering names aligned with ISO 14224 Annex A equipment-class attributes and extended P&ID boundary metadata (`FR-102`). Stored as flat string key-value pairs with engineering units included or suffixed (`_mm`, `_bar`, `_rpm`) to allow deterministic `@>` filtering without nested object traversal.

| Property / Key | JSON Type | Required | Validation / Format | Description & Traceability |
| --- | --- | --- | --- | --- |
| `pid_reference_code` | `string` | Optional | Uppercase drawing code (`^[A-Z0-9-]{4,40}$`) | Governing P&ID revision reference linked to the component's boundary envelope (`FR-102`). |
| `api_plan` | `string` | Optional | Controlled engineering tag (e.g., `Plan 53A`, `API 682`) | Mechanical seal flush or lubrication arrangement standard per ISO 14224 Annex A. |
| `shaft_diameter_mm` | `string` | Optional | Decimal string with unit clarity | Nominal shaft or journal size for seal and bearing compatibility. |
| `design_pressure_bar` | `string` | Optional | Decimal string (e.g., `"40.0"`) | Maximum allowable working pressure rating (`MAWP`). |
| `design_temperature_c` | `string` | Optional | Signed numeric string (e.g., `"-10 to 185"`) | Operating thermal envelope declared by manufacturer specification. |
| `elastomer_material` | `string` | Optional | Material family code (e.g., `FKM / Viton`, `PTFE`) | Wetted seal elastomer compatibility for corrosive hydrocarbon service. |
| `<custom_annex_a_key>` | `string` | Optional | Lower `snake_case` key (`max 64` chars), non-empty string value (`max 255` chars) | Class-specific ISO 14224 Annex A engineering attributes added during Level 8 registration. |

```json
{
  "pid_reference_code": "PID-TFA-1045-REV3",
  "api_plan": "Plan 53A",
  "shaft_diameter_mm": "65.0",
  "design_pressure_bar": "40.0",
  "design_temperature_c": "185",
  "elastomer_material": "FKM / Viton"
}
```

### 6.2 `mtto.work_orders.scope_checklist`

- **Contract Pattern:** Strict Schema (*Ordered JSON Array of Task Objects*).
- **Domain Entity & Traceability:** `WorkOrder` (`mtto.work_orders`, [DT-DM-DOC-001 §3](../class/DT-DM-DOC-001.md#3-stereotype-mapping-table)) — technical execution scope checklist ([MTTO-002](../../requirements/user-stories/mtto/MTTO-002.md), `FR-010`, `FR-012`).
- **Storage & Query Rules:** Serialized as a JSON array (`[]` when empty or `NULL` prior to task planning). Every element must contain `taskId`, `description`, and `isCompleted`. Technical closure (`WorkOrder.CompleteExecution()`, [DT-DM-DOC-002 §3](../class/DT-DM-DOC-002.md#3-layer-2-maintenance-management-mtto)) validates that all checklist items carry `"isCompleted": true` (`FR-010`, `FR-012`).

| Property / Key | JSON Type | Required | Validation / Format | Description & Traceability |
| --- | --- | --- | --- | --- |
| `[].taskId` | `string` | Required | UUIDv7 canonical hyphenated format | Stable task item identifier correlating field execution toggles with persisted checklist state. |
| `[].description` | `string` | Required | Non-empty string (`1..255` chars) | Actionable field step inherited from the `MaintenancePlan` or added during Work Order planning. |
| `[].isCompleted` | `boolean` | Required | JSON boolean (`true` / `false`) | Field completion flag confirming task step execution prior to technical closure. |

```json
[
  {
    "taskId": "0194f1c2-8a30-7b12-9e14-3a91c0d41001",
    "description": "Verify barrier fluid pressure in Plan 53A pot (target 12.5 bar) before seal housing inspection.",
    "isCompleted": true
  },
  {
    "taskId": "0194f1c2-8a30-7b12-9e14-3a91c0d41002",
    "description": "Torque gland plate bolts in cross-pattern to 48 Nm and record radial runout (< 0.05 mm).",
    "isCompleted": true
  }
]
```

### 6.3 `vis.spatial_metadata.position`

- **Contract Pattern:** Strict Schema (*3D Vector Object*).
- **Domain Entity & Traceability:** `SpatialMetadata` Value Object supporting 3D Digital Twin asset localization (`vis.mesh_mappings` -> `vis.spatial_metadata`, [DT-DM-DOC-001 §3](../class/DT-DM-DOC-001.md#3-stereotype-mapping-table)).
- **Storage & Query Rules:** Mandatory `NOT NULL` JSON object representing Cartesian translation coordinates in plant world meters relative to the facility origin `(0, 0, 0)` in a standard right-handed Y-up 3D Digital Twin scene coordinate frame.

| Property / Key | JSON Type | Required | Validation / Format | Description & Traceability |
| --- | --- | --- | --- | --- |
| `x` | `number` | Required | Finite IEEE-754 decimal number (meters) | East-West plant axis offset from facility datum. |
| `y` | `number` | Required | Finite IEEE-754 decimal number (meters) | Vertical elevation above grade datum. |
| `z` | `number` | Required | Finite IEEE-754 decimal number (meters) | North-South plant axis offset from facility datum. |

```json
{
  "x": 142.5,
  "y": 1.25,
  "z": -38.4
}
```

### 6.4 `vis.spatial_metadata.rotation`

- **Contract Pattern:** Strict Schema (*Unit Quaternion Object*).
- **Domain Entity & Traceability:** `SpatialMetadata` Value Object (`vis.spatial_metadata`, [DT-DM-DOC-001 §3](../class/DT-DM-DOC-001.md#3-stereotype-mapping-table)).
- **Storage & Query Rules:** Nullable (`NULL` implies identity orientation `{ "x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0 }`). When non-null, represents a normalized Hamiltonian unit quaternion ($\sqrt{x^2 + y^2 + z^2 + w^2} = 1 \pm 10^{-4}$) to eliminate gimbal lock during 3D mesh placement.

| Property / Key | JSON Type | Required | Validation / Format | Description & Traceability |
| --- | --- | --- | --- | --- |
| `x` | `number` | Required | Finite number in `[-1.0, 1.0]` | Imaginary `i` vector component of the unit quaternion. |
| `y` | `number` | Required | Finite number in `[-1.0, 1.0]` | Imaginary `j` vector component of the unit quaternion. |
| `z` | `number` | Required | Finite number in `[-1.0, 1.0]` | Imaginary `k` vector component of the unit quaternion. |
| `w` | `number` | Required | Finite number in `[-1.0, 1.0]` | Scalar real component of the unit quaternion. |

```json
{
  "x": 0.0,
  "y": 0.707107,
  "z": 0.0,
  "w": 0.707107
}
```

### 6.5 `vis.spatial_metadata.scale`

- **Contract Pattern:** Strict Schema (*3D Scale Multiplier Vector Object*).
- **Domain Entity & Traceability:** `SpatialMetadata` Value Object (`vis.spatial_metadata`, [DT-DM-DOC-001 §3](../class/DT-DM-DOC-001.md#3-stereotype-mapping-table)).
- **Storage & Query Rules:** Nullable (`NULL` implies uniform unit scale `{ "x": 1.0, "y": 1.0, "z": 1.0 }`). All axes must be strictly positive (`> 0.0`) to prevent inverted face normals in 3D geometry rendering.

| Property / Key | JSON Type | Required | Validation / Format | Description & Traceability |
| --- | --- | --- | --- | --- |
| `x` | `number` | Required | Finite positive number (`> 0.0`) | Scale factor along local mesh X axis. |
| `y` | `number` | Required | Finite positive number (`> 0.0`) | Scale factor along local mesh Y axis. |
| `z` | `number` | Required | Finite positive number (`> 0.0`) | Scale factor along local mesh Z axis. |

```json
{
  "x": 1.0,
  "y": 1.0,
  "z": 1.0
}
```

### 6.6 `vis.work_order_isolations.telemetry_snapshot`

- **Contract Pattern:** Extensible Typed Dictionary (*Numeric Telemetry Key-Value Map*).
- **Domain Entity & Traceability:** `WorkOrderIsolation` (`vis.work_order_isolations`, [DT-DM-DOC-001 §3](../class/DT-DM-DOC-001.md#3-stereotype-mapping-table) & [DT-DM-DOC-002 §5](../class/DT-DM-DOC-002.md#5-layer-4-digital-twin-convergence-vis)) — Zero-Energy physical Try-Out attestation ([VIS-011](../../requirements/user-stories/vis/VIS-011.md), `FR-230`, `NFR-229`, `TR-001`).
- **Storage & Query Rules:** Captures an immutable snapshot of instantaneous telemetry channel values at the exact timestamp of physical Try-Out attestation (`FR-230`, `TR-001`). Keys identify the cutoff sensor signal tag or canonical metric (`<tag_or_signal_unit>`) and values must be exact numeric decimals matching `DECIMAL(18,6)` telemetry precision.

| Property / Key | JSON Type | Required | Validation / Format | Description & Traceability |
| --- | --- | --- | --- | --- |
| `<sensor_channel_key>` | `number` | Required (at least 1 channel on online attestation) | Exact finite decimal number (`0.0` .. sensor max) | Instantaneous reading mapped by cutoff tag/signal identifier (e.g., `MCC_04B_VOLTAGE_V`, `LINE_PRESSURE_PSIG`, `FLOW_RATE_GPM`) proving zero-energy state at attestation (`NFR-229`). |

```json
{
  "MCC_04B_VOLTAGE_V": 0.00,
  "MCC_04B_CURRENT_A": 0.00,
  "SUCTION_HDR_PSIG": 0.12,
  "DISCHARGE_FLOW_GPM": 0.00
}
```

### 6.7 `adm.audit_logs.previous_state` and `new_state`

- **Contract Pattern:** Polymorphic Audit Envelope (`JSONB` paired snapshots sealed inside `integrity_hash` per [ADR-003](../../architecture/adr/ADR-003.md)).
- **Domain Entity & Traceability:** `AuditLog` (`adm.audit_logs`, [DT-DM-DOC-001 §3](../class/DT-DM-DOC-001.md#3-stereotype-mapping-table) & [DT-DM-DOC-002 §6](../class/DT-DM-DOC-002.md#6-layer-5-safety-and-governance-adm)) — Forensic ledger inspection and cross-cutting governed domain mutations ([ADM-032](../../requirements/user-stories/adm/ADM-032.md), [ADM-013](../../requirements/user-stories/adm/ADM-013.md), [ADM-014](../../requirements/user-stories/adm/ADM-014.md), [INV-005](../../requirements/user-stories/inv/INV-005.md), [INV-006](../../requirements/user-stories/inv/INV-006.md), [INV-027](../../requirements/user-stories/inv/INV-027.md), [INV-031](../../requirements/user-stories/inv/INV-031.md), [MTTO-026](../../requirements/user-stories/mtto/MTTO-026.md), [MTTO-029](../../requirements/user-stories/mtto/MTTO-029.md)).
- **Storage & Query Rules:**
  - `previous_state` holds the pre-mutation entity snapshot (`NULL` on `CREATE`, `QUERY`, and `SECURITY_ALERT` events).
  - `new_state` holds the post-mutation state (`RETURNING new.*` per `ADR-003`) or operational event payload, enriched with transversal governance keys listed below so every entry remains searchable via GIN `@>` and cryptographically sealed inside `integrity_hash` (`SHA-256`).
  - **Mandatory Secret Redaction Rule (`FR-349`, `NFR-357`):** Keys matching `(password_hash|token_hash|secret|private_key|signature_key)` must never store plaintext credentials and must be masked to `"[REDACTED SECRET]"` before forensic presentation or signed audit export ([ADM-032](../../requirements/user-stories/adm/ADM-032.md)).

| Property / Key | JSON Type | Applies To | Required | Validation / Format | Description & Traceability |
| --- | --- | --- | --- | --- | --- |
| `<entity_column_snake_case>` | `any` (`string \| number \| boolean \| array \| null`) | `CREATE`, `UPDATE`, `DELETE`, `ADJUST` | Conditional | Mirrors physical column values of `entity_type` | Atomic before/after field snapshot used to compute deterministic property-level diffs during forensic inspection (`ADM-032`, `FR-348`). |
| `justification` | `string` | `new_state` on governed `CREATE`, `UPDATE`, `DELETE`, `ADJUST` | Conditional (Mandatory on governed security/master mutations) | Trimmed string (`>= 15` chars on governed security/master mutations) | Unified transversal key storing operator audit/technical justification across governed domain mutations (`FR-120`, `FR-162`, `FR-174`, `FR-248`, `FR-263`, `FR-098`) or inventory reconciliation rationale (`INV-006`). |
| `queryFilters` | `object` | `new_state` on `QUERY` (Meta-Audit) | Required on `QUERY` | Structured filter object (`dateFromUtc`, `dateToUtc`, `eventType`, `entityType`, `jsonbContainment`) | Captures self-referential audit search or compliance export criteria (`NFR-360`, `TR-001-FR-361`). |
| `resultCount` | `number` | `new_state` on `QUERY` | Required on `QUERY` | Non-negative integer (`>= 0`) | Total audit entries returned or exported by the audited query execution. |
| `exportFormat` | `string` | `new_state` on `QUERY` export | Optional | `"CSV"` or `"JSON"` | Present when the `QUERY` entry records a signed forensic export (`FR-353`). |
| `violatedRule` | `string` | `new_state` on `SECURITY_ALERT` | Conditional | Rule code (e.g., `"SOD-SAF-01"`, `"HASH_CHAIN_BREACH"`, `"BRUTE_FORCE_LOCKOUT"`) | Identifies the violated security invariant (`FR-249`, `FR-346`, `TR-003-NFR-377`). |
| `diagnosticSummary` | `string` | `new_state` on `SECURITY_ALERT` | Optional | Non-empty summary (`1..500` chars) | Contextual forensic detail explaining the rejected bypass or integrity breach. |

**Example A — Governed RBAC Mutation (`UPDATE` on `Role`, `new_state`):**

```json
{
  "role_id": "0194e8a1-42c0-7d10-b120-9a18f004c210",
  "role_name": "Maintenance Planner",
  "is_active": true,
  "granted_permissions": [
    "MAINTENANCE:CREATE",
    "MAINTENANCE:READ",
    "MAINTENANCE:EDIT",
    "ASSETS:READ"
  ],
  "justification": "Granted MAINTENANCE:EDIT to allow backlog scheduling calibration per change ticket CHG-2026-041."
}
```

**Example B — Meta-Audit Query Execution (`QUERY` on `AuditLog`, `new_state`):**

```json
{
  "queryFilters": {
    "dateFromUtc": "2026-11-15T00:00:00Z",
    "dateToUtc": "2026-11-16T12:00:00Z",
    "entityType": "Role",
    "jsonbContainment": { "role_name": "Maintenance Planner" }
  },
  "resultCount": 4,
  "exportFormat": "JSON"
}
```

## 7. Optimistic Concurrency Mapping (PostgreSQL `xmin` System Column)

Per [DT-ARQ-DB-DOC-001 §3.12](../../architecture/DT-ARQ-DB-DOC-001.md#312-optimistic-concurrency-control-via-postgresql-xmin-system-column) and [NFR-169](../../requirements/user-stories/inv/INV-027.md#non-functional-requirements-nfr), every mutable aggregate root in schemas `tax`, `mtto`, `inv`, `vis`, and `adm` enforces optimistic concurrency through PostgreSQL's native 32-bit `xmin` transaction-ID system column rather than a custom `row_version` column:

| Persistence Layer | Wire / DTO Representation | Conflict Handling |
| :--- | :--- | :--- |
| PostgreSQL `xmin` (`xid` system column) mapped in EF Core via `builder.Property<uint>("ConcurrencyToken").IsRowVersion()` | `uint ConcurrencyToken` in DTOs/commands paired with HTTP `ETag: "{xmin}"` (response) and `If-Match: "{xmin}"` (request) | Npgsql appends `AND xmin = @pN` on `UPDATE`/`DELETE`; 0 affected rows raises `DbUpdateConcurrencyException` $\to$ `HTTP 409 Conflict` (`HTTP 412 Precondition Failed` on header mismatch). |
