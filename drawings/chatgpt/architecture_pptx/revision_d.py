"""Owner review D: direct annotation and developed active elevations.

Executed in revise.py's drafting namespace. No source specification is edited.
Counter split is a visual proposal, not a fabricated dimension from the render.
"""
def mesh(v,x,z,w,h):
    v.r(x,z,w,h,'B6AD9A')
    for k in range(-int(h/2),int(w)+20,20):
        lo=max(0,k);hi=min(w,k+h/2)
        if hi>lo:
            v.l(x+lo,z+2*(lo-k),x+hi,z+2*(hi-k),'6C6B61',.18)
            v.l(x+lo,z+h-2*(lo-k),x+hi,z+h-2*(hi-k),'6C6B61',.18)

def display(v,x,w,base=True,uppermesh=False):
    v.r(x,0,w,H,'E8DFCF')
    if base:
        v.r(x,0,w,100,'424540');v.r(x,100,w,500,'DAD3C5')
        v.l(x+w/2,110,x+w/2,575,GREY,.35)
    if uppermesh:mesh(v,x,2200,w,400)
    for xx in (x,x+w-25):v.r(xx,0,25,H,INK)
    v.r(x,H-25,w,25,INK)
    for j,z in enumerate(C['units']['shelf_levels']):
        v.r(x,z-25,w,25,INK)
        v.l(x+25,z-22,x+w-25,z-22,GOLD,.8)
        if z<2200:
            tinybottle(v,x+80,z+3,j);tinybottle(v,x+w-150,z+3,j+1)

def call(v,x,z,u,y,text):
    leader(v.s,*v.p(x,z),u,y,text,w=66)

# Additional plan interfaces: structure at the storefront and rear, counter frame.
s=prs.slides[2];v=View(s,90,238,20)
for x in (0,1950):
    for xx in (x,x+425):v.r(xx,0,25,450,INK)
    v.l(x+25,250,x+425,250,GREY,.5,True)
for x in (250,1650):
    for xx in (x,x+475):v.r(xx,2856,25,25,INK)
for x in (700,1680):
    for y in (1706,2136):v.r(x,y,20,20,INK)
v.dim(700,2156,1700,2156,-9)
v.dim(1700,1706,1700,2156,17)
txt(s,226,118,62,12,'COUNTER FRAME\n20 × 20 black steel',8)
txt(s,22,179,58,18,'STREET-FACING DISPLAY\nDashed line: shelf above\nSolid return toward interior',8,GREY)

# Reflected ceiling: keep known positions; unspecified spot stations stay TBC.
s=clean(5,'Reflected ceiling plan · lighting, display footprints and dimensional coordination')
notes(s,[('TRACK LIGHTING','Two matte-black tracks, four cylindrical adjustable heads each. 3000 K. Track coordinates dimensioned directly.'),('ENTRANCE DOWNLIGHTS','Three downlights at x=700 / 1200 / 1700; y=225. Symbol sizes indicative, not cut-out sizes.'),('DISPLAY LIGHTING','Concealed LEDs beneath shelves, and two 2656-long plinth runs. Dashed joinery footprint coordinates the ceiling with displays below.'),('CEILING / SERVICES','Warm off-white gypsum at 2600. No invented fire devices, wiring circuits or access panels. Consultant to coordinate under TBC #16.')])
v=View(s,75,238,20);shell(v)
for x in (0,2150):v.r(x,450,250,2656,None,'B8B7AE',True)
for x in (0,1950):v.r(x,0,450,450,None,'B8B7AE',True)
v.r(700,1706,1000,450,None,'B8B7AE',True)
for x in C['lighting']['track_x']:
    v.l(x,450,x,2656,INK,2)
    for y in (600,1200,1800,2400):
        v.r(x-28,y-60,56,120,INK)
        v.l(x,y,x+(-130 if x<1200 else 130),y+100,GOLD,.5)
for x,y in C['lighting']['downlights']:
    a,b=v.p(x,y);circle(s,a,b,1.7,GOLD);line(s,a-2.5,b,a+2.5,b,GREY,.35)
for x in (220,2180):v.l(x,450,x,D,GOLD,1,True)
v.dim(0,D,650,D,-8);v.dim(650,D,1750,D,-8);v.dim(1750,D,W,D,-8)
v.dim(0,0,0,D,-15);v.dim(650,450,650,2656,10)
v.dim(0,0,W,0,14)
call(v,1750,2400,211,105,'BLACK TRACK\nAdjustable spot heads')
call(v,2180,1500,211,144,'SHELF LEDs BELOW\n3000 K concealed light')
call(v,1700,225,211,223,'ENTRANCE DOWNLIGHTS\nThree approved positions')
cloud(s,207,169,77,32,'TBC #16\nHead stations / aiming indicative.\nConfirm MEP, fixings, drivers\nand ceiling access on site.')
v.bar(0,-530,1000)

