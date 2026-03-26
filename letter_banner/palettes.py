"""
letter_banner.palettes
~~~~~~~~~~~~~~~~~~~~~~
Colour themes and named palette collections.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Theme:
    """One colour theme for a single letter page."""
    bg:     str = "#ffffff"   # page background
    dot:    str = "#dddddd"   # polka-dot / texture colour
    fill:   str = "#888888"   # letter fill colour
    stroke: str = "#333333"   # letter stroke / outline colour
    accent: str = "#bbbbbb"   # decoration accent colour

    def __post_init__(self) -> None:
        for attr in ("bg", "dot", "fill", "stroke", "accent"):
            v = getattr(self, attr)
            if not isinstance(v, str) or not v.startswith("#"):
                raise ValueError(
                    f"Theme.{attr} must be a hex colour string (e.g. '#ff0000'), got: {v!r}"
                )


_T = Theme  # compact alias for palette definitions below

# ---------------------------------------------------------------------------
# Named palettes
# Each palette is a list of Theme objects that cycle across letters.
# ---------------------------------------------------------------------------

PALETTES: dict[str, list[Theme]] = {
    # ── Seasonal / occasion ──────────────────────────────────────────────────
    "easter": [
        _T("#fff6f8","#f9a8c9","#fb85b0","#c0496e","#ffd0e5"),
        _T("#f8fff5","#a8e6a3","#6cc96a","#2e7a2c","#c8f0c5"),
        _T("#fffef0","#ffe57a","#ffd034","#a87800","#fff0a0"),
        _T("#f4f0ff","#c8b4f8","#9b72ef","#4b2fa0","#ddd0fc"),
        _T("#fff8f0","#ffc38a","#ff8b2d","#9e4700","#ffe0c0"),
        _T("#f0fbff","#85d8f7","#31b8ef","#085e8a","#c0eeff"),
        _T("#fff0fb","#f7aaee","#ef65d8","#8c1f80","#fdd0f8"),
        _T("#f0fff8","#88f0de","#20c9a8","#07705c","#b0f8ec"),
    ],
    "christmas": [
        _T("#fff0f0","#ffaaaa","#cc2222","#880000","#ffcccc"),
        _T("#f0fff0","#aaffaa","#228822","#005500","#ccffcc"),
        _T("#fffff8","#ffeeaa","#ddcc00","#888800","#ffffcc"),
        _T("#fff2f2","#ffbbbb","#ee3333","#990000","#ffdddd"),
        _T("#f2fff2","#bbffbb","#33aa33","#006600","#ddffdd"),
        _T("#fffcf0","#ffe8a0","#ddbb00","#887700","#fff4cc"),
    ],
    "halloween": [
        _T("#1a0a00","#cc6600","#ff8800","#cc4400","#ff6600"),
        _T("#0d0d0d","#9933cc","#7700cc","#440088","#cc88ff"),
        _T("#1a1000","#dd8800","#ff6600","#aa3300","#ffaa44"),
        _T("#0a000a","#cc44cc","#aa00aa","#660066","#ee88ee"),
        _T("#1a0800","#ee7700","#ff5500","#cc2200","#ffaa00"),
    ],
    "valentines": [
        _T("#fff0f4","#ffaac0","#ff4488","#aa0044","#ffd0e0"),
        _T("#fff0f8","#ffb8d8","#ff6699","#cc0055","#ffe0ee"),
        _T("#fdf0f2","#f8a0b8","#ee3366","#990033","#fcc8d8"),
        _T("#fff4f6","#ffc0cc","#ff5577","#bb2244","#ffdde4"),
    ],
    "halloween_kids": [
        _T("#fff8f0","#ffcc88","#ff9900","#884400","#ffeedd"),
        _T("#f8fff0","#aaffaa","#44dd22","#226600","#ddffcc"),
        _T("#f8f0ff","#ddbbff","#aa44ff","#550099","#eeddff"),
        _T("#fff0f0","#ffaaaa","#ff4444","#990000","#ffcccc"),
    ],

    # ── Mood / aesthetic ─────────────────────────────────────────────────────
    "pastel": [
        _T("#fdf0f5","#f9cce0","#f4a0c0","#c06080","#ffe0ee"),
        _T("#f0fdf5","#c0f0d0","#80d8a0","#308050","#d8f8e4"),
        _T("#f0f5fd","#c0d0f8","#90b0f0","#3050a0","#d8e4fc"),
        _T("#fdfdf0","#f8f0a0","#e8d860","#907820","#f8f4c0"),
        _T("#fdf5f0","#f8d0b0","#f0a878","#a05828","#fce8d4"),
        _T("#f5f0fd","#d8c0f8","#b898e8","#604898","#eddcfc"),
        _T("#f0fdfb","#b8ece4","#78d4c8","#2a7068","#d0f8f0"),
        _T("#fdfaf0","#f0e0a8","#d8c060","#786020","#f4ecc0"),
    ],
    "vivid": [
        _T("#fff0f0","#ff9999","#ff2222","#990000","#ffcccc"),
        _T("#fff8f0","#ffcc88","#ff8800","#884400","#ffe8cc"),
        _T("#fffff0","#ffee88","#ffcc00","#887700","#ffffcc"),
        _T("#f0fff0","#88ee88","#00cc22","#006611","#ccffcc"),
        _T("#f0f0ff","#8899ff","#2244ff","#001199","#ccd4ff"),
        _T("#f8f0ff","#cc88ff","#aa00ff","#550088","#e8ccff"),
        _T("#f0ffff","#66dddd","#00aaaa","#005555","#bbffff"),
    ],
    "monochrome": [
        _T("#f8f8f8","#aaaaaa","#444444","#111111","#cccccc"),
        _T("#ffffff","#cccccc","#888888","#333333","#dddddd"),
        _T("#f0f0f0","#999999","#333333","#000000","#bbbbbb"),
    ],
    "black_gold": [
        _T("#0d0d0d","#c8a820","#ffd700","#c8a820","#8b6914"),
        _T("#111111","#d4af37","#ffc200","#b8960c","#9a7010"),
        _T("#1a1008","#cc9900","#ffbb00","#aa7700","#7a5500"),
    ],
    "neon": [
        _T("#0a0a0a","#ff00ff","#ff00cc","#cc0099","#ff88ff"),
        _T("#050510","#00ffff","#00ccff","#0066cc","#88eeff"),
        _T("#0a0500","#ffff00","#ffcc00","#cc9900","#ffee88"),
        _T("#050a00","#00ff44","#00cc33","#009922","#88ffaa"),
        _T("#0a0008","#ff44ff","#cc00ff","#8800cc","#ff88ff"),
    ],

    # ── Colour temperature ───────────────────────────────────────────────────
    "warm": [
        _T("#fff8f0","#ffd0a0","#ff9944","#aa4400","#ffe8d0"),
        _T("#fff4f0","#ffb8a8","#ff6644","#aa2200","#ffd8cc"),
        _T("#fffff0","#ffeea0","#ffcc44","#886600","#fff8c0"),
        _T("#fdf4e8","#f0c880","#d89040","#7a4800","#f8e4c0"),
        _T("#fff0e8","#f8b888","#e07040","#8a3800","#fcd8c0"),
    ],
    "cool": [
        _T("#f0f4ff","#a8c0f8","#4868e8","#102090","#d0dcfc"),
        _T("#f0faff","#a0d8f8","#2090e0","#005090","#c8eeff"),
        _T("#f0fff8","#88f0d0","#20c890","#007050","#c0f8e8"),
        _T("#f4f0ff","#c0a8f8","#8044e8","#400090","#ddd0fc"),
        _T("#f0f8f8","#90d0d0","#3090a8","#105060","#c8ecec"),
    ],
    "ocean": [
        _T("#f0faff","#a0d8f8","#2090e0","#005090","#c8eeff"),
        _T("#f0fffa","#a0f0d8","#20d0a0","#006050","#c0fcea"),
        _T("#f0f4ff","#a0b8f8","#3060e8","#081880","#c8d4ff"),
        _T("#e8f8ff","#88d0f0","#1080c8","#004070","#c0e8f8"),
        _T("#f0fff8","#88f8d8","#10c888","#004840","#c0f8e8"),
    ],
    "rainbow": [
        _T("#fff0f0","#ffaaaa","#ff4444","#990000","#ffcccc"),
        _T("#fff8f0","#ffddaa","#ff9900","#884400","#ffeedd"),
        _T("#fffff0","#ffeeaa","#ffdd00","#887700","#ffffcc"),
        _T("#f0fff0","#aaffaa","#44dd44","#006600","#ccffcc"),
        _T("#f0f0ff","#aaaaff","#4444ff","#000099","#ccccff"),
        _T("#f8f0ff","#ddaaff","#bb44ff","#660099","#eeccff"),
    ],

    # ── Formal / event ───────────────────────────────────────────────────────
    "wedding": [
        _T("#fffcf8","#f8e8d8","#e8c8a8","#8a6040","#f0d8c0"),
        _T("#f8fcff","#d8e8f8","#a8c8e8","#406080","#c0d8f0"),
        _T("#fff8fc","#f8d8e8","#e8a8c8","#80406a","#f0c0d8"),
        _T("#fcfcf8","#e8e8d8","#c8c8a8","#606040","#d8d8c0"),
    ],
    "graduation": [
        _T("#0d0d0d","#c8a820","#ffd700","#c8a820","#8b6914"),
        _T("#111122","#8899ff","#4455ee","#002299","#aabbff"),
        _T("#0a0a0a","#dddddd","#ffffff","#888888","#cccccc"),
    ],
}


def get_palette(name: str) -> list[Theme]:
    """Return a named palette, raising ValueError if not found."""
    if name not in PALETTES:
        available = ", ".join(sorted(PALETTES))
        raise ValueError(f"Unknown palette {name!r}. Available: {available}")
    return PALETTES[name]


def list_palettes() -> list[str]:
    """Return sorted list of available palette names."""
    return sorted(PALETTES)
