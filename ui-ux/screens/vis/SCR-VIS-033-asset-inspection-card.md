---
id: SCR-VIS-033
title: Inspección de Activos sobre el Plano Base 2D
module: VIS
isa101_level: L1 (COP) | L3 (Detalle Activo)
platform: Shared Component
target_device: Tablet Industrial | Desktop
roles:
  - Supervisor de Mantenimiento
  - Técnico de Mantenimiento
  - Inspector HSEQ
  - Ingeniero de Confiabilidad
user_stories:
  - "[[VIS-033]]"
use_cases:
  - "[[UC-VIS-033]]"
requirements:
  - FR-598
  - FR-599
  - FR-600
  - FR-601
  - FR-602
  - NFR-603
  - NFR-604
  - NFR-605
  - "[[TR-010]]"
  - "[[TR-011]]"
version: 1.2
date: 2026-09-03
status: In Review
---

# SCR-VIS-033: Inspección de Activos sobre el Plano Base 2D

## 1. Propósito y Contexto Operacional
* **Objetivo de la Vista:** Visualización espacial interactiva de la planta o subsistema en 2D, permitiendo la localización de equipos, consulta de condición en tiempo real bajo filosofía HPHMI y despliegue de la ficha contextual de operaciones.
* **Contexto Operativo:** Desplegada en consolas web de escritorio (Tema Claro) y en tabletas industriales de campo (Tema Oscuro con ergonomía táctil apta para uso con guantes).
* **Modo de Operación:** Supervisión, diagnóstico visual y navegación contextual pasiva. La interfaz no emite comandos de control industrial (arranque/parada), no altera variables de proceso ni ejecuta maniobras remotas sobre el SCADA.

---

## 2. Artefacto Visual

![[SCR-VIS-033-asset-inspection-card.svg]]

---

## 3. Inventario Funcional de Componentes

> La grilla base, tipografía, paletas neutras y áreas de contacto táctil mínimas se heredan de [[DT-UI-DS-DOC-001-design-system-tokens|DT-UI-DS-DOC-001]]. Esta tabla define exclusivamente los componentes presentes, sus tokens semánticos y el enlace con el modelo.

