import numpy as np #type: ignore
from sys import getsizeof
from typing import NamedTuple
from pprint import pprint

import hypercube as hc


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MoveError(Error):

    def __init__(self, message, arg):
        self.message = message
        self.arg = arg





class TicTacToe():

    _MOVE_BASE = 99
    Memory = NamedTuple('Memory', [('dtype', str), ('board', int), ('lines', int), ('scopes', int), ('total', int)]) 

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:

        try:            
            struct = hc.structure_np(d, n, False, self._MOVE_BASE)
        except MemoryError:
            raise MemoryError("The board is too big to fit into available memory")

        self.d = d
        self.n = n
        self.moves_per_turn = moves_per_turn
        self.drop = drop

        self.board = struct[0]
        self.lines = struct[1]
        self.num_lines = len(self.lines)
        self.scopes = struct[2]

        self.active_player = 1
        self.active_moves = 0            


    def clear(self):
        self.board.fill(0)


    def memory(self) -> Memory:
        m = self.board.nbytes, getsizeof(self.lines), getsizeof(self.scopes)
        return self.Memory(self.board.dtype, *m, sum(m))


    def display(self, header = True):
        b = hc.display(self.board) + '\n'
        if header:
            b = f'\nd = {self.d}, n = {self.n}\n\n' + b
        print(b)


    def move(self, cell):
        # check is valid move, if not raise error (custom exception??)
        raise MoveError("hi there", cell)
        if self.drop:
            pass
        else:
            # make sure cell has not already been played
            if abs(self.board(cell)) > self._MOVE_BASE:
                pass
            else:
                pass
                ##self.board(cell) = 
        # record move
        # check for win
        # check if time to change active player
        # return active player
        pass




if __name__ == "__main__":
 
    dim = 3
    size = 4
    ttt = TicTacToe(dim, size)

    #print(ttt.board.dtype)
 
    #print(ttt.memory())
    
    #print(tictactoe.scopes)
    #print(hc.scopes_size_cells(tictactoe.scopes))
    #print(hc.scopes_size(tictactoe.scopes))

    #tictactoe.display_term()
    try:
        ttt.move('@')
    except MoveError as error:
        print(error.arg)
    #ttt.display()
    #print(s)
    #print(tictactoe.board)


    #s = ['AAA\nBBB\nCCC', 'MMM\nNNN', 'XXX\nYYY\nZZZ']
    #ss = ['AAA\nBBB\nCCC', 'MMM\nNNN\nOOO', 'XXX\nYYY\nZZZ']

    #ml = join_multiline(s)
    #print(ml)
    #pprint(ml)