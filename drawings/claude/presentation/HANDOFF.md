# Presentation handoff: Claude to ChatGPT

These are drawing assets for the A3 portrait HTML/CSS presentation
(`chatgpt/portrait-presentation`, in `drawings/chatgpt/`).

**Source commit:** `main` @ `0e28b4e`, the Rev A spec with the merged TBC answers.
The technical SD-01 to SD-08 sheets in `drawings/claude/` are unchanged and remain the
true 1:20 record.

## 1. Asset paths

All files are in `drawings/claude/presentation/`. Each view comes as an SVG (vector, with every label kept as
editable `<text>`) and a 200 dpi PNG preview of the same view.

| View | SVG | Source sheet | Size (mm) |
|---|---|---|---|
| Furniture plan | `furniture-plan.svg` | SD-02 | 181 × 205 |
| Storefront elevation | `storefront-elevation.svg` | SD-05 | 160 × 206 |
| Rear elevation | `rear-elevation.svg` | SD-06 | 163 × 168 |
| Left display elevation | `left-elevation.svg` | SD-07 | 214 × 181 |
| Right display elevation | `right-elevation.svg` | SD-08 | 214 × 181 |
| Reflected ceiling plan | `reflected-ceiling-plan.svg` | SD-04 | 177 × 186 |

Other assets:
- **Approved render:** `assets/renders/born-fragrance-shop.png` (design intent only)
- **Logo:** `assets/brand/born-fragrance-logo-black.svg`. Scale it uniformly only; its ratio is 2.2076 : 1.
- **Full technical set:** `drawings/claude/BF_SD-01-08_set.pdf`

Usage notes:
- **Captions:** every view already carries "NOT TO SCALE - presentation view of SD-0x". Keep it,
  or repeat it in your caption.
- **Sheet furniture removed:** the sheet border, title block, scale bar and side notes are gone. All
  geometry, dimensions and coordination warnings are kept.
- **Scaling and fonts:** the SVGs scale freely, but use one uniform scale and never stretch them. Labels use
  `DejaVu Sans` inline; override it with CSS (`svg text { font-family: ... !important }`) if needed.
- **Colours in the drawings:** red is a TBC or CHECK warning, blue is a dimension, and dark fill is the
  black steel frame. Do not recolour the red warnings.
- **Regenerating:** run `python3 drawings/claude/src/present.py`. It also re-runs the asset checks.

## 2. Confirmed key dimensions (mm)

| Item | Value |
|---|---|
| Internal size | 2400 W × 3106 D; ceiling 2600 |
| Storefront | 450 column + 1500 opening + 450 column; the opening holds 488 fixed glass + 1000 × 2580 pivot door (12 mm toughened, inward); 600 sign band; 3200 overall |
| Storefront columns | 450 × 450, shelves face the street |
| Side display runs | 2656 long (behind the columns to the rear wall), 4 bays × 664, 250 deep |
| Shelf levels | 600 (cabinet top), 1000, 1400, 1800, 2200; frame height 2600 |
| Mesh | 2200–2600 front infill on the side bays and storefront columns; **no mesh on the rear bays** |
| Base cabinets | 600 H, including a 100 H × 50 D recessed plinth with toe-kick LED |
| Rear wall | **500 bay + 900 logo zone + 500 bay**, 250 deep |
| Interior logo | **600 × 271.8**, centred at 1900 above floor, non-illuminated black |
| Exterior logo | 1000 × 452.98, black halo-lit on 25 mm stand-offs, centred in the sign band |
| Counter | 1000 W × 450 D × 900 H, **centred at x 700–1700**, rear edge y 2156 (700 to the rear unit) |
| Counter clearance | **450 each side to the side-unit face: CHECK with consultant (TBC #16)** |
| Counter mesh insert | 300 × 450, centred, 150 above floor |
| Lighting | 3000 K; 2 black tracks at x 650 / 1750, 2206 long, 4 spots each; 3 recessed downlights; concealed shelf LED + toe-kick LED |
| Floor | 1200 × 600 porcelain, option A (1200 across), 2 mm grout, 5 mm perimeter joint; cuts 1194 / 343 |

The counter clearance is a consultant CHECK. **Do not describe it as code-compliant.**

## 3. Approved materials and finishes

| Code | Material | Where |
|---|---|---|
| M1 | Raw textured light plaster | Walls, rear logo zone |
| M2 | 25×25×1.6 / 20×20×1.6 MS SHS, matte black powder coat | Display frames, counter frame |
| M3 | ~20×40 diamond expanded metal mesh, black | Upper infill 2200–2600, counter insert |
| M4 | 1200×600 rectified stone-look porcelain, 2 mm grout | Floor, full area |
| M5 | 3 mm MS folded tray shelf, 25 mm downstand, matte black | Shelves (concealing the LED) |
| M6 | 1.5 mm powder-coated steel, light neutral, flush handleless | Base cabinet doors |
| M7 | Light neutral panel, simple light-coloured top | Counter front and top |
| M8 | 12 mm clear toughened glass | Pivot door, fixed glass |
| M9 | Smooth gypsum, matte warm off-white | Ceiling |
| L1 | 3000 K concealed LED, black track spots, recessed downlights | Lighting |

**Excluded (never show):** timber, brass, decorative arches, heavy joinery, pendants,
decorative ceiling features, plants, loose products. The reference boards contain
timber, plants and pendants, so take their composition only.

## 4. Open site and consultant items

These are shown as ASSUMED in the drawings. They must be confirmed before fabrication.

| TBC | Item | Needs |
|---|---|---|
| #4 | Is 2400 × 3106 the finished size after plaster? | Site survey |
| #16 | Fixings, MEP, fire and escape, including the 450 counter clearances | Consultant |
| #23 | North direction (drawn as assumed, toward the storefront) | Site survey |
| #26 | Floor-level datum (FFL ±0) and wall thickness (100 assumed) | Site survey |
