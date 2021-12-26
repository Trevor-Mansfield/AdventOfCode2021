def solve1():
  reading_size = 12
  bit_counts = [0 for _ in range(reading_size)]
  readings = 0
  with open("day3/input.txt", "r") as input1:
    for reading in input1:
      readings += 1
      for index in range(len(reading)):
        if reading[index] == "1":
          bit_counts[index] += 1
  threshold = readings / 2
  gamma_bits = ["1" if bit_count > threshold else "0" for bit_count in bit_counts]
  gamma_rate = int("".join(gamma_bits), 2)
  epsilon_bits = ["1" if bit_count < threshold else "0" for bit_count in bit_counts]
  epsilon_rate = int("".join(epsilon_bits), 2)
  print(gamma_rate * epsilon_rate)

def filter_by_bits(readings, bit_filter):
  index = 0
  while len(readings) != 1:
    bit_count = 0
    for reading in readings:
      if reading[index] == "1":
        bit_count += 1
    filter_bit = bit_filter(bit_count, len(readings))
    readings = [reading for reading in readings if reading[index] == filter_bit]
    index += 1
  return readings[0]

def solve2():
  with open("day3/input.txt", "r") as input2:
    readings = input2.readlines()

  def filter_oxygen_bit(bit_count, num_readings):
    return "1" if bit_count >= num_readings / 2 else "0"

  oxygen_reading = int(filter_by_bits(readings.copy(), filter_oxygen_bit), 2)
  
  def filter_co2_bit(bit_count, num_readings):
    return "0" if bit_count >= num_readings / 2 else "1"

  co2_reading = int(filter_by_bits(readings.copy(), filter_co2_bit), 2)

  print(oxygen_reading * co2_reading)