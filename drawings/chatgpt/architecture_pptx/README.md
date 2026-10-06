# BORN FRAGRANCE — architectural presentation

Client and consultant coordination package. Open `BORN_FRAGRANCE_Architecture.pptx` in PowerPoint. A3 landscape; drawings carry individual scales valid only at original A3 size. Text and drawing geometry are native editable PowerPoint objects; logo and original reference render are embedded images.

Source: repository `spec/SHOP_SPEC.json` (including owner-confirmed Rev A), `spec/TBC.md`, and `drawings/chatgpt/presentation/presentation.pdf`. The source PDF contains four 664 mm modules, a 1000 x 2580 door and the centred counter. These supersede earlier unapproved TBC proposals. The render is never measured.

The three books named in the handoff were not attached or available in the repository. No pages or technical claims are attributed to them. Assembly details are proposed coordination strategies, not engineered or manufacturer-approved fabrication instructions.

New detail decisions remain in clouds under TBC #16/#26. Surveyed dimensions are not available. Confirmed design dimensions, site assumptions and unapproved fabrication decisions are distinguished throughout. Existing spec and Claude files are unchanged.

Build: `python3 drawings/chatgpt/architecture_pptx/build.py` (python-pptx, cairosvg, Pillow). Export PDF with LibreOffice. `audit.py` verifies the written deck and creates the audit report and SVG exports when the PDF is available.
