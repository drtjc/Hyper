import abc
from typing import Tuple, Union

Cell_coord = Tuple[int, ...]


class Strategy(abc.ABC):

    #def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
    #    pass
    def __init__(self) -> None:
        self.shared = False
        super().__init__()

    # @property
    # @abc.abstractmethod
    # def shared(self):
    #      """ ## """

    # @shared.setter
    # @abc.abstractmethod
    # def shared(self, val):
    #      """ ## """

    # @property
    # def shared(self):
    #     return self._shared

    # @shared.setter
    # def shared(self, val):
    #     self._shared = val

    @abc.abstractmethod
    def move(self, cell: Union[Cell_coord]) -> Cell_coord:
        """ Calculate the move to be played """

    @abc.abstractmethod
    def undo(self):
        """ Undo last move played """

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Strategy:

            move_found = False
            undo_found = False
            for B in C.__mro__:
                for attr in B.__dict__:
                    if attr == "move":
                        move_found = True
                    
                    if attr == "undo":                        
                        undo_found = True
                    
                    if move_found and undo_found:
                        return True

        return NotImplemented


