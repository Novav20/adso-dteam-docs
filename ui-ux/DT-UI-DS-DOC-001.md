---
code: DT-UI-DS-DOC-001
version: 1.7
date: 2026-09-06
status: APPROVED
author: Juan David Julio Serrano
standard:
  - ISA-101.01-2015 (Human Machine Interfaces for Process Automation Systems)
  - The High Performance HMI Handbook (Hollifield et al.)
  - ISO 9241-110:2020 / ISO 9241-210:2019 (Ergonomics of Human-System Interaction and Human-Centered Design)
  - WCAG 2.1 Level AA (Web Content Accessibility Guidelines)
  - ISO 45001:2018 (Clause 8.1 — LOTO & Operational Safety)
---
		
# Design Tokens Technical Specification

## 1. Scope
This document establishes the **Single Source of Truth** for all design tokens applied in prototype design and user interface implementation of the DTEAM platform, covering both mobile clients for field operations and web portals for supervision and administration.

### Mandatory Principles:
1. **90/10 HPHMI Rule:** 90% of the interface operates in neutral, low-contrast grayscale to minimize visual fatigue. The remaining 10% of saturated color is reserved exclusively for anomalies, alarms, and hazard conditions.
2. **Elimination of Green as "Normal" State:** Green is not used to indicate that a motor is running or in normal operation. Normal state is represented using grays and text ("RUNNING" / "UP"). The use of color in documentary confirmations or connection status is restricted to **Teal / Pine** shades (`--dt-primitive-teal-600` or `--dt-primitive-teal-400`), avoiding any confusion with the industrial state green.
3. **Redundant Coding (WCAG 2.1 AA):** No critical safety or alarm state should be communicated solely by color. Every indicator must combine **Shape + Icon + Color + Text**.
4. **Industrial Tactile Ergonomics:** Interactive elements on mobile devices and field tablets must respect a minimum touch area of **$48 \times 48\text{ px}$** to allow operation with safety gloves.

---

## 2. Spatial and Layout Tokens

Spacing and sizing are governed by an **8px** base grid system (with a 4px sub-frame for micro-adjustments).

> **Multiplier Scale of $4\text{px}$ / $0.25\text{rem}$:**  
> The `--dt-space-N` naming utilizes a **linear multiplier** convention where $N$ represents the factor by which the $4\text{px}$ base unit is multiplied ($N \times 4\text{px}$ or $N \times 0.25\text{rem}$), an industry standard (Tailwind CSS / W3C DTCG).  
> From $16\text{px}$, the scale deliberately omits odd/intermediate values like `--dt-space-5` ($20\text{px}$) or `--dt-space-7` ($28\text{px}$) to ensure all larger spacings are **strictly multiples of 8px** ($24\text{px} = 3 \times 8$, $32\text{px} = 4 \times 8$, $48\text{px} = 6 \times 8$, $64\text{px} = 8 \times 8$), preserving visual harmonic alignment of the layout and preventing design decision paralysis.

### 2.1. Spacing Scale

| CSS Token | Value (px) | Value (rem) | Primary Use in Layout and Components                                                       |
| :------------ | :--------: | :---------: | :----------------------------------------------------------------------------------------- |
| --dt-space-0  |    0px     |    0rem     | Reset margins and paddings.                                                            |
| --dt-space-1  |    4px     |   0.25rem   | Micro-spacing: gap between icon and text in badges, internal padding of tags.        |
| --dt-space-2  |    8px     |   0.5rem    | Compact spacing: gap between narrow form fields, table cell padding.  |
| --dt-space-3  |    12px    |   0.75rem   | Medium spacing: gap in toolbars, internal padding of inputs.      |
| --dt-space-4  |    16px    |   1.0rem    | **Base spacing:** card padding, standard gap in Auto-Layout.              |
| --dt-space-6  |    24px    |   1.5rem    | Wide spacing: perimeter screen padding, separation between functional sections. |
| --dt-space-8  |    32px    |   2.0rem    | Separation of major blocks in desktop views (Dashboards).                        |
| --dt-space-12 |    48px    |   3.0rem    | Separation between macro-level containers or 2D viewer margins.                |
| --dt-space-16 |    64px    |   4.0rem    | Structural margins on high-resolution monitors (1920x1080).                        |

