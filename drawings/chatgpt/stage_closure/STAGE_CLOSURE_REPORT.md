# BORN FRAGRANCE — stage closure report

Closed: 6 October 2026 (Asia/Bahrain). Scope: architectural/interior presentation stage.

The stage deliverables are saved and committed. The outstanding project pull requests have been merged into `main`, and the completed working branches have been deleted. Original branch heads remain recoverable through archive tags and a verified full-history Git bundle. Presentation closure does not constitute fabrication, survey or consultant approval.

## Final deliverables

Use revision **I** for the client presentation:

- [Eight-page client PDF](../architecture_pptx/BORN_FRAGRANCE_Review_I.pdf)
- [Editable PowerPoint](../architecture_pptx/BORN_FRAGRANCE_Review_I.pptx)
- [Full 23-sheet archive PDF](../architecture_pptx/BORN_FRAGRANCE_Architecture.pdf)
- [Full editable archive](../architecture_pptx/BORN_FRAGRANCE_Architecture.pptx)
- [Verification report](../architecture_pptx/AUDIT.md)
- [File inventory and SHA-256 hashes](FILE_MANIFEST.json)

The active set contains the design reference gallery, overall plan, ceiling plan, storefront elevation, rear elevation, left/right display elevations and cutaway axonometric. The main technical views are A3 landscape at 1:20; enlarged interfaces carry their own scales; reference images and axonometric are NTS.

Historical review revisions C–H, source scripts, SVG exports and linked raster media are retained. The original paused AP-12–26 sheets remain unchanged in the full archive and are excluded from the client review PDF. The portrait presentation and Claude presentation contributions are also preserved on main.

## Final changes

- Uppercase titles; removed top banners, selected footers, narrative sidebars and cloud graphics as directed.
- Direct component descriptions with 27 aligned callouts and corrected leader targets.
- Five-view cover layout using the saved neutral-tone reference render.
- Light-blue entrance glazing with the door leaf emphasised.
- Complete storefront and rear elevation height chains, using approved values.
- Restrained depth shadows in the six marked drawing views.

## Merge and branch closure

| PR | Contribution | Result | Merge commit |
| --- | --- | --- | --- |
| [#5](https://github.com/mohammedhadeez/born_fragrance/pull/5) | Claude presentation views | Merged into main | `6b609ff` |
| [#7](https://github.com/mohammedhadeez/born_fragrance/pull/7) | Architecture presentation and inventory | Merged into portrait branch, then main through #6 | `cdc4cca` |
| [#6](https://github.com/mohammedhadeez/born_fragrance/pull/6) | Portrait presentation plus architecture set | Merged into main | `847165c` |

Deleted remote working branches: `chatgpt/architecture-pptx`, `chatgpt/portrait-presentation`, `chatgpt/tbc-answers`, `claude/great-goldberg-anh45q`. Their original heads are all ancestors of the integration commit. Corresponding local branches are removed. The unrelated local onboarding `work` branch is archived, then removed; its old logo assets are preserved in history rather than overwriting current artwork.

Archive tags use `archive/born-fragrance/2026-10-06/` followed by the original branch name; the local onboarding tag ends in `local-work`. The final stage tag is `stage-closed/born-fragrance-presentation-2026-10-06`. Main remains the working branch. The temporary report-publication branch is removed after its merge.

## Verification

- 208 presentation files checked against saved SHA-256 hashes after merging: all match.
- A3 page sizes, 20 named geometry read-backs and nine dimensional chains: PASS.
- Two added elevation height chains: PASS; rear 100 + 500 + 5 × 400 = 2600; storefront adds 600 = 3200.
- All 27 callouts: no annotation-box overlap or leader intersection with exported text.
- Paused archive pages: pixel-identical to the original; paused slide XML unchanged.
- All marked final views visually inspected. The closure re-audit produced the same client PDF page content; the original saved PDF bytes are retained.
- No merge conflicts. Spec, capsule and AGENTS.md were not edited during closure.

## Open technical decisions retained for the next stage

| Item | Still required |
| --- | --- |
| TBC #4 | Verify finished internal sizes by site survey. |
| TBC #16 | Consultant/fabricator confirmation of fixings, MEP, fire and escape/staff access; counter panel split and top construction. |
| TBC #23 | Verify assumed north direction. |
| TBC #26 | Verify FFL, wall/substrate and construction build-ups. |

The owner-directed counter front shows mesh left and a larger neutral solid panel right; the older approved central insert and paused counter details remain historical until spec coordination. LOD 350 remains a development target, not a certified completed model. The reference render is design intent only and was never measured.

## Recovery

A verified Git bundle is saved at `/workspace/born_fragrance-stage-backup-2026-10-06.bundle`; it is a workspace backup, not a committed repository file. GitHub retains main plus the archive and stage tags. Recover any earlier stage by checking out its tag; the final PDF/PPTX can also be downloaded directly from main.
