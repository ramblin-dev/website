# /// script
# requires-python = ">=3.10"
# dependencies = ["fonttools>=4.50"]
# ///
"""Render the ramblin.dev logo: a clean logo.svg and a review mockup.

Downloads the Google Fonts it needs and bakes the lettering into the output
SVGs as real vector outlines, so the result does not depend on the viewer
fetching webfonts. Glyph metrics place "dev", the shared dot, and the trailing
path precisely; logo.svg is cropped to the artwork's computed bounding box.

Run:  uv run design/logo/render_logo.py
"""
import math
import os
import urllib.request
import xml.dom.minidom

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = "/tmp/ramblin-logo-fonts"
OUT = os.path.join(HERE, "mockup-script-composition.svg")
OUT_LOGO = os.path.join(HERE, "logo.svg")

# Kaushan Script is OFL-licensed; Satisfy and Yellowtail are Apache-2.0.
# Both licenses permit modification.
FONTS = {
    "Kaushan Script": "https://raw.githubusercontent.com/google/fonts/main/ofl/kaushanscript/KaushanScript-Regular.ttf",
    "Satisfy":        "https://raw.githubusercontent.com/google/fonts/main/apache/satisfy/Satisfy-Regular.ttf",
    "Yellowtail":     "https://raw.githubusercontent.com/google/fonts/main/apache/yellowtail/Yellowtail-Regular.ttf",
}

# Panels to render: (label, font, word). "dev" is always lowercase.
PANELS = [
    ("Satisfy capital R", "Satisfy", "Ramblin"),
]


# Palette: "ramblin" / road, "dev", and the shared dot.
COL_RAMBLIN = "#E03A4C"  # heart red
COL_DEV = "#3E9D63"      # green
COL_DOT = "#7C7C82"      # mid grey — meant to read on both white and dark

# Layout constants (SVG px)
X0 = 90            # left margin of the word
R = 132            # "ramblin" cap size
DEV = 84           # "dev" size
DEV_ROTATE = -12   # "dev" rotation in degrees (negative = counter-clockwise)
PANEL_H = 372
BASE0 = 320        # baseline of the first panel
TRAIL_W = R * 0.0340  # weight of the return path (lighter than the lettering)
TRAIL_END = 0.01       # the road's width at the R end, as a fraction of TRAIL_W
TAPER_FROM = 0.2     # fraction of the road's length before the taper begins
N_TIP_DY = -3         # nudge the n-end connection up (SVG px)
R_FOOT_DY = 0         # nudge the R-leg connection down (SVG px)
LOGO_MARGIN = 8       # px of breathing room around the cropped logo.svg
DOT_SHRINK = 2        # trim the dot radius by this many SVG px


def font_path(name, url):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name.replace(" ", "") + ".ttf")
    if not os.path.exists(p):
        print(f"  downloading {name} ...")
        urllib.request.urlretrieve(url, p)
    return p


