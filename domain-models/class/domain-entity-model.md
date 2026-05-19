---
document_control:
  code: GD-DM-DOC-001
  version: 1.2-MVP
  date: 2026-05-19
  status: Draft
  author: Juan David
  approver: Antigravity
  standard: ISO 9001:2015 / ISO 14224:2016 / ISO 55000-Series
---

# Domain Entity Model

## 1. Purpose

This document is the business companion to the PlantUML domain model for the Gemelo Digital solution. It acts as the Single Source of Truth (SSoT) for domain meaning, tactical DDD boundaries, enum vocabularies, and preliminary persistence rules before the physical ERD is generated.

The document is intentionally focused on business rules and storage traceability rather than implementation details. The PlantUML model defines the structure; this document explains why each element exists, how it should be interpreted, and how it should be constrained in the database layer.

## 2. Critical Synthesis Decisions

### 2.1 Status Splitting on `EquipmentUnit`

The previous single `status` field is intentionally decomposed into three separate dimensions:

- `operationalStatus`: captures the real operational condition of the asset, such as uptime, downtime, or standby state, in line with ISO 14224 reliability and operating-state logic.
- `lifecycleStatus`: captures the business and accounting phase of the asset, such as storage, installation, commissioning, or decommissioning, which is more aligned with asset-management lifecycle governance.
- `maintenanceStatus`: captures the current maintenance context, such as whether the asset is operational, under maintenance, or under test.

This split reduces coupling, prevents overloaded business logic, and avoids storing unrelated meanings in a single field. It also makes transactional validation easier because each dimension can be constrained independently.

### 2.2 Qualitative RIME Factors

The RIME factors in `WorkRequest` are treated as qualitative selectors rather than fixed monetary formulas. This is important for the MVP because the maintenance backlog must work across plants with different financial scales, different downtime costs, and different operational maturity levels.

Using `CRITICAL`, `MAJOR`, and `MINOR` as the base levels keeps the model auditable and comparable while allowing the calculation engine to remain stable. The `economyFactor` is therefore not a hard-coded currency range in the domain model; it is a relative prioritization level that can be mapped to local cost bands in configuration.

### 2.3 Multi-Source Isolation and Safety Extensibility

The model intentionally supports safety isolation types beyond only electrical or mechanical energy. Industrial interventions may involve thermal, chemical, or gravitational hazards depending on the asset and the work scope. The permit model therefore needs extensible values and a controlled fallback such as `Other`.

### 2.4 Modeling Note on the Standards Set

The approved capsule set provides strong guidance for LOTO, competence, and safety governance, but it does not include a dedicated OSHA permit taxonomy capsule. For that reason, the permit and isolation vocabularies below are normalized project vocabularies aligned with the approved references rather than verbatim codes lifted from a single standard. This is deliberate and should be preserved in the ERD design as controlled lookup data.

### 2.5 Modeling Note on `MediaAttachment`

`MediaAttachment` is modeled as a `Value Object` in the domain layer because its business meaning is purely evidentiary. However, a relational implementation may still assign a technical surrogate key if the storage engine requires independent row addressing. That persistence detail does not change the domain classification.

## 3. Stereotype Mapping Table

