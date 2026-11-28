#!/usr/bin/env python3
"""Extracts Notion CSV exports from zip archives into requirements/data.

Cross-platform (Windows & Linux) replacement for the bash-only implementation.

Usage:
    python scripts/import_notion_backup.py
    python scripts/import_notion_backup.py --dry-run
    python scripts/import_notion_backup.py --keep-source
    python scripts/import_notion_backup.py --backup-dir /path/to/backup
"""

from __future__ import annotations

import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path

MAPPING_RULES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("Actores y Roles", "Actors"), "actors.csv"),
    (("Objetos de Datos", "Data Objects", "I/O"), "ios.csv"),
    (("Business Processes", "Procesos"), "processes.csv"),
    (
        (
            "Requisitos Transversales",
            "Transversal Requirements",
            "Cross-cutting Requirements",
            "NFR",
            "TR",
        ),
        "transversal-requirements.csv",
    ),
    (("SRS", "Functional Requirements", "Requirements"), "srs.csv"),
    (("Historias de Usuario", "User Stories", "US"), "user-stories.csv"),
    (("Acceptance Criteria", "AC"), "gherkin.csv"),
)


def resolve_target_name(filename: str) -> str | None:
    """Map a Notion *_all.csv filename to its canonical target CSV name."""
    for keywords, target in MAPPING_RULES:
        if any(kw in filename for kw in keywords):
            return target
    return None


def extract_zip(zip_path: Path, dest_dir: Path) -> None:
    """Extract a zip archive safely into dest_dir."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest_dir)


def process_backups(
    backup_dir: Path,
    target_dir: Path,
    dry_run: bool = False,
    keep_source: bool = False,
) -> tuple[int, int]:
    """Process all outer Notion export zip archives in backup_dir."""
    if not backup_dir.is_dir():
        raise FileNotFoundError(f"Backup directory not found: {backup_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)
    outer_zips = sorted(backup_dir.glob("*.zip"))

    if not outer_zips:
        print(f"No .zip files found in {backup_dir}")
        return 0, 0

    print(f"Found {len(outer_zips)} zip archive(s) in {backup_dir.name}/\n")

    deployed = 0
    skipped = 0

    for outer_zip in outer_zips:
        archive_deployed = 0
        print(f"--- Processing: {outer_zip.name}")

        with tempfile.TemporaryDirectory(prefix="notion_import_") as tmp:
            tmp_path = Path(tmp)
            outer_dir = tmp_path / "outer"
            inner_dir = tmp_path / "inner"
            outer_dir.mkdir()
            inner_dir.mkdir()

            extract_zip(outer_zip, outer_dir)

            for inner_zip in sorted(outer_dir.rglob("*.zip")):
                extract_zip(inner_zip, inner_dir)

            all_csvs = sorted(inner_dir.rglob("*_all.csv")) + sorted(
                outer_dir.rglob("*_all.csv")
            )

            if not all_csvs:
                print("  WARN: No *_all.csv files found. Skipping.")
                skipped += 1
                continue

            for csv_file in all_csvs:
                target_name = resolve_target_name(csv_file.name)
                if not target_name:
                    print(f"  WARN: Unrecognized type for {csv_file.name} -- Skipping.")
                    skipped += 1
                    continue

                target_path = target_dir / target_name
                print(f"  {csv_file.name} -> {target_name}")

                if dry_run:
                    print(f"    (dry-run) Would copy to: {target_path}")
                else:
                    shutil.copy2(csv_file, target_path)
                    print(f"    Copied to: {target_path}")

                deployed += 1
                archive_deployed += 1

        if dry_run:
            print(f"  (dry-run) Would preserve source: {outer_zip.name}")
        elif archive_deployed > 0 and not keep_source:
            outer_zip.unlink()
            print(f"  Removed source archive: {outer_zip.name}")
        else:
            print(f"  Preserved source archive: {outer_zip.name}")
        print()

    print("===========================================")
    print("Summary:")
    print(f"  Deployed: {deployed}")
    print(f"  Skipped:  {skipped}")
    return deployed, skipped


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent

    parser = argparse.ArgumentParser(
        description="Extract Notion CSV exports into requirements/data."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without copying or deleting zip archives.",
    )
    parser.add_argument(
        "--keep-source",
        action="store_true",
        help="Preserve processed zip archives instead of deleting them.",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=script_dir / "temp",
        help="Override input backup directory (default: scripts/temp).",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=project_root / "requirements" / "data",
        help="Override target data directory (default: requirements/data).",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("Dry-run mode: no files will be copied or deleted.\n")

    process_backups(
        backup_dir=args.backup_dir,
        target_dir=args.target_dir,
        dry_run=args.dry_run,
        keep_source=args.keep_source,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
