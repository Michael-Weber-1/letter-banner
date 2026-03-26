"""
letter_banner.fonts
~~~~~~~~~~~~~~~~~~~
Font presets and paper size definitions.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Google Fonts presets
# ---------------------------------------------------------------------------

FONT_PRESETS: dict[str, str] = {
    "bold":      "Lilita One",
    "fun":       "Boogaloo",
    "chunky":    "Fredoka One",
    "retro":     "Righteous",
    "elegant":   "Playfair Display",
    "handmade":  "Pacifico",
    "kids":      "Baloo 2",
    "modern":    "Nunito",
    "comic":     "Patrick Hand",
    "rounded":   "Varela Round",
    "display":   "Abril Fatface",
    "slab":      "Alfa Slab One",
    "script":    "Dancing Script",
    "pixel":     "Press Start 2P",
    "condensed": "Barlow Condensed",
}

# ---------------------------------------------------------------------------
# Paper sizes: width × height in inches (portrait)
# ---------------------------------------------------------------------------

PAPER_SIZES: dict[str, tuple[float, float]] = {
    "letter": (8.5,   11.0),
    "A4":     (8.267, 11.693),
    "A3":     (11.693, 16.535),
    "legal":  (8.5,   14.0),
    "tabloid": (11.0, 17.0),
}


def resolve_font(font: str) -> str:
    """
    Given a font preset key or a direct Google Font name, return the
    exact font-family string to embed in CSS / SVG.
    """
    return FONT_PRESETS.get(font, font)


def google_fonts_url(*font_names: str) -> str:
    """
    Build a single Google Fonts CSS URL for one or more font-family names.
    Always requests weights 400, 700, 900.
    """
    families = "&".join(
        f"family={name.replace(' ', '+')}:wght@400;700;900"
        for name in font_names
    )
    return f"https://fonts.googleapis.com/css2?{families}&display=swap"


def list_fonts() -> list[str]:
    """Return sorted list of available font preset keys."""
    return sorted(FONT_PRESETS)
