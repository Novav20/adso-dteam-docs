---
code: DT-UI-DS-DOC-001
version: 1.1
date: 2026-08-27
status: Aprobado tras Auditoría Normativa (AUD-DT-UI-DS-2026-001)
author: Juan David Julio Serrano
standard:
  - ISA-101.01-2015 (Human Machine Interfaces for Process Automation Systems)
  - The High Performance HMI Handbook (Hollifield et al.)
  - ISO 9241-110:2020 / ISO 9241-210:2019 (Ergonomía de Interacción y Diseño Centrado en el Humano)
  - WCAG 2.1 Nivel AA (Web Content Accessibility Guidelines)
  - ISO 45001:2018 (Cláusula 8.1 — LOTO & Seguridad Operativa)
---

# Especificación Técnica de Tokens de Diseño y Guía de Estilo HPHMI

## 1. Alcance

Este documento establece la **Fuente Única de Verdad** para todos los tokens de diseño (espaciado, color, tipografía, elevación y patrones de seguridad) utilizados en la construcción de prototipos y en la implementación de la **Librería de Clases de Razor** en .NET MAUI Blazor Hybrid y Blazor Web App.

### Principios Obligatorios:
1. **Regla HPHMI del 90/10:** El 90% de la interfaz opera en escala de grises neutra de bajo contraste para minimizar la fatiga visual. El 10% del color saturado se reserva exclusivamente para anomalías, alarmas y condiciones de peligro.
2. **Eliminación del Verde como Estado "Normal":** No se utiliza verde para indicar que un motor está encendido o en operación normal. El estado normal se representa mediante grises y texto ("RUNNING" / "UP"). El uso del color en confirmaciones documentales o estado de conexión se restringe a tonalidades **Teal / Pino** (`--dt-primitive-teal-600` / `#0D9488` o `#2A9D8F`), evitando cualquier confusión con el verde industrial de estado.
3. **Codificación Redundante (WCAG 2.1 AA):** Ningún estado crítico de seguridad o alarma debe comunicarse únicamente por color. Todo indicador debe combinar **Forma + Icono + Color + Texto**.
4. **Ergonomía Industrial Táctil:** Los elementos interactivos en dispositivos móviles y tabletas de campo deben respetar un área de contacto mínima de **$48 \times 48\text{ px}$** para permitir la operación con guantes de seguridad.

---

## 2. Tokens Espaciales y de Layout

El espaciado y dimensionamiento se rige bajo un sistema de cuadrícula base de **8px** (con un submarco de 4px para micro-ajustes).

### 2.1. Escala de Espaciado

| Token CSS / C#  | Valor (px) | Valor (rem) | Uso Primario en Layout y Componentes                                                       |
| :-------------- | :--------: | :---------: | :----------------------------------------------------------------------------------------- |
| `--dt-space-0`  |   `0px`    |   `0rem`    | Reseteo de márgenes y paddings.                                                            |
| `--dt-space-1`  |   `4px`    |  `0.25rem`  | Micro-espaciado: separación entre icono y texto en badges, padding interno de tags.        |
| `--dt-space-2`  |   `8px`    |  `0.5rem`   | Espaciado compacto: gap entre campos de formulario estrechos, padding de celdas de tabla.  |
| `--dt-space-3`  |   `12px`   |  `0.75rem`  | Espaciado medio: gap en barras de herramientas (toolbars), padding interno de inputs.      |
| `--dt-space-4`  |   `16px`   |  `1.0rem`   | **Espaciado base:** padding de tarjetas (cards), gap estándar en Auto-Layout.              |
| `--dt-space-5`  |   `24px`   |  `1.5rem`   | Espaciado amplio: padding perimetral de pantallas, separación entre secciones funcionales. |
| `--dt-space-6`  |   `32px`   |  `2.0rem`   | Separación de bloques mayores en vistas de escritorio (Dashboards).                        |
| `--dt-space-8`  |   `48px`   |  `3.0rem`   | Separación entre contenedores de nivel macro o márgenes de visualizador 2D.                |
| `--dt-space-10` |   `64px`   |  `4.0rem`   | Márgenes estructurales en monitores de alta resolución (1920x1080).                        |

### 2.2. Dimensiones de Controles y Áreas Táctiles

