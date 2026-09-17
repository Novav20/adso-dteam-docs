---
id: SCR-VIS-008
title: Plano General de Planta con Capa de Permisos de Trabajo (SIMOPS)
module: VIS
isa101_level: L1 (COP - Visión General)
platform: Shared Component
target_device: Tablet Industrial | Desktop
roles:
  - Inspector HSEQ
  - Supervisor de Mantenimiento
user_stories:
  - "[[VIS-008]]"
use_cases:
  - "[[UC-VIS-008]]"
requirements:
  - FR-182
  - FR-183
  - FR-184
  - FR-185
  - FR-186
  - FR-187
  - FR-188
  - NFR-190
  - NFR-193
  - "[[TR-010]]"
  - "[[TR-011]]"
version: 1.0
date: 2026-09-05
status: Draft
---

# SCR-VIS-008: Plano General de Planta con Capa de Permisos de Trabajo (SIMOPS)

## 1. Propósito y Contexto Operacional
* **Objetivo de la Vista:** Proporcionar una visión macroespacial (Plot Plan) de las Ubicaciones Funcionales de la planta industrial. Permite a los inspectores de seguridad activar una capa visual de Permisos de Trabajo (PTW) para detectar cruces operacionales peligrosos (SIMOPS) y orfandad de permisos.
* **Contexto Operativo:** Uso crítico en terreno por personal HSEQ con tabletas industriales para rondas de auditoría de contratistas, o en oficina central de permisos para aprobación en escritorio.

---

## 2. Artefacto Visual

![[SCR-VIS-008-simops-layer.svg]]

---

## 3. Inventario Funcional de Componentes

> Hereda estilos, elevaciones y codificación de alarmas de [[DT-UI-DS-DOC-001]].

| ID       | Control / Componente    | Rol Visual / Contenido     | Token Semántico             | Enlace de Datos / Regla de Comportamiento                                                                                                                        |
| :------- | :---------------------- | :------------------------- | :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CMP-01` | L1 Plot Plan Canvas     | Lienzo SVG de planta macro | `--dt-color-bg-canvas`      | Renderiza polígonos que representan Ubicaciones Funcionales (Niveles 1 al 4 de ISO 14224), no tuberías individuales.                                             |
| `CMP-02` | Viewport Toolbar        | Barra de navegación        | `--dt-color-surface-card`   | Controles de visor. El botón `[≡ Capas]` está activado y resaltado (`--dt-color-state-info`).                                                                    |
| `CMP-03` | User Avatar Widget      | Control de perfil          | `--dt-color-surface-card`   | Botón circular flotante (esquina superior derecha). Despliega menú contextual del usuario activo.                                                                |
| `CMP-04` | Functional Zone Polygon | Zona en el SVG             | `--dt-color-border-subtle`  | Representa un área (ej. *Tanques de Crudo*). En estado normal tiene borde sutil y fondo transparente.                                                            |
| `CMP-05` | PTW Overlay Badges      | Iconos de permisos activos | Matriz de Seguridad         | Superpuestos sobre los polígonos `CMP-04`. Aplican codificación redundante obligatoria.                                                                          |
| `CMP-06` | Popover / Tooltip       | Tarjeta emergente de PTW   | `--dt-color-surface-raised` | Se despliega al hacer clic sobre un `CMP-05`. Muestra: Tipo, Contratista, HSEQ, Horario y Estado (`FR-184`). Elevación: `--dt-z-overlay-card`.                   |
| `CMP-07` | SIMOPS Integrity Panel  | Panel de alertas huérfanas | `--dt-color-surface-card`   | Panel lateral/Bottom Sheet. Se activa solo si existen permisos aprobados cuyos Tags no existen en el lienzo gráfico (`FR-185`).                                  |
| `CMP-08` | Filter Chips            | Botonera de filtrado PTW   | `--dt-color-surface-base`   | Fila de chips flotantes en la base del lienzo: `[Caliente]`, `[Alturas]`, `[Confinado]`, `[Eléctrico]`. Permite aislar visualmente tipos de permisos (`FR-188`). |

---

## 4. Matriz de Estados de la Pantalla

| Estado | Modificación Visual en la Interfaz | Condición de Activación |
| :--- | :--- | :--- |
| **Normal (Capa Inactiva)** | El lienzo muestra las zonas en escala de grises neutra sin distintivos superpuestos. | El usuario desactiva el switch/botón de "Capa PTW". |
| **Capa PTW Activa** | Aparecen los íconos `CMP-05` sobre sus respectivas zonas geográficas. | Activación del botón de Capas en `CMP-02`. |
| **Permiso Seleccionado** | El icono `CMP-05` resalta su contorno y se abre la tarjeta flotante `CMP-06` junto al icono, sin oscurecer el resto de la planta. | Clic/Tap sobre un icono de permiso en el lienzo. |
| **Orfandad Detectada (SIMOPS Alert)** | Se abre el panel `CMP-07` forzosamente, destacando en rojo (`--dt-color-alarm-critical`) la cantidad de permisos rotos. | Carga inicial detecta inconsistencia referencial o SignalR envía permiso sin coordenadas. |
| **Pérdida de Sincronización** | Banner ámbar (`--dt-color-alarm-warning`) indica "Operando con datos cacheados". Los íconos PTW se mantienen visibles pero atenuados. | Pérdida de conexión con SignalR / Servidor. |

---

## 5. Reglas de Interacción y Flujo de Datos

### 5.1. Renderizado de Capa Espacial
1. Al cargar la vista L1, el sistema dibuja las Ubicaciones Funcionales.
2. Si el selector de Capa PTW está activo, el sistema consulta los `WorkPermits` en estado `APPROVED`.
3. El sistema cruza el `EquipmentUnitId` de cada permiso con los polígonos dibujados para posicionar los iconos de seguridad (`FR-185`).

### 5.2. Panel de Integridad (Fallos de Visualización)
1. Si un `WorkPermit` apunta a un activo que no posee `MeshMapping` en este plano, el permiso se clasifica como Huérfano.
2. El icono NO se dibuja arbitrariamente en el plano. En su lugar, se inyecta en el panel lateral `CMP-07` ("Fallos de Visualización").
3. El Inspector HSEQ debe procesar la lista del panel `CMP-07` para reasignar o resolver las inconsistencias geométricas (`FR-186`).

### 5.3. Sincronización en Tiempo Real
1. La vista se suscribe a los eventos de dominio de Permisos de Trabajo mediante SignalR (`TR-010`).
2. Cuando un contratista revoca o finaliza un permiso, el icono `CMP-05` desaparece del plano en $< 5\text{s}$ sin requerir que el inspector refresque la página (`FR-187`).

---

## 6. Consideraciones Industriales y de Seguridad

* **Conciencia Situacional SIMOPS:** El diseño del popover `CMP-06` está restringido en tamaño para que, al inspeccionar un Permiso en Caliente, el inspector siga viendo si hay un Permiso de Espacio Confinado a pocos metros en el lienzo de fondo.
* **Ergonomía de Filtrado:** El panel de `Filter Chips` (`CMP-08`) no requiere navegación por menús desplegables; los operadores con guantes pueden activar o apagar categorías de riesgo con un solo toque directo en la base de la pantalla.