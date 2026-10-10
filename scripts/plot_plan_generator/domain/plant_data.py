"""
Data model and spatial definitions for Tank Farm Alpha (TFA).
"""
import math
from ..config import K, OX, OY, CU, SU, ROT, GRID_DEG, HW
from ..core.geometry import (
    P, uvp, uv_of, offset_poly, clip_half, ray_hit, line_x, Frame,
    dist_poly, dist_seg, pip
)

# Irregular site boundary (traced from survey, design px)
BND = [(480, 10), (967, 187), (936, 252), (803, 352), (806, 497), (790, 512),
       (550, 523), (412, 525), (385, 520), (363, 495), (235, 532), (70, 343), (255, 140)]

BNDU = [P(*p) for p in BND]
_RAW15 = offset_poly(BND, 15)

# Corner merge for SE chamfer (fence vertices 4-5) to keep full 15 m turning radius
ROADC = _RAW15[:4] + [line_x(_RAW15[6], _RAW15[5], _RAW15[3], _RAW15[4])] + _RAW15[6:]
RINGM = offset_poly(BND, 10)             # perimeter fire-water main (px)
HYDR = offset_poly(BND, 5)               # perimeter hydrant line (px)

# Angles for pipe stubs
A_PV, A_MV, A_PU, A_MU = ROT, ROT + 180, GRID_DEG, GRID_DEG + 180      # +v, -v, +u, -u

# Tanks: (tag, u, v, r_px, kind, shell_height_m, pipe_dir_deg)
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
ALL_TANKS = [t for ts in TKS.values() for t in ts] + [FWT]

# Bund definitions and clipping against fence
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

BUND_TANKS = {
    "SW": TKS["SW"],
    "ST": TKS["ST"],
    "CE": TKS["CE"],
    "NE1": [t for t in TKS["NE"] if t[3] == 15],
    "NE2": [t for t in TKS["NE"] if t[3] == 22]
}
WALL_PX = 3.0                            # 6 units = 1.2 m concrete wall

# Roads (plant-grid coordinates)
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
ROAD_EXT = []
for (rid, pts, a_, b_), (_, ppx) in zip(ROADS, ROADS_PX):
    e0, e1 = uv_of(*ppx[0]), uv_of(*ppx[-1])
    if pts[0][1] == pts[-1][1]:
        ROAD_EXT.append(("u", pts[0][1], min(e0[0], e1[0]), max(e0[0], e1[0])))
    else:
        ROAD_EXT.append(("v", pts[0][0], min(e0[1], e1[1]), max(e0[1], e1[1])))

# Sleeperways
SLEEPERS = [("v", 346, -82, 296), ("u", 111, 346, 672), ("v", 672, 20, 264), ("u", 290, 346, 600)]

# Equipment frames
PF, MF, GF = Frame(702, 122), Frame(706, 262), Frame(700, 380)
PUMP_TAGS = ["P-0101A", "P-0101B", "P-0101C", "P-0201A", "P-0201B", "P-0201C"]
PUMP_PITCH, PUMP_X0, PUMP_Y, PUMP_S = 40, 12, 43, 0.7
ISL_W, BAY_W = 14, 30
ISL_X = [(ISL_W + BAY_W) * k for k in range(5)]
BAY_X = [ISL_W + (ISL_W + BAY_W) * k for k in range(4)]
LANE_V = [GF.uv(BAY_X[k_] + BAY_W / 2, 0)[1] for k_ in range(4)]

# Distributed Buildings
BLDG = {
    "MCR": (804, 826, 244, 284),
    "FAR": (600, 624, 436, 470),
    "HV SUB": (730, 750, 342, 368),
    "MCC-1": (308, 332, 28, 62),
    "MCC-2": (616, 640, 150, 182),
    "MCC-3": (628, 652, 436, 470),
    "WH-01": (378, 408, 308, 350),
    "WH-02": (414, 438, 308, 342),
    "FW PUMP HOUSE": (790, 808, 288, 308)
}

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

BLDG_SHORT = {
    "MCR": "MCR", "FAR": "FAR", "HV SUB": "HV SUB", "MCC-1": "MCC-1",
    "MCC-2": "MCC-2", "MCC-3": "MCC-3", "WH-01": "WH-01", "WH-02": "WH-02",
    "FW PUMP HOUSE": "FWPH"
}

BASIN = (765, 815, 190, 240)

GATES = [
    ("G1", "HV ENTRY", 6, (485, 524)),
    ("G2", "HV EXIT", 7, (400, 522.8)),
    ("G3", "EMERGENCY / LV ACCESS", 4, (798, 504.5))
]
GATE_PX = GATES[0][3]
PUB_ROAD = [(380, 610), (1010, 490)]            # public road outside the fence


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


_o23, _o41 = offset_poly(BND, 23), offset_poly(BND, 41)
YARD_PX = [lerp(_o23[4], _o23[3], 0.14), lerp(_o23[4], _o23[3], 0.96),
           lerp(_o41[4], _o41[3], 0.96), lerp(_o41[4], _o41[3], 0.14)]
GANT_W, GANT_Y0, GANT_Y1 = 190, -20, 154

# Zones metadata
ZONES = [
    ("1", "TANK FARM 1 — CRUDE OIL (CLASS I) · FLOATING ROOF", (470, -77)),
    ("2", "TANK FARM 2 — DIESEL · CONE ROOF", (506, 52)),
    ("3", "TANK FARM 3 — REFINED PRODUCTS · CONE ROOF", (493, 190)),
    ("4", "TANK FARM 4 — PRODUCTS (CONE) + CRUDE FR", (520, 362)),
    ("5", "MANIFOLD & PUMP STATION", (727, 185)),
    ("6", "TRUCK LOADING GANTRY (4 BAYS)", (700, 428)),
    ("7", "MCR · FIRE WATER · OWS BASIN · HV SUBSTATION", (800, 255)),
    ("8", "SERVICES — MAINTENANCE WAREHOUSE · LUBE STORE", (408, 372))
]

# Obstacles for free-space validation
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
