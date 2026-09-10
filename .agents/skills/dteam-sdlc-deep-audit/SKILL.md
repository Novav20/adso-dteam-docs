---
name: dteam-sdlc-deep-audit
description: >-
  Auditor en profundidad del repositorio docs-as-code del proyecto DTEAM.
  Realiza un análisis holístico y cronológico de los artefactos (SDLC) para detectar
  redundancias cross-layer, contradicciones lógicas a lo largo del tiempo,
  y decisiones arquitectónicas sin un ADR que las justifique.
  Úsalo cuando se solicite una auditoría completa, profunda o al final de un milestone.
---

# DTEAM Docs-as-Code — Auditor de Ciclo de Vida (SDLC Deep Audit)

## Descripción General

Esta skill ejecuta un análisis exhaustivo e histórico del estado de la documentación en el repositorio `adso-dteam-docs`. A diferencia de `dteam-coherence-audit` (que evalúa un artefacto individual al ser añadido), esta skill evalúa **todo el repositorio** leyendo los artefactos en el orden en que se supone que fueron creados según el SDLC (Software Development Life Cycle).

Su propósito es identificar:
1. **Redundancias Inter-capas**: Información repetida innecesariamente entre artefactos (ej. requerimientos vs casos de uso vs pantallas) sin propósito de refinamiento.
2. **Contradicciones Históricas**: Inconsistencias lógicas entre artefactos (versiones, IDs, roles, tecnologías) que surgen con el tiempo.
3. **Decisiones Arbitrarias (Falta de ADRs)**: Identificar decisiones arquitectónicas o de diseño clave que carecen de un Architecture Decision Record (ADR) formal que las respalde.
4. **Desincronización de Terminología**: Incoherencias en el uso de IDs, roles y términos a lo largo del ciclo de vida.

## Activación desde el Chat

El agente debe activar esta skill cuando el usuario solicite:
- "Haz un análisis en profundidad de los docs"
- "Ejecuta una auditoría completa del SDLC"
- "Audita todo el ciclo de vida"
- "Busca redundancias y contradicciones en todo el repo"

**Nota:** Se recomienda sugerir al usuario el uso del comando `/goal` para asegurar que el agente no se detenga antes de terminar de revisar todos los archivos necesarios.

## Workflow de Ejecución

### Paso 1 — Reconstruir el Orden Cronológico (SDLC)
Utiliza comandos como `git log` y la estructura de carpetas (nombres, prefijos lógicos) para determinar el orden de evolución de la documentación.

### Paso 2 — Escaneo Secuencial
Procede a leer los artefactos clave del repositorio, respetando el orden lógico del SDLC (por ejemplo: Requerimientos -> Modelos de Dominio/Casos de Uso -> Arquitectura -> UI/UX).

### Paso 3 — Ejecución Cruzada (Opcional)
Para apalancar herramientas existentes, puedes solicitar una ejecución de la skill de coherencia (`dteam-coherence-audit`) en modo global (`audit-all`) para levantar errores de referencias básicos y enfocarte en el análisis profundo.
```bash
uv run .agents/skills/dteam-coherence-audit/scripts/audit.py audit-all
```

### Paso 4 — Generación del Informe
Genera un informe detallado con los hallazgos.
- El informe **NO** debe guardarse en el repositorio de código de la documentación, sino en el repositorio de evidencias (`sena-evidence`), específicamente en la ruta:
  `/home/novillus/Documents/vscode/SENA-Career/sena-evidence/02-Planning/AP5-Prototyping/Deep-in/Audits/AUD-SDLC-DOCS-IN-DEPTH-ANALYSIS.md`
- Actualiza la versión del informe existente si ya hay uno.
- Estructura el informe con:
  - Hallazgos (con estado: `[RESUELTO]`, `[PENDIENTE: ADR]`, `[PENDIENTE: DECISIÓN]`, etc.)
  - Redundancias detectadas
  - Decisiones arbitrarias o falta de ADRs
  - Contradicciones lógicas