### 2.2. Dimensions of Controls and Touch Areas
| Control Token | Min Height (px) | Min Width (px) | Target Platform / Justification                                                                |
| ------------------------ | ------------------ | ----------------- | -------------------------------------------------------------------------------------------------- |
| --dt-touch-target-mobile | 48px               | 48px              | **Mandatory minimum on Tablet/Mobile:** Action buttons, LOTO checkboxes, and field selectors. |
| --dt-control-height-sm   | 32px               | auto              | Desktop Web: Compact buttons in dense data tables and secondary filters.                    |
| --dt-control-height-md   | 40px               | auto              | Desktop Web: Standard text inputs, selectors, and form buttons.                       |
| --dt-control-height-lg   | 48px               | auto              | Mobile/Tablet: Standard height for all input fields (InputText, InputSelect).          |
| --dt-control-height-xl   | 56px               | 100%              | Mobile: Primary footer action button (e.g., "Complete Work Order").            |

### 2.3. Responsive Breakpoints and Reference Frames

The designs and responsive adaptation rules in CSS are calibrated against the following form factors and standard canvas resolutions:

| Breakpoint Token | Min Width (px) | Base Canvas Dimensions (W x H) | Aspect Ratio | Reference Device | Layout and Container Disposition |
| :------------------ | :---------------: | :-----------------------------: | :-----------------: | :--------------------------------------------------- | :--------------------------------------------- |
| --dt-breakpoint-sm  |       390px       |          390 x 844 px           |      $9:19.5$       | Vertical Smartphone (iOS / Android)                  | 1 column; bottom bar navigation.      |
| --dt-breakpoint-md  |       768px       |          768 x 1024 px          |        $3:4$        | Vertical Tablet / Industrial Collector                | 1 to 2 columns; collapsible drawer.             |
| --dt-breakpoint-lg  |      1280px       |          1280 x 800 px          |       $16:10$       | **Industrial Tablet (Zebra ET51 / Honeywell RT10A)** | 2 columns (SVG Canvas + Contextual panel).    |
| --dt-breakpoint-xl  |      1920px       |         1920 x 1080 px          |       $16:9$        | Desktop Workstation (Full HD)                | 3 columns (Sidebar + Central Panel + Drawer). |

---

## 3. Color Tokens and Surfaces
The palette is structured in two layers: **Primitive Tokens** (absolute palette values, **where the only declaration of HEX codes resides in the design document**) and **Semantic Tokens** dynamically assigned based on the operational lighting context (Dark Theme and Light Theme), which reference the primitive variables.

