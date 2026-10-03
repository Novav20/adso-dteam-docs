#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_terminal_svg.py
========================
Parametric generator for a 2D General Arrangement (GA) Plot Plan of a mid-size
Bulk Liquid Hydrocarbon Terminal (400 m x 300 m plot) as a pure SVG file.

Contract : DT-UI-SVG-DOC-001
Scale    : 1 SVG unit = 0.2 m  (viewBox 0 0 2000 1500)  -> 5 units per metre
Output   : terminal_plot_plan.svg   (root class "dt-canvas zoom-l1")
           terminal_plot_plan_l2.svg / _l3.svg  (same drawing, root class
           switched so the ISA-101 L2 / L3 detail can be previewed directly)

Layers (AIA CAD / ISO 13567 mapping)
  L-CIVIL  L-STRUCT  L-MECH  L-PIPE  L-FIRE  L-ANNO
Semantic zoom (ISA-101 progressive disclosure)
  (none)        macro outlines, always visible at L1
  dt-zoom-l2    secondary detail  (rack bents, pump bases, road striping ...)
  dt-zoom-l3    micro detail      (stair treads, flanges, nozzle CL, handwheels)
Data binding (ISO 14224)
  CMP-EQP-TANK / CMP-EQP-PUMP / CMP-EQP-BAY  + data-tag + class dt-interactive
Styling (ISA-101 high-performance HMI)
  Neutral greys only; saturated colour is reserved for live alarms.
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


def poly(pts, **kw):
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


# --------------------------------------------------------------------------
# Master parameters (all geometry derives from these)
# --------------------------------------------------------------------------
FENCE = 30
RING = 90                         # ring-road centreline inset
RW = U(8)                         # 8 m road width            = 40
TURN_IN = U(15)                   # 15 m inner turning radius = 75
RING_RC = TURN_IN + RW / 2        # centreline radius         = 95
R1X = 950                         # N-S internal fire road
R5Y = 610                         # E-W road (south of tank farms)
R2Y = 1000                        # E-W road (south of process area)
R6Y = 800                         # pump-station access spur
R1_BAND = (R1X - RW / 2, R1X + RW / 2)
R5_BAND = (R5Y - RW / 2, R5Y + RW / 2)
R2_BAND = (R2Y - RW / 2, R2Y + RW / 2)

# Tanks ---------------------------------------------------------------
TK1_D, TK1_H = 40.0, 12.0         # m  floating roof, crude (Class I)
TK2_D, TK2_H = 25.0, 12.0         # m  cone roof, diesel
FW_D = 20.0                       # m  fire-water tank
TK1_R, TK2_R, FW_R = U(TK1_D) / 2, U(TK2_D) / 2, U(FW_D) / 2

B1 = (130, 140, 830, 540)         # Tank-farm-1 bund (x1,y1,x2,y2)
B2 = (1300, 140, 1850, 560)       # Tank-farm-2 bund
WALL_T = 6                        # 1.2 m concrete wall

TK1 = [("TK-0101", 360.0, 340.0), ("TK-0102", 600.0, 340.0)]
TK2 = [("TK-0201", 1437.5, 245.0), ("TK-0202", 1712.5, 245.0),
       ("TK-0203", 1437.5, 455.0), ("TK-0204", 1712.5, 455.0)]
FW_TK = ("TK-0301", 720.0, 1180.0)

# Sleeperway (6 m = 30 units) ------------------------------------------
SLP_W = U(6)
S1_X0, S1_X1 = 275, 1650
S1_A, S1_B = 676, 684             # process header A / B centrelines
S2V_AX, S2V_BX = 1296, 1284
S2H_A, S2H_B = 924, 936

# Pump station ---------------------------------------------------------
PX0, PITCH, PUMP_Y = 345, 70, 785
PUMP_TAGS = ["P-0101A", "P-0101B", "P-0101C", "P-0201A", "P-0201B", "P-0201C"]

# Truck gantry ---------------------------------------------------------
GX = 1400
ISL_W, BAY_W = 20, 40
ISL_X = [GX + (ISL_W + BAY_W) * k for k in range(5)]          # island left edges
BAY_X = [GX + ISL_W + (ISL_W + BAY_W) * k for k in range(4)]  # bay left edges
ISL_Y0, ISL_Y1 = 1050, 1230

# --------------------------------------------------------------------------
# Engineering checks (computed, then printed + asserted)
# --------------------------------------------------------------------------
def vol(d, h):
    return math.pi * (d / 2) ** 2 * h


V1, V2 = vol(TK1_D, TK1_H), vol(TK2_D, TK2_H)


def bund_calc(b, v_largest, other_tank_d_list, wall_h_step=0.1, freeboard=0.15):
    x1, y1, x2, y2 = b
    a = M(x2 - x1 - 2 * WALL_T) * M(y2 - y1 - 2 * WALL_T)
    a_other = sum(math.pi * (d / 2) ** 2 for d in other_tank_d_list)
    req = 1.10 * v_largest
    h_req = req / (a - a_other)
    h_des = math.ceil((h_req + freeboard) / wall_h_step) * wall_h_step
    net = (a - a_other) * h_des
    return dict(area=a, req=req, h_req=h_req, h_des=h_des, net=net)


C1 = bund_calc(B1, V1, [TK1_D])
C2 = bund_calc(B2, V2, [TK2_D] * 3)
# intermediate (fire-break) compartment check for TF2
cell_w = (B2[2] - B2[0] - 2 * WALL_T - 4) / 2
cell_h = (B2[3] - B2[1] - 2 * WALL_T - 4) / 2
INT_H = 0.6
cell_net = (M(cell_w) * M(cell_h) - math.pi * (TK2_D / 2) ** 2) * INT_H
cell_pct = 100 * cell_net / V2

GAP1 = M(TK1[1][1] - TK1[0][1]) - TK1_D
GAP2_X = M(TK2[1][1] - TK2[0][1]) - TK2_D
GAP2_Y = M(TK2[2][2] - TK2[0][2]) - TK2_D

assert GAP1 >= TK1_D / 6, "TF1 shell-to-shell < D/6"
assert GAP2_X >= TK2_D / 6 and GAP2_Y >= TK2_D / 6, "TF2 shell-to-shell < D/6"
assert C1["h_des"] <= 2.5 and C2["h_des"] <= 2.5
assert cell_pct >= 10.0, "intermediate compartment < 10 % of tank volume"
assert abs(RING_RC - RW / 2 - U(15)) < 1e-6 and abs(RW - U(8)) < 1e-6
assert abs(SLP_W - 30) < 1e-6 and abs(U(40) - 200) < 1e-6 and abs(U(25) - 125) < 1e-6
for _, cx, cy in TK1:
    assert B1[0] + WALL_T + U(1.5) < cx - TK1_R and cx + TK1_R < B1[2] - WALL_T - U(1.5)
    assert B1[1] + WALL_T + U(1.5) < cy - TK1_R and cy + TK1_R < B1[3] - WALL_T - U(1.5)
for _, cx, cy in TK2:
    assert B2[0] + WALL_T + U(1.5) < cx - TK2_R and cx + TK2_R < B2[2] - WALL_T - U(1.5)
    assert B2[1] + WALL_T + U(1.5) < cy - TK2_R and cy + TK2_R < B2[3] - WALL_T - U(1.5)

# --------------------------------------------------------------------------
# Layer buffers
# --------------------------------------------------------------------------
CIV, STR, MEC, PIP, FIR, ANN = ([] for _ in range(6))
VAL2, VAL3, FLG = [], [], []          # collected valve bodies / handwheels / flanges


def valve(x, y, orient, s=4.5):
    if orient == "h":
        VAL2.append(path(f"M{n(x-s)},{n(y-s*.7)} L{n(x+s)},{n(y+s*.7)} L{n(x+s)},{n(y-s*.7)} "
                         f"L{n(x-s)},{n(y+s*.7)} Z", f=WHITE, s=INK, w=0.9))
        yy = y - s * .7 - 5
        VAL3.append(line(x, y, x, yy, s=INK, w=0.7))
        VAL3.append(line(x - 3.5, yy, x + 3.5, yy, s=INK, w=1.2))
    else:
        VAL2.append(path(f"M{n(x-s*.7)},{n(y-s)} L{n(x+s*.7)},{n(y+s)} L{n(x-s*.7)},{n(y+s)} "
                         f"L{n(x+s*.7)},{n(y-s)} Z", f=WHITE, s=INK, w=0.9))
        xx = x + s * .7 + 5
        VAL3.append(line(x, y, xx, y, s=INK, w=0.7))
        VAL3.append(line(xx, y - 3.5, xx, y + 3.5, s=INK, w=1.2))


