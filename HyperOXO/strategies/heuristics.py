from strategy import Strategy, Cell_coord
from tictactoe import TicTacToe, LineState
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
        
        # calculate scope scores for an empty board
        self._calc_scopes_scores()        

    def move(self, cell: Optional[Cell_coord]) -> Union[Cell_coord, str]:     
        if cell is not None:
            # update scopes scores for previous move
            ### TO DO unless previous move was by same player - get rid of multiple moves??                
            self.prior_score = self.scopes_scores[cell]
            self.scopes_scores[cell] = -1
            self._calc_scope_score(cell)
            
        print(self.scopes_scores)
        tc = self._calc_top_cells()
        print(tc)
        m = tc[randrange(len(tc))]
        self.scopes_scores[m] = -1
        self.ttt.move(m)

        return m ## should protocol to be return nothing    


        ## for cell played, need to calculate all scope lines scores,
        # and then any cell with those lines in scope
        # basically, any cell (incl one played) and all those in scoped lines
        # need a line idx to cell coords

    def undo(self): ##does this really need to be double undo?? 
        prior_cell = self.ttt.moves_played[-1][1]
        self.scopes_scores[prior_cell] = self.prior_score
        super().undo()


    def _calc_line_score(self, idx: int) -> None:
        line_state = self.ttt.lines_states[idx]

        if self.ttt.active_player: # player 2
            me_total_marks = line_state.P2_total_marks
            you_total_marks = line_state.P1_total_marks
        else: # player 1
            me_total_marks = line_state.P1_total_marks
            you_total_marks = line_state.P2_total_marks
        
        if me_total_marks > 0 and you_total_marks > 0:
            self.lines_scores[idx] = 0            
        else:
            self.lines_scores[idx] = 0            

    def _calc_scope_score(self, cell: Cell_coord) -> None:
        self.scopes_scores[cell] = 0
        for idx in self.ttt.scopes[cell]:
            self._calc_line_score(idx)
            self.scopes_scores[cell] += self.lines_scores[idx]

    def _calc_scopes_scores(self) -> None:
        for cell in self.ttt.scopes.keys():
            self._calc_scope_score(cell)

    def _calc_top_cells(self) -> List[Cell_coord]:        
        unplayed_scores = {k: v for k, v in self.scopes_scores.items() if k in self.ttt.unplayed}
        max_score = max(unplayed_scores.values())
        return [k for k, v in unplayed_scores.items() if v == max_score]


# need to find all lines affected
    def _calc_affected_cells(self, cell: Cell_coord) -> List[Cell_coord]:
        a_cells: Set[Cell_coord] = set()
        return []
        
        # for each line in scope of cell 
        # add each cell in line

        # need to find all cells that belong to line
        
