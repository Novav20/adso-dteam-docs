---
id: SCR-VIS-033
title: "Inspección de Activos sobre el Plano Base 2D"
module: VIS
isa101_level: "L1 (COP) | L3 (Detalle Activo)"
platform: Shared Component
target_device: Tablet Industrial | Desktop
roles:
  - "Supervisor de Mantenimiento"
  - "Técnico de Mantenimiento"
  - "Inspector HSEQ"
  - "Ingeniero de Confiabilidad"
user_stories:
  - "[[VIS-033]]"
use_cases:
  - "[[UC-VIS-033]]"
requirements:
  - "FR-598"
  - "FR-599"
  - "FR-600"
  - "FR-601"
  - "FR-602"
  - "NFR-603"
  - "NFR-604"
  - "NFR-605"
  - "TR-010"
  - "TR-011"
version: 1.0
date: 2026-09-03
status: Draft
---

# SCR-VIS-033: Inspección de Activos sobre el Plano Base 2D

## 1. Propósito y Contexto Operacional
* **Objetivo de la Vista:** Proporcionar una representación espacial interactiva en 2D de la planta o subsistema operativo, permitiendo la localización rápida de equipos, la evaluación de su condición en tiempo real mediante indicadores HPHMI y el despliegue de una ficha contextual para el lanzamiento de operaciones de mantenimiento y seguridad.
* **Contexto Operativo:** Utilizada tanto en salas de control sobre monitores de escritorio (Tema Claro, navegación con ratón y teclado) como en campo sobre tabletas industriales robustecidas (Tema Oscuro, interacción táctil con guantes de seguridad bajo condiciones de alta o baja iluminación).

---

## 2. Artefacto Visual

![[SCR-VIS-033-asset-inspection-card.svg]]

---

## 3. Inventario Funcional de Componentes

> Los estilos visuales, paletas neutras, elevaciones y dimensiones táctiles mínimas se rigen bajo [[DT-UI-DS-DOC-001-design-system-tokens|DT-UI-DS-DOC-001]]. Esta tabla especifica únicamente la semántica de interacción y enlace de datos.

| ID | Control / Componente | Contenido / Rol Visual | Token Semántico | Regla de Negocio / Comportamiento |
| :--- | :--- | :--- | :--- | :--- |
| `CMP-01` | Canvas Viewport 2D | Lienzo SVG interactivo | `--dt-color-bg-canvas` | Renderiza el plano vectorial del área seleccionada. Soporta paneo continuo y zoom dual (geométrico y semántico) a $\ge 30\text{ FPS}$ (`FR-598`, `NFR-605`). |
| `CMP-02` | Viewport Toolbar | Barra flotante de control | `--dt-color-surface-card` | Controles rápidos compactos: `[Restaurar Vista / Home]`, `[Zoom + / -]`, selector de capas (`Capas`) y distintivo de nivel actual (`L1: Visión General` / `L2: Bahía`). |
| `CMP-03` | Command Palette Trigger | Barra / Botón de búsqueda | `--dt-color-border-subtle` | Entrada rápida de texto o atajo global (`Ctrl + K` / `/`). Permite búsqueda difusa de activos por Tag o descripción técnica. |
| `CMP-04` | Equipment Hotspot | Símbolo de equipo en SVG | `--dt-color-surface-card` | Elemento gráfico Nivel 6 ISO 14224 vinculado unívocamente por `TagNumber` (`FR-599`). En estado normal se muestra en gris neutro; en alarma crítica resalta con halo y forma roja (`--dt-color-alarm-critical`). |
| `CMP-05` | Context Container | Panel Lateral / Bottom Sheet | `--dt-color-surface-card` | En escritorio: panel lateral derecho retráctil ($380\text{px}$) con elevación `--dt-z-overlay-card`. En móvil/tableta: lámina inferior deslizante (*Bottom Sheet*) accesible con el pulgar (`FR-600`). |
| `CMP-06` | Asset Header Block | Tag + Estado + Criticidad | `--dt-font-mono-data` | Muestra el Tag técnico en tipografía monoespaciada, estado operativo (`UP`, `DOWN`, `STANDBY`) mediante badge neutro, y nivel de criticidad (1-10) para el motor RIME. |
| `CMP-07` | Live Telemetry Block | Indicadores analógicos MAI | `--dt-color-mai-*` | Renderiza barras MAI para variables continuas críticas (presión, temperatura, vibración) con zona de operación normal y puntero neutro. Se actualiza vía SignalR en $<1\text{s}$ (`FR-601`, `NFR-604`). |
| `CMP-08` | Safety & Work Badges | Resumen de OTs y Seguridad | `--dt-color-state-info` | Indicadores compactos: número de OTs activas sobre el equipo, distintivo de Permiso de Trabajo vigente (`VIS-008`) y estado de aislamiento LOTO (`VIS-011`). |
| `CMP-09` | Quick Action Buttons | Botonera de acciones clave | `--dt-touch-target-mobile` | Accesos directos de ejecución: `[Ver Ruta LOTO]` (hacia `SCR-VIS-003`), `[Ver / Gestionar OTs]` (hacia `SCR-MTTO-004`) y `[Ficha Maestra]` (hacia `SCR-INV-001`). |

---

## 4. Matriz de Estados de la Pantalla

