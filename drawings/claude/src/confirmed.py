"""Sheets drawn from owner-confirmed values (spec "confirmed" block).

Each sheet needs certain blocks of SPEC["confirmed"]. When they are all
present the sheet is drawn with real geometry and dimensions; otherwise
build.py falls back to the TBC version of that sheet. Items that still need
a site survey or consultant (#4, #16, #23, #26) stay clouded either way.

All dimensions are computed from the spec; each dimension carries the value
it must match so verify.py can check it against the file.
"""

import math

from build import (CEIL, CTR, D, DOOR_W, GLASS_T, GROUT, SHELF, TILE_L, TILE_S, W, CONF, E,
                   P, SCALE, Sheet, elev_notes, plan_shell, tile_cuts)

SF = CONF.get("storefront", {})
UN = CONF.get("units", {})
CT = CONF.get("counter", {})
LT = CONF.get("lighting", {})
SG = CONF.get("signage", {})
FL = CONF.get("floor", {})

NEEDS = {
    "SD-01_setting-out-plan": ("storefront",),
    "SD-02_display-furniture-plan": ("storefront", "units", "counter"),
    "SD-03_floor-finish-plan": ("floor",),
    "SD-04_reflected-ceiling-plan": ("lighting", "units", "storefront"),
    "SD-05_storefront-elevation": ("storefront", "units", "signage"),
    "SD-06_rear-elevation": ("units", "signage", "counter"),
    "SD-07_left-elevation": ("units", "storefront"),
    "SD-08_right-elevation": ("units", "storefront"),
}
SITE_TBC = [4, 16, 23, 26]


def ready(stem):
    return all(k in CONF for k in NEEDS.get(stem, ("never",)))


# ------------------------------------------------------------ derived geometry
def storefront():
    cw, gap = SF["column_width"], SF["glass_gap"]
    x0 = cw
    if SF["fixed_glass_side"] == "left":  # viewed externally = low x
        glass = (x0 + gap, x0 + gap + SF["fixed_glass"])
        door = (glass[1] + gap, glass[1] + gap + DOOR_W)
    else:
        door = (x0 + gap, x0 + gap + DOOR_W)
        glass = (door[1] + gap, door[1] + gap + SF["fixed_glass"])
    return glass, door


def side_bays():
    y0, y1 = SF["column_depth"], UN["side_run_end"]
    n = UN["side_bays"]
    return [y0 + (y1 - y0) * k / n for k in range(n + 1)]


def rear_bounds():
    xs = [SHELF]
    for z in UN["rear_zones"]:
        xs.append(xs[-1] + z)
    return xs


def counter_box():
    x0, x1 = CT["x"]
    y1 = CT["y_rear"]
    return x0, y1 - CTR["D"], x1, y1


def site_note(s, x=18, y=40):
    s.text((x, y), "Site / consultant items still open: #4 finished size, #16 MEP/fire,",
           h=1.5, layer="A-TBC-CLOUD")
    s.text((x, y - 2.8), "#23 north, #26 datum + wall thickness. Verify before fabrication.",
           h=1.5, layer="A-TBC-CLOUD")


def north(s, x=300, y=255):
    # assumed direction only (TBC #23 needs survey): north toward the storefront (-y)
    s.circle((x, y), 6, lw=0.25, layer="A-SHEET")
    s.pl([(x, y - 5), (x - 2.2, y + 1), (x + 2.2, y + 1)], fill="k", lw=0.1, layer="A-SHEET")
    s.text((x, y + 7.5), "N (ASSUMED)", h=1.6, ha="center", layer="A-SHEET", bold=True)
    s.cloud(x - 10, y - 9, x + 10, y + 11)
    s.text((x, y - 12.5), "CONFIRM BY SURVEY #23", h=1.5, ha="center", layer="A-TBC-CLOUD")


