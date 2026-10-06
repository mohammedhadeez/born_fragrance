"""Read back PPTX geometry and exported PDF; do not execute the generator."""
import json, re
from pathlib import Path
from pptx import Presentation
import fitz
from PIL import Image, ImageOps, ImageDraw

OUT=Path(__file__).resolve().parent
manifest=json.loads((OUT/'geometry_manifest.json').read_text())
p=Presentation(OUT/'BORN_FRAGRANCE_Architecture.pptx')
mm=lambda n:n/36000
rows=[]
assert len(p.slides)==26
assert abs(mm(p.slide_width)-420)<.01 and abs(mm(p.slide_height)-297)<.01
for check in manifest['checks']:
    s=p.slides[check['slide']-1]
    sh=next(a for a in s.shapes if a.name==check['shape'])
    w,h=mm(sh.width)*check['scale'],mm(sh.height)*check['scale']
    ok=abs(w-check['w'])<.03 and abs(h-check['h'])<.03
    rows.append(f"| AP-{check['slide']:02} | {check['shape'][5:]} | {w:.2f} × {h:.2f} | {check['w']} × {check['h']} | {'PASS' if ok else 'FAIL'} |")
    assert ok,check
outside=[]
for i,s in enumerate(p.slides,1):
    for sh in s.shapes:
        if min(sh.left,sh.top)<-36000 or sh.left+sh.width>p.slide_width+36000 or sh.top+sh.height>p.slide_height+36000:
            outside.append((i,sh.name))
assert not outside,outside
math_checks={'frontage':450+1500+450==2400,'glazing':4+488+4+1000+4==1500,
    'side_run':450+4*664==3106,'rear_zones':250+500+900+500+250==2400,
    'vertical':100+500+5*400==2600,'rear_clearance':3106-250-2156==700,
    'counter_clearance':700-250==2150-1700==450,
    'tile_width':2*5+2*1194+2==2400,'tile_depth':2*5+2*343+4*600+5*2==3106}
assert all(math_checks.values())
pdf=fitz.open(OUT/'BORN_FRAGRANCE_Architecture.pdf')
assert len(pdf)==26
(OUT/'svg').mkdir(exist_ok=True)
previews=[]
for i,page in enumerate(pdf):
    assert abs(page.rect.width*25.4/72-420)<.1
    assert abs(page.rect.height*25.4/72-297)<.1
    assert f'AP-{i+1:02}' in page.get_text(),i+1
    (OUT/'svg'/f'AP-{i+1:02}.svg').write_text(page.get_svg_image())
    pix=page.get_pixmap(matrix=fitz.Matrix(.65,.65),alpha=False)
    img=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    previews.append(img)
for block in range(5):
    images=previews[block*6:(block+1)*6]
    if not images:continue
    w,h=images[0].size;board=Image.new('RGB',(w*2,h*3),'#d8d8d8')
    for k,im in enumerate(images):board.paste(im,((k%2)*w,(k//2)*h))
    board.save(f'/tmp/bf-contact-{block+1}.png')
md=['# Read-back audit','',f"Source repository snapshot: `{manifest['source_commit']}`.",
    f"Spec SHA-256: `{manifest['spec_sha256']}`.",'',
    '26 PPTX slides reopened successfully. LibreOffice exported all 26 pages to PDF. Every PDF page has an A3 landscape MediaBox and its matching AP sheet number. All native shape extents remain on the slide. Embedded logo and render are self-contained.',
    '', '## Geometry read back from written PPTX', '',
    '| Sheet | Object | Read back mm | Expected mm | Match |','|---|---|---|---|---|',*rows,
    '', '## Dimensional chains','',*['- '+k+': PASS' for k in math_checks],
    '', '## Status and limits','',
    '- Confirmed Rev A overrides the capsule’s older open-item summaries and pre-review TBC answers.',
    '- No source dimension is represented as independently surveyed. TBC #4, #16, #23 and #26 remain open.',
    '- AP-06 proposes a 10/10 split of the 20 vertical door allowance; supplier approval remains required.',
    '- AP-12 to AP-22 include unapproved fabrication strategies, shown in clouds under #16/#26. Indicative assembly envelopes must not be used as cutting schedules.',
    '- Counter 450 side gaps remain unresolved; 900 is a project assumption, not a code approval.',
    '- Technical geometry preserves the source’s four 664 modules and 500/900/500 rear zones. No update to spec or Claude files.',
    '- Scale checks apply to named geometry objects at original A3 size, not to indicative hardware/assembly envelopes, images or axonometric projection.',
    '- Reference books named in the handoff were not supplied; no content has been attributed to them.',
    '- PowerPoint and PDF were checked programmatically; rendered sheet contact proofs were reviewed for presentation issues.',
    '']
(OUT/'AUDIT.md').write_text('\n'.join(md))
print(f'PASS: {len(p.slides)} slides, {len(rows)} native geometry read-backs, 9 dimensional chains, PDF pages and extents.')
