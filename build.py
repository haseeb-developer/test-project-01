#!/usr/bin/env python3
"""
PROFILE QUEST · pixel-art GitHub profile README generator
python build.py  -> writes ./assets/*.svg and ./README.md
Everything is pure SVG (SMIL), so it animates inside GitHub <img> tags. No JS, no external files.
Edit CONFIG (data comes from haseebkn.vercel.app + github.com/haseeb-developer), re-run, push.
"""
import itertools, math, os, random
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "assets")

CONFIG = {
  "login": "haseeb-developer", "portfolio": "https://haseeb-kn.vercel.app/",
  "upwork": "https://www.upwork.com/freelancers/haseebkn", "linkedin": "https://www.linkedin.com/in/haseeb-developer",
  "email": "mhaseebkn@gmail.com", "codepen": "https://codepen.io/haseebdevv",
  "status": [("CLASS", "FRONTEND + SHOPIFY"), ("GUILD", "MARKLOOPS (SENIOR)"), ("REALM", "ISLAMABAD, PAKISTAN"),
             ("LEVEL", "04+ YEARS"), ("CLEARED", "100+ PROJECTS")],
  "gear": [("WEAPON", "REACT.JS", "#29adff"), ("ARMOR", "SHOPIFY", "#00e436"), ("TOME", "TYPESCRIPT", "#ffec27"),
           ("FAMILIAR", "CLAUDE CODE", "#ff77a8"), ("COMPANION", "CURSOR", "#ffa300"), ("MOUNT", "VERCEL", "#c2c3c7")],
  "tree": [  # (domain, color, tools, locked)
    ("LANGUAGES", "#ffec27", ["JAVASCRIPT", "TYPESCRIPT", "HTML", "CSS", "SQL"], False),
    ("FRONTEND", "#29adff", ["REACT", "NEXT", "REDUX", "TAILWIND", "SCSS", "RWD", "REST"], False),
    ("COMMERCE & CMS", "#00e436", ["SHOPIFY", "LIQUID", "WORDPRESS", "WOOCOMMERCE"], False),
    ("BACKEND", "#ff77a8", ["SUPABASE", "POSTGRES", "VERCEL", "NETLIFY", "CLERK"], False),
    ("WORKFLOW", "#ffa300", ["GIT", "GITHUB", "VSCODE", "CURSOR", "NPM", "FIGMA"], False),
    ("SECURITY & ENG", "#ff004d", ["AUTH", "ENCRYPTION", "API", "DB DESIGN", "RLS"], False),
    ("EXPLORING", "#83769c", ["LINUX", "DOCKER", "PYTHON", "AGENTIC AI", "AI FLOW"], True)],
  "quests": [
    ("UPTEK", "FRONTEND DEVELOPER", "05/2022 - 07/2023", 14, ["React.js UI components", "Shopify themes in Liquid", "Figma to pixel-accurate layouts"], False),
    ("NODE AGENCY", "SENIOR REACT.JS / NEXT.JS DEV", "07/2023 - 10/2024", 15, ["10+ production client projects", "Lighthouse: 60s to 90+", "Mentored two junior developers"], False),
    ("MARKLOOPS", "SENIOR SHOPIFY / REACT.JS DEV", "10/2024 - PRESENT", 24, ["Shopify Plus storefronts, end to end", "Checkout customization + metafields", "React tooling for product + support"], True)],
  "trophies": ["PAIR EXTRAORDINAIRE", "QUICKDRAW", "PULL SHARK", "YOLO"],  # real GitHub achievements
  "work": {
    "Shopify": [("Wear London","wear-london.com"),("Hudson Valley Fisheries","hudsonvalleyfisheries.com"),("Nulastin","nulastin.com"),("Payet Maison","payetmaison.com"),("Her Height","www.herheight.com"),("BarGear","bargear.eu"),("Happy Day Pets","www.happydaypets.com"),("GolfTailor","www.golftailor.eu"),("Beach Weekend","beachweekend.com"),("Sulene Serenity","suleneserenity.com"),("More Hair Organics","morehairorganics.com"),("Affinity Home Medical","affinityhomemedical.com"),("Ordek Waterfowl","ordekwaterfowl.com"),("Happy Hands World","happyhandsworld.com"),("AZO Products","azoproducts.com"),("Archer Jerky","archerjerky.com"),("Trina Hot Sauce","www.trinahotsauce.com")],
    "Web Apps": [("PanteraGPT","app.panteragpt.com"),("Brisbane Gateway","www.brisbanegateway.com.au"),("Zooplus","www.zooplus.com"),("Kit","app.kit.com"),("SkinDoc","www.skindoc.uk"),("Saalz CRM","app.saalz.com"),("Skyscanner","www.skyscanner.pk"),("Ecommerce Store","ecommerce-haseeb.vercel.app"),("Secure Dev Platform","devsafe.vercel.app"),("API Manager","keyvault-api-manager.vercel.app")],
    "WordPress": [("Petco Pakistan","petco.pk"),("MightyCall","www.mightycall.com"),("SharePoint Design Works","sharepointdesignworks.com"),("Wolfpack Wrestling TX","wolfpackwrestlingtx.com"),("Learnmate Australia","learnmate.com.au")],
    "UI/UX": [("FarmInBox","www.farminbox.in"),("TerraPay","www.terrapay.com"),("TenTwenty","www.tentwenty.me"),("Colab Software","www.colabsoftware.com")]},
}
BG, NAVY, PLUM, GRN2, BRN = "#0b1026", "#1d2b53", "#7e2553", "#008751", "#ab5236"
DG, LG, WH, RED, ORG, YEL, GRN, BLU, LAV, PNK, PCH = "#5f574f", "#c2c3c7", "#fff1e8", "#ff004d", "#ffa300", "#ffec27", "#00e436", "#29adff", "#83769c", "#ff77a8", "#ffccaa"
CAT = {"Shopify": GRN, "Web Apps": BLU, "WordPress": ORG, "UI/UX": PNK}
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
_u = itertools.count(1)
F = {'A':[14,17,17,31,17,17,17],'B':[30,17,17,30,17,17,30],'C':[14,17,16,16,16,17,14],'D':[30,17,17,17,17,17,30],'E':[31,16,16,30,16,16,31],'F':[31,16,16,30,16,16,16],'G':[14,17,16,23,17,17,15],'H':[17,17,17,31,17,17,17],'I':[14,4,4,4,4,4,14],'J':[7,2,2,2,2,18,12],'K':[17,18,20,24,20,18,17],'L':[16,16,16,16,16,16,31],'M':[17,27,21,21,17,17,17],'N':[17,25,21,19,17,17,17],'O':[14,17,17,17,17,17,14],'P':[30,17,17,30,16,16,16],'Q':[14,17,17,17,21,18,13],'R':[30,17,17,30,20,18,17],'S':[15,16,16,14,1,1,30],'T':[31,4,4,4,4,4,4],'U':[17,17,17,17,17,17,14],'V':[17,17,17,17,17,10,4],'W':[17,17,17,21,21,27,17],'X':[17,17,10,4,10,17,17],'Y':[17,17,10,4,4,4,4],'Z':[31,1,2,4,8,16,31],'0':[14,17,19,21,25,17,14],'1':[4,12,4,4,4,4,14],'2':[14,17,1,2,4,8,31],'3':[30,1,1,14,1,1,30],'4':[2,6,10,18,31,2,2],'5':[31,16,30,1,1,17,14],'6':[6,8,16,30,17,17,14],'7':[31,1,2,4,8,8,8],'8':[14,17,17,14,17,17,14],'9':[14,17,17,15,1,2,12],'+':[0,4,4,31,4,4,0],'-':[0,0,0,31,0,0,0],'/':[1,1,2,4,8,16,16],'.':[0,0,0,0,0,0,4],':':[0,4,0,0,0,4,0],'!':[4,4,4,4,4,0,4],'>':[16,8,4,2,4,8,16],'&':[12,18,20,8,21,18,13],',':[0,0,0,0,6,2,4],'(':[2,4,8,8,8,4,2],')':[8,4,2,2,2,4,8],'?':[14,17,1,2,4,0,4],'^':[10,31,31,31,14,4,0],'*':[0,4,21,14,21,4,0],'=':[0,0,31,0,31,0,0],'_':[0,0,0,0,0,0,31],'#':[10,10,31,10,31,10,10]}

