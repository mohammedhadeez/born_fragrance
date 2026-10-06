"""Presentation assets: cropped SVG views of the Rev A drawings.

Builds the same sheets as build.py (same spec, same geometry, same dimensions)
but without the sheet border, title block, scale bar and side notes, cropped to
the drawing. Text stays as editable SVG <text>. Each view carries a
"NOT TO SCALE" caption; the SD sheets in drawings/claude/ remain the true
1:20 record and are not touched.

Run from the repo root:  python3 drawings/claude/src/present.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib  # noqa: E402

matplotlib.rcParams["svg.fonttype"] = "none"  # keep labels as editable text

import build  # noqa: E402
import confirmed  # noqa: E402

OUT = build.OUT / "presentation"
NOTES_X = 105  # side notes / legends on the SD sheets sit left of this (paper mm)

VIEWS = [
    ("furniture-plan", "SD-02_display-furniture-plan", "SD-02"),
    ("storefront-elevation", "SD-05_storefront-elevation", "SD-05"),
    ("rear-elevation", "SD-06_rear-elevation", "SD-06"),
    ("left-elevation", "SD-07_left-elevation", "SD-07"),
    ("right-elevation", "SD-08_right-elevation", "SD-08"),
    ("reflected-ceiling-plan", "SD-04_reflected-ceiling-plan", "SD-04"),
]


def text_box(op):
    """Corners of a label's estimated extent (paper mm), from its anchor, size,
    alignment and rotation. DejaVu Sans caps run about 0.7 x height per character."""
    _, (x, y), txt, h, _layer, ha, va, rot, _bold = op
    lines = txt.split("\n")
    w = max(len(ln) for ln in lines) * h * 0.7
    tall = len(lines) * h * 1.3
    dx = {"left": (0, w), "center": (-w / 2, w / 2), "right": (-w, 0)}[ha]
    dy = {"bottom": (0, tall), "center": (-tall / 2, tall / 2), "top": (-tall, 0)}[va]
    corners = [(u, v) for u in dx for v in dy]
    if rot % 180:  # 90 / 270: swap axes
        corners = [(-v, u) for u, v in corners]
    return [(x + u, y + v) for u, v in corners]


def bbox(ops):
    pts = []
    for op in ops:
        kind = op[0]
        if kind == "pl":
            pts += op[1]
        elif kind == "text":
            pts += text_box(op)
        elif kind == "circle":
            (cx, cy), r = op[1], op[2]
            pts += [(cx - r, cy - r), (cx + r, cy + r)]
        elif kind == "logo":
            pts += [p for sp in op[1] for p in sp]
        elif kind == "dim":
            a, b, off = op[1], op[2], op[3]
            ln = math.dist(a, b)
            nx, ny = -(b[1] - a[1]) / ln, (b[0] - a[0]) / ln
            pts += [a, b, (a[0] + nx * off, a[1] + ny * off), (b[0] + nx * off, b[1] + ny * off)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def build_view(stem):
    # no border/title block; assumed-north symbol moved next to the plan
    build.Sheet.frame = lambda self: None
    orig_north = confirmed.north
    confirmed.north = lambda s, x=282, y=232: orig_north(s, x, y)
    confirmed.site_note = lambda s, *a, **k: None
    confirmed.elev_notes = lambda s: None
    try:
        s = confirmed.SHEETS[stem]()
    finally:
        confirmed.north = orig_north
    # drop the sheet's side legends/notes (everything left of the drawing area)
    def in_notes(op):
        if op[0] == "text":
            return op[1][0] < NOTES_X
        if op[0] == "pl":
            return all(p[0] < NOTES_X for p in op[1])
        if op[0] == "circle":
            return op[1][0] < NOTES_X
        return False

    s.ops = [op for op in s.ops if not in_notes(op)]
    # keep the counter-clearance warning readable: move it clear of the 1000 dimension
    for i, op in enumerate(s.ops):
        if op[0] == "text" and "CHECK #16" in op[2]:
            s.ops[i] = (op[0], (op[1][0], op[1][1] - 4.5), *op[2:])
    return s


# what each asset must contain (text), and its outline proportion (width / height)
EXPECT = {
    "furniture-plan": (["2400", "500", "900", "664", "2656", "450", "1000", "700",
                        "CHECK #16", "NOT TO SCALE"], build.W / build.D),
    "storefront-elevation": (["2400", "450", "1500", "488", "1000", "2580", "600", "3200",
                              "NOT TO SCALE"], build.W / build.CEIL),
    "rear-elevation": (["2400", "500", "900", "1000", "900", "300", "450", "1900",
                        "NOT TO SCALE"], build.W / build.CEIL),
    "left-elevation": (["3106", "664", "450", "2600", "NOT TO SCALE"], build.D / build.CEIL),
    "right-elevation": (["3106", "664", "450", "2600", "NOT TO SCALE"], build.D / build.CEIL),
    "reflected-ceiling-plan": (["2400", "3106", "2206", "650", "CEILING +2600",
                                "NOT TO SCALE"], build.W / build.D),
}


def check(path):
    """Parse the SVG and confirm labels are editable text, required values exist,
    the outline keeps its true proportion and no sheet border/title block remains."""
    import re
    import xml.etree.ElementTree as ET

    name = path.stem
    root = ET.parse(path).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    texts = ["".join(t.itertext()) for t in root.iter(f"{ns}text")]
    want, ratio = EXPECT[name]
    missing = [w for w in want if not any(w in t for t in texts)]
    shell = root.find(f".//{ns}g[@id='SHELL']/{ns}path")
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", shell.get("d"))]
    xs, ys = nums[0::2], nums[1::2]
    got = (max(xs) - min(xs)) / (max(ys) - min(ys))
    leftovers = [t for t in texts if t.strip() in ("PROJECT", "SHEET", "SCALE 1:20 @ A3")]
    ok = not missing and abs(got - ratio) < 0.002 and not leftovers and len(texts) > 5
    return ok, f"{name}: text={len(texts)} missing={missing} ratio={got:.4f}/{ratio:.4f} " \
               f"sheet-leftovers={leftovers}"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = []
    for name, stem, sheet in VIEWS:
        assert confirmed.ready(stem), f"{stem}: confirmed values missing"
        s = build_view(stem)
        x0, y0, x1, y1 = bbox(s.ops)
        s.text(((x0 + x1) / 2, y0 - 4), f"NOT TO SCALE - presentation view of {sheet} "
               "(true 1:20 on the SD sheet)", h=1.8, ha="center", va="top")
        x0, y0, x1, y1 = bbox(s.ops)
        pad = 4
        s.render(str(OUT / name), None, crop=(x0 - pad, y0 - pad - 2, x1 + pad, y1 + pad))
        made.append(OUT / f"{name}.svg")
        print(f"{name}.svg  {x1 - x0 + 2 * pad:.0f} x {y1 - y0 + 2 * pad + 2:.0f} mm  ({sheet})")
    results = [check(p) for p in made]
    for ok, msg in results:
        print(("PASS " if ok else "FAIL ") + msg)
    if not all(ok for ok, _ in results):
        raise SystemExit("presentation asset check failed")
    return made


if __name__ == "__main__":
    main()
