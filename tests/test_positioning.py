from pictex import Canvas, Row, Column, Text, Image


def test_place_absolute_is_removed_from_row_flow(file_regression, render_engine):
    """
    Tests that an element with place() is ignored by the
    Row's layout algorithm. Text 'One' and 'Three' should appear
    next to each other as if 'Two' doesn't exist in the flow.
    """
    render_func, check_func = render_engine

    element = Row(
        Text("One").padding(10).background_color("#3498db"),
        Text("Two")
        .place("center", "center")  # This element is out of the layout flow.
        .padding(10)
        .background_color("#e74c3c"),
        Text("Three").padding(10).background_color("#2ecc71"),
    ).size(
        width=400, height=150  # Give the parent a fixed size for stable positioning.
    ).background_color("#ecf0f1")

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_place_absolute_is_removed_from_column_flow(file_regression, render_engine):
    """
    Tests that an element with place() is ignored by the
    Column's layout algorithm. The logic is the same as for Row, but
    on the vertical axis.
    """
    render_func, check_func = render_engine

    element = Column(
        Text("One").padding(10).background_color("#3498db"),
        Text("Two")
        .place("center", "center")
        .padding(10)
        .background_color("#e74c3c"),
        Text("Three").padding(10).background_color("#2ecc71"),
    ).size(
        width=200, height=300
    ).background_color("#ecf0f1")

    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_place_anchors_and_offsets(file_regression, render_engine):
    """
    Tests various combinations of anchor keywords and pixel offsets to ensure
    the positioning calculations are correct relative to the parent container.
    """
    render_func, check_func = render_engine

    container = Row(
        Text("TL").place("left", "top").background_color("#1abc9c"),
        Text("TR").place("right", "top").background_color("#1abc9c"),
        Text("BL").place("left", "bottom").background_color("#1abc9c"),
        Text("BR").place("right", "bottom").background_color("#1abc9c"),
        Text("Center").place("center", "center").background_color("#9b59b6"),
        Text("Offset").place(
            "left", "top", x_offset=50, y_offset=50
        ).background_color("#f1c40f"),
    ).size(
        width=300, height=200
    ).padding(
        10
    ).background_color("#bdc3c7")

    image = render_func(Canvas(), container)
    check_func(file_regression, image)


def test_place_with_percentages(file_regression, render_engine):
    """
    Tests that percentage-based positions are calculated correctly based on
    the parent's content-box dimensions.
    """
    render_func, check_func = render_engine

    container = Column(
        Text("25% x, 75% y").place("25%", "75%").background_color("#e67e22")
    ).size(
        width=400, height=300
    ).padding(
        50
    ).background_color("#ecf0f1")

    image = render_func(Canvas(), container)
    check_func(file_regression, image)


def test_place_with_mixed_anchors(file_regression, render_engine):
    """
    Tests that a combination of keyword and percentage anchors works as expected.
    Also tests the content anchor calculation (centering the element on the anchor point).
    """
    render_func, check_func = render_engine

    container = Row(
        Text("Centered on 50%, 20px")
        .place("50%", 20)
        .background_color("#34495e")
        .color("white")
        .padding(10)
    ).size(
        width=500, height=200
    ).background_color("#ecf0f1")

    # In this case, '50%' means the element's center is at the 50% mark,
    # because place() applies the corresponding translate automatically.

    image = render_func(Canvas(), container)
    check_func(file_regression, image)


def test_container_with_place(file_regression, render_engine):
    """Test a container with place positioning using pixel values."""
    render_func, check_func = render_engine
    
    container = Row(Column("test").place(0, 0)).size(100, 100)
    image = render_func(Canvas(), container)
    check_func(file_regression, image)


def test_absolute_position_with_inset(file_regression, render_engine):
    """Test absolute_position with CSS-style inset values."""
    render_func, check_func = render_engine
    
    container = Row(
        Text("Top-Left").absolute_position(top=10, left=10).background_color("#3498db"),
        Text("Bottom-Right").absolute_position(bottom=10, right=10).background_color("#e74c3c"),
    ).size(
        width=300, height=200
    ).background_color("#ecf0f1")
    
    image = render_func(Canvas(), container)
    check_func(file_regression, image)


def test_translate_for_centering(file_regression, render_engine):
    """Test using translate for true centering."""
    render_func, check_func = render_engine
    
    container = Row(
        Text("Centered")
        .absolute_position(top="50%", left="50%")
        .translate(x="-50%", y="-50%")
        .background_color("#9b59b6")
        .padding(10)
    ).size(
        width=300, height=200
    ).background_color("#ecf0f1")
    
    image = render_func(Canvas(), container)
    check_func(file_regression, image)
