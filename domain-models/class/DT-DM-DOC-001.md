---
code: DT-DM-DOC-001
version: 1.3
date: 2026-09-14
status: Approved — Domain Conceptual Specification
author: Juan David Julio Serrano
standard:
  - ISO 9001:2015
  - ISO 14224:2016
  - ISO 55000-Series
  - ISO 13374-Series
  - ISO 27001:2022
---

# Domain Model Specification

## 1. Purpose

This document is the business complement to the Digital Twin solution's domain model. It acts as the Single Source of Truth (SSoT) for domain meaning, DDD tactical boundaries, enumerator (enum) vocabularies, and preliminary persistence rules before generating the physical ERD.

The document focuses on business rules and storage traceability rather than implementation details. The UML model defines the structure; this document explains why each element exists, how it should be interpreted, and how it must be constrained in the database layer.

## 2. Critical Synthesis Decisions

### 2.1 State Division in EquipmentUnit

The `status` field is decomposed into four independent and specialized dimensions:

- `operationalStatus`: captures the actual operating condition of the Equipment Unit, such as uptime, downtime, or standby, in line with ISO 14224 reliability and operational state logic.
- `lifecycleStatus`: captures the accounting and business phase of the Equipment Unit, such as storage, installation, commissioning, or decommissioning, which is more aligned with lifecycle governance in asset management (ISO 55000).
- `maintenanceStatus`: captures the current maintenance context, such as whether the Equipment Unit is operational, under maintenance, or under test.
- `healthStatus`: captures the consolidated physical and mechanical health (Undetermined, Good, Fair, Serious, Critical, etc.) based on condition monitoring telemetry (ISO 13374).

This division reduces coupling, avoids overloading business logic, and prevents storing unrelated meanings in a single field. It also facilitates transactional validation because each dimension can be constrained independently.

### 2.2 Configurable RIME Prioritization

To comply with the risk management required by the ISO 55001 standard and best practices in maintenance engineering, the system adopts the RIME (Ranking Index for Maintenance Expenditure) standard.

According to [[ADR-002]], the calculation of the priority score is encapsulated under the *Strategy* pattern through a domain service. The architecture decouples this algorithm from the Work Order, allowing future strategies adapted to economic or inventory factors to be incorporated without altering the core entities.

### 2.3 Multi-Source Isolation and Safety Extensibility

The model intentionally supports safety isolation types beyond merely electrical or mechanical energy. Industrial interventions can involve thermal, chemical, or gravitational risks depending on the Equipment Unit and the scope of work. Therefore, the permit model needs extensible values and a controlled alternative (fallback) such as `OTHER`.

### 2.4 Modeling Note on the Standard Suite

The approved capsules set provides strong guidance for LOTO, competencies, and safety governance, but does not include a capsule dedicated to the OSHA permit taxonomy. For that reason, the permit and isolation vocabularies below are normalized project vocabularies aligned with the approved references rather than literal codes extracted from a single standard. This is deliberate and must be preserved in the ERD design as controlled lookup data.

### 2.5 Modeling Note on MediaAttachment

`MediaAttachment` is modeled as a Value Object in the domain layer because its business meaning is purely evidential. However, a relational implementation could still assign it a technical surrogate key if the storage engine requires independent row addressing. That persistence detail does not change the classification in the domain.

### 2.6 Module Isolation via Database Schemas

To reflect the Modular Monolith architecture in the persistence layer and avoid saturating the default schema (`public`), the system tables are distributed into dedicated schemas corresponding to the DDD Bounded Contexts:

- `tax`: Taxonomy and assets according to ISO 14224 (`functional_locations`, `equipment_units`, `subunits`, `maintainable_items`, `equipment_classes`).
- `mtto`: Maintenance and reliability management (`work_requests`, `work_orders`, `maintenance_plans`, `failure_records`, `backlog_items`).
- `inv`: Resource and supply control (`spare_parts`, `inventory_transactions`, `material_requirements`, `warehouses`, `suppliers`).
- `vis`: Digital twin and operational safety layers (`mesh_mappings`, `spatial_metadata`, `telemetry_signals`, `work_permits`, `isolation_points`).
- `adm`: Perimeter security, IAM, and immutable audit (`users`, `roles`, `role_permissions`, `auth_tokens`, `audit_logs`).