s=clean(6,'Developed storefront · street-facing displays, glazed entrance and halo-lit brand')
notes(s,[('DISPLAY COLUMNS','450 wide, 450 deep; shelf depth 250. Black frame and folded trays; warm concealed LEDs. Bottles indicate use only.'),('CLEAR GLASS ENTRANCE','488 fixed pane, 1000 pivot leaf; 12 toughened glass. Faint rear joinery is visible through glass, not applied to it.'),('BRANDING / FINISH','600-high plaster fascia. 1000-wide native logo; black halo-lit letters on 25 stand-offs. Supports remain TBC #16.'),('GLAZING COORDINATION','Door fittings are indicative only. Handle, pivots, patch fittings, structural support and glass procurement require supplier confirmation.')])
v=View(s,65,237,20);v.r(0,0,W,3200,name='storefront-envelope')
v.r(0,2600,W,600,BEIGE);v.logo(700,2600+(600-1000/ratio)/2,1000)
# Rear display ghosted through clear glass; no false opaque door fill.
for x in (450,1650):
    v.r(x,0,300,600,None,'D7D0C3')
    for z in C['units']['shelf_levels']:v.l(x,z,x+300,z,'D7D0C3',.3)
v.r(700,0,1000,900,None,'D7D0C3')
for x in (0,1950):display(v,x,450,False,True)
v.r(454,10,488,2580,None,BLUE)
v.r(946,10,1000,2580,None,BLUE,name='door-leaf')
v.l(1030,950,1030,1250,INK,1.3)
for z in (25,2540):v.r(1810,z,90,25,'777970')
v.dim(0,0,W,0,14);v.dim(0,0,450,0,7);v.dim(450,0,1950,0,7);v.dim(1950,0,W,0,7)
v.dim(0,0,0,3200,-13);v.dim(2400,2600,2400,3200,9)
call(v,225,1700,205,141,'FOLDED BLACK SHELF\nWarm concealed light')
call(v,1500,1600,205,166,'CLEAR TOUGHENED GLASS\n12 mm; interior visible beyond')
call(v,1400,2900,205,83,'HALO-LIT BRAND\n1000 wide; 25 stand-offs')
cloud(s,205,198,77,33,'TBC #16\nHandle / fittings schematic.\n10 + 2580 + 10 height split\nrequires glazier confirmation.')
v.bar(0,-480,1000)

s=clean(7,'Rear focal wall · developed shelving + owner-directed counter front')
notes(s,[('REAR DISPLAY','500 / 900 / 500 zones between side units. 25 main posts, 3 mm folded trays, 25 downstands and warm concealed LEDs. No rear mesh.'),('COUNTER / RENDER DIRECTION','Left mesh panel, larger light-neutral right panel, light top and black perimeter frame. Replaces the small central mesh graphic at owner request.'),('DIMENSIONS RETAINED','Counter 1000 × 450 × 900 high, 20 × 20 black frame. Location and 450 side gaps unchanged. Revised front panel split is not a cutting schedule.'),('BRAND / FINISH','600-wide native black logo, centre 1900 AFFL, unlit. Raw light plaster backdrop. Product silhouettes indicative only.')])
v=View(s,65,222,20);v.r(0,0,W,H,'F0E8DA',name='internal-envelope')
for x in (0,2150):v.r(x,0,250,H,'DDD5C6');v.r(x+225,0,25,H,INK)
for x in (250,1650):display(v,x,500)
v.logo(900,1900-300/ratio,600)
v.r(700,0,1000,900,'D9CBB4',name='counter-elevation')
# Split and top thickness below are graphic envelopes, explicitly unapproved.
mesh(v,720,55,330,805)
for x in (700,1040,1680):v.r(x,20,20,860,INK)
v.r(700,20,1000,20,INK);v.r(700,860,1000,20,INK)
v.r(700,880,1000,20,'EEE7DB')
v.dim(0,0,W,0,17);v.dim(700,0,1700,0,8);v.dim(0,0,0,H,-13)
v.dim(0,H,250,H,-9);v.dim(250,H,750,H,-9);v.dim(750,H,1650,H,-9);v.dim(1650,H,2150,H,-9);v.dim(2150,H,W,H,-9)
v.dim(1700,0,1700,900,8)
call(v,1950,1400,206,131,'BLACK TRAY / WARM LED\n25 downstand; 250 depth')
call(v,1200,1900,206,103,'UNLIT BLACK LOGO\n600 wide; centre 1900')
cloud(s,205,174,78,40,'COUNTER REVISION / TBC #16\nOwner visual direction: mesh left,\nsolid panel right. Panel split, top\nthickness and connections TBC.\nSupersedes central insert depiction.')
v.bar(0,-700,1000)
