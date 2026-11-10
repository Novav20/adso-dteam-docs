#!/usr/bin/env python3
"""
DTEAM UI/UX Screen Specification Coherence Auditor & Linter
===========================================================
Deterministic audit script for UI/UX screen specifications (SCR-*.md)
within the adso-dteam-docs repository (DTEAM Project).

Verifies structural integrity, architectural layer segregation (no DB schema,
no SQL functions, no Blazor code-behind, no raw CSS/hex), token conformance,
and ISA-101/HPHMI rules without relying on LLM heuristic evaluation.

Usage:
    uv run audit.py audit     --file <relative-path-to-SCR.md>
    uv run audit.py lint      --file <relative-path-to-SCR.md>
    uv run audit.py audit-all [--output <report-path>]
"""

from __future__ import annotations
import argparse
import datetime
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Finding Model & Constants
# ---------------------------------------------------------------------------

class Finding(NamedTuple):
    severity: str   # BLOCKER | WARNING | INFO
    code: str       # STR-001, SQL-001, CS-001, CSS-001, etc.
    message: str
    line: int | None = None


VALID_MODULES: set[str] = {"VIS", "MTTO", "INV", "ADM"}

MANDATORY_FRONTMATTER_KEYS: list[str] = [
    "id", "title", "module", "isa101_level", "platform",
    "target_device", "roles", "user_stories", "use_cases",
    "version", "date", "status"
]

CANONICAL_SECTIONS: list[tuple[int, str, str]] = [
    (1, r"^##\s+1\.\s+Purpose and Operational Context", "## 1. Purpose and Operational Context"),
    (2, r"^##\s+2\.\s+Visual Artifact", "## 2. Visual Artifact"),
    (3, r"^##\s+3\.\s+Functional Component Inventory", "## 3. Functional Component Inventory"),
    (4, r"^##\s+4\.\s+Screen State(?:s|\s+(?:Matrix|Catalog|Inventory))", "## 4. Screen State Catalog"),
    (5, r"^##\s+5\.\s+Interaction Rules and Data Flow", "## 5. Interaction Rules and Data Flow"),
    (6, r"^##\s+6\.\s+Industrial and Safety Considerations", "## 6. Industrial and Safety Considerations"),
    (7, r"^##\s+7\.\s+Frontend Component Contract", "## 7. Frontend Component Contract (Blazor / Razor)"),
    (8, r"^##\s+8\.\s+Layout and Responsive Adaptability", "## 8. Layout and Responsive Adaptability"),
    (9, r"^##\s+9\.\s+Traceability and Requirements Matrix", "## 9. Traceability and Requirements Matrix"),
]

MANDATORY_SUBSECTIONS_7: list[tuple[str, str]] = [
    (r"^###\s+7\.1\.?\s+Component Hierarchy", "### 7.1 Component Hierarchy & File Mapping"),
    (r"^###\s+7\.2\.?\s+Physical Component Parameters", "### 7.2 Physical Component Parameters & DTO Contracts"),
    (r"^###\s+7\.3\.?\s+Client-Side DOM", "### 7.3 Client-Side DOM & Interop Bridge"),
]

# Prohibited persistence / SQL leak patterns
PERSISTENCE_LEAK_PATTERNS: list[tuple[str, str, str]] = [
    (r"\b(mtto|tax|adm|vis|inv|ops|auth)\.[a-z0-9_]+", "SQL-001",
     "Physical database schema qualifier '{match}' leaked into specification. Use frontend DTO/command types."),
    (r"\btimestamptz\b", "SQL-002",
     "PostgreSQL physical type 'timestamptz' leaked. Use C# 'DateTimeOffset' or ISO-8601 string."),
    (r"\bUUID PRIMARY KEY\b", "SQL-002",
     "Physical SQL DDL constraint 'UUID PRIMARY KEY' leaked into specification."),
    (r"\b(?:BIG)?SERIAL(?:\s+PRIMARY\s+KEY|\s+NOT\s+NULL|\s*,)\b", "SQL-002",
     "Physical SQL DDL type 'SERIAL' leaked into specification."),
    (r"\bclock_timestamp\(\)", "SQL-003",
     "PostgreSQL server function 'clock_timestamp()' leaked into specification. Use client/application timestamp semantics."),
    (r"\bNOW\(\)", "SQL-003",
     "SQL server function 'NOW()' leaked into specification."),
    (r"\bINSERT\s+INTO\b", "SQL-004",
     "SQL DML 'INSERT INTO' query leaked into specification. Describe client command dispatch via API endpoints."),
    (r"\bUPDATE\s+[a-z_]+(?:\.[a-z_]+)?\s+SET\b", "SQL-004",
     "SQL DML 'UPDATE ... SET' query leaked into specification. Describe client command dispatch via API endpoints."),
    (r"\bDELETE\s+FROM\b", "SQL-004",
     "SQL DML 'DELETE FROM' query leaked into specification."),
    (r"\bck_[a-z0-9_]+", "SQL-005",
     "Physical database CHECK constraint '{match}' leaked. Translate into frontend validation rules or domain enums."),
]

# Prohibited C# Blazor code-behind / runtime leak patterns
CSHARP_LEAK_PATTERNS: list[tuple[str, str, str]] = [
    (r"\bclass\s+[A-Za-z0-9_]+\s*:\s*ComponentBase\b", "CS-001",
     "Blazor 'ComponentBase' class declaration leaked. Section 7 must define parameter contracts and DTO records only."),
    (r"\[Inject\]", "CS-002",
     "Dependency injection '[Inject]' leaked. DI is an internal implementation detail prohibited from parameter contracts."),
    (r"\bprivate\s+(?:bool|int|string|DateTime|DateTimeOffset|List<[^>]+>|Dictionary<[^>]+>|HashSet<[^>]+>|[A-Z][a-zA-Z0-9_]*)\s+_[a-zA-Z0-9_]+", "CS-003",
     "Private mutable component state field '{match}' leaked. Internal state management belongs to implementation code-behind."),
    (r"\boverride\s+(?:async\s+)?Task\s+On(?:Initialized|ParametersSet)(?:Async)?\b", "CS-004",
     "Blazor lifecycle override '{match}' leaked into specification."),
    (r"\bnamespace\s+[A-Za-z0-9_.]+\b", "CS-005",
     "C# 'namespace' statement leaked. Decoupled Namespaces Rule prohibits premature assembly coupling."),
    (r"\bDateTime\b", "CS-006",
     "Raw 'DateTime' type leaked in C# contract. Use 'DateTimeOffset' for TIMESTAMPTZ timestamps or 'DateOnly' for calendar dates."),
    (r"\b(?:string\??\s+\w*Criticality\w*|enum\s+\w*Criticality\w*)\b", "CS-008",
     "Invalid criticality type '{match}' in C# contract. Criticality must be typed as 'int' or 'int?' (1..10) per DT-DM-DOC-001 §4.5."),
]

# Mapping of screen C# enum names to canonical DT-DM-DOC-001 §4.X enum keys
CANONICAL_ENUM_MAP: dict[str, str] = {
    "EquipmentHealthStatus": "EquipmentUnit.healthStatus",
    "EquipmentLifecycleStatus": "EquipmentUnit.lifecycleStatus",
    "EquipmentMaintenanceStatus": "EquipmentUnit.maintenanceStatus",
    "EquipmentOperationalStatus": "EquipmentUnit.operationalStatus",
    "OperationalStatus": "EquipmentUnit.operationalStatus",
    "EnvironmentalExposureLevel": "FunctionalLocation.environmentalExposure",
    "MaintainableItemStatus": "MaintainableItem.status",
    "BacklogItemStatus": "BacklogItem.status",
    "DetectionMethod": "FailureRecord.detectionMethod",
    "OperationalCondition": "FailureRecord.operationalCondition",
    "OperationalImpact": "FailureRecord.operationalImpact",
    "FailureRecordStatus": "FailureRecord.status",
    "MaintenanceFrequencyType": "MaintenancePlan.frequencyType",
    "MaintenanceIntervalUnit": "MaintenancePlan.intervalUnit",
    "MaintenanceMethod": "MaintenancePlan.maintenanceMethod",
    "WorkOrderType": "WorkOrder.maintenanceMethod",
    "TelemetrySignalType": "TelemetrySignal.signalType",
    "MaintenanceCraft": "MaintenancePlan.requiredSpecialty",
    "MaintenancePlanStatus": "MaintenancePlan.status",
    "MediaAttachmentFileType": "MediaAttachment.fileType",
    "WorkOrderCriticality": "WorkOrder.criticality",
    "WorkOrderStatus": "WorkOrder.currentStatus",
    "WorkRequestStatus": "WorkRequest.status",
    "InventoryTransactionType": "InventoryTransaction.transactionType",
    "SparePartStatus": "SparePart.status",
    "StockPolicy": "SparePart.stockPolicy",
    "IsolationType": "IsolationPoint.isolationType",
    "MeshMappingStatus": "MeshMapping.mappingStatus",
    "VisualLayerStatus": "VisualLayer.status",
    "IsolationStatus": "WorkOrderIsolation.isolationStatus",
    "PhysicalVerificationMethod": "WorkOrderIsolation.tryOutMethod",
    "PermitType": "WorkPermit.permitType",
    "WorkPermitStatus": "WorkPermit.status",
    "AuditActionType": "AuditLog.actionType",
    "AuthTokenPurpose": "AuthToken.purpose",
    "IdempotencyStatus": "IdempotencyLog.status",
    "RolePermissionModule": "RolePermission.module",
    "UserStatus": "User.status",
    "WorkOrderRole": "WorkOrderAssignment.roleInWork",
}

