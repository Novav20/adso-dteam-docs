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

| English Term (Standard)   | Definition / Context                                                                  |
| :------------------------ | :------------------------------------------------------------------------------------ |
| **Work Order (WO)**       | The core execution document for a maintenance intervention.                           |
| **Work Request (WR)**     | An anomaly report that has not yet been approved as a Work Order.                     |
| **Work Permit**           | Safety authorization required for high-risk operations (Hot Work, Confined Space).    |
| **Equipment**             | A physical asset that can be maintained. Not "Machine" or "Asset" in general context. |
| **Digital Twin**          | The virtual representation of the physical plant.                                     |
| **Lockout/Tagout (LOTO)** | The physical safety procedure to ensure zero energy state.                            |
| **Functional Location**   | The logical place or position in the plant where an asset operates.                   |
| **Product Master**        | Abstract definition of the equipment (Model, Manufacturer). Works as a template.      |
| **Asset Record**          | The unique physical instance with a Serial Number (SN).                               |
| **Kardex**                | Detailed and chronological record of each inventory transaction.                      |
| **Spare Part Request**    | Formal request for a specific inventory component (MRO).                              |
| **Maintainable Item**     | The lowest level of equipment tracked for maintenance (ISO 14224 Level 8).            |
| **Purchase Order (PO)**   | Commercial document issued to a supplier indicating types, quantities, and agreed prices. |
| **Rotable Spare**         | A spare part that can be repaired and reused, often serialized and tracked individually. |
| **Reorder Point**         | The specific inventory level that triggers an automatic replenishment/purchase request. |
| **HMI (Human-Machine Interface)** | The visual dashboard or software interface used by operators to interact with the Digital Twin. |
| **Equipment Unit**        | The physical machine as defined by ISO 14224 Level 6 (e.g., a specific Pump).         |
| **Asset**                 | A general business term for anything that holds value. **Rule:** When referring to physical machinery in documentation, use **Equipment Unit** or **Maintainable Item** to maintain ISO 14224 precision. |
| **BOM (Bill of Materials)** | The comprehensive list of parts, items, and materials required to perform a specific maintenance task. |
| **Work Request (WR)**     | An unapproved report of an anomaly or request for maintenance work. It must be validated by a Planner before becoming a WO. |
| **RUL (Remaining Useful Life)** | The estimated time an Equipment Unit can continue to operate before it fails, typically calculated via ML/predictive models. |
| **Subunit**               | A major structural or functional part of an Equipment Unit (ISO 14224 Level 7).       |
| **Maintenance Plan**      | Owns a planned maintenance schedule and its cadence.                                  |
| **Failure Record**        | Historical failure event directly linked to a Maintainable Item.                      |
| **Backlog Item**          | Derived prioritization record linked to maintenance intake.                           |
| **Inventory Transaction** | Traceable movement record linked to parts, WOs, and warehouses.                       |
| **Warehouse**             | Represents a stock location boundary with capacity rules.                             |
| **Supplier**              | Owns procurement identity, commercial context, and warranty logic.                    |
| **Mesh Mapping**          | Graphical projection linking a 3D mesh or SVG with an Equipment Unit.                 |
| **Telemetry Signal**      | Raw measurement record with a timestamp used for traceability.                        |
| **Isolation Point**       | Permanent lockout point on an equipment required to be isolated during WOs.           |
| **Visual Layer**          | Presentation record associated with a work order and visual state.                    |
| **Work Order History**    | Append-only lifecycle transition record for a work order.                             |
| **RIME (Ranking Index for Maintenance Expenditure)** | Configurable prioritization strategy for work orders combining asset criticality and work class. |
| **Wrench Time**           | The actual active labor time spent by a technician physically executing a work order, excluding administrative delays. |
| **Offline-First**         | An architecture pattern ensuring mobile applications remain fully functional without network connectivity by using local databases and delayed sync queues. |
| **Idempotency Filter**    | A mechanism during data synchronization to prevent the same offline transaction from being processed twice in the central database. |
| **P&ID (Piping and Instrumentation Diagram)** | The detailed engineering schematic used as a reference to define the logical and physical boundaries of process equipment. |
| **Physical Boundaries**   | The exact start and end points in a process flow (e.g., specific flanges) that delimit the scope of an Equipment Unit according to ISO 14224. |
| **Condition-Based Maintenance (CBM)** | Maintenance strategy driven by telemetry or physical condition limits rather than strict calendar schedules. |
| **Asset Swap**            | The functional replacement of an Equipment Unit at a Functional Location, typically used for rotable spares. |
| **Commissioning Gate**    | A strict validation milestone ensuring all mandatory technical and safety configurations are met before asset activation. |
| **SKU (Stock Keeping Unit)** | Unique identifier for inventory items within the Part Master.                         |
| **Part Master**           | The centralized master catalog defining standardized materials, spare parts, and their technical parameters. |
| **SCE (Safety Critical Equipment)** | Equipment whose failure could cause a severe safety or environmental incident, requiring stricter maintenance controls. |
| **Zero Energy**           | A strict state where an asset is completely isolated from all active and residual energy sources, validated prior to any intervention. |
| **SIMOPS (Simultaneous Operations)** | Situations where two or more operations occur in the same physical location at the same time, requiring strict visual coordination to mitigate interference risks. |
| **HPHMI Grayscale**       | High-Performance Human-Machine Interface design philosophy using a neutral grayscale palette with redundant visual coding (Shape + Color) to reduce cognitive fatigue and highlight alarms. |
| **Semantic Zoom**         | A navigation interaction in the Digital Twin where information density (e.g., tags, ports) automatically adjusts based on zoom scale thresholds. |
| **Geometric Zoom**        | A fluid visual scaling interaction on the digital canvas viewport.                    |
| **Try-Out Test**          | The final physical test performed by a technician to physically verify the absence of tension or energy before beginning maintenance work. |
| **Segregation of Duties (SoD)** | A critical security principle preventing a single user role from having enough privileges to both execute and approve a sensitive transaction autonomously. |
| **Tamper-Evident**        | A cryptographic property of the audit log that ensures any external modification or deletion of records instantly breaks the hash chain, raising a critical alert. |
| **Root Cause Analysis (RCA)** | A systematic engineering process for identifying the fundamental origin of a failure to prevent its recurrence. |
| **Meta-Audit**            | The action of recording and tracing the queries made by administrators or auditors over the immutable audit log itself. |
| **Offline Lease**         | A bounded temporary authorization token signed via HMAC-SHA256, issued to a mobile device to perform safety-critical operations (like LOTO) offline within a safe time window. |
| **Command-Sourced Synchronization** | Architectural pattern where mobile clients synchronize atomic operational commands to a local queue (`SyncOutbox`) instead of final mutated states. |
| **Cryptographic Manual Override** | An exception for areas without network coverage, allowing technicians to manually bypass digital safety blocks after physical verification. |
| **LOTO Watchdog**         | A native background thread on the mobile device that continually monitors the safety heartbeat over WebSockets to trigger Fail-Safe actions. |
| **Preventive Security Lockout** | A fail-safe state triggered automatically by the LOTO Watchdog when the grace window expires without receiving a heartbeat. |
| **Grace Window**          | A defined time threshold (e.g., 30s) used by the LOTO Watchdog to tolerate RF Shadowing and AP roaming without generating false positive safety lockouts. |
| **Unit of Work**          | A transactional persistence pattern ensuring multiple database changes succeed or fail as a single atomic operation. |
| MAI (Moving Analog Indicator) | A visual pattern for continuous process variables (pressure, flow, etc.) that allows rapid condition evaluation without relying solely on numeric digits, conforming to ISA-101.01. |
| HPHMI                     | High-Performance Human-Machine Interface. Design philosophy prioritizing situational awareness, minimizing cognitive fatigue, and ensuring pre-attentive visibility of safety alarms. |
| Redundant Coding          | The practice of communicating critical states using multiple simultaneous channels (Shape + Icon + Color + Text) to guarantee accessibility, especially for color blindness. |
| Discrete Switching (UI)   | A UI interaction pattern requiring explicit taps (rather than continuous swipe/drag gestures) to toggle container states, necessary due to the low precision of capacitive sensors operated with industrial gloves. |
