---
name: dteam-sdlc-deep-audit
description: >-
  In-depth auditor for the DTEAM project's docs-as-code repository.
  Performs a holistic and chronological analysis of the artifacts (SDLC) to detect
  cross-layer redundancies, logical contradictions over time,
  and architectural decisions without a justifying ADR.
  Use it when a complete, deep audit or an end-of-milestone review is requested.
---

# DTEAM Docs-as-Code — Lifecycle Auditor (SDLC Deep Audit)

## General Description

This skill executes an exhaustive and historical analysis of the documentation state in the `adso-dteam-docs` repository. Unlike `dteam-coherence-audit` (which evaluates a single artifact when added), this skill evaluates **the entire repository** by reading the artifacts in the order they are supposed to have been created according to the SDLC (Software Development Life Cycle).

Its purpose is to identify:
1. **Inter-layer Redundancies**: Unnecessarily repeated information between artifacts (e.g., requirements vs use cases vs screens) without refinement purpose.
2. **Historical Contradictions**: Logical inconsistencies between artifacts (versions, IDs, roles, technologies) that arise over time.
3. **Arbitrary Decisions (Lack of ADRs)**: Identify key architectural or design decisions that lack a formal Architecture Decision Record (ADR) backing them.
4. **Terminology Desynchronization**: Incoherencies in the use of IDs, roles, and terms throughout the lifecycle.

## Chat Activation

The agent must activate this skill when the user requests:
- "Do an in-depth analysis of the docs"
- "Execute a full SDLC audit"
- "Audit the entire lifecycle"
- "Search for redundancies and contradictions across the whole repo"

**Note:** It is recommended to suggest the user to use the `/goal` command to ensure the agent does not stop before finishing reviewing all necessary files.

## Execution Workflow

### Step 1 — Reconstruct the Chronological Order (SDLC)
Use commands like `git log` and the folder structure (names, logical prefixes) to determine the evolution order of the documentation.

### Step 2 — Sequential Scanning
Proceed to read the key artifacts of the repository, respecting the logical order of the SDLC (e.g., Requirements -> Domain Models/Use Cases -> Architecture -> UI/UX).

### Step 3 — Cross-Execution (Optional)
To leverage existing tools, you can request an execution of the coherence skill (`dteam-coherence-audit`) in global mode (`audit-all`) to raise basic reference errors and focus on the deep analysis.
```bash
uv run .agents/skills/dteam-coherence-audit/scripts/audit.py audit-all
```

### Step 4 — Report Generation
Generate a detailed report with the findings.
- The report **MUST NOT** be saved in the documentation code repository, but in the evidence repository (`sena-evidence`), specifically at the path:
  `/home/novillus/Documents/vscode/SENA-Career/sena-evidence/02-Planning/AP5-Prototyping/Deep-in/Audits/AUD-SDLC-DOCS-IN-DEPTH-ANALYSIS.md`
- Update the existing report version if one already exists.
- Structure the report with:
  - Findings (with status: `[RESOLVED]`, `[PENDING: ADR]`, `[PENDING: DECISION]`, etc.)
  - Detected redundancies
  - Arbitrary decisions or lack of ADRs
  - Logical contradictions
