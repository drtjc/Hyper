from strategy import Strategy, Cell_coord
from tictactoe import TicTacToe
from random import randrange
from typing import Union, Optional, Tuple


class Random(Strategy):
    
    def move(self) -> None:     
        m = self.ttt.unplayed[randrange(len(self.ttt.unplayed))]
        self.ttt.move(m)
    
