"""BORN FRAGRANCE shop drawings SD-01 to SD-08.

Reads spec/SHOP_SPEC.json and writes A3 landscape sheets at 1:20 as PDF, SVG
and DXF to drawings/claude/. Every dimension is computed from the spec; any
value the spec does not lock is drawn inside a revision cloud as TBC.

Coordinates: plan origin is the front-left internal corner, x across the
shop, y into the shop, millimetres. PDF/SVG are drawn in paper mm (model/20);
DXF model space is in real mm (paper x 20), so it plots at 1:20 on A3.

Run from the repo root:  python3 drawings/claude/src/build.py
"""

import datetime
import json
import math
import re
import subprocess
from pathlib import Path

import ezdxf
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402
from matplotlib.patches import PathPatch, Polygon  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from ezdxf.enums import TextEntityAlignment  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "drawings" / "claude"
SCALE = 20  # 1:20
A3 = (420.0, 297.0)
PT = 72 / 25.4  # points per mm

# ----------------------------------------------------------------- spec data
SPEC = json.loads((ROOT / "spec" / "SHOP_SPEC.json").read_text())
L = SPEC["locked"]
W = L["internal_size"]["W"]
D = L["internal_size"]["D"]
CEIL = L["ceiling_height"]
SHELF = L["shelf_depth"]
DOOR_W = int(re.search(r"(\d+)\s*pivot", L["entrance"]).group(1))
GLASS_T = int(re.search(r"(\d+)\s*mm", L["entrance"]).group(1))
TILE_L, TILE_S = (int(v) for v in re.search(r"(\d+)x(\d+)", L["floor"]).groups())
GROUT = int(re.search(r"(\d+)\s*mm grout", L["floor"]).group(1))
CTR = L["counter"]
LOGO_RATIO = L["signage"]["logo_aspect_ratio"]
LOGO_FILE = ROOT / L["signage"]["logo_asset"]
CTR_X = SPEC["derived_proposals_unverified"]["counter_position_x"]
AISLE = W - 2 * SHELF

