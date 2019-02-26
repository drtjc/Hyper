import hypercube as hc
from strategy import Strategy

Cell_coord = hc.Cell_coord


class Random(Strategy):
    
    def __init__(self, shared: bool, d: int, n: int, moves_per_turn = 1, drop = False) -> None:
        self.shared = shared

    @property
    def shared(self):
        return self._shared

    @shared.setter
    def shared(self, val):
        self._shared = val

    def move(self, cell: Cell_coord) -> Cell_coord:
        return (2,)

    def undo(self):
        pass
