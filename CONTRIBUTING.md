# Contributing to letter-banner

Thank you for your interest in contributing! This document covers
everything you need to get started.

---

## Table of contents

1. [Development setup](#development-setup)
2. [Running the tests](#running-the-tests)
3. [Code style](#code-style)
4. [Adding a new palette](#adding-a-new-palette)
5. [Adding a new font preset](#adding-a-new-font-preset)
6. [Adding a new decoration style](#adding-a-new-decoration-style)
7. [Submitting a pull request](#submitting-a-pull-request)
8. [Reporting bugs](#reporting-bugs)

---

## Development setup

```bash
# 1. Fork & clone
git clone https://github.com/your-username/letter-banner.git
cd letter-banner

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install in editable mode with all dev dependencies
pip install -e ".[dev]"

# 4. Verify everything works
pytest
letter-banner --list-palettes
```

---

## Running the tests

```bash
# All tests
pytest

# With coverage report
pytest --cov=letter_banner --cov-report=term-missing

# Single file
pytest tests/test_core.py

# Specific test
pytest tests/test_cli.py::TestCLI::test_basic_color_mode
```

---

## Code style

We use **ruff** for linting and formatting.

```bash
# Check for issues
ruff check letter_banner/

# Auto-fix
ruff check --fix letter_banner/

# Format
ruff format letter_banner/
```

Type hints are encouraged throughout.  Run `mypy letter_banner/` to check.

---

## Adding a new palette

Open `letter_banner/palettes.py` and add an entry to the `PALETTES` dict:

```python
"my_palette": [
    Theme(bg="#ffffff", dot="#aabbcc", fill="#3344dd", stroke="#001199", accent="#aabbff"),
    Theme(bg="#fff8f0", dot="#ffccaa", fill="#ff8833", stroke="#994400", accent="#ffddc0"),
    # … add 4–8 themes for good variety
],
```

**Guidelines**
- Provide at least **4 themes** so consecutive letters always differ.
- Keep `bg` light (near white) unless going for a dark theme (like `black_gold`).
- `dot` should be a muted version of `fill` for the polka-dot texture.
- `accent` is used by the decoration layer — usually a lighter tint of `fill`.
- Add the new name to `PALETTES` and it is automatically available in the CLI
  (`--palette my_palette`) and via `get_palette("my_palette")`.

Write a quick sanity check:

```bash
letter-banner "ABCDE" --palette my_palette --no-pdf -o /tmp/test_palette
```

---

## Adding a new font preset

Open `letter_banner/fonts.py` and add an entry to `FONT_PRESETS`:

```python
"my_font": "My Google Font Name",
```

The value must be the exact family name as it appears on
[fonts.google.com](https://fonts.google.com).  The CLI key (left side)
should be short, lowercase, and memorable.

Test it:

```bash
letter-banner "HELLO" --font my_font --no-pdf -o /tmp/test_font
```

---

## Adding a new decoration style

1. Add the style name to `DECORATION_STYLES` in `letter_banner/decorations.py`.
2. Implement the drawing logic inside `_build_inner()` using the existing
   `rng`, `W`, `H`, and `theme` variables.
3. All coordinates are in SVG user units (pixels at 96 dpi).
4. Keep elements `pointer-events:none` — decorations must never block interaction.
5. Add a test case in `tests/test_cli.py::TestCLI::test_all_deco_styles`.

---

## Submitting a pull request

1. Create a feature branch: `git checkout -b feat/my-feature`
2. Make your changes, add/update tests.
3. Ensure `pytest` and `ruff check` both pass.
4. Commit with a clear message: `git commit -m "feat: add ocean-sunset palette"`
5. Push and open a PR against `main`.

**PR checklist**

- [ ] Tests pass (`pytest`)
- [ ] Linter clean (`ruff check letter_banner/`)
- [ ] New palette/font/feature documented in `CHANGELOG.md` under `[Unreleased]`
- [ ] `README.md` updated if user-facing behaviour changed

---

## Reporting bugs

Please open an issue on GitHub with:

- Your Python version (`python --version`)
- Your OS
- The exact command or code that triggered the bug
- The full traceback
- (For image bugs) a minimal reproducible image or description of the image
