"""
Coordinate transformation, vector algebra, and polygon math.
"""
import math
from ..config import K, OX, OY, CU, SU, ROT, M_PER_UNIT
from .svg_primitives import n, G


def U(metres):
    """metres -> SVG units"""
    return metres / M_PER_UNIT


def M(units):
    """SVG units -> metres"""
    return units * M_PER_UNIT


def P(x, y):
    """Design px -> SVG coordinates"""
    return (OX + K * x, OY + K * y)


def uvp(u, v):
    """Plant-grid (u down-right, v up-right) -> design px"""
    return (u * CU + v * SU, u * SU - v * CU)


def UVu(u, v):
    """Plant-grid -> SVG units"""
    return P(*uvp(u, v))


def uv_of(x, y):
    """Design px -> plant-grid coordinates"""
    return (x * CU + y * SU, x * SU - y * CU)


def poly_area(p):
    """Signed polygon area."""
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
    """Point-in-polygon test (ray casting)."""
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


def line_x(p1, p2, p3, p4):
    d1, d2 = (p2[0] - p1[0], p2[1] - p1[1]), (p4[0] - p3[0], p4[1] - p3[1])
    cr = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((p3[0] - p1[0]) * d2[1] - (p3[1] - p1[1]) * d2[0]) / cr
    return (p1[0] + d1[0] * t, p1[1] + d1[1] * t)


class Frame:
    """Local equipment frame: x' = +v (up-right), y' = +u (down-right), units."""

    def __init__(self, u0, v0):
        self.u0, self.v0 = u0, v0
        self.o = UVu(u0, v0)

    def uv(self, x, y):
        return (self.u0 + y / K, self.v0 + x / K)

    def pt(self, x, y):
        return UVu(*self.uv(x, y))

    def g(self, children, **kw):
        return G(children, transform=f"translate({n(self.o[0])} {n(self.o[1])}) rotate({n(ROT)})", **kw)
