"""
Mechanical & Equipment Layer (L-MECH-EQPM) generator.
Includes tanks (FR and cone roof), pump skids, loading bays, and stairs.
Complies with ISO 14224 (Level 5 data-func-loc, Level 6 data-equip-id, data-status).
"""
import math
from ..config import K, ZL2, ZL3, DASHDOT
from ..core.geometry import M, UVu
from ..core.svg_primitives import circle, line, rect, path, G, frange, polar, arc_band
from ..domain.plant_data import (
    ALL_TANKS, PUMP_TAGS, PUMP_X0, PUMP_PITCH, PUMP_Y, PUMP_S,
    BLDG, BAY_X, BAY_W, ISL_X, ISL_W, GANT_Y0, GANT_Y1, PF, GF
)


def stair(cx, cy, r, a0, sweep, palette, wd=5.0, step=3.0):
    r1, r2 = r + 0.8, r + 0.8 + wd
    a1 = a0 + sweep
    base = path(arc_band(cx, cy, r1, r2, a0, a1), f=palette.PALE, s=palette.INK, w=0.8)
    plat = path(arc_band(cx, cy, r1, r2 + 6, a1 - 3, a1 + 10), f=palette.WHITE, s=palette.INK, w=0.9, c=ZL2)
    treads = G([line(*polar(cx, cy, r1, a), *polar(cx, cy, r2, a), s=palette.INK, w=0.4)
                for a in frange(a0 + step, a1 - step, step)], c=ZL3)
    return [base, plat, treads]


def tank_fr(t, palette):
    tag, u, v, rp, kind, Hm, av = t
    cx, cy = UVu(u, v)
    r = rp * K
    sw = 120.0
    a0 = av + 180 - sw / 2
    els = [circle(cx, cy, r, f=palette.WHITE, s=palette.INK, w=2.2), circle(cx, cy, r - 2, s=palette.STEEL, w=0.7, c=ZL2),
           circle(cx, cy, r * 0.92, s=palette.STEEL, w=0.9, c=ZL2), circle(cx, cy, r * 0.78, s=palette.STEEL, w=0.9, c=ZL2),
           G([line(*polar(cx, cy, r * .92, a), *polar(cx, cy, r * .78, a), s=palette.STEEL, w=0.6)
              for a in frange(0, 337.5, 22.5)], c=ZL2)]
    a_end = a0 + sw
    ax_, ay_ = polar(cx, cy, r, a_end)
    bx_, by_ = polar(cx, cy, r * 0.3, a_end)
    nx_, ny_ = -math.sin(math.radians(a_end)), math.cos(math.radians(a_end))
    els.append(G([line(ax_ + nx_ * 1.6, ay_ + ny_ * 1.6, bx_ + nx_ * 1.6, by_ + ny_ * 1.6, s=palette.INK, w=0.8),
                  line(ax_ - nx_ * 1.6, ay_ - ny_ * 1.6, bx_ - nx_ * 1.6, by_ - ny_ * 1.6, s=palette.INK, w=0.8)], c=ZL2))
    micro = [circle(cx, cy, 4, f=palette.PALE, s=palette.INK, w=0.8)]
    for rr_, cnt in ((r * .45, 10), (r * .65, 16)):
        micro += [circle(*polar(cx, cy, rr_, k_ * 360 / cnt), 1.1, f=palette.STEEL) for k_ in range(cnt)]
    micro.append(line(*polar(cx, cy, r + 14, av), *polar(cx, cy, r - 12, av), s=palette.INK, w=0.5, d=DASHDOT))
    micro.append(circle(*polar(cx, cy, r - 1, av), 2.2, f=palette.WHITE, s=palette.INK, w=0.8))
    for a in (av + 60, av - 60):
        mx, my = polar(cx, cy, r + 5, a)
        micro.append(rect(mx - 4, my - 2.5, 8, 5, f=palette.WHITE, s=palette.INK, w=0.7))
    els.append(G(micro, c=ZL3))
    stairs = stair(cx, cy, r, a0, sw, palette, wd=5.0, step=2.5)

    tank_g = G(els,
               id=f"tag-{tag}",
               data_cmp_id="CMP-EQP-TANK",
               data_func_loc=f"TFA-CSS-{tag}",
               data_equip_id=f"EQ-{tag}-A",
               data_shell_diam_m=M(r * 2),
               data_tank_height_m=Hm,
               data_design_std="API-650",
               data_status="E",
               c="dt-interactive equipment-hotspot")
    return tank_g, stairs


