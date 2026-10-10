"""
SVG Document Assembly and Orchestration Coordinator.
Combines all 7 standard layers, injects MOC metadata, styles, and SVG defs.
"""
from .config import W, H, M_PER_UNIT, LIGHT_PALETTE, THEMES, load_theme_palette
from .layers.civil import build_civil_layer
from .layers.mechanical import build_mechanical_layer
from .layers.piping import build_piping_layer
from .layers.fire import build_fire_layer
from .layers.annotation import build_annotation_layer


def format_layer(lid, cls, items):
    """Wraps elements inside a standard SVG group layer."""
    body = "\n".join(i for i in items if i)
    return f'<g id="{lid}" class="{cls}">\n{body}\n</g>' if body else f'<g id="{lid}" class="{cls}"/>'


def build_plot_plan(zoom="zoom-l1", palette=None, theme="light", theme_file=None, include_cad_tables=False):
    """
    Builds the complete SVG plot plan.
    
    Args:
        zoom: 'zoom-l1', 'zoom-l2', or 'zoom-l3'
        palette: Palette instance. If None, resolved from theme.
        theme: 'light' or 'dark'
        theme_file: Optional path to external themes JSON file.
        include_cad_tables: whether to include title block, bund data, legends (default False)
    """
    if palette is None:
        palette = load_theme_palette(theme, theme_file=theme_file)

    # 1. Generate Layers
    CIV, gate_u, gatehouses, wbc = build_civil_layer(palette)
    MEC = build_mechanical_layer(palette)
    INS = []  # Reserved for instrumentation / transmitters
    PIP, pipe_net, stubs = build_piping_layer(palette)
    FIR, hyd, fm_list, nearest_main = build_fire_layer(palette)
    HAZ = []  # Reserved for electrical hazardous zones
    ANN = build_annotation_layer(
        palette, gate_u, gatehouses, wbc, include_cad_tables=include_cad_tables
    )

    # 2. Defs and Styles
    style = f"""
.dt-canvas {{ font-family: Arial, Helvetica, sans-serif; background: {palette.CANVAS_BG}; }}
/* ISA-101 progressive disclosure */
.zoom-l1 .dt-zoom-l2, .zoom-l1 .dt-zoom-l3, .zoom-l2 .dt-zoom-l3 {{ display: none !important; }}
.dt-interactive {{ cursor: pointer; }}
.dt-interactive:hover {{ opacity: 0.85; }}
"""
    defs = f"""
<pattern id="hatch-concrete" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="6" stroke="{palette.MID}" stroke-width="1"/>
</pattern>
<pattern id="hatch-light" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
<line x1="0" y1="0" x2="0" y2="5" stroke="{palette.FAINT}" stroke-width="0.6"/>
</pattern>
"""

    # 3. Assemble Root Document
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg viewBox="0 0 {W} {H}" class="dt-canvas {zoom}" xmlns="http://www.w3.org/2000/svg" '
        f'data-moc-id="MOC-2026-0042" data-rev-number="2.0" '
        f'data-checksum-sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" '
        f'data-scale-ratio="{M_PER_UNIT}" data-units="meters">',
        "<title>General Arrangement Plot Plan — Irregular-site Bulk Liquid Hydrocarbon Terminal (DT-UI-SVG-DOC-001)</title>",
        "<desc>Irregular plot traced from a reference survey; 1 SVG unit = 0.2 m. Layers per AIA CAD / ISO 13567; "
        "ISA-101 semantic zoom classes dt-zoom-l2 / dt-zoom-l3; ISO 14224 data binding on equipment.</desc>",
        f"<defs>{defs}</defs>",
        f"<style>{style}</style>",
        format_layer("L-CIVL-BOTM", "dt-layer-civil-botm", CIV),
        format_layer("L-MECH-EQPM", "dt-layer-mech-eqpm", MEC),
        format_layer("L-INSP-INST", "dt-layer-insp-inst", INS),
        format_layer("L-PIPE-PROC", "dt-layer-pipe-proc", PIP),
        format_layer("L-FIRE-PROT", "dt-layer-fire-prot", FIR),
        format_layer("L-ELEC-HAZ", "dt-layer-elec-haz", HAZ),
        format_layer("L-ANNO-TEXT", "dt-layer-anno-text", ANN),
        "</svg>"
    ]
    svg_content = "\n".join(parts)
    meta = {
        "pipe_net": pipe_net,
        "stubs": stubs,
        "hyd": hyd,
        "fm_list": fm_list,
        "gate_u": gate_u,
        "CIV": CIV,
        "MEC": MEC,
        "PIP": PIP,
        "FIR": FIR,
        "ANN": ANN
    }
    return svg_content, meta
