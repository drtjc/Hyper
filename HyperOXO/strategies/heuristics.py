from strategy import Strategy, Cell_coord
from tictactoe import TicTacToe
from random import randrange
from typing import Union, Optional, List, DefaultDict, Dict, Set


class Heuristics(Strategy):

    def __init__(self, ttt: TicTacToe) -> None:
        super().__init__(ttt)
        self.lines_scores: Dict = {}
        self.scopes_scores: DefaultDict[Cell_coord, int] = DefaultDict(int)
        self.reset()

    def reset(self) -> None:
        
        self.first_move = True
        #self.prior_score = 0 # score for prior move            
        # calculate scores for an empty board
        #self._update_all_lines_scores() ## but who is active
        #self._update_all_scopes_scores()    

    
    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]:     


        if cell is not None and not self.first_move:
            #self.prior_score = self.scopes_scores[cell]
            
            # update scopes scores for previous move
            ### TO DO unless previous move was by same player - get rid of multiple moves??                
            #self._update_lines_scores(cell)
            #self._update_connected_scopes_scores(cell)

            self._update_all_lines_scores()
            self._update_all_scopes_scores()    



        elif self.first_move: 
            self.first = False
            
            # if other player played first then their move will be in calculation
            self._update_all_lines_scores()
            self._update_all_scopes_scores()    

        # Note: not possible to not be first move with cell is None


        print(self.lines_scores)
        print(self.scopes_scores)

        # need score for all unplayed cells

        tc = self._top_cells()

        print(tc)
        m = tc[randrange(len(tc))]

        # doesn't the move also change the scores


        self.ttt.move(m)

        return m ## should protocol to be return nothing    


    def undo(self): ##does this really need to be double undo?? 
        #prior_cell = self.ttt.moves_played[-1][1]
        #self.scopes_scores[prior_cell] = self.prior_score
        #super().undo()
        pass



    def _update_line_score(self, idx: int) -> None:
        line_state = self.ttt.lines_states[idx]

        if line_state.Active_total_marks and line_state.Inactive_total_marks:
            # no score if not a potential winning or losing line
            self.lines_scores[idx] = 0            
        elif line_state.Inactive_total_marks:
            # possible losing line
            self.lines_scores[idx] = 2 ** (2 * (line_state.Inactive_total_marks + 1) - 3)
        else:
            # possible winning line
            self.lines_scores[idx] = 2 ** (2 * (line_state.Inactive_total_marks + 1) - 2)


        #vW1 = 1, S2=2, W2=4, S3 = 8, W3 = 16, ... , Si = 2^(2i-3), Wi = 2^(2i-2), ... 


    def _update_lines_scores(self, cell: Cell_coord) -> None:
        for idx in self.ttt.scopes[cell]:
            self._update_line_score(idx)

    def _update_all_lines_scores(self) -> None:
        for idx in self.ttt.lines.keys():
            self._update_line_score(idx)

    def _update_scope_score(self, cell: Cell_coord) -> None:
        self.scopes_scores[cell] = 0
        for idx in self.ttt.scopes[cell]:
            self.scopes_scores[cell] += self.lines_scores[idx]

    def _update_connected_scopes_scores(self, cell: Cell_coord) -> None:
        for cc in self.ttt.connected_cells[cell]:
            self._update_scope_score(cc)

    def _update_all_scopes_scores(self) -> None:
        for cell in self.ttt.scopes.keys():
            self._update_scope_score(cell)

    def _top_cells(self) -> List[Cell_coord]:

        ## need

        unplayed_scores = {k: v for k, v in self.scopes_scores.items() if k in self.ttt.unplayed}
        max_score = max(unplayed_scores.values())
        return [k for k, v in unplayed_scores.items() if v == max_score]


