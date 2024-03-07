from .. import assets, console_utils
from .board_model import BoardAction, BoardModel, BoardState
from .cell import Cell, CellState, CellType


_CELL_VISUALS = {
    CellState.OPEN: {
        CellType.UNINITIALIZED: None,
        CellType.MINE: "⎈",
        CellType.EMPTY: "-",
        CellType.NUMBER_1: "1",
        CellType.NUMBER_2: "2",
        CellType.NUMBER_3: "3",
        CellType.NUMBER_4: "4",
        CellType.NUMBER_5: "5",
        CellType.NUMBER_6: "6",
        CellType.NUMBER_7: "7",
        CellType.NUMBER_8: "8",
    },
    CellState.CLOSE: "⎕",
    CellState.FLAG: "⍟",
    CellState.NOT_SURE: "?",
}

_BOARD_ACTION_TO_COLOR = {
    BoardAction.OPEN: console_utils.ANSIGraphicsMode.GREEN,
    BoardAction.FLAG: console_utils.ANSIGraphicsMode.RED,
}


def show_board_page(board: BoardModel):
    """Shows the board and it's stats"""
    match board.state:
        case BoardState.PLAYING:
            _print_grid(board)
        case BoardState.WON:
            console_utils.write_line(assets.WON_MESSAGE)
        case BoardState.LOST:
            console_utils.write_line(assets.LOST_MESSAGE)

    _print_status(board.state, board.active_action, board.remaining_mines)


def _print_grid(board: BoardModel):
    width, height = board.dimensions

    spacer = "--" * (width + 1) + "\n"
    console_utils.write(spacer, flush=False)
    for row in range(height):
        line = "|"
        for col in range(width):
            cell = board.grid[row][col]
            is_active = row == board.active_row and col == board.active_col
            cell_visual = _generate_cell_visual(cell, board.active_action, is_active)
            line += f"{cell_visual} "
        line += "|"
        console_utils.write_line(line, flush=False)
    console_utils.write(spacer)


def _generate_cell_visual(cell: Cell, action: BoardAction, is_active_cell: bool):
    visual = _CELL_VISUALS[cell.state]
    if isinstance(visual, dict):
        visual = visual[cell.type]

    if is_active_cell:
        color = _BOARD_ACTION_TO_COLOR[action]
        visual = console_utils.apply_graphic(visual, color)
        # visual = console_utils.underline(visual)

    return visual


def _print_status(state: BoardState, action: BoardAction, remaining_mines: int):
    console_utils.write_line(
        ", ".join(
            [
                f"State: {state.value}",
                f"Action: {action.value}",
                f"Mines: {remaining_mines}",
                # f"Time: {self._stopwatch.time_format}"
            ]
        )
    )
