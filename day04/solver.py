class Bingo:

  def __init__(self, lines):
    self.lines = lines
    self.board = [[False for _ in range(len(lines))] for _ in range(len(lines))]
    self.squares = {}
    for row, line in enumerate(lines):
      for col, square in enumerate(filter(None, line.strip().split(" "))):
        self.squares[square] = (row, col)

  def _check_row(self, row):
    for col in range(len(self.board)):
      if not self.board[row][col]:
        return False
    return True

  def _check_col(self, col):
    for row in range(len(self.board)):
      if not self.board[row][col]:
        return False
    return True

  def mark(self, square):
    square = self.squares.pop(square, None)
    if square:
      row, col = square
      self.board[row][col] = True
      return self._check_row(row) or self._check_col(col)

  def sum_remaining_squares(self):
    total = 0
    for square in self.squares.keys():
      total += int(square)
    return total
    

def solve1():
  with open("day4/input.txt", "r") as input1:
    lines = input1.readlines()
  numbers = lines[0]
  index = 1
  boards = []
  while index < len(lines):
    boards.append(Bingo(lines[index + 1 : index + 6]))
    index += 6
  for number in numbers.split(","):
    for board in boards:
      if board.mark(number):
        print(int(number) * board.sum_remaining_squares())
        return

def solve2():
  with open("day4/input.txt", "r") as input2:
    lines = input2.readlines()
  numbers = lines[0].split(",")
  index = 1
  boards = []
  while index < len(lines):
    boards.append(Bingo(lines[index + 1 : index + 6]))
    index += 6
  index = 0
  while len(boards) != 1:
    boards = [board for board in boards if not board.mark(numbers[index])]
    index += 1
  board = boards[0]
  while not board.mark(numbers[index]):
    index += 1
  print(int(numbers[index]) * board.sum_remaining_squares())