### 3.1. Primitive Palette Tokens
| Primitive Token | Hex Value | Family / Base Use                                                   |
| ------------------------ | --------- | -------------------------------------------------------------------- |
| --dt-primitive-gray-980  | #111827   | High-contrast black for text in light theme (Tailwind gray-900) |
| --dt-primitive-gray-950  | #11141A   | Deep neutral tone (Extreme UI background)                      |
| --dt-primitive-gray-900  | #16191F   | Dark neutral tone (Canvas in dark theme)                      |
| --dt-primitive-gray-850  | #1F2937   | Charcoal gray for base text in light theme                            |
| --dt-primitive-gray-800  | #1E222B   | Dark base neutral tone (App background in dark theme)         |
| --dt-primitive-gray-700  | #2A2F3D   | Intermediate dark surface (Cards in dark theme)                    |
| --dt-primitive-gray-650  | #3A4154   | Subtle dark border (Layer differentiation in dark theme)               |
| --dt-primitive-gray-620  | #4B5563   | Medium gray for secondary text in light theme (Tailwind gray-600)        |
| --dt-primitive-gray-600  | #353B4D   | Elevated dark surface (Floating panels / Modals in dark theme)    |
| --dt-primitive-gray-580  | #4A5263   | Disabled gray for dark background                                 |
| --dt-primitive-gray-550  | #6B7280   | Focused input border in light theme (Tailwind gray-500)                  |
| --dt-primitive-gray-500  | #5C667A   | Neutral border and interactive element                                  |
| --dt-primitive-gray-450  | #6E7A92   | Focused input border in dark theme                                     |
| --dt-primitive-gray-420  | #8A98AA   | Light gray for secondary text in dark theme                           |
| --dt-primitive-gray-400  | #7E8B9B   | Secondary and muted text overall                                  |
| --dt-primitive-gray-380  | #9CA3AF   | Disabled gray for light background (Tailwind gray-400)              |
| --dt-primitive-gray-350  | #AAB1BD   | Subtle intermediate border for controls in light theme                  |
| --dt-primitive-gray-300  | #B8C0CC   | Borders on light background                                                |
| --dt-primitive-gray-280  | #C2CBD6   | Light gray for base text in dark theme                                 |
| --dt-primitive-gray-200  | #D8DBE0   | Light neutral gray (Munsell N7.5 / Hollifield / Canvas in light)      |
| --dt-primitive-gray-100  | #E5E8EC   | Base light surface (App background in light theme)                 |
| --dt-primitive-gray-50   | #F4F5F7   | Light card surface (Cards in light theme)                      |
| --dt-primitive-gray-10   | #FDFEFE   | High-contrast off-white for text in dark theme              |
| --dt-primitive-white     | #FFFFFF   | Pure white (Canvas, elevated backgrounds)                                |
| --dt-primitive-red-600   | #E63946   | Industrial alarm red                                            |
| --dt-primitive-amber-600 | #AC5E04   | Amber / Warning on light background (Adjusted WCAG AA 3.47:1)         |
| --dt-primitive-amber-500 | #D97706   | Ámbar / Advertencia base                                             |
| --dt-primitive-amber-400 | #F4A261   | Amber / Warning on dark background                                  |
| --dt-primitive-blue-700  | #0369A1   | Normal MAI operation zone on dark background                         |
| --dt-primitive-blue-600  | #2563EB   | Informational blue on light background                                      |
| --dt-primitive-blue-450  | #4881A4   | Informational blue on dark background (Adjusted WCAG AA 3.15:1)           |
| --dt-primitive-blue-400  | #457B9D   | Azul informativo base                                                |
| --dt-primitive-blue-200  | #BAE6FD   | Normal MAI operation zone on light background                          |
| --dt-primitive-teal-700  | #0B857A   | Documentary confirmation on light background (Adjusted WCAG AA 3.25:1)     |
| --dt-primitive-teal-600  | #0D9488   | Confirmación documental base                                         |
| --dt-primitive-teal-400  | #2A9D8F   | Documentary confirmation on dark background                              |

### 3.2. Semantic Tokens for Light and Dark Themes
*Application of the 90% neutral surfaces HPHMI rule using direct references to primitive tokens*

| Semantic Token | Dark Theme (Mobile / Night) | Light Theme (Desktop / Day) | Interface Application                                                  |
| -------------------------- | --------------------------- | ----------------------------- | ----------------------------------------------------------------------- |
| --dt-color-bg-canvas       | --dt-primitive-gray-900     | --dt-primitive-gray-200       | 2D canvas background / Floor plan                                   |
| --dt-color-surface-base    | --dt-primitive-gray-800     | --dt-primitive-gray-100       | App background / Header                                         |
| --dt-color-surface-card    | --dt-primitive-gray-700     | --dt-primitive-gray-50        | Asset cards / Table rows                                    |
| --dt-color-surface-raised  | --dt-primitive-gray-600     | --dt-primitive-white          | Modals / Floating panels                                             |
| --dt-color-border-subtle   | --dt-primitive-gray-650     | --dt-primitive-gray-300       | Dividing lines / Separators                                         |
| --dt-color-border-focus    | --dt-primitive-gray-450     | --dt-primitive-gray-550       | Focused input border (Dark Theme adjusted to 3.09:1 WCAG AA)          |
| --dt-color-text-muted      | --dt-primitive-gray-420     | --dt-primitive-gray-620       | Units of measurement / Timestamps (Dark Theme adjusted to 4.55:1 WCAG AA) |
| --dt-color-text-body       | --dt-primitive-gray-280     | --dt-primitive-gray-850       | Main text / Table values                                      |
| --dt-color-text-primary    | --dt-primitive-gray-10      | --dt-primitive-gray-980       | Titles / Critical values                                              |
| --dt-color-mai-track       | --dt-primitive-gray-700     | --dt-primitive-gray-100       | Analog MAI indicator track background                              |
| --dt-color-mai-normal-zone | --dt-primitive-blue-700     | --dt-primitive-blue-200       | Normal operation range strip in MAI                              |
| --dt-color-mai-pointer     | --dt-primitive-gray-10      | --dt-primitive-gray-980       | MAI current value pointer                                             |
| --dt-color-mai-interlock   | --dt-primitive-gray-10      | --dt-primitive-gray-980       | MAI interlock trip limit marker                    |

