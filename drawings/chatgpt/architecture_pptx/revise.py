"""Apply the five owner PDF comments; keep original AP-12 onward frozen."""
import io, json, math, subprocess, re, os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/bf-mpl')
OUT=Path(__file__).resolve().parent
BASE='83d60a940ffe9859af6a13fc94b04012bdb9da98'
ROOT=OUT.parents[2]
def old(path):return subprocess.check_output(['git','show',f'{BASE}:drawings/chatgpt/architecture_pptx/{path}'],cwd=ROOT)
# Reuse drafting primitives only, without executing the old sheet generator.
exec(compile((OUT/'build.py').read_text().split("s=sheet('Retail interior")[0],str(OUT/'build.py'),'exec'))
prs=Presentation(io.BytesIO(old('BORN_FRAGRANCE_Architecture.pptx')))
frozen=[s._element.xml for s in list(prs.slides)[11:]]
manifest=json.loads(old('geometry_manifest.json'))
def clean(i,subtitle):
    s=prs.slides[i-1]
    for sh in list(s.shapes):
        y=sh.top/36000
        if 49<y<272:s.shapes._spTree.remove(sh._element)
        elif sh.has_text_frame:
            if 35<y<40:sh.text_frame.paragraphs[0].runs[0].text=subtitle
            if 'REV B' in sh.text:sh.text_frame.paragraphs[0].runs[0].text=sh.text.replace('REV B','REV C')
    return s
def tag(s,x,y,n,color=INK):
    circle(s,x,y,3.3,color,PAPER);txt(s,x-2,y-1.6,5,5,n,8,color,bold=True)
def leadtag(s,v,x,y,u,z,n):
    a,b=v.p(x,y);line(s,a,b,u-4,z,GREY,.55);tag(s,u,z,n)
def tinybottle(v,x,z,style=0):
    # Indicative symbols only: never dimensions, schedules or quantities.
    widths=[50,62,44];heights=[95,120,105];w=widths[style%3];h=heights[style%3]
    v.r(x,z,w,h,None,'AAA79F');v.r(x+w*.27,z+h,w*.46,18,'AAA79F','AAA79F')
    v.l(x+8,z+h*.42,x+w-8,z+h*.42,'C8C4BC',.25)

# AP-03: lineweight hierarchy, footprint interfaces, setting-out and named leaders.
s=clean(3,'Setting-out / coordinated interfaces · 1:20 · finish-face dimensions; site verification pending')
notes(s,[('01 / FRAME + SETTING-OUT','250 deep side units. Four 664 modules from y=450 to 3106. 25 main uprights shown; shelf/support lines distinguished.'),('02 / COUNTER + REAR','1000 × 450 counter; x=700–1700, y=1706–2156. 700 to rear-unit face. Side routes remain 450 / 450.'),('03 / GLAZED ENTRANCE','488 fixed pane + 1000 pivot leaf + three 4 gaps = 1500. Pivot 100 from right edge; inward sweep shown.'),('04 / COORDINATION STATUS','LOD 350 development target: interfaces shown, not certified complete. Anchors, hardware, substrate and access remain TBC #16/#26.')])
v=View(s, 90,238,20)
# Graphic wall cut bands are not dimensioned construction thicknesses.
rect(s,87.5,238-D/20,2.5,D/20,'777970','777970')
rect(s,210,238-D/20,2.5,D/20,'777970','777970')
rect(s,87.5,235.5-D/20,125,2.5,'777970','777970')
v.r(0,0,W,D,'F5F1E9',name='internal-envelope')
for y in (348,950,1552,2154,2756):v.l(0,y,W,y,'DDD8CE',.25)
v.l(1200,0,1200,D,'DDD8CE',.25)
unitplan(v)
for x in (0,2150):
    v.r(x+25,475,200,2606,None,'A6A195')
    for y in (450,1101.5,1765.5,2429.5,3081):
        for xx in (x,x+225):v.r(xx,y,25,25,INK)
    v.l(x+225,450,x+225,D,GOLD,.55,True)
for x in (250,1650):v.r(x+25,2881,450,200,None,GREY)
v.r(700,1706,1000,450,'D6CEC0',name='counter-plan');v.r(720,1726,960,410,None,GREY)
v.l(720,2116,1680,2116,GREY,.5,True)
v.l(1200,1550,1200,2330,GREY,.45,True)
v.l(454,0,942,0,BLUE,1.6);v.l(946,0,1946,0,BLUE,1.6)
v.l(454,12,942,12,BLUE,.5);v.l(946,12,1946,12,BLUE,.5)
px=1846
for radius in (900,100):
    prev=(px-radius,0) if radius==900 else (px+radius,0)
    for j in range(1,33):
        t=j*math.pi/64;pt=(px-radius*math.cos(t),radius*math.sin(t)) if radius==900 else (px+radius*math.cos(t),-radius*math.sin(t))
        v.l(*prev,*pt,BLUE,.45,True);prev=pt