| Entity | DDD Stereotype | Justification | Reference Standard |
|---|---|---|---|
| `FunctionalLocation` | `Aggregate Root` | Owns the asset location hierarchy and boundary definition. | ISO 14224 Chapter 8.1 and 8.2 |
| `EquipmentClass` | `Aggregate Root` | Owns the asset-class taxonomy and class-specific boundary semantics. | ISO 14224 Annex A |
| `EquipmentUnit` | `Aggregate Root` | Owns the inventory record and the three-way state split for a physical asset. | ISO 14224 Chapter 9.1 and Table 5 |
| `Subunit` | `Entity` | Depends on the parent asset lifecycle and taxonomy context. | ISO 14224 Levels 6–9 taxonomy |
| `MaintainableItem` | `Entity` | Represents the lowest repairable level used for maintenance and failure analysis. | ISO 14224 Levels 8–9 taxonomy |
| `WorkRequest` | `Aggregate Root` | Starts the maintenance intake flow and owns the RIME prioritization factors. | ISO 55000 risk and decision-making guidance; ADR 002 |
| `MaintenancePlan` | `Aggregate Root` | Owns a planned maintenance schedule and its cadence. | ISO 14224 maintenance data guidance |
| `WorkOrder` | `Aggregate Root` | Owns execution, history, attachments, and downstream work records. | ISO 14224 event data; ISO 9000 record control |
| `MediaAttachment` | `Value Object` | Pure evidence payload without independent business identity. | ISO 9000 documented information and records |
| `WorkOrderHistory` | `Entity` | Append-only lifecycle transition record for a work order. | ISO 9000 record immutability |
| `FailureRecord` | `Entity` | Historical failure event linked to equipment and maintenance history. | ISO 14224 failure logic |
| `BacklogItem` | `Entity` | Derived prioritization record tied to maintenance intake and asset context. | ISO 55000 risk ranking guidance |
| `SparePart` | `Aggregate Root` | Inventory master record for a part family with stock policy and cost data. | ISO 14224 inventory data; ISO 55000 planning guidance |
| `InventoryTransaction` | `Entity` | Traceable movement record linked to parts, work orders, and warehouses. | ISO 14224 transaction data; ISO 9000 traceability |
| `Warehouse` | `Aggregate Root` | Represents a stock-location boundary with capacity rules. | ISO 55000 resource planning guidance |
| `Supplier` | `Aggregate Root` | Owns procurement identity, commercial context, and warranty logic. | ISO 9000 documented information |
| `MeshMapping` | `Entity` | Persistent mapping record between the physical asset and the digital visualization. | ISO 9000 data vs. information separation |
| `TelemetrySignal` | `Entity` | Timestamped raw measurement record used for traceability and safety analytics. | ISO 9000 monitoring and measurement |
| `WorkPermit` | `Aggregate Root` | Safety authorization boundary for a field intervention. | ISO 55000 competence and LOTO guidance |
| `IsolationPoint` | `Entity` | Controlled isolation record executed under a permit/work scope. | ISO 55000 LOTO guidance; ISO 14224 safety governance |
| `VisualLayer` | `Entity` | Presentation record associated with a work order and visual state. | ISO 9000 record behavior |
| `SpatialMetadata` | `Value Object` | Immutable location and geometry descriptor for a visual artifact. | ISO 9000 data vs. information separation |
| `User` | `Aggregate Root` | Root of the account, password, lockout, and token lifecycle. | ISO 55000 audit governance; ISO 9000 audit control |
| `Role` | `Aggregate Root` | Root of authorization semantics and permission grouping. | ISO 55000 competence and role gating |
| `Permission` | `Value Object` | Atomic authorization rule with no standalone lifecycle. | ISO 9000 controlled workflow |
| `AuthToken` | `Entity` | Has issuance, use, and expiry lifecycle and must remain traceable to the owner. | ISO 9000 traceability |
| `WorkOrderAssignment` | `Entity` | Auditable relationship between a user/role and a work order. | ISO 55000 competency gatekeeping |
| `AuditLog` | `Entity` | Append-only audit record containing before/after state. | ISO 9000 audit evidence and record immutability |

## 4. Controlled Vocabulary (Enums)

### 4.1 `EquipmentUnit.operationalStatus`

| Value | Meaning |
|---|---|
| `UP` | The asset is running or ready in an operational sense. |
| `DOWN` | The asset is unavailable due to a failure or outage. |
| `STANDBY` | The asset is ready but not actively producing output. |

### 4.2 `EquipmentUnit.lifecycleStatus`

| Value | Meaning |
|---|---|
| `IN_STORAGE` | The asset exists as inventory but is not installed. |
| `INSTALLED` | The asset is physically installed in its functional location. |
| `COMMISSIONING` | The asset is being brought into service. |
| `DECOMMISSIONED` | The asset has been permanently removed from service. |

### 4.3 `EquipmentUnit.maintenanceStatus`

