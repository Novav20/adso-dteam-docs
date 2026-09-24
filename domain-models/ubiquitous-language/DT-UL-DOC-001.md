# DT-UL-DOC-001: Ubiquitous Language & Glossary

| Document ID | DT-UL-DOC-001 |
| ----------- | ------------- |
| Version     | 1.0.0         |
| Status      | DRAFT         |
| Scope       | Domain-Driven Design |

## Purpose
This document defines the strict **Ubiquitous Language** for the DTEAM project. It serves as the single source of truth for domain concepts to prevent terminology drift between the business domain, technical requirements, and source code. 

All actors, entities, processes, and states must adhere strictly to these definitions in English.

## Glossary
*(Note: Add terms here as you discover them during your Notion audit)*

| English Term (Standard)   | Spanish Translation (SENA Evidence) | Definition / Context                                                                  |
| :------------------------ | :---------------------------------- | :------------------------------------------------------------------------------------ |
| **Work Order (WO)**       | Orden de Trabajo                    | The core execution document for a maintenance intervention.                           |
| **Work Request (WR)**     | Solicitud de Trabajo                | An anomaly report that has not yet been approved as a Work Order.                     |
| **Work Permit**           | Permiso de Trabajo                  | Safety authorization required for high-risk operations (Hot Work, Confined Space).    |
| **Equipment**             | Equipo                              | A physical asset that can be maintained. Not "Machine" or "Asset" in general context. |
| **Digital Twin**          | Gemelo Digital                      | The virtual representation of the physical plant.                                     |
| **Lockout/Tagout (LOTO)** | Bloqueo LOTO / Aislamiento Seguro   | The physical safety procedure to ensure zero energy state.                            |
| **Functional Location**   | Ubicación Funcional                 | The logical place or position in the plant where an asset operates.                   |
| **Product Master**        | Maestro de Productos                | Abstract definition of the equipment (Model, Manufacturer). Works as a template.      |
| **Asset Record**          | Registro de Activo (Serializado)    | The unique physical instance with a Serial Number (SN).                               |
| **Kardex**                | Kardex / Historial de Movimientos   | Detailed and chronological record of each inventory transaction.                      |
| **Spare Part Request**    | Solicitud de Repuesto               | Formal request for a specific inventory component (MRO).                              |
| **Maintainable Item** | Activo Mantenible / Ítem Mantenible | The lowest level of equipment tracked for maintenance (ISO 14224 Level 8). |
| **Purchase Order (PO)** | Orden de Compra | Commercial document issued to a supplier indicating types, quantities, and agreed prices. |
| **Rotable Spare** | Repuesto Rotable | A spare part that can be repaired and reused, often serialized and tracked individually. |
| **Reorder Point** | Punto de Reorden | The specific inventory level that triggers an automatic replenishment/purchase request. |
| **HMI (Human-Machine Interface)** | Interfaz Hombre-Máquina | The visual dashboard or software interface used by operators to interact with the Digital Twin. |
| **Equipment Unit** | Unidad de Equipo | The physical machine as defined by ISO 14224 Level 6 (e.g., a specific Pump). |
| **Asset** | Activo | A general business term for anything that holds value. **Rule:** When referring to physical machinery in documentation, use **Equipment Unit** or **Maintainable Item** to maintain ISO 14224 precision. |
| **BOM (Bill of Materials)** | Lista de Materiales | The comprehensive list of parts, items, and materials required to perform a specific maintenance task. |
| **Work Request (WR)** | Solicitud de Trabajo | An unapproved report of an anomaly or request for maintenance work. It must be validated by a Planner before becoming a WO. |
| **RUL (Remaining Useful Life)** | Vida Útil Restante | The estimated time an Equipment Unit can continue to operate before it fails, typically calculated via ML/predictive models. |
| **Subunit** | Subunidad | A major structural or functional part of an Equipment Unit (ISO 14224 Level 7). |
| **Maintenance Plan** | Plan de Mantenimiento | Owns a planned maintenance schedule and its cadence. |
| **Failure Record** | Registro de Falla | Historical failure event directly linked to a Maintainable Item. |
| **Backlog Item** | Ítem de Backlog | Derived prioritization record linked to maintenance intake. |
| **Inventory Transaction** | Transacción de Inventario | Traceable movement record linked to parts, WOs, and warehouses. |
| **Warehouse** | Almacén / Bodega | Represents a stock location boundary with capacity rules. |
| **Supplier** | Proveedor | Owns procurement identity, commercial context, and warranty logic. |
| **Mesh Mapping** | Mapeo de Malla (Mesh) | Graphical projection linking a 3D mesh or SVG with an Equipment Unit. |
| **Telemetry Signal** | Señal de Telemetría | Raw measurement record with a timestamp used for traceability. |
| **Isolation Point** | Punto de Aislamiento | Permanent lockout point on an equipment required to be isolated during WOs. |
| **Visual Layer** | Capa Visual | Presentation record associated with a work order and visual state. |
| **Work Order History** | Historial de Orden de Trabajo | Append-only lifecycle transition record for a work order. |
| **RIME (Ranking Index for Maintenance Expenditure)** | RIME (Índice de Priorización) | Configurable prioritization strategy for work orders combining asset criticality and work class. |
| **Wrench Time** | Wrench Time / Horas-Hombre Estimadas | The actual active labor time spent by a technician physically executing a work order, excluding administrative delays. |
| **Offline-First** | Operación sin Conexión | An architecture pattern ensuring mobile applications remain fully functional without network connectivity by using local databases and delayed sync queues. |
| **Idempotency Filter** | Filtro de Idempotencia | A mechanism during data synchronization to prevent the same offline transaction from being processed twice in the central database. |
| **P&ID (Piping and Instrumentation Diagram)** | Diagrama de Tubería e Instrumentación (P&ID) | The detailed engineering schematic used as a reference to define the logical and physical boundaries of process equipment. |
| **Physical Boundaries** | Límites Físicos (Boundaries) | The exact start and end points in a process flow (e.g., specific flanges) that delimit the scope of an Equipment Unit according to ISO 14224. |
| **Condition-Based Maintenance (CBM)** | Mantenimiento Basado en Condición | Maintenance strategy driven by telemetry or physical condition limits rather than strict calendar schedules. |
| **Asset Swap** | Rotación de Activo (Asset Swap) | The functional replacement of an Equipment Unit at a Functional Location, typically used for rotable spares. |
| **Commissioning Gate** | Compuerta de Activación / Validación | A strict validation milestone ensuring all mandatory technical and safety configurations are met before asset activation. |
| **SKU (Stock Keeping Unit)** | SKU / Código Único | Unique identifier for inventory items within the Part Master. |
| **Part Master** | Catálogo de Repuestos Maestro | The centralized master catalog defining standardized materials, spare parts, and their technical parameters. |
| **SCE (Safety Critical Equipment)** | Equipo Crítico de Seguridad (SCE) | Equipment whose failure could cause a severe safety or environmental incident, requiring stricter maintenance controls. |
| **Zero Energy** | Energía Cero | A strict state where an asset is completely isolated from all active and residual energy sources, validated prior to any intervention. |
| **SIMOPS (Simultaneous Operations)** | SIMOPS (Operaciones Simultáneas) | Situations where two or more operations occur in the same physical location at the same time, requiring strict visual coordination to mitigate interference risks. |
| **HPHMI Grayscale** | Escala de Grises HPHMI | High-Performance Human-Machine Interface design philosophy using a neutral grayscale palette with redundant visual coding (Shape + Color) to reduce cognitive fatigue and highlight alarms. |
| **Semantic Zoom** | Zoom Semántico | A navigation interaction in the Digital Twin where information density (e.g., tags, ports) automatically adjusts based on zoom scale thresholds. |
| **Geometric Zoom** | Zoom Geométrico | A fluid visual scaling interaction on the digital canvas viewport. |
| **Try-Out Test** | Prueba de Arranque (Try-Out) | The final physical test performed by a technician to physically verify the absence of tension or energy before beginning maintenance work. |
| **Segregation of Duties (SoD)** | Segregación de Funciones (SoD) | A critical security principle preventing a single user role from having enough privileges to both execute and approve a sensitive transaction autonomously. |
| **Tamper-Evident** | Evidente de Manipulación / Tamper-Evident | A cryptographic property of the audit log that ensures any external modification or deletion of records instantly breaks the hash chain, raising a critical alert. |
| **Root Cause Analysis (RCA)** | Análisis de Causa Raíz (RCA) | A systematic engineering process for identifying the fundamental origin of a failure to prevent its recurrence. |
| **Meta-Audit** | Meta-Auditoría | The action of recording and tracing the queries made by administrators or auditors over the immutable audit log itself. |
| **Offline Lease** | Arrendamiento Fuera de Línea | A bounded temporary authorization token signed via HMAC-SHA256, issued to a mobile device to perform safety-critical operations (like LOTO) offline within a safe time window. |
| **Command-Sourced Synchronization** | Sincronización por Comandos de Intención | Architectural pattern where mobile clients synchronize atomic operational commands to a local queue (`SyncOutbox`) instead of final mutated states. |
| **Cryptographic Manual Override** | Anulación Manual Criptográfica | An exception for areas without network coverage, allowing technicians to manually bypass digital safety blocks after physical verification. |
| **LOTO Watchdog** | LOTO Watchdog (Perro Guardián) | A native background thread on the mobile device that continually monitors the safety heartbeat over WebSockets to trigger Fail-Safe actions. |
| **Preventive Security Lockout** | Bloqueo Preventivo de Seguridad | A fail-safe state triggered automatically by the LOTO Watchdog when the grace window expires without receiving a heartbeat. |
| **Grace Window** | Ventana de Gracia | A defined time threshold (e.g., 30s) used by the LOTO Watchdog to tolerate RF Shadowing and AP roaming without generating false positive safety lockouts. |
| **Unit of Work** | Unidad de Trabajo | A transactional persistence pattern ensuring multiple database changes succeed or fail as a single atomic operation. |
