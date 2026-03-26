"""
letter_banner.images
~~~~~~~~~~~~~~~~~~~~
Image discovery, loading (with HEIC/HEIF support), and grid / mosaic layout
calculation for the SVG clip-path letter fill.
"""
from __future__ import annotations

import base64
import io
import math
import random
import sys
from pathlib import Path
from typing import Literal, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

IMAGE_EXTENSIONS: frozenset[str] = frozenset(
    {".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif"}
)

GridStyle = Literal["single", "grid", "strips_h", "strips_v", "diagonal", "mosaic", "random"]

GRID_STYLES: tuple[str, ...] = (
    "single", "grid", "strips_h", "strips_v", "diagonal", "mosaic", "random"
)

# Maximum image dimension when encoding (keeps HTML file size manageable)
DEFAULT_MAX_DIM = 1400


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def collect_images(source: str | Path) -> list[Path]:
    """
    Return a list of image paths from a *file* or *directory*.

    - File   → returns ``[source]`` if it has a supported extension.
    - Folder → returns all supported images found (non-recursive, sorted).

    Raises
    ------
    FileNotFoundError
        If the source path does not exist or the folder contains no images.
    ValueError
        If a file path has an unsupported extension.
    """
    p = Path(source)

    if p.is_file():
        if p.suffix.lower() not in IMAGE_EXTENSIONS:
            raise ValueError(
                f"Unsupported image extension {p.suffix!r}. "
                f"Supported: {', '.join(sorted(IMAGE_EXTENSIONS))}"
            )
        return [p]

    if p.is_dir():
        found = sorted(
            f for f in p.iterdir()
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
        )
        if not found:
            raise FileNotFoundError(
                f"No supported image files found in directory: {p}"
            )
        return found

    raise FileNotFoundError(f"Image source does not exist: {p}")


# ---------------------------------------------------------------------------
# Loading / encoding
# ---------------------------------------------------------------------------

def image_to_data_url(path: Path, max_dim: int = DEFAULT_MAX_DIM) -> str:
    """
    Load *path* and return a base64-encoded ``data:`` URL.

    - Resizes images larger than *max_dim* on the longest side.
    - Converts HEIC/HEIF to JPEG automatically (requires ``pillow-heif``).
    - Falls back to raw base64 if Pillow is not installed (no resize, no HEIC).

    Raises
    ------
    ImportError
        If a HEIC/HEIF file is requested and ``pillow-heif`` is not installed.
    """
    ext = path.suffix.lower()

    if ext in (".heic", ".heif"):
        _ensure_heif()

    # ── Try Pillow (resize + normalise) ─────────────────────────────────────
    try:
        from PIL import Image

        img = Image.open(path).convert("RGB")
        if max(img.size) > max_dim:
            img.thumbnail((max_dim, max_dim))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/jpeg;base64,{b64}"

    except ImportError:
        pass  # Pillow not available → raw read

    # ── Raw read fallback ────────────────────────────────────────────────────
    if ext in (".heic", ".heif"):
        raise ImportError(
            "Pillow is required to decode HEIC/HEIF files.\n"
            "Install:  pip install pillow pillow-heif"
        )
    _MIME = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png",  ".webp": "image/webp", ".gif": "image/gif",
    }
    mime = _MIME.get(ext, "image/jpeg")
    b64  = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


def load_images(
    source: str | Path,
    max_dim: int = DEFAULT_MAX_DIM,
    shuffle: bool = True,
    seed: Optional[int] = None,
) -> list[str]:
    """
    Collect all images from *source* (file or folder), encode them as
    data-URLs, and return the list.  Failures are logged to stderr and skipped.

    Parameters
    ----------
    source  : Image file or folder path.
    max_dim : Maximum pixel dimension when loading (long edge).
    shuffle : Randomise the image order.
    seed    : Optional random seed for reproducible shuffling.
    """
    paths = collect_images(source)

    if shuffle:
        rng = random.Random(seed)
        rng.shuffle(paths)

    urls: list[str] = []
    for p in paths:
        try:
            urls.append(image_to_data_url(p, max_dim=max_dim))
        except Exception as exc:
            print(f"[letter-banner] skipping {p.name}: {exc}", file=sys.stderr)

    if not urls:
        raise ValueError("No images could be loaded from the specified source.")

    return urls