| Value | Meaning |
|---|---|
| `OPERATIONAL` | The asset is not currently under maintenance intervention. |
| `UNDER_MAINTENANCE` | The asset is actively being serviced. |
| `UNDER_TEST` | The asset is under verification or functional test. |

### 4.4 RIME factor vocabularies

All four `WorkRequest` factors use the same controlled levels.

| Value | Weight | Meaning |
|---|---|---|
| `CRITICAL` | 3 | Highest priority / highest exposure. |
| `MAJOR` | 2 | Medium priority / material exposure. |
| `MINOR` | 1 | Lowest priority / limited exposure. |

### 4.5 `MaintenancePlan.frequencyType`

| Value | Meaning |
|---|---|
| `CALENDAR_TIME` | Plan is driven by elapsed calendar time. |
| `OPERATING_HOURS` | Plan is driven by accumulated run hours. |
| `CYCLES` | Plan is driven by cycles or starts. |

### 4.6 `WorkPermit.permitType`

| Value | Meaning |
|---|---|
| `HOT_WORK` | Work involving flame, sparks, welding, or cutting. |
| `CONFINED_SPACE` | Work inside a confined or restricted-access area. |
| `ELECTRICAL_WORK` | Work on or near energized electrical systems. |
| `WORK_AT_HEIGHT` | Work at elevation with fall exposure. |
| `EXCAVATION` | Work that exposes subsurface hazards or trench risks. |
| `CHEMICAL` | Work that involves hazardous chemicals or exposure risk. |
| `THERMAL` | Work that involves high-temperature hazards. |
| `OTHER` | Site-specific permit type not covered by the standard list. |

### 4.7 `WorkPermit.status`

| Value | Meaning |
|---|---|
| `DRAFT` | Permit prepared but not yet issued. |
| `ISSUED` | Permit approved and released. |
| `ACTIVE` | Permit is currently in force. |
| `SUSPENDED` | Permit is temporarily paused. |
| `CLOSED` | Permit has been formally closed. |
| `EXPIRED` | Permit validity window has elapsed. |

### 4.8 `IsolationPoint.isolationType`

| Value | Meaning |
|---|---|
| `ELECTRICAL` | Electrical energy isolation. |
| `MECHANICAL` | Mechanical energy isolation. |
| `HYDRAULIC` | Hydraulic energy isolation. |
| `PNEUMATIC` | Pneumatic energy isolation. |
| `THERMAL` | Thermal energy isolation. |
| `CHEMICAL` | Chemical isolation. |
| `GRAVITATIONAL` | Gravity / stored-potential-energy hazard. |
| `OTHER` | Site-specific isolation type not covered by the standard list. |

### 4.9 `SparePart.stockPolicy`

| Value | Meaning |
|---|---|
| `REORDER_POINT` | Replenish when inventory reaches a trigger threshold. |
| `MIN_MAX` | Maintain stock between minimum and maximum levels. |
| `JUST_IN_TIME` | Replenish only when demand is expected. |

### 4.10 `MediaAttachment.fileType`

| Value | Meaning |
|---|---|
| `PDF` | Portable Document Format. |
| `JPG` | JPEG image file. |
| `PNG` | Portable Network Graphics image file. |

## 5. Physical Column Traceability Table

**Note:** Association-derived foreign keys are omitted from the field list below for readability, but they must be added in the physical ERD. The following mapping focuses on the logical fields already present in the PlantUML model.

### 5.1 Taxonomy Layer