def check_valve(x, y):
    VAL2.append(poly([(x - 4, y + 3.5), (x + 4, y + 3.5), (x, y - 3.5)], f=WHITE, s=INK, w=0.9))
    VAL2.append(line(x - 4, y - 3.5, x + 4, y - 3.5, s=INK, w=1.1))


def flange(x, y, orient="v", size=4.5):
    if orient == "v":      # pipe runs vertically -> flange faces are horizontal ticks
        FLG.append(line(x - size, y, x + size, y, s=INK, w=1.1))
        FLG.append(line(x - size, y + 2.2, x + size, y + 2.2, s=INK, w=1.1))
    else:
        FLG.append(line(x, y - size, x, y + size, s=INK, w=1.1))
        FLG.append(line(x + 2.2, y - size, x + 2.2, y + size, s=INK, w=1.1))


def hpath(y, x0, x1, loops=(), sign=1, start=None):
    """Horizontal run with U-shaped expansion loops. sign +1 = loop toward +y."""
    d = start if start else f"M{n(x0)},{n(y)}"
    for xc, wd, dp in sorted(loops):
        d += (f" L{n(xc-wd/2)},{n(y)} L{n(xc-wd/2)},{n(y+sign*dp)} "
              f"L{n(xc+wd/2)},{n(y+sign*dp)} L{n(xc+wd/2)},{n(y)}")
    return d + f" L{n(x1)},{n(y)}"


def dim_h(x1, x2, y, label, off=-5):
    return G([line(x1, y, x2, y, s=INK, w=0.6),
              line(x1, y - 4, x1, y + 4, s=INK, w=0.6),
              line(x2, y - 4, x2, y + 4, s=INK, w=0.6),
              text((x1 + x2) / 2, y + off, label, size=7, anchor="middle")], c=ZL2)


def dim_v(x, y1, y2, label, off=4):
    return G([line(x, y1, x, y2, s=INK, w=0.6),
              line(x - 4, y1, x + 4, y1, s=INK, w=0.6),
              line(x - 4, y2, x + 4, y2, s=INK, w=0.6),
              text(x + off, (y1 + y2) / 2 + 2.5, label, size=7)], c=ZL2)


# ==========================================================================
#                               L-CIVIL
# ==========================================================================
CIV.append(rect(0, 0, W, H, f=LIGHT))                                     # ground
CIV.append(rect(4, 4, W - 8, H - 8, s=MID, w=1.5, d="30 6 4 6"))          # property limit

# --- perimeter fence + gate ------------------------------------------------
fx0, fy0, fx1, fy1, g0, g1 = FENCE, FENCE, W - FENCE, H - FENCE, 330, 390
CIV.append(path(f"M{fx0},{fy0} H{fx1} V{fy1} H{g1} M{g0},{fy1} H{fx0} V{fy0}", s=INK, w=1.2))
CIV.append(line(300, fy1 + 3, g0, fy1 + 3, s=INK, w=3))
CIV.append(line(g1, fy1 + 3, g1 + 30, fy1 + 3, s=INK, w=3))
posts = []
for x in range(fx0, fx1 + 1, 50):
    posts.append(rect(x - 1.5, fy0 - 1.5, 3, 3, f=INK))
    if not (g0 - 25 < x < g1 + 25):
        posts.append(rect(x - 1.5, fy1 - 1.5, 3, 3, f=INK))
for y in range(fy0 + 50, fy1, 50):
    posts.append(rect(fx0 - 1.5, y - 1.5, 3, 3, f=INK))
    posts.append(rect(fx1 - 1.5, y - 1.5, 3, 3, f=INK))
CIV.append(G(posts, c=ZL2))

# --- asphalt roads (two-pass edge/fill trick) --------------------------------
def road_strokes(width, colour):
    out = [rect(RING, RING, W - 2 * RING, H - 2 * RING, rx=RING_RC, s=colour, w=width)]
    out.append(line(R1X, RING, R1X, H - RING, s=colour, w=width))
    for y in (R5Y, R2Y):
        out.append(line(RING, y, W - RING, y, s=colour, w=width))
    out.append(line(770, R6Y, R1_BAND[0], R6Y, s=colour, w=width))
    return out


CIV += road_strokes(RW + 2, STEEL)
CIV += road_strokes(RW, ASPH)
CIV.append(line(770, R6Y - RW / 2, 770, R6Y + RW / 2, s=STEEL, w=1))


def fillet(vx, hy, sx, sy, R=TURN_IN):
    px, py = vx + sx * RW / 2, hy + sy * RW / 2
    ax, ay = px + sx * R, py
    bx, by = px, py + sy * R
    sweep = 0 if sx * sy > 0 else 1
    fill = path(f"M{n(px)},{n(py)} L{n(ax)},{n(ay)} A{n(R)},{n(R)} 0 0 {sweep} {n(bx)},{n(by)} Z", f=ASPH)
    edge = path(f"M{n(ax)},{n(ay)} A{n(R)},{n(R)} 0 0 {sweep} {n(bx)},{n(by)}", s=STEEL, w=1)
    return fill, edge


junc = []
for sx in (-1, 1):
    for sy in (-1, 1):
        junc += [(R1X, R5Y, sx, sy), (R1X, R2Y, sx, sy)]
junc += [(R1X, RING, sx, 1) for sx in (-1, 1)]
junc += [(R1X, H - RING, sx, -1) for sx in (-1, 1)]
for hy in (R5Y, R2Y):
    junc += [(RING, hy, 1, sy) for sy in (-1, 1)]
    junc += [(W - RING, hy, -1, sy) for sy in (-1, 1)]
junc += [(R1X, R6Y, -1, sy) for sy in (-1, 1)]
fills, edges = [], []
for j in junc:
    f_, e_ = fillet(*j)
    fills.append(f_)
    edges.append(e_)
CIV += fills + edges

# truck apron, entrance drive, parking
CIV.append(rect(1370, 1020, 320, 370, f=ASPH))
CIV.append(line(1370, 1020, 1370, 1390, s=STEEL, w=1))
CIV.append(line(1690, 1020, 1690, 1390, s=STEEL, w=1))
CIV.append(rect(g0, 1430, g1 - g0, 40, f=ASPH))
CIV.append(line(g0, 1430, g0, 1470, s=STEEL, w=1))
CIV.append(line(g1, 1430, g1, 1470, s=STEEL, w=1))
CIV.append(rect(200, 1020, 140, 70, f=ASPH, s=STEEL, w=0.8))
CIV.append(G([line(x, 1022, x, 1046, s=LIGHT, w=0.8) for x in range(212, 340, 12)] +
             [line(x, 1064, x, 1088, s=LIGHT, w=0.8) for x in range(212, 340, 12)], c=ZL2))

# road striping (L2)
stripes = [rect(RING, RING, W - 2 * RING, H - 2 * RING, rx=RING_RC, s=LIGHT, w=1.2, d="12 9"),
           line(R1X, RING, R1X, H - RING, s=LIGHT, w=1.2, d="12 9"),
           line(RING, R5Y, W - RING, R5Y, s=LIGHT, w=1.2, d="12 9"),
           line(RING, R2Y, W - RING, R2Y, s=LIGHT, w=1.2, d="12 9"),
           line(770, R6Y, R1X, R6Y, s=LIGHT, w=1.2, d="12 9"),
           line((g0 + g1) / 2, 1430, (g0 + g1) / 2, 1470, s=LIGHT, w=1.2, d="12 9")]
CIV.append(G(stripes, c=ZL2))

# --- concrete bunds ---------------------------------------------------------
def bund(b):
    x1, y1, x2, y2 = b
    t = WALL_T
    wall = (f"M{x1},{y1} H{x2} V{y2} H{x1} Z M{x1+t},{y1+t} H{x2-t} V{y2-t} H{x1+t} Z")
    return [rect(x1 + t, y1 + t, x2 - x1 - 2 * t, y2 - y1 - 2 * t, f=BUNDFILL),
            path(wall, f=CONC, fill_rule="evenodd"),
            path(wall, f="url(#hatch-concrete)", fill_rule="evenodd", s=INK, w=1.2)]


