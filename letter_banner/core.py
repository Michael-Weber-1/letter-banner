"""
letter_banner.core
~~~~~~~~~~~~~~~~~~
Core generation logic: BannerConfig dataclass, HTML / PDF builders,
and the high-level ``save_banner`` convenience function.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Optional

from .decorations import DECORATION_STYLES, build_svg_decoration
from .fonts import (
    PAPER_SIZES,
    google_fonts_url,
    resolve_font,
)
from .images import (
    DEFAULT_MAX_DIM,
    GRID_STYLES,
    GridStyle,
    build_svg_image_letter,
    load_images,
)
from .palettes import PALETTES, Theme, get_palette

# ---------------------------------------------------------------------------
# BannerConfig
# ---------------------------------------------------------------------------


@dataclass
class BannerConfig:
    """
    Full configuration for a letter banner.

    All fields have sensible defaults — you can construct one with zero
    arguments and pass it straight to :func:`save_banner`.
    """

    # ── Fill mode ────────────────────────────────────────────────────────────
    mode: Literal["color", "outline", "image"] = "color"
    """
    How each letter is filled:

    ``"color"``
        Solid fill drawn from the active colour palette.
    ``"outline"``
        Transparent interior, stroke only.
    ``"image"``
        Letter interior is a photo mosaic / collage.
    """

    # ── Colour ───────────────────────────────────────────────────────────────
    palette_name:     str         = "pastel"
    """Named palette from :data:`letter_banner.palettes.PALETTES`."""

    palette_override: list[Theme] = field(default_factory=list)
    """Supply your own :class:`~letter_banner.palettes.Theme` list."""

    # ── Image options (mode == "image") ──────────────────────────────────────
    image_source:  Optional[str | Path] = None
    """Path to an image file **or** a folder containing images."""

    grid_style:    GridStyle = "mosaic"
    """Photo layout inside each letter.  One of :data:`~letter_banner.images.GRID_STYLES`."""

    image_max_dim: int = DEFAULT_MAX_DIM
    """Resize images so their longest edge does not exceed this value (pixels)."""

    image_seed:    Optional[int] = None
    """Seed for shuffling the image pool.  ``None`` → random each run."""

    # ── Outline options (mode == "outline") ──────────────────────────────────
    outline_color: str = "#222222"
    """Stroke colour for outline mode."""

    outline_width: int = 16
    """Stroke width in pixels for outline mode."""

    outline_bg:    str = "#ffffff"
    """Page background colour for outline mode."""

    # ── Typography ───────────────────────────────────────────────────────────
    font: str = "bold"
    """
    Font preset key (e.g. ``"fun"``, ``"kids"``) **or** a direct
    `Google Fonts <https://fonts.google.com>`_ family name (e.g.
    ``"Baloo Bhaijaan 2"``).
    """

    font_size: float = 0.82
    """Letter height as a fraction of the page height (0 < font_size ≤ 1)."""

    # ── Decorations ──────────────────────────────────────────────────────────
    decoration: str = "dots"
    """
    Background decoration style.  One of:
    ``"none"``, ``"minimal"``, ``"dots"``, ``"shapes"``, ``"festive"``, ``"confetti"``.
    """

    dot_opacity: float = 0.15
    """Opacity of the polka-dot texture layer (0 = invisible)."""

    # ── Page layout ──────────────────────────────────────────────────────────
    paper: str = "letter"
    """Paper size key.  One of: ``"letter"``, ``"A4"``, ``"A3"``, ``"legal"``, ``"tabloid"``."""

    # ── Page background override ─────────────────────────────────────────────
    page_bg: str = ""
    """
    Override the page background colour for every letter page.
    Any CSS colour works: ``"#ffffff"``, ``"white"``, ``"transparent"``.
    Default ``""`` uses the palette theme ``bg`` colour.
    Use ``"transparent"`` with ``decoration="none"`` and ``dot_opacity=0``
    to produce a page that contains nothing but the letter itself.
    """

    # ── Extras ───────────────────────────────────────────────────────────────
    show_label:  bool = False
    """Print a small caption with the letter character at the bottom of each page."""

    label_override: str = ""
    """Override the caption text for every page (useful for single-character banners)."""

    def validate(self) -> None:
        """Raise ``ValueError`` for invalid configuration."""
        if self.mode not in ("color", "outline", "image"):
            raise ValueError(f"Invalid mode: {self.mode!r}")
        if self.mode == "image" and not self.image_source:
            raise ValueError("mode='image' requires image_source to be set.")
        if self.paper not in PAPER_SIZES:
            avail = ", ".join(PAPER_SIZES)
            raise ValueError(f"Unknown paper size {self.paper!r}.  Available: {avail}")
        if self.decoration not in DECORATION_STYLES:
            avail = ", ".join(DECORATION_STYLES)
            raise ValueError(f"Unknown decoration {self.decoration!r}.  Available: {avail}")
        if not (0 < self.font_size <= 1):
            raise ValueError(f"font_size must be between 0 and 1, got {self.font_size}.")


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

_PAGE_CSS = """\
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: #d8d8d8;
  font-family: var(--lb-font), 'Lilita One', Impact, Arial Black, sans-serif;
}

