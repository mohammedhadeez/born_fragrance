# BORN FRAGRANCE — Context Capsule

Read this first. It brings any AI tool (ChatGPT, Claude, Gemini, Antigravity,
Hermes) up to date on the project. It is a **summary**, not the source of
truth: if anything here disagrees with `spec/SHOP_SPEC.json`, `spec/TBC.md`
or `AGENTS.md`, those files win.

| | |
|---|---|
| Capsule version | v1, 2026-10-05 |
| Written by | Claude |
| Spec state it describes | commit `e1fbc1c` on branch `claude/great-goldberg-anh45q` (see §6) |
| Owner | mohammedhadeez. The only person who merges, closes TBC items or changes the spec |

---

## 1. What the project is

A full set of shop drawings for **BORN FRAGRANCE**, a small perfume shop.
The design is **final and approved**. The job now is to turn it into
dimensionally honest drawings, not to redesign it.

- **Inputs:** an AI-generated render (design intent only), the owner's
  written brief, and the brand logo.
- **Output:** measured drawings produced **in code** (true scale), with
  every unverified value shown as **TBC** instead of guessed.

## 2. Ground rules (summary of `AGENTS.md`)

1. Never push to `main`. Work on `<tool>/<task>` (e.g. `chatgpt/plans`) and open a PR.
2. Add files only. Never edit or delete another tool's files.
3. Outputs go in `drawings/<tool>/` only.
4. Only the owner edits `spec/SHOP_SPEC.json` and `spec/TBC.md`. Propose changes in a PR description.
5. Dimensions come only from the spec. **The render is never measured.**
6. Anything not locked is **TBC**: draw it in a revision cloud with its TBC number. Never guess or round to look complete.
7. Logo: use the black SVG, scaled by aspect ratio only. Never redraw or distort it.
8. Never draw anything on the exclusions list (§3).
9. Each PR states the tool used, the spec commit SHA read, and every TBC item hit.

## 3. Locked data (from the brief, owner-approved)

