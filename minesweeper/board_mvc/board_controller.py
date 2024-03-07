from typing import Optional

from .board_model import BoardModel
from .board_view import show_board_page
from ..user_action import UserAction


# default board config
_WIDTH = 10
_HEIGHT = 10
_MINES = 10


class BoardController:
    """Class to control and show the Minesweeper game board"""

    def __init__(self):
        self._board = BoardModel(_WIDTH, _HEIGHT, _MINES)

        self._key_action_map = {
            b"w": UserAction(
                key_visual="w",
                operation="move",
                callback=lambda: self._board.offset_row(-1),
            ),
            b"s": UserAction(
                key_visual="s",
                operation="move",
                callback=lambda: self._board.offset_row(1),
            ),
            b"d": UserAction(
                key_visual="d",
                operation="move",
                callback=lambda: self._board.offset_col(1),
            ),
            b"a": UserAction(
                key_visual="a",
                operation="move",
                callback=lambda: self._board.offset_col(-1),
            ),
            b"c": UserAction(
                key_visual="c",
                operation="change action",
                callback=lambda: self._board.rotate_action(),  # pylint: disable=unnecessary-lambda
            ),
            b"n": UserAction(
                key_visual="n",
                operation="new board",
                callback=self._create_new_board_with_same_config,
            ),
            b"\x20": UserAction(
                key_visual="space",
                operation="press",
                callback=lambda: self._board.press(),  # pylint: disable=unnecessary-lambda
            ),
        }

    @property
    def help_message(self) -> str:
        """Returns the help message"""
        return UserAction.generate_help_message(self._key_action_map.values())

    def run(self, char: Optional[bytes] = None) -> bool:
        """Runs the current controller"""
        handled = False
        action = self._key_action_map.get(char, None)
        if action:
            action.callback()
            handled = True

        show_board_page(self._board)

        return handled

    def create_new_board(self, width: int, height: int, mines: int):
        """Create a new board from a given configuration"""
        self._board = BoardModel(width, height, mines)

    def _create_new_board_with_same_config(self):
        width, height = self._board.dimensions
        mines = self._board.mines
        self.create_new_board(width, height, mines)
