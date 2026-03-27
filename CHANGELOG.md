# Changelog

All notable changes to **letter-banner** are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- `--page-bg` CLI flag and `BannerConfig.page_bg` field to override the page
  background colour on every letter page
- Use `--page-bg "#ffffff" --deco none --dot-opacity 0` for a clean white page
  with just the letter
- Use `--page-bg "transparent"` for a fully transparent background suitable
  for overlays and compositing
- New "Clean / letter-only output" section in README with full examples

---

## [1.0.0] – 2026-03-27

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
