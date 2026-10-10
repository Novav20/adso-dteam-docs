"""
Process safety calculations: Dike volumetric sizing (NFPA 30) and D/6 tank shell spacing.
"""
import math
from ..config import K, M_PER_UNIT, ROAD_W
from ..core.geometry import U, poly_area, uvp, pip, offset_poly, dist_poly
from .plant_data import BUNDS, BUND_TANKS, WALL_PX, TKS, BND, CLIP_D, FWT


def m2(px_area):
    """Square design pixels -> square meters"""
    return px_area * (K * M_PER_UNIT) ** 2


def tk_geom(t):
    """(radius_m, height_m)"""
    return (t[3] * K * M_PER_UNIT, t[5])


def compute_bund_capacities():
    """Calculates bund retention volumes (NFPA 30 110% net capacity rule) and asserts compliance."""
    bund_res = {}
    for k_, poly in BUNDS.items():
        ts = BUND_TANKS[k_]
        vols = [math.pi * tk_geom(t)[0] ** 2 * tk_geom(t)[1] for t in ts]
        big = max(range(len(ts)), key=lambda i: vols[i])
        a_net = m2(abs(poly_area(poly))) - sum(math.pi * tk_geom(t)[0] ** 2 for i, t in enumerate(ts) if i != big)
        h_req = 1.10 * vols[big] / a_net
        h_des = max(1.0, math.ceil((h_req + 0.15) / 0.1) * 0.1)
        bund_res[k_] = dict(v=vols[big], req=1.1 * vols[big], h_req=h_req, h_des=h_des, net=a_net * h_des, tag=ts[big][0])
        assert h_des <= 2.5, f"bund {k_} wall too high ({h_des})"

        # Shell-to-shell spacing (>= D/6) and wall clearance (>= 1.5 m)
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

    return bund_res
