from dataclasses import dataclass
from enum import Enum
from random import randint
from typing import List

from .cell import Cell, CellState, CellType


@dataclass
class GameConfig:
    level: str
    width: int
    height: int
    mines: int


class GameState(Enum):
    Running = "Running"
    Won = "Won"
    Lost = "Lost"


class GameAction(Enum):
    Open = "Open"
    Flag = "Flag"


_SERROUNDING_OFFSETS = {
    "upper": (-1, 0),
    "right": (0, 1),
    "bottom": (1, 0),
    "left": (0, -1),
    "upper_right": (-1, -1),
    "upper_left": (-1, 1),
    "bottom_right": (1, 1),
    "bottom_left": (1, -1),
}


_MINE_COUNT_TO_TYPE = {
    0: CellType.Empty,
    1: CellType.Number_1,
    2: CellType.Number_2,
    3: CellType.Number_3,
    4: CellType.Number_4,
    5: CellType.Number_5,
    6: CellType.Number_6,
    7: CellType.Number_7,
    8: CellType.Number_8,
}


class GameBoard:
    def __init__(self, config: GameConfig):
        self._config = config
        self._cells = None
        self._action = GameAction.Open
        self._state = GameState.Running
        self._statistics = {"opened": 0, "flagged": 0}

        self._create_board()

    @property
    def config(self):
        return self._config
    
    @property
    def height(self) -> int:
        return self._config.height

    @property
    def width(self) -> int:
        return self._config.width

    @property
    def remaining_mines(self) -> int:
        return self._config.mines - self._statistics["flagged"]

    @property
    def cells(self) -> List[List[Cell]]:
        return self._cells

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def action(self) -> GameAction:
        return self._action

    def _create_board(self):
        self._create_cells()
        self._create_mines()
        self._create_numbers()

    def _create_cells(self):
        self._cells = [
            [Cell(row, col) for col in range(self._config.width)]
            for row in range(self._config.height)
        ]

    def _create_mines(self):
        for _ in range(self._config.mines):
            cell = self._get_random_free_cell()
            cell.type = CellType.Mine

    def _get_random_free_cell(self) -> Cell:
        optional_index = randint(0, self._config.width * self._config.height - 1)
        row, col = int(optional_index / self._config.width), int(optional_index % self._config.width)
        cell = self._cells[row][col]
        while self._is_cell_initialized(row, col):
            optional_index = randint(0, self._config.width + self._config.height)
            row, col = int(optional_index / self._config.width), int(
                optional_index % self._config.width
            )
            cell = self._cells[row][col]

        return cell

    def _create_numbers(self):
        for row in range(self._config.height):
            for col in range(self._config.width):
                if self._is_cell_initialized(row, col):
                    continue

                mines_count = self._count_mines_around_cell(row, col)
                self._cells[row][col].type = _MINE_COUNT_TO_TYPE[mines_count]

    def _is_cell_initialized(self, row: int, col: int) -> bool:
        return self._cells[row][col].type is not CellType.Uninitialized

    def _count_mines_around_cell(self, row: int, col: int) -> int:
        count = 0
        for _, offset in _SERROUNDING_OFFSETS.items():
            _row, _col = row + offset[0], col + offset[1]
            if (
                self._is_cell_in_bound(_row, _col)
                and self._cells[_row][_col].type == CellType.Mine
            ):
                count += 1

        return count

    def _is_cell_in_bound(self, row: int, col: int) -> bool:
        return not (
            row < 0 or row > self._config.height - 1 or col < 0 or col > self._config.width - 1
        )

    def switch_action(self):
        self._action = (
            GameAction.Open if self._action == GameAction.Flag else GameAction.Flag
        )

    def handle_action(self, row: int, col: int):
        match self._action:
            case GameAction.Open:
                self._handle_action_open(row, col)
            case GameAction.Flag:
                self._handle_action_flag(row, col)

    def _handle_action_open(self, row: int, col: int):
        cell = self.cells[row][col]
        if cell.state != CellState.Closed:
            return

        if cell.type == CellType.Mine:
            self._handle_open_mine()
        else:
            self._handle_open_number_or_empty(row, col)

    def _handle_open_mine(self):
        self._set_lost_board()
        self._state = GameState.Lost

    def _set_lost_board(self):
        cells = (cell for row in self._cells for cell in row)
        for cell in cells:
            if cell.state == CellState.Closed:
                cell.state = CellState.Opened

    def _handle_open_number_or_empty(self, row: int, col: int):
        if not self._is_cell_in_bound(row, col):
            return

        cell = self.cells[row][col]

        if cell.state != CellState.Closed:
            return

        if cell.type == CellType.Mine:
            return

        cell.state = CellState.Opened
        self._statistics["opened"] += 1

        if cell.type == CellType.Empty:
            for _, offset in _SERROUNDING_OFFSETS.items():
                _row, _col = row + offset[0], col + offset[1]
                self._handle_open_number_or_empty(_row, _col)

        if self._check_win():
            self._handle_win()

    def _check_win(self) -> bool:
        not_mines = self._config.width * self._config.height - self._config.mines
        return not_mines == self._statistics["opened"]

    def _handle_win(self):
        self._set_won_board()
        self._state = GameState.Won

    def _set_won_board(self):
        cells = (cell for row in self._cells for cell in row)
        for cell in cells:
            if cell.type == CellType.Mine:
                cell.state = CellState.Flagged

    def _handle_action_flag(self, row: int, col: int):
        cell = self.cells[row][col]

        match cell.state:
            case CellState.Closed:
                cell.state = CellState.Flagged
                self._statistics["flagged"] += 1
            case CellState.Flagged:
                cell.state = CellState.Closed
                self._statistics["flagged"] -= 1