.lb-page {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  page-break-after: always;
  break-after: page;
  flex-shrink: 0;
}

/* Polka-dot texture */
.lb-page::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, var(--lb-dot, #ccc) 5px, transparent 5px);
  background-size: 44px 44px;
  opacity: var(--lb-dot-opacity, 0.15);
  pointer-events: none;
  z-index: 0;
}

.lb-letter-wrap {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lb-letter {
  text-align: center;
  user-select: none;
  line-height: 1;
}

.lb-label {
  position: absolute;
  bottom: 18px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 20px;
  opacity: 0.45;
  z-index: 3;
  white-space: nowrap;
}

@media print {
  html, body { background: white; margin: 0; padding: 0; }
  .lb-page {
    width: 100vw !important;
    height: 100vh !important;
    page-break-after: always;
    break-after: page;
    break-inside: avoid;
  }
}

@media screen {
  body {
    padding: 28px;
    display: flex;
    flex-direction: column;
    gap: 28px;
    align-items: center;
    min-height: 100vh;
  }
  .lb-page {
    border-radius: 10px;
    box-shadow: 0 6px 40px rgba(0, 0, 0, 0.22);
    max-width: calc(100vw - 56px);
  }
}
"""


def _build_page_html(
    letter:      str,
    idx:         int,
    cfg:         BannerConfig,
    palette:     list[Theme],
    font_family: str,
    data_urls:   list[str],
    w_in:        float,
    h_in:        float,
) -> str:
    theme = palette[idx % len(palette)]

    # Page background + dot colour
    _default_bg = theme.bg if cfg.mode != "outline" else cfg.outline_bg
    bg           = cfg.page_bg if cfg.page_bg else _default_bg
    dot_color = theme.dot       if cfg.mode != "outline" else "#cccccc"
    lbl_color = theme.stroke    if cfg.mode != "outline" else cfg.outline_color

    # ── Decoration SVG ───────────────────────────────────────────────────────
    deco = build_svg_decoration(
        style=cfg.decoration, theme=theme,
        w_in=w_in, h_in=h_in, idx=idx,
    )

    # ── Letter element ───────────────────────────────────────────────────────
    if cfg.mode == "image":
        letter_html = build_svg_image_letter(
            letter=letter, data_urls=data_urls,
            grid_style=cfg.grid_style, font_family=font_family,
            w_in=w_in, h_in=h_in, idx=idx,
        )
        wrap_html = letter_html   # SVG is absolutely positioned

    elif cfg.mode == "outline":
        letter_div = (
            f'<div class="lb-letter" style="'
            f'-webkit-text-stroke:{cfg.outline_width}px {cfg.outline_color};'
            f'color:transparent;'
            f'font-size:{cfg.font_size * 100:.1f}vh;">'
            f'{letter}</div>'
        )
        wrap_html = f'<div class="lb-letter-wrap">{letter_div}</div>'

    else:  # color
        letter_div = (
            f'<div class="lb-letter" style="'
            f'-webkit-text-stroke:14px {theme.stroke};'
            f'color:{theme.fill};'
            f'filter:drop-shadow(0 10px 0 {theme.stroke});'
            f'font-size:{cfg.font_size * 100:.1f}vh;">'
            f'{letter}</div>'
        )
        wrap_html = f'<div class="lb-letter-wrap">{letter_div}</div>'

    # ── Optional label ───────────────────────────────────────────────────────
    label_html = ""
    if cfg.show_label:
        label_text = cfg.label_override or letter
        label_html = (
            f'<div class="lb-label" style="color:{lbl_color};">'
            f'{label_text}</div>'
        )

    page_style = (
        f"background:{bg};"
        f"--lb-dot:{dot_color};"
        f"--lb-dot-opacity:{cfg.dot_opacity:.3f};"
        f"width:{w_in}in;height:{h_in}in;"
    )

    return (
        f'<div class="lb-page" style="{page_style}">'
        f'{deco}{wrap_html}{label_html}</div>'
    )


def generate_html(
    text:  str,
    cfg:   Optional[BannerConfig] = None,
    *,
    title: str = "",
) -> str:
    """
    Build a complete, self-contained HTML document with one page per letter.

    Parameters
    ----------
    text  : Input string.  Spaces are skipped; each other character → one page.
    cfg   : :class:`BannerConfig` instance.  Uses defaults when ``None``.
    title : ``<title>`` tag content.  Defaults to ``text.upper()``.

    Returns
    -------
    str
        Complete HTML document as a string, ready to write to a ``.html`` file
        or pass to :func:`generate_pdf`.
    """
    if cfg is None:
        cfg = BannerConfig()
    cfg.validate()

    palette     = cfg.palette_override if cfg.palette_override else get_palette(cfg.palette_name)
    font_family = resolve_font(cfg.font)
    w_in, h_in  = PAPER_SIZES[cfg.paper]

    # Pre-load images once (only for image mode)
    data_urls: list[str] = []
    if cfg.mode == "image":
        data_urls = load_images(
            cfg.image_source,
            max_dim=cfg.image_max_dim,
            shuffle=True,
            seed=cfg.image_seed,
        )

    letters = [ch for ch in text.upper() if not ch.isspace()]
    if not letters:
        raise ValueError("text contains no printable characters.")

    pages = [
        _build_page_html(ch, i, cfg, palette, font_family, data_urls, w_in, h_in)
        for i, ch in enumerate(letters)
    ]

    # Google Fonts
    extra_fonts = []
    if font_family != "Lilita One":
        extra_fonts.append("Lilita One")   # always available as fallback
    gf_url = google_fonts_url(font_family, *extra_fonts)

    doc_title = title or text.upper()
    font_css   = font_family.replace("'", "\\'")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{doc_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{gf_url}" rel="stylesheet">
  <style>
    :root {{ --lb-font: '{font_css}'; }}
    {_PAGE_CSS}
  </style>
</head>
<body>
{"".join(pages)}
</body>
</html>"""


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------

def _pdf_via_weasyprint(html: str, output_path: Path) -> None:
    """Render HTML → PDF using WeasyPrint."""
    from weasyprint import HTML as WP_HTML, CSS          # noqa: PLC0415
    from weasyprint.text.fonts import FontConfiguration  # noqa: PLC0415

    font_config = FontConfiguration()
    reset_css   = CSS(
        string="@page { margin: 0; } body { margin: 0; padding: 0; }",
        font_config=font_config,
    )
    WP_HTML(string=html).write_pdf(
        str(output_path),
        stylesheets=[reset_css],
        font_config=font_config,
    )


def _pdf_via_pdfkit(html: str, output_path: Path) -> None:
    """Render HTML → PDF using pdfkit + wkhtmltopdf (must be on PATH)."""
    import pdfkit  # noqa: PLC0415

    options = {
        "page-size":                "Letter",
        "margin-top":               "0",
        "margin-right":             "0",
        "margin-bottom":            "0",
        "margin-left":              "0",
        "encoding":                 "UTF-8",
        "enable-local-file-access": "",
        "no-outline":               "",
        "print-media-type":         "",
    }
    pdfkit.from_string(html, str(output_path), options=options)


def _pdf_via_playwright(html: str, output_path: Path) -> None:
    """
    Render HTML → PDF using Playwright + headless Chromium.

    Playwright downloads its own bundled Chromium to the user home folder —
    no admin rights or system install needed.

    Install once:
        pip install playwright
        playwright install chromium
    """
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page    = browser.new_page()
        page.set_content(html, wait_until="networkidle")
        page.pdf(
            path=str(output_path),
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def _pdf_via_xhtml2pdf(html: str, output_path: Path) -> None:
    """
    Render HTML → PDF using xhtml2pdf — 100% pure Python, no binaries.

    Install:  pip install xhtml2pdf

    Note: CSS support is limited (no Google Fonts, basic layout only).
    The letter shape will still print correctly; decorative fonts fall back
    to a system serif.  For best quality use Playwright instead.
    """
    from xhtml2pdf import pisa  # noqa: PLC0415

    # xhtml2pdf cannot fetch remote Google Fonts; strip the link tag so it
    # degrades gracefully to system fonts instead of erroring.
    import re  # noqa: PLC0415
    clean = re.sub(r'<link[^>]+fonts\.googleapis\.com[^>]*>', '', html)

    with open(output_path, "wb") as fh:
        result = pisa.CreatePDF(clean, dest=fh)

    if result.err:
        raise RuntimeError(f"xhtml2pdf reported errors: {result.err}")


def generate_pdf(html: str, output_path: str | Path) -> None:
    """
    Render an HTML string to a PDF file.

    Tries four backends in order, using the first one that works:

    1. **WeasyPrint**   — best quality on macOS / Linux
    2. **Playwright**   — best quality on Windows (pip-only, no admin needed)
    3. **pdfkit**       — good quality, needs wkhtmltopdf installed separately
    4. **xhtml2pdf**    — pure Python fallback, basic CSS only

    Parameters
    ----------
    html        : Complete HTML document string (from :func:`generate_html`).
    output_path : Destination ``.pdf`` file path.

    Windows quick start (no admin rights needed)
    --------------------------------------------
    .. code-block:: bash

        pip install playwright
        playwright install chromium   # downloads ~130 MB to your user folder

    macOS / Linux quick start
    -------------------------
    .. code-block:: bash

        pip install weasyprint
        brew install pango            # macOS only
        # Linux: sudo apt install libpango-1.0-0 libpangocairo-1.0-0

    Pure-Python fallback (any OS, limited CSS)
    ------------------------------------------
    .. code-block:: bash

        pip install xhtml2pdf

    Raises
    ------
    RuntimeError
        If no working PDF backend is found.
    """
    output_path = Path(output_path)
    errors: list[str] = []

    # ── 1. WeasyPrint ────────────────────────────────────────────────────────
    try:
        _pdf_via_weasyprint(html, output_path)
        return
    except ImportError:
        errors.append("WeasyPrint not installed  →  pip install weasyprint")
    except Exception as exc:
        errors.append(
            f"WeasyPrint failed ({exc.__class__.__name__}: {exc})\n"
            "  macOS/Linux fix: make sure pango is installed.\n"
            "  Windows:         use Playwright instead (see below)."
        )

    # ── 2. Playwright ────────────────────────────────────────────────────────
    try:
        _pdf_via_playwright(html, output_path)
        return
    except ImportError:
        errors.append(
            "Playwright not installed  →  pip install playwright\n"
            "  Then run once:           playwright install chromium"
        )
    except Exception as exc:
        errors.append(
            f"Playwright failed ({exc.__class__.__name__}: {exc})\n"
            "  Run: playwright install chromium"
        )

    # ── 3. pdfkit + wkhtmltopdf ──────────────────────────────────────────────
    try:
        _pdf_via_pdfkit(html, output_path)
        return
    except ImportError:
        errors.append("pdfkit not installed  →  pip install pdfkit")
    except OSError:
        errors.append(
            "pdfkit: wkhtmltopdf binary not found on PATH.\n"
            "  Download from https://wkhtmltopdf.org/downloads.html"
        )
    except Exception as exc:
        errors.append(f"pdfkit failed ({exc.__class__.__name__}: {exc})")

    # ── 4. xhtml2pdf ─────────────────────────────────────────────────────────
    try:
        _pdf_via_xhtml2pdf(html, output_path)
        return
    except ImportError:
        errors.append(
            "xhtml2pdf not installed  →  pip install xhtml2pdf\n"
            "  (pure Python, no admin rights needed, limited CSS)"
        )
    except Exception as exc:
        errors.append(f"xhtml2pdf failed ({exc.__class__.__name__}: {exc})")

    # ── All backends failed ───────────────────────────────────────────────────
    attempts = "\n\n".join(f"  [{i+1}] {e}" for i, e in enumerate(errors))
    raise RuntimeError(
        "PDF generation failed — no working PDF backend found.\n\n"
        + attempts +
        "\n\n"
        "Recommended fix (Windows, no admin rights):\n"
        "  pip install playwright\n"
        "  playwright install chromium\n\n"
        "Recommended fix (macOS / Linux):\n"
        "  pip install weasyprint\n"
        "  brew install pango           # macOS\n"
        "  sudo apt install libpango-1.0-0 libpangocairo-1.0-0  # Linux\n\n"
        "Simplest fix (any platform, pure Python):\n"
        "  pip install xhtml2pdf\n"
    )


# ---------------------------------------------------------------------------
# High-level API
# ---------------------------------------------------------------------------

def save_banner(
    text:  str,
    cfg:   Optional[BannerConfig] = None,
    *,
    output_basename: Optional[str] = None,
    write_html: bool = True,
    write_pdf:  bool = True,
    title:      str  = "",
) -> dict[str, Path]:
    """
    Generate HTML and/or PDF banner files and write them to disk.

    Parameters
    ----------
    text            : Text to render (spaces skipped).
    cfg             : :class:`BannerConfig`.  Defaults used when ``None``.
    output_basename : Base file name without extension.  Default: slugified text.
    write_html      : Write ``.html`` output.
    write_pdf       : Write ``.pdf`` output (requires WeasyPrint).
    title           : Custom HTML ``<title>`` tag content.

    Returns
    -------
    dict
        ``{"html": Path(...), "pdf": Path(...)}`` — only keys for files
        that were actually written.
    """
    if cfg is None:
        cfg = BannerConfig()

    base = output_basename or _slugify(text)
    html = generate_html(text, cfg, title=title or text.upper())

    saved: dict[str, Path] = {}

    if write_html:
        hp = Path(base + ".html")
        hp.write_text(html, encoding="utf-8")
        print(f"[letter-banner] HTML  →  {hp}")
        saved["html"] = hp

    if write_pdf:
        pp = Path(base + ".pdf")
        try:
            generate_pdf(html, pp)
            print(f"[letter-banner] PDF   →  {pp}")
            saved["pdf"] = pp
        except (ImportError, RuntimeError) as exc:
            print(f"[letter-banner] PDF skipped: {exc}", file=sys.stderr)

    return saved


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "banner"
