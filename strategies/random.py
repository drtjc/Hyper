import hypercube as hc
from strategy import Strategy
from tictactoe import TicTacToe
from typing import Union, Optional

Cell_coord = hc.Cell_coord


class Random(Strategy):
    
    def __init__(self, ttt: TicTacToe) -> None:
        super().__init__(ttt)

    def reset(self) -> None:
        pass

    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]: 
        return (2,)

    def undo(self):
        pass