# ------------------------------------------------------------------ plan bits
def plan_storefront(s, swing=True):
    cw, cd = SF["column_width"], SF["column_depth"]
    glass, door = storefront()
    for x0 in (0, W - cw):
        s.rect(*P(x0, 0), *P(x0 + cw, cd), lw=0.35, layer="A-FURN", fill="#e6e1d8")
        s.text(P(x0 + cw / 2, cd / 2), "DISPLAY\nCOLUMN", h=1.3, ha="center", va="center")
    s.rect(*P(glass[0], -GLASS_T / 2), *P(glass[1], GLASS_T / 2), lw=0.35,
           layer="A-STOREFRONT", fill="#9ec3d6")
    s.rect(*P(door[0], -GLASS_T / 2), *P(door[1], GLASS_T / 2), lw=0.35, layer="A-STOREFRONT")
    if swing:
        piv = door[1] - SF["pivot_offset"] if SF["pivot_from"] == "right" else \
            door[0] + SF["pivot_offset"]
        long_ = DOOR_W - SF["pivot_offset"]
        s.circle(P(piv, 0), 0.8, fill="k", layer="A-STOREFRONT")
        sign = -1 if SF["pivot_from"] == "right" else 1
        s.line(P(piv, 0), P(piv, long_), lw=0.25, layer="A-STOREFRONT")
        arc = [P(piv + sign * long_ * math.cos(math.radians(a)), long_ * math.sin(math.radians(a)))
               for a in range(0, 91, 5)]
        s.pl(arc, closed=False, lw=0.13, layer="A-STOREFRONT", ls="--")
    s.text(P(W / 2, -330), f"{DOOR_W} x {SF['door_height']} GLASS PIVOT DOOR, {GLASS_T} mm "
           f"TOUGHENED, SWINGS {SF['swing'].upper()}", h=1.7, ha="center", va="top")


def plan_units(s, dashed=False):
    ls = "--" if dashed else "-"
    fill = None if dashed else "#f1ece4"
    ys = side_bays()
    for x0 in (0, W - SHELF):
        s.rect(*P(x0, ys[0]), *P(x0 + SHELF, ys[-1]), lw=0.25, layer="A-FURN", ls=ls, fill=fill)
        for y in ys[1:-1]:
            s.line(P(x0, y), P(x0 + SHELF, y), lw=0.18, layer="A-FURN", ls=ls)
    xs = rear_bounds()
    s.rect(*P(xs[0], D - SHELF), *P(xs[-1], D), lw=0.25, layer="A-FURN", ls=ls, fill=fill)
    for x in xs[1:-1]:
        s.line(P(x, D - SHELF), P(x, D), lw=0.18, layer="A-FURN", ls=ls)


# ------------------------------------------------------------------- sheets
def sd01():
    s = Sheet("SD-01", "SETTING-OUT PLAN", SITE_TBC)
    s.frame()
    plan_shell(s)
    plan_storefront(s)
    glass, door = storefront()
    cw = SF["column_width"]
    s.circle(P(0, 0), 1.2, fill="k", layer="A-SETOUT")
    s.text((P(0, 0)[0] - 3, P(0, 0)[1] - 3), "DATUM 0,0", h=1.6, ha="right", va="top")
    s.dim(P(0, D), P(W, D), 16, key="internal width", expect=W)
    s.dim(P(0, 0), P(0, D), 16, key="internal depth", expect=D)
    s.dim(P(0, D), P(SHELF, D), 9, key="side unit depth L", expect=SHELF)
    s.dim(P(SHELF, D), P(W - SHELF, D), 9, key="clear aisle", expect=W - 2 * SHELF)
    s.dim(P(W - SHELF, D), P(W, D), 9, key="side unit depth R", expect=SHELF)
    # storefront chain
    s.dim(P(0, 0), P(cw, 0), -24, key="storefront column L", expect=cw)
    s.dim(P(cw, 0), P(W - cw, 0), -24, key="entrance opening", expect=SF["opening"])
    s.dim(P(W - cw, 0), P(W, 0), -24, key="storefront column R", expect=cw)
    s.dim(P(*glass, ) if False else P(glass[0], 0), P(glass[1], 0), -17, key="fixed glass",
          expect=SF["fixed_glass"])
    s.dim(P(door[0], 0), P(door[1], 0), -17, key="door leaf width", expect=DOOR_W)
    s.dim(P(W, 0), P(W, SF["column_depth"]), -10, key="storefront column depth",
          expect=SF["column_depth"])
    for x in (SHELF, W - SHELF, cw, W - cw):
        s.line(P(x, 0), P(x, D), lw=0.13, layer="A-SETOUT", ls="-.")
    x, y = 18, 270
    s.text((x, y), "SETTING-OUT POINTS (mm, from datum)", h=2.2, bold=True)
    pts = [("A", "datum, front-left internal corner", 0, 0), ("B", "front-right corner", W, 0),
           ("C", "rear-right corner", W, D), ("D", "rear-left corner", 0, D),
           ("E", "left column inner face", cw, 0), ("F", "right column inner face", W - cw, 0),
           ("G", "fixed glass", glass[0], 0), ("H", "door leaf", door[0], 0),
           ("J", "left unit face line", SHELF, "-"), ("K", "right unit face line", W - SHELF, "-")]
    for i, (k, desc, px, py) in enumerate(pts):
        s.text((x, y - 5 - i * 3.6), f"{k}  x={px:g}  y={py}   {desc}", h=1.7)
    s.text((x, y - 45), f"Glass joints {SF['glass_gap']} mm (glazier to confirm).", h=1.6)
    north(s)
    site_note(s)
    return s


