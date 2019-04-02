import hypercube as hc
from strategy import Strategy
from tictactoe import TicTacToe as ttt
from typing import Union

Cell_coord = hc.Cell_coord


class Random(Strategy):
    
    def __init__(self, shared: bool, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        super().__init__()
        self.shared = shared



    def reset(self) -> None:
        pass

    def move(self, cell: Union[Cell_coord]) -> Cell_coord:
        return (2,)

    def undo(self):
        pass
