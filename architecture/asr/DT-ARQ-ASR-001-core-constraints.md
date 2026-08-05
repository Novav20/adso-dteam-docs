---
code: DT-ARQ-ASR-001
version: 1.0
date: 2026-06-10
status: Aprobado
author: Juan David Julio Serrano
---

# Requisitos Arquitectónicamente Significativos (ASRs)

## 1. Operación Offline-First (Tolerancia a Particiones)
*   **Origen:** [[TR-007]], [[MTTO-002]], [[INV-006]].
*   **Atributo de Calidad:** Tolerancia a Fallos / Disponibilidad.
*   **Impacto Arquitectónico:** Obliga a una topología distribuida. El cliente móvil debe incorporar una base de datos local (ej. SQLite) y una cola de sincronización. El backend debe exponer APIs idempotentes y manejar resolución de conflictos (Last-Write-Wins) basados en marcas de tiempo generadas offline.

## 2. Seguridad LOTO en Tiempo Real y Fail-Safe (Disponibilidad y Consistencia)
*   **Origen:** [[TR-010]], [[VIS-011]], NFR-229, NFR-238.
*   **Atributo de Calidad:** Seguridad Funcional (Safety) / Tiempo Real.
*   **Impacto Arquitectónico:** Exige una capa de comunicación persistente (WebSockets/PubSub) independiente de las peticiones HTTP estándar, para propagar lecturas de telemetría y revocaciones de permisos en sub-segundos. Incluye la excepción de "Anulación Manual Criptográfica" para zonas sin cobertura de red, garantizando el principio *Fail-Safe* sin bloquear la operación crítica validada físicamente.

## 3. Registro de Auditoría Inmutable (Cumplimiento)
*   **Origen:** [[TR-001]], [[ADM-032]], FR-347, FR-351.
*   **Atributo de Calidad:** No Repudio / Auditabilidad.
*   **Impacto Arquitectónico:** Impide almacenar registros de auditoría en tablas transaccionales estándar con permisos de escritura total. Obliga a establecer un límite de almacenamiento de solo adición (*append-only*), implementado en el MVP mediante el aislamiento de roles en PostgreSQL (Row-Level Security) y validación de integridad por *hashing* criptográfico.

## 4. Kernel Transaccional de Taxonomía (Integridad de Datos)
*   **Origen:** [[TR-008]], [[INV-027]], [[MTTO-029]], FR-414, FR-417.
*   **Atributo de Calidad:** Consistencia Estructural.
*   **Impacto Arquitectónico:** La jerarquía ISO 14224 (9 niveles) requiere validaciones de grafos (prevención de ciclos y control de profundidad) en menos de 500ms. Esto fuerza a centralizar la lógica de taxonomía en un contexto delimitado (*Bounded Context*) estricto, utilizando extensiones de bases de datos jerárquicas (ej. `ltree` en PostgreSQL) para prevenir que reglas de negocio complejas se dispersen por la capa de aplicación.