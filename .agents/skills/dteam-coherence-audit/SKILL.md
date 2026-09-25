---
name: dteam-coherence-audit
description: >-
  Coherence auditor for the docs-as-code repository of the DTEAM project
  (EAM Digital Twin, Oil & Gas sector). Verifies that each new artifact
  principal does not break traceability, normative coherence, or the approved
  MVP scope. Use it when the user says "audit this artifact",
  "verify coherence of [file]", "check if this document is consistent"
  or similar. Also callable via CLI with `uv run audit.py audit --file <path>`.
---

# DTEAM Docs-as-Code — Coherence Auditor

## General Description

This skill executes three verification axes on a candidate artifact
before it is formally integrated into the `adso-dteam-docs` repository:

1. **Reference Traceability** — Validates that all cited IDs (UC-XXX,
   SCR-XXX, ADR-NNN, ASR-NNN, DT-UI-*) exist as actual files in the repo.
2. **Normative Coherence** — Verifies that colors, ISA-101 levels, RBAC roles
   and target client are consistent with the approved canonical artifacts.
3. **Scope Guard** — Detects if the artifact introduces screens, use cases,
   actors, or technologies that do not belong to the approved MVP index.

The skill **never modifies** the audited artifact. It only reports findings
with BLOCKER / WARNING / INFO severities and generates a Markdown report in
`../sena-evidence/00-Overview/Audits/Compliance/`.

---

## Chat Activation

The agent must activate this skill when detecting phrases like:
- "audit [file]"
- "verify the coherence of [document]"
- "does this artifact break anything?"
- "check consistency of [path]"
- "check coherence"
- "coherence audit"

---

## Workflow

### Step 1 — Identify the Candidate Artifact

Determine the absolute path of the artifact to audit:
- If the user explicitly mentions it, use it.
- If the user describes the artifact by name/code (e.g., "DT-UI-NAV-DOC-001"),
  search for it with `find . -name "*NAV-DOC-001*"` from the repository root.

The repository root is always:
`/home/novillus/Documents/vscode/SENA-Career/adso-dteam-docs`

### Step 2 — Execute the Helper Script

From the repository root, execute:

```bash
cd /home/novillus/Documents/vscode/SENA-Career/adso-dteam-docs
uv run .agents/skills/dteam-coherence-audit/scripts/audit.py audit --file <ruta-relativa>
```

The script automatically generates the report in `../sena-evidence/00-Overview/Audits/Compliance/`.

### Step 3 — Present Results to the User

Read the generated report and present it in a structured way:
1. Show the overall verdict (✅ APPROVED / ⚠️ CONDITIONAL / 🔴 BLOCKED).
2. List all BLOCKER findings first, WARNING next, INFO last.
3. For each BLOCKER, explain the specific impact on the DTEAM project.
4. Ask the user how they wish to proceed with the findings.

### Step 4 — Full Repository Audit Mode (Optional)

If the user asks to "audit the whole repository" or "CI mode":

```bash
cd /home/novillus/Documents/vscode/SENA-Career/adso-dteam-docs
uv run .agents/skills/dteam-coherence-audit/scripts/audit.py audit-all \
  --output ../sena-evidence/00-Overview/Audits/AUD-FULL-REPO.md
```

---

## Available Subcommands

| Subcommand | Purpose |
| :--- | :--- |
| `audit --file <path>` | Full audit of an artifact + Markdown report |
| `check-refs --file <path>` | Only reference traceability (fast) |
| `check-scope --file <path>` | Only scope guard verification |
| `audit-all --output <path>` | Scans all artifacts in the repository |

---

## Exit Code Interpretation

| Exit Code | Meaning |
| :--- | :--- |
| `0` | No findings or only WARNING/INFO — artifact approved with observations |
| `1` | Execution error (file not found, outside the repo) |
| `2` | BLOCKER found — the artifact MUST NOT be integrated without correction |

---

## Common Errors

- **"File not found"**: Verify that the path is relative to the repo root.
- **"Not a git repository"**: The script must be executed from within `adso-dteam-docs/`.
- **"ID not in MVP index"**: The referenced ID may be legitimate but the script's index requires manual update — consult the architect before modifying it.
