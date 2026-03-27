"""
letter_only.py — Letter-only output examples
=============================================

Shows every way to produce a page with NOTHING but the letter:
  • no background colour
  • no decoration shapes
  • no polka-dot texture
  • no fill inside the letter (outline / stencil mode)

These are ideal for:
  • colouring-in pages for kids
  • stencil templates to cut out
  • overlaying on top of another design
  • printing on coloured card stock

─────────────────────────────────────────────────────────────────────────────
CLI equivalents are shown in each section comment.
Run this file from inside the letter-banner folder:
    python examples/letter_only.py
─────────────────────────────────────────────────────────────────────────────
"""

from letter_banner import BannerConfig, save_banner

# =============================================================================
# 1.  TRANSPARENT BACKGROUND  (letter outline, nothing else)
#     CLI shortcut:  letter-banner "HELLO" --clean
#     CLI long form: letter-banner "HELLO" --mode outline
#                        --page-bg transparent --deco none --dot-opacity 0
# =============================================================================
save_banner(
    "HELLO",
    BannerConfig(
        mode        = "outline",
        page_bg     = "transparent",   # no background at all
        decoration  = "none",          # no shapes
        dot_opacity = 0,               # no polka dots
        outline_color = "#000000",     # black outline
        outline_width = 18,
        font        = "bold",
    ),
    output_basename = "letter_only_transparent",
    write_pdf = False,   # change to True once a PDF backend is installed
)
print("→ letter_only_transparent.html")


# =============================================================================
# 2.  WHITE BACKGROUND  (letter outline on white — ready to print & colour in)
#     CLI shortcut:  letter-banner "HELLO" --clean-white
#     CLI long form: letter-banner "HELLO" --mode outline
#                        --page-bg "#ffffff" --deco none --dot-opacity 0
# =============================================================================
save_banner(
    "HELLO",
    BannerConfig(
        mode        = "outline",
        page_bg     = "#ffffff",       # plain white
        decoration  = "none",
        dot_opacity = 0,
        outline_color = "#000000",
        outline_width = 18,
        font        = "bold",
    ),
    output_basename = "letter_only_white",
    write_pdf = False,
)
print("→ letter_only_white.html")


# =============================================================================
# 3.  COLOURED OUTLINE ON WHITE  (nice for themed colouring-in pages)
#     CLI: letter-banner "KIDS" --clean-white --outline-color "#6600cc" --font kids
# =============================================================================
save_banner(
    "KIDS",
    BannerConfig(
        mode          = "outline",
        page_bg       = "#ffffff",
        decoration    = "none",
        dot_opacity   = 0,
        outline_color = "#6600cc",     # purple outline
        outline_width = 20,
        font          = "kids",
    ),
    output_basename = "letter_only_purple",
    write_pdf = False,
)
print("→ letter_only_purple.html")


# =============================================================================
# 4.  SOLID COLOUR, NO BACKGROUND / DECORATION
#     (filled letter, white page, nothing else)
#     CLI shortcut:  letter-banner "SPRING" --filled --palette easter
#     CLI long form: letter-banner "SPRING" --mode color --palette easter
#                        --page-bg "#ffffff" --deco none --dot-opacity 0
# =============================================================================
save_banner(
    "SPRING",
    BannerConfig(
        mode        = "color",
        palette_name = "easter",
        page_bg     = "#ffffff",
        decoration  = "none",
        dot_opacity = 0,
        font        = "chunky",
    ),
    output_basename = "letter_only_filled",
    write_pdf = False,
)
print("→ letter_only_filled.html")


# =============================================================================
# 5.  THIN OUTLINE — stencil style
#     CLI: letter-banner "CUT" --clean-white --outline-color "#333333"
#              --outline-width 8 --font condensed
# =============================================================================
save_banner(
    "CUT",
    BannerConfig(
        mode          = "outline",
        page_bg       = "#ffffff",
        decoration    = "none",
        dot_opacity   = 0,
        outline_color = "#333333",
        outline_width = 8,            # thin = easy to cut out
        font          = "condensed",
    ),
    output_basename = "letter_only_stencil",
    write_pdf = False,
)
print("→ letter_only_stencil.html")


# =============================================================================
# 6.  FULL WORD, ALL LETTERS CLEAN, A4 PAPER
#     CLI: letter-banner "EASTER" --clean-white --paper A4 --font fun
# =============================================================================
save_banner(
    "EASTER",
    BannerConfig(
        mode          = "outline",
        page_bg       = "#ffffff",
        decoration    = "none",
        dot_opacity   = 0,
        outline_color = "#222222",
        outline_width = 16,
        font          = "fun",
        paper         = "A4",
    ),
    output_basename = "easter_clean_A4",
    write_pdf = False,
)
print("→ easter_clean_A4.html")


print("\nAll done!  Open any .html file in your browser and print.")
print("Tip: set write_pdf=True (and install pdfkit or WeasyPrint) to get PDFs.")
