import hypercube as hc
from strategy import Strategy
from tictactoe import TicTacToe
from random import randrange
from typing import Union, Optional, List

Cell_coord = hc.Cell_coord


class Random(Strategy):
    
    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]:     
        m = self.ttt.unplayed[randrange(len(self.ttt.unplayed))]
        self.ttt.move(m)
        return m