v.l(px,-100,px,900,BLUE,1);a,b=v.p(px,0);circle(s,a,b,1,BLUE,PAPER)
v.dim(0,0,W,0,22);v.dim(0,0,450,0,10);v.dim(450,0,1950,0,10);v.dim(1950,0,W,0,10)
v.dim(0,0,0,D,-26)
for y0,y1 in [(0,450),(450,1114),(1114,1778),(1778,2442),(2442,3106)]:v.dim(0,y0,0,y1,-12)
v.dim(0,D,250,D,-7);v.dim(250,D,2150,D,-7);v.dim(2150,D,W,D,-7)
v.dim(250,1706,700,1706,8);v.dim(1700,1706,2150,1706,8);v.dim(1700,2156,1700,2856,10)
for x,y,n in [(0,0,'A'),(W,0,'B'),(W,D,'C'),(0,D,'D')]:
    a,b=v.p(x,y);circle(s,a,b,1.3,INK,PAPER);txt(s,a+2,b-5,8,6,n,8,bold=True)
leadtag(s,v,225,1800, 50,137,'01');leadtag(s,v,1300,1900,248,140,'02');leadtag(s,v,1846,0,248,233,'03')
txt(s,22, 60, 60,10,'SET-OUT DATUMS',9,GOLD,bold=True)
txt(s,22,72, 60,43,'A  0 / 0\nB  2400 / 0\nC  2400 / 3106\nD  0 / 3106',9)
cloud(s,226,166,58,35,'#16\n450 side routes\nAccess / escape unresolved')
txt(s,226, 80,58,24,'N ↓ STOREFRONT\nASSUMED #23',8,RED)
txt(s,22,208,62,25,'Wall bands graphic only\nThickness TBC #26\nEnvelope TBC #4',8,RED)
v.bar(0,-580,1000)

# AP-08 / AP-09: accurately sized steel members, mesh, trays, lights and sparse props.
for i,reverse in [(8,False),(9,True)]:
    s=clean(i,'Developed display elevation · interfaces + material codes · bottles indicative only')
    notes(s,[('01 / STEEL FRAME','25 × 25 × 1.6 main SHS; 20 × 20 × 1.6 secondary supports. 664 module is not a fabrication cut size.'),('02 / SHELF + LIGHT','3 mm tray / 25 downstand / 250 depth. Concealed 3000 K LED behind front edge; see section inset.'),('03 / BASE + MESH','600 base includes 100 recessed plinth. 1.5 PPC doors. Mesh at 2200–2600; approximate 20 × 40 diamonds.'),('04 / INDICATIVE CONTENT','Sparse fragrance bottles added at owner request for visual scale only. Excluded from dimensions and schedules. Fixings and cable routing #16 remain open.')])
    v=View(s,51,222,20);v.r(0,0,D,H,'F1EBE0',name='side-envelope')
    start=0 if reverse else 450;end=start+2656;col=2656 if reverse else 0
    v.r(col,0,450,H,'DDD5C6');v.r(col+25,25,400,2550,None,GREY)
    for z in C['units']['shelf_levels']:v.l(col+25,z,col+425,z,GREY,.5)
    v.r(start,0,2656,100,'51534E');v.r(start,100,2656,500,'DED8CD')
    v.r(start,2200,2656,400,'D3CCBD')
    # Nominal mesh pitch at correct geometry; thin lines remain subordinate.
    for k in range(-200,2857,20):
        xa=max(0,k);xb=min(2656,k+200)
        if xb>xa:
            v.l(start+xa,2200+(xa-k)*2,start+xb,2200+(xb-k)*2,'878478',.15)
            v.l(start+xa,2600-(xa-k)*2,start+xb,2600-(xb-k)*2,'878478',.15)
    for k in range(5):
        p=start+(0 if k==0 else 2656-25 if k==4 else k*664-12.5)
        v.r(p,0,25,2600,INK)
    for z in C['units']['shelf_levels']:
        v.r(start,z-25,2656,25,INK);v.l(start+25,z-22,end-25,z-22,GOLD,.65)
    for k in range(4):
        x=start+k*664
        v.l(x+332,110,x+332,575,'B7B0A2',.35);v.l(x+290,555,x+375,555,INK,.65)
        for j,z in enumerate((600,1000,1400,1800)):
            if (k+j)%2==0:
                tinybottle(v,x+150,z+3,j);tinybottle(v,x+245,z+3,j+1)
    v.l(start+25,55,end-25,55,GOLD,1)
    v.dim(0,0,D,0,17);v.dim(0,0,0,H,-15)
    for k in range(4):v.dim(start+k*664,0,start+(k+1)*664,0,8)
    for z0,z1 in [(0,100),(100,600),(600,1000),(1000,1400),(1400,1800),(1800,2200),(2200,2600)]:v.dim(D,z0,D,z1,9)
    leadtag(s,v,start+1328,2400,270,96,'03');leadtag(s,v,start+1900,1390,270,139,'02');leadtag(s,v,start+1328,150,270,209,'01')
    txt(s,22, 61,260,9,'M01 / BLACK STEEL    M02 / NEUTRAL PPC    M05 / MESH    L03 / 3000 K LED',8,GOLD)
    # Section inset uses only the approved depth and steel sizes.
    u=View(s,234,185,5);u.r(0,0,250,3,INK);u.r(247,-22,3,25,INK);u.r(15,-20,20,20,None,INK)
    u.dim(0,3,250,3,-6);txt(s,234,192,53,8,'SHELF SECTION 1:5',7,GREY)
    v.bar(0,-700,1000)
    txt(s,117,249,170,12,'INDICATIVE BOTTLES · NOT A STOCK / CAPACITY SCHEDULE',7.5,GREY)

