from strategy import Strategy, Cell_coord
from tictactoe import TicTacToe, DuplicateMoveError, UnknownMoveError
from typing import Union, Optional, Tuple


class Interactive(Strategy):
    
    def move(self) -> None: 
        while True:
            resp = input('Enter move: ')
            if resp.upper() in ["Q", "QUIT", "F", "FORFEIT"]:
                self.ttt.forfeit()
                return 
            else:
                try:
                    self.ttt.move(resp)
                    return
                except DuplicateMoveError as e:
                    print(e)
                except UnknownMoveError as e:
                    print(e)