| Estado | Modificación Visual en la Interfaz | Condición de Activación |
| :--- | :--- | :--- |
| **Normal (Default)** | Lienzo y paneles en paleta neutra en escala de grises. Equipos en operación normal sin colores saturados. Controles habilitados. | Carga inicial completada y enlace de telemetría activo en rango seguro. |
| **Cargando (Loading)** | Indicador de carga atenuado sobre el lienzo central; esqueleto shimmer en el panel lateral de inspección. | Cambio de área funcional o recuperación inicial del plano SVG (`NFR-603`). |
| **Equipo Seleccionado** | El símbolo SVG del equipo activo resalta con contorno de selección azul informativo (`--dt-color-state-info`). Se despliega el panel `CMP-05`. | Clic / Tap sobre un hotspot en el plano o selección desde la Command Palette (`CMP-03`). |
| **Alarma Crítica de Activo** | El hotspot SVG adquiere borde rojo (`--dt-color-alarm-critical`) acompañado de un marcador cuadrado visible en L1. En la ficha, el indicador MAI muestra el símbolo '1' rojo. | Variable de proceso superando límites de seguridad funcional o equipo en paro no programado (`DOWN`). |
| **Pérdida de Telemetría (`AF-002`)** | Los valores del bloque `CMP-07` se congelan; se muestra un triángulo ámbar (`--dt-color-alarm-warning`) y el texto: *"Datos Desactualizados. Conexión Perdida"* con la hora del corte. | Caída de la conexión persistente SignalR / SCADA (`TR-010`). |
| **Activo Sin Mapeo (`AF-001`)** | El panel lateral muestra los datos tabulares del equipo, pero el botón *"Localizar en Plano"* se muestra deshabilitado con el distintivo: *"Mapeo Espacial Pendiente"*. | Búsqueda textual de un activo registrado en el catálogo maestro pero sin geometría asociada en el SVG actual. |

---

## 5. Reglas de Interacción y Flujo de Datos

### 5.1. Carga Inicial y Renderizado Espacial
1. Al acceder a la vista, el sistema consulta la configuración del plano correspondiente a la ubicación funcional seleccionada y renderiza el SVG base (`L1`).
2. El sistema recupera el catálogo de equipos de Nivel 6 correspondientes al área y asocia dinámicamente cada nodo gráfico (`svgElementId`) con su entidad física (`EquipmentUnit`) mediante su `TagNumber` (`FR-599`).
3. El plano se posiciona centrado con factor de escala base ($100\%$).

### 5.2. Navegación y Zoom Dual
1. **Interacción con Ratón / Gestual:** El usuario realiza paneo arrastrando el lienzo y zoom mediante rueda o pellizco multitáctil centrado en el cursor (`FR-598`).
2. **Conmutación por Zoom Semántico:**
   * Si la escala visual está alejada ($s < s_{\text{threshold}}$): El plano muestra únicamente las siluetas estructurales de los equipos y badges de alarma crítica.
   * Si la escala visual cruza el umbral cercano ($s \ge s_{\text{threshold}}$): Aparecen dinámicamente las etiquetas alfanuméricas de Tag, indicadores de sentido de flujo y puertos de instrumentación.

### 5.3. Inspección Contextual de Activo
1. El usuario hace clic o tap sobre el equipo `CMP-04` (o ejecuta la búsqueda rápida en `CMP-03` y presiona Enter).
2. El sistema centra suavemente la cámara sobre el equipo seleccionado ($<800\text{ms}$) y resalta su contorno.
3. Se despliega el panel contextual `CMP-05` (Sidebar en escritorio / Bottom Sheet en móvil).
4. El sistema establece la suscripción en tiempo real al canal de telemetría física del equipo (`TR-010`).
5. El panel consume las lecturas continuas del SCADA y refresca los indicadores analógicos móviles (`CMP-07`) con latencia $<1\text{s}$ sin provocar parpadeo ni recargar la interfaz (`FR-601`, `NFR-604`).

### 5.4. Lanzamiento de Operaciones
1. Desde el panel contextual, el usuario puede pulsar:
   * **`[Ver Ruta LOTO]`:** Abre la superposición gráfica de aislamiento de energía en el plano (`SCR-VIS-003` / `VIS-011`).
   * **`[Ver / Gestionar OTs]`:** Navega al backlog operativo filtrando las órdenes asociadas al activo (`SCR-MTTO-004`).
   * **`[Ficha Maestra]`:** Abre la vista completa de ingeniería y ciclo de vida del equipo (`SCR-INV-001`).

---

## 6. Consideraciones Industriales y de Seguridad

* **Filosofía HPHMI (ISA-101 / Hollifield):**
  * Cumplimiento estricto de la regla del 90/10. Ningún equipo operativo se dibuja en verde; el estado normal es neutro (`--dt-color-surface-card` / `--dt-color-border-subtle`).
  * Las alarmas reservan los únicos colores saturados y siempre van acompañadas de símbolos geométricos redundantes (Cuadrado para Crítica, Triángulo para Advertencia).
* **Ergonomía Táctil en Campo:**
  * En dispositivos móviles y tabletas, la lámina inferior (*Bottom Sheet*) permite la inspección con una sola mano mediante deslizamiento vertical.
  * Todos los botones de acción rápida (`CMP-09`) y elementos interactivos cumplen con el tamaño táctil industrial mínimo de $48 \times 48\text{ px}$ para uso con guantes.
* **Resiliencia de Telemetría (Fail-Safe):**
  * Ante la interrupción del flujo SCADA, el panel no oculta la información ni muestra valores en cero (lo cual falsearía lecturas de presión o temperatura); congela el último valor válido y aplica la advertencia de desactualización para evitar decisiones operativas sobre datos ciegos.