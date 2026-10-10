"""
SVG serialization toolkit and primitive shapes.
"""
import math
from xml.sax.saxutils import escape

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


def text(x, y, s, size=9, anchor="start", weight="normal", rot=None, fill="#2B2D42", **kw):
    kw.setdefault("f", fill)
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
