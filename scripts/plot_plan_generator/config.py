"""
Configuration, Scales, and Themes for Plot Plan Generation.
"""
import math
from dataclasses import dataclass

M_PER_UNIT = 0.2
W, H = 2000, 1500

K = 2.0                                  # SVG units per design px
OX, OY = -37.0, 120.0                    # design px -> SVG translation
GRID_DEG = 49.0                          # plant grid rotation (matches the survey reference)
ROT = -(90.0 - GRID_DEG)                 # SVG rotate() angle of the u/v frame (-41 deg)
CU = math.cos(math.radians(GRID_DEG))
SU = math.sin(math.radians(GRID_DEG))
HW = (6.0 / M_PER_UNIT) / K / 2          # road / sleeperway half width in px (7.5)
ROAD_W = 6.0 / M_PER_UNIT                # 6 m internal & perimeter roads = 30 units

ZL2 = "dt-zoom-l2"
ZL3 = "dt-zoom-l3"
DASHDOT = "10 3 2 3"

@dataclass(frozen=True)
class Palette:
    name: str
    INK: str
    MID: str
    LIGHT: str
    PALE: str
    STEEL: str
    ASPH: str
    CONC: str
    WHITE: str
    FAINT: str
    BUNDFILL: str
    CANVAS_BG: str


LIGHT_PALETTE = Palette(
    name="light",
    INK="#2B2D42",
    MID="#8D99AE",
    LIGHT="#EDF2F4",
    PALE="#E5E5E5",
    STEEL="#5C677D",
    ASPH="#C5CAD3",
    CONC="#D6DAE0",
    WHITE="#FAFBFC",
    FAINT="#B9C0CC",
    BUNDFILL="#E8EAED",
    CANVAS_BG="#EDF2F4"
)

DARK_PALETTE = Palette(
    name="dark",
    INK="#E2E8F0",
    MID="#64748B",
    LIGHT="#111827",
    PALE="#1F2937",
    STEEL="#64748B",
    ASPH="#1E2430",
    CONC="#2D3748",
    WHITE="#1E2530",
    FAINT="#374151",
    BUNDFILL="#171F2C",
    CANVAS_BG="#0F172A"
)

THEMES = {
    "light": LIGHT_PALETTE,
    "dark": DARK_PALETTE
}