This segregation allows for:
1. **Defense in Depth:** Granular assignment of SQL privileges (GRANT/REVOKE) per module to prevent unauthorized cross-access.
2. **Query Clarity:** Elimination of redundant prefixes in table names (e.g., `mtto.work_orders` instead of `public.mtto_work_orders`).
3. **Maintainability and Evolution:** Facilitates the future extraction of a module into its own microservice or independent database if scalability requirements demand it.

## 3. Stereotype Mapping Table

| Entity | DDD Stereotype | Justification | Reference Standard |
| --- | --- | --- | --- |
| FunctionalLocation | Aggregate Root | Owns the asset's location hierarchy and boundary definition. | ISO 14224 Chapters 8.1 and 8.2 |
| EquipmentClass | Aggregate Root | Owns the asset class taxonomy and class-specific boundary semantics. | ISO 14224 Annex A |
| EquipmentUnit | Aggregate Root | Owns the inventory record and the three-way status split for a physical asset. | ISO 14224 Chapter 9.1 and Table 5 |
| Subunit | Entity | Depends on the parent asset's lifecycle and taxonomy context. | ISO 14224 Taxonomy Levels 6–9 |
| MaintainableItem | Entity | Represents the lowest repairable level used for maintenance and failure analysis. | ISO 14224 Taxonomy Levels 8–9 |
| WorkRequest | Aggregate Root | Initiates the maintenance intake flow and owns the RIME prioritization factors. | ISO 55000 risk and decision guidance; ADR 002 |
| MaintenancePlan | Aggregate Root | Owns a planned maintenance schedule and its cadence. | ISO 14224 maintenance data guidance |
| WorkOrder | Aggregate Root | Owns execution, history, attachments, and downstream work records. | ISO 14224 event data; ISO 9000 record control |
| MediaAttachment | Value Object | Pure evidence payload with no independent business identity. | ISO 9000 documented information and records |
| WorkOrderHistory | Entity | Append-only lifecycle transition record for a work order. | ISO 9000 record immutability |
| FailureRecord | Entity | Historical failure event directly linked to the MaintainableItem that experiences it. | ISO 14224 failure logic |
| BacklogItem | Entity | Derived prioritization record linked to maintenance intake and asset context. | ISO 55000 risk classification guidance |
| SparePart | Aggregate Root | Inventory master record for a part family with stock policy and cost data. | ISO 14224 inventory data; ISO 55000 planning guidance |
| InventoryTransaction | Entity | Traceable movement record linked to parts, work orders, and warehouses. | ISO 14224 transaction data; ISO 9000 traceability |
| Warehouse | Aggregate Root | Represents a stock location boundary with capacity rules. | ISO 55000 resource planning guidance |
| Supplier | Aggregate Root | Owns procurement identity, commercial context, and warranty logic. | ISO 9000 documented information |
| MeshMapping | Entity | Graphical projection of the Sidecar pattern that uniquely links geometry (SVG or 3D mesh) with Level 6 (EquipmentUnit). Levels 7 and 8 do not possess individual geometric coordinates on the general blueprint. | ISO 9000 data vs. information separation |
| TelemetrySignal | Entity | Raw measurement record with a timestamp used for traceability and safety analytics. | ISO 9000 monitoring and measurement |
| WorkPermit | Aggregate Root | Safety authorization boundary that validates the execution of specific work orders in the field. | ISO 55000 competence and LOTO guidance |
| IsolationPoint | Entity | Permanent lockout point belonging to an EquipmentUnit, required to be isolated during work orders. | ISO 55000 LOTO guidance; ISO 14224 governance |
| VisualLayer | Entity | Presentation record associated with a work order and visual state. | ISO 9000 record behavior |
| SpatialMetadata | Value Object | Immutable descriptor of location and geometry for a visual artifact. | ISO 9000 data vs. information separation |
| User | Aggregate Root | Root of the account, password, lockout, and token lifecycle. | ISO 55000 audit governance; ISO 9000 audit control |
| WorkOrderIsolation | Entity | Represents the state and temporal record of a safety lockout on an isolation point for a Work Order. | ISO 55000 LOTO guidance; ISO 14224 |
| Role | Aggregate Root | Root of authorization semantics and permission grouping. | ISO 55000 competence and role guidance |
| Permission | Value Object | Atomic authorization rule without an independent lifecycle. | ISO 9000 controlled workflow |
| AuthToken | Entity | Has a lifecycle of issuance, usage, and expiration, and must remain traceable back to its owner. | ISO 9000 traceability |
| WorkOrderAssignment | Entity | Auditable relationship between a user/role and a work order. | ISO 55000 competence control |
| AuditLog | Entity | Append-only audit record containing the before/after state. | ISO 9000 audit evidence and record immutability |
| MaterialRequirement | Entity | Represents future planning and consumption reservation of a spare part for a specific work order. | ISO 55000 resource planning |

