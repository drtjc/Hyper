from strategy import Strategy
from typing import Union


@Strategy.register
class Testv:
    pass

import hypercube as hc
Cell_coord = hc.Cell_coord

class SCH:

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        pass
        #super().__init__(d, n, moves_per_turn, drop)
        

    def move(self, cell: Union[Cell_coord]) -> Cell_coord:
        #print("SCH")
        return (4,)

    def undo(self) -> None:
        return None

  