def sd02():
    s = Sheet("SD-02", "DISPLAY / FURNITURE PLAN", SITE_TBC)
    s.frame()
    plan_shell(s)
    plan_storefront(s)
    plan_units(s)
    ys = side_bays()
    for i in range(len(ys) - 1):
        s.dim(P(0, ys[i]), P(0, ys[i + 1]), 7, key=f"side bay {i + 1}",
              expect=(ys[-1] - ys[0]) / UN["side_bays"])
    s.dim(P(0, ys[0]), P(0, ys[-1]), 14, key="side run", expect=UN["side_run_end"] -
          SF["column_depth"])
    s.dim(P(0, 0), P(0, ys[0]), 14, key="storefront column depth", expect=SF["column_depth"])
    xs = rear_bounds()
    for i, z in enumerate(UN["rear_zones"]):
        s.dim(P(xs[i], D), P(xs[i + 1], D), 7, key=f"rear zone {i + 1}", expect=z)
    s.dim(P(0, D), P(W, D), 14, key="internal width", expect=W)
    cx0, cy0, cx1, cy1 = counter_box()
    s.rect(*P(cx0, cy0), *P(cx1, cy1), lw=0.35, layer="A-FURN", fill="#e9e4da")
    s.text(P((cx0 + cx1) / 2, (cy0 + cy1) / 2), f"COUNTER {CTR['W']}x{CTR['D']}x{CTR['H']}H",
           h=1.6, ha="center", va="center")
    s.dim(P(cx0, cy0), P(cx1, cy0), -6, key="counter width", expect=CTR["W"])
    s.dim(P(cx1, cy0), P(cx1, cy1), -5, key="counter depth", expect=CTR["D"])
    esc = CT["escape_min"]
    s.dim(P(cx1, cy0 + 120), P(W - SHELF, cy0 + 120), 0.0001, key="clearance right of counter",
          expect=W - SHELF - cx1)
    if cx0 > SHELF:
        s.dim(P(SHELF, cy0 + 120), P(cx0, cy0 + 120), 0.0001, key="clearance left of counter",
              expect=cx0 - SHELF)
    if max(cx0 - SHELF, W - SHELF - cx1) < esc:
        s.cloud(*P(SHELF - 20, cy0 - 40), *P(W - SHELF + 20, cy1 + 40))
    s.dim(P((cx0 + cx1) / 2, cy1), P((cx0 + cx1) / 2, D - SHELF), 0.0001,
          key="counter to rear unit", expect=D - SHELF - cy1)
    s.text(P(W / 2, cy0 - 120), f"ESCAPE >= {esc} OK" if max(cx0 - SHELF, W - SHELF - cx1) >= esc
           else f"GAPS < {esc} ESCAPE ASSUMPTION - CHECK #16", h=1.5, ha="center", va="top",
           layer="A-TEXT" if max(cx0 - SHELF, W - SHELF - cx1) >= esc else "A-TBC-CLOUD")
    x, y = 18, 270
    s.text((x, y), "LEGEND", h=2.2, bold=True)
    for i, t in enumerate([
            f"Side runs {UN['side_bays']} bays, 25x25 + 20x20 MS SHS, black PPC, {SHELF} deep",
            f"Rear unit zones {' + '.join(str(z) for z in UN['rear_zones'])} (centre = logo)",
            f"Base cabinets {UN['base_cab_h']} H incl. {UN['plinth_h']}x{UN['plinth_d']} recessed "
            "plinth",
            f"Cabinet doors: {UN['cab_door']}",
            f"Storefront columns {SF['column_width']}x{SF['column_depth']}, shelves face "
            f"{SF['column_facing']}",
            f"Counter x {cx0}-{cx1}, rear edge y {cy1}",
            "No timber, brass, plants or loose products."]):
        s.text((x, y - 5 - i * 3.4), t, h=1.6)
    north(s)
    site_note(s)
    return s


