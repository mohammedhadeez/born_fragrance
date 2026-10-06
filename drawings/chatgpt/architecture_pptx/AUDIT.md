# Read-back audit

Source repository snapshot: `eeccbde1cde8b3b40e75f30c1da98bf092c2f7eb`.
Spec SHA-256: `58469767d64fed65cb53908ddbf3c5408fb7b5cdafefebd68b173381b6522c2b`.

23 PPTX slides reopened successfully. LibreOffice exported every page to PDF. All pages have A3 landscape MediaBoxes and stable AP sheet numbers. All native shape extents remain on the slide. Embedded images are self-contained.

## Geometry read back from written PPTX

| Sheet | Object | Read back mm | Expected mm | Match |
|---|---|---|---|---|
| AP-03 | internal-envelope | 2400.00 × 3106.00 | 2400 × 3106 | PASS |
| AP-03 | counter-plan | 1000.00 × 450.00 | 1000 × 450 | PASS |
| AP-05 | internal-envelope | 2400.00 × 3106.00 | 2400 × 3106 | PASS |
| AP-06 | storefront-envelope | 2400.00 × 3200.00 | 2400 × 3200 | PASS |
| AP-06 | door-leaf | 1000.00 × 2580.00 | 1000 × 2580 | PASS |
| AP-07 | internal-envelope | 2400.00 × 2600.00 | 2400 × 2600 | PASS |
| AP-07 | counter-elevation | 1000.00 × 900.00 | 1000 × 900 | PASS |
| AP-08 | side-envelope | 3106.00 × 2600.00 | 3106 × 2600 | PASS |
| AP-09 | side-envelope | 3106.00 × 2600.00 | 3106 × 2600 | PASS |
| AP-13 | shelf-section | 250.00 × 3.00 | 250 × 3 | PASS |
| AP-13 | secondary-shs | 20.00 × 20.00 | 20 × 20 | PASS |
| AP-14 | mesh-zone | 664.00 × 400.00 | 664 × 400 | PASS |
| AP-15 | door-glass-head | 12.00 × 40.00 | 12 × 40 | PASS |
| AP-20 | counter-top | 1000.00 × 450.00 | 1000 × 450 | PASS |
| AP-20 | counter-front | 1000.00 × 900.00 | 1000 × 900 | PASS |
| AP-20 | mesh-insert | 300.00 × 450.00 | 300 × 450 | PASS |
| AP-20 | counter-section | 450.00 × 900.00 | 450 × 900 | PASS |
| AP-05 | active-tray | 250.00 × 3.00 | 250 × 3 | PASS |
| AP-05 | active-support | 20.00 × 20.00 | 20 × 20 | PASS |
| AP-07 | active-counter-detail | 1000.00 × 450.00 | 1000 × 450 | PASS |

## Dimensional chains

- frontage: PASS
- glazing: PASS
- side_run: PASS
- rear_zones: PASS
- vertical: PASS
- rear_clearance: PASS
- counter_clearance: PASS
- tile_width: PASS
- tile_depth: PASS

## Status and limits

- Confirmed Rev A overrides the capsule’s older open-item summaries and pre-review TBC answers.
- No source dimension is represented as independently surveyed. TBC #4, #16, #23 and #26 remain open.
- AP-06 proposes a 10/10 split of the 20 vertical door allowance; supplier approval remains required.
- AP-12 to AP-22 include unapproved fabrication strategies, shown in clouds under #16/#26. Indicative assembly envelopes must not be used as cutting schedules.
- Counter 450 side gaps remain unresolved; 900 is a project assumption, not a code approval.
- Technical geometry preserves the source’s four 664 modules and 500/900/500 rear zones. No update to spec or Claude files.
- Scale checks apply to named geometry objects at original A3 size, not to indicative hardware/assembly envelopes, images or axonometric projection.
- Reference books named in the handoff were not supplied; no content has been attributed to them.
- PowerPoint and PDF were checked programmatically; rendered sheet contact proofs were reviewed for presentation issues.
- Revision D removes AP-02 and AP-04. AP-12–26 remain frozen; their original register is historical. Indicative bottles are an explicit owner exception to the loose-products exclusion.
- LOD 350 is a development target, not a certified achieved model status. Survey and unapproved connection details remain open.
- Paused original pages 12–26: PDF raster comparison is pixel-identical at 0.7×. The 8-page Review_G PPTX/PDF omits all paused sheets.
- Rev D removes AP-04 as requested; the active Review_D is nine pages. AP-12–26 still compare pixel-identical to the original. Counter left-mesh front is an owner-directed visual revision; split and construction thicknesses remain TBC #16. The paused counter details retain the old insert and are not current design authority.
- Review E removes selected footer texts, narrative sidebars and clouds from all nine active slides. The owner explicitly overrides their previous presentation requirements. Sheet IDs/scales/status stay in the manifest and README; connection-specific TBC notes remain beside relevant interfaces. The paused archive is unchanged.
- Review E adds 1:5 rear/side corner and plinth sections, 1:2 pivot and folded-tray/light interfaces, a 1:10 counter footprint and a newly rendered orthographic cutaway with native editable leaders. See LOD_REVIEW_E.md for component reliability and references.
- Review F removes AP-11 material palette and replaces the reference render with an owner-requested AI image edit to reduce the reddish cast. All measured technical views remain unchanged Python-generated geometry. Source render and spec are preserved.
- Review F cover is a native five-picture layout: storefront hero, interior view and three aligned details. Crop/frame aspect ratios are read back and checked to prevent stretching.
- Review G annotation audit: 27 direct callouts; no new annotation boxes overlap and no leader intersects exported PDF text ink. Seven technical sheets visually inspected. Named measured geometry and paused slide XML preserved against F.
