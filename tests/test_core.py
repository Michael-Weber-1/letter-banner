"""
Tests for letter_banner.core (HTML generation, config validation).
Run with:  pytest
"""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

import pytest

from letter_banner import (
    BannerConfig,
    Theme,
    generate_html,
    list_fonts,
    list_palettes,
    save_banner,
)


# ---------------------------------------------------------------------------
# BannerConfig validation
# ---------------------------------------------------------------------------

class TestBannerConfig:
    def test_defaults_are_valid(self):
        cfg = BannerConfig()
        cfg.validate()  # should not raise

    def test_invalid_mode(self):
        cfg = BannerConfig(mode="laser")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="mode"):
            cfg.validate()

    def test_image_mode_without_source(self):
        cfg = BannerConfig(mode="image")
        with pytest.raises(ValueError, match="image_source"):
            cfg.validate()

    def test_invalid_paper(self):
        cfg = BannerConfig(paper="A9")
        with pytest.raises(ValueError, match="paper"):
            cfg.validate()

    def test_invalid_decoration(self):
        cfg = BannerConfig(decoration="glitter")
        with pytest.raises(ValueError, match="decoration"):
            cfg.validate()

    def test_invalid_font_size(self):
        cfg = BannerConfig(font_size=1.5)
        with pytest.raises(ValueError, match="font_size"):
            cfg.validate()

    def test_palette_override_accepted(self):
        cfg = BannerConfig(
            palette_override=[
                Theme(bg="#fff", dot="#ccc", fill="#f00", stroke="#800", accent="#fcc"),
            ]
        )
        cfg.validate()

    def test_theme_bad_hex(self):
        with pytest.raises(ValueError):
            Theme(bg="red", dot="#ccc", fill="#f00", stroke="#800", accent="#fcc")


# ---------------------------------------------------------------------------
# generate_html
# ---------------------------------------------------------------------------

class TestGenerateHtml:
    def _html(self, text, **kwargs):
        cfg = BannerConfig(**kwargs) if kwargs else None
        return generate_html(text, cfg)

    def test_returns_string(self):
        assert isinstance(self._html("HI"), str)

    def test_contains_doctype(self):
        html = self._html("A")
        assert "<!DOCTYPE html>" in html

    def test_one_page_per_letter(self):
        html = self._html("ABC")
        assert html.count('class="lb-page"') == 3

    def test_spaces_are_skipped(self):
        html = self._html("A B C")
        assert html.count('class="lb-page"') == 3

    def test_empty_text_raises(self):
        with pytest.raises(ValueError):
            generate_html("   ")

    def test_color_mode_contains_fill(self):
        html = self._html("X", mode="color", palette_name="vivid")
        assert "color:" in html

    def test_outline_mode_transparent(self):
        html = self._html("X", mode="outline", outline_color="#ff0000")
        assert "transparent" in html
        assert "#ff0000" in html

    def test_all_palettes_generate(self):
        for name in list_palettes():
            html = generate_html("AB", BannerConfig(palette_name=name))
            assert "lb-page" in html

    def test_all_font_presets_generate(self):
        for key in list_fonts():
            html = generate_html("A", BannerConfig(font=key))
            assert "lb-page" in html

    def test_custom_title(self):
        html = generate_html("X", title="My Custom Banner")
        assert "<title>My Custom Banner</title>" in html

    def test_all_paper_sizes(self):
        from letter_banner.fonts import PAPER_SIZES
        for paper in PAPER_SIZES:
            html = generate_html("A", BannerConfig(paper=paper))
            assert f"{PAPER_SIZES[paper][0]}in" in html

    def test_all_decoration_styles(self):
        from letter_banner.decorations import DECORATION_STYLES
        for style in DECORATION_STYLES:
            html = generate_html("A", BannerConfig(decoration=style))
            assert "lb-page" in html

    def test_google_fonts_link_present(self):
        html = self._html("A")
        assert "fonts.googleapis.com" in html

    def test_show_label(self):
        html = generate_html("X", BannerConfig(show_label=True))
        assert 'class="lb-label"' in html

    def test_no_label_by_default(self):
        html = generate_html("X")
        assert 'class="lb-label"' not in html

    def test_page_bg_override(self):
        html = generate_html("X", BannerConfig(page_bg="#ff0000"))
        assert "background:#ff0000" in html

    def test_page_bg_transparent(self):
        html = generate_html("X", BannerConfig(page_bg="transparent"))
        assert "background:transparent" in html

    def test_page_bg_default_uses_palette(self):
        # When page_bg is empty, palette bg should be used (not literal "")
        html = generate_html("X", BannerConfig(page_bg=""))
        assert "background:;" not in html


# ---------------------------------------------------------------------------
# save_banner
# ---------------------------------------------------------------------------

class TestSaveBanner:
    def test_saves_html(self, tmp_path):
        result = save_banner(
            "HI",
            output_basename=str(tmp_path / "out"),
            write_html=True,
            write_pdf=False,
        )
        assert "html" in result
        assert result["html"].exists()
        assert result["html"].stat().st_size > 0

    def test_html_contains_pages(self, tmp_path):
        result = save_banner(
            "HELLO",
            output_basename=str(tmp_path / "out"),
            write_html=True,
            write_pdf=False,
        )
        content = result["html"].read_text(encoding="utf-8")
        assert content.count('class="lb-page"') == 5

    def test_no_pdf_without_weasyprint(self, tmp_path, monkeypatch):
        """save_banner should not crash when neither PDF backend is available."""
        import builtins
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name in ("weasyprint", "pdfkit"):
                raise ImportError("mocked absence")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        # generate_pdf will raise RuntimeError; save_banner catches it gracefully
        result = save_banner(
            "A",
            output_basename=str(tmp_path / "out"),
            write_html=True,
            write_pdf=True,
        )
        assert "html" in result
        assert "pdf" not in result

    def test_custom_palette_override(self, tmp_path):
        cfg = BannerConfig(
            palette_override=[
                Theme(bg="#ffffff", dot="#ff0000", fill="#ff0000", stroke="#880000", accent="#ffcccc"),
            ]
        )
        result = save_banner(
            "X",
            cfg,
            output_basename=str(tmp_path / "out"),
            write_html=True,
            write_pdf=False,
        )
        html = result["html"].read_text()
        assert "#ff0000" in html


# ---------------------------------------------------------------------------
# Palettes & fonts listing
# ---------------------------------------------------------------------------

class TestListFunctions:
    def test_list_palettes_returns_list(self):
        names = list_palettes()
        assert isinstance(names, list)
        assert len(names) > 0
        assert all(isinstance(n, str) for n in names)

    def test_list_fonts_returns_list(self):
        keys = list_fonts()
        assert isinstance(keys, list)
        assert "bold" in keys

    def test_get_palette_unknown_raises(self):
        from letter_banner import get_palette
        with pytest.raises(ValueError, match="Unknown palette"):
            get_palette("nonexistent_palette_xyz")
