"""
Annotation & Text Layer (L-ANNO-TEXT) generator.
Includes coordinate grid bubbles, tank tags, zone badges, equipment tags,
dimension lines, compass rose, scale bar, spatial calibration vector,
and optional CAD engineering tables (title block, bund data, building key, legend).
"""
import math
from ..config import W, H, M_PER_UNIT, K, ROT, GRID_DEG, ZL2, ZL3
from ..core.geometry import UVu, P, poly_area
from ..core.svg_primitives import circle, line, rect, text, polyg, G, n
from ..domain.plant_data import (
    ALL_TANKS, ZONES, PUMP_TAGS, PUMP_X0, PUMP_PITCH, BAY_X, BAY_W,
    BLDG, BLDG_INFO, BASIN, GATES, YARD_PX, LANE_V, TKS, BND,
    PF, GF, MF
)
from ..domain.process_safety import compute_bund_capacities, m2


BLDG_SHORT = {
    "MCR": "MCR", "FAR": "FAR", "HV SUB": "HV SUB", "MCC-1": "MCC-1",
    "MCC-2": "MCC-2", "MCC-3": "MCC-3", "WH-01": "WH-01", "WH-02": "WH-02",
    "FW PUMP HOUSE": "FWPH"
}


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def dim_uv(a, b, label, palette):
    (x1, y1), (x2, y2) = UVu(*a), UVu(*b)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return G([line(x1, y1, x2, y2, s=palette.INK, w=0.6),
              circle(x1, y1, 1.6, f=palette.INK),
              circle(x2, y2, 1.6, f=palette.INK),
              text(mx, my - 4, label, size=6.5, anchor="middle", fill=palette.INK)], c=ZL2)


def gap_m(t1, t2):
    return (math.hypot(t1[1] - t2[1], t1[2] - t2[2]) - t1[3] - t2[3]) * K * M_PER_UNIT


def nf(v):
    return f"{v:,.0f}"