| Entity | Logical Field | Physical Type (SQL Standard) | Nullability | Constraints / Key | Justification |
|---|---|---|---|---|---|
| `FunctionalLocation` | `tagNumber` | `VARCHAR(50)` | NOT NULL | UNIQUE | ISO 14224 tag identity and location traceability. |
| `FunctionalLocation` | `name` | `VARCHAR(150)` | NOT NULL |  | Human-readable location name. |
| `FunctionalLocation` | `description` | `VARCHAR(255)` | NULL |  | Optional explanatory text. |
| `FunctionalLocation` | `criticality` | `VARCHAR(30)` | NOT NULL | CHECK or lookup | Controlled priority vocabulary. |
| `FunctionalLocation` | `geographicLocation` | `VARCHAR(150)` | NULL |  | Physical context of the location. |
| `FunctionalLocation` | `hierarchyLevel` | `SMALLINT` | NOT NULL | CHECK (1..9) | ISO 14224 taxonomy level. |
| `EquipmentClass` | `className` | `VARCHAR(120)` | NOT NULL | UNIQUE | Class-level master data. |
| `EquipmentClass` | `description` | `VARCHAR(255)` | NULL |  | Class description. |
| `EquipmentClass` | `manufacturerStandard` | `VARCHAR(120)` | NULL |  | Standardization reference. |
| `EquipmentUnit` | `serialNumber` | `VARCHAR(100)` | NOT NULL | UNIQUE | Asset identification integrity. |
| `EquipmentUnit` | `manufacturer` | `VARCHAR(120)` | NOT NULL |  | Asset provenance. |
| `EquipmentUnit` | `model` | `VARCHAR(120)` | NOT NULL |  | Asset type identification. |
| `EquipmentUnit` | `purchaseDate` | `DATE` | NOT NULL |  | Procurement chronology. |
| `EquipmentUnit` | `rejectionReason` | `VARCHAR(255)` | NULL |  | Only present when procurement is rejected. |
| `EquipmentUnit` | `boundaryStart` | `VARCHAR(150)` | NOT NULL |  | Boundary definition start point. |
| `EquipmentUnit` | `boundaryEnd` | `VARCHAR(150)` | NOT NULL |  | Boundary definition end point. |
| `EquipmentUnit` | `acquisitionDate` | `DATE` | NOT NULL |  | Asset acquisition traceability. |
| `EquipmentUnit` | `installationDate` | `DATE` | NULL |  | Installation may be pending. |
| `EquipmentUnit` | `operationStartDate` | `DATE` | NULL |  | Operational start may be pending. |
| `EquipmentUnit` | `operatingHours` | `BIGINT` | NOT NULL | DEFAULT 0 | Reliability and usage tracking. |
| `EquipmentUnit` | `operationalStatus` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Controlled operating-state vocabulary. |
| `EquipmentUnit` | `lifecycleStatus` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Controlled lifecycle vocabulary. |
| `EquipmentUnit` | `maintenanceStatus` | `VARCHAR(30)` | NOT NULL | CHECK or lookup | Controlled maintenance-state vocabulary. |
| `Subunit` | `subunitType` | `VARCHAR(80)` | NOT NULL |  | Subcomponent taxonomy. |
| `Subunit` | `name` | `VARCHAR(120)` | NOT NULL |  | Subcomponent label. |
| `MaintainableItem` | `componentName` | `VARCHAR(120)` | NOT NULL |  | Maintainable item identity. |
| `MaintainableItem` | `subunitType` | `VARCHAR(80)` | NOT NULL |  | Taxonomic classification. |
| `MaintainableItem` | `sparePartType` | `VARCHAR(80)` | NULL |  | Optional spare-part correspondence. |
| `MaintainableItem` | `designAttributes` | `VARCHAR(255)` | NULL |  | Static design properties. |
| `MaintainableItem` | `status` | `VARCHAR(30)` | NOT NULL | CHECK or lookup | Item lifecycle state. |

### 5.2 Maintenance and Work Management

