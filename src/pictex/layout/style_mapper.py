"""Style mapper for converting pictex styles to stretchable styles.

This module provides utilities for mapping pictex Style properties to their
stretchable equivalents, enabling the layout engine to use Taffy for layout computation.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from stretchable.style import (
    Style as StretchableStyle,
    FlexDirection,
    AlignItems,
    JustifyContent,
    Display,
    Position as StretchablePosition,
    AUTO,
    PCT,
)

if TYPE_CHECKING:
    from ..nodes import Node
    from ..models import (
        SizeValue,
        Padding,
        Margin,
        Border,
        Position,
        Inset,
    )


class StyleMapper:
    """Maps pictex Style properties to stretchable Style.
    
    This class handles the conversion between pictex's style system
    and stretchable's CSS-like style properties.
    
    Example:
        >>> from pictex.layout.style_mapper import StyleMapper
        >>> stretchable_style = StyleMapper.create_style(pictex_node)
    """

    # Mapping from pictex HorizontalDistribution to stretchable JustifyContent
    HORIZONTAL_DISTRIBUTION_MAP = {
        'left': JustifyContent.START,
        'center': JustifyContent.CENTER,
        'right': JustifyContent.END,
        'space-between': JustifyContent.SPACE_BETWEEN,
        'space-around': JustifyContent.SPACE_AROUND,
        'space-evenly': JustifyContent.SPACE_EVENLY,
    }

    # Mapping from pictex VerticalDistribution to stretchable JustifyContent
    VERTICAL_DISTRIBUTION_MAP = {
        'top': JustifyContent.START,
        'center': JustifyContent.CENTER,
        'bottom': JustifyContent.END,
        'space-between': JustifyContent.SPACE_BETWEEN,
        'space-around': JustifyContent.SPACE_AROUND,
        'space-evenly': JustifyContent.SPACE_EVENLY,
    }

    # Mapping from pictex VerticalAlignment to stretchable AlignItems
    VERTICAL_ALIGNMENT_MAP = {
        'top': AlignItems.START,
        'center': AlignItems.CENTER,
        'bottom': AlignItems.END,
        'stretch': AlignItems.STRETCH,
    }

    # Mapping from pictex HorizontalAlignment to stretchable AlignItems
    HORIZONTAL_ALIGNMENT_MAP = {
        'left': AlignItems.START,
        'center': AlignItems.CENTER,
        'right': AlignItems.END,
        'stretch': AlignItems.STRETCH,
    }

    @classmethod
    def create_row_style(cls, node: 'Node') -> StretchableStyle:
        """Create stretchable style for a Row node (flex-direction: row)."""
        computed = node.computed_styles
        
        # Map distribution and alignment
        h_dist = computed.horizontal_distribution.get()
        v_align = computed.vertical_alignment.get()
        
        justify_content = cls.HORIZONTAL_DISTRIBUTION_MAP.get(h_dist.value, JustifyContent.START)
        align_items = cls.VERTICAL_ALIGNMENT_MAP.get(v_align.value, AlignItems.START)
        
        return cls._create_base_style(
            node,
            flex_direction=FlexDirection.ROW,
            justify_content=justify_content,
            align_items=align_items,
        )

    @classmethod
    def create_column_style(cls, node: 'Node') -> StretchableStyle:
        """Create stretchable style for a Column node (flex-direction: column)."""
        computed = node.computed_styles
        
        # Map distribution and alignment (inverted for column)
        v_dist = computed.vertical_distribution.get()
        h_align = computed.horizontal_alignment.get()
        
        justify_content = cls.VERTICAL_DISTRIBUTION_MAP.get(v_dist.value, JustifyContent.START)
        align_items = cls.HORIZONTAL_ALIGNMENT_MAP.get(h_align.value, AlignItems.START)
        
        return cls._create_base_style(
            node,
            flex_direction=FlexDirection.COLUMN,
            justify_content=justify_content,
            align_items=align_items,
        )

    @classmethod
    def create_leaf_style(cls, node: 'Node') -> StretchableStyle:
        """Create stretchable style for a leaf node (Text, Image, etc.)."""
        return cls._create_base_style(node)

    @classmethod
    def _create_base_style(
        cls,
        node: 'Node',
        flex_direction: Optional[FlexDirection] = None,
        justify_content: Optional[JustifyContent] = None,
        align_items: Optional[AlignItems] = None,
    ) -> StretchableStyle:
        """Create base stretchable style with common properties."""
        computed = node.computed_styles
        
        # Get spacing values
        padding: 'Padding' = computed.padding.get()
        margin: 'Margin' = computed.margin.get()
        border: 'Border' = computed.border.get()
        gap: float = computed.gap.get()
        
        # Get size values
        width_value = computed.width.get()
        height_value = computed.height.get()
        
        # Build style kwargs
        style_kwargs = {
            'display': Display.FLEX,
            'padding': (padding.top, padding.right, padding.bottom, padding.left),
            'margin': (margin.top, margin.right, margin.bottom, margin.left),
            'border': border.width if border else 0.0,
            'gap': gap,
        }
        
        # Add flex properties if provided
        if flex_direction is not None:
            style_kwargs['flex_direction'] = flex_direction
        if justify_content is not None:
            style_kwargs['justify_content'] = justify_content
        if align_items is not None:
            style_kwargs['align_items'] = align_items
        
        # Map size values
        size = cls._map_size(node, width_value, height_value)
        if size is not None:
            style_kwargs['size'] = size
        
        # Map flex_grow for fill-available
        flex_grow = cls._get_flex_grow(width_value, height_value)
        if flex_grow > 0:
            style_kwargs['flex_grow'] = flex_grow
        
        # Map position and inset
        position_config: 'Position' = computed.position.get()
        if position_config is not None:
            position_type, inset = cls._map_position(position_config)
            if position_type is not None:
                style_kwargs['position'] = position_type
            if inset is not None:
                style_kwargs['inset'] = inset
        
        return StretchableStyle(**style_kwargs)

    @classmethod
    def _map_size(
        cls,
        node: 'Node',
        width: Optional['SizeValue'],
        height: Optional['SizeValue'],
    ) -> Optional[tuple]:
        """Map pictex size values to stretchable size tuple."""
        from stretchable.style import AUTO
        
        w = cls._map_single_size(node, width, 'width') if width else AUTO
        h = cls._map_single_size(node, height, 'height') if height else AUTO
        
        return (w, h)

    @classmethod
    def _map_single_size(cls, node: 'Node', size_value: Optional['SizeValue'], dimension: str):
        """Map a single pictex SizeValue to stretchable length.
        
        Args:
            node: The node being styled (to access background image if needed)
            size_value: The SizeValue to map
            dimension: Either 'width' or 'height'
        """
        from stretchable.style import AUTO, PCT
        
        if size_value is None:
            return AUTO
        
        mode = size_value.mode
        value = size_value.value
        
        if mode == 'auto' or mode == 'fit-content':
            return AUTO
        elif mode == 'absolute':
            return value
        elif mode == 'percent':
            return value * PCT
        elif mode == 'fill-available':
            # Will be handled by flex_grow
            return AUTO
        elif mode == 'fit-background-image':
            # Get background image and return its dimensions
            bg_image_info = node.computed_styles.background_image.get()
            if bg_image_info:
                bg_image = bg_image_info.get_skia_image()
                if bg_image:
                    if dimension == 'width':
                        return float(bg_image.width())
                    else:  # height
                        return float(bg_image.height())
            return AUTO
        else:
            return AUTO

    @classmethod
    def _get_flex_grow(
        cls,
        width: Optional['SizeValue'],
        height: Optional['SizeValue'],
    ) -> float:
        """Determine flex_grow based on fill-available sizing."""
        if width and width.mode == 'fill-available':
            return 1.0
        if height and height.mode == 'fill-available':
            return 1.0
        return 0.0

    @classmethod
    def _map_position(cls, position: 'Position') -> tuple:
        """Map pictex Position to stretchable position and inset.
        
        Args:
            position: The pictex Position configuration.
            
        Returns:
            Tuple of (stretchable_position, inset_tuple)
        """
        from ..models import PositionType
        
        # Map position type
        position_type = None
        if position.type == PositionType.ABSOLUTE:
            position_type = StretchablePosition.ABSOLUTE
        elif position.type == PositionType.RELATIVE:
            position_type = StretchablePosition.RELATIVE
        # STATIC is the default, no need to set
        
        # Map inset values
        inset = position.inset
        if inset is None:
            return position_type, None
        
        top = cls._map_inset_value(inset.top)
        right = cls._map_inset_value(inset.right)
        bottom = cls._map_inset_value(inset.bottom)
        left = cls._map_inset_value(inset.left)
        
        # Only return inset if at least one value is set
        if all(v is AUTO for v in [top, right, bottom, left]):
            return position_type, None
        
        return position_type, (top, right, bottom, left)

    @classmethod
    def _map_inset_value(cls, value) -> any:
        """Map a single pictex inset value to stretchable length.
        
        Args:
            value: Inset value - None, pixels (int/float), or percentage string.
            
        Returns:
            Stretchable length value (AUTO, pixels, or percentage).
        """
        if value is None:
            return AUTO
        
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, str) and value.endswith('%'):
            pct = float(value.rstrip('%'))
            return pct * PCT
        
        return AUTO
