---
name: dteam-srs-quality-audit
description: >-
  Auditor de calidad y DDD (Domain-Driven Design) para la base de datos maestra 
  de requerimientos (srs.csv) del proyecto DTEAM. Verifica la rigurosidad de 
  las referencias normativas (ISO, NIST), el uso correcto de ISO 25010:2023, y 
  la ausencia de términos legacy o genéricos (como "activo" en lugar de 
  "Equipment Unit"). Úsalo cuando el usuario diga "audita los requerimientos", 
  "revisa el dataset srs.csv" o "verifica la calidad de los requisitos".
---

# DTEAM Docs-as-Code — Auditor de Calidad SRS

## Descripción General

Esta skill ejecuta un análisis programático directamente sobre el archivo 
`requirements/data/srs.csv` para garantizar que la ingeniería de requisitos 
se mantiene en el estándar más alto exigido por el proyecto DTEAM.

Evalúa tres ejes fundamentales:
1. **ISO 25010:2023:** Garantiza que no se utilicen categorías depreciadas 
   (como *Usability* o *Portability*) en favor de las actuales (*Interaction Capability*, *Flexibility*, etc.).
2. **Domain-Driven Design (DDD):** Escanea las descripciones en busca de 
   términos genéricos prohibidos (ej. "activo") para forzar el uso del 
   Lenguaje Ubicuo (ej. "Equipment Unit" / "Maintainable Item" según ISO 14224).
3. **Referencias Normativas:** Valida con expresiones regulares que la columna 
   `Normative Reference` cite estándares accionables (ISO, NIST, OWASP, ACID, etc.) 
   en lugar de texto genérico (como "UX Best Practices").

## Activación desde el Chat

El agente debe activar esta skill cuando detecte:
- "Audita el dataset srs.csv"
- "Revisa la calidad de los requerimientos"
- "Verifica si usamos bien el lenguaje de dominio en el CSV"
- "Check SRS quality"

## Workflow

### Paso 1 — Ejecutar el Script de Auditoría

Desde la raíz del repositorio, ejecuta el script Python que analizará el CSV:

```bash
cd /home/novillus/Documents/vscode/SENA-Career/adso-dteam-docs
uv run .agents/skills/dteam-srs-quality-audit/scripts/srs_audit.py
```

### Paso 2 — Presentar Resultados

El script retornará un resumen con severidades BLOCKER, WARNING e INFO.
1. Muestra al usuario el veredicto.
2. Si hay **BLOCKERS** (ej. categorías ISO inválidas o referencias faltantes en TRs), 
   informa que el CSV debe ser corregido antes de poder regenerar las User Stories.
3. Si hay **WARNINGS** (violaciones del lenguaje de dominio o referencias débiles), 
   enuméralas y pregunta al usuario si desea corregirlas.

### Paso 3 — Interpretar Exit Codes

| Exit Code | Significado |
| :--- | :--- |
| `0` | Aprobado (puede contener Warnings/Infos pero no rompe el sistema) |
| `1` | Error catastrófico (no se encontró el CSV o faltan columnas clave) |
| `2` | BLOCKER encontrado — Categorías inválidas o reglas arquitectónicas rotas |
