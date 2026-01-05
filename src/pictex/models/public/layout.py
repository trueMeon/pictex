from dataclasses import dataclass
from enum import Enum

@dataclass
class Margin:
    top: float = 0
    right: float = 0
    bottom: float = 0
    left: float = 0

@dataclass
class Padding:
    top: float = 0
    right: float = 0
    bottom: float = 0
    left: float = 0

class JustifyContent(str, Enum):
    """Main-axis distribution for flex containers (CSS justify-content)."""
    START = "start"
    CENTER = "center"
    END = "end"
    SPACE_BETWEEN = "space-between"
    SPACE_AROUND = "space-around"
    SPACE_EVENLY = "space-evenly"

class AlignItems(str, Enum):
    """Cross-axis alignment for flex containers (CSS align-items)."""
    START = "start"
    CENTER = "center"
    END = "end"
    STRETCH = "stretch"

class AlignSelf(str, Enum):
    """Self-alignment override for flex items (CSS align-self)."""
    AUTO = "auto"
    START = "start"
    CENTER = "center"
    END = "end"
    STRETCH = "stretch"

class FlexWrap(str, Enum):
    """Flex wrapping behavior (CSS flex-wrap)."""
    NOWRAP = "nowrap"
    WRAP = "wrap"
    WRAP_REVERSE = "wrap-reverse"
