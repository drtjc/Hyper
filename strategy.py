import abc
import hypercube as hc
from typing import Tuple, Dict, Type, Optional

Cell_coord = hc.Cell_coord

class Strategy(abc.ABC):

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        self.d = d
        self.n = n
        self.moves_per_turn = moves_per_turn
        self.drop = drop

    @abc.abstractmethod
    def move(self, cell: Cell_coord) -> Cell_coord:
        """ Calculate the move to be played """

    @abc.abstractmethod
    def undo(self, cell: Cell_coord) -> Cell_coord:
        """ Undo last move played """


class Strategies(Dict[str, Type[Strategy]]):

    def __init__(self) -> None:
        super()

    def register(self, s: Type[Strategy]) -> None:
        self[s.__name__] = s 


strategies = Strategies()


def dec_strategy(s):
    strategies.register(s)
    return s



#import heuristics


#class LineState(NamedTuple):
#    P1_total_marks: int
#    P1_consecutive_marks: int
#    P2_total_marks: int
#    P2_consecutive_marks: int







if __name__ == "__main__":

    #import strategy
    print(f'y1')
    import heuristics as he
    print("2")
    


    print(len(strategies))
    print(strategies)
    t = strategies['Heuristics'](4,3)
    print(t.drop)
    #sn = [s.__name__ for s in strategies]
    #print(sn)

    #h = Heuristics(3, 4)
    #print(h.d)
