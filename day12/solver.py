from utils.parsers import scan_lines 
from utils.graph import Graph


class CaveMap(Graph):
    
    def __init__(self):
        super().__init__()
        for a, b in scan_lines("day12/input.txt", lambda l: l.split("-")):
            self.add_edge(a, b)
        # Prevent returning to start
        for start_edge in self.edges["start"]:
            self.edges[start_edge].remove("start")
        # Prevent leaving end
        self.edges["end"].clear()
    
    def is_small_cave(self, cave):
        return cave.islower()


class SingleVisitTracker(object):

    def __init__(self):
        self.caves = set()

    def can_enter(self, next_cave):
        return next_cave not in self.caves

    def add(self, next_cave):
        self.caves.add(next_cave)

    def remove(self, next_cave):
        self.caves.remove(next_cave)

class OneDoubleVisitTracker(object):

    def __init__(self):
        self.caves = set()
        self.double_cave = None

    def can_enter(self, next_cave):
        return self.double_cave is None or next_cave not in self.caves

    def add(self, next_cave):
        if next_cave in self.caves:
            self.double_cave = next_cave
        else:
            self.caves.add(next_cave)
    
    def remove(self, next_cave):
        if self.double_cave == next_cave:
            self.double_cave = None
        else:
            self.caves.remove(next_cave)

def count_paths(cave_map, cave, cave_tracker):
    if "end" == cave:
        return 1
    paths = 0
    for next_cave in cave_map[cave]:
        if cave_map.is_small_cave(next_cave):
            if cave_tracker.can_enter(next_cave):
                cave_tracker.add(next_cave)
                paths += count_paths(cave_map, next_cave, cave_tracker)
                cave_tracker.remove(next_cave)
        else:
            paths += count_paths(cave_map, next_cave, cave_tracker)
    return paths

def solve1():
    cave_map = CaveMap()
    print(count_paths(cave_map, "start", SingleVisitTracker()))

def solve2():
    cave_map = CaveMap()
    print(count_paths(cave_map, "start", OneDoubleVisitTracker()))
