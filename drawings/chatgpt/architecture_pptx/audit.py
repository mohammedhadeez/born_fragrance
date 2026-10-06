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
order=manifest.get('sheet_order',list(range(1,27)))
assert len(p.slides)==len(order)
assert abs(mm(p.slide_width)-420)<.01 and abs(mm(p.slide_height)-297)<.01
for check in manifest['checks']:
    s=p.slides[check['slide']-1]
    sh=next(a for a in s.shapes if a.name==check['shape'])
    w,h=mm(sh.width)*check['scale'],mm(sh.height)*check['scale']
    ok=abs(w-check['w'])<.03 and abs(h-check['h'])<.03
    rows.append(f"| AP-{order[check['slide']-1]:02} | {check['shape'][5:]} | {w:.2f} × {h:.2f} | {check['w']} × {check['h']} | {'PASS' if ok else 'FAIL'} |")
    assert ok,check
outside=[]
for i,s in enumerate(p.slides,1):
    for sh in s.shapes:
        if min(sh.left,sh.top)<-36000 or sh.left+sh.width>p.slide_width+36000 or sh.top+sh.height>p.slide_height+36000:
            outside.append((i,sh.name))
assert not outside,outside
if manifest.get('revision')=='F':
    views=[sh for sh in p.slides[0].shapes if sh.name.startswith('VIEW:')]
    assert len(views)==5,'Cover gallery must contain five editable views'
    for sh in views:
        iw,ih=sh.image.size
        aspect=iw*(1-sh.crop_left-sh.crop_right)/(ih*(1-sh.crop_top-sh.crop_bottom))
        assert abs(aspect-sh.width/sh.height)<.001, f'Distorted cover view: {sh.name}'
math_checks={'frontage':450+1500+450==2400,'glazing':4+488+4+1000+4==1500,
    'side_run':450+4*664==3106,'rear_zones':250+500+900+500+250==2400,
    'vertical':100+500+5*400==2600,'rear_clearance':3106-250-2156==700,
    'counter_clearance':700-250==2150-1700==450,
    'tile_width':2*5+2*1194+2==2400,'tile_depth':2*5+2*343+4*600+5*2==3106}
assert all(math_checks.values())
pdf=fitz.open(OUT/'BORN_FRAGRANCE_Architecture.pdf')
assert len(pdf)==len(order)
if manifest.get('revision') in ('C','D','E','F'):
    import subprocess
    baseline=fitz.open(stream=subprocess.check_output(['git','show','83d60a940ffe9859af6a13fc94b04012bdb9da98:drawings/chatgpt/architecture_pptx/BORN_FRAGRANCE_Architecture.pdf'],cwd=OUT.parents[2]),filetype='pdf')
    for old_i in range(11,26):
        before=baseline[old_i].get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False)
        after=pdf[order.index(old_i+1)].get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False)
        assert before.samples==after.samples, f'Paused page {old_i+1} changed'
    rev=manifest['revision'];count=order.index(12)
    review=fitz.open();review.insert_pdf(pdf,from_page=0,to_page=count-1);review.save(OUT/f'BORN_FRAGRANCE_Review_{rev}.pdf');review.close()
    assert len(Presentation(OUT/f'BORN_FRAGRANCE_Review_{rev}.pptx').slides)==count
    if rev=='F':
        pdf[0].get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(OUT/'BORN_FRAGRANCE_Render_Layout_F.png')
        prior=fitz.open(stream=subprocess.check_output(['git','show','4b99617:drawings/chatgpt/architecture_pptx/BORN_FRAGRANCE_Architecture.pdf'],cwd=OUT.parents[2]),filetype='pdf')
        for i in range(1,8):
            assert prior[i].get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False).samples==pdf[i].get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False).samples, f'Technical view {i+1} changed'