def svg(w, h, label, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}" shape-rendering="crispEdges">'
            f'<style>.m{{font-family:{MONO}}}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>'
            f'<defs><pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".16"/></pattern>{defs}</defs>'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}<rect width="{w}" height="{h}" fill="url(#sl)" pointer-events="none"/></svg>')

def pw(s, sc=3, sp=1): return len(s) * (5 + sp) * sc - sp * sc
def ptext(s, x, y, sc=3, fill=WH, sp=1, wave=0, ws=0.08, shadow=None, anchor="s"):
    if anchor == "m": x = x - pw(s, sc, sp) / 2
    out, cx = [], x
    for i, ch in enumerate(s.upper()):
        g = F.get(ch)
        if g:
            d = ""
            for r, row in enumerate(g):
                c = 0
                while c < 5:
                    if row >> (4 - c) & 1:
                        s0 = c
                        while c < 5 and row >> (4 - c) & 1: c += 1
                        d += f"M{cx + s0 * sc:g} {y + r * sc:g}h{(c - s0) * sc}v{sc}h-{(c - s0) * sc}z"
                    else: c += 1
            p = f'<path d="{d}" fill="{fill}"/>'
            if shadow: p = f'<path d="{d}" fill="{shadow}" transform="translate({sc} {sc})"/>' + p
            if wave:
                p = (f'<g>{p}<animateTransform attributeName="transform" type="translate" values="0 0;0 {-wave};0 0;0 0" keyTimes="0;.12;.24;1" '
                     f'calcMode="discrete" dur="2.6s" begin="{i * ws:.2f}s" repeatCount="indefinite"/></g>')
            out.append(p)
        cx += (5 + sp) * sc
    return "".join(out)