| ID       | Control / Componente    | Rol Visual / Contenido           | Token Semántico                                                                                                                  | Enlace de Datos / Regla de Comportamiento                                                                                                                                                                                       |
| :------- | :---------------------- | :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `CMP-01` | Canvas Viewport 2D      | Lienzo vectorial SVG interactivo | `--dt-color-bg-canvas`                                                                                                           | Renderiza el plano SVG del área. Soporta paneo continuo y zoom dual (geométrico y semántico) según [[UC-VIS-033]].                                                                                                              |
| `CMP-02` | Viewport Toolbar        | Barra de navegación espacial     | `--dt-color-surface-card`                                                                                                        | Controles de visor: Restablecer vista, niveles de zoom, selector de capas y badge de nivel contextual.                                                                                                                          |
| `CMP-03` | Command Palette Trigger | Acceso a búsqueda rápida         | `--dt-color-border-subtle`<br>`--dt-color-text-muted`                                                                            | Disparador de búsqueda difusa global (`Ctrl + K` / `/`) en escritorio. En móvil se renderiza como botón de acción táctil ($\ge 48\text{px}$) con icono de lupa.                                                                 |
| `CMP-04` | Equipment Hotspot       | Símbolo de equipo en SVG         | `--dt-color-surface-card`                                                                                                        | Geometría de Nivel 6 vinculada unívocamente por `TagNumber` (FR-599). En condición normal opera en gris neutro; en alarma adquiere halo y forma de severidad según [[DT-UI-DS-DOC-001-design-system-tokens\|DT-UI-DS-DOC-001]]. |
| `CMP-05` | Context Container       | Panel contextual de activo       | `--dt-color-surface-raised`                                                                                                      | Contenedor adaptable (Panel lateral o *Bottom Sheet*). Elevación: `--dt-z-overlay-card`.                                                                                                                                        |
| `CMP-06` | Asset Header Block      | Identificación y estado          | `--dt-font-mono-data`                                                                                                            | Presenta `TagNumber`, criticidad para priorización ([[ADR-002-RIME-MVP-Static-Factors\|ADR-002]]) y estado operativo según `EquipmentUnit.operationalStatus` ([[DT-DM-DOC-001-domain-model-specification\|DT-DM-DOC-001]]).     |
| `CMP-07` | Live Telemetry Block    | Indicadores analógicos MAI       | `--dt-color-mai-*`                                                                                                               | Barras analógicas para variables de proceso críticas ([[DT-UI-DS-DOC-001-design-system-tokens\|DT-UI-DS-DOC-001]]). Se actualiza dinámicamente vía SignalR ([[TR-010]]).                                                        |
| `CMP-08` | Safety & Work Badges    | Indicadores de trabajo y riesgo  | [[DT-UI-DS-DOC-001-design-system-tokens#6.2. Matriz de Codificación Redundante para Permisos y LOTO        \| DT-UI-DS-DOC-001]] | Consume datos de Permisos y LOTO aplicando codificación redundante obligatoria.                                                                                                                                                 |
| `CMP-09` | Quick Action Buttons    | Botonera de acciones primarias   | `--dt-color-surface-base`<br>`--dt-color-text-primary`                                                                           | Enlaces de navegación rápida: `[Ver Ruta LOTO]` $\to$ SCR-VIS-011, `[Ver OTs]` $\to$ SCR-MTTO-026, `[Ficha Maestra]` $\to$ SCR-INV-005.                                                                                         |


---

## 4. Matriz de Estados de la Pantalla

| Estado                       | Modificación Visual en la Interfaz                                                                                                        | Condición de Activación                                                                                                  |
| :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **Normal (Default)**         | Superficies y activos en paleta neutra en escala de grises. Telemetría dentro de rangos operativos normales.                              | Carga exitosa del área y flujo de datos activo sin alarmas.                                                              |
| **Cargando (Loading)**       | Indicador de actividad atenuado sobre el lienzo; esqueleto visual (*shimmer*) en el panel contextual.                                     | Transición de área funcional o recuperación inicial del plano SVG.                                                       |
| **Activo Seleccionado**      | El equipo activo resalta con borde de selección informativo (`--dt-color-state-info`). Se despliega `CMP-05`.                             | Clic / Tap sobre `CMP-04` o selección mediante `CMP-03`.                                                                 |
| **Alarma Crítica de Activo** | `CMP-04` adquiere borde y símbolo cuadrado en `--dt-color-alarm-critical`. En `CMP-07` el MAI muestra marcador de severidad P1.           | Variable física excediendo umbrales de seguridad o equipo en condición `DOWN`.                                           |
| **Pérdida de Telemetría**    | Los valores en `CMP-07` se congelan; se muestra icono de advertencia ámbar (`--dt-color-alarm-warning`) y marca de tiempo de desconexión. | Interrupción de la conexión en tiempo real con la fuente SCADA ([[UC-VIS-033]], `AF-002`).                               |
| **Mapeo Pendiente**          | `CMP-05` presenta la información tabular del activo pero deshabilita la acción de localización espacial con badge informativo.            | Consulta de un equipo del catálogo maestro que carece de geometría asociada en el SVG actual ([[UC-VIS-033]], `AF-001`). |

---

## 5. Reglas de Interacción y Flujo de Datos

### 5.1. Carga Inicial
1. El sistema recupera el plano vectorial correspondiente a la ubicación funcional y renderiza el lienzo base.
2. Se vinculan bidireccionalmente los nodos gráficos interactivos con las entidades de equipo registradas (FR-599).
3. El plano se inicializa centrado en su vista macro.

### 5.2. Navegación Espacial y Ergonomía Móvil
1. **Desplazamiento y Zoom:** Navegación dual (Geométrica y Semántica) según [[UC-VIS-033]].
2. **Controlabilidad Táctil:** El contenedor `CMP-05` conmuta sus estados mediante un disparador gráfico superior que hereda el tamaño táctil de `--dt-touch-target-mobile`.
3. **Responsive Layout:** La transformación del contenedor `CMP-05` (Bottom Sheet $\leftrightarrow$ Lateral Panel) se delega a las reglas de orientación de dispositivo definidas en [[DT-UI-NAV-DOC-001-navigation-specification|DT-UI-NAV-DOC-001]].
  
### 5.3. Inspección y Telemetría
1. La selección de un activo en el plano invoca la apertura de `CMP-05` y la suscripción en tiempo real al canal de telemetría del equipo.
2. **Gestión de Suscripción SignalR:** Sujeta a políticas globales de *debouncing* para prevenir colisiones de red por selección rápida múltiple ([[DT-ARQ-CMP-DOC-001-architecture-interfaces-specification|DT-ARQ-CMP-DOC-001]]).
3. **Resiliencia de Conexión:** Si el componente detecta violación del umbral del *Heartbeat* o recibe un paquete con calidad "Bad" ([[DT-ARQ-DEP-DOC-001-deployment-specification|DT-ARQ-DEP-DOC-001]]), transiciona inmediatamente a la visualización de "Pérdida de Telemetría".
---

## 6. Consideraciones Industriales y de Seguridad

* **Filosofía HPHMI ([[TR-011]]):** Se prohíbe el uso de color verde para denotar funcionamiento normal. La interfaz permanece estrictamente en escala de grises neutra; los colores saturados se reservan para condiciones de alarma y advertencia con codificación de forma redundante.
* **Resiliencia de Telemetría:** Ninguna variable sin marca de tiempo confirmada puede presentarse como lectura viva. La interfaz distingue explícitamente entre una lectura real de valor cero y la desconexión del instrumento.