class Word:
    """Lays out a string from one font and renders glyph outlines to SVG."""

    def __init__(self, ttf, text):
        self.font = TTFont(ttf)
        self.upm = self.font["head"].unitsPerEm
        self.cmap = self.font.getBestCmap()
        self.glyphset = self.font.getGlyphSet()
        self.hmtx = self.font["hmtx"]
        self.glyphs = []  # (char, glyphname, x_units)
        x = 0
        for ch in text:
            gname = self.cmap.get(ord(ch))
            if gname is None:
                x += int(self.upm * 0.3)
                continue
            self.glyphs.append((ch, gname, x))
            x += self.hmtx[gname][0]
        self.advance = x

    def glyph_of(self, ch):
        for c, gname, x in self.glyphs:
            if c == ch:
                return gname, x
        return None, None

    def right_edge_of(self, ch):
        for c, gname, x in self.glyphs:
            if c == ch:
                return x + self.hmtx[gname][0]
        return self.advance

    def outline_group(self, x_svg, baseline, size, color, rotate=0):
        scale = size / self.upm
        rot = f" rotate({rotate})" if rotate else ""
        parts = [
            f'<g transform="translate({x_svg:.2f} {baseline:.2f}){rot} '
            f'scale({scale:.6f} {-scale:.6f})" fill="{color}">'
        ]
        for _, gname, x in self.glyphs:
            pen = SVGPathPen(self.glyphset)
            self.glyphset[gname].draw(pen)
            d = pen.getCommands()
            if d:
                parts.append(f'<path transform="translate({x} 0)" d="{d}"/>')
        parts.append("</g>")
        return "".join(parts)

    def tittle_bbox(self, gname):
        """Bounding box (font units) of the topmost contour of a glyph."""
        glyf = self.font.get("glyf")
        if glyf is None:
            return None
        g = glyf[gname]
        if g.isComposite() or g.numberOfContours is None or g.numberOfContours < 2:
            return None
        coords = list(g.coordinates)
        contours, start = [], 0
        for end in g.endPtsOfContours:
            contours.append(coords[start:end + 1])
            start = end + 1
        top = max(contours, key=lambda pts: max(y for _, y in pts))
        xs = [p[0] for p in top]
        ys = [p[1] for p in top]
        return min(xs), min(ys), max(xs), max(ys)

    def glyph_bbox(self, gname):
        pen = BoundsPen(self.glyphset)
        self.glyphset[gname].draw(pen)
        return pen.bounds  # (xMin, yMin, xMax, yMax) or None

    def extreme(self, ch, score):
        """Outline point of char `ch` maximizing score(x, y), in word units.

        Prefers on-curve points; falls back to the glyph bbox corners."""
        gname, xoff = self.glyph_of(ch)
        if gname is None:
            return (self.advance, 0)
        glyf = self.font.get("glyf")
        g = glyf[gname] if glyf is not None else None
        if g is not None and not g.isComposite() and getattr(g, "coordinates", None):
            pts = list(g.coordinates)
            flags = list(g.flags)
            oncurve = [p for p, fl in zip(pts, flags) if fl & 1]
            cand = oncurve or pts
        else:
            bb = self.glyph_bbox(gname) or (0, 0, 0, 0)
            cand = [(bb[0], bb[1]), (bb[2], bb[1]), (bb[0], bb[3]), (bb[2], bb[3])]
        px, py = max(cand, key=lambda p: score(p[0], p[1]))
        return (xoff + px, py)


