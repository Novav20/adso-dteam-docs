---
name: dteam-coherence-audit
description: >-
  Auditor de coherencia para el repositorio docs-as-code del proyecto DTEAM
  (Gemelo Digital EAM, sector Oil & Gas). Verifica que cada nuevo artefacto
  principal no rompa la trazabilidad, la coherencia normativa ni el alcance
  aprobado del MVP. Úsalo cuando el usuario diga "audita este artefacto",
  "verifica coherencia de [archivo]", "revisa si este documento es consistente"
  o similar. También invocable por CLI con `uv run audit.py audit --file <ruta>`.
---

# DTEAM Docs-as-Code — Auditor de Coherencia

## Descripción General

Esta skill ejecuta tres ejes de verificación sobre un artefacto candidato
antes de que sea integrado formalmente al repositorio `adso-gemelo-digital-docs`:

1. **Trazabilidad de Referencias** — Valida que todos los IDs citados (UC-XXX,
   SCR-XXX, ADR-NNN, ASR-NNN, DT-UI-*) existan como archivos reales en el repo.
2. **Coherencia Normativa** — Verifica que colores, niveles ISA-101, roles RBAC
   y cliente target sean consistentes con los artefactos canónicos aprobados.
3. **Scope Guard** — Detecta si el artefacto introduce pantallas, casos de uso,
   actores o tecnologías que no pertenecen al índice aprobado del MVP.

La skill **nunca modifica** el artefacto auditado. Solo reporta hallazgos
con severidades BLOCKER / WARNING / INFO y genera un informe Markdown en
`compliance/`.

---

## Activación desde el Chat

El agente debe activar esta skill cuando detecte frases como:
- "audita [archivo]"
- "verifica la coherencia de [documento]"
- "¿este artefacto rompe algo?"
- "revisa consistencia de [ruta]"
- "check coherence"
- "coherence audit"

---

## Workflow

### Paso 1 — Identificar el Artefacto Candidato

Determina la ruta absoluta del artefacto a auditar:
- Si el usuario la menciona explícitamente, úsala.
- Si el usuario describe el artefacto por nombre/código (ej. "DT-UI-NAV-DOC-001"),
  búscalo con `find . -name "*NAV-DOC-001*"` desde la raíz del repositorio.

La raíz del repositorio es siempre:
`/home/novillus/Documents/vscode/SENA-Career/adso-gemelo-digital-docs`

### Paso 2 — Ejecutar el Helper Script

Desde la raíz del repositorio, ejecuta:

```bash
cd /home/novillus/Documents/vscode/SENA-Career/adso-gemelo-digital-docs
uv run .agents/skills/dteam-coherence-audit/scripts/audit.py audit --file <ruta-relativa>
```

El script genera automáticamente el informe en `compliance/`.

### Paso 3 — Presentar Resultados al Usuario

Lee el informe generado y preséntalo de forma estructurada:
1. Muestra el veredicto global (✅ APROBADO / ⚠️ CONDICIONAL / 🔴 BLOQUEADO).
2. Lista todos los hallazgos BLOCKER primero, WARNING después, INFO al final.
3. Para cada BLOCKER, explica el impacto específico en el proyecto DTEAM.
4. Pregunta al usuario cómo desea proceder con los hallazgos.

### Paso 4 — Modo Auditoría Completa del Repositorio (Opcional)

Si el usuario pide "audita todo el repositorio" o "modo CI":

```bash
cd /home/novillus/Documents/vscode/SENA-Career/adso-gemelo-digital-docs
uv run .agents/skills/dteam-coherence-audit/scripts/audit.py audit-all \
  --output compliance/AUD-FULL-REPO.md
```

---

## Subcomandos Disponibles

| Subcomando | Propósito |
| :--- | :--- |
| `audit --file <ruta>` | Auditoría completa de un artefacto + informe Markdown |
| `check-refs --file <ruta>` | Solo trazabilidad de referencias (rápido) |
| `check-scope --file <ruta>` | Solo verificación de scope guard |
| `audit-all --output <ruta>` | Escanea todos los artefactos del repositorio |

---

## Interpretación de Exit Codes

| Exit Code | Significado |
| :--- | :--- |
| `0` | Sin hallazgos o solo WARNING/INFO — artefacto aprobado con observaciones |
| `1` | Error de ejecución (archivo no encontrado, fuera del repo) |
| `2` | BLOCKER encontrado — el artefacto NO debe integrarse sin corrección |

---

## Errores Comunes

- **"Archivo no encontrado"**: Verifica que la ruta sea relativa a la raíz del repo.
- **"No es un repositorio git"**: El script debe ejecutarse desde dentro de `adso-gemelo-digital-docs/`.
- **"ID no en índice MVP"**: El ID referenciado puede ser legítimo pero el índice del script requiere actualización manual — consulta al arquitecto antes de modificarlo.
