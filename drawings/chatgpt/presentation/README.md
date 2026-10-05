# Born Fragrance editable portrait presentation

Open `index.html` in Chrome or Edge. It is self-contained and works offline.

- Click text to edit it.
- Double-click a drawing or render to replace it with an SVG, PNG or JPEG.
- Click a material swatch to change its colour.
- Use the arrows above a page to change page order.
- Use the accent colour control to change the presentation theme.
- Browser edits are saved locally. **Download edited HTML** saves a portable copy with all images embedded. Browser storage is not a shared repository edit.
- Use **Print / PDF**, choose A3 portrait, no browser headers/footers, and enable background graphics. The print layout retains A3 dimensions; the phone layout reflows text for reading.

`presentation.pdf` is the initial A3 portrait export. Editing the HTML does not automatically update that PDF; print again after editing.

Build the initial file with `python drawings/chatgpt/presentation/build.py`. The generator reads the pinned Claude asset commit `2941708870757a46da6f33b40b4330994e909f40` using Git; fetch `claude/great-goldberg-anh45q` first in a fresh checkout. This resets generated HTML to the repository assets; keep downloaded custom versions separately.

The ten-page presentation embeds Claude's six clean SVG assets unchanged from PR #5, commit `2941708`. Project dimensions, materials and open items are transcribed from its `HANDOFF.md` (Rev A spec source `0e28b4e`). Drawing views are **not to scale**, uniformly fitted, and retain red warnings. Refer to the original A3 landscape 1:20 drawing set for technical use. The approved render is design intent only; depicted styling props are outside the technical scope. TBC #4, #16, #23 and #26 remain open; the 450 mm counter side gaps retain a consultant CHECK.

All presentation text and layout are editable. The imported render and drawing objects can be replaced; their internal geometry is not edited through this browser interface.
