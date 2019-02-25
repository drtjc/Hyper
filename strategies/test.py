#from strategy import Strategy



#@Strategy.register
#class Testv:
#    pass

import hypercube as hc
Cell_coord = hc.Cell_coord

class SCH:

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        pass
        #super().__init__(d, n, moves_per_turn, drop)
        self.dd = None

    def move(self, cell: Cell_coord) -> Cell_coord:
        print("SCH")
        return (1,)

    def undo(self) -> None:
        return None

  