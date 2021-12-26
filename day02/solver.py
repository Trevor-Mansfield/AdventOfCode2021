def solve1():
  depth = 0
  horizontal = 0
  with open("day2/input.txt", "r") as input1:
    for command in input1:
      direction, magnitude = command.split(" ")
      magnitude = int(magnitude)
      if direction == "forward":
        horizontal += magnitude
      elif direction == "up":
        depth -= magnitude
      elif direction == "down":
        depth += magnitude
      else:
        raise ValueError("Unknown direction: [%s]".format(direction))
  print(depth * horizontal)

def solve2():
  depth = 0
  horizontal = 0
  aim = 0
  with open("day2/input.txt", "r") as input2:
    for command in input2:
      direction, magnitude = command.split(" ")
      magnitude = int(magnitude)
      if direction == "forward":
        horizontal += magnitude
        depth += magnitude * aim
      elif direction == "up":
        aim -= magnitude
      elif direction == "down":
        aim += magnitude
      else:
        raise ValueError("Unknown direction: [%s]".format(direction))
  print(depth * horizontal)
      