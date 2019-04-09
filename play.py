from tictactoe import TicTacToe
from tictactoe import GameState
from tictactoe import Cell_coord
from strategy import Strategy
from typing import Optional, Tuple
import strategies as st  

def input_q(msg: str) -> str: 
    resp = input(msg)
    if resp.upper() in ["Q", "QUIT"]:
        raise SystemExit
    else:
        return resp

def create_board() -> TicTacToe:
    while True:
        print('')
        d = input_q("Number of dimensions: ")
        n = input_q("Size of board: ")

        try:
            ##TJC thread this in case takes a long time??
            return TicTacToe(int(d), int(n))
        except MemoryError:
            print("The board is too big to fit into available memory")
        except Exception as e:
            print("Could not create board. Please provide valid parameters")
            print(f'{e}')

def choose_names(ttt: TicTacToe) -> None:
    while True:
        print('')
        p1_name = input_q("Name of player 1: ")
        p2_name = input_q("Name of player 2: ")

        try:
            ttt.names = p1_name, p2_name
            return
        except Exception as e:
            print(f'{e}')

def choose_strategy(ttt: TicTacToe, p: int) -> Strategy:
    idx_cls = {}
    msg = f'Choose strategy for {str(ttt.names[p])}:\n'
    idx = 0
    for i, (k, v) in enumerate(st.strategies_cls.items(), 1):
        try:
            if v.validate(ttt.d, ttt.n, ttt.moves_per_turn, ttt.drop):
                idx += 1
                msg = msg + '  ' + str(idx) + '. ' + k + '\n'
                idx_cls[str(idx)] = v
        except:
            pass
    msg = msg + 'Selection: '
    
    while True:
        print('')
        s = input_q(msg)

        try:    
            return idx_cls[s](ttt)
        except Exception as e:
            print(f'Invalid selection: {e}')
    
def require_move_confirmation() -> bool: 
    print('')
    resp = input_q("Require player confirmation before next move? (y/n): ")
    return resp.upper() in ['TRUE', 'T', 'YES', 'Y']

def confirm_move(ttt: TicTacToe, s: Tuple[Strategy, Strategy]) -> None:
    while True:
        print('')
        resp = input_q("Move(m), undo(u), restart(r), new game(n) or quit(q): ")

        try:
            if resp.upper() in ['MOVE', 'M', '']:
                return
            elif resp.upper() in ['UNDO', 'U']:
                ttt.undo()
                ttt.display()
                return
            elif resp.upper() in ['RESTART', 'R']:
                restart(ttt, s, True)
                return
            elif resp.upper() in ['NEWGAME', 'N']:
                new_game()
                return
        except Exception as e:
            print(f'{e}')

def restart(ttt: TicTacToe, s: Tuple[Strategy, Strategy], req_move_conf: bool) -> None:
    s[0].reset()
    s[1].reset()  
    ttt.display()
    while ttt.state == GameState.IN_PROGRESS:
        
        print(f'\nActive player: {ttt.names[ttt.active_player]}')
        
        try:
            m: Optional[Cell_coord] = ttt.moves[-1][1]
        except IndexError:
            m = None

        s[ttt.active_player].move(m)        
        ttt.display()

        if req_move_conf:
            confirm_move(ttt, s)

    # game has finished without user resart or new game
    print("game over")

def new_game():
    ttt = create_board()
    choose_names(ttt)
    s = choose_strategy(ttt, 0), choose_strategy(ttt, 1)
    req_move_conf = require_move_confirmation()
    restart(ttt, s, req_move_conf)

def play_again():
    pass


if __name__ == "__main__":

    # Display welcome message and instructions
    msg = "Welcome to HyperOXO."
    print(msg)

    new_game()
