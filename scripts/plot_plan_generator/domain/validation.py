"""
Geometric, topological, process safety, and XML validation suites.
"""
import math
import re
import colorsys
import xml.etree.ElementTree as ET
from pathlib import Path
from ..config import W, H, HW, K, ROAD_W
from ..core.geometry import (
    U, P, uvp, pip, dist_poly, dist_seg
)
from .plant_data import (
    BND, BUNDS, FRAME_BOX, BASIN, YARD_PX, OBST, SLEEPERS, BLDG, CIRC,
    ROAD_SEGS_PX, ROADC, ROADS_PX, GATES, ALL_TANKS, GF, BAY_X, BAY_W,
    GANT_Y0, GANT_Y1
)


def seg_hit(p1, p2, p3, p4):
    def o(a, b_, c):
        return (b_[0] - a[0]) * (c[1] - a[1]) - (b_[1] - a[1]) * (c[0] - a[0])
    return (o(p1, p2, p3) * o(p1, p2, p4) < 0) and (o(p3, p4, p1) * o(p3, p4, p2) < 0)


def polys_overlap(p, q):
    if any(pip(v, q) for v in p) or any(pip(v, p) for v in q):
        return True
    return any(seg_hit(p[i], p[(i + 1) % len(p)], q[j], q[(j + 1) % len(q)])
               for i in range(len(p)) for j in range(len(q)))


def poly_seg_dist(poly, a, b_):
    d = min(dist_seg(v, a, b_) for v in poly)
    d = min(d, min(dist_seg(a, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))),
            min(dist_seg(b_, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))))
    if any(seg_hit(a, b_, poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))) or pip(a, poly):
        return 0.0
    return d


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


def validate_layout(pipe_net, stubs):
    """Asserts site spatial integrity, clearances, routing, and piping network connectivity."""
    BLDG_POLY = {k_: [uvp(a0, b0), uvp(a1, b0), uvp(a1, b1), uvp(a0, b1)] for k_, (a0, a1, b0, b1) in BLDG.items()}
    BASIN_POLY = [uvp(BASIN[0], BASIN[2]), uvp(BASIN[1], BASIN[2]), uvp(BASIN[1], BASIN[3]), uvp(BASIN[0], BASIN[3])]
    ALL_ROAD_SEGS = ROAD_SEGS_PX + [(ROADC[i], ROADC[(i + 1) % len(ROADC)]) for i in range(len(ROADC))]
    SLEEPER_POLY = [o for o in OBST[len(BUNDS):len(BUNDS) + len(SLEEPERS)]]

    # 1. Buildings
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

    # 2. Staging yard
    assert all(pip(v, BND) for v in YARD_PX)
    for nm_, o_ in list(("bund " + n2, BUNDS[n2]) for n2 in BUNDS) + [("basin", BASIN_POLY)] + [("bldg " + k2, v2) for k2, v2 in BLDG_POLY.items()]:
        assert not polys_overlap(YARD_PX, o_), f"yard overlaps {nm_}"
    for (ca, r_) in CIRC:
        assert dist_poly(ca, YARD_PX) >= r_, "yard overlaps a tank"

    # 3. Roads connectivity
    for ri, (rid, pts) in enumerate(ROADS_PX):
        for end in (pts[0], pts[-1]):
            on_perim = dist_poly(end, ROADC) <= 1.5
            on_other = any(dist_seg(end, a_, b_) <= 1.5 for rj, (rid2, p2) in enumerate(ROADS_PX) if rj != ri
                           for a_, b_ in zip(p2[:-1], p2[1:]))
            assert on_perim or on_other, f"road {rid} has a dead end at {end}"

    # 4. One-way HV circuit
    LANE_V = [GF.uv(BAY_X[k_] + BAY_W / 2, 0)[1] for k_ in range(4)]
    LANE_ENTRY_U, LANE_EXIT_U = GF.uv(0, GANT_Y1)[0] - 1.0, GF.uv(0, GANT_Y0)[0]
    G1_IN, _ = proj_on_poly(GATES[0][3], ROADC)
    G2_IN, _ = proj_on_poly(GATES[1][3], ROADC)
    R06_FOOT = ROADS_PX[5][1][0]
    LANE_PROJ = [proj_on_poly(uvp(LANE_ENTRY_U, v_), ROADC)[0] for v_ in LANE_V]
    HV_ENTRY = [G1_IN, ROADC[5], ROADC[4], ROADC[3], LANE_PROJ[-1]]
    HV_LANES = [[LANE_PROJ[k_], uvp(LANE_ENTRY_U, LANE_V[k_]), uvp(LANE_EXIT_U, LANE_V[k_])] for k_ in range(4)]
    HV_EXIT = [uvp(LANE_EXIT_U, LANE_V[-1]), R06_FOOT, ROADC[6], G2_IN]

    def on_roads(p, tol=1.0):
        return any(dist_seg(p, a_, b_) <= tol for a_, b_ in ALL_ROAD_SEGS)

    for ptn in HV_ENTRY[1:] + [q for ln in HV_LANES for q in ln] + HV_EXIT:
        assert on_roads(ptn) or any(pip(ptn, f) for f in FRAME_BOX), f"HV route leaves the road network at {ptn}"
    assert math.hypot(*(HV_ENTRY[-1][i] - HV_LANES[-1][0][i] for i in (0, 1))) < 1.0
    assert math.hypot(*(HV_LANES[-1][-1][i] - HV_EXIT[0][i] for i in (0, 1))) < 1.0
    assert dist_poly(G1_IN, ROADC) < 1.0 and dist_poly(G2_IN, ROADC) < 1.0 and dist_poly(R06_FOOT, ROADC) < 1.5
    assert math.hypot(GATES[0][3][0] - GATES[1][3][0], GATES[0][3][1] - GATES[1][3][1]) >= 60, "HV gates too close"

    # 5. Piping
    def poly_samples(pts, step=1.0):
        out = []
        for (u1, v1), (u2, v2) in zip(pts[:-1], pts[1:]):
            L = math.hypot(u2 - u1, v2 - v1)
            for i in range(int(L / step) + 1):
                t = min(1.0, i * step / L) if L else 0
                out.append((u1 + (u2 - u1) * t, v1 + (v2 - v1) * t))
        out.append(pts[-1])
        return out

    for pi_, pts in enumerate(pipe_net):
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

    _par = list(range(len(pipe_net)))

    def _find(i):
        while _par[i] != i:
            _par[i] = _par[_par[i]]
            i = _par[i]
        return i

    for i in range(len(pipe_net)):
        for j in range(i + 1, len(pipe_net)):
            if pipes_touch(pipe_net[i], pipe_net[j]):
                _par[_find(i)] = _find(j)
    pipe_components = len({_find(i) for i in range(len(pipe_net))})
    assert pipe_components == 1, f"piping network split into {pipe_components} islands"
    assert len(stubs) == len([t for t in ALL_TANKS if t[0] != "TK-0501"]), "a storage tank has no connecting stub"


