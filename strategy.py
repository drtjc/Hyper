import abc
from typing import Tuple, Dict, Type


from inspect import signature, isfunction, _empty


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
    def undo(self):
        """ Undo last move played """

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Strategy:

            move_found = False
            undo_found = False
            for B in C.__mro__:
                for attr in B.__dict__:
                    
                    if attr in ["move", "undo", "dd"]: 
                        print(attr)
                        try:
                            sig = signature(B.__dict__[attr])
                            params = sig.parameters
                            ret = sig.return_annotation
                        except:
                            continue

                        if attr == "move":
                            if len(params) == 2 and ret is not _empty and ret is not None:
                                move_found = True
                    
                        if attr == "undo":                        
                            if len(params) == 1 and (ret is _empty or ret is None):
                                undo_found = True
                    
                if move_found and undo_found:
                    return True

        return NotImplemented


strategies: Dict[str, Type[Strategy]] = {}


