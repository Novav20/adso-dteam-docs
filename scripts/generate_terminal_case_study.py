#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_terminal_svg_irregular.py   (rev B - engineering corrections)
=====================================================================
Parametric 2D General Arrangement (GA) plot plan of a bulk liquid hydrocarbon terminal on an
IRREGULAR plot traced from a reference survey (31 tanks = 30 storage + 1 fire-water, 6 pumps,
4 loading bays) on a 49-degree plant grid.

Contract : DT-UI-SVG-DOC-001  (6 layers, ISA-101 zoom classes, ISO 14224 data binding)
Scale    : 1 SVG unit = 0.2 m (viewBox 0 0 2000 1500); design space 1 px = 2 units
Colour   : neutral greys only (colour is reserved for live alarms)

Rev B corrections, all asserted at generation time
  1. Distributed buildings: ONE Main Control Room + ONE Field Auxiliary/Rack Room, ONE Main HV
     Substation + THREE zone MCCs, ONE Maintenance Warehouse + ONE Consumables/Lube store.
  2. One-way HV tanker circuit: G1 HV entry -> perimeter road (CCW) -> staging/queue yard ->
     4 gantry lanes (SE -> NW) -> R-06 southbound -> R-02 -> R-05 -> R-01 -> perimeter -> G2 HV exit.
     G3 = emergency / light-vehicle access.  No dead-end road vectors; the short SE fence chamfer is
     merged into one road corner so the 15 m turning radius is continuous.
  3. Tank spacing (shell-to-shell >= D/6), wall clearance (>= 1.5 m) and bund walls sized for 110 %
     of the largest tank in each bund plus displacement of the others.
  4. Sleeperway network is a single connected piping graph reaching every tank stub, the pump pad,
     manifold and gantry; no pipe enters a building, basin, yard or tank.
