---
code: DT-UC-TRC-001
version: 1.3
date: 2026-09-03
status: Vigente — Alcance MVP Segmentado y Casos de Uso Estandarizados
author: Juan David Julio Serrano
standard:
  - ISO 9001:2015
  - ISO 14224:2016
  - ISO 45001:2018
  - ISO 55001:2014
---
# Especificación de Casos de Uso y Matriz de Trazabilidad

Este documento constituye la **Única Fuente de Verdad (SSoT)** para la especificación y trazabilidad de los Casos de Uso del sistema Gemelo Digital EAM (DTEAM).

---

## Módulo de Operaciones de Mantenimiento (MTTO)

### Alcance MVP

| Caso de Uso (ID)    | Nombre del Caso de Uso (Acción / Objetivo)      | Historia de Usuario (ID) | Actor Principal            | Sustento Normativo / Invariante de Negocio                                                                                                 |
| :------------------ | :---------------------------------------------- | :----------------------- | :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| **[[UC-MTTO-001]]** | Programar Mantenimiento Preventivo              | [[MTTO-001]]             | Planificador               | **ISO 55001 (8.1):** Programación sistemática para evitar el desgaste acelerado y fallas catastróficas.                                    |
| **[[UC-MTTO-002]]** | Cerrar Orden de Trabajo con Taxonomía ISO 14224 | [[MTTO-002]]             | Técnico                    | **ISO 14224 (Sección 5):** Captura mandatoria de datos de falla (modo, causa y mecanismo) para indicadores de fiabilidad (MTBF).           |
| **[[UC-MTTO-023]]** | Programar Mantenimiento por Telemetría          | [[MTTO-023]]             | Planificador               | **ISO 13374 / CBM:** Planificación dinámica basada en el desgaste mecánico y uso real acumulado (horómetros).                              |
| **[[UC-MTTO-026]]** | Priorizar Backlog mediante RIME                 | [[MTTO-026]]             | Planificador               | **ISO 55001 (6.2.2) / ADR-002:** Priorización objetiva de recursos críticos delegada en estrategia RIME configurable.                      |
| **[[UC-MTTO-029]]** | Definir Límites de Activos                      | [[MTTO-029]]             | Ingeniero de Confiabilidad | **ISO 14224 (Sección 5.6):** Especificación mandatoria de los límites del equipo para evitar duplicidad de costos de mantenimiento.        |

### Casos de Uso Planificados para Fases Posteriores (Fuera del MVP)

| Caso de Uso (ID) | Nombre del Caso de Uso (Acción / Objetivo) | Historia de Usuario (ID) | Actor Principal | Sustento Normativo / Invariante de Negocio                                                                                                 |
| :--------------- | :----------------------------------------- | :----------------------- | :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| UC-MTTO-003      | Cargar Informe de Contratista (PDF)        | [[MTTO-003]]             | Contratista     | **ISO 55001 (8.3 - Outsourcing):** Control e integridad documental de los servicios ejecutados por terceros.                               |
| UC-MTTO-004      | Extraer Datos de Informe con IA            | [[MTTO-004]]             | Supervisor      | **ISO 55001 (7.5 - Requisitos de Información):** Ingesta y validación asíncrona de reportes para garantizar la calidad del dato maestro.   |
| UC-MTTO-020      | Visualizar Documentación Móvil             | [[MTTO-020]]             | Técnico         | **ISO 55001 (7.5):** Disponibilidad offline de manuales de fabricante y planos técnicos en el punto de trabajo.                            |
| UC-MTTO-028      | Consultar Chatbot RAG Técnico              | [[MTTO-028]]             | Técnico         | **ISO 55001 (7.2 - Competencia):** Asistencia interactiva de seguridad para evitar errores humanos de interpretación durante reparaciones. |
| UC-MTTO-030      | Gestionar Garantías de Activos             | [[MTTO-030]]             | Planificador    | **ISO 55001 (8.1 - Controles):** Validación de cobertura de proveedor antes de la ejecución de gastos internos de mantenimiento.           |

---

## Módulo de Control de Recursos (`INV`)

### Alcance MVP