CIV += bund(B1)
CIV += bund(B2)
# TF2 intermediate fire-break walls (lower than outer bund)
bx1, by1, bx2, by2 = B2
midx, midy = (bx1 + bx2) / 2, (by1 + by2) / 2
for rr in (rect(midx - 2, by1 + WALL_T, 4, by2 - by1 - 2 * WALL_T, f=CONC, s=INK, w=0.8),
           rect(bx1 + WALL_T, midy - 2, bx2 - bx1 - 2 * WALL_T, 4, f=CONC, s=INK, w=0.8)):
    CIV.append(rr)
# bund step-over stairs (L3) and sumps
stairs = []
for (sx_, sy_) in [(470, B1[3] - 10), (B1[0] + 10, 200), (1500, B2[3] - 10), (B2[2] - 10, 300)]:
    horiz = sy_ in (B1[3] - 10, B2[3] - 10)
    if horiz:
        stairs.append(rect(sx_ - 12, sy_ - 3, 24, 26, f=WHITE, s=INK, w=0.7))
        stairs += [line(sx_ - 12, yy, sx_ + 12, yy, s=INK, w=0.4) for yy in range(int(sy_), int(sy_) + 24, 3)]
    else:
        stairs.append(rect(sx_ - 3, sy_ - 12, 26, 24, f=WHITE, s=INK, w=0.7))
        stairs += [line(xx, sy_ - 12, xx, sy_ + 12, s=INK, w=0.4) for xx in range(int(sx_), int(sx_) + 24, 3)]
CIV.append(G(stairs, c=ZL3))
SUMP1 = (810.0, 520.0)
SUMP2 = (1318.0, 546.0)
for (sx_, sy_) in (SUMP1, SUMP2):
    CIV.append(rect(sx_ - 7, sy_ - 7, 14, 14, f=PALE, s=INK, w=1))
    CIV.append(G([line(sx_ - 7, sy_ - 7, sx_ + 7, sy_ + 7, s=INK, w=0.5),
                  line(sx_ - 7, sy_ + 7, sx_ + 7, sy_ - 7, s=INK, w=0.5)], c=ZL3))

# --- sleeperway concrete strips ------------------------------------------------
sl = []
for p, q in split(S1_X0, S1_X1, [R1_BAND]):
    sl.append(rect(p, S1_A - 11, q - p, SLP_W, f=CONC, s=STEEL, w=0.8))
sl.append(rect(1275, 665, SLP_W, 280, f=CONC, s=STEEL, w=0.8))          # S2 vertical
sl.append(rect(1275, 915, 325, SLP_W, f=CONC, s=STEEL, w=0.8))           # S2 horizontal
for _, cx, cy in TK1:
    for p, q in split(B1[3], 665, [R5_BAND]):
        sl.append(rect(cx - 15, p, SLP_W, q - p, f=CONC, s=STEEL, w=0.8))
for _, cx, cy in TK2[:2]:
    for p, q in split(B2[3], 665, [R5_BAND]):
        sl.append(rect(cx - 94, p, SLP_W, q - p, f=CONC, s=STEEL, w=0.8))
CIV.append(G(sl))

# road crossings (pipe sleeves / culverts)
sleeves = [rect(R1_BAND[0] - 4, 662, RW + 8, 36, s=STEEL, w=1, d="4 2")]
for _, cx, _cy in TK1:
    sleeves.append(rect(cx - 18, R5_BAND[0] - 2, 36, RW + 4, s=STEEL, w=1, d="4 2"))
for _, cx, _cy in TK2[:2]:
    sleeves.append(rect(cx - 97, R5_BAND[0] - 2, 36, RW + 4, s=STEEL, w=1, d="4 2"))
for x in (1410, 1470, 1530, 1590):
    sleeves.append(rect(x - 8, R2_BAND[0] - 2, 16, RW + 4, s=STEEL, w=1, d="4 2"))
CIV.append(G(sleeves, c=ZL2))

# --- pump pad / manifold pad ---------------------------------------------------
CIV.append(rect(320, 715, 440, 170, f=CONC, s=STEEL, w=1))
CIV.append(rect(324, 719, 432, 162, s=STEEL, w=0.6, d="5 3", c=ZL2))
corr = []
for i in range(5):
    xa = PX0 + PITCH * i + 40
    corr.append(rect(xa, 722, PITCH - 40, 154, f="url(#hatch-light)", s=MID, w=0.6, d="3 2"))
corr.append(text(540, 878, "MAINTENANCE ACCESS CORRIDORS 6.0 m BETWEEN SKIDS", size=6.5, anchor="middle"))
corr.append(line(320, 872, 740, 872, s=STEEL, w=1.2, d="6 3"))        # pad drain trench
corr.append(rect(741, 867, 10, 10, f=PALE, s=INK, w=0.8))              # pad sump
CIV.append(G(corr, c=ZL2))
CIV.append(rect(990, 712, 275, 155, f=CONC, s=STEEL, w=1))
CIV.append(rect(994, 716, 267, 147, s=STEEL, w=0.6, d="5 3", c=ZL2))

# --- retention / OWS basin + drain lines -----------------------------------------
CIV.append(rect(1000, 1100, 250, 230, rx=10, f="#D0D4DB", s=STEEL, w=1.4))
CIV.append(G([rect(1000 + k, 1100 + k, 250 - 2 * k, 230 - 2 * k, rx=max(2, 10 - k / 4), s=STEEL,
                   w=0.5, d="4 3") for k in (20, 40, 60, 80)], c=ZL2))
drain = [path(f"M{SUMP1[0]},{SUMP1[1]} H915 V1115 H1000", s=STEEL, w=1.8, d="6 3"),
         path(f"M{SUMP2[0]},{SUMP2[1]} V1115 H1250", s=STEEL, w=1.8, d="6 3"),
         circle(840, SUMP1[1], 3, f=WHITE, s=INK, w=0.8),
         circle(SUMP2[0], B2[3] + 0, 3, f=WHITE, s=INK, w=0.8)]
CIV.append(G(drain, c=ZL2))

# --- gantry islands (concrete) --------------------------------------------------
for xi in ISL_X:
    CIV.append(rect(xi, ISL_Y0, ISL_W, ISL_Y1 - ISL_Y0, rx=4, f=PALE, s=INK, w=1))

# ==========================================================================
#                               L-STRUCT
# ==========================================================================
# pipe-rack bents / sleeper supports (L2)
def bents_h(x1, x2, y, skips=(), pitch=40, wd=30):
    out, x = [], x1 + 10
    while x <= x2 - 6:
        if not any(a - 4 <= x <= b for a, b in skips):
            out.append(rect(x, y - wd / 2, 4, wd, f=STEEL, s=INK, w=0.3))
        x += pitch
    return out


def bents_v(x, y1, y2, skips=(), pitch=40, wd=30):
    out, y = [], y1 + 10
    while y <= y2 - 6:
        if not any(a - 4 <= y <= b for a, b in skips):
            out.append(rect(x - wd / 2, y, wd, 4, f=STEEL, s=INK, w=0.3))
        y += pitch
    return out


bents = bents_h(S1_X0, S1_X1, S1_A + 4, [R1_BAND])
bents += bents_v(1290, 700, 945)
bents += bents_h(1280, 1600, 930)
for _, cx, _cy in TK1:
    bents += bents_v(cx, B1[3] + 6, 665, [R5_BAND])
for _, cx, _cy in TK2[:2]:
    bents += bents_v(cx - 79, B2[3] + 6, 665, [R5_BAND])
STR.append(G(bents, c=ZL2))


def stair(cx, cy, r, a0, sweep, wd=5, step=2.5):
    r1, r2 = r + 0.8, r + 0.8 + wd
    a1 = a0 + sweep
    base = path(arc_band(cx, cy, r1, r2, a0, a1), f=PALE, s=INK, w=0.8)
    plat = path(arc_band(cx, cy, r1, r2 + 7, a1 - 2, a1 + 9), f=WHITE, s=INK, w=0.9, c=ZL2)
    treads = G([line(*polar(cx, cy, r1, a), *polar(cx, cy, r2, a), s=INK, w=0.4)
                for a in frange(a0 + step, a1 - step, step)], c=ZL3)
    return [base, plat, treads]


