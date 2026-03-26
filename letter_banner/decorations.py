"""
letter_banner.decorations
~~~~~~~~~~~~~~~~~~~~~~~~~
SVG decoration snippets rendered behind each letter.
"""
from __future__ import annotations

import random

from .palettes import Theme

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

DECORATION_STYLES = ("none", "minimal", "dots", "shapes", "festive", "confetti")


def build_svg_decoration(
    style:  str,
    theme:  Theme,
    w_in:   float,
    h_in:   float,
    idx:    int,
    dpi:    int = 96,
) -> str:
    """
    Return a full ``<svg>`` element (or empty string for ``style='none'``)
    containing decorative shapes positioned on the page.

    Parameters
    ----------
    style   : One of DECORATION_STYLES.
    theme   : Colour theme for this page.
    w_in    : Page width in inches.
    h_in    : Page height in inches.
    idx     : Letter index — used as RNG seed for deterministic output.
    dpi     : Screen/render DPI used for SVG viewport.
    """
    if style == "none":
        return ""

    inner = _build_inner(style, theme, w_in * dpi, h_in * dpi, idx)
    if not inner:
        return ""

    return (
        f'<svg class="lb-deco" xmlns="http://www.w3.org/2000/svg" '
        f'style="position:absolute;inset:0;width:100%;height:100%;'
        f'z-index:0;pointer-events:none;overflow:visible;">'
        f'{inner}</svg>'
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha:.2f})"


def _build_inner(style: str, theme: Theme, W: float, H: float, idx: int) -> str:
    rng   = random.Random(idx * 7919 + 42)
    parts: list[str] = []
    fills = [theme.fill, theme.accent, theme.stroke]

    # ── Corner blobs (minimal, dots, shapes, festive, confetti) ─────────────
    if style != "none":
        size = min(W, H) * 0.075
        for cx, cy in [(0, 0), (W, 0), (W, H), (0, H)]:
            parts.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size:.1f}" '
                f'fill="{_rgba(theme.fill, 0.18)}"/>'
            )

    # ── Scattered shapes ─────────────────────────────────────────────────────
    if style in ("dots", "shapes", "festive", "confetti"):
        count = {"dots": 8, "shapes": 16, "festive": 24, "confetti": 10}[style]
        for i in range(count):
            x     = rng.uniform(0.04, 0.96) * W
            y     = rng.uniform(0.04, 0.96) * H
            r     = rng.uniform(7, 26)
            fc    = fills[i % len(fills)]
            alpha = rng.uniform(0.10, 0.26)
            fa    = _rgba(fc, alpha)
            shape = i % 5

            if shape == 0:   # circle
                parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fa}"/>')
            elif shape == 1: # diamond
                pts = f"{x:.1f},{(y-r):.1f} {(x+r):.1f},{y:.1f} {x:.1f},{(y+r):.1f} {(x-r):.1f},{y:.1f}"
                parts.append(f'<polygon points="{pts}" fill="{fa}"/>')
            elif shape == 2: # 4-point star
                si  = r * 0.42
                pts = (
                    f"{x:.1f},{(y-r):.1f} {(x+si):.1f},{(y-si):.1f} "
                    f"{(x+r):.1f},{y:.1f} {(x+si):.1f},{(y+si):.1f} "
                    f"{x:.1f},{(y+r):.1f} {(x-si):.1f},{(y+si):.1f} "
                    f"{(x-r):.1f},{y:.1f} {(x-si):.1f},{(y-si):.1f}"
                )
                parts.append(f'<polygon points="{pts}" fill="{fa}"/>')
            elif shape == 3: # ring
                parts.append(
                    f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" '
                    f'fill="none" stroke="{fa}" stroke-width="3"/>'
                )
            else:            # triangle
                pts = (
                    f"{x:.1f},{(y-r):.1f} "
                    f"{(x+r*0.87):.1f},{(y+r*0.5):.1f} "
                    f"{(x-r*0.87):.1f},{(y+r*0.5):.1f}"
                )
                parts.append(f'<polygon points="{pts}" fill="{fa}"/>')

    # ── Edge confetti strips (festive, confetti) ─────────────────────────────
    if style in ("festive", "confetti"):
        for i in range(14):
            fc   = fills[i % len(fills)]
            fa   = _rgba(fc, rng.uniform(0.30, 0.50))
            rot  = rng.uniform(-55, 55)
            # top edge
            x, y = rng.uniform(0, W), rng.uniform(0, 55)
            parts.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="14" height="6" rx="2" '
                f'fill="{fa}" transform="rotate({rot:.1f} {x:.1f} {y:.1f})"/>'
            )
            # bottom edge
            y2 = rng.uniform(H - 55, H)
            parts.append(
                f'<rect x="{x:.1f}" y="{y2:.1f}" width="14" height="6" rx="2" '
                f'fill="{fa}" transform="rotate({rot:.1f} {x:.1f} {y2:.1f})"/>'
            )

    # ── Large soft blobs in corners (festive) ────────────────────────────────
    if style == "festive":
        blob_r = min(W, H) * 0.18
        positions = [(0, 0), (W, 0), (W, H), (0, H)]
        for i, (bx, by) in enumerate(positions):
            fc = fills[i % len(fills)]
            parts.append(
                f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{blob_r:.1f}" '
                f'fill="{_rgba(fc, 0.09)}"/>'
            )

    return "\n  ".join(parts)