try:
    SPEC_SHA = subprocess.run(
        ["git", "log", "-1", "--format=%h", "--", "spec/SHOP_SPEC.json"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
except Exception:  # noqa: BLE001
    SPEC_SHA = "unknown"
DATE = datetime.date.today().isoformat()

# Gaps found in review that the TBC register does not number yet.
PROPOSED_TBC = {
    23: "North direction",
    24: "Side bay count, widths and upright spacing",
    25: "Counter lateral position (centring is a proposal)",
    26: "Vertical datum (FFL) and wall thickness / construction",
    27: "Counter mesh insert size",
}


def tile_cuts(length, tile, joint):
    """Smallest number of full tiles leaving two equal end cuts <= one tile.

    Joints sit between tiles only (none against the wall).
    Returns (full_tiles, cut_size).
    """
    n = 0
    while True:
        cut = (length - n * tile - (n + 1) * joint) / 2
        if cut <= tile:
            return n, cut
        n += 1


# --------------------------------------------------------------------- logo
def load_logo():
    """Logo outline as flattened sub-paths, normalised to width 1, y up."""
    s = LOGO_FILE.read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    toks = re.findall(r"[MLCZz]|-?\d+\.?\d*", " ".join(re.findall(r' d="([^"]+)"', s)))
    subs, cur, cmd, i = [], (0.0, 0.0), None, 0
    while i < len(toks):
        if toks[i] in "MLCZz":
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                continue
        if cmd == "M":
            cur = (float(toks[i]), float(toks[i + 1]))
            i += 2
            subs.append([cur])
            cmd = "L"  # implicit lineto after moveto
        elif cmd == "L":
            cur = (float(toks[i]), float(toks[i + 1]))
            i += 2
            subs[-1].append(cur)
        elif cmd == "C":
            p = [float(v) for v in toks[i:i + 6]]
            i += 6
            p0, p1, p2, p3 = cur, (p[0], p[1]), (p[2], p[3]), (p[4], p[5])
            for k in range(1, 9):
                t = k / 8
                u = 1 - t
                subs[-1].append((
                    u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
            cur = p3
    x0, y0, w, h = vb
    return [[((x - x0) / w, (y0 + h - y) / w) for x, y in sp] for sp in subs], h / w


LOGO_PATHS, LOGO_H_PER_W = load_logo()


# -------------------------------------------------------------------- sheet
class Sheet:
    """Collects drawing operations in paper mm and renders them to mpl + DXF."""

    def __init__(self, no, title, tbcs):
        self.no, self.title, self.tbcs = no, title, tbcs
        self.ops = []
        self.dims = []  # verification registry

    # primitives (paper mm) ------------------------------------------------
    def line(self, a, b, lw=0.25, layer="A-LINE", ls="-"):
        self.ops.append(("pl", [a, b], False, lw, layer, ls, None, None))

    def pl(self, pts, closed=True, lw=0.25, layer="A-LINE", ls="-", fill=None, gid=None):
        self.ops.append(("pl", list(pts), closed, lw, layer, ls, fill, gid))

    def rect(self, x0, y0, x1, y1, **kw):
        self.pl([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], True, **kw)

    def text(self, p, s, h=2.5, layer="A-TEXT", ha="left", va="bottom", rot=0, bold=False):
        self.ops.append(("text", p, s, h, layer, ha, va, rot, bold))

    def circle(self, c, r, lw=0.25, layer="A-LINE", fill=None):
        self.ops.append(("circle", c, r, lw, layer, fill))

    def dim(self, a, b, off, text=None, key=None, expect=None, layer="A-DIMS"):
        """Aligned dimension a->b, dimension line offset `off` to the left."""
        self.ops.append(("dim", a, b, off, text, layer, len(self.dims)))
        self.dims.append({"key": key, "expect": expect, "text": text,
                          "paper": math.dist(a, b), "handle": None})

    def cloud(self, x0, y0, x1, y1, label=None, r=2.2, h=2.2):
        """Revision cloud around a rectangle (paper mm), scallops outward."""
        pts = []
        corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for (ax, ay), (bx, by) in zip(corners, corners[1:] + corners[:1]):
            ln = math.dist((ax, ay), (bx, by))
            n = max(1, round(ln / (2 * r)))
            ux, uy = (bx - ax) / ln, (by - ay) / ln
            nx, ny = uy, -ux  # outward for CCW rectangle
            seg = ln / n
            for k in range(n):
                cx, cy = ax + ux * seg * (k + 0.5), ay + uy * seg * (k + 0.5)
                for j in range(7):
                    t = math.pi * j / 6
                    pts.append((cx - ux * math.cos(t) * seg / 2 + nx * math.sin(t) * seg / 2.6,
                                cy - uy * math.cos(t) * seg / 2 + ny * math.sin(t) * seg / 2.6))
        self.pl(pts, True, lw=0.35, layer="A-TBC-CLOUD", )
        if label:
            self.text((x0 + 1.2, y1 - 1.2), label, h=h, layer="A-TBC-CLOUD", va="top", bold=True)

    def logo(self, x, y, w, layer="A-LOGO"):
        """Logo with bottom-left at (x, y), width w; height from the SVG ratio."""
        subs = [[(x + px * w, y + py * w) for px, py in sp] for sp in LOGO_PATHS]
        self.ops.append(("logo", subs, layer))
        return w * LOGO_H_PER_W

    # common furniture -------------------------------------------------------
    def frame(self):
        self.rect(10, 10, 410, 287, lw=0.5, layer="A-SHEET")
        self.rect(330, 10, 410, 287, lw=0.35, layer="A-SHEET")
        x = 333
        self.logo(x + 14, 262, 46, layer="A-SHEET")
        y = 262 - 5
        rows = [
            ("PROJECT", "BORN FRAGRANCE - shop fit-out"),
            ("SHEET", f"{self.no}"),
            ("TITLE", self.title),
            ("SCALE", "1:20 @ A3"),
            ("DATE", DATE),
            ("REV", "00 - preliminary"),
            ("SPEC", f"spec/SHOP_SPEC.json @ {SPEC_SHA}"),
            ("DRAWN", "Claude Code (AI), for owner review"),
        ]
        for k, v in rows:
            self.text((x, y), k, h=1.6, layer="A-SHEET")
            self.text((x + 16, y), v, h=2.0 if k != "SHEET" else 3.4, layer="A-SHEET",
                      bold=k in ("SHEET", "TITLE"))
            y -= 6.5
            self.line((330, y + 4.4), (410, y + 4.4), lw=0.13, layer="A-SHEET")
        y -= 2
        self.text((x, y), "TBC ITEMS ON THIS SHEET", h=1.8, layer="A-SHEET", bold=True)
        y -= 4
        reg = {**tbc_register(), **PROPOSED_TBC}
        for n in self.tbcs:
            s = f"#{n}{'*' if n in PROPOSED_TBC else ''} {reg[n]}"
            for part in wrap(s, 46):
                self.text((x, y), part, h=1.5, layer="A-SHEET")
                y -= 2.6
        y -= 1.5
        for note in ("* proposed item, not yet in spec/TBC.md",
                     "TBC items are shown in revision clouds.",
                     "Dimensions computed from SHOP_SPEC.json.",
                     "Do not scale from the render.",
                     "PRELIMINARY - NOT FOR CONSTRUCTION"):
            self.text((x, y), note, h=1.5, layer="A-SHEET",
                      bold=note.startswith("PRELIM"))
            y -= 2.6
        # scale bar 0-2000 mm
        sx, sy = 20, 18
        for i in range(4):
            self.rect(sx + i * 25, sy, sx + (i + 1) * 25, sy + 2, lw=0.18, layer="A-SHEET",
                      fill="k" if i % 2 == 0 else None)
            self.text((sx + i * 25, sy + 3), f"{i * 500}", h=1.6, layer="A-SHEET", ha="center")
        self.text((sx + 100, sy + 3), "2000 mm", h=1.6, layer="A-SHEET", ha="center")
        self.text((sx, sy - 4), "SCALE 1:20 @ A3", h=1.8, layer="A-SHEET")
        self.dims.append({"key": "scale bar 2000 mm", "expect": 2000, "text": None,
                          "paper": 100.0, "handle": None, "bar": True})

    def north(self, x, y):
        self.circle((x, y), 6, lw=0.25, layer="A-SHEET")
        self.text((x, y), "N ?", h=3, ha="center", va="center", layer="A-SHEET", bold=True)
        self.cloud(x - 9, y - 12, x + 9, y + 9)
        self.text((x, y - 10.5), "NORTH TBC #23*", h=1.6, ha="center", layer="A-TBC-CLOUD")

    # render -----------------------------------------------------------------
    def render(self, stem, pdf):
        fig = plt.figure(figsize=(A3[0] / 25.4, A3[1] / 25.4))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, A3[0])
        ax.set_ylim(0, A3[1])
        ax.set_aspect("equal")
        ax.axis("off")
        doc = ezdxf.new("R2018", setup=True)
        doc.header["$INSUNITS"] = 4  # mm
        doc.header["$LTSCALE"] = 10
        msp = doc.modelspace()
        ds = doc.dimstyles.new("BF20")
        ds.dxf.dimtxt = 2.0 * SCALE
        ds.dxf.dimasz = 1.5 * SCALE
        ds.dxf.dimexo = 1.0 * SCALE
        ds.dxf.dimexe = 1.0 * SCALE
        ds.dxf.dimtsz = 1.0 * SCALE  # oblique ticks
        ds.dxf.dimdec = 0
        ds.dxf.dimgap = 0.6 * SCALE
        ds.dxf.dimtad = 1
        colors = {"A-TBC-CLOUD": 1, "A-PROPOSAL": 3, "A-DIMS": 4, "A-WALL": 8, "A-LOGO": 7}
        layers = {op[4] if op[0] == "pl" else op[4] if op[0] == "text" else op[4]
                  if op[0] == "circle" else op[5] if op[0] == "dim" else op[2] for op in self.ops}
        for name in sorted(layers):
            if name not in doc.layers:
                doc.layers.add(name, color=colors.get(name, 7))
        lts = {"-": "CONTINUOUS", "--": "DASHED", "-.": "DASHDOT", ":": "DOT"}
        lw_ok = [13, 18, 25, 35, 50, 70, 100]

        def dxf_lw(lw):
            return min(lw_ok, key=lambda v: abs(v - lw * 100))

        def S(p):
            return (p[0] * SCALE, p[1] * SCALE)

        for op in self.ops:
            kind = op[0]
            if kind == "pl":
                _, pts, closed, lw, layer, ls, fill, gid = op
                red = layer == "A-TBC-CLOUD"
                col = "#c0392b" if red else ("#2e7d32" if layer == "A-PROPOSAL" else "k")
                if fill:
                    patch = Polygon(pts, closed=True, facecolor=fill, edgecolor="none", zorder=1)
                    ax.add_patch(patch)
                    hatch = msp.add_hatch(color=8 if fill != "k" else 7, dxfattribs={"layer": layer})
                    hatch.paths.add_polyline_path([S(p) for p in pts], is_closed=True)
                xs = [p[0] for p in pts] + ([pts[0][0]] if closed else [])
                ys = [p[1] for p in pts] + ([pts[0][1]] if closed else [])
                (ln,) = ax.plot(xs, ys, color=col, lw=lw * PT, ls=ls, zorder=3,
                                solid_joinstyle="miter", dash_capstyle="butt")
                if gid:
                    ln.set_gid(gid)
                msp.add_lwpolyline([S(p) for p in pts], close=closed, dxfattribs={
                    "layer": layer, "linetype": lts[ls], "lineweight": dxf_lw(lw)})
            elif kind == "text":
                _, p, s, h, layer, ha, va, rot, bold = op
                col = "#c0392b" if layer == "A-TBC-CLOUD" else (
                    "#2e7d32" if layer == "A-PROPOSAL" else "k")
                ax.text(p[0], p[1], s, fontsize=h * PT / 0.72, ha=ha, va=va, rotation=rot,
                        color=col, fontweight="bold" if bold else "normal",
                        family="DejaVu Sans", zorder=5)
                al = {("left", "bottom"): "BOTTOM_LEFT", ("center", "bottom"): "BOTTOM_CENTER",
                      ("right", "bottom"): "BOTTOM_RIGHT", ("left", "center"): "MIDDLE_LEFT",
                      ("center", "center"): "MIDDLE_CENTER", ("right", "center"): "MIDDLE_RIGHT",
                      ("left", "top"): "TOP_LEFT", ("center", "top"): "TOP_CENTER",
                      ("right", "top"): "TOP_RIGHT"}[(ha, va)]
                msp.add_text(s, height=h * SCALE, rotation=rot, dxfattribs={"layer": layer}
                             ).set_placement(S(p), align=TextEntityAlignment[al])
            elif kind == "circle":
                _, c, r, lw, layer, fill = op
                ax.add_patch(plt.Circle(c, r, fill=bool(fill), facecolor=fill or "none",
                                        edgecolor="k", lw=lw * PT, zorder=4))
                msp.add_circle(S(c), r * SCALE, dxfattribs={"layer": layer})
            elif kind == "logo":
                _, subs, layer = op
                verts, codes = [], []
                for sp in subs:
                    verts += sp + [sp[0]]
                    codes += [MPath.MOVETO] + [MPath.LINETO] * (len(sp) - 1) + [MPath.CLOSEPOLY]
                ax.add_patch(PathPatch(MPath(verts, codes), facecolor="k", edgecolor="none",
                                       zorder=4))
                hatch = msp.add_hatch(color=7, dxfattribs={"layer": layer})
                for sp in subs:
                    hatch.paths.add_polyline_path([S(p) for p in sp], is_closed=True)
            elif kind == "dim":
                _, a, b, off, text, layer, idx = op
                dx, dy = b[0] - a[0], b[1] - a[1]
                ln = math.hypot(dx, dy)
                ux, uy = dx / ln, dy / ln
                nx, ny = -uy, ux
                a2 = (a[0] + nx * off, a[1] + ny * off)
                b2 = (b[0] + nx * off, b[1] + ny * off)
                sgn = 1 if off >= 0 else -1
                for p, q in ((a, a2), (b, b2)):
                    ax.plot([p[0] + nx * sgn * 1.0, q[0] + nx * sgn * 1.0],
                            [p[1] + ny * sgn * 1.0, q[1] + ny * sgn * 1.0],
                            color="#1f4e79", lw=0.13 * PT, zorder=3)
                ax.plot([a2[0] - ux * 1.5, b2[0] + ux * 1.5], [a2[1] - uy * 1.5, b2[1] + uy * 1.5],
                        color="#1f4e79", lw=0.18 * PT, zorder=3)
                for q in (a2, b2):
                    t = 0.9
                    ax.plot([q[0] - (ux + nx) * t, q[0] + (ux + nx) * t],
                            [q[1] - (uy + ny) * t, q[1] + (uy + ny) * t],
                            color="#1f4e79", lw=0.35 * PT, zorder=3)
                value = round(ln * SCALE, 1)
                label = text if text else f"{value:g}"
                ang = math.degrees(math.atan2(uy, ux))
                if ang > 90.1 or ang < -89.9:
                    ang += 180
                mid = ((a2[0] + b2[0]) / 2 + nx * 0.8, (a2[1] + b2[1]) / 2 + ny * 0.8)
                col = "#c0392b" if text and "TBC" in text else (
                    "#2e7d32" if text and "PROP" in text else "#1f4e79")
                ax.text(mid[0], mid[1], label, fontsize=1.9 * PT / 0.72, rotation=ang,
                        ha="center", va="bottom" if off >= 0 else "top", color=col,
                        rotation_mode="anchor", zorder=5)
                dim = msp.add_aligned_dim(p1=S(a), p2=S(b), distance=off * SCALE,
                                          dimstyle="BF20", text=text or "<>",
                                          dxfattribs={"layer": layer})
                dim.render()
                self.dims[idx]["handle"] = dim.dimension.dxf.handle

        fig.savefig(OUT / f"{stem}.svg", format="svg")
        fig.savefig(OUT / "preview" / f"{stem}.png", dpi=110)
        fig.savefig(OUT / f"{stem}.pdf", format="pdf")
        pdf.savefig(fig)
        plt.close(fig)
        doc.saveas(OUT / f"{stem}.dxf")


def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if cur and len(cur) + len(w) + 1 > n:
            out.append(cur)
            cur = "   " + w
        else:
            cur = f"{cur} {w}" if cur else w
    out.append(cur)
    return out


def tbc_register():
    reg = {}
    for row in (ROOT / "spec" / "TBC.md").read_text().splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+)\|", row)
        if m:
            reg[int(m.group(1))] = m.group(2).strip()
    return reg


# ------------------------------------------------------------- plan helpers
OX, OY = 135.0, 75.0  # paper position of the plan origin (front-left internal corner)
WALL = 6.0            # graphic wall band (paper mm) - construction is TBC #26


def P(x, y):
    return (OX + x / SCALE, OY + y / SCALE)


def plan_shell(s, walls=True):
    x1, y1 = P(W, D)
    if walls:
        for poly in ([(OX - WALL, OY), (OX, OY), (OX, y1), (OX - WALL, y1 + WALL)],
                     [(x1, OY), (x1 + WALL, OY), (x1 + WALL, y1 + WALL), (x1, y1)],
                     [(OX - WALL, y1 + WALL), (OX, y1), (x1, y1), (x1 + WALL, y1 + WALL)]):
            s.pl(poly, fill="#9a9a9a", lw=0.13, layer="A-WALL")
        s.text((x1 + WALL + 1.5, (OY + y1) / 2), "WALL BAND GRAPHIC ONLY - THICKNESS TBC #26*",
               h=1.5, rot=90, ha="center", va="bottom", layer="A-TBC-CLOUD")
    s.pl([P(0, 0), P(W, 0), P(W, D), P(0, D)], lw=0.5, layer="A-WALL", gid="SHELL")


def storefront_plan(s, door=True):
    s.line(P(0, 0), P(W, 0), lw=0.18, layer="A-STOREFRONT", ls="--")
    if door:
        dx0 = (W - DOOR_W) / 2
        s.rect(*P(dx0, -GLASS_T / 2), *P(dx0 + DOOR_W, GLASS_T / 2), lw=0.35, layer="A-STOREFRONT")
        s.text(P(W / 2, -260), f"{DOOR_W} GLASS PIVOT DOOR, {GLASS_T} mm TOUGHENED (LOCKED)",
               h=1.8, ha="center", va="top")
        s.text(P(W / 2, -360), "POSITION, SWING + PIVOT TBC #2 #3 - SHOWN CENTRED",
               h=1.6, ha="center", va="top", layer="A-TBC-CLOUD")
    s.cloud(*P(-200, -520), *P(W + 200, 330), label="STOREFRONT TBC #2 #18 #20")


def side_units(s, layer="A-FURN", ls="-"):
    for x0 in (0, W - SHELF):
        s.rect(*P(x0, 0), *P(x0 + SHELF, D), lw=0.25, layer=layer, ls=ls,
               fill="#f1ece4" if ls == "-" else None)


# ------------------------------------------------------------------- sheets
def sd01():
    s = Sheet("SD-01", "SETTING-OUT PLAN", [2, 3, 4, 18, 20, 23, 26, 16])
    s.frame()
    plan_shell(s)
    storefront_plan(s)
    s.circle(P(0, 0), 1.2, fill="k", layer="A-SETOUT")
    s.text((OX - 3, OY - 3), "DATUM 0,0\nFRONT-LEFT\nINTERNAL CORNER", h=1.6, ha="right", va="top",
           layer="A-SETOUT")
    # overall
    s.dim(P(0, D), P(W, D), 16, key="internal width", expect=W)
    s.dim(P(0, 0), P(0, D), 16, key="internal depth", expect=D)
    # display faces
    s.dim(P(0, D), P(SHELF, D), 9, key="side unit depth L", expect=SHELF)
    s.dim(P(SHELF, D), P(W - SHELF, D), 9, key="clear aisle (proposal)", expect=AISLE)
    s.dim(P(W - SHELF, D), P(W, D), 9, key="side unit depth R", expect=SHELF)
    for x in (SHELF, W - SHELF):
        s.line(P(x, 0), P(x, D), lw=0.13, layer="A-SETOUT", ls="-.")
    s.line(P(W / 2, -150), P(W / 2, D + 150), lw=0.13, layer="A-SETOUT", ls="-.")
    s.text(P(W / 2 + 30, D - 120), "CL SHOP", h=1.6, layer="A-SETOUT")
    s.dim(P(W, 0), P(W, D), -16, text="SIDE RUN TBC #9 #18 #24*", key="side run (TBC)")
    s.text(P(W / 2, D / 2), "SHOP FLOOR\nFFL +/-0 TBC #26*", h=2.2, ha="center", va="center")
    # setting-out table
    x, y = 18, 270
    s.text((x, y), "SETTING-OUT POINTS (mm, from datum)", h=2.2, bold=True)
    y -= 5
    pts = [("A", "datum / front-left internal corner", 0, 0),
           ("B", "front-right internal corner", W, 0),
           ("C", "rear-right internal corner", W, D),
           ("D", "rear-left internal corner", 0, D),
           ("E", "left unit face line", SHELF, "-"),
           ("F", "right unit face line", W - SHELF, "-"),
           ("G", "shop centre line", W / 2, "-")]
    for k, desc, px, py in pts:
        s.text((x, y), f"{k}  x={px:g}  y={py}   {desc}", h=1.7)
        y -= 3.6
    s.text((x, y - 2), "Ceiling +2600 above FFL (locked).", h=1.7)
    s.text((x, y - 6), "Clear aisle 1900 = 2400 - 2 x 250 (derived).", h=1.7)
    s.text((x, y - 10), "Is 2400 x 3106 finished size? TBC #4.", h=1.7, layer="A-TBC-CLOUD")
    s.north(300, 255)
    return s


def sd02():
    s = Sheet("SD-02", "DISPLAY / FURNITURE PLAN", [7, 9, 10, 13, 18, 24, 25, 4])
    s.frame()
    plan_shell(s)
    storefront_plan(s)
    side_units(s)
    for x0 in (0, W - SHELF):
        s.text(P(x0 + SHELF / 2, D / 2), "DISPLAY UNIT - 250 DEEP - BLACK SHS FRAME",
               h=1.6, rot=90, ha="center", va="center")
    s.cloud(*P(-150, 1200), *P(SHELF + 120, 1900), label="")
    s.text(P(-450, 1950), "BAYS ~600, COUNT TBC #24*\nBASE CAB TBC #7", h=1.5, ha="right",
           layer="A-TBC-CLOUD")
    # rear units (layout TBC #9)
    rear = D - SHELF
    s.rect(*P(SHELF, rear), *P(W - SHELF, D), lw=0.18, layer="A-FURN", ls="--")
    s.cloud(*P(SHELF - 30, rear - 80), *P(W - SHELF + 30, D + 40),
            label="REAR BAYS + LOGO TBC #9")
    # counter (x proposal, y TBC)
    cy0 = D - SHELF - 650 - CTR["D"]  # indicative only
    cx0, cx1 = CTR_X
    s.rect(*P(cx0, cy0), *P(cx1, cy0 + CTR["D"]), lw=0.35, layer="A-FURN", fill="#e9e4da")
    s.text(P(W / 2, cy0 + CTR["D"] / 2), f"COUNTER {CTR['W']}x{CTR['D']}x{CTR['H']}H",
           h=1.7, ha="center", va="center")
    s.dim(P(cx0, cy0), P(cx1, cy0), -6, key="counter width", expect=CTR["W"])
    s.dim(P(cx1, cy0), P(cx1, cy0 + CTR["D"]), -6, key="counter depth", expect=CTR["D"])
    s.dim(P(SHELF, cy0 + CTR["D"] / 2), P(cx0, cy0 + CTR["D"] / 2), 0.0001,
          text="450 CHECK <600", key="counter clearance L (proposal)", expect=cx0 - SHELF)
    s.dim(P(cx1, cy0 + CTR["D"] / 2), P(W - SHELF, cy0 + CTR["D"] / 2), 0.0001,
          text="450 CHECK <600", key="counter clearance R (proposal)", expect=W - SHELF - cx1)
    s.cloud(*P(cx0 - 60, cy0 - 330), *P(cx1 + 60, D - SHELF - 30),
            label="Y POSITION TBC #10, X #25*")
    s.dim(P(0, D), P(W, D), 14, key="internal width", expect=W)
    s.dim(P(0, 0), P(0, D), 14, key="internal depth", expect=D)
    s.dim(P(0, D), P(SHELF, D), 7, key="unit depth L", expect=SHELF)
    s.dim(P(SHELF, D), P(W - SHELF, D), 7, key="clear aisle (proposal)", expect=AISLE)
    s.dim(P(W - SHELF, D), P(W, D), 7, key="unit depth R", expect=SHELF)
    s.text(P(W + 350, 600), "FLOOR LED TBC #13", h=1.6, layer="A-TBC-CLOUD")
    x, y = 18, 270
    s.text((x, y), "LEGEND", h=2.2, bold=True)
    s.rect(x, y - 7, x + 8, y - 3, fill="#f1ece4", lw=0.25, layer="A-FURN")
    s.text((x + 10, y - 6.5), "Display unit, 25x25x1.6 + 20x20x1.6 MS SHS,", h=1.6)
    s.text((x + 10, y - 9.3), "matte black powder coat, 250 deep (locked)", h=1.6)
    s.rect(x, y - 15, x + 8, y - 11, fill="#e9e4da", lw=0.35, layer="A-FURN")
    s.text((x + 10, y - 14.5), "Counter 1000x450x900H, 20x20 black frame,", h=1.6)
    s.text((x + 10, y - 17.3), "light panel + mesh insert, light top (locked)", h=1.6)
    s.text((x, y - 24), "Counter centred x 700-1700 is a PROPOSAL.", h=1.6)
    s.text((x, y - 27), "Side clearance 450 < 600: CHECK staff access.", h=1.6,
           layer="A-TBC-CLOUD")
    s.text((x, y - 30), "Exclusions: no timber, brass, plants, products.", h=1.6)
    s.north(300, 255)
    return s


def sd03():
    s = Sheet("SD-03", "FLOOR FINISH PLAN", [22, 14, 20, 4, 26])
    s.frame()
    plan_shell(s)
    storefront_plan(s, door=False)
    # Option A: 1200 across the width, 600 along the depth
    nx, cx = tile_cuts(W, TILE_L, GROUT)
    ny, cy = tile_cuts(D, TILE_S, GROUT)
    xs = [cx] + [TILE_L] * nx + [cx]
    ys = [cy] + [TILE_S] * ny + [cy]
    x = 0
    for t in xs[:-1]:
        x += t
        s.line(P(x + GROUT / 2, 0), P(x + GROUT / 2, D), lw=0.13, layer="A-FLOOR")
        x += GROUT
    y = 0
    for t in ys[:-1]:
        y += t
        s.line(P(0, y + GROUT / 2), P(W, y + GROUT / 2), lw=0.13, layer="A-FLOOR")
        y += GROUT
    # dimension chain along the depth (left)
    y = 0
    for i, t in enumerate(ys):
        s.dim(P(0, y), P(0, y + t), 7, key=f"tile row {i + 1} (option A)",
              expect=cy if i in (0, len(ys) - 1) else TILE_S)
        y += t + GROUT
    x = 0
    for i, t in enumerate(xs):
        s.dim(P(x, D), P(x + t, D), 7, key=f"tile col {i + 1} (option A)",
              expect=cx if i in (0, len(xs) - 1) else TILE_L)
        x += t + GROUT
    s.dim(P(0, D), P(W, D), 14, key="internal width", expect=W)
    s.dim(P(0, 0), P(0, D), 15, key="internal depth", expect=D)
    side_units(s, layer="A-FURN", ls="--")
    s.cloud(*P(-60, 100), *P(SHELF + 60, D - 100), label="")
    s.text(P(-500, D - 300), "TILE UNDER\nUNITS TBC #14", h=1.5, ha="right", layer="A-TBC-CLOUD")
    s.line(P(W / 2, -100), P(W / 2, D + 100), lw=0.18, layer="A-SETOUT", ls="-.")
    s.text(P(W / 2 + 40, 200), "SETTING-OUT LINE = CL", h=1.5, layer="A-SETOUT", rot=90)
    s.cloud(*P(W + 260, 2300), *P(W + 1250, D), label="ORIENTATION\nTBC #22")
    # options table
    bx, bcx = tile_cuts(W, TILE_S, GROUT)
    by, bcy = tile_cuts(D, TILE_L, GROUT)
    x, y = 18, 270
    s.text((x, y), f"FLOOR: {TILE_L}x{TILE_S} RECTIFIED STONE-LOOK PORCELAIN", h=2.0, bold=True)
    s.text((x, y - 4), f"{GROUT} mm grout. Joints between tiles only;", h=1.6)
    s.text((x, y - 6.8), "perimeter/movement joint TBC #26*.", h=1.6)
    rows = [("OPTION A (drawn): 1200 across", f"across: {nx} full + 2 x {cx:g}",
             f"depth: {ny} full + 2 x {cy:g}"),
            ("OPTION B: 1200 along depth", f"across: {bx} full + 2 x {bcx:g}",
             f"depth: {by} full + 2 x {bcy:g}")]
    y -= 13
    for a, b, c in rows:
        s.text((x, y), a, h=1.8, bold=True)
        s.text((x + 2, y - 3.2), b, h=1.6)
        s.text((x + 2, y - 6), c, h=1.6)
        y -= 11
    s.text((x, y), "Owner to choose A or B (TBC #22).", h=1.6, layer="A-TBC-CLOUD")
    s.text((x, y - 3), "Threshold / level change TBC #20.", h=1.6, layer="A-TBC-CLOUD")
    s.dims.append({"key": "check: A depth sum", "expect": D, "text": None,
                   "paper": (2 * cy + ny * TILE_S + (ny + 1) * GROUT) / SCALE, "handle": None})
    s.dims.append({"key": "check: A width sum", "expect": W, "text": None,
                   "paper": (2 * cx + nx * TILE_L + (nx + 1) * GROUT) / SCALE, "handle": None})
    s.north(300, 255)
    return s


def sd04():
    s = Sheet("SD-04", "REFLECTED CEILING PLAN", [11, 12, 13, 17, 21, 4])
    s.frame()
    plan_shell(s)
    s.line(P(0, 0), P(W, 0), lw=0.18, layer="A-STOREFRONT", ls="--")
    side_units(s, layer="A-FURN", ls="--")
    # concealed LED under shelves follows the unit fronts
    for x in (SHELF - 30, W - SHELF + 30):
        s.line(P(x, 60), P(x, D - 60), lw=0.35, layer="E-LED", ls=":")
    # two tracks (count locked, position TBC)
    for x in (SHELF + 300, W - SHELF - 300):
        s.line(P(x, 350), P(x, D - 450), lw=0.7, layer="E-TRACK")
        for k in range(4):
            s.circle(P(x, 600 + k * 600), 1.3, lw=0.25, layer="E-TRACK")
    s.cloud(*P(SHELF + 120, 250), *P(W - SHELF - 120, D - 350),
            label="TRACK POSITION/LENGTH + SPOT COUNT TBC #11")
    s.text(P(W / 2, 1500), "CEILING +2600 (LOCKED)\nFINISH TBC #21", h=2.0, ha="center",
           va="center")
    s.cloud(*P(200, -650), *P(W - 200, -120), label="DOWNLIGHTS TBC #12, SIGN LIGHT #17")
    s.dim(P(0, D), P(W, D), 10, key="internal width", expect=W)
    s.dim(P(0, 0), P(0, D), 10, key="internal depth", expect=D)
    x, y = 18, 270
    s.text((x, y), "LIGHTING LEGEND (3000 K)", h=2.2, bold=True)
    s.line((x, y - 5), (x + 10, y - 5), lw=0.7, layer="E-TRACK")
    s.text((x + 12, y - 6), "Black ceiling track (2 no., locked)", h=1.6)
    s.circle((x + 5, y - 10), 1.3, layer="E-TRACK")
    s.text((x + 12, y - 11), "Black cylindrical adjustable spot (count TBC #11)", h=1.6)
    s.line((x, y - 15), (x + 10, y - 15), lw=0.35, layer="E-LED", ls=":")
    s.text((x + 12, y - 16), "Concealed 3000 K LED under shelves (locked)", h=1.6)
    s.text((x, y - 22), "No pendants or decorative ceiling features.", h=1.6)
    s.text((x, y - 25), "Positions shown are diagrammatic only.", h=1.6, layer="A-TBC-CLOUD")
    s.text((x, y - 28), "Floor-level LED strip TBC #13.", h=1.6, layer="A-TBC-CLOUD")
    s.north(300, 255)
    return s


# -------------------------------------------------------------- elevations
EX, EY = 115.0, 70.0  # paper origin of elevation (left end at FFL)


def E(x, z):
    return (EX + x / SCALE, EY + z / SCALE)


def elev_shell(s, length, label_l, label_r):
    s.line(E(-300, 0), E(length + 300, 0), lw=0.5, layer="A-WALL")
    s.pl([E(0, 0), E(length, 0), E(length, CEIL), E(0, CEIL)], lw=0.5, layer="A-WALL", gid="SHELL")
    s.text(E(length + 320, 0), "FFL +/-0 (DATUM TBC #26*)", h=1.6, va="center")
    s.text(E(length + 320, CEIL), f"CEILING +{CEIL}", h=1.6, va="center")
    s.dim(E(0, 0), E(0, CEIL), 10, key="floor to ceiling", expect=CEIL)
    s.dim(E(0, CEIL), E(length, CEIL), 8, key="elevation length",
          expect=length)
    s.text(E(0, -250), label_l, h=1.6, ha="left", va="top")
    s.text(E(length, -250), label_r, h=1.6, ha="right", va="top")


def wall_units_elev(s, x0, x1, title):
    s.rect(*E(x0, 0), *E(x1, CEIL), lw=0.18, layer="A-FURN", ls="--")
    for x in (x0, x1):
        s.rect(*E(x, 0), *E(x + (25 if x == x0 else -25), CEIL), lw=0.25, layer="A-FURN",
               fill="#222222")
    s.cloud(*E(x0 + 80, 150), *E(x1 - 80, CEIL - 120),
            label=f"{title}: FRAME HEIGHT #5, SHELF COUNT/PITCH #6,\n"
                  "BASE CAB #7, MESH ZONE #8, SHELF MATL #19, BAYS #24*")
    s.text(E((x0 + x1) / 2, CEIL / 2 + 200), "RAW TEXTURED PLASTER BEHIND (LOCKED)",
           h=1.8, ha="center")
    s.text(E((x0 + x1) / 2, CEIL / 2 - 100), "CONCEALED 3000 K LED UNDER EACH SHELF (LOCKED)",
           h=1.8, ha="center")
    s.text(E((x0 + x1) / 2, CEIL / 2 - 400), "~20x40 BLACK EXPANDED MESH, UPPER LEVEL (LOCKED)",
           h=1.8, ha="center")


def elev_notes(s):
    x, y = 18, 270
    s.text((x, y), "MATERIALS (LOCKED)", h=2.2, bold=True)
    for i, t in enumerate(["M1 Raw textured light plaster",
                           "M2 25x25x1.6 / 20x20x1.6 MS SHS, matte black PPC",
                           "M3 ~20x40 diamond expanded mesh, black",
                           "M4 1200x600 stone-look porcelain floor",
                           "L1 Concealed 3000 K LED under shelves",
                           "Heights not listed are TBC - never scaled."]):
        s.text((x, y - 4.5 - i * 3.2), t, h=1.6)


def sd05():
    s = Sheet("SD-05", "STOREFRONT ELEVATION (EXTERNAL)", [1, 2, 3, 12, 15, 17, 18, 20])
    s.frame()
    s.line(E(-300, 0), E(W + 300, 0), lw=0.5, layer="A-WALL")
    s.line(E(0, 0), E(0, CEIL), lw=0.35, layer="A-WALL")
    s.line(E(W, 0), E(W, CEIL), lw=0.35, layer="A-WALL")
    s.line(E(0, CEIL), E(W, CEIL), lw=0.18, layer="A-WALL", ls="--")
    s.pl([E(0, 0), E(W, 0), E(W, CEIL), E(0, CEIL)], lw=0.01, layer="A-WALL", gid="SHELL")
    s.text(E(W + 320, CEIL), f"INTERNAL CEILING +{CEIL} (REF)", h=1.6, va="center")
    s.text(E(W + 320, 0), "PAVEMENT / FFL TBC #20 #26*", h=1.6, va="center")
    dx0 = (W - DOOR_W) / 2
    s.rect(*E(dx0, 0), *E(dx0 + DOOR_W, 2100), lw=0.35, layer="A-STOREFRONT")
    s.line(E(dx0 + 60, 1050), E(dx0 + 60, 1250), lw=0.5, layer="A-STOREFRONT")
    s.text(E(W / 2, 1050), f"{DOOR_W} GLASS PIVOT DOOR\n{GLASS_T} mm CLEAR TOUGHENED",
           h=1.8, ha="center", va="center")
    s.dim(E(dx0, 0), E(dx0 + DOOR_W, 0), -8, key="door leaf width", expect=DOOR_W)
    s.dim(E(dx0 + DOOR_W, 0), E(dx0 + DOOR_W, 2100), -6, text="DOOR HT TBC #2",
          key="door height (TBC)")
    s.dim(E(0, 0), E(W, 0), -16, key="shopfront internal width", expect=W)
    s.dim(E(0, 0), E(0, CEIL), 10, key="floor to ceiling (ref)", expect=CEIL)
    s.cloud(*E(-250, 80), *E(dx0 - 40, CEIL - 80), label="DISPLAY COL\n#2 #18")
    s.cloud(*E(dx0 + DOOR_W + 40, 80), *E(W + 250, CEIL - 80), label="DISPLAY COL\n#2 #18")
    s.cloud(*E(-250, CEIL + 60), *E(W + 250, CEIL + 1450),
            label="SIGN BAND + STOREFRONT HEIGHT TBC #1")
    lw_ = 1000
    h = s.logo(E(W / 2 - lw_ / 2, 0)[0], E(0, CEIL + 420)[1], lw_ / SCALE)
    s.text(E(W / 2, CEIL + 300), "EXTERIOR LOGO - HALO-LIT (LOCKED) vs FRONT-LIT (RENDER) #17;"
           " SHOWN 1000 W FOR LAYOUT ONLY, SIZE TBC #15", h=1.4, ha="center", va="top",
           layer="A-TBC-CLOUD")
    s.dims.append({"key": "logo aspect ratio (w/h)", "expect": LOGO_RATIO, "text": None,
                   "paper": lw_ / SCALE / h, "handle": None, "ratio": True})
    s.text(E(W / 2, -900), "MESH PANELS + DISPLAY COLUMNS PER RENDER INTENT; ALL SIZES TBC",
           h=1.6, ha="center", layer="A-TBC-CLOUD")
    elev_notes(s)
    return s


def sd06():
    s = Sheet("SD-06", "REAR ELEVATION (INTERNAL)", [5, 6, 7, 9, 15, 19, 25, 26, 27])
    s.frame()
    elev_shell(s, W, "LEFT WALL", "RIGHT WALL")
    for x0 in (0, W - SHELF):
        s.rect(*E(x0, 0), *E(x0 + SHELF, CEIL), lw=0.35, layer="A-FURN", fill="#d9d4cc")
        s.text(E(x0 + SHELF / 2, CEIL / 2), "SIDE UNIT IN SECTION", h=1.4, rot=90,
               ha="center", va="center")
    s.dim(E(0, CEIL), E(SHELF, CEIL), 3, key="side unit depth L", expect=SHELF)
    s.dim(E(W - SHELF, CEIL), E(W, CEIL), 3, key="side unit depth R", expect=SHELF)
    s.cloud(*E(SHELF + 40, 1000), *E(W - SHELF - 40, CEIL - 60),
            label="REAR BAYS EITHER SIDE OF LOGO #9,\nFRAME #5, SHELVES #6 #19")
    lw_ = 600
    h = s.logo(E(W / 2 - lw_ / 2, 0)[0], E(0, 1650)[1], lw_ / SCALE)
    s.text(E(W / 2, 1600), "INTERIOR LOGO, NON-ILLUMINATED BLACK (LOCKED)\n"
           "SHOWN 600 W FOR LAYOUT; SIZE + HEIGHT TBC #9 #15", h=1.4, ha="center", va="top",
           layer="A-TBC-CLOUD")
    cx0, cx1 = CTR_X
    s.rect(*E(cx0, 0), *E(cx1, CTR["H"]), lw=0.35, layer="A-FURN", fill="#e9e4da")
    s.rect(*E(cx0, 0), *E(cx0 + CTR["W"] * 0.4, CTR["H"] - 40), lw=0.18, layer="A-FURN",
           fill="#8a8a8a")
    s.text(E((cx0 + cx1) / 2, CTR["H"] / 2), "COUNTER (IN FRONT)", h=1.5, ha="center",
           va="center")
    s.dim(E(cx0, 0), E(cx1, 0), -8, key="counter width", expect=CTR["W"])
    s.dim(E(cx1, 0), E(cx1, CTR["H"]), -6, key="counter height", expect=CTR["H"])
    s.text(E(W / 2, -600), "Counter x 700-1700 is a PROPOSAL (#25*); mesh insert size TBC #27*.",
           h=1.5, ha="center", va="top")
    s.dims.append({"key": "logo aspect ratio (w/h)", "expect": LOGO_RATIO, "text": None,
                   "paper": lw_ / SCALE / h, "handle": None, "ratio": True})
    elev_notes(s)
    return s


def sd_side(no, title, left_label, right_label):
    s = Sheet(no, title, [5, 6, 7, 8, 9, 18, 19, 24])
    s.frame()
    elev_shell(s, D, left_label, right_label)
    wall_units_elev(s, 0, D, "SIDE UNIT")
    elev_notes(s)
    return s


def sd07():
    return sd_side("SD-07", "LEFT ELEVATION (INTERNAL)", "STOREFRONT", "REAR WALL")


def sd08():
    return sd_side("SD-08", "RIGHT ELEVATION (INTERNAL)", "REAR WALL", "STOREFRONT")


SHEETS = [
    ("SD-01_setting-out-plan", sd01),
    ("SD-02_display-furniture-plan", sd02),
    ("SD-03_floor-finish-plan", sd03),
    ("SD-04_reflected-ceiling-plan", sd04),
    ("SD-05_storefront-elevation", sd05),
    ("SD-06_rear-elevation", sd06),
    ("SD-07_left-elevation", sd07),
    ("SD-08_right-elevation", sd08),
]


def main():
    (OUT / "preview").mkdir(parents=True, exist_ok=True)
    built = []
    with PdfPages(OUT / "BF_SD-01-08_set.pdf") as pdf:
        for stem, fn in SHEETS:
            s = fn()
            s.render(stem, pdf)
            built.append((stem, s))
    import verify  # noqa: PLC0415
    verify.run(built)


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    main()
