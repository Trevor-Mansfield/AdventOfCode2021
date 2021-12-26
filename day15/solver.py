from queue import PriorityQueue
from utils.parsers import parse_grid
from utils.grid import Grid


class ChitonMap(Grid):

    def __init__(self, expansion_factor=1):
        super().__init__(parse_grid("day15/input.txt"))
        if expansion_factor > 1:
            new_grid = [[] for _ in range(expansion_factor * self.rows)]
            wrap_risk = lambda v: ((v - 1) % 9) + 1
            for row_factor in range(expansion_factor):
                for row in range(self.rows):
                    for col_factor in range(expansion_factor):
                        for col in range(self.cols):
                            new_grid[row_factor * self.rows + row].append(
                                wrap_risk(self[row][col] + row_factor + col_factor)
                            )
            super().__init__(new_grid)
        self.risk_paths = self.make_mirror(None)

    def calc_risk_paths(self):
        risk_paths = PriorityQueue()
        risk_paths.put((-self[0][0], (0, 0)))
        while not risk_paths.empty():
            path_risk, (row, col) = risk_paths.get()
            if self.risk_paths[row][col] is None:
                total_path_risk = path_risk + self[row][col]
                self.risk_paths[row][col] = total_path_risk
                for ortho_row, ortho_col in self.ortho_locs(row, col):
                    if self.risk_paths[ortho_row][ortho_col] is None:
                        risk_paths.put((total_path_risk, (ortho_row, ortho_col)))
        

def solve1():
    chiton_map = ChitonMap()
    chiton_map.calc_risk_paths()
    print(chiton_map.risk_paths[chiton_map.rows - 1][chiton_map.cols - 1])

def solve2():
    chiton_map = ChitonMap(5)
    chiton_map.calc_risk_paths()
    print(chiton_map.risk_paths[chiton_map.rows - 1][chiton_map.cols - 1])