FR_STAIR = (180, 150)           # start angle, sweep (clockwise on screen)
CONE_STAIR = (270, 140)
for _, cx, cy in TK1:
    STR += stair(cx, cy, TK1_R, *FR_STAIR)
for _, cx, cy in TK2:
    STR += stair(cx, cy, TK2_R, *CONE_STAIR)
STR += stair(FW_TK[1], FW_TK[2], FW_R, *CONE_STAIR, wd=4)

# gantry canopy, columns, bollards, stair tower
cx0, cx1, cy0, cy1 = 1385, 1675, 1065, 1215
STR.append(rect(cx0, cy0, cx1 - cx0, cy1 - cy0, f="none", s=STEEL, w=1.6, d="10 4"))
cols, beams = [], []
for xi in ISL_X:
    xc = xi + ISL_W / 2
    for yc in (1075, 1205):
        cols.append(rect(xc - 3, yc - 3, 6, 6, f=STEEL, s=INK, w=0.6))
    for off in (-5, 5):
        for yb in (1056, 1224):
            cols.append(circle(xc + off, yb, 2.2, f=INK))          # bollards
for yc in (1075, 1205):
    beams.append(line(ISL_X[0] + 10, yc, ISL_X[-1] + 10, yc, s=STEEL, w=0.7, d="6 3"))
for xi in ISL_X:
    beams.append(line(xi + 10, 1075, xi + 10, 1205, s=STEEL, w=0.7, d="6 3"))
beams.append(line(cx0, (cy0 + cy1) / 2, cx1, (cy0 + cy1) / 2, s=STEEL, w=0.7, d="2 4"))   # ridge
STR.append(G(cols))
STR.append(G(beams, c=ZL2))
STR.append(rect(1664, 1100, 18, 50, f=WHITE, s=INK, w=1))                                # stair tower
STR.append(G([line(1664, yy, 1682, yy, s=INK, w=0.4) for yy in range(1103, 1150, 3)], c=ZL3))

# buildings
STR.append(rect(140, 1130, 200, 90, f=PALE, s=INK, w=1.6))                    # admin / control
STR.append(rect(136, 1126, 208, 98, s=MID, w=0.7, d="5 3", c=ZL2))            # roof overhang
STR.append(rect(380, 1040, 90, 70, f=PALE, s=INK, w=1.6))                     # substation / MCC
STR.append(rect(790, 1140, 90, 60, f=PALE, s=INK, w=1.6))                     # FW pump house
STR.append(rect(400, 1440, 30, 25, f=PALE, s=INK, w=1.4))                     # gatehouse
STR.append(G([line(140 + k * 25, 1130, 140 + k * 25, 1220, s=MID, w=0.5) for k in range(1, 8)] +
             [line(380 + k * 15, 1040, 380 + k * 15, 1110, s=MID, w=0.5) for k in range(1, 6)], c=ZL3))

# ==========================================================================
#                               L-MECH
# ==========================================================================
def tank_fr(tag, cx, cy, r):
    els = [circle(cx, cy, r, f=WHITE, s=INK, w=2.4),
           circle(cx, cy, r - 2, s=STEEL, w=0.7, c=ZL2),                  # rim seal
           circle(cx, cy, r - 7, s=STEEL, w=0.9, c=ZL2),                  # pontoon outer
           circle(cx, cy, r - 20, s=STEEL, w=0.9, c=ZL2)]                 # pontoon inner / deck
    els.append(G([line(*polar(cx, cy, r - 7, a), *polar(cx, cy, r - 20, a), s=STEEL, w=0.6)
                  for a in frange(0, 337.5, 22.5)], c=ZL2))               # pontoon bulkheads
    # rolling ladder (shell top of stair -> roof)
    a_end = FR_STAIR[0] + FR_STAIR[1]
    ax, ay = polar(cx, cy, r, a_end)
    bx, by = polar(cx, cy, r * 0.35, a_end)
    nx, ny = -math.sin(math.radians(a_end)), math.cos(math.radians(a_end))
    els.append(G([line(ax + nx * 1.6, ay + ny * 1.6, bx + nx * 1.6, by + ny * 1.6, s=INK, w=0.8),
                  line(ax - nx * 1.6, ay - ny * 1.6, bx - nx * 1.6, by - ny * 1.6, s=INK, w=0.8)], c=ZL2))
    # L3: roof drain sump, roof legs, nozzles, mixers
    micro = [circle(cx, cy, 5, f=PALE, s=INK, w=0.8)]
    for rr_, cnt in ((r * 0.45, 12), (r * 0.7, 18)):
        micro += [circle(*polar(cx, cy, rr_, k * 360 / cnt), 1.2, f=STEEL) for k in range(cnt)]
    for off in (-6, 6):                                                   # south nozzle CL
        micro.append(line(cx + off, cy + r + 16, cx + off, cy + r - 14, s=INK, w=0.5, d=DASHDOT))
        micro.append(circle(cx + off, cy + r - 1, 2.2, f=WHITE, s=INK, w=0.8))
    for a in (30, 120):                                                   # side-entry mixers
        mx, my = polar(cx, cy, r + 5, a)
        micro.append(rect(mx - 4, my - 2.5, 8, 5, f=WHITE, s=INK, w=0.7))
        micro.append(line(*polar(cx, cy, r - 12, a), *polar(cx, cy, r + 10, a), s=INK, w=0.5, d=DASHDOT))
    els.append(G(micro, c=ZL3))
    return G(els, data_cmp_id="CMP-EQP-TANK", data_tag=tag, c="dt-interactive")


def tank_cone(tag, cx, cy, r, nozzle_stubs=True):
    els = [circle(cx, cy, r, f=WHITE, s=INK, w=2.2),
           circle(cx, cy, r - 2.5, s=STEEL, w=0.7, c=ZL2),                # roof eave
           circle(cx, cy, r * 0.5, s=STEEL, w=0.6, c=ZL2),                # centre ring girder
           circle(cx, cy, 5, f=PALE, s=INK, w=0.9)]                       # centre vent
    els.append(G([line(*polar(cx, cy, 5, a), *polar(cx, cy, r - 2.5, a), s=STEEL, w=0.4)
                  for a in frange(0, 345, 15)], c=ZL2))                   # rafters
    micro = [circle(*polar(cx, cy, r * 0.72, 300), 3, f=WHITE, s=INK, w=0.7),   # roof manway
             circle(*polar(cx, cy, r * 0.72, 40), 2, f=WHITE, s=INK, w=0.7)]   # PV vent
    for a in (60, 100):                                                   # foam chambers
        fx, fy = polar(cx, cy, r - 1, a)
        micro.append(rect(fx - 3, fy - 2, 6, 4, f=PALE, s=INK, w=0.6))
    if nozzle_stubs:
        for off in (-6, 6):
            micro.append(line(cx - r - 14, cy + off, cx - r + 8, cy + off, s=INK, w=0.5, d=DASHDOT))
            micro.append(circle(cx - r + 0.5, cy + off, 2, f=WHITE, s=INK, w=0.8))
    els.append(G(micro, c=ZL3))
    return G(els, data_cmp_id="CMP-EQP-TANK", data_tag=tag, c="dt-interactive")


for tag, cx, cy in TK1:
    MEC.append(tank_fr(tag, cx, cy, TK1_R))
for tag, cx, cy in TK2:
    MEC.append(tank_cone(tag, cx, cy, TK2_R))
MEC.append(tank_cone(FW_TK[0], FW_TK[1], FW_TK[2], FW_R, nozzle_stubs=False))