## 4. Controlled Vocabulary

### Schema: TAX

#### 4.1 EquipmentUnit.healthStatus

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| UNDETERMINED | Unknown health status. | ISO 13374-4 Health Assessment |
| GOOD | All indicators within normal limits. | ISO 13374-4 Health Assessment |
| FAIR | Some minor anomalies detected, no immediate risk. | ISO 13374-4 Health Assessment |
| SERIOUS_BUT_STABLE | Serious anomalies but without progressive worsening. | ISO 13374-4 Health Assessment |
| SERIOUS | Serious anomalies deteriorating. | ISO 13374-4 Health Assessment |
| CRITICAL_BUT_STABLE | Critical condition that does not worsen in the short term. | ISO 13374-4 Health Assessment |
| CRITICAL | Imminent failure, immediate intervention required. | ISO 13374-4 Health Assessment |

#### 4.2 EquipmentUnit.lifecycleStatus

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| IN_STORAGE | The asset exists as inventory but is not installed. | |
| INSTALLED | The asset is physically installed in its functional location. | |
| COMMISSIONING | The asset is being commissioned / put into service. | |
| DECOMMISSIONED | The asset has been permanently retired from service. | |

#### 4.3 EquipmentUnit.maintenanceStatus

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| OPERATIONAL | The asset is not currently under maintenance intervention. | |
| UNDER_MAINTENANCE | The asset is actively being repaired or serviced. | |
| UNDER_TEST | The asset is under functional testing or verification. | |

#### 4.4 EquipmentUnit.operationalStatus

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| UP | The asset is running or ready in an operational sense. | |
| DOWN | The asset is unavailable due to failure or outage. | |
| STANDBY | The asset is ready but not actively producing. | |

#### 4.5 FunctionalLocation.environmentalExposure

| Value | Meaning | Reference Norm |
| --- | --- | --- |
| SEVERE | Facilities not enclosed or outdoors; exposed to vibration, heat, dust, or salt spray. | ISO 14224:2016 Table A.70 |
| MODERATE | Partially enclosed or moderately exposed facilities; natural ventilation. | ISO 14224:2016 Table A.70 |
| LOW | Enclosed or indoor facilities; minimal exposure; mechanical ventilation. | ISO 14224:2016 Table A.70 |
| UNKNOWN | Information on environmental exposure is not available. | ISO 14224:2016 Table A.70 |

#### 4.6 MaintainableItem.status

| Value | Meaning | Reference Norm |
| --- | --- | --- |
| OPERATIONAL | Healthy and operating within design parameters. | ISO 13374 (Normal) |
| DEGRADED | Partial failure or condition warning; requires monitoring or planned intervention. | ISO 14224 (Partial Failure) / ISO 13374 (Alert) |
| FAILED | Complete functional failure; the item can no longer perform its required function. | ISO 14224 (Complete Failure) |
| UNDER_REPAIR | The component is actively being maintained, repaired, or replaced. | EAM Transactional State |
| REPLACED | End of the component's lifecycle in that location; preserved for MTBF history. | Reliability History |

