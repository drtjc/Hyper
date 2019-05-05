import abc
from tictactoe import TicTacToe, Cell_coord, Move
from typing import Tuple, Union, Optional, List


class Strategy(abc.ABC):

    @classmethod
    def validate(cls, d: int, n: int, moves_per_turn: int) -> bool:
        """ Are the supplied game paramters valid for the strategy? """
        return True

    def __init__(self, ttt: TicTacToe) -> None:
        super().__init__()
        self.ttt = ttt

    def reset(self) -> None:
        """ Play resets """
        self.ttt.reset()

    @abc.abstractmethod
    def move(self) -> None: 
        """ Calculate the move to be played """
        moves = self.ttt.moves[-self.ttt.moves_per_turn:]
        self.opponent_moves: Optional[List[Cell_coord]] = [m.Cell for m in moves]

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Strategy:

            validate_found = False
            reset_found = False
            move_found = False
            for B in C.__mro__:
                for attr in B.__dict__:
                    if attr == "validate":
                        validate_found = True                    
                
                    if attr == "reset":
                        reset_found = True                    
                    
                    if attr == "move":
                        move_found = True
                    
                    if validate_found and reset_found and move_found:
                        return True

        return NotImplemented


