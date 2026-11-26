"""Analemma favicon: the sun's noon position over a year (NOAA equation-of-time and declination series).
Run from the repo root: python3 tools/make_favicon.py (writes favicon.svg, favicon.ico, apple-touch-icon.png)."""
import math, sys
from PIL import Image, ImageDraw
pts = []
for d in range(365):
    g = 2 * math.pi / 365 * d
    eot = 229.18 * (0.000075 + 0.001868*math.cos(g) - 0.032077*math.sin(g) - 0.014615*math.cos(2*g) - 0.040849*math.sin(2*g))
    dec = (0.006918 - 0.399912*math.cos(g) + 0.070257*math.sin(g) - 0.006758*math.cos(2*g) + 0.000907*math.sin(2*g)
           - 0.002697*math.cos(3*g) + 0.00148*math.sin(3*g))
    pts.append((eot / 4.0, math.degrees(dec)))   # degrees east-west (4 min = 1 deg), degrees north-south
XS = 2.2                                          # widen the narrow figure-8 so it reads at 16 px
xs = [p[0]*XS for p in pts]; ys = [p[1] for p in pts]
cx, cy = (max(xs)+min(xs))/2, (max(ys)+min(ys))/2
span = max(max(ys)-min(ys), max(xs)-min(xs))
def mapped(size, pad):
    k = (size - 2*pad) / span
    return [(size/2 + (x-cx)*k, size/2 - (y-cy)*k) for x, y in zip(xs, ys)]
AMBER, BG = "#f0b13a", "#000000"
# SVG
S = 64
p = mapped(S, 7)
d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in p) + " Z"
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}">
<rect width="{S}" height="{S}" rx="14" fill="{BG}"/>
<path d="{d}" fill="none" stroke="{AMBER}" stroke-width="3.4" stroke-linejoin="round"/>
</svg>
'''
open("favicon.svg", "w").write(svg)
# PNGs, drawn 8x and downsampled
def png(size, name, rounded=True):
    big = size * 8
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([0, 0, big-1, big-1], radius=int(big*14/64) if rounded else 0, fill=BG)
    q = mapped(big, big*7/64)
    w = max(1, round(big*3.4/64))
    r = w / 2
    ring = q + [q[0]]
    for (x0, y0), (x1, y1) in zip(ring, ring[1:]):   # stamp discs densely along the curve: a clean round stroke
        n = max(1, int(math.hypot(x1-x0, y1-y0) / 2))
        for i in range(n):
            x, y = x0 + (x1-x0)*i/n, y0 + (y1-y0)*i/n
            dr.ellipse([x-r, y-r, x+r, y+r], fill=AMBER)
    im.resize((size, size), Image.LANCZOS).save(name)
png(180, "apple-touch-icon.png", rounded=False)
png(32, "favicon-32.png"); png(16, "favicon-16.png"); png(256, "preview.png")
ico = Image.open("favicon-32.png"); ico.save("favicon.ico", sizes=[(16, 16), (32, 32)])
print("x range deg", min(p[0] for p in pts), max(p[0] for p in pts), "y range", min(ys), max(ys))
