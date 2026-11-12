#!/usr/bin/env python3
"""
verify_markdown_links.py - Docs-as-Code Link & Anchor Verification Tool

Audits all Markdown files in the repository to guarantee:
1. Universal Relative Links: All internal links use valid relative paths.
2. Section Anchor Integrity: All '#anchor' fragments resolve to valid GFM heading slugs.
3. Zero Body Wikilinks: Obsidian-style wikilinks (`[[...]]` or `![[...]]`) are prohibited
   in document bodies (while safely preserving YAML frontmatter metadata).
4. Asset Verification: Linked assets (e.g. SVG, images, documents) exist on disk,
   with known planned stubs handled cleanly.

Usage:
    python3 scripts/verify_markdown_links.py [--root PATH] [-v|--verbose] [--strict-stubs]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

# Known planned stubs: architectural mockups and wireframes planned in roadmap
STUB_PATTERNS = [
    r"assets/SCR-.*-wireframe\.svg$",
    r"assets/SCR-VIS-.*\.svg$",
    r"views/DT-ARQ-.*\.drawio$",
]


def is_stub(path_str: str) -> bool:
    """Check if a missing file target matches an allowed planned stub pattern."""
    normalized = path_str.replace("\\", "/")
    for pattern in STUB_PATTERNS:
        if re.search(pattern, normalized):
            return True
    return False


def gfm_slug(text: str) -> str:
    """
    Generate a GitHub Flavored Markdown (GFM) anchor slug from heading text.
    
    Rules:
    - Downcase
    - Strip inline markdown formatting (links, bold, italics, code, HTML)
    - Remove punctuation (characters other than alphanumeric, space, hyphen, underscore)
    - Replace spaces with hyphens
    """
    # Remove markdown links: [foo](url) -> foo
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove markdown images: ![alt](url) -> alt
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    # Remove bold/italics with asterisks: ***text*** -> text, **text** -> text, *text* -> text
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    # Remove strikethrough
    text = re.sub(r"~~([^~]+)~~", r"\1", text)
    # Remove inline backticks: `code` -> code
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Lowercase
    text = text.strip().lower()
    # Remove any character not in [a-zA-Z0-9_ -]
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace whitespace sequences with hyphens
    text = re.sub(r"[\s]+", "-", text)
    return text


def extract_headings(file_path: Path) -> set[str]:
    """Extract all GFM heading slugs from a markdown file, accounting for duplicates."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Warning: Unable to read headings from {file_path}: {e}", file=sys.stderr)
        return set()

    # Strip YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    # Strip fenced code blocks
    content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)

    anchors = set()
    slug_counts: dict[str, int] = {}
    for line in content.splitlines():
        line = line.strip()
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            raw_title = m.group(2).strip()
            slug = gfm_slug(raw_title)
            if slug:
                if slug in slug_counts:
                    slug_counts[slug] += 1
                    anchors.add(f"{slug}-{slug_counts[slug]}")
                else:
                    slug_counts[slug] = 0
                    anchors.add(slug)
    return anchors


def find_markdown_files(root: Path) -> list[Path]:
    """Discover all non-ignored Markdown files in repository."""
    ignored_parts = {".git", ".venv", "node_modules", "temp", "__pycache__"}
    md_files = []
    for p in root.rglob("*.md"):
        rel_parts = p.relative_to(root).parts
        if any(part in ignored_parts or part.startswith(".") for part in rel_parts):
            continue
        md_files.append(p.resolve())
    return sorted(md_files)