# ---------------------------------------------------------------------------
# Grid / mosaic layout
# ---------------------------------------------------------------------------

def compute_grid_cells(
    style:    GridStyle,
    n_images: int,
    x0: float, y0: float,
    w:  float, h:  float,
    rng: random.Random,
) -> list[dict]:
    """
    Return a list of cell dicts with keys:
    ``x, y, w, h, img`` (all in SVG user units, same CRS as the caller).

    ``img`` is an index into the caller's image list (modulo n_images).
    """
    if style == "random":
        style = rng.choice(["grid", "strips_h", "strips_v", "diagonal", "mosaic"])

    if style == "single" or n_images == 1:
        return [_c(x0, y0, w, h, 0)]

    if style == "strips_h":
        return _strips(x0, y0, w, h, n_images, horizontal=True)

    if style == "strips_v":
        return _strips(x0, y0, w, h, n_images, horizontal=False)

    if style == "diagonal":
        return _diagonal(x0, y0, w, h, n_images)

    if style == "grid":
        return _grid(x0, y0, w, h, n_images)

    if style == "mosaic":
        return _mosaic(x0, y0, w, h, n_images)

    # fallback
    return _grid(x0, y0, w, h, n_images)


# ---------------------------------------------------------------------------
# Layout implementations
# ---------------------------------------------------------------------------

def _c(x, y, w, h, img) -> dict:
    return {"x": x, "y": y, "w": w, "h": h, "img": img}


def _strips(x0, y0, w, h, n, *, horizontal: bool) -> list[dict]:
    n = min(n, 7)
    cells = []
    for i in range(n):
        if horizontal:
            ch = h / n
            cells.append(_c(x0, y0 + i * ch, w, ch, i % n))
        else:
            cw = w / n
            cells.append(_c(x0 + i * cw, y0, cw, h, i % n))
    return cells


def _diagonal(x0, y0, w, h, n) -> list[dict]:
    """Approximate diagonal bands as vertical strips (full clip applied by SVG)."""
    n = min(n, 7)
    cw = w / n
    return [_c(x0 + i * cw, y0, cw, h, i % n) for i in range(n)]


def _grid(x0, y0, w, h, n) -> list[dict]:
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    cw, ch = w / cols, h / rows
    cells = []
    for row in range(rows):
        for col in range(cols):
            idx = row * cols + col
            if idx >= n:
                break
            cells.append(_c(x0 + col * cw, y0 + row * ch, cw, ch, idx % n))
    return cells


def _mosaic(x0, y0, w, h, n) -> list[dict]:
    """Asymmetric magazine-style layout."""
    if n == 1:
        return [_c(x0, y0, w, h, 0)]
    if n == 2:
        return [
            _c(x0,            y0, w * 0.58, h,     0),
            _c(x0 + w * 0.58, y0, w * 0.42, h,     1),
        ]
    if n == 3:
        return [
            _c(x0,            y0,           w * 0.55, h,       0),
            _c(x0 + w * 0.55, y0,           w * 0.45, h * 0.5, 1),
            _c(x0 + w * 0.55, y0 + h * 0.5, w * 0.45, h * 0.5, 2),
        ]
    if n == 4:
        return [
            _c(x0,            y0,            w * 0.55, h * 0.55, 0),
            _c(x0 + w * 0.55, y0,            w * 0.45, h * 0.55, 1),
            _c(x0,            y0 + h * 0.55, w * 0.45, h * 0.45, 2),
            _c(x0 + w * 0.45, y0 + h * 0.55, w * 0.55, h * 0.45, 3),
        ]
    if n == 5:
        return [
            _c(x0,            y0,            w * 0.5,  h * 0.6,  0),
            _c(x0 + w * 0.5,  y0,            w * 0.5,  h * 0.6,  1),
            _c(x0,            y0 + h * 0.6,  w * 0.34, h * 0.4,  2),
            _c(x0 + w * 0.34, y0 + h * 0.6,  w * 0.33, h * 0.4,  3),
            _c(x0 + w * 0.67, y0 + h * 0.6,  w * 0.33, h * 0.4,  4),
        ]
    # 6+: large hero left + stacked right column
    right_n = n - 1
    right_h = h / right_n
    cells   = [_c(x0, y0, w * 0.5, h, 0)]
    for i in range(right_n):
        cells.append(_c(x0 + w * 0.5, y0 + i * right_h, w * 0.5, right_h, i + 1))
    return cells


