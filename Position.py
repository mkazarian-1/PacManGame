from enum import Enum, auto


class Position(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()
    NOT_DEFINED = auto()