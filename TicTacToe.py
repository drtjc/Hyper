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


    def db(self, s1, s2):
        # add two strings together that have \n in them
        # number of lines
        #tt = [x.split() for x in spl]

        # even dim in string, odd odd dimension to end of string

        # existing string has n lines and assume last is an empty lime

        # given string of n lines, add new string with n lines)
        #  need existing string by lines
        # spl_1 = s1.split('\n')
        # n_1 = len(spl_1)

        # spl_2 = s2.split('\n')
        # n_2 = len(spl_2)

        # if n_1 != n_2:
        #     print("ooooops")

        # m = [x + " " + y for x, y in zip(spl_1, spl_2)]
        # mm = '\n'.join(m)
        # print(mm)

        ## XXX
        ## XXX
        ## XXX
        print(join_multiline(s1, s2))


    def display_board(self):
        # number of horizontals is d/2, d even, (d+1)/2, d odd
        # number of verticals is (d-1)/2, d odd, d/2, d even
        d = self.d
        n = self.n
        h = int(d / 2 if d % 2 == 0 else (d + 1) / 2)
        v = int(d / 2 if d % 2 == 0 else (d - 1) / 2)
        print(h)
        print(v)

        vis = ""
        for y in range(1, 2 ** v):
            for j in range(n):
                for x in range(1, 2 ** h): # take what had before and add d-1 times 
                    for i in range(n):
                        vis += "X"
                        if i == n - 1:
                            vis += " "
                vis += "\n"
                if j == n - 1:
                    vis += "\n"
        print(vis)


if __name__ == "__main__":
 
    dim = 5
    size = 3
    tictactoe = TicTacToe(dim, size)

    #print(tictactoe.num_lines)
 
    #print(tictactoe.memory())
    
    #print(tictactoe.scopes)
    #print(hc.scopes_size_cells(tictactoe.scopes))
    #print(hc.scopes_size(tictactoe.scopes))

    #tictactoe.display_term()
    s1 = "XXX\nXXX\nXXX\n"
    s2 = "YYY\nYYY\nYYY\n"
    tictactoe.db(s1, s2)
    #print(tictactoe.board)