def sd03():
    s = Sheet("SD-03", "FLOOR FINISH PLAN", SITE_TBC)
    s.frame()
    plan_shell(s)
    pj = FL["perimeter_joint"]
    across, along = (TILE_L, TILE_S) if FL["option"] == "A" else (TILE_S, TILE_L)
    nx, cx = tile_cuts(W - 2 * pj, across, GROUT)
    ny, cy = tile_cuts(D - 2 * pj, along, GROUT)
    xs = [cx] + [across] * nx + [cx]
    ys = [cy] + [along] * ny + [cy]
    s.rect(*P(pj, pj), *P(W - pj, D - pj), lw=0.13, layer="A-FLOOR", ls="--")
    x = pj
    for i, t in enumerate(xs):
        s.dim(P(x, D), P(x + t, D), 7, key=f"tile col {i + 1}", expect=cx if i in (0, len(xs) - 1)
              else across)
        x += t
        if i < len(xs) - 1:
            s.line(P(x + GROUT / 2, pj), P(x + GROUT / 2, D - pj), lw=0.13, layer="A-FLOOR")
            x += GROUT
    y = pj
    for i, t in enumerate(ys):
        s.dim(P(0, y), P(0, y + t), 7, key=f"tile row {i + 1}", expect=cy if i in (0, len(ys) - 1)
              else along)
        y += t
        if i < len(ys) - 1:
            s.line(P(pj, y + GROUT / 2), P(W - pj, y + GROUT / 2), lw=0.13, layer="A-FLOOR")
            y += GROUT
    s.dim(P(0, D), P(W, D), 14, key="internal width", expect=W)
    s.dim(P(0, 0), P(0, D), 15, key="internal depth", expect=D)
    s.dims.append({"key": "check: width sum incl. joints", "expect": W, "text": None,
                   "paper": (2 * cx + nx * across + (nx + 1) * GROUT + 2 * pj) / SCALE,
                   "handle": None})
    s.dims.append({"key": "check: depth sum incl. joints", "expect": D, "text": None,
                   "paper": (2 * cy + ny * along + (ny + 1) * GROUT + 2 * pj) / SCALE,
                   "handle": None})
    s.line(P(W / 2, -100), P(W / 2, D + 100), lw=0.18, layer="A-SETOUT", ls="-.")
    x, y = 18, 270
    s.text((x, y), f"FLOOR: {TILE_L}x{TILE_S} RECTIFIED STONE-LOOK PORCELAIN", h=2.0, bold=True)
    for i, t in enumerate([
            f"Option {FL['option']}: {across} across the width, {along} along the depth.",
            f"Across: {nx} full + 2 x {cx:g} cut.   Depth: {ny} full + 2 x {cy:g} cut.",
            f"Grout {GROUT} mm between tiles; {pj} mm perimeter movement joint.",
            f"Tiles run under all units and the counter ({FL['extent']}).",
            "Threshold flush, no level change (#20). Set out from the centre line."]):
        s.text((x, y - 5 - i * 3.4), t, h=1.6)
    north(s)
    site_note(s)
    return s


