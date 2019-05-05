from strategy import Strategy
from tictactoe import TicTacToe
from typing import Union, Optional


@Strategy.register
class Testv:
    
    @classmethod
    def validate(cls, d: int, n: int, moves_per_turn: int) -> bool:
        return True

import hypercube as hc
Cell_coord = hc.Cell_coord

class SCH:

    @classmethod
    def validate(cls, d: int, n: int, moves_per_turn: int, drop: bool) -> bool:
        return True

    def __init__(self, ttt: TicTacToe) -> None:
        pass

    def reset(self) -> None:
        pass        

    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]: 
        #print("SCH")
        return (4,)


  