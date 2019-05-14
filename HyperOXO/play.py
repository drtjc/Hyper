from tictactoe import TicTacToe, GameState, Cell_coord
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
        mt = input_q("Number of moves per turn: ")
        m = input_q("Misere (win if opponent gets n in a row): ")
        
        try:
            return TicTacToe(int(d), int(n), int(mt), m[0].upper() in ['Y', 'T'])
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
            if v.validate(ttt.d, ttt.n, ttt.moves_per_turn, True):
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


def restart(ttt: TicTacToe, s: Tuple[Strategy, Strategy]) -> None:
    s[0].reset()
    s[1].reset()
    ttt.reset()  
    ttt.display()
    while ttt.state == GameState.IN_PROGRESS:     
        print(f'\nActive player: {ttt.names[ttt.active_player]}')
        s[ttt.active_player].move()
        ttt.display()

    # game has finished without user restart or new game
    print(ttt.state_str())
    play_again(ttt, s)


def new_game():
    ttt = create_board()
    choose_names(ttt)
    s = choose_strategy(ttt, 0), choose_strategy(ttt, 1)
    restart(ttt, s)


def play_again(ttt: TicTacToe, s: Tuple[Strategy, Strategy]) -> None:
    while True:
        print('')
        resp = input_q("Replay(r), swap(s), new game(n) or quit(q): ")

        try:
            if resp.upper() in ['REPLAY', 'R']:
                restart(ttt, s)
                return
            if resp.upper() in ['SWAP', 'S']:
                ttt.names = ttt.names[1], ttt.names[0]
                s = s[1], s[0]
                restart(ttt, s)
                return
            elif resp.upper() in ['NEWGAME', 'N']:
                new_game()
                return
        except Exception as e:
            print(f'{e}')    


if __name__ == "__main__":

    # Display welcome message and instructions
    msg = "Welcome to HyperOXO."
    print(msg)

    new_game()

