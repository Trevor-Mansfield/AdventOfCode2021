def ortho_locs(row, col):
    offsets = [(-1,0), (0,-1), (0,1), (1,0)]
    for row_offset, col_offset in offsets:
        yield row + row_offset, col + col_offset

def adj_locs(row, col):
    offsets = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for row_offset, col_offset in offsets:
        yield row + row_offset, col + col_offset


class Grid:

    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def __getitem__(self, row):
        return self.grid[row]

    def __iter__(self):
        return self.grid.__iter__()

    def valid_loc(self, row, col):
        return row >= 0 and row < self.rows and col >= 0 and col < self.cols

    def ortho_locs(self, row, col):
        for ortho_row, ortho_col in ortho_locs(row, col):
            if self.valid_loc(ortho_row, ortho_col):
                yield ortho_row, ortho_col

    def adj_locs(self, row, col):
        for adj_row, adj_col in adj_locs(row, col):
            if self.valid_loc(adj_row, adj_col):
                yield adj_row, adj_col

    def make_mirror(self, value):
        return [[value for _ in row] for row in self.grid]


def build_grid(rows, cols, value):
    return Grid([[value for _ in range(cols)] for _ in range(rows)])

def print_grid(grid, formatter=lambda v: v):
    for row in grid:
        for col in row:
            print(formatter(col), end="")
        print("")