### 3.3. Alarm and Safety Semantics (10% Reserved)

| State / Severity | Color Token | Value (Dark Theme) | Value (Light Theme) | Mandatory Symbol                                                 |
| --------------------------------- | ------------------------- | ------------------------ | ------------------------ | ------------------------------------------------------------------- |
| **Critical Alarm / LOTO Danger** | --dt-color-alarm-critical | --dt-primitive-red-600   | --dt-primitive-red-600   | Square / Octagon                                                 |
| **Warning / Approaching Limit**  | --dt-color-alarm-warning  | --dt-primitive-amber-400 | --dt-primitive-amber-600 | Triangle (Adjusted WCAG AA 3.47:1 on light background)                  |
| **Informational / Selection**       | --dt-color-state-info     | --dt-primitive-blue-450  | --dt-primitive-blue-600  | Circle / Rhombus (Adjusted WCAG AA 3.15:1 on dark background)           |
| **Documentary Confirmation**       | --dt-color-state-success  | --dt-primitive-teal-400  | --dt-primitive-teal-700  | Checkmark ( $\checkmark$ ) (Adjusted WCAG AA 3.25:1 on light background) |
| **Disabled Element**        | --dt-color-state-disabled | --dt-primitive-gray-580  | --dt-primitive-gray-380  | Dotted border                                                      |

---

## 4. Typographic Tokens
Typography is defined under a dual model: high-availability native fonts in the design engine (Google Fonts in Penpot) and comprehensive fallback stacks (*System Fallbacks*) for production web stylesheets.

### 4.1. Typographic Families
| Typographic Role | Base Font (Penpot / Design) | Fallback Stack (CSS / Web) | Application Use |
| :------------------ | :---------------------------- | :------------------------------------------------- | :------------------------------------------------ |
| Primary Sans-Serif | Inter                         | Segoe UI, Inter, Roboto, -apple-system, sans-serif | Titles, labels, descriptions, and controls     |
| Monospaced       | Roboto Mono                   | Cascadia Code, SF Mono, Consolas, monospace        | Equipment tags (P-101), hashes, IPs and timestamps |

### 4.2. Typographic Scale
| Typographic Token | Size (px) | Size (rem) | Line Height (px) | Weight (Font-Weight) | Standard Application Use |
| :------------------ | :---------- | :----------- | :------------------- | :----------------- | :-------------------------------------------------------------- |
| --dt-font-display   | 28px        | 1.75rem      | 36px                 | Bold (700)         | Executive-level macro KPIs on Dashboard L1                  |
| --dt-font-h1        | 22px        | 1.375rem     | 28px                 | SemiBold (600)     | Main screen title / Asset name on L3 Card |
| --dt-font-h2        | 18px        | 1.125rem     | 24px                 | SemiBold (600)     | Card headers, modal titles, and side panels |
| --dt-font-body-lg   | 16px        | 1.0rem       | 24px                 | Regular (400)      | Text for input fields on mobile, main reading of WOs   |
| --dt-font-body-md   | 14px        | 0.875rem     | 20px                 | Regular (400)      | Text for table cells, technical descriptions and menus        |
| --dt-font-caption   | 12px        | 0.75rem      | 16px                 | Medium (500)       | Floating form labels, metadata, log authorship  |
| --dt-font-mono-data | 13px        | 0.8125rem    | 16px                 | Medium (500)       | Industrial tags (P-101), cryptographic hashes, IPs, and times    |

---

## 5. Elevation, Borders and Depth Tokens
To comply with the HPHMI philosophy in dark interfaces, depth is not expressed through decorative or diffuse shadows, but through normative **surface color differentiation and subtle borders**.

### 5.1. Border Radii
| Token | Value (px) | Component Application |
| ---------------- | ---------- | -------------------------------------------------------------- |
| --dt-radius-none | 0px        | 2D map canvas, full-bleed mobile containers.           |
| --dt-radius-sm   | 4px        | Status badges, equipment class tags, checkboxes.         |
| --dt-radius-md   | 6px        | Text fields (InputText), selectors, standard buttons.     |
| --dt-radius-lg   | 8px        | Information cards (Cards), side panels, dropdowns. |
| --dt-radius-xl   | 12px       | Modal windows, LOTO lockout dialogs.                    |