def sd04():
    s = Sheet("SD-04", "REFLECTED CEILING PLAN", SITE_TBC)
    s.frame()
    plan_shell(s)
    plan_units(s, dashed=True)
    cw, cd = SF["column_width"], SF["column_depth"]
    for x0 in (0, W - cw):
        s.rect(*P(x0, 0), *P(x0 + cw, cd), lw=0.18, layer="A-FURN", ls="--")
    y0, y1 = LT["track_y"]
    n = LT["spots_per_track"]
    for x in LT["track_x"]:
        s.line(P(x, y0), P(x, y1), lw=0.7, layer="E-TRACK")
        for k in range(n):
            s.circle(P(x, y0 + (y1 - y0) * (k + 0.5) / n), 1.3, layer="E-TRACK")
    s.dim(P(LT["track_x"][0], y0), P(LT["track_x"][0], y1), 5, key="track length",
          expect=y1 - y0)
    s.dim(P(0, y1 + 120), P(LT["track_x"][0], y1 + 120), 0.0001, key="track 1 from left wall",
          expect=LT["track_x"][0])
    s.dim(P(LT["track_x"][1], y1 + 120), P(W, y1 + 120), 0.0001, key="track 2 from right wall",
          expect=W - LT["track_x"][1])
    for dx, dy in LT["downlights"]:
        c = P(dx, dy)
        s.circle(c, 1.4, layer="E-LIGHT")
        s.line((c[0] - 2, c[1]), (c[0] + 2, c[1]), lw=0.13, layer="E-LIGHT")
        s.line((c[0], c[1] - 2), (c[0], c[1] + 2), lw=0.13, layer="E-LIGHT")
    ys = side_bays()
    for x in (SHELF - 30, W - SHELF + 30):
        s.line(P(x, ys[0] + 30), P(x, ys[-1] - 30), lw=0.35, layer="E-LED", ls=":")
    s.dim(P(0, D), P(W, D), 10, key="internal width", expect=W)
    s.dim(P(0, 0), P(0, D), 10, key="internal depth", expect=D)
    s.text(P(W / 2, 1500), f"CEILING +{CEIL}\n{LT['ceiling_finish'].upper()}", h=1.8,
           ha="center", va="center")
    x, y = 18, 270
    s.text((x, y), f"LIGHTING LEGEND ({LT['cct']})", h=2.2, bold=True)
    s.line((x, y - 5), (x + 10, y - 5), lw=0.7, layer="E-TRACK")
    s.text((x + 12, y - 6), f"Black track, 2 no., {y1 - y0} long", h=1.6)
    s.circle((x + 5, y - 10), 1.3, layer="E-TRACK")
    s.text((x + 12, y - 11), f"Black cylindrical spot, {n} per track", h=1.6)
    s.circle((x + 5, y - 15), 1.4, layer="E-LIGHT")
    s.text((x + 12, y - 16), f"Recessed downlight, {len(LT['downlights'])} no.", h=1.6)
    s.line((x, y - 20), (x + 10, y - 20), lw=0.35, layer="E-LED", ls=":")
    s.text((x + 12, y - 21), "Concealed LED under shelves + toe-kick LED", h=1.6)
    s.text((x, y - 27), "No pendants or decorative ceiling features.", h=1.6)
    north(s)
    site_note(s)
    return s


# -------------------------------------------------------------- elevations
def mesh(s, x0, z0, x1, z1, step=60):
    s.rect(*E(x0, z0), *E(x1, z1), lw=0.18, layer="A-MESH", fill="#cfcfcf")
    w, h = x1 - x0, z1 - z0
    k = -h
    while k < w:
        a = (x0 + max(k, 0), z0 + max(-k, 0))
        t = min(w - max(k, 0), h - max(-k, 0))
        s.line(E(*a), E(a[0] + t, a[1] + t), lw=0.09, layer="A-MESH")
        b = (x1 - max(k, 0), z0 + max(-k, 0))
        s.line(E(*b), E(b[0] - t, b[1] + t), lw=0.09, layer="A-MESH")
        k += step


