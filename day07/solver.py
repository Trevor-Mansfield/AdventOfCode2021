import math

def get_crab_indexes():
  with open("day7/input.txt", "r") as input_file:
    return [int(num) for num in input_file.readline().split(",")]

def solve1():
  crab_indexes = get_crab_indexes()
  # With a linear fuel cost, the fuel cost for each crab moving can be modeled
  # by |x-index|. Thus the cheapest index for all crabs will be the median of every
  # crab's index.
  crab_indexes.sort()
  align_index = crab_indexes[math.floor(len(crab_indexes)/2)]
  fuel_cost = 0
  for index in crab_indexes:
    fuel_cost += abs(index - align_index)
  print(fuel_cost)

def fuel_cost_2(index, align_index):
  diff = abs(index - align_index)
  return 0.5 * (diff + 1) * diff

def solve2():
  crab_indexes = get_crab_indexes()
  # Fuel cost = (1/2)(x-a+1)(x-a)
  # The cheapest index for all crabs will be at the average of every crab's index.
  align_index = sum(crab_indexes) / len(crab_indexes)
  print(align_index)
  align_index_floor = math.floor(align_index)
  align_index_ceil = math.ceil(align_index)
  fuel_cost_floor = 0
  fuel_cost_ceil = 0
  for index in crab_indexes:
    fuel_cost_floor += fuel_cost_2(index, align_index_floor)
    fuel_cost_ceil += fuel_cost_2(index, align_index_ceil)
    print(fuel_cost_2(index, align_index_ceil))
  print(min(fuel_cost_floor, fuel_cost_ceil))