| Entity | Logical Field | Physical Type (SQL Standard) | Nullability | Constraints / Key | Justification |
|---|---|---|---|---|---|
| `WorkRequest` | `description` | `VARCHAR(255)` | NOT NULL |  | Request narrative. |
| `WorkRequest` | `priority` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Request priority label. |
| `WorkRequest` | `requestDate` | `TIMESTAMP` | NOT NULL |  | Audit timeline. |
| `WorkRequest` | `requestSource` | `VARCHAR(80)` | NOT NULL |  | Origin of the request. |
| `WorkRequest` | `status` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Request lifecycle state. |
| `WorkRequest` | `riskFactor` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | RIME controlled vocabulary. |
| `WorkRequest` | `impactFactor` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | RIME controlled vocabulary. |
| `WorkRequest` | `maintainabilityFactor` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | RIME controlled vocabulary. |
| `WorkRequest` | `economyFactor` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | RIME controlled vocabulary. |
| `MaintenancePlan` | `maintenanceMethod` | `VARCHAR(80)` | NOT NULL |  | Maintenance strategy. |
| `MaintenancePlan` | `frequency` | `VARCHAR(80)` | NOT NULL |  | Human-readable frequency description. |
| `MaintenancePlan` | `frequencyType` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Controlled plan cadence. |
| `MaintenancePlan` | `nextWorkOrderDate` | `DATE` | NULL |  | Scheduled execution date. |
| `MaintenancePlan` | `status` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Plan lifecycle state. |
| `WorkOrder` | `currentStatus` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Execution lifecycle state. |
| `WorkOrder` | `maintenanceMethod` | `VARCHAR(80)` | NOT NULL |  | Maintenance method. |
| `WorkOrder` | `creationDate` | `TIMESTAMP` | NOT NULL |  | Work order creation timestamp. |
| `WorkOrder` | `scheduledDate` | `TIMESTAMP` | NULL |  | Planned start. |
| `WorkOrder` | `actualStart` | `TIMESTAMP` | NULL |  | Execution start. |
| `WorkOrder` | `actualFinish` | `TIMESTAMP` | NULL |  | Execution finish. |
| `WorkOrder` | `actualLaborHours` | `DECIMAL(10,2)` | NULL |  | Actual labor duration. |
| `WorkOrder` | `criticality` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Work order impact label. |
| `MediaAttachment` | `fileUrl` | `VARCHAR(255)` | NOT NULL |  | Evidence location. |
| `MediaAttachment` | `fileType` | `VARCHAR(10)` | NOT NULL | CHECK or lookup | Controlled attachment format. |
| `MediaAttachment` | `uploadedAt` | `TIMESTAMP` | NOT NULL |  | Evidence ingestion time. |
| `WorkOrderHistory` | `oldStatus` | `VARCHAR(20)` | NOT NULL |  | Prior lifecycle state. |
| `WorkOrderHistory` | `newStatus` | `VARCHAR(20)` | NOT NULL |  | New lifecycle state. |
| `WorkOrderHistory` | `timestamp` | `TIMESTAMP` | NOT NULL |  | Transition time. |
| `WorkOrderHistory` | `durationSeconds` | `BIGINT` | NOT NULL |  | Time spent in state. |
| `FailureRecord` | `failureId` | `UUID` | NOT NULL | PK | Failure event identity. |
| `FailureRecord` | `failureMode` | `VARCHAR(120)` | NOT NULL | CHECK or lookup | ISO 14224 failure coding. |
| `FailureRecord` | `failureMechanism` | `VARCHAR(120)` | NOT NULL | CHECK or lookup | ISO 14224 failure coding. |
| `FailureRecord` | `failureCause` | `VARCHAR(120)` | NOT NULL | CHECK or lookup | ISO 14224 failure coding. |
| `FailureRecord` | `downtime` | `DECIMAL(10,2)` | NOT NULL |  | Reliability analysis metric. |
| `FailureRecord` | `status` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Failure record state. |
| `BacklogItem` | `priorityScore` | `INT` | NOT NULL |  | RIME-derived backlog score. |
| `BacklogItem` | `status` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Backlog lifecycle state. |

### 5.3 Inventory and Supply