def box(x, y, w, h, title=None, border=LG, fill=NAVY, tc=YEL, op=1):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{border}"/><rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" fill="{fill}" opacity="{op}"/>'
    for cx, cy in ((x, y), (x + w - 4, y), (x, y + h - 4), (x + w - 4, y + h - 4)): s += f'<rect x="{cx}" y="{cy}" width="4" height="4" fill="{BG}"/>'
    if title: s += f'<rect x="{x + 16}" y="{y - 8}" width="{pw(title, 2) + 16}" height="16" fill="{BG}"/>' + ptext(title, x + 24, y - 7, 2, tc)
    return s

def blink(el_body, dur="1s", vals="1;0"): return f'<g>{el_body}<animate attributeName="opacity" values="{vals}" dur="{dur}" calcMode="discrete" repeatCount="indefinite"/></g>'

SPRITE = ["....................", ".....HHHHHHHHHH.....", "....HHHHHHHHHHHH....", "....HHHHHHHHHHHH....", "...GHHHHHHHHHHHHG...",
          "..gGHSSSSSSSSSSHGg..", "..gGHSSSSSSSSSSHGg..", "..gGSSEESSSSEESSGg..", "..gGSSEESSSSEESSGg..", "..gGSSSSSSSSSSSSGg..",
          "...GSSSSSMMSSSSSG...", "....sSSSSSSSSSSs....", ".....ssSSSSSSss.....", "........SSSS........", "....bBBBBBBBBBBb....",
          "..bBBBBBBWWBBBBBBb..", "..bBBBBBBWWBBBBBBb..", ".bBBBBLLLLLLLLBBBBb.", ".bBBBBLLLYYLLLBBBBb.", ".bBBBlllllllllBBBBb."]
SPC = {'H': "#2b1d1d", 'S': PCH, 's': "#e8a982", 'E': NAVY, 'M': BRN, 'G': LAV, 'g': DG, 'B': BLU, 'b': "#1b6fb3", 'W': WH, 'L': LG, 'l': DG, 'Y': YEL}
for _r in SPRITE: assert len(_r) == 20, _r
assert len(SPRITE) == 20

def sprite(x, y, px, bob=True):
    body, eyes = [], []
    for r, row in enumerate(SPRITE):
        c = 0
        while c < 20:
            ch = row[c]
            if ch == '.': c += 1; continue
            s0 = c
            while c < 20 and row[c] == ch: c += 1
            rect = f'<rect x="{x + s0 * px}" y="{y + r * px}" width="{(c - s0) * px}" height="{px}" fill="{SPC[ch]}"%s/>'
            if ch == 'E': eyes.append((x + s0 * px, y + r * px, (c - s0) * px)); body.append(rect % "")
            elif ch == 'Y': body.append(rect % "")
            else: body.append(rect % "")
    lids = "".join(f'<rect x="{a}" y="{b}" width="{w}" height="{px}" fill="{PCH}" opacity="0"><animate attributeName="opacity" values="0;1;0" keyTimes="0;.5;1" dur="4.2s" begin="{(i % 4) * 0}s" calcMode="discrete" repeatCount="indefinite"/></rect>' for i, (a, b, w) in enumerate(eyes))
    lids = lids.replace('values="0;1;0" keyTimes="0;.5;1"', 'values="0;0;1;0" keyTimes="0;.92;.95;1"')
    g = "".join(body) + lids
    if bob: g = f'<g>{g}<animateTransform attributeName="transform" type="translate" values="0 0;0 {-max(1, px // 3)};0 0" keyTimes="0;.5;1" calcMode="discrete" dur="1.3s" repeatCount="indefinite"/></g>'
    return g

def ridge(base, amp, col, seed, step=16, ks=(1, 3, 5)):
    r = random.Random(seed); ph = [r.uniform(0, 6.28) for _ in ks]; o = []
    for i in range(960 // step):
        x = i * step; v = sum((1, .5, .25)[j] * math.sin(2 * math.pi * ks[j] * x / 960 + ph[j]) for j in range(3))
        h = int(amp * (v + 1.75) / 3.5) // 8 * 8 + 8
        o.append(f'<rect x="{x}" y="{base - h}" width="{step}" height="{h}" fill="{col}"/>')
    return "".join(o)

def tiled(content, dur, shift=960):
    return f'<g><g>{content}</g><g transform="translate({shift} 0)">{content}</g><animateTransform attributeName="transform" type="translate" values="0 0;-{shift} 0" dur="{dur}s" repeatCount="indefinite"/></g>'

def city(base, seed, col="#121a3c"):
    r = random.Random(seed); x = 0; o = []
    while x < 960:
        w = min(r.choice([48, 64, 80, 96]), 960 - x)
        if 960 - x - w < 48 and 960 - x - w > 0: w = 960 - x
        h = r.choice([88, 120, 152, 184, 216]); y = base - h
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}"/>')
        for wx in range(x + 8, x + w - 8, 16):
            for wy in range(y + 12, base - 44, 20):
                if r.random() < .22:
                    a = f'<animate attributeName="opacity" values="1;.2;1" dur="{r.uniform(3, 7):.1f}s" repeatCount="indefinite"/>' if r.random() < .25 else ""
                    o.append(f'<rect x="{wx}" y="{wy}" width="8" height="8" fill="{YEL}">{a}</rect>')
        if r.random() < .6:
            for k in range(0, w, 8): o.append(f'<rect x="{x + k}" y="{base - 36}" width="8" height="12" fill="{RED if (k // 8) % 2 == 0 else WH}"/>')
        x += w
    return "".join(o)

