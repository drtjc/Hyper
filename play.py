

if __name__ == "__main__":

    from tictactoe import TicTacToe
    from tictactoe import GameState
    import strategies as st  

    def input_q(msg: str): ## may not return
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

    def choose_strategy(ttt: TicTacToe, p: int): #return type is object bound by Strategy
        idx_cls = {}
        msg = f'Choose strategy for {str(ttt.names[p])}:\n'
        for i, (k, v) in enumerate(st.strategies_cls.items(), 1):
            msg = msg + '  ' + str(i) + '. ' + k + '\n'
            idx_cls[str(i)] = v
        msg = msg + 'Selection: '
        
        while True:
            print('')
            s = input_q(msg)

            try:    
                # should add strat to ttt
                return idx_cls[s](ttt)
            except Exception as e:
                print(f'Invalid selection: {e}')
        
    def require_move_confirmation() -> bool: 
        print('')
        res = input_q("Require player confirmation before next move? (y/n): ")
        return res.upper() in ['TRUE', 'T', 'YES', 'Y']

    def confirm_move(ttt: TicTacToe) -> None:
        while True:
            print('')
            res = input("Quit(q), undo(u) or move(m): ")

            # if quit, game is forfeit
            # if undo, 
            try:
                ttt.names = p1_name, p2_name
                return
            except Exception as e:
                print(f'{e}')


    # Display welcome message and instructions
    msg = "Welcome to HyperOXO."
    print(msg)

    # set up game
    ttt = create_board()
    choose_names(ttt)
    #st_1 = choose_strategy(ttt, 0)
    #st_2 = choose_strategy(ttt, 1)
    st = choose_strategy(ttt, 0), choose_strategy(ttt, 1)

    # ask if move confirmation is required
    req_move_conf = require_move_confirmation()

    ttt.display()
    print(f'\nActive player: {ttt.names[ttt.active_player]}')
    ttt.move(st[ttt.active_player].move(None))
    ttt.display()
    while ttt.state == GameState.IN_PROGRESS:
        # active player to move
        # if ask to move then allow quit, undo as well

        #if req_move_conf:
        #    confirm_move(ttt)
    
        print(f'\nActive player: {ttt.names[ttt.active_player]}')
        ttt.move(st[ttt.active_player].move(ttt.moves[-1]))
        #ttt.move(st_1.move((-1,-1,-1)))
        ttt.display()



    # use a co-routine to play?

    #print(st_1.shared)
    #ttt.strategies = st_1, st_2


    #print(ttt.strategies[0].move((9,)))
    #print(ttt.strategies[1].move((9,)))
    

    # choose

    #sel = input(msg)
    

 
   
    
    #t = strategies['Heuristics'](4,3)
    #print(t.d) 
    #print(type(strategies['Heuristics']))


##    dim = 4
##    size = 3
##    ttt = TicTacToe(dim, size, preload_scope = True)
    #ttt.p_names = ['Tom 2', 'Tom']
#    ttt.p_names = 'Tom 2', 'Tom'
    #print(ttt.p_names[0])
#    ttt.p_marks = "O", "X"

    #_, scopes = hc.structure_coord(dim, size)
    #print(scopes[(0,0)])

    #hc.get_lines_flat_coord(dim, size)

    #s0 = hc.get_scope_cell_coord(dim, size, (0,0))
    #print(s0)

    # print(ttt.memory())
    # print(ttt.state_str())

    # ttt.move('1111')
    # ttt.display(False)
    # print(ttt.state_str())

    # ttt.move('1211')
    # ttt.display(False)
    # print(ttt.state_str())

    # ttt.move('2222')
    # ttt.display(False)
    # print(ttt.state_str())
    
    # ttt.move('1312')
    # ttt.display(False)
    # print(ttt.state_str())

    # ttt.move('3333')
    # ttt.display(False)
    # print(ttt.state_str())



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
    