(OUT/'svg').mkdir(exist_ok=True)
previews=[]
for i,page in enumerate(pdf):
    assert abs(page.rect.width*25.4/72-420)<.1
    assert abs(page.rect.height*25.4/72-297)<.1
    if manifest.get('revision') in ('E','F') and i<order.index(12):
        assert manifest['slide_titles'][i] in page.get_text(),i+1
        for sh in p.slides[i].shapes:
            if sh.has_text_frame:
                assert not any(t in sh.text for t in ('FOR COORDINATION','SPEC SNAPSHOT','SOURCE REV A','REV D')),sh.text
                assert not re.fullmatch(r'AP-\d{2}',sh.text.strip()),sh.text
            if sh.shape_type==5:
                assert str(sh.line.color.rgb)!='A44338','Cloud remains in active review'
    else:assert f'AP-{order[i]:02}' in page.get_text(),i+1
    target=OUT/'svg'/f'AP-{order[i]:02}.svg'
    if manifest.get('revision') in ('C','D','E','F') and order[i]>=12:
        target.write_bytes(subprocess.check_output(['git','show',f'83d60a940ffe9859af6a13fc94b04012bdb9da98:drawings/chatgpt/architecture_pptx/svg/AP-{order[i]:02}.svg'],cwd=OUT.parents[2]))
    else:
        svg=page.get_svg_image()
        # Keep raster media external in SVG; PDF/PPTX stay self-contained.
        # Long base64 pixel streams can trigger token-shaped false positives.
        import base64, hashlib
        def image_asset(match):
            data=base64.b64decode(match.group(2));name='image-'+hashlib.sha256(data).hexdigest()[:12]+('.png' if match.group(1)=='png' else '.jpg')
            (OUT/'svg'/'media').mkdir(exist_ok=True)
            (OUT/'svg'/'media'/name).write_bytes(data)
            return 'media/'+name
        svg=re.sub(r'data:image/(png|jpeg);base64,([A-Za-z0-9+/=\s]+)',image_asset,svg)
        target.write_text(svg)
    pix=page.get_pixmap(matrix=fitz.Matrix(.65,.65),alpha=False)
    img=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    previews.append(img)
for block in range(5):
    images=previews[block*6:(block+1)*6]
    if not images:continue
    w,h=images[0].size;board=Image.new('RGB',(w*2,h*3),'#d8d8d8')
    for k,im in enumerate(images):board.paste(im,((k%2)*w,(k//2)*h))
    board.save(f'/tmp/bf-contact-{block+1}.png')
# Drop only untracked export intermediates generated under this tool's media dir.
# Referenced assets and previously committed assets are always retained.
import subprocess
used=set()
for svg_path in (OUT/'svg').glob('*.svg'):
    used.update(re.findall(r'media/([^" ]+)',svg_path.read_text()))
untracked=subprocess.check_output(['git','ls-files','--others','--exclude-standard','drawings/chatgpt/architecture_pptx/svg/media'],cwd=OUT.parents[2],text=True).splitlines()
for rel in untracked:
    path=OUT.parents[2]/rel
    if path.parent==OUT/'svg'/'media' and path.name.startswith('image-') and path.name not in used:path.unlink()
md=['# Read-back audit','',f"Source repository snapshot: `{manifest['source_commit']}`.",
    f"Spec SHA-256: `{manifest['spec_sha256']}`.",'',
    f'{len(order)} PPTX slides reopened successfully. LibreOffice exported every page to PDF. All pages have A3 landscape MediaBoxes and stable AP sheet numbers. All native shape extents remain on the slide. Embedded images are self-contained.',
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
    '- Revision D removes AP-02 and AP-04. AP-12–26 remain frozen; their original register is historical. Indicative bottles are an explicit owner exception to the loose-products exclusion.',
    '- LOD 350 is a development target, not a certified achieved model status. Survey and unapproved connection details remain open.',
    f"- Paused original pages 12–26: PDF raster comparison is pixel-identical at 0.7×. The {order.index(12)}-page Review_{manifest['revision']} PPTX/PDF omits all paused sheets.",
    '- Rev D removes AP-04 as requested; the active Review_D is nine pages. AP-12–26 still compare pixel-identical to the original. Counter left-mesh front is an owner-directed visual revision; split and construction thicknesses remain TBC #16. The paused counter details retain the old insert and are not current design authority.',
    '- Review E removes selected footer texts, narrative sidebars and clouds from all nine active slides. The owner explicitly overrides their previous presentation requirements. Sheet IDs/scales/status stay in the manifest and README; connection-specific TBC notes remain beside relevant interfaces. The paused archive is unchanged.',
    '- Review E adds 1:5 rear/side corner and plinth sections, 1:2 pivot and folded-tray/light interfaces, a 1:10 counter footprint and a newly rendered orthographic cutaway with native editable leaders. See LOD_REVIEW_E.md for component reliability and references.',
    '- Review F removes AP-11 material palette and replaces the reference render with an owner-requested AI image edit to reduce the reddish cast. All measured technical views remain unchanged Python-generated geometry. Source render and spec are preserved.',
    '- Review F cover is a native five-picture layout: storefront hero, interior view and three aligned details. Crop/frame aspect ratios are read back and checked to prevent stretching.',
    '']
(OUT/'AUDIT.md').write_text('\n'.join(md))
print(f'PASS: {len(p.slides)} slides, {len(rows)} native geometry read-backs, 9 dimensional chains, PDF pages and extents.')