def hero():
    W, H, b = 960, 420, []
    for i, c in enumerate(["#0b1026", "#0f1838", "#142046", "#1d2b53", "#2c2a5e", "#43295f", PLUM]): b.append(f'<rect y="{i * 48}" width="{W}" height="48" fill="{c}"/>')
    r = random.Random(4)
    for i in range(44):
        x, y = r.randrange(0, W, 4), r.randrange(40, 230, 4)
        b.append(f'<rect x="{x}" y="{y}" width="{r.choice([2, 4])}" height="{r.choice([2, 4])}" fill="{WH}" opacity=".3"><animate attributeName="opacity" values=".15;1;.15" dur="{r.uniform(1.5, 4):.1f}s" begin="{r.uniform(0, 3):.1f}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    for i in range(8):
        for j in range(8):
            if (i - 3.5) ** 2 + (j - 3.5) ** 2 <= 16: b.append(f'<rect x="{846 + i * 8}" y="{44 + j * 8}" width="8" height="8" fill="{WH if (i, j) not in ((2, 2), (4, 4), (3, 5)) else LG}"/>')
    b.append(tiled(ridge(330, 150, "#1a2250", 3), 70)); b.append(tiled(city(330, 9), 26))
    b.append(f'<rect y="330" width="{W}" height="90" fill="#0a1230"/><rect y="330" width="{W}" height="8" fill="{GRN2}"/>')
    b.append(tiled("".join(f'<rect x="{k * 64}" y="370" width="28" height="4" fill="{DG}"/>' for k in range(16)), 1.6, 64) .replace("-64 0", "-64 0"))
    b.append(box(36, 92, 570, 240, None, LG, BG, op=.78))
    b.append(ptext("HASEEB", 56, 112, 12, WH, wave=10, shadow=PLUM))
    b.append(ptext("DEVELOPER", 58, 214, 5, BLU)); b.append(ptext("FRONTEND + SHOPIFY ENGINEER", 58, 262, 2, LG))
    b.append(blink(ptext("PRESS START", 58, 292, 3, YEL), "1.2s"))
    b.append(f'<rect x="680" y="284" width="210" height="14" fill="{LG}"/><rect x="680" y="298" width="210" height="6" fill="{DG}"/>')
    b.append(f'<g><g>{sprite(710, 100, 9, False)}</g><g>' + "".join(f'<rect x="{x}" y="304" width="12" height="12" fill="{ORG}"/><rect x="{x + 2}" y="316" width="8" height="8" fill="{YEL}"/>' for x in (700, 770, 840)) +
             '<animate attributeName="opacity" values="1;.4;1" dur=".3s" calcMode="discrete" repeatCount="indefinite"/></g>'
             '<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" keyTimes="0;.5;1" calcMode="discrete" dur="1.6s" repeatCount="indefinite"/></g>')
    b.append(ptext("PLAYER 1", 24, 18, 2, WH)); b.append(ptext("^^^", 150, 18, 2, RED, sp=0))
    b.append(ptext("SCORE 100+ PROJECTS", 300, 18, 2, YEL)); b.append(ptext("LV 04", 880, 18, 2, WH))
    return svg(W, H, "Pixel hero: a developer on a hover-desk flying over a scrolling storefront skyline. Haseeb, frontend and Shopify developer. Press start.", "".join(b))

def player(cfg):
    W, H, b = 960, 440, []
    b.append(box(20, 24, 300, 396, "PLAYER 1", tc=YEL))
    b.append(f'<rect x="60" y="316" width="220" height="14" fill="{LG}"/><rect x="60" y="330" width="220" height="6" fill="{DG}"/>')
    b.append(f'<g>{sprite(80, 110, 10)}</g>' + '<g opacity=".9">' + "".join(f'<rect x="{x}" y="338" width="10" height="{h}" fill="{ORG}"><animate attributeName="height" values="{h};{h + 8};{h}" dur=".4s" calcMode="discrete" repeatCount="indefinite"/></rect>' for x, h in ((100, 8), (160, 12), (220, 8))) + '</g>')
    b.append(ptext("HASEEB", 170, 62, 5, WH, anchor="m", shadow=PLUM)); b.append(ptext("FRONTEND + SHOPIFY", 170, 380, 2, LG, anchor="m"))
    b.append(box(340, 24, 600, 396, "STATUS", tc=YEL))
    for i, (k, v) in enumerate(cfg["status"]):
        y = 60 + i * 34
        b.append(ptext(k, 364, y + 4, 2, LAV)); b.append(ptext(v, 520, y, 3, WH))
        b.append(f'<rect x="364" y="{y + 26}" width="552" height="2" fill="{NAVY}" opacity=".0"/><rect x="364" y="{y + 28}" width="552" height="2" fill="#2a3a70"/>')
    b.append(ptext("EQUIPMENT", 364, 246, 2, YEL))
    for i, (slot, item, col) in enumerate(cfg["gear"]):
        x, y = 364 + (i % 3) * 190, 274 + (i // 3) * 70
        b.append(f'<rect x="{x}" y="{y}" width="52" height="52" fill="{DG}"/><rect x="{x + 3}" y="{y + 3}" width="46" height="46" fill="{BG}"/>')
        b.append(ptext(item[0], x + 13, y + 9, 5, col)); b.append(ptext(slot, x + 62, y + 8, 2, LAV)); b.append(ptext(item, x + 62, y + 30, 2, WH))
        b.append(f'<rect x="{x}" y="{y}" width="52" height="52" fill="none" stroke="{WH}" stroke-width="3" opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.04;.12;1" dur="9s" begin="{i * 1.5}s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "Player sheet: Haseeb, Frontend and Shopify class, guild Markloops, Islamabad, level 4 plus years, 100 plus projects cleared, equipment React, Shopify, TypeScript, Claude Code, Cursor, Vercel", "".join(b))

def skills(cfg):
    W, H, b = 960, 560, []
    b.append(box(20, 20, 920, 520, "SKILL TREE", tc=YEL))
    rows = cfg["tree"]; ys = [76 + i * 66 for i in range(len(rows))]; mid = (ys[0] + ys[-1]) / 2 + 14
    b.append(f'<rect x="36" y="{mid - 18:g}" width="96" height="36" fill="{LG}"/><rect x="40" y="{mid - 14:g}" width="88" height="28" fill="{PLUM}"/>' + ptext("HASEEB", 84, mid - 7, 2, WH, anchor="m"))
    b.append(f'<rect x="148" y="{ys[0] + 14}" width="4" height="{ys[-1] - ys[0]}" fill="{DG}"/><rect x="132" y="{mid - 2:g}" width="18" height="4" fill="{DG}"/>')
    b.append(f'<rect width="8" height="8" fill="{WH}"><animateMotion path="M{148 - 3} {mid:g}V{ys[0] + 14}" dur="2.2s" repeatCount="indefinite"/></rect><rect width="8" height="8" fill="{WH}"><animateMotion path="M{148 - 3} {mid:g}V{ys[-1] + 14}" dur="2.2s" begin=".5s" repeatCount="indefinite"/></rect>')
    for i, (dom, col, tools, lock) in enumerate(rows):
        y, my = ys[i], ys[i] + 14
        b.append(f'<rect x="150" y="{my - 2}" width="20" height="4" fill="{col}"/>')
        b.append(f'<rect x="170" y="{y - 2}" width="190" height="32" fill="{col}"/><rect x="174" y="{y + 2}" width="182" height="24" fill="{BG}"/>' + ptext(dom, 186, y + 6, 2, col))
        x = 376; b.append(f'<rect x="360" y="{my - 2}" width="16" height="4" fill="{col}"/>')
        for k, t in enumerate(tools):
            w = len(t) * 12 + 12
            if lock: b.append(f'<g><rect x="{x}" y="{y}" width="{w}" height="28" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="4 4"/>' + ptext(t, x + 6, y + 7, 2, col) + f'<animate attributeName="opacity" values="1;.35;1" dur="{2 + k * .4:.1f}s" calcMode="discrete" repeatCount="indefinite"/></g>')
            else:
                b.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" fill="{col}"/><rect x="{x + 3}" y="{y + 3}" width="{w - 6}" height="22" fill="{NAVY}"/>' + ptext(t, x + 6, y + 7, 2, WH))
                b.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" fill="{WH}" opacity="0"><animate attributeName="opacity" values="0;.55;0;0" keyTimes="0;.03;.1;1" dur="10s" begin="{i * .7 + k * .3:.1f}s" repeatCount="indefinite"/></rect>')
            x += w
            if k < len(tools) - 1: b.append(f'<rect x="{x}" y="{my - 2}" width="6" height="4" fill="{col}"/>'); x += 6
        assert x <= 925, (dom, x)
        if lock: b.append(ptext("LOCKED", 292, y + 44, 1, LAV, anchor="m")) if False else None
        b.append(f'<rect width="8" height="8" fill="{col}"><animateMotion path="M152 {my - 4}H{x}" dur="{3 + i * .3:.1f}s" begin="{i * .4:.1f}s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "Skill tree: Languages (JavaScript, TypeScript, HTML, CSS, SQL), Frontend (React, Next.js, Redux, Tailwind, SCSS), Commerce and CMS (Shopify, Liquid, WordPress, WooCommerce), Backend (Supabase, Postgres, Vercel, Netlify, Clerk), Workflow (Git, GitHub, VS Code, Cursor, npm, Figma), Security, and locked exploring branch: Linux, Docker, Python, Agentic AI", "".join(b))

def quests(cfg):
    W, H, b = 960, 440, []
    b.append(box(20, 20, 920, 400, "QUEST LOG", tc=YEL))
    b.append(f'<rect x="60" y="94" width="840" height="8" fill="{DG}"/>' + "".join(f'<rect x="{x}" y="96" width="16" height="4" fill="{BG}"/>' for x in range(60, 900, 32)))
    for i, (co, role, per, mo, notes, cur) in enumerate(cfg["quests"]):
        x = 36 + i * 306; cx = x + 140; col = ORG if cur else GRN
        b.append(f'<rect x="{cx - 12}" y="82" width="24" height="24" fill="{col}"/><rect x="{cx - 8}" y="86" width="16" height="16" fill="{BG}"/>' + ptext(str(i + 1), cx - 3, 89, 1, col))
        b.append(f'<rect x="{cx - 12}" y="82" width="24" height="24" fill="none" stroke="{col}" stroke-width="2" opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.05;.2;1" dur="3s" begin="{i * .8}s" repeatCount="indefinite"/></rect>')
        b.append(box(x, 124, 280, 276, None, col, NAVY))
        b.append(ptext(f"QUEST 0{i + 1}", x + 16, 140, 2, YEL)); b.append(ptext(co, x + 16, 168, 3, WH))
        b.append(f'<text class="m" x="{x + 16}" y="214" font-size="11" fill="{BLU}">{role}</text><text class="m" x="{x + 16}" y="232" font-size="11" fill="{LAV}">{per}</text>')
        segs = round(mo / 2)
        b.append(ptext("XP", x + 16, 250, 2, LAV))
        for s in range(12): b.append(f'<rect x="{x + 48 + s * 17}" y="248" width="14" height="14" fill="{col if s < segs else BG}" stroke="{DG}" stroke-width="2"/>')
        b.append(ptext(f"{mo} MO" if mo < 24 else "2 YR", x + 16, 272, 2, col))
        if cur: b.append(blink(ptext("IN PROGRESS", x + 130, 272, 2, ORG), "1.2s"))
        for k, n in enumerate(notes): b.append(f'<text class="m" x="{x + 16}" y="{308 + k * 24}" font-size="11.5" fill="{WH}"><tspan fill="{col}">+ </tspan>{n}</text>')
    b.append(f'<g>{sprite(0, 0, 2, False)}<animateTransform attributeName="transform" type="translate" values="150 58;150 58;610 58;610 58" keyTimes="0;.08;.9;1" dur="10s" calcMode="linear" repeatCount="indefinite"/></g>')
    return svg(W, H, "Quest log: Uptek (frontend developer, 05/2022 to 07/2023), Node Agency (senior React and Next.js developer, 07/2023 to 10/2024), Markloops (senior Shopify and React developer, 10/2024 to present, in progress)", "".join(b))

def cartridges(cfg):
    W, H, b = 960, 480, []
    b.append(box(20, 20, 920, 448, "CARTRIDGE SHELF", tc=YEL))
    items = [(n, c) for c, v in cfg["work"].items() for n, _ in v]; N = len(items); assert N == 36
    pos = []
    for i, (n, c) in enumerate(items):
        x, y = 34 + (i % 12) * 75, 66 + (i // 12) * 100; col = CAT[c]; pos.append((x, y))
        ws = n.split(); ini = (ws[0][0] + ws[1][0]) if len(ws) > 1 else ws[0][:2]
        d = 1.3 + (i % 5) * .2
        b.append(f'<g><rect x="{x}" y="{y + 8}" width="62" height="70" fill="{DG}"/><rect x="{x + 4}" y="{y}" width="54" height="12" fill="{DG}"/><rect x="{x + 4}" y="{y + 14}" width="54" height="42" fill="{col}"/>'
                 f'<rect x="{x + 8}" y="{y + 18}" width="46" height="34" fill="{BG}"/>' + ptext(ini, x + 31, y + 28, 2, col, anchor="m") +
                 f'<rect x="{x + 10}" y="{y + 62}" width="42" height="8" fill="{LG}"/>' + "".join(f'<rect x="{x + 12 + k * 6}" y="{y + 66}" width="3" height="4" fill="{DG}"/>' for k in range(7)) +
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -2;0 0" keyTimes="0;.5;1" calcMode="discrete" dur="{d}s" begin="{i * .13:.2f}s" repeatCount="indefinite"/></g>')
    dt = .55; tot = N * dt
    kt = ";".join(f"{i / N:.4f}" for i in range(N))
    b.append(f'<rect width="70" height="86" fill="none" stroke="{WH}" stroke-width="4"><animate attributeName="x" values="{";".join(str(p[0] - 4) for p in pos)}" keyTimes="{kt}" calcMode="discrete" dur="{tot}s" repeatCount="indefinite"/>'
             f'<animate attributeName="y" values="{";".join(str(p[1] - 4) for p in pos)}" keyTimes="{kt}" calcMode="discrete" dur="{tot}s" repeatCount="indefinite"/></rect>')
    b.append(f'<rect x="40" y="368" width="880" height="44" fill="{BG}" stroke="{DG}" stroke-width="3"/>')
    for i, (n, c) in enumerate(items):
        b.append(f'<g opacity="0">' + ptext(n, 480, 380, 3, CAT[c], anchor="m") + f'<animate attributeName="opacity" values="1;0" keyTimes="0;{1 / N:.4f}" calcMode="discrete" dur="{tot}s" begin="{i * dt:.2f}s" repeatCount="indefinite"/></g>')
    for i, (c, col) in enumerate(CAT.items()):
        x = 60 + i * 210; b.append(f'<rect x="{x}" y="428" width="14" height="14" fill="{col}"/>' + ptext(c.upper(), x + 24, 430, 2, LG))
    return svg(W, H, "Cartridge shelf: 36 projects as game cartridges across Shopify, Web Apps, WordPress and UI/UX, with a selector cycling through them", "".join(b))

def trophies(cfg):
    W, H, b = 960, 260, []
    b.append(box(20, 20, 920, 220, "ACHIEVEMENTS", tc=YEL)); cols = [PNK, YEL, BLU, RED]
    for i, t in enumerate(cfg["trophies"]):
        cx = 140 + i * 226; col = cols[i]
        b.append(f'<g><rect x="{cx - 28}" y="62" width="56" height="12" fill="{col}"/><rect x="{cx - 24}" y="74" width="48" height="36" fill="{col}"/><rect x="{cx - 16}" y="110" width="32" height="12" fill="{col}"/><rect x="{cx - 4}" y="122" width="8" height="14" fill="{DG}"/><rect x="{cx - 20}" y="136" width="40" height="8" fill="{DG}"/>'
                 f'<rect x="{cx - 14}" y="80" width="8" height="24" fill="{WH}" opacity=".5"/>' + ptext(str(i + 1), cx - 6, 86, 2, BG) +
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" keyTimes="0;.5;1" calcMode="discrete" dur="1.8s" begin="{i * .3}s" repeatCount="indefinite"/></g>')
        b.append(ptext(t, cx, 160, 2, WH, anchor="m")); b.append(blink(ptext("UNLOCKED", cx, 190, 2, GRN, anchor="m"), "1.6s", "1;.3"))
        b.append(f'<rect x="{cx - 4}" y="48" width="8" height="8" fill="{WH}" opacity="0"><animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.05;.15;1" dur="6s" begin="{i * 1.2}s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "Achievements unlocked on GitHub: Pair Extraordinaire, Quickdraw, Pull Shark, YOLO", "".join(b))

def activity(counts=None, mode="sample"):
    W, H = 960, 300; r = random.Random(8)
    counts = counts or [r.choice([0, 1, 1, 2, 3, 5]) for _ in range(60)]; mx = max(counts) or 1; b = []
    b.append(box(20, 20, 920, 260, f"ACTIVITY // 60 DAYS // {mode.upper()}", tc=YEL))
    b.append(f'<rect x="36" y="246" width="888" height="6" fill="{DG}"/>')
    for i, c in enumerate(counts[:60]):
        x = 40 + i * 14.7; h = 8 + int(150 * c / mx) // 8 * 8; col = [NAVY, BLU, GRN, YEL][min(3, c * 4 // (mx + 1))] if c else NAVY
        b.append(f'<rect x="{x:.0f}" y="{246 - h}" width="12" height="{h}" fill="{col}"/>')
        for wy in range(246 - h + 6, 240, 12):
            if r.random() < .4: b.append(f'<rect x="{x + 3:.0f}" y="{wy}" width="3" height="4" fill="{WH}" opacity=".8"><animate attributeName="opacity" values=".9;.1;.9" dur="{r.uniform(2, 6):.1f}s" begin="{r.uniform(0, 3):.1f}s" calcMode="discrete" repeatCount="indefinite"/></rect>')
    b.append(f'<rect x="36" y="46" width="8" height="8" fill="{YEL}"><animate attributeName="x" values="36;916;36" dur="14s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "Activity skyline: one tower per day for the last 60 days, height equals public GitHub events", "".join(b))

def divider():
    W = 960; o = "".join(f'<rect x="{k * 32}" y="10" width="16" height="4" fill="{DG}"/>' for k in range(32))
    coin = f'<rect y="0" width="8" height="8" fill="{YEL}"><animate attributeName="x" values="-8;{W}" dur="9s" repeatCount="indefinite"/></rect>'
    return svg(W, 24, "", f'<g>{o}<animateTransform attributeName="transform" type="translate" values="0 0;-32 0" dur=".9s" repeatCount="indefinite"/></g>' + coin).replace('<rect width="960" height="24" fill="#0b1026"/>', "")

def button(label, col=BLU):
    w = pw(label, 2) + 56
    return svg(w, 44, label, f'<rect x="0" y="6" width="{w}" height="34" fill="{DG}"/><rect x="0" y="0" width="{w}" height="34" fill="{col}"/><rect x="4" y="4" width="{w - 8}" height="26" fill="{NAVY}"/>' +
               blink(f'<rect x="12" y="11" width="8" height="12" fill="{YEL}"/><rect x="20" y="14" width="4" height="6" fill="{YEL}"/>', "1s") + ptext(label, 34, 10, 2, WH)).replace(f'<rect width="{w}" height="44" fill="{BG}"/>', "")

def footer():
    W, H, b = 960, 220, ['<rect x="0" y="0" width="960" height="4" fill="#7e2553"/>']
    b.append(ptext("CONTINUE?", 480, 38, 9, WH, anchor="m", shadow=PLUM, wave=6, ws=.06))
    for i, d in enumerate("9876543210"): b.append(f'<g opacity="0">' + ptext(d, 480, 118, 8, YEL, anchor="m") + f'<animate attributeName="opacity" values="1;0" keyTimes="0;.1" calcMode="discrete" dur="10s" begin="{i}s" repeatCount="indefinite"/></g>')
    b.append(f'<g><rect x="290" y="130" width="16" height="32" fill="{YEL}"><animate attributeName="width" values="16;10;4;10;16" dur="1.2s" calcMode="discrete" repeatCount="indefinite"/><animate attributeName="x" values="290;293;296;293;290" dur="1.2s" calcMode="discrete" repeatCount="indefinite"/></rect></g>')
    b.append(blink(ptext("INSERT COIN: HIRE ON UPWORK", 480, 176, 3, GRN, anchor="m"), "1.4s"))
    return svg(W, H, "Continue? Insert coin: hire Haseeb on Upwork", "".join(b))

def readme(cfg):
    c = cfg
    def mod(a, cmd, img, alt, op=True): return f'<a id="{a}"></a>\n<details{" open" if op else ""}>\n<summary><code>{cmd}</code></summary>\n<br>\n<div align="center">\n<img src="assets/{img}" alt="{alt}" width="100%">\n</div>\n</details>\n'
    nav = "\n".join(f'<a href="#{a}"><img src="assets/btn-{a}.svg" alt="jump to {a}" height="44"></a>' for a in ("player", "skills", "quests", "cartridges", "trophies", "activity"))
    head = "".join(f'<th align="left">{k}</th>' for k in c["work"])
    cells = "".join("<td valign=\"top\">" + "<br>".join(f'<a href="https://{u}/">{n}</a>' for n, u in v) + "</td>" for v in c["work"].values())
    return f'''<div align="center">

<img src="assets/hero.svg" alt="Pixel hero: Haseeb on a hover-desk above a storefront skyline. Frontend and Shopify developer. Press start." width="100%">

{nav}
<br>
<a href="{c["upwork"]}"><img src="assets/btn-insert-coin.svg" alt="insert coin: hire on Upwork" height="44"></a>
<a href="{c["portfolio"]}"><img src="assets/btn-portfolio.svg" alt="open portfolio" height="44"></a>

<img src="assets/divider.svg" alt="" width="100%">

</div>

<a id="player"></a>
<div align="center"><img src="assets/player.svg" alt="Player sheet: Frontend and Shopify class, guild Markloops, Islamabad, level 4 plus years, 100 plus projects cleared" width="100%"></div>

<div align="center"><img src="assets/divider.svg" alt="" width="100%"></div>

{mod("skills", "> open skill_tree", "skills.svg", "Skill tree of languages, frontend, commerce, backend, workflow, security, plus a locked exploring branch")}
{mod("quests", "> open quest_log", "quests.svg", "Quest log: Uptek, Node Agency, Markloops")}
{mod("cartridges", "> open cartridge_shelf", "cartridges.svg", "36 projects as game cartridges")}
<details>
<summary><code>> load save_files (live links)</code></summary>
<br>

<table><tr>{head}</tr><tr>{cells}</tr></table>

</details>

{mod("trophies", "> open achievements", "trophies.svg", "GitHub achievements: Pair Extraordinaire, Quickdraw, Pull Shark, YOLO")}
{mod("activity", "> open activity_skyline", "activity.svg", "Skyline of the last 60 days of GitHub activity")}
<details>
<summary><code>> cat player_contacts.txt</code></summary>

```text
portfolio   {c["portfolio"]}
upwork      {c["upwork"]}
linkedin    {c["linkedin"]}
codepen     {c["codepen"]}
email       {c["email"]}
```

</details>

<details>
<summary><code>> cat plain_text_mode.txt</code></summary>

```text
Muhammad Haseeb · Frontend & Shopify Developer · Islamabad, Pakistan
Senior Shopify / React.js Developer at Markloops (10/2024 - present)
Before: Node Agency (07/2023 - 10/2024), Uptek (05/2022 - 07/2023)
100+ projects delivered · 20+ Shopify and WordPress builds · 4+ years frontend
Languages: JavaScript, TypeScript, HTML, CSS, SQL
Frontend: React.js, Next.js, Redux Toolkit, Tailwind CSS, SCSS, REST APIs
Commerce: Shopify, Liquid, WordPress, WooCommerce
Backend: Supabase, PostgreSQL, Vercel, Netlify, Clerk
Exploring: Linux, Docker, Python, Agentic AI, AI workflow
```

</details>

<div align="center"><a href="{c["upwork"]}"><img src="assets/footer.svg" alt="Continue? Insert coin: hire on Upwork" width="100%"></a></div>
'''

def w(name, s):
    os.makedirs(OUT, exist_ok=True); open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)

def main():
    c = CONFIG
    for n, s in (("hero", hero()), ("player", player(c)), ("skills", skills(c)), ("quests", quests(c)), ("cartridges", cartridges(c)), ("trophies", trophies(c)), ("activity", activity()), ("divider", divider()), ("footer", footer())): w(n + ".svg", s)
    for lab, fn in (("player", "player"), ("skills", "skills"), ("quests", "quests"), ("cartridges", "cartridges"), ("trophies", "trophies"), ("activity", "activity"), ("insert coin", "insert-coin"), ("portfolio", "portfolio")): w(f"btn-{fn}.svg", button(lab.upper(), ORG if "coin" in lab else BLU))
    open(os.path.join(HERE, "README.md"), "w", encoding="utf-8").write(readme(c)); print("built", OUT)

if __name__ == "__main__": main()
