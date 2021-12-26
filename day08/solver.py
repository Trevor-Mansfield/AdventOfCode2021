def update_mapping(map, input_chars, output_chars):
    for char, map_set in map.items():
        if char in input_chars:
            map_set.intersection_update(output_chars)
        else:
            map_set.difference_update(output_chars)
            
def flatten_set(set):
    return "".join(sorted(list(set)))

def map_set(set, mapping):
    return {mapping[c] for c in set}
    
display_lines = {
    0: {'a', 'b', 'c', 'e', 'f', 'g'},
    1: {'c', 'f'},
    2: {'a', 'c', 'd', 'e', 'g'},
    3: {'a', 'c', 'd', 'f', 'g'},
    4: {'b', 'c', 'd', 'f'},
    5: {'a', 'b', 'd', 'f', 'g'},
    6: {'a', 'b', 'd', 'e', 'f', 'g'},
    7: {'a', 'c', 'f'},
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    9: {'a', 'b', 'c', 'd', 'f', 'g'},
}

display_lookup = {flatten_set(value): key for key,value in display_lines.items()}

def decode_number(line):
    line_parts = line.split(" | ")

    display_map = {c: set("abcdefg") for c in "abcdefg"}

    signal_patterns = sorted([set(lp) for lp in line_parts[0].split(" ")], key=lambda s: len(s))

    cf = signal_patterns[0]
    update_mapping(display_map, cf, set("cf"))

    a = signal_patterns[1].difference(signal_patterns[0])
    update_mapping(display_map, a, set("a"))

    # 2, 3, 5 common segments
    adg = signal_patterns[3].intersection(signal_patterns[4], signal_patterns[5])
    update_mapping(display_map, adg, set("adg"))

    # 0, 6, 9 common segments
    abfg = signal_patterns[6].intersection(signal_patterns[7], signal_patterns[8])
    update_mapping(display_map, abfg, set("abfg"))

    display_map = {c: m.pop() for c, m in display_map.items()}

    multiplier = 1000
    number = 0
    for output_value in line_parts[1].split(" "):
        digit = display_lookup[flatten_set(map_set(output_value, display_map))]
        number += digit * multiplier
        multiplier /= 10
    return number

def solve1():
    num_easy_digits = 0
    with open("day8/input.txt", "r") as input_file:
        for line in input_file:
            for output_value in line.strip().split(" | ")[1]:
                if len(output_value) in (2, 4, 3, 7):
                    num_easy_digits += 1
    print(num_easy_digits)

def solve2():
    total = 0
    with open("day8/input.txt", "r") as input_file:
        for line in input_file:
            total += decode_number(line.strip())
    print(total)       