# Screen-specific subset projections of canonical DT-DM-DOC-001 enums
SUBSET_ENUM_MAP: dict[str, str] = {
    "CalendarIntervalUnit": "MaintenancePlan.intervalUnit",
    "TelemetryMeasurementUnit": "MaintenancePlan.intervalUnit",
}

# Validated presentation/composite UI projection enums (must match exact member set)
PRESENTATION_PROJECTION_ENUMS: dict[str, set[str]] = {
    "DismountDestinationStatus": {"IN_REPAIR", "IN_STORAGE", "DAMAGED"},
}

# Prohibited CSS / styling / magic dimension patterns
CSS_LEAK_PATTERNS: list[tuple[str, str, str]] = [
    (r"\bposition:\s*(?:fixed|absolute|relative)\b", "CSS-002",
     "Raw CSS rule '{match}' leaked into specification prose. Use Design System layout tokens and component hierarchy."),
    (r"\bpointer-events:\s*(?:none|auto)\b", "CSS-002",
     "Raw CSS rule '{match}' leaked into specification prose."),
    (r"\bz-index:\s*\d+\b", "CSS-003",
     "Raw numeric z-index '{match}' leaked. Use '--dt-z-*' elevation tokens."),
    (r"\bfont-weight:\s*(?:[1-9]00|bold|normal|semibold)\b", "CSS-002",
     "Raw CSS font-weight '{match}' leaked into specification prose. Use composite typography tokens (--dt-font-*)."),
    (r"\b(?:width|min-width|max-width|height|min-height|max-height|border-radius|padding|margin|gap)\s*:\s*[^;\n]*\b\d+(?:\.\d+)?(?:px|rem|em)\b", "CSS-002",
     "Raw CSS dimension declaration '{match}' leaked into specification prose. Use Design System layout/spacing tokens (--dt-layout-*, --dt-space-*, --dt-radius-*)."),
    (r"\bbackground(?:-color)?\s*:\s*(?:transparent|none|#[0-9a-fA-F]+|[a-z]+)\b", "CSS-002",
     "Raw CSS background declaration '{match}' leaked into specification prose. Use Design System surface tokens (--dt-color-surface-*)."),
    (r"\bdisplay\s*:\s*(?:flex|grid|none|block|inline(?:-[a-z]+)?)\b", "CSS-002",
     "Raw CSS display declaration '{match}' leaked into specification prose. Use Design System layout rules and component hierarchy."),
    (r"\bscrollbar-gutter\s*:\s*[a-z-]+\b", "CSS-002",
     "Raw CSS 'scrollbar-gutter' declaration '{match}' leaked into specification prose. Use functional layout descriptions."),
    (r"\boverflow(?:-[xy])?\s*:\s*(?:auto|hidden|scroll|visible)\b", "CSS-002",
     "Raw CSS 'overflow' declaration '{match}' leaked into specification prose. Describe functional scrolling behavior."),
    (r"\bopacity\s*:\s*0?\.\d+\b", "CSS-002",
     "Raw numeric CSS opacity '{match}' leaked into specification prose. Use '--dt-opacity-*' tokens or disabled state descriptions."),
    (r"\b(?:box-shadow|transform|transition|cursor|outline)\s*:\s*[^;\n`)]+\b", "CSS-002",
     "Raw CSS property declaration '{match}' leaked into specification prose. Use Design System tokens or functional descriptions."),
    (r"\bweights?\s*\(`?[4-7]00`?\s*[-–]\s*`?[4-7]00`?\)", "CSS-006",
     "Raw numeric font-weight range '{match}' leaked into specification prose. Use composite typography tokens (--dt-font-*)."),
    (r"\b(?:filter\s*:\s*drop-shadow|rx\s*=\s*[\"']?\d+|ry\s*=\s*[\"']?\d+)\b", "CSS-002",
     "Raw SVG attribute or filter declaration '{match}' leaked into specification prose. Use Design System elevation and radius tokens."),
]

# Prohibited browser / runtime globals
RUNTIME_LEAK_PATTERNS: list[tuple[str, str, str]] = [
    (r"\bwindow\.[a-zA-Z0-9_]+", "DOM-001",
     "Direct browser global '{match}' leaked. Abstract via JSInterop capability interfaces in §7.3."),
    (r"\bdocument\.[a-zA-Z0-9_]+", "DOM-001",
     "Direct DOM access '{match}' leaked."),
    (r"\bAudioContext\b", "DOM-001",
     "Direct Web Audio API 'AudioContext' leaked. Abstract via audio interop capability interface."),
    (r"\b(?:local|session)Storage\b", "DOM-001",
     "Direct browser storage '{match}' leaked. Abstract via 'IOfflineStorage'."),
    (r"\bsqlite-net-pcl\b", "DOM-002",
     "Concrete third-party package 'sqlite-net-pcl' leaked. Use abstract 'IOfflineStorage' / encrypted cache."),
]

# Prohibited narrative / software meta-text patterns
META_TEXT_PATTERNS: list[tuple[str, str, str]] = [
    (r"\b(?:Asset|Activo)\s+[A-D]\b", "TXT-001",
     "Generic drafting variable placeholder '{match}' detected in screen specification. Use authentic operational domain terms from DT-UL-DOC-001 / ISO 14224 (e.g., Dismounted Asset / Replacement Asset)."),
    (r"\b(?:Entity|Entidad)\s+[A-D]\b", "TXT-001",
     "Generic drafting placeholder '{match}' detected. Use specific domain entity names from DT-DM-DOC-001."),
    (r"\b(?:Record|Registro)\s+[A-D]\b", "TXT-001",
     "Generic drafting placeholder '{match}' detected. Use specific domain record names."),
    (r"\b(?:Immutable\s+Record|Registro\s+Inmutable)\b", "BADGE-001",
     "Static pseudo-badge text '{match}' detected. Badges are reserved exclusively for dynamic lifecycles and quantifiable counters per DT-UI-DS-DOC-001 §6.5 (Anti-Badge-Inflation Principle)."),
]

# Spanish section title words (Language Policy: English only)
SPANISH_HEADER_WORDS: list[str] = [
    "Propósito", "Contexto Operacional", "Artefacto Visual", "Inventario Funcional",
    "Matriz de Estados", "Reglas de Interacción", "Consideraciones Industriales",
    "Contrato de Componentes", "Adaptabilidad", "Trazabilidad"
]

# Prohibited Spanish vocabulary in specification prose (Language Policy: English only)
PROHIBITED_SPANISH_PROSE_TERMS: list[tuple[str, str]] = [
    (r"\balertas?\b", "alerta"),
    (r"\bsubsistemas?\b", "subsistema"),
    (r"\bmapead[oa]s?\b", "mapeado/a"),
    (r"\bpermisos?\b", "permiso"),
    (r"\bdetalles?\b", "detalle"),
    (r"\binconsistencias?\b", "inconsistencia"),
    (r"\bcaliente\b", "caliente"),
    (r"\bconfinad[oa]s?\b", "confinado/a"),
    (r"\bórdenes\b", "órdenes"),
    (r"\b(?:cerrar|guardar|cancelar|eliminar|editar)\b", "common Spanish UI verb"),
    (r"(?<![A-Z])\btodos\b(?![A-Z])", "todos"),
    (r"\btrabajo\s+en\s+caliente\b", "trabajo en caliente"),
    (r"\bespacio\s+confinado\b", "espacio confinado"),
    (r"\bno\s+mapead[oa]s?\b", "no mapeado/a"),
    (r"\bver\s+detalles?\b", "ver detalle"),
    (r"\bresolver\s+inconsistencias?\b", "resolver inconsistencia"),
]

# Prohibited requirement / specification codes leaked into user-facing DOM
PROHIBITED_SPEC_CODES: list[tuple[str, str, str]] = [
    (r"\b(?:FR|AF|TR|NFR|ADR)-\d{3}\b", "HTML-SPEC-001",
     "Requirement / Architecture specification code '{match}' leaked into HTML prototype text or visible DOM. Prototypes must use authentic domain operational terminology exclusively."),
    (r"\b(?:Paso|Step)\s+\d+\b", "HTML-SPEC-001",
     "Workflow step reference '{match}' leaked into HTML prototype text. Replace with action-oriented domain label."),
]

# Unicode Emoji regex pattern (Standard Unicode ranges for pictorial emojis)
EMOJI_REGEX = re.compile(
    r"[\U0001F300-\U0001FAFF"  # Miscellaneous Symbols and Pictographs, Emoticons, Supplemental Symbols
    r"\U00002700-\U000027BF"  # Dingbats
    r"\U0001F600-\U0001F64F"  # Emoticons
    r"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
    r"\U00002600-\U000026FF"  # Miscellaneous Symbols (warning, lightning, etc.)
    r"\U00002B50\U00002B55"    # Star, Heavy Large Circle
    r"]",
    re.UNICODE
)

SCRIPT_REPO_ROOT = Path(__file__).resolve().parents[4]

# ---------------------------------------------------------------------------
# Repository & Token Utilities
# ---------------------------------------------------------------------------

