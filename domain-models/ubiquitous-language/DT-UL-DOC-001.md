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