| Item | Value |
|---|---|
| Internal size | **2400 W × 3106 D mm** (whether this is the finished size is TBC #4) |
| Ceiling height | **2600 mm** |
| Entrance | single **1000 mm pivot door**, **12 mm clear toughened glass** |
| Coordinate origin | front-left internal corner; x across, y into the shop; units mm |
| Main frame | 25×25×1.6 MS SHS |
| Secondary frame | 20×20×1.6 MS SHS |
| Shelf depth | 250 mm |
| Bay width rule | about 600, adjusted to the actual wall run |
| Mesh | about 20×40 diamond expanded metal, black, mainly upper level |
| Walls | raw textured light plaster |
| Floor | 1200×600 rectified stone-look porcelain, 2 mm grout |
| Metal finish | matte black powder coat |
| Counter | **1000 W × 450 D × 900 H**, 20×20 black steel frame, light neutral front panel with small mesh insert, simple light top |
| Lighting | 3000 K; 2 black ceiling tracks; simple cylindrical black adjustable spots; concealed LED under shelves; no pendants |
| Signage | exterior black backlit/halo-lit, interior smaller non-illuminated black logo; both sizes TBC |
| Logo | `assets/brand/born-fragrance-logo-black.svg`, aspect ratio **2.21 : 1** |

**Exclusions (never draw):** timber, brass, decorative arches, heavy
joinery, pendants, decorative ceiling features, plants, loose products.

## 4. Proposals (Claude's arithmetic, unverified; label as PROPOSAL)

| Item | Value | Note |
|---|---|---|
| Clear aisle | 1900 | 2400 − 2 × 250 |
| Counter position | x = 700 to 1700 (centred) | y position is TBC #10 |
| Counter side clearance | 450 each side | under 600: flag **CHECK** |
| Floor tile cuts (depth) | 4 full courses + 2 × 348 | 4×600 + 5×2 grout + 2×348 = 3106. Tile direction TBC #22 |
| Floor tiles (width) | **not** an exact fit | 2 × 1200 + 2 mm joint = 2402 > 2400 |
| Side bays | **superseded** | "5 × 621.2" assumed the full 3106 run; real run depends on TBC #9 and #18 |

## 5. Render vs spec: known conflicts

The render (`assets/renders/born-fragrance-shop.png`) shows the storefront,
interior views and a materials board (raw plaster, black metal shelf,
metal mesh panel, stone-look floor tile). Read it for **look and intent
only**.

| Render shows | Spec / handling |
|---|---|
| Shop far deeper than 3106 (7–8 bays per side) | Ignore. Spec depth wins |
| Sign looks front-lit by downlights | Spec says halo-lit → TBC #17 |
| Storefront: display column, ~1500 opening, display column; shelves face the street | Widths, depths and facing → TBC #2, #18 |
| No glass door leaf visible | Door is locked as a 1000 glass pivot; swing → TBC #3 |
| Recessed downlights at the entrance and over the sign | TBC #12 |
| Glowing strip at the base of the units | TBC #13 |
| Closed lower cabinets | TBC #7 |
| Mesh at the top of the interior side units | TBC #8 |
| Black metal shelves | Shelf material and thickness → TBC #19 |
| Step at the entrance | TBC #20 |
| Counter front about half mesh | Brief says "small" insert; size TBC (Priority 2) |
| Plants, bottles, gold caps | Excluded |

**Brand history:** an earlier render said "HERITAGE PERFUMES" with a crest.
That is obsolete. The brand is BORN FRAGRANCE with the perfume-bottle
emblem in the logo file.

## 6. Repo state

```
AGENTS.md                         rules for every tool
spec/SHOP_SPEC.json               source of truth for dimensions
spec/TBC.md                       22 open items (all Open)
assets/brand/born-fragrance-logo.svg        cream source, 1774×887 canvas (2.0)
assets/brand/born-fragrance-logo-black.svg  black, viewBox cropped to artwork 1419.5×643 (2.21)
assets/brand/born-fragrance-logo.png        cream raster
assets/renders/born-fragrance-shop.png      approved render (intent only)
context/CONTEXT_CAPSULE.md        this file
--                                stray placeholder file from the first commit (owner to remove)
```

- **On `main`:** everything above except the `e1fbc1c` fix and this capsule.
  PR #1 merged the spec, the TBC list, `AGENTS.md` and the black logo.
- **On `claude/great-goldberg-anh45q` only, until merged:** commit
  `e1fbc1c`. It fixes the two findings from the Codex review on PR #1. It
  crops the black logo's viewBox to the artwork, sets the ratio to 2.21,
  changes the tile cuts from 353 to 348, and marks the side bays as
  superseded. Read the spec from this branch until it reaches `main`.
- **Drawings:** none exist yet.
- **`main` is not branch-protected.** The owner has been advised to require PRs.

## 7. Open TBC items (summary of `spec/TBC.md`)

| # | Item | Blocks |
|---|---|---|
| 1 | Storefront overall height, sign band height | SD-05 |
| 2 | Display column width, door opening width, fixed glass | SD-01, SD-05 |
| 3 | Door swing direction, pivot offset | SD-01, SD-05 |
| 4 | Is 2400 × 3106 the finished size (after plaster)? | All |
| 5 | Display frame height | SD-06–08 |
| 6 | Shelf count and pitch per bay | SD-06–08 |
| 7 | Base cabinet height and door type | SD-02, SD-06–08 |
| 8 | Mesh extent on side walls | SD-07, SD-08 |
| 9 | Rear wall bay width, shelf count, logo size and height | SD-06 |
| 10 | Counter distance from rear wall, staff clearance | SD-02 |
| 11 | Track positions and lengths, spotlight count | SD-04 |
| 12 | Recessed downlights: keep or omit | SD-04, SD-05 |
| 13 | Floor-level LED strip: keep or omit | SD-02, SD-04 |
| 14 | Floor tile extent under display units | SD-03 |
| 15 | Exterior and interior sign sizes | SD-05, SD-06 |
| 16 | Fixings, MEP, fire and escape | All |
| 17 | Exterior sign lighting: halo-lit or front-lit | SD-04, SD-05 |
| 18 | Storefront column depth, shelf facing | SD-01, SD-02, SD-05, SD-07, SD-08 |
| 19 | Shelf material and thickness | SD-06–08 |
| 20 | Entrance threshold or step, level change | SD-01, SD-03, SD-05 |
| 21 | Ceiling finish | SD-04 |
| 22 | Floor tile orientation; grout-adjusted cut sizes | SD-03 |

**Closing these unblocks the most:** #4, #2 + #18, #5, #6, #22.

## 8. Drawing standard and sheet list

**Method:** code only (Python, ezdxf + matplotlib), never image generation
for measured sheets. A3 landscape, true 1:20, one drawing per sheet. Each
sheet has a title block (sheet no., title, project, scale, date, rev 00,
black logo, "TBC items shown in clouds", spec SHA), a graphic scale bar
and layers by type. The north arrow is TBC. Dimensions are computed from
spec data, never typed. Export PDF + SVG + DXF.

| Sheet | Drawing |
|---|---|
| SD-01 | Setting-out plan |
| SD-02 | Display / furniture plan |
| SD-03 | Floor finish plan |
| SD-04 | Reflected ceiling plan |
| SD-05 | Storefront elevation (external) |
| SD-06 | Rear elevation |
| SD-07 | Left elevation |
| SD-08 | Right elevation |
| P2-1 | Typical display-wall detail, 1:5 (hold until TBC #5–#8 closed) |
| P2-2 | Counter detail, 1:10 (hold until TBC #10 closed) |

**Verification (required before any sheet is accepted):** a table of
drawing | dimension | value read back from the DXF/SVG | spec value | match,
plus a plan-vs-elevation cross-check and a list of every TBC clouded.

## 9. What happens next

1. Owner merges the `e1fbc1c` spec fix to `main`.
2. Claude draws SD-01–SD-04, then SD-05–SD-08, in `drawings/claude/`, and runs the verification.
3. Other tools may produce an independent set in `drawings/<tool>/` for comparison, if the owner asks.
4. Owner closes TBC items, starting with #4, #2, #18, #5, #6, #22. Each closed item turns clouds into dimensions on the next run.
5. Priority 2 details, then the owner's extra detailing, then an optional presentation restyle (restyle only, no geometry changes).

## 10. Decision log

| Date | Decision |
|---|---|
| 2026-10-05 | Image generation can't hold scale, so measured drawings are made in code; image mode is for presentation only |
| 2026-10-05 | "Final approved design"; render = design intent only; unverified values are TBC, never guessed |
| 2026-10-05 | Brand is BORN FRAGRANCE; the HERITAGE PERFUMES crest render is obsolete |
| 2026-10-05 | Logo drawn in black (source is cream #fff4df) |
| 2026-10-05 | Multi-tool repo rules adopted (`AGENTS.md`); PR #1 merged |
| 2026-10-05 | TBC items #17–#22 added after the render-vs-spec review |
| 2026-10-05 | Codex review on PR #1: logo canvas ratio and grout-adjusted tile cuts fixed in `e1fbc1c` |
