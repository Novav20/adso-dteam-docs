#!/usr/bin/env bash
# import_notion_backup.sh — Extracts Notion CSV exports into requirements/data.
#
# Usage:
#   ./scripts/import_notion_backup.sh
#   ./scripts/import_notion_backup.sh --dry-run
#   ./scripts/import_notion_backup.sh --keep-source
#   ./scripts/import_notion_backup.sh --backup-dir /path/to/backup
#
# Workflow:
#   1. Scans temp/ for .zip files (outer Notion export zips).
#   2. Extracts inner ZIP files when present.
#   3. Finds *_all.csv files recursively in either layout.
#   4. Renames based on content type mapping.
#   5. Copies to requirements/data/.
#   6. Cleans up all temporary files.

set -euo pipefail

DRY_RUN=false
KEEP_SOURCE=false

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
BACKUP_DIR="$SCRIPT_DIR/temp"
TARGET_DIR="$PROJECT_ROOT/requirements/data"

usage() {
    cat <<'USAGE'
Uso: import_notion_backup.sh [opciones]

Opciones:
  --dry-run                 Mostrar cambios sin copiar ni borrar ZIPs.
  --keep-source             Conservar los ZIP procesados como respaldo.
  --backup-dir RUTA         Sobrescribir el directorio de entrada.
  --target-dir RUTA         Sobrescribir el directorio de destino.
  -h, --help                Mostrar esta ayuda.
USAGE
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            ;;
        --keep-source)
            KEEP_SOURCE=true
            ;;
        --backup-dir|--target-dir)
            if [[ $# -lt 2 ]]; then
                echo "❌ Falta la ruta para $1" >&2
                exit 2
            fi
            if [[ "$1" == "--backup-dir" ]]; then
                BACKUP_DIR="$2"
            else
                TARGET_DIR="$2"
            fi
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "❌ Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
    shift
done

TEMP_DIR="$BACKUP_DIR/_import_tmp"

if $DRY_RUN; then
    echo "🧪 Dry-run mode: no files will be copied or deleted."
    echo ""
fi

# ── Validation ────────────────────────────────────────────────────────────────
if [[ ! -d "$BACKUP_DIR" ]]; then
    echo "❌ Directorio de backup no encontrado: $BACKUP_DIR"
    exit 1
fi

mkdir -p "$TARGET_DIR"

# Count outer zips
shopt -s nullglob
OUTER_ZIPS=("$BACKUP_DIR"/*.zip)
shopt -u nullglob

if [[ ${#OUTER_ZIPS[@]} -eq 0 ]]; then
    echo "⚠️  No se encontraron archivos .zip en $BACKUP_DIR"
    exit 0
fi

echo "📦 Encontrados ${#OUTER_ZIPS[@]} archivo(s) zip en temp/"
echo ""

# ── Mapping rules ─────────────────────────────────────────────────────────────
resolve_target_name() {
    local filename="$1"
    if [[ "$filename" == *"Actores y Roles"* || "$filename" == *"Actors"* ]]; then
        echo "actors.csv"
    elif [[ "$filename" == *"Objetos de Datos"* || "$filename" == *"Data Objects"* || "$filename" == *"I/O"* ]]; then
        echo "ios.csv"
    elif [[ "$filename" == *"Business Processes"* || "$filename" == *"Procesos"* ]]; then
        echo "processes.csv"
    elif [[ "$filename" == *"Requisitos Transversales"* || "$filename" == *"Transversal Requirements"* || "$filename" == *"Cross-cutting Requirements"* || "$filename" == *"NFR"* || "$filename" == *"TR"* ]]; then
        echo "transversal-requirements.csv"
    elif [[ "$filename" == *"SRS"* || "$filename" == *"Functional Requirements"* || "$filename" == *"Requirements"* ]]; then
        echo "srs.csv"
    elif [[ "$filename" == *"Historias de Usuario"* || "$filename" == *"User Stories"* || "$filename" == *"US"* ]]; then
        echo "user-stories.csv"
    elif [[ "$filename" == *"Acceptance Criteria"* || "$filename" == *"Acceptance Criteria"* || "$filename" == *"AC"* ]]; then
        echo "gherkin.csv"
    else
        echo ""
    fi
}

# ── Processing ────────────────────────────────────────────────────────────────
DEPLOYED=0
SKIPPED=0

cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

for outer_zip in "${OUTER_ZIPS[@]}"; do
    outer_name="$(basename "$outer_zip")"
    archive_deployed=0
    echo "─── Procesando: $outer_name"

    # Step 1: Extract outer zip → inner Part-N.zip(s)
    rm -rf "$TEMP_DIR"
    mkdir -p "$TEMP_DIR/outer" "$TEMP_DIR/inner"
    unzip -q -o "$outer_zip" -d "$TEMP_DIR/outer"

    # Step 2: Find and extract inner ZIPs when this export has them.
    mapfile -d '' INNER_ZIPS < <(find "$TEMP_DIR/outer" -type f -name '*.zip' -print0)
    for inner_zip in "${INNER_ZIPS[@]}"; do
        unzip -q -o "$inner_zip" -d "$TEMP_DIR/inner"
    done

    # Step 3: Find *_all.csv files in direct or nested Notion export layouts.
    mapfile -d '' ALL_CSVS < <(find "$TEMP_DIR/inner" -type f -name '*_all.csv' -print0)
    mapfile -d '' OUTER_CSVS < <(find "$TEMP_DIR/outer" -type f -name '*_all.csv' -print0)
    ALL_CSVS+=("${OUTER_CSVS[@]}")

    if [[ ${#ALL_CSVS[@]} -eq 0 ]]; then
        echo "  ⚠️  No se encontraron archivos *_all.csv. Saltando."
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    for csv_file in "${ALL_CSVS[@]}"; do
        csv_basename="$(basename "$csv_file")"
        target_name="$(resolve_target_name "$csv_basename")"

        if [[ -z "$target_name" ]]; then
            echo "  ⚠️  No se reconoce tipo para: $csv_basename — Saltando."
            SKIPPED=$((SKIPPED + 1))
            continue
        fi

        target_path="$TARGET_DIR/$target_name"
        echo "  📄 $csv_basename → $target_name"

        if $DRY_RUN; then
            echo "     🧪 (dry-run) Would copy to: $target_path"
        else
            cp "$csv_file" "$target_path"
            echo "     ✅ Copiado a: $target_path"
        fi
        DEPLOYED=$((DEPLOYED + 1))
        archive_deployed=$((archive_deployed + 1))
    done

    if $DRY_RUN; then
        echo "  🧪 (dry-run) Would preserve origin: $outer_zip"
    elif [[ $archive_deployed -gt 0 && "$KEEP_SOURCE" == false ]]; then
        rm "$outer_zip"
        echo "  ♻️  Origen eliminado: $outer_name"
    else
        echo "  📦 Origen conservado: $outer_name"
    fi

    echo ""
done

# ── Summary ───────────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════"
echo "📊 Resumen:"
echo "   Desplegados: $DEPLOYED"
echo "   Saltados:    $SKIPPED"
if $DRY_RUN; then
    echo "   Modo:        dry-run"
else
    echo "   Modo:        write"
fi
echo "═══════════════════════════════════════════"
