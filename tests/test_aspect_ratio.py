from pictex import *

def test_aspect_ratio_16_9_with_width(file_regression, render_engine):
    """
    Tests that aspect_ratio maintains 16:9 proportion when width is specified.
    Height should be automatically calculated (400 / (16/9) = 225).
    """
    render_func, check_func = render_engine

    element = Row(
        Text("16:9 Video")
    ).size(width=400).aspect_ratio(16/9).background_color("#3498db").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_aspect_ratio_1_1_square(file_regression, render_engine):
    """
    Tests that aspect_ratio creates a perfect square (1:1 ratio).
    """
    render_func, check_func = render_engine

    element = Column(
        Text("Square")
    ).size(width=300).aspect_ratio(1).background_color("#e74c3c").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_aspect_ratio_9_16_portrait(file_regression, render_engine):
    """
    Tests that aspect_ratio maintains 9:16 portrait proportion.
    Useful for vertical story formats (Instagram, TikTok).
    """
    render_func, check_func = render_engine

    element = Row(
        Text("Story 9:16")
    ).size(height=480).aspect_ratio(9/16).background_color("#9b59b6").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_aspect_ratio_string_format(file_regression, render_engine):
    """
    Tests that aspect_ratio accepts string format like "4/3".
    """
    render_func, check_func = render_engine

    element = Row(
        Text("4:3 Format")
    ).size(width=400).aspect_ratio("4/3").background_color("#1abc9c").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_aspect_ratio_with_multiple_elements(file_regression, render_engine):
    """
    Tests aspect_ratio in a layout with multiple elements.
    """
    render_func, check_func = render_engine

    element = Row(
        Column(Text("16:9")).size(width=200).aspect_ratio(16/9).background_color("#f39c12").padding(10),
        Column(Text("1:1")).size(width=200).aspect_ratio(1).background_color("#2ecc71").padding(10),
        Column(Text("9:16")).size(width=150).aspect_ratio(9/16).background_color("#3498db").padding(10)
    ).gap(20).background_color("#ecf0f1").padding(30)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_aspect_ratio_golden_ratio(file_regression, render_engine):
    """
    Tests the golden ratio (approximately 1.618), commonly used in design.
    """
    render_func, check_func = render_engine

    element = Row(
        Text("Golden Ratio")
    ).size(width=400).aspect_ratio(1.618).background_color("#e67e22").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_aspect_ratio_with_flex_grow(file_regression, render_engine):
    """
    Tests that aspect_ratio works correctly with flex_grow.
    """
    render_func, check_func = render_engine

    element = Row(
        Column(Text("Fixed")).size(width=100, height=100).background_color("#95a5a6").padding(10),
        Column(Text("Flexible 16:9"))
            .flex_grow(1)
            .aspect_ratio(16/9)
            .background_color("#2980b9")
            .padding(10)
    ).size(width=600, height=200).gap(20).background_color("#ecf0f1").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)