Output   : terminal_plot_plan_irregular.svg (+ _l2 / _l3 preview copies)
"""
import colorsys
import math
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------
# Scale helpers
# --------------------------------------------------------------------------
M_PER_UNIT = 0.2


def U(metres):
    """metres -> SVG units"""
    return metres / M_PER_UNIT


def M(units):
    """SVG units -> metres"""
    return units * M_PER_UNIT


W, H = 2000, 1500

# --------------------------------------------------------------------------
# ISA-101 neutral palette
# --------------------------------------------------------------------------
INK = "#2B2D42"
MID = "#8D99AE"
LIGHT = "#EDF2F4"
PALE = "#E5E5E5"
STEEL = "#5C677D"
ASPH = "#C5CAD3"
CONC = "#D6DAE0"
WHITE = "#FAFBFC"
FAINT = "#B9C0CC"
BUNDFILL = "#E8EAED"

ZL2 = "dt-zoom-l2"
ZL3 = "dt-zoom-l3"
DASHDOT = "10 3 2 3"

# --------------------------------------------------------------------------
# Tiny SVG string toolkit
# --------------------------------------------------------------------------
KEYMAP = {
    "f": "fill", "s": "stroke", "w": "stroke-width", "d": "stroke-dasharray",
    "o": "opacity", "c": "class", "fo": "fill-opacity", "so": "stroke-opacity",
    "lc": "stroke-linecap", "lj": "stroke-linejoin",
}


def n(v):
    if isinstance(v, float):
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        return "0" if s in ("-0", "") else s
    return str(v)


def A(kw):
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        k = KEYMAP.get(k, k).replace("_", "-")
        out.append(f'{k}="{n(v)}"')
    return " ".join(out)


def rect(x, y, wd, ht, **kw):
    kw.setdefault("f", "none")
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(wd)}" height="{n(ht)}" {A(kw)}/>'


def circle(cx, cy, r, **kw):
    kw.setdefault("f", "none")
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" {A(kw)}/>'


def line(x1, y1, x2, y2, **kw):
    return f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" {A(kw)}/>'


def path(dd, **kw):
    kw.setdefault("f", "none")
    return f'<path d="{dd}" {A(kw)}/>'


def polyg(pts, **kw):
    kw.setdefault("f", "none")
    p = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
    return f'<polygon points="{p}" {A(kw)}/>'


def text(x, y, s, size=9, anchor="start", weight="normal", rot=None, **kw):
    kw.setdefault("f", INK)
    tr = f' transform="rotate({n(rot)} {n(x)} {n(y)})"' if rot is not None else ""
    return (f'<text x="{n(x)}" y="{n(y)}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{n(size)}" text-anchor="{anchor}" font-weight="{weight}"{tr} '
            f'{A(kw)}>{escape(s)}</text>')


def G(children, **kw):
    body = "\n".join(c for c in children if c)
    if not body:
        return ""
    return f"<g {A(kw)}>\n{body}\n</g>" if kw else f"<g>\n{body}\n</g>"


def frange(a, b, step):
    x = a
    while x <= b + 1e-9:
        yield x
        x += step


def polar(cx, cy, r, a_deg):
    t = math.radians(a_deg)
    return cx + r * math.cos(t), cy + r * math.sin(t)


def arc_band(cx, cy, r1, r2, a0, a1):
    x0, y0 = polar(cx, cy, r2, a0)
    x1, y1 = polar(cx, cy, r2, a1)
    x2, y2 = polar(cx, cy, r1, a1)
    x3, y3 = polar(cx, cy, r1, a0)
    large = 1 if ((a1 - a0) % 360) > 180 else 0
    return (f"M{n(x0)},{n(y0)} A{n(r2)},{n(r2)} 0 {large} 1 {n(x1)},{n(y1)} "
            f"L{n(x2)},{n(y2)} A{n(r1)},{n(r1)} 0 {large} 0 {n(x3)},{n(y3)} Z")


def split(a, b, skips):
    segs = [(a, b)]
    for s0, s1 in skips:
        new = []
        for p, q in segs:
            if s1 <= p or s0 >= q:
                new.append((p, q))
                continue
            if p < s0:
                new.append((p, s0))
            if q > s1:
                new.append((s1, q))
        segs = new
    return segs




# ==========================================================================
#  SITE MODEL  (design space = reference "px"; 1 px = 2 SVG units = 0.4 m)
# ==========================================================================
K = 2.0                                  # SVG units per design px
OX, OY = -37.0, 120.0                    # design px -> SVG translation
GRID_DEG = 49.0                          # plant grid rotation (matches the reference)
ROT = -(90.0 - GRID_DEG)                 # SVG rotate() angle of the u/v frame (-41 deg)
CU, SU = math.cos(math.radians(GRID_DEG)), math.sin(math.radians(GRID_DEG))
HW = U(6) / K / 2                        # road / sleeperway half width in px (7.5)
ROAD_W = U(6)                            # 6 m internal & perimeter roads = 30 units


def P(x, y):
    return (OX + K * x, OY + K * y)


def uvp(u, v):                           # plant-grid (u down-right, v up-right) -> design px
    return (u * CU + v * SU, u * SU - v * CU)


def UVu(u, v):                           # plant-grid -> SVG units
    return P(*uvp(u, v))


def uv_of(x, y):
    return (x * CU + y * SU, x * SU - y * CU)


# ---- irregular site boundary (traced from the reference, design px) -------------
BND = [(480, 10), (967, 187), (936, 252), (803, 352), (806, 497), (790, 512),
       (550, 523), (412, 525), (385, 520), (363, 495), (235, 532), (70, 343), (255, 140)]


def poly_area(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1]
               for i in range(len(p))) / 2


def offset_poly(p, d):
    """Inward miter offset (positive d = inward), valid for either orientation."""
    s = 1 if poly_area(p) > 0 else -1
    nn, lines, out = len(p), [], []
    for i in range(nn):
        a, b = p[i], p[(i + 1) % nn]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * s, dx / L * s
        lines.append(((a[0] + nx * d, a[1] + ny * d), (dx / L, dy / L)))
    for i in range(nn):
        (p1, d1), (p2, d2) = lines[i - 1], lines[i]
        cr = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(cr) < 1e-9:
            out.append(p2)
            continue
        t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / cr
        out.append((p1[0] + d1[0] * t, p1[1] + d1[1] * t))
    return out


def dist_seg(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def dist_poly(p, poly):
    return min(dist_seg(p, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))


def pip(p, poly):
    x, y, c = p[0], p[1], False
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def clip_half(poly, a, b, d):
    """Keep the part of poly that lies >= d inside boundary edge a->b (BND is CW on screen)."""
    ex, ey = b[0] - a[0], b[1] - a[1]
    L = math.hypot(ex, ey)
    nx, ny = -ey / L, ex / L
    f = lambda q: (q[0] - a[0]) * nx + (q[1] - a[1]) * ny - d
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = f(p), f(q)
        if fp >= 0:
            out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def ray_hit(p, d, poly):
    best = None
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = d[0] * ey - d[1] * ex
        if abs(den) < 1e-9:
            continue
        t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
        s = ((a[0] - p[0]) * d[1] - (a[1] - p[1]) * d[0]) / den
        if t > 1e-6 and -1e-9 <= s <= 1 + 1e-9 and (best is None or t < best):
            best = t
    return best


def rounded_closed(pts, r):
    """Closed polygon path with arc-rounded corners (radius clamped to adjacent edges)."""
    nn, d = len(pts), ""
    for i in range(nn):
        pv, v, nx_ = pts[i - 1], pts[i], pts[(i + 1) % nn]
        a, b = (pv[0] - v[0], pv[1] - v[1]), (nx_[0] - v[0], nx_[1] - v[1])
        la, lb = math.hypot(*a), math.hypot(*b)
        ua, ub = (a[0] / la, a[1] / la), (b[0] / lb, b[1] / lb)
        phi = math.acos(max(-1, min(1, ua[0] * ub[0] + ua[1] * ub[1])))
        cmd = "M" if i == 0 else "L"
        if phi > math.pi - 1e-3:
            d += f"{cmd}{n(v[0])},{n(v[1])} "
            continue
        t = min(r / math.tan(phi / 2), 0.48 * la, 0.48 * lb)
        rr = t * math.tan(phi / 2)
        A_ = (v[0] + ua[0] * t, v[1] + ua[1] * t)
        B_ = (v[0] + ub[0] * t, v[1] + ub[1] * t)
        cross = (v[0] - pv[0]) * (nx_[1] - v[1]) - (v[1] - pv[1]) * (nx_[0] - v[0])
        d += f"{cmd}{n(A_[0])},{n(A_[1])} A{n(rr)},{n(rr)} 0 0 {1 if cross > 0 else 0} {n(B_[0])},{n(B_[1])} "
    return d + "Z"


def pts_path(pts, close=False):
    d = "M" + " L".join(f"{n(x)},{n(y)}" for x, y in pts)
    return d + (" Z" if close else "")


def uvpath(pts_uv, close=False):
    return pts_path([UVu(*p) for p in pts_uv], close)


class Frame:
    """Local equipment frame: x' = +v (up-right), y' = +u (down-right), units."""

    def __init__(s, u0, v0):
        s.u0, s.v0 = u0, v0
        s.o = UVu(u0, v0)

    def uv(s, x, y):
        return (s.u0 + y / K, s.v0 + x / K)

    def pt(s, x, y):
        return UVu(*s.uv(x, y))

    def g(s, children, **kw):
        return G(children, transform=f"translate({n(s.o[0])} {n(s.o[1])}) rotate({n(ROT)})", **kw)


BNDU = [P(*p) for p in BND]
_RAW15 = offset_poly(BND, 15)


def _line_x(p1, p2, p3, p4):
    d1, d2 = (p2[0] - p1[0], p2[1] - p1[1]), (p4[0] - p3[0], p4[1] - p3[1])
    cr = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((p3[0] - p1[0]) * d2[1] - (p3[1] - p1[1]) * d2[0]) / cr
    return (p1[0] + d1[0] * t, p1[1] + d1[1] * t)


# the short SE chamfer (fence vertices 4-5) would force a ~1 m turn: merge it into ONE corner so the
# rounded road keeps the full 15 m turning radius
ROADC = _RAW15[:4] + [_line_x(_RAW15[6], _RAW15[5], _RAW15[3], _RAW15[4])] + _RAW15[6:]
RINGM = offset_poly(BND, 10)             # perimeter fire-water main (px)
HYDR = offset_poly(BND, 5)               # perimeter hydrant line (px)

# ---- tank farms -------------------------------------------------------------------
# (tag, u, v, r_px, kind, shell_height_m, pipe_dir_deg)   pipe_dir = screen angle of the stub
A_PV, A_MV, A_PU, A_MU = ROT, ROT + 180, GRID_DEG, GRID_DEG + 180      # +v, -v, +u, -u
TKS = {
    "SW": [("TK-0101", 396, -110, 24, "FR", 12, A_PV), ("TK-0102", 402, -44, 23, "FR", 12, A_MV),
           ("TK-0103", 458, -112, 23, "FR", 12, A_PV), ("TK-0104", 462, -48, 22, "FR", 12, A_MV),
           ("TK-0105", 522, -82, 34, "FR", 12, A_MU)],
    "ST": [(f"TK-020{i+1}", 410 + 48 * i, 52, 18, "CR", 12, A_PV) for i in range(5)],
    "CE": [(f"TK-03{i*3+j+1:02d}", 400 + 62 * i, 150 + 40 * j, 14, "CR", 10, A_PV if j == 0 else A_MV)
           for i in range(4) for j in range(3)],
    "NE": [(f"TK-040{i*3+j+1}", 500 + 48 * i, 326 + 36 * j, 15, "CR", 10, A_PU if i == 0 else A_MU)
           for i in range(2) for j in range(3)] +
          [("TK-0407", 642, 336, 22, "FR", 8, A_PV), ("TK-0408", 642, 393, 22, "FR", 8, A_MV)],
}
FWT = ("TK-0501", 772, 278, 19, "CR", 9, A_MU)

# bund rectangles in (u0,u1,v0,v1) + boundary edges that clip them (index into BND)
BUND_DEF = {
    "SW": ((358, 574, -148, -8), [9, 10, 11]),
    "ST": ((382, 630, 24, 80), []),
    "CE": ((376, 610, 126, 254), []),
    "NE1": ((467, 573, 301, 423), [0]),
    "NE2": ((608, 676, 302, 427), [0]),
}
CLIP_D = 26.0
BUNDS = {}
for k_, ((u0, u1, v0, v1), edges) in BUND_DEF.items():
    poly = [uvp(u0, v0), uvp(u1, v0), uvp(u1, v1), uvp(u0, v1)]
    for e in edges:
        poly = clip_half(poly, BND[e], BND[(e + 1) % len(BND)], CLIP_D)
    BUNDS[k_] = poly
BUND_TANKS = {"SW": TKS["SW"], "ST": TKS["ST"], "CE": TKS["CE"],
              "NE1": [t for t in TKS["NE"] if t[3] == 15], "NE2": [t for t in TKS["NE"] if t[3] == 22]}
WALL_PX = 3.0                            # 6 units = 1.2 m concrete wall

# ---- roads (plant-grid coordinates) ----------------------------------------------------
# (id, [(u,v),...], snap_start, snap_end)
ROADS = [("R-01", [(300, 8), (670, 8)], True, True),
         ("R-02", [(300, 92), (690, 92)], True, False),
         ("R-03", [(364, 8), (364, 300)], False, True),
         ("R-04", [(364, 273), (690, 273)], False, False),
         ("R-05", [(655, 8), (655, 273)], False, False),
         ("R-06", [(690, 92), (690, 500)], True, True),
         ("R-07", [(585, 273), (585, 440)], False, True)]
SNAP_PX = ROADC


def snap_road(pts, s0, s1):
    p = [uvp(*q) for q in pts]
    out = list(p)
    for flag, idx, nb in ((s0, 0, 1), (s1, -1, -2)):
        if not flag:
            continue
        a, b = p[idx], p[nb]
        d = (a[0] - b[0], a[1] - b[1])
        L = math.hypot(*d)
        d = (d[0] / L, d[1] / L)
        t = ray_hit(a, d, SNAP_PX)
        if t is not None and t < 400:
            out[idx] = (a[0] + d[0] * t, a[1] + d[1] * t)
    return out


ROADS_PX = [(rid, snap_road(pts, a, b)) for rid, pts, a, b in ROADS]
ROAD_EXT = []       # (type, const, lo, hi) from the SNAPPED geometry; type 'u' = runs along u at v=const
for (rid, pts, a_, b_), (_, ppx) in zip(ROADS, ROADS_PX):
    e0, e1 = uv_of(*ppx[0]), uv_of(*ppx[-1])
    if pts[0][1] == pts[-1][1]:
        ROAD_EXT.append(("u", pts[0][1], min(e0[0], e1[0]), max(e0[0], e1[0])))
    else:
        ROAD_EXT.append(("v", pts[0][0], min(e0[1], e1[1]), max(e0[1], e1[1])))

# ---- sleeperways / pipe corridors -----------------------------------------------------------
SLEEPERS = [("v", 346, -82, 296), ("u", 111, 346, 672), ("v", 672, 20, 264), ("u", 290, 346, 600)]

# ---- equipment frames ---------------------------------------------------------------------------
PF, MF, GF = Frame(702, 122), Frame(706, 262), Frame(700, 380)
PUMP_TAGS = ["P-0101A", "P-0101B", "P-0101C", "P-0201A", "P-0201B", "P-0201C"]
PUMP_PITCH, PUMP_X0, PUMP_Y, PUMP_S = 40, 12, 43, 0.7
ISL_W, BAY_W = 14, 30
ISL_X = [(ISL_W + BAY_W) * k for k in range(5)]
BAY_X = [ISL_W + (ISL_W + BAY_W) * k for k in range(4)]

# ---- site buildings: distributed architecture (plant-grid rectangles u0,u1,v0,v1) ---------------
# name -> rect ; BLDG_INFO name -> (tag, short label, discipline, serves)
BLDG = {"MCR": (804, 826, 244, 284),
        "FAR": (600, 624, 436, 470),
        "HV SUB": (730, 750, 342, 368),
        "MCC-1": (308, 332, 28, 62),
        "MCC-2": (616, 640, 150, 182),
        "MCC-3": (628, 652, 436, 470),
        "WH-01": (378, 408, 308, 350),
        "WH-02": (414, 438, 308, 342),
        "FW PUMP HOUSE": (790, 808, 288, 308)}
BLDG_INFO = {
    "MCR": ("BLD-MCR-01", "MAIN CONTROL ROOM (MCR)", "Control", "whole terminal"),
    "FAR": ("BLD-FAR-01", "FIELD AUXILIARY ROOM (FAR) / RACK ROOM", "Control", "tank farms 3 & 4, manifold"),
    "HV SUB": ("BLD-SUB-01", "MAIN HV SUBSTATION", "Power", "incoming supply, MV distribution"),
    "MCC-1": ("BLD-MCC-01", "MCC-1 (TANK FARMS 1 & 2)", "Power", "TF1 / TF2 mixers, valves, sumps"),
    "MCC-2": ("BLD-MCC-02", "MCC-2 (TANK FARM 3)", "Power", "TF3 valves, sumps, lighting"),
    "MCC-3": ("BLD-MCC-03", "MCC-3 (TANK FARM 4 + PUMPS)", "Power", "TF4, pump station, gantry"),
    "WH-01": ("BLD-WH-01", "MAIN MAINTENANCE WAREHOUSE", "Storage", "spares, tools, workshop"),
    "WH-02": ("BLD-WH-02", "CONSUMABLES / LUBE STORAGE", "Storage", "lubricants, additives, PPE"),
    "FW PUMP HOUSE": ("BLD-FWP-01", "FIRE-WATER PUMP HOUSE", "Fire", "ring main"),
}
BASIN = (765, 815, 190, 240)

# ---- gates: (id, role, boundary-edge index, point on the fence in design px) ------------------------
GATES = [("G1", "HV ENTRY", 6, (485, 524)),
         ("G2", "HV EXIT", 7, (400, 522.8)),
         ("G3", "EMERGENCY / LV ACCESS", 4, (798, 504.5))]
GATE_PX = GATES[0][3]
PUB_ROAD = [(380, 610), (1010, 490)]            # public road outside the fence

# ---- one-way heavy-vehicle (HV) staging yard along the east perimeter, inside the road ------------------
def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


_o23, _o41 = offset_poly(BND, 23), offset_poly(BND, 41)
YARD_PX = [lerp(_o23[4], _o23[3], 0.14), lerp(_o23[4], _o23[3], 0.96),
           lerp(_o41[4], _o41[3], 0.96), lerp(_o41[4], _o41[3], 0.14)]
GANT_W, GANT_Y0, GANT_Y1 = 190, -20, 154

# ---- tanks, obstacles and free-space tests (design px) ---------------------------------------------
ALL_TANKS = [t for ts in TKS.values() for t in ts] + [FWT]
OBST = [BUNDS[k_] for k_ in BUNDS]
for ax, c, a, b_ in SLEEPERS:
    if ax == "v":
        OBST.append([uvp(c - HW, a), uvp(c + HW, a), uvp(c + HW, b_), uvp(c - HW, b_)])
    else:
        OBST.append([uvp(a, c - HW), uvp(b_, c - HW), uvp(b_, c + HW), uvp(a, c + HW)])
for (a0, a1, b0, b1) in list(BLDG.values()) + [BASIN]:
    OBST.append([uvp(a0, b0), uvp(a1, b0), uvp(a1, b1), uvp(a0, b1)])
FRAME_BOX = []
for fr, (w_, h_, x0_, y0_) in ((PF, (250, 100, 0, 0)), (MF, (150, 80, 0, 0)), (GF, (GANT_W + 24, GANT_Y1 - GANT_Y0, -12, GANT_Y0))):
    FRAME_BOX.append([uvp(*fr.uv(x0_, y0_)), uvp(*fr.uv(x0_ + w_, y0_)), uvp(*fr.uv(x0_ + w_, y0_ + h_)), uvp(*fr.uv(x0_, y0_ + h_))])
OBST += FRAME_BOX + [YARD_PX]
ROAD_SEGS_PX = [(pts[i], pts[i + 1]) for _, pts in ROADS_PX for i in range(len(pts) - 1)]
CIRC = [(uvp(t[1], t[2]), t[3]) for t in ALL_TANKS]


def free(p, clr_road=10.5, margin=1.0):
    if dist_poly(p, BND) < 4 or not pip(p, BND):
        return False
    if dist_poly(p, ROADC) < clr_road:
        return False
    if any(dist_seg(p, a, b) < clr_road for a, b in ROAD_SEGS_PX):
        return False
    for o in OBST:
        if pip(p, o) or dist_poly(p, o) < margin:
            return False
    for c, r in CIRC:
        if math.hypot(p[0] - c[0], p[1] - c[1]) < r + 1:
            return False
    return True


# ==========================================================================
#  ENGINEERING SELF-CHECK (computed, printed, asserted)
# ==========================================================================
def m2(px_area):
    return px_area * (K * M_PER_UNIT) ** 2


def tk_geom(t):
    return (t[3] * K * M_PER_UNIT, t[5])      # radius_m, height_m


BUND_RES = {}
for k_, poly in BUNDS.items():
    ts = BUND_TANKS[k_]
    vols = [math.pi * tk_geom(t)[0] ** 2 * tk_geom(t)[1] for t in ts]
    big = max(range(len(ts)), key=lambda i: vols[i])
    a_net = m2(abs(poly_area(poly))) - sum(math.pi * tk_geom(t)[0] ** 2 for i, t in enumerate(ts) if i != big)
    h_req = 1.10 * vols[big] / a_net
    h_des = max(1.0, math.ceil((h_req + 0.15) / 0.1) * 0.1)
    BUND_RES[k_] = dict(v=vols[big], req=1.1 * vols[big], h_req=h_req, h_des=h_des, net=a_net * h_des, tag=ts[big][0])
    assert h_des <= 2.5, f"bund {k_} wall too high ({h_des})"
    # shell-to-shell spacing (>= D/6) and wall clearance (>= 1.5 m)
    for i in range(len(ts)):
        c = uvp(ts[i][1], ts[i][2])
        assert pip(c, poly), f"{ts[i][0]} outside bund"
        inner = offset_poly(poly, WALL_PX)
        assert dist_poly(c, inner) - ts[i][3] >= 1.5 / (K * M_PER_UNIT) - 1e-6, f"{ts[i][0]} too close to wall"
        for j in range(i + 1, len(ts)):
            d = math.hypot(ts[i][1] - ts[j][1], ts[i][2] - ts[j][2])
            gap_m = (d - ts[i][3] - ts[j][3]) * K * M_PER_UNIT
            dmax = 2 * max(tk_geom(ts[i])[0], tk_geom(ts[j])[0])
            assert gap_m >= dmax / 6 - 1e-6, f"{ts[i][0]}-{ts[j][0]} gap {gap_m:.1f} m < D/6"
for k_, ts in TKS.items():
    for t in ts:
        c = uvp(t[1], t[2])
        assert dist_poly(c, BND) - t[3] >= 24, f"{t[0]} within 24 px of fence"
for k_, poly in BUNDS.items():
    for q in poly:
        assert dist_poly(q, BND) >= CLIP_D - 1.0, f"bund {k_} too close to fence"
assert abs(ROAD_W - U(6)) < 1e-9 and abs(U(40) - 200) < 1e-9
assert pip(uvp(*FWT[1:3]), BND)

# ==========================================================================
#                              LAYER BUFFERS
# ==========================================================================
CIV, STR, MEC, PIP, INS, FIR, HAZ, ANN = ([] for _ in range(8))
VAL2, VAL3, FLG = [], [], []


def ang_of(along):
    return ROT if along == "v" else GRID_DEG


def valve(uv, along="v", s=4.5):
    x, y = UVu(*uv)
    tr = f"translate({n(x)} {n(y)}) rotate({n(ang_of(along))})"
    VAL2.append(G([path(f"M{n(-s)},{n(-s*.7)} L{n(s)},{n(s*.7)} L{n(s)},{n(-s*.7)} L{n(-s)},{n(s*.7)} Z",
                        f=WHITE, s=INK, w=0.9)], transform=tr))
    VAL3.append(G([line(0, -s * .7, 0, -s * .7 - 5, s=INK, w=0.7),
                   line(-3.5, -s * .7 - 5, 3.5, -s * .7 - 5, s=INK, w=1.2)], transform=tr))


def check_valve(uv, along="v"):
    x, y = UVu(*uv)
    VAL2.append(G([polyg([(-4, -3.5), (-4, 3.5), (4, 0)], f=WHITE, s=INK, w=0.9),
                   line(4, -3.5, 4, 3.5, s=INK, w=1.1)], transform=f"translate({n(x)} {n(y)}) rotate({n(ang_of(along))})"))


def flange(uv, along="v", size=4.5):
    x, y = UVu(*uv)
    FLG.append(G([line(0, -size, 0, size, s=INK, w=1.1), line(2.2, -size, 2.2, size, s=INK, w=1.1)],
                 transform=f"translate({n(x)} {n(y)}) rotate({n(ang_of(along))})"))


PIPE_NET = []          # every process polyline (plant-grid points) for connectivity / clearance checks
STUBS = {}             # tank tag -> its stub polyline


def pipe(pts_uv, kind="A", w=2.6):
    PIPE_NET.append(list(pts_uv))
    return path(uvpath(pts_uv), s=INK if kind == "A" else STEEL, w=w, lj="round")


# ==========================================================================
#                                L-CIVIL
# ==========================================================================
CIV.append(rect(0, 0, W, H, f=LIGHT))
prop = offset_poly(BND, -3)
CIV.append(path(pts_path([P(*q) for q in prop], True), s=MID, w=1.5, d="30 6 4 6"))      # property limit
# public road outside the fence
pub = [P(*PUB_ROAD[0]), P(*PUB_ROAD[1])]
CIV.append(line(*pub[0], *pub[1], s=STEEL, w=44))
CIV.append(line(*pub[0], *pub[1], s=ASPH, w=42))
CIV.append(line(*pub[0], *pub[1], s=LIGHT, w=1.2, d="14 10", c=ZL2))


def pub_y(x):
    return PUB_ROAD[0][1] + (x - PUB_ROAD[0][0]) * (PUB_ROAD[1][1] - PUB_ROAD[0][1]) / (PUB_ROAD[1][0] - PUB_ROAD[0][0])


def edge_dirs(ei):
    a_, b_ = BND[ei], BND[(ei + 1) % len(BND)]
    L = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
    d = ((b_[0] - a_[0]) / L, (b_[1] - a_[1]) / L)
    return d, (d[1], -d[0])            # unit along fence, OUTWARD normal (BND is clockwise on screen)


# gate throats (asphalt drives down to the public road) and gate leaves
GATE_U = {}
for gid, role, ei, gp in GATES:
    d, nout = edge_dirs(ei)
    w_ = 11.0
    reach = 0.0
    while gp[1] + nout[1] * reach < pub_y(gp[0] + nout[0] * reach) - 9 and reach < 120:
        reach += 1
    q1 = (gp[0] - d[0] * w_, gp[1] - d[1] * w_)
    q2 = (gp[0] + d[0] * w_, gp[1] + d[1] * w_)
    q3 = (q2[0] + nout[0] * (reach + 3), q2[1] + nout[1] * (reach + 3))
    q4 = (q1[0] + nout[0] * (reach + 3), q1[1] + nout[1] * (reach + 3))
    CIV.append(polyg([P(*q) for q in (q1, q2, q3, q4)], f=ASPH, s=STEEL, w=1))
    GATE_U[gid] = (P(*gp), d, nout)
# fence (boundary polygon) with posts every 25 units; gate openings skipped
CIV.append(path(pts_path(BNDU, True), s=INK, w=1.4))
posts = []
for i in range(len(BNDU)):
    a, b_ = BNDU[i], BNDU[(i + 1) % len(BNDU)]
    L = math.hypot(b_[0] - a[0], b_[1] - a[1])
    for k_ in range(int(L // 25) + 1):
        t = k_ * 25 / L
        x, y = a[0] + t * (b_[0] - a[0]), a[1] + t * (b_[1] - a[1])
        if any(math.hypot(x - gu[0][0], y - gu[0][1]) < 28 for gu in GATE_U.values()):
            continue
        posts.append(rect(x - 1.5, y - 1.5, 3, 3, f=INK))
CIV.append(G(posts, c=ZL2))
for gid, ((gx_, gy_), d, nout) in GATE_U.items():
    for s_ in (-1, 1):
        CIV.append(line(gx_ + s_ * d[0] * 14 + nout[0] * 3, gy_ + s_ * d[1] * 14 + nout[1] * 3,
                        gx_ + s_ * d[0] * 28 + nout[0] * 3, gy_ + s_ * d[1] * 28 + nout[1] * 3, s=INK, w=3))
gx, gy = GATE_U["G1"][0]

# --- asphalt roads (two-pass: edge colour then fill) ------------------------------------
perim_pts = [P(*q) for q in ROADC]
perim_d = rounded_closed(perim_pts, U(15) + ROAD_W / 2)      # 15 m inner turning radius target
road_lines = [[P(*q) for q in pts] for _, pts in ROADS_PX]


def road_pass(width, colour):
    out = [path(perim_d, s=colour, w=width, lj="round")]
    for pl_ in road_lines:
        out.append(path(pts_path(pl_), s=colour, w=width, lc="butt", lj="round"))
    return out


CIV += road_pass(ROAD_W + 2, STEEL)
CIV += road_pass(ROAD_W, ASPH)

# junction fillets between internal orthogonal roads
FIL_CANDIDATES = (75.0, 60.0, 50.0, 40.0, 30.0, 22.0)     # units: 15 m ... 4.4 m inner radius
FIL_LOG = {}


def fillet_poly(pu, pv, su, sv, Rp, n_arc=10):
    cu_, cv_ = pu + su * Rp, pv + sv * Rp
    arc = [(cu_ - su * Rp * math.sin(math.radians(90 * i / n_arc)), cv_ - sv * Rp * math.cos(math.radians(90 * i / n_arc)))
           for i in range(n_arc + 1)]
    return [(pu, pv)] + arc, arc


def fillet_clear(poly_uv):
    pts = [uvp(*q) for q in poly_uv]
    cen = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    for p in pts[1:] + [cen]:
        if not pip(p, BND) or dist_poly(p, BND) < 26:
            return False
        for o in OBST:
            if pip(p, o):
                return False
        for c, r in CIRC:
            if math.hypot(p[0] - c[0], p[1] - c[1]) < r:
                return False
    return True


fills, edges = [], []
for ia, (ta, ca, la, ha) in enumerate(ROAD_EXT):
    if ta != "u":
        continue
    for ib, (tb, cb, lb, hb) in enumerate(ROAD_EXT):
        if tb != "v":
            continue
        if not (la <= cb <= ha and lb <= ca <= hb):
            continue
        for su in (-1, 1):
            for sv in (-1, 1):
                arm_u = (ha > cb + 1) if su > 0 else (la < cb - 1)
                arm_v = (hb > ca + 1) if sv > 0 else (lb < ca - 1)
                if not (arm_u and arm_v):
                    continue
                if abs(la - 120 - cb) < 1 or abs(ha + 120 - cb) < 1:
                    continue
                pu, pv = cb + su * HW, ca + sv * HW
                arm_len = min((ha - cb) if su > 0 else (cb - la), (hb - ca) if sv > 0 else (ca - lb)) * K - HW * K
                for Rc in FIL_CANDIDATES:
                    poly_uv, arc = fillet_poly(pu, pv, su, sv, Rc / K)
                    if Rc / K <= arm_len / K + 1e-9 and fillet_clear(poly_uv):
                        break
                else:
                    Rc = FIL_CANDIDATES[-1]
                    poly_uv, arc = fillet_poly(pu, pv, su, sv, Rc / K)
                FIL_LOG[(cb, ca, su, sv)] = Rc
                fills.append(path(uvpath(poly_uv, True), f=ASPH))
                edges.append(path(uvpath(arc), s=STEEL, w=1))
CIV += fills + edges

# ---- one-way heavy-vehicle (HV) tanker circuit ------------------------------------------------------
def proj_on_poly(p, poly):
    best, bq, bi = 1e9, None, 0
    for i in range(len(poly)):
        a_, b_ = poly[i], poly[(i + 1) % len(poly)]
        dx, dy = b_[0] - a_[0], b_[1] - a_[1]
        t = max(0, min(1, ((p[0] - a_[0]) * dx + (p[1] - a_[1]) * dy) / (dx * dx + dy * dy)))
        q = (a_[0] + t * dx, a_[1] + t * dy)
        d_ = math.hypot(p[0] - q[0], p[1] - q[1])
        if d_ < best:
            best, bq, bi = d_, q, i
    return bq, bi


LANE_V = [GF.uv(BAY_X[k_] + BAY_W / 2, 0)[1] for k_ in range(4)]              # lane centre-lines (v)
LANE_ENTRY_U, LANE_EXIT_U = GF.uv(0, GANT_Y1)[0] - 1.0, GF.uv(0, GANT_Y0)[0]   # SE entry end / NW exit end
G1_IN, _g1i = proj_on_poly(GATES[0][3], ROADC)
G2_IN, _g2i = proj_on_poly(GATES[1][3], ROADC)
R06_FOOT = ROADS_PX[5][1][0]
assert R06_FOOT[0] < G1_IN[0] - 10, "exit road must reach the perimeter west of the HV entry gate"
LANE_PROJ = [proj_on_poly(uvp(LANE_ENTRY_U, v_), ROADC)[0] for v_ in LANE_V]
HV_ENTRY = [G1_IN, ROADC[5], ROADC[4], ROADC[3], LANE_PROJ[-1]]            # gate -> perimeter CCW -> gantry
HV_LANES = [[LANE_PROJ[k_], uvp(LANE_ENTRY_U, LANE_V[k_]), uvp(LANE_EXIT_U, LANE_V[k_])] for k_ in range(4)]
HV_EXIT = [uvp(LANE_EXIT_U, LANE_V[-1]), R06_FOOT, ROADC[6], G2_IN]
HV_YARD_MID = [lerp(YARD_PX[0], YARD_PX[3], 0.5), lerp(YARD_PX[1], YARD_PX[2], 0.5)]


def arrow_polys(pts_px, spacing=55.0, size=5.5, start=14.0):
    out = []
    pos = start
    for i in range(len(pts_px) - 1):
        a_, b_ = pts_px[i], pts_px[i + 1]
        L = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
        if L < 1e-6:
            continue
        d = ((b_[0] - a_[0]) / L, (b_[1] - a_[1]) / L)
        nrm = (-d[1], d[0])
        while pos < L:
            c = P(a_[0] + d[0] * pos, a_[1] + d[1] * pos)
            tip = (c[0] + d[0] * size, c[1] + d[1] * size)
            l_ = (c[0] - d[0] * size * .7 + nrm[0] * size * .75, c[1] - d[1] * size * .7 + nrm[1] * size * .75)
            r_ = (c[0] - d[0] * size * .7 - nrm[0] * size * .75, c[1] - d[1] * size * .7 - nrm[1] * size * .75)
            out.append(polyg([tip, l_, r_], f=INK, s=LIGHT, w=0.6))
            pos += spacing
        pos -= L
    return out


# inward gate throats: fence opening -> perimeter road
for gid, role, ei_, gp_ in GATES:
    q_, _i = proj_on_poly(gp_, ROADC)
    dx_, dy_ = q_[0] - gp_[0], q_[1] - gp_[1]
    L_ = math.hypot(dx_, dy_)
    nx2, ny2 = -dy_ / L_ * 11, dx_ / L_ * 11
    CIV.append(polyg([P(gp_[0] + nx2, gp_[1] + ny2), P(q_[0] + nx2, q_[1] + ny2), P(q_[0] - nx2, q_[1] - ny2), P(gp_[0] - nx2, gp_[1] - ny2)],
                     f=ASPH))
# staging / queuing yard (asphalt) + weighbridge on the entry lane
CIV.append(polyg([P(*q) for q in YARD_PX], f=ASPH, s=STEEL, w=1))
CIV.append(path(pts_path([P(*lerp(YARD_PX[0], YARD_PX[3], 0.5)), P(*lerp(YARD_PX[1], YARD_PX[2], 0.5))]), s=LIGHT, w=1.2, d="10 8", c=ZL2))
_d6 = edge_dirs(6)[0]
_wbc = (G1_IN[0] - _d6[0] * 30, G1_IN[1] - _d6[1] * 30)
_nn = (-_d6[1], _d6[0])
CIV.append(polyg([P(_wbc[0] + _d6[0] * s_ * 18 + _nn[0] * t_ * 6, _wbc[1] + _d6[1] * s_ * 18 + _nn[1] * t_ * 6)
                  for s_, t_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))], f=CONC, s=INK, w=1))
hv_arrows = (arrow_polys(HV_ENTRY, 60) + arrow_polys(HV_EXIT, 60) + arrow_polys(HV_YARD_MID, 40, 5, 10) +
             [p_ for ln in HV_LANES for p_ in arrow_polys(ln[1:], 40, 5, 12)])
CIV.append(G(hv_arrows))

# centre-line striping (L2)
stripes = [path(perim_d, s=LIGHT, w=1.2, d="12 9")]
for pl_ in road_lines:
    stripes.append(path(pts_path(pl_), s=LIGHT, w=1.2, d="12 9"))
CIV.append(G(stripes, c=ZL2))

# --- concrete bunds -------------------------------------------------------------------------
BUNDU = {}
for k_, poly in BUNDS.items():
    outer = [P(*q) for q in poly]
    inner = [P(*q) for q in offset_poly(poly, WALL_PX)]
    BUNDU[k_] = (outer, inner)
    wall = pts_path(outer, True) + " " + pts_path(inner, True)
    CIV.append(path(pts_path(inner, True), f=BUNDFILL))
    CIV.append(path(wall, f=CONC, fill_rule="evenodd"))
    CIV.append(path(wall, f="url(#hatch-concrete)", fill_rule="evenodd", s=INK, w=1.2))

# internal fire-break walls: central compound (between rows) and NE farm (between rows)
def wall_line(u0, u1, v0, v1, t=2.0):
    return polyg([UVu(u0, v0), UVu(u1, v0), UVu(u1, v1), UVu(u0, v1)], f=CONC, s=INK, w=0.8)


for ub in (431, 493, 555):
    CIV.append(wall_line(ub - 1.2, ub + 1.2, 126 + WALL_PX, 254 - WALL_PX))
# sumps (one per bund, lowest corner = nearest the retention basin side)
SUMPS = {"SW": (560, -20), "ST": (620, 70), "CE": (600, 244), "NE1": (562, 412), "NE2": (668, 418)}
sump_el = []
for k_, (su_, sv_) in SUMPS.items():
    c = UVu(su_, sv_)
    sump_el.append(rect(c[0] - 6, c[1] - 6, 12, 12, f=PALE, s=INK, w=1))
CIV.append(G(sump_el))
CIV.append(G([G([line(UVu(su_, sv_)[0] - 6, UVu(su_, sv_)[1] - 6, UVu(su_, sv_)[0] + 6, UVu(su_, sv_)[1] + 6, s=INK, w=0.5),
                 line(UVu(su_, sv_)[0] - 6, UVu(su_, sv_)[1] + 6, UVu(su_, sv_)[0] + 6, UVu(su_, sv_)[1] - 6, s=INK, w=0.5)])
              for (su_, sv_) in SUMPS.values()], c=ZL3))

# --- sleeperway concrete strips + road-crossing sleeves ---------------------------------------
def split_bands(a, b, bands):
    return split(a, b, bands)


sl, sleeves = [], []
for ax, c, a, b in SLEEPERS:
    bands = []
    for (t, cc, lo, hi) in ROAD_EXT:
        if ax == "v" and t == "u" and lo <= c <= hi:
            bands.append((cc - HW, cc + HW))
        if ax == "u" and t == "v" and lo <= c <= hi:
            bands.append((cc - HW, cc + HW))
    for p, q in split_bands(a, b, bands):
        if ax == "v":
            sl.append(polyg([UVu(c - HW, p), UVu(c + HW, p), UVu(c + HW, q), UVu(c - HW, q)], f=CONC, s=STEEL, w=0.8))
        else:
            sl.append(polyg([UVu(p, c - HW), UVu(p, c + HW), UVu(q, c + HW), UVu(q, c - HW)], f=CONC, s=STEEL, w=0.8))
    for (b0, b1) in bands:
        if not (a < b0 and b1 < b):
            continue
        if ax == "v":
            sleeves.append(polyg([UVu(c - HW - 2, b0 - 2), UVu(c + HW + 2, b0 - 2), UVu(c + HW + 2, b1 + 2), UVu(c - HW - 2, b1 + 2)],
                                s=STEEL, w=1, d="4 2"))
        else:
            sleeves.append(polyg([UVu(b0 - 2, c - HW - 2), UVu(b1 + 2, c - HW - 2), UVu(b1 + 2, c + HW + 2), UVu(b0 - 2, c + HW + 2)],
                                s=STEEL, w=1, d="4 2"))
CIV.append(G(sl))
CIV.append(G(sleeves, c=ZL2))

# --- pump pad, manifold pad (rotated frames) -----------------------------------------------------
corr = []
for i in range(5):
    xa = PUMP_X0 + PUMP_PITCH * i + 28
    corr.append(rect(xa, 6, PUMP_PITCH - 28, 88, f="url(#hatch-light)", s=MID, w=0.6, d="3 2"))
corr.append(text(125, 98, "6 m MAINTENANCE CORRIDORS", size=5.5, anchor="middle"))
CIV.append(PF.g([rect(0, 0, 250, 100, f=CONC, s=STEEL, w=1),
                 G([rect(4, 4, 242, 92, s=STEEL, w=0.6, d="5 3")] + corr, c=ZL2)]))
CIV.append(MF.g([rect(0, 0, 150, 80, f=CONC, s=STEEL, w=1), rect(4, 4, 142, 72, s=STEEL, w=0.6, d="5 3", c=ZL2)]))

# --- retention / OWS basin ---------------------------------------------------------------------------
bu0, bu1, bv0, bv1 = BASIN
CIV.append(polyg([UVu(bu0, bv0), UVu(bu1, bv0), UVu(bu1, bv1), UVu(bu0, bv1)], f="#D0D4DB", s=STEEL, w=1.4))
CIV.append(G([polyg([UVu(bu0 + k_, bv0 + k_), UVu(bu1 - k_, bv0 + k_), UVu(bu1 - k_, bv1 - k_), UVu(bu0 + k_, bv1 - k_)],
                   s=STEEL, w=0.5, d="4 3") for k_ in (6, 12, 18)], c=ZL2))

# --- truck gantry: apron + concrete islands --------------------------------------------------------------
CIV.append(GF.g([rect(-12, GANT_Y0, GANT_W + 24, GANT_Y1 - GANT_Y0, f=ASPH, s=STEEL, w=1)] +
                [rect(xi, 15, ISL_W, 110, rx=3, f=PALE, s=INK, w=1) for xi in ISL_X]))
CIV.append(GF.g([line(x, GANT_Y0, x, GANT_Y1, s=LIGHT, w=0.8, d="8 4") for x in (BAY_X[0] - 1, BAY_X[-1] + BAY_W + 1)], c=ZL2))

# --- parking ------------------------------------------------------------------------------------------------

# ==========================================================================
#                                L-STRUCT
# ==========================================================================
def stair(cx, cy, r, a0, sweep, wd=5.0, step=3.0):
    r1, r2 = r + 0.8, r + 0.8 + wd
    a1 = a0 + sweep
    base = path(arc_band(cx, cy, r1, r2, a0, a1), f=PALE, s=INK, w=0.8)
    plat = path(arc_band(cx, cy, r1, r2 + 6, a1 - 3, a1 + 10), f=WHITE, s=INK, w=0.9, c=ZL2)
    treads = G([line(*polar(cx, cy, r1, a), *polar(cx, cy, r2, a), s=INK, w=0.4)
                for a in frange(a0 + step, a1 - step, step)], c=ZL3)
    return [base, plat, treads]


# rack bents along every sleeperway (L2)
bents = []
for ax, c, a, b in SLEEPERS:
    bands = [(cc - HW, cc + HW) for (t, cc, lo, hi) in ROAD_EXT
             if (ax == "v" and t == "u" and lo <= c <= hi) or (ax == "u" and t == "v" and lo <= c <= hi)]
    pos = a + 8
    while pos <= b - 6:
        if not any(x0 - 2 <= pos <= x1 for x0, x1 in bands):
            if ax == "v":
                bents.append(polyg([UVu(c - HW, pos), UVu(c + HW, pos), UVu(c + HW, pos + 2), UVu(c - HW, pos + 2)],
                                  f=STEEL, s=INK, w=0.3))
            else:
                bents.append(polyg([UVu(pos, c - HW), UVu(pos, c + HW), UVu(pos + 2, c + HW), UVu(pos + 2, c - HW)],
                                  f=STEEL, s=INK, w=0.3))
        pos += 20
CIV.append(G(bents, c=ZL2))

# gantry canopy, columns, bollards, stair tower (local frame)
canopy = [rect(-6, 25, GANT_W + 12, 90, f="none", s=STEEL, w=1.6, d="10 4")]
cols = []
for xi in ISL_X:
    xc = xi + ISL_W / 2
    for yc in (33, 107):
        cols.append(rect(xc - 3, yc - 3, 6, 6, f=STEEL, s=INK, w=0.6))
    for off in (-4, 4):
        for yb in (19, 121):
            cols.append(circle(xc + off, yb, 2, f=INK))
beams = [line(5, yc, GANT_W - 5, yc, s=STEEL, w=0.7, d="6 3") for yc in (33, 107)]
beams += [line(xi + 7, 33, xi + 7, 107, s=STEEL, w=0.7, d="6 3") for xi in ISL_X]
CIV.append(GF.g(canopy + cols))
CIV.append(GF.g(beams, c=ZL2))
CIV.append(GF.g([rect(GANT_W + 14, 40, 16, 44, f=WHITE, s=INK, w=1)] +
                [G([line(GANT_W + 14, yy, GANT_W + 30, yy, s=INK, w=0.4) for yy in range(43, 84, 3)], c=ZL3)]))

# buildings (+ roof overhang L2, structural grid L3)
for name, (a0, a1, b0, b1) in BLDG.items():
    CIV.append(polyg([UVu(a0, b0), UVu(a1, b0), UVu(a1, b1), UVu(a0, b1)], f=PALE, s=INK, w=1.6))
    CIV.append(polyg([UVu(a0 - 2, b0 - 2), UVu(a1 + 2, b0 - 2), UVu(a1 + 2, b1 + 2), UVu(a0 - 2, b1 + 2)], s=MID, w=0.7, d="5 3", c=ZL2))
GATEHOUSES = {}
for gid, ei_, off_ in (("G1", 6, 16), ("G2", 7, 16)):
    d_, nout_ = edge_dirs(ei_)
    gp_ = [g_ for g_ in GATES if g_[0] == gid][0][3]
    cc = (gp_[0] - nout_[0] * (HW + 11) + d_[0] * off_, gp_[1] - nout_[1] * (HW + 11) + d_[1] * off_)
    GATEHOUSES[gid] = [(cc[0] + d_[0] * s_ * 9 - nout_[0] * t_ * 6, cc[1] + d_[1] * s_ * 9 - nout_[1] * t_ * 6)
                       for s_, t_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    CIV.append(polyg([P(*q) for q in GATEHOUSES[gid]], f=PALE, s=INK, w=1.4))

# ==========================================================================
#                                L-MECH
# ==========================================================================
STAIRS_BUF = []


def tank_fr(t):
    tag, u, v, rp, kind, Hm, av = t
    cx, cy = UVu(u, v)
    r = rp * K
    sw = 120.0
    a0 = av + 180 - sw / 2
    els = [circle(cx, cy, r, f=WHITE, s=INK, w=2.2), circle(cx, cy, r - 2, s=STEEL, w=0.7, c=ZL2),
           circle(cx, cy, r * 0.92, s=STEEL, w=0.9, c=ZL2), circle(cx, cy, r * 0.78, s=STEEL, w=0.9, c=ZL2),
           G([line(*polar(cx, cy, r * .92, a), *polar(cx, cy, r * .78, a), s=STEEL, w=0.6)
              for a in frange(0, 337.5, 22.5)], c=ZL2)]
    a_end = a0 + sw
    ax_, ay_ = polar(cx, cy, r, a_end)
    bx_, by_ = polar(cx, cy, r * 0.3, a_end)
    nx_, ny_ = -math.sin(math.radians(a_end)), math.cos(math.radians(a_end))
    els.append(G([line(ax_ + nx_ * 1.6, ay_ + ny_ * 1.6, bx_ + nx_ * 1.6, by_ + ny_ * 1.6, s=INK, w=0.8),
                  line(ax_ - nx_ * 1.6, ay_ - ny_ * 1.6, bx_ - nx_ * 1.6, by_ - ny_ * 1.6, s=INK, w=0.8)], c=ZL2))
    micro = [circle(cx, cy, 4, f=PALE, s=INK, w=0.8)]
    for rr_, cnt in ((r * .45, 10), (r * .65, 16)):
        micro += [circle(*polar(cx, cy, rr_, k_ * 360 / cnt), 1.1, f=STEEL) for k_ in range(cnt)]
    micro.append(line(*polar(cx, cy, r + 14, av), *polar(cx, cy, r - 12, av), s=INK, w=0.5, d=DASHDOT))
    micro.append(circle(*polar(cx, cy, r - 1, av), 2.2, f=WHITE, s=INK, w=0.8))
    for a in (av + 60, av - 60):
        mx, my = polar(cx, cy, r + 5, a)
        micro.append(rect(mx - 4, my - 2.5, 8, 5, f=WHITE, s=INK, w=0.7))
    els.append(G(micro, c=ZL3))
    STR.extend(stair(cx, cy, r, a0, sw, wd=5.0, step=2.5))
    return G(els,
             data_cmp_id="CMP-EQP-TANK",
             data_func_loc=f"TFA-CSS-{tag}",
             data_equip_id=f"EQ-{tag}-A",
             data_shell_diam_m=M(r * 2),
             data_tank_height_m=Hm,
             data_design_std="API-650",
             data_status="E",
             c="dt-interactive")


def tank_cone(t):
    tag, u, v, rp, kind, Hm, av = t
    cx, cy = UVu(u, v)
    r = rp * K
    sw = 140.0
    a0 = av + 180 - sw / 2
    els = [circle(cx, cy, r, f=WHITE, s=INK, w=2.0), circle(cx, cy, r - 2.5, s=STEEL, w=0.7, c=ZL2),
           circle(cx, cy, r * 0.5, s=STEEL, w=0.6, c=ZL2), circle(cx, cy, 4, f=PALE, s=INK, w=0.9),
           G([line(*polar(cx, cy, 4, a), *polar(cx, cy, r - 2.5, a), s=STEEL, w=0.4) for a in frange(0, 345, 15)], c=ZL2)]
    micro = [circle(*polar(cx, cy, r * .72, av + 90), 2.6, f=WHITE, s=INK, w=0.7),
             circle(*polar(cx, cy, r * .72, av + 150), 1.8, f=WHITE, s=INK, w=0.7)]
    for a in (av + 40, av - 40):
        fx_, fy_ = polar(cx, cy, r - 1, a)
        micro.append(rect(fx_ - 3, fy_ - 2, 6, 4, f=PALE, s=INK, w=0.6))
    micro.append(line(*polar(cx, cy, r + 14, av), *polar(cx, cy, r - 12, av), s=INK, w=0.5, d=DASHDOT))
    micro.append(circle(*polar(cx, cy, r - 1, av), 2, f=WHITE, s=INK, w=0.8))
    els.append(G(micro, c=ZL3))
    STR.extend(stair(cx, cy, r, a0, sw, wd=4.0, step=3.0))
    return G(els,
             data_cmp_id="CMP-EQP-TANK",
             data_func_loc=f"TFA-CSS-{tag}",
             data_equip_id=f"EQ-{tag}-A",
             data_shell_diam_m=M(r * 2),
             data_tank_height_m=Hm,
             data_design_std="API-650",
             data_status="E",
             c="dt-interactive")


for t in ALL_TANKS:
    MEC.append(tank_fr(t) if t[4] == "FR" else tank_cone(t))

# pump skids
for i, tag in enumerate(PUMP_TAGS):
    x, y = PUMP_X0 + PUMP_PITCH * i, PUMP_Y
    els = [rect(0, 0, 40, 20, f=PALE, s=INK, w=1, c=ZL2), circle(11, 10, 7.5, f=WHITE, s=INK, w=1.4),
           rect(24, 3, 15, 14, rx=2, f=WHITE, s=INK, w=1.2),
           G([rect(19, 7, 5, 6, f=MID, s=INK, w=0.6), rect(29, -1, 6, 4, f=PALE, s=INK, w=0.6),
              line(-4, 10, 44, 10, s=INK, w=0.5, d=DASHDOT)] +
             [line(xx, 3, xx, 17, s=INK, w=0.3) for xx in (27, 29.5, 32, 34.5, 37)] +
             [circle(bx, by, 1, f=INK) for bx, by in ((3, 3), (37, 3), (3, 17), (37, 17))], c=ZL3)]
    MEC.append(PF.g([G(els,
                       data_cmp_id="CMP-EQP-PUMP",
                       data_func_loc=f"TFA-CSS-{tag}",
                       data_equip_id=f"EQ-{tag}-A",
                       data_status="E",
                       c="dt-interactive",
                       transform=f"translate({x} {y}) scale({PUMP_S})")]))

# fire-water pumps in pump house
fw0, fw1, fv0, fv1 = BLDG["FW PUMP HOUSE"]
MEC.append(G([circle(*UVu((fw0 + fw1) / 2, fv0 + 6 + 9 * k_), 3.6, f=WHITE, s=INK, w=1) for k_ in range(3)], c=ZL2))

# truck loading bays
for k_, xl in enumerate(BAY_X):
    tag = f"BAY-{k_ + 1:02d}"
    arm_x, bay_c = ISL_X[k_] + ISL_W / 2, xl + BAY_W / 2
    els = [rect(xl, 15, BAY_W, 110, s=INK, w=1),
           G([line(xl, GANT_Y0, xl, GANT_Y1, s=MID, w=0.6, d="8 4"), line(xl + BAY_W, GANT_Y0, xl + BAY_W, GANT_Y1, s=MID, w=0.6, d="8 4"),
              rect(bay_c - 6.5, 30, 13, 60, rx=5, f=WHITE, s=STEEL, w=0.9),
              rect(bay_c - 5.5, 92, 11, 16, rx=2, f=WHITE, s=STEEL, w=0.9),
              line(xl + 2, 24, xl + BAY_W - 2, 24, s=INK, w=0.8, d="3 2")], c=ZL2),
           G([circle(bay_c, yy, 1.8, f=WHITE, s=INK, w=0.6) for yy in (45, 60, 75)] +
             [circle(arm_x, 70, 26, s=STEEL, w=0.7, d="4 3"), circle(arm_x, 70, 3, f=INK),
              line(arm_x, 70, bay_c, 60, s=INK, w=1.6)], c=ZL3)]
    MEC.append(GF.g([G(els,
                       data_cmp_id="CMP-EQP-BAY",
                       data_func_loc=f"TFA-TLG-{tag}",
                       data_equip_id=f"EQ-{tag}-A",
                       data_status="E",
                       c="dt-interactive")]))

# ==========================================================================
#                                L-PIPE
# ==========================================================================
# --- SN trunk with expansion loops (project to -u), SA, SB, SR sleeper trunks ----------
def trunk_v(c_u, v0, v1, loops, depth_sign, line_off, kind):
    """Trunk along v at u=c_u+line_off with U-loops projecting depth_sign*(depth) in u."""
    pts = [(c_u + line_off, v0)]
    for vc, wd, dp in sorted(loops):
        pts += [(c_u + line_off, vc - wd / 2), (c_u + line_off + depth_sign * dp, vc - wd / 2),
                (c_u + line_off + depth_sign * dp, vc + wd / 2), (c_u + line_off, vc + wd / 2)]
    pts.append((c_u + line_off, v1))
    return pts


SN_A = trunk_v(346, -82, 296, [(-30, 36, 14), (190, 36, 14)], -1, 0, "A")
PIP.append(pipe(SN_A, "A", 3.0))                       # SN  : farm outlet header -> SA / SR
PIP.append(pipe([(346, 111), (672, 111)], "A", 3.0))     # SA  : trunk to the pump station
PIP.append(pipe([(672, 20), (672, 264)], "A", 3.0))      # SB  : trunk past pump suction and manifold
PIP.append(pipe([(346, 290), (600, 290)], "A", 3.0))     # SR  : trunk along the TF3 / TF4 corridor

# --- farm collectors and tank stubs -------------------------------------------------------------
def collector(pts, w=2.4):
    PIP.append(pipe(pts, "A", w))


def stub_v(t, vc):        # stub along v from shell to collector at v=vc
    tag, u, v, rp, *_ = t
    s = 1 if vc > v else -1
    PIP.append(pipe([(u, v + s * rp), (u, vc)], "A", 2.0))
    STUBS[tag] = PIPE_NET[-1]
    flange((u, v + s * (rp + 1.5)), "v", 3.6)


def stub_u(t, uc):
    tag, u, v, rp, *_ = t
    s = 1 if uc > u else -1
    PIP.append(pipe([(u + s * rp, v), (uc, v)], "A", 2.0))
    STUBS[tag] = PIPE_NET[-1]
    flange((u + s * (rp + 1.5), v), "u", 3.6)


sw = TKS["SW"]
collector([(488, -77), (346, -77)])
STUBS["TK-0105"] = PIPE_NET[-1]          # the big tank is fed directly by the end of its collector
for t in sw[:4]:
    stub_v(t, -77)
valve((366, -77), "u")
st = TKS["ST"]
collector([(602, 74), (346, 74)])
for t in st:
    stub_v(t, 74)
valve((392, 74), "u")
for vc in (170, 210):
    collector([(586, vc), (346, vc)])
    valve((386, vc), "u")
for t in TKS["CE"]:
    stub_v(t, 170 if t[2] <= 190 else 210)
ne_small = [t for t in TKS["NE"] if t[3] == 15]
collector([(522, 290), (522, 398)])
for t in ne_small:
    stub_u(t, 522)
valve((522, 312), "v")
collector([(600, 290), (600, 364.5), (642, 364.5)])
for t in TKS["NE"][-2:]:
    stub_v(t, 364.5)
valve((620, 364.5), "u")

# --- pump-station piping (suction north, discharge south) -------------------------------------------
xcs = [PUMP_X0 + PUMP_PITCH * i + 11 * PUMP_S for i in range(6)]
SUC_U = PF.uv(0, 20)[0]
DIS_U = PF.uv(0, 76)[0]
PIP.append(pipe([(672, 122), (SUC_U, 122), (SUC_U, PF.uv(xcs[-1], 20)[1])], "A", 3.0))
PIP.append(pipe([(DIS_U, PF.uv(xcs[0], 0)[1]), (DIS_U, MF.uv(4, 0)[1])], "A", 3.0))
for xc in xcs:
    PIP.append(pipe([PF.uv(xc, 20), PF.uv(xc, PUMP_Y + 5.25 - 1.5)], "A", 2.2))
    PIP.append(pipe([PF.uv(xc, PUMP_Y + 14 - 5.25 + 1.5), PF.uv(xc, 76)], "A", 2.2))
    valve(PF.uv(xc, 30), "u", 4)
    check_valve(PF.uv(xc, 62), "u")
    valve(PF.uv(xc, 69), "u", 4)
    flange(PF.uv(xc, 40), "u")
    flange(PF.uv(xc, 58), "u")
valve((680, 122), "u", 4)

# --- manifold block: 5 headers + valve ladders ---------------------------------------------------------
MH = [12 + 14 * k_ for k_ in range(5)]
for k_, yy in enumerate(MH):
    x_end = 146
    PIP.append(pipe([MF.uv(4, yy), MF.uv(x_end, yy)], "A" if k_ % 2 == 0 else "B", 2.6))
    for xv in (16, 134):
        valve(MF.uv(xv, yy), "v", 4)
    if k_ >= 3:
        flange(MF.uv(x_end, yy), "v")
for xt in (50, 100):
    for a_, b_ in zip(MH[:-1], MH[1:]):
        PIP.append(pipe([MF.uv(xt, a_), MF.uv(xt, b_)], "A", 1.6))
        valve(MF.uv(xt, (a_ + b_) / 2), "u", 3.6)
PIP.append(pipe([(672, 262), (MF.uv(0, MH[0])[0], 262), MF.uv(4, MH[0])], "A", 2.6))
# manifold -> gantry loading header
G_A = GF.uv(0, 5)
PIP.append(pipe([MF.uv(146, MH[2]), (MF.uv(146, MH[2])[0], 358), (G_A[0], 358), G_A], "A", 2.8))
valve((MF.uv(146, MH[2])[0], 350), "v", 4)
PIP.append(pipe([GF.uv(0, 5), GF.uv(GANT_W - 6, 5)], "A", 2.8))
for k_ in range(4):
    xa = ISL_X[k_] + ISL_W / 2
    PIP.append(pipe([GF.uv(xa, 5), GF.uv(xa, 70)], "A", 2.4))
    valve(GF.uv(xa, 40), "u", 4)
    flange(GF.uv(xa, 62), "u")
# R-06 crossing sleeves for suction / manifold branches
for (a_, b_) in [(122, 122), (262, 262)]:
    sleeves_extra = polyg([UVu(690 - HW - 2, a_ - 8), UVu(690 + HW + 2, a_ - 8), UVu(690 + HW + 2, a_ + 8), UVu(690 - HW - 2, a_ + 8)],
                         s=STEEL, w=1, d="4 2")
    CIV.append(G([sleeves_extra], c=ZL2))

PIP.append(G(VAL2, c=ZL2))
PIP.append(G(VAL3, c=ZL3))
PIP.append(G(FLG, c=ZL3))

# ==========================================================================
#                                L-FIRE
# ==========================================================================
mains = [path(pts_path([P(*q) for q in RINGM], True), s=STEEL, w=2.4, d="16 4 3 4")]
main_segs = [(RINGM[i], RINGM[(i + 1) % len(RINGM)]) for i in range(len(RINGM))]
for (rid, pts), (_, pu, _s0, _s1) in zip(ROADS_PX, ROADS):
    (u1, v1), (u2, v2) = pu[0], pu[-1]
    da = uvp(0, 6) if v1 == v2 else uvp(6, 0)           # underground main 6 px beside the road centre-line
    sa = (pts[0][0] + da[0], pts[0][1] + da[1])
    sb = (pts[-1][0] + da[0], pts[-1][1] + da[1])
    mains.append(path(pts_path([P(*sa), P(*sb)]), s=STEEL, w=2.0, d="16 4 3 4"))
    main_segs.append((sa, sb))
FIR.append(G(mains))


def nearest_main(p):
    best, bp = 1e9, None
    for a, b in main_segs:
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy)))
        q = (ax + t * dx, ay + t * dy)
        d = math.hypot(p[0] - q[0], p[1] - q[1])
        if d < best:
            best, bp = d, q
    return bp


# hydrants: perimeter line (between fence and road) + beside internal roads
hyd = []
acc = 0.0
for i in range(len(HYDR)):
    a, b = HYDR[i], HYDR[(i + 1) % len(HYDR)]
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    pos = 20 - acc
    while pos < L:
        t = pos / L
        q = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        if math.hypot(q[0] - GATE_PX[0], q[1] - GATE_PX[1]) > 22 and pip(q, BND) and dist_poly(q, BND) > 3:
            hyd.append((q, "perim"))
        pos += 80
    acc = (pos - L)
for (rid, pts) in ROADS_PX:
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        ux_, uy_ = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        nx_, ny_ = -uy_, ux_
        pos, side = 30, 1
        while pos < L - 15:
            for sgn in (side, -side):
                q = (a[0] + ux_ * pos + nx_ * 11.5 * sgn, a[1] + uy_ * pos + ny_ * 11.5 * sgn)
                if free(q):
                    hyd.append((q, "road"))
                    break
            pos += 90
            side = -side
hyd_sym, hyd_spur, hyd_tag = [], [], []
for i, (q, kind) in enumerate(hyd, 1):
    x, y = P(*q)
    hyd_sym += [circle(x, y, 4.5, f=WHITE, s=INK, w=1.2), circle(x, y, 1.4, f=INK)]
    m_ = nearest_main(q)
    if m_ is not None and math.hypot(q[0] - m_[0], q[1] - m_[1]) < 25:
        hyd_spur.append(line(x, y, *P(*m_), s=STEEL, w=1.2))
    hyd_tag.append(text(x + 6, y - 5, f"FH-{i:02d}", size=5.5))
FIR.append(G(hyd_sym))
FIR.append(G(hyd_spur, c=ZL2))
FIR.append(G(hyd_tag, c=ZL3))

# foam monitor towers: two diagonal corners of every bund (on the wall), plus pump/gantry
fm_list = []
for k_, poly_ in BUNDS.items():
    cen = (sum(q[0] for q in poly_) / len(poly_), sum(q[1] for q in poly_) / len(poly_))
    best, pair = -1, None
    for i in range(len(poly_)):
        for j in range(i + 1, len(poly_)):
            d = math.hypot(poly_[i][0] - poly_[j][0], poly_[i][1] - poly_[j][1])
            if d > best:
                best, pair = d, (i, j)
    for idx in pair:
        q = poly_[idx]
        d = (cen[0] - q[0], cen[1] - q[1])
        L = math.hypot(*d)
        fm_list.append((q[0] + d[0] / L * 3.5, q[1] + d[1] / L * 3.5))
fm_list += [uvp(705, 254), uvp(676, 470)]
cov, fm_sp, fm_sym, fm_tag = [], [], [], []
for i, q in enumerate(fm_list, 1):
    x, y = P(*q)
    cov.append(circle(x, y, U(50), s=MID, w=0.7, d="10 6", o=0.5))
    m_ = nearest_main(q)
    fm_sp.append(line(x, y, *P(*m_), s=STEEL, w=1.4, d="6 3"))
    fm_sym += [rect(x - 5, y - 5, 10, 10, f=WHITE, s=INK, w=1.3), line(x - 5, y - 5, x + 5, y + 5, s=INK, w=0.8),
               line(x - 5, y + 5, x + 5, y - 5, s=INK, w=0.8), circle(x, y, 2, f=INK)]
    fm_tag.append(text(x + 8, y + 3, f"FM-{i:02d}", size=6))
FIR.append(G(cov, c=ZL2))
FIR.append(G(fm_sp, c=ZL2))
FIR.append(G(fm_sym))
FIR.append(G(fm_tag, c=ZL2))

# ==========================================================================
#                                L-ANNO
# ==========================================================================
# coordinate grid (40 m modules) with bubbles on all four sides
grid, bub = [], []
for k_, x in enumerate(range(200, 1801, 200)):
    grid.append(line(x, 26, x, H - 26, s=MID, w=0.5, d="2 6", o=0.7))
    for yb in (17, H - 17):
        bub += [circle(x, yb, 9, f=WHITE, s=INK, w=0.8), text(x, yb + 3, "ABCDEFGHI"[k_], size=8, anchor="middle")]
for k_, y in enumerate(range(200, 1401, 200)):
    grid.append(line(26, y, W - 26, y, s=MID, w=0.5, d="2 6", o=0.7))
    for xb in (17, W - 17):
        bub += [circle(xb, y, 9, f=WHITE, s=INK, w=0.8), text(xb, y + 3, str(k_ + 1), size=8, anchor="middle")]
ANN.append(G(grid, c=ZL2))
ANN.append(G(bub))

# tank tags
for t in ALL_TANKS:
    cx, cy = UVu(t[1], t[2])
    r = t[3] * K
    big = r > 44
    ANN.append(text(cx, cy + (2 if not big else -3), t[0], size=14 if big else (8.5 if r > 30 else 7.5), anchor="middle", weight="bold"))
    if big:
        ANN.append(text(cx, cy + 13, f"Ø{2*r*M_PER_UNIT:.0f} m · {'FLOATING' if t[4]=='FR' else 'CONE'} ROOF", size=7, anchor="middle"))

# zone bubbles + key
ZONES = [("1", "TANK FARM 1 — CRUDE OIL (CLASS I) · FLOATING ROOF", (470, -77)),
         ("2", "TANK FARM 2 — DIESEL · CONE ROOF", (506, 52)),
         ("3", "TANK FARM 3 — REFINED PRODUCTS · CONE ROOF", (493, 190)),
         ("4", "TANK FARM 4 — PRODUCTS (CONE) + CRUDE FR", (520, 362)),
         ("5", "MANIFOLD & PUMP STATION", (727, 185)),
         ("6", "TRUCK LOADING GANTRY (4 BAYS)", (700, 428)),
         ("7", "MCR · FIRE WATER · OWS BASIN · HV SUBSTATION", (800, 255)),
         ("8", "SERVICES — MAINTENANCE WAREHOUSE · LUBE STORE", (408, 372))]
zb = []
for num, name, (zu, zv) in ZONES:
    x, y = UVu(zu, zv)
    zb += [circle(x, y, 12, f=INK), text(x, y + 4.5, num, size=13, anchor="middle", weight="bold", f=LIGHT)]
ANN.append(G(zb))

# equipment labels (L2 where small)
ANN.append(G([text(*PF.pt(PUMP_X0 + PUMP_PITCH * i + 2, 38), t, size=6, weight="bold") for i, t in enumerate(PUMP_TAGS)], c=ZL2))
for k_, xl in enumerate(BAY_X):
    ANN.append(text(*GF.pt(xl + BAY_W / 2, 140), f"BAY-{k_ + 1:02d}", size=7.5, anchor="middle", weight="bold"))
ANN.append(text(*MF.pt(75, 90), "MANIFOLD M-0101 · 5 HDRS", size=6.5, anchor="middle", weight="bold"))
BLDG_SHORT = {"MCR": "MCR", "FAR": "FAR", "HV SUB": "HV SUB", "MCC-1": "MCC-1", "MCC-2": "MCC-2", "MCC-3": "MCC-3",
              "WH-01": "WH-01", "WH-02": "WH-02", "FW PUMP HOUSE": "FWPH"}
for name, (a0, a1, b0, b1) in BLDG.items():
    ANN.append(text(*UVu((a0 + a1) / 2, (b0 + b1) / 2 + 1.5), BLDG_SHORT[name], size=6.2, anchor="middle", weight="bold"))
    ANN.append(G([text(*UVu((a0 + a1) / 2, (b0 + b1) / 2 - 6), BLDG_INFO[name][0], size=4.6, anchor="middle")], c=ZL2))
ANN.append(G([text(*UVu((BASIN[0] + BASIN[1]) / 2, (BASIN[2] + BASIN[3]) / 2), "RETENTION / OWS BASIN", size=7, anchor="middle", weight="bold")]))
for gid, role, ei_, gp_ in GATES:
    (gx_, gy_), d_, nout_ = GATE_U[gid]
    ANN.append(text(gx_ + nout_[0] * 40, gy_ + nout_[1] * 40 + 2, f"{gid} · {role}", size=8, anchor="middle", weight="bold"))
ANN.append(G([text(*P(*lerp(GATEHOUSES["G1"][0], GATEHOUSES["G1"][2], 0.5)), "GATE-HOUSE", size=4.8, anchor="middle"),
              text(*P(*lerp(GATEHOUSES["G2"][0], GATEHOUSES["G2"][2], 0.5)), "GATE-HOUSE", size=4.8, anchor="middle"),
              text(*P(_wbc[0], _wbc[1] + 11), "WEIGHBRIDGE", size=5.5, anchor="middle")], c=ZL2))
_yc = lerp(lerp(YARD_PX[0], YARD_PX[3], 0.5), lerp(YARD_PX[1], YARD_PX[2], 0.5), 0.5)
ANN.append(text(*P(_yc[0] - 17, _yc[1] + 4), "HV STAGING / QUEUE (one-way)", size=6.5, anchor="middle", weight="bold", rot=-88))
ANN.append(G([text(*UVu(735, LANE_V[0] - 14), "LANE 1-4  (one-way, SE → NW)", size=6, anchor="start", rot=ROT)], c=ZL2))
ANN.append(G([text(*UVu(690 + 1.5, 200), "HV EXIT — ONE-WAY SOUTH", size=6, anchor="middle", rot=ROT)], c=ZL2))
ANN.append(text(*P(700, 548), "PUBLIC ROAD", size=8, anchor="middle", rot=-11.3))
ANN.append(G([text(*UVu(430, 8 + 1.5), "R-01 · 6.0 m FIRE ACCESS", size=6.5, anchor="middle", rot=GRID_DEG),
              text(*UVu(520, 92 + 1.5), "R-02", size=6.5, anchor="middle", rot=GRID_DEG),
              text(*UVu(364 + 1.5, 170), "R-03", size=6.5, anchor="middle", rot=ROT),
              text(*UVu(520, 273 + 1.5), "R-04", size=6.5, anchor="middle", rot=GRID_DEG),
              text(*UVu(690 + 1.5, 330), "R-06", size=6.5, anchor="middle", rot=ROT),
              text(*UVu(585 + 1.5, 440), "R-07", size=6.5, anchor="middle", rot=ROT),
              text(*UVu(450, 111 - 5.0), "SLEEPERWAY SA · HEADERS A/B", size=6, anchor="middle", rot=GRID_DEG),
              text(*UVu(346 - 6, 120), "SN · TRUNK", size=6, anchor="middle", rot=ROT),
              text(*UVu(346 - 20, -30), "EXP. LOOP", size=5.5, anchor="middle", rot=ROT),
              text(*UVu(346 - 20, 190), "EXP. LOOP", size=5.5, anchor="middle", rot=ROT)], c=ZL2))

# dimensions (shell-to-shell spacing) — SW and NE examples
def dim_uv(a, b, label):
    (x1, y1), (x2, y2) = UVu(*a), UVu(*b)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return G([line(x1, y1, x2, y2, s=INK, w=0.6), circle(x1, y1, 1.6, f=INK), circle(x2, y2, 1.6, f=INK),
              text(mx, my - 4, label, size=6.5, anchor="middle")], c=ZL2)


def gap_m(t1, t2):
    return (math.hypot(t1[1] - t2[1], t1[2] - t2[2]) - t1[3] - t2[3]) * K * M_PER_UNIT


ANN.append(dim_uv((396 + 0, -110 + 24), (402, -44 - 23), f"{gap_m(sw[0], sw[1]):.1f} m"))
ANN.append(dim_uv((400, 150 + 14), (400, 190 - 14), f"{gap_m(TKS['CE'][0], TKS['CE'][1]):.1f} m"))

# compass rose (plant north = up), scale bar, bund data, title block, legend
cr_x, cr_y = 120, 520
ANN.append(G([circle(cr_x, cr_y, 36, s=INK, w=1), circle(cr_x, cr_y, 3, f=INK),
              polyg([(cr_x, cr_y - 36), (cr_x - 7, cr_y), (cr_x + 7, cr_y)], f=INK),
              polyg([(cr_x, cr_y + 36), (cr_x - 7, cr_y), (cr_x + 7, cr_y)], f=WHITE, s=INK, w=0.8),
              line(cr_x - 36, cr_y, cr_x + 36, cr_y, s=INK, w=0.8),
              text(cr_x, cr_y - 41, "N", size=12, anchor="middle", weight="bold"),
              text(cr_x, cr_y + 50, "S", size=8, anchor="middle"), text(cr_x + 44, cr_y + 3, "E", size=8),
              text(cr_x - 44, cr_y + 3, "W", size=8, anchor="end"), text(cr_x, cr_y + 64, "PLANT NORTH", size=7, anchor="middle")]))
sb_x, sb_y = 40, 610
sb = [rect(sb_x + k_ * 50, sb_y, 50, 6, f=INK if k_ % 2 == 0 else WHITE, s=INK, w=0.8) for k_ in range(4)]
sb += [text(sb_x + k_ * 50, sb_y + 17, str(k_ * 10), size=7, anchor="middle") for k_ in range(5)]
sb += [text(sb_x + 215, sb_y + 17, "m", size=7), text(sb_x, sb_y - 6, "SCALE 1 unit = 0.2 m  (5 units / m)", size=7)]
ANN.append(G(sb))


def nf(v):
    return f"{v:,.0f}"


bd = [text(40, 1270, "BUND DATA  (NFPA 30 · 110 % OF LARGEST TANK · SHELL SPACING ≥ D/6 · WALL CLEARANCE ≥ 1.5 m)", size=9, weight="bold")]
names = {"SW": "B-01 TF1", "ST": "B-02 TF2", "CE": "B-03 TF3", "NE1": "B-04 TF4", "NE2": "B-05 TF4-FR"}
for i, (k_, r_) in enumerate(BUND_RES.items()):
    bd.append(text(40, 1288 + 14 * i, f"{names[k_]}  largest {r_['tag']}  V = {nf(r_['v'])} m³  → 110 % = {nf(r_['req'])} m³   "
                   f"H req. {r_['h_req']:.2f} m → wall H {r_['h_des']:.1f} m · net {nf(r_['net'])} m³", size=7.5))
bd.append(text(40, 1288 + 14 * 5 + 6, "Fillet R = 4.4 m at internal junctions (narrow corridors); perimeter road corners R = 15 m + half-width where edges allow.", size=7))
bd.append(text(40, 1288 + 14 * 6 + 6, "Underground drains / OWS lines not shown. Sumps drain to the retention basin (zone 7).", size=7))
ANN.append(G(bd))
bk = [text(1090, 1270, "BUILDING / GATE KEY  (distributed architecture)", size=9, weight="bold")]
for i, (nm, info) in enumerate(BLDG_INFO.items()):
    bk.append(text(1090, 1288 + 13 * i, f"{BLDG_SHORT[nm]:6s} {info[0]}   {info[1]}  —  {info[2]}: {info[3]}", size=7))
for j, (gid, role, ei_, gp_) in enumerate(GATES):
    bk.append(text(1090, 1288 + 13 * (len(BLDG_INFO) + j), f"{gid:6s} {role}", size=7, weight="bold"))
ANN.append(G(bk))

tb = [rect(30, 30, 520, 118, f=WHITE, s=INK, w=1.4), line(30, 58, 550, 58, s=INK, w=0.8), line(320, 58, 320, 148, s=INK, w=0.8),
      text(40, 49, "GENERAL ARRANGEMENT — PLOT PLAN · BULK LIQUID HYDROCARBON TERMINAL", size=9.5, weight="bold"),
      text(40, 74, f"IRREGULAR PLOT ≈ {m2(poly_area(BND)) / 1e4:.1f} ha · 1 UNIT = 0.2 m", size=8),
      text(40, 88, "DRAWING  DT-UI-SVG-DOC-001 / GA-003      REV B", size=8),
      text(40, 102, f"TANKS: {sum(1 for t in ALL_TANKS if t[0] != 'TK-0501')} + 1 FW  ·  PUMPS: 6  ·  BAYS: 4", size=8),
      text(40, 116, "LAYERS: L-CIVIL · L-STRUCT · L-MECH · L-PIPE · L-FIRE · L-ANNO", size=7),
      text(40, 130, "SEMANTIC ZOOM: L1 macro · L2 secondary · L3 micro", size=7),
      text(330, 74, "CODES / STANDARDS", size=8, weight="bold"), text(330, 88, "NFPA 30 (spacing, diking)", size=7.5),
      text(330, 100, "ISA-101 (HMI, progressive disclosure)", size=7.5), text(330, 112, "ISO 13567 / AIA CAD layering", size=7.5),
      text(330, 124, "ISO 14224 (APM data binding)", size=7.5), text(330, 140, "COLOUR RESERVED FOR LIVE ALARMS", size=7, weight="bold")]
ANN.append(G(tb))

lg = [rect(30, 160, 300, 256, f=WHITE, s=INK, w=1.2), text(40, 175, "LEGEND / ZONE KEY", size=8, weight="bold")]
for i, (num, name, _) in enumerate(ZONES):
    lg += [circle(48, 191 + 14 * i, 5.5, f=INK), text(48, 193.5 + 14 * i, num, size=7, anchor="middle", weight="bold", f=LIGHT),
           text(60, 193.5 + 14 * i, name, size=6.3)]
yy = 191 + 14 * 8 + 10
lg += [circle(46, yy, 5, f=WHITE, s=INK, w=1.2), text(58, yy + 2.5, "STORAGE TANK (FR / CONE ROOF)", size=6.3),
       circle(46, yy + 13, 3.5, f=WHITE, s=INK, w=1.2), circle(46, yy + 13, 1.2, f=INK), text(58, yy + 15.5, "HYDRANT", size=6.3),
       rect(41, yy + 24, 10, 10, f=WHITE, s=INK, w=1.2), text(58, yy + 32, "FOAM MONITOR (R = 50 m)", size=6.3),
       line(36, yy + 46, 56, yy + 46, s=INK, w=2.6), line(36, yy + 51, 56, yy + 51, s=STEEL, w=1.0),
       text(64, yy + 50, "PROCESS HEADER / SLEEPER LINES", size=6.3),
       line(176, yy, 196, yy, s=STEEL, w=2, d="16 4 3 4"), text(202, yy + 3, "FIRE-WATER MAIN", size=6.3),
       rect(176, yy + 8, 20, 8, f="url(#hatch-concrete)", s=INK, w=1), text(202, yy + 15, "CONCRETE BUND", size=6.3),
       rect(176, yy + 22, 20, 8, f=CONC, s=STEEL, w=0.8), text(202, yy + 29, "SLEEPERWAY 6 m", size=6.3),
       line(176, yy + 42, 196, yy + 42, s=ASPH, w=8), text(202, yy + 45, "ROAD 6 m", size=6.3),
       polyg([(206, yy + 56), (196, yy + 52), (196, yy + 60)], f=INK), text(212, yy + 59, "HV ONE-WAY DIRECTION", size=6.3)]
ANN.append(G(lg))



# ==========================================================================
#  LAYOUT / LOGISTICS / PIPING VALIDATION  (asserted at generation time)
# ==========================================================================
def seg_hit(p1, p2, p3, p4):
    def o(a, b_, c):
        return (b_[0] - a[0]) * (c[1] - a[1]) - (b_[1] - a[1]) * (c[0] - a[0])
    return (o(p1, p2, p3) * o(p1, p2, p4) < 0) and (o(p3, p4, p1) * o(p3, p4, p2) < 0)


def polys_overlap(p, q):
    if any(pip(v, q) for v in p) or any(pip(v, p) for v in q):
        return True
    return any(seg_hit(p[i], p[(i + 1) % len(p)], q[j], q[(j + 1) % len(q)]) for i in range(len(p)) for j in range(len(q)))


def poly_seg_dist(poly, a, b_):
    d = min(dist_seg(v, a, b_) for v in poly)
    d = min(d, min(dist_seg(a, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))),
            min(dist_seg(b_, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))))
    if any(seg_hit(a, b_, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))) or pip(a, poly):
        return 0.0
    return d


BLDG_POLY = {k_: [uvp(a0, b0), uvp(a1, b0), uvp(a1, b1), uvp(a0, b1)] for k_, (a0, a1, b0, b1) in BLDG.items()}
BASIN_POLY = [uvp(BASIN[0], BASIN[2]), uvp(BASIN[1], BASIN[2]), uvp(BASIN[1], BASIN[3]), uvp(BASIN[0], BASIN[3])]
ALL_ROAD_SEGS = ROAD_SEGS_PX + [(ROADC[i], ROADC[(i + 1) % len(ROADC)]) for i in range(len(ROADC))]
SLEEPER_POLY = [o for o in OBST[len(BUNDS):len(BUNDS) + len(SLEEPERS)]]

# 1. buildings: inside the fence, off every road / bund / pad / sleeper / tank / basin / yard / other building
for k_, bp in BLDG_POLY.items():
    assert all(pip(v, BND) and dist_poly(v, BND) >= 24 for v in bp), f"building {k_} too close to fence"
    for nm_, o_ in list(("bund " + n2, BUNDS[n2]) for n2 in BUNDS) + [("pad/apron", f) for f in FRAME_BOX] + \
            [("basin", BASIN_POLY), ("yard", YARD_PX)] + [("sleeper", s_) for s_ in SLEEPER_POLY] + \
            [("bldg " + k2, v2) for k2, v2 in BLDG_POLY.items() if k2 != k_]:
        assert not polys_overlap(bp, o_), f"building {k_} overlaps {nm_}"
    for (ca, r_) in CIRC:
        assert dist_poly(ca, bp) >= r_ + 1 and not pip(ca, bp), f"building {k_} overlaps a tank"
    for a_, b_ in ALL_ROAD_SEGS:
        assert poly_seg_dist(bp, a_, b_) >= HW + 0.5, f"building {k_} clips a road"

# 2. staging yard: inside the fence and clear of equipment
assert all(pip(v, BND) for v in YARD_PX)
for nm_, o_ in list(("bund " + n2, BUNDS[n2]) for n2 in BUNDS) + [("basin", BASIN_POLY)] + [("bldg " + k2, v2) for k2, v2 in BLDG_POLY.items()]:
    assert not polys_overlap(YARD_PX, o_), f"yard overlaps {nm_}"
for (ca, r_) in CIRC:
    assert dist_poly(ca, YARD_PX) >= r_, "yard overlaps a tank"

# 3. no dead-end or floating road vectors: every road end lies on the perimeter road or on another road
for ri, (rid, pts) in enumerate(ROADS_PX):
    for end in (pts[0], pts[-1]):
        on_perim = dist_poly(end, ROADC) <= 1.5
        on_other = any(dist_seg(end, a_, b_) <= 1.5 for rj, (rid2, p2) in enumerate(ROADS_PX) if rj != ri
                       for a_, b_ in zip(p2[:-1], p2[1:]))
        assert on_perim or on_other, f"road {rid} has a dead end at {end}"

# 4. one-way HV circuit: gate -> perimeter -> staging yard -> lanes -> R-06 -> R-02 -> R-05 -> R-01 -> perimeter -> exit gate
def on_roads(p, tol=1.0):
    return any(dist_seg(p, a_, b_) <= tol for a_, b_ in ALL_ROAD_SEGS)


for ptn in HV_ENTRY[1:] + [q for ln in HV_LANES for q in ln] + HV_EXIT:
    assert on_roads(ptn) or any(pip(ptn, f) for f in FRAME_BOX), f"HV route leaves the road network at {ptn}"
assert math.hypot(*(HV_ENTRY[-1][i] - HV_LANES[-1][0][i] for i in (0, 1))) < 1.0
assert math.hypot(*(HV_LANES[-1][-1][i] - HV_EXIT[0][i] for i in (0, 1))) < 1.0
assert dist_poly(G1_IN, ROADC) < 1.0 and dist_poly(G2_IN, ROADC) < 1.0 and dist_poly(R06_FOOT, ROADC) < 1.5
assert math.hypot(GATES[0][3][0] - GATES[1][3][0], GATES[0][3][1] - GATES[1][3][1]) >= 60, "HV gates too close"
def vertex_radius(i, r=U(15) + ROAD_W / 2):
    pv, v, nx_ = ROADC[i - 1], ROADC[i], ROADC[(i + 1) % len(ROADC)]
    a_, b_ = (pv[0] - v[0], pv[1] - v[1]), (nx_[0] - v[0], nx_[1] - v[1])
    la, lb = math.hypot(*a_), math.hypot(*b_)
    phi = math.acos(max(-1, min(1, (a_[0] * b_[0] + a_[1] * b_[1]) / (la * lb))))
    if phi > math.pi - 1e-3:
        return float("inf")
    t = min(r / math.tan(phi / 2), 0.48 * la, 0.48 * lb)
    return (t * math.tan(phi / 2)) * K - ROAD_W / 2         # inner-edge radius in units


HV_R = {f"perimeter vertex {i}": vertex_radius(i) for i in (5, 4, 3, 6)}
HV_DEFLECT_R06 = 41.0     # deg: R-06 merges into the perimeter road at a shallow angle (no 90-degree corner)

# 5. piping: sleeperways reach every bund, pump pad, manifold and gantry without crossing buildings or tanks
def poly_samples(pts, step=1.0):
    out = []
    for (u1, v1), (u2, v2) in zip(pts[:-1], pts[1:]):
        L = math.hypot(u2 - u1, v2 - v1)
        for i in range(int(L / step) + 1):
            t = min(1.0, i * step / L) if L else 0
            out.append((u1 + (u2 - u1) * t, v1 + (v2 - v1) * t))
    out.append(pts[-1])
    return out


for pi_, pts in enumerate(PIPE_NET):
    for (u_, v_) in poly_samples(pts):
        p_ = uvp(u_, v_)
        for k_, bp in list(BLDG_POLY.items()) + [("basin", BASIN_POLY), ("yard", YARD_PX)]:
            assert not pip(p_, bp) if isinstance(k_, str) else True, f"pipe {pi_} enters {k_}"
        for (ca, r_) in CIRC:
            assert math.hypot(p_[0] - ca[0], p_[1] - ca[1]) >= r_ - 0.4, f"pipe {pi_} passes through a tank at {(u_, v_)}"


def pipes_touch(p1, p2, tol=1.0):
    ends1, ends2 = (p1[0], p1[-1]), (p2[0], p2[-1])
    segs1, segs2 = list(zip(p1[:-1], p1[1:])), list(zip(p2[:-1], p2[1:]))
    return (any(dist_seg(e, a_, b_) <= tol for e in ends1 for a_, b_ in segs2) or
            any(dist_seg(e, a_, b_) <= tol for e in ends2 for a_, b_ in segs1))


_par = list(range(len(PIPE_NET)))


def _find(i):
    while _par[i] != i:
        _par[i] = _par[_par[i]]
        i = _par[i]
    return i


for i in range(len(PIPE_NET)):
    for j in range(i + 1, len(PIPE_NET)):
        if pipes_touch(PIPE_NET[i], PIPE_NET[j]):
            _par[_find(i)] = _find(j)
PIPE_COMPONENTS = len({_find(i) for i in range(len(PIPE_NET))})
assert PIPE_COMPONENTS == 1, f"piping network split into {PIPE_COMPONENTS} islands"
assert len(STUBS) == len([t for t in ALL_TANKS if t[0] != "TK-0501"]), "a storage tank has no connecting stub"
_net_idx = {tuple(map(tuple, p_)): i for i, p_ in enumerate(PIPE_NET)}

# --------------------------------------------------------------------------
# Assemble document
# --------------------------------------------------------------------------
STYLE = """
.dt-canvas { font-family: Arial, Helvetica, sans-serif; background: #EDF2F4; }
/* ISA-101 progressive disclosure */
.zoom-l1 .dt-zoom-l2, .zoom-l1 .dt-zoom-l3, .zoom-l2 .dt-zoom-l3 { display: none; }
.dt-interactive { cursor: pointer; }
.dt-interactive:hover { opacity: 0.85; }
"""
DEFS = """
<pattern id="hatch-concrete" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="6" stroke="#8D99AE" stroke-width="1"/>
</pattern>
<pattern id="hatch-light" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
<line x1="0" y1="0" x2="0" y2="5" stroke="#B9C0CC" stroke-width="0.6"/>
</pattern>
"""


def layer(lid, cls, items):
    return f'<g id="{lid}" class="{cls}">\n' + "\n".join(i for i in items if i) + "\n</g>"


def build(zoom="zoom-l1"):
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg viewBox="0 0 {W} {H}" class="dt-canvas {zoom}" xmlns="http://www.w3.org/2000/svg">',
        "<title>General Arrangement Plot Plan — Irregular-site Bulk Liquid Hydrocarbon Terminal (DT-UI-SVG-DOC-001)</title>",
        "<desc>Irregular plot traced from a reference survey; 1 SVG unit = 0.2 m. Layers per AIA CAD / ISO 13567; "
        "ISA-101 semantic zoom classes dt-zoom-l2 / dt-zoom-l3; ISO 14224 data binding on equipment.</desc>",
        f"<defs>{DEFS}</defs>", f"<style>{STYLE}</style>",
        layer("L-CIVL-BOTM", "dt-layer-civil-botm", CIV), 
        layer("L-MECH-EQPM", "dt-layer-mech-eqpm", MEC), layer("L-INSP-INST", "dt-layer-insp-inst", INS), layer("L-PIPE-PROC", "dt-layer-pipe-proc", PIP),
        layer("L-FIRE-PROT", "dt-layer-fire-prot", FIR), layer("L-ELEC-HAZ", "dt-layer-elec-haz", HAZ), layer("L-ANNO-TEXT", "dt-layer-anno-text", ANN), "</svg>"]
    return "\n".join(parts)


def validate(p):
    tree = ET.parse(p)
    root = tree.getroot()
    ns = "{http://www.w3.org/2000/svg}"
    assert root.tag == ns + "svg" and root.get("viewBox") == f"0 0 {W} {H}"
    assert root.get("class") in ("dt-canvas zoom-l1", "dt-canvas zoom-l2", "dt-canvas zoom-l3")
    layers = [g for g in root if g.tag == ns + "g"]
    ids = [g.get("id") for g in layers]
    assert ids == ["L-CIVL-BOTM", "L-MECH-EQPM", "L-INSP-INST", "L-PIPE-PROC", "L-FIRE-PROT", "L-ELEC-HAZ", "L-ANNO-TEXT"], ids
    by = {}
    for e in root.iter(ns + "g"):
        if "dt-interactive" in (e.get("class") or ""):
            assert e.get("data-cmp-id"), f"missing data-cmp-id in {e.attrib}"
            loc = e.get("data-func-loc") or e.get("data-tag")
            assert loc, f"missing functional location or tag in {e.attrib}"
            assert e.get("data-status"), f"missing data-status in {e.attrib}"
            by.setdefault(e.get("data-cmp-id"), []).append(loc)
    assert len(by["CMP-EQP-TANK"]) == 31 and len(by["CMP-EQP-PUMP"]) == 6 and len(by["CMP-EQP-BAY"]) == 4
    raw = Path(p).read_text(encoding="utf-8")
    for hx in set(re.findall(r"#[0-9A-Fa-f]{6}", raw)):
        r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
        assert colorsys.rgb_to_hls(r, g, b)[2] <= 0.30, f"saturated colour {hx}"
    z2 = sum(1 for e in root.iter() if "dt-zoom-l2" in (e.get("class") or ""))
    z3 = sum(1 for e in root.iter() if "dt-zoom-l3" in (e.get("class") or ""))
    counts = {i: sum(1 for _ in g.iter()) - 1 for i, g in zip(ids, layers)}
    return by, z2, z3, counts, len(raw)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate industrial terminal General Arrangement (GA) SVG conforming to DT-UI-SVG-DOC-001 rev 2.0."
    )
    parser.add_argument(
        "output_path",
        type=Path,
        help="Mandatory target output SVG file or directory path (e.g., path/to/terminal_plot_plan.svg)"
    )
    args = parser.parse_args()

    target = args.output_path
    if target.is_dir() or target.suffix != ".svg":
        target.mkdir(parents=True, exist_ok=True)
        out = target / "terminal_plot_plan_irregular.svg"
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        out = target

    out.write_text(build("zoom-l1"), encoding="utf-8")
    out.with_name(out.stem + "_l2.svg").write_text(build("zoom-l2"), encoding="utf-8")
    out.with_name(out.stem + "_l3.svg").write_text(build("zoom-l3"), encoding="utf-8")
    by, z2, z3, counts, size = validate(out)
    print(f"Wrote {out}  ({size/1024:.0f} KB) — valid XML")
    print("Interactive units :", {k_: len(v) for k_, v in by.items()})
    print("Elements per layer:", counts)
    print(f"Zoom-tagged elems : L2={z2}  L3={z3}")
    print(f"HV circuit: {GATES[0][0]} {GATES[0][1]} -> perimeter -> staging yard -> 4 lanes -> R-06 -> R-02 -> R-05 -> R-01 -> {GATES[1][0]} {GATES[1][1]}; "
          f"{GATES[2][0]} = {GATES[2][1]}")
    print("HV perimeter-vertex inner radii (m):", {k_: ("straight" if v_ == float("inf") else f"{v_*M_PER_UNIT:.1f}") for k_, v_ in HV_R.items()})
    print(f"Piping network: {len(PIPE_NET)} polylines, {PIPE_COMPONENTS} connected component, {len(STUBS)} tank stubs; buildings: {', '.join(BLDG)}")
    print(f"Plot area ≈ {m2(poly_area(BND))/1e4:.1f} ha ; hydrants {len(hyd)} ; foam monitors {len(fm_list)}")
    for k_, r_ in BUND_RES.items():
        print(f"Bund {names[k_]:12s} largest {r_['tag']} V={r_['v']:,.0f} m3  110%={r_['req']:,.0f}  "
              f"H_req={r_['h_req']:.2f} m  wall={r_['h_des']:.1f} m")


if __name__ == "__main__":
    main()
