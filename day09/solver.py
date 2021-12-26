from utils.parsers import parse_grid
from utils.grid import Grid


class HeightMap(Grid):

    def __init__(self):
        super().__init__(parse_grid("day09/input.txt"))
        self.basins = self.make_mirror(0)
        self.basin_sizes = {}
        self.next_basin = 1

    def is_low_point(self, row, col):
        height = self[row][col]
        for ortho_row, ortho_col in self.ortho_locs(row, col):
            if self[ortho_row][ortho_col] <= height:
                return False
        return True

    def possible_basin(self, row, col):
        return self[row][col] < 9 and self.basins[row][col] == 0

    def load_basin(self, start_row, start_col):
        if not self.possible_basin(start_row, start_col):
            return
        basin_checks = {(start_row, start_col)}
        basin = self.next_basin
        self.basin_sizes[basin] = 0
        while basin_checks:
            row, col = basin_checks.pop()
            height = self[row][col]
            self.basins[row][col] = basin
            self.basin_sizes[basin] += 1
            for ortho_row, ortho_col in self.ortho_locs(row, col):
                if self.possible_basin(ortho_row, ortho_col) and height < self[ortho_row][ortho_col]:
                    basin_checks.add((ortho_row, ortho_col))
        self.next_basin += 1


def solve1():
    height_map = HeightMap()
    risk_total = 0
    for row in range(height_map.rows):
        for col in range(height_map.cols):
            if height_map.is_low_point(row, col):
                risk_total += height_map[row][col] + 1
    print(risk_total)

def solve2():
    height_map = HeightMap()
    for row in range(height_map.rows):
        for col in range(height_map.cols):
            if height_map.is_low_point(row, col):
                height_map.load_basin(row, col)
    total = 1
    for basin_size in sorted(list(height_map.basin_sizes.values()), reverse=True)[:3]:
        total *= basin_size
    print(total)
