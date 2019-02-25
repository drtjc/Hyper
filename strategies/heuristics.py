import hypercube as hc
from strategy import Strategy

Cell_coord = hc.Cell_coord



#import heuristics


#class LineState(NamedTuple):
#    P1_total_marks: int
#    P1_consecutive_marks: int
#    P2_total_marks: int
#    P2_consecutive_marks: int



class Heuristics(Strategy):

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        super().__init__(d, n, moves_per_turn, drop)

    def move(self, cell: Cell_coord) -> Cell_coord:
        return (1,)

    def undo(self):
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


