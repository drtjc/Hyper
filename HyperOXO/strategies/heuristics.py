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

    def move(self) -> None:     
        super().move() # calculates self.opponent_moves
        self._update_all_lines_scores()
        self._update_all_scopes_scores()    
        tc = self._top_cells()
        m = tc[randrange(len(tc))]
        self.ttt.move(m)

    ## HEURISTIC SCORING ###############################################
    def _update_line_score(self, idx: int) -> None:  
        # Score points for making moves that lead to possible wins or
        # stop possible losses. Score as follows:
        # W1=1, S2=10, W2=100, S3 = 1000, W3 = 10000, ... , Si = 10^(2i-3), Wi = 10^(2i-2), ...
        # where Wi means i own markers, and Si means i opponent markers 
        
        line_state = self.ttt.lines_states[idx]
        if line_state.Active_total_marks and line_state.Inactive_total_marks:
            # no score if not a potential winning or losing line
            self.lines_scores[idx] = 0            
        elif line_state.Inactive_total_marks: # possible losing line
            self.lines_scores[idx] = 10 ** (2 * (line_state.Inactive_total_marks + 1) - 3)
        else: # possible winning line
            self.lines_scores[idx] = 10 ** (2 * (line_state.Inactive_total_marks + 1) - 2)

    ## HELPER FUNCTIONS ################################################
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

    def _update_all_scopes_scores(self) -> None:
        for cell in self.ttt.scopes.keys():
            self._update_scope_score(cell)

    def _top_cells(self) -> List[Cell_coord]:
        unplayed_scores = {k: v for k, v in self.scopes_scores.items() if k in self.ttt.unplayed}
        max_score = max(unplayed_scores.values())
        return [k for k, v in unplayed_scores.items() if v == max_score]