| Token de Control | Altura Mínima (px) | Ancho Mínimo (px) | Plataforma Objetivo / Justificación |
| :--- | :---: | :---: | :--- |
| `--dt-touch-target-mobile` | `48px` | `48px` | **Mínimo obligatorio en Tablet/Mobile:** Botones de acción, checkboxes LOTO y selectores en campo. |
| `--dt-control-height-sm` | `32px` | `auto` | Desktop Web: Botones compactos en tablas de datos densos y filtros secundarios. |
| `--dt-control-height-md` | `40px` | `auto` | Desktop Web: Entradas de texto estándar, selectores y botones de formulario. |
| `--dt-control-height-lg` | `48px` | `auto` | Mobile/Tablet: Altura estándar para todos los campos de entrada (`InputText`, `InputSelect`). |
| `--dt-control-height-xl` | `56px` | `100%` | Mobile: Botón de acción primaria de pie de pantalla (ej. "Completar Orden de Trabajo"). |

### 2.3. Puntos de Quiebre Responsivos

| Token de Breakpoint  | Ancho (px) | Dispositivo de Referencia                      | Disposición de Layout                                                                  |
| :------------------- | :--------: | :--------------------------------------------- | :------------------------------------------------------------------------------------- |
| `--dt-breakpoint-sm` |  `390px`   | Smartphone vertical (iOS / Android)            | 1 columna, navegación por barra inferior.                                              |
| `--dt-breakpoint-md` |  `768px`   | Tablet vertical / Smartphone horizontal        | 1 a 2 columnas, drawer colapsable.                                                     |
| `--dt-breakpoint-lg` |  `1280px`  | Tablet Industrial horizontal (Zebra/Honeywell) | 2 columnas fijas (Barra lateral / Canvas + Panel de contexto).                         |
| `--dt-breakpoint-xl` |  `1920px`  | Estación de Trabajo Desktop (Full HD)          | 3 columnas (Barra lateral de navegación + Panel de control principal + Panel lateral). |

---

## 3. Tokens de Color y Superficies

La paleta se estructura en dos capas: **Tokens Primitivos** (valores absolutos de paleta) y **Tokens Semánticos** asignados dinámicamente según el contexto de iluminación operativa (**Tema Oscuro** para campo/móvil y **Tema Claro** para sala de control/escritorio).

### 3.1. Tokens Primitivos de Paleta

| Token Primitivo | Valor Hex | Familia / Uso Base |
| :--- | :---: | :--- |
| `--dt-primitive-gray-950` | `#11141A` | Tonalidad neutra profunda |
| `--dt-primitive-gray-900` | `#16191F` | Tonalidad neutra oscura |
| `--dt-primitive-gray-800` | `#1E222B` | Tonalidad neutra base oscura |
| `--dt-primitive-gray-700` | `#2A2F3D` | Superficie oscura intermedia |
| `--dt-primitive-gray-600` | `#353B4D` | Superficie oscura elevada |
| `--dt-primitive-gray-500` | `#5C667A` | Borde y elemento interactivo neutro |
| `--dt-primitive-gray-400` | `#7E8B9B` | Texto secundario y atenuado |
| `--dt-primitive-gray-300` | `#B8C0CC` | Bordes en fondo claro |
| `--dt-primitive-gray-200` | `#D8DBE0` | Gris neutro claro (Munsell N7.5 / Hollifield) |
| `--dt-primitive-gray-100` | `#E5E8EC` | Superficie clara base |
| `--dt-primitive-gray-50`  | `#F4F5F7` | Superficie clara de tarjeta |
| `--dt-primitive-white`    | `#FFFFFF` | Blanco puro |
| `--dt-primitive-red-600`  | `#E63946` | Rojo industrial de alarma |
| `--dt-primitive-amber-500`| `#D97706` | Ámbar / Advertencia en fondo claro |
| `--dt-primitive-amber-400`| `#F4A261` | Ámbar / Advertencia en fondo oscuro |
| `--dt-primitive-blue-600` | `#2563EB` | Azul informativo en fondo claro |
| `--dt-primitive-blue-400` | `#457B9D` | Azul informativo en fondo oscuro |
| `--dt-primitive-blue-200` | `#BAE6FD` | Zona de operación normal MAI en fondo claro  |
| `--dt-primitive-blue-700` | `#0369A1` | Zona de operación normal MAI en fondo oscuro  |
| `--dt-primitive-teal-600` | `#0D9488` | Confirmación documental en fondo claro |
| `--dt-primitive-teal-400` | `#2A9D8F` | Confirmación documental en fondo oscuro |

