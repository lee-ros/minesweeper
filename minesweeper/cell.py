from enum import Enum, auto


class CellType(Enum):
    Uninitialized = auto()
    Mine = auto()
    Empty = auto()
    Number_1 = auto()
    Number_2 = auto()
    Number_3 = auto()
    Number_4 = auto()
    Number_5 = auto()
    Number_6 = auto()
    Number_7 = auto()
    Number_8 = auto()


class CellState(Enum):
    Opened = auto()
    Closed = auto()
    Flagged = auto()


class Cell:
    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col
        self.type = CellType.Uninitialized
        self.state = CellState.Closed

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col
    
    @property
    def is_initialized(self):
        return self._type != CellType.Uninitialized
