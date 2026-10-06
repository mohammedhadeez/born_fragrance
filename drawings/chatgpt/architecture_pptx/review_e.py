"""Owner review E: drawing-led layout and enlarged coordination interfaces."""
import io, json, subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
BASE_D='8d176ad8f12c98729205d55a98d00aba001f485b'
exec(compile((OUT/'build.py').read_text().split("s=sheet('Retail interior")[0],str(OUT/'build.py'),'exec'))
def old(name):return subprocess.check_output(['git','show',f'{BASE_D}:drawings/chatgpt/architecture_pptx/{name}'],cwd=ROOT)
prs=Presentation(io.BytesIO(old('BORN_FRAGRANCE_Architecture.pptx')))
manifest=json.loads(old('geometry_manifest.json'))
frozen=[s._element.xml for s in list(prs.slides)[9:]]
def delete(s,sh):s.shapes._spTree.remove(sh._element)
def color(sh):
    try:return str(sh.line.color.rgb)
    except (AttributeError,TypeError):return None
for s in list(prs.slides)[:9]:
    clouds=[(sh.left/36000,sh.top/36000,sh.width/36000,sh.height/36000) for sh in s.shapes if sh.shape_type==5 and color(sh)==RED]
    for sh in list(s.shapes):
        x,y,w,h=[n/36000 for n in (sh.left,sh.top,sh.width,sh.height)]
        incloud=any(cx-2<=x<=cx+cw+2 and cy-2<=y<=cy+ch+2 for cx,cy,cw,ch in clouds)
        if y>=277 or (x>=300 and 50<y<271) or (abs(x-293)<.1 and y>50) or (abs(y-272)<.1 and w>300) or incloud:delete(s,sh)
    for sh in s.shapes:
        style=sh._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
        if style is not None:sh._element.remove(style)
def title(s,y,a,b,x=300,w=105):
    txt(s,x,y,w,8,a,10,bold=True);txt(s,x,y+8,w,10,b,8,GREY)
def elbow(s,point,x,y,label,body='',side='right',w=67):
    px,py=point;end=x-3 if side=='right' else x+w+3;corner=end-5 if side=='right' else end+5
    line(s,px,py,corner,y+3,GREY,.5);line(s,corner,y+3,end,y+3,GREY,.5);circle(s,px,py,.55,GREY,GREY)
    txt(s,x,y,w,7,label,9,bold=True)
    if body:txt(s,x,y+7,w,17,body,8,GREY)
def shs(v,x,y,size=25):
    v.r(x,y,size,size,INK);v.r(x+1.6,y+1.6,size-3.2,size-3.2,PAPER)
def shelf(s,x,y,named=False):
    u=View(s,x,y,2);u.r(0,0,250,3,INK,name='active-tray' if named else None);u.r(247,-22,3,25,INK)
    u.r(15,-20,20,20,INK,name='active-support' if named else None);u.r(16.6,-18.4,16.8,16.8,PAPER)
    u.l(230,-10,245,-10,GOLD,1.3);u.dim(0,3,250,3,-9)
    txt(s,x,y+16,125,20,'3 mm folded tray · 25 front downstand\n20 × 20 × 1.6 support · LED profile TBC #16',8,GREY)

# Overall plan: reinforce member footprints and add genuine corner/pivot views.
s=prs.slides[1];v=View(s,90,238,20)
for x in (0,2150):
    for j in range(5):
        y=450+(0 if j==0 else 2631 if j==4 else j*664-12.5)
        for xx in (x,x+225):shs(v,xx,y)
for x in (250,1650):
    for xx in (x,x+475):shs(v,xx,2856);shs(v,xx,3081)
