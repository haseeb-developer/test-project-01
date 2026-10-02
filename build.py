#!/usr/bin/env python3
"""
PORTRAIT ENGINE · generative GitHub profile README
  pip install pillow numpy
  1. drop your photo at  assets/photo.jpg   (.jpeg / .png / .webp also work)
  2. python build.py     -> rebuilds assets/*.svg, assets/pipeline.png and README.md
No photo present? A synthetic placeholder portrait is used so the pipeline still runs.
Every SVG is pure SMIL/CSS (no JS, no external files) so it animates inside GitHub <img> tags.
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__)); AS = os.path.join(HERE, "assets")
CFG = dict(
    focus=(0.5, 0.42),   # where the face is in your photo (x, y as 0..1). Tune if the crop misses your face.
    zoom=1.0,            # >1 crops tighter
    invert=False,        # True for photos with a very bright background
    words=["REACT", "NEXT.JS", "TYPESCRIPT", "SHOPIFY", "LIQUID", "WORDPRESS", "SUPABASE", "TAILWIND", "REDUX", "VERCEL"],
    traj=[("UPTEK", "FRONTEND DEV", "05/22", 14), ("NODE AGENCY", "SR REACT/NEXT", "07/23", 15), ("MARKLOOPS", "SR SHOPIFY/REACT", "10/24", 24)],
    portfolio="https://haseeb-kn.vercel.app/", upwork="https://www.upwork.com/freelancers/haseebkn",
    linkedin="https://www.linkedin.com/in/haseeb-developer", github="https://github.com/haseeb-developer", email="mhaseebkn@gmail.com", codepen="https://codepen.io/haseebdevv")
WORK = {
 "Shopify": [("Wear London","wear-london.com"),("Hudson Valley Fisheries","hudsonvalleyfisheries.com"),("Nulastin","nulastin.com"),("Payet Maison","payetmaison.com"),("Her Height","www.herheight.com"),("BarGear","bargear.eu"),("Happy Day Pets","www.happydaypets.com"),("GolfTailor","www.golftailor.eu"),("Beach Weekend","beachweekend.com"),("Sulene Serenity","suleneserenity.com"),("More Hair Organics","morehairorganics.com"),("Affinity Home Medical","affinityhomemedical.com"),("Ordek Waterfowl","ordekwaterfowl.com"),("Happy Hands World","happyhandsworld.com"),("AZO Products","azoproducts.com"),("Archer Jerky","archerjerky.com"),("Trina Hot Sauce","www.trinahotsauce.com")],
 "Web Apps": [("PanteraGPT","app.panteragpt.com"),("Brisbane Gateway","www.brisbanegateway.com.au"),("Zooplus","www.zooplus.com"),("Kit","app.kit.com"),("SkinDoc","www.skindoc.uk"),("Saalz CRM","app.saalz.com"),("Skyscanner","www.skyscanner.pk"),("Ecommerce Store","ecommerce-haseeb.vercel.app"),("Secure Dev Platform","devsafe.vercel.app"),("API Manager","keyvault-api-manager.vercel.app")],
 "WordPress": [("Petco Pakistan","petco.pk"),("MightyCall","www.mightycall.com"),("SharePoint Design Works","sharepointdesignworks.com"),("Wolfpack Wrestling TX","wolfpackwrestlingtx.com"),("Learnmate Australia","learnmate.com.au")],
 "UI/UX": [("FarmInBox","www.farminbox.in"),("TerraPay","www.terrapay.com"),("TenTwenty","www.tentwenty.me"),("Colab Software","www.colabsoftware.com")]}

BG, INK, DIM, HAIR, ACC = "#0b0c0e", "#ecebe6", "#7b7d82", "#25272c", "#ff5a1f"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"; SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

# ───────────────────────── image pipeline ─────────────────────────
def synthetic(w=400, h=500):
    im = Image.new("L", (w, h), 16); d = ImageDraw.Draw(im)
    d.ellipse((w * .0, h * .80, w * 1.0, h * 1.3), fill=96); d.rectangle((w * .40, h * .55, w * .60, h * .86), fill=118)
    d.ellipse((w * .27, h * .12, w * .73, h * .68), fill=196); d.pieslice((w * .24, h * .06, w * .76, h * .52), 180, 360, fill=38)
    for ex in (.39, .61): d.ellipse((w * (ex - .06), h * .355, w * (ex + .06), h * .385), fill=34); d.line((w * (ex - .08), h * .325, w * (ex + .07), h * .32), fill=60, width=5)
    d.line((w * .5, h * .38, w * .47, h * .51), fill=140, width=7); d.arc((w * .42, h * .54, w * .58, h * .60), 15, 165, fill=70, width=5)
    d.chord((w * .28, h * .52, w * .72, h * .76), 20, 160, fill=150)
    a = np.asarray(im, float) * (0.6 + 0.6 * (1 - np.tile(np.linspace(0, 1, w), (h, 1))))
    im = Image.fromarray(np.clip(a, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(3))
    return Image.fromarray(np.clip(np.asarray(im, float) + np.random.default_rng(1).normal(0, 4, (h, w)), 0, 255).astype("uint8"))

def source():
    for n in ("photo.jpg", "photo.jpeg", "photo.png", "photo.webp"):
        p = os.path.join(AS, n)
        if os.path.exists(p): print("using photo:", n); return ImageOps.exif_transpose(Image.open(p)).convert("L"), True
    print("no assets/photo.* found -> synthetic placeholder portrait"); im = synthetic(); im.save(os.path.join(AS, "placeholder_portrait.png")); return im, False

def crop(im, aspect):
    W, H = im.size; cw = min(W, H * aspect) / CFG["zoom"]; ch = cw / aspect
    l = min(max(CFG["focus"][0] * W - cw / 2, 0), W - cw); t = min(max(CFG["focus"][1] * H - ch / 2, 0), H - ch)
    return im.crop((int(l), int(t), int(l + cw), int(t + ch)))

def tone(im, cols, rows):
    a = np.asarray(im.resize((cols, rows), Image.LANCZOS), float) / 255
    lo, hi = np.percentile(a, [2, 98]); a = np.clip((a - lo) / max(hi - lo, 1e-3), 0, 1)
    bl = np.asarray(Image.fromarray((a * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(cols * .09)), float) / 255
    a = np.clip(a + .8 * (a - bl), 0, 1) ** 1.15
    if CFG["invert"]: a = 1 - a
    yy, xx = np.mgrid[0:rows, 0:cols]; nx = (xx / (cols - 1) - .5) / .5; ny = (yy / (rows - 1) - .46) / .56
    return a * np.clip(1.25 - (nx ** 2 + ny ** 2) ** 1.1 * 1.3, 0, 1)

def dither(a, s):
    f = (a * s).copy(); H, W = f.shape; out = []
    for y in range(H):
        for x in range(W):
            o = f[y, x]; n = 1.0 if o >= .5 else 0.0; e = o - n
            if n: out.append((x, y))
            if x + 1 < W: f[y, x + 1] += e * 7 / 16
            if y + 1 < H:
                if x > 0: f[y + 1, x - 1] += e * 3 / 16
                f[y + 1, x] += e * 5 / 16
                if x + 1 < W: f[y + 1, x + 1] += e / 16
    return out

def stipple(a, target=3000):
    d = a ** 1.35; lo, hi = .05, 1.6
    for _ in range(9):
        m = (lo + hi) / 2
        if len(dither(d, m)) > target: hi = m
        else: lo = m
    return dither(d, (lo + hi) / 2)

def march(f, t):
    H, W = f.shape; segs = []; e = 1e-9
    for y in range(H - 1):
        for x in range(W - 1):
            a, b, c, d = f[y, x], f[y, x + 1], f[y + 1, x + 1], f[y + 1, x]
            i = int(a > t) | int(b > t) << 1 | int(c > t) << 2 | int(d > t) << 3
            if i in (0, 15): continue
            T = (x + (t - a) / (b - a + e), y); R = (x + 1, y + (t - b) / (c - b + e)); B = (x + (t - d) / (c - d + e), y + 1); L = (x, y + (t - a) / (d - a + e))
            segs += {1: [(L, T)], 2: [(T, R)], 3: [(L, R)], 4: [(R, B)], 5: [(L, T), (R, B)], 6: [(T, B)], 7: [(L, B)], 8: [(L, B)], 9: [(T, B)], 10: [(L, B), (T, R)], 11: [(R, B)], 12: [(L, R)], 13: [(T, R)], 14: [(L, T)]}[i]
    return segs

# ───────────────────────── svg helpers ─────────────────────────
def svg(w, h, label, body, css="", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">'
            f'<style>.mo{{font-family:{MONO}}}.sa{{font-family:{SANS}}}.se{{font-family:{SERIF}}}{css}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>'
            f'<defs>{defs}</defs><rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>')

def frame(w, h, idx, title):
    o = "".join(f'<path d="M{x} {y + 14 * sy}V{y}H{x + 14 * sx}" fill="none" stroke="{DIM}"/>' for x, y, sx, sy in ((24, 24, 1, 1), (w - 24, 24, -1, 1), (24, h - 24, 1, -1), (w - 24, h - 24, -1, -1)))
    o += "".join(f'<path d="M{x} 24V{h - 24}" stroke="{HAIR}" stroke-width=".5" opacity=".6"/>' for x in range(120, w - 60, 120))
    return o + f'<text class="mo" x="56" y="58" font-size="11" fill="{ACC}" letter-spacing="2">{idx}</text><text class="mo" x="{w - 56}" y="58" font-size="11" fill="{DIM}" text-anchor="end" letter-spacing="2">{title}</text>'

def counter(x, y, tend, steps=20, T=16):
    o = []
    for k in range(steps + 1):
        a = max(k * tend / steps, .0001); b = (k + 1) * tend / steps if k < steps else .84
        o.append(f'<text class="mo" x="{x}" y="{y}" font-size="11" fill="{ACC}" opacity="0">{k * 5:03d}%<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;{a:.4f};{b:.4f};1" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/></text>')
    return "".join(o)

# ───────────────────────── 01 reconstruction ─────────────────────────
def hero(src, N=3000):
    W, H, PX, PY, PW, PH, C, R, T = 960, 640, 500, 70, 400, 500, 100, 125, 16
    a = tone(crop(src, .8), C, R); pts = stipple(a, N); rnd = random.Random(11); circ, acc = [], []
    for i, (x, y) in enumerate(pts):
        cx = (x + .5) * PW / C + rnd.uniform(-1.3, 1.3); cy = (y + .5) * PH / R + rnd.uniform(-1.3, 1.3); th = rnd.uniform(0, 6.283); A = rnd.uniform(220, 640)
        circ.append(f'<circle class="d" cx="{cx:.1f}" cy="{cy:.1f}" r="{.8 + 1.1 * a[y, x] ** .7:.2f}" style="--x:{math.cos(th) * A:.0f};--y:{math.sin(th) * A * .55:.0f};--t:{cy / PH * 3 + rnd.uniform(0, 1.2):.2f}s"/>')
        if i % 3 == 0: acc.append(f"M{cx - 1:.1f} {cy - 1:.1f}h2v2h-2z")
    css = (f".d{{fill:{INK};animation:asm {T}s cubic-bezier(.22,.8,.2,1) infinite both;animation-delay:var(--t)}}"
           "@keyframes asm{0%{transform:translate(calc(var(--x)*1px),calc(var(--y)*1px));opacity:0}6%{opacity:.95}22%{transform:translate(0,0);opacity:1}"
           "84%{transform:translate(0,0);opacity:1}100%{transform:translate(calc(var(--x)*-.55px),calc(var(--y)*-.55px));opacity:0}}")
    kt = "0;.36;.78;1"
    b = [frame(W, H, "01 / RECONSTRUCTION", "PARTICLE FIELD")]
    ruler = "".join(f'<path d="M{486 - (8 if k % 5 == 0 else 4)} {PY + k * 10}H486" stroke="{DIM}" stroke-width=".6"/>' for k in range(51)) + "".join(f'<text class="mo" x="{478}" y="{PY + k * 50 + 3}" font-size="8" fill="{DIM}" text-anchor="end">{k * 50:03d}</text>' for k in range(0, 10, 2))
    b.append(ruler)
    b.append(f'<g transform="translate({PX} {PY})"><clipPath id="band"><rect x="-60" y="-4" width="46" height="508"><animate attributeName="x" values="-60;-60;440;440" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>'
             + "".join(circ) + f'<path d="{"".join(acc)}" fill="{ACC}" clip-path="url(#band)"/>'
             f'<g><rect width="1" height="500" fill="{ACC}"/><path d="M-6 0h12M-6 125h12M-6 250h12M-6 375h12M-6 499h12" stroke="{ACC}"/><animateTransform attributeName="transform" type="translate" values="-14 0;-14 0;486 0;486 0" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></g></g>')
    b.append(f'<path d="M{PX - 12} {PY - 12}h14M{PX - 12} {PY - 12}v14M{PX + PW + 12} {PY + PH + 12}h-14M{PX + PW + 12} {PY + PH + 12}v-14" stroke="{ACC}" fill="none"/>')
    b.append(f'<text class="sa" x="56" y="112" font-size="20" fill="{DIM}" letter-spacing="14">MUHAMMAD<animate attributeName="letter-spacing" values="26;6;6;26" keyTimes="0;.22;.84;1" dur="{T}s" repeatCount="indefinite"/></text>')
    b.append(f'<clipPath id="nm"><rect x="40" y="130" width="0" height="170"><animate attributeName="width" values="0;420;420;0" keyTimes="0;.2;.86;1" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>'
             f'<text class="se" x="52" y="268" font-size="124" font-style="italic" fill="{INK}" textLength="384" lengthAdjust="spacingAndGlyphs" clip-path="url(#nm)">Haseeb</text>')
    b.append(f'<text class="sa" x="56" y="326" font-size="22" fill="{INK}">Frontend &amp; Shopify engineer</text><text class="mo" x="56" y="352" font-size="12" fill="{DIM}">Senior Shopify / React.js · Markloops</text><text class="mo" x="56" y="370" font-size="12" fill="{DIM}">Islamabad, PK · 33.6844° N  73.0479° E</text>')
    for i, (n, c) in enumerate((("100+", "PROJECTS"), ("20+", "SHOPIFY + WP"), ("4+", "YEARS FRONTEND"))):
        x = 56 + i * 140; b.append(f'<path d="M{x} 428H{x + 116}" stroke="{HAIR}"/><text class="se" x="{x}" y="478" font-size="46" fill="{INK}">{n}</text><text class="mo" x="{x}" y="500" font-size="10" fill="{DIM}" letter-spacing="1.5">{c}</text>')
    b.append(f'<text class="mo" x="56" y="582" font-size="11" fill="{DIM}" letter-spacing="2">RECONSTRUCTING</text>' + counter(190, 582, .22) + f'<rect x="56" y="594" width="372" height="1" fill="{HAIR}"/><rect x="56" y="593" width="0" height="3" fill="{ACC}"><animate attributeName="width" values="0;372;372;0" keyTimes="0;.22;.84;1" dur="{T}s" repeatCount="indefinite"/></rect>')
    b.append(f'<text class="mo" x="{PX}" y="{PY + PH + 32}" font-size="10" fill="{DIM}" letter-spacing="1">{len(pts):,} PARTICLES · FLOYD-STEINBERG SEED · CURL SCATTER</text>')
    return svg(W, H, "Portrait reconstructed from three thousand particles that stream in, assemble into the face, are scanned by a light band, then disperse. Muhammad Haseeb, frontend and Shopify engineer, Islamabad.", "".join(b), css), pts

# ───────────────────────── 02 isolines ─────────────────────────
def isolines(src):
    W, H, PX, PY, PW, PH, C, R, T = 960, 640, 56, 70, 400, 500, 100, 125, 14
    a = tone(crop(src, .8), C, R); f = np.asarray(Image.fromarray((a * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.4)), float) / 255
    lv = np.linspace(.10, .88, 10); cell = PW / (C - 1); b = [frame(W, H, "02 / ISOLINES", "LUMINANCE TOPOGRAPHY")]; allsegs = []
    g = [f'<g transform="translate({PX} {PY})">']
    for k, t in enumerate(lv):
        s = march(f, t); allsegs.append(s); d = "".join(f"M{p[0] * cell:.1f} {p[1] * cell:.1f}L{q[0] * cell:.1f} {q[1] * cell:.1f}" for p, q in s); hot = k >= 8
        g.append(f'<g><path d="{d}" fill="none" stroke="{ACC if hot else INK}" stroke-width="{.7 + k * .05:.2f}" stroke-linecap="round" opacity="{1 if hot else .2 + k * .09:.2f}"/>'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;{(k - 4.5) * .55:.1f} {(4.5 - k) * .45:.1f};0 0" keyTimes="0;.5;1" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1" dur="{6 + k * .7:.1f}s" repeatCount="indefinite"/></g>')
    rows = np.linspace(0, R - 1, 36).astype(int); seq = list(rows) + list(rows[-2:0:-1]); LX, LY, LW, LH = 520, 236, 384, 150
    def prof(r): return [(LX + i * LW / (C - 1), LY + LH - 10 - f[r, i] * (LH - 28)) for i in range(0, C, 2)]
    dl = [("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in prof(r))) for r in seq]; fl = [d + f"L{LX + LW} {LY + LH}L{LX} {LY + LH}Z" for d in dl]; n = len(seq)
    g.append(f'<g><rect width="{PW}" height="1" fill="{ACC}"/><path d="M-10 0h10M{PW} 0h10" stroke="{ACC}"/><animate attributeName="opacity" values="1" dur="1s"/>'
             f'<animate attributeName="transform" type="translate" values="{";".join(f"0 {r * cell:.1f}" for r in seq)}" dur="{T}s" repeatCount="indefinite" additive="replace"/></g>')
    g[-1] = g[-1].replace('<animate attributeName="opacity" values="1" dur="1s"/>', "").replace('<animate attributeName="transform" type="translate"', '<animateTransform attributeName="transform" type="translate"')
    b.append("".join(g) + "</g>")
    b.append(f'<text class="se" x="{LX}" y="148" font-size="40" font-style="italic" fill="{INK}">Topography of a face</text><text class="mo" x="{LX}" y="176" font-size="11" fill="{DIM}">10 isoluminance levels · gaussian σ 1.4 · per-level parallax drift</text><text class="mo" x="{LX}" y="192" font-size="11" fill="{DIM}">marching squares on a 100 × 125 luminance field</text>')
    b.append(f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" fill="none" stroke="{HAIR}"/><text class="mo" x="{LX}" y="{LY - 10}" font-size="10" fill="{DIM}" letter-spacing="2">CROSS-SECTION · LIVE</text><text class="mo" x="{LX + LW}" y="{LY - 10}" font-size="10" fill="{ACC}" text-anchor="end">LUMINANCE ↑ / X →</text>'
             + "".join(f'<path d="M{LX} {LY + LH - 10 - v * (LH - 28):.1f}H{LX + LW}" stroke="{HAIR}" stroke-width=".5" stroke-dasharray="2 4"/>' for v in (.25, .5, .75, 1))
             + f'<path d="{fl[0]}" fill="{ACC}" opacity=".12"><animate attributeName="d" values="{";".join(fl)}" dur="{T}s" repeatCount="indefinite"/></path><path d="{dl[0]}" fill="none" stroke="{ACC}" stroke-width="1.4"><animate attributeName="d" values="{";".join(dl)}" dur="{T}s" repeatCount="indefinite"/></path>')
    tot = sum(m for *_, m in CFG["traj"]); x = LX; ty = 500
    b.append(f'<text class="mo" x="{LX}" y="{ty - 48}" font-size="10" fill="{DIM}" letter-spacing="2">TRAJECTORY · 2022 → NOW</text>')
    for i, (co, role, st, m) in enumerate(CFG["traj"]):
        w = (LW - 8) * m / tot; cur = i == 2; col = ACC if cur else INK
        b.append(f'<rect x="{x:.0f}" y="{ty}" width="{w:.0f}" height="1" fill="{HAIR}"/><rect x="{x:.0f}" y="{ty - 1}" width="0" height="3" fill="{col}"><animate attributeName="width" values="0;{w:.0f};{w:.0f};0" keyTimes="0;.{3 + i * 2};.9;1" dur="{T}s" repeatCount="indefinite"/></rect>'
                 f'<circle cx="{x:.0f}" cy="{ty}" r="3.5" fill="{BG}" stroke="{col}"/><text class="sa" x="{x:.0f}" y="{ty - 16}" font-size="12" fill="{col}" letter-spacing="1.5">{co}</text><text class="mo" x="{x:.0f}" y="{ty + 22}" font-size="10" fill="{DIM}">{st} · {role}</text>')
        x += w + 4
    b.append(f'<text class="mo" x="{LX}" y="{PY + PH + 32}" font-size="10" fill="{DIM}" letter-spacing="1">{sum(len(s) for s in allsegs):,} CONTOUR SEGMENTS · {n} PROFILE FRAMES</text>')
    return svg(W, H, "Topographic isoline map of the portrait with parallax drift, a scanning line, and a live luminance cross-section plot, beside a career trajectory: Uptek, Node Agency, Markloops.", "".join(b)), allsegs

# ───────────────────────── 03 language ─────────────────────────
def mosaic(src):
    W, H, C, R, cw, lh, T = 960, 640, 84, 54, 5.7, 10.2, 20; words = CFG["words"]
    a = tone(crop(src, (C * cw) / (R * lh)), C, R); stream = ""
    while len(stream) < C * R: stream += "/".join(words) + "/"
    widx = []; wi = 0
    for ch in "/".join(words) + "/": widx.append(wi); wi = wi + 1 if ch == "/" else wi; wi %= len(words)
    # build per-character word index aligned with the repeating stream
    seq = [i for k in range(C * R // len("/".join(words) + "/") + 2) for i in widx]
    cls = lambda v: 4 if v > .75 else 3 if v > .55 else 2 if v > .35 else 1 if v > .18 else 0
    rows = []
    for r in range(R):
        spans = []; cur = None; txt = ""
        for c in range(C):
            i = r * C + c; k = (cls(a[r, c]), seq[i]); ch = stream[i]
            if k != cur:
                if cur: spans.append(f'<tspan class="c{cur[0]} w{cur[1]}">{txt}</tspan>')
                cur, txt = k, ""
            txt += ch
        spans.append(f'<tspan class="c{cur[0]} w{cur[1]}">{txt}</tspan>')
        rows.append(f'<text x="0" y="{(r + 1) * lh - 2:.1f}" textLength="{C * cw:.1f}" lengthAdjust="spacingAndGlyphs">{"".join(spans)}</text>')
    css = (f".mz text{{font-family:{MONO};font-size:9.5px;fill:{INK}}}.c0{{fill-opacity:.09}}.c1{{fill-opacity:.26}}.c2{{fill-opacity:.5}}.c3{{fill-opacity:.78}}.c4{{fill-opacity:1}}"
           f"@keyframes hl{{0%,9%{{fill:{ACC}}}13%,100%{{fill:{INK}}}}}@keyframes lg{{0%,9%{{fill:{ACC}}}13%,100%{{fill:{DIM}}}}}"
           + "".join(f".w{k}{{animation:hl {T}s infinite;animation-delay:{k * 2}s}}.l{k}{{animation:lg {T}s infinite;animation-delay:{k * 2}s}}" for k in range(len(words))))
    MX, MY, MW, MH = 56, 66, C * cw, R * lh; RX = 590
    b = [frame(W, H, "03 / LANGUAGE", "GLYPH FIELD"), f'<clipPath id="rv"><rect x="0" y="0" width="{MW:.0f}" height="0"><animate attributeName="height" values="0;{MH:.0f};{MH:.0f};0" keyTimes="0;.25;.95;1" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>',
         f'<g transform="translate({MX} {MY})"><g class="mz" clip-path="url(#rv)">{"".join(rows)}</g><rect x="0" y="0" width="{MW:.0f}" height="1.2" fill="{ACC}"><animate attributeName="y" values="0;{MH:.0f};{MH:.0f};0" keyTimes="0;.25;.95;1" dur="{T}s" repeatCount="indefinite"/></rect></g>']
    for i, ln in enumerate(("This face is", "typeset in the", "tools I ship with.")): b.append(f'<text class="se" x="{RX}" y="{148 + i * 38}" font-size="32" font-style="italic" fill="{INK}">{ln}</text>')
    b.append(f'<path d="M{RX} 262H904" stroke="{HAIR}"/><text class="mo" x="{RX}" y="282" font-size="10" fill="{DIM}" letter-spacing="2">TOKENS · ACTIVE GLYPHS LIGHT UP IN THE FIELD</text>')
    for k, w in enumerate(words): b.append(f'<text class="mo l{k}" x="{RX + 26}" y="{314 + k * 24}" font-size="13" fill="{DIM}">{w}</text><text class="mo" x="{RX}" y="{314 + k * 24}" font-size="10" fill="{HAIR}">{k + 1:02d}</text>')
    b.append(f'<rect x="{RX + 150}" y="304" width="14" height="1.5" fill="{ACC}"><animate attributeName="y" values="{";".join(str(304 + k * 24) for k in range(len(words)))}" keyTimes="{";".join(f"{k / len(words):.3f}" for k in range(len(words)))}" calcMode="discrete" dur="{T}s" repeatCount="indefinite"/></rect>')
    b.append(f'<text class="mo" x="{RX}" y="{MY + MH - 6}" font-size="10" fill="{DIM}" letter-spacing="1">{C} × {R} CELLS · {C * R:,} GLYPHS · {len(words)} TOKENS</text>')
    return svg(W, H, "The portrait typeset as a field of 4,536 glyphs spelling the tools used: React, Next.js, TypeScript, Shopify, Liquid, WordPress, Supabase, Tailwind, Redux, Vercel. Each token lights up in turn.", "".join(b), css)

def footer():
    b = (f'<path d="M56 0H904" stroke="{HAIR}"/><text class="se" x="56" y="70" font-size="40" font-style="italic" fill="{INK}">Let’s build the system.</text>'
         f'<circle cx="590" cy="60" r="4" fill="{ACC}"><animate attributeName="opacity" values="1;.2;1" dur="1.8s" repeatCount="indefinite"/></circle><text class="mo" x="604" y="64" font-size="12" fill="{INK}" letter-spacing="1">AVAILABLE FOR NEW ENGAGEMENTS</text>'
         f'<text class="mo" x="56" y="106" font-size="11" fill="{DIM}">UPWORK  ·  PORTFOLIO  ·  LINKEDIN  ·  EMAIL</text><rect x="56" y="124" width="120" height="1.5" fill="{ACC}"><animate attributeName="x" values="56;784;56" dur="8s" repeatCount="indefinite"/></rect>')
    return svg(960, 140, "Let's build the system. Available for new engagements.", b)

def pipeline(src, pts, segs):
    P = (220, 275); im = crop(src, .8).resize(P); tn = Image.fromarray((tone(crop(src, .8), 220, 275) * 255).astype("uint8"))
    st = Image.new("L", P, 12); d = ImageDraw.Draw(st)
    for x, y in pts: d.ellipse((x * 2.2 - 1, y * 2.2 - 1, x * 2.2 + 1, y * 2.2 + 1), fill=235)
    ct = Image.new("L", P, 12); d = ImageDraw.Draw(ct)
    for k, s in enumerate(segs):
        for p, q in s: d.line((p[0] * 2.2, p[1] * 2.2, q[0] * 2.2, q[1] * 2.2), fill=60 + k * 20)
    cv = Image.new("RGB", (4 * 220 + 5 * 16, 275 + 64), (11, 12, 14)); ft = ImageFont.load_default()
    for i, (t, p) in enumerate((("01 SOURCE", im), ("02 TONE MAP + VIGNETTE", tn), ("03 STIPPLE (DITHER)", st), ("04 ISOLINES", ct))):
        x = 16 + i * 236; cv.paste(p.convert("RGB"), (x, 32)); ImageDraw.Draw(cv).text((x, 12), t, fill=(123, 125, 130), font=ft)
    cv.save(os.path.join(AS, "pipeline.png"), optimize=True)

def readme():
    c = CFG; head = "".join(f'<th align="left">{k}</th>' for k in WORK); cells = "".join('<td valign="top">' + "<br>".join(f'<a href="https://{u}/">{n}</a>' for n, u in v) + "</td>" for v in WORK.values())
    def sec(a, t, img, alt): return f'<a id="{a}"></a>\n<details open>\n<summary><code>{t}</code></summary>\n<br>\n<div align="center"><img src="assets/{img}" alt="{alt}" width="100%"></div>\n</details>\n'
    return f'''<div align="center">

<sub><code><a href="#reconstruction">01 reconstruction</a> &nbsp;/&nbsp; <a href="#isolines">02 isolines</a> &nbsp;/&nbsp; <a href="#language">03 language</a> &nbsp;/&nbsp; <a href="{c["portfolio"]}">portfolio</a> &nbsp;/&nbsp; <a href="{c["upwork"]}">hire</a></code></sub>

</div>

{sec("reconstruction", "01 / reconstruction", "reconstruction.svg", "Portrait rebuilt from about three thousand particles that assemble into the face. Muhammad Haseeb, frontend and Shopify engineer in Islamabad.")}
{sec("isolines", "02 / isolines", "isolines.svg", "Topographic isoline map of the portrait with a live cross-section plot and career trajectory: Uptek, Node Agency, Markloops.")}
{sec("language", "03 / language", "language.svg", "The portrait typeset from the names of the tools used: React, Next.js, TypeScript, Shopify, Liquid, WordPress, Supabase, Tailwind, Redux, Vercel.")}
<details>
<summary><code>&gt; inspect pipeline: how this was made</code></summary>
<br>
<div align="center"><img src="assets/pipeline.png" alt="Pipeline: source photo, tone map with vignette, stipple dither, isolines" width="100%"></div>

Photo → tone map (percentile stretch, local contrast, elliptical vignette) → three independent renderers. Everything is precomputed by `build.py` into pure SVG, because GitHub strips JavaScript: the motion is SMIL and CSS keyframes.
</details>

<details>
<summary><code>&gt; ls /work</code></summary>
<br>

<table><tr>{head}</tr><tr>{cells}</tr></table>

</details>

<details>
<summary><code>&gt; cat contact</code></summary>

```text
portfolio   {c["portfolio"]}
upwork      {c["upwork"]}
linkedin    {c["linkedin"]}
codepen     {c["codepen"]}
email       {c["email"]}
```

</details>

<details>
<summary><code>&gt; cat plain.txt</code></summary>

```text
Muhammad Haseeb · Frontend & Shopify Developer · Islamabad, Pakistan
Senior Shopify / React.js Developer, Markloops (10/2024 - present)
Before: Node Agency (07/2023 - 10/2024), Uptek (05/2022 - 07/2023)
100+ projects · 20+ Shopify and WordPress builds · 4+ years frontend
JavaScript, TypeScript, HTML, CSS, SQL · React.js, Next.js, Redux Toolkit, Tailwind CSS, SCSS
Shopify, Liquid, WordPress, WooCommerce · Supabase, PostgreSQL, Vercel, Netlify, Clerk
Exploring: Linux, Docker, Python, Agentic AI
```

</details>

<div align="center"><a href="{c["upwork"]}"><img src="assets/footer.svg" alt="Let's build the system. Available for new engagements." width="100%"></a></div>
'''

def main():
    os.makedirs(AS, exist_ok=True); src, real = source()
    h, pts = hero(src); iso, segs = isolines(src)
    for n, s in (("reconstruction", h), ("isolines", iso), ("language", mosaic(src)), ("footer", footer())): open(os.path.join(AS, n + ".svg"), "w", encoding="utf-8").write(s)
    pipeline(src, pts, segs); open(os.path.join(HERE, "README.md"), "w", encoding="utf-8").write(readme()); print("built · real photo:", real)

if __name__ == "__main__": main()
