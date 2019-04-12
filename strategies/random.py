from strategy import Strategy, Cell_coord
from tictactoe import TicTacToe
from random import randrange
from typing import Union, Optional, Tuple


class Random(Strategy):
    
    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]:     
        m = self.ttt.unplayed[randrange(len(self.ttt.unplayed))]
        self.ttt.move(m)
        return m
