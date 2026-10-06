# BORN FRAGRANCE — architectural presentation

Client and consultant coordination package. Open `BORN_FRAGRANCE_Architecture.pptx` in PowerPoint. A3 landscape; drawings carry individual scales valid only at original A3 size. Text and drawing geometry are native editable PowerPoint objects; logo and original reference render are embedded images.

Source: repository `spec/SHOP_SPEC.json` (including owner-confirmed Rev A), `spec/TBC.md`, and `drawings/chatgpt/presentation/presentation.pdf`. The source PDF contains four 664 mm modules, a 1000 x 2580 door and the centred counter. These supersede earlier unapproved TBC proposals. The render is never measured.

The three books named in the handoff were not attached or available in the repository. No pages or technical claims are attributed to them. Assembly details are proposed coordination strategies, not engineered or manufacturer-approved fabrication instructions.

Active review sheets use concise connection-specific TBC notes; the owner requested removing their clouds. The paused archive retains its historical clouds. Surveyed dimensions are not available. Existing spec and Claude files are unchanged.

Build the current revision with `PYTHONPATH=/tmp/bf-ppt-libs python3 drawings/chatgpt/architecture_pptx/review_g.py` (python-pptx, CairoSVG). It loads pinned committed revision F. Export the full Architecture PPTX to PDF with LibreOffice, then run `audit.py` to verify the deck and produce the focused review PDF, audit report and SVG exports. Older generators reproduce their corresponding historical revisions.

## Current review — revision G

Use `BORN_FRAGRANCE_Review_G.pptx` / `.pdf` for the eight active sheets. All seven technical sheets have revised native annotations: aligned direct descriptions, consistent title/body typography, horizontal leader terminals and corrected shelf, plinth, glass, track and branding targets. Dimension numbers are centred; side pitch figures sit outside their dimension line. The axonometric has an editable picture crop to remove unused raster space and shorter leaders on aligned left/right columns. The five-image cover arrangement from F is retained.

The audit checks all 27 new callouts for overlapping text boxes and leader intersections with exported PDF text, alongside the existing A3, geometry and dimensional-chain checks. Named measured geometry is unchanged; the 15 paused slides are unchanged in XML and PDF rendering. This presentation cleanup does not resolve the documented TBC decisions or certify LOD 350.

## Previous review — revision F

Use `BORN_FRAGRANCE_Review_F.pptx` / `.pdf`: eight active sheets, AP-01, AP-03, AP-05–10. The owner-selected material palette AP-11 is removed. The full Architecture package has 23 sheets, including the 15 unchanged paused archive sheets AP-12–26.

The reference board on the cover is replaced by `born-fragrance-shop-neutral.png`, an image-generation-tool edit of the original render to reduce the reddish/orange cast, restore neutral ivory/beige material tones and retain gently warm lighting. The edited board remains design intent only; the original `assets/renders/born-fragrance-shop.png` is untouched. Technical drawings and their dimensions are unchanged. The edited image is saved locally so rebuilding F does not invoke image generation again.

The cover no longer displays the entire collage as one image. Five independently editable picture frames crop the saved board into a large storefront view, a supporting interior view, and three aligned details with direct captions. The material swatches are omitted from this gallery. Crop/frame aspect ratios are verified so the images are not stretched. `BORN_FRAGRANCE_Render_Layout_F.png` is the exported cover preview.

Run `python3 drawings/chatgpt/architecture_pptx/review_f.py`, export the full Architecture PPTX using the LibreOffice command below, then run `audit.py`. Earlier review files are historical snapshots. The LOD assessment in `LOD_REVIEW_E.md` still applies to the technical views; its page-nine palette entry is now omitted.

## Previous review — revision E

Open `BORN_FRAGRANCE_Review_E.pdf` or the editable `BORN_FRAGRANCE_Review_E.pptx`. All nine active slides now omit the three footer fields, narrative sidebars and cloud graphics selected by the owner. The header remains. New drawing interfaces occupy the former sidebar area: rear/side corner, pivot edge, unit head/ceiling, folded tray/LED, recessed plinth, halo stand-off and counter footprint. The axonometric has thin trays, depth-tested edges, a consistent 600 cut, exploded ceiling tracks with projection guides, and native editable leaders anchored to model coordinates.

