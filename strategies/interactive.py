import hypercube as hc
from strategy import dec_strategy, Strategy

Cell_coord = hc.Cell_coord

@dec_strategy
class Interactive(Strategy):
    
    def __init__(self, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        super().__init__(d, n, moves_per_turn, drop)

    def move(self, cell: Cell_coord) -> Cell_coord:
        return cell

    def undo(self, cell: Cell_coord) -> Cell_coord:
        return cell