# --- pump skids ---------------------------------------------------------------
for i, tag in enumerate(PUMP_TAGS):
    x, y = PX0 + PITCH * i, PUMP_Y
    els = [rect(x, y, 40, 20, f=PALE, s=INK, w=1, c=ZL2),                 # baseplate
           circle(x + 11, y + 10, 7.5, f=WHITE, s=INK, w=1.4),            # casing
           rect(x + 24, y + 3, 15, 14, rx=2, f=WHITE, s=INK, w=1.2),      # motor
           G([rect(x + 19, y + 7, 5, 6, f=MID, s=INK, w=0.6),             # coupling guard
              rect(x + 29, y - 1, 6, 4, f=PALE, s=INK, w=0.6),            # terminal box
              line(x - 4, y + 10, x + 44, y + 10, s=INK, w=0.5, d=DASHDOT)] +   # shaft CL
             [line(x + xx, y + 3, x + xx, y + 17, s=INK, w=0.3) for xx in (27, 29.5, 32, 34.5, 37)] +
             [circle(x + bx, y + by, 1, f=INK) for bx, by in ((3, 3), (37, 3), (3, 17), (37, 17))],
             c=ZL3)]
    MEC.append(G(els, data_cmp_id="CMP-EQP-PUMP", data_tag=tag, c="dt-interactive"))

# --- heat exchangers (crude heaters) ---------------------------------------------
HX = [("E-0101A", 340.0, 925.0), ("E-0101B", 470.0, 925.0)]
for tag, x, y in HX:
    els = [rect(x, y, 80, 16, rx=7, f=WHITE, s=INK, w=1.4),
           rect(x + 10, y - 3, 6, 22, f=PALE, s=INK, w=0.8, c=ZL2),       # saddles
           rect(x + 60, y - 3, 6, 22, f=PALE, s=INK, w=0.8, c=ZL2),
           G([line(x + 8, y + 3 + k * 2.5, x + 72, y + 3 + k * 2.5, s=STEEL, w=0.4) for k in range(5)] +
             [circle(x + 12, y, 2, f=WHITE, s=INK, w=0.7), circle(x + 68, y, 2, f=WHITE, s=INK, w=0.7)],
             c=ZL3)]
    MEC.append(G(els, data_cmp_id="CMP-EQP-HX", data_tag=tag))

# --- FW pumps (inside pump house outline) -------------------------------------------
MEC.append(G([G([circle(810 + 22 * k, 1170, 5, f=WHITE, s=INK, w=1),
                 rect(816 + 22 * k, 1166, 8, 8, rx=1, f=WHITE, s=INK, w=0.8)])
              for k in range(3)], c=ZL2))

# --- truck loading bays -------------------------------------------------------------
for k, xl in enumerate(BAY_X):
    tag = f"BAY-{k + 1:02d}"
    arm_x = ISL_X[k] + ISL_W / 2                                          # serving island centre
    bay_c = xl + BAY_W / 2
    els = [rect(xl, ISL_Y0, BAY_W, ISL_Y1 - ISL_Y0, s=INK, w=1),                       # bay envelope
           G([line(xl, 1020, xl, 1390, s=MID, w=0.6, d="8 4"),                       # lane edges
              line(xl + BAY_W, 1020, xl + BAY_W, 1390, s=MID, w=0.6, d="8 4"),
              rect(bay_c - 6.5, 1098, 13, 80, rx=5, f=WHITE, s=STEEL, w=0.9),         # tanker barrel
              rect(bay_c - 5.5, 1180, 11, 16, rx=2, f=WHITE, s=STEEL, w=0.9),         # cab
              line(xl + 2, 1090, xl + BAY_W - 2, 1090, s=INK, w=0.8, d="3 2")], c=ZL2),  # stop line
           G([circle(bay_c, yy, 1.8, f=WHITE, s=INK, w=0.6) for yy in (1118, 1138, 1158)] +   # manways
             [circle(arm_x, 1140, 32, s=STEEL, w=0.7, d="4 3"),                             # arm envelope
              circle(arm_x, 1140, 3, f=INK),                                                # pedestal
              line(arm_x, 1140, bay_c, 1138, s=INK, w=1.6)], c=ZL3)]                        # loading arm
    MEC.append(G(els, data_cmp_id="CMP-EQP-BAY", data_tag=tag, c="dt-interactive"))

# ==========================================================================
#                               L-PIPE
# ==========================================================================
def pl(d, kind="A", w=3.0):
    return path(d, s=INK if kind == "A" else STEEL, w=w, lj="round")


# S1 manifold header, both lines, with expansion loops (south)
S1_LOOPS_A = [(860, 76, 46), (1500, 76, 46)]
S1_LOOPS_B = [(860, 52, 32), (1500, 52, 32)]
PIP.append(pl(hpath(S1_A, S1_X0, S1_X1, S1_LOOPS_A, +1), "A"))
PIP.append(pl(hpath(S1_B, S1_X0, S1_X1, S1_LOOPS_B, +1), "B"))

# S2: vertical + horizontal to gantry, loops projecting north
PIP.append(pl(hpath(S2H_A, S2V_AX, 1590, [(1350, 36, 24)], -1, start=f"M{S2V_AX},{S1_A} V{S2H_A}"), "A"))
PIP.append(pl(hpath(S2H_B, S2V_BX, 1600, [(1350, 58, 38)], -1, start=f"M{S2V_BX},{S1_B} V{S2H_B}"), "B"))
for x in (1410, 1470, 1530, 1590):                        # drops to loading-arm pedestals
    PIP.append(pl(f"M{x},{S2H_A} V1140", "A", 2.6))
    flange(x, 1052, "v")

# Tank Farm 1 branches (two lines per tank)
for _, cx, cy in TK1:
    y_end = cy + math.sqrt(TK1_R ** 2 - 36)
    PIP.append(pl(f"M{cx-6},{S1_A} V{n(y_end)}", "A"))
    PIP.append(pl(f"M{cx+6},{S1_B} V{n(y_end)}", "B"))
    valve(cx - 6, 646, "v")
    valve(cx + 6, 654, "v")
    flange(cx - 6, y_end + 8, "v")
    flange(cx + 6, y_end + 8, "v")

# Tank Farm 2 branches (risers + stubs into each cone-roof tank)
for col, cx in enumerate((TK2[0][1], TK2[1][1])):
    xa, xb = cx - 84, cx - 74
    top_cy, bot_cy = TK2[0][2], TK2[2][2]
    xs_ = cx - math.sqrt(TK2_R ** 2 - 36)
    PIP.append(pl(f"M{xa},{S1_A} V{top_cy-6} H{n(xs_)}", "A", 2.6))
    PIP.append(pl(f"M{xb},{S1_B} V{top_cy+6} H{n(xs_)}", "B", 2.6))
    PIP.append(pl(f"M{xa},{bot_cy-6} H{n(xs_)}", "A", 2.6))
    PIP.append(pl(f"M{xb},{bot_cy+6} H{n(xs_)}", "B", 2.6))
    valve(xa, 646, "v")
    valve(xb, 654, "v")
    for yy in (top_cy - 6, top_cy + 6, bot_cy - 6, bot_cy + 6):
        flange(xs_ - 6, yy, "h")

# Pump station piping
xs_list = [PX0 + PITCH * i + 11 for i in range(6)]
PIP.append(pl(f"M{S1_X0 + 15},{S1_B} V850 H{xs_list[-1]}", "B", 3.0))          # suction header
PIP.append(pl(f"M{xs_list[0]},745 H790 V{S1_A}", "A", 3.0))                    # discharge header
for xs in xs_list:
    PIP.append(pl(f"M{xs},805 V850", "B", 2.4))
    PIP.append(pl(f"M{xs},785 V745", "A", 2.4))
    valve(xs, 830, "v")
    check_valve(xs, 770)
    valve(xs, 756, "v")
    flange(xs, 806, "v")
    flange(xs, 780, "v")
for _, x, y in HX:                                        # heater tie-ins to suction header
    for xo in (12, 68):
        PIP.append(pl(f"M{x+xo},850 V{y}", "B", 2.2))
        flange(x + xo, y - 8, "v")

# Manifold block (5 headers + valve ladders)
MF_Y = [740 + 25 * i for i in range(5)]
PIP.append(pl(f"M1000,{MF_Y[0]} H{S2V_AX}", "A", 2.8))
PIP.append(pl(f"M1000,{MF_Y[1]} H{S2V_BX}", "B", 2.8))
for yy in MF_Y[2:]:
    PIP.append(pl(f"M1000,{yy} H1250", "A" if yy % 50 else "B", 2.8))
PIP.append(pl(f"M1006,{MF_Y[0]} V{S1_A}", "A", 2.4))
PIP.append(pl(f"M1018,{MF_Y[1]} V{S1_B}", "B", 2.4))
for xt in (1070, 1190):
    PIP.append(path(f"M{xt},{MF_Y[0]} V{MF_Y[-1]}", s=INK, w=1.6))
    for a_, b_ in zip(MF_Y[:-1], MF_Y[1:]):
        valve(xt, (a_ + b_) / 2, "v", 4)
