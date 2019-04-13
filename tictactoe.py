from numpy import unravel_index
from itertools import groupby
from sys import getsizeof
from enum import Enum, auto
from typing import NamedTuple, List, Tuple, Union, Any
from colorama import init, Fore, Back, Style
init()


import hypercube as hc
from hypercube import Line_np, Cell_coord


class Error(Exception):
    """ Base class for exceptions in this module."""
    pass


class DuplicateMoveError(Error):
    """ Raised if a cell has already been played."""

    def __init__(self, message: str, cell: Any):
        self.message = message
        self.cell = cell


class UnknownMoveError(Error):
    """ Raised if cell is not a valid cell."""

    def __init__(self, message: str, cell: Any):
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
    lines: int
    scopes: int
    total: int


class Move(NamedTuple):
    Player: int
    Cell: Cell_coord


class LineState(NamedTuple):
    P1_total_marks: int
    P1_consecutive_marks: int
    P2_total_marks: int
    P2_consecutive_marks: int


class TicTacToe():
    """ TO DO
    """

    _MOVE_BASE = 99
    
    GameState_str = {GameState.WIN_P1: 'p1 wins', GameState.WIN_P2: 'p2 wins',
                     GameState.TIE: "It's a tie", GameState.IN_PROGRESS: 'In progress'}

    def __init__(self, d: int, n: int, moves_per_turn: int = 1, drop: bool = False) -> None:

        try:            
            self.board, self.lines, self.scopes = hc.structure_np(d, n, zeros = False, OFFSET = self._MOVE_BASE)
        except MemoryError:
            print("The board is too big to fit into available memory")
            raise

        self.d = d
        self.n = n
        self.shape = [n] * d
        self.moves_per_turn = moves_per_turn
        self.drop = drop
        self._names = 'Player 1', 'Player 2'
        self._marks = 'O', 'X'
        self.reset()
        self.color_last_move = Fore.BLUE
        self.color_win_line = Back.MAGENTA
        self._maintain_lines_states = False

    def reset(self) -> None:
        """ Reset the board. """
        self.state = GameState.IN_PROGRESS  
        self.board.fill(0)
        self.win_line: List[int] = []
        
        self.active_player = 0
        self.active_moves = 0

        self.forfeited = False

        self.moves: List[Move] = []
        self.moves_played: List[int] = [0, 0] # number of moves played in game by each player
        self.unplayed = [unravel_index(i, self.shape) for i in range(self.n ** self.d)]

    @property
    def maintain_lines_states(self) -> bool: 
        return self._maintain_lines_states

    @maintain_lines_states.setter
    def maintain_lines_states(self, maintain: bool) -> None:
        if not self._maintain_lines_states and maintain and self.state == GameState.IN_PROGRESS:
            # Trying to start maintaining line states while games is in progress
            # Require full calculation of all line states
            pass
            ## TO DO
        else:
            self._maintain_lines_states = maintain

    @property
    def names(self) -> Tuple[str, str]: 
        return self._names

    @names.setter
    def names(self, names: Tuple[str, str]) -> None:
        if not all(names):
            raise ValueError("Player names cannot be empty strings")
        elif names[0] == names[1]:
            raise ValueError("Player names must be unique")
        else:
            self._names = names

    @property
    def marks(self) -> Tuple[str, str]:
        return self._marks

    @marks.setter
    def marks(self, marks: Tuple[str, str]) -> None:
        if not all(marks):
            raise ValueError("Player marks cannot be empty strings")
        elif len(marks[0]) != len(marks[1]):
            raise ValueError("Player marks must be of the same length")
        elif marks[0] == marks[1]:
            raise ValueError("Player marks must be unique")
        else:
            self._marks = marks

    def state_str(self) -> str:
        """ Description of the game state.

        Returns
        -------
        str :
            Description of the game state.
        """
        
        return self.GameState_str[self.state].replace('p1', self.names[0]).replace('p2', self.names[1])

    ## TJC
    def memory(self) -> Memory:
        m = self.board.nbytes, getsizeof(self.lines), getsizeof(self.scopes)
        return Memory(self.board.dtype, *m, sum(m))

    def display_cell(self, v: int) -> Tuple[str, str, str]:
        """ Callback function used by hypercube.display_np to determine display string for cell.

        Parameters
        ----------
        v : int
            The value in the cell

        Returns
        -------
        tuple :
            Three strings are returned:
            1. The string to be displayed
            2. Any formatting (typically applying color changes) applied before the string is displayed
            3. Any formatting (typically removing color changes) applied afer the string is displayed

        See Also
        --------
        hypercube.display_np

        """
        f: str = Fore.RESET
        b: str = Back.RESET

        if v > 0: # player 0 move
            s = self.marks[0]
        elif v < 0: # player 1 move
            s = self.marks[1]
        else: # cell has not been played
            s = ' ' * len(self.marks[0])

        # check if cell is last move, and adjust color if so
        if len(self.moves) > 0:
            last_move = self.moves[-1][1]
            if self.board[last_move] == v:
                f = self.color_last_move
        
        # check if game has been won and adjust background color of winning line if so
        if self.state == GameState.WIN_P1 or self.state == GameState.WIN_P2:
            if v in self.win_line:
                b = self.color_win_line

        return s, f + b, Style.RESET_ALL
    
    def display(self, header: bool = False) -> None:
        """ Display the board to the terminal.

        Parameters
        ----------
        header
            Is header information shown or not

        Returns
        -------
        None
        """
        b = hc.display_np(self.board, self.display_cell) + '\n'
        if header:
            b = f'\nd = {self.d}, n = {self.n}\n\n' + b
        print(b)


    def move(self, cell: Union[str, Cell_coord], offset: int = 1) -> None:
        """ Player makes a move.

        Parameters
        ----------
        cell: str or tuple
            The cell being played
        offset: int, optional
            For a cell specified as a string, what is first dimension.
            Defaults to 1; typically 0 would be the other choice 

        Returns
        -------
        None

        Raises
        ------
        ##TO DO

        Example
        -------

        """
        if self.state != GameState.IN_PROGRESS:
            raise GameOverError("The game is over")

        try:
            if isinstance(cell, str):
                t_cell = hc.str_to_tuple(self.d, self.n, cell, offset)
            else:
                t_cell = tuple(cell)
            
            v = self.board[t_cell]
        except:
            raise UnknownMoveError("Invalid cell argument was provided", cell)

        # we now have a validly defined cell
        if self.drop:
            pass
        else:
            pass

        # check if cell has already been played
        if abs(v) > self._MOVE_BASE:
            raise DuplicateMoveError("The cell has already been played", cell)

        # we now have an empty cell
        self.moves_played[self.active_player] += 1
        sgn = -1 if self.active_player == 1 else 1 # player 0 is positive, player 1 negative
        self.board[t_cell] = sgn * (self.moves_played[self.active_player] + self._MOVE_BASE)
        
        # add to list of moves played and remove from unplayed list
        self.moves.append(Move(self.active_player, t_cell))
        self.unplayed.remove(t_cell)

        # check for win or tie
        if self.is_win(): 
            self.state = GameState.WIN_P2 if self.active_player else GameState.WIN_P1
        elif self.is_tie():
            self.state = GameState.TIE
        else:
            self.state = GameState.IN_PROGRESS

        # note that undo function can undo a win or tie
        self.active_moves += 1
        if self.active_moves == self.moves_per_turn:
            self.active_moves = 0
            self.active_player = int(not self.active_player)

        ##
        for l in self.scopes[t_cell]:
            print(self.calc_line_state(l))
        print(self.board)
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

        self.state = GameState.IN_PROGRESS

        if self.forfeited:
            self.forfeited = False
            return    

        if len(self.moves) == 0:
            return
        
        if self.active_moves == 0:
            self.active_moves = self.moves_per_turn - 1
            self.active_player = int(not self.active_player)
        else:
            self.active_moves -= 1

        self.moves_played[self.active_player] -= 1
        self.board[self.moves[-1][1]] = replace
        self.unplayed.append(self.moves[-1][1])
        del self.moves[-1]

    def forfeit(self) -> None:
        self.forfeited = True
        self.state = GameState.WIN_P1 if self.active_player else GameState.WIN_P2

    def calc_line_state(self, line: Line_np) -> LineState:
        P1_total_marks = sum(line > self._MOVE_BASE)
        
        P1_consecutive_marks = max((len(list(seq)) for val, seq in 
            groupby(line, key=lambda x: x > self._MOVE_BASE) if val), default = 0)
        
        P2_total_marks = sum(line < -self._MOVE_BASE)
        
        P2_consecutive_marks = max((len(list(seq)) for val, seq in 
            groupby(line, key=lambda x: x < -self._MOVE_BASE) if val), default = 0)
        
        ls = LineState(P1_total_marks, P1_consecutive_marks, P2_total_marks, P2_consecutive_marks)
        return ls