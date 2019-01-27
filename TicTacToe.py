import numpy as np #type: ignore
from sys import getsizeof
from typing import NamedTuple
from pprint import pprint

import hypercube as hc
from helper import underline


class TicTacToe():

    Memory = NamedTuple('Memory', [('board', int), ('lines', int), ('scopes', int), ('total', int)]) 

    def __init__(self, d: int, n: int) -> None:
        try:
            self.d = d
            self.n = n
            
            struct = hc.structure_np(d, n)
            self.board = struct[0]
            self.lines = struct[1]
            self.num_lines = len(self.lines)
            self.scopes = struct[2]

        except MemoryError:
            raise MemoryError("The board is too big to fit into available memory")

    def clear(self):
        self.board.fill(0)

    def memory(self) -> Memory:
        m = self.board.nbytes, getsizeof(self.lines), getsizeof(self.scopes)
        return self.Memory(*m, sum(m))





if __name__ == "__main__":
 
    dim = 2
    size = 2
    tictactoe = TicTacToe(dim, size)

    print(tictactoe.num_lines)
 
    print(tictactoe.memory())
    print(tictactoe.board)
    print(tictactoe.scopes)
    print(hc.scopes_size_cells(tictactoe.scopes))
    print(hc.scopes_size(tictactoe.scopes))