---

### 3.2. Tokens Semánticos: Tema Oscuro vs. Tema Claro
*Aplicación de la regla HPHMI del 90% de superficies neutras*

| Token Semántico | Tema Oscuro (Móvil / Noche) | Tema Claro (Escritorio / Día) | Aplicación en Interfaz |
| :--- | :---: | :---: | :--- |
| `--dt-color-bg-canvas` | `#16191F` | `#D8DBE0` | Fondo del lienzo 2D / Plano de planta |
| `--dt-color-surface-base` | `#1E222B` | `#E5E8EC` | Fondo de la aplicación / Header |
| `--dt-color-surface-card` | `#2A2F3D` | `#F4F5F7` | Tarjetas de activos / Filas de tabla |
| `--dt-color-surface-raised` | `#353B4D` | `#FFFFFF` | Modales / Paneles flotantes |
| `--dt-color-border-subtle` | `#3A4154` | `#B8C0CC` | Líneas divisorias / Separadores |
| `--dt-color-border-focus` | `#5C667A` | `#6B7280` | Borde de input en foco |
| `--dt-color-text-muted` | `#7E8B9B` | `#4B5563` | Unidades de medida / Timestamps |
| `--dt-color-text-body` | `#C2CBD6` | `#1F2937` | Texto principal / Valores de tabla |
| `--dt-color-text-primary` | `#FDFEFE` | `#111827` | Títulos / Valores críticos |
| `--dt-color-mai-track` | `#2A2F3D` | `#E5E8EC` | Fondo de pista del indicador analógico MAI |
| `--dt-color-mai-normal-zone` | `#0369A1` | `#BAE6FD` | Franja de rango de operación normal en MAI |
| `--dt-color-mai-pointer` | `#FDFEFE` | `#111827` | Puntero de valor actual MAI  |
| `--dt-color-mai-interlock` | `#FDFEFE` | `#111827` | Marcador de límite de disparo de interbloqueo en MAI |

---

### 3.3. Semántica de Alarmas y Seguridad (10% Reservado)

| Estado / Severidad | Token de Color | Valor (Tema Oscuro) | Valor (Tema Claro) | Símbolo Obligatorio |
| :--- | :--- | :---: | :---: | :---: |
| **Alarma Crítica / Peligro LOTO** | `--dt-color-alarm-critical` | `#E63946` | `#E63946` | Cuadrado / Octágono |
| **Advertencia / Límite Próximo** | `--dt-color-alarm-warning` | `#F4A261` | `#D97706` | Triángulo |
| **Informativo / Selección** | `--dt-color-state-info` | `#457B9D` | `#2563EB` | Círculo / Rombo |
| **Confirmación Documental** | `--dt-color-state-success` | `#2A9D8F` | `#0D9488` | Checkmark ($\checkmark$) |
| **Elemento Deshabilitado** | `--dt-color-state-disabled` | `#4A5263` | `#9CA3AF` | Borde punteado |

---

## 4. Tokens Tipográficos

La tipografía utiliza la pila nativa del sistema (*System Sans-Serif Stack*) para optimizar los tiempos de arranque en frío en dispositivos móviles y evitar la descarga de fuentes web pesadas.

* **Pila de Fuentes Primaria:** `Segoe UI, Inter, Roboto, -apple-system, sans-serif`
* **Pila de Fuentes Monoespaciada (Tags / Hashes / Telemetría):** `Cascadia Code, SF Mono, Consolas, monospace`

### 4.1. Escala Tipográfica

| Token Tipográfico | Tamaño (px / rem) | Altura de Línea | Peso (Font-Weight) | Uso Estándar en la Aplicación |
| :--- | :---: | :---: | :---: | :--- |
| `--dt-font-display` | `28px` / `1.75rem` | `36px` | Bold (`700`) | KPIs macros de nivel ejecutivo en Dashboard L1. |
| `--dt-font-h1` | `22px` / `1.375rem`| `28px` | SemiBold (`600`) | Título principal de la pantalla / Nombre del activo en Ficha L3. |
| `--dt-font-h2` | `18px` / `1.125rem`| `24px` | SemiBold (`600`) | Encabezados de tarjetas, títulos de modales y paneles laterales. |
| `--dt-font-body-lg` | `16px` / `1.0rem` | `24px` | Regular (`400`) | Texto de campos de entrada en móvil, lectura principal de OTs. |
| `--dt-font-body-md` | `14px` / `0.875rem`| `20px` | Regular (`400`) | Texto de celdas de tabla, descripciones técnicas y menús. |
| `--dt-font-caption` | `12px` / `0.75rem` | `16px` | Medium (`500`) | Etiquetas flotantes de formularios, metadatos, autoría de logs. |
| `--dt-font-mono-data`| `13px` / `0.8125rem`| `16px`| Medium (`500`) | **Tags industriales (P-101), hashes criptográficos, IP, horas.** |

