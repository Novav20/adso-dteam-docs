"""
Fire Protection & Safety Layer (L-FIRE-PROT) generator.
Includes fire-water ring mains, road branch mains, hydrants (FH-XX),
foam monitors (FM-XX), coverage circles, and supply spurs.
"""
import math
from ..config import ZL2, ZL3
from ..core.geometry import U, P, uvp, pts_path, offset_poly, pip, dist_poly
from ..core.svg_primitives import circle, line, rect, path, text, G
from ..domain.plant_data import (
    BND, GATES, ROADS, ROADS_PX, BUNDS, free
)


def build_fire_layer(palette):
    """Assembles all fire protection mains, hydrants, and foam towers for L-FIRE-PROT."""
    FIR = []

    # 1. Fire-water ring main and road underground mains
    RINGM = offset_poly(BND, 10)
    mains = [path(pts_path([P(*q) for q in RINGM], True), s=palette.STEEL, w=2.4, d="16 4 3 4")]
    main_segs = [(RINGM[i], RINGM[(i + 1) % len(RINGM)]) for i in range(len(RINGM))]

    for (rid, pts), (_, pu, _s0, _s1) in zip(ROADS_PX, ROADS):
        (u1, v1), (u2, v2) = pu[0], pu[-1]
        da = uvp(0, 6) if v1 == v2 else uvp(6, 0)
        sa = (pts[0][0] + da[0], pts[0][1] + da[1])
        sb = (pts[-1][0] + da[0], pts[-1][1] + da[1])
        mains.append(path(pts_path([P(*sa), P(*sb)]), s=palette.STEEL, w=2.0, d="16 4 3 4"))
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

    # 2. Hydrants (perimeter + internal roads)
    HYDR = offset_poly(BND, 5)
    GATE_PX = GATES[0][3]
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
        hyd_sym += [circle(x, y, 4.5, f=palette.WHITE, s=palette.INK, w=1.2), circle(x, y, 1.4, f=palette.INK)]
        m_ = nearest_main(q)
        if m_ is not None and math.hypot(q[0] - m_[0], q[1] - m_[1]) < 25:
            hyd_spur.append(line(x, y, *P(*m_), s=palette.STEEL, w=1.2))
        hyd_tag.append(text(x + 6, y - 5, f"FH-{i:02d}", size=5.5, fill=palette.INK))
    FIR.append(G(hyd_sym))
    FIR.append(G(hyd_spur, c=ZL2))
    FIR.append(G(hyd_tag, c=ZL3))

    # 3. Foam Monitor Towers
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
        cov.append(circle(x, y, U(50), s=palette.MID, w=0.7, d="10 6", o=0.5))
        m_ = nearest_main(q)
        fm_sp.append(line(x, y, *P(*m_), s=palette.STEEL, w=1.4, d="6 3"))
        fm_sym += [rect(x - 5, y - 5, 10, 10, f=palette.WHITE, s=palette.INK, w=1.3),
                   line(x - 5, y - 5, x + 5, y + 5, s=palette.INK, w=0.8),
                   line(x - 5, y + 5, x + 5, y - 5, s=palette.INK, w=0.8),
                   circle(x, y, 2, f=palette.INK)]
        fm_tag.append(text(x + 8, y + 3, f"FM-{i:02d}", size=6, fill=palette.INK))
    FIR.append(G(cov, c=ZL2))
    FIR.append(G(fm_sp, c=ZL2))
    FIR.append(G(fm_sym))
    FIR.append(G(fm_tag, c=ZL2))

    return FIR, hyd, fm_list, nearest_main
