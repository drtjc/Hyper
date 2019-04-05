import abc
from tictactoe import TicTacToe
from typing import Tuple, Union, Optional

Cell_coord = Tuple[int, ...]


class Strategy(abc.ABC):

    def __init__(self, ttt: TicTacToe) -> None:
        super().__init__()
        self.ttt = ttt

    @abc.abstractmethod
    def reset(self) -> None:
        """ Play resets """

    @abc.abstractmethod
    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]: 
        """ Calculate the move to be played """

    @abc.abstractmethod
    def undo(self):
        """ Undo last move played """

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Strategy:

            reset_found = False
            move_found = False
            undo_found = False
            for B in C.__mro__:
                for attr in B.__dict__:
                    if attr == "reset":
                        reset_found = True                    
                    
                    if attr == "move":
                        move_found = True
                    
                    if attr == "undo":                        
                        undo_found = True
                    
                    if reset_found and move_found and undo_found:
                        return True

        return NotImplemented