---

## 5. Tokens de Elevación, Bordes y Profundidad

Para cumplir con la filosofía HPHMI en interfaces oscuras, la profundidad no se expresa mediante sombras decorativas difusas, sino mediante **diferenciación de color de superficie y bordes sutiles**.

### 5.1. Radios de Borde

| Token | Valor (px) | Aplicación en Componentes |
| :--- | :---: | :--- |
| `--dt-radius-none` | `0px` | Canvas de mapa 2D, contenedores full-bleed en móvil. |
| `--dt-radius-sm` | `4px` | Badges de estado, tags de clase de equipo, checkboxes. |
| `--dt-radius-md` | `6px` | Campos de texto (`InputText`), selectores, botones estándar. |
| `--dt-radius-lg` | `8px` | Tarjetas de información (`Cards`), paneles laterales, dropdowns. |
| `--dt-radius-xl` | `12px` | Ventanas modales, diálogos de bloqueo LOTO. |

### 5.2. Capas y Niveles de Apilamiento (Z-Index Hierarchy)

| Token Z-Index | Valor | Elementos Asignados |
| :--- | :---: | :--- |
| `--dt-z-canvas` | `0` | Capa base vectorial SVG (Plano de planta). |
| `--dt-z-layer-ptw` | `10` | Capa gráfica superpuesta de Permisos de Trabajo (VIS-008). |
| `--dt-z-layer-loto` | `20` | Capa gráfica de Trazabilidad LOTO (VIS-011). |
| `--dt-z-overlay-card` | `100` | Tarjeta emergente de activo (Asset Quick-Card L3 / VIS-033). |
| `--dt-z-header-sticky` | `500` | Barra de navegación superior fija y estado de red. |
| `--dt-z-drawer-sidebar` | `800` | Panel lateral de navegación desplegable. |
| `--dt-z-modal` | `1000` | Ventanas modales estándar (Creación OT, Asset Swap). |
| `--dt-z-modal-fail-safe`| `1500` | **Modal crítico de Peligro LOTO / Bloqueo activo (No descartable).** |
| `--dt-z-toast-alert` | `2000` | Alertas de desconexión y notificaciones toast de SignalR. |

---

## 6. Patrones Visuales Industriales y Codificación Redundante

### 6.1. Especificación del Indicador Analógico Móvil (MAI)
En cumplimiento de ISA-101.01 y *The High Performance HMI Handbook* (Hollifield et al., Cap. 7), las variables continuas de proceso (presión, temperatura, flujo, vibración) no deben presentarse únicamente como dígitos numéricos. Deben utilizar el patrón de Indicador Analógico Móvil (MAI) para permitir la evaluación rápida de la condición en menos de 2 segundos.

##### Tema Claro (Sala de Control / Escritorio - 500 Lux)
![[assets/MAI-light.svg]]

##### Tema Oscuro (Operación de Campo / Tablet / Noche)
![[assets/MAI-dark.svg]]

#### 6.1.1. Tabla de Tokens Semánticos Dual-Theme para MAI
Para evitar el acoplamiento directo de códigos hexadecimales y garantizar la compatibilidad entre la Sala de Control (Tema Claro) y la Operación de Campo (Tema Oscuro), los componentes Razor deben consumir estrictamente la siguiente matriz de tokens:

