"""ImageNode - renders background images with intrinsic sizing.

This node knows how to calculate its intrinsic size from its background image,
which is essential for stretchable layout to properly size images.
"""
import skia
from .container_node import ContainerNode
from ..models import Style
from ..utils import clone_skia_rect


class ImageNode(ContainerNode):
    """Node that displays an image as background with intrinsic sizing support."""

    def __init__(self, style: Style) -> None:
        super().__init__(style, [])

    def compute_intrinsic_width(self) -> float:
        """Get intrinsic width from background image."""
        image = self._get_background_image()
        if image:
            return float(image.width())
        return 0.0
    
    def compute_intrinsic_height(self) -> float:
        """Get intrinsic height from background image."""
        image = self._get_background_image()
        if image:
            return float(image.height())
        return 0.0
    
    def _get_background_image(self) -> 'skia.Image | None':
        """Get the skia image from background_image style."""
        bg_image_info = self.computed_styles.background_image.get()
        if not bg_image_info:
            return None
        return bg_image_info.get_skia_image()