def bay_elev(s, x0, x1, shelves=True, door=True, with_mesh=True):
    """One display bay between uprights x0..x1 (elevation mm)."""
    pl, cab = UN["plinth_h"], UN["base_cab_h"]
    s.rect(*E(x0, pl), *E(x1, cab), lw=0.18, layer="A-FURN", fill="#ebe7df")
    s.rect(*E(x0 + UN["plinth_d"] / 5, 0), *E(x1 - UN["plinth_d"] / 5, pl), lw=0.13,
           layer="A-FURN", ls="--")
    s.line(E(x0 + 40, pl / 2), E(x1 - 40, pl / 2), lw=0.25, layer="E-LED", ls=":")
    if door:
        s.line(E((x0 + x1) / 2, pl + 20), E((x0 + x1) / 2, cab - 20), lw=0.13, layer="A-FURN")
    mz0, mz1 = UN["mesh_zone"]
    if shelves:
        for z in UN["shelf_levels"]:
            if z <= cab:
                continue
            s.rect(*E(x0, z - UN["shelf_downstand"]), *E(x1, z), lw=0.18, layer="A-FURN",
                   fill="#222222")
            s.line(E(x0 + 20, z - UN["shelf_downstand"] - 15),
                   E(x1 - 20, z - UN["shelf_downstand"] - 15), lw=0.25, layer="E-LED", ls=":")
    if with_mesh:
        mesh(s, x0, mz0, x1, mz1)


def uprights(s, xs):
    for x in xs:
        s.rect(*E(x - 12.5, 0), *E(x + 12.5, UN["frame_h"]), lw=0.18, layer="A-FURN",
               fill="#111111")


def vchain(s, x, keyp):
    zs = sorted({0, UN["plinth_h"], UN["base_cab_h"], *UN["shelf_levels"], UN["mesh_zone"][0],
                 UN["frame_h"]})
    for a, b in zip(zs, zs[1:]):
        s.dim(E(x, a), E(x, b), 6, key=f"{keyp} level {a}-{b}", expect=b - a)
    s.dim(E(x, 0), E(x, UN["frame_h"]), 13, key="display frame height", expect=UN["frame_h"])


def sd_side(no, title, left_is_front):
    s = Sheet(no, title, SITE_TBC)
    s.frame()
    s.line(E(-300, 0), E(D + 300, 0), lw=0.5, layer="A-WALL")
    s.pl([E(0, 0), E(D, 0), E(D, CEIL), E(0, CEIL)], lw=0.5, layer="A-WALL", gid="SHELL")
    s.dim(E(0, CEIL), E(D, CEIL), 8, key="elevation length", expect=D)
    s.text(E(D + 320, CEIL), f"CEILING +{CEIL}", h=1.6, va="center")
    s.text(E(D + 320, 0), "FFL +/-0", h=1.6, va="center")

    def ex(y):  # plan y -> elevation x
        return y if left_is_front else D - y

    ys = side_bays()
    xs = sorted(ex(y) for y in ys)
    for a, b in zip(xs, xs[1:]):
        bay_elev(s, a + 12.5, b - 12.5)
    uprights(s, xs)
    for i, (a, b) in enumerate(zip(xs, xs[1:])):
        s.dim(E(a, 0), E(b, 0), -7, key=f"side bay {i + 1}",
              expect=(ys[-1] - ys[0]) / UN["side_bays"])
    c0, c1 = sorted((ex(0), ex(SF["column_depth"])))
    s.rect(*E(c0, 0), *E(c1, UN["frame_h"]), lw=0.35, layer="A-FURN", fill="#d9d4cc")
    s.text(E((c0 + c1) / 2, CEIL / 2), "STOREFRONT COLUMN (SIDE)", h=1.3, rot=90, ha="center",
           va="center")
    s.dim(E(c0, 0), E(c1, 0), -7, key="storefront column depth", expect=SF["column_depth"])
    s.dim(E(0, 0), E(0, CEIL), 20, key="floor to ceiling", expect=CEIL)
    vchain(s, D, "side")
    s.text(E(0, -500), "STOREFRONT" if left_is_front else "REAR WALL", h=1.6, va="top")
    s.text(E(D, -500), "REAR WALL" if left_is_front else "STOREFRONT", h=1.6, ha="right",
           va="top")
    elev_notes(s)
    site_note(s)
    return s


