"""
Example: color fill mode with different palettes.
Run from the repo root:  python examples/basic_color.py
"""
from letter_banner import BannerConfig, save_banner

# ── Default pastel palette ───────────────────────────────────────────────────
save_banner(
    "HELLO WORLD",
    BannerConfig(palette_name="pastel", decoration="dots"),
    output_basename="hello_world_pastel",
    write_pdf=False,
)

# ── Vivid palette with festive decoration ────────────────────────────────────
save_banner(
    "HAPPY BIRTHDAY",
    BannerConfig(palette_name="vivid", decoration="festive", font="fun"),
    output_basename="happy_birthday_vivid",
    write_pdf=False,
)

# ── Black & gold — elegant occasion ─────────────────────────────────────────
save_banner(
    "GALA",
    BannerConfig(palette_name="black_gold", decoration="shapes", font="elegant"),
    output_basename="gala_black_gold",
    write_pdf=False,
)

# ── Custom palette override ───────────────────────────────────────────────────
from letter_banner import Theme

custom = [
    Theme(bg="#0a0a0a", dot="#ff00ff", fill="#ee00cc", stroke="#880077", accent="#ff88ff"),
    Theme(bg="#050510", dot="#00ffff", fill="#00ccff", stroke="#006699", accent="#88eeff"),
    Theme(bg="#050500", dot="#ffff00", fill="#ffcc00", stroke="#886600", accent="#ffee88"),
]
save_banner(
    "NEON",
    BannerConfig(palette_override=custom, decoration="confetti", font="retro"),
    output_basename="neon_custom",
    write_pdf=False,
)

print("\nDone!  Open any .html file in your browser and print.")
