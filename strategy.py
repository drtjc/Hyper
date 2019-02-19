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


def strategy(s):
    strategies.register(s)
    return s






#class LineState(NamedTuple):
#    P1_total_marks: int
#    P1_consecutive_marks: int
#    P2_total_marks: int
#    P2_consecutive_marks: int


@strategy
class Heuristics(Strategy):

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        super().__init__(d, n, moves_per_turn, drop)
        print("here")

    def move(self, cell: Cell_coord) -> Cell_coord:
        pass

    def undo(self, cell: Cell_coord) -> Cell_coord:
        pass

    # def get_lines_state(self) -> int:
    #     # list of tuples - each tuple containg number of +ves and -eves in a line
    #     ##TJC do we want also how many are consecutive??
    #     # return idx of winning line if there is one
    #     self.lines_state.clear()
    #     for c, line in enumerate(self.lines):
    #         #state = (sum(line > self._MOVE_BASE), sum(line < -self._MOVE_BASE))
    #         state = LineState(sum(line > self._MOVE_BASE), -1, sum(line < -self._MOVE_BASE), -1)
    #         self.lines_state.append(state)
    #         if state[0] == self.n or state[2] == self.n:
    #             self.win_line = line
    #             return c

    #             ## could check scope of last move first for winning line

    #     return -1 # no winning line


@strategy
class Random(Strategy):
    
    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        super().__init__(d, n, moves_per_turn, drop)

    def move(self, cell: Cell_coord) -> Cell_coord:
        pass

    def undo(self, cell: Cell_coord) -> Cell_coord:
        pass



@strategy
class Interactive(Strategy):
    
    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        super().__init__(d, n, moves_per_turn, drop)

    def move(self, cell: Cell_coord) -> Cell_coord:
        pass

    def undo(self, cell: Cell_coord) -> Cell_coord:
        pass




if __name__ == "__main__":


    d = {'a':3, 'b':4}

    #s = Strategies_test()
    #s.add(Random)
    #print(s)

    print(strategies)
    t = strategies['Heuristics'](4,3)
    print(t.drop)
    #sn = [s.__name__ for s in strategies]
    #print(sn)

    #h = Heuristics(3, 4)
    #print(h.d)
