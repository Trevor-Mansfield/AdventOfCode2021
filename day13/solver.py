from utils.parsers import scan_line_sections
from utils.grid import build_grid


class TransparentOrigami(object):

    def __init__(self):
        self.points = set()
        self.folds = []
        self.next_fold = 0

        line_parsers = [
            lambda l: l.split(","),
            lambda l: l[len("fold along "):].split("="),
        ]

        line_handler = self._add_point
        for line in scan_line_sections("day13/input.txt", line_parsers):
            if line:
                line_handler(*line)
            else:
                line_handler = self._add_fold
    
    def _add_point(self, x, y):
        self.points.add((int(x), int(y)))

    def _add_fold(self, axis, magnitude):
        self.folds.append((axis, int(magnitude)))

    def check_size(self):
        max_x = 0
        max_y = 0
        for x, y in self.points:
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return max_x + 1, max_y + 1

    def fold(self):
        axis, magnitude = self.folds[self.next_fold]
        folded_points = set()
        if 'x' == axis:
            for x, y in self.points:
                if x < magnitude:
                    folded_points.add((x, y))
                else:
                    folded_points.add((2 * magnitude - x, y))
        elif 'y' == axis:
            for x, y in self.points:
                if y < magnitude:
                    folded_points.add((x, y))
                else:
                    folded_points.add((x, 2 * magnitude - y))
        self.points = folded_points
        self.next_fold += 1

    def do_folds(self, num=None):
        for _ in range(num if num is not None else len(self.folds) - self.next_fold):
            self.fold()

    def convert_to_grid(self):
        rows, cols = self.check_size()
        grid = build_grid(rows, cols, '.')
        for x, y in self.points:
            grid[x][y] = '#'
        return grid


def solve1():
    puzzle = TransparentOrigami()
    puzzle.do_folds(1)
    print(len(puzzle.points))

def solve2():
    puzzle = TransparentOrigami()
    puzzle.do_folds()
    # Prints rotated 90 degrees counter clockwise
    for row in reversed(puzzle.convert_to_grid().grid):
        for col in row:
            print(col, end="")
        print("")