def sd05():
    s = Sheet("SD-05", "STOREFRONT ELEVATION (EXTERNAL)", SITE_TBC + [16])
    s.frame()
    cw = SF["column_width"]
    top = CEIL + SF["sign_band_h"]
    s.line(E(-300, 0), E(W + 300, 0), lw=0.5, layer="A-WALL")
    s.pl([E(0, 0), E(W, 0), E(W, CEIL), E(0, CEIL)], lw=0.01, layer="A-WALL", gid="SHELL")
    s.rect(*E(0, CEIL), *E(W, top), lw=0.35, layer="A-WALL", fill="#f2ede4")
    lw_ = SG["exterior_logo_w"]
    h = s.logo(E(W / 2 - lw_ / 2, 0)[0], 0, lw_ / SCALE)
    zc = CEIL + SF["sign_band_h"] / 2
    s.ops.pop()
    s.logo(E(W / 2 - lw_ / 2, 0)[0], E(0, zc)[1] - h / 2, lw_ / SCALE)
    for x0 in (0, W - cw):
        bay_elev(s, x0 + 12.5, x0 + cw - 12.5, door=True)
        uprights(s, [x0, x0 + cw])
    glass, door = storefront()
    s.rect(*E(glass[0], 0), *E(glass[1], CEIL), lw=0.35, layer="A-STOREFRONT", fill="#dbe9f0")
    gap = (CEIL - SF["door_height"]) / 2
    s.rect(*E(door[0], gap), *E(door[1], gap + SF["door_height"]), lw=0.35, layer="A-STOREFRONT",
           fill="#e8f1f5")
    piv = door[1] - SF["pivot_offset"] if SF["pivot_from"] == "right" else \
        door[0] + SF["pivot_offset"]
    for z in (gap, gap + SF["door_height"]):
        s.circle(E(piv, z), 0.7, fill="k", layer="A-STOREFRONT")
    s.text(E((door[0] + door[1]) / 2, CEIL / 2), f"PIVOT DOOR\n{GLASS_T} mm TOUGHENED",
           h=1.6, ha="center", va="center")
    s.dim(E(0, 0), E(cw, 0), -8, key="storefront column L", expect=cw)
    s.dim(E(cw, 0), E(W - cw, 0), -8, key="entrance opening", expect=SF["opening"])
    s.dim(E(W - cw, 0), E(W, 0), -8, key="storefront column R", expect=cw)
    s.dim(E(glass[0], 0), E(glass[1], 0), -15, key="fixed glass", expect=SF["fixed_glass"])
    s.dim(E(door[0], 0), E(door[1], 0), -15, key="door leaf width", expect=DOOR_W)
    s.dim(E(0, 0), E(W, 0), -22, key="shopfront internal width", expect=W)
    s.dim(E(door[1], gap), E(door[1], gap + SF["door_height"]), -4, key="door leaf height",
          expect=SF["door_height"])
    s.dim(E(W, 0), E(W, CEIL), -10, key="floor to ceiling (ref)", expect=CEIL)
    s.dim(E(W, CEIL), E(W, top), -10, key="sign band height", expect=SF["sign_band_h"])
    s.dim(E(W, 0), E(W, top), -17, key="storefront overall height", expect=SF["overall_h"])
    s.dims.append({"key": "logo aspect ratio (w/h)", "expect": CONF["signage"]["ratio"],
                   "text": None, "paper": lw_ / SCALE / h, "handle": None, "ratio": True})
    s.text(E(W / 2, top + 120), f"{SG['exterior']}", h=1.6, ha="center")
    elev_notes(s)
    site_note(s)
    return s


