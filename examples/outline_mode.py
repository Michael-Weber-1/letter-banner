"""
Example: outline (transparent letter interior) mode.
Run from the repo root:  python examples/outline_mode.py
"""
from letter_banner import BannerConfig, save_banner

# Simple black outline on white
save_banner(
    "SPRING",
    BannerConfig(
        mode="outline",
        outline_color="#222222",
        outline_width=18,
        outline_bg="#ffffff",
        decoration="minimal",
        font="elegant",
    ),
    output_basename="spring_outline_black",
    write_pdf=False,
)

# Coloured outline on a tinted background
save_banner(
    "LOVE",
    BannerConfig(
        mode="outline",
        outline_color="#cc0055",
        outline_width=20,
        outline_bg="#fff0f4",
        decoration="dots",
        dot_opacity=0.12,
        font="handmade",
    ),
    output_basename="love_outline_pink",
    write_pdf=False,
)

# Bold purple outline — great for colouring-in pages for kids
save_banner(
    "KIDS",
    BannerConfig(
        mode="outline",
        outline_color="#6600cc",
        outline_width=22,
        outline_bg="#ffffff",
        decoration="none",
        font="kids",
    ),
    output_basename="kids_outline_purple",
    write_pdf=False,
)

print("\nDone!")