# AP-10: shaded 3D cutaway from approved geometry, not a traced render.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, pathpatch_2d_to_3d
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MPath
from matplotlib.transforms import Affine2D
import xml.etree.ElementTree as ET
fig=plt.figure(figsize=(11,9),dpi=220,facecolor='#FCFBF7');ax=fig.add_subplot(111,projection='3d',computed_zorder=False)
ax.set_proj_type('ortho');ax.view_init(elev=27,azim=-58);ax.set_box_aspect((2400,3106,2800));ax.set_axis_off();ax.set_facecolor('#FCFBF7')
allfaces=[];facecolors=[];edgecolors=[];widths=[]
from matplotlib.colors import to_rgb
def box(x,y,z,w,d,h,c,edge='#45443E',lw=.22):
    a=[(x,y,z),(x+w,y,z),(x+w,y+d,z),(x,y+d,z),(x,y,z+h),(x+w,y,z+h),(x+w,y+d,z+h),(x,y+d,z+h)]
    faces=[[a[k] for k in f] for f in [(0,1,2,3),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]]
    # Tessellate exposed faces so depth sorting cannot hide long posts/shelves.
    import numpy as np
    for face,shade in zip(faces,(.80,.93,.84,.90,.88,1)):
        p0,p1,p2,p3=map(np.array,face);u=p1-p0;v=p3-p0
        nu=max(1,math.ceil(np.linalg.norm(u)/125));nv=max(1,math.ceil(np.linalg.norm(v)/125))
        for i in range(nu):
            for j in range(nv):
                allfaces.append([p0+u*a+v*b for a,b in [(i/nu,j/nv),((i+1)/nu,j/nv),((i+1)/nu,(j+1)/nv),(i/nu,(j+1)/nv)]])
                facecolors.append(tuple(v*shade for v in to_rgb(c)));edgecolors.append('none');widths.append(0)
for x in range(0,W,400):
    for y in range(0,D,400):box(x,y,-35,min(400,W-x),min(400,D-y),35,'#C7BFB0',edge='#C7BFB0',lw=0)
for x in range(0,W,400):
    for z in range(0,H,400):box(x,3106,z,min(400,W-x),18,min(400,H-z),'#E8DDC9',edge='#E8DDC9',lw=0)
for y in range(0,D,400):
    for z in range(0,H,400):box(-18,y,z,18,min(400,D-y),min(400,H-z),'#E4D7C0',edge='#E4D7C0',lw=0)
for y in (348,950,1552,2154,2756):box(0,y,0,W,2,1,'#EEE8DB')
box(1199,0,0,2,D,1,'#EEE8DB')
for x in (0,2150):
    # Near-side upper structure removed to expose room; base footprint stays exact.
    full=x==0;top=2600 if full else 600
    box(x,450,100,250,2656,500,'#D3CBBE')
    box(x+50,450,0,200,2656,100,'#393A36')
    for k in range(5):
        y=450+(0 if k==0 else 2631 if k==4 else k*664-12.5)
        for xx in (x,x+225):box(xx,y,0,25,25,top,'#242725')
    if full:
        for z in C['units']['shelf_levels']:
            box(x,450,z-25,250,2656,25,'#292B28');box(x+250,465,z-23,2,2626,5,'#EBC378',edge='#EBC378')
        for y in range(450,3106,40):
            ax.plot([250,250],[y,min(y+200,3106)],[2200,2600],color='#30312B',lw=.6)
            ax.plot([250,250],[y,min(y+200,3106)],[2600,2200],color='#30312B',lw=.6)
        for k in range(4):
            for j,z in enumerate((600,1000,1400,1800)):
                if (k+j)%2==0:
                    for q in (180,275):
                        box(95,450+k*664+q,z+3,55, 50,105,'#776F5D',lw=.15)
                        box(108,463+k*664+q,z+108,29,24,18,'#292B28',lw=.1)
