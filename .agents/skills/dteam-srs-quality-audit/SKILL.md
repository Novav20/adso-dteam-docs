---
name: dteam-srs-quality-audit
description: >-
  Quality and DDD (Domain-Driven Design) auditor for the master database 
  of requirements (srs.csv) of the DTEAM project. Verifies the rigorousness of 
  the normative references (ISO, NIST), the correct use of ISO 25010:2023, and 
  the absence of legacy or generic terms (like "activo" instead of 
  "Equipment Unit"). Use it when the user says "audit the requirements", 
  "review the srs.csv dataset" or "verify the quality of the requirements".
---

# DTEAM Docs-as-Code — SRS Quality Auditor

## General Description

This skill executes a programmatic analysis directly over the file 
`requirements/data/srs.csv` to guarantee that the requirements engineering 
is maintained at the highest standard required by the DTEAM project.

It evaluates three fundamental axes:
1. **ISO 25010:2023:** Guarantees that deprecated categories are not used 
   (like *Usability* or *Portability*) in favor of current ones (*Interaction Capability*, *Flexibility*, etc.).
2. **Domain-Driven Design (DDD):** Scans the descriptions looking for 
   forbidden generic terms (e.g. "activo" / "asset") to force the use of the 
   Ubiquitous Language (e.g. "Equipment Unit" / "Maintainable Item" per ISO 14224).
3. **Normative References:** Validates with regular expressions that the column 
   `Normative Reference` cites actionable standards (ISO, NIST, OWASP, ACID, etc.) 
   instead of generic text (like "UX Best Practices").

## Chat Activation

The agent must activate this skill when detecting:
- "Audit the srs.csv dataset"
- "Review the quality of the requirements"
- "Verify if we use the domain language correctly in the CSV"
- "Check SRS quality"

## Workflow

### Step 1 — Execute the Audit Script

From the repository root, execute the Python script that will analyze the CSV:

```bash
cd /home/novillus/Documents/vscode/SENA-Career/adso-dteam-docs
uv run .agents/skills/dteam-srs-quality-audit/scripts/srs_audit.py
```

### Step 2 — Present Results

The script will return a summary with BLOCKER, WARNING and INFO severities.
1. Show the user the verdict.
2. If there are **BLOCKERS** (e.g. invalid ISO categories or missing references in TRs), 
   report that the CSV must be corrected before being able to regenerate the User Stories.
3. If there are **WARNINGS** (domain language violations or weak references), 
   list them and ask the user if they want to correct them.

### Step 3 — Interpret Exit Codes

| Exit Code | Meaning |
| :--- | :--- |
| `0` | Approved (may contain Warnings/Infos but does not break the system) |
| `1` | Catastrophic error (CSV not found or missing key columns) |
| `2` | BLOCKER found — Invalid categories or broken architectural rules |
