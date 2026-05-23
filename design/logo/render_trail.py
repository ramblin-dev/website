# /// script
# requires-python = ">=3.10"
# dependencies = ["fonttools>=4.50"]
# ///
"""Render the trail-r icon mark — lowercase r in gravel-trail tan (Patrick
Hand) with a few minimal green pine trees around it, so the letter doubles
as both an r and a sketched nature trail.

Patrick Hand is a neat hand-printed sans (OFL) — neat enough that the r
reads as a letter, casual enough to read as a hand-sketched trail. The
trail colour is a warm gravel tan so it doesn't read as a tree-trunk or
log. Trees are plain green triangles in the wordmark green, ties the icon
to the wordmark palette.

Output: icon-trail.svg (clean), icon-trail-mockup.svg (proof sheet).
Run:  uv run design/logo/render_trail.py
"""
import os
import urllib.request
import xml.dom.minidom

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = "/tmp/ramblin-logo-fonts"

FONT_URL = ("https://raw.githubusercontent.com/google/fonts/main/"
            "ofl/patrickhand/PatrickHand-Regular.ttf")
FONT_NAME = "Patrick_Hand"

COL_TRAIL = "#ffd79d"          # warm peach gravel trail
COL_TREE = "#3E9D63"           # the wordmark's green — tree foliage
COL_TRUNK = "#5C3A1E"          # dark bark brown — tree trunks
BG_WHITE = "#ffffff"
BG_DARK = "#1e1e22"
INK_MONO = "#1e1e22"           # one-ink fallback (loses the colour meaning)
INK_DARK = "#f4f4f4"

# How large the r fills the 100-box (leaves room for trees around the edges)
R_TARGET = 70

# Tree positions in 100-box: (cx, base_y, height). Foreground trees are
# bigger; the background tree near the arm tip is smaller. The crook tree
# nestles inside the bend of the r so the trail+trees integrate.
TREES = [
    (12, 92, 28),    # lower-left, biggest (foreground, closest to viewer)
    (60, 58, 18),    # in the crook of the r — nudged out for breathing room
    (88, 82, 18),    # lower-right
    (90, 28, 13),    # upper-right, smallest (down the trail, distant)
]


def _cached(name, url):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name + ".ttf")
    if not os.path.exists(p):
        print(f"  downloading {name} ...")
        urllib.request.urlretrieve(url, p)
    return p


def glyph_r(font):
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    pen = SVGPathPen(gs)
    gs[cmap[ord("r")]].draw(pen)
    bp = BoundsPen(gs)
    gs[cmap[ord("r")]].draw(bp)
    return pen.getCommands(), bp.bounds


def pine_paths(cx, by, h, w=None):
    """Stylized 3-tier pine — returns (foliage_path, trunk_path) as two
    separate polygons so the trunk can be coloured distinctly from the
    foliage. Base-centre at (cx, by), total height h (incl. trunk)."""
    if w is None:
        w = h * 0.78
    def px(u):
        return cx + (u - 0.5) * w
    def py(u):
        return by - h + u * h

    Y_TOP_BASE = 0.22
    Y_MID_BASE = 0.55
    Y_BOT_BASE = 0.90
    Y_TRUNK = 1.00

    HW_TOP_BASE = 0.18
    HW_MID_TOP = 0.26        # > HW_TOP_BASE → visible shelf
    HW_MID_BASE = 0.37
    HW_BOT_TOP = 0.45        # > HW_MID_BASE → visible shelf
    HW_BOT_BASE = 0.50
    HW_TRUNK = 0.08

    # Foliage: 3-tier silhouette with a flat bottom edge above the trunk
    foliage_pts = [
        (px(0.5),               py(0.0)),
        (px(0.5 + HW_TOP_BASE), py(Y_TOP_BASE)),
        (px(0.5 + HW_MID_TOP),  py(Y_TOP_BASE)),       # shelf right
        (px(0.5 + HW_MID_BASE), py(Y_MID_BASE)),
        (px(0.5 + HW_BOT_TOP),  py(Y_MID_BASE)),       # shelf right
        (px(0.5 + HW_BOT_BASE), py(Y_BOT_BASE)),
        (px(0.5 - HW_BOT_BASE), py(Y_BOT_BASE)),       # flat bottom
        (px(0.5 - HW_BOT_TOP),  py(Y_MID_BASE)),
        (px(0.5 - HW_MID_BASE), py(Y_MID_BASE)),       # shelf left
        (px(0.5 - HW_MID_TOP),  py(Y_TOP_BASE)),
        (px(0.5 - HW_TOP_BASE), py(Y_TOP_BASE)),       # shelf left
    ]
    foliage_d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in foliage_pts) + " Z"

    # Trunk: small rectangle below the foliage's flat bottom
    tx0, tx1 = px(0.5 - HW_TRUNK), px(0.5 + HW_TRUNK)
    ty0, ty1 = py(Y_BOT_BASE), py(Y_TRUNK)
    trunk_d = (f"M {tx0:.2f} {ty0:.2f} L {tx1:.2f} {ty0:.2f} "
               f"L {tx1:.2f} {ty1:.2f} L {tx0:.2f} {ty1:.2f} Z")
    return foliage_d, trunk_d


