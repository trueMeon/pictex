from pictex import *

def test_max_width_prevents_overflow(file_regression, render_engine):
    """
    Tests that max_width prevents an element from growing beyond the
    specified maximum, even when content would normally make it wider.
    """
    render_func, check_func = render_engine

    element = Row(
        Text("Label:").size(width=80).background_color("#95a5a6").padding(10),
        Text("This is a very long product name that should be constrained by max width")
            .size(width="fit-content")
            .max_width(150)
            .background_color("#3498db")
            .padding(10),
        Text("$99").size(width=50).background_color("#95a5a6").padding(10)
    ).gap(10).background_color("#ecf0f1").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_min_width_prevents_collapse(file_regression, render_engine):
    """
    Tests that min_width ensures an element maintains a minimum width,
    even when content is shorter than the constraint.
    """
    render_func, check_func = render_engine

    element = Row(
        Text("Short").min_width(300).background_color("#e74c3c").padding(10),
        Text("This is longer text").background_color("#2ecc71").padding(10)
    ).gap(10).background_color("#ecf0f1").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_max_height_limits_vertical_growth(file_regression, render_engine):
    """
    Tests that max_height limits the vertical size of an element.
    """
    render_func, check_func = render_engine

    element = Column(
        Text("Header").background_color("#9b59b6").padding(10),
        Text("This is a description that has a max height constraint applied to limit its vertical growth")
            .max_height(60)
            .background_color("#f1c40f")
            .padding(10),
        Text("Footer").background_color("#1abc9c").padding(10)
    ).gap(10).background_color("#ecf0f1").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_min_height_ensures_minimum_space(file_regression, render_engine):
    """
    Tests that min_height ensures an element maintains a minimum height,
    even when content is shorter.
    """
    render_func, check_func = render_engine

    element = Column(
        Text("Header").background_color("#34495e").padding(10),
        Text("Short content").min_height(100).background_color("#e67e22").padding(10),
        Text("Footer").background_color("#34495e").padding(10)
    ).gap(10).background_color("#ecf0f1").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_max_width_with_flex_grow(file_regression, render_engine):
    """
    Tests that max_width works correctly with flex_grow, preventing
    unlimited growth while still allowing the element to be flexible.
    """
    render_func, check_func = render_engine

    element = Row(
        Text("Fixed").size(width=100).background_color("#c0392b").padding(10),
        Text("Grows but limited")
            .flex_grow(1)
            .max_width(150)
            .background_color("#27ae60")
            .padding(10)
            .text_wrap("nowrap"),
        Text("Grows unlimited")
            .flex_grow(1)
            .background_color("#2980b9")
            .padding(10)
            .text_wrap("nowrap")
    ).size(width=500, height=100).gap(10).background_color("#ecf0f1").padding(10)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_min_width_with_flex_shrink(file_regression, render_engine):
    """
    Tests that min_width prevents an element from shrinking below
    the minimum, even with flex_shrink enabled.
    """
    render_func, check_func = render_engine

    element = Row(
        Text("Cannot shrink below 150px")
            .size(width=200)
            .min_width(150)
            .flex_shrink(1)
            .background_color("#8e44ad")
            .padding(10)
            .text_wrap("nowrap"),
        Text("Can shrink freely")
            .size(width=200)
            .flex_shrink(1)
            .background_color("#16a085")
            .padding(10)
            .text_wrap("nowrap")
    ).size(width=300, height=100).gap(10).background_color("#ecf0f1").padding(10)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_size_constraints_with_percentages(file_regression, render_engine):
    """
    Tests that min/max size constraints work with percentage values.
    """
    render_func, check_func = render_engine

    element = Column(
        Text("50% width, min 100px")
            .size(width="50%")
            .min_width(100)
            .background_color("#d35400")
            .padding(10),
        Text("50% width, max 80px")
            .size(width="50%")
            .max_width(80)
            .background_color("#2c3e50")
            .padding(10)
    ).size(width=300, height=200).gap(10).background_color("#ecf0f1").padding(20)

    image = render_func(Canvas(), element)
    check_func(file_regression, image)