### Schema: MTTO

#### 4.7 BacklogItem.status

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| PENDING | Awaiting technical analysis or material definition. | Planning Queue |
| READY | Fully planned and ready to be scheduled. | Ready to Schedule |
| DEFERRED | Intentionally postponed (lack of budget or plant turnaround). | Queue Suspension |

#### 4.8 FailureRecord.detectionMethod

| Value | Meaning | Reference Norm |
| --- | --- | --- |
| PERIODIC_MAINTENANCE | Discovered during scheduled activities of the preventive plan. | ISO 14224:2016 Table B.4 |
| FUNCTIONAL_TESTING | Discovered when activating a function and comparing against standard. | ISO 14224:2016 Table B.4 |
| INSPECTION | Discovered during planned visual inspection or NDT testing. | ISO 14224:2016 Table B.4 |
| PERIODIC_CBM | Revealed during scheduled measurement rounds (vibration, offline thermography). | ISO 14224:2016 Table B.4 |
| PRESSURE_TESTING | Observed specifically during pressure testing. | ISO 14224:2016 Table B.4 |
| CONTINUOUS_CBM | Revealed by alarms or online instrument readings (SCADA). | ISO 14224:2016 Table B.4 |
| PRODUCTION_INTERFERENCE | Discovered by unexpected interruption or reduction in production. | ISO 14224:2016 Table B.4 |
| CASUAL_OBSERVATION | Discovered by senses (noise, smell, leak) during normal routines. | ISO 14224:2016 Table B.4 |
| CORRECTIVE_MAINTENANCE | Observed while repairing a different failure. | ISO 14224:2016 Table B.4 |
| ON_DEMAND | Discovered during an actual attempt to activate (e.g., failure of an ESD valve to close). | ISO 14224:2016 Table B.4 |
| OTHER | Other unclassified detection method. | ISO 14224:2016 Table B.4 |

#### 4.9 FailureRecord.operationalCondition

| Value | Meaning | Reference Norm |
| --- | --- | --- |
| RUNNING | In normal process operation at the time of the event. | ISO 14224:2016 Table 6 |
| START_UP | Occurred during the start-up process. | ISO 14224:2016 Table 6 |
| RUN_DOWN | Occurred during the shutdown/take-out-of-service process. | ISO 14224:2016 Table 6 |
| HOT_STANDBY | In active standby (ready to operate immediately). | ISO 14224:2016 Table 6 |
| COLD_STANDBY | In passive standby (requires prior actions to operate). | ISO 14224:2016 Table 6 |
| IDLE | Available but not required by the process. | ISO 14224:2016 Table 6 |
| TESTING | Occurred during the execution of a functional test. | ISO 14224:2016 Table 6 |

#### 4.10 FailureRecord.operationalImpact

| Value | Meaning | Reference Norm |
| --- | --- | --- |
| EXTENSIVE_STOP | Extensive catastrophic shutdown of production or facility. | ISO 14224:2016 Table C.2 |
| STOP_ABOVE_ACCEPTABLE | Production shutdown above the acceptable plant limit. | ISO 14224:2016 Table C.2 |
| STOP_BELOW_ACCEPTABLE | Production shutdown below the acceptable limit. | ISO 14224:2016 Table C.2 |
| STOP_MINOR | Minor or negligible production impact. | ISO 14224:2016 Table C.2 |

#### 4.11 MaintenancePlan.frequencyType

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| CALENDAR_TIME | The plan is driven by elapsed calendar time. | |
| OPERATING_HOURS | The plan is driven by accumulated operating hours. | |
| CYCLES | The plan is driven by cycles or starts. | |

#### 4.12 MaintenancePlan.maintenanceMethod

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| PREVENTIVE | Systematic preventive maintenance (time/usage-based). | ISO 14224 (Preventative) |
| PREDICTIVE | Predictive monitoring (vibration analysis, thermography, etc.). | ISO 14224 (Condition-based) |
| CONDITION_BASED | Direct actions triggered by sensor limits in telemetry. | ISO 13374 / CBM |

