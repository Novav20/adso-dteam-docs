---
code: DT-UI-DS-DOC-001
version: 1.5
date: 2026-09-04
status: Aprobado
author: Juan David Julio Serrano
standard:
  - ISA-101.01-2015 (Human Machine Interfaces for Process Automation Systems)
  - The High Performance HMI Handbook (Hollifield et al.)
  - ISO 9241-110:2020 / ISO 9241-210:2019 (Ergonomía de Interacción y Diseño Centrado en el Humano)
  - WCAG 2.1 Nivel AA (Web Content Accessibility Guidelines)
  - ISO 45001:2018 (Cláusula 8.1 — LOTO & Seguridad Operativa)
---

# Especificación Técnica de Tokens de Diseño

## 1. Alcance
Este documento establece la **Fuente Única de Verdad** para todos los tokens de diseño aplicados en el diseño de prototipos y en la implementación de las interfaces de usuario de la plataforma DTEAM, abarcando tanto los clientes móviles de operación en campo como los portales web de supervisión y administración.

### Principios Obligatorios:
1. **Regla HPHMI del 90/10:** El 90% de la interfaz opera en escala de grises neutra de bajo contraste para minimizar la fatiga visual. El 10% del color saturado se reserva exclusivamente para anomalías, alarmas y condiciones de peligro.
2. **Eliminación del Verde como Estado "Normal":** No se utiliza verde para indicar que un motor está encendido o en operación normal. El estado normal se representa mediante grises y texto ("RUNNING" / "UP"). El uso del color en confirmaciones documentales o estado de conexión se restringe a tonalidades **Teal / Pino** (`--dt-primitive-teal-600` o `--dt-primitive-teal-400`), evitando cualquier confusión con el verde industrial de estado.
3. **Codificación Redundante (WCAG 2.1 AA):** Ningún estado crítico de seguridad o alarma debe comunicarse únicamente por color. Todo indicador debe combinar **Forma + Icono + Color + Texto**.
4. **Ergonomía Industrial Táctil:** Los elementos interactivos en dispositivos móviles y tabletas de campo deben respetar un área de contacto mínima de **$48 \times 48\text{ px}$** para permitir la operación con guantes de seguridad.

---

## 2. Tokens Espaciales y de Layout

El espaciado y dimensionamiento se rige bajo un sistema de cuadrícula base de **8px** (con un submarco de 4px para micro-ajustes).

> **Escala por Multiplicador de $4\text{px}$ / $0.25\text{rem}$:**  
> La nomenclatura `--dt-space-N` utiliza una convención de **multiplicador lineal** donde $N$ representa el factor por el cual se multiplica la unidad base de $4\text{px}$ ($N \times 4\text{px}$ o $N \times 0.25\text{rem}$), estándar en la industria (Tailwind CSS / W3C DTCG).  
> A partir de $16\text{px}$, la escala omite deliberadamente valores impares/intermedios como `--dt-space-5` ($20\text{px}$) o `--dt-space-7` ($28\text{px}$) para garantizar que todos los espaciados mayores sean **estrictamente múltiplos de 8px** ($24\text{px} = 3 \times 8$, $32\text{px} = 4 \times 8$, $48\text{px} = 6 \times 8$, $64\text{px} = 8 \times 8$), preservando la alineación armónica visual del layout y previniendo la parálisis de decisión en el diseño.

### 2.1. Escala de Espaciado

