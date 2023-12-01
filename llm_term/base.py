"""
Base classes and types for llm_term
"""

from typing import Any

from rich.console import RenderableType
from rich.padding import Padding


class NoPadding(Padding):
    """
    Empty Renderable
    """

    def __init__(self, renderable: RenderableType, **kwargs: Any) -> None:
        """
        Create an empty Padding
        """
        _ = kwargs
        pad = (0, 0, 0, 0)
        super().__init__(renderable, pad=pad)
