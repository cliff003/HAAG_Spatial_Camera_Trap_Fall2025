"""HAAG poster palette — "Field Guide".

Inspired by natural-history field guides and Smithsonian mammal plates.
Warm aged-paper ground with ink-black text and silhouettes, muted
naturalist accents for data. Meant to stand out at conferences full of
slick corporate-blue posters without resorting to saturated primaries.

Imported by `make_poster.py` and by downstream plotting notebooks:

    import matplotlib as mpl
    from poster.palette import MPL_RCPARAMS
    mpl.rcParams.update(MPL_RCPARAMS)
"""

from cycler import cycler


# -- 11-token palette --
PAPER      = "#F6EFD8"  # warm aged paper — slide background
PARCHMENT  = "#E8DEBF"  # slightly darker parchment — ribbon tags
IRON       = "#1F1F1F"  # near-black ink — text, silhouettes, rules
INDIGO     = "#1F3A5F"  # deep naturalist blue — primary accent, numerals
TERRACOTTA = "#C7623C"  # warm red-orange — highlights, alerts, + / =
FOREST     = "#3F6B3A"  # forest green — categorical
STRAW      = "#D9B24F"  # warm straw yellow — categorical
SKY        = "#6FA0B8"  # soft dusk sky blue — categorical
CLAY       = "#B5785A"  # warm tan clay — categorical
STONE      = "#706A58"  # warm gray — captions, secondary text
FOG        = "#CFC7AB"  # muted taupe — dividers


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


PAPER_RGB      = _hex_to_rgb(PAPER)
PARCHMENT_RGB  = _hex_to_rgb(PARCHMENT)
IRON_RGB       = _hex_to_rgb(IRON)
INDIGO_RGB     = _hex_to_rgb(INDIGO)
TERRACOTTA_RGB = _hex_to_rgb(TERRACOTTA)
FOREST_RGB     = _hex_to_rgb(FOREST)
STRAW_RGB      = _hex_to_rgb(STRAW)
SKY_RGB        = _hex_to_rgb(SKY)
CLAY_RGB       = _hex_to_rgb(CLAY)
STONE_RGB      = _hex_to_rgb(STONE)
FOG_RGB        = _hex_to_rgb(FOG)

# INK is conceptually the same as IRON — kept as a semantic alias
# so downstream "body text" callers can use INK_RGB without confusion.
INK     = IRON
INK_RGB = IRON_RGB

CATEGORICAL = [INDIGO, TERRACOTTA, FOREST, STRAW, SKY, CLAY]

WHITE     = "#FFFFFF"
WHITE_RGB = (255, 255, 255)


PALETTE_ROLES = [
    ("PAPER",      PAPER,      PAPER_RGB,      "slide background (warm aged paper)"),
    ("PARCHMENT",  PARCHMENT,  PARCHMENT_RGB,  "ribbon-tag backgrounds"),
    ("IRON",       IRON,       IRON_RGB,       "ink — text · silhouettes · rules"),
    ("INDIGO",     INDIGO,     INDIGO_RGB,     "primary accent · numeral badges"),
    ("TERRACOTTA", TERRACOTTA, TERRACOTTA_RGB, "highlights · alerts · + / = symbols"),
    ("FOREST",     FOREST,     FOREST_RGB,     "categorical-1"),
    ("STRAW",      STRAW,      STRAW_RGB,      "categorical-2"),
    ("SKY",        SKY,        SKY_RGB,        "categorical-3"),
    ("CLAY",       CLAY,       CLAY_RGB,       "categorical-4"),
    ("STONE",      STONE,      STONE_RGB,      "captions · secondary text"),
    ("FOG",        FOG,        FOG_RGB,        "subtle borders · dividers"),
]


MPL_RCPARAMS = {
    "figure.facecolor": PAPER,
    "axes.facecolor":   PAPER,
    "axes.edgecolor":   IRON,
    "axes.labelcolor":  IRON,
    "axes.titlecolor":  INDIGO,
    "text.color":       IRON,
    "xtick.color":      IRON,
    "ytick.color":      IRON,
    "axes.prop_cycle":  cycler(color=CATEGORICAL),
    "font.family":      "serif",
    "font.serif":       ["Georgia", "Cambria", "DejaVu Serif"],
    "font.size":        11,
    "axes.grid":        True,
    "grid.color":       FOG,
    "grid.linewidth":   0.5,
}