def catmull_samples(pts, per_seg=24):
    """Sample a Catmull-Rom spline through `pts` into a dense list of points."""
    if len(pts) < 2:
        return list(pts)
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        last_seg = i == len(p) - 3
        for s in range(per_seg + (1 if last_seg else 0)):
            t = s / per_seg
            t2, t3 = t * t, t * t * t
            x = 0.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * (2 * p1[1] + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    return out


def tapered_outline(samples, w_full, w_end, taper_from):
    """Closed filled-path outline of a ribbon along `samples`: full width until
    `taper_from` of the length, then easing down to `w_end` at the final point."""
    n = len(samples)
    left, right = [], []
    for i, (x, y) in enumerate(samples):
        a = samples[max(0, i - 1)]
        b = samples[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        length = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / length, tx / length          # unit normal
        t = i / (n - 1)
        if t <= taper_from:
            w = w_full
        else:
            u = (t - taper_from) / (1.0 - taper_from)
            ease = u * u * (3 - 2 * u)               # smoothstep, no kink
            w = w_full + ease * (w_end - w_full)
        hw = w / 2.0
        left.append((x + nx * hw, y + ny * hw))
        right.append((x - nx * hw, y - ny * hw))
    d = f"M {left[0][0]:.2f} {left[0][1]:.2f} "
    d += " ".join(f"L {x:.2f} {y:.2f}" for x, y in left[1:])
    d += " " + " ".join(f"L {x:.2f} {y:.2f}" for x, y in reversed(right))
    xs = [p[0] for p in left + right]
    ys = [p[1] for p in left + right]
    return d + " Z", (min(xs), min(ys), max(xs), max(ys))


def trail_path(start, end, base):
    """Winding return path from `start` (the n's tip) under the word to `end`
    (the R's leg tip), so the whole logo reads as one connected line."""
    sx, sy = start
    ex, ey = end
    span = sx - ex
    mid = base + 0.33 * R          # centre of the under-word band (close to the word)
    amp = 0.10 * R                 # how far the wander swings
    pts = [
        (sx, sy),                              # the n's tip, exactly
        (sx + 0.36 * R, sy + 0.06 * R),        # brief wander out to the right
        (sx + 0.20 * R, base + 0.34 * R),      # turn down, under the word
        (ex + 0.78 * span, mid + amp),         # ---- meander leftward ----
        (ex + 0.60 * span, mid - amp),
        (ex + 0.42 * span, mid + amp),
        (ex + 0.25 * span, mid - 0.6 * amp),
        (ex + 0.12 * span, base + 0.20 * R),   # rise toward the R
        (ex, ey),                              # the R's leg tip, exactly
    ]
    samples = catmull_samples(pts)
    return tapered_outline(samples, TRAIL_W, TRAIL_W * TRAIL_END, TAPER_FROM)


def word_svg_bbox(word, x_svg, baseline, size, rotate=0):
    """SVG-space bounding box of a word drawn via Word.outline_group."""
    s = size / word.upm
    a = math.radians(rotate)
    ca, sa = math.cos(a), math.sin(a)
    xs, ys = [], []
    for _, gname, xoff in word.glyphs:
        bb = word.glyph_bbox(gname)
        if bb is None:
            continue
        for gx in (bb[0], bb[2]):
            for gy in (bb[1], bb[3]):
                px, py = s * (xoff + gx), -s * gy              # scale(s, -s)
                rx, ry = px * ca - py * sa, px * sa + py * ca  # rotate
                xs.append(x_svg + rx)
                ys.append(baseline + ry)
    return (min(xs), min(ys), max(xs), max(ys))


def panel(label, ttf, text, base):
    ramblin = Word(ttf, text)
    scale_r = R / ramblin.upm

    g_ramblin = ramblin.outline_group(X0, base, R, COL_RAMBLIN)

    # Shared dot, located on the "i" tittle.
    i_gname, i_x = ramblin.glyph_of("i")
    tb = ramblin.tittle_bbox(i_gname)
    if tb:
        tcx, tcy = (tb[0] + tb[2]) / 2, (tb[1] + tb[3]) / 2
        dot_cx = X0 + (i_x + tcx) * scale_r
        dot_cy = base - tcy * scale_r
        dot_r = max(tb[2] - tb[0], tb[3] - tb[1]) / 2 * scale_r + 3
        note = "tittle contour"
    else:
        bb = ramblin.glyph_bbox(i_gname)
        dot_cx = X0 + (i_x + (bb[0] + bb[2]) / 2) * scale_r
        dot_cy = base - bb[3] * 0.92 * scale_r
        dot_r = 0.085 * R
        note = "fallback (no separate tittle)"
    dot_r -= DOT_SHRINK  # the dot reads better a touch smaller

    # "dev": baseline sits at the dot, reading to its right.
    dev = Word(ttf, "dev")
    dev_x = dot_cx + dot_r + 10
    g_dev = dev.outline_group(dev_x, dot_cy, DEV, COL_DEV, rotate=DEV_ROTATE)

    # Trailing path: from the n's right tip, under the word, into the R's leg tip.
    def to_svg(pt):
        return (X0 + pt[0] * scale_r, base - pt[1] * scale_r)

    n_tip = to_svg(ramblin.extreme("n", lambda x, y: x))
    r_foot = to_svg(ramblin.extreme(text[0], lambda x, y: x - y))
    n_tip = (n_tip[0], n_tip[1] + N_TIP_DY)
    r_foot = (r_foot[0], r_foot[1] + R_FOOT_DY)
    trail_d, trail_bbox = trail_path(n_tip, r_foot, base)
    path = f'<path d="{trail_d}" fill="{COL_RAMBLIN}"/>'

    dot = f'<circle cx="{dot_cx:.1f}" cy="{dot_cy:.1f}" r="{dot_r:.1f}" fill="{COL_DOT}"/>'
    label_el = f'<text x="{X0}" y="{base - 212:.0f}" class="label">{label.upper()}</text>'

    print(f"  {label}: dot=({dot_cx:.0f},{dot_cy:.0f}) [{note}]  "
          f"n_tip=({n_tip[0]:.0f},{n_tip[1]:.0f})  "
          f"r_foot=({r_foot[0]:.0f},{r_foot[1]:.0f})")

    # tight bounding box of the logo: lettering + dev + trail + dot
    boxes = [
        word_svg_bbox(ramblin, X0, base, R),
        word_svg_bbox(dev, dev_x, dot_cy, DEV, DEV_ROTATE),
        trail_bbox,
        (dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r),
    ]
    bbox = (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))

    # path behind the lettering; dot on top
    logo = "\n  ".join([path, g_ramblin, g_dev, dot])
    return {
        "labelled": "\n  ".join([label_el, logo]),
        "logo": logo,
        "bbox": bbox,
    }


def verify(svg_path):
    """Sanity-check the written SVG: confirm it parses and report element counts."""
    try:
        doc = xml.dom.minidom.parse(svg_path)
    except Exception as exc:  # report any parse failure rather than failing silently
        print(f"  WARNING: output is not well-formed XML: {exc}")
        return
    n_path = len(doc.getElementsByTagName("path"))
    n_circle = len(doc.getElementsByTagName("circle"))
    print(f"  well-formed SVG · {n_path} paths · {n_circle} circles")


def build():
    print(f"  palette: ramblin {COL_RAMBLIN} · dev {COL_DEV} · dot {COL_DOT}")
    width = 1100
    panels = []
    for i, (label, fname, text) in enumerate(PANELS):
        ttf = font_path(fname, FONTS[fname])
        panels.append(panel(label, ttf, text, BASE0 + i * PANEL_H))

    # Review mockup: the logo on white, then again on a dark band so the
    # white-rimmed dot can be checked against a dark background.
    light_h = BASE0 + (len(PANELS) - 1) * PANEL_H + 220
    band_h = 320
    height = light_h + band_h
    _, by0, _, by1 = panels[0]["bbox"]
    band_dy = (light_h + band_h / 2) - (by0 + by1) / 2

    mockup = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="ramblin.dev logo composition mockup">
  <title>ramblin.dev — logo composition mockup (real font outlines)</title>
  <defs>
    <style>
      .label {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 16px; fill: #9a9a9a; letter-spacing: 0.09em; }}
    </style>
  </defs>
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  <rect x="0" y="{light_h}" width="{width}" height="{band_h}" fill="#1e1e22"/>
  <text x="{X0}" y="44" class="label" style="fill:#20424a;font-size:17px">ramblin.dev — logo composition mockup &#183; real font outlines, metric-placed</text>
  {"".join(chr(10) + "  " + p["labelled"] for p in panels)}
  <text x="{X0}" y="{light_h + 42:.0f}" class="label">ON A DARK BACKGROUND</text>
  <g transform="translate(0 {band_dy:.1f})">{panels[0]["logo"]}</g>
</svg>
"""
    with open(OUT, "w") as f:
        f.write(mockup)
    print(f"wrote {OUT}")
    verify(OUT)

    # Clean logo: cropped to its bounding box, transparent, no label or title.
    x0, y0, x1, y1 = panels[0]["bbox"]
    m = LOGO_MARGIN
    view = f"{x0 - m:.1f} {y0 - m:.1f} {x1 - x0 + 2 * m:.1f} {y1 - y0 + 2 * m:.1f}"
    logo_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img" aria-label="ramblin.dev">
  <title>ramblin.dev</title>
  {panels[0]["logo"]}
</svg>
"""
    with open(OUT_LOGO, "w") as f:
        f.write(logo_svg)
    print(f"wrote {OUT_LOGO}")
    verify(OUT_LOGO)


if __name__ == "__main__":
    build()
