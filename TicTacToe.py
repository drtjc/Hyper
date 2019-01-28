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


    def display_2D_term(self):
        
        if self.d != 2:
            raise ValueError("Not a 2D board")

        vis = ""
        for r in range(self.n):
            for c in range(self.n):

                s = str(self.board[r,c])
                #s = "X"
                    
                if r != (self.n - 1): # not last row 
                    vis += underline(s)
                else: # last row
                    vis += s

                if c != (self.n - 1): # not last column
                    vis += "|"
                else: # last column
                    vis += "\n"
        print(vis)
        return

    
    
    def display_3D_term(self):
        
        if self.d != 3:
            raise ValueError("Not a 3D board")

        vis = ""
        for r in range(self.n):
            for p in range(self.n):
                for c in range(self.n):

                    s = str(self.board[p,r,c])
                    s = "X"
                    
                    if r != (self.n - 1): # not last row 
                        vis += underline(s)
                    else: # last row
                        vis += s

                    if c != (self.n - 1): # not last column
                        vis += "|"
                    else: # last column
                        if p == (self.n - 1): # last pillar
                            vis += "\n"
                        else: # not last pillar
                            vis += "  "
        print(vis)
        return


if __name__ == "__main__":
 
    dim = 2
    size = 3
    tictactoe = TicTacToe(dim, size)

    #print(tictactoe.num_lines)
 
    #print(tictactoe.memory())
    
    #print(tictactoe.scopes)
    #print(hc.scopes_size_cells(tictactoe.scopes))
    #print(hc.scopes_size(tictactoe.scopes))

    tictactoe.display_2D_term()
    #print(tictactoe.board)
