from pictex import *


def test_flex_grow_basic(file_regression, render_engine):
    """Test that flex_grow allows elements to fill available space proportionally."""
    render_func, check_func = render_engine
    
    test_case = Row(
        Text("Fixed").size(width=100).background_color("#3498db").padding(10),
        Text("Grow x1").flex_grow(1).background_color("#e74c3c").padding(10),
        Text("Grow x2").flex_grow(2).background_color("#2ecc71").padding(10),
    ).size(width=600).background_color("#ecf0f1")
    
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)


def test_flex_shrink_prevents_shrinking(file_regression, render_engine):
    """Test that flex_shrink(0) prevents an element from shrinking."""
    render_func, check_func = render_engine
    
    test_case = Row(
        Text("Don't shrink").flex_shrink(0).size(width=300).background_color("#3498db").padding(10),
        Text("Can shrink").flex_shrink(1).size(width=300).background_color("#e74c3c").padding(10),
    ).size(width=400).background_color("#ecf0f1")
    
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)


def test_align_self_overrides_container(file_regression, render_engine):
    """Test that align_self overrides the container's align_items."""
    render_func, check_func = render_engine
    
    test_case = Row(
        Text("A").font_size(80).background_color("#3498db"),
        Text("B (end)").font_size(60).align_self('end').background_color("#e74c3c"),
        Text("C (center)").font_size(40).align_self('center').background_color("#2ecc71"),
        Text("D").font_size(50).background_color("#f39c12"),
    ).align_items('start').size(height=200).background_color("#ecf0f1")
    
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)


def test_flex_wrap_creates_grid(file_regression, render_engine):
    """Test that flex_wrap enables multi-line layouts."""
    render_func, check_func = render_engine
    
    items = [
        Text(f"Item {i}").size(width=80).background_color("#3498db" if i % 2 == 0 else "#e74c3c").padding(10)
        for i in range(12)
    ]
    
    test_case = Row(*items).flex_wrap('wrap').size(width=350).gap(10).background_color("#ecf0f1").padding(10)
    
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)


def test_flex_wrap_with_align_items(file_regression, render_engine):
    """Test flex_wrap combined with align_items."""
    render_func, check_func = render_engine
    
    items = [
        Text("Short").background_color("#3498db").padding(10),
        Text("Tall\nItem").background_color("#e74c3c").padding(10),
        Text("Medium").background_color("#2ecc71").padding(10),
        Text("Another\nTall\nOne").background_color("#f39c12").padding(10),
        Text("Last").background_color("#9b59b6").padding(10),
    ]
    
    test_case = Row(*items).flex_wrap('wrap').align_items('center').size(width=300).gap(10).background_color("#ecf0f1").padding(10)
    
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)


def test_combined_flex_properties(file_regression, render_engine):
    """Test combining multiple flex properties."""
    render_func, check_func = render_engine
    
    test_case = Row(
        Text("Fixed").size(width=80).flex_shrink(0).background_color("#3498db").padding(10),
        Text("Flexible").flex_grow(1).background_color("#e74c3c").padding(10),
        Text("Aligned").flex_grow(1).align_self('end').background_color("#2ecc71").padding(10),
    ).size(width=500, height=150).align_items('start').background_color("#ecf0f1")
    
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)