title(s,57,'REAR / SIDE JUNCTION','LOCAL PLAN 1:5')
u=View(s,300,179,5)
u.r(0,0,250,500,'E5DECF');u.r(250,250,250,250,'E5DECF')
for x,y in ((0,475),(225,475),(250,250),(250,475)):shs(u,x,y)
u.l(225,0,225,475,GOLD,.8,True);u.l(275,250,500,250,GOLD,.8,True)
u.dim(0,0,250,0,7);u.dim(250,500,500,500,-7);u.dim(500,250,500,500,7)
txt(s,300,190,105,19,'25 × 25 × 1.6 SHS / 250-deep units\nRear bay continues right; no overlap',8,GREY)
line(s,398,128,402,132,INK,.6);line(s,398,131,402,135,INK,.6)
title(s,217,'DOOR EDGE / PIVOT','LOCAL PLAN 1:2')
u=View(s,310,269,2);u.r(0,0,150,12,None,BLUE);shs(u,154,0)
u.l(50,-10,50,55,GREY,.5,True);a,b=u.p(50,6);circle(s,a,b,1.5,BLUE)
u.dim(50,12,150,12,-9);u.dim(150,0,154,0,7)
txt(s,300,282,105,8,'12 glass / 4 gap / 25 SHS · pivot fittings TBC #16',8,GREY)

# Reflected ceiling: show unit-to-ceiling interface and full-size tray section.
s=prs.slides[2]
title(s,57,'UNIT HEAD / CEILING','SECTION 1:5')
u=View(s,310,165,5)
u.r(0,0,25,400,INK);u.r(1.6,0,21.8,375,PAPER)
u.r(225,0,25,400,INK);u.r(226.6,0,21.8,375,PAPER)
u.r(0,375,250,25,INK);u.r(25,376.6,200,21.8,PAPER)
u.r(0,0,250,3,INK);u.r(247,-22,3,25,INK);u.r(15,-20,20,20,INK);u.r(16.6,-18.4,16.8,16.8,PAPER)
u.l(-15,400,285,400,GREY,.5)
for z in range(0,380,40):u.l(237,z,237,z+20,'AAA79F',.4)
u.dim(0,400,250,400,-9);u.dim(250,0,250,400,9)
txt(s,300,180,105,23,'2600 ceiling / frame datum\nMesh zone 2200–2600 at front\nWall fixings TBC #16; no gypsum fixing',8,GREY)
title(s,220,'FOLDED TRAY / LIGHT','SECTION 1:2',284,126);shelf(s,284,260,True)

# Side elevations: larger tray section and a properly drawn plinth recess.
for pos in (5,6):
    s=prs.slides[pos]
    for sh in list(s.shapes):
        x,y=[n/36000 for n in (sh.left,sh.top)]
        if 230<=x<289 and 171<y<216:delete(s,sh)
    title(s,65,'SHELF / FRONT EDGE','SECTION 1:2',284,126);shelf(s,284,114)
    title(s,177,'CABINET / PLINTH','SECTION 1:5',305,100)
    u=View(s,315,264,5);u.r(0,100,250,260,'DED8CD');u.r(0,0,200,100,'51534E')
    u.l(200,60,245,60,GOLD,1);u.dim(200,0,250,0,8);u.dim(250,0,250,100,8)
    txt(s,305,281,105,9,'100 high · 50 recess · warm toe-kick LED',8,GREY)

s=prs.slides[3];v=View(s,65,237,20)
elbow(s,v.p(1950,2400),302,83,'BLACK SHS FRAME','25 × 25 × 1.6 main steel',w=103)
title(s,165,'HALO LETTER / BACKING','STAND-OFF SECTION 1:2',303,103)
u=View(s,310,234,2);u.l(0,0,0,75,GREY,.6);u.l(25,0,25,75,INK,1.5);u.l(0,35,25,35,INK,.6);u.dim(0,75,25,75,-8)
txt(s,303,247,103,26,'25 stand-off · halo behind black letters\nBacking / wall support / drivers TBC #16',8,GREY)
s=prs.slides[4];v=View(s,65,222,20)
elbow(s,v.p(720,450),206,202,'COUNTER MESH / SOLID','Owner render direction\nPanel split / top thickness TBC #16',w=75)
title(s,64,'REAR SHELF / FRAME','SECTION 1:2',284,126);shelf(s,284,121)
title(s,194,'COUNTER / FOOTPRINT','PLAN 1:10',302,103)
u=View(s,302,263,10);u.r(0,0,1000,450,'D7CBB8',name='active-counter-detail')
for x in (0,980):
    for y in (0,430):u.r(x,y,20,20,INK)
