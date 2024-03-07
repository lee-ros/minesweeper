from enum import Enum
import sys


class ANSIGraphicsMode(Enum):
    END = "\033[0m"
    UNDERLINE = "\033[4m"
    BOLD = "\033[1m"
    ITALIC = "\033[2m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


class ANSIDirection(Enum):
    UP = "\033[{}A"
    DOWN = "\033[{}B"
    RIGHT = "\033[{}C"
    LEFT = "\033[{}D"
    HOME = "\033[H"


class ANSIClear(Enum):
    CURSOR_DOWN = "\033[0J"
    CURSOR_UP = "\033[1J"
    ENTIRE_SCREEN = "\033[2J"
    END_OF_LINE = "\033[0K"
    START_OF_LINE = "\033[1K"
    WHOLE_LINE = "\033[2K"


class ANSICursor(Enum):
    INVISIBLE = "\033[?25l"
    VISIBLE = "\033[?25h"


def write(text: str, flush=True):
    sys.stdout.write(text)

    if flush:
        sys.stdout.flush()


def set_cursor_visibility(visible: bool):
    visibility_type = ANSICursor.VISIBLE if visible else ANSICursor.INVISIBLE
    write(visibility_type.value)


def underline(text: str):
    return ANSIGraphicsMode.UNDERLINE.value + text + ANSIGraphicsMode.END.value


def apply_graphic(text: str, graphic: ANSIGraphicsMode):
    return graphic.value + text + ANSIGraphicsMode.END.value


def clear(direction: ANSIClear):
    sys.stdout.reconfigure(encoding="utf-8")
    write(direction.value)


def write_line(text: str, flush=True):
    write(text + "\n", flush)


def move_cursor_to(direction: ANSIDirection):
    write(direction.value)
