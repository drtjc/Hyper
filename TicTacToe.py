import numpy as np #type: ignore
import re
from collections.abc import Sequence
from sys import getsizeof
from enum import Enum, auto
from typing import NamedTuple, List, Tuple
from pprint import pprint
from colorama import init, Fore, Back, Style
init()

import hypercube as hc


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class MoveError(Error):

    def __init__(self, message, cell):
        self.message = message
        self.cell = cell


class GameOverError(Error):

    def __init__(self, message):
        self.message = message



class GameState(Enum):
    P1_WIN = auto()
    P2_WIN = auto()
    TIE = auto()
    IN_PROGRESS = auto()


class TicTacToe():

    _MOVE_BASE = 99
    
    Memory = NamedTuple('Memory', [('dtype', str), ('board', int), ('lines', int),
                                   ('scopes', int), ('total', int)]) 
    
    GameState_str = {GameState.P1_WIN: 'p1 wins', GameState.P2_WIN: 'p2 wins', 
                     GameState.TIE: "It's a tie", GameState.IN_PROGRESS: 'In progress'}

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:

        try:            
            struct = hc.structure_np(d, n, zeros = False, OFFSET = self._MOVE_BASE)
        except MemoryError:
            print("The board is too big to fit into available memory")
            raise

        self.d = d
        self.n = n
        self.moves_per_turn = moves_per_turn
        self.drop = drop

        self.board = struct[0]
        self.lines = struct[1]
        self.num_lines = len(self.lines)
        self.scopes = struct[2]

        self.reset()

        self.p1_name = 'Player 1'
        self.p2_name = 'Player 2'
        # p1 and p2 should be alphabetic characters, and of the same length
        self.p1_mark = 'O'
        self.p2_mark = 'X'
        
        self.color_last_move = Fore.BLUE
        self.color_win_line = Back.MAGENTA

    def state_str(self):
        return self.GameState_str[self.state].replace('p1', self.p1_name).replace('p2', self.p2_name)

    def reset(self):
        self.state = GameState.IN_PROGRESS  
        self.board.fill(0)
        self.win_line: List[int] = []
        
        self.active_player: int = 0
        self.active_moves: int = 0

        # record player 0 moves as positive integers, and player 1 moves as negative integer
        self.moves: List[Tuple[int, ...]] = []  
        self.moves_played: List[int] = [0, 0] # number of moves played in game by each player

        self.lines_state = []


    def memory(self) -> Memory:
        m = self.board.nbytes, getsizeof(self.lines), getsizeof(self.scopes)
        return self.Memory(self.board.dtype, *m, sum(m))


    def display_cell(self, v):

        f = Fore.RESET
        b = Back.RESET

        if v > 0:
            s = self.p1_mark
        elif v < 0:
            s = self.p2_mark
        else:
            s = ' ' * len(self.p1_mark)

        # check if cell is last move, and adjust color if so
        if len(self.moves) > 0:
            last_move = self.moves[-1][1]
            if self.board[last_move] == v:
                f = self.color_last_move
        
        if self.state == GameState.P1_WIN or self.state == GameState.P2_WIN:
            if v in self.win_line:
                b = self.color_win_line

        return s, f + b
    
        

    def display(self, header = True):
        b = hc.display_np(self.board, self.display_cell) + '\n'
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
        if self.state != GameState.IN_PROGRESS:
            raise GameOverError("The game is over")

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

        # check for win now
        idx = self.get_lines_state()
        if idx > - 1:
            self.state = GameState.P2_WIN if self.active_player else GameState.P1_WIN
            return -1

        # game still in progress
        self.active_moves += 1
        if self.active_moves == self.moves_per_turn:
            self.active_moves = 0
            self.active_player = int(not self.active_player)

        # need to check if the game can be won
        if self.is_tie():
            self.state = GameState.TIE
            return 0
        else:
            return 1


    def is_tie(self):
        if self.state == GameState.TIE:
            return True
        else: 
            # check if a win is possible
            if len(self.moves) == self.n ** self.d:
                return True
            else:
                return False

    def is_win(self):
        if self.state == GameState.P1_WIN or self.state == GameState.P2_WIN:
            return True
        elif self.state == GameState.TIE:
            return False
        else: # check to see if last move was a winning move
            if len(self.moves) < 2 * self.n:
                return False
            else:
                t_cell = self.moves[-1]
                ## tjc check each line on scope of t_cell

    def get_lines_state(self):
        # list of tuples - each tuple containg number of +ves and -eves in a line
        ##TJC do we want also how many are consecutive??
        # return idx of winning line if there is one
        self.lines_state.clear()
        for c, line in enumerate(self.lines):
            state = (sum(line > self._MOVE_BASE), sum(line < -self._MOVE_BASE))
            self.lines_state.append(state)
            if state[0] == self.n or state[1] == self.n:
                self.win_line = line
                return c

                ## could check scope of last move first for winning line

        return -1 # no winning line


    def undo(self, replace = 0):
        if len(self.moves) == 0:
            return

        self.state = GameState.IN_PROGRESS
        
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
 
    dim = 2
    size = 3
    ttt = TicTacToe(dim, size, 1)
    ttt.p1_name = 'Tom'
    ttt.p2_name = 'Other'

    #ttt.color_last_move = Fore.MAGENTA

    print(ttt.state_str())

    m = ttt.move('11')
    ttt.display(False)
    #print(ttt.state_str())

    m = ttt.move('12')
    ttt.display(False)
#     print(ttt.state_str())
    
    m = ttt.move('21')
    ttt.display(False)
#     print(ttt.state_str())

    m = ttt.move('33')
    ttt.display(False)
#     print(ttt.state_str())

    m = ttt.move('31')
    ttt.display(False)
#     print(ttt.state_str())

    print(ttt.win_line)

#    m = ttt.move('23')
#    ttt.display(False)
#     print(ttt.state_str())

# # game over
#    m = ttt.move('31')
#    ttt.display(False)
#     print(ttt.state_str())

#     ttt.undo()
#     #ttt.display(False)
#     print(ttt.state_str())


# if played with game over then game over error
    #m = ttt.move('13')
    #ttt.display(False)
    #print(ttt.state_str())

    #m = ttt.move('31')
    #ttt.display(False)
    #print(ttt.state_str())

    #m = ttt.move('32')
    #ttt.display(False)
    #print(ttt.state_str())



# move already played
#    m = ttt.move('23')
#    ttt.display(False)
#    print(ttt.state_str)
    