def tank_cone(t, palette):
    tag, u, v, rp, kind, Hm, av = t
    cx, cy = UVu(u, v)
    r = rp * K
    sw = 140.0
    a0 = av + 180 - sw / 2
    els = [circle(cx, cy, r, f=palette.WHITE, s=palette.INK, w=2.0), circle(cx, cy, r - 2.5, s=palette.STEEL, w=0.7, c=ZL2),
           circle(cx, cy, r * 0.5, s=palette.STEEL, w=0.6, c=ZL2), circle(cx, cy, 4, f=palette.PALE, s=palette.INK, w=0.9),
           G([line(*polar(cx, cy, 4, a), *polar(cx, cy, r - 2.5, a), s=palette.STEEL, w=0.4) for a in frange(0, 345, 15)], c=ZL2)]
    micro = [circle(*polar(cx, cy, r * .72, av + 90), 2.6, f=palette.WHITE, s=palette.INK, w=0.7),
             circle(*polar(cx, cy, r * .72, av + 150), 1.8, f=palette.WHITE, s=palette.INK, w=0.7)]
    for a in (av + 40, av - 40):
        fx_, fy_ = polar(cx, cy, r - 1, a)
        micro.append(rect(fx_ - 3, fy_ - 2, 6, 4, f=palette.PALE, s=palette.INK, w=0.6))
    micro.append(line(*polar(cx, cy, r + 14, av), *polar(cx, cy, r - 12, av), s=palette.INK, w=0.5, d=DASHDOT))
    micro.append(circle(*polar(cx, cy, r - 1, av), 2, f=palette.WHITE, s=palette.INK, w=0.8))
    els.append(G(micro, c=ZL3))
    stairs = stair(cx, cy, r, a0, sw, palette, wd=4.0, step=3.0)

    tank_g = G(els,
               id=f"tag-{tag}",
               data_cmp_id="CMP-EQP-TANK",
               data_func_loc=f"TFA-CSS-{tag}",
               data_equip_id=f"EQ-{tag}-A",
               data_shell_diam_m=M(r * 2),
               data_tank_height_m=Hm,
               data_design_std="API-650",
               data_status="E",
               c="dt-interactive equipment-hotspot")
    return tank_g, stairs


def build_mechanical_layer(palette):
    """Builds all mechanical equipment elements for L-MECH-EQPM."""
    MEC = []
    STAIRS = []

    # 1. Storage Tanks
    for t in ALL_TANKS:
        tg, st = tank_fr(t, palette) if t[4] == "FR" else tank_cone(t, palette)
        MEC.append(tg)
        STAIRS.extend(st)

    # Fold stairs into mechanical layer
    MEC.extend(STAIRS)

    # 2. Pump Skids
    for i, tag in enumerate(PUMP_TAGS):
        x, y = PUMP_X0 + PUMP_PITCH * i, PUMP_Y
        els = [rect(0, 0, 40, 20, f=palette.PALE, s=palette.INK, w=1, c=ZL2), circle(11, 10, 7.5, f=palette.WHITE, s=palette.INK, w=1.4),
               rect(24, 3, 15, 14, rx=2, f=palette.WHITE, s=palette.INK, w=1.2),
               G([rect(19, 7, 5, 6, f=palette.MID, s=palette.INK, w=0.6), rect(29, -1, 6, 4, f=palette.PALE, s=palette.INK, w=0.6),
                  line(-4, 10, 44, 10, s=palette.INK, w=0.5, d=DASHDOT)] +
                 [line(xx, 3, xx, 17, s=palette.INK, w=0.3) for xx in (27, 29.5, 32, 34.5, 37)] +
                 [circle(bx, by, 1, f=palette.INK) for bx, by in ((3, 3), (37, 3), (3, 17), (37, 17))], c=ZL3)]
        MEC.append(PF.g([G(els,
                           id=f"tag-{tag}",
                           data_cmp_id="CMP-EQP-PUMP",
                           data_func_loc=f"TFA-CSS-{tag}",
                           data_equip_id=f"EQ-{tag}-A",
                           data_status="E",
                           c="dt-interactive equipment-hotspot",
                           transform=f"translate({x} {y}) scale({PUMP_S})")]))

    # 3. Fire-water pumps in pump house
    fw0, fw1, fv0, fv1 = BLDG["FW PUMP HOUSE"]
    MEC.append(G([circle(*UVu((fw0 + fw1) / 2, fv0 + 6 + 9 * k_), 3.6, f=palette.WHITE, s=palette.INK, w=1) for k_ in range(3)], c=ZL2))

    # 4. Truck Loading Bays
    for k_, xl in enumerate(BAY_X):
        tag = f"BAY-{k_ + 1:02d}"
        arm_x, bay_c = ISL_X[k_] + ISL_W / 2, xl + BAY_W / 2
        els = [rect(xl, 15, BAY_W, 110, s=palette.INK, w=1),
               G([line(xl, GANT_Y0, xl, GANT_Y1, s=palette.MID, w=0.6, d="8 4"), line(xl + BAY_W, GANT_Y0, xl + BAY_W, GANT_Y1, s=palette.MID, w=0.6, d="8 4"),
                  rect(bay_c - 6.5, 30, 13, 60, rx=5, f=palette.WHITE, s=palette.STEEL, w=0.9),
                  rect(bay_c - 5.5, 92, 11, 16, rx=2, f=palette.WHITE, s=palette.STEEL, w=0.9),
                  line(xl + 2, 24, xl + BAY_W - 2, 24, s=palette.INK, w=0.8, d="3 2")], c=ZL2),
               G([circle(bay_c, yy, 1.8, f=palette.WHITE, s=palette.INK, w=0.6) for yy in (45, 60, 75)] +
                 [circle(arm_x, 70, 26, s=palette.STEEL, w=0.7, d="4 3"), circle(arm_x, 70, 3, f=palette.INK),
                  line(arm_x, 70, bay_c, 60, s=palette.INK, w=1.6)], c=ZL3)]
        MEC.append(GF.g([G(els,
                           id=f"tag-{tag}",
                           data_cmp_id="CMP-EQP-BAY",
                           data_func_loc=f"TFA-TLG-{tag}",
                           data_equip_id=f"EQ-{tag}-A",
                           data_status="E",
                           c="dt-interactive equipment-hotspot")]))

    return MEC