| Entity | Logical Field | Physical Type (SQL Standard) | Nullability | Constraints / Key | Justification |
|---|---|---|---|---|---|
| `SparePart` | `sku` | `VARCHAR(80)` | NOT NULL | UNIQUE | Part identity. |
| `SparePart` | `description` | `VARCHAR(255)` | NOT NULL |  | Human-readable part description. |
| `SparePart` | `manufacturer` | `VARCHAR(120)` | NOT NULL |  | Supplier/manufacturer identity. |
| `SparePart` | `commodityCode` | `VARCHAR(80)` | NULL |  | Classification code. |
| `SparePart` | `reorderPoint` | `DECIMAL(18,2)` | NOT NULL |  | Inventory trigger. |
| `SparePart` | `unitOfMeasure` | `VARCHAR(20)` | NOT NULL |  | Inventory unit. |
| `SparePart` | `stockPolicy` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Controlled inventory policy. |
| `SparePart` | `quantityOnHand` | `DECIMAL(18,2)` | NOT NULL |  | Available quantity. |
| `SparePart` | `reservedQuantity` | `DECIMAL(18,2)` | NOT NULL | DEFAULT 0 | Allocated stock. |
| `SparePart` | `maxCapacity` | `DECIMAL(18,2)` | NULL |  | Maximum storage cap. |
| `SparePart` | `unitCost` | `DECIMAL(18,2)` | NOT NULL |  | Cost tracking. |
| `SparePart` | `status` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Part lifecycle state. |
| `InventoryTransaction` | `quantity` | `DECIMAL(18,2)` | NOT NULL |  | Movement amount. |
| `InventoryTransaction` | `transactionType` | `VARCHAR(30)` | NOT NULL | CHECK or lookup | Issue/receipt/adjustment classification. |
| `InventoryTransaction` | `timestamp` | `TIMESTAMP` | NOT NULL |  | Transaction time. |
| `InventoryTransaction` | `reason` | `VARCHAR(255)` | NOT NULL |  | Transaction justification. |
| `InventoryTransaction` | `totalCost` | `DECIMAL(18,2)` | NOT NULL |  | Financial traceability. |
| `Warehouse` | `name` | `VARCHAR(120)` | NOT NULL | UNIQUE | Warehouse identity. |
| `Warehouse` | `location` | `VARCHAR(150)` | NOT NULL |  | Physical location. |
| `Warehouse` | `capacity` | `DECIMAL(18,2)` | NOT NULL |  | Storage capacity. |
| `Supplier` | `name` | `VARCHAR(150)` | NOT NULL | UNIQUE | Supplier identity. |
| `Supplier` | `contactInfo` | `VARCHAR(255)` | NULL |  | Contact record. |
| `Supplier` | `warrantyTerms` | `VARCHAR(255)` | NULL |  | Commercial warranty context. |

### 5.4 Digital Convergence and Safety Visualization

| Entity | Logical Field | Physical Type (SQL Standard) | Nullability | Constraints / Key | Justification |
|---|---|---|---|---|---|
| `MeshMapping` | `meshUuid` | `UUID` | NOT NULL | UNIQUE | Digital twin mapping identity. |
| `MeshMapping` | `mappingStatus` | `VARCHAR(30)` | NOT NULL | CHECK or lookup | Mapping lifecycle state. |
| `MeshMapping` | `lastSyncTime` | `TIMESTAMP` | NULL |  | Last synchronization time. |
| `TelemetrySignal` | `signalType` | `VARCHAR(80)` | NOT NULL |  | Sensor signal label. |
| `TelemetrySignal` | `value` | `DECIMAL(18,6)` | NOT NULL |  | Raw measurement value. |
| `TelemetrySignal` | `unit` | `VARCHAR(20)` | NOT NULL |  | Measurement unit. |
| `TelemetrySignal` | `threshold` | `DECIMAL(18,6)` | NULL |  | Alert threshold. |
| `TelemetrySignal` | `timestamp` | `TIMESTAMP` | NOT NULL |  | Measurement time. |
| `TelemetrySignal` | `isSafetyCritical` | `BOOLEAN` | NOT NULL | DEFAULT FALSE | Safety classification flag. |
| `WorkPermit` | `permitIdentifier` | `VARCHAR(80)` | NOT NULL | UNIQUE | Permit traceability. |
| `WorkPermit` | `permitType` | `VARCHAR(30)` | NOT NULL | CHECK or lookup | Permit vocabulary. |
| `WorkPermit` | `contractorName` | `VARCHAR(150)` | NOT NULL |  | Contractor identification. |
| `WorkPermit` | `status` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Permit lifecycle state. |
| `IsolationPoint` | `isolationTag` | `VARCHAR(80)` | NOT NULL | UNIQUE | Isolation point identity. |
| `IsolationPoint` | `isolationType` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Isolation vocabulary. |
| `IsolationPoint` | `isVerified` | `BOOLEAN` | NOT NULL | DEFAULT FALSE | Verification state. |
| `VisualLayer` | `layerType` | `VARCHAR(80)` | NOT NULL |  | Visual representation type. |
| `VisualLayer` | `opacityLevel` | `DECIMAL(5,2)` | NOT NULL | CHECK (0..1) | Rendering control. |
| `VisualLayer` | `status` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Visual layer state. |
| `SpatialMetadata` | `position` | `VARCHAR(120)` | NOT NULL |  | Spatial coordinate or descriptor. |
| `SpatialMetadata` | `rotation` | `VARCHAR(120)` | NULL |  | Orientation descriptor. |
| `SpatialMetadata` | `scale` | `VARCHAR(120)` | NULL |  | Scale descriptor. |

