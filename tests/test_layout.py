import pytest
from pictex import Canvas, Row, Column, Text

ROW_CHILDREN = [
    Text("A").font_size(20).background_color("#3498db").padding(10),
    Row(Text("B")).font_size(40).background_color("#e74c3c").padding(10),
    Text("C").font_size(30).background_color("#2ecc71").padding(10),
]

COLUMN_CHILDREN = [
    Text("Short").background_color("#3498db").padding(10),
    Text("Loooooooooong").background_color("#e74c3c").padding(10),
    Text("Meeedium").background_color("#2ecc71").padding(10),
]

def test_row_default_layout(file_regression, render_engine):
    test_case = Row(*ROW_CHILDREN)
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)

@pytest.mark.parametrize("mode", [
    "start", "center", "end", "space-between", "space-around", "space-evenly"
])
def test_row_horizontal_distribution(file_regression, render_engine, mode):
    test_case = (
        Row(*ROW_CHILDREN)
        .size(width=600)
        .background_color("#ecf0f1")
        .justify_content(mode)
    )
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)

@pytest.mark.parametrize("mode", ["start", "center", "end", "stretch"])
def test_row_vertical_alignment(file_regression, render_engine, mode):
    test_case = (
        Row(*ROW_CHILDREN)
        .size(height=150)
        .background_color("#ecf0f1")
        .align_items(mode)
    )
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)

def test_row_with_gap(file_regression, render_engine):
    test_case = Row(*ROW_CHILDREN).gap(20)
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)

def test_row_with_gap_and_distribution(file_regression, render_engine):
    test_case = (
        Row(*ROW_CHILDREN)
        .size(width=800)
        .background_color("#ecf0f1")
        .gap(20)
        .justify_content('space-around')
    )
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)

def test_column_default_layout(file_regression, render_engine):
    test_case = Column(*COLUMN_CHILDREN)
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)

@pytest.mark.parametrize("mode", [
    "start", "center", "end", "space-between", "space-around", "space-evenly"
])
def test_column_vertical_distribution(file_regression, render_engine, mode):
    test_case = (
        Column(*COLUMN_CHILDREN)
        .size(height=500)
        .background_color("#ecf0f1")
        .justify_content(mode)
    )
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)

@pytest.mark.parametrize("mode", ["start", "center", "end", "stretch"])
def test_column_horizontal_alignment(file_regression, render_engine, mode):
    test_case = (
        Column(*COLUMN_CHILDREN)
        .size(width=300)
        .background_color("#ecf0f1")
        .align_items(mode)
    )
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)

def test_column_with_gap(file_regression, render_engine):
    test_case = Column(*COLUMN_CHILDREN).gap(15)
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)

def test_column_with_gap_and_distribution(file_regression, render_engine):
    test_case = (
        Column(*COLUMN_CHILDREN)
        .size(height=600)
        .background_color("#ecf0f1")
        .gap(15)
        .justify_content('space-between')
    )
    render_func, check_func = render_engine
    image = render_func(Canvas(), test_case)
    check_func(file_regression, image)
