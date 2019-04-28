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
        self.prior_score = 0 # score for prior move            
        # calculate scores for an empty board
        self._update_all_lines_scores()
        self._update_all_scopes_scores()    
    
    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]:     


        if cell is not None:
            self.prior_score = self.scopes_scores[cell]
            
            # update scopes scores for previous move
            ### TO DO unless previous move was by same player - get rid of multiple moves??                
            self._update_lines_scores(cell)
            self._update_connected_scopes_scores(cell)

        print(self.scopes_scores)

        tc = self._top_cells()

        print(tc)
        m = tc[randrange(len(tc))]
        self.ttt.move(m)

        return m ## should protocol to be return nothing    


    def undo(self): ##does this really need to be double undo?? 
        #prior_cell = self.ttt.moves_played[-1][1]
        #self.scopes_scores[prior_cell] = self.prior_score
        #super().undo()
        pass



    def _update_line_score(self, idx: int) -> None:
        line_state = self.ttt.lines_states[idx]

        if line_state.Inactive_total_marks > 0:
            self.lines_scores[idx] = 0            
        else:
            self.lines_scores[idx] = 1            




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
        unplayed_scores = {k: v for k, v in self.scopes_scores.items() if k in self.ttt.unplayed}
        max_score = max(unplayed_scores.values())
        return [k for k, v in unplayed_scores.items() if v == max_score]


