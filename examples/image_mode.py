"""
Example: image / photo-mosaic fill mode.
Edit IMAGE_SOURCE to point at your own photo file or folder.
Run from the repo root:  python examples/image_mode.py
"""
from pathlib import Path
from letter_banner import BannerConfig, save_banner
from letter_banner.images import GRID_STYLES

# ── Change this to your own image file or folder ─────────────────────────────
IMAGE_SOURCE = "./photos"         # folder with many photos
# IMAGE_SOURCE = "./rose.jpg"     # single photo

if not Path(IMAGE_SOURCE).exists():
    print(
        f"[demo] Image source {IMAGE_SOURCE!r} not found.\n"
        "       Create a 'photos' folder and add some JPEG/PNG/HEIC files,\n"
        "       or set IMAGE_SOURCE to an existing image path."
    )
else:
    # ── Mosaic layout (default, recommended for folders) ─────────────────────
    save_banner(
        "PARTY",
        BannerConfig(
            mode="image",
            image_source=IMAGE_SOURCE,
            grid_style="mosaic",
            decoration="festive",
            font="fun",
        ),
        output_basename="party_mosaic",
        write_pdf=False,
    )

    # ── Horizontal strips ─────────────────────────────────────────────────────
    save_banner(
        "SUMMER",
        BannerConfig(
            mode="image",
            image_source=IMAGE_SOURCE,
            grid_style="strips_h",
            decoration="shapes",
            font="chunky",
        ),
        output_basename="summer_strips",
        write_pdf=False,
    )

    # ── Diagonal bands ────────────────────────────────────────────────────────
    save_banner(
        "WOW",
        BannerConfig(
            mode="image",
            image_source=IMAGE_SOURCE,
            grid_style="diagonal",
            decoration="confetti",
            font="retro",
        ),
        output_basename="wow_diagonal",
        write_pdf=False,
    )

    # ── All grid styles, one letter each ─────────────────────────────────────
    print("\nGenerating one letter per grid style...")
    for style in GRID_STYLES:
        if style == "random":
            continue
        save_banner(
            "A",
            BannerConfig(
                mode="image",
                image_source=IMAGE_SOURCE,
                grid_style=style,
                decoration="dots",
            ),
            output_basename=f"grid_{style}",
            write_pdf=False,
        )

    print("\nDone!")
