"""
Tests for letter_banner.images (image discovery and grid layout).
"""
from __future__ import annotations

import io
from pathlib import Path

import pytest

from letter_banner.images import (
    GRID_STYLES,
    collect_images,
    compute_grid_cells,
)
import random


# ---------------------------------------------------------------------------
# collect_images
# ---------------------------------------------------------------------------

class TestCollectImages:
    def test_single_file(self, tmp_path):
        f = tmp_path / "photo.jpg"
        f.write_bytes(b"JFIF")
        result = collect_images(f)
        assert result == [f]

    def test_directory(self, tmp_path):
        for name in ("a.jpg", "b.png", "c.webp", "ignore.txt"):
            (tmp_path / name).write_bytes(b"x")
        result = collect_images(tmp_path)
        assert len(result) == 3
        assert all(p.suffix.lower() in {".jpg", ".png", ".webp"} for p in result)

    def test_empty_directory_raises(self, tmp_path):
        (tmp_path / "readme.txt").write_text("hi")
        with pytest.raises(FileNotFoundError, match="No supported"):
            collect_images(tmp_path)

    def test_nonexistent_path_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            collect_images(tmp_path / "ghost.jpg")

    def test_unsupported_extension_raises(self, tmp_path):
        f = tmp_path / "movie.mp4"
        f.write_bytes(b"x")
        with pytest.raises(ValueError, match="Unsupported"):
            collect_images(f)


# ---------------------------------------------------------------------------
# compute_grid_cells
# ---------------------------------------------------------------------------

class TestComputeGridCells:
    """Verify that every grid style returns non-overlapping, valid cells."""

    def _cells(self, style, n, w=400, h=500):
        rng = random.Random(42)
        return compute_grid_cells(style, n, 0, 0, w, h, rng)

    def test_single_returns_one_cell(self):
        cells = self._cells("single", 5)
        assert len(cells) == 1

    def test_n1_always_one_cell(self):
        for style in GRID_STYLES:
            if style == "random":
                continue
            cells = self._cells(style, 1)
            assert len(cells) >= 1

    def test_grid_fills_n_cells(self):
        for n in range(2, 8):
            cells = self._cells("grid", n)
            assert len(cells) == n

    def test_strips_h_fills(self):
        cells = self._cells("strips_h", 4)
        assert len(cells) == 4
        assert all(c["w"] == 400 for c in cells)

    def test_strips_v_fills(self):
        cells = self._cells("strips_v", 3)
        assert len(cells) == 3
        assert all(c["h"] == 500 for c in cells)

    def test_mosaic_various_n(self):
        for n in range(1, 8):
            cells = self._cells("mosaic", n)
            assert len(cells) >= 1

    def test_all_cells_have_positive_dimensions(self):
        for style in GRID_STYLES:
            if style == "random":
                continue
            for n in (1, 3, 5):
                cells = self._cells(style, n)
                for c in cells:
                    assert c["w"] > 0, f"style={style} n={n}: w<=0"
                    assert c["h"] > 0, f"style={style} n={n}: h<=0"

    def test_img_index_within_range(self):
        for style in GRID_STYLES:
            if style == "random":
                continue
            for n in (2, 4, 6):
                cells = self._cells(style, n)
                for c in cells:
                    assert 0 <= c["img"] < n, f"style={style} n={n}: img out of range"