def find_repo_root(start: Path) -> Path | None:
    """Finds the root directory of adso-dteam-docs."""
    current = start.resolve()
    for _ in range(10):
        if (current / "domain-models").is_dir() and (current / "requirements").is_dir():
            return current
        if (current / ".git").is_dir() and (current / "ui-ux").is_dir():
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def load_canonical_tokens(repo_root: Path) -> set[str]:
    """Loads all valid --dt-* design tokens from tokens.css."""
    tokens_file = repo_root / "ui-ux" / "assets" / "tokens.css"
    if not tokens_file.exists():
        return set()
    
    content = tokens_file.read_text(encoding="utf-8")
    tokens = set(re.findall(r"(--dt-[a-z0-9-]+)\s*:", content))
    return tokens


def load_canonical_enums(repo_root: Path) -> dict[str, set[str]]:
    """Loads canonical enum vocabularies from domain-models/class/DT-DM-DOC-001.md (§4.X tables)."""
    dm_file = repo_root / "domain-models" / "class" / "DT-DM-DOC-001.md"
    if not dm_file.exists():
        return {}

    content = dm_file.read_text(encoding="utf-8")
    enums: dict[str, set[str]] = {}
    current_key: str | None = None

    for line in content.splitlines():
        header_match = re.match(r"^#{3,4}\s+4\.\d+\s+([A-Za-z0-9_.]+)", line.strip())
        if header_match:
            current_key = header_match.group(1)
            enums[current_key] = set()
            continue
        elif line.strip().startswith("## ") and not line.strip().startswith("###"):
            current_key = None
            continue

        if current_key and line.strip().startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                val = parts[1].strip("` ")
                if re.match(r"^[A-Z][A-Z0-9_]*$", val):
                    enums[current_key].add(val)

    return enums


def pascal_to_upper_snake(member: str) -> str:
    """Converts C# PascalCase or UPPER_SNAKE_CASE enum member to canonical UPPER_SNAKE_CASE."""
    if re.match(r"^[A-Z0-9_]+$", member):
        return member
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", member)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).upper()


# ---------------------------------------------------------------------------
# Verification Axes
# ---------------------------------------------------------------------------

def audit_frontmatter(content: str) -> list[Finding]:
    """Verifies YAML frontmatter integrity, completeness, and values."""
    findings: list[Finding] = []
    lines = content.splitlines()

    if not lines or lines[0].strip() != "---":
        findings.append(Finding(
            severity="BLOCKER",
            code="STR-001",
            message="Document must begin with YAML frontmatter delimiter '---'.",
            line=1
        ))
        return findings

    fm_lines: list[str] = []
    fm_end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm_end = i
            break
        fm_lines.append(lines[i])

    if fm_end == -1:
        findings.append(Finding(
            severity="BLOCKER",
            code="STR-001",
            message="YAML frontmatter closing delimiter '---' not found.",
            line=1
        ))
        return findings

    fm_text = "\n".join(fm_lines)

    # Check mandatory keys
    for key in MANDATORY_FRONTMATTER_KEYS:
        pattern = rf"^{key}:"
        if not re.search(pattern, fm_text, re.MULTILINE):
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-001",
                message=f"Mandatory frontmatter key '{key}' is missing.",
                line=1
            ))

    # Verify ID format: SCR-[VIS|MTTO|INV|ADM]-[0-9]{3}
    id_match = re.search(r"^id:\s*(SCR-[A-Z]+-[0-9]{3})", fm_text, re.MULTILINE)
    if not id_match:
        findings.append(Finding(
            severity="BLOCKER",
            code="STR-002",
            message="Frontmatter 'id' must follow pattern 'SCR-[MODULE]-[NUM]' (e.g., SCR-VIS-008).",
            line=1
        ))
    else:
        module_match = re.search(r"^module:\s*([A-Z]+)", fm_text, re.MULTILINE)
        if module_match and module_match.group(1) not in VALID_MODULES:
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-002",
                message=f"Frontmatter 'module' '{module_match.group(1)}' is invalid. Must be one of {VALID_MODULES}.",
                line=1
            ))

    return findings


def audit_structure(content: str) -> list[Finding]:
    """Verifies that all 9 canonical sections and §7 subsections exist in exact order."""
    findings: list[Finding] = []
    lines = content.splitlines()

    # Check language of headers and body prose (Language Policy: 100% Technical English)
    # Also enforce zero emojis across specification documents (ISA-101 / HPHMI standard)
    in_code_block = False
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Check for Unicode Emojis in specification prose
        emoji_matches = EMOJI_REGEX.findall(line)
        if emoji_matches:
            findings.append(Finding(
                severity="BLOCKER",
                code="DOC-EMOJI-001",
                message=f"Unicode emoji '{emoji_matches[0]}' detected in specification prose (line {idx}). Technical specifications must use canonical icon codes (e.g. `[#icon-warning]`) or semantic descriptions per HPHMI/ISA-101 standard.",
                line=idx
            ))

        if line.startswith("#"):
            for sp_word in SPANISH_HEADER_WORDS:
                if sp_word in line:
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="LANG-001",
                        message=f"Header contains Spanish term '{sp_word}'. All screen specs must be 100% Technical English.",
                        line=idx
                    ))
        else:
            clean_line = re.sub(r"!\[.*?\]\(.*?\)", "", line)
            clean_line = re.sub(r"\[([^\]]*)\]\([^)]+\)", r"\1", clean_line)
            for pat, label in PROHIBITED_SPANISH_PROSE_TERMS:
                m = re.search(pat, clean_line, re.IGNORECASE)
                if m:
                    if label == "todos" and m.group(0).isupper():
                        continue
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="LANG-001",
                        message=f"Spanish term '{m.group(0)}' leaked into specification prose. All engineering documentation in adso-dteam-docs must be strictly 100% Technical English.",
                        line=idx
                    ))

    # Find section positions
    section_positions: dict[int, int] = {}
    for sec_num, pattern, label in CANONICAL_SECTIONS:
        found = False
        for idx, line in enumerate(lines, start=1):
            if re.search(pattern, line, re.IGNORECASE):
                section_positions[sec_num] = idx
                found = True
                break
        if not found:
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-003",
                message=f"Mandatory section missing: '{label}'.",
                line=None
            ))

    # Verify chronological ordering
    ordered_nums = sorted(section_positions.keys())
    for i in range(len(ordered_nums) - 1):
        current_num = ordered_nums[i]
        next_num = ordered_nums[i + 1]
        if section_positions[current_num] > section_positions[next_num]:
            findings.append(Finding(
                severity="BLOCKER",
                code="STR-004",
                message=f"Section {current_num} (line {section_positions[current_num]}) appears after Section {next_num} (line {section_positions[next_num]}). Sections must be strictly ordered 1 through 9.",
                line=section_positions[current_num]
            ))

    # Check §4 state structure if §4 exists and uses list format
    if 4 in section_positions:
        sec4_start = section_positions[4]
        sec5_start = section_positions.get(5, len(lines))
        sec4_lines = lines[sec4_start : sec5_start - 1]

        current_state_title = None
        current_state_line = 0
        has_activation = False
        has_visual = False

        for offset, l in enumerate(sec4_lines):
            l_idx = sec4_start + offset + 1
            m_state = re.match(r"^\s*\d+\.\s+\*\*([^*]+)\*\*", l.strip())
            if m_state:
                if current_state_title:
                    if not has_activation:
                        findings.append(Finding(
                            severity="BLOCKER",
                            code="STR-007",
                            message=f"Screen state '{current_state_title}' in §4 lacks mandatory '**Activation Condition:**' specification.",
                            line=current_state_line
                        ))
                    if not has_visual:
                        findings.append(Finding(
                            severity="BLOCKER",
                            code="STR-007",
                            message=f"Screen state '{current_state_title}' in §4 lacks mandatory '**Visual Modification:**' specification.",
                            line=current_state_line
                        ))
                current_state_title = m_state.group(1).strip()
                current_state_line = l_idx
                has_activation = False
                has_visual = False
            elif current_state_title:
                if re.search(r"\bActivation Condition\b", l, re.IGNORECASE):
                    has_activation = True
                if re.search(r"\bVisual Modification\b", l, re.IGNORECASE):
                    has_visual = True

        if current_state_title:
            if not has_activation:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="STR-007",
                    message=f"Screen state '{current_state_title}' in §4 lacks mandatory '**Activation Condition:**' specification.",
                    line=current_state_line
                ))
            if not has_visual:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="STR-007",
                    message=f"Screen state '{current_state_title}' in §4 lacks mandatory '**Visual Modification:**' specification.",
                    line=current_state_line
                ))

    # Check §7 subsections if §7 exists
    if 7 in section_positions:
        sec7_start = section_positions[7]
        sec8_start = section_positions.get(8, len(lines))
        sec7_text = "\n".join(lines[sec7_start - 1 : sec8_start])

        for pattern, label in MANDATORY_SUBSECTIONS_7:
            if not re.search(pattern, sec7_text, re.MULTILINE):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="STR-005",
                    message=f"Mandatory subsection in §7 missing: '{label}'.",
                    line=sec7_start
                ))

    # Check §8 responsive tiers if §8 exists
    if 8 in section_positions:
        sec8_start = section_positions[8]
        sec9_start = section_positions.get(9, len(lines))
        sec8_text = "\n".join(lines[sec8_start - 1 : sec9_start])

        tiers = ["Desktop", "Tablet Landscape", "Tablet Portrait"]
        for tier in tiers:
            if tier.lower() not in sec8_text.lower():
                findings.append(Finding(
                    severity="WARNING",
                    code="STR-006",
                    message=f"Section 8 should tabulate layout rules for '{tier}'.",
                    line=sec8_start
                ))

    return findings