### 5.5 Governance and Security

| Entity | Logical Field | Physical Type (SQL Standard) | Nullability | Constraints / Key | Justification |
|---|---|---|---|---|---|
| `User` | `username` | `VARCHAR(80)` | NOT NULL | UNIQUE | Account identity. |
| `User` | `email` | `VARCHAR(150)` | NOT NULL | UNIQUE | Contact and login identity. |
| `User` | `status` | `VARCHAR(20)` | NOT NULL | CHECK or lookup | Account lifecycle state. |
| `User` | `passwordHash` | `VARCHAR(255)` | NOT NULL |  | Credential security. |
| `User` | `failedLoginAttempts` | `INT` | NOT NULL | DEFAULT 0 | Lockout control. |
| `User` | `lockoutUntil` | `TIMESTAMP` | NULL |  | Account lock window. |
| `Role` | `roleName` | `VARCHAR(80)` | NOT NULL | UNIQUE | Authorization role name. |
| `Role` | `description` | `VARCHAR(255)` | NULL |  | Role meaning. |
| `Role` | `isSystemRole` | `BOOLEAN` | NOT NULL | DEFAULT FALSE | Root/admin role protection. |
| `Permission` | `module` | `VARCHAR(80)` | NOT NULL |  | Authorization scope. |
| `Permission` | `action` | `VARCHAR(80)` | NOT NULL |  | Authorization action. |
| `AuthToken` | `tokenHash` | `VARCHAR(255)` | NOT NULL | UNIQUE | Token security. |
| `AuthToken` | `expiresAt` | `TIMESTAMP` | NOT NULL |  | Expiration control. |
| `AuthToken` | `isUsed` | `BOOLEAN` | NOT NULL | DEFAULT FALSE | One-time-use state. |
| `WorkOrderAssignment` | `roleInWork` | `VARCHAR(80)` | NOT NULL |  | Assigned role in execution. |
| `WorkOrderAssignment` | `assignedAt` | `TIMESTAMP` | NOT NULL |  | Assignment time. |
| `AuditLog` | `entityType` | `VARCHAR(80)` | NOT NULL |  | Audited entity type. |
| `AuditLog` | `actionType` | `VARCHAR(80)` | NOT NULL |  | Audited action. |
| `AuditLog` | `timestamp` | `TIMESTAMP` | NOT NULL |  | Audit event time. |
| `AuditLog` | `integrityHash` | `VARCHAR(255)` | NOT NULL |  | Tamper evidence. |
| `AuditLog` | `entityIdentifier` | `VARCHAR(120)` | NOT NULL |  | Correlates the record to the business object. |
| `AuditLog` | `previousState` | `JSON` | NULL |  | Before-image for audit traceability. |
| `AuditLog` | `newState` | `JSON` | NULL |  | After-image for audit traceability. |

## 6. Final Notes

- The domain model should remain the business source of truth until the physical ERD is generated.
- Controlled vocabularies that are stable and low cardinality can be enforced with `CHECK` constraints.
- Vocabularies that are likely to change or grow should move to lookup tables.
- Audit and failure records should remain append-only and traceable.
- The safety-related vocabulary for permits and isolation points should be treated as controlled compliance data, not free text.
