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
    the positioning calculations are correct.
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
    the canvas dimensions.
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

def test_place_with_nested_children(file_regression, render_engine):
    """Tests that place() works with nested children."""
    render_func, check_func = render_engine

    container = (
        Row(
            Column(
                Text("This should be centered"),
                Text("Another text"),
            ),
        )
        .place("center", "center")
        .border(width=5, color="red")
    )

    canvas = Canvas().size(500, 500).background_color("pink")
    image = render_func(canvas, container)
    check_func(file_regression, image)


def test_container_with_place(file_regression, render_engine):
    """Test a container with place positioning using pixel values (FIXED)."""
    render_func, check_func = render_engine
    
    container = Row(Column("test").place(0, 0)).size(100, 100)
    image = render_func(Canvas(), container)
    check_func(file_regression, image)


def test_absolute_position_with_inset(file_regression, render_engine):
    """Test absolute_position with CSS-style inset values (parent-relative)."""
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

def test_translate_with_nested_children(file_regression, render_engine):
    """Test using translate with nested children."""
    render_func, check_func = render_engine
    
    with_translate = (
        Row(Text("With translate child"))
        .absolute_position(top="50%", left="50%")
        .translate(x="-50%", y="-50%")
        .background_color("#9b59b6")
        .padding(10)
    )
    without_translate = Text("Without translate child")

    container = Column(without_translate, with_translate).size(400, 400).background_color("pink")
    image = render_func(Canvas(), container)
    check_func(file_regression, image)


def test_fixed_position_canvas_relative(file_regression, render_engine):
    """Test that fixed_position elements are positioned relative to canvas root."""
    render_func, check_func = render_engine
    
    element = Row(
        Column(
            Text("FIXED")
            .fixed_position(top=10, left=10)
            .background_color("#e74c3c")
            .padding(5)
        ).size(width=100, height=100).background_color("#f8d7da").padding(20)
    ).size(width=200, height=150).background_color("#d1ecf1").padding(30)
    
    image = render_func(Canvas().size(300, 200).background_color("#ecf0f1"), element)
    check_func(file_regression, image)


def test_fixed_vs_absolute_positioning(file_regression, render_engine):
    """Test the difference between fixed (canvas-relative) and absolute (parent-relative)."""
    render_func, check_func = render_engine
    
    element = Row(
        Text("FIXED").fixed_position(top=50, left=50).background_color("#28a745").color("white").padding(5),
        Text("ABS").absolute_position(top=50, left=50).background_color("#dc3545").color("white").padding(5),
    ).size(width=200, height=150).background_color("#ffc107").padding(20).border(25, "red").margin(30)
    
    image = render_func(Canvas().size(400, 300).background_color("#6c757d"), element)
    check_func(file_regression, image)


def test_relative_position_offset(file_regression, render_engine):
    """Test relative_position offsets element from its normal flow position."""
    render_func, check_func = render_engine
    
    element = Row(
        Text("A").background_color("#17a2b8").padding(10),
        Text("B")
        .relative_position(top=-10, left=20)  # Nudged up and right
        .background_color("#ffc107")
        .padding(10),
        Text("C").background_color("#28a745").padding(10),
    ).gap(10).background_color("#f8f9fa").padding(20)
    
    image = render_func(Canvas(), element)
    check_func(file_regression, image)


def test_fixed_with_canvas_box_model(file_regression, render_engine):
    """Test that fixed_position ignores canvas margin/padding/border."""
    render_func, check_func = render_engine
    
    element = Row(
        Text("FIXED@0,0").fixed_position(top=0, left=0).background_color("#fff").color("#000").padding(3),
        Text("ABS@0,0").absolute_position(top=0, left=0).background_color("#ff0").color("#000").padding(3),
    )
    
    canvas = Canvas()\
        .margin(25)\
        .padding(25)\
        .border(25, "red")\
        .background_color("blue")\
        .size(200, 200)
    
    image = render_func(canvas, element)
    check_func(file_regression, image)


def test_multiple_fixed_elements(file_regression, render_engine):
    """Test multiple fixed elements at different canvas positions."""
    render_func, check_func = render_engine
    
    element = Row(
        Text("TL").fixed_position(top=10, left=10).background_color("#007bff").color("white").padding(5),
        Text("TR").fixed_position(top=10, right=10).background_color("#28a745").color("white").padding(5),
        Text("BL").fixed_position(bottom=10, left=10).background_color("#ffc107").padding(5),
        Text("BR").fixed_position(bottom=10, right=10).background_color("#dc3545").color("white").padding(5),
    ).size(width=200, height=150).background_color("#e9ecef").padding(30)
    
    image = render_func(Canvas().size(300, 200).background_color("#dee2e6"), element)
    check_func(file_regression, image)
