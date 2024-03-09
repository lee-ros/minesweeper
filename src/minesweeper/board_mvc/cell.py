from enum import Enum, auto
from typing import Generator


class CellType(Enum):
    """Possible cell types"""

    UNINITIALIZED = -2
    MINE = -1
    EMPTY = 0
    NUMBER_1 = 1
    NUMBER_2 = 2
    NUMBER_3 = 3
    NUMBER_4 = 4
    NUMBER_5 = 5
    NUMBER_6 = 6
    NUMBER_7 = 7
    NUMBER_8 = 8


class CellState(Enum):
    """Possible cell states"""

    OPEN = auto()
    CLOSE = auto()
    FLAG = auto()
    NOT_SURE = auto()


class Cell:
    """A cell for minesweeper board"""

    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col
        self._state = CellState.CLOSE
        self.type = CellType.UNINITIALIZED

        self._marks_generator = self._create_marks_generator()

    @property
    def row(self) -> int:
        """Returns the row that the cell is placed at relative to the `parent_table`"""
        return self._row

    @property
    def col(self) -> int:
        """Returns the column that the cell is placed at relative to the `parent_table`"""
        return self._col

    @property
    def state(self) -> CellState:
        """Returns the state of the cell"""
        return self._state

    @property
    def is_initialized(self) -> bool:
        """Returns True if cell is initialized else False"""
        return self.type != CellType.UNINITIALIZED

    def open(self):
        """Sets the state of the cell to opened if cell was closed"""
        if self._state == CellState.CLOSE:
            self._state = CellState.OPEN

    def toggle_flag(self):
        """Toggles the state of the cell to flag"""
        if self._state == CellState.OPEN:
            return
        self._state = next(self._marks_generator)

    def _create_marks_generator(self) -> Generator[None, None, CellState]:
        marks = [CellState.FLAG, CellState.NOT_SURE, CellState.CLOSE]
        marks_count = len(marks)
        i = 0
        while True:
            yield marks[i]
            i = (i + 1) % marks_count