def trees_svg(foliage_col, trunk_col):
    parts = []
    for cx, by, h in TREES:
        foliage, trunk = pine_paths(cx, by, h)
        # Trunk drawn first; foliage sits above and never overlaps the trunk.
        parts.append(f'<path d="{trunk}" fill="{trunk_col}"/>')
        parts.append(f'<path d="{foliage}" fill="{foliage_col}"/>')
    return ''.join(parts)


def icon_body(font, trail_col, foliage_col, trunk_col):
    d, b = glyph_r(font)
    x0, y0, x1, y1 = b
    s = R_TARGET / max(x1 - x0, y1 - y0)
    cx, cy = 50, 50
    tx = cx - s * (x0 + x1) / 2
    ty = cy + s * (y0 + y1) / 2
    letter = (f'<g transform="translate({tx:.3f} {ty:.3f}) '
              f'scale({s:.5f} {-s:.5f})"><path d="{d}" fill="{trail_col}"/></g>')
    # Trees first, letter on top — so any overlap reads as the trail in front.
    return trees_svg(foliage_col, trunk_col) + letter


def r_only(font, color):
    d, b = glyph_r(font)
    x0, y0, x1, y1 = b
    s = R_TARGET / max(x1 - x0, y1 - y0)
    cx, cy = 50, 50
    tx = cx - s * (x0 + x1) / 2
    ty = cy + s * (y0 + y1) / 2
    return (f'<g transform="translate({tx:.3f} {ty:.3f}) '
            f'scale({s:.5f} {-s:.5f})"><path d="{d}" fill="{color}"/></g>')


def verify(p):
    try:
        doc = xml.dom.minidom.parse(p)
    except Exception as exc:
        print(f"  WARN: {p}: {exc}")
        return
    n = sum(len(doc.getElementsByTagName(t))
            for t in ("path", "circle", "polygon"))
    print(f"  well-formed SVG · {n} drawn elements · {p}")


def placed(body, x, y, size):
    return f'<g transform="translate({x} {y}) scale({size / 100:.5f})">{body}</g>'


def build():
    font = TTFont(_cached(FONT_NAME, FONT_URL))
    two_color = icon_body(font, COL_TRAIL, COL_TREE, COL_TRUNK)
    ink_dark = r_only(font, INK_DARK)
    ink_white = r_only(font, INK_MONO)

    icon = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
            f'role="img" aria-label="ramblin.dev">\n'
            f'  <title>ramblin.dev</title>\n  {two_color}\n</svg>\n')
    p = os.path.join(HERE, "icon-trail.svg")
    with open(p, "w") as f:
        f.write(icon)
    print(f"wrote {p}")
    verify(p)

    width, height = 1000, 360
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="ramblin.dev trail icon">',
        '  <defs><style>'
        ".lab{font-family:'Helvetica Neue',Arial,sans-serif;fill:#9a9a9a;"
        "font-size:14px;letter-spacing:0.09em}"
        ".big{font-family:'Helvetica Neue',Arial,sans-serif;fill:#20424a;"
        "font-size:18px;letter-spacing:0.04em}"
        '</style></defs>',
        f'  <rect width="{width}" height="{height}" fill="#ffffff"/>',
        '  <text x="60" y="48" class="big">ramblin.dev — trail icon · '
        'Patrick Hand r in gravel-tan with green pines</text>',
    ]
    cy = 80

    out.append(f'  <rect x="60" y="{cy}" width="200" height="200" '
               f'fill="none" stroke="#e3e3e3"/>')
    out.append("  " + placed(two_color, 60, cy, 200))
    out.append(f'  <text x="60" y="{cy + 224}" class="lab">TWO-COLOUR ON WHITE</text>')

    out.append(f'  <rect x="300" y="{cy}" width="200" height="200" fill="#1e1e22"/>')
    out.append("  " + placed(two_color, 300, cy, 200))
    out.append(f'  <text x="300" y="{cy + 224}" class="lab">TWO-COLOUR ON DARK</text>')

    out.append(f'  <text x="560" y="{cy - 8}" class="lab">'
               f'FAVICON SIZES &#8212; 64 / 32 / 16 px (two-colour)</text>')
    ladder = [(64, 0), (32, 80), (16, 132)]
    for s, dx in ladder:
        x = 560 + dx
        out.append(f'  <rect x="{x}" y="{cy}" width="64" height="64" '
                   f'fill="none" stroke="#e3e3e3"/>')
        off = (64 - s) / 2
        out.append("  " + placed(two_color, x + off, cy + off, s))
    for s, dx in ladder:
        x = 560 + dx
        yd = cy + 96
        out.append(f'  <rect x="{x}" y="{yd}" width="64" height="64" fill="#1e1e22"/>')
        off = (64 - s) / 2
        out.append("  " + placed(two_color, x + off, yd + off, s))
    out.append(f'  <text x="560" y="{cy + 90}" class="lab">on white</text>')
    out.append(f'  <text x="560" y="{cy + 174}" class="lab">on dark</text>')

    out.append(f'  <rect x="800" y="{cy}" width="200" height="200" '
               f'fill="none" stroke="#e3e3e3"/>')
    out.append("  " + placed(ink_white, 800, cy, 200))
    out.append(f'  <text x="800" y="{cy + 224}" class="lab">'
               f'ONE-INK FALLBACK &#183; r only</text>')

    out.append("</svg>\n")
    p = os.path.join(HERE, "icon-trail-mockup.svg")
    with open(p, "w") as f:
        f.write("\n".join(out))
    print(f"wrote {p}")
    verify(p)


if __name__ == "__main__":
    build()
