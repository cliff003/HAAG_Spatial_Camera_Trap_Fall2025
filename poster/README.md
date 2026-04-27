# HAAG Conference Poster — "Field Guide"

Editable 24" × 36" portrait conference poster inspired by Jenny McGuire's
2025 GRC poster and the aesthetic of classic natural-history field guides
and Smithsonian mammal plates.

```bash
python poster/make_poster.py
```

Open [poster.pptx](poster.pptx) in PowerPoint / Keynote / LibreOffice
Impress. Native vector throughout — no rasterized text.

## Design concept

**Warm aged paper, ink silhouettes, naturalist accents.** Inspired by:

- **Asymmetric title + hero figure** — no centered header band; the BIG
  research-question title sits top-right, the compact author/affiliation
  block sits top-left. Reads like a Nature cover rather than a lab report.
- **Numbered ribbon tags ①–⑥** — each section has an INDIGO circled
  numeral hanging off the left edge of a parchment-colored title bar
  with a thin IRON outline. Scannable, gives the poster rhythm.
- **Body-Mass Strata strip** — a full-width horizontal strip with five
  colored tabs (≤50 g → ≥1000 g) replaces McGuire's "Studied Periods"
  historical timeline. Shows the stratification at a glance.
- **Visual equation in Results** — "[SAC figure] + [CI-gap figure] =
  [Headline 2×2]" with giant TERRACOTTA `+` and `=` symbols. The math
  of the method made visible.
- **Silhouette placeholders** scattered in margin areas and inside the
  strata strip. Replace with grayscale PhyloPic CC-0 mammal outlines.
- **Field-plate illustration slot** at the bottom-right — for a small
  vintage-style natural-history illustration.

## Layout

```
+------------------------------------------------------------+  y=0
| GA TECH · HAAG   Spatial Camera-Trap Audit | DO CAMERAS AND|
| Cliff [surname] · Kefei · Jacquie · Neel.  | RANGE MAPS SEE|  header
| Advisors: McGuire · Mussmann · Weigel      | THE SAME      |  3.65
| [OMSCS 2026]                               | BIODIVERSITY? |
+--------------------------------+---------------------------+
|①|ribbon tag: Motivation       |                           |
| body... body... body...       |    HERO VISUAL            |
|                                |    (SSUSA ∩ IUCN map)     |
| | pull-quote research question |                           |
|                                |                           |
+--------------------------------+---------------------------+
|②|ribbon tag: Data Sources                                 |
| SSUSA | IUCN | COMBINE                                     |
+------------------------------------------------------------+
|③|ribbon tag: Body-Mass Strata                             |
| [≤50g] → [50-100g] → [100-500g] → [500-1000g] → [≥1000g]   |
+------------------------------------------------------------+
|④|ribbon tag: Results                                      |
|                                                            |
| [SAC fig]  +  [CI-gap fig]  =  ┌─ 4.4% misclassified ──┐   |
|                                │  [HEADLINE FIGURE]    │   |
|                                └───────────────────────┘   |
+--------------------------------+---------------------------+
|⑤|Supporting Analysis          |⑥|Takeaways & Next Steps  |
| body...                        | ▪ bullet 1               |
| [SUPPORTING FIG]               | ▪ bullet 2               |
|                                | ▪ bullet 3     [FIELD    |
|                                | github.com/...  PLATE]  |
|                                |            [QR]          |
+------------------------------------------------------------+
|                  [palette swatch strip]                    |  footer
|  Institution |  Conference · Session  |  email  | v0.4.0   |
+------------------------------------------------------------+
```

## Palette — "Field Guide"

Defined once in [palette.py](palette.py) as hex strings and RGB tuples.

| Token      | Hex       | Role                                      |
|------------|-----------|-------------------------------------------|
| PAPER      | `#F6EFD8` | slide background (warm aged paper)        |
| PARCHMENT  | `#E8DEBF` | ribbon-tag backgrounds                    |
| IRON       | `#1F1F1F` | ink — text · silhouettes · rules          |
| INDIGO     | `#1F3A5F` | primary accent · numeral badges           |
| TERRACOTTA | `#C7623C` | highlights · alerts · + / = symbols       |
| FOREST     | `#3F6B3A` | categorical-1                             |
| STRAW      | `#D9B24F` | categorical-2                             |
| SKY        | `#6FA0B8` | categorical-3                             |
| CLAY       | `#B5785A` | categorical-4                             |
| STONE      | `#706A58` | captions · secondary text                 |
| FOG        | `#CFC7AB` | subtle borders · dividers                 |

Plot convention: IRON for axes/text; INDIGO as primary series; TERRACOTTA
to highlight one series; FOREST / STRAW / SKY / CLAY for additional
categories; PAPER as figure `facecolor` so plots sit seamlessly on the
poster.

## matplotlib integration

```python
import matplotlib as mpl
from poster.palette import MPL_RCPARAMS, CATEGORICAL
mpl.rcParams.update(MPL_RCPARAMS)
```

`cycler` ships with matplotlib — no extra dependency.

## Reusing for a different conference

Edit the `Conference metadata` block at the top of
[make_poster.py](make_poster.py):

```python
OUTPUT_FILENAME = "poster.pptx"
CONFERENCE_TAG  = "OMSCS Conference 2026"
AFFILIATION     = "Georgia Institute of Technology · …"
FOOTER_LEFT     = "Human-Augmented Analytics Group · Georgia Tech"
FOOTER_CENTER   = "OMSCS Conference 2026 · Poster & Demo Session · May 12, 2026"
FOOTER_RIGHT    = "[[FILL: presenter email]]"
```

Content lives inside the band builders (`build_header`, `build_top_row`,
`build_data_sources_band`, `build_strata_strip`, `build_results_row`,
`build_bottom_row`) — edit in place for new prose.

## Remaining `[[…]]` markers

| Marker                                          | Location                               |
|-------------------------------------------------|----------------------------------------|
| `[[FILL: surname]]`                             | Author line (header)                   |
| `[[FILL: presenter email]]`                     | Footer, right side                     |
| `[[HERO VISUAL — …]]`                           | Upper-right (hero figure)              |
| `[[FIGURE — SAC completeness curves by strata]]`| Results box A                          |
| `[[FIGURE — CI-gap upper bound by effort]]`     | Results box B                          |
| `[[HEADLINE FIGURE — 2×2 SAC × CI-gap]]`        | Results box C (inside INDIGO callout)  |
| `[[SUPPORTING FIGURE]]`                         | Bottom-left                            |
| `[[QR]]`                                        | Bottom-right takeaways panel           |
| `[[FIELD-PLATE ILLUSTRATION]]`                  | Bottom-right vintage-style slot        |
| `[[SILHOUETTE]]` × 5                            | Strata strip + 3 margin spots          |

## Print spec

- 24 × 36 in portrait
- 300 DPI PDF export
- Bleed = 0 (trim to edge)
- Build stamp (faint gray) in the bottom-right for iteration tracking

## Code layout

- [palette.py](palette.py) — color tokens + `MPL_RCPARAMS`.
- [make_poster.py](make_poster.py) — generator. Flat module; each
  `build_*` composer draws one numbered section or band.
- [__init__.py](__init__.py) — makes `poster` a package so notebooks
  can `from poster.palette import …`.
- [poster.pptx](poster.pptx) — regenerated on every run.

## Credits

Visual language inspired by Jenny L. McGuire's Spatial Ecology and
Paleontology Lab 2025 GRC poster — the ribbon-tag numbering, the
asymmetric hero title, the silhouette marginalia, and the visual-equation
results row are all lifted in spirit from that design.
