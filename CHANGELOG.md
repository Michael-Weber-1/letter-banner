# Changelog

All notable changes to **letter-banner** are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] – 2026-03-27

### Added
- `--photo` / `-P` shortcut: photo fill mode, transparent background, no decoration,
  no outline — the cleanest way to use image mode
- `--photo-white` / `-Q` shortcut: photo fill, white background, no decoration, no outline
- `--image-stroke PX` flag: optional stroke width drawn over the photo mosaic letter
  (default `0` — no outline); use `--image-stroke 4` for a thin edge
- `--image-stroke-color CSS` flag: colour of the optional photo stroke
- `BannerConfig.image_stroke_width` and `image_stroke_color` fields
- Image mode now defaults to **no outline** (`image_stroke_width=0`)
- `--clean` / `-C` shortcut: outline letter, transparent background, no decoration — one flag
- `--clean-white` / `-W` shortcut: outline letter, white background, no decoration
- `--filled` / `-F` shortcut: solid colour letter, white background, no decoration
- All shortcuts can be overridden by any individual flag that follows them
- `--page-bg CSS_COLOUR` flag and `BannerConfig.page_bg` field to override the page
  background on every letter page (use `transparent` or any CSS colour)
- Four PDF backends tried automatically in order: WeasyPrint → Playwright → pdfkit → xhtml2pdf
- Playwright backend launched with `--ignore-certificate-errors` for corporate proxy compat
- New example `examples/letter_only.py` with clean/outline output variants
- New **Letter size** section in README with practical `--font-size` guide

### Changed
- Letter now rendered as **inline SVG** using absolute pixel dimensions — eliminates
  `vh`/`vw` CSS units, fixes rendering in WeasyPrint, Playwright, and xhtml2pdf
- Default `font_size` raised to **0.95**; maximum relaxed to 2.0
- Default `outline_width` reduced from 16 → **4** SVG px (≈1mm at print — clean and thin)
- Stroke width now scales proportionally with font size (≈0.6% of em); `outline_width`
  acts as a fine-tune multiplier (4 = thin, 8 = medium, 16 = bold, 24 = heavy)

### Fixed
- **Double outline fixed**: SVG letter fill now uses the page background colour
  instead of `none` — only the outer stroke edge is visible, giving a clean
  single outline (e.g. `--clean-white` fills the letter interior with white)
- **PDF blank pages fixed**: removed CSS `page-break-after` from xhtml2pdf output;
  `<pdf:nextpage/>` alone handles page separation — no more empty pages between letters
- **PDF letter size fixed**: xhtml2pdf preprocessor no longer uses SVG (unreliable);
  each letter is rendered as a plain HTML table-cell with large pt-sized text,
  guaranteed to fill the page at 88% of page height
- **PDF outline letters fixed**: new **ReportLab backend** (backend 4) generates
  true outline text — the letter interior is filled with the page background colour
  so only the outer stroke edge shows; ReportLab is already installed as part of
  xhtml2pdf (`pip install xhtml2pdf`)
- **PDF blank pages fixed (ReportLab)**: switched from `drawString()` + `_textRenderMode`
  (which does not emit the PDF `Tr` operator) to `beginText()` + `setTextRenderMode(2)`
  + `drawText()` — the `2 Tr` operator is now correctly written to each page stream
- **Thick outline fixed**: CLI `--outline-width` default corrected from 16 → 4
  to match the `BannerConfig` default
- **PDF one-letter-per-page**: xhtml2pdf preprocessor now injects `<pdf:nextpage/>`
  between letters and a correct `@page { size }` rule
- **xhtml2pdf letter too small**: SVG coordinate system fully converted from 96dpi px
  to 72dpi pt — width, height, viewBox, x, y, font-size, and stroke-width all scaled
  by ×0.75 so the letter fills the page correctly
- **Letter centering**: SVG baseline calculated from cap-height (≈72% of em) so the
  glyph body is visually centred on the page in every rendering backend
- xhtml2pdf: outline mode renders with `fill="none"` — transparent letter interior

---

## [1.0.0] – 2026-03-26

### Added
- Three fill modes: `color`, `outline`, `image`
- 16 named colour palettes: `easter`, `christmas`, `halloween`, `halloween_kids`,
  `valentines`, `pastel`, `vivid`, `monochrome`, `black_gold`, `neon`,
  `warm`, `cool`, `ocean`, `rainbow`, `wedding`, `graduation`
- 15 Google Font presets: `bold`, `fun`, `chunky`, `retro`, `elegant`,
  `handmade`, `kids`, `modern`, `comic`, `rounded`, `display`, `slab`,
  `script`, `pixel`, `condensed`
- 6 decoration styles: `none`, `minimal`, `dots`, `shapes`, `festive`, `confetti`
- 6 photo grid layouts: `single`, `grid`, `strips_h`, `strips_v`, `diagonal`, `mosaic`
- HEIC/HEIF photo support via `pillow-heif`
- 5 paper sizes: `letter`, `A4`, `A3`, `legal`, `tabloid`
- Full CLI (`letter-banner` command + `python -m letter_banner`)
- Python API: `BannerConfig`, `save_banner`, `generate_html`, `generate_pdf`
- Custom palette override via `Theme` dataclass
- Direct Google Fonts name support (not limited to presets)
- Optional letter label caption at page bottom
- Reproducible image shuffling via `image_seed`
- Self-contained HTML output (images base64-embedded)
- GitHub Actions CI: lint, multi-OS tests (Python 3.9–3.12), PyPI publish

[1.1.0]: https://github.com/Michael-Weber-1/letter-banner/releases/tag/v1.1.0
[1.0.0]: https://github.com/Michael-Weber-1/letter-banner/releases/tag/v1.0.0