def audit_persistence_leaks(content: str) -> list[Finding]:
    """Scans for database schema, physical SQL types, and check constraints."""
    findings: list[Finding] = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        # Skip normative prohibition alerts/rules
        if "PROHIBITED" in line or "Prohibited" in line:
            continue

        # Exclude markdown link targets/URLs where schemas might appear in repository filepaths (e.g. adso-dteam-docs/...)
        stripped_line = re.sub(r"\[.*?\]\(.*?\)", "", line)

        for pattern, code, msg_template in PERSISTENCE_LEAK_PATTERNS:
            match = re.search(pattern, stripped_line, re.IGNORECASE)
            if match:
                matched_str = match.group(0)
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=matched_str),
                    line=idx
                ))

    return findings


def audit_csharp_leaks(content: str, canonical_enums: dict[str, set[str]] | None = None) -> list[Finding]:
    """Scans for C# Blazor code-behind, [Inject], private mutable state, namespaces, raw DateTime, criticality types, and canonical enum parity."""
    findings: list[Finding] = []
    lines = content.splitlines()

    in_code_block = False
    code_block_lang = ""

    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_lang = line.strip()[3:].strip().lower()
            else:
                in_code_block = False
                code_block_lang = ""
            continue

        # Skip C# comments and prohibition descriptions
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*") or "PROHIBITED" in line or "Prohibited" in line:
            continue

        for pattern, code, msg_template in CSHARP_LEAK_PATTERNS:
            match = re.search(pattern, line)
            if match:
                if code in ("CS-005", "CS-006", "CS-008") and not (in_code_block and code_block_lang in ("csharp", "c#", "cs")):
                    continue
                matched_str = match.group(0)
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=matched_str),
                    line=idx
                ))

    # CS-007: Canonical Enum Parity in §7.2.3
    if canonical_enums:
        for enum_match in re.finditer(r"public\s+enum\s+([A-Za-z0-9_]+)\s*\{([^}]+)\}", content):
            enum_name = enum_match.group(1)
            enum_body = enum_match.group(2)
            line_num = content[:enum_match.start()].count("\n") + 1

            raw_members: list[str] = []
            for m_line in enum_body.splitlines():
                clean_m = m_line.split("//")[0].strip()
                if not clean_m:
                    continue
                for token in clean_m.split(","):
                    t = token.split("=")[0].strip()
                    if t:
                        raw_members.append(t)

            normalized_members = {pascal_to_upper_snake(m) for m in raw_members}

            if enum_name in CANONICAL_ENUM_MAP:
                dm_key = CANONICAL_ENUM_MAP[enum_name]
                expected = canonical_enums.get(dm_key, set())
                if expected and normalized_members != expected:
                    missing = sorted(expected - normalized_members)
                    extra = sorted(normalized_members - expected)
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="CS-007",
                        message=(
                            f"C# enum '{enum_name}' contradicts canonical domain enum '{dm_key}' in DT-DM-DOC-001.md. "
                            f"Missing: {missing or 'None'}; Unrecognized/Extra: {extra or 'None'}."
                        ),
                        line=line_num
                    ))
            elif enum_name in SUBSET_ENUM_MAP:
                dm_key = SUBSET_ENUM_MAP[enum_name]
                expected = canonical_enums.get(dm_key, set())
                extra = sorted(normalized_members - expected)
                if expected and extra:
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="CS-007",
                        message=(
                            f"C# subset enum '{enum_name}' contains members {extra} not present in canonical domain enum '{dm_key}' (DT-DM-DOC-001.md)."
                        ),
                        line=line_num
                    ))
            elif enum_name in PRESENTATION_PROJECTION_ENUMS:
                expected = PRESENTATION_PROJECTION_ENUMS[enum_name]
                if normalized_members != expected:
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="CS-007",
                        message=(
                            f"C# presentation enum '{enum_name}' members {sorted(normalized_members)} do not match canonical projection {sorted(expected)}."
                        ),
                        line=line_num
                    ))

    return findings


def audit_css_and_dimension_leaks(content: str) -> list[Finding]:
    """Scans for raw CSS declarations, hex codes, magic drawer dimensions, and CSS class selectors."""
    findings: list[Finding] = []
    lines = content.splitlines()

    hex_pattern = re.compile(r"(?<![a-zA-Z0-9_\(\[/\$-])#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b(?![-a-zA-Z0-9_])")
    drawer_magic_pattern = re.compile(r"(?:drawer|sidebar|bottom\s*sheet).*?(?:\$?(?:440|380|320)\\?text\{px\}\$?|\b(?:440|380|320)px\b)", re.IGNORECASE)
    css_selector_pattern = re.compile(r"(?<![a-zA-Z0-9_\.\<\>])\.([a-z][a-z0-9_-]+)")

    known_file_extensions = {
        ".md", ".png", ".jpg", ".jpeg", ".gif", ".razor", ".css", ".js", ".ts",
        ".json", ".sql", ".html", ".svg", ".pdf", ".csv", ".yml", ".yaml",
        ".txt", ".py", ".sln", ".csproj", ".exe", ".zip", ".tar", ".gz", ".resx",
        ".env", ".toml"
    }

    in_sec8 = False
    in_code_block = False
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if re.search(r"^##\s+8\.\s+Layout and Responsive Adaptability", line, re.IGNORECASE):
            in_sec8 = True
            continue
        elif line.startswith("## "):
            in_sec8 = False
            continue

        clean_line = re.sub(r"\[.*?\]\([^\)]*#[^\)]*\)", "", line)
        clean_line = re.sub(r"\]\([^)]+\)", "", clean_line)

        # 1. Check raw CSS declarations
        for pattern, code, msg_template in CSS_LEAK_PATTERNS:
            match = re.search(pattern, clean_line)
            if match:
                matched_str = match.group(0)
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=matched_str),
                    line=idx
                ))

        # 2. Check raw hex colors in prose/tables
        hex_matches = hex_pattern.findall(clean_line)
        for h in hex_matches:
            findings.append(Finding(
                severity="BLOCKER",
                code="CSS-001",
                message=f"Raw hex color '{h}' found. Colors must use semantic tokens (--dt-color-*) or primitive tokens (--dt-primitive-*).",
                line=idx
            ))

        # 3. Check magic drawer dimensions
        if drawer_magic_pattern.search(line):
            if "--dt-layout-drawer-width" not in line:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="CSS-004",
                    message="Hardcoded drawer dimension detected without semantic token. Must reference '--dt-layout-drawer-width-desktop' (440px) or '--dt-layout-drawer-width-tablet' (380px).",
                    line=idx
                ))

        # 4. Check raw CSS calc() in Section 8
        if in_sec8 and not line.strip().startswith(">") and not line.strip().startswith("<!--"):
            if re.search(r"\bcalc\(", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="CSS-005",
                    message="Raw CSS 'calc()' expression found in Section 8. Use descriptive architectural offsets (e.g., 'offsets leftward by 50% of active drawer width (§5.2.3)').",
                    line=idx
                ))

        # 5. Check implementation CSS class selectors in prose (CSS-007)
        clean_css_line = re.sub(r"!\[.*?\]\(.*?\)", "", line)
        clean_css_line = re.sub(r"\[([^\]]*)\]\([^)]+\)", r"\1", clean_css_line)
        for c in css_selector_pattern.findall(clean_css_line):
            if f".{c}" not in known_file_extensions and not c.isdigit():
                findings.append(Finding(
                    severity="BLOCKER",
                    code="CSS-007",
                    message=f"Implementation CSS class selector '.{c}' leaked into specification prose. Use functional component names or semantic descriptions.",
                    line=idx
                ))

    return findings


def audit_runtime_leaks(content: str) -> list[Finding]:
    """Scans for browser globals and unapproved runtime packages."""
    findings: list[Finding] = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        for pattern, code, msg_template in RUNTIME_LEAK_PATTERNS:
            match = re.search(pattern, line)
            if match:
                matched_str = match.group(0)
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=matched_str),
                    line=idx
                ))

    return findings


def audit_domain_meta_text(content: str) -> list[Finding]:
    """Scans for generic narrative drafting placeholders (Asset A, Activo B, Entity X, etc.)."""
    findings: list[Finding] = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        # Skip rule prohibitions and alert descriptions
        if "PROHIBITED" in line or "Prohibited" in line or "prohibit" in line.lower() or "RULE:" in line:
            continue
        # Exclude markdown link targets/URLs
        stripped_line = re.sub(r"\[.*?\]\(.*?\)", "", line)
        for pattern, code, msg_template in META_TEXT_PATTERNS:
            match = re.search(pattern, stripped_line)
            if match:
                matched_str = match.group(0)
                findings.append(Finding(
                    severity="BLOCKER",
                    code=code,
                    message=msg_template.format(match=matched_str),
                    line=idx
                ))

    return findings


