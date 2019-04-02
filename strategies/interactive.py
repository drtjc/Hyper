import hypercube as hc
from strategy import Strategy
from tictactoe import TicTacToe as ttt
from typing import Union

Cell_coord = hc.Cell_coord


class Interactive(Strategy):
    
    def __init__(self, board: ttt) -> None:
        super().__init__(board)

    def reset(self) -> None:
        pass

    def move(self, cell: Union[Cell_coord]) -> Cell_coord:
        res = input('Enter move: ')

        # check for invalid/repeated move
        return res

    def undo(self):
        pass
