import random

from enum import Enum
from typing import Generator, List, Tuple, TypeVar

from .cell import Cell, CellState, CellType


T = TypeVar("T")
Grid = List[List[T]]


class BoardState(Enum):
    """Possible states of the board"""

    PLAYING = "Playing"
    WON = "Won"
    LOST = "Lost"


class BoardAction(Enum):
    """Supported game actions"""

    OPEN = "Open"
    FLAG = "Flag"


class BoardModel:
    def __init__(self, width, height, mines):
        self._dimensions = (width, height)
        self._mines = mines

        self._grid = None
        self._initialize_grid()

        self._active_action = None
        self._action_generator = self._create_action_generator()
        self.rotate_action()

        self._active_row = 0
        self._active_col = 0
        self._state = BoardState.PLAYING
        self._opened_count = 0
        self._flagged_count = 0
        self._mine_opened = False

    @property
    def dimensions(self) -> Tuple[int, int]:
        """Returns the dimensions of the board (width, height)"""
        return self._dimensions

    @property
    def mines(self) -> int:
        """Returns the number of mines in the board"""
        return self._mines

    @property
    def state(self) -> BoardState:
        """Returns the current board state"""
        return self._state

    @property
    def remaining_mines(self) -> int:
        """Returns the number of mines left to be found on the board"""
        return self._mines - self._flagged_count

    @property
    def grid(self) -> Grid:
        """Returns the grid of cells"""
        return self._grid

    @property
    def active_row(self) -> int:
        """Returns the active row"""
        return self._active_row

    @property
    def active_col(self) -> int:
        """Returns the active col"""
        return self._active_col

    @property
    def active_action(self) -> BoardAction:
        """Returns the active action"""
        return self._active_action

    def offset_row(self, offset: int):
        """Adds the `offset` to the active column"""
        self._active_row = (self._active_row + offset) % self._dimensions[1]

    def offset_col(self, offset: int):
        """Adds the `offset` to the active column"""
        self._active_col = (self._active_col + offset) % self._dimensions[0]

    def rotate_action(self):
        """Rotates through the board actions"""
        self._active_action = next(self._action_generator)

    def press(self):
        """Acts on the active action"""
        match self._active_action:
            case BoardAction.OPEN:
                self.open(self._active_row, self._active_col)
            case BoardAction.FLAG:
                self.flag(self._active_row, self._active_col)

    def _initialize_grid(self):
        width, height = self._dimensions
        self._grid = [[Cell(row, col) for col in range(width)] for row in range(height)]

        for cell in self._get_random_cells_for_mines():
            cell.type = CellType.MINE

        for row in range(height):
            for col in range(width):
                cell = self._grid[row][col]
                if cell.is_initialized:
                    continue

                mine_count = self._count_mines_around_cell(cell)
                cell.type = CellType(mine_count)

    def _get_random_cells_for_mines(self) -> List[Cell]:
        width, height = self._dimensions
        free_cells = filter(
            lambda cell: not cell.is_initialized,
            (self._grid[row][col] for row in range(height) for col in range(width)),
        )
        return random.sample([*free_cells], self.mines)

    def _count_mines_around_cell(self, cell: Cell) -> int:
        width, height = self._dimensions
        count = 0
        for row in range(max(0, cell.row - 1), min(height, cell.row + 2)):
            for col in range(max(0, cell.col - 1), min(width, cell.col + 2)):
                if self._grid[row][col].type == CellType.MINE:
                    count += 1
        return count

    def open(self, row: int, col: int):
        """Opens the cell at (row, col)"""
        cell = self._grid[row][col]
        self._open_and_expand_selection(cell)
        self._update_board_state()

    def _open_and_expand_selection(self, cell: Cell):
        """Opens the selected cell and expand the opened area if relevant
        Returns the number of opened cells
        """
        if cell is None or cell.state != CellState.CLOSE:
            return

        self._open_cell(cell)

        if cell.type != CellType.EMPTY:
            return

        width, height = self._dimensions
        for row in range(max(0, cell.row - 1), min(height, cell.row + 2)):
            for col in range(max(0, cell.col - 1), min(width, cell.col + 2)):
                _cell = self._grid[row][col]
                self._open_and_expand_selection(_cell)

    def _open_cell(self, cell):
        cell.open()

        if cell.type == CellType.MINE:
            self._mine_opened = True
        else:
            self._opened_count += 1

    def flag(self, row: int, col: int):
        """Toggles the flag on the cell at (row, col)"""
        cell = self._grid[row][col]
        prev_state = cell.state
        cell.toggle_flag()
        curr_state = cell.state

        if prev_state == CellState.CLOSE and curr_state == CellState.FLAG:
            self._flagged_count += 1

        elif prev_state == CellState.FLAG:
            self._flagged_count -= 1

    def _update_board_state(self):
        width, height = self._dimensions
        if self._mine_opened:
            self._state = BoardState.LOST
        elif self._opened_count == width * height - self._mines:
            self._state = BoardState.WON

    def _create_action_generator(self) -> Generator[None, None, BoardAction]:
        actions = [*BoardAction]
        actions_count = len(actions)
        i = 0
        while True:
            yield actions[i]
            i = (i + 1) % actions_count
