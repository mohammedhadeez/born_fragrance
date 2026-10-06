"""Owner review F: remove palette page and replace render white balance."""
import io,json,subprocess
from pathlib import Path
from pptx import Presentation
from pptx.util import Mm,Pt
from pptx.dml.color import RGBColor
from PIL import Image
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
BASE='4b99617'
def old(name):return subprocess.check_output(['git','show',f'{BASE}:drawings/chatgpt/architecture_pptx/{name}'],cwd=ROOT)
p=Presentation(io.BytesIO(old('BORN_FRAGRANCE_Architecture.pptx')))
m=json.loads(old('geometry_manifest.json'))
frozen=[s._element.xml for s in list(p.slides)[9:]]
s=p.slides[0]
for sh in list(s.shapes):
    if sh.top/36000>50:s.shapes._spTree.remove(sh._element)
    elif sh.has_text_frame and 35<sh.top/36000<40:
        sh.text_frame.paragraphs[0].runs[0].text='Storefront, interior and display details · neutral material tones'
asset=OUT/'born-fragrance-shop-neutral.png'
imw,imh=Image.open(asset).size
gallery=[]
def view(name,bbox,frame):
    left,top,right,bottom=bbox;x,y,w,h=frame
    # Crop inside each original panel to fill a matching frame without stretching.
    ratio=w/h;bw,bh=right-left,bottom-top
    if bw/bh>ratio:
        trim=(bw-bh*ratio)/2;left+=trim;right-=trim
    else:
        trim=(bh-bw/ratio)/2;top+=trim;bottom-=trim
    pic=s.shapes.add_picture(str(asset),Mm(x),Mm(y),width=Mm(w),height=Mm(h))
    pic.name='VIEW:'+name
    pic.crop_left=left/imw;pic.crop_right=1-right/imw
    pic.crop_top=top/imh;pic.crop_bottom=1-bottom/imh
    assert abs((right-left)/(bottom-top)-ratio)<.001
    gallery.append({'name':pic.name,'frame_mm':frame,'crop_px':[left,top,right,bottom]})
def caption(x,y,w,text):
    box=s.shapes.add_textbox(Mm(x),Mm(y),Mm(w),Mm(7));tf=box.text_frame
    tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
    q=tf.paragraphs[0];q.text=text;q.font.name='Liberation Sans';q.font.size=Pt(8)
    q.font.bold=True;q.font.color.rgb=RGBColor.from_string('252725')
view('Storefront',(0,0,677,750),(17,58,185,205))
caption(17,269,185,'STOREFRONT / DESIGN INTENT')
view('Interior',(0,762,645,1162),(216,58,189,117))
caption(216,181,189,'INTERIOR / DISPLAY AND COUNTER')
for i,(name,bbox,text) in enumerate([
    ('Mesh and lighting',(687,0,1077,421),'MESH / LIGHT'),
    ('Display frame',(709,762,969,1162),'DISPLAY FRAME'),
    ('Plaster and shelf',(1052,762,1330,1162),'PLASTER / SHELF'),
]):
    x=216+i*(189+5)/3;w=(189-10)/3
    view(name,bbox,(x,199,w,72));caption(x,277,w,text)
assert frozen==[s._element.xml for s in list(p.slides)[9:]]
entry=p.slides._sldIdLst[8];p.part.drop_rel(entry.rId);p.slides._sldIdLst.remove(entry)
m['sheet_order'].remove(11);m['slide_titles'].pop(8)
for c in m['checks']:
    if c['slide']>9:c['slide']-=1
m['revision']='F';m['removed_sheet']='AP-02, AP-04, AP-11'
m['render_gallery']=gallery
m['review_source_commit']=subprocess.check_output(['git','rev-parse',BASE],cwd=ROOT,text=True).strip()
(OUT/'geometry_manifest.json').write_text(json.dumps(m,indent=2))
p.save(OUT/'BORN_FRAGRANCE_Architecture.pptx')
for entry in list(p.slides._sldIdLst)[8:]:p.part.drop_rel(entry.rId);p.slides._sldIdLst.remove(entry)
p.save(OUT/'BORN_FRAGRANCE_Review_F.pptx')
print('Revision F: eight review sheets; full archive 23; paused slides unchanged.')
