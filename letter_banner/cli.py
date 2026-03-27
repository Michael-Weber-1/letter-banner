"""
letter_banner.cli
~~~~~~~~~~~~~~~~~
Command-line interface for letter-banner.
Invoked as:  letter-banner <text> [options]
             python -m letter_banner <text> [options]
"""
from __future__ import annotations

import argparse
import sys

from .core import BannerConfig, save_banner
from .fonts import FONT_PRESETS, PAPER_SIZES, list_fonts
from .images import GRID_STYLES
from .palettes import PALETTES, list_palettes


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="letter-banner",
        description=(
            "Generate printable letter banners — one letter per page.\n"
            "Output: HTML (always) + PDF (requires WeasyPrint).\n\n"
            "Examples:\n"
            "  letter-banner 'HAPPY BIRTHDAY' --palette vivid --deco festive\n"
            "  letter-banner 'HELLO' --mode outline --outline-color '#ff0088'\n"
            "  letter-banner 'LOVE' --mode image --images ./photos/ --grid mosaic\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    p.add_argument(
        "text",
        nargs="?",
        help="Text to render (spaces are skipped; each character → 1 page).",
    )

    # ── Mode ─────────────────────────────────────────────────────────────────
    p.add_argument(
        "--mode", "-m",
        choices=["color", "outline", "image"],
        default="color",
        help="Letter fill mode  (default: color)",
    )

    # ── Colour ───────────────────────────────────────────────────────────────
    p.add_argument(
        "--palette", "-p",
        default="pastel",
        metavar="NAME",
        dest="palette_name",
        help=f"Colour palette name  (default: pastel).  Use --list-palettes to see all.",
    )

    # ── Image ─────────────────────────────────────────────────────────────────
    p.add_argument(
        "--images", "-i",
        default=None,
        metavar="FILE_OR_DIR",
        dest="image_source",
        help="Image file or folder for --mode image.",
    )
    p.add_argument(
        "--grid", "-g",
        choices=list(GRID_STYLES),
        default="mosaic",
        dest="grid_style",
        help=f"Photo mosaic layout  (default: mosaic)",
    )
    p.add_argument(
        "--image-max-dim",
        default=1400,
        type=int,
        metavar="PX",
        help="Resize images so their longest side ≤ this value  (default: 1400)",
    )
    p.add_argument(
        "--image-seed",
        default=None,
        type=int,
        metavar="INT",
        help="Random seed for image shuffling (for reproducible output).",
    )

    # ── Outline ───────────────────────────────────────────────────────────────
    p.add_argument(
        "--outline-color",
        default="#222222",
        metavar="HEX",
        help="Stroke colour for outline mode  (default: #222222)",
    )
    p.add_argument(
        "--outline-width",
        default=16,
        type=int,
        metavar="PX",
        help="Stroke width in px for outline mode  (default: 16)",
    )
    p.add_argument(
        "--outline-bg",
        default="#ffffff",
        metavar="HEX",
        help="Background colour for outline mode  (default: #ffffff)",
    )
    p.add_argument(
        "--page-bg",
        default="",
        metavar="CSS_COLOUR",
        dest="page_bg",
        help=(
            "Override the page background for every letter. "
            "Use '#ffffff' for white, 'transparent' for no background. "
            "Combine with --deco none --dot-opacity 0 to show only the letter."
        ),
    )

    # ── Typography ────────────────────────────────────────────────────────────
    p.add_argument(
        "--font", "-f",
        default="bold",
        metavar="PRESET_OR_NAME",
        help=(
            "Font preset key or direct Google Fonts name  (default: bold).  "
            "Use --list-fonts to see presets."
        ),
    )
    p.add_argument(
        "--font-size",
        default=0.82,
        type=float,
        metavar="FRACTION",
        help="Letter height as fraction of page height, e.g. 0.82  (default: 0.82)",
    )

    # ── Decoration ────────────────────────────────────────────────────────────
    p.add_argument(
        "--deco", "-d",
        default="dots",
        dest="decoration",
        choices=["none", "minimal", "dots", "shapes", "festive", "confetti"],
        help="Background decoration style  (default: dots)",
    )
    p.add_argument(
        "--dot-opacity",
        default=0.15,
        type=float,
        metavar="0-1",
        help="Opacity of polka-dot texture  (default: 0.15)",
    )

    # ── Page ──────────────────────────────────────────────────────────────────
    p.add_argument(
        "--paper",
        default="letter",
        choices=list(PAPER_SIZES),
        help="Paper size  (default: letter)",
    )

    # ── Output ────────────────────────────────────────────────────────────────
    p.add_argument(
        "--output", "-o",
        default=None,
        metavar="BASENAME",
        dest="output_basename",
        help="Output file base name without extension  (default: slugified text).",
    )
    p.add_argument(
        "--no-html",
        action="store_true",
        help="Skip HTML output.",
    )
    p.add_argument(
        "--no-pdf",
        action="store_true",
        help="Skip PDF output.",
    )
    p.add_argument(
        "--title",
        default="",
        help="Custom HTML <title> tag content.",
    )

    # ── Extras ────────────────────────────────────────────────────────────────
    p.add_argument(
        "--label",
        action="store_true",
        dest="show_label",
        help="Print the letter as a small caption at the bottom of each page.",
    )

    # ── Shortcuts ─────────────────────────────────────────────────────────────
    shortcuts = p.add_argument_group(
        "shortcuts",
        "Single-flag presets — each sets several options at once. "
        "Any individual flag that follows will override the shortcut.",
    )
    shortcuts.add_argument(
        "--clean", "-C",
        action="store_true",
        help=(
            "Letter outline only — no fill, no background, no decoration. "
            "Equivalent to: --mode outline --page-bg transparent "
            "--deco none --dot-opacity 0"
        ),
    )
    shortcuts.add_argument(
        "--clean-white", "-W",
        action="store_true",
        dest="clean_white",
        help=(
            "Letter outline on a plain white page — no decoration. "
            "Equivalent to: --mode outline --page-bg '#ffffff' "
            "--deco none --dot-opacity 0"
        ),
    )
    shortcuts.add_argument(
        "--filled", "-F",
        action="store_true",
        help=(
            "Solid colour letter on a plain white page — no decoration. "
            "Equivalent to: --mode color --page-bg '#ffffff' "
            "--deco none --dot-opacity 0"
        ),
    )

    # ── Info ──────────────────────────────────────────────────────────────────
    p.add_argument(
        "--list-palettes",
        action="store_true",
        help="Print available palette names and exit.",
    )
    p.add_argument(
        "--list-fonts",
        action="store_true",
        help="Print available font preset keys and exit.",
    )

    return p


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args   = parser.parse_args(argv)

    # Info commands
    if args.list_palettes:
        _print_palettes()
        return 0
    if args.list_fonts:
        _print_fonts()
        return 0

    if not args.text:
        parser.print_help()
        return 1

    if args.mode == "image" and not args.image_source:
        parser.error("--mode image requires --images FILE_OR_DIR")

    # ── Apply shortcut presets (individual flags below override these) ────────
    if args.clean:
        if args.mode        == "color":    args.mode        = "outline"
        if args.page_bg     == "":         args.page_bg     = "transparent"
        if args.decoration  == "dots":     args.decoration  = "none"
        if args.dot_opacity == 0.15:       args.dot_opacity = 0.0

    if args.clean_white:
        if args.mode        == "color":    args.mode        = "outline"
        if args.page_bg     == "":         args.page_bg     = "#ffffff"
        if args.decoration  == "dots":     args.decoration  = "none"
        if args.dot_opacity == 0.15:       args.dot_opacity = 0.0

    if args.filled:
        if args.page_bg     == "":         args.page_bg     = "#ffffff"
        if args.decoration  == "dots":     args.decoration  = "none"
        if args.dot_opacity == 0.15:       args.dot_opacity = 0.0

    cfg = BannerConfig(
        mode           = args.mode,
        palette_name   = args.palette_name,
        image_source   = args.image_source,
        grid_style     = args.grid_style,
        image_max_dim  = args.image_max_dim,
        image_seed     = args.image_seed,
        outline_color  = args.outline_color,
        outline_width  = args.outline_width,
        outline_bg     = args.outline_bg,
        font           = args.font,
        font_size      = args.font_size,
        decoration     = args.decoration,
        dot_opacity    = args.dot_opacity,
        paper          = args.paper,
        show_label     = args.show_label,
        page_bg        = args.page_bg,
    )

    try:
        save_banner(
            text            = args.text,
            cfg             = cfg,
            output_basename = args.output_basename,
            write_html      = not args.no_html,
            write_pdf       = not args.no_pdf,
            title           = args.title,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


# ---------------------------------------------------------------------------
# Info helpers
# ---------------------------------------------------------------------------

def _print_palettes() -> None:
    print(f"\n{'Palette':<18}  {'Sample fills'}")
    print("-" * 60)
    for name in list_palettes():
        themes  = PALETTES[name]
        samples = "  ".join(t.fill for t in themes[:5])
        print(f"  {name:<16}  {samples}")
    print()


def _print_fonts() -> None:
    print(f"\n{'Preset key':<16}  Google Font name")
    print("-" * 46)
    for key in list_fonts():
        print(f"  {key:<14}  {FONT_PRESETS[key]}")
    print()


if __name__ == "__main__":
    sys.exit(main())
