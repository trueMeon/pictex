from typing import Tuple, Callable
from .node import Node
from ..painters import Painter, BackgroundPainter, BorderPainter
from ..models import Style, Constraints, SizeValueMode
import skia

class ContainerNode(Node):

    def __init__(self, style: Style, children: list[Node]) -> None:
        super().__init__(style)
        self._set_children(children)
        self.clear()

    def _calculate_children_relative_positions(self, children: list[Node], get_child_bounds: Callable[[Node], skia.Rect]) -> list[Tuple[float, float]]:
        raise NotImplemented
    
    def _resize_children_if_needed(self, children: list[Node]):
        raise NotImplemented

    def _compute_paint_bounds(self) -> skia.Rect:
        paint_bounds = skia.Rect.MakeEmpty()

        children = self._get_positionable_children()
        positions = self._calculate_children_relative_positions(children, lambda node: node.paint_bounds)
        for i, child in enumerate(children):
            position = positions[i]
            child_bounds_shifted = child.paint_bounds.makeOffset(position[0], position[1])
            paint_bounds.join(child_bounds_shifted)

        paint_bounds.join(self._compute_shadow_bounds(self.border_bounds, self.computed_styles.box_shadows.get()))
        paint_bounds.join(self.margin_bounds)
        return paint_bounds

    def _get_painters(self) -> list[Painter]:
        return [
            BackgroundPainter(self.computed_styles, self.border_bounds, self._render_props.is_svg),
            BorderPainter(self.computed_styles, self.border_bounds),
        ]

    def _setup_absolute_position(self, x: float = 0, y: float = 0) -> None:
        super()._setup_absolute_position(x, y)
        x, y = self._absolute_position
        positionable_children = self._get_positionable_children()
        self._resize_children_if_needed(positionable_children)
        positions = self._calculate_children_relative_positions(positionable_children, lambda node: node.margin_bounds)
        for i, child in enumerate(positionable_children):
            position = positions[i]
            child._setup_absolute_position(x + position[0], y + position[1])

        non_positionable_children = self._get_non_positionable_children()
        for child in non_positionable_children:
            child._setup_absolute_position()

    def _compute_node_constraints(self, parent_constraints: Constraints) -> Constraints:
        """
        Compute constraints for this container based on parent constraints and own sizing.
        """
        width_style = self.computed_styles.width.get()
        height_style = self.computed_styles.height.get()
        
        max_width = None
        max_height = None
        
        # Determine width constraint
        if width_style:
            if width_style.mode == SizeValueMode.ABSOLUTE:
                max_width = float(width_style.value)
            elif width_style.mode == SizeValueMode.PERCENT and parent_constraints.has_width_constraint():
                max_width = parent_constraints.get_effective_width() * (width_style.value / 100.0)
            # For other modes like fill-available, fit-content, we inherit parent constraint
            elif parent_constraints.has_width_constraint():
                max_width = parent_constraints.get_effective_width()
        else:
            # No explicit width, inherit parent constraint
            if parent_constraints.has_width_constraint():
                max_width = parent_constraints.get_effective_width()
        
        # Determine height constraint (similar logic)
        if height_style:
            if height_style.mode == SizeValueMode.ABSOLUTE:
                max_height = float(height_style.value)
            elif height_style.mode == SizeValueMode.PERCENT and parent_constraints.has_height_constraint():
                max_height = parent_constraints.get_effective_height() * (height_style.value / 100.0)
            elif parent_constraints.has_height_constraint():
                max_height = parent_constraints.get_effective_height()
        else:
            if parent_constraints.has_height_constraint():
                max_height = parent_constraints.get_effective_height()
        
        return Constraints(max_width=max_width, max_height=max_height)

    def _compute_child_constraints(self, own_constraints: Constraints) -> Constraints:
        """
        Compute constraints to pass to children. Default implementation 
        subtracts padding and border from own constraints.
        """
        if not own_constraints.has_width_constraint() and not own_constraints.has_height_constraint():
            return Constraints.none()
        
        padding = self.computed_styles.padding.get()
        border = self.computed_styles.border.get()
        border_width = border.width if border else 0
        
        horizontal_spacing = padding.left + padding.right + (border_width * 2)
        vertical_spacing = padding.top + padding.bottom + (border_width * 2)
        
        child_max_width = None
        child_max_height = None
        
        if own_constraints.has_width_constraint():
            child_max_width = max(0, own_constraints.get_effective_width() - horizontal_spacing)
        
        if own_constraints.has_height_constraint():
            child_max_height = max(0, own_constraints.get_effective_height() - vertical_spacing)
        
        return Constraints(max_width=child_max_width, max_height=child_max_height)
