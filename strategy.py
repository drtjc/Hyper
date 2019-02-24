import abc
from typing import Tuple, Dict, Type

Cell_coord = Tuple[int, ...]

class Strategy(abc.ABC):

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        self.d = d
        self.n = n
        self.moves_per_turn = moves_per_turn
        self.drop = drop

    @abc.abstractmethod
    def move(self, cell: Cell_coord) -> Cell_coord:
        """ Calculate the move to be played """

    @abc.abstractmethod
    def undo(self, cell: Cell_coord) -> Cell_coord:
        """ Undo last move played """

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Strategy:
            pass
        return NotImplemented

class Strategies(Dict[str, Type[Strategy]]):

    def __init__(self) -> None:
        super()

    def register(self, s: Type[Strategy]) -> None:
        self[s.__name__] = s 


strategies = Strategies()


def dec_strategy(s):
    strategies.register(s)
    return s

