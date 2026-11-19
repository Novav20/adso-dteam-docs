#!/usr/bin/env python3
"""
WCAG 2.1 Contrast Ratio Verification Script
Project: DTEAM HPHMI Design System (DT-UI-DS-DOC-001)
Dynamically parses ui-ux/assets/tokens.css (:root and [data-theme="dark"]),
resolves var(--dt-...) references to hex, and fails non-zero if any active
semantic pair breaches WCAG 2.1 AA thresholds.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS_CSS = ROOT / "ui-ux" / "assets" / "tokens.css"


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Convert hex string (e.g., '#D8DBE0') to RGB integer tuple."""
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def linearize_channel(c_8bit: int) -> float:
    """Linearize sRGB channel according to W3C WCAG 2.1 formula."""
    c_srgb = c_8bit / 255.0
    if c_srgb <= 0.04045:
        return c_srgb / 12.92
    return ((c_srgb + 0.055) / 1.055) ** 2.4


def calculate_relative_luminance(hex_str: str) -> float:
    """Calculate relative luminance (L) of a color hex string."""
    r, g, b = hex_to_rgb(hex_str)
    return 0.2126 * linearize_channel(r) + 0.7152 * linearize_channel(g) + 0.0722 * linearize_channel(b)


def calculate_contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate contrast ratio between two hex colors."""
    l1 = calculate_relative_luminance(hex1)
    l2 = calculate_relative_luminance(hex2)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def parse_css_vars(css_text: str) -> tuple[dict[str, str], dict[str, str]]:
    """Parse :root (light) and [data-theme=\"dark\"] variable maps and resolve to hex."""
    root_match = re.search(r":root\s*\{(.*?)\n\}", css_text, re.DOTALL)
    dark_match = re.search(r'\[data-theme="dark"\]\s*\{(.*?)\n\}', css_text, re.DOTALL)
    if not root_match or not dark_match:
        raise ValueError("Could not locate :root or [data-theme=\"dark\"] blocks in tokens.css")

    def extract_block(block: str) -> dict[str, str]:
        vars_map: dict[str, str] = {}
        for m in re.finditer(r"^\s*(--dt-[a-z0-9-]+)\s*:\s*([^;]+);", block, re.MULTILINE):
            vars_map[m.group(1)] = m.group(2).strip()
        return vars_map

    light_raw = extract_block(root_match.group(1))
    dark_raw = {**light_raw, **extract_block(dark_match.group(1))}

    def resolve(table: dict[str, str], token: str, depth: int = 0) -> str:
        if depth > 6:
            raise ValueError(f"Circular token reference: {token}")
        val = table[token]
        if re.fullmatch(r"#[0-9A-Fa-f]{6}", val):
            return val.upper()
        ref = re.fullmatch(r"var\((--dt-[a-z0-9-]+)\)", val)
        if ref:
            return resolve(table, ref.group(1), depth + 1)
        return val

    light_resolved = {k: resolve(light_raw, k) for k in light_raw if k.startswith("--dt-color-") or k.startswith("--dt-primitive-")}
    dark_resolved = {k: resolve(dark_raw, k) for k in dark_raw if k.startswith("--dt-color-") or k.startswith("--dt-primitive-")}
    return light_resolved, dark_resolved


def main() -> int:
    if not TOKENS_CSS.exists():
        print(f"[ERROR] tokens.css not found at {TOKENS_CSS}", file=sys.stderr)
        return 1

    css_text = TOKENS_CSS.read_text(encoding="utf-8")
    light_tokens, dark_tokens = parse_css_vars(css_text)

    surfaces = [
        ("Canvas", "--dt-color-bg-canvas"),
        ("Base", "--dt-color-surface-base"),
        ("Card", "--dt-color-surface-card"),
    ]
    fg_checks = [
        ("--dt-color-text-primary", 4.5, "Std Text"),
        ("--dt-color-text-body", 4.5, "Std Text"),
        ("--dt-color-text-muted", 4.5, "Std Text"),
        ("--dt-color-alarm-critical", 3.0, "UI/Graph"),
        ("--dt-color-alarm-warning", 3.0, "UI/Graph"),
        ("--dt-color-state-info", 3.0, "UI/Graph"),
        ("--dt-color-state-success", 3.0, "UI/Graph"),
        ("--dt-color-border-focus", 3.0, "UI/Graph"),
    ]

    print("===============================================================================================")
    print("        WCAG 2.1 / ISO 9241-110 DYNAMIC CONTRAST AUDIT (Source: ui-ux/assets/tokens.css)       ")
    print("===============================================================================================")
    print(f"{'Theme':<6} | {'BG Token':<24} | {'BG Hex':<7} | {'FG Token':<27} | {'FG Hex':<7} | {'Ratio':<8} | {'Target':<6} | {'Status'}")
    print("-" * 105)

    failures = 0
    tested = 0

    for theme_name, token_map in [("Light", light_tokens), ("Dark", dark_tokens)]:
        for bg_label, bg_tok in surfaces:
            bg_hex = token_map[bg_tok]
            for fg_tok, target, _kind in fg_checks:
                fg_hex = token_map[fg_tok]
                cr = calculate_contrast_ratio(bg_hex, fg_hex)
                tested += 1
                ok = cr >= target
                if not ok:
                    failures += 1
                status = "PASS" if ok else "FAIL"
                print(f"{theme_name:<6} | {bg_label:<24} | {bg_hex:<7} | {fg_tok:<27} | {fg_hex:<7} | {cr:5.2f}:1 | {target:3.1f}:1 | {status}")

        # MAI badge text contrast checks
        for fg_tok, bg_tok, target in [
            ("--dt-color-alarm-text-critical", "--dt-color-alarm-critical", 3.0),
            ("--dt-color-alarm-text-warning", "--dt-color-alarm-warning", 4.5),
        ]:
            fg_hex = token_map[fg_tok]
            bg_hex = token_map[bg_tok]
            cr = calculate_contrast_ratio(bg_hex, fg_hex)
            tested += 1
            ok = cr >= target
            if not ok:
                failures += 1
            status = "PASS" if ok else "FAIL"
            print(f"{theme_name:<6} | {bg_tok:<24} | {bg_hex:<7} | {fg_tok:<27} | {fg_hex:<7} | {cr:5.2f}:1 | {target:3.1f}:1 | {status}")

    print("-" * 105)
    print(f"Summary: Tested={tested} | Passed={tested - failures} | Failed={failures}")
    return 1 if failures > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
