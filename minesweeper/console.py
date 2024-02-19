from enum import Enum
import sys


class ANSIGraphicsMode(Enum):
    End = "\033[0m"
    Underline = "\033[4m"
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    White = "\033[37m"


class ANSIDirection(Enum):
    Up = "\033[{}A"
    Down = "\033[{}B"
    Right = "\033[{}C"
    Left = "\033[{}D"
    Home = "\033[H"


class ANSIClear(Enum):
    CursorDown = "\033[0J"
    CursorUp = "\033[1J"
    EntireScreen = "\033[2J"


class ANSICursor(Enum):
    Invisible = "\033[?25l"
    Visible = "\033[?25h"


def flush_stdout(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        sys.stdout.flush()

    return wrapper


@flush_stdout
def set_cursor_visibility(visible: ANSICursor):
    sys.stdout.write(visible.value)


def underline(text: str):
    return ANSIGraphicsMode.Underline + text + ANSIGraphicsMode.End


def color(text: str, color: ANSIGraphicsMode):
    return color.value + text + ANSIGraphicsMode.End.value


@flush_stdout
def clear():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(ANSIClear.EntireScreen.value)


@flush_stdout
def write(text: str):
    sys.stdout.write(text)


@flush_stdout
def move_cursor_home():
    sys.stdout.write(ANSIDirection.Home.value)