def validate_svg(target_or_str, is_dark=False):
    """Validates XML structure, AIA/ISO layers, ISO 14224 bindings, and progressive zoom attributes."""
    if isinstance(target_or_str, (str, Path)) and Path(target_or_str).is_file():
        raw = Path(target_or_str).read_text(encoding="utf-8")
        tree = ET.parse(str(target_or_str))
        root = tree.getroot()
    else:
        raw = target_or_str
        root = ET.fromstring(raw)

    ns = "{http://www.w3.org/2000/svg}"
    assert root.tag == ns + "svg" and root.get("viewBox") == f"0 0 {W} {H}"
    assert any(c in root.get("class", "") for c in ("zoom-l1", "zoom-l2", "zoom-l3"))

    layers = [g for g in root if g.tag == ns + "g"]
    ids = [g.get("id") for g in layers]
    expected_ids = ["L-CIVL-BOTM", "L-MECH-EQPM", "L-INSP-INST", "L-PIPE-PROC", "L-FIRE-PROT", "L-ELEC-HAZ", "L-ANNO-TEXT"]
    assert ids == expected_ids, f"Layer mismatch: {ids} vs {expected_ids}"

    by = {}
    for e in root.iter(ns + "g"):
        if "dt-interactive" in (e.get("class") or ""):
            assert e.get("data-cmp-id"), f"missing data-cmp-id in {e.attrib}"
            loc = e.get("data-func-loc") or e.get("data-tag")
            assert loc, f"missing functional location or tag in {e.attrib}"
            assert e.get("data-status"), f"missing data-status in {e.attrib}"
            by.setdefault(e.get("data-cmp-id"), []).append(loc)

    assert len(by.get("CMP-EQP-TANK", [])) == 31, f"Expected 31 tanks, found {len(by.get('CMP-EQP-TANK', []))}"
    assert len(by.get("CMP-EQP-PUMP", [])) == 6, f"Expected 6 pumps, found {len(by.get('CMP-EQP-PUMP', []))}"
    assert len(by.get("CMP-EQP-BAY", [])) == 4, f"Expected 4 bays, found {len(by.get('CMP-EQP-BAY', []))}"

    if not is_dark:
        for hx in set(re.findall(r"#[0-9A-Fa-f]{6}", raw)):
            r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5))
            assert colorsys.rgb_to_hls(r, g, b)[2] <= 0.30, f"saturated colour {hx}"

    z2 = sum(1 for e in root.iter() if "dt-zoom-l2" in (e.get("class") or ""))
    z3 = sum(1 for e in root.iter() if "dt-zoom-l3" in (e.get("class") or ""))
    counts = {i: sum(1 for _ in g.iter()) - 1 for i, g in zip(ids, layers)}
    return by, z2, z3, counts, len(raw)
