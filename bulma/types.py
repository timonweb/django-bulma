from enum import Enum
from typing import NewType


class Size(Enum):
    SMALL = "small"
    NORMAL = "normal"
    MEDIUM = "medium"
    LARGE = "large"


InputSizesStr = NewType("InputSizes", Size)