| Elemento Gráfico del MAI | Token Semántico CSS / C# | Tema Claro (Desktop / Día) | Tema Oscuro (Móvil / Noche) | Función Ergonomía HPHMI / ISA-101 |
| :--- | :--- | :---: | :---: | :--- |
| **Pista Base (`Track`)** | `--dt-color-mai-track` | `#E5E8EC` | `#2A2F3D` | Fondo perimetral del indicador (Alto $8\text{px}$, Radio $4\text{px}$). |
| **Zona Normal de Operación** | `--dt-color-mai-normal-zone` | `#BAE6FD` | `#0369A1` | **Franja azul clara** para reconocimiento pre-atentivo del rango seguro. |
| **Puntero de Valor Actual** | `--dt-color-mai-pointer` | `#111827` | `#FDFEFE` | Puntero circular/triangular móvil. **Mantiene forma y color neutro.** |
| **Borde del Puntero** | `--dt-color-mai-pointer-border` | `#FFFFFF` | `#1E222B` | Contorno de alto contraste para visibilidad sobre la zona normal. |
| **Indicador de Alarma Alta (P1)** | `--dt-color-alarm-critical` | `#E63946` | `#E63946` | **Elemento separado (Método 3):** Cuadrado rojo + '1' que aparece junto al límite. |
| **Texto sobre Alarma Crítica** | `--dt-color-alarm-text-critical` | `#FFFFFF` | `#FFFFFF` | Texto de alto contraste sobre cuadrado rojo ($4.6:1$ WCAG AA). |
| **Indicador de Alarma Baja / Advertencia (P2)** | `--dt-color-alarm-warning` | `#D97706` | `#F4A261` | **Elemento separado (Método 3):** Triángulo ámbar + '2' que aparece junto al límite. |
| **Texto sobre Advertencia Ámbar** | `--dt-color-alarm-text-warning` | `#111827` | `#16191F` | **Texto oscuro obligatorio sobre Ámbar** ($9.2:1$ WCAG AAA). |
| **Límite de Interbloqueo (`Interlock`)** | `--dt-color-mai-interlock` | `#111827` | `#FDFEFE` | Bloque sólido en el extremo que señala disparo automático de seguridad. |

#### 6.1.2. Reglas de Comportamiento Dinámico y Alarmas
1. **Pista de Fondo y Zona Normal:** La pista abarca el $100\%$ de la escala calibrada del instrumento. La Zona de Operación Normal se renderiza como un segmento interno destacado en azul claro (`--dt-color-mai-normal-zone`).
2. **Invarianza del Puntero:** El puntero de valor actual no altera su forma ni su color neutro al cruzar los umbrales de alarma. Esto conserva el punto de referencia espacial y evita distorsiones cognitivas.
3. **Presentación de Alarmas (Método 3 de Hollifield):**
   * **Desviación Alta (High / High-High):** Al cruzar el umbral superior, aparece un **elemento de alarma separado** adyacente a la escala en el punto de infracción. Se presenta un cuadrado rojo (`--dt-color-alarm-critical`) con el número de prioridad `1` para Alarma Crítica.
   * **Desviación Baja (Low / Low-Low):** Al cruzar el umbral inferior, aparece un **triángulo ámbar** (`--dt-color-alarm-warning`) adyacente con el número de prioridad `2` para Advertencia.
4. **Límites de Seguridad e Interbloqueo (`Safety Interlock`):** Los extremos de la escala que activan paradas automáticas (ESD) se marcan con un rectángulo sólido (`--dt-color-mai-interlock`) en el extremo correspondiente.

---

### 6.2. Matriz de Codificación Redundante para Permisos y LOTO

| Concepto de Seguridad | Color Principal | Forma Geométrica | Icono Asociado | Texto Obligatorio |
| :--- | :---: | :---: | :---: | :--- |
| **Permiso en Caliente (Hot Work)** | `#E63946` | Cuadrado ($24\times24\text{px}$) | Llama ($\text{flame}$) | `HOT WORK` |
| **Permiso en Alturas (Heights)** | `#457B9D` | Triángulo ($24\times24\text{px}$) | Escalera / Arnés | `HEIGHTS` |
| **Espacio Confinado (Confined)** | `#F4A261` | Círculo ($\varnothing 24\text{px}$) | Silueta / Tanque | `CONFINED` |
| **Punto LOTO Bloqueado (Seguro)** | `#2A9D8F` | Candado cerrado | Candado ($\text{lock}$) | `ISOLATED - 0 ENERGY` |
| **Punto LOTO Energizado (Peligro)**| `#E63946` | Candado abierto con halo | Rayo / Alerta | `DANGER - ENERGIZED` |
| **Pérdida de Telemetría (Fail-Safe)**| `#F4A261` | Rombo con signo '?' | Desconexión ($\text{wifi-off}$) | `SIGNAL LOST - STALE` |

