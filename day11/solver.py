from utils.parsers import parse_grid
from utils.grid import Grid
        

class OctopusMap(Grid):

    def __init__(self):
        super().__init__(parse_grid("day11/input.txt"))

    def step(self, row, col):
        self[row][col] += 1
        if 10 == self[row][col]:
            for adj_row, adj_col in self.adj_locs(row, col):
                self.step(adj_row, adj_col)

    def step_all(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.step(row, col)
        flashes = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self[row][col] > 9:
                    self[row][col] = 0
                    flashes += 1
        return flashes

        
def solve1():
    octopus_map = OctopusMap()
    flashes = 0
    for _ in range(100):
        flashes += octopus_map.step_all()
    print(flashes)

def solve2():
    octopus_map = OctopusMap()
    octopi = octopus_map.rows * octopus_map.cols
    step = 1
    while octopus_map.step_all() != octopi:
        step += 1
    print(step)