| Token CSS     | Valor (px) | Valor (rem) | Uso Primario en Layout y Componentes                                                       |
| :------------ | :--------: | :---------: | :----------------------------------------------------------------------------------------- |
| --dt-space-0  |    0px     |    0rem     | Reseteo de márgenes y paddings.                                                            |
| --dt-space-1  |    4px     |   0.25rem   | Micro-espaciado: separación entre icono y texto en badges, padding interno de tags.        |
| --dt-space-2  |    8px     |   0.5rem    | Espaciado compacto: gap entre campos de formulario estrechos, padding de celdas de tabla.  |
| --dt-space-3  |    12px    |   0.75rem   | Espaciado medio: gap en barras de herramientas (toolbars), padding interno de inputs.      |
| --dt-space-4  |    16px    |   1.0rem    | **Espaciado base:** padding de tarjetas (cards), gap estándar en Auto-Layout.              |
| --dt-space-6  |    24px    |   1.5rem    | Espaciado amplio: padding perimetral de pantallas, separación entre secciones funcionales. |
| --dt-space-8  |    32px    |   2.0rem    | Separación de bloques mayores en vistas de escritorio (Dashboards).                        |
| --dt-space-12 |    48px    |   3.0rem    | Separación entre contenedores de nivel macro o márgenes de visualizador 2D.                |
| --dt-space-16 |    64px    |   4.0rem    | Márgenes estructurales en monitores de alta resolución (1920x1080).                        |

### 2.2. Dimensiones de Controles y Áreas Táctiles
| Token de Control         | Altura Mínima (px) | Ancho Mínimo (px) | Plataforma Objetivo / Justificación                                                                |
| ------------------------ | ------------------ | ----------------- | -------------------------------------------------------------------------------------------------- |
| --dt-touch-target-mobile | 48px               | 48px              | **Mínimo obligatorio en Tablet/Mobile:** Botones de acción, checkboxes LOTO y selectores en campo. |
| --dt-control-height-sm   | 32px               | auto              | Desktop Web: Botones compactos en tablas de datos densos y filtros secundarios.                    |
| --dt-control-height-md   | 40px               | auto              | Desktop Web: Entradas de texto estándar, selectores y botones de formulario.                       |
| --dt-control-height-lg   | 48px               | auto              | Mobile/Tablet: Altura estándar para todos los campos de entrada (InputText, InputSelect).          |
| --dt-control-height-xl   | 56px               | 100%              | Mobile: Botón de acción primaria de pie de pantalla (ej. "Completar Orden de Trabajo").            |

### 2.3. Puntos de Quiebre Responsivos
| Token de Breakpoint | Ancho (px) | Dispositivo de Referencia                      | Disposición de Layout                                                                  |
| ------------------- | ---------- | ---------------------------------------------- | -------------------------------------------------------------------------------------- |
| --dt-breakpoint-sm  | 390px      | Smartphone vertical (iOS / Android)            | 1 columna, navegación por barra inferior.                                              |
| --dt-breakpoint-md  | 768px      | Tablet vertical / Smartphone horizontal        | 1 a 2 columnas, drawer colapsable.                                                     |
| --dt-breakpoint-lg  | 1280px     | Tablet Industrial horizontal (Zebra/Honeywell) | 2 columnas fijas (Barra lateral / Canvas + Panel de contexto).                         |
| --dt-breakpoint-xl  | 1920px     | Estación de Trabajo Desktop (Full HD)          | 3 columnas (Barra lateral de navegación + Panel de control principal + Panel lateral). |

---

## 3. Tokens de Color y Superficies
La paleta se estructura en dos capas: **Tokens Primitivos** (valores absolutos de paleta, **donde reside la única declaración de códigos HEX en el documento de diseño**) y **Tokens Semánticos** asignados dinámicamente según el contexto de iluminación operativa (Tema Oscuro y Tema Claro), que hacen referencia a las variables primitivas.

