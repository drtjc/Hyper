import numpy as np #type: ignore
from collections.abc import Sequence
from sys import getsizeof
from enum import Enum, auto
from typing import NamedTuple, List, Tuple, Union, Sequence
from pprint import pprint
from colorama import init, Fore, Back, Style
init()

import hypercube as hc
Cell_coord = hc.Cell_coord

class Error(Exception):
    """ Base class for exceptions in this module."""
    pass


class MoveError(Error):
    """ Raised if a cell has already been played."""

    def __init__(self, message: str, cell: Cell_coord):
        self.message = message
        self.cell = cell


class GameOverError(Error):
    """ Raised if a move is played when the game is not in progress."""

    def __init__(self, message: str):
        self.message = message


class GameState(Enum):
    """ Enumeration used to store state of game."""

    WIN_P1 = auto()
    WIN_P2 = auto()
    TIE = auto()
    IN_PROGRESS = auto()


class Memory(NamedTuple):
    dtype: int
    board: int
    scopes: int
    total: int


class Move(NamedTuple):
    Player: int
    Cell: Cell_coord


class TicTacToe():
    """ TO DO
    """

    _MOVE_BASE = 99
    
    GameState_str = {GameState.WIN_P1: 'p1 wins', GameState.WIN_P2: 'p2 wins',
                     GameState.TIE: "It's a tie", GameState.IN_PROGRESS: 'In progress'}

    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:

        try:            
            self.board, _, self.scopes = hc.structure_np(d, n, zeros = False, OFFSET = self._MOVE_BASE)
        except MemoryError:
            print("The board is too big to fit into available memory")
            raise

        self.d = d
        self.n = n
        self.moves_per_turn = moves_per_turn
        self.drop = drop
        self.reset()
        self._p_names = ['Player 1', 'Player 2']
        self._p_marks = ['O', 'X']     
        self.color_last_move = Fore.BLUE
        self.color_win_line = Back.MAGENTA

    def reset(self) -> None:
        self.state = GameState.IN_PROGRESS  
        self.board.fill(0)
        self.win_line: List[int] = []
        
        self.active_player = 0
        self.active_moves = 0

        self.moves: List[Move] = []
        self.moves_played: List[int] = [0, 0] # number of moves played in game by each player

    @property
    def p_names(self) -> Sequence[str]:
        return self._p_names

    @p_names.setter
    def p_names(self, names: Sequence[str]) -> None:
        if not all(names):
            raise ValueError("Player names cannot be empty strings")
        elif names[0] == names[1]:
            raise ValueError("Player names must be unique")
        else:
            self._p_names = list(names)

    @property
    def p_marks(self) -> Sequence[str]:
        return self._p_marks

    @p_marks.setter
    def p_marks(self, marks: Sequence[str]) -> None:
        if not all(marks):
            raise ValueError("Player marks cannot be empty strings")
        elif len(marks[0]) != len(marks[1]):
            raise ValueError("Player marks must be of the same length")
        elif marks[0] == marks[1]:
            raise ValueError("Player marks must be unique")
        else:
            self._p_marks = list(marks)

    def state_str(self) -> str:
        return self.GameState_str[self.state].replace('p1', self.p_names[0]).replace('p2', self.p_names[1])

    def memory(self) -> Memory:
        m = self.board.nbytes, getsizeof(self.scopes)
        return Memory(self.board.dtype, *m, sum(m))

    def display_cell(self, v: int) -> Tuple[str, str]:

        f: str = Fore.RESET
        b: str = Back.RESET

        if v > 0:
            s = self.p_marks[0]
        elif v < 0:
            s = self.p_marks[1]
        else:
            s = ' ' * len(self.p_marks[0])

        # check if cell is last move, and adjust color if so
        if len(self.moves) > 0:
            last_move = self.moves[-1][1]
            if self.board[last_move] == v:
                f = self.color_last_move
        
        if self.state == GameState.WIN_P1 or self.state == GameState.WIN_P2:
            if v in self.win_line:
                b = self.color_win_line

        return s, f + b
    
    def display(self, header: bool = False) -> None:
        b = hc.display_np(self.board, self.display_cell) + '\n'
        if header:
            b = f'\nd = {self.d}, n = {self.n}\n\n' + b
        print(b)


    def move(self, cell: Union[str, Cell_coord], offset: int = 1) -> None:
        if self.state != GameState.IN_PROGRESS:
            raise GameOverError("The game is over")

        try:
            if isinstance(cell, str):
                t_cell = hc.str_to_tuple(self.d, self.n, cell, offset)
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
            raise MoveError("The cell has already been played", t_cell)

        # we now have an empty cell
        self.moves_played[self.active_player] += 1
        sgn = -1 if self.active_player == 1 else 1 # player 0 is positive, player 1 negative
        self.board[t_cell] = sgn * (self.moves_played[self.active_player] + self._MOVE_BASE)
        self.moves.append(Move(self.active_player, t_cell))

        # don't check for win yet as undo function can undo a win, but will
        # not work properly unless code below is executed
        self.active_moves += 1
        if self.active_moves == self.moves_per_turn:
            self.active_moves = 0
            self.active_player = int(not self.active_player)

        # check for win now
        if self.is_win(): 
            self.state = GameState.WIN_P2 if self.active_player else GameState.WIN_P1
            return
        elif self.is_tie():
            self.state = GameState.TIE
            return
        else:
            self.state = GameState.IN_PROGRESS
            return


    def is_tie(self) -> bool:
        if self.state == GameState.TIE:
            return True
        else: 
            if len(self.moves) == self.n ** self.d:
                # all cells played
                return True
            else:
                return False

    def is_win(self) -> bool:
        if self.state == GameState.WIN_P1 or self.state == GameState.WIN_P2:
            return True
        elif self.state == GameState.TIE:
            return False
        else: # check to see if last move was a winning move
            if len(self.moves) < 2 * self.n - 1:
                return False
            else:
                t_cell = self.moves[-1][1]
                for line in self.scopes[t_cell]:
                    if sum(line > self._MOVE_BASE) == self.n or sum(line < -self._MOVE_BASE) == self.n:
                        self.win_line = line
                        return True
                return False


    def undo(self, replace: int = 0) -> None:
        """ Undo the last move.

        Parameters
        ----------
        replace: int, optional
            The value that will be put into the cell that the last
            move was made in.
        
        Returns
        -------
        None

        Examples
        --------
        >>> ttt = TicTacToe(2, 3)
        >>> ttt.move('22')
        >>> ttt.move('11')
        >>> ttt.move('33')
        >>> ttt.display() #doctest: +SKIP
        X̲|_|_
        _|O̲|_
         | |O    
        >>> ttt.moves
        [(0, (1, 1)), (1, (0, 0)), (0, (2, 2))]
        >>> ttt.undo()
        >>> ttt.display() #doctest: +SKIP
        X̲|_|_
        _|O̲|_
         | |   
        >>> ttt.moves
        [(0, (1, 1)), (1, (0, 0))]
        """

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






if __name__ == "__main__":
 
    dim = 4
    size = 3
    ttt = TicTacToe(dim, size, 1)
    ttt.p_names = ['Tom 2', 'Tom']
    ttt.p_names = 'Tom 2', 'Tom'
    print(ttt.p_names[0])
    ttt.p_marks = ["0", "X"]
    #ttt.color_last_move = Fore.MAGENTA

    #print(ttt.state_str())

    ttt.move('1111')
    ttt.display(False)
    print(ttt.state_str())

    ttt.move('1211')
    ttt.display(False)
    print(ttt.state_str())

    ttt.move('2222')
    ttt.display(False)
    print(ttt.state_str())
    
    ttt.move('1312')
    ttt.display(False)
    print(ttt.state_str())

#    ttt.move('3333')
#    ttt.display(False)
#    print(ttt.state_str())



#     print(ttt.state_str())
    
    #m = ttt.move('21')
    #ttt.display(False)
#     print(ttt.state_str())

    #m = ttt.move('33')
    #ttt.display(False)
#     print(ttt.state_str())

    #m = ttt.move('31')
    #ttt.display(False)
#     print(ttt.state_str())

    #print(ttt.win_line)

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
    