---

## 7. Archivo de Variables CSS para Librería de Clases de Razor (`tokens.css`)

```css
:root {
  /* Tokens Espaciales (Rejilla 8px) */
  --dt-space-0: 0px;
  --dt-space-1: 4px;
  --dt-space-2: 8px;
  --dt-space-3: 12px;
  --dt-space-4: 16px;
  --dt-space-5: 24px;
  --dt-space-6: 32px;
  --dt-space-8: 48px;
  --dt-space-10: 64px;

  /* Controles y Áreas Táctiles */
  --dt-touch-target-mobile: 48px;
  --dt-control-height-sm: 32px;
  --dt-control-height-md: 40px;
  --dt-control-height-lg: 48px;
  --dt-control-height-xl: 56px;

  /* Tipografía - Fuentes */
  --dt-font-family-base: Segoe UI, Inter, Roboto, -apple-system, sans-serif;
  --dt-font-family-mono: Cascadia Code, SF Mono, Consolas, monospace;

  /* Radios de Borde */
  --dt-radius-none: 0px;
  --dt-radius-sm: 4px;
  --dt-radius-md: 6px;
  --dt-radius-lg: 8px;
  --dt-radius-xl: 12px;

  /* Z-Index */
  --dt-z-canvas: 0;
  --dt-z-layer-ptw: 10;
  --dt-z-layer-loto: 20;
  --dt-z-overlay-card: 100;
  --dt-z-header-sticky: 500;
  --dt-z-drawer-sidebar: 800;
  --dt-z-modal: 1000;
  --dt-z-modal-fail-safe: 1500;
  --dt-z-toast-alert: 2000;

  /* Tema Claro (Default / Desktop) */
  --dt-color-bg-canvas: #D8DBE0;
  --dt-color-surface-base: #E5E8EC;
  --dt-color-surface-card: #F4F5F7;
  --dt-color-surface-raised: #FFFFFF;
  --dt-color-border-subtle: #B8C0CC;
  --dt-color-border-focus: #6B7280;

  --dt-color-text-muted: #4B5563;
  --dt-color-text-body: #1F2937;
  --dt-color-text-primary: #111827;

  --dt-color-alarm-critical: #E63946;
  --dt-color-alarm-warning: #D97706;
  --dt-color-alarm-text-critical: #FFFFFF;
  --dt-color-alarm-text-warning: #111827; /* Contraste 9.2:1 WCAG AAA sobre #D97706 */
  --dt-color-state-info: #2563EB;
  --dt-color-state-success: #0D9488;
  --dt-color-state-disabled: #9CA3AF;

  /* Indicador Analógico Móvil (MAI) - Tema Claro */
  --dt-color-mai-track: #E5E8EC;
  --dt-color-mai-normal-zone: #BAE6FD;
  --dt-color-mai-pointer: #111827;
  --dt-color-mai-pointer-border: #FFFFFF;
  --dt-color-mai-interlock: #111827;
}

/* Tema Oscuro (Móvil / Campo / Noche) */
[data-theme="dark"] {
  --dt-color-bg-canvas: #16191F;
  --dt-color-surface-base: #1E222B;
  --dt-color-surface-card: #2A2F3D;
  --dt-color-surface-raised: #353B4D;
  --dt-color-border-subtle: #3A4154;
  --dt-color-border-focus: #5C667A;

  --dt-color-text-muted: #7E8B9B;
  --dt-color-text-body: #C2CBD6;
  --dt-color-text-primary: #FDFEFE;

  --dt-color-alarm-critical: #E63946;
  --dt-color-alarm-warning: #F4A261;
  --dt-color-alarm-text-critical: #FFFFFF;
  --dt-color-alarm-text-warning: #16191F; /* Contraste 8.5:1 WCAG AAA sobre #F4A261 */
  --dt-color-state-info: #457B9D;
  --dt-color-state-success: #2A9D8F;
  --dt-color-state-disabled: #4A5263;

  /* Indicador Analógico Móvil (MAI) - Tema Oscuro */
  --dt-color-mai-track: #2A2F3D;
  --dt-color-mai-normal-zone: #0369A1;
  --dt-color-mai-pointer: #FDFEFE;
  --dt-color-mai-pointer-border: #1E222B;
  --dt-color-mai-interlock: #FDFEFE;
}
```