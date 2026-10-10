"""
Process Piping Layer (L-PIPE-PROC) generator.
Includes main headers, expansion loops, collectors, tank stubs,
pump suction/discharge, manifold distribution, gantry lines, valves, and flanges.
"""
import math
from ..config import ROT, GRID_DEG, ZL2, ZL3
from ..core.geometry import UVu, uvpath
from ..core.svg_primitives import G, path, line, polyg, n
from ..domain.plant_data import (
    TKS, PF, MF, GF, PUMP_X0, PUMP_PITCH, PUMP_Y, PUMP_S, GANT_W, ISL_X, ISL_W
)


def ang_of(along):
    return ROT if along == "v" else GRID_DEG


def trunk_v(c_u, v0, v1, loops, depth_sign, line_off, kind):
    """Trunk along v at u=c_u+line_off with U-loops projecting depth_sign*(depth) in u."""
    pts = [(c_u + line_off, v0)]
    for vc, wd, dp in sorted(loops):
        pts += [(c_u + line_off, vc - wd / 2), (c_u + line_off + depth_sign * dp, vc - wd / 2),
                (c_u + line_off + depth_sign * dp, vc + wd / 2), (c_u + line_off, vc + wd / 2)]
    pts.append((c_u + line_off, v1))
    return pts


def build_piping_layer(palette):
    """Assembles all piping, valves, and in-line instrumentation for L-PIPE-PROC."""
    PIP = []
    VAL2, VAL3, FLG = [], [], []
    PIPE_NET = []
    STUBS = {}

    def valve(uv, along="v", s=4.5):
        x, y = UVu(*uv)
        tr = f"translate({n(x)} {n(y)}) rotate({n(ang_of(along))})"
        VAL2.append(G([path(f"M{n(-s)},{n(-s*.7)} L{n(s)},{n(s*.7)} L{n(s)},{n(-s*.7)} L{n(-s)},{n(s*.7)} Z",
                            f=palette.WHITE, s=palette.INK, w=0.9)], transform=tr))
        VAL3.append(G([line(0, -s * .7, 0, -s * .7 - 5, s=palette.INK, w=0.7),
                       line(-3.5, -s * .7 - 5, 3.5, -s * .7 - 5, s=palette.INK, w=1.2)], transform=tr))

    def check_valve(uv, along="v"):
        x, y = UVu(*uv)
        VAL2.append(G([polyg([(-4, -3.5), (-4, 3.5), (4, 0)], f=palette.WHITE, s=palette.INK, w=0.9),
                       line(4, -3.5, 4, 3.5, s=palette.INK, w=1.1)], transform=f"translate({n(x)} {n(y)}) rotate({n(ang_of(along))})"))

    def flange(uv, along="v", size=4.5):
        x, y = UVu(*uv)
        FLG.append(G([line(0, -size, 0, size, s=palette.INK, w=1.1), line(2.2, -size, 2.2, size, s=palette.INK, w=1.1)],
                     transform=f"translate({n(x)} {n(y)}) rotate({n(ang_of(along))})"))

    def pipe(pts_uv, kind="A", w=2.6):
        PIPE_NET.append(list(pts_uv))
        return path(uvpath(pts_uv), s=palette.INK if kind == "A" else palette.STEEL, w=w, lj="round")

    def collector(pts, w=2.4):
        PIP.append(pipe(pts, "A", w))

    def stub_v(t, vc):
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

    # 1. Trunks
    SN_A = trunk_v(346, -82, 296, [(-30, 36, 14), (190, 36, 14)], -1, 0, "A")
    PIP.append(pipe(SN_A, "A", 3.0))                       # SN  : farm outlet header -> SA / SR
    PIP.append(pipe([(346, 111), (672, 111)], "A", 3.0))     # SA  : trunk to the pump station
    PIP.append(pipe([(672, 20), (672, 264)], "A", 3.0))      # SB  : trunk past pump suction and manifold
    PIP.append(pipe([(346, 290), (600, 290)], "A", 3.0))     # SR  : trunk along the TF3 / TF4 corridor

    # 2. Collectors & Tank Stubs
    sw = TKS["SW"]
    collector([(488, -77), (346, -77)])
    STUBS["TK-0105"] = PIPE_NET[-1]
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

    # 3. Pump Station Piping
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

    # 4. Manifold Block
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

    # 5. Manifold -> Gantry Loading Header
    G_A = GF.uv(0, 5)
    PIP.append(pipe([MF.uv(146, MH[2]), (MF.uv(146, MH[2])[0], 358), (G_A[0], 358), G_A], "A", 2.8))
    valve((MF.uv(146, MH[2])[0], 350), "v", 4)
    PIP.append(pipe([GF.uv(0, 5), GF.uv(GANT_W - 6, 5)], "A", 2.8))
    for k_ in range(4):
        xa = ISL_X[k_] + ISL_W / 2
        PIP.append(pipe([GF.uv(xa, 5), GF.uv(xa, 70)], "A", 2.4))
        valve(GF.uv(xa, 40), "u", 4)
        flange(GF.uv(xa, 62), "u")

    # Zoom-bracketed valves and flanges
    PIP.append(G(VAL2, c=ZL2))
    PIP.append(G(VAL3, c=ZL3))
    PIP.append(G(FLG, c=ZL3))

    return PIP, PIPE_NET, STUBS
