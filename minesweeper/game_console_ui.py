import msvcrt
import atexit
import time

from . import console
from .cell import CellType, CellState
from .game_board import GameAction, GameBoard, GameConfig, GameState
from .stopwatch import Stopwatch


CELL_TYPE_TO_VISUALS = {
    CellType.Uninitialized: None,
    CellType.Mine: "⎈",
    CellType.Empty: "-",
    CellType.Number_1: "1",
    CellType.Number_2: "2",
    CellType.Number_3: "3",
    CellType.Number_4: "4",
    CellType.Number_5: "5",
    CellType.Number_6: "6",
    CellType.Number_7: "7",
    CellType.Number_8: "8",
}


CELL_STATE_TO_VISUALS = {
    CellState.Opened: None,
    CellState.Closed: "⎕",
    CellState.Flagged: "⍟",
}


GAME_ACTION_TO_COLOR = {
    GameAction.Open: console.ANSIGraphicsMode.Green,
    GameAction.Flag: console.ANSIGraphicsMode.Red,
}

help_message = "(w/a/s/d) - move , (space) - press, (c) - change action, (n) - new board ,(Esc) - quit\n"

lost_message = """

░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓████████▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░   ░▒▓█▓▒░
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░
   ░▒▓█▓▒░    ░▒▓██████▓▒░ ░▒▓██████▓▒░       ░▒▓████████▓▒░▒▓██████▓▒░░▒▓███████▓▒░   ░▒▓█▓▒░▒▓██▓▒░▒▓██▓▒░▒▓██▓▒░

"""

won_message = """

░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
   ░▒▓█▓▒░    ░▒▓██████▓▒░ ░▒▓██████▓▒░        ░▒▓█████████████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░

"""


default_configs = [
    GameConfig(level="easy", width=10, height=10, mines=10),
    GameConfig(level="medium", width=15, height=10, mines=40),
    GameConfig(level="hard", width=25, height=25, mines=99),
]


class GameConsoleUI:
    def __init__(self):
        self._board = None
        self._config = default_configs[0]
        self._selected_row = 0
        self._selected_col = 0
        self._stopwatch = Stopwatch()

        

    def run(self):
        self._create_board()
        console.set_cursor_visibility(console.ANSICursor.Invisible)
        console.clear()
        
        while True:
            self._print_board()
            self._handle_input()
            
            time.sleep(0.005)

    def _print_board(self):
        console.move_cursor_home()
        console.write(console.ANSIClear.CursorDown.value)

        self._print_helper_message()

        match self._board.state:
            case GameState.Running:
                self._print_game_board()

            case GameState.Won:
                self._stopwatch.stop()
                console.write(won_message)

            case GameState.Lost:
                self._stopwatch.stop()
                console.write(lost_message)

        self._print_status_bar()

    def _print_helper_message(self):
        console.write(help_message)

    def _print_game_board(self):
        spacer = "--" * (self._board.width + 1) + "\n"
        console.write(spacer)
        for row in range(self._board.height):
            line = "|"
            for col in range(self._board.width):
                cell_visual = self._generate_cell_visual(row, col)
                line += f"{cell_visual} "
            line += "|\n"
            console.write(line)
        console.write(spacer)

    def _print_status_bar(self):
        console.write(
            ", ".join([
                f"State: {self._board.state.value}",
                f"Action: {self._board.action.value}",
                f"Mines: {self._board.remaining_mines}",
                f"Time: {self._stopwatch.time_format}\n"
            ])
        )

    def _generate_cell_visual(self, row: int, col: int):
        cell_visual = self._get_cell_visual(row, col)
        if row != self._selected_row or col != self._selected_col:
            return cell_visual

        color = GAME_ACTION_TO_COLOR[self._board.action]
        cell_visual = console.color(cell_visual, color)
        if cell_visual == CELL_TYPE_TO_VISUALS[CellType.Empty]:
            cell_visual = console.underline(cell_visual)

        return cell_visual

    def _get_cell_visual(self, row: int, col: int):
        cell = self._board.cells[row][col]
        return (
            CELL_STATE_TO_VISUALS[cell.state]
            if cell.state is not CellState.Opened
            else CELL_TYPE_TO_VISUALS[cell.type]
        )

    def _handle_input(self):
        if not msvcrt.kbhit():
            return 
        
        input = msvcrt.getch()
        self._handle_basic_input(input)
        if self._board.state == GameState.Running:
            self._handle_game_input(input)

    def _handle_basic_input(self, input: bytes):
        match input:
            case b"n":
                self._create_board()
            case b"\x1b":  # Esc
                console.set_cursor_visibility(console.ANSICursor.Visible)
                self._stopwatch.stop()
                exit()

    def _create_board(self):
        self._stopwatch.run()
        self._board = GameBoard(self._config)

    def _handle_game_input(self, input: bytes):
        match input:
            case b"w":
                self._move_selection_by(row=-1),
            case b"s":
                self._move_selection_by(row=+1),
            case b"a":
                self._move_selection_by(col=-1),
            case b"d":
                self._move_selection_by(col=+1),
            case b"c":
                self._board.switch_action()
            case b'1' | b'2' | b'3':
                self._config = default_configs[int(input) - 1]
                self._create_board()
            case b"\x20":  # space
                self._board.handle_action(self._selected_row, self._selected_col),
            

    def _move_selection_by(self, *, row=0, col=0):
        self._selected_row = (self._selected_row + row) % self._board.config.height
        self._selected_col = (self._selected_col + col) % self._board.config.width