### 3.1. Tokens Primitivos de Paleta
| Token Primitivo          | Valor Hex | Familia / Uso Base                                                   |
| ------------------------ | --------- | -------------------------------------------------------------------- |
| --dt-primitive-gray-980  | #111827   | Negro de alto contraste para texto en tema claro (Tailwind gray-900) |
| --dt-primitive-gray-950  | #11141A   | Tonalidad neutra profunda (Fondo de UI extrema)                      |
| --dt-primitive-gray-900  | #16191F   | Tonalidad neutra oscura (Lienzo en tema oscuro)                      |
| --dt-primitive-gray-850  | #1F2937   | Gris carbón para texto base en tema claro                            |
| --dt-primitive-gray-800  | #1E222B   | Tonalidad neutra base oscura (Fondo de aplicación en oscuro)         |
| --dt-primitive-gray-700  | #2A2F3D   | Superficie oscura intermedia (Tarjetas en oscuro)                    |
| --dt-primitive-gray-650  | #3A4154   | Borde sutil oscuro (Diferenciación de capas en oscuro)               |
| --dt-primitive-gray-620  | #4B5563   | Gris medio para texto secundario en claro (Tailwind gray-600)        |
| --dt-primitive-gray-600  | #353B4D   | Superficie oscura elevada (Paneles flotantes / Modales en oscuro)    |
| --dt-primitive-gray-580  | #4A5263   | Gris deshabilitado para fondo oscuro                                 |
| --dt-primitive-gray-550  | #6B7280   | Borde de input en foco en claro (Tailwind gray-500)                  |
| --dt-primitive-gray-500  | #5C667A   | Borde y elemento interactivo neutro                                  |
| --dt-primitive-gray-450  | #6E7A92   | Borde de input en foco en oscuro                                     |
| --dt-primitive-gray-420  | #8A98AA   | Gris claro para texto secundario en oscuro                           |
| --dt-primitive-gray-400  | #7E8B9B   | Texto secundario y atenuado general                                  |
| --dt-primitive-gray-380  | #9CA3AF   | Gris deshabilitado para fondo claro (Tailwind gray-400)              |
| --dt-primitive-gray-300  | #B8C0CC   | Bordes en fondo claro                                                |
| --dt-primitive-gray-280  | #C2CBD6   | Gris claro para texto base en oscuro                                 |
| --dt-primitive-gray-200  | #D8DBE0   | Gris neutro claro (Munsell N7.5 / Hollifield / Lienzo en claro)      |
| --dt-primitive-gray-100  | #E5E8EC   | Superficie clara base (Fondo de aplicación en claro)                 |
| --dt-primitive-gray-50   | #F4F5F7   | Superficie clara de tarjeta (Tarjetas en claro)                      |
| --dt-primitive-gray-10   | #FDFEFE   | Blanco roto de alto contraste para texto en tema oscuro              |
| --dt-primitive-white     | #FFFFFF   | Blanco puro (Lienzo, fondos elevados)                                |
| --dt-primitive-red-600   | #E63946   | Rojo industrial de alarma                                            |
| --dt-primitive-amber-600 | #AC5E04   | Ámbar / Advertencia en fondo claro (Ajustado WCAG AA 3.47:1)         |
| --dt-primitive-amber-500 | #D97706   | Ámbar / Advertencia base                                             |
| --dt-primitive-amber-400 | #F4A261   | Ámbar / Advertencia en fondo oscuro                                  |
| --dt-primitive-blue-700  | #0369A1   | Zona de operación normal MAI en fondo oscuro                         |
| --dt-primitive-blue-600  | #2563EB   | Azul informativo en fondo claro                                      |
| --dt-primitive-blue-450  | #4881A4   | Azul informativo en fondo oscuro (Ajustado WCAG AA 3.15:1)           |
| --dt-primitive-blue-400  | #457B9D   | Azul informativo base                                                |
| --dt-primitive-blue-200  | #BAE6FD   | Zona de operación normal MAI en fondo claro                          |
| --dt-primitive-teal-700  | #0B857A   | Confirmación documental en fondo claro (Ajustado WCAG AA 3.25:1)     |
| --dt-primitive-teal-600  | #0D9488   | Confirmación documental base                                         |
| --dt-primitive-teal-400  | #2A9D8F   | Confirmación documental en fondo oscuro                              |

### 3.2. Tokens Semánticos para los Temas Claro y Oscuro
*Aplicación de la regla HPHMI del 90% de superficies neutras utilizando referencias directas a tokens primitivos*

