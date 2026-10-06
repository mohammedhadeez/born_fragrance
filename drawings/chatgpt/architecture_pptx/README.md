# BORN FRAGRANCE — architectural presentation

Client and consultant coordination package. Open `BORN_FRAGRANCE_Architecture.pptx` in PowerPoint. A3 landscape; drawings carry individual scales valid only at original A3 size. Text and drawing geometry are native editable PowerPoint objects; logo and original reference render are embedded images.

Source: repository `spec/SHOP_SPEC.json` (including owner-confirmed Rev A), `spec/TBC.md`, and `drawings/chatgpt/presentation/presentation.pdf`. The source PDF contains four 664 mm modules, a 1000 x 2580 door and the centred counter. These supersede earlier unapproved TBC proposals. The render is never measured.

The three books named in the handoff were not attached or available in the repository. No pages or technical claims are attributed to them. Assembly details are proposed coordination strategies, not engineered or manufacturer-approved fabrication instructions.

New detail decisions remain in clouds under TBC #16/#26. Surveyed dimensions are not available. Confirmed design dimensions, site assumptions and unapproved fabrication decisions are distinguished throughout. Existing spec and Claude files are unchanged.

Build the current revision with `python3 drawings/chatgpt/architecture_pptx/revise.py` (python-pptx, cairosvg, Pillow, matplotlib, numpy). Export the full Architecture PPTX to PDF with LibreOffice, then run `audit.py` to verify the deck and produce the focused review PDF, audit report and SVG exports. The original `build.py` reproduces Rev B only.

## Current owner review — revision D

Open `BORN_FRAGRANCE_Review_D.pdf` or the editable `BORN_FRAGRANCE_Review_D.pptx`. Nine active sheets: AP-01, AP-03, AP-05–11. AP-04 floor-finish sheet is removed at the owner's request; AP-02 was removed previously. The full Architecture files contain 24 sheets, retaining paused AP-12–26 unchanged.

Numbered bubbles are replaced with direct component names. The plan now includes storefront posts, rear posts and counter frame footprints; ceiling coordination includes joinery below, spot symbols, aiming indicators and track offsets. Storefront and rear elevations show steel frames, folded trays, integrated light, mesh where approved and indicative fragrance bottles. Side elevations show a solid column return, with displays facing the street around the corner.

The owner's render reference changes the visible counter front to a left mesh panel beside a larger light-neutral solid panel, with a black perimeter frame and light top. The approved 1000 × 450 × 900 envelope and position remain. The drawn split and top thickness are visual proposals under TBC #16; they are not extracted measurements. This conflicts with the old small central insert in confirmed Rev A. The spec has not been edited, and paused counter details AP-20/21 retain the old design: use them only as historical references pending owner/spec coordination. The revised counter appears on AP-07 and AP-10.

Audit: A3 sizes, named geometry and dimensional chains verified; paused AP-12–26 render pixel-identically to their original PDFs. Standalone SVGs require adjacent `svg/media/` assets; PDF and PPTX embed their images. Review_C files below are retained as the previous review snapshot.

## Owner review revision C

Use `revise.py` to reproduce the reviewed version from the pinned Rev B commit (also requires matplotlib). The original `build.py` reproduces Rev B only. Rev C removes AP-02, develops the plan and both side elevations, and replaces the wireframe axonometric with a shaded model. The owner explicitly permits sparse indicative perfume bottles; these are not dimensions, stock quantities or fabrication data. LOD 350 remains a coordination-development target pending the documented site/consultant decisions.

AP-12–26 are paused and preserved unchanged, including their historical register. Stable drawing numbers are retained after removing AP-02. Its original page remains recoverable from Git. The new PPTX/PDF has 25 pages; active review is the first 10 pages (original AP-01 and AP-03–11).

Use `BORN_FRAGRANCE_Review_C.pptx` / `.pdf` for the focused 10-page review, excluding all paused sheets. The full `Architecture` file preserves the paused pages for reference. The audit checks those original pages 12–26 for pixel-identical PDF rendering.
