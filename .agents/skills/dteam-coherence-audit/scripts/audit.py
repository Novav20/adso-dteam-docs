#!/usr/bin/env python3
"""
DTEAM Docs-as-Code Coherence Auditor
=====================================
Verifica trazabilidad, coherencia normativa y scope guard sobre artefactos
del repositorio adso-dteam-docs (proyecto DTEAM).

Uso:
    uv run audit.py audit       --file <ruta-relativa>
    uv run audit.py check-refs  --file <ruta-relativa>
    uv run audit.py check-scope --file <ruta-relativa>
    uv run audit.py audit-all   --output <ruta-salida>
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
# APPROVED MVP INDICES — update only by explicit architectural decision
# ---------------------------------------------------------------------------

MVP_APPROVED_UCS: set[str] = {
    "UC-VIS-008", "UC-VIS-009", "UC-VIS-010", "UC-VIS-011", "UC-VIS-033",
    "UC-MTTO-001", "UC-MTTO-002", "UC-MTTO-023", "UC-MTTO-026", "UC-MTTO-029",
    "UC-INV-005", "UC-INV-006", "UC-INV-007", "UC-INV-025", "UC-INV-027", "UC-INV-031",
    "UC-ADM-013", "UC-ADM-014", "UC-ADM-032",
}

MVP_APPROVED_SCREENS: set[str] = {
    "SCR-VIS-001", "SCR-VIS-002", "SCR-VIS-003",
    "SCR-VIS-008", "SCR-VIS-011", "SCR-VIS-033",
    "SCR-MTTO-001", "SCR-MTTO-002", "SCR-MTTO-003", "SCR-MTTO-004", "SCR-MTTO-005",
    "SCR-MTTO-023", "SCR-MTTO-026", "SCR-MTTO-029",
    "SCR-INV-001", "SCR-INV-002", "SCR-INV-003", "SCR-INV-004", "SCR-INV-005",
    "SCR-INV-006", "SCR-INV-025", "SCR-INV-027", "SCR-INV-031",
    "SCR-ADM-001", "SCR-ADM-002", "SCR-ADM-003",
    "SCR-ADM-013", "SCR-ADM-014", "SCR-ADM-032",
}

APPROVED_ROLES: set[str] = {
    "Technician", "Supervisor", "Planner", "Reliability Eng.",
    "Warehouse Manager", "HSEQ", "Administrator", "Auditor", "Manager",
    "Reliability Engineering", "Field Technician",
}

APPROVED_COLOR_PALETTE: set[str] = {
    # Primitivos (DS v1.2)
    "#11141A", "#16191F", "#1E222B", "#2A2F3D", "#353B4D",
    "#5C667A", "#6B7280", "#6E7A92", "#7E8B9B", "#8A98AA",
    "#B8C0CC", "#D8DBE0", "#E5E8EC", "#F4F5F7", "#FFFFFF",
    "#FDFEFE", "#C2CBD6", "#4B5563", "#1F2937", "#111827",
    "#3A4154",
    # Alarmas y estados (v1.2 — valores actualizados)
    "#E63946",  # alarm-critical
    "#AC5E04",  # alarm-warning light (AJUSTADO v1.2)
    "#D97706",  # amber base (primitive, not semantic)
    "#F4A261",  # alarm-warning dark
    "#2563EB",  # state-info light
    "#4881A4",  # state-info dark (AJUSTADO v1.2)
    "#457B9D",  # blue-400 base
    "#0B857A",  # state-success light (AJUSTADO v1.2)
    "#0D9488",  # teal-600 base
    "#2A9D8F",  # state-success dark
    "#9CA3AF", "#4A5263",
    # MAI
    "#BAE6FD", "#0369A1",
    # Alarm text
    "#FFFFFF",  # alarm-text-critical
}

APPROVED_STANDARDS: set[str] = {
    "ISA-101", "ANSI/ISA-101", "ISA-101.01", "ANSI/ISA-101.01",
    "ISO 9241-110", "ISO 9241-210", "ISO 9241-110:2020", "ISO 9241-210:2019",
    "ISO 45001", "ISO 45001:2018",
    "ISO 14224", "ISO 14224:2016",
    "WCAG 2.1", "WCAG 2.1 AA", "WCAG 2.1 AAA",
    "IEC 62443", "NFPA 70E",
}

APPROVED_TECH: set[str] = {
    ".NET MAUI", "Blazor Hybrid", "Blazor Web App", "Razor", "RCL",
    "C#", ".NET 10", "ASP.NET Core", "SignalR",
    "sqlite-net-pcl", "SQLCipher", "PostgreSQL", "TimescaleDB",
    "Azure IoT Hub", "Docker", "Nginx", "Azure",
    "SVG", "MQTT", "AMQP", "HTTPS", "WSS", "TLS",
    "JWT", "PBKDF2", "AES-256",
}

FORBIDDEN_TECH_PATTERNS: list[tuple[str, str]] = [
    (r"\bReact\b(?!\s+Native\s+Paper|\s+Native\s+Navigation)", "React (frontend no aprobado — usar Blazor)"),
    (r"\bAngular\b", "Angular (frontend no aprobado — usar Blazor)"),
    (r"\bVue\.?js\b", "Vue.js (frontend no aprobado — usar Blazor)"),
    (r"\bReact Native\b", "React Native (plataforma no aprobada — usar .NET MAUI)"),
    (r"\bFlutter\b", "Flutter (plataforma no aprobada — usar .NET MAUI)"),
    (r"\bEntity Framework.*mobile\b", "EF Core on mobile (forbidden — use sqlite-net-pcl)"),
    (r"\bREST\s+sin\s+contrato\b", "REST sin contrato (requiere OpenAPI/Swagger)"),
]

VALID_ISA_LEVELS: set[str] = {"L1", "L2", "L3", "L4"}
VALID_CLIENTS: set[str] = {"maui", "web", "both", "mobile", "desktop"}

# ---------------------------------------------------------------------------
# Modelos de Hallazgo
# ---------------------------------------------------------------------------

class Finding(NamedTuple):
    severity: str   # BLOCKER | WARNING | INFO
    code: str       # B-001, W-002, I-003
    message: str
    line: int | None = None

# ---------------------------------------------------------------------------
# Repository search utilities
# ---------------------------------------------------------------------------

def find_repo_root(start: Path) -> Path | None:
    """Sube desde `start` buscando el directorio .git."""
    current = start.resolve()
    for _ in range(10):
        if (current / ".git").exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def file_exists_in_repo(repo_root: Path, id_pattern: str) -> bool:
    """Searches for any file whose name contains the pattern (glob-like)."""
    for p in repo_root.rglob(f"*{id_pattern}*"):
        if p.is_file():
            return True
    return False

# ---------------------------------------------------------------------------
# Audit Axes
# ---------------------------------------------------------------------------

def _counters() -> dict[str, int]:
    return {"B": 0, "W": 0, "I": 0}


def audit_traceability(content: str, repo_root: Path) -> list[Finding]:
    """Eje 1: Valida que todos los IDs referenciados existan en el repositorio."""
    findings: list[Finding] = []
    b = _counters()["B"]
    w = _counters()["W"]

    patterns = [
        # (regex, blocker_or_warning, label)
        (r"\bUC-[A-Z]+-\d+\b",   "BLOCKER", "Caso de Uso"),
        (r"\bSCR-[A-Z]+-\d+\b",  "BLOCKER", "Screen"),
        (r"\bADR-\d+\b",         "BLOCKER", "Architecture Decision Record"),
        (r"\bASR-\d+\b",         "WARNING", "Architecturally Significant Requirement"),
        (r"\bDT-UI-DS-DOC-\d+\b","WARNING", "Documento Design System"),
        (r"\bDT-UI-NAV-DOC-\d+\b","WARNING","Navigation Document"),
        (r"\bDT-ARQ-[A-Z-]+-\d+\b","WARNING","Artefacto de Arquitectura"),
        (r"\bDT-DM-DOC-\d+\b",   "WARNING", "Documento Modelo de Dominio"),
        (r"\bDT-UC-TRC-\d+\b",   "WARNING", "Trazabilidad de Casos de Uso"),
    ]

    found_ids: set[str] = set()
    for pattern, severity, label in patterns:
        for match in re.finditer(pattern, content):
            artifact_id = match.group(0)
            if artifact_id in found_ids:
                continue
            found_ids.add(artifact_id)
            line_num = content[:match.start()].count("\n") + 1
            if not file_exists_in_repo(repo_root, artifact_id):
                if severity == "BLOCKER":
                    b += 1
                    findings.append(Finding(
                        "BLOCKER", f"B-TR{b:02d}",
                        f"{label} `{artifact_id}` referenciado pero no existe en el repositorio.",
                        line_num
                    ))
                else:
                    w += 1
                    findings.append(Finding(
                        "WARNING", f"W-TR{w:02d}",
                        f"{label} `{artifact_id}` referenced but its file was not found. Verify the name.",
                        line_num
                    ))
    return findings


def audit_normative(content: str) -> list[Finding]:
    """Axis 2: Verifies coherence with approved standards, tokens, and roles."""
    findings: list[Finding] = []
    b, w, i = 0, 0, 0

    # — Colores hexadecimales no en paleta
    for match in re.finditer(r"#([0-9A-Fa-f]{6})\b", content):
        color = f"#{match.group(1).upper()}"
        if color.upper() not in {c.upper() for c in APPROVED_COLOR_PALETTE}:
            line_num = content[:match.start()].count("\n") + 1
            # Detectar si es el token obsoleto D97706 (reemplazado en v1.2)
            if color.upper() == "#D97706":
                w += 1
                findings.append(Finding(
                    "WARNING", f"W-NRM{w:02d}",
                    f"Color `{color}` is the primitive base amber. The semantic warning token "
                    f"en tema claro fue actualizado a `#AC5E04` en v1.2 (WCAG AA 3.47:1). "
                    f"Using the primitive explicitly is valid only in the palette section.",
                    line_num
                ))
            else:
                w += 1
                findings.append(Finding(
                    "WARNING", f"W-NRM{w:02d}",
                    f"Color `{color}` is not in the approved palette of DT-UI-DS-DOC-001 v1.2.",
                    line_num
                ))

    # — Invalid ISA-101 Levels (Lx donde x no es 1-4)
    # Excluir ocurrencias dentro de versiones de norma (ej. 9241-110) o URLs
    for match in re.finditer(r"(?<![0-9\-./])L(\d+)\b", content):
        level = f"L{match.group(1)}"
        if level not in VALID_ISA_LEVELS:
            line_num = content[:match.start()].count("\n") + 1
            b += 1
            findings.append(Finding(
                "BLOCKER", f"B-NRM{b:02d}",
                f"ISA-101 Level `{level}` invalid. Only L1, L2, L3, and L4 are allowed "
                f"according to DT-UI-NAV-DOC-001.",
                line_num
            ))

    # — Prohibited Technologies
    for pattern, description in FORBIDDEN_TECH_PATTERNS:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            line_num = content[:match.start()].count("\n") + 1
            w += 1
            findings.append(Finding(
                "WARNING", f"W-NRM{w:02d}",
                f"Unapproved technology found: {description}. "
                f"Verificar contra DT-ARQ-TECH-001 y ADR-004.",
                line_num
            ))

    # — Frontmatter: verificar campo `standard` si existe
    fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL | re.MULTILINE)
    if fm_match:
        fm = fm_match.group(1)
        # Extracts standards listed under specific keys
        std_match = re.search(r"(?:standards|normativa|normas|estandar):\s*\n((?:\s*-\s+[^\n]+\n?)+)", fm, re.IGNORECASE)
        if std_match:
            std_lines = re.findall(r"-\s+([^\n]+)", std_match.group(1))
            for std_line in std_lines:
                # Extracts the acronym before the parenthesis if there is one
                std_name = std_line.split("(")[0].strip()
                matched = any(
                    approved.lower() in std_name.lower() or std_name.lower() in approved.lower()
                    for approved in APPROVED_STANDARDS
                )
                if not matched and len(std_name) > 3:
                    i += 1
                    findings.append(Finding(
                        "INFO", f"I-NRM{i:02d}",
                        f"Standard `{std_name}` in frontmatter is not in the recognized catalog. "
                        f"Verify pertinence and add to catalog if valid.",
                        None
                    ))

    return findings


def audit_scope(content: str) -> list[Finding]:
    """Axis 3: Detects silent expansion of the MVP scope."""
    findings: list[Finding] = []
    b, w = 0, 0

    # — Screens outside the MVP index
    for match in re.finditer(r"\bSCR-([A-Z]+)-(\d+)\b", content):
        screen_id = match.group(0)
        if screen_id not in MVP_APPROVED_SCREENS:
            line_num = content[:match.start()].count("\n") + 1
            b += 1
            findings.append(Finding(
                "BLOCKER", f"B-SCP{b:02d}",
                f"Screen `{screen_id}` is not in the approved MVP screen index. "
                f"If it is a new screen, it must be approved via an explicit scope decision.",
                line_num
            ))

    # — Use cases outside the MVP index
    for match in re.finditer(r"\bUC-([A-Z]+)-(\d+)\b", content):
        uc_id = match.group(0)
        if uc_id not in MVP_APPROVED_UCS:
            line_num = content[:match.start()].count("\n") + 1
            b += 1
            findings.append(Finding(
                "BLOCKER", f"B-SCP{b:02d}",
                f"Use Case `{uc_id}` is not in the approved MVP UC index. "
                f"If it is a new use case, update the index with explicit approval.",
                line_num
            ))

    # — Roles no definidos en RBAC
    # Estrategia mejorada para evitar falsos positivos: buscar solo en columnas de tablas llamadas "Rol", "Roles" o "Actor"
    table_pattern = re.compile(r'(^\|.*\|\n(?:\|[-:\s|]+\|\n)(?:\|.*\|\n)*)', re.MULTILINE)
    for table_match in table_pattern.finditer(content):
        table_text = table_match.group(1)
        lines = table_text.strip().split('\n')
        if len(lines) < 3:
            continue
        
        headers = [h.strip().lower() for h in lines[0].strip('|').split('|')]
        # Search for the index of the roles column
        role_col_idx = -1
        for i, h in enumerate(headers):
            if re.search(r'\b(rol|roles|actor|actores)\b', h):
                role_col_idx = i
                break
                
        if role_col_idx == -1:
            continue
            
        # Extraer los datos de esa columna
        for row in lines[2:]:
            # Ignore empty rows
            if not row.strip():
                continue
            cells = [c.strip() for c in row.strip('|').split('|')]
            if role_col_idx < len(cells):
                cell = cells[role_col_idx]
                for candidate in re.split(r"[,]", cell):
                    candidate = candidate.strip().strip(".").strip()
                    if len(candidate) < 4 or len(candidate.split()) > 5:
                        continue
                    if re.match(r"^(All|Screen|Event|Target|Level|Source|State|Token|Value|Application|Symbol|Theme|Type|Layer|Technology|Use|Traceability)", candidate, re.IGNORECASE):
                        continue
                    
                    # Check against approved roles
                    if not any(
                        role.lower() in candidate.lower() or candidate.lower() in role.lower()
                        for role in APPROVED_ROLES
                    ):
                        w += 1
                        findings.append(Finding(
                            "WARNING", f"W-SCP{w:02d}",
                            f"Posible rol no definido en la Matriz RBAC: `{candidate}`. "
                            f"Verificar contra SCR-ADM-013 o si es un alias.",
                            None
                        ))

    return findings

# ---------------------------------------------------------------------------
# Generador de Informe
# ---------------------------------------------------------------------------

def generate_report(
    artifact_path: Path,
    all_findings: list[Finding],
    repo_root: Path,
) -> str:
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M")

    blockers = [f for f in all_findings if f.severity == "BLOCKER"]
    warnings = [f for f in all_findings if f.severity == "WARNING"]
    infos    = [f for f in all_findings if f.severity == "INFO"]

    if blockers:
        verdict_icon = "🔴"
        verdict_text = "BLOQUEADO — El artefacto NO debe integrarse sin resolver los BLOCKERs."
    elif warnings:
        verdict_icon = "⚠️"
        verdict_text = "CONDICIONAL — El artefacto puede integrarse tras revisar las advertencias."
    else:
        verdict_icon = "✅"
        verdict_text = "APPROVED — No critical findings."

    rel_path = artifact_path.relative_to(repo_root) if artifact_path.is_absolute() else artifact_path

    lines = [
        f"---",
        f"code: AUD-COHERENCE-{now.strftime('%Y%m%d')}-{artifact_path.stem[:30]}",
        f"date: {date_str}",
        f"artifact: {rel_path}",
        f"verdict: {verdict_text}",
        f"---",
        f"",
        f"# Informe de Coherencia — `{artifact_path.name}`",
        f"",
        f"**Audit Date:** {date_str}  ",
        f"**Artefacto:** `{rel_path}`  ",
        f"**Verdict:** {verdict_icon} {verdict_text}",
        f"",
        f"**Resumen:** {len(blockers)} BLOCKER | {len(warnings)} WARNING | {len(infos)} INFO",
        f"",
        f"---",
        f"",
    ]

    def format_findings(findings: list[Finding], header: str) -> list[str]:
        out = [f"## {header} ({len(findings)})", ""]
        if not findings:
            out.append("*Sin hallazgos.*")
            out.append("")
        for f in findings:
            loc = f" *(line {f.line})*" if f.line else ""
            out.append(f"- **[{f.code}]**{loc} {f.message}")
        out.append("")
        return out

    lines += format_findings(blockers, "🔴 BLOCKER")
    lines += format_findings(warnings, "⚠️ WARNING")
    lines += format_findings(infos,    "ℹ️ INFO")

    lines += [
        "---",
        "",
        "## Next Steps",
        "",
        "| Prioridad | Action |",
        "| :--- | :--- |",
    ]
    if blockers:
        lines.append("| 1. Critical | Resolve all BLOCKER findings before continuing |")
    if warnings:
        lines.append("| 2. Review | Evaluate the WARNINGs with the architect and document the decision |")
    if infos:
        lines.append("| 3. Optional | Verify INFOs and update catalogs if applicable |")
    if not all_findings:
        lines.append("| — | No action required |")

    lines += [
        "",
        "---",
        "",
        f"*Generated by: dteam-coherence-audit v1.0 — DTEAM AP5 SENA*",
    ]

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Subcomandos
# ---------------------------------------------------------------------------

def cmd_audit(args: argparse.Namespace, repo_root: Path) -> int:
    artifact_path = (repo_root / args.file).resolve()
    if not artifact_path.exists():
        print(f"[ERROR] Artifact not found: {artifact_path}", file=sys.stderr)
        return 1

    content = artifact_path.read_text(encoding="utf-8")
    print(f"[INFO] Auditing: {artifact_path.relative_to(repo_root)}")

    findings: list[Finding] = []
    findings += audit_traceability(content, repo_root)
    findings += audit_normative(content)
    findings += audit_scope(content)

    # Deduplicar por mensaje
    seen: set[str] = set()
    unique: list[Finding] = []
    for f in findings:
        if f.message not in seen:
            seen.add(f.message)
            unique.append(f)
    findings = unique

    report_text = generate_report(artifact_path, findings, repo_root)

    # Determine output path
    now = datetime.datetime.now()
    out_dir = repo_root.parent / "sena-evidence" / "00-Overview" / "Audits" / "Compliance"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"AUD-COHERENCE-{now.strftime('%Y%m%d')}-{artifact_path.stem[:30]}.md"
    out_file.write_text(report_text, encoding="utf-8")

    blockers = [f for f in findings if f.severity == "BLOCKER"]
    warnings = [f for f in findings if f.severity == "WARNING"]
    infos    = [f for f in findings if f.severity == "INFO"]

    print(f"[INFO] Findings: {len(blockers)} BLOCKER | {len(warnings)} WARNING | {len(infos)} INFO")
    print(f"[INFO] Report generated at: {out_file}")

    return 2 if blockers else 0


def cmd_check_refs(args: argparse.Namespace, repo_root: Path) -> int:
    artifact_path = (repo_root / args.file).resolve()
    if not artifact_path.exists():
        print(f"[ERROR] Artifact not found: {artifact_path}", file=sys.stderr)
        return 1
    content = artifact_path.read_text(encoding="utf-8")
    findings = audit_traceability(content, repo_root)
    blockers = [f for f in findings if f.severity == "BLOCKER"]
    for f in findings:
        loc = f" (line {f.line})" if f.line else ""
        print(f"[{f.severity}] [{f.code}]{loc} {f.message}")
    if not findings:
        print("[OK] All references are traceable.")
    return 2 if blockers else 0


def cmd_check_scope(args: argparse.Namespace, repo_root: Path) -> int:
    artifact_path = (repo_root / args.file).resolve()
    if not artifact_path.exists():
        print(f"[ERROR] Artifact not found: {artifact_path}", file=sys.stderr)
        return 1
    content = artifact_path.read_text(encoding="utf-8")
    findings = audit_scope(content)
    blockers = [f for f in findings if f.severity == "BLOCKER"]
    for f in findings:
        loc = f" (line {f.line})" if f.line else ""
        print(f"[{f.severity}] [{f.code}]{loc} {f.message}")
    if not findings:
        print("[OK] Scope within the approved MVP index.")
    return 2 if blockers else 0


def cmd_audit_all(args: argparse.Namespace, repo_root: Path) -> int:
    exclude_dirs = {".git", ".agents", "compliance", "scripts"}
    md_files = [
        p for p in repo_root.rglob("*.md")
        if not any(exc in p.parts for exc in exclude_dirs)
    ]

    all_artifact_findings: dict[str, list[Finding]] = {}
    total_blockers = 0

    for md_file in sorted(md_files):
        content = md_file.read_text(encoding="utf-8")
        findings: list[Finding] = []
        findings += audit_traceability(content, repo_root)
        findings += audit_normative(content)
        findings += audit_scope(content)
        # Dedup
        seen: set[str] = set()
        unique = [f for f in findings if not (f.message in seen or seen.add(f.message))]
        rel = str(md_file.relative_to(repo_root))
        all_artifact_findings[rel] = unique
        total_blockers += sum(1 for f in unique if f.severity == "BLOCKER")

    # Construir informe global
    now = datetime.datetime.now()
    lines = [
        f"---",
        f"code: AUD-FULL-REPO-{now.strftime('%Y%m%d')}",
        f"date: {now.strftime('%Y-%m-%d %H:%M')}",
        f"scope: Full Repository",
        f"---",
        f"",
        f"# Full Repository Audit — DTEAM",
        f"",
        f"**Date:** {now.strftime('%Y-%m-%d %H:%M')}  ",
        f"**Audited artifacts:** {len(md_files)}  ",
        f"**Total BLOCKERs:** {total_blockers}",
        f"",
        f"---",
        f"",
    ]

    for rel_path, findings in all_artifact_findings.items():
        if not findings:
            continue
        blockers = [f for f in findings if f.severity == "BLOCKER"]
        warnings = [f for f in findings if f.severity == "WARNING"]
        infos    = [f for f in findings if f.severity == "INFO"]
        verdict = "🔴" if blockers else ("⚠️" if warnings else "ℹ️")
        lines.append(f"## {verdict} `{rel_path}`")
        lines.append(f"*{len(blockers)} BLOCKER | {len(warnings)} WARNING | {len(infos)} INFO*")
        lines.append("")
        for f in findings:
            loc = f" *(line {f.line})*" if f.line else ""
            lines.append(f"- **[{f.severity}][{f.code}]**{loc} {f.message}")
        lines.append("")

    if all(not v for v in all_artifact_findings.values()):
        lines.append("✅ **No findings in any artifact.**")

    report_text = "\n".join(lines)

    out_path = (repo_root / args.output) if args.output else (repo_root.parent / "sena-evidence" / "00-Overview" / "Audits" / "Compliance" / f"AUD-FULL-REPO-{now.strftime('%Y%m%d')}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report_text, encoding="utf-8")
    print(f"[INFO] Full report generated at: {out_path}")
    return 2 if total_blockers > 0 else 0

# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="DTEAM Docs-as-Code Coherence Auditor v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="Full audit of an artifact")
    p_audit.add_argument("--file", required=True, help="Relative path to the artifact (from repo root)")

    p_refs = sub.add_parser("check-refs", help="Solo verificar trazabilidad de referencias")
    p_refs.add_argument("--file", required=True, help="Ruta relativa al artefacto")

    p_scope = sub.add_parser("check-scope", help="Solo verificar scope guard MVP")
    p_scope.add_argument("--file", required=True, help="Ruta relativa al artefacto")

    p_all = sub.add_parser("audit-all", help="Auditar todo el repositorio (modo CI)")
    p_all.add_argument("--output", default=None, help="Ruta del informe de salida")

    args = parser.parse_args()

    # Find repository root from CWD
    repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        print("[ERROR] Git repository root not found. "
              "Ejecutar desde dentro de adso-dteam-docs/.", file=sys.stderr)
        return 1

    dispatch = {
        "audit":       cmd_audit,
        "check-refs":  cmd_check_refs,
        "check-scope": cmd_check_scope,
        "audit-all":   cmd_audit_all,
    }
    return dispatch[args.command](args, repo_root)


if __name__ == "__main__":
    sys.exit(main())