| Token Semántico            | Tema Oscuro (Móvil / Noche) | Tema Claro (Escritorio / Día) | Aplicación en Interfaz                                                  |
| -------------------------- | --------------------------- | ----------------------------- | ----------------------------------------------------------------------- |
| --dt-color-bg-canvas       | --dt-primitive-gray-900     | --dt-primitive-gray-200       | Fondo del lienzo 2D / Plano de planta                                   |
| --dt-color-surface-base    | --dt-primitive-gray-800     | --dt-primitive-gray-100       | Fondo de la aplicación / Header                                         |
| --dt-color-surface-card    | --dt-primitive-gray-700     | --dt-primitive-gray-50        | Tarjetas de activos / Filas de tabla                                    |
| --dt-color-surface-raised  | --dt-primitive-gray-600     | --dt-primitive-white          | Modales / Paneles flotantes                                             |
| --dt-color-border-subtle   | --dt-primitive-gray-650     | --dt-primitive-gray-300       | Líneas divisorias / Separadores                                         |
| --dt-color-border-focus    | --dt-primitive-gray-450     | --dt-primitive-gray-550       | Borde de input en foco (Tema Oscuro ajustado a 3.09:1 WCAG AA)          |
| --dt-color-text-muted      | --dt-primitive-gray-420     | --dt-primitive-gray-620       | Unidades de medida / Timestamps (Tema Oscuro ajustado a 4.55:1 WCAG AA) |
| --dt-color-text-body       | --dt-primitive-gray-280     | --dt-primitive-gray-850       | Texto principal / Valores de tabla                                      |
| --dt-color-text-primary    | --dt-primitive-gray-10      | --dt-primitive-gray-980       | Títulos / Valores críticos                                              |
| --dt-color-mai-track       | --dt-primitive-gray-700     | --dt-primitive-gray-100       | Fondo de pista del indicador analógico MAI                              |
| --dt-color-mai-normal-zone | --dt-primitive-blue-700     | --dt-primitive-blue-200       | Franja de rango de operación normal en MAI                              |
| --dt-color-mai-pointer     | --dt-primitive-gray-10      | --dt-primitive-gray-980       | Puntero de valor actual MAI                                             |
| --dt-color-mai-interlock   | --dt-primitive-gray-10      | --dt-primitive-gray-980       | Marcador de límite de disparo de interbloqueo en MAI                    |

### 3.3. Semántica de Alarmas y Seguridad (10% Reservado)

| Estado / Severidad                | Token de Color            | Valor (Tema Oscuro)      | Valor (Tema Claro)       | Símbolo Obligatorio                                                 |
| --------------------------------- | ------------------------- | ------------------------ | ------------------------ | ------------------------------------------------------------------- |
| **Alarma Crítica / Peligro LOTO** | --dt-color-alarm-critical | --dt-primitive-red-600   | --dt-primitive-red-600   | Cuadrado / Octágono                                                 |
| **Advertencia / Límite Próximo**  | --dt-color-alarm-warning  | --dt-primitive-amber-400 | --dt-primitive-amber-600 | Triángulo (Ajustado WCAG AA 3.47:1 en fondo claro)                  |
| **Informativo / Selección**       | --dt-color-state-info     | --dt-primitive-blue-450  | --dt-primitive-blue-600  | Círculo / Rombo (Ajustado WCAG AA 3.15:1 en fondo oscuro)           |
| **Confirmación Documental**       | --dt-color-state-success  | --dt-primitive-teal-400  | --dt-primitive-teal-700  | Checkmark ( $\checkmark$ ) (Ajustado WCAG AA 3.25:1 en fondo claro) |
| **Elemento Deshabilitado**        | --dt-color-state-disabled | --dt-primitive-gray-580  | --dt-primitive-gray-380  | Borde punteado                                                      |

---

