# 🔤 letter-banner

<!-- 
[![CI](https://github.com/Michael-Weber-1/letter-banner/actions/workflows/ci.yml/badge.svg)](https://github.com/Michael-Weber-1/letter-banner/actions)
[![PyPI](https://img.shields.io/pypi/v/letter-banner.svg)](https://pypi.org/project/letter-banner/)
[![Python](https://img.shields.io/pypi/pyversions/letter-banner.svg)](https://pypi.org/project/letter-banner/)
-->
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Generate printable letter banners for any occasion — one big decorative letter per page, saved as HTML and PDF.**

Perfect for birthdays, holidays, school events, weddings, graduations, baby showers, and anything else worth hanging on a wall.

---

## Features

- 🎨 **Three fill modes** — solid colour, outline-only (colour-in), or photo mosaic
- 🖼️ **Photo fill** — point at a single image or a whole folder; photos are randomly assembled inside the letter shape using six layout styles
- 📷 **HEIC/HEIF support** — iPhone photos work out of the box
- 🌈 **16 colour palettes** — easter, christmas, halloween, valentines, pastel, vivid, neon, ocean, warm, cool, rainbow, wedding, graduation, black & gold, and more
- 🔤 **15 font presets** — bold, fun, elegant, kids, retro, handmade, pixel, script, and more — or use any Google Font by name
- ✨ **6 decoration styles** — none, minimal, dots, shapes, festive, confetti
- 📄 **5 paper sizes** — Letter, A4, A3, Legal, Tabloid
- 📦 **Self-contained HTML** — images are base64-embedded, no external assets at print time
- 🖨️ **PDF output** via WeasyPrint
- 🐍 **Clean Python API** + **CLI**

---

## Installation

```bash
# Minimal (HTML output only, no optional dependencies)
pip install letter-banner

# With PDF support
pip install "letter-banner[pdf]"

# With image support (resize + HEIC/HEIF)
pip install "letter-banner[image]"
# or
pip install "letter-banner[heic]"

# Everything
pip install "letter-banner[all]"
```

> **PDF on Windows** (recommended): install **pdfkit + wkhtmltopdf**
> ```
> pip install pdfkit
> ```
> Then download and install **wkhtmltopdf** from [wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html) and restart your terminal.
>
> **PDF on macOS / Linux** (recommended): install **WeasyPrint**
> ```
> pip install weasyprint
> brew install pango          # macOS
> sudo apt install libpango-1.0-0 libpangocairo-1.0-0   # Linux
> ```
>
> Both backends can be installed at the same time — WeasyPrint is tried first,
> pdfkit is the automatic fallback.

---

## Quick start

### CLI

```bash
# ── Shortcuts (single flag does everything) ───────────────────────────────

# --clean (-C)       outline only, transparent background, no decoration
letter-banner "HELLO" --clean

# --clean-white (-W) outline only, white background, no decoration — print & colour in
letter-banner "KIDS" --clean-white

# --filled (-F)      solid colour letter, white background, no decoration
letter-banner "SPRING" --filled --palette easter

# ── Common examples ───────────────────────────────────────────────────────

# Colour fill with decoration
letter-banner "HAPPY BIRTHDAY" --palette vivid --deco festive

# Outline with a custom colour
letter-banner "KIDS" --mode outline --outline-color "#6600cc" --font kids

# Photo fill — single image
letter-banner "LOVE" --mode image --images rose.jpg

# Photo fill — folder of photos (randomly sampled per letter)
letter-banner "PARTY" --mode image --images ./my-photos/ --grid mosaic

# A4 paper, elegant font
letter-banner "FROHE OSTERN" --paper A4 --font elegant

# Clean letter, override outline colour and font
letter-banner "EASTER" --clean-white --outline-color "#e03060" --font fun --paper A4

# See all options
letter-banner --help
letter-banner --list-palettes
letter-banner --list-fonts
```

### Python API

```python
from letter_banner import BannerConfig, save_banner

# Colour fill
save_banner("HAPPY BIRTHDAY", BannerConfig(palette_name="vivid", decoration="festive"))

# Outline
save_banner("HELLO", BannerConfig(mode="outline", outline_color="#ff0088"))

# Photo fill from a folder
save_banner(
    "SUMMER",
    BannerConfig(mode="image", image_source="./photos/", grid_style="mosaic"),
)
```

---

## Modes

### `color` (default)

Each letter page gets a background + bold filled letter drawn from the active palette.  
Palette colours cycle across letters so consecutive pages always differ.

```bash
letter-banner "EASTER" --palette easter --deco festive
letter-banner "XMAS" --palette christmas --font chunky
```

### `outline`

The letter interior is **transparent** — perfect as a colouring-in page or for
a minimalist look.

```bash
letter-banner "COLOR ME" --mode outline --outline-color "#222222" --outline-bg "#ffffff"
letter-banner "SPRING" --mode outline --outline-color "#cc0055" --outline-bg "#fff0f4"
```

| Option | Default | Description |
|---|---|---|
| `--outline-color` | `#222222` | Stroke colour |
| `--outline-width` | `16` | Stroke width in px |
| `--outline-bg` | `#ffffff` | Page background colour |

### `image`

Each letter becomes a window into a **photo collage**.  
Point at a single photo or an entire folder — photos are randomly sampled and
arranged inside the letter using the chosen grid style.

```bash
# Single photo
letter-banner "LOVE" --mode image --images rose.jpg --grid single

# Folder — mosaic layout (recommended)
letter-banner "PARTY" --mode image --images ./photos/ --grid mosaic

# Reproducible shuffle (same seed = same layout every run)
letter-banner "WOW" --mode image --images ./photos/ --image-seed 42
```

#### Grid / layout styles

| Style | Description |
|---|---|
| `single` | One photo fills the entire letter |
| `grid` | Best-fit rectangular grid |
| `strips_h` | Horizontal photo strips |
| `strips_v` | Vertical photo strips |
| `diagonal` | Diagonal bands |
| `mosaic` | Asymmetric magazine-style layout (default) |
| `random` | Randomly picks a different style per letter |

---

## Letter-only output (no background, no decoration)

Three shortcuts handle the most common clean-output scenarios in a single flag:

| Shortcut | Short | What it does |
|---|---|---|
| `--clean` | `-C` | Outline letter, **transparent** background, no decoration |
| `--clean-white` | `-W` | Outline letter, **white** background, no decoration |
| `--filled` | `-F` | Solid colour letter, **white** background, no decoration |

```bash
# Transparent — letter shape only, ideal for overlays / compositing
letter-banner "HELLO" --clean

# White page — print and colour in, or use as a stencil template
letter-banner "HELLO" --clean-white

# Change the outline colour or font after the shortcut
letter-banner "KIDS" --clean-white --outline-color "#6600cc" --font kids

# Solid colour, no clutter
letter-banner "SPRING" --filled --palette easter

# A4 colouring-in sheet
letter-banner "EASTER" --clean-white --paper A4 --font fun
```

Shortcuts set sensible defaults but **any individual flag that follows overrides them**:

```bash
# --clean sets transparent bg, but we override it to light pink
letter-banner "LOVE" --clean --page-bg "#fff0f4"
```

**Python API — letter-only:**

```python
from letter_banner import BannerConfig, save_banner

# Transparent background (letter outline only)
save_banner(
    "HELLO",
    BannerConfig(
        mode        = "outline",
        page_bg     = "transparent",
        decoration  = "none",
        dot_opacity = 0,
    ),
)

# White background — colouring-in page
save_banner(
    "KIDS",
    BannerConfig(
        mode          = "outline",
        page_bg       = "#ffffff",
        decoration    = "none",
        dot_opacity   = 0,
        outline_color = "#6600cc",
        outline_width = 20,
        font          = "kids",
    ),
)

# Solid colour, white page, no decoration
save_banner(
    "SPRING",
    BannerConfig(
        mode         = "color",
        palette_name = "easter",
        page_bg      = "#ffffff",
        decoration   = "none",
        dot_opacity  = 0,
    ),
)
```

> **See also:** `examples/letter_only.py` for a full set of letter-only examples
> with inline CLI equivalents for every variant.

> **Tip:** `--page-bg` accepts any CSS colour — hex (`#ffffff`),
> named colours (`white`, `transparent`), or `rgb()`/`hsl()` strings.

---

## Palettes

Use `letter-banner --list-palettes` to see them all.

| Palette | Occasion / mood |
|---|---|
| `easter` | Spring pastels — pinks, greens, yellows, purples |
| `christmas` | Reds and greens |
| `halloween` | Dark oranges, blacks, purples |
| `halloween_kids` | Bright, fun Halloween |
| `valentines` | Pinks and reds |
| `pastel` | Soft, muted tones — any occasion |
| `vivid` | Bold, saturated primaries |
| `neon` | Dark backgrounds with glowing fills |
| `warm` | Oranges and ambers |
| `cool` | Blues, teals, purples |
| `ocean` | Blues and aquas |
| `rainbow` | Full spectrum, one colour per letter |
| `monochrome` | Greys — minimalist |
| `black_gold` | Dark background with gold fills |
| `wedding` | Creams, ivory, blush |
| `graduation` | Black, gold, navy |

### Custom palette

```python
from letter_banner import BannerConfig, Theme, save_banner

themes = [
    Theme(bg="#0a0a0a", dot="#ff00ff", fill="#ee00cc", stroke="#880077", accent="#ff88ff"),
    Theme(bg="#050510", dot="#00ffff", fill="#00ccff", stroke="#006699", accent="#88eeff"),
    Theme(bg="#0a0a00", dot="#ffff00", fill="#ffcc00", stroke="#886600", accent="#ffee88"),
]
save_banner("NEON", BannerConfig(palette_override=themes, decoration="confetti"))
```

---

## Fonts

Use `letter-banner --list-fonts` to see all presets.

| Key | Google Font | Style |
|---|---|---|
| `bold` | Lilita One | Rounded bold — default |
| `fun` | Boogaloo | Playful informal |
| `chunky` | Fredoka One | Chunky rounded |
| `retro` | Righteous | 70s retro feel |
| `elegant` | Playfair Display | Serif — weddings, formal |
| `handmade` | Pacifico | Brush script |
| `kids` | Baloo 2 | Friendly, child-oriented |
| `modern` | Nunito | Clean sans-serif |
| `comic` | Patrick Hand | Hand-drawn look |
| `rounded` | Varela Round | Soft geometric |
| `display` | Abril Fatface | Heavy display serif |
| `slab` | Alfa Slab One | Bold slab serif |
| `script` | Dancing Script | Flowing script |
| `pixel` | Press Start 2P | 8-bit pixel style |
| `condensed` | Barlow Condensed | Tall, narrow |

Use **any Google Font** by passing its exact family name:

```bash
letter-banner "HELLO" --font "Baloo Bhaijaan 2"
```

---

## Decorations

| Style | Description |
|---|---|
| `none` | Plain background + polka-dot texture only |
| `minimal` | Subtle corner accent blobs |
| `dots` | Corner blobs + 8 scattered shapes |
| `shapes` | Corner blobs + 16 mixed shapes (circles, diamonds, stars, rings) |
| `festive` | 24 shapes + large corner blobs + confetti strips |
| `confetti` | Corner blobs + small shapes + dense confetti edge strips |

---

## Paper sizes

| Key | Dimensions |
|---|---|
| `letter` | 8.5 × 11 in (US Letter) — default |
| `A4` | 210 × 297 mm |
| `A3` | 297 × 420 mm |
| `legal` | 8.5 × 14 in |
| `tabloid` | 11 × 17 in |

---

## Full CLI reference

```
usage: letter-banner [-h] [--mode {color,outline,image}]
                     [--palette NAME] [--images FILE_OR_DIR]
                     [--grid {single,grid,strips_h,strips_v,diagonal,mosaic,random}]
                     [--image-max-dim PX] [--image-seed INT]
                     [--outline-color HEX] [--outline-width PX] [--outline-bg HEX]
                     [--font PRESET_OR_NAME] [--font-size FRACTION]
                     [--deco {none,minimal,dots,shapes,festive,confetti}]
                     [--dot-opacity 0-1] [--paper {letter,A4,A3,legal,tabloid}]
                     [--output BASENAME] [--no-html] [--no-pdf]
                     [--page-bg CSS_COLOUR]
                     [--title TITLE] [--label]
                     [--list-palettes] [--list-fonts]
                     [text]
```

---

## Full Python API reference

### `BannerConfig`

```python
@dataclass
class BannerConfig:
    # Fill mode
    mode: Literal["color", "outline", "image"] = "color"

    # Colour
    palette_name:     str         = "pastel"
    palette_override: list[Theme] = []       # overrides palette_name

    # Image options
    image_source:  str | Path | None = None  # file or folder
    grid_style:    GridStyle         = "mosaic"
    image_max_dim: int               = 1400
    image_seed:    int | None        = None  # for reproducibility

    # Outline options
    outline_color: str = "#222222"
    outline_width: int = 16
    outline_bg:    str = "#ffffff"

    # Typography
    font:      str   = "bold"   # preset key or Google Font name
    font_size: float = 0.82     # fraction of page height

    # Decorations
    decoration:  str   = "dots"
    dot_opacity: float = 0.15

    # Page
    paper: str = "letter"

    # Page background override
    page_bg: str = ""          # "" = palette default; any CSS colour overrides it

    # Extras
    show_label:     bool = False
    label_override: str  = ""
```

### `Theme`

```python
@dataclass
class Theme:
    bg:     str   # page background hex colour
    dot:    str   # polka-dot texture hex colour
    fill:   str   # letter fill hex colour
    stroke: str   # letter stroke / outline hex colour
    accent: str   # decoration accent hex colour
```

### Functions

```python
# Generate HTML string
html: str = generate_html(text, cfg, title="")

# Render HTML to PDF (requires WeasyPrint)
generate_pdf(html, "output.pdf")

# All-in-one: generate + write files
saved: dict = save_banner(
    text,
    cfg,
    output_basename="my_banner",   # default: slugified text
    write_html=True,
    write_pdf=True,
    title="",
)
# saved == {"html": Path("my_banner.html"), "pdf": Path("my_banner.pdf")}

# Palette helpers
list_palettes() -> list[str]
get_palette("vivid") -> list[Theme]

# Font helpers
list_fonts() -> list[str]
resolve_font("kids") -> "Baloo 2"
```

---

## Printing

1. Open the generated `.html` file in any browser (Chrome, Firefox, Safari).
2. **File → Print** (or `Ctrl+P` / `Cmd+P`).
3. Set:
   - Paper size to match your chosen `--paper` option.
   - Margins: **None**.
   - Background graphics: **On** (important for colour fill mode).
4. Print or save as PDF.

For best results with colour pages, use a colour printer and matte or glossy
paper.  Outline / `--clean-white` pages work great on plain paper for colouring-in
and can be used as stencil templates.

---

## Recipes

```bash
# Birthday banner, kids font, festive decoration
letter-banner "HAPPY BIRTHDAY EMMA" --palette vivid --font kids --deco festive

# Easter in German, A4 paper
letter-banner "FROHE OSTERN" --palette easter --paper A4

# Minimal wedding favour tags
letter-banner "MR AND MRS SMITH" --palette wedding --font elegant --deco minimal

# ── Letter-only shortcuts ─────────────────────────────────────────────────────

# Colouring-in pages for kids — one command
letter-banner "BOO" --clean-white --outline-color "#550077" --font fun

# Transparent letter — overlay on a photo or coloured card
letter-banner "JOY" --clean

# Stencil template — thin outline, condensed font, easy to cut out
letter-banner "CUT" --clean-white --outline-width 8 --font condensed

# Solid colour, no clutter, A4
letter-banner "SPRING" --filled --palette easter --paper A4

# ── Photo banners ─────────────────────────────────────────────────────────────

# Photo banner from iPhone photos (HEIC)
letter-banner "JUNE" --mode image --images ./iphone-photos/ --grid mosaic --deco festive

# Same output every time (useful for CI / automation)
letter-banner "TEST" --mode image --images ./photos/ --image-seed 99
```

---

## Development

```bash
git clone https://github.com/Michael-Weber-1/letter-banner.git
cd letter-banner
pip install -e ".[dev]"
pytest
ruff check letter_banner/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add palettes, fonts, and
decoration styles.

---

## License

[MIT](LICENSE) © letter-banner contributors