### 5.2. Layers and Stacking Levels (Z-Index Hierarchy)
| Z-Index Token          | Value | Assigned Elements                                                  |
| ---------------------- | ----- | -------------------------------------------------------------------- |
| --dt-z-canvas          | 0     | SVG vector base layer (Floor plan).                           |
| --dt-z-layer-ptw       | 10    | Work Permits overlapping graphic layer [[VIS-008]].         |
| --dt-z-layer-loto      | 20    | LOTO Traceability graphic layer [[VIS-011]].                       |
| --dt-z-overlay-card    | 100   | Asset pop-up card (Asset Quick-Card L3 / VIS-033).         |
| --dt-z-header-sticky   | 500   | Fixed top navigation bar and network status.                   |
| --dt-z-drawer-sidebar  | 800   | Collapsible navigation side panel.                             |
| --dt-z-modal           | 1000  | Standard modal windows (WO Creation, Asset Swap).                 |
| --dt-z-modal-fail-safe | 1500  | **Critical LOTO Danger / Active lockout modal (Non-dismissible).** |
| --dt-z-toast-alert     | 2000  | Disconnection alerts and SignalR toast notifications.            |

---

## 6. Industrial Visual Patterns and Redundant Coding

### 6.1. Moving Analog Indicator (MAI) Specification
In compliance with ISA-101.01 and *The High Performance HMI Handbook* (Hollifield et al., Ch. 7), continuous process variables (pressure, temperature, flow, vibration) must not be presented solely as numeric digits. They must use the Moving Analog Indicator (MAI) pattern to allow rapid condition evaluation in under 2 seconds.

#### Light Theme (Control Room / Desktop - 500 Lux)
![[assets/MAI-light.svg]]
#### Dark Theme (Field Operation / Tablet / Night)
![[assets/MAI-dark.svg]]

#### 6.1.1. Dual-Theme Semantic Token Table for MAI
To avoid direct coupling of hexadecimal codes and ensure compatibility between the Control Room (Light Theme) and Field Operation (Dark Theme), frontend interface components must consume the following token matrix:

| MAI Graphic Element | Semantic CSS / C# Token | Light Theme (Desktop / Day) | Dark Theme (Mobile / Night) | HPHMI / ISA-101 Ergonomic Function                                                       |
| ----------------------------------------------- | --------------------------------- | -------------------------- | --------------------------- | --------------------------------------------------------------------------------------- |
| **Base Track**                          | --dt-color-mai-track              | --dt-primitive-gray-300    | --dt-primitive-gray-700     | Indicator perimeter background (Height $8\text{px}$, Radius $4\text{px}$).                 |
| **Base Track Border**                         | --dt-color-mai-track-border       | --dt-primitive-gray-350    | --dt-primitive-gray-650     | Subtle outline (`1px`) to define the absolute limits of the instrument scale. |
| **Normal Operating Zone**                    | --dt-color-mai-normal-zone        | --dt-primitive-blue-200    | --dt-primitive-blue-700     | **Light blue strip** for pre-attentive recognition of the safe range.                |
| **Normal Zone Border**                        | --dt-color-mai-normal-zone-border | --dt-primitive-blue-400    | --dt-primitive-blue-450     | Outline (`0.5px` or `1px`) to improve the contrast of the safe blue block.            |
| **Current Value Pointer**                     | --dt-color-mai-pointer            | --dt-primitive-gray-980    | --dt-primitive-gray-10      | Moving circular pointer. **Maintains shape and neutral color.** Border `2px`.                 |
| **Pointer Border**                           | --dt-color-mai-pointer-border     | --dt-primitive-white       | --dt-primitive-gray-980     | High-contrast outline for visibility over the normal zone.                       |
| **High Alarm Indicator (P1)**               | --dt-color-alarm-critical         | --dt-primitive-red-600     | --dt-primitive-red-600      | **Separate element (Method 3):** Red square + '1' appearing next to the limit.      |
| **Text on Critical Alarm**                  | --dt-color-alarm-text-critical    | --dt-primitive-white       | --dt-primitive-white        | High contrast text on red square ($4.6:1$ WCAG AA).                          |
| **Low Alarm / Warning Indicator (P2)** | --dt-color-alarm-warning          | --dt-primitive-amber-600   | --dt-primitive-amber-400    | **Separate element (Method 3):** Amber triangle + '2' (Adjusted WCAG AA $3.47:1$).    |
| **Text on Amber Warning**               | --dt-color-alarm-text-warning     | --dt-primitive-white       | --dt-primitive-gray-900     | High contrast text on Amber ($5.36:1$ on light, $8.5:1$ on dark).             |
| **Interlock Limit**          | --dt-color-mai-interlock          | --dt-primitive-gray-980    | --dt-primitive-gray-10      | Solid block at the end indicating automatic safety trip.                 |