def audit_repository(root: Path, verbose: bool = False, strict_stubs: bool = False) -> bool:
    """Run full link, anchor, and wikilink audit across the repository."""
    md_files = find_markdown_files(root)
    print(f"🔍 Discovered {len(md_files)} Markdown files under {root}")

    # Step 1: Pre-index headings for all markdown files
    file_anchors: dict[Path, set[str]] = {p: extract_headings(p) for p in md_files}

    body_wikilinks: list[tuple[Path, int, str]] = []
    broken_links: list[tuple[Path, str, str]] = []
    broken_anchors: list[tuple[Path, str, str, Path]] = []
    stub_references: list[tuple[Path, str]] = []
    frontmatter_wikilinks_count = 0
    total_links = 0

    wikilink_pattern = re.compile(r"(!?\[\[(.*?)\]\])")
    md_link_pattern = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")

    # Step 2: Audit each file
    for file_path in md_files:
        rel_src = file_path.relative_to(root)
        content = file_path.read_text(encoding="utf-8")

        # Parse frontmatter
        body = content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                body = parts[2]
                fm_matches = wikilink_pattern.findall(fm)
                frontmatter_wikilinks_count += len(fm_matches)

        # Strip fenced code blocks
        clean_body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
        # Strip inline code spans
        clean_body = re.sub(r"`[^`\n]+`", "", clean_body)

        # Check for prohibited body wikilinks
        for wm in wikilink_pattern.finditer(clean_body):
            # Calculate line number approximation
            line_no = clean_body[: wm.start()].count("\n") + 1
            body_wikilinks.append((rel_src, line_no, wm.group(1)))

        # Audit markdown links
        for lm in md_link_pattern.finditer(clean_body):
            total_links += 1
            url = lm.group(2).strip()

            # Ignore external protocols
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url) or url.startswith("mailto:") or url.startswith("tel:"):
                continue

            # Split path and anchor
            if "#" in url:
                target_url_path, anchor = url.split("#", 1)
            else:
                target_url_path, anchor = url, None

            target_url_path = unquote(target_url_path)

            if not target_url_path:
                resolved_file = file_path
            else:
                resolved_file = (file_path.parent / target_url_path).resolve()

            # Validate target file existence
            if not resolved_file.exists():
                if is_stub(target_url_path) or is_stub(str(resolved_file)):
                    stub_references.append((rel_src, url))
                    if strict_stubs:
                        broken_links.append((rel_src, url, f"Planned stub file missing: {resolved_file}"))
                    continue
                broken_links.append((rel_src, url, f"Target file not found: {resolved_file}"))
                continue

            # Validate anchor if target is a Markdown file
            if anchor and resolved_file in file_anchors:
                valid_anchors = file_anchors[resolved_file]
                norm_anchor = anchor.lower()
                if norm_anchor not in valid_anchors:
                    broken_anchors.append((rel_src, url, norm_anchor, resolved_file.relative_to(root)))

            if verbose:
                print(f"  [OK] {rel_src} -> {url}")

    # Step 3: Print summary report
    print("\n" + "=" * 70)
    print("📋 MARKDOWN LINK VERIFICATION REPORT")
    print("=" * 70)
    print(f"Files scanned:                  {len(md_files)}")
    print(f"Total links verified:           {total_links}")
    print(f"Frontmatter wikilinks (safe):   {frontmatter_wikilinks_count}")
    print(f"Planned stubs referenced:       {len(stub_references)}")
    print(f"Prohibited body wikilinks:      {len(body_wikilinks)}")
    print(f"Broken file links:              {len(broken_links)}")
    print(f"Broken section anchors:         {len(broken_anchors)}")
    print("=" * 70)

    # Detailed failures
    failed = False

    if body_wikilinks:
        failed = True
        print("\n❌ PROHIBITED BODY WIKILINKS FOUND:")
        for src, line_no, raw in body_wikilinks:
            print(f"  {src}:{line_no} -> {raw}")

    if broken_links:
        failed = True
        print("\n❌ BROKEN FILE TARGETS:")
        for src, url, err in broken_links:
            print(f"  {src} -> {url} ({err})")

    if broken_anchors:
        failed = True
        print("\n❌ BROKEN SECTION ANCHORS:")
        for src, url, anchor, target in broken_anchors:
            print(f"  {src} -> {url} [Anchor '{anchor}' not found in {target}]")

    if not failed:
        print("\n✅ ALL CHECKS PASSED: 100% universal relative links and anchor integrity.")
        return True
    else:
        print("\n❌ AUDIT FAILED: Errors must be resolved before merging.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify universal relative markdown links and anchor integrity in Docs-as-Code."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root path to audit (defaults to parent of scripts directory).",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Display all verified links in real time.",
    )
    parser.add_argument(
        "--strict-stubs",
        action="store_true",
        help="Treat known planned wireframe/diagram stubs as broken links.",
    )

    args = parser.parse_args()
    success = audit_repository(args.root, verbose=args.verbose, strict_stubs=args.strict_stubs)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