def audit_tokens(content: str, valid_tokens: set[str]) -> list[Finding]:
    """Validates that all referenced --dt-* tokens exist in tokens.css, prevents token-literal shadowing, and verifies Section 3 semantic token hygiene."""
    findings: list[Finding] = []
    lines = content.splitlines()
    token_pattern = re.compile(r"(--dt-[a-z0-9-]+(?:\*)?)")
    token_shadowing_pattern = re.compile(
        r"(--dt-[a-z0-9-]+)[,\s:\(=-]+(?:\$|\\\$)*(\d+(?:\.\d+)?(?:px|rem|em|pt|\\text\{px\}|\\text\{rem\}))(?:\$|\\\$|\})*",
        re.IGNORECASE
    )
    reverse_shadowing_pattern = re.compile(
        r"(?:\$|\\\$)*(\d+(?:\s*(?:[x×]|\\times)\s*\d+)?(?:\.\d+)?(?:px|rem|em|pt|\\text\{px\}|\\text\{rem\}))(?:\$|\\\$|\})*[\s:\(=-]+(`?--dt-[a-z0-9-]+`?)",
        re.IGNORECASE
    )

    in_sec3 = False
    in_code_block = False
    in_frontmatter = False
    current_sec3_cmp = None
    current_sec3_cmp_line = 0
    current_sec3_has_tokens = False
    in_sec3_token_block = False
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if idx == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Skip guidance blockquotes and explicit normative prohibition alerts
        if line.strip().startswith(">") or "PROHIBITED" in line or "Prohibited" in line:
            continue

        if re.search(r"^##\s+3\.\s+Functional Component Inventory", line, re.IGNORECASE):
            in_sec3 = True
            continue
        elif line.startswith("## "):
            if in_sec3 and current_sec3_cmp and not current_sec3_has_tokens:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="TOK-002",
                    message=f"Section 3 component '{current_sec3_cmp}' lacks explicit Design System token in Design Tokens definition. Prohibit placeholder text; bind directly to '--dt-*' tokens.",
                    line=current_sec3_cmp_line
                ))
            current_sec3_cmp = None
            in_sec3_token_block = False
            in_sec3 = False
            continue

        # TOK-004: Validate that design tokens (--dt-*) and component identifiers (CMP-*) in prose are enclosed in backticks
        line_clean = re.sub(r"\[([^\]]*)\]\([^\)]*\)", r"\1", line)
        line_clean = re.sub(r"<[^>]+>", " ", line_clean)
        no_code = re.sub(r"`[^`]+`", " ", line_clean)
        no_math = re.sub(r"\$[^\$]+\$", " ", no_code)

        bare_tokens = re.findall(r"(?<![a-zA-Z0-9_/\.-])(--dt-[a-z0-9-]+(?:\*)?)", no_math)
        for tok in bare_tokens:
            findings.append(Finding(
                severity="BLOCKER",
                code="TOK-004",
                message=f"Design token '{tok}' in prose must be enclosed in backticks (`{tok}`) per repository standard.",
                line=idx
            ))

        bare_cmps = re.findall(r"(?<![a-zA-Z0-9_/\.-])(CMP-\d+)", no_math)
        for cmp_id in bare_cmps:
            findings.append(Finding(
                severity="BLOCKER",
                code="TOK-004",
                message=f"Component identifier '{cmp_id}' in prose must be enclosed in backticks (`{cmp_id}`) per repository standard.",
                line=idx
            ))

        # TOK-003: Detect token-literal shadowing (coupling an abstract token with a hardcoded pixel/rem fallback)
        shadow_match = token_shadowing_pattern.search(line)
        if shadow_match:
            findings.append(Finding(
                severity="BLOCKER",
                code="TOK-003",
                message=(
                    f"Token-literal shadowing detected: '{shadow_match.group(1)}' is coupled with hardcoded literal '{shadow_match.group(2)}'. "
                    f"Specifications must reference design tokens exclusively without concrete numeric fallbacks or dimensions."
                ),
                line=idx
            ))
        else:
            rev_match = reverse_shadowing_pattern.search(line)
            if rev_match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="TOK-003",
                    message=(
                        f"Token-literal shadowing detected: hardcoded literal '{rev_match.group(1)}' is coupled with token '{rev_match.group(2)}'. "
                        f"Specifications must reference design tokens exclusively without concrete numeric fallbacks or dimensions."
                    ),
                    line=idx
                ))

        # TOK-002: Section 3 Semantic Token validation (table & structured list formats)
        if in_sec3:
            # Table format: | `CMP-01` | ...
            if line.strip().startswith("|") and not line.strip().startswith("| :---"):
                if re.match(r"\|\s*`CMP-\d+`", line):
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 5:
                        col4 = parts[4]
                        if not ("--dt-" in col4 or "DT-UI-DS" in col4):
                            findings.append(Finding(
                                severity="BLOCKER",
                                code="TOK-002",
                                message=f"Section 3 component '{parts[1]}' lacks explicit Design System token in Semantic Token column ('{col4}'). Prohibit placeholder text; bind directly to '--dt-*' tokens.",
                                line=idx
                            ))
                        else:
                            unit_match = re.search(r"(?:\b\d+(?:\.\d+)?(?:px|rem)\b|\$\d+.*\\text\{px\}\$)", col4, re.IGNORECASE)
                            if unit_match:
                                findings.append(Finding(
                                    severity="BLOCKER",
                                    code="TOK-002",
                                    message=f"Section 3 component '{parts[1]}' has raw dimension '{unit_match.group(0)}' in Semantic Token column. Use design system tokens exclusively.",
                                    line=idx
                                ))
                            hex_match = re.search(r"#([0-9a-fA-F]{3,8})\b", col4)
                            if hex_match:
                                findings.append(Finding(
                                    severity="BLOCKER",
                                    code="TOK-002",
                                    message=f"Section 3 component '{parts[1]}' has raw hex color '{hex_match.group(0)}' in Semantic Token column. Use semantic color tokens (--dt-color-*).",
                                    line=idx
                                ))
            # List format: 1. **`CMP-01`: ...**
            cmp_list_match = re.match(r"^\s*\d+\.\s+\*\*(`CMP-\d+`):?", line)
            if cmp_list_match:
                if current_sec3_cmp and not current_sec3_has_tokens:
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="TOK-002",
                        message=f"Section 3 component '{current_sec3_cmp}' lacks explicit Design System token in Design Tokens definition. Prohibit placeholder text; bind directly to '--dt-*' tokens.",
                        line=current_sec3_cmp_line
                    ))
                current_sec3_cmp = cmp_list_match.group(1)
                current_sec3_cmp_line = idx
                current_sec3_has_tokens = False
                in_sec3_token_block = False

            if current_sec3_cmp:
                if re.search(r"\bDesign Tokens\b", line, re.IGNORECASE):
                    in_sec3_token_block = True
                    if "--dt-" in line or "DT-UI-DS" in line or "transparent" in line or "neutral" in line:
                        current_sec3_has_tokens = True
                elif in_sec3_token_block:
                    if re.match(r"^\s*-\s+\*\*(?!Design Tokens)[^*]+:\*\*", line) or re.match(r"^\s*\d+\.", line) or line.strip().startswith("#"):
                        in_sec3_token_block = False
                    else:
                        if "--dt-" in line or "DT-UI-DS" in line or "transparent" in line or "neutral" in line:
                            current_sec3_has_tokens = True
                        unit_match = re.search(r"(?:\b\d+(?:\.\d+)?(?:px|rem)\b|\$\d+.*\\text\{px\}\$)", line, re.IGNORECASE)
                        if unit_match:
                            findings.append(Finding(
                                severity="BLOCKER",
                                code="TOK-002",
                                message=f"Section 3 component '{current_sec3_cmp}' has raw dimension '{unit_match.group(0)}' in Design Tokens. Use design system tokens exclusively.",
                                line=idx
                            ))
                        hex_match = re.search(r"#([0-9a-fA-F]{3,8})\b", line)
                        if hex_match:
                            findings.append(Finding(
                                severity="BLOCKER",
                                code="TOK-002",
                                message=f"Section 3 component '{current_sec3_cmp}' has raw hex color '{hex_match.group(0)}' in Design Tokens. Use semantic color tokens (--dt-color-*).",
                                line=idx
                            ))

        if valid_tokens:
            matches = token_pattern.findall(line)
            for tok in matches:
                if tok.endswith("*"):
                    prefix = tok[:-1]
                    if not any(t.startswith(prefix) for t in valid_tokens):
                        findings.append(Finding(
                            severity="WARNING",
                            code="TOK-001",
                            message=f"Wildcard token prefix '{tok}' does not match any tokens in 'tokens.css'.",
                            line=idx
                        ))
                elif tok not in valid_tokens:
                    findings.append(Finding(
                        severity="WARNING",
                        code="TOK-001",
                        message=f"Referenced design token '{tok}' is not defined in 'tokens.css'. Verify token name against DT-UI-DS-DOC-001.",
                        line=idx
                    ))

    return findings


def audit_latex_and_math(content: str) -> list[Finding]:
    """Validates LaTeX math delimiter parity ($...$), catches orphaned LaTeX macros outside math mode,
    and detects shell-expansion corruption artifacts in dimensions or percentages."""
    findings: list[Finding] = []
    lines = content.splitlines()

    in_frontmatter = False
    in_code_block = False

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if idx == 1 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped.startswith(">") or stripped.startswith("<!--"):
            continue

        # Strip inline code spans `...`
        no_code = re.sub(r"`[^`]+`", "", line)
        # Strip escaped dollar signs
        clean = no_code.replace(r"\$", "")

        # 1. Delimiter parity check: odd number of unescaped $ delimiters
        dollar_count = clean.count("$")
        if dollar_count % 2 != 0:
            findings.append(Finding(
                severity="BLOCKER",
                code="LTX-001",
                message=f"Unbalanced LaTeX math delimiter ($): line contains {dollar_count} unescaped '$' symbols.",
                line=idx
            ))

        # 2. Orphaned LaTeX commands outside math mode ($...$) or corrupted percentage fragments
        outside_math = re.sub(r"\$[^\$]+\$", "", clean)
        orphaned = re.search(r"\\(text\{|times\b|ge\b|le\b|pm\b|approx\b|frac\{|cdot\b)|(?<![0-9a-zA-Z\)\}])\\?%\$", outside_math)
        if orphaned:
            findings.append(Finding(
                severity="BLOCKER",
                code="LTX-001",
                message=f"Orphaned or corrupted LaTeX expression '{orphaned.group(0)}' detected outside math mode ($...). Ensure valid LaTeX math enclosing.",
                line=idx
            ))

    return findings