u.dim(0,450,1000,450,-8);u.dim(1000,0,1000,450,4)
txt(s,302,279,103,12,'20 × 20 frame · front split TBC #16',8,GREY)

s=prs.slides[0]
for sh in list(s.shapes):
    if sh.shape_type==13 and sh.top/36000>50:
        sh.left=Mm(85);sh.top=Mm(54);sh.height=Mm(217);sh.width=Mm(217*1341/1173)
    elif sh.has_text_frame and 'REFERENCE RENDER' in sh.text:delete(s,sh)
txt(s,85,280,250,8,'REFERENCE RENDER · DESIGN INTENT',8,GREY)

from axon_e import render
anchors=render(ROOT,SPEC,OUT)
s=prs.slides[7]
for sh in list(s.shapes):
    if 49<sh.top/36000<277:delete(s,sh)
    elif sh.has_text_frame and 35<sh.top/36000<40:sh.text_frame.paragraphs[0].runs[0].text='Spatial cutaway · orthographic projection · direct material and interface annotations'
ix,iy,iw,ih=81,57,256,221
s.shapes.add_picture(str(OUT/'axonometric_revE.png'),Mm(ix),Mm(iy),width=Mm(iw),height=Mm(ih))
def anchor(name):
    x,y=anchors[name];return ix+x*iw,iy+y*ih
for key,x,y,a,b,side,w in [
    ('mesh',19,70,'EXPANDED MESH','Upper infill 2200–2600\nApprox. 20 × 40 diamonds','left',62),
    ('tray',19,122,'BLACK STEEL TRAYS','250 depth · 3 mm steel\n25 folded front downstand','left',62),
    ('base',19,178,'NEUTRAL BASE DOORS','1.5 mm PPC steel\n600 base incl. 100 plinth','left',62),
    ('entry',19,234,'STREET DISPLAY CUT','Upper column removed\n1500 clear entrance','left',62),
    ('track',344,62,'CEILING TRACKS','Exploded above room\nInstalled at 2600 · 3000 K\nTwo tracks / four spots each','right',62),
    ('logo',344,114,'REAR BRAND WALL','Raw light plaster\n600-wide unlit native logo','right',62),
    ('counter',344,175,'COUNTER','1000 × 450 × 900\nMesh left / neutral panel right','right',62),
    ('cut',344,233,'NEAR-SIDE CUTAWAY','Upper joinery omitted at 600\nFull run shown in elevations','right',62),
]:elbow(s,anchor(key),x,y,a,b,side,w)
txt(s,137,282,203,8,'ORTHOGRAPHIC CUTAWAY · NTS · ceiling plane removed',8,GREY)
for slide in list(prs.slides)[:9]:
    for sh in list(slide.shapes):
        if sh.has_text_frame and sh.text.startswith('3 mm tray · 25 downstand'):delete(slide,sh);continue
        style=sh._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
        if style is not None:sh._element.remove(style)
        sppr=sh._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}spPr')
        if sppr is not None:
            for effect in list(sppr.findall('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')):sppr.remove(effect)
            sppr.append(OxmlElement('a:effectLst'))
assert frozen==[s._element.xml for s in list(prs.slides)[9:]],'Paused slides changed'
manifest['revision']='E';manifest['review_source_commit']=BASE_D
manifest['checks'] += [
    {'slide':3,'shape':'GEOM:active-tray','w':250,'h':3,'scale':2},
    {'slide':3,'shape':'GEOM:active-support','w':20,'h':20,'scale':2},
    {'slide':5,'shape':'GEOM:active-counter-detail','w':1000,'h':450,'scale':10},
]
manifest['slide_titles']=[next(sh.text for sh in s.shapes if sh.has_text_frame and 19<sh.top/36000<25) for s in prs.slides]
(OUT/'geometry_manifest.json').write_text(json.dumps(manifest,indent=2))
prs.save(OUT/'BORN_FRAGRANCE_Architecture.pptx')
for entry in list(prs.slides._sldIdLst)[9:]:prs.part.drop_rel(entry.rId);prs.slides._sldIdLst.remove(entry)
prs.save(OUT/'BORN_FRAGRANCE_Review_E.pptx')
print('Review E: nine sheets; full deck 24; paused slide XML preserved.')
