# Plot Plan Generator (`plot_plan_generator`)

Motor modular en Python para la generación automatizada de planos 2D General Arrangement (GA) y gemelos digitales espaciales, conforme al estándar industrial **`DT-UI-SVG-DOC-001` Rev 2.0** y los lineamientos de **High-Performance HMI (ANSI/ISA-101 / Hollifield)**.

---

## 🚀 Guía de Ejecución

El generador está estructurado como un paquete ejecutable de Python (`python3 -m scripts.plot_plan_generator`).

### 1. Comando Básico (Generación Estándar para Prototipo)

Desde la raíz del repositorio `adso-dteam-docs`:

```bash
# Genera el plano L1 limpio con validación automática
python3 -m scripts.plot_plan_generator.cli ../sena-evidence/00-Overview/Protoyping/ui-prototype/assets/tfa_terminal_plot_plan.svg --validate
```

### 2. Generación Multi-Nivel de Zoom (`--all-zooms`)

Genera concurrentemente los archivos macro, intermedio y micro (`tfa_terminal_plot_plan.svg`, `_l2.svg`, `_l3.svg`):

```bash
python3 -m scripts.plot_plan_generator.cli ../sena-evidence/00-Overview/Protoyping/ui-prototype/assets/tfa_terminal_plot_plan.svg --all-zooms --validate
```

### 3. Modo Oscuro HPHMI (`--theme=dark`)

Genera el plano con la paleta nocturna/tableta de alto rendimiento:

```bash
python3 -m scripts.plot_plan_generator.cli assets/tfa_terminal_dark.svg --theme=dark --validate
```

### 4. Inclusión de Tablas CAD de Ingeniería (`--include-cad-tables`)

Por defecto, los planos de gemelo digital omiten tablas estáticas de dibujo en papel. Si se requiere depuración o documentación impresa:

```bash
python3 -m scripts.plot_plan_generator.cli assets/tfa_terminal_cad.svg --include-cad-tables --validate
```

### 5. Uso de Archivo de Temas Externo (`--theme-file`)

Permite desacoplar los tokens de color del código Python mediante un archivo JSON externo:

```bash
python3 -m scripts.plot_plan_generator.cli assets/tfa_terminal_custom.svg --theme-file=scripts/plot_plan_generator/themes.json --theme=dark
```

---

## ⚙️ Argumentos del CLI

| Argumento | Tipo | Por Defecto | Descripción |
| :--- | :---: | :---: | :--- |
| `output_path` | Posicional | *(Obligatorio)* | Ruta destino del archivo SVG (o directorio). |
| `--theme` | Opción | `light` | Selector de paleta de color (`light` o `dark`). |
| `--theme-file` | Path | `themes.json` | Ruta a archivo JSON con especificación de temas y tokens de diseño. |
| `--include-cad-tables` | Flag | `False` | Incluye cajetín de rotulación, tablas de cubicaje NFPA 30 y leyenda estática. |
| `--validate` | Flag | `False` | Ejecuta validación topológica, distancias NFPA 30 y conformidad de esquema XML. |
| `--all-zooms` | Flag | `False` | Emite automáticamente las variantes semánticas `_l2.svg` y `_l3.svg`. |

---

## 🏗️ Estructura del Paquete

```
plot_plan_generator/
├── __init__.py          # Metadatos del paquete.
├── __main__.py          # Punto de entrada para ejecución como módulo (`python -m`).
├── cli.py               # Orquestación de argumentos de línea de comandos.
├── config.py            # Constantes físicas (0.2 m/unit, 2000x1500), rotación (49°) y carga de temas.
├── themes.json          # Single Source of Truth para tokens de color y mapeo a DT-UI-DS-DOC-001.
├── builder.py           # Coordinador de capas, defs XML, inyección de metadatos MOC y estilos CSS.
├── core/
│   ├── geometry.py      # Transformaciones de malla UV, proyecciones vectoriales, clipping y miter offsets.
│   └── svg_primitives.py# Constructores de elementos XML (rect, circle, line, path, text, G).
├── domain/
│   ├── plant_data.py    # Entidades de Tank Farm Alpha (tanques, viales, durmientes, bombas, edificios).
│   ├── process_safety.py# Reglas de proceso: cubicaje de cubetos NFPA 30 (110%) y separación D/6.
│   └── validation.py    # Suite de assertions geométricas, conectividad de tuberías y esquema XML.
└── layers/
    ├── civil.py         # L-CIVL-BOTM: Viales, límites de propiedad, cubetos, durmientes, edificios.
    ├── mechanical.py    # L-MECH-EQPM: Tanques API 650, patines de bombas, bahías de carga, escaleras.
    ├── piping.py        # L-PIPE-PROC: Tuberías principales con loops, colectores, manifolds, válvulas.
    ├── fire.py          # L-FIRE-PROT: Anillo contra incendios, hidrantes FH y torres monitoras FM.
    └── annotation.py    # L-ANNO-TEXT: Malla 40m, tags de equipos, cotas, vector de calibración y tablas CAD.
```

---

## 🎨 Integración de Tokens de Diseño (`themes.json`)

Para evitar la fragilidad de tener colores hexadecimales hardcodeados en el código, los temas se cargan dinámicamente desde `themes.json`:

1. **Alineación con `DT-UI-DS-DOC-001`:**
   - Cada color está referenciado contra los grises primitivos del Design System (`--dt-primitive-gray-*`).
   - **Regla HPHMI 90/10:** El 100% de los elementos estáticos del plano emplean tonos neutros, reservando el color saturado exclusivamente para estados dinámicos de alarma operativa en vivo.
2. **Materiales Físicos:**
   - `ASPH`: Superficies de asfalto para viales y playas de maniobra.
   - `CONC`: Hormigón armado para muros de cubetos y cimentaciones.
   - `STEEL`: Acero estructural para durmientes de tubería y vigas de gantry.
   - `BUNDFILL`: Suelo de contención secundaria.

---

## 🛡️ Contrato de Ingesta y Calidad (`DT-UI-SVG-DOC-001`)

Todo SVG emitido por esta herramienta cumple estrictamente con:
- **7 Capas Normativas:** `L-CIVL-BOTM`, `L-MECH-EQPM`, `L-INSP-INST`, `L-PIPE-PROC`, `L-FIRE-PROT`, `L-ELEC-HAZ`, `L-ANNO-TEXT`.
- **Enlace de Datos ISO 14224:** Atributos `data-cmp-id`, `data-func-loc`, `data-equip-id` y `data-status` en todos los hotspots interactivos.
- **Auditoría MOC:** Encabezados `<svg>` con `data-moc-id`, `data-rev-number` y `data-checksum-sha256`.
- **Vector de Calibración:** Línea oculta `CALIBRATION-VECTOR` con `data-real-meters="200.0"` para escalamiento métrico nativo en el cliente.
