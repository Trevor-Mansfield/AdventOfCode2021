class Point:

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "{},{}".format(self.x, self.y)

  def __repr__(self):
    return self.__str__(self)


class Line:

  def __init__(self, x1, y1, x2, y2):
    self.p1 = Point(x1, y1)
    self.p2 = Point(x2, y2)
    
  def is_horizontal(self):
    return self.p1.y == self.p2.y

  def is_vertical(self):
    return self.p1.x == self.p2.x

  def is_diagonal(self):
    return self.p1.x != self.p2.x and self.p1.y != self.p2.y

  def __str__(self):
    return "{} -> {}".format(self.p1, self.p2)

  def __repr__(self):
    return self.__str__()


def fill_grid(grid, line):
  if line.is_horizontal():
    y = line.p1.y
    x1 = min(line.p1.x, line.p2.x)
    x2 = max(line.p1.x, line.p2.x)
    for x in range(x1, x2 + 1):
      grid[x][y] += 1
  elif line.is_vertical():
    x = line.p1.x
    y1 = min(line.p1.y, line.p2.y)
    y2 = max(line.p1.y, line.p2.y)
    for y in range(y1, y2 + 1):
      grid[x][y] += 1
  elif line.is_diagonal():
    x_incr = 1 if line.p1.x < line.p2.x else -1
    y_incr = 1 if line.p1.y < line.p2.y else -1
    x = line.p1.x
    y = line.p1.y
    while x != line.p2.x and y != line.p2.y:
      grid[x][y] += 1
      x += x_incr
      y += y_incr
    grid[x][y] += 1

def count_grid(grid, threshold):
  total = 0
  for row in grid:
    for element in row:
      if element >= threshold:
        total += 1
  return total

def read_file():
  def make_line(line):
    p1, p2 = line.split(" -> ")
    x1, y1 = p1.split(",")
    x2, y2 = p2.split(",")
    return Line(int(x1), int(y1), int(x2), int(y2))
  with open("day5/input.txt", "r") as input1:
    return [make_line(line) for line in input1]

def solve1():
  lines = filter(lambda l: not l.is_diagonal(), read_file())
  grid = [[0 for _ in range(1000)] for _ in range(1000)]
  for line in lines:
    fill_grid(grid, line)
  print(count_grid(grid, 2))      

def solve2():
  grid = [[0 for _ in range(1000)] for _ in range(1000)]
  for line in read_file():
    fill_grid(grid, line)
  print(count_grid(grid, 2))