#### 6.1.2. Dynamic Behavior and Alarm Rules
1. **Background Track and Normal Zone:** The track covers $100\%$ of the instrument's calibrated scale. The Normal Operation Zone is rendered as a highlighted inner segment in light blue (`--dt-color-mai-normal-zone`).
2. **Pointer Invariance:** The current value pointer does not alter its shape or neutral color when crossing alarm thresholds. This preserves the spatial reference point and avoids cognitive distortions.
3. **Alarm Presentation (Hollifield Method 3):**
    * **High Deviation (High / High-High):** When crossing the upper threshold, a **separate alarm element** appears adjacent to the scale at the point of infraction. A red square (`--dt-color-alarm-critical`) with priority number 1 for Critical Alarm is presented.
    * **Low Deviation (Low / Low-Low):** When crossing the lower threshold, an **amber triangle** (`--dt-color-alarm-warning`) appears adjacent with priority number 2 for Warning.
4. **Safety and Interlock Limits (Safety Interlock):** The ends of the scale that trigger automatic shutdowns (ESD) are marked with a solid rectangle (`--dt-color-mai-interlock`) at the corresponding end.

### 6.2. Redundant Coding Matrix for Permits and LOTO

| Safety Concept | Main Color / Token | Geometric Shape | Associated Icon | Mandatory Text   |
| ------------------------------------- | ------------------------- | ------------------------------------- | -------------------------- | ------------------- |
| **Hot Work Permit**    | --dt-color-alarm-critical | Square ( $24\times24\text{px}$ )    | Flame ( `flame` )          | HOT WORK            |
| **Heights Permit**      | --dt-color-state-info     | Triangle ( $24\times24\text{px}$ )   | Ladder / Harness           | HEIGHTS             |
| **Confined Space**      | --dt-color-alarm-warning  | Circle ( $\varnothing 24\text{px}$ ) | Silhouette / Tank           | CONFINED            |
| **LOTO Point Locked (Safe)**     | --dt-color-state-success  | Closed padlock                       | Padlock ( `lock` )         | ISOLATED - 0 ENERGY |
| **LOTO Point Energized (Danger)**   | --dt-color-alarm-critical | Open padlock with halo              | Lightning / Alert              | DANGER - ENERGIZED  |
| **Telemetry Loss (Fail-Safe)** | --dt-color-alarm-warning  | Rhombus                                 | Disconnection ( `wifi-off` ) | SIGNAL LOST - STALE |

### 6.3. Sliding Containers Pattern (*Bottom Sheets* and *Drawers*)
In compliance with the principle of **Controllability** (ISO 9241-110:2020, Clause 5.5) and to mitigate the low precision of capacitive sensors when operating with industrial gloves or in wet conditions, mobile sliding containers must follow these guidelines:

1. **Exclusive Gesture Prohibition:** It is forbidden to condition the deployment, collapse, or closure of a container exclusively to continuous drag or swipe gestures (*swipe/drag*).
2. **Dedicated Physical Trigger:** Every container must integrate an explicit interactive element (handle or touch header) whose touch area dimensions inherit the `--dt-touch-target-mobile` token.
3. **Discrete Switching:** A simple press (*tap*) on this element must sequentially toggle between the defined states for the component (Collapsed, Partial View, Expanded), guaranteeing operation without requiring fine motor skills.
---

## 7. Design System CSS Variables File

For physical implementation in web style sheets or decoupled components, consult the canonical file:
`ui-ux/assets/tokens.css`