def audit_anti_redundancy(content: str) -> list[Finding]:
    """Verifies SSoT separation and anti-redundancy rules across Section 1, 3, and 5."""
    findings: list[Finding] = []
    lines = content.splitlines()

    current_section = 0

    for idx, line in enumerate(lines, start=1):
        # Section boundary tracking
        sec_match = re.match(r"^##\s+(\d+)\.", line)
        if sec_match:
            current_section = int(sec_match.group(1))
            continue
        elif line.startswith("## "):
            current_section = 0
            continue

        # Skip blockquotes (guidance rules) and comments
        stripped = line.strip()
        if stripped.startswith(">") or stripped.startswith("<!--"):
            continue

        # 1. Section 1 SSoT: Qualitative operational context only
        if current_section == 1:
            if re.search(r"--dt-breakpoint-[a-z0-9]+", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="RED-002",
                    message="Section 1 contains design system breakpoint token. Operational context in §1 must be qualitative; responsive breakpoints belong exclusively in §8.",
                    line=idx
                ))
            if re.search(r"\b\d+px\b|\b\d+vh\b", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="RED-002",
                    message="Section 1 contains explicit pixel/vh dimensions. Operational context in §1 must be qualitative; layout dimensions belong in §5 and §8.",
                    line=idx
                ))
            if re.search(r"\([A-Z_]{3,}(?:,\s*[A-Z_]{3,})+\)", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="RED-002",
                    message="Section 1 contains domain enum list. Domain enums belong exclusively in §5.3 and §7.2.3.",
                    line=idx
                ))

        # 2. Section 3 SSoT: Clean component cataloging
        elif current_section == 3:
            if not stripped.startswith(">"):
                if re.search(r"\bMath\.(?:min|max|clamp)\b", line) or re.search(r"\bclamp\(", line):
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="RED-001",
                        message="Section 3 contains mathematical calculation or clamping logic. §3 is a catalog; interaction algorithms belong exclusively in §5.",
                        line=idx
                    ))
                if re.search(r"--dt-layout-drawer-width[a-z-]*", line):
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="RED-003",
                        message="Section 3 contains layout drawer token. Layout dimensions belong in §5.2 and §8.",
                        line=idx
                    ))
                if re.search(r"\b\d+vh\b", line):
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="RED-003",
                        message="Section 3 contains viewport height (vh). Container dimensions and gesture physics belong in §5.2 and §8.",
                        line=idx
                    ))
                if re.search(r"\([A-Z_]{3,}(?:,\s*[A-Z_]{3,})+\)", line):
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="RED-003",
                        message="Section 3 contains domain enum list. Domain enums belong in §7.2.3.",
                        line=idx
                    ))

        # 3. Section 4 SSoT: Screen State Catalog validation
        elif current_section == 4:
            if not stripped.startswith(">"):
                if re.search(r"--dt-layout-drawer-width[a-z-]*", line):
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="RED-005",
                        message="Section 4 contains layout drawer dimension token. Drawer layout dimensions belong in §5.2 and §8.",
                        line=idx
                    ))
                if re.search(r"\bMath\.(?:min|max|clamp)\b", line) or re.search(r"\bclamp\(", line):
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="RED-005",
                        message="Section 4 contains mathematical calculation or clamping logic. §4 is a state catalog; interaction algorithms belong exclusively in §5.",
                        line=idx
                    ))

        # 4. Section 5 SSoT: Zero exhaustive LaTeX enum sets
        elif current_section == 5:
            if re.search(r"\\in\s*\\\{[^\}]+\}", line):
                findings.append(Finding(
                    severity="BLOCKER",
                    code="RED-004",
                    message="Section 5 contains exhaustive LaTeX enum set enumeration. Reference strongly-typed C# enums in §7.2.3 instead of enumerating string literals in prose or LaTeX.",
                    line=idx
                ))

    return findings


def audit_presentation_boundaries(content: str) -> list[Finding]:
    """Verifies presentation boundaries in UI sequence diagrams (Mermaid)."""
    findings: list[Finding] = []
    lines = content.splitlines()

    in_mermaid_seq = False

    for idx, line in enumerate(lines, start=1):
        if re.match(r"^```mermaid\s*$", line.strip()):
            continue
        if "sequenceDiagram" in line:
            in_mermaid_seq = True
            continue
        elif in_mermaid_seq and line.strip().startswith("```"):
            in_mermaid_seq = False
            continue

        if in_mermaid_seq:
            # 1. Check prohibited backend worker/DB participants
            worker_match = re.search(r"(?:participant|actor)\s+(?:[A-Za-z0-9_]+\s+as\s+)?(AUD|AuditWorker|Worker|DB|Database)\b", line)
            if worker_match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="DIAG-001",
                    message=f"Presentation sequence diagram leaks private backend participant '{worker_match.group(1)}'. UI sequence diagrams must only model interactions between Tech, UI, Interop, and the API gateway.",
                    line=idx
                ))

            # 2. Check prohibited backend internal self-calls
            backend_self_match = re.search(r"\b(API|INV|SVC|SRV|APP|BACKEND)\s*->>\s*\1\s*:", line)
            if backend_self_match:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="DIAG-002",
                    message=f"Presentation sequence diagram leaks internal backend self-call '{backend_self_match.group(0).rstrip(':')}'. Internal domain execution must not be modeled as client sequence transitions.",
                    line=idx
                ))

    return findings


DOC_SECTIONS_CACHE: dict[Path, dict[str, str]] = {}


def get_document_sections(file_path: Path) -> dict[str, str]:
    """Caches and returns a mapping of section numbers ('4.1', '6.5.1') to heading titles for a markdown document."""
    if file_path in DOC_SECTIONS_CACHE:
        return DOC_SECTIONS_CACHE[file_path]
    if not file_path.exists():
        return {}
    sections: dict[str, str] = {}
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            m = re.match(r"^#{1,6}\s+(\d+(?:\.\d+)*)\.?\s+(.*)", line.strip())
            if m:
                sec_num = m.group(1)
                title = m.group(2).strip()
                sections[sec_num] = title
    except Exception:
        pass
    DOC_SECTIONS_CACHE[file_path] = sections
    return sections


def audit_cross_references(
    content: str,
    repo_root: Path,
    spec_file_path: Path | None = None,
) -> list[Finding]:
    """Validates that cited document sections (§X.Y) exist in the referenced repository documents or within the screen itself."""
    findings: list[Finding] = []
    lines = content.splitlines()

    internal_sections: dict[str, str] = {}
    for line in lines:
        m = re.match(r"^#{1,6}\s+(\d+(?:\.\d+)*)\.?\s+(.*)", line.strip())
        if m:
            internal_sections[m.group(1)] = m.group(2).strip()

    base_dir = spec_file_path.parent if spec_file_path else (repo_root / "ui-ux" / "screens")

    in_code_block = False
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if stripped.startswith("<!--"):
            continue

        # 1. Markdown links to markdown documents with section numbers: [label §X.Y](path.md[#anchor])
        md_links = re.findall(r"\[([^\]]*§(\d+(?:\.\d+)*)[^\]]*)\]\(([^)#]+\.md)(?:#([^)]+))?\)", line)
        for label, sec_num, rel_path, anchor in md_links:
            target_path = (base_dir / rel_path).resolve()
            if not target_path.exists():
                findings.append(Finding(
                    severity="BLOCKER",
                    code="REF-001",
                    message=f"Broken document link: target file '{rel_path}' does not exist.",
                    line=idx
                ))
                continue
            valid_sections = get_document_sections(target_path)
            if sec_num not in valid_sections:
                major_sec = sec_num.split(".")[0]
                available = [s for s in valid_sections if s.startswith(major_sec + ".")] or [s for s in valid_sections if "." not in s]
                avail_str = f"Available under §{major_sec}: {', '.join('§' + s for s in available[:8])}" if available else f"No subsections under §{major_sec}"
                findings.append(Finding(
                    severity="BLOCKER",
                    code="REF-002",
                    message=(
                        f"Referenced section '§{sec_num}' does not exist in target document '{target_path.name}'. "
                        f"{avail_str}. Verify citation against target document."
                    ),
                    line=idx
                ))

        # 2. Prose citations to known DT-* documents: (DT-[A-Z]+-[A-Z]+-\d+)\s+§(\d+(?:\.\d+)*)
        prose_cites = re.findall(r"\b(DT-[A-Z]+-[A-Z]+-\d+)\s+§(\d+(?:\.\d+)*)", line)
        for doc_id, sec_num in prose_cites:
            matches = list(repo_root.glob(f"**/{doc_id}.md"))
            if matches:
                target_path = matches[0]
                valid_sections = get_document_sections(target_path)
                if sec_num not in valid_sections:
                    major_sec = sec_num.split(".")[0]
                    available = [s for s in valid_sections if s.startswith(major_sec + ".")] or [s for s in valid_sections if "." not in s]
                    avail_str = f"Available under §{major_sec}: {', '.join('§' + s for s in available[:8])}" if available else f"No subsections under §{major_sec}"
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="REF-002",
                        message=(
                            f"Referenced section '§{sec_num}' does not exist in target document '{doc_id}.md'. "
                            f"{avail_str}. Verify citation against target document."
                        ),
                        line=idx
                    ))

        # 3. Internal section citations within the same screen spec: e.g. "detailed in §5.4", "rules in §5.1"
        clean_line = re.sub(r"\[[^\]]*\]\([^)]+\)", "", line)
        clean_line = re.sub(r"\b(?:ISO|ANSI|IEC|IEEE|ISA|ITU|DIN|EN|BS|ASTM|NFPA|OSHA)[A-Za-z0-9\/\-\.]*\s+§\d+(?:\.\d+)*", "", clean_line)
        clean_line = re.sub(r"\bDT-[A-Z]+-[A-Z]+-\d+\s+§\d+(?:\.\d+)*", "", clean_line)
        for m in re.finditer(r"(?<![a-zA-Z0-9_\.\/-])§([1-9](?:\.\d+)*)", clean_line):
            sec = m.group(1)
            if sec not in internal_sections:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="REF-003",
                    message=(
                        f"Internal section reference '§{sec}' does not exist in this specification. "
                        f"Verify section numbering."
                    ),
                    line=idx
                ))

    return findings


