import numpy as np #type: ignore
from sys import getsizeof
from typing import NamedTuple
from pprint import pprint

import hypercube as hc
from helper import underline, join_multiline


class TicTacToe():

    Memory = NamedTuple('Memory', [('board', int), ('lines', int), ('scopes', int), ('total', int)]) 

    def __init__(self, d: int, n: int) -> None:
        try:
            self.d = d
            self.n = n
            
            struct = hc.structure_np(d, n, False)
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


    def display_order(self):
        do = [0]
        for i in range(2, self.d + 1):
            do = [x + 1 for x in do]
            if i % 2 == 0: #even
                do.insert(0, 0)
            else: # odd
                do.insert(-int((i + 1) / 2) + 1, 0)
        return do


    def display_term(self):
        if self.d == 2:
            self.display_2D_term()
        elif self.d == 3:
            self.display_3D_term()
        elif self.d == 4:
            self.display_4D_term()
        elif self.d == 5:
            self.display_5D_term()
        else:
            raise ValueError("Only 2D, 3D or 4D boards can be printed to the terminal") #what about 1d, 5d
        return


    def display_2D_term(self):
        
        if self.d != 2:
            raise ValueError("Not a 2D board")

        vis = ""
        for r in range(self.n):
            for c in range(self.n):

                s = str(self.board[r, c])
                #s = "X"
                    
                if r != (self.n - 1): # not last row 
                    vis += underline(s)
                else: # last row
                    vis += s

                if c != (self.n - 1): # not last column
                    vis += "|"

                if c == (self.n - 1) and r != (self.n - 1):
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

                    s = str(self.board[p, r, c])
                    s = "X"
                    
                    if r != (self.n - 1): # not last row 
                        vis += underline(s)
                    else: # last row
                        vis += s

                    if c != (self.n - 1): # not last column
                        vis += "|"

                    if c == (self.n - 1) and p != (self.n - 1):
                        vis += "  "

                    if c == (self.n - 1) and p == (self.n - 1) and r != (self.n - 1): # last pillar
                        vis += "\n"
        print(vis)
        return


    def display_4D_term(self):
        
        if self.d != 4:
            raise ValueError("Not a 4D board")

        vis = ""
        for l in range(self.n):
            for r in range(self.n):
                for p in range(self.n):
                    for c in range(self.n):
                        
                        s = str(self.board[l, p, r, c])
                        #s = "X"

                        if r != (self.n - 1): # not last row 
                            vis += underline(s)
                        else: # last row
                            vis += s

                        if c != (self.n - 1): # not last column
                            vis += "|"
                        
                        if c == (self.n - 1) and p != (self.n - 1):
                            vis += "  "

                        if c == (self.n - 1) and p == (self.n - 1): # last pillar
                            vis += "\n"
                        
                        if r == (self.n - 1) and c ==  (self.n - 1) and p == (self.n - 1) and l != (self.n -1):
                            vis += "\n" 
        print(vis)
        return



    def display_5D_term(self):
        
        if self.d != 5:
            raise ValueError("Not a 5D board")

        vis = ""
        for l in range(self.n):
            for r in range(self.n):
                for e in range(self.n):
                    for p in range(self.n):
                        for c in range(self.n):
                        
                            s = f'{(self.board[e, l, p, r, c]): <{3}}'
                            #s = "XX"

                            if r != (self.n - 1): # not last row 
                                #vis += underline(s)
                                vis += s
                            else: # last row
                                vis += s

                            if c != (self.n - 1): # not last column
                                vis += "|"

                            if c == (self.n - 1) and p != (self.n - 1):
                                vis += "  "

                            if c == (self.n - 1) and p == (self.n - 1) and e != (self.n - 1): # last pillar
                                vis += "  |  "
                            
                            if c ==  (self.n - 1) and p == (self.n - 1) and e == (self.n - 1):
                                vis += "\n"    

                            if r == (self.n - 1) and c ==  (self.n - 1) and p == (self.n - 1) and e == (self.n - 1) and l != (self.n - 1):
                                vis += "--------------|\n" 
        print(vis)
        return





def db2():
    disp = ""

    def dbr(arr):
        nonlocal disp

        if arr.size == 1:
            return str(arr).ljust(2)
            #return "_"
            #return underline("X")
            #return f'{arr: <{3}}'

        sub_arr = [arr[i] for i in range(arr.shape[0])]
        print(f'sub_arr = {sub_arr}')
        sub_arr_str = [dbr(a) for a in sub_arr]
        print(f'sub_arr_str = {sub_arr_str}')
        
        d = arr.ndim
        print(f'd = {d}')
        if d % 2 == 0: # even number of dimensions - display down the screen
            if d == 2:
                return disp.join('\n'.join(sub_arr_str))
            else:
                # need to put in dividing line size of which depends on dim and size
                return disp.join('\n\n'.join(sub_arr_str))
        else: # odd number of dimensions - display across the screen
            if d == 1:
                return disp.join(join_multiline(sub_arr_str, "|"))
            else:
                # space betwnee || depends on dim and size i think
                return disp.join(join_multiline(sub_arr_str, "  ||  ", 2, "            "))
        
                    
        return disp
    return dbr



if __name__ == "__main__":
 
    dim = 6
    size = 2
    tictactoe = TicTacToe(dim, size)

    #print(tictactoe.num_lines)
 
    #print(tictactoe.memory())
    
    #print(tictactoe.scopes)
    #print(hc.scopes_size_cells(tictactoe.scopes))
    #print(hc.scopes_size(tictactoe.scopes))

    #tictactoe.display_term()
    s = db2()(tictactoe.board)
    print(s)
    #print(tictactoe.board)


    #s = ['AAA\nBBB\nCCC\n', 'MMM\nNNN\nOOO\n', 'XXX\nYYY\nZZZ\n']
    #ss = ['AAA\nBBB\nCCC', 'MMM\nNNN\nOOO', 'XXX\nYYY\nZZZ']

    #ml = join_multiline(s)
    #print(ml)
    #pprint(ml)