See `LOD_REVIEW_E.md` for component reliability, open questions, internet references and stable sheet IDs/scales. Footer/cloud removal is an explicit owner presentation override; it does not close TBC decisions. The approved geometry remains; counter panel split and fabrication/MEP connections remain unresolved. The 15 paused sheets AP-12–26 retain their original content and original footer/cloud graphics in the full archive deck.

Rebuild in the cloud:

```sh
cd /workspace/born_fragrance
python3 -m pip install --target /tmp/bf-ppt-libs cairosvg==2.9.1
MPLCONFIGDIR=/tmp/bf-mpl XDG_CACHE_HOME=/tmp/bf-font-cache PYTHONPATH=/tmp/bf-ppt-libs python3 drawings/chatgpt/architecture_pptx/review_e.py
XDG_CACHE_HOME=/tmp/bf-font-cache soffice -env:UserInstallation=file:///tmp/bf-lo-profile --headless --convert-to pdf --outdir drawings/chatgpt/architecture_pptx drawings/chatgpt/architecture_pptx/BORN_FRAGRANCE_Architecture.pptx
python3 drawings/chatgpt/architecture_pptx/audit.py
```

Review_C and Review_D are historical snapshots. Main orthographic drawings remain 1:20 at A3 landscape; enlarged interface scales are printed beside each view. The cutaway and reference render are NTS. SVGs use adjacent media assets; PPTX and PDF embed images.

## Previous owner review — revision D

Open `BORN_FRAGRANCE_Review_D.pdf` or the editable `BORN_FRAGRANCE_Review_D.pptx`. Nine active sheets: AP-01, AP-03, AP-05–11. AP-04 floor-finish sheet is removed at the owner's request; AP-02 was removed previously. The full Architecture files contain 24 sheets, retaining paused AP-12–26 unchanged.

Numbered bubbles are replaced with direct component names. The plan now includes storefront posts, rear posts and counter frame footprints; ceiling coordination includes joinery below, spot symbols, aiming indicators and track offsets. Storefront and rear elevations show steel frames, folded trays, integrated light, mesh where approved and indicative fragrance bottles. Side elevations show a solid column return, with displays facing the street around the corner.

The owner's render reference changes the visible counter front to a left mesh panel beside a larger light-neutral solid panel, with a black perimeter frame and light top. The approved 1000 × 450 × 900 envelope and position remain. The drawn split and top thickness are visual proposals under TBC #16; they are not extracted measurements. This conflicts with the old small central insert in confirmed Rev A. The spec has not been edited, and paused counter details AP-20/21 retain the old design: use them only as historical references pending owner/spec coordination. The revised counter appears on AP-07 and AP-10.

Audit: A3 sizes, named geometry and dimensional chains verified; paused AP-12–26 render pixel-identically to their original PDFs. Standalone SVGs require adjacent `svg/media/` assets; PDF and PPTX embed their images. Review_C files below are retained as the previous review snapshot.

## Owner review revision C

Use `revise.py` to reproduce the reviewed version from the pinned Rev B commit (also requires matplotlib). The original `build.py` reproduces Rev B only. Rev C removes AP-02, develops the plan and both side elevations, and replaces the wireframe axonometric with a shaded model. The owner explicitly permits sparse indicative perfume bottles; these are not dimensions, stock quantities or fabrication data. LOD 350 remains a coordination-development target pending the documented site/consultant decisions.

AP-12–26 are paused and preserved unchanged, including their historical register. Stable drawing numbers are retained after removing AP-02. Its original page remains recoverable from Git. The new PPTX/PDF has 25 pages; active review is the first 10 pages (original AP-01 and AP-03–11).

Use `BORN_FRAGRANCE_Review_C.pptx` / `.pdf` for the focused 10-page review, excluding all paused sheets. The full `Architecture` file preserves the paused pages for reference. The audit checks those original pages 12–26 for pixel-identical PDF rendering.
