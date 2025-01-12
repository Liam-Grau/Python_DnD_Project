from enum import Enum


class Color(Enum):
    RED = '\033[31m'
    LIGHT_RED = '\033[1;31m'
    DARK_GREEN = '\033[38;5;22m'
    GREEN = '\033[32m'
    LIGHT_GREEN = '\033[92m'
    YELLOW = '\033[33m'
    DARK_BLUE = '\033[38;5;18m'
    BLUE = '\033[34m'
    LIGHT_BLUE = '\033[94m'
    BLACK = '\033[30m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    PURPLE = '\033[35m'
    ORANGE = '\033[38;5;208m'
    RESET = '\033[0m'

class BackgroundColor(Enum):
    RED = '\033[41m'
    LIGHT_RED = '\033[101m'
    DARK_GREEN = '\033[48;5;22m'
    GREEN = '\033[42m'
    LIGHT_GREEN = '\033[102m'
    YELLOW = '\033[43m'
    DARK_BLUE = '\033[48;5;18m'
    BLUE = '\033[44m'
    LIGHT_BLUE = '\033[104m'
    BLACK = '\033[40m'
    WHITE = '\033[107m'
    GRAY = '\033[100m'
    PURPLE = '\033[45m'
    ORANGE = '\033[48;5;208m'


def b_color(b_color: BackgroundColor = BackgroundColor.BLACK):
    return f"{b_color.value}"

def colored_str(text, color: Color = Color.WHITE):
    return f"{color.value}{text}{Color.RESET.value}"


def print_colored(text, color: Color = Color.WHITE, b_color: BackgroundColor = BackgroundColor.BLACK):
    print(f"{color.value}{b_color.value}{text}{Color.RESET.value}")
