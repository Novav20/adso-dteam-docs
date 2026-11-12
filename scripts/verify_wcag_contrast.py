#!/usr/bin/env python3
"""
WCAG 2.1 Contrast Ratio Verification Script
Project: DTEAM HPHMI Design System (DT-UI-DS-DOC-001)
Audit ID: AUD-WCAG-ISO-2026-002 (A-P02 Audit Verification)
"""

import sys

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Convert hex string (e.g., '#D8DBE0') to RGB integer tuple."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def linearize_channel(c_8bit: int) -> float:
    """Linearize sRGB channel according to W3C WCAG 2.1 formula."""
    c_srgb = c_8bit / 255.0
    if c_srgb <= 0.04045:
        return c_srgb / 12.92
    else:
        return ((c_srgb + 0.055) / 1.055) ** 2.4

def calculate_relative_luminance(hex_str: str) -> float:
    """Calculate relative luminance (L) of a color hex string."""
    r, g, b = hex_to_rgb(hex_str)
    r_lin = linearize_channel(r)
    g_lin = linearize_channel(g)
    b_lin = linearize_channel(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

def calculate_contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate contrast ratio between two hex colors."""
    l1 = calculate_relative_luminance(hex1)
    l2 = calculate_relative_luminance(hex2)
    l_light = max(l1, l2)
    l_dark = min(l1, l2)
    return (l_light + 0.05) / (l_dark + 0.05)


def main():
    print("=========================================================================================")
    print("           WCAG 2.1 / ISO 9241-110 CONTRAST RATIO AUDIT VERIFICATION SCRIPT              ")
    print("=========================================================================================")
    print()

    # Define test pairs from Table 1 of A-P02 Audit Report
    test_pairs = [
        # Light Theme on Canvas (#D8DBE0)
        {"theme": "Light", "bg_name": "Canvas", "bg_hex": "#D8DBE0", "fg_name": "text-primary", "fg_hex": "#111827", "target": 4.5, "type": "Std Text"},
        {"theme": "Light", "bg_name": "Canvas", "bg_hex": "#D8DBE0", "fg_name": "text-body", "fg_hex": "#1F2937", "target": 4.5, "type": "Std Text"},
        {"theme": "Light", "bg_name": "Canvas", "bg_hex": "#D8DBE0", "fg_name": "text-muted", "fg_hex": "#4B5563", "target": 4.5, "type": "Std Text"},
        {"theme": "Light", "bg_name": "Canvas", "bg_hex": "#D8DBE0", "fg_name": "alarm-critical", "fg_hex": "#E63946", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Light", "bg_name": "Canvas", "bg_hex": "#D8DBE0", "fg_name": "alarm-warning", "fg_hex": "#D97706", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Light", "bg_name": "Canvas", "bg_hex": "#D8DBE0", "fg_name": "state-info", "fg_hex": "#2563EB", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Light", "bg_name": "Canvas", "bg_hex": "#D8DBE0", "fg_name": "state-success", "fg_hex": "#0D9488", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Light", "bg_name": "Canvas", "bg_hex": "#D8DBE0", "fg_name": "border-subtle", "fg_hex": "#B8C0CC", "target": 3.0, "type": "UI/Graph*"},
        {"theme": "Light", "bg_name": "Canvas", "bg_hex": "#D8DBE0", "fg_name": "border-focus", "fg_hex": "#6B7280", "target": 3.0, "type": "UI/Graph"},

        # Light Theme on Surface Card (#F4F5F7)
        {"theme": "Light", "bg_name": "Card", "bg_hex": "#F4F5F7", "fg_name": "text-primary", "fg_hex": "#111827", "target": 4.5, "type": "Std Text"},
        {"theme": "Light", "bg_name": "Card", "bg_hex": "#F4F5F7", "fg_name": "text-body", "fg_hex": "#1F2937", "target": 4.5, "type": "Std Text"},
        {"theme": "Light", "bg_name": "Card", "bg_hex": "#F4F5F7", "fg_name": "text-muted", "fg_hex": "#4B5563", "target": 4.5, "type": "Std Text"},
        {"theme": "Light", "bg_name": "Card", "bg_hex": "#F4F5F7", "fg_name": "alarm-critical", "fg_hex": "#E63946", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Light", "bg_name": "Card", "bg_hex": "#F4F5F7", "fg_name": "alarm-warning", "fg_hex": "#D97706", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Light", "bg_name": "Card", "bg_hex": "#F4F5F7", "fg_name": "state-info", "fg_hex": "#2563EB", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Light", "bg_name": "Card", "bg_hex": "#F4F5F7", "fg_name": "state-success", "fg_hex": "#0D9488", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Light", "bg_name": "Card", "bg_hex": "#F4F5F7", "fg_name": "border-subtle", "fg_hex": "#B8C0CC", "target": 3.0, "type": "UI/Graph*"},
        {"theme": "Light", "bg_name": "Card", "bg_hex": "#F4F5F7", "fg_name": "border-focus", "fg_hex": "#6B7280", "target": 3.0, "type": "UI/Graph"},

        # Dark Theme on Canvas (#16191F)
        {"theme": "Dark", "bg_name": "Canvas", "bg_hex": "#16191F", "fg_name": "text-primary", "fg_hex": "#FDFEFE", "target": 4.5, "type": "Std Text"},
        {"theme": "Dark", "bg_name": "Canvas", "bg_hex": "#16191F", "fg_name": "text-body", "fg_hex": "#C2CBD6", "target": 4.5, "type": "Std Text"},
        {"theme": "Dark", "bg_name": "Canvas", "bg_hex": "#16191F", "fg_name": "text-muted", "fg_hex": "#7E8B9B", "target": 4.5, "type": "Std Text"},
        {"theme": "Dark", "bg_name": "Canvas", "bg_hex": "#16191F", "fg_name": "alarm-critical", "fg_hex": "#E63946", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Dark", "bg_name": "Canvas", "bg_hex": "#16191F", "fg_name": "alarm-warning", "fg_hex": "#F4A261", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Dark", "bg_name": "Canvas", "bg_hex": "#16191F", "fg_name": "state-info", "fg_hex": "#457B9D", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Dark", "bg_name": "Canvas", "bg_hex": "#16191F", "fg_name": "state-success", "fg_hex": "#2A9D8F", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Dark", "bg_name": "Canvas", "bg_hex": "#16191F", "fg_name": "border-subtle", "fg_hex": "#3A4154", "target": 3.0, "type": "UI/Graph*"},
        {"theme": "Dark", "bg_name": "Canvas", "bg_hex": "#16191F", "fg_name": "border-focus", "fg_hex": "#5C667A", "target": 3.0, "type": "UI/Graph"},

        # Dark Theme on Surface Card (#2A2F3D)
        {"theme": "Dark", "bg_name": "Card", "bg_hex": "#2A2F3D", "fg_name": "text-primary", "fg_hex": "#FDFEFE", "target": 4.5, "type": "Std Text"},
        {"theme": "Dark", "bg_name": "Card", "bg_hex": "#2A2F3D", "fg_name": "text-body", "fg_hex": "#C2CBD6", "target": 4.5, "type": "Std Text"},
        {"theme": "Dark", "bg_name": "Card", "bg_hex": "#2A2F3D", "fg_name": "text-muted", "fg_hex": "#7E8B9B", "target": 4.5, "type": "Std Text"},
        {"theme": "Dark", "bg_name": "Card", "bg_hex": "#2A2F3D", "fg_name": "alarm-critical", "fg_hex": "#E63946", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Dark", "bg_name": "Card", "bg_hex": "#2A2F3D", "fg_name": "alarm-warning", "fg_hex": "#F4A261", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Dark", "bg_name": "Card", "bg_hex": "#2A2F3D", "fg_name": "state-info", "fg_hex": "#457B9D", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Dark", "bg_name": "Card", "bg_hex": "#2A2F3D", "fg_name": "state-success", "fg_hex": "#2A9D8F", "target": 3.0, "type": "UI/Graph"},
        {"theme": "Dark", "bg_name": "Card", "bg_hex": "#2A2F3D", "fg_name": "border-subtle", "fg_hex": "#3A4154", "target": 3.0, "type": "UI/Graph*"},
        {"theme": "Dark", "bg_name": "Card", "bg_hex": "#2A2F3D", "fg_name": "border-focus", "fg_hex": "#5C667A", "target": 3.0, "type": "UI/Graph"},
    ]

    print(f"{'Theme':<6} | {'BG Name':<7} | {'BG Hex':<7} | {'FG Token':<14} | {'FG Hex':<7} | {'Calc Ratio':<10} | {'Target':<8} | {'Status':<10}")
    print("-" * 95)

    passed_count = 0
    failed_count = 0

    for item in test_pairs:
        cr = calculate_contrast_ratio(item["bg_hex"], item["fg_hex"])
        status = "MEETS" if cr >= item["target"] else "FAILS"
        if status == "MEETS":
            passed_count += 1
            status_str = "\033[92mMEETS\033[0m" if sys.stdout.isatty() else "MEETS"
        else:
            failed_count += 1
            status_str = "\033[91mFAILS\033[0m" if sys.stdout.isatty() else "FAILS"

        print(f"{item['theme']:<6} | {item['bg_name']:<7} | {item['bg_hex']:<7} | {item['fg_name']:<14} | {item['fg_hex']:<7} | {cr:6.2f}:1    | {item['target']:3.1f}:1 ({item['type'][:3]}) | {status_str}")

    print("-" * 95)
    print(f"Summary: Total Tested: {len(test_pairs)} | Passed: {passed_count} | Failed: {failed_count}")
    print()

    # Re-engineering Verification for 5 Failure Recommendations
    print("=========================================================================================")
    print("               VERIFICATION OF RE-ENGINEERED PROPOSED ALTERNATIVES                       ")
    print("=========================================================================================")
    print()

    reengineering_cases = [
        {"id": 1, "desc": "Light Theme alarm-warning on Canvas", "bg": "#D8DBE0", "old_fg": "#D97706", "new_fg": "#AC5E04", "target": 3.0},
        {"id": 2, "desc": "Light Theme state-success on Canvas", "bg": "#D8DBE0", "old_fg": "#0D9488", "new_fg": "#0B857A", "target": 3.0},
        {"id": 3, "desc": "Dark Theme text-muted on Card", "bg": "#2A2F3D", "old_fg": "#7E8B9B", "new_fg": "#8A98AA", "target": 4.5},
        {"id": 4, "desc": "Dark Theme state-info on Card", "bg": "#2A2F3D", "old_fg": "#457B9D", "new_fg": "#4881A4", "target": 3.0},
        {"id": 5, "desc": "Dark Theme border-focus on Card", "bg": "#2A2F3D", "old_fg": "#5C667A", "new_fg": "#6E7A92", "target": 3.0},
    ]

    print(f"{'#':<2} | {'Description':<36} | {'BG Hex':<7} | {'Old Hex':<7} | {'Old Ratio':<9} | {'New Hex':<7} | {'New Ratio':<9} | {'Verdict':<8}")
    print("-" * 98)

    all_reengineered_pass = True
    for case in reengineering_cases:
        old_cr = calculate_contrast_ratio(case["bg"], case["old_fg"])
        new_cr = calculate_contrast_ratio(case["bg"], case["new_fg"])
        passes = new_cr >= case["target"]
        if not passes:
            all_reengineered_pass = False
        verdict_str = "PASS" if passes else "FAIL"
        if sys.stdout.isatty():
            verdict_str = f"\033[92m{verdict_str}\033[0m" if passes else f"\033[91m{verdict_str}\033[0m"

        print(f"{case['id']:<2} | {case['desc']:<36} | {case['bg']:<7} | {case['old_fg']:<7} | {old_cr:5.2f}:1   | {case['new_fg']:<7} | {new_cr:5.2f}:1   | {verdict_str}")

    print("-" * 98)
    if all_reengineered_pass:
        print("RESULT: ALL RE-ENGINEERED PROPOSED ALTERNATIVES ARE MATHEMATICALLY CONFIRMED COMPLIANT!")
    else:
        print("RESULT: SOME PROPOSED ALTERNATIVES STILL FAIL. REVISION NEEDED.")
    print("=========================================================================================")

if __name__ == "__main__":
    main()