#### 4.13 MaintenancePlan.requiredSpecialty

| Value | Meaning | Reference / Framework |
| --- | --- | --- |
| MECHANICAL | Mechanical interventions, transmission adjustment, alignment, and pumps. | Internal Vocabulary (SMRP Practices) |
| ELECTRICAL | Power systems, electric motors, switchboards, and substations. | Internal Vocabulary (SMRP Practices) |
| INSTRUMENTATION_AND_CONTROL | Instrument calibration, control loops, and automation/PLCs. | Internal Vocabulary (SMRP Practices) |
| LUBRICATION | Lubrication routes, oil changes, and specialized greasing. | Internal Vocabulary (ISO 18436-4 / SMRP) |
| CONDITION_MONITORING | Predictive monitoring routes (vibrations, thermography, ultrasound). | Internal Vocabulary (ISO 18436-2 / SMRP) |
| ELECTRONICS | Electronic boards, variable frequency drives, and digital components. | Internal Vocabulary (SMRP Practices) |
| WELDING_FABRICATION | Welding, boilermaking, pipefitting, and structural repairs. | Internal Vocabulary (SMRP Practices) |
| FACILITIES | Civil infrastructure, structures, lighting, and general services. | Internal Vocabulary (EAM Practices) |

#### 4.14 MaintenancePlan.status

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| DRAFT | Plan in design or technical review phase, inactive. | Document control |
| ACTIVE | Active and triggering work orders according to its cycle. | Operational |
| INACTIVE | Temporarily deactivated due to outage or operational change. | Cycle suspension |
| ARCHIVED | Obsolete or replaced; retained for audit history. | ISO 55001 Lifecycle |

#### 4.15 MediaAttachment.fileType

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| PDF | Portable Document Format. | |
| JPG | JPEG image file. | |
| PNG | Portable Network Graphics image file. | |

#### 4.16 WorkOrder.criticality

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| EMERGENCY | Total plant shutdown, imminent safety or environmental risk. | Maximum Criticality |
| URGENT | Failure with immediate operational impact; repair in under 24-48h. | High Priority |
| NORMAL | Plannable within weekly cycles and windows. | Medium Priority |
| LOW | Aesthetic tasks or minor operational convenience. | Low Priority |

#### 4.17 WorkOrder.currentStatus

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| PLANNING | Definition of spare parts, LOTO permits, and resources. | FSM - Planning |
| WAITING_PARTS | Active waiting for spare parts in warehouse/purchasing. | FSM - Logistics Bottleneck |
| SCHEDULED | Assigned with technician and scheduled execution date. | FSM - Scheduling |
| IN_PROGRESS | The technician is executing the labor (clock-in active). | FSM - Execution ("Wrench Time") |
| COMPLETE | Technical work finished, pending review. | FSM - Technical Pre-closure |
| CLOSED | Administratively closed and failure codes entered. | FSM - QA / ISO 14224 Audit |

**FSM Transition Constraints (Industrial Safety & LOTO):**

- To transition from any previous state (`PLANNING`, `SCHEDULED`, `WAITING_PARTS`) to **`IN_PROGRESS`**, the system must programmatically verify the following preconditions:
  1. **Work Permit (`WorkPermit`):** An associated work permit must exist and its `status` must be strictly `APPROVED`.
  2. **Lockout/Tagout (LOTO):** All isolation points declared for the work order in the intermediate `work_order_isolations` table must have their lockout status verified (`is_isolated = TRUE` and `isolated_at` not null).

#### 4.18 WorkOrder.maintenanceMethod

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| CORRECTIVE | Reactive corrective maintenance (repair after failure). | ISO 14224 (Corrective) |
| PREVENTIVE | Systematic scheduled preventive (derived from plan). | ISO 14224 (Preventative) |
| PREDICTIVE | Scheduled predictive monitoring or inspection. | ISO 14224 (Condition-based) |
| IMPROVEMENT | Modification, redesign, or technical improvement (CAPEX/OPEX). | Change Management / Engineering |

