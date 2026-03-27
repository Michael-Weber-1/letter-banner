# Changelog

All notable changes to **letter-banner** are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **Outline too thick fixed**: `outline_width` default reduced from 16 → **4** SVG px (~1mm at print)
  Stroke now scales proportionally with font size (≈0.6% of em) so it looks
  consistent at any `--font-size` value; `outline_width` acts as a fine-tune multiplier
- **xhtml2pdf letters small fixed**: SVG pixel dimensions converted to pt (×0.75)
  so the letter fills the page correctly (xhtml2pdf renders at 72dpi, SVG at 96dpi)
- **Playwright SSL**: browser launched with `--ignore-certificate-errors` to work
  behind corporate proxies; error message now includes `NODE_EXTRA_CA_CERTS` hint
- **PDF one-page bug fixed**: xhtml2pdf now receives `<pdf:nextpage/>` tags
  between letters and a correct `@page { size }` rule — each letter prints
  on its own page
- **Letter centering fixed**: SVG baseline calculated from cap-height (72% of em)
  so the glyph body is visually centred on the page in all backends
- **Font size maximised**: default raised to 0.95; width cap factor increased
  to 1.35 so wide glyphs (W, M) grow larger before hitting the page edge
- New `--font-size` / `font_size` documentation section in README with a
  practical guide (0.95 default → 1.0 → 1.1 → 1.3) and examples
- Letter now rendered as **inline SVG** in all modes (color + outline + image)
  using absolute `px` dimensions from paper size — eliminates `vh`/`vw` entirely
- Font fills the full page correctly in every backend: browser, WeasyPrint,
  Playwright, and xhtml2pdf
- Default `font_size` raised from 0.82 → 0.92 for better page coverage
- `font_size` upper limit relaxed to 2.0 for power users
- xhtml2pdf: outline mode now renders as transparent letter (SVG `fill="none"`)
  instead of filled; letter is centred vertically on the page
- xhtml2pdf preprocessor simplified — no `vh`→`pt` conversion needed
- `--clean` / `-C` shortcut: outline mode, transparent background, no decoration — one flag only
- `--clean-white` / `-W` shortcut: outline mode, white background, no decoration
- `--filled` / `-F` shortcut: solid colour letter, white background, no decoration
- Shortcuts can be overridden by any individual flag that follows them
- Four PDF backends tried automatically in order: WeasyPrint → Playwright → pdfkit → xhtml2pdf
  — **Playwright** works on Windows with no admin rights (`pip install playwright && playwright install chromium`)
  — **xhtml2pdf** is a pure-Python last resort (`pip install xhtml2pdf`), no binaries at all
  — fixes `libgobject` / GTK crash on Windows
- New example `examples/letter_only.py` covering all clean/outline output variants
- `--page-bg` CLI flag and `BannerConfig.page_bg` field to override the page
  background colour on every letter page
- Use `--page-bg "#ffffff" --deco none --dot-opacity 0` for a clean white page
  with just the letter
- Use `--page-bg "transparent"` for a fully transparent background suitable
  for overlays and compositing
- New "Clean / letter-only output" section in README with full examples

---

## [1.0.0] – 2026-03-26

### Added
- **Three fill modes**: `color`, `outline`, `image`
- **14 named colour palettes**: `easter`, `christmas`, `halloween`, `halloween_kids`,
  `valentines`, `pastel`, `vivid`, `monochrome`, `black_gold`, `neon`,
  `warm`, `cool`, `ocean`, `rainbow`, `wedding`, `graduation`
- **15 Google Font presets**: `bold`, `fun`, `chunky`, `retro`, `elegant`,
  `handmade`, `kids`, `modern`, `comic`, `rounded`, `display`, `slab`,
  `script`, `pixel`, `condensed`
- **6 decoration styles**: `none`, `minimal`, `dots`, `shapes`, `festive`, `confetti`
- **6 photo grid layouts**: `single`, `grid`, `strips_h`, `strips_v`, `diagonal`, `mosaic`
- **HEIC/HEIF support** via `pillow-heif` (optional dependency)
- **5 paper sizes**: `letter`, `A4`, `A3`, `legal`, `tabloid`
- Full **CLI** (`letter-banner` command + `python -m letter_banner`)
- **Python API**: `BannerConfig`, `save_banner`, `generate_html`, `generate_pdf`
- Custom **palette override** via `Theme` dataclass
- Direct Google Fonts name support (not limited to presets)
- Optional letter **label** caption at page bottom
- Reproducible image shuffling via `image_seed`
- Self-contained HTML output (images base64-embedded)
- GitHub Actions CI: lint, multi-OS tests (Python 3.9–3.12), PyPI publish

[1.0.0]: https://github.com/Michael-Weber-1/letter-banner/releases/tag/v1.0.0
