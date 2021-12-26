def count_increases(depths, window_size=1):
  increases = 0
  for index in range(window_size, len(depths)):
    if depths[index] > depths[index - window_size]:
      increases += 1
  return increases

def solve1():
  with open("day1/input.txt", "r") as input1:
    depths = [int(depth) for depth in input1.readlines()]
    print(count_increases(depths, 1))

def solve2():
  with open("day1/input.txt", "r") as input2:
    depths = [int(depth) for depth in input2.readlines()]
    print(count_increases(depths, 3))
