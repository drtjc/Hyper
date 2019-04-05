from strategy import Strategy
from tictactoe import TicTacToe
from typing import Union, Optional


@Strategy.register
class Testv:
    pass

import hypercube as hc
Cell_coord = hc.Cell_coord

class SCH:

    def __init__(self, ttt: TicTacToe) -> None:
        super().__init__(ttt)

    def reset(self) -> None:
        pass        

    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]: 
        #print("SCH")
        return (4,)

    def undo(self) -> None:
        return None

  