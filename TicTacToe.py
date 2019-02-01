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




def db2(): #maybe take size of arr as parameter?
    disp = ""

    def dbr(arr):
        nonlocal disp

        if arr.size == 1:
            #return str(arr).ljust(3)
            #return "_"
            return underline("X")
            #return f'{arr: <{3}}'

        sub_arr = [arr[i] for i in range(arr.shape[0])]
        sub_arr_str = [dbr(a) for a in sub_arr]
        
        d = arr.ndim
        if d % 2 == 0: # even number of dimensions - display down the screen
            if d == 2:
                #return disp.join('\n'.join(sub_arr_str))
                return ''.join('\n'.join(sub_arr_str))
            else:
                sp = '\n' + '\n' * int(d / 2 - 1)
                #return disp.join(sp.join(sub_arr_str))
                return sp.join(sub_arr_str)
        else: # odd number of dimensions - display across the screen
            if d == 1:
                #print(disp)
                #print(sub_arr_str)
                #return disp.join(join_multiline(sub_arr_str, "|")) 
                return '|'.join(sub_arr_str) ### do underlining here??
            else:
                #print(disp)
                #return disp.join(join_multiline(sub_arr_str, '.' * d))
                return ''.join(join_multiline(sub_arr_str, '.' * d))

    return dbr



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
    s = db2()(tictactoe.board)
    print(s)
    #print(tictactoe.board)


    #s = ['AAA\nBBB\nCCC\n', 'MMM\nNNN\nOOO\n', 'XXX\nYYY\nZZZ\n']
    #ss = ['AAA\nBBB\nCCC', 'MMM\nNNN\nOOO', 'XXX\nYYY\nZZZ']

    #ml = join_multiline(s)
    #print(ml)
    #pprint(ml)