for x in (250,1650):
    box(x,2856,100,500,250,500,'#D3CBBE')
    for xx in (x,x+475):box(xx,2856,0,25,25,2600,'#242725')
    for z in C['units']['shelf_levels']:box(x,2856,z-25,500,250,25,'#282B28')
box(700,1706,0,1000,450,880,'#D4C6AF');box(700,1706,880,1000,450,20,'#ECE5D7')
box(1050,1704,150,300,2,450,'#494941')
for x in (0,1950):
    top=2600 if x==0 else 900
    box(x,0,0,450,450,top,'#C9BDA5')
    for xx in (x,x+425):box(xx,0,0,25,450,top,'#292C29')
    for z in (600,1000,1400,1800,2200):
        if z<top:box(x+25,0,z-25,400,250,25,'#272A27')
# Original logo paths projected onto the rear wall, preserving geometry and ratio.
svg=ET.parse(ROOT/L['signage']['logo_asset']).getroot();d=svg.find('{http://www.w3.org/2000/svg}path').attrib['d']
tok=re.findall(r'[MLCZmlcz]|[-+]?(?:\d*\.\d+|\d+)',d);verts=[];codes=[];i=0
while i<len(tok):
    if tok[i] in ('M','L','C','Z','z'):
        cmd=tok[i];i+=1
    if cmd in ('M','L'):
        verts.append((float(tok[i]),float(tok[i+1])));codes.append(MPath.MOVETO if cmd=='M' else MPath.LINETO);i+=2
        if cmd=='M':cmd='L'
    elif cmd=='C':
        for k in range(3):verts.append((float(tok[i]),float(tok[i+1])));codes.append(MPath.CURVE4);i+=2
    elif cmd in ('Z','z'):verts.append((0,0));codes.append(MPath.CLOSEPOLY)
    else:raise ValueError(cmd)
path=MPath(verts,codes);t=Affine2D().translate(-184,-128).scale(600/1419.5,-600/1419.5).translate(900,1900+300/ratio)
patch=PathPatch(t.transform_path(path),facecolor='#252725',edgecolor='none');ax.add_patch(patch);pathpatch_2d_to_3d(patch,z=3100,zdir='y')
ax.add_collection3d(Poly3DCollection(allfaces,facecolors=facecolors,edgecolors=edgecolors,linewidths=widths,zsort='average',zorder=1,antialiased=False))
patch.set_zorder(5)
ax.set_xlim(-100,2600);ax.set_ylim(-100,3250);ax.set_zlim(-50,2850);fig.subplots_adjust(0,0,1,1)
# Orthographic software depth buffer: intersecting joinery needs per-pixel depth,
# not Matplotlib's painter ordering of large transparent display collections.
import numpy as np
from PIL import Image
az,el=map(math.radians,(-58,27))
right=np.array([-math.sin(az),math.cos(az),0]);up=np.array([-math.cos(az)*math.sin(el),-math.sin(az)*math.sin(el),math.cos(el)])
cam=np.array([math.cos(az)*math.cos(el),math.sin(az)*math.cos(el),math.sin(el)])
verts3=np.concatenate([np.asarray(f) for f in allfaces]);uu=verts3@right;vv=verts3@up
iw,ih=2200,1900;factor=min((iw-180)/(uu.max()-uu.min()),(ih-180)/(vv.max()-vv.min()))
def project(a):
    a=np.asarray(a);return np.stack([90+(a@right-uu.min())*factor,90+(vv.max()-a@up)*factor,a@cam],axis=-1)
