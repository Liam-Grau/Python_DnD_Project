from enum import Enum


class Color(Enum):
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    BLACK = '\033[30m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    PURPLE = '\033[35m'
    ORANGE = '\033[38;5;208m'
    RESET = '\033[0m'


def colored_str(text, color: Color = Color.WHITE):
    return f"{color.value}{text}{Color.RESET.value}"


def print_colored(text, color: Color = Color.WHITE):
    print(f"{color.value}{text}{Color.RESET.value}")