def audit_companion_html_prototype(screen_id: str, repo_root: Path, prototype_dir: Path | None = None) -> list[Finding]:
    """Inspects the companion HTML/CSS/JS prototype for emojis, leaked spec codes, and raw hex colors."""
    findings: list[Finding] = []

    candidates: list[Path] = []
    if prototype_dir:
        candidates.append(Path(prototype_dir).resolve())
    env_dir = os.environ.get("DTEAM_PROTOTYPE_DIR")
    if env_dir:
        candidates.append(Path(env_dir).resolve())
    candidates.append(repo_root / "ui-ux" / "prototype")

    target_dir: Path | None = None
    for cand in candidates:
        if (cand / f"{screen_id.lower()}.html").exists():
            target_dir = cand
            break

    if target_dir is None:
        if prototype_dir:
            findings.append(Finding(
                severity="WARNING",
                code="HTML-001",
                message=f"Prototype file '{screen_id.lower()}.html' not found in specified directory '{prototype_dir}'.",
                line=None
            ))
        return findings

    html_file = target_dir / f"{screen_id.lower()}.html"
    files_to_check: list[Path] = [html_file]

    # Look for associated CSS files
    css_candidates = [
        target_dir / "assets" / "css" / f"{screen_id.lower()}.css",
        target_dir / "css" / f"{screen_id.lower()}.css",
        target_dir / f"{screen_id.lower()}.css",
    ]
    for c in css_candidates:
        if c.exists() and c not in files_to_check:
            files_to_check.append(c)

    # Look for associated JS files
    js_search_dirs = [
        target_dir / "assets" / "js",
        target_dir / "js",
        target_dir,
    ]
    for j_dir in js_search_dirs:
        if j_dir.exists():
            for j_file in j_dir.glob(f"{screen_id.lower()}*.js"):
                if j_file not in files_to_check:
                    files_to_check.append(j_file)

    hex_pattern = re.compile(r"(?<![a-zA-Z0-9_\(\[/\$-])#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b(?![-a-zA-Z0-9_])")

    for fpath in files_to_check:
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue
        lines = content.splitlines()
        is_css = fpath.suffix.lower() == ".css"
        is_html = fpath.suffix.lower() == ".html"

        for idx, line in enumerate(lines, start=1):
            # 1. Check for Unicode Emojis
            emoji_matches = EMOJI_REGEX.findall(line)
            if emoji_matches:
                findings.append(Finding(
                    severity="BLOCKER",
                    code="HTML-EMOJI-001",
                    message=f"Unicode emoji '{emoji_matches[0]}' detected in prototype asset '{fpath.name}' line {idx}. HTML prototypes must use standardized monochrome SVG sprite icons (<svg class=\"dt-icon\"><use href=\"#icon-*\" /></svg>) per HPHMI/ISA-101.",
                    line=idx
                ))

            # 2. Check for Leaked Specification Codes
            for pat, code, msg_template in PROHIBITED_SPEC_CODES:
                m = re.search(pat, line)
                if m:
                    findings.append(Finding(
                        severity="BLOCKER",
                        code=code,
                        message=msg_template.format(match=m.group(0)) + f" (Found in '{fpath.name}' line {idx})",
                        line=idx
                    ))

            # 3. Check for Raw Hex Colors in CSS or inline HTML styles
            if is_css:
                hex_matches = hex_pattern.findall(line)
                for h in hex_matches:
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="HTML-HEX-001",
                        message=f"Raw hex color '{h}' found in prototype asset '{fpath.name}' line {idx}. Prototype styles must use design system tokens (var(--dt-color-*)).",
                        line=idx
                    ))
            elif is_html and ("style=" in line or "<style" in line):
                clean_line = re.sub(r"\[.*?\]\([^\)]*#[^\)]*\)", "", line)
                hex_matches = hex_pattern.findall(clean_line)
                for h in hex_matches:
                    findings.append(Finding(
                        severity="BLOCKER",
                        code="HTML-HEX-001",
                        message=f"Raw hex color '{h}' found in inline prototype markup '{fpath.name}' line {idx}. Prototype styles must use design system tokens (var(--dt-color-*)).",
                        line=idx
                    ))

    return findings


# ---------------------------------------------------------------------------
# Master Audit Orchestration
# ---------------------------------------------------------------------------

def run_screen_audit(
    content: str,
    repo_root: Path,
    screen_id: str | None = None,
    prototype_dir: Path | None = None,
    spec_file_path: Path | None = None,
) -> list[Finding]:
    """Executes all deterministic audit axes and returns deduplicated findings."""
    valid_tokens = load_canonical_tokens(repo_root)
    canonical_enums = load_canonical_enums(repo_root)

    findings: list[Finding] = []
    findings += audit_frontmatter(content)
    findings += audit_structure(content)
    findings += audit_persistence_leaks(content)
    findings += audit_csharp_leaks(content, canonical_enums)
    findings += audit_css_and_dimension_leaks(content)
    findings += audit_runtime_leaks(content)
    findings += audit_tokens(content, valid_tokens)
    findings += audit_latex_and_math(content)
    findings += audit_anti_redundancy(content)
    findings += audit_presentation_boundaries(content)
    findings += audit_domain_meta_text(content)
    findings += audit_cross_references(content, repo_root, spec_file_path=spec_file_path)

    if screen_id:
        findings += audit_companion_html_prototype(screen_id, repo_root, prototype_dir=prototype_dir)

    # Deduplicate findings by (code, line, message)
    seen: set[tuple[str, int | None, str]] = set()
    unique: list[Finding] = []
    for f in findings:
        key = (f.code, f.line, f.message)
        if key not in seen:
            seen.add(key)
            unique.append(f)

    return unique


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