pixels=np.full((ih,iw,3),[252,251,247],dtype=np.uint8);depth=np.full((ih,iw),-np.inf)
for f,col in zip(allfaces,facecolors):
    p=project(f)
    for ids in ((0,1,2),(0,2,3)):
        q=p[list(ids)];x0=max(0,int(q[:,0].min()));x1=min(iw,int(q[:,0].max())+1);y0=max(0,int(q[:,1].min()));y1=min(ih,int(q[:,1].max())+1)
        if x1<=x0 or y1<=y0:continue
        xx,yy=np.meshgrid(np.arange(x0,x1)+.5,np.arange(y0,y1)+.5)
        a,b,c=q;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(den)<1e-9:continue
        wa=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
        wb=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;wc=1-wa-wb
        z=wa*a[2]+wb*b[2]+wc*c[2];mask=(wa>=-1e-7)&(wb>=-1e-7)&(wc>=-1e-7)&(z>depth[y0:y1,x0:x1]-0.0001)
        depth[y0:y1,x0:x1][mask]=z[mask];pixels[y0:y1,x0:x1][mask]=np.array(col)*255
for ln in ax.lines:
    pts=project(np.array(ln.get_data_3d()).T)
    for a,b in zip(pts[:-1],pts[1:]):
        n=max(2,int(np.linalg.norm(b[:2]-a[:2])*2))
        q=np.linspace(a,b,n);xx=q[:,0].astype(int);yy=q[:,1].astype(int)
        valid=(xx>=0)&(xx<iw)&(yy>=0)&(yy<ih);xx=xx[valid];yy=yy[valid];zz=q[valid,2]
        visible=zz>=depth[yy,xx]-2;pixels[yy[visible],xx[visible]]=[45,47,42]
plt.close(fig)
# Vector logo lies on the visible central rear panel; no redrawing of the asset.
f2=plt.figure(figsize=(11,9.5),dpi=200);a2=f2.add_axes([0,0,1,1]);a2.imshow(pixels);a2.set_axis_off()
lp=t.transform_path(path);world=np.column_stack([lp.vertices[:,0],np.full(len(lp.vertices),3100),lp.vertices[:,1]])
lp2=MPath(project(world)[:,:2],lp.codes);a2.add_patch(PathPatch(lp2,facecolor='#252725',edgecolor='none'))
a2.set_xlim(0,iw);a2.set_ylim(ih,0);f2.savefig(OUT/'axonometric_revC.png',dpi=200,pad_inches=0);plt.close(f2)
s=clean(10,'Shaded cutaway / approved geometry + render material language · near wall and ceiling removed')
notes(s,[('01 / SPATIAL CHARACTER','Warm plaster, black frames, mesh, neutral cabinetry and warm shelf lighting follow the reference render.'),('02 / GEOMETRIC BASIS','2400 × 3106 × 2600 envelope. Four 664 modules; centred 1000 × 450 counter; 500 / 900 / 500 rear zones.'),('03 / CUTAWAY','Near-side upper units and ceiling removed to expose the room. Their full extent remains on the plans and elevations.'),('04 / ACCURACY LIMIT','Visual fidelity target, not a measurable 80% certification. Approved dimensions override the render. Bottles are indicative; hardware and fixings remain TBC.')])
s.shapes.add_picture(str(OUT/'axonometric_revC.png'),Mm(22),Mm(51),width=Mm(245),height=Mm(245*9.5/11))
txt(s,24,257,255,10,'CUTAWAY AXONOMETRIC · NTS · ceiling and near-side upper joinery omitted',8,GREY)

# Suppress theme effects only on changed sheets.
for i in (3,8,9,10):
    for sh in prs.slides[i-1].shapes:
        style=sh._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
        if style is not None:sh._element.remove(style)
        sppr=sh._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}spPr')
        if sppr is not None:sppr.append(OxmlElement('a:effectLst'))
assert frozen==[s._element.xml for s in list(prs.slides)[11:]],'Paused sheets changed'
# Remove original AP-02; preserve stable drawing numbers and frozen register.
entry=prs.slides._sldIdLst[1];prs.part.drop_rel(entry.rId);prs.slides._sldIdLst.remove(entry)
prs.save(OUT/'BORN_FRAGRANCE_Architecture.pptx')
for entry in list(prs.slides._sldIdLst)[10:]:
    prs.part.drop_rel(entry.rId);prs.slides._sldIdLst.remove(entry)
prs.save(OUT/'BORN_FRAGRANCE_Review_C.pptx')
manifest['revision']='C';manifest['removed_sheet']='AP-02';manifest['frozen_sheets']='AP-12 to AP-26'
manifest['sheet_order']=[1]+list(range(3,27))
manifest['checks']=[dict(c,slide=c['slide']-1 if c['slide']>2 else c['slide']) for c in manifest['checks']]
(OUT/'geometry_manifest.json').write_text(json.dumps(manifest,indent=2))
print('Rev C: 25 slides; AP-02 removed; AP-03/08/09/10 revised; AP-12–26 XML unchanged.')
