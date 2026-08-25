---
code: DT-ARQ-ASR-001
version: 1.1
date: 2026-08-25
status: Aprobado
author: Juan David Julio Serrano
---

# Requisitos Arquitectónicamente Significativos (ASRs)

## 1. Operación Offline-First y Tolerancia a Particiones
*   **Origen:** [[TR-007]], [[MTTO-002]], [[INV-006]].
*   **Atributo de Calidad:** Tolerancia a Fallos / Disponibilidad.
*   **Impacto Arquitectónico:** Obliga a una topología distribuida. El cliente móvil debe incorporar un motor de base de datos local relacional y una cola de sincronización transaccional. El sistema central debe exponer APIs idempotentes y gestionar la resolución de conflictos bajo el principio *Last-Write-Wins*, basándose en marcas de tiempo generadas durante la operación sin conexión.

## 2. Seguridad LOTO en Tiempo Real y Falla Segura
*   **Origen:** [[TR-010]], [[VIS-011]], NFR-229, NFR-238.
*   **Atributo de Calidad:** Seguridad Funcional (Safety) / Tiempo Real.
*   **Impacto Arquitectónico:** Exige una capa de comunicación persistente (WebSockets/PubSub) independiente de las peticiones HTTP estándar, para propagar lecturas de telemetría y revocaciones de permisos en sub-segundos. Incluye la excepción de "Anulación Manual Criptográfica" para zonas sin cobertura de red, garantizando el principio de falla segura sin bloquear la operación crítica que ya ha sido validada físicamente.

## 3. Registro de Auditoría Inmutable
*   **Origen:** [[TR-001]], [[ADM-032]], FR-347, FR-351.
*   **Atributo de Calidad:** No Repudio / Auditabilidad.
*   **Impacto Arquitectónico:** Impide almacenar registros de auditoría en tablas transaccionales estándar con permisos de escritura total. Obliga a establecer un límite de almacenamiento de solo inserción, implementado en el MVP con el aislamiento de roles en PostgreSQL mediante seguridad a nivel de fila (*Row-Level Security*) y la validación de integridad mediante dispersión criptográfica encadenada (SHA-256).

## 4. Núcleo Transaccional de Taxonomía
*   **Origen:** [[TR-008]], [[INV-027]], [[MTTO-029]], FR-414, FR-417.
*   **Atributo de Calidad:** Consistencia Estructural.
*   **Impacto Arquitectónico:** La jerarquía de la norma ISO 14224 abarca 9 niveles distribuidos transversalmente en el modelo de dominio: las Ubicaciones Funcionales gobiernan los Niveles 1 al 5, las Unidades de Equipo el Nivel 6, las Subunidades y los Ítems Mantenibles los Niveles 7 y 8, y el Catálogo de Repuestos el Nivel 9. Esta distribución requiere validaciones de grafos (prevención de ciclos y control de anidamiento jerárquico) en menos de 500 ms. Esto obliga a centralizar la lógica de taxonomía en un contexto delimitado (*Bounded Context*) estricto, utilizando extensiones de bases de datos jerárquicas (ej. `ltree` en PostgreSQL) para prevenir que reglas de negocio complejas se dispersen por la capa de aplicación.