from typing import Optional, Protocol


class Controller(Protocol):  # pylint: disable=too-few-public-methods
    """MCV Controller protocol"""

    def run(self, char: Optional[bytes]) -> bool:
        """Runs the controller"""