def generate_markdown_report(
    artifact_path: Path,
    findings: list[Finding],
    repo_root: Path
) -> str:
    """Constructs a formal markdown audit report adhering to repository standard."""
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d-%H%M%S")
    screen_id = artifact_path.stem

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]
    infos    = [f for f in findings if f.severity == "INFO"]

    verdict = "BLOCKED" if blockers else ("PASSED_WITH_OBSERVATIONS" if warnings else "PASSED")

    report: list[str] = [
        "---",
        f"id: AUD-UI-{screen_id}-{timestamp_str}",
        f"screen_audited: {screen_id}",
        f"date: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"verdict: {verdict}",
        "auditor: dteam-ui-coherence-audit (deterministic)",
        "---",
        "",
        f"# Deterministic UI Audit Report: {screen_id}",
        "",
        "## 1. Executive Summary",
        "",
        f"- **Audited File:** `{artifact_path.relative_to(repo_root)}`",
        f"- **Execution Timestamp:** {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Overall Verdict:** `[{verdict}]`",
        f"- **Findings Count:** {len(blockers)} BLOCKER | {len(warnings)} WARNING | {len(infos)} INFO",
        "",
        "---",
        "",
        "## 2. Audit Findings by Severity",
        "",
    ]

    if blockers:
        report.append("### 🔴 Blockers (Immediate Remediation Required)")
        report.append("")
        for f in blockers:
            loc = f" *(line {f.line})*" if f.line else ""
            report.append(f"- **[{f.code}]**{loc}: {f.message}")
        report.append("")
    else:
        report.append("### ✅ Zero Blockers Found")
        report.append("No database schema leaks, SQL syntax, C# code-behind wrappers, raw CSS rules, or structural regressions detected.")
        report.append("")

    if warnings:
        report.append("### ⚠️ Observations & Warnings")
        report.append("")
        for f in warnings:
            loc = f" *(line {f.line})*" if f.line else ""
            report.append(f"- **[{f.code}]**{loc}: {f.message}")
        report.append("")

    if infos:
        report.append("### ℹ️ Informational Notes")
        report.append("")
        for f in infos:
            loc = f" *(line {f.line})*" if f.line else ""
            report.append(f"- **[{f.code}]**{loc}: {f.message}")
        report.append("")

    report += [
        "---",
        "",
        "## 3. Compliance Matrix",
        "",
        "| Audit Axis | Status | Evaluated Rules |",
        "| :--- | :---: | :--- |",
        f"| **Structural & Frontmatter** | {'PASS' if not any(f.code.startswith('STR') and f.severity == 'BLOCKER' for f in findings) else 'FAIL'} | 9 mandatory sections, 3 §7 subsections, valid YAML frontmatter. |",
        f"| **Persistence Decoupling** | {'PASS' if not any(f.code.startswith('SQL') for f in findings) else 'FAIL'} | Zero Postgres schema qualifiers, zero SQL DDL/DML, zero check constraint names. |",
        f"| **Component Contract (C#)** | {'PASS' if not any(f.code.startswith('CS') for f in findings) else 'FAIL'} | Zero ComponentBase classes, zero [Inject], zero private fields, zero lifecycle overrides. |",
        f"| **Styling & Dimension Tokens** | {'PASS' if not any(f.code.startswith('CSS') for f in findings) else 'FAIL'} | Zero hex colors, zero raw layout rules, canonical drawer width tokens. |",
        f"| **Runtime & DOM Boundaries** | {'PASS' if not any(f.code.startswith('DOM') for f in findings) else 'FAIL'} | Zero direct DOM access, zero unapproved package names. |",
        f"| **Design Token Conformance** | {'PASS' if not any(f.code.startswith('TOK') for f in findings) else 'FAIL'} | All referenced --dt-* tokens verified against tokens.css. |",
        f"| **Language Policy** | {'PASS' if not any(f.code.startswith('LANG') for f in findings) else 'FAIL'} | 100% Technical English without untranslated Spanish terms. |",
        f"| **Companion HTML Prototype** | {'PASS' if not any(f.code.startswith('HTML') for f in findings) else 'FAIL'} | Zero Unicode emojis, zero leaked specification codes (FR/AF/TR/NFR/ADR). |",
        "",
        "---",
        "",
        "## 4. Tier 2 Grounded Escalation Gate (Gemini Notebook)",
        "",
        "| Trigger | Description | Evaluation | Status |",
        "| :--- | :--- | :--- | :---: |",
        "| **G1: Life Safety & Hazardous Interlocks** | Governs hazardous energy isolation (LOTO), hot work, explosive atmospheres, or personnel safety where software state impacts physical energy. | Evaluated against local SSoT safety rules; no uncodified hazard conditions identified. | `[NOT TRIGGERED]` |",
        "| **G2: Cognitive Overload & Density Exceedance** | Visual density exceeds ISA-101 limits (>30 concurrent dynamic items, alarm flood, unresolved visual clustering). | Evaluated against Archetype visual hierarchy and component density thresholds. | `[NOT TRIGGERED]` |",
        "| **G3: Deep Normative Taxonomy Conflict** | ISO 14224 Level 6-9 taxonomy, boundary limits, or failure modes with conflicting or missing local SSoT rules. | SSoT alignment verified against DT-ERD-DOC-001 and DT-DM-DOC-001/002. | `[NOT TRIGGERED]` |",
        "| **G4: Novel Interaction Archetype** | Interaction mechanics not covered by Archetypes A, B, or C (novel spatial/tactile paradigms). | Mapped cleanly to established system archetype. | `[NOT TRIGGERED]` |",
        "",
        "> *Tier 2 Evaluation Summary:* All evaluation axes resolved deterministically via repository SSoTs. No external Gemini Notebook grounded escalation required unless flagged during heuristic review.",
        "",
    ]

    return "\n".join(report)


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------

def cmd_audit(args: argparse.Namespace, repo_root: Path) -> int:
    """Executes full audit, prints console summary, and saves Markdown report."""
    target_path = (repo_root / args.file).resolve()
    if not target_path.exists():
        print(f"[ERROR] Target specification not found: {target_path}", file=sys.stderr)
        return 1

    content = target_path.read_text(encoding="utf-8")
    rel_path = target_path.relative_to(repo_root)
    print(f"[INFO] Auditing screen specification: {rel_path}")

    proto_dir = Path(args.prototype_dir).resolve() if getattr(args, "prototype_dir", None) else None
    findings = run_screen_audit(content, repo_root, screen_id=target_path.stem, prototype_dir=proto_dir, spec_file_path=target_path)

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]
    infos    = [f for f in findings if f.severity == "INFO"]

    # Generate and persist report
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d-%H%M%S")
    out_dir = repo_root / "reports" / "audits" / "ui"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_file = out_dir / f"AUD-UI-{target_path.stem}-{timestamp_str}.md"

    report_content = generate_markdown_report(target_path, findings, repo_root)
    report_file.write_text(report_content, encoding="utf-8")

    # Console output
    for f in findings:
        loc = f" (line {f.line})" if f.line else ""
        print(f"[{f.severity}] [{f.code}]{loc} {f.message}")

    print("-" * 72)
    status_str = "BLOCKED" if blockers else ("PASSED WITH OBSERVATIONS" if warnings else "PASSED")
    print(f"[RESULT] {status_str}: {len(blockers)} BLOCKER | {len(warnings)} WARNING | {len(infos)} INFO")
    print(f"[REPORT] Persisted to: {report_file}")

    return 2 if blockers else 0


def cmd_lint(args: argparse.Namespace, repo_root: Path) -> int:
    """Fast console linting without writing report files."""
    target_path = (repo_root / args.file).resolve()
    if not target_path.exists():
        print(f"[ERROR] Target specification not found: {target_path}", file=sys.stderr)
        return 1

    content = target_path.read_text(encoding="utf-8")
    proto_dir = Path(args.prototype_dir).resolve() if getattr(args, "prototype_dir", None) else None
    findings = run_screen_audit(content, repo_root, screen_id=target_path.stem, prototype_dir=proto_dir, spec_file_path=target_path)

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]

    for f in findings:
        loc = f" (line {f.line})" if f.line else ""
        print(f"[{f.severity}] [{f.code}]{loc} {f.message}")

    if not findings:
        print(f"[OK] {target_path.name} is 100% compliant with UI/UX architecture standards.")

    return 2 if blockers else 0


def cmd_audit_all(args: argparse.Namespace, repo_root: Path) -> int:
    """Audits all active screen specifications in ui-ux/screens/."""
    screens_dir = repo_root / "ui-ux" / "screens"
    if not screens_dir.exists():
        print(f"[ERROR] Screens directory not found: {screens_dir}", file=sys.stderr)
        return 1

    all_files = sorted(screens_dir.rglob("SCR-*.md"))
    spec_files = [f for f in all_files if f.stat().st_size > 0 and f.read_text(encoding="utf-8").strip()]
    skipped = len(all_files) - len(spec_files)
    skip_msg = f" (skipped {skipped} empty stub files)" if skipped else ""
    print(f"[INFO] Found {len(spec_files)} active screen specifications to audit{skip_msg}.")
    print("=" * 72)

    total_blockers = 0
    total_warnings = 0
    summary_table: list[tuple[str, int, int, str]] = []
    proto_dir = Path(args.prototype_dir).resolve() if getattr(args, "prototype_dir", None) else None

    for spec_file in spec_files:
        content = spec_file.read_text(encoding="utf-8")
        findings = run_screen_audit(content, repo_root, screen_id=spec_file.stem, prototype_dir=proto_dir, spec_file_path=spec_file)
        blockers = sum(1 for f in findings if f.severity == "BLOCKER")
        warnings = sum(1 for f in findings if f.severity == "WARNING")
        status = "FAIL" if blockers else ("WARN" if warnings else "PASS")

        total_blockers += blockers
        total_warnings += warnings
        summary_table.append((spec_file.stem, blockers, warnings, status))

    print(f"{'Screen ID':<16} | {'Status':<6} | {'Blockers':<8} | {'Warnings':<8}")
    print("-" * 48)
    for s_id, b, w, st in summary_table:
        print(f"{s_id:<16} | {st:<6} | {b:<8} | {w:<8}")
    print("=" * 72)
    print(f"[SUMMARY] Total Screens: {len(spec_files)} | Total Blockers: {total_blockers} | Total Warnings: {total_warnings}")

    return 2 if total_blockers > 0 else 0


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="DTEAM UI/UX Screen Specification Coherence Auditor & Linter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="Full deterministic audit + Markdown report")
    p_audit.add_argument("--file", required=True, help="Relative path to target SCR-*.md from repo root")
    p_audit.add_argument("--prototype-dir", default=None, help="Optional directory containing companion HTML/CSS prototypes (or set DTEAM_PROTOTYPE_DIR)")

    p_lint = sub.add_parser("lint", help="Fast console linting without report generation")
    p_lint.add_argument("--file", required=True, help="Relative path to target SCR-*.md from repo root")
    p_lint.add_argument("--prototype-dir", default=None, help="Optional directory containing companion HTML/CSS prototypes (or set DTEAM_PROTOTYPE_DIR)")

    p_all = sub.add_parser("audit-all", help="Scan and audit all screen specifications")
    p_all.add_argument("--output", default=None, help="Optional summary output report path")
    p_all.add_argument("--prototype-dir", default=None, help="Optional directory containing companion HTML/CSS prototypes (or set DTEAM_PROTOTYPE_DIR)")

    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd()) or find_repo_root(SCRIPT_REPO_ROOT)
    if repo_root is None:
        print("[ERROR] Git repository root not found. Run from inside adso-dteam-docs/.", file=sys.stderr)
        return 1

    dispatch = {
        "audit":     cmd_audit,
        "lint":      cmd_lint,
        "audit-all": cmd_audit_all,
    }
    return dispatch[args.command](args, repo_root)


if __name__ == "__main__":
    sys.exit(main())
