from .. import console_utils


def show_game_help_bar(help_message: str):
    console_utils.move_cursor_to(console_utils.ANSIDirection.HOME)
    console_utils.clear(console_utils.ANSIClear.CURSOR_DOWN)
    console_utils.write_line(help_message)