for yy in MF_Y:
    for xv in (1035, 1230):
        if xv == 1230 and yy in MF_Y[:2]:
            continue
        valve(xv, yy, "h", 4)
    if yy in MF_Y[2:]:
        flange(1250, yy, "h")
for xv, yy in ((1006, 700), (1018, 708)):
    valve(xv, yy, "v", 3.6)

# tank-farm / header isolation valves along S1 and S2 lines
for xv in (330, 700, 1100, 1250):
    valve(xv, S1_A, "h", 4)
valve(S2V_AX, 800, "v", 4)
valve(S2V_BX, 800, "v", 4)
for xv in (1410, 1470, 1530, 1590):
    valve(xv, 960, "v", 4)

PIP.append(G(VAL2, c=ZL2))
PIP.append(G(VAL3, c=ZL3))
PIP.append(G(FLG, c=ZL3))
# pipe supports inside bunds (L2) -- low sleepers under tank-farm lines
sup = []
for _, cx, cy in TK1:
    for yy in range(int(cy + TK1_R + 12), int(B1[3] - WALL_T), 30):
        sup.append(rect(cx - 12, yy, 24, 3, f=STEEL, s=INK, w=0.3))
PIP.append(G(sup, c=ZL2))

# ==========================================================================
#                               L-FIRE
# ==========================================================================
mains = [rect(58, 58, W - 116, H - 116, s=STEEL, w=2.4, d="16 4 3 4"),               # ring main
         path("M982,58 V1442", s=STEEL, w=2.0, d="16 4 3 4"),                         # internal branch
         path("M880,1170 H982", s=STEEL, w=2.0, d="16 4 3 4")]                        # FW pump-house tie
FIR.append(G(mains))

hyd = []
for x in range(200, 1801, 200):
    hyd.append((x, 48))
    if not (300 <= x <= 420):
        hyd.append((x, H - 48))
for y in range(200, 1401, 200):
    hyd.append((48, y))
    hyd.append((W - 48, y))
for y in range(200, 1400, 200):
    if any(a - 12 <= y <= b + 12 for a, b in (R5_BAND, R2_BAND)):
        continue
    hyd.append((982, y))
hyd_sym, hyd_spur, hyd_tag = [], [], []
for i, (x, y) in enumerate(hyd, 1):
    hyd_sym += [circle(x, y, 4.5, f=WHITE, s=INK, w=1.2), circle(x, y, 1.4, f=INK)]
    if x in (48, W - 48) or y in (48, H - 48):
        tx, ty = (58, y) if x == 48 else ((W - 58, y) if x == W - 48 else ((x, 58) if y == 48 else (x, H - 58)))
        hyd_spur.append(line(x, y, tx, ty, s=STEEL, w=1.2))
    hyd_tag.append(text(x + 7, y - 6, f"FH-{i:02d}", size=5.5))
FIR.append(G(hyd_sym))
FIR.append(G(hyd_spur, c=ZL2))
FIR.append(G(hyd_tag, c=ZL3))

FM = [("FM-01", 865, 160, (982, 160)), ("FM-02", 865, 555, (982, 555)),
      ("FM-03", 1270, 160, (982, 160)), ("FM-04", 1270, 555, (982, 555)),
      ("FM-05", 1870, 360, (W - 58, 360)), ("FM-06", 260, 740, (58, 740)),
      ("FM-07", 1352, 1060, (982, 1060)), ("FM-08", 1710, 1060, (W - 58, 1060))]
cov, fm_sym, fm_sp, fm_tag = [], [], [], []
for tag, x, y, tgt in FM:
    cov.append(circle(x, y, U(50), s=MID, w=0.7, d="10 6", o=0.55))
    fm_sp.append(line(x, y, tgt[0], tgt[1], s=STEEL, w=1.4, d="6 3"))
    fm_sym += [rect(x - 6, y - 6, 12, 12, f=WHITE, s=INK, w=1.3),
               line(x - 6, y - 6, x + 6, y + 6, s=INK, w=0.8), line(x - 6, y + 6, x + 6, y - 6, s=INK, w=0.8),
               circle(x, y, 2.4, f=INK)]
    fm_tag.append(text(x + 9, y + 3, tag, size=6.5))
FIR.append(G(cov, c=ZL2))
FIR.append(G(fm_sp, c=ZL2))
FIR.append(G(fm_sym))
FIR.append(G(fm_tag, c=ZL2))

# ==========================================================================
#                               L-ANNO
# ==========================================================================
# coordinate grid (40 m modules) with bubbles on all four sides
grid, bub = [], []
cols_ = "ABCDEFGHI"
for k, x in enumerate(range(200, 1801, 200)):
    grid.append(line(x, 26, x, H - 26, s=MID, w=0.5, d="2 6", o=0.7))
    for yb in (17, H - 17):
        bub += [circle(x, yb, 9, f=WHITE, s=INK, w=0.8), text(x, yb + 3, cols_[k], size=8, anchor="middle")]
for k, y in enumerate(range(200, 1401, 200)):
    grid.append(line(26, y, W - 26, y, s=MID, w=0.5, d="2 6", o=0.7))
    for xb in (17, W - 17):
        bub += [circle(xb, y, 9, f=WHITE, s=INK, w=0.8), text(xb, y + 3, str(k + 1), size=8, anchor="middle")]
ANN.append(G(grid, c=ZL2))
ANN.append(G(bub))

# zone labels + zone envelopes
ANN.append(text(B1[0] + 6, 131, "ZONE 1 — TANK FARM 1 · CRUDE OIL (CLASS I) · FLOATING ROOF", size=11, weight="bold"))
ANN.append(text(B2[0] + 6, 131, "ZONE 2 — TANK FARM 2 · REFINED PRODUCTS / DIESEL · CONE ROOF", size=11, weight="bold"))
ANN.append(text(322, 708, "ZONE 3 — MANIFOLD & PUMP STATION (PUMPS)", size=10, weight="bold"))
ANN.append(text(996, 706, "ZONE 3 — MANIFOLD", size=10, weight="bold"))
ANN.append(text(1380, 1295, "ZONE 4 — TRUCK LOADING GANTRY (4 BAYS)", size=11, weight="bold"))
ANN.append(G([rect(312, 712, 456, 180, s=INK, w=0.8, d="14 4 3 4"),
              rect(986, 710, 283, 158, s=INK, w=0.8, d="14 4 3 4"),
              rect(1360, 1020, 340, 372, s=INK, w=0.8, d="14 4 3 4")]))

# tank tags
for tag, cx, cy in TK1:
    ANN.append(text(cx, cy - 2, tag, size=17, anchor="middle", weight="bold"))
    ANN.append(text(cx, cy + 14, f"Ø{TK1_D:.0f} m · FLOATING ROOF · H {TK1_H:.0f} m", size=7.5, anchor="middle"))
for tag, cx, cy in TK2:
    ANN.append(text(cx, cy - 20, tag, size=12, anchor="middle", weight="bold"))
    ANN.append(text(cx, cy - 8, f"Ø{TK2_D:.0f} m · CONE ROOF", size=6.5, anchor="middle"))
ANN.append(text(FW_TK[1], FW_TK[2] - 12, FW_TK[0], size=10, anchor="middle", weight="bold"))
ANN.append(text(FW_TK[1], FW_TK[2], f"FIRE WATER Ø{FW_D:.0f} m", size=6.5, anchor="middle"))

# pump / HX / bay / building tags
ANN.append(G([text(PX0 + PITCH * i + 18, 773, t, size=7, weight="bold") for i, t in enumerate(PUMP_TAGS)], c=ZL2))
ANN.append(G([text(x + 40, y + 29, t, size=7, anchor="middle", weight="bold") for t, x, y in HX], c=ZL2))
for k, xl in enumerate(BAY_X):
    ANN.append(text(xl + BAY_W / 2, 1247, f"BAY-{k + 1:02d}", size=8, anchor="middle", weight="bold"))