#### 4.19 WorkRequest.status

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| NEW | Newly created request pending evaluation. | Basic CMMS Intake |
| APPROVED | Approved and promoted to Work Order (`WorkOrder`). | Transition to planning |
| REJECTED | Rejected for being invalid, duplicated, or a false alarm. | False positive traceability |

#### 4.20 WorkRequest.workClassCode (Work Class RIME)

| Code (Weight) | Work Class | Industrial Example |
| --- | --- | --- |
| 10 | Safety or Environmental Emergency | Hydrocarbon leak, critical safety isolation failure. |
| 9 | Production Shutdown (Direct Downtime) | Catastrophic functional failure in a critical asset (Level 6 Pump). |
| 8 | High Priority Process Work | Performance degradation with imminent risk of shutdown. |
| 7 | Regulated Preventive Maintenance (PM) | Instrumented safety calibrations required by law. |
| 6 | Systematic Preventive Maintenance | Calendar or telemetry-based cyclical plans. |
| 5 | Predictive Maintenance (Analysis / Route) | Vibration inspection, planned thermography. |
| 4 | Non-Critical Corrective Work | Repair of failures with active redundancy in the system. |
| 3 | Engineering Modifications (Improvements) | CAPEX optimization projects (Non-urgent). |
| 2 | Aesthetic Work / Order and Cleanliness | Painting structures, handrails, general cleaning. |
| 1 | Work for Operational Convenience | Minor comfort adjustments or administrative support. |

### Schema: INV

#### 4.21 InventoryTransaction.transactionType

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| RECEIPT | Inventory input (purchase, return, transfer). | Stock Intake |
| ISSUE | Inventory output (consumption in Work Order). | Charge to WO Costs |
| ADJUSTMENT | Manual/automatic adjustment due to physical count discrepancy. | Inventory Reconciliation |

#### 4.22 SparePart.status

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| ACTIVE | Active and available for consumption and purchases. | Stock Management |
| OBSOLETE | Obsolete, no new purchase allowed (kept for history). | ISO 55001 Lifecycle |
| SUSPENDED | Temporarily blocked due to quality control or supplier issues. | Quality Control |

#### 4.23 SparePart.stockPolicy

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| REORDER_POINT | Replenish when inventory reaches an activation threshold (trigger). | |
| MIN_MAX | Maintain stock between minimum and maximum levels. | |
| JUST_IN_TIME | Replenish only when demand is expected. | |
### Schema: VIS

#### 4.24 IsolationPoint.isolationType

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| ELECTRICAL | Opening of circuit breakers or physical disconnection. | Electrical LOTO (OSHA) |
| MECHANICAL | Mechanical locks, pins, or physical blocks. | Mechanical LOTO |
| PNEUMATIC | Bleeding and locking of compressed air or gas lines. | Pneumatic LOTO |
| HYDRAULIC | Closing of fluid valves and accumulator bleeding. | Hydraulic LOTO |
| CHEMICAL | Double Block and Bleed. | Chemical / Process LOTO |
| THERMAL | Thermal isolation of hot or cryogenic surfaces. | Thermal LOTO |
| GRAVITATIONAL | Physical blocks to prevent suspended masses from falling. | Gravitational LOTO |

#### 4.25 MeshMapping.mappingStatus

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| MAPPED | The asset is correctly linked to its 3D representation in the twin. | Digital Linking |
| UNMAPPED | The asset's 3D mesh is missing or unpositioned. | Incomplete Twin |
| SYNC_ERROR | Consistency or loading error between the graphics engine and the DB. | Synchronization Error |

#### 4.26 TelemetrySignal.signalType

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| TEMPERATURE | Thermal measurement. | Temperature Sensor |
| PRESSURE | Fluid/gas pressure measurement. | Pressure Sensor |
| VIBRATION | Mechanical oscillation measurement. | Vibration Analysis |
| FLOW_RATE | Flow rate measurement. | Flowmeter |
| VOLTAGE | Electrical voltage measurement. | Voltage Sensor |
| RPM | Angular velocity measurement. | Tachometer |

