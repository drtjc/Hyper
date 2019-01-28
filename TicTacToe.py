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

    def display_4x4x4_term(self, players = True, settings = True):
        
        if self.d != 3:
            raise ValueError("not a 3d board")

        if self.n != 4:
            raise ValueError("not a board of 4 cells")
        

        # iter over cells, flat, turn index into coords.
        shape = [self.n] * self.d
        for count, cell in enumerate(np.nditer(self.board)):
            coord = np.unravel_index(count, shape)
            print(coord)
        
        
        # print(self.underline("test"))
        # vis = ""
        # for cell in self.board.cells_rlc():
            
        #     #print(cell.position, end = ' ')

        #     if cell.is_empty:
        #         cell._value = "B"

        #     if not cell.is_front_face:
        #         #print("see")
        #         vis += self.underline(cell.value)
        #     else:
        #         #print("hi")
        #         vis += cell.value

        #     if not cell.is_right_face:
        #         #print("line")
        #         vis += "|"
        #     else:
        #         #print("here")
        #         if cell.is_bottom_face:
        #             #print("bottom)")
        #             vis += "\n"
        #         else:
        #             vis += "  "
        #             #print("space")    

        # print(vis)
        return




if __name__ == "__main__":
 
    dim = 3
    size = 3
    tictactoe = TicTacToe(dim, size)

    #print(tictactoe.num_lines)
 
    #print(tictactoe.memory())
    #print(tictactoe.board)
    #print(tictactoe.scopes)
    #print(hc.scopes_size_cells(tictactoe.scopes))
    #print(hc.scopes_size(tictactoe.scopes))

    tictactoe.display3D_term()