## 4. Tokens Tipográficos
La tipografía utiliza la pila nativa del sistema (*System Sans-Serif Stack*) para optimizar los tiempos de arranque en frío en dispositivos móviles y evitar la descarga de fuentes web pesadas.
* **Pila de Fuentes Primaria:** Segoe UI, Inter, Roboto, -apple-system, sans-serif
* **Pila de Fuentes Monoespaciada (Tags / Hashes / Telemetría):** Cascadia Code, SF Mono, Consolas, monospace

### 4.1. Escala Tipográfica
| Token Tipográfico   | Tamaño (px / rem) | Altura de Línea | Peso (Font-Weight) | Uso Estándar en la Aplicación                                    |
| ------------------- | ----------------- | --------------- | ------------------ | ---------------------------------------------------------------- |
| --dt-font-display   | 28px / 1.75rem    | 36px            | Bold (700)         | KPIs macros de nivel ejecutivo en Dashboard L1.                  |
| --dt-font-h1        | 22px / 1.375rem   | 28px            | SemiBold (600)     | Título principal de la pantalla / Nombre del activo en Ficha L3. |
| --dt-font-h2        | 18px / 1.125rem   | 24px            | SemiBold (600)     | Encabezados de tarjetas, títulos de modales y paneles laterales. |
| --dt-font-body-lg   | 16px / 1.0rem     | 24px            | Regular (400)      | Texto de campos de entrada en móvil, lectura principal de OTs.   |
| --dt-font-body-md   | 14px / 0.875rem   | 20px            | Regular (400)      | Texto de celdas de tabla, descripciones técnicas y menús.        |
| --dt-font-caption   | 12px / 0.75rem    | 16px            | Medium (500)       | Etiquetas flotantes de formularios, metadatos, autoría de logs.  |
| --dt-font-mono-data | 13px / 0.8125rem  | 16px            | Medium (500)       | **Tags industriales (P-101), hashes criptográficos, IP, horas.** |

---

## 5. Tokens de Elevación, Bordes y Profundidad
Para cumplir con la filosofía HPHMI en interfaces oscuras, la profundidad no se expresa mediante sombras de tipo decorativo o difusas, sino mediante **diferenciación de color de superficie y bordes sutiles** normativos.

### 5.1. Radios de Borde
| Token            | Valor (px) | Aplicación en Componentes                                      |
| ---------------- | ---------- | -------------------------------------------------------------- |
| --dt-radius-none | 0px        | Canvas de mapa 2D, contenedores full-bleed en móvil.           |
| --dt-radius-sm   | 4px        | Badges de estado, tags de clase de equipo, checkboxes.         |
| --dt-radius-md   | 6px        | Campos de texto (InputText), selectores, botones estándar.     |
| --dt-radius-lg   | 8px        | Tarjetas de información (Cards), paneles laterales, dropdowns. |
| --dt-radius-xl   | 12px       | Ventanas modales, diálogos de bloqueo LOTO.                    |

### 5.2. Capas y Niveles de Apilamiento (Z-Index Hierarchy)
| Token Z-Index          | Valor | Elementos Asignados                                                  |
| ---------------------- | ----- | -------------------------------------------------------------------- |
| --dt-z-canvas          | 0     | Capa base vectorial SVG (Plano de planta).                           |
| --dt-z-layer-ptw       | 10    | Capa gráfica superpuesta de Permisos de Trabajo [[VIS-008]].         |
| --dt-z-layer-loto      | 20    | Capa gráfica de Trazabilidad LOTO [[VIS-011]].                       |
| --dt-z-overlay-card    | 100   | Tarjeta emergente de activo (Asset Quick-Card L3 / VIS-033).         |
| --dt-z-header-sticky   | 500   | Barra de navegación superior fija y estado de red.                   |
| --dt-z-drawer-sidebar  | 800   | Panel lateral de navegación desplegable.                             |
| --dt-z-modal           | 1000  | Ventanas modales estándar (Creación OT, Asset Swap).                 |
| --dt-z-modal-fail-safe | 1500  | **Modal crítico de Peligro LOTO / Bloqueo activo (No descartable).** |
| --dt-z-toast-alert     | 2000  | Alertas de desconexión y notificaciones toast de SignalR.            |

