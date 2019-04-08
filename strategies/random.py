import hypercube as hc
from strategy import Strategy
from tictactoe import TicTacToe
from random import randrange
from typing import Union, Optional, List

Cell_coord = hc.Cell_coord


class Random(Strategy):
    
    def __init__(self, ttt: TicTacToe) -> None:
        super().__init__(ttt)
        self.unplayed: List = []

    def reset(self) -> None:
        super().reset()
        self.shape = [self.ttt.n] * self.ttt.d
        self.unplayed = [i for i in range(self.ttt.n ** self.ttt.d)]

    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]: 
        if cell is None or not self.unplayed:
            self.reset()

        m_idx = self.unplayed[randrange(len(self.unplayed))]
        self.unplayed.remove(m_idx)
        m = hc.np.unravel_index(m_idx, self.shape)
        return m

    def undo(self):
        pass
