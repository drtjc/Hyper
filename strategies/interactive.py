import hypercube as hc
from strategy import Strategy
from tictactoe import TicTacToe, DuplicateMoveError, UnknownMoveError
from typing import Union, Optional

Cell_coord = hc.Cell_coord


class Interactive(Strategy):
    
    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]: 
        while True:
            resp = input('Enter move: ')
            if resp.upper() in ["Q", "QUIT", "F", "FORFEIT"]:
                self.ttt.forfeit()
                return str(-1) 

            try:
                self.ttt.move(resp)
                return resp
            except DuplicateMoveError as e:
                print(e)
            except UnknownMoveError as e:
                print(e)
