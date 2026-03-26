"""
letter-banner
~~~~~~~~~~~~~
Printable letter banner generator — one big letter per page,
output as HTML and/or PDF.

Quick start
-----------
::

    from letter_banner import BannerConfig, save_banner

    # Solid colour fill (default)
    save_banner("HAPPY BIRTHDAY", BannerConfig(palette_name="vivid"))

    # Outline only
    save_banner("HELLO", BannerConfig(mode="outline", outline_color="#ff0088"))

    # Photo mosaic fill
    save_banner(
        "LOVE",
        BannerConfig(mode="image", image_source="./photos/", grid_style="mosaic"),
    )

CLI
---
::

    letter-banner "HAPPY BIRTHDAY" --palette vivid --deco festive
    letter-banner "HELLO" --mode outline --outline-color "#ff0088"
    letter-banner "LOVE" --mode image --images ./photos/ --grid mosaic
    letter-banner --list-palettes
    letter-banner --list-fonts
"""

from .core import BannerConfig, generate_html, generate_pdf, save_banner
from .fonts import FONT_PRESETS, PAPER_SIZES, list_fonts, resolve_font
from .images import GRID_STYLES, GridStyle, collect_images, load_images
from .palettes import PALETTES, Theme, get_palette, list_palettes

__version__ = "1.0.0"
__author__  = "letter-banner contributors"
__license__ = "MIT"

__all__ = [
    # Core
    "BannerConfig",
    "generate_html",
    "generate_pdf",
    "save_banner",
    # Palettes
    "Theme",
    "PALETTES",
    "get_palette",
    "list_palettes",
    # Fonts
    "FONT_PRESETS",
    "PAPER_SIZES",
    "list_fonts",
    "resolve_font",
    # Images
    "GRID_STYLES",
    "GridStyle",
    "collect_images",
    "load_images",
]
