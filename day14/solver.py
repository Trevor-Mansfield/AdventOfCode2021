from collections import defaultdict

from utils.parsers import line_splitter, scan_line_sections, no_op


class Polymerizer(object):

    def __init__(self):
        self.polymer_pairs = defaultdict(lambda: 0)
        self.polymer_counts = defaultdict(lambda: 0)
        self.rules = {}

        line_parsers = [
            no_op,
            line_splitter(" -> "),
        ]

        line_handler = self._add_polymer_pairs
        for line in scan_line_sections("day14/input.txt", line_parsers):
            if line:
                line_handler(line)
            else:
                line_handler = self._add_rule

    def _add_polymer_pairs(self, polymers):
        for index in range(len(polymers) - 1):
            self.polymer_pairs[polymers[index : index + 2]] += 1
            self.polymer_counts[polymers[index]] += 1
        self.polymer_counts[polymers[-1]] += 1
    
    def _add_rule(self, rule):
        polymer_pair, polymer = rule
        self.rules[polymer_pair] = polymer

    def polymerize(self):
        new_polymers = defaultdict(lambda: 0)
        for polymer_pair, count in self.polymer_pairs.items():
            new_polymer = self.rules.get(polymer_pair, None)
            if new_polymer:
                new_polymers[f"{polymer_pair[0]}{new_polymer}"] += count
                new_polymers[f"{new_polymer}{polymer_pair[1]}"] += count
                self.polymer_counts[new_polymer] += count
            else:
                new_polymers[polymer_pair] += count
        self.polymer_pairs = new_polymers


def solve1():
    polymerizer = Polymerizer()
    for _ in range(10):
        polymerizer.polymerize()
    polymer_counts = sorted(polymerizer.polymer_counts.values())
    print(polymer_counts[-1] - polymer_counts[0])

def solve2():
    polymerizer = Polymerizer()
    for _ in range(40):
        polymerizer.polymerize()
    polymer_counts = sorted(polymerizer.polymer_counts.values())
    print(polymer_counts[-1] - polymer_counts[0])