ANN.append(text(240, 1181, "ADMIN / CONTROL BUILDING", size=8, anchor="middle", weight="bold"))
ANN.append(text(425, 1078, "SUBSTATION / MCC", size=7, anchor="middle", weight="bold"))
ANN.append(text(835, 1215, "FIRE WATER PUMP HOUSE", size=7, anchor="middle", weight="bold"))
ANN.append(text(270, 1056, "PARKING", size=7, anchor="middle"))
ANN.append(text(415, 1432, "GATE-HOUSE", size=6.5, anchor="middle"))
ANN.append(text((g0 + g1) / 2, 1486, "MAIN GATE", size=8, anchor="middle", weight="bold"))
ANN.append(text(1125, 1222, "RETENTION / OWS BASIN", size=9, anchor="middle", weight="bold"))
ANN.append(text(1135, 902, "MANIFOLD M-0101  (5 HEADERS)", size=8, anchor="middle", weight="bold"))
ANN.append(G([text(450, 662, "SLEEPERWAY S1 · 6.0 m · HEADER A (PRODUCT) / HEADER B (SUCTION)", size=6.5),
              text(1301, 905, "S2 · TO LOADING GANTRY", size=6.5),
              text(860, 735, "EXP. LOOP", size=6, anchor="middle"),
              text(1500, 735, "EXP. LOOP", size=6, anchor="middle"),
              text(1350, 883, "EXP. LOOP", size=6, anchor="middle")], c=ZL2))

# roads
ANN.append(G([text(500, 94, "PERIMETER FIRE ACCESS ROAD · 8.0 m · Ri = 15 m", size=8, anchor="middle"),
              text(R1X + 3, 400, "FIRE ACCESS ROAD R-01 · 8.0 m", size=8, anchor="middle", rot=-90),
              text(1130, R5Y + 3, "ACCESS ROAD R-02 · 8.0 m", size=8, anchor="middle"),
              text(600, R2Y + 3, "ACCESS ROAD R-03 · 8.0 m", size=8, anchor="middle"),
              text(850, R6Y + 3, "R-04 PUMP ACCESS", size=7, anchor="middle")], c=ZL2))

# dimensions (shell-to-shell spacing)
ANN.append(dim_h(TK1[0][1] + TK1_R, TK1[1][1] - TK1_R, 340, f"{GAP1:.1f} m"))
ANN.append(dim_h(TK2[0][1] + TK2_R, TK2[1][1] - TK2_R, TK2[0][2], f"{GAP2_X:.1f} m"))
ANN.append(dim_v(TK2[0][1] + 30, TK2[0][2] + TK2_R, TK2[2][2] - TK2_R, f"{GAP2_Y:.1f} m"))

# bund data block
def nf(v):
    return f"{v:,.0f}"


ANN.append(G([
    text(1010, 196, "BUND DATA  (NFPA 30 · 110 % OF LARGEST TANK)", size=8, weight="bold"),
    text(1010, 208, f"B-01  TK-0101/0102  V = {nf(V1)} m³  → 110 % = {nf(C1['req'])} m³", size=7),
    text(1010, 218, f"      H req. {C1['h_req']:.2f} m → wall H {C1['h_des']:.1f} m · net {nf(C1['net'])} m³", size=7),
    text(1010, 232, f"B-02  TK-0201..0204  V = {nf(V2)} m³  → 110 % = {nf(C2['req'])} m³", size=7),
    text(1010, 242, f"      H req. {C2['h_req']:.2f} m → wall H {C2['h_des']:.1f} m · net {nf(C2['net'])} m³", size=7),
    text(1010, 252, f"      fire-break walls H {INT_H:.1f} m · cell = {cell_pct:.0f} % of tank", size=7),
    text(1010, 266, "SHELL SPACING  (≥ D/6)", size=8, weight="bold"),
    text(1010, 277, f"TF1  {GAP1:.1f} m ≥ {TK1_D/6:.1f} m   ·   TF2  {min(GAP2_X, GAP2_Y):.1f} m ≥ {TK2_D/6:.1f} m", size=7),
]))
ANN.append(G([text(142, 160, "BUND B-01", size=8, weight="bold"),
              text(142, 170, f"110 % × TK-0101 = {nf(C1['req'])} m³", size=6.5),
              text(142, 180, f"WALL H {C1['h_des']:.1f} m", size=6.5)], c=ZL2))

# compass rose (plant north = up)
cr_x, cr_y = 1145, 370
ANN.append(G([circle(cr_x, cr_y, 38, s=INK, w=1), circle(cr_x, cr_y, 3, f=INK),
              poly([(cr_x, cr_y - 38), (cr_x - 7, cr_y), (cr_x + 7, cr_y)], f=INK),
              poly([(cr_x, cr_y + 38), (cr_x - 7, cr_y), (cr_x + 7, cr_y)], f=WHITE, s=INK, w=0.8),
              line(cr_x - 38, cr_y, cr_x + 38, cr_y, s=INK, w=0.8),
              text(cr_x, cr_y - 43, "N", size=12, anchor="middle", weight="bold"),
              text(cr_x, cr_y + 52, "S", size=8, anchor="middle"),
              text(cr_x + 46, cr_y + 3, "E", size=8), text(cr_x - 46, cr_y + 3, "W", size=8, anchor="end"),
              text(cr_x, cr_y + 66, "PLANT NORTH", size=7, anchor="middle")]))
# scale bar 0-40 m
sb_x, sb_y = 1010, 470
sb = []
for k in range(4):
    sb.append(rect(sb_x + k * 50, sb_y, 50, 6, f=INK if k % 2 == 0 else WHITE, s=INK, w=0.8))
for k in range(5):
    sb.append(text(sb_x + k * 50, sb_y + 17, f"{k * 10}", size=7, anchor="middle"))
sb.append(text(sb_x + 215, sb_y + 17, "m", size=7))
sb.append(text(sb_x, sb_y - 6, "SCALE 1 unit = 0.2 m  (5 units / m)", size=7))
ANN.append(G(sb))

# title block
tb = [rect(140, 1262, 500, 118, f=WHITE, s=INK, w=1.4),
      line(140, 1290, 640, 1290, s=INK, w=0.8), line(400, 1290, 400, 1380, s=INK, w=0.8),
      text(150, 1281, "GENERAL ARRANGEMENT — PLOT PLAN · BULK LIQUID HYDROCARBON TERMINAL", size=10, weight="bold"),
      text(150, 1306, "PLOT 400 m × 300 m   ·   1 UNIT = 0.2 m", size=8),
      text(150, 1320, "DRAWING  DT-UI-SVG-DOC-001 / GA-001      REV A", size=8),
      text(150, 1334, "TANK FARM 1: 2 × FR Ø40 m   ·   TANK FARM 2: 4 × CR Ø25 m", size=8),
      text(150, 1348, "PUMPS: 6 × CENTRIFUGAL   ·   GANTRY: 4 BAYS", size=8),
      text(150, 1366, "LAYERS: L-CIVIL · L-STRUCT · L-MECH · L-PIPE · L-FIRE · L-ANNO", size=7),
      text(410, 1306, "CODES / STANDARDS", size=8, weight="bold"),
      text(410, 1320, "NFPA 30 (spacing, diking)", size=7.5),
      text(410, 1332, "ISA-101 (HMI, progressive disclosure)", size=7.5),
      text(410, 1344, "ISO 13567 / AIA CAD layering", size=7.5),
      text(410, 1356, "ISO 14224 (APM data binding)", size=7.5),
      text(410, 1372, "COLOUR RESERVED FOR LIVE ALARMS", size=7, weight="bold")]
ANN.append(G(tb))

# legend
lg_x, lg_y = 680, 1262
lg = [rect(lg_x, lg_y, 240, 118, f=WHITE, s=INK, w=1.2),
      text(lg_x + 8, lg_y + 12, "LEGEND", size=8, weight="bold")]
rows = [("sym_fr", "FLOATING ROOF TANK"), ("sym_cr", "CONE ROOF TANK"), ("pipeA", "PROCESS HEADER A / B"),
        ("fire", "FIRE-WATER RING MAIN"), ("hyd", "HYDRANT"), ("fm", "FOAM MONITOR + COVERAGE"),
        ("bund", "CONCRETE BUND"), ("slp", "PIPE SLEEPERWAY (6 m)")]
