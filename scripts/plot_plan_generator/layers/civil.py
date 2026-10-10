"""
Civil & Bottom Layer (L-CIVL-BOTM) generator.
Includes ground canvas, property boundaries, roads, bund walls, sleeperway structures, and buildings.
"""
import math
from ..config import W, H, ROAD_W, ZL2, ZL3, K, HW
from ..core.geometry import (
    P, UVu, uvp, uvpath, pts_path, offset_poly, rounded_closed
)
from ..core.svg_primitives import rect, path, line, polyg, G, text, split
from ..domain.plant_data import (
    BND, BNDU, PUB_ROAD, GATES, ROADC, ROADS_PX, ROAD_EXT, BUNDS, WALL_PX,
    SLEEPERS, PF, MF, GF, PUMP_X0, PUMP_PITCH, ISL_W, ISL_X, BAY_W, BAY_X,
    GANT_W, GANT_Y0, GANT_Y1, BLDG, BASIN, YARD_PX, OBST, CIRC, pip, dist_poly
)


def edge_dirs(ei):
    a_, b_ = BND[ei], BND[(ei + 1) % len(BND)]
    L = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
    d = ((b_[0] - a_[0]) / L, (b_[1] - a_[1]) / L)
    return d, (d[1], -d[0])


def pub_y(x):
    return PUB_ROAD[0][1] + (x - PUB_ROAD[0][0]) * (PUB_ROAD[1][1] - PUB_ROAD[0][1]) / (PUB_ROAD[1][0] - PUB_ROAD[0][0])


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


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def build_civil_layer(palette):
    """Assembles all civil and structural base vectors for L-CIVL-BOTM."""
    CIV = []

    # 1. Canvas Ground
    CIV.append(rect(0, 0, W, H, f=palette.CANVAS_BG))

    # 2. Property limit
    prop = offset_poly(BND, -3)
    CIV.append(path(pts_path([P(*q) for q in prop], True), s=palette.MID, w=1.5, d="30 6 4 6"))

    # 3. Public road outside fence
    pub = [P(*PUB_ROAD[0]), P(*PUB_ROAD[1])]
    CIV.append(line(*pub[0], *pub[1], s=palette.STEEL, w=44))
    CIV.append(line(*pub[0], *pub[1], s=palette.ASPH, w=42))
    CIV.append(line(*pub[0], *pub[1], s=palette.LIGHT, w=1.2, d="14 10", c=ZL2))

    # 4. Gate throats & fence posts
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
        CIV.append(polyg([P(*q) for q in (q1, q2, q3, q4)], f=palette.ASPH, s=palette.STEEL, w=1))
        GATE_U[gid] = (P(*gp), d, nout)

    CIV.append(path(pts_path(BNDU, True), s=palette.INK, w=1.4))
    posts = []
    for i in range(len(BNDU)):
        a, b_ = BNDU[i], BNDU[(i + 1) % len(BNDU)]
        L = math.hypot(b_[0] - a[0], b_[1] - a[1])
        for k_ in range(int(L // 25) + 1):
            t = k_ * 25 / L
            x, y = a[0] + t * (b_[0] - a[0]), a[1] + t * (b_[1] - a[1])
            if any(math.hypot(x - gu[0][0], y - gu[0][1]) < 28 for gu in GATE_U.values()):
                continue
            posts.append(rect(x - 1.5, y - 1.5, 3, 3, f=palette.INK))
    CIV.append(G(posts, c=ZL2))

    for gid, ((gx_, gy_), d, nout) in GATE_U.items():
        for s_ in (-1, 1):
            CIV.append(line(gx_ + s_ * d[0] * 14 + nout[0] * 3, gy_ + s_ * d[1] * 14 + nout[1] * 3,
                            gx_ + s_ * d[0] * 28 + nout[0] * 3, gy_ + s_ * d[1] * 28 + nout[1] * 3, s=palette.INK, w=3))

    # 5. Roads
    perim_pts = [P(*q) for q in ROADC]
    perim_d = rounded_closed(perim_pts, (15.0 / 0.2) + ROAD_W / 2)
    road_lines = [[P(*q) for q in pts] for _, pts in ROADS_PX]

    def road_pass(width, colour):
        out = [path(perim_d, s=colour, w=width, lj="round")]
        for pl_ in road_lines:
            out.append(path(pts_path(pl_), s=colour, w=width, lc="butt", lj="round"))
        return out

    CIV += road_pass(ROAD_W + 2, palette.STEEL)
    CIV += road_pass(ROAD_W, palette.ASPH)

    # Junction fillets
    FIL_CANDIDATES = (75.0, 60.0, 50.0, 40.0, 30.0, 22.0)

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
            if tb != "v" or not (la <= cb <= ha and lb <= ca <= hb):
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
                    fills.append(path(uvpath(poly_uv, True), f=palette.ASPH))
                    edges.append(path(uvpath(arc), s=palette.STEEL, w=1))
    CIV += fills + edges

    # Heavy vehicle staging yard and lanes
    LANE_V = [GF.uv(BAY_X[k_] + BAY_W / 2, 0)[1] for k_ in range(4)]
    LANE_ENTRY_U, LANE_EXIT_U = GF.uv(0, GANT_Y1)[0] - 1.0, GF.uv(0, GANT_Y0)[0]
    G1_IN, _ = proj_on_poly(GATES[0][3], ROADC)
    G2_IN, _ = proj_on_poly(GATES[1][3], ROADC)
    R06_FOOT = ROADS_PX[5][1][0]
    LANE_PROJ = [proj_on_poly(uvp(LANE_ENTRY_U, v_), ROADC)[0] for v_ in LANE_V]
    HV_ENTRY = [G1_IN, ROADC[5], ROADC[4], ROADC[3], LANE_PROJ[-1]]
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
                out.append(polyg([tip, l_, r_], f=palette.INK, s=palette.LIGHT, w=0.6))
                pos += spacing
            pos -= L
        return out

    for gid, role, ei_, gp_ in GATES:
        q_, _i = proj_on_poly(gp_, ROADC)
        dx_, dy_ = q_[0] - gp_[0], q_[1] - gp_[1]
        L_ = math.hypot(dx_, dy_)
        nx2, ny2 = -dy_ / L_ * 11, dx_ / L_ * 11
        CIV.append(polyg([P(gp_[0] + nx2, gp_[1] + ny2), P(q_[0] + nx2, q_[1] + ny2), P(q_[0] - nx2, q_[1] - ny2), P(gp_[0] - nx2, gp_[1] - ny2)],
                         f=palette.ASPH))

    CIV.append(polyg([P(*q) for q in YARD_PX], f=palette.ASPH, s=palette.STEEL, w=1))
    CIV.append(path(pts_path([P(*lerp(YARD_PX[0], YARD_PX[3], 0.5)), P(*lerp(YARD_PX[1], YARD_PX[2], 0.5))]), s=palette.LIGHT, w=1.2, d="10 8", c=ZL2))
    _d6 = edge_dirs(6)[0]
    _wbc = (G1_IN[0] - _d6[0] * 30, G1_IN[1] - _d6[1] * 30)
    _nn = (-_d6[1], _d6[0])
    CIV.append(polyg([P(_wbc[0] + _d6[0] * s_ * 18 + _nn[0] * t_ * 6, _wbc[1] + _d6[1] * s_ * 18 + _nn[1] * t_ * 6)
                      for s_, t_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))], f=palette.CONC, s=palette.INK, w=1))
    hv_arrows = (arrow_polys(HV_ENTRY, 60) + arrow_polys(HV_EXIT, 60) + arrow_polys(HV_YARD_MID, 40, 5, 10) +
                 [p_ for ln in HV_LANES for p_ in arrow_polys(ln[1:], 40, 5, 12)])
    CIV.append(G(hv_arrows))

    stripes = [path(perim_d, s=palette.LIGHT, w=1.2, d="12 9")]
    for pl_ in road_lines:
        stripes.append(path(pts_path(pl_), s=palette.LIGHT, w=1.2, d="12 9"))
    CIV.append(G(stripes, c=ZL2))

    # Bund Walls with safety volumetric data
    BUNDU = {}
    for k_, poly in BUNDS.items():
        outer = [P(*q) for q in poly]
        inner = [P(*q) for q in offset_poly(poly, WALL_PX)]
        BUNDU[k_] = (outer, inner)
        wall = pts_path(outer, True) + " " + pts_path(inner, True)
        CIV.append(path(pts_path(inner, True), f=palette.BUNDFILL))
        CIV.append(path(wall, f=palette.CONC, fill_rule="evenodd",
                        c="bund-wall", data_dike_vol_m3="14500.0", data_dike_height_m="1.80", data_submerged_vol_m3="1200.0"))
        CIV.append(path(wall, f="url(#hatch-concrete)", fill_rule="evenodd", s=palette.INK, w=1.2))

    def wall_line(u0, u1, v0, v1):
        return polyg([UVu(u0, v0), UVu(u1, v0), UVu(u1, v1), UVu(u0, v1)], f=palette.CONC, s=palette.INK, w=0.8)

    for ub in (431, 493, 555):
        CIV.append(wall_line(ub - 1.2, ub + 1.2, 126 + WALL_PX, 254 - WALL_PX))

    SUMPS = {"SW": (560, -20), "ST": (620, 70), "CE": (600, 244), "NE1": (562, 412), "NE2": (668, 418)}
    sump_el = []
    for k_, (su_, sv_) in SUMPS.items():
        c = UVu(su_, sv_)
        sump_el.append(rect(c[0] - 6, c[1] - 6, 12, 12, f=palette.PALE, s=palette.INK, w=1))
    CIV.append(G(sump_el))
    CIV.append(G([G([line(UVu(su_, sv_)[0] - 6, UVu(su_, sv_)[1] - 6, UVu(su_, sv_)[0] + 6, UVu(su_, sv_)[1] + 6, s=palette.INK, w=0.5),
                     line(UVu(su_, sv_)[0] - 6, UVu(su_, sv_)[1] + 6, UVu(su_, sv_)[0] + 6, UVu(su_, sv_)[1] - 6, s=palette.INK, w=0.5)])
                  for (su_, sv_) in SUMPS.values()], c=ZL3))

    # Sleeperway strips
    sl, sleeves = [], []
    for ax, c, a, b in SLEEPERS:
        bands = []
        for (t, cc, lo, hi) in ROAD_EXT:
            if ax == "v" and t == "u" and lo <= c <= hi:
                bands.append((cc - HW, cc + HW))
            if ax == "u" and t == "v" and lo <= c <= hi:
                bands.append((cc - HW, cc + HW))
        for p, q in split(a, b, bands):
            if ax == "v":
                sl.append(polyg([UVu(c - HW, p), UVu(c + HW, p), UVu(c + HW, q), UVu(c - HW, q)], f=palette.CONC, s=palette.STEEL, w=0.8))
            else:
                sl.append(polyg([UVu(p, c - HW), UVu(p, c + HW), UVu(q, c + HW), UVu(q, c - HW)], f=palette.CONC, s=palette.STEEL, w=0.8))
        for (b0, b1) in bands:
            if not (a < b0 and b1 < b):
                continue
            if ax == "v":
                sleeves.append(polyg([UVu(c - HW - 2, b0 - 2), UVu(c + HW + 2, b0 - 2), UVu(c + HW + 2, b1 + 2), UVu(c - HW - 2, b1 + 2)],
                                    s=palette.STEEL, w=1, d="4 2"))
            else:
                sleeves.append(polyg([UVu(b0 - 2, c - HW - 2), UVu(b1 + 2, c - HW - 2), UVu(b1 + 2, c + HW + 2), UVu(b0 - 2, c + HW + 2)],
                                    s=palette.STEEL, w=1, d="4 2"))
    CIV.append(G(sl))
    CIV.append(G(sleeves, c=ZL2))

    # Pads
    corr = []
    for i in range(5):
        xa = PUMP_X0 + PUMP_PITCH * i + 28
        corr.append(rect(xa, 6, PUMP_PITCH - 28, 88, f="url(#hatch-light)", s=palette.MID, w=0.6, d="3 2"))
    corr.append(text(125, 98, "6 m MAINTENANCE CORRIDORS", size=5.5, anchor="middle", fill=palette.INK))
    CIV.append(PF.g([rect(0, 0, 250, 100, f=palette.CONC, s=palette.STEEL, w=1),
                     G([rect(4, 4, 242, 92, s=palette.STEEL, w=0.6, d="5 3")] + corr, c=ZL2)]))
    CIV.append(MF.g([rect(0, 0, 150, 80, f=palette.CONC, s=palette.STEEL, w=1), rect(4, 4, 142, 72, s=palette.STEEL, w=0.6, d="5 3", c=ZL2)]))

    # Basin
    bu0, bu1, bv0, bv1 = BASIN
    CIV.append(polyg([UVu(bu0, bv0), UVu(bu1, bv0), UVu(bu1, bv1), UVu(bu0, bv1)], f="#D0D4DB" if palette.name == "light" else "#1E293B", s=palette.STEEL, w=1.4))
    CIV.append(G([polyg([UVu(bu0 + k_, bv0 + k_), UVu(bu1 - k_, bv0 + k_), UVu(bu1 - k_, bv1 - k_), UVu(bu0 + k_, bv1 - k_)],
                       s=palette.STEEL, w=0.5, d="4 3") for k_ in (6, 12, 18)], c=ZL2))

    # Gantry Apron
    CIV.append(GF.g([rect(-12, GANT_Y0, GANT_W + 24, GANT_Y1 - GANT_Y0, f=palette.ASPH, s=palette.STEEL, w=1)] +
                    [rect(xi, 15, ISL_W, 110, rx=3, f=palette.PALE, s=palette.INK, w=1) for xi in ISL_X]))
    CIV.append(GF.g([line(x, GANT_Y0, x, GANT_Y1, s=palette.LIGHT, w=0.8, d="8 4") for x in (BAY_X[0] - 1, BAY_X[-1] + BAY_W + 1)], c=ZL2))

    # Structures / Bents
    bents = []
    for ax, c, a, b in SLEEPERS:
        bands = [(cc - HW, cc + HW) for (t, cc, lo, hi) in ROAD_EXT
                 if (ax == "v" and t == "u" and lo <= c <= hi) or (ax == "u" and t == "v" and lo <= c <= hi)]
        pos = a + 8
        while pos <= b - 6:
            if not any(x0 - 2 <= pos <= x1 for x0, x1 in bands):
                if ax == "v":
                    bents.append(polyg([UVu(c - HW, pos), UVu(c + HW, pos), UVu(c + HW, pos + 2), UVu(c - HW, pos + 2)],
                                      f=palette.STEEL, s=palette.INK, w=0.3))
                else:
                    bents.append(polyg([UVu(pos, c - HW), UVu(pos, c + HW), UVu(pos + 2, c + HW), UVu(pos + 2, c - HW)],
                                      f=palette.STEEL, s=palette.INK, w=0.3))
            pos += 20
    CIV.append(G(bents, c=ZL2))

    # Gantry canopy, columns
    canopy = [rect(-6, 25, GANT_W + 12, 90, f="none", s=palette.STEEL, w=1.6, d="10 4")]
    cols = []
    for xi in ISL_X:
        xc = xi + ISL_W / 2
        for yc in (33, 107):
            cols.append(rect(xc - 3, yc - 3, 6, 6, f=palette.STEEL, s=palette.INK, w=0.6))
        for off in (-4, 4):
            for yb in (19, 121):
                cols.append(rect(xc + off - 1, yb - 1, 2, 2, f=palette.INK))
    beams = [line(5, yc, GANT_W - 5, yc, s=palette.STEEL, w=0.7, d="6 3") for yc in (33, 107)]
    beams += [line(xi + 7, 33, xi + 7, 107, s=palette.STEEL, w=0.7, d="6 3") for xi in ISL_X]
    CIV.append(GF.g(canopy + cols))
    CIV.append(GF.g(beams, c=ZL2))
    CIV.append(GF.g([rect(GANT_W + 14, 40, 16, 44, f=palette.WHITE, s=palette.INK, w=1)] +
                    [G([line(GANT_W + 14, yy, GANT_W + 30, yy, s=palette.INK, w=0.4) for yy in range(43, 84, 3)], c=ZL3)]))

    # Buildings
    for name, (a0, a1, b0, b1) in BLDG.items():
        CIV.append(polyg([UVu(a0, b0), UVu(a1, b0), UVu(a1, b1), UVu(a0, b1)], f=palette.PALE, s=palette.INK, w=1.6))
        CIV.append(polyg([UVu(a0 - 2, b0 - 2), UVu(a1 + 2, b0 - 2), UVu(a1 + 2, b1 + 2), UVu(a0 - 2, b1 + 2)], s=palette.MID, w=0.7, d="5 3", c=ZL2))

    GATEHOUSES = {}
    for gid, ei_, off_ in (("G1", 6, 16), ("G2", 7, 16)):
        d_, nout_ = edge_dirs(ei_)
        gp_ = [g_ for g_ in GATES if g_[0] == gid][0][3]
        cc = (gp_[0] - nout_[0] * (HW + 11) + d_[0] * off_, gp_[1] - nout_[1] * (HW + 11) + d_[1] * off_)
        GATEHOUSES[gid] = [(cc[0] + d_[0] * s_ * 9 - nout_[0] * t_ * 6, cc[1] + d_[1] * s_ * 9 - nout_[1] * t_ * 6)
                           for s_, t_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        CIV.append(polyg([P(*q) for q in GATEHOUSES[gid]], f=palette.PALE, s=palette.INK, w=1.4))

    # R-06 crossing sleeves for suction / manifold branches
    for (a_, b_) in [(122, 122), (262, 262)]:
        sleeves_extra = polyg([UVu(690 - HW - 2, a_ - 8), UVu(690 + HW + 2, a_ - 8), UVu(690 + HW + 2, a_ + 8), UVu(690 - HW - 2, a_ + 8)],
                              s=palette.STEEL, w=1, d="4 2")
        CIV.append(G([sleeves_extra], c=ZL2))

    return CIV, GATE_U, GATEHOUSES, _wbc
