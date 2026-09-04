# 🛠️ Automatizaciones y Generadores Docs-as-Code

Este directorio contiene los scripts de soporte para la sincronización y generación automatizada de documentos Markdown a partir de los datos maestros tabulares (`requirements/data/`).

## `generate_design_tokens.py`

Genera `ui-ux/assets/tokens.css` a partir de las tablas y definiciones de
`ui-ux/DT-UI-DS-DOC-001.md`. El CSS es un artefacto generado; los cambios deben
hacerse en el documento Markdown y después regenerarse:

```bash
python3 scripts/generate_design_tokens.py
```

También admite rutas explícitas para validaciones o fuentes alternativas:

```bash
python3 scripts/generate_design_tokens.py \
	--source ui-ux/DT-UI-DS-DOC-001.md \
	--target ui-ux/assets/tokens.css
```

---

## 📌 `generate_requirements_docs.py`

Script unificado encargado de compilar:
1. **Requisitos Transversales (`TR-001` a `TR-011` e `INDEX.md`):** Generados en `requirements/common/`.
2. **Historias de Usuario (US):** Agrupadas por módulo/epic (`adm/`, `inv/`, `mtto/`, `vis/`) en `requirements/user-stories/`.

### 🛡️ Seguridad por Defecto (Dry-Run)
El script **nunca sobreescribe archivos por defecto**. Si se ejecuta sin parámetros, opera en modo de simulación (*dry-run*), indicando en consola qué archivos serían creados o modificados.

---

## 🚀 Ejemplos de Uso

### 1. Simulación General (Verificar qué cambiaría)
```bash
python scripts/generate_requirements_docs.py
```

### 2. Ver Diferencias Exactas Línea por Línea (Diff)
```bash
python scripts/generate_requirements_docs.py --diff
```

### 3. Aplicar Cambios en Disco (Escritura Real)
```bash
python scripts/generate_requirements_docs.py --write
```

### 4. Generar y Actualizar el `INDEX.md` de Requisitos Transversales
```bash
python scripts/generate_requirements_docs.py --write --write-index
```

### 5. Filtrar por Módulo Específico (ej. solo Mantenimiento e Inventario)
```bash
python scripts/generate_requirements_docs.py --modules MTTO INV --write
```

### 6. Filtrar por ID Específico (ej. una sola US o un solo TR)
```bash
python scripts/generate_requirements_docs.py --ids MTTO-001 TR-003 --write
```

### 7. Generar Solo Historias de Usuario o Solo Transversales
```bash
# Solo Historias de Usuario
python scripts/generate_requirements_docs.py --only-us --write

# Solo Requisitos Transversales (COMMON)
python scripts/generate_requirements_docs.py --only-tr --write
```

---

## 📂 Mapeo de Rutas Predeterminadas

| Origen (CSV Maestro) | Destino Generado (Markdown) | Formato / Contenido |
| :--- | :--- | :--- |
| `requirements/data/srs.csv` + `transversal-requirements.csv` | `requirements/common/TR-xxx.md` | Contexto transversal, tablas FR/NFR y referencias normativas. |
| `requirements/data/srs.csv` + `user-stories.csv` + `gherkin.csv` | `requirements/user-stories/{epic}/{US-ID}.md` | Como/Quiero/Para, Criterios de Aceptación Gherkin, tablas FR/NFR y trazabilidad. |