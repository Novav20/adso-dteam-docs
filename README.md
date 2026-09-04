# DTEAM — Digital Twin Enterprise Asset Management

Hub canónico de documentación técnica y arquitectura para la plataforma **DTEAM**, orientada al sector industrial Oil & Gas.

---

## 1. Visión del Sistema
DTEAM es una plataforma de gestión de activos de alta criticidad que integra la gobernanza de mantenimiento industrial, control de recursos físicos, monitoreo de condición pasivo IoT y visualización esquemática espacial. 

El sistema está diseñado bajo el cumplimiento estricto de estándares internacionales:
* **ISO 55001:2014:** Gestión estratégica de activos, priorización de riesgo y toma de decisiones.
* **ISO 14224:2016:** Taxonomía de 9 niveles, límites de equipo (*boundaries*) y captura estandarizada de fallas para confiabilidad (MTBF/MTTR).
* **ISO 45001:2018 / OSHA:** Seguridad operacional, control de operaciones simultáneas (SIMOPS) y aseguramiento de Energía Cero (LOTO Fail-Safe).
* **ISO 27001:2022:** Control de acceso granular (RBAC/SoD) y registro de auditoría inmutable mediante encadenamiento criptográfico SHA-256 (ADR-003).
* **ANSI/ISA-101.01-2015 / IEC 63303:** Interfaces de operador de alto desempeño (HPHMI) en escala de grises neutra y despliegue jerárquico L1 a L4.

---

## 2. Stack Tecnológico
Conforme a la decisión de arquitectura **[[ADR-004]]** y la matriz de trazabilidad **[[DT-ARQ-TECH-001]]**, el software se implementa bajo un ecosistema unificado en **.NET**:

* **Backend:** Monolito Modular en .NET 10 estructurado con Arquitectura Hexagonal (*Ports & Adapters*) y Domain-Driven Design (DDD).
* **Base de Datos Central:** PostgreSQL 18 + extensión TimescaleDB (series de tiempo para telemetría) + extensión `ltree` (árbol taxonómico ISO 14224).
* **Cliente Móvil de Campo:** .NET MAUI Blazor Hybrid (Android/iOS) con persistencia local relacional cifrada vía `sqlite-net-pcl` con SQLCipher (Offline-First).
* **Cliente Web Administrativo:** Blazor Web App para supervisión HSEQ, planificación de backlog y tableros de control en estaciones de escritorio.
* **Librería de Componentes:** Componentes Razor compartidos en una Razor Class Library (RCL) que consumen los tokens del Design System.
* **Tiempo Real:** SignalR sobre WebSockets (WSS TLS 1.3) para latido de seguridad LOTO (2s) y transmisión de telemetría de proceso.
* **Ingesta IoT:** Azure IoT Hub consumiendo telemetría industrial vía MQTT desde SCADA y exponiéndola al backend vía AMQP.
* **Lienzo Gráfico:** Estrategia 2D-First basada en planos vectoriales interactivos SVG ([[ADR-001]]) con evolución hacia modelos 3D.

---

## 3. Estructura del Repositorio

```text
adso-dteam-docs/
├── architecture/         # Vistas C4 (Componentes y Despliegue), ASRs, ADRs y Matriz de Stack
│   ├── adr/              # Architecture Decision Records (ADR-001 a ADR-004)
│   ├── asr/              # Architecturally Significant Requirements (ASR-001)
│   ├── patterns/         # Catálogo de patrones GoF y tácticas DDD aplicadas
│   └── views/            # Modelos C4 de Componentes (CMP) y Despliegue Físico (DEP)
├── business-processes/   # Flujos de procesos operativos BPMN 2.0 (Draw.io)
├── compliance/           # Escudo normativo y justificaciones de cumplimiento ISO 14224 / ISO 55001
├── domain-models/        # Modelado táctico DDD, diagramas de actividad y Casos de Uso
│   ├── activity/         # Diagramas de actividad UML para flujos críticos (LOTO, Preventivo)
│   ├── class/            # Especificación del modelo de dominio, entidades y métodos DDD
│   ├── entity-relationship/ # Modelos conceptual y lógico de base de datos relacional
│   └── use-cases/        # Casos de uso formales y Matriz Maestra de Trazabilidad (DT-UC-TRC-001)
├── requirements/         # Requisitos de software y fuentes maestras
│   ├── common/           # Requisitos Transversales de Dominio y Plataforma (TR-001 a TR-011)
│   ├── data/             # Catálogos maestros sincronizados en CSV (actores, SRS, historias)
│   ├── interviews/       # Transcripciones de elicitación y entrevistas de campo
│   └── user-stories/     # Historias de usuario detalladas por módulo (ADM, INV, MTTO, VIS)
├── scripts/              # Herramientas de generación documental y auditoría de coherencia
└── ui-ux/                # Diseño de interfaz de usuario y arquitectura de información
    ├── assets/           # Archivos CSS (tokens.css), gráficos MAI (SVG) y wireframes
    ├── screens/          # Blueprints técnicos de especificación de pantalla (SCR-*.md)
    ├── DT-UI-DS-DOC-001  # Tokens de Diseño, HPHMI y Guía de Estilo Visual
    └── DT-UI-NAV-DOC-001 # Especificación de Navegación Global y Guardas de Seguridad
```

---

## 4. Ecosistema de Desarrollo
El proyecto opera bajo dos repositorios complementarios:
1. **`adso-dteam-docs` (Este repositorio):** Especificaciones de diseño, modelos formales, contratos de interfaz y escudo normativo.
2. **`adso-dteam-code` (En preparación):** Código fuente, pruebas unitarias/integración y pipelines de CI/CD.

---

## 5. Control Documental
Todos los artefactos técnicos aplican control de versiones bajo la norma **ISO 9001:2015**. Los cambios arquitectónicos requieren la aprobación del Arquitecto de Software y deben formalizarse mediante un nuevo registro ADR o la actualización justificada de las matrices de trazabilidad.