def build_annotation_layer(palette, gate_u, gatehouses, wbc, include_cad_tables=False):
    """Assembles all textual annotations, grid, compass, and optional CAD tables for L-ANNO-TEXT."""
    ANN = []

    # 1. Coordinate grid (40 m modules) with bubbles on all four sides
    grid, bub = [], []
    for k_, x in enumerate(range(200, 1801, 200)):
        grid.append(line(x, 26, x, H - 26, s=palette.MID, w=0.5, d="2 6", o=0.7))
        for yb in (17, H - 17):
            bub += [circle(x, yb, 9, f=palette.WHITE, s=palette.INK, w=0.8),
                    text(x, yb + 3, "ABCDEFGHI"[k_], size=8, anchor="middle", fill=palette.INK)]
    for k_, y in enumerate(range(200, 1401, 200)):
        grid.append(line(26, y, W - 26, y, s=palette.MID, w=0.5, d="2 6", o=0.7))
        for xb in (17, W - 17):
            bub += [circle(xb, y, 9, f=palette.WHITE, s=palette.INK, w=0.8),
                    text(xb, y + 3, str(k_ + 1), size=8, anchor="middle", fill=palette.INK)]
    ANN.append(G(grid, c=ZL2))
    ANN.append(G(bub))

    # 2. Metric Calibration Vector (Normative requirement per DT-UI-SVG-DOC-001 Rev 2.0)
    ANN.append(f'<line x1="0" y1="0" x2="1000" y2="0" id="CALIBRATION-VECTOR" data-real-meters="{1000 * M_PER_UNIT:.1f}" stroke="none" fill="none" style="display:none;" />')

    # 3. Tank Tags
    for t in ALL_TANKS:
        cx, cy = UVu(t[1], t[2])
        r = t[3] * K
        big = r > 44
        ANN.append(text(cx, cy + (2 if not big else -3), t[0], size=14 if big else (8.5 if r > 30 else 7.5),
                        anchor="middle", weight="bold", fill=palette.INK))
        if big:
            ANN.append(text(cx, cy + 13, f"Ø{2*r*M_PER_UNIT:.0f} m · {'FLOATING' if t[4]=='FR' else 'CONE'} ROOF",
                            size=7, anchor="middle", fill=palette.INK))

    # 4. Zone bubbles
    zb = []
    for num, name, (zu, zv) in ZONES:
        x, y = UVu(zu, zv)
        zb += [circle(x, y, 12, f=palette.INK),
               text(x, y + 4.5, num, size=13, anchor="middle", weight="bold", fill=palette.LIGHT)]
    ANN.append(G(zb))

    # 5. Equipment labels
    ANN.append(G([text(*PF.pt(PUMP_X0 + PUMP_PITCH * i + 2, 38), t, size=6, weight="bold", fill=palette.INK)
                  for i, t in enumerate(PUMP_TAGS)], c=ZL2))
    for k_, xl in enumerate(BAY_X):
        ANN.append(text(*GF.pt(xl + BAY_W / 2, 140), f"BAY-{k_ + 1:02d}", size=7.5, anchor="middle", weight="bold", fill=palette.INK))
    ANN.append(text(*MF.pt(75, 90), "MANIFOLD M-0101 · 5 HDRS", size=6.5, anchor="middle", weight="bold", fill=palette.INK))

    for name, (a0, a1, b0, b1) in BLDG.items():
        ANN.append(text(*UVu((a0 + a1) / 2, (b0 + b1) / 2 + 1.5), BLDG_SHORT[name], size=6.2, anchor="middle", weight="bold", fill=palette.INK))
        ANN.append(G([text(*UVu((a0 + a1) / 2, (b0 + b1) / 2 - 6), BLDG_INFO[name][0], size=4.6, anchor="middle", fill=palette.INK)], c=ZL2))

    ANN.append(G([text(*UVu((BASIN[0] + BASIN[1]) / 2, (BASIN[2] + BASIN[3]) / 2), "RETENTION / OWS BASIN", size=7, anchor="middle", weight="bold", fill=palette.INK)]))

    for gid, role, ei_, gp_ in GATES:
        (gx_, gy_), d_, nout_ = gate_u[gid]
        ANN.append(text(gx_ + nout_[0] * 40, gy_ + nout_[1] * 40 + 2, f"{gid} · {role}", size=8, anchor="middle", weight="bold", fill=palette.INK))

    ANN.append(G([text(*P(*lerp(gatehouses["G1"][0], gatehouses["G1"][2], 0.5)), "GATE-HOUSE", size=4.8, anchor="middle", fill=palette.INK),
                  text(*P(*lerp(gatehouses["G2"][0], gatehouses["G2"][2], 0.5)), "GATE-HOUSE", size=4.8, anchor="middle", fill=palette.INK),
                  text(*P(wbc[0], wbc[1] + 11), "WEIGHBRIDGE", size=5.5, anchor="middle", fill=palette.INK)], c=ZL2))

    _yc = lerp(lerp(YARD_PX[0], YARD_PX[3], 0.5), lerp(YARD_PX[1], YARD_PX[2], 0.5), 0.5)
    ANN.append(text(*P(_yc[0] - 17, _yc[1] + 4), "HV STAGING / QUEUE (one-way)", size=6.5, anchor="middle", weight="bold", rot=-88, fill=palette.INK))
    ANN.append(G([text(*UVu(735, LANE_V[0] - 14), "LANE 1-4  (one-way, SE → NW)", size=6, anchor="start", rot=ROT, fill=palette.INK)], c=ZL2))
    ANN.append(G([text(*UVu(690 + 1.5, 200), "HV EXIT — ONE-WAY SOUTH", size=6, anchor="middle", rot=ROT, fill=palette.INK)], c=ZL2))
    ANN.append(text(*P(700, 548), "PUBLIC ROAD", size=8, anchor="middle", rot=-11.3, fill=palette.INK))

    ANN.append(G([text(*UVu(430, 8 + 1.5), "R-01 · 6.0 m FIRE ACCESS", size=6.5, anchor="middle", rot=GRID_DEG, fill=palette.INK),
                  text(*UVu(520, 92 + 1.5), "R-02", size=6.5, anchor="middle", rot=GRID_DEG, fill=palette.INK),
                  text(*UVu(364 + 1.5, 170), "R-03", size=6.5, anchor="middle", rot=ROT, fill=palette.INK),
                  text(*UVu(520, 273 + 1.5), "R-04", size=6.5, anchor="middle", rot=GRID_DEG, fill=palette.INK),
                  text(*UVu(690 + 1.5, 330), "R-06", size=6.5, anchor="middle", rot=ROT, fill=palette.INK),
                  text(*UVu(585 + 1.5, 440), "R-07", size=6.5, anchor="middle", rot=ROT, fill=palette.INK),
                  text(*UVu(450, 111 - 5.0), "SLEEPERWAY SA · HEADERS A/B", size=6, anchor="middle", rot=GRID_DEG, fill=palette.INK),
                  text(*UVu(346 - 6, 120), "SN · TRUNK", size=6, anchor="middle", rot=ROT, fill=palette.INK),
                  text(*UVu(346 - 20, -30), "EXP. LOOP", size=5.5, anchor="middle", rot=ROT, fill=palette.INK),
                  text(*UVu(346 - 20, 190), "EXP. LOOP", size=5.5, anchor="middle", rot=ROT, fill=palette.INK)], c=ZL2))

    # 6. Dimensions (shell spacing)
    sw = TKS["SW"]
    ANN.append(dim_uv((396 + 0, -110 + 24), (402, -44 - 23), f"{gap_m(sw[0], sw[1]):.1f} m", palette))
    ANN.append(dim_uv((400, 150 + 14), (400, 190 - 14), f"{gap_m(TKS['CE'][0], TKS['CE'][1]):.1f} m", palette))

    # 7. Compass rose & Scale bar
    cr_x, cr_y = 120, 520
    ANN.append(G([circle(cr_x, cr_y, 36, s=palette.INK, w=1),
                  circle(cr_x, cr_y, 3, f=palette.INK),
                  polyg([(cr_x, cr_y - 36), (cr_x - 7, cr_y), (cr_x + 7, cr_y)], f=palette.INK),
                  polyg([(cr_x, cr_y + 36), (cr_x - 7, cr_y), (cr_x + 7, cr_y)], f=palette.WHITE, s=palette.INK, w=0.8),
                  line(cr_x - 36, cr_y, cr_x + 36, cr_y, s=palette.INK, w=0.8),
                  text(cr_x, cr_y - 41, "N", size=12, anchor="middle", weight="bold", fill=palette.INK),
                  text(cr_x, cr_y + 50, "S", size=8, anchor="middle", fill=palette.INK),
                  text(cr_x + 44, cr_y + 3, "E", size=8, fill=palette.INK),
                  text(cr_x - 44, cr_y + 3, "W", size=8, anchor="end", fill=palette.INK),
                  text(cr_x, cr_y + 64, "PLANT NORTH", size=7, anchor="middle", fill=palette.INK)]))

    sb_x, sb_y = 40, 610
    sb = [rect(sb_x + k_ * 50, sb_y, 50, 6, f=palette.INK if k_ % 2 == 0 else palette.WHITE, s=palette.INK, w=0.8) for k_ in range(4)]
    sb += [text(sb_x + k_ * 50, sb_y + 17, str(k_ * 10), size=7, anchor="middle", fill=palette.INK) for k_ in range(5)]
    sb += [text(sb_x + 215, sb_y + 17, "m", size=7, fill=palette.INK),
           text(sb_x, sb_y - 6, "SCALE 1 unit = 0.2 m  (5 units / m)", size=7, fill=palette.INK)]
    ANN.append(G(sb))

    # 8. Optional CAD Engineering Tables (only when include_cad_tables is True)
    if include_cad_tables:
        bund_res = compute_bund_capacities()
        names = {"SW": "B-01 TF1", "ST": "B-02 TF2", "CE": "B-03 TF3", "NE1": "B-04 TF4", "NE2": "B-05 TF4-FR"}

        bd = [text(40, 1270, "BUND DATA  (NFPA 30 · 110 % OF LARGEST TANK · SHELL SPACING ≥ D/6 · WALL CLEARANCE ≥ 1.5 m)",
                   size=9, weight="bold", fill=palette.INK)]
        for i, (k_, r_) in enumerate(bund_res.items()):
            bd.append(text(40, 1288 + 14 * i,
                           f"{names[k_]}  largest {r_['tag']}  V = {nf(r_['v'])} m³  → 110 % = {nf(r_['req'])} m³   "
                           f"H req. {r_['h_req']:.2f} m → wall H {r_['h_des']:.1f} m · net {nf(r_['net'])} m³",
                           size=7.5, fill=palette.INK))
        bd.append(text(40, 1288 + 14 * 5 + 6,
                       "Fillet R = 4.4 m at internal junctions (narrow corridors); perimeter road corners R = 15 m + half-width where edges allow.",
                       size=7, fill=palette.INK))
        bd.append(text(40, 1288 + 14 * 6 + 6,
                       "Underground drains / OWS lines not shown. Sumps drain to the retention basin (zone 7).",
                       size=7, fill=palette.INK))
        ANN.append(G(bd))

        bk = [text(1090, 1270, "BUILDING / GATE KEY  (distributed architecture)", size=9, weight="bold", fill=palette.INK)]
        for i, (nm, info) in enumerate(BLDG_INFO.items()):
            bk.append(text(1090, 1288 + 13 * i, f"{BLDG_SHORT[nm]:6s} {info[0]}   {info[1]}  —  {info[2]}: {info[3]}",
                           size=7, fill=palette.INK))
        for j, (gid, role, ei_, gp_) in enumerate(GATES):
            bk.append(text(1090, 1288 + 13 * (len(BLDG_INFO) + j), f"{gid:6s} {role}", size=7, weight="bold", fill=palette.INK))
        ANN.append(G(bk))

        tb = [rect(30, 30, 520, 118, f=palette.WHITE, s=palette.INK, w=1.4),
              line(30, 58, 550, 58, s=palette.INK, w=0.8),
              line(320, 58, 320, 148, s=palette.INK, w=0.8),
              text(40, 49, "GENERAL ARRANGEMENT — PLOT PLAN · BULK LIQUID HYDROCARBON TERMINAL", size=9.5, weight="bold", fill=palette.INK),
              text(40, 74, f"IRREGULAR PLOT ≈ {m2(poly_area(BND)) / 1e4:.1f} ha · 1 UNIT = 0.2 m", size=8, fill=palette.INK),
              text(40, 88, "DRAWING  DT-UI-SVG-DOC-001 / GA-003      REV B", size=8, fill=palette.INK),
              text(40, 102, f"TANKS: {sum(1 for t in ALL_TANKS if t[0] != 'TK-0501')} + 1 FW  ·  PUMPS: 6  ·  BAYS: 4", size=8, fill=palette.INK),
              text(40, 116, "LAYERS: L-CIVL-BOTM · L-MECH-EQPM · L-PIPE-PROC · L-INSP-INST · L-FIRE-PROT · L-ELEC-HAZ · L-ANNO-TEXT", size=6.5, fill=palette.INK),
              text(40, 130, "SEMANTIC ZOOM: L1 macro · L2 secondary · L3 micro", size=7, fill=palette.INK),
              text(330, 74, "CODES / STANDARDS", size=8, weight="bold", fill=palette.INK),
              text(330, 88, "NFPA 30 (spacing, diking)", size=7.5, fill=palette.INK),
              text(330, 100, "ISA-101 (HMI, progressive disclosure)", size=7.5, fill=palette.INK),
              text(330, 112, "ISO 13567 / AIA CAD layering", size=7.5, fill=palette.INK),
              text(330, 124, "ISO 14224 (APM data binding)", size=7.5, fill=palette.INK),
              text(330, 140, "COLOUR RESERVED FOR LIVE ALARMS", size=7, weight="bold", fill=palette.INK)]
        ANN.append(G(tb))

        lg = [rect(30, 160, 300, 256, f=palette.WHITE, s=palette.INK, w=1.2),
              text(40, 175, "LEGEND / ZONE KEY", size=8, weight="bold", fill=palette.INK)]
        for i, (num, name, _) in enumerate(ZONES):
            lg += [circle(48, 191 + 14 * i, 5.5, f=palette.INK),
                   text(48, 193.5 + 14 * i, num, size=7, anchor="middle", weight="bold", fill=palette.LIGHT),
                   text(60, 193.5 + 14 * i, name, size=6.3, fill=palette.INK)]
        yy = 191 + 14 * 8 + 10
        lg += [circle(46, yy, 5, f=palette.WHITE, s=palette.INK, w=1.2),
               text(58, yy + 2.5, "STORAGE TANK (FR / CONE ROOF)", size=6.3, fill=palette.INK),
               circle(46, yy + 13, 3.5, f=palette.WHITE, s=palette.INK, w=1.2),
               circle(46, yy + 13, 1.2, f=palette.INK),
               text(58, yy + 15.5, "HYDRANT", size=6.3, fill=palette.INK),
               rect(41, yy + 24, 10, 10, f=palette.WHITE, s=palette.INK, w=1.2),
               text(58, yy + 32, "FOAM MONITOR (R = 50 m)", size=6.3, fill=palette.INK),
               line(36, yy + 46, 56, yy + 46, s=palette.INK, w=2.6),
               line(36, yy + 51, 56, yy + 51, s=palette.STEEL, w=1.0),
               text(64, yy + 50, "PROCESS HEADER / SLEEPER LINES", size=6.3, fill=palette.INK),
               line(176, yy, 196, yy, s=palette.STEEL, w=2, d="16 4 3 4"),
               text(202, yy + 3, "FIRE-WATER MAIN", size=6.3, fill=palette.INK),
               rect(176, yy + 8, 20, 8, f="url(#hatch-concrete)", s=palette.INK, w=1),
               text(202, yy + 15, "CONCRETE BUND", size=6.3, fill=palette.INK),
               rect(176, yy + 22, 20, 8, f=palette.CONC, s=palette.STEEL, w=0.8),
               text(202, yy + 29, "SLEEPERWAY 6 m", size=6.3, fill=palette.INK),
               line(176, yy + 42, 196, yy + 42, s=palette.ASPH, w=8),
               text(202, yy + 45, "ROAD 6 m", size=6.3, fill=palette.INK),
               polyg([(206, yy + 56), (196, yy + 52), (196, yy + 60)], f=palette.INK),
               text(212, yy + 59, "HV ONE-WAY DIRECTION", size=6.3, fill=palette.INK)]
        ANN.append(G(lg))

    return ANN
