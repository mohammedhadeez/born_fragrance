# BORN FRAGRANCE — architectural presentation

Client and consultant coordination package. Open `BORN_FRAGRANCE_Architecture.pptx` in PowerPoint. A3 landscape; drawings carry individual scales valid only at original A3 size. Text and drawing geometry are native editable PowerPoint objects; logo and original reference render are embedded images.

Source: repository `spec/SHOP_SPEC.json` (including owner-confirmed Rev A), `spec/TBC.md`, and `drawings/chatgpt/presentation/presentation.pdf`. The source PDF contains four 664 mm modules, a 1000 x 2580 door and the centred counter. These supersede earlier unapproved TBC proposals. The render is never measured.

The three books named in the handoff were not attached or available in the repository. No pages or technical claims are attributed to them. Assembly details are proposed coordination strategies, not engineered or manufacturer-approved fabrication instructions.

New detail decisions remain in clouds under TBC #16/#26. Surveyed dimensions are not available. Confirmed design dimensions, site assumptions and unapproved fabrication decisions are distinguished throughout. Existing spec and Claude files are unchanged.

Build: `python3 drawings/chatgpt/architecture_pptx/build.py` (python-pptx, cairosvg, Pillow). Export PDF with LibreOffice. `audit.py` verifies the written deck and creates the audit report and SVG exports when the PDF is available.

## Owner review revision C

Use `revise.py` to reproduce the reviewed version from the pinned Rev B commit (also requires matplotlib). The original `build.py` reproduces Rev B only. Rev C removes AP-02, develops the plan and both side elevations, and replaces the wireframe axonometric with a shaded model. The owner explicitly permits sparse indicative perfume bottles; these are not dimensions, stock quantities or fabrication data. LOD 350 remains a coordination-development target pending the documented site/consultant decisions.

AP-12–26 are paused and preserved unchanged, including their historical register. Stable drawing numbers are retained after removing AP-02. Its original page remains recoverable from Git. The new PPTX/PDF has 25 pages; active review is the first 10 pages (original AP-01 and AP-03–11).

Use `BORN_FRAGRANCE_Review_C.pptx` / `.pdf` for the focused 10-page review, excluding all paused sheets. The full `Architecture` file preserves the paused pages for reference. The audit checks those original pages 12–26 for pixel-identical PDF rendering.