# ---------------------------------------------------------------------------
# SVG builder
# ---------------------------------------------------------------------------

def build_svg_image_letter(
    letter:      str,
    data_urls:   list[str],
    grid_style:  GridStyle,
    font_family: str,
    w_in:        float,
    h_in:        float,
    idx:         int = 0,
    dpi:         int = 96,
    stroke_color:  str   = "rgba(0,0,0,0.30)",
    stroke_width:  float = 8.0,
    gap_px:        float = 3.0,
) -> str:
    """
    Return a self-contained ``<svg>`` string where the *letter* shape acts as
    a clip-path revealing a photo mosaic beneath.

    The stroke outline is painted on top (outside the clip) so the letter
    boundary remains crisp regardless of image content.

    Parameters
    ----------
    letter       : Single uppercase character.
    data_urls    : Pre-encoded image data-URLs.
    grid_style   : Layout style for the photo mosaic.
    font_family  : CSS font-family string (display name, not key).
    w_in / h_in  : Page dimensions in inches.
    idx          : Letter index — used as RNG seed.
    dpi          : Pixel density for the SVG viewport.
    stroke_color : CSS colour for the letter outline drawn on top.
    stroke_width : Width in SVG user units of the outline stroke.
    gap_px       : Gap between mosaic cells in SVG units.
    """
    W, H  = w_in * dpi, h_in * dpi
    rng   = random.Random(idx * 3571 + hash(letter) % 9973)

    # Pick a random subset of images for this letter (max 6)
    n_pick   = min(len(data_urls), rng.randint(2, 6) if len(data_urls) > 1 else 1)
    chosen   = rng.sample(data_urls, n_pick)

    # Letter geometry
    font_size = H * 0.82
    cx, cy    = W / 2, H / 2
    baseline  = cy + font_size * 0.30

    # Bounding box estimate for the photo region
    lw = font_size * 0.72
    lh = font_size * 0.88
    lx = cx - lw / 2
    ly = cy - lh / 2 + font_size * 0.04

    cells    = compute_grid_cells(grid_style, len(chosen), lx, ly, lw, lh, rng)
    clip_id  = f"lbclip_{idx}_{abs(hash(letter)) % 99991}"
    font_ref = f"'{font_family}', 'Lilita One', Impact, Arial Black, sans-serif"

    img_elems = []
    for cell in cells:
        url = chosen[cell["img"] % len(chosen)]
        # Apply a small inset gap
        ix = cell["x"] + gap_px / 2
        iy = cell["y"] + gap_px / 2
        iw = max(cell["w"] - gap_px, 1)
        ih = max(cell["h"] - gap_px, 1)
        img_elems.append(
            f'  <image x="{ix:.2f}" y="{iy:.2f}" width="{iw:.2f}" height="{ih:.2f}" '
            f'preserveAspectRatio="xMidYMid slice" '
            f'clip-path="url(#{clip_id})" '
            f'href="{url}"/>'
        )

    images_block = "\n".join(img_elems)

    return f"""<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {W:.2f} {H:.2f}"
     width="{W:.2f}" height="{H:.2f}"
     style="position:absolute;inset:0;z-index:1;pointer-events:none;">
  <defs>
    <clipPath id="{clip_id}">
      <text x="{cx:.2f}" y="{baseline:.2f}"
            text-anchor="middle"
            font-family="{font_ref}"
            font-size="{font_size:.2f}"
            font-weight="900">{letter}</text>
    </clipPath>
  </defs>
{images_block}
  <!-- stroke outline on top for crisp edges -->
  <text x="{cx:.2f}" y="{baseline:.2f}"
        text-anchor="middle"
        font-family="{font_ref}"
        font-size="{font_size:.2f}"
        font-weight="900"
        fill="none"
        stroke="{stroke_color}"
        stroke-width="{stroke_width:.1f}"
        paint-order="stroke">{letter}</text>
</svg>"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ensure_heif() -> None:
    try:
        import pillow_heif  # noqa: F401
        pillow_heif.register_heif_opener()
    except ImportError:
        raise ImportError(
            "pillow-heif is required for HEIC/HEIF images.\n"
            "Install:  pip install pillow pillow-heif"
        )