| Caso de Uso (ID)   | Nombre del Caso de Uso (Acción / Objetivo) | Historia de Usuario (ID) | Actor Principal            | Sustento Normativo / Invariante de Negocio                                                                                                                    |
| :----------------- | :----------------------------------------- | :----------------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **[[UC-INV-005]]** | Crear Ficha Técnica de Activo              | [[INV-005]]              | Ingeniero de Proyectos     | **ISO 14224 (9.1a):** Alta de datos maestros para la identificación física unívoca de unidades de equipo (Nivel 6).                                           |
| **[[UC-INV-006]]** | Gestionar Movimientos de Inventario        | [[INV-006]]              | Jefe de Almacén            | **ISO 55001 (8.1 - Control):** Integridad transaccional (ingresos, egresos y devoluciones) para control real de stock y costo de OTs.                         |
| **[[UC-INV-007]]** | Validar y Activar Activos Nuevos           | [[INV-007]]              | Ingeniero de Confiabilidad | **ISO 55001 (8.1):** Control de calidad del catálogo antes de habilitar activos preliminares para operación comercial.                                        |
| **[[UC-INV-025]]** | Ejecutar Rotación de Activo                | [[INV-025]]              | Ingeniero de Proyectos     | **ISO 14224 (Sección 6 - Taxonomía):** Desacoplamiento físico-lógico: mueve el activo desmontado al almacén y vincula el reemplazo en la ubicación funcional. |
| **[[UC-INV-027]]** | Crear Ubicaciones Funcionales              | [[INV-027]]              | Ingeniero de Proyectos     | **ISO 14224 (Sección 6):** Modelación del árbol taxonómico (niveles 1-5) para retener el historial de la posición del proceso.                                |
| **[[UC-INV-031]]** | Gestionar Catálogo de Repuestos Maestro    | [[INV-031]]              | Jefe de Almacén            | **ISO 55001 (8.1):** Centralización técnica del Part Master usando códigos comoditizados (SKUs) para evitar duplicados en el catálogo.                        |

### Casos de Uso Planificados para Fases Posteriores (Fuera del MVP)

| Caso de Uso (ID) | Nombre del Caso de Uso (Acción / Objetivo) | Historia de Usuario (ID) | Actor Principal | Sustento Normativo / Invariante de Negocio                                                                                       |
| :--------------- | :----------------------------------------- | :----------------------- | :-------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| UC-INV-021       | Monitorear Reabastecimiento de Stock       | [[INV-021]]             | Jefe de Almacén | **ISO 55001 (7.5 - Planificación):** Gestión de compras técnicas automatizadas basadas en criticidad y repuestos clase A, B o C. |

---

## Módulo de Convergencia Gemelo Digital (`VIS`)

### Alcance MVP

| Caso de Uso (ID)   | Nombre del Caso de Uso (Acción / Objetivo)             | Historia de Usuario (ID) | Actor Principal | Sustento Normativo / Invariante de Negocio                                                                                                     |
| :----------------- | :----------------------------------------------------- | :----------------------- | :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| **[[UC-VIS-008]]** | Visualizar Capa de Permisos de Trabajo                 | [[VIS-008]]              | Inspector HSEQ  | **ISO 45001 (8.1):** Control visual de operaciones simultáneas (SIMOPS) para mitigar interferencias de alto riesgo.                            |
| **[[UC-VIS-011]]** | Verificar Rutas de Aislamiento (LOTO) y Bloqueo Activo | [[VIS-011]]              | Técnico         | **ISO 45001 (8.1) / ASR-2:** Bloqueo de software (fail-safe) que impide iniciar la ejecución si hay energía en campo o falla el latido de red. |
| **[[UC-VIS-033]]** | Inspeccionar Activos sobre el Plano Base 2D            | [[VIS-033]]              | Supervisor      | **ISO 55001 (7.5) / ISA-101.01 / ADR-001:** Lienzo base HPHMI 2D para concienciación situacional e inspección contextual en tiempo real.       |

### Casos de Uso Planificados para Fases Posteriores (Fuera del MVP)

