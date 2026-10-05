# BORN FRAGRANCE shop drawings (Claude)

Priority 1 set SD-01 to SD-08, A3 landscape at 1:20, rev 00 (preliminary, not for construction).

| Sheet | Drawing |
|---|---|
| SD-01 | Setting-out plan |
| SD-02 | Display / furniture plan |
| SD-03 | Floor finish plan (tile option A drawn, A/B cut table) |
| SD-04 | Reflected ceiling plan |
| SD-05 | Storefront elevation (external) |
| SD-06 | Rear elevation (internal) |
| SD-07 | Left elevation (internal) |
| SD-08 | Right elevation (internal) |

**Files:** each sheet as `.pdf`, `.svg` and `.dxf`. `BF_SD-01-08_set.pdf` has all eight sheets in one file, and `preview/` has PNGs for quick viewing.
**DXF:** model space is in real millimetres (the sheet frame is drawn at ×20). Plot at 1:20 on A3. Dimensions are true DIMENSION entities, and TBC items are on layer `A-TBC-CLOUD`.
**Checks:** see `VERIFICATION.md`. Every dimension is read back from the written files and compared to `spec/SHOP_SPEC.json`.

## Rebuild

```
pip install matplotlib ezdxf
python3 drawings/claude/src/build.py
```

The build reads only `spec/SHOP_SPEC.json`, `spec/TBC.md` and the black logo. Close a TBC in the spec and rerun, and the drawings and verification update.

## Conventions

- **Red cloud = TBC.** Nothing inside a cloud is a dimension; indicative positions are labelled as such.
- **PROPOSAL** marks Claude's arithmetic from `derived_proposals_unverified` (clear aisle 1900, counter x 700–1700).
- **Walls** are drawn as a graphic band only, because wall thickness is unknown.
- **Logos** are uniformly scaled from the black SVG and are never redrawn.
- Items marked with `*` are **proposed TBC items #23–#27**, gaps found in review that `spec/TBC.md` doesn't number yet:
  - **#23** North direction
  - **#24** Side bay count, widths and upright spacing
  - **#25** Counter lateral position (centring is a proposal)
  - **#26** Vertical datum (FFL) and wall thickness / construction
  - **#27** Counter mesh insert size
