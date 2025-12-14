from pictex import Canvas
from .conftest import STATIC_FONT_PATH
import tempfile
import os

def test_svg_with_embedded_font():
    """
    Tests that rendering an SVG with `embed_font=True` includes the
    @font-face and base64 data.
    """
    canvas = Canvas().font_family(STATIC_FONT_PATH).font_size(50)

    vector_image = canvas.render_as_svg("Embed Test", embed_font=True)
    svg_content = vector_image.svg

    assert "<style" in svg_content
    assert "@font-face" in svg_content
    assert "font-family: 'pictex-Lato'" in svg_content
    assert "src: url('data:font/ttf;base64," in svg_content
    assert "format('truetype')" in svg_content

def test_svg_without_embedded_font():
    """
    Tests that rendering an SVG with `embed_font=False` does NOT include
    the font data.
    """
    canvas = Canvas().font_family(STATIC_FONT_PATH).font_size(50)
    vector_image = canvas.render_as_svg("No Embed Test", embed_font=False)
    svg_content = vector_image.svg

    assert "<style" in svg_content
    assert "@font-face" in svg_content
    assert "base64" not in svg_content
    assert "font-family: 'pictex-Lato'" in svg_content

def test_svg_font_auto_copy():
    """
    Tests that fonts are automatically copied when saving with embed_font=False.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        canvas = Canvas().font_family(STATIC_FONT_PATH).font_size(50)
        vector_image = canvas.render_as_svg("Font Copy Test", embed_font=False)
        output_path = os.path.join(temp_dir, "test.svg")
        vector_image.save(output_path)
        fonts_dir = os.path.join(temp_dir, "fonts")
        assert os.path.exists(fonts_dir), "fonts directory should be created"
        assert os.path.isdir(fonts_dir), "fonts should be a directory"
        
        font_basename = os.path.basename(STATIC_FONT_PATH)
        copied_font_path = os.path.join(fonts_dir, font_basename)
        assert os.path.exists(copied_font_path), f"Font file {font_basename} should be copied"
        
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_svg = f.read()
        
        assert f"url('fonts/{font_basename}')" in saved_svg, "SVG should reference font with relative path"
        assert f"url('{font_basename}')" not in saved_svg, "SVG should not contain old reference with only basename"

def test_svg_default_font_copied():
    """
    Tests that the bundled default font (InterVariable.ttf) is copied correctly
    when no font is specified and embed_font=False.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        canvas = Canvas().font_size(50)
        vector_image = canvas.render_as_svg("Default Font Test", embed_font=False)
        output_path = os.path.join(temp_dir, "test_default.svg")
        vector_image.save(output_path)
        
        fonts_dir = os.path.join(temp_dir, "fonts")
        assert os.path.exists(fonts_dir), "fonts directory should be created"
        
        inter_font_path = os.path.join(fonts_dir, "InterVariable.ttf")
        assert os.path.exists(inter_font_path), "InterVariable.ttf should be copied"
        
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_svg = f.read()
        
        assert "url('fonts/InterVariable.ttf')" in saved_svg, "SVG should reference InterVariable.ttf with relative path"

def test_svg_custom_fonts_subdir():
    """
    Tests that custom fonts_subdir parameter works correctly.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        canvas = Canvas().font_family(STATIC_FONT_PATH).font_size(50)
        vector_image = canvas.render_as_svg("Custom Subdir Test", embed_font=False)
        output_path = os.path.join(temp_dir, "test.svg")
        vector_image.save(output_path, fonts_subdir="my-fonts")

        custom_fonts_dir = os.path.join(temp_dir, "my-fonts")
        assert os.path.exists(custom_fonts_dir), "Custom fonts directory should be created"
        
        font_basename = os.path.basename(STATIC_FONT_PATH)
        copied_font_path = os.path.join(custom_fonts_dir, font_basename)
        assert os.path.exists(copied_font_path), "Font should be in custom directory"
        
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_svg = f.read()
        
        assert f"url('my-fonts/{font_basename}')" in saved_svg, "SVG should reference font with custom subdirectory"

def test_svg_copy_fonts_disabled():
    """
    Tests that setting copy_fonts=False prevents font copying.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        canvas = Canvas().font_family(STATIC_FONT_PATH).font_size(50)
        vector_image = canvas.render_as_svg("No Copy Test", embed_font=False)
        
        output_path = os.path.join(temp_dir, "test.svg")
        vector_image.save(output_path, copy_fonts=False)
        
        fonts_dir = os.path.join(temp_dir, "fonts")
        assert not os.path.exists(fonts_dir), "fonts directory should NOT be created"
        
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_svg = f.read()
        
        font_basename = os.path.basename(STATIC_FONT_PATH)
        assert f"url('{font_basename}')" in saved_svg, "SVG should keep basename reference when copy_fonts=False"

def test_svg_embedded_font_no_copy():
    """
    Tests that fonts are NOT copied when embed_font=True (fonts are embedded).
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        canvas = Canvas().font_family(STATIC_FONT_PATH).font_size(50)
        vector_image = canvas.render_as_svg("Embedded No Copy", embed_font=True)
        
        output_path = os.path.join(temp_dir, "test.svg")
        vector_image.save(output_path)
        
        fonts_dir = os.path.join(temp_dir, "fonts")
        assert not os.path.exists(fonts_dir), "fonts directory should NOT be created when fonts are embedded"