#### 4.27 VisualLayer.status

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| VISIBLE | Layer actively displayed in the 3D viewer. | Rendered State |
| HIDDEN | Layer temporarily hidden. | Rendered State |
| GHOSTED | Layer visible with transparency to reveal interiors. | Rendered State |

#### 4.28 WorkPermit.permitType

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| HOT_WORK | Work with ignition sources or open flame (requires extinguisher). | Industrial Safety (OSHA) |
| COLD_WORK | Standard work without spark hazards (mechanical, cleaning). | Industrial Safety (OSHA) |
| CONFINED_SPACE | Entry into tanks, ducts, or areas with limited ventilation. | Confined Space (High Risk) |
| ELECTRICAL | Intervention in high or medium voltage lines (requires LOTO). | Electrical Risk |
| WORK_AT_HEIGHT | Work above 1.5m in height with fall risk. | Heights (OSHA / Res. 4272) |
| EXCAVATION | Excavations, trenches, or deep earthworks. | Excavation (OSHA) |
| CHEMICAL | Handling or exposure to hazardous chemicals or noxious gases. | Chemical Risk |

#### 4.29 WorkPermit.status

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| DRAFT | Permit prepared by the executor but not yet submitted. | Authorization Cycle |
| PENDING | Submitted and in the process of evaluation and signature by the supervisor. | Authorization Cycle |
| APPROVED | Formally authorized (enables the work order). | Active Permit / FSM Trigger |
| EXPIRED | Automatically expired (the valid time window was exceeded). | Risk Control |
| REVOKED | Immediately canceled due to unsafe conditions in the field. | Emergency Intervention |
| CLOSED | Formally finished after concluding the intervention and removing LOTO. | Operation Closure |

### Schema: ADM

#### 4.30 AuditLog.actionType

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| CREATE | Initial record of a new object in the system. | ISO 9001 Audit |
| UPDATE | Modification of existing fields (tracks previous state). | ISO 9001 Audit |
| DELETE | Logical or physical deletion of a critical entity. | ISO 9001 Audit |

#### 4.31 RolePermission.module

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| ASSETS | Management of taxonomy, equipment, and plans. | Assets Domain |
| MAINTENANCE | Management of requests, backlog, and history. | Maintenance Domain |
| INVENTORY | Management of spare parts, warehouses, and movements. | Inventory Domain |
| SAFETY | Management of telemetry, LOTO permits, and isolations. | Safety Domain |
| SYSTEM | Governance, users, roles, and audit logs. | IAM Domain |

#### 4.32 User.status

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| ACTIVE | Active account authorized to interact with the platform. | Account Lifecycle |
| INACTIVE | Account deactivated temporarily or permanently (history preserved). | Account Lifecycle |
| LOCKED | Automatically locked after exceeding failed login attempts. | Brute Force Mitigation |

#### 4.33 WorkOrderAssignment.roleInWork

| Value | Meaning | Reference Norm / Concept |
| --- | --- | --- |
| TECHNICIAN | Executing technician who performs the labor and logs wrench time. | Technical Execution |
| SUPERVISOR | Supervisor who signs the technical closure and approves LOTO. | Line Manager |
| PLANNER | Planner who designs the order, assigns spare parts, and times. | Maintenance Engineering |

## 5. Physical Mapping and Data Dictionary

For details on the physical mapping and the relational schema, see [[DT-ERD-DOC-001]].

## 6. Final Notes

- The domain model must remain the business source of truth until the physical ERD is generated.
- Controlled vocabularies that are stable and of low cardinality can be enforced via CHECK constraints.
- Vocabularies that are likely to change or grow must be moved to lookup tables.
- Failure and audit logs must remain append-only and traceable.
- Safety-related vocabulary for permits and isolation points must be treated as controlled compliance data, not as free text.