for i, (kind, label) in enumerate(rows):
    col = i // 4
    yy = lg_y + 26 + (i % 4) * 22
    xx = lg_x + 14 + col * 118
    if kind == "sym_fr":
        lg += [circle(xx + 6, yy, 6, f=WHITE, s=INK, w=1.4), circle(xx + 6, yy, 3.5, s=STEEL, w=0.6)]
    elif kind == "sym_cr":
        lg += [circle(xx + 6, yy, 6, f=WHITE, s=INK, w=1.4), circle(xx + 6, yy, 1.5, f=INK)]
    elif kind == "pipeA":
        lg += [line(xx, yy - 2, xx + 14, yy - 2, s=INK, w=2.4), line(xx, yy + 3, xx + 14, yy + 3, s=STEEL, w=2.4)]
    elif kind == "fire":
        lg += [line(xx, yy, xx + 14, yy, s=STEEL, w=2, d="6 2 2 2")]
    elif kind == "hyd":
        lg += [circle(xx + 6, yy, 4.5, f=WHITE, s=INK, w=1.2), circle(xx + 6, yy, 1.4, f=INK)]
    elif kind == "fm":
        lg += [rect(xx, yy - 6, 12, 12, f=WHITE, s=INK, w=1.3), line(xx, yy - 6, xx + 12, yy + 6, s=INK, w=0.8),
               line(xx, yy + 6, xx + 12, yy - 6, s=INK, w=0.8)]
    elif kind == "bund":
        lg += [rect(xx, yy - 4, 14, 8, f="url(#hatch-concrete)", s=INK, w=1)]
    elif kind == "slp":
        lg += [rect(xx, yy - 4, 14, 8, f=CONC, s=STEEL, w=0.8)]
    lg.append(text(xx + 20, yy + 3, label, size=6.5))
lg.append(text(lg_x + 8, lg_y + 112, "L2 / L3 DETAIL REVEALED BY SEMANTIC ZOOM CLASSES", size=6))
ANN.append(G(lg))


# --------------------------------------------------------------------------
# Assemble document
# --------------------------------------------------------------------------
STYLE = """
.dt-canvas { font-family: Arial, Helvetica, sans-serif; background: #EDF2F4; }
/* ISA-101 progressive disclosure with fluid opacity transitions (DT-UI-SVG-DOC-001) */
.dt-zoom-l2, .dt-zoom-l3 {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.zoom-l2 .dt-zoom-l2, .zoom-l3 .dt-zoom-l2 {
  opacity: 1;
  pointer-events: auto;
}
.zoom-l3 .dt-zoom-l3 {
  opacity: 1;
  pointer-events: auto;
}
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
        f'<svg viewBox="0 0 {W} {H}" id="dt-plant-svg" width="100%" height="100%" class="dt-canvas {zoom}" xmlns="http://www.w3.org/2000/svg">',
        "<title>General Arrangement Plot Plan — Bulk Liquid Hydrocarbon Terminal (DT-UI-SVG-DOC-001)</title>",
        "<desc>400 m x 300 m terminal plot; 1 SVG unit = 0.2 m. Layers per AIA CAD / ISO 13567; "
        "ISA-101 semantic zoom classes dt-zoom-l2 / dt-zoom-l3; ISO 14224 data binding on equipment.</desc>",
        f"<defs>{DEFS}</defs>",
        f"<style>{STYLE}</style>",
        layer("L-CIVIL", "dt-layer-civil", CIV),
        layer("L-STRUCT", "dt-layer-struct", STR),
        layer("L-MECH", "dt-layer-mech", MEC),
        layer("L-PIPE", "dt-layer-pipe", PIP),
        layer("L-FIRE", "dt-layer-fire", FIR),
        layer("L-ANNO", "dt-layer-anno", ANN),
        "</svg>",
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------
# Validation & Prototype Sync
# --------------------------------------------------------------------------
def validate(p):
    tree = ET.parse(p)                                   # raises on malformed XML
    root = tree.getroot()
    ns = "{http://www.w3.org/2000/svg}"
    assert root.tag == ns + "svg"
    assert root.get("viewBox") == f"0 0 {W} {H}"
    assert "dt-canvas" in (root.get("class") or "")
    ids = [g.get("id") for g in root if g.tag == ns + "g"]
    assert ids == ["L-CIVIL", "L-STRUCT", "L-MECH", "L-PIPE", "L-FIRE", "L-ANNO"], ids
    inter = [e for e in root.iter(ns + "g") if "dt-interactive" in (e.get("class") or "")]
    by = {}
    for e in inter:
        by.setdefault(e.get("data-cmp-id"), []).append(e.get("data-tag"))
    assert len([t for t in by["CMP-EQP-TANK"] if t.startswith("TK-01")]) == 2
    assert len([t for t in by["CMP-EQP-TANK"] if t.startswith("TK-02")]) == 4
    assert len(by["CMP-EQP-PUMP"]) == 6 and len(by["CMP-EQP-BAY"]) == 4
    for e in root.iter():
        if e.tag.endswith("circle") or e.tag.endswith("rect") or e.tag.endswith("path"):
            pass
    raw = Path(p).read_text(encoding="utf-8")
    for hx in set(re.findall(r"#[0-9A-Fa-f]{6}", raw)):
        r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
        _, _, s = colorsys.rgb_to_hls(r, g, b)
        assert s <= 0.30, f"saturated colour {hx} not allowed for static equipment"
    z2 = sum(1 for e in root.iter() if "dt-zoom-l2" in (e.get("class") or ""))
    z3 = sum(1 for e in root.iter() if "dt-zoom-l3" in (e.get("class") or ""))
    counts = {i: sum(1 for _ in g.iter()) - 1 for i, g in zip(ids, [g for g in root if g.tag == ns + "g"])}
    return by, z2, z3, counts, len(raw)


def sync_prototype_html(svg_text, html_path):
    if not html_path.exists():
        return False
    html = html_path.read_text(encoding="utf-8")
    # Clean svg_text of XML declaration if embedding inside HTML
    clean_svg = re.sub(r'<\?xml[^>]*\?>\s*', '', svg_text)
    pattern = r'(<div id="dt-svg-container">)[\s\S]*?(</div>\s*</div>\s*<!-- =+\s*CONTEXTUAL INSPECTION DRAWER)'
    match = re.search(pattern, html)
    if not match:
        return False
    new_html = html[:match.start(1)] + f'<div id="dt-svg-container">\n{clean_svg}\n        ' + html[match.start(2):]
    html_path.write_text(new_html, encoding="utf-8")
    return True


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("terminal_plot_plan.svg")
    out.parent.mkdir(parents=True, exist_ok=True)
    svg_l1 = build("zoom-l1")
    out.write_text(svg_l1, encoding="utf-8")
    out.with_name(out.stem + "_l2.svg").write_text(build("zoom-l2"), encoding="utf-8")
    out.with_name(out.stem + "_l3.svg").write_text(build("zoom-l3"), encoding="utf-8")
    by, z2, z3, counts, size = validate(out)
    print(f"Wrote {out}  ({size/1024:.0f} KB) — valid XML")
    print("Interactive units :", {k: len(v) for k, v in by.items()})
    print("Tags              :", ", ".join(t for v in by.values() for t in v))
    print("Elements per layer:", counts)
    print(f"Zoom-tagged elems : L2={z2}  L3={z3}")
    print(f"TF1 bund: V_tank={V1:,.0f} m3  110%={C1['req']:,.0f}  H_req={C1['h_req']:.2f} m  wall={C1['h_des']:.1f} m")
    print(f"TF2 bund: V_tank={V2:,.0f} m3  110%={C2['req']:,.0f}  H_req={C2['h_req']:.2f} m  wall={C2['h_des']:.1f} m  "
          f"intermediate cell={cell_pct:.0f}% of tank")
    print(f"Shell spacing: TF1 {GAP1:.1f} m (D/6={TK1_D/6:.1f})  TF2 {GAP2_X:.1f}/{GAP2_Y:.1f} m (D/6={TK2_D/6:.1f})")

    # Auto-sync prototype if present
    proto_html = out.parent / "index.html"
    if not proto_html.exists():
        proto_html = Path(__file__).resolve().parent.parent / "temp" / "canvas-prototype" / "index.html"
    if proto_html.exists():
        if sync_prototype_html(svg_l1, proto_html):
            print(f"Synchronized SVG canvas into {proto_html}")


if __name__ == "__main__":
    main()

