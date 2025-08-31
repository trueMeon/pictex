from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Constraints:
    """
    Represents sizing constraints for a node.
    
    These constraints define the maximum available space for a node,
    which is used to determine how content should be laid out
    (e.g., whether text should wrap).
    """
    max_width: Optional[float] = None
    max_height: Optional[float] = None
    
    def has_width_constraint(self) -> bool:
        """Returns True if there is a width constraint."""
        return self.max_width is not None
    
    def has_height_constraint(self) -> bool:
        """Returns True if there is a height constraint."""
        return self.max_height is not None
    
    def get_effective_width(self) -> Optional[float]:
        """Returns the effective width constraint, or None if unconstrained."""
        return self.max_width
    
    def get_effective_height(self) -> Optional[float]:
        """Returns the effective height constraint, or None if unconstrained."""
        return self.max_height
    
    @classmethod
    def none(cls) -> 'Constraints':
        """Returns unconstrained constraints."""
        return cls()
    
    @classmethod
    def fixed_width(cls, width: float) -> 'Constraints':
        """Returns constraints with a fixed width."""
        return cls(max_width=width)
    
    @classmethod
    def fixed_height(cls, height: float) -> 'Constraints':
        """Returns constraints with a fixed height."""
        return cls(max_height=height)
    
    @classmethod
    def fixed(cls, width: float, height: float) -> 'Constraints':
        """Returns constraints with fixed width and height."""
        return cls(max_width=width, max_height=height)