def sd06():
    s = Sheet("SD-06", "REAR ELEVATION (INTERNAL)", SITE_TBC)
    s.frame()
    s.line(E(-300, 0), E(W + 300, 0), lw=0.5, layer="A-WALL")
    s.pl([E(0, 0), E(W, 0), E(W, CEIL), E(0, CEIL)], lw=0.5, layer="A-WALL", gid="SHELL")
    s.dim(E(0, CEIL), E(W, CEIL), 8, key="elevation length", expect=W)
    s.dim(E(0, 0), E(0, CEIL), 20, key="floor to ceiling", expect=CEIL)
    for x0 in (0, W - SHELF):
        s.rect(*E(x0, 0), *E(x0 + SHELF, UN["frame_h"]), lw=0.35, layer="A-FURN",
               fill="#d9d4cc")
        s.text(E(x0 + SHELF / 2, CEIL / 2), "SIDE UNIT IN SECTION", h=1.3, rot=90,
               ha="center", va="center")
    s.dim(E(0, CEIL), E(SHELF, CEIL), 3, key="side unit depth L", expect=SHELF)
    s.dim(E(W - SHELF, CEIL), E(W, CEIL), 3, key="side unit depth R", expect=SHELF)
    xs = rear_bounds()
    mid = len(UN["rear_zones"]) // 2
    for i, (a, b) in enumerate(zip(xs, xs[1:])):
        if i != mid:
            bay_elev(s, a + 12.5, b - 12.5, with_mesh=UN.get("rear_mesh", True))
            uprights(s, [a, b])
        s.dim(E(a, 0), E(b, 0), -14, key=f"rear zone {i + 1}", expect=UN["rear_zones"][i])
    lw_ = SG["interior_logo_w"]
    h = s.logo(0, 0, lw_ / SCALE)
    s.ops.pop()
    s.logo(E(W / 2 - lw_ / 2, 0)[0], E(0, SG["interior_logo_centre_z"])[1] - h / 2, lw_ / SCALE)
    s.dims.append({"key": "logo aspect ratio (w/h)", "expect": CONF["signage"]["ratio"],
                   "text": None, "paper": lw_ / SCALE / h, "handle": None, "ratio": True})
    s.dim(E(W / 2 + lw_ / 2 + 60, 0), E(W / 2 + lw_ / 2 + 60, SG["interior_logo_centre_z"]), 0.0001,
          key="interior logo centre height", expect=SG["interior_logo_centre_z"])
    cx0, cx1 = CT["x"]
    s.rect(*E(cx0, 0), *E(cx1, CTR["H"]), lw=0.35, layer="A-FURN", fill="#e9e4da")
    mw, mh, mz = CT["mesh_insert"]["w"], CT["mesh_insert"]["h"], CT["mesh_insert"]["z"]
    mx = (cx0 + cx1) / 2 - mw / 2
    mesh(s, mx, mz, mx + mw, mz + mh, step=40)
    s.dim(E(cx0, 0), E(cx1, 0), -7, key="counter width", expect=CTR["W"])
    s.dim(E(cx1, 0), E(cx1, CTR["H"]), -5, key="counter height", expect=CTR["H"])
    s.dim(E(mx, mz + mh), E(mx + mw, mz + mh), 3, key="counter mesh insert width", expect=mw)
    s.dim(E(mx, mz), E(mx, mz + mh), 3, key="counter mesh insert height", expect=mh)
    vchain(s, W, "rear")
    elev_notes(s)
    site_note(s)
    return s


SHEETS = {
    "SD-01_setting-out-plan": sd01,
    "SD-02_display-furniture-plan": sd02,
    "SD-03_floor-finish-plan": sd03,
    "SD-04_reflected-ceiling-plan": sd04,
    "SD-05_storefront-elevation": sd05,
    "SD-06_rear-elevation": sd06,
    "SD-07_left-elevation": lambda: sd_side("SD-07", "LEFT ELEVATION (INTERNAL)", True),
    "SD-08_right-elevation": lambda: sd_side("SD-08", "RIGHT ELEVATION (INTERNAL)", False),
}
