"""Orthographic architectural cutaway with depth-tested edges and anchors."""
import math, re, xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D
from matplotlib.colors import to_rgb

def render(root,spec,out):
    L,C=spec['locked'],spec['confirmed'];W=L['internal_size']['W'];D=L['internal_size']['D'];H=L['ceiling_height']
    faces=[];colors=[];strokes=[]
    def stroke(a,b,color='#78776D',width=.8):strokes.append((np.array(a),np.array(b),color,width))
    def box(x,y,z,w,d,h,color,edges=True):
        a=np.array([(x,y,z),(x+w,y,z),(x+w,y+d,z),(x,y+d,z),(x,y,z+h),(x+w,y,z+h),(x+w,y+d,z+h),(x,y+d,z+h)])
        for ids,shade in zip(((0,1,2,3),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)),(.90,.98,.90,.95,.91,1)):
            faces.append(a[list(ids)]);colors.append(np.array(to_rgb(color))*shade)
        if edges:
            for i,j in ((0,1),(0,3),(1,2),(2,3),(4,5),(4,7),(5,6),(6,7),(0,4),(1,5),(2,6),(3,7)):stroke(a[i],a[j])
    def bottle(x,y,z,j=0):
        # Owner-authorized indication of use; excluded from dimensions / counts.
        box(x,y,z,55,45,105,'#AAA394' if j%2 else '#575A53')
        box(x+14,y+10,z+105,27,25,18,'#393C36')
    box(0,0,-35,W,D,35,'#E8E2D5')
    # Surface planes do not assert a surveyed wall construction thickness.
    box(-2,0,0,2,D,H,'#F0EADB',False);box(0,D,0,W,2,H,'#F3EFE4',False)
    for y in (348,950,1552,2154,2756):stroke((0,y,.5),(W,y,.5),'#C9C5B9',.6)
    stroke((1200,0,.5),(1200,D,.5),'#C9C5B9',.6)
    for x in (0,2150):
        box(x,450,100,250,2656,500,'#DDD7CB')
        box(x+(50 if x==0 else 0),450,0,200,2656,100,'#585B53')
        for k in range(1,8):stroke((x+250 if x==0 else x,450+k*332,110),(x+250 if x==0 else x,450+k*332,580),'#99978B',.65)
        stroke((250 if x==0 else 2150,450,55),(250 if x==0 else 2150,D,55),'#C0A67A',1.4)
        if x==0:
            for k in range(5):
                y=450+(0 if k==0 else 2631 if k==4 else k*664-12.5)
                for xx in (0,225):box(xx,y,0,25,25,H,'#30352F')
            for z in C['units']['shelf_levels']:
                box(0,450,z,250,2656,3,'#3E443C')
                box(247,450,z-22,3,2656,25,'#30352F')
                stroke((250,465,z-12),(250,3090,z-12),'#C0A67A',1.4)
                for k in range(4):box(15,465+k*664,z-20,20,639,20,'#3A4037',False)
            for k in range(-200,2856,20):
                lo=max(0,k);hi=min(2656,k+200)
                if hi>lo:
                    stroke((251,450+lo,2200+2*(lo-k)),(251,450+hi,2200+2*(hi-k)),'#787B6B',.5)
                    stroke((251,450+lo,2600-2*(lo-k)),(251,450+hi,2600-2*(hi-k)),'#787B6B',.5)
            for k in range(4):
                for j,z in enumerate((600,1000,1400,1800)):
                    for q in (160,265):bottle(155,450+k*664+q,z+3,j+k)
        else:
            box(x,450,600,250,2656,3,'#EEE9DE')
            for k in range(5):
                y=450+(0 if k==0 else 2631 if k==4 else k*664-12.5)
                for xx in (x,x+225):box(xx,y,575,25,25,25,'#30352F')
    for x in (250,1650):
        box(x,2856,100,500,250,500,'#DDD7CB');box(x,2906,0,500,200,100,'#585B53')
        for xx in (x,x+475):box(xx,2856,0,25,25,H,'#30352F')
        for z in C['units']['shelf_levels']:
            box(x,2856,z,500,250,3,'#3E443C');box(x,2856,z-22,500,3,25,'#30352F')
            stroke((x+25,2855,z-12),(x+475,2855,z-12),'#C0A67A',1.2)
            if z<2200:
                for j,q in enumerate((90,200,310)):bottle(x+q,2880,z+3,j)
    # Both storefront columns cut at the same base datum to expose the entry.
    for x in (0,1950):
        box(x,0,0,450,450,600,'#DFD6C6')
        for xx in (x,x+425):box(xx,0,0,25,25,600,'#30352F')
        box(x+25,0,575,400,250,25,'#30352F')
    stroke((450,0,0),(1950,0,0),'#6C8A8D',1.2)
    # Owner counter-front direction; split / top thickness remain TBC.
    box(700,1706,0,1000,450,880,'#E0D4BD');box(700,1706,880,1000,450,20,'#F4EEE0')
    box(720,1703,55,330,3,805,'#A6A397')
    for xx in (700,1040,1680):box(xx,1702,20,20,4,860,'#30352F')
    box(700,1702,20,1000,4,20,'#30352F')
    for k in range(-402,350,20):
        lo=max(0,k);hi=min(330,k+402.5)
        if hi>lo:
            stroke((720+lo,1702,55+2*(lo-k)),(720+hi,1702,55+2*(hi-k)),'#4C5045',.5)
            stroke((720+lo,1702,860-2*(lo-k)),(720+hi,1702,860-2*(hi-k)),'#4C5045',.5)
    # Exploded ceiling layer: display translation, not a new ceiling height.
    display_offset=1000
    for x in C['lighting']['track_x']:
        box(x-8,450,H+display_offset-10,16,2206,10,'#434940')
        for y in (600,1200,1800,2400):box(x-22,y-40,H+display_offset-95,44,80,75,'#434940')
        for y in (450,2656):
            for z in range(H,H+display_offset,60):stroke((x,y,z),(x,y,min(z+24,H+display_offset)),'#B9B8AB',.5)
    az,el=map(math.radians,(-58,29))
    right=np.array([-math.sin(az),math.cos(az),0]);up=np.array([-math.cos(az)*math.sin(el),-math.sin(az)*math.sin(el),math.cos(el)])
    cam=np.array([math.cos(az)*math.cos(el),math.sin(az)*math.cos(el),math.sin(el)])
    vertices=np.concatenate(faces);uu=vertices@right;vv=vertices@up
    iw,ih=2560,2210;pad=80;scale=min((iw-2*pad)/(uu.max()-uu.min()),(ih-2*pad)/(vv.max()-vv.min()))
    def project(a):
        a=np.asarray(a);return np.stack([pad+(a@right-uu.min())*scale,pad+(vv.max()-a@up)*scale,a@cam],axis=-1)
    pixels=np.full((ih,iw,3),[252,251,247],dtype=np.uint8);depth=np.full((ih,iw),-np.inf)
    for face,col in zip(faces,colors):
        p=project(face)
        for ids in ((0,1,2),(0,2,3)):
            q=p[list(ids)];x0=max(0,int(q[:,0].min()));x1=min(iw,int(q[:,0].max())+1);y0=max(0,int(q[:,1].min()));y1=min(ih,int(q[:,1].max())+1)
            if x1<=x0 or y1<=y0:continue
            xx,yy=np.meshgrid(np.arange(x0,x1)+.5,np.arange(y0,y1)+.5);a,b,c=q
            den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-8:continue
            wa=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
            wb=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;wc=1-wa-wb
            z=wa*a[2]+wb*b[2]+wc*c[2];mask=(wa>=-1e-7)&(wb>=-1e-7)&(wc>=-1e-7)&(z>depth[y0:y1,x0:x1]-.0001)
            depth[y0:y1,x0:x1][mask]=z[mask];pixels[y0:y1,x0:x1][mask]=col*255
    for a,b,c,width in strokes:
        p=project([a,b]);n=max(2,int(np.linalg.norm(p[1,:2]-p[0,:2])*2));q=np.linspace(*p,n)
        for dx in range(-int(width/2),int(width/2)+1):
            xx=q[:,0].astype(int)+dx;yy=q[:,1].astype(int);ok=(xx>=0)&(xx<iw)&(yy>=0)&(yy<ih)
            xx=xx[ok];yy=yy[ok];zz=q[ok,2];visible=zz>=depth[yy,xx]-2
            pixels[yy[visible],xx[visible]]=np.array(to_rgb(c))*255
    # Project original vector logo onto the rear wall, preserving aspect ratio.
    svg=ET.parse(root/L['signage']['logo_asset']).getroot();d=svg.find('{http://www.w3.org/2000/svg}path').attrib['d']
    tok=re.findall(r'[MLCZmlcz]|[-+]?(?:\d*\.\d+|\d+)',d);verts=[];codes=[];i=0
    while i<len(tok):
        if tok[i] in ('M','L','C','Z','z'):cmd=tok[i];i+=1
        if cmd in ('M','L'):
            verts.append((float(tok[i]),float(tok[i+1])));codes.append(Path.MOVETO if cmd=='M' else Path.LINETO);i+=2
            if cmd=='M':cmd='L'
        elif cmd=='C':
            for j in range(3):verts.append((float(tok[i]),float(tok[i+1])));codes.append(Path.CURVE4);i+=2
        else:verts.append((0,0));codes.append(Path.CLOSEPOLY)
    path=Path(verts,codes);ratio=1419.5/643
    path=Affine2D().translate(-184,-128).scale(600/1419.5,-600/1419.5).translate(900,1900+300/ratio).transform_path(path)
    world=np.column_stack([path.vertices[:,0],np.full(len(path.vertices),D-1),path.vertices[:,1]])
    fig=plt.figure(figsize=(12.8,11.05),dpi=200);ax=fig.add_axes([0,0,1,1]);ax.imshow(pixels);ax.set_axis_off()
    ax.add_patch(PathPatch(Path(project(world)[:,:2],path.codes),facecolor='#363C33',edgecolor='none'))
    ax.set_xlim(0,iw);ax.set_ylim(ih,0);fig.savefig(out/'axonometric_revE.png',dpi=200,pad_inches=0);plt.close(fig)
    points={'mesh':(251,1950,2410),'tray':(250,1100,1400),'base':(251,1100,380),'entry':(225,100,600),
            'track':(1750,1800,H+display_offset-50),'logo':(1200,D-1,1900),'counter':(1430,1702,500),'cut':(2250,1250,600)}
    return {k:(project([v])[0,0]/iw,project([v])[0,1]/ih) for k,v in points.items()}
