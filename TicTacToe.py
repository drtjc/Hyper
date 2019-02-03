import numpy as np #type: ignore
import re
from collections.abc import Sequence
from sys import getsizeof
from typing import NamedTuple, List, Tuple
from pprint import pprint

import hypercube as hc


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MoveError(Error):

    def __init__(self, message, cell):
        self.message = message
        self.cell = cell





class TicTacToe():

    _MOVE_BASE = 99
    Memory = NamedTuple('Memory', [('dtype', str), ('board', int), ('lines', int), ('scopes', int), ('total', int)]) 

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:

        try:            
            struct = hc.structure_np(d, n, zeros = True, OFFSET = self._MOVE_BASE)
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

        self.reset()

        self.p1 = 'O'
        self.p2 = 'X'

    def reset(self):
        self.in_progress = True 
        self.board.fill(0)
        
        self.active_player: int = 0
        self.active_moves: int = 0

        # record player 0 moves as positive integers, and player 1 moves as negative integer
        self.moves: List[Tuple[int]] = [] ##TJC need to specifiy tuple for mypy is d lots of int 
        self.moves_played: List[int] = [0, 0] # number of moves played in game by each player

        self.lines_state = []


    def memory(self) -> Memory:
        m = self.board.nbytes, getsizeof(self.lines), getsizeof(self.scopes)
        return self.Memory(self.board.dtype, *m, sum(m))


    def display_cell(self, v):
        if v > 0:
            return self.p1
        elif v < 0:
            return self.p2
        else:
            return ' '

    def display(self, header = True):
        b = hc.display(self.board, self.display_cell) + '\n'
        if header:
            b = f'\nd = {self.d}, n = {self.n}\n\n' + b
        print(b)

    def str_to_tuple(self, cell, base = 1):
        if isinstance(cell, str):
            # check to see if there are any non-digits
            nd = re.findall(r'\D+', cell) 
            if len(nd) == 0: 
                if self.d - -1 + base > 9:
                    raise ValueError("Too many dimensions for each to be specified by single digit")
                else:
                    tup = tuple(int(coord) - base for coord in cell) 
            else: # there are non-digits, use these as separators
                tup = tuple(int(coord) - base for coord in re.findall(r'\d+', cell)) 
            
            # check that correct number of coordinates specified
            if len(tup) != self.d:
                raise ValueError("Incorrect number of coordinates provided")

            # check that each coordinate is valid
            if all(t in range(self.n) for t in tup):
                return tup
            else:
                raise ValueError("One or more coordinates are not valid")           
        else:
            raise TypeError(f'String argument expected, got {type(cell)})')

    def move(self, cell, base = 1):
        if not self.in_progress:
            print("New game")
            self.reset()

        try:
            if isinstance(cell, str):
                t_cell = self.str_to_tuple(cell, base)
            else:
                t_cell = tuple(cell)
            
            v = self.board[t_cell]
        except:
            raise Error("Invalid cell argument was provided")

        # we now have a validly defined cell
        if self.drop:
            pass
        else:
            pass

        if abs(v) > self._MOVE_BASE:
            # if players whose turn it is is interative then get them
            # to put another move in rather than raise error
            raise MoveError("The cell has already been played", cell)

        # we now have an empty cell
        self.moves_played[self.active_player] += 1
        sgn = -1 if self.active_player == 1 else 1 # player 0 is positive, player 1 negative
        self.board[t_cell] = sgn * (self.moves_played[self.active_player] + self._MOVE_BASE)
        self.moves.append((self.active_player, t_cell))
        self.display(False)

        self.active_moves += 1
        if self.active_moves == self.moves_per_turn:
            self.active_moves = 0
            self.active_player = int(not self.active_player)

        # can check for win now
        idx = self.get_lines_state()
        if idx > - 1:
            self.in_progress = False
            print("winner!\n")
            return True
        else:
            return False

    def get_lines_state(self):
        # list of tuples - each tuple containg number of +ves and -eves in a line
        ##TJC do we want also how many are consecutive??
        # return idx of winning line if there is one
        self.lines_state.clear()
        for c, line in enumerate(self.lines):
            state = (sum(line > self._MOVE_BASE), sum(line < -self._MOVE_BASE))
            self.lines_state.append(state)
            if state[0] == self.n or state[1] == self.n:
                return c

        return -1 # no winning line


    def undo(self, replace = 0):
        if len(self.moves) == 0:
            return

        self.in_progress = True # in case game has just been won
        
        if self.active_moves == 0:
            self.active_moves = self.moves_per_turn - 1
            self.active_player = int(not self.active_player)
        else:
            self.active_moves -= 1

        self.moves_played[self.active_player] -= 1
        self.board[self.moves[-1][1]] = replace
        del self.moves[-1]
        self.get_lines_state()



if __name__ == "__main__":
 
    dim = 9
    size = 2
    ttt = TicTacToe(dim, size, 1)

    #print(ttt.lines[0])
    #m = ttt.move('111')
    #m = ttt.move('131')
    #m = ttt.move('222')
    #m = ttt.move('121')
    #m = ttt.move('333')


    #if m:
    #    print("game over")
    #print(ttt.moves)
    #ttt.move('22')

    #ttt.undo()
    #print(ttt.moves)
    ttt.display()

    #m = ttt.move('333')

    #m = ttt.move('11')

    #print(ttt.lines[1])
    #print(sum((ttt.lines[1]) > 0))

