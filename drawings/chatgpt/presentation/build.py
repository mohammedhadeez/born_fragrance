"""Build a portable, editable presentation from approved repository assets."""
import base64
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ASSET_COMMIT = '2941708870757a46da6f33b40b4330994e909f40'
SOURCE_COMMIT = '0e28b4e'
def source_file(name):
    return subprocess.check_output(['git', 'show', f'{ASSET_COMMIT}:drawings/claude/presentation/{name}'], cwd=ROOT)

handoff = source_file('HANDOFF.md').decode()
# All project content below is transcribed from this pinned handoff, not inferred from renders.
assert '2400 W × 3106 D; ceiling 2600' in handoff

def data(path, mime):
    return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode()

def drawing(name):
    # Embed Claude's clean vector asset unchanged; CSS object-fit preserves uniform scale.
    return 'data:image/svg+xml;base64,' + base64.b64encode(source_file(name + '.svg')).decode()

def text(tag, value, cls=''):
    return f'<{tag} class="{cls}" contenteditable="true">{value}</{tag}>'

def picture(src, label, cls=''):
    return f'<figure class="{cls}"><img src="{src}" alt="{label}" tabindex="0" title="Double-click to replace image"><figcaption contenteditable="true">{label}</figcaption></figure>'

pages = []
logo = data(ROOT / 'assets/brand/born-fragrance-logo-black.svg', 'image/svg+xml')
render = data(ROOT / 'assets/renders/born-fragrance-shop.png', 'image/png')

def page(title, subtitle, body, cls=''):
    number = len(pages) + 1
    pages.append(f'<section class="page {cls}" data-page="{number}"><div class="page-actions"><button data-move="-1">↑</button><button data-move="1">↓</button></div><header><img class="brand" src="{logo}" alt="Born Fragrance"><span contenteditable="true">DESIGN PRESENTATION · REV A</span></header>{text("h1",title)}{text("p",subtitle,"subtitle")}<div class="body">{body}</div><footer><span contenteditable="true">BORN FRAGRANCE · FOR COORDINATION · SITE ITEMS OPEN</span><span class="folio">{number:02}</span></footer></section>')

page('A small space.<br>A distinctive presence.', 'BORN FRAGRANCE / RETAIL INTERIOR', picture(render, 'Approved render — design intent only. Do not measure. Styling props shown in the render are excluded from the technical scope.') + text('p', 'Fine black steel lines, light textured surfaces and warm integrated lighting create a focused setting for fragrance.', 'lead') + '<div class="facts">' + text('div', '2400 × 3106 mm<br><small>Internal size · survey pending</small>') + text('div', '2600 mm<br><small>Ceiling height</small>') + text('div', 'Rev A<br><small>Coordination issue</small>') + '</div>', 'cover')

def view(title, subtitle, name, caption, notes):
    body = picture(drawing(name), caption, 'drawing') + '<div class="notes">' + ''.join(text('p', n) for n in notes) + '</div>'
    page(title, subtitle, body)

view('The layout', '01 / DISPLAY & FURNITURE PLAN', 'furniture-plan', 'NOT TO SCALE · presentation view of SD-02', ['Side display runs: 2656 mm, four 664 mm modules per side.', 'Counter: 1000 × 450 × 900 mm, centred at x=700–1700; rear edge y=2156, 700 mm to rear unit.', 'CHECK — TBC #16: 450 mm each side of counter. Consultant to confirm escape and staff access.'])
view('The street presence', '02 / STOREFRONT', 'storefront-elevation', 'NOT TO SCALE · presentation view of SD-05', ['Frontage: 450 + 1500 + 450 = 2400 mm; columns 450 × 450 mm face the street.', 'Pivot door: 1000 W × 2580 H mm. Fixed glass: 488 mm; glazier to confirm gaps.', 'Exterior logo: 1000 × 452.98 mm, black halo-lit on 25 mm stand-offs; 600 mm sign band, 3200 mm overall height.'])
view('The focal wall', '03 / REAR ELEVATION', 'rear-elevation', 'NOT TO SCALE · presentation view of SD-06', ['Rear zones: 500 + 900 + 500 = 1900 mm between side units; rear unit 250 mm deep.', 'Interior logo: 600 × 271.8 mm, centred at 1900 mm AFFL, non-illuminated black.', 'No mesh on rear display bays. Counter mesh insert: 300 × 450 mm, centred, bottom 150 mm above floor.'])
view('The display system', '04 / LEFT ELEVATION', 'left-elevation', 'NOT TO SCALE · presentation view of SD-07', ['Shelf levels: 600, 1000, 1400, 1800 and 2200 mm AFFL; frame height 2600 mm.', 'Front mesh infill: 2200–2600 mm. Shelf depth: 250 mm.', '3 mm folded MS shelves with 25 mm front downstand concealing LED profile.', '600 mm base cabinet includes a 100 H × 50 D mm recessed plinth.'])
view('A continuous rhythm', '05 / RIGHT ELEVATION', 'right-elevation', 'NOT TO SCALE · presentation view of SD-08', ['Four 664 mm bays over each 2656 mm side run, behind storefront columns to the rear wall.', '1.5 mm powder-coated steel cabinet doors: light neutral, flush and handleless.', 'CHECK — TBC #16: fix frames to floor and walls; no fixing to gypsum ceiling. Consultant to confirm anchors and substrate.'])
view('Light, carefully placed', '06 / CEILING & INTEGRATED LIGHTING', 'reflected-ceiling-plan', 'NOT TO SCALE · presentation view of SD-04', ['3000 K lighting: two black tracks at x=650/1750, 2206 mm long, four adjustable spots per track.', 'Three recessed downlights; smooth gypsum ceiling, matte warm off-white.', 'Concealed shelf LEDs and two 2656 mm toe-kick runs within recessed plinths.'])

materials = [('Black steel', '#252525', 'Matte black powder coat. Main frame 25×25×1.6 MS SHS; secondary frame 20×20×1.6 MS SHS.'), ('Light-neutral steel', '#d9d4ca', '1.5 mm powder-coated steel cabinet doors; flush, handleless. No timber.'), ('Textured plaster', '#e7e2d8', 'Raw light textured plaster. Swatch is indicative; approve physical finish sample.'), ('Stone-look porcelain', '#c7c3b9', '1200×600 mm rectified porcelain, 2 mm grout; option A with 5 mm perimeter movement joints.'), ('Clear glass', '#dce7e9', '12 mm clear toughened glass pivot door. Glazier to confirm fabrication and hardware.'), ('Expanded mesh', '#565656', 'Black diamond expanded metal, approximately 20×40 mm. Upper side display infill only.')]
body = '<div class="materials">' + ''.join(f'<article><div class="swatch" style="background:{c}" tabindex="0" title="Click to change swatch colour"></div>{text("h2",name)}{text("p",note)}</article>' for name,c,note in materials) + '</div>' + text('p', 'Palette colours are indicative screen references, not procurement specifications.', 'small')
page('Material character', '07 / FINISHES & FABRICATION', body)
page('Finishing the picture', '08 / COUNTER, CEILING & LIGHT', '<div class="coordination">' + ''.join(text('h2', title)+text('p', note) for title,note in [('M7 — counter front and top','Light neutral panel with a simple light-coloured top.'),('M9 — ceiling','Smooth gypsum, matte warm off-white. Frame fixings must not load the gypsum ceiling.'),('L1 — lighting','3000 K concealed LEDs, black track spots and recessed downlights.'),('Floor setting-out','Option A: 1200 mm across, 2 mm grout, 5 mm perimeter joint; end cuts 1194 / 343 mm.')]) + '</div>' + text('p','Excluded from the technical scope: timber, brass, decorative arches, heavy joinery, pendants, decorative ceiling features, plants and loose products. Reference boards inform composition only.','small'))
page('Ready for coordination', '09 / OPEN ITEMS & SOURCE DOCUMENTS', '<div class="coordination">' + ''.join(text('h2', title)+text('p', note) for title,note in [('TBC #4 — finished dimensions','Verify 2400 × 3106 mm clear internal size after plaster before fabrication.'),('TBC #16 — consultant review','Confirm counter access and escape, frame anchors, substrate capacity, fire and MEP requirements. The 450 mm counter side gaps remain a CHECK.'),('TBC #23 — orientation','North toward storefront is an assumption pending survey.'),('TBC #26 — construction and datum','FFL ±0 and 100 mm wall thickness are assumed; confirm construction and datum on site.')]) + '</div>' + text('p', 'Original SD-01–SD-08 technical sheets remain A3 landscape at 1:20. This portrait document is a presentation summary; its drawing views are not to scale.', 'lead') + text('p', f'Source: Claude HANDOFF.md and unchanged SVGs at {ASSET_COMMIT[:12]}; Rev A spec on main at {SOURCE_COMMIT}.', 'small'))

css = (HERE/'style.css').read_text()
js = (HERE/'editor.js').read_text()
html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Born Fragrance · Editable presentation</title><style>'+css+'</style></head><body><nav class="toolbar"><strong>BORN / EDITOR</strong><button id="edit">Editing on</button><button id="save">Download edited HTML</button><button id="print">Print / PDF</button><label>Accent <input id="accent" type="color" value="#a58a58"></label><button id="reset">Reset saved edits</button><span id="status">Double-click an image to replace it. Click text to edit.</span></nav><input id="upload" type="file" accept="image/*" hidden><main>'+''.join(pages)+'</main><script>'+js+'</script></body></html>'
(HERE/'index.html').write_text(html)
print(f'Built {len(pages)} editable A3 portrait pages: {HERE / "index.html"}')
