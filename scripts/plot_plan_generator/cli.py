"""
Command-Line Interface (CLI) for Plot Plan Generation.
"""
import argparse
import sys
from pathlib import Path
from .builder import build_plot_plan
from .domain.validation import validate_layout, validate_svg
from .domain.process_safety import compute_bund_capacities


def main():
    parser = argparse.ArgumentParser(
        description="Generate industrial terminal General Arrangement (GA) SVG conforming to DT-UI-SVG-DOC-001 rev 2.0."
    )
    parser.add_argument(
        "output_path",
        type=Path,
        help="Mandatory target output SVG file or directory path (e.g., path/to/tfa_terminal_plot_plan.svg)"
    )
    parser.add_argument(
        "--theme",
        choices=["light", "dark", "tokens"],
        default="light",
        help="Color theme palette: 'light', 'dark', or 'tokens' (dynamic CSS variables conforming to Design System tokens)."
    )
    parser.add_argument(
        "--theme-file",
        type=Path,
        default=None,
        help="Path to custom JSON theme file overriding built-in palettes."
    )
    parser.add_argument(
        "--include-cad-tables",
        action="store_true",
        default=False,
        help="Include legacy CAD engineering tables, compass rose, and scale bar. Disabled by default for clean Digital Twin HMI."
    )
    parser.add_argument(
        "--include-grid-axes",
        action="store_true",
        default=False,
        help="Include coordinate grid axis bubble markers 1..9 and A..I. Disabled by default for clean Digital Twin HMI."
    )
    parser.add_argument(
        "--include-fire-radii",
        action="store_true",
        default=False,
        help="Include dashed fire monitor coverage throw circles. Disabled by default for clean Digital Twin HMI."
    )
    parser.add_argument(
        "--include-zone-badges",
        action="store_true",
        default=False,
        help="Include numbered zone bubbles 1..8. Disabled by default for clean Digital Twin HMI."
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        default=False,
        help="Run strict layout, process safety, and XML schema validation."
    )
    parser.add_argument(
        "--all-zooms",
        action="store_true",
        default=False,
        help="Also emit zoom-l2 and zoom-l3 SVGs beside the main file."
    )

    args = parser.parse_args()

    target = args.output_path
    if target.is_dir() or target.suffix != ".svg":
        target.mkdir(parents=True, exist_ok=True)
        out = target / "tfa_terminal_plot_plan.svg"
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        out = target

    # Generate main L1 plot plan
    svg_l1, meta = build_plot_plan(
        zoom="zoom-l1",
        theme=args.theme,
        theme_file=args.theme_file,
        include_cad_tables=args.include_cad_tables,
        include_grid_axes=args.include_grid_axes,
        include_fire_radii=args.include_fire_radii,
        include_zone_badges=args.include_zone_badges
    )
    out.write_text(svg_l1, encoding="utf-8")

    # Optional multi-zoom files
    if args.all_zooms:
        svg_l2, _ = build_plot_plan(
            zoom="zoom-l2", theme=args.theme, theme_file=args.theme_file,
            include_cad_tables=args.include_cad_tables,
            include_grid_axes=args.include_grid_axes,
            include_fire_radii=args.include_fire_radii,
            include_zone_badges=args.include_zone_badges
        )
        svg_l3, _ = build_plot_plan(
            zoom="zoom-l3", theme=args.theme, theme_file=args.theme_file,
            include_cad_tables=args.include_cad_tables,
            include_grid_axes=args.include_grid_axes,
            include_fire_radii=args.include_fire_radii,
            include_zone_badges=args.include_zone_badges
        )
        out.with_name(out.stem + "_l2.svg").write_text(svg_l2, encoding="utf-8")
        out.with_name(out.stem + "_l3.svg").write_text(svg_l3, encoding="utf-8")

    # Validation
    if args.validate:
        compute_bund_capacities()
        validate_layout(meta["pipe_net"], meta["stubs"])
        by, z2, z3, counts, size = validate_svg(out, is_dark=(args.theme in ("dark", "tokens")))
        print(f"Validated {out} ({size/1024:.0f} KB) — PASS")
        print("Interactive units :", {k_: len(v) for k_, v in by.items()})
        print("Elements per layer:", counts)
        print(f"Zoom-tagged elems : L2={z2}  L3={z3}")
    else:
        print(f"Wrote {out} ({len(svg_l1)/1024:.0f} KB) [theme={args.theme}, cad_tables={args.include_cad_tables}]")


if __name__ == "__main__":
    main()
