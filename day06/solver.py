def simulate_fish(fish_freq, days):
  for _ in range(days):
    new_fish_freq = fish_freq[1:]
    new_fish_freq.append(fish_freq[0])
    new_fish_freq[6] += fish_freq[0]
    fish_freq = new_fish_freq
  return fish_freq

def count_fish(fish_freq):
  total_fish = 0
  for freq in fish_freq:
    total_fish += freq
  return total_fish

def solve_fish(days):
  fish_freq = [0 for _ in range(9)]
  with open("day6/input.txt", "r") as input1:
    for fish in input1.readline().split(","):
      fish_freq[int(fish)] += 1
  fish_freq = simulate_fish(fish_freq, days)
  print(count_fish(fish_freq))

def solve1():
  solve_fish(80)

def solve2():
  solve_fish(256)
