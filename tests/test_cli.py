"""
Tests for letter_banner.cli (command-line interface).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from letter_banner.cli import main


class TestCLI:
    def test_basic_color_mode(self, tmp_path):
        rc = main(["HELLO", "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0
        assert (tmp_path / "out.html").exists()

    def test_outline_mode(self, tmp_path):
        rc = main([
            "HI",
            "--mode", "outline",
            "--outline-color", "#ff0000",
            "--no-pdf", "-o", str(tmp_path / "out"),
        ])
        assert rc == 0

    def test_all_palette_names(self, tmp_path):
        from letter_banner import list_palettes
        for name in list_palettes():
            rc = main(["A", "--palette", name, "--no-pdf", "-o", str(tmp_path / f"p_{name}")])
            assert rc == 0, f"palette {name!r} failed"

    def test_all_paper_sizes(self, tmp_path):
        from letter_banner.fonts import PAPER_SIZES
        for paper in PAPER_SIZES:
            rc = main(["A", "--paper", paper, "--no-pdf", "-o", str(tmp_path / f"paper_{paper}")])
            assert rc == 0

    def test_all_deco_styles(self, tmp_path):
        for deco in ("none", "minimal", "dots", "shapes", "festive", "confetti"):
            rc = main(["A", "--deco", deco, "--no-pdf", "-o", str(tmp_path / f"deco_{deco}")])
            assert rc == 0

    def test_list_palettes_exits_zero(self, capsys):
        rc = main(["--list-palettes"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "pastel" in out

    def test_list_fonts_exits_zero(self, capsys):
        rc = main(["--list-fonts"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "bold" in out

    def test_image_mode_without_images_exits_nonzero(self, tmp_path):
        with pytest.raises(SystemExit) as exc:
            main(["A", "--mode", "image", "--no-pdf", "-o", str(tmp_path / "out")])
        assert exc.value.code != 0

    def test_no_text_exits_nonzero(self):
        rc = main([])
        assert rc != 0

    def test_label_flag(self, tmp_path):
        rc = main(["A", "--label", "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0
        html = (tmp_path / "out.html").read_text()
        assert "lb-label" in html

    def test_font_preset(self, tmp_path):
        rc = main(["A", "--font", "kids", "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0

    def test_custom_title(self, tmp_path):
        rc = main(["A", "--title", "My Party", "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0
        html = (tmp_path / "out.html").read_text()
        assert "My Party" in html

    def test_page_bg_white(self, tmp_path):
        rc = main(["A", "--page-bg", "#ffffff", "--deco", "none",
                   "--dot-opacity", "0", "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0
        html = (tmp_path / "out.html").read_text()
        assert "#ffffff" in html

    def test_page_bg_transparent(self, tmp_path):
        rc = main(["A", "--page-bg", "transparent", "--deco", "none",
                   "--dot-opacity", "0", "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0
        html = (tmp_path / "out.html").read_text()
        assert "transparent" in html

    def test_shortcut_clean(self, tmp_path):
        rc = main(["A", "--clean", "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0
        html = (tmp_path / "out.html").read_text()
        assert "transparent" in html
        assert "transparent" in html

    def test_shortcut_clean_white(self, tmp_path):
        rc = main(["A", "--clean-white", "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0
        html = (tmp_path / "out.html").read_text()
        assert "#ffffff" in html

    def test_shortcut_filled(self, tmp_path):
        rc = main(["A", "--filled", "--palette", "vivid",
                   "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0
        html = (tmp_path / "out.html").read_text()
        assert "#ffffff" in html

    def test_shortcut_overridden_by_explicit_flag(self, tmp_path):
        # --clean sets transparent, but --page-bg overrides it
        rc = main(["A", "--clean", "--page-bg", "#ff0000",
                   "--no-pdf", "-o", str(tmp_path / "out")])
        assert rc == 0
        html = (tmp_path / "out.html").read_text()
        assert "#ff0000" in html
