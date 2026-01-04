"""Stretchable-based layout engine implementation.

This module provides a layout engine that uses stretchable (Taffy bindings)
for computing CSS-like flexbox layouts.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Callable, Dict, Tuple

from stretchable import Node as StretchableNode, Edge
from stretchable.style.geometry.size import SizePoints, SizeAvailableSpace
from stretchable.style.geometry.length import Scale

from .style_mapper import StyleMapper
from .layout_result import LayoutResult

from math import ceil

if TYPE_CHECKING:
    from ..nodes import Node, TextNode


class LayoutEngine:
    def __init__(self):
        self._node_map: Dict['Node', StretchableNode] = {}
        self._style_mapper = StyleMapper()

    def compute_layout(self, root: 'Node') -> None:
        """Compute layout using stretchable's flexbox algorithm."""
        self._node_map.clear()

        stretchable_root = self._build_stretchable_tree(root)
        stretchable_root.compute_layout()
        
        self._link_layout_results(root, stretchable_root)
        
        root_box = stretchable_root.get_box(Edge.MARGIN, relative=False)
        origin = (root_box.x, root_box.y)
        self._fix_canvas_relative_positions(root, origin)

    def _build_stretchable_tree(self, node: 'Node') -> StretchableNode:
        """Recursively build stretchable node tree from pictex node tree."""
        style = self._create_style_for_node(node)
        measure_fn = self._create_measure_function(node)
        stretchable_node = StretchableNode(style=style, measure=measure_fn)
        self._node_map[node] = stretchable_node
        
        for child in node.children:
            child_stretchable = self._build_stretchable_tree(child)
            stretchable_node.add(child_stretchable)
        
        return stretchable_node

    def _create_style_for_node(self, node: 'Node'):
        """Create appropriate stretchable style based on node type."""
        from ..nodes import RowNode, ColumnNode
        
        if isinstance(node, RowNode):
            return self._style_mapper.create_row_style(node)
        elif isinstance(node, ColumnNode):
            return self._style_mapper.create_column_style(node)
        else:
            return self._style_mapper.create_leaf_style(node)

    def _create_measure_function(self, node: 'Node') -> Optional[Callable]:
        """Create measure function for leaf nodes."""
        from ..nodes import TextNode
        
        if node.children:
            return None
        
        if isinstance(node, TextNode):
            return self._create_text_node_measure_function(node)
        
        return self._create_non_text_node_measure_function(node)

    def _create_text_node_measure_function(self, text_node: 'TextNode') -> Callable:
        """Create measure function for TextNode with text wrapping support."""
        def measure(_node: StretchableNode, _known_size: SizePoints, available_space: SizeAvailableSpace) -> SizePoints:
            text_node._clear_bounds()
            text_node.set_text_wrap_width(None)
            wrap_width = None

            if available_space.width is not None:
                if available_space.width.scale == Scale.POINTS:
                    wrap_width = available_space.width.value
                elif available_space.width.scale == Scale.MIN_CONTENT:
                    wrap_width = 0
            
            if wrap_width is not None:
                # We need to use ceil here since the text content bounds are computed using ceil
                # If we use floor (or the float value) here, the text may be cut off in some edge cases
                text_node.set_text_wrap_width(ceil(wrap_width))
            
            width = text_node.compute_intrinsic_width()
            height = text_node.compute_intrinsic_height()
            text_node._clear_bounds()

            # This could cause an issue:
            # Stretchable is using float width/height
            # However, we're using integer bounds in pictex for skia (to avoid rendering artefacs with float)
            # Keep this in mind if a weird bug appears
            return SizePoints(float(width), float(height))
        
        return measure

    def _create_non_text_node_measure_function(self, node: 'Node') -> Callable:
        """Create generic measure function for non-text leaf nodes."""
        def measure(_node: StretchableNode, _known_size: SizePoints, _available_space: SizeAvailableSpace) -> SizePoints:
            node._clear_bounds()
            width = node.compute_intrinsic_width()
            height = node.compute_intrinsic_height()
            node._clear_bounds()
            return SizePoints(float(width), float(height))
        
        return measure

    def _link_layout_results(self, pictex_node: 'Node', stretchable_node: StretchableNode) -> None:
        """Link stretchable layout results back to pictex nodes using parallel traversal."""
        pictex_node.set_layout_result(LayoutResult(stretchable_node))
        
        for pictex_child in pictex_node.children:
            stretchable_child = self._get_stretchable_node(pictex_child)
            self._link_layout_results(pictex_child, stretchable_child)

    def _fix_canvas_relative_positions(self, pictex_node: 'Node', origin: Tuple[float, float]) -> None:
        """Recursively fix FIXED position elements to be canvas-relative.
        
        FIXED elements are positioned relative to the canvas, not their parent.
        This method calculates the required offset and updates LayoutResult accordingly.
        """
        from ..models import PositionType

        for pictex_child in pictex_node.children:
            position_config = pictex_child.computed_styles.position.get()
            is_fixed = position_config and position_config.type == PositionType.FIXED

            if is_fixed:
                stretchable_child = self._get_stretchable_node(pictex_child)
                stretchable_parent = self._get_stretchable_node(pictex_node)
                parent_box = stretchable_parent.get_box(Edge.PADDING, relative=False)
                offset_x = -abs(origin[0] - parent_box.x)
                offset_y = -abs(origin[1] - parent_box.y)
                pictex_child._clear_bounds()
                pictex_child.set_layout_result(LayoutResult(stretchable_child, offset_x, offset_y))

            self._fix_canvas_relative_positions(pictex_child, origin)

    def _get_stretchable_node(self, pictex_node: 'Node') -> StretchableNode:
        if pictex_node not in self._node_map:
            raise ValueError(f"Node {pictex_node} not found in node map")
        return self._node_map[pictex_node]
