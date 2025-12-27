"""Stretchable-based layout engine implementation.

This module provides a layout engine that uses stretchable (Taffy bindings)
for computing CSS-like flexbox layouts. It replaces the multi-pass layout
algorithm with a single compute_layout() call.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Callable, Dict

from stretchable import Node as StretchableNode
from stretchable.style.geometry.size import SizePoints, SizeAvailableSpace
from stretchable.style.geometry.length import Scale

from .style_mapper import StyleMapper
from .layout_result import LayoutResult

from math import ceil

if TYPE_CHECKING:
    from ..nodes import Node, TextNode, RowNode, ColumnNode
    from ..models import RenderProps


class LayoutEngine:
    def __init__(self):
        """Initialize the layout engine."""
        self._node_map: Dict['Node', StretchableNode] = {}

    def compute_layout(self, root: 'Node') -> None:
        """Compute layout using stretchable's flexbox algorithm.
        
        Args:
            root: The root pictex node to compute layout for.
        """
        self._node_map.clear()
        stretchable_root = self._build_stretchable_tree(root)
        stretchable_root.compute_layout()

        self._link_layout_results(root, stretchable_root)

    def _build_stretchable_tree(self, node: 'Node') -> StretchableNode:
        """Recursively build stretchable node tree from pictex node tree.
        
        Args:
            node: The pictex node to convert.
            
        Returns:
            The corresponding stretchable node with children.
        """
        style = self._create_style_for_node(node)
        measure_fn = self._create_measure_function(node)
        stretchable_node = StretchableNode(style=style, measure=measure_fn)
        self._node_map[node] = stretchable_node
        for child in node.children:
            child_stretchable = self._build_stretchable_tree(child)
            stretchable_node.add(child_stretchable)
        
        return stretchable_node

    def _create_style_for_node(self, node: 'Node'):
        """Create appropriate stretchable style based on node type.
        
        Args:
            node: The pictex node.
            
        Returns:
            StretchableStyle configured for this node type.
        """
        from ..nodes import RowNode, ColumnNode
        
        if isinstance(node, RowNode):
            return StyleMapper.create_row_style(node)
        elif isinstance(node, ColumnNode):
            return StyleMapper.create_column_style(node)
        else:
            return StyleMapper.create_leaf_style(node)

    def _create_measure_function(self, node: 'Node') -> Optional[Callable]:
        """Create measure function for leaf nodes.
        
        Stretchable calls measure functions to determine the intrinsic size
        of nodes that don't have explicit dimensions.
        
        Args:
            node: The pictex node.
            
        Returns:
            Measure function if this is a leaf node, None otherwise.
        """
        from ..nodes import TextNode
        
        # Only create measure functions for leaf nodes
        if node.children:
            return None
        
        if isinstance(node, TextNode):
            return self._create_text_node_measure_function(node)
        
        return self._create_non_text_node_measure_function(node)

    def _create_text_node_measure_function(self, text_node: 'TextNode') -> Callable:
        """Create measure function for TextNode with text wrapping support.
        
        This function preserves text_node in closure for measuring.
        
        Args:
            text_node: The TextNode to measure.
            
        Returns:
            Measure function compatible with stretchable.
        """
        def measure(_node: StretchableNode, _known_size: SizePoints, available_space: SizeAvailableSpace) -> SizePoints:
            text_node._clear_bounds()
            text_node.set_text_wrap_width(None)
            wrap_width = None
            if available_space.width is not None and available_space.width.scale == Scale.POINTS:
                wrap_width = available_space.width.value
            
            if wrap_width is not None and wrap_width > 0:
                # We need to use ceil here since the text content bounds are computed using ceil
                # If we use floor (or the float value) here, the text may be cut off in some edge cases
                text_node.set_text_wrap_width(ceil(wrap_width))
            
            width = text_node.compute_intrinsic_width()
            height = text_node.compute_intrinsic_height()

            # This could cause an issue:
            # Stretchable is using float width/height
            # However, we're using integer bounds in pictex for skia (to avoid rendering artefacs with float)
            # Keep this in mind if a weird bug appears
            return SizePoints(float(width), float(height))
        
        return measure

    def _create_non_text_node_measure_function(self, node: 'Node') -> Callable:
        """Create generic measure function for non-text leaf nodes.
        
        Args:
            node: The leaf node to measure.
            
        Returns:
            Measure function that uses node's intrinsic size.
        """
        def measure(_node: StretchableNode, _known_size: SizePoints, _available_space: SizeAvailableSpace) -> SizePoints:
            node._clear_bounds()
            width = node.compute_intrinsic_width()
            height = node.compute_intrinsic_height()
            return SizePoints(float(width), float(height))
        
        return measure

    def _link_layout_results(self, pictex_node: 'Node', stretchable_node: StretchableNode) -> None:
        """Link layout results by assigning LayoutResult wrapper to each node.
        
        Uses the public set_layout_result() method to respect encapsulation.
        """

        pictex_node._clear_bounds()
        pictex_node.set_layout_result(LayoutResult(stretchable_node))
        for child in pictex_node.children:
            if child in self._node_map:
                self._link_layout_results(child, self._node_map[child])