| Caso de Uso (ID) | Nombre del Caso de Uso (Acción / Objetivo)     | Historia de Usuario (ID) | Actor Principal        | Sustento Normativo / Invariante de Negocio                                                                                     |
| :--------------- | :--------------------------------------------- | :----------------------- | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| UC-VIS-009       | Navegar Jerárquicamente con Zoom Semántico     | [[VIS-009]]              | Supervisor             | **HPHMI (Hollifield):** Estructura jerárquica de navegación por niveles (1-3) para mitigar fatiga de datos (UX).                 |
| UC-VIS-010       | Visualizar Despiece en 3D (Vista Explosionada) | [[VIS-010]]              | Técnico                | **ISO 55001 (7.5 - Accesibilidad) / ADR-001 (Fase 3D):** Despiece en 3D para reconocimiento espacial previo al desmontaje físico. |
| UC-VIS-012       | Configurar Jerarquía de Componentes 3D         | [[VIS-012]]              | Ingeniero de Proyectos | **ISO 55001 (7.5) / ADR-001 (Fase 3D):** Administración técnica de la correspondencia entre mallas 3D (`.glb`) y el árbol.     |

---

## Módulo de Seguridad y Gobernanza (`ADM`)

### Alcance MVP

| Caso de Uso (ID)   | Nombre del Caso de Uso (Acción / Objetivo) | Historia de Usuario (ID) | Actor Principal   | Sustento Normativo / Invariante de Negocio                                                                                               |
| :----------------- | :----------------------------------------- | :----------------------- | :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **[[UC-ADM-013]]** | Gestionar Roles y Permisos                 | [[ADM-013]]              | Administrador     | **ISO 55001 (5.3 - Roles):** Definición de autoridad y segregación de funciones (SoD) para evitar conflictos.                            |
| **[[UC-ADM-014]]** | Administrar Ciclo de Vida de Usuarios      | [[ADM-014]]              | Administrador     | **ISO 27001 (A.8.2 - IAM):** Ciclo seguro: inactividad por fuerza bruta, cifrado PBKDF2 y borrado lógico (soft-delete).                  |
| **[[UC-ADM-032]]** | Consultar Registro de Auditoría Inmutable  | [[ADM-032]]              | Auditor / Gerente | **ISO 27001 (A.8.15 - Registro) / ADR-003:** Trazabilidad criptográfica SHA-256 encadenada para asegurar la inalterabilidad de los logs. |

### Casos de Uso Planificados para Fases Posteriores (Fuera del MVP)

| Caso de Uso (ID) | Nombre del Caso de Uso (Acción / Objetivo) | Historia de Usuario (ID) | Actor Principal       | Sustento Normativo / Invariante de Negocio                                                                                               |
| :--------------- | :----------------------------------------- | :----------------------- | :-------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| UC-ADM-015       | Configurar Integración ERP                 | [[ADM-015]]              | Administrador         | **ISO 55001 (8.3 - Terceros):** Interoperabilidad industrial (MIMOSA) para flujos de inventario con Odoo/ERP.                            |
| UC-ADM-016       | Publicar Anuncios del Sistema              | [[ADM-016]]              | Administrador         | **ISO 55001 (7.3 - Concienciación):** Comunicación masiva de ventanas de mantenimiento para mitigar riesgos operativos.                  |
| UC-ADM-017       | Consultar Dashboard Ejecutivo de KPIs      | [[ADM-017]]              | Gerente de Planta     | **ISO 14224 (Anexo C):** Consolidación matemática de MTBF, MTTR e indisponibilidad para identificar "activos problema" (Pareto).         |
| UC-ADM-018       | Generar Reportes Ejecutivos PDF            | [[ADM-018]]              | Gerente de Planta     | **ISO 55001 (7.5 - Trazabilidad):** Exportación inmutable y compatible para análisis fuera de línea en comités directivos.               |
| UC-ADM-019       | Sincronizar Datos con Herramientas BI      | [[ADM-019]]              | Gerente de Planta     | **ISO 27001 (A.8.24 - Intercambio):** Exposición controlada (API OAuth 2.0 / rate-limiting) de datasets de confiabilidad para analítica. |
| UC-ADM-022       | Evaluar Sugerencias de Optimización (PMO)  | [[ADM-022]]              | Ing. de Confiabilidad | **ISO 55001 (10.2 - Mejora Continua):** Análisis histórico de fallas para evitar sobre-mantenimiento (CAPEX/OPEX).                       |
| UC-ADM-024       | Configurar Parámetros Generales            | [[ADM-024]]              | Administrador         | **ISO 55001 (7.5):** Parametrización de zona horaria y unidades de medida (ISO 80000) sin alterar el código base.                        |
