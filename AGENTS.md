# Rules for every contributor (human or AI tool)

This repo is shared by several AI tools (Claude, ChatGPT, Gemini, Antigravity,
Hermes, ...). Follow these rules to avoid collisions.

1. **Never push to `main`.** Work on your own branch named `<tool>/<task>`
   (e.g. `claude/plans`) and open a pull request. The owner merges.
2. **Add, don't overwrite.** Never delete or edit another tool's files.
   Read the current state and latest commit before every write.
3. **One output folder per tool:** `drawings/<tool>/` (e.g. `drawings/claude/`,
   `drawings/chatgpt/`). Outputs never collide and can be compared.
4. **Source of truth:** `spec/SHOP_SPEC.json` and `spec/TBC.md`.
   Only the owner edits these. Propose changes in a PR description or issue.
5. **Dimensions come only from `SHOP_SPEC.json`.** The render is design intent
   only. Anything not in `locked` is TBC: mark it in a revision cloud,
   never guess.
6. **Brand assets** live in `assets/brand/`. Source logo is cream; drawings
   use black fill, scaled by aspect ratio only (never redrawn or distorted).
7. **Exclusions** listed in the spec (timber, brass, pendants, plants,
   loose products, ...) never appear in drawings.
8. **Drawing standard:** A3 landscape, 1:20, title block with sheet no.,
   revision, scale bar; dimensions computed from data, not typed by hand.
   Export PDF + SVG + DXF.
9. **Say what you did:** each PR describes the tool used, the spec version it
   read (commit SHA), and any TBC items it hit.