---

## 6. Patrones Visuales Industriales y Codificación Redundante

### 6.1. Especificación del Indicador Analógico Móvil (MAI)
En cumplimiento de ISA-101.01 y *The High Performance HMI Handbook* (Hollifield et al., Cap. 7), las variables continuas de proceso (presión, temperatura, flujo, vibración) no deben presentarse únicamente como dígitos numéricos. Deben utilizar el patrón de Indicador Analógico Móvil (MAI) para permitir la evaluación rápida de la condición en menos de 2 segundos.

#### Tema Claro (Sala de Control / Escritorio - 500 Lux)
![[assets/MAI-light.svg]]
#### Tema Oscuro (Operación de Campo / Tablet / Noche)
![[assets/MAI-dark.svg]]

#### 6.1.1. Tabla de Tokens Semánticos Dual-Theme para MAI
Para evitar el acoplamiento directo de códigos hexadecimales y garantizar la compatibilidad entre la Sala de Control (Tema Claro) y la Operación de Campo (Tema Oscuro), los componentes de interfaz en el frontend deben consumir la siguiente matriz de tokens:

| Elemento Gráfico del MAI                        | Token Semántico CSS / C#       | Tema Claro (Desktop / Día) | Tema Oscuro (Móvil / Noche) | Función Ergonomía HPHMI / ISA-101                                                    |
| ----------------------------------------------- | ------------------------------ | -------------------------- | --------------------------- | ------------------------------------------------------------------------------------ |
| **Pista Base (Track)**                          | --dt-color-mai-track           | --dt-primitive-gray-100    | --dt-primitive-gray-700     | Fondo perimetral del indicador (Alto $8\text{px}$, Radio $4\text{px}$).              |
| **Zona Normal de Operación**                    | --dt-color-mai-normal-zone     | --dt-primitive-blue-200    | --dt-primitive-blue-700     | **Franja azul clara** para reconocimiento pre-atentivo del rango seguro.             |
| **Puntero de Valor Actual**                     | --dt-color-mai-pointer         | --dt-primitive-gray-980    | --dt-primitive-gray-10      | Puntero circular/triangular móvil. **Mantiene forma y color neutro.**                |
| **Borde del Puntero**                           | --dt-color-mai-pointer-border  | --dt-primitive-white       | --dt-primitive-gray-800     | Contorno de alto contraste para visibilidad sobre la zona normal.                    |
| **Indicador de Alarma Alta (P1)**               | --dt-color-alarm-critical      | --dt-primitive-red-600     | --dt-primitive-red-600      | **Elemento separado (Método 3):** Cuadrado rojo + '1' que aparece junto al límite.   |
| **Texto sobre Alarma Crítica**                  | --dt-color-alarm-text-critical | --dt-primitive-white       | --dt-primitive-white        | Texto de alto contraste sobre cuadrado rojo ($4.6:1$ WCAG AA).                       |
| **Indicador de Alarma Baja / Advertencia (P2)** | --dt-color-alarm-warning       | --dt-primitive-amber-600   | --dt-primitive-amber-400    | **Elemento separado (Método 3):** Triángulo ámbar + '2' (Ajustado WCAG AA $3.47:1$). |
| **Texto sobre Advertencia Ámbar**               | --dt-color-alarm-text-warning  | --dt-primitive-white       | --dt-primitive-gray-900     | Texto de alto contraste sobre Ámbar ($5.36:1$ en claro, $8.5:1$ en oscuro).          |
| **Límite de Interbloqueo (Interlock)**          | --dt-color-mai-interlock       | --dt-primitive-gray-980    | --dt-primitive-gray-10      | Bloque sólido en el extremo que señala disparo automático de seguridad.              |

#### 6.1.2. Reglas de Comportamiento Dinámico y Alarmas
1. **Pista de Fondo y Zona Normal:** La pista abarca el $100\%$ de la escala calibrada del instrumento. La Zona de Operación Normal se renderiza como un segmento interno destacado en azul claro (`--dt-color-mai-normal-zone`).
2. **Invarianza del Puntero:** El puntero de valor actual no altera su forma ni su color neutro al cruzar los umbrales de alarma. Esto conserva el punto de referencia espacial y evita distorsiones cognitivas.
3. **Presentación de Alarmas (Método 3 de Hollifield):**
    * **Desviación Alta (High / High-High):** Al cruzar el umbral superior, aparece un **elemento de alarma separado** adyacente a la escala en el punto de infracción. Se presenta un cuadrado rojo (`--dt-color-alarm-critical`) con el número de prioridad 1 para Alarma Crítica.
    * **Desviación Baja (Low / Low-Low):** Al cruzar el umbral inferior, aparece un **triángulo ámbar** (`--dt-color-alarm-warning`) adyacente con el número de prioridad 2 para Advertencia.
4. **Límites de Seguridad e Interbloqueo (Safety Interlock):** Los extremos de la escala que activan paradas automáticas (ESD) se marcan con un rectángulo sólido (`--dt-color-mai-interlock`) en el extremo correspondiente.

### 6.2. Matriz de Codificación Redundante para Permisos y LOTO

| Concepto de Seguridad                 | Color Principal / Token   | Forma Geométrica                      | Icono Asociado             | Texto Obligatorio   |
| ------------------------------------- | ------------------------- | ------------------------------------- | -------------------------- | ------------------- |
| **Permiso en Caliente (Hot Work)**    | --dt-color-alarm-critical | Cuadrado ( $24\times24\text{px}$ )    | Llama ( `flame` )          | HOT WORK            |
| **Permiso en Alturas (Heights)**      | --dt-primitive-blue-400   | Triángulo ( $24\times24\text{px}$ )   | Escalera / Arnés           | HEIGHTS             |
| **Espacio Confinado (Confined)**      | --dt-primitive-amber-400  | Círculo ( $\varnothing 24\text{px}$ ) | Silueta / Tanque           | CONFINED            |
| **Punto LOTO Bloqueado (Seguro)**     | --dt-color-state-success  | Candado cerrado                       | Candado ( `lock` )         | ISOLATED - 0 ENERGY |
| **Punto LOTO Energizado (Peligro)**   | --dt-color-alarm-critical | Candado abierto con halo              | Rayo / Alerta              | DANGER - ENERGIZED  |
| **Pérdida de Telemetría (Fail-Safe)** | --dt-color-alarm-warning  | Rombo con signo '?'                   | Desconexión ( `wifi-off` ) | SIGNAL LOST - STALE |

### 6.3. Patrón de Contenedores Deslizantes (*Bottom Sheets* y *Drawers*)
En cumplimiento del principio de **Controlabilidad** (ISO 9241-110:2020, Cláusula 5.5) y para mitigar la baja precisión de sensores capacitivos al operar con guantes industriales o en condiciones húmedas, los contenedores móviles deslizantes deben regirse por las siguientes directrices:

1. **Prohibición de Gesto Exclusivo:** Queda prohibido condicionar el despliegue, colapso o cierre de un contenedor exclusivamente a gestos continuos de arrastre o deslizamiento (*swipe/drag*).
2. **Disparador Físico Dedicado:** Todo contenedor debe integrar un elemento interactivo explícito (manija o cabecera táctil) cuyas dimensiones de área de contacto hereden el token `--dt-touch-target-mobile`.
3. **Conmutación Discreta:** La pulsación simple (*tap*) sobre dicho elemento debe alternar secuencialmente entre los estados definidos para el componente (Colapsado, Vista Parcial, Expandido), garantizando la operación sin requerir motricidad fina.
---

## 7. Archivo de Variables CSS del Sistema de Diseño

Para la implementación física en hojas de estilo web o componentes desacoplados, consúltese el archivo canónico:
`ui-ux/assets/tokens.css`