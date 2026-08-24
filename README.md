# Gemelo Digital EAM (Enterprise Asset Management)

Este repositorio constituye el **Hub Técnico de Documentación** (Docs-as-Code) para el proyecto de desarrollo de un sistema de gestión de activos industriales basado en conceptos de Gemelo Digital.

## Visión
El Gemelo Digital EAM es una plataforma diseñada bajo los estándares de ingeniería **ISO 55001** (Gestión de Activos) e **ISO 14224** (Taxonomía de Mantenimiento). El objetivo es proporcionar una gestión de activos robusta, auditable y escalable, integrando datos de sensores, modelos 3D y lógica de mantenimiento predictivo.

Este repositorio es la "Fuente de Verdad" para el diseño, la arquitectura y el cumplimiento normativo antes y durante la fase de implementación.

## Stack Tecnológico del Sistema (Objetivo)
Los artefactos documentados aquí están diseñados para una implementación basada en:
- **Backend:** .NET 10 (C#).
- **Frontend:** .NET MAUI Blazor Hybrid.
- **Base de Datos:** PostgreSQL + TimescaleDB  & SQLite.
- **Infraestructura:** Azure IoT Hub & Cloud Services.
- **Visualización:** Modelos 3D (Patrón Sidecar).

## Estructura del Repositorio
| Carpeta | Propósito |
| :--- | :--- |
| `bpmn/` | Modelos de procesos de negocio (ej. ciclos de mantenimiento) que definen la lógica operativa core. |
| `domain-models/` | Modelos conceptuales del software, incluyendo diagramas de clases y casos de uso de alta fidelidad. |
| `compliance/` | Escudo normativo: mapeos y justificaciones de cumplimiento con ISO 14224/55001. |
| `architecture/` | Registros de decisiones de arquitectura (ADR) y definiciones de infraestructura. |
| `assets/` | Recursos suplementarios: esquemas de base de datos (CSV), transcripciones de entrevistas y datos de requisitos. |

## Ecosistema del Proyecto
Para mantener la limpieza y profesionalismo del desarrollo, el proyecto se divide en dos frentes:
1.  **`adso-gemelo-digital-docs` (Este repo):** Documentación técnica, modelos y diseño.
2.  **`adso-gemelo-digital-code` (Próximamente):** Código fuente, pruebas unitarias y despliegue.

## Cómo Colaborar
Las contribuciones técnicas deben seguir las guías de estilo de PlantUML y BPMN 2.0. Para más detalles, consulte el archivo (próximamente) `CONTRIBUTING.md`.

---
*Este repositorio está enfocado en la excelencia de ingeniería y la documentación dirigida por estándares.*
