from pictex import VectorImage, RenderNode, NodeType, Box

def test_vector_image_properties():
    """Tests the basic properties and methods of the VectorImage class."""
    dummy_svg = '<svg width="10" height="10"><rect x="0" y="0" width="10" height="10" fill="red"/></svg>'
    vector_image = VectorImage(svg_content=dummy_svg)

    assert vector_image.svg == dummy_svg
    assert str(vector_image) == dummy_svg
    assert vector_image._repr_svg_() == dummy_svg
    assert vector_image.render_tree is None  # Default is None
    assert isinstance(vector_image, VectorImage)

def test_vector_image_with_render_tree():
    """Tests VectorImage with render tree functionality."""
    dummy_svg = '<svg width="100" height="50"><text x="10" y="20">Hello</text></svg>'
    
    # Create a mock render tree
    text_node = RenderNode(
        bounds=Box(x=10, y=15, width=40, height=20),
        children=[],
        node_type=NodeType.TEXT
    )
    column_node = RenderNode(
        bounds=Box(x=5, y=10, width=50, height=30),
        children=[text_node],
        node_type=NodeType.COLUMN
    )
    root_node = RenderNode(
        bounds=Box(x=0, y=0, width=100, height=50),
        children=[column_node],
        node_type=NodeType.ROW
    )
    
    vector_image = VectorImage(svg_content=dummy_svg, render_tree=root_node)
    
    assert vector_image.svg == dummy_svg
    assert vector_image.render_tree is root_node
    assert vector_image.render_tree.node_type == NodeType.ROW
    assert len(vector_image.render_tree.children) == 1
    
    # Test nested structure
    column_child = vector_image.render_tree.children[0]
    assert column_child.node_type == NodeType.COLUMN
    assert len(column_child.children) == 1
    assert column_child.children[0].node_type == NodeType.TEXT
    
    # Test find_nodes_by_type
    text_nodes = vector_image.render_tree.find_nodes_by_type(NodeType.TEXT)
    assert len(text_nodes) == 1
    assert text_nodes[0].bounds == Box(x=10, y=15, width=40, height=20)
    
    column_nodes = vector_image.render_tree.find_nodes_by_type(NodeType.COLUMN)
    assert len(column_nodes) == 1
    assert column_nodes[0].bounds == Box(x=5, y=10, width=50, height=30)
    
    # Test that we can still use the SVG normally
    assert str(vector_image) == dummy_svg
