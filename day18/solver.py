import math
from copy import deepcopy

from utils.tree import TreeNode
from utils.slide_iter import SlideIter
from utils.parsers import scan_lines, parse_lines


class SnailNumber(TreeNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __add__(self, other):
        assert self.parent is None
        assert other.parent is None
        snail_num = SnailNumber(value=None, left=self, right=other)
        self.parent = snail_num
        other.parent = snail_num
        snail_num.reduce()
        return snail_num

    def try_explode(self, depth=0):
        depth += 1
        if self.value is not None:
            return False
        if self.left.try_explode(depth) or self.right.try_explode(depth):
            return True
        if depth > 4:
            assert self.left.value is not None and self.right.value is not None
            # Explode left value out
            left_value = self.left.value
            self.left = None
            left_iter = self.get_iter()
            left_iter.go_left_until(lambda v: v is not None)
            if left_iter:
                left_iter.target.value += left_value
            # Explode right value out
            right_value = self.right.value
            self.right = None
            right_iter = self.get_iter()
            right_iter.go_right_until(lambda v: v is not None)
            if right_iter:
                right_iter.target.value += right_value
            # Set value to 0
            self.value = 0
            return True
        return False

    def try_split(self):
        if self.value is not None:
            if self.value >= 10:
                self.left = SnailNumber(math.floor(self.value / 2), parent=self)
                self.right = SnailNumber(math.ceil(self.value / 2), parent=self)
                self.value = None
                return True
            return False
        return self.left.try_split() or self.right.try_split()

    def reduce(self):
        while self.try_explode() or self.try_split():
            pass

    def magnitude(self):
        if self.value is None:
            return self.left.magnitude() * 3 + self.right.magnitude() * 2
        return self.value

    @staticmethod
    def FromIter(snail_iter, parent=None, end_hint="]"):
        if snail_iter.peek() == "[":
            snail_num = SnailNumber(None, parent=parent)
            snail_iter.skip()
            snail_num.left = SnailNumber.FromIter(snail_iter, snail_num, ",")
            assert "," == snail_iter.get()
            snail_num.right = SnailNumber.FromIter(snail_iter, snail_num)
            assert "]" == snail_iter.get()
        else:
            snail_num = SnailNumber(int(snail_iter.get_to(end_hint)),
                                    parent=parent)
        return snail_num

    @staticmethod
    def FromStr(raw_snail_num):
        return SnailNumber.FromIter(SlideIter(raw_snail_num))

    def check_valid(self):
        assert (self.left is None) == (self.right is None)
        assert (self.value is None) != (self.left is None)
        if self.left:
            assert self.left.parent == self
            assert self.right.parent == self
            self.left.check_valid()
            self.right.check_valid()

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return f"[{str(self.left)},{str(self.right)}]"


def solve1():
    snail_sum = None
    for snail_number in scan_lines("day18/input.txt", line_parser=SnailNumber.FromStr):
        if snail_sum is None:
            snail_sum = snail_number
        else:
            snail_sum += snail_number
    print(snail_sum.magnitude())

def solve2():
    snail_nums = parse_lines("day18/input.txt", line_parser=SnailNumber.FromStr)
    max_magnitude = 0
    for i1, x in enumerate(snail_nums):
        for i2, y in enumerate(snail_nums):
            max_magnitude = max(max_magnitude, (deepcopy(x) + deepcopy(y)).magnitude())
            print(i1, i2)
    print(max_magnitude)