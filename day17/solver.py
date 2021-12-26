import math
import re

from utils.parsers import parse_line
    

class LaunchTarget(object):

    # The target is always expected to have min_x >= 0 and max_y <= 0

    def __init__(self):
        line = parse_line("day17/input.txt")
        regex_line = re.search(r"target area: x=(.*)\.\.(.*), y=(.*)\.\.(.*)", line)
        self.min_x = int(regex_line.group(1))
        self.max_x = int(regex_line.group(2))
        self.min_y = int(regex_line.group(3))
        self.max_y = int(regex_line.group(4))

    def in_target(self, x, y):
        return x >= self.min_x and x <= self.max_x and y >= self.min_y and y <=                 self.max_y

    # This is only a small optimization since any loop could also start from 0
    # instead of min_vx
    def min_vx(self):
        # The launcher can only shoot forward, so self.min_x is always positive.
        # The min_vx is the smallest value of vx such that
        # vx + (vx - 1) + (vx - 2) + ... >= self.min_x
        # Because vx goes to 0, this problem is equivalent to finding the smallest n
        # such that the sum of the first n integers is >= self.min_x
        # Thus we are solving for n such that (n * (n + 1)) / 2 >= self.min_x
        # Let n = math.ceil(x) so we can solve (x * (x + 1)) / 2 = self.min_x
        # x^2 + x = 2self.min_x -> x^2 + x - 2self.min_x = 0
        # Applying the quadratic formula,
        # -1 +/- sqrt(1 - 4 * 1 * (-2self.min_x))
        #             / 2 * 1
        # The positive root is therefore
        # x = -1 + sqrt(1 + 8 * self.min_x)
        return math.ceil((math.sqrt(1 + 8 * self.min_x) - 1) / 2)

    def max_vx(self):
        # Any vx larger than self.max_x is too far after t=1, so max_vx = self.max_x
        return self.max_x

    def min_vy(self):
        # Note min_vy is the largest negative vy, so when we shoot the probe straight
        # down any vy less than self.min_y is too deep after t=1, so min_vy = self.min_y
        return self.min_y

    def max_vy(self):
        # Recall that in parabolic motion, if we launch the probe up with vy,
        # it will have -vy when passing the same height it was launched from.
        # Note that due to updates happening as steps, there is an extra delay
        # at the apex we need to adjust for.
        #                                          vvvvvvv
        # e.x. for (y, vy) we have (0, 1), (1, 0), (1, -1), (0, -2)
        return -self.min_vy() - 1

    # Returns a tuple of the first and last time (inclusive) the probe will be
    # in the x bound of the target. Note that if due to drag reducing vx to 0,
    # the last time may be None to indicate it will remain in the target.
    def find_times_x_in_target(self, vx):
        x = 0
        t = 0
        first_t = None
        last_t = None
        while x <= self.max_x:
            if x >= self.min_x:
                first_t = first_t or t
                if vx == 0:
                    last_t = None
                    break
                last_t = t
            x += vx
            vx = max(vx - 1, 0)
            t += 1
        return first_t, last_t

    # Returns a tuple of the first and last time (inclusive) the probe will be
    # in the y bound of the target.
    def find_times_y_in_target(self, vy):
        y = 0
        t = 0
        first_t = None
        last_t = None
        while y >= self.min_y:
            if y <= self.max_y:
                first_t = first_t or t
                last_t = t
            y += vy
            vy -= 1
            t += 1
        return first_t, last_t

    def will_hit_target(self, vx, vy):
        x = 0
        y = 0
        while x <= self.max_x and y >= self.min_y:
            if self.in_target(x, y):
                return True
            x += vx
            y += vy
            vx = max(vx - 1, 0)
            vy -= 1
        return False

def solve1():
    target = LaunchTarget()
    
    # First, we'll find all the times we can find an x velocity for to be in the target.
    # For vx that stay in the target forever, we'll only save the earliest
    # time we could be in the target forever.
    vx_0_start = None
    # For all other vx, we'll just keep the set of times the probe in the target.
    discrete_times = set()
    for vx in range(target.min_vx(), target.max_vx()):
        min_t, max_t = target.find_times_x_in_target(vx)
        if min_t is None:
            continue
        if max_t is None:
            vx_0_start = min(vx_0_start or min_t, min_t)
        else:
            # Brute list the times
            for t in range(min_t, max_t + 1):
                discrete_times.add(t)

    # Now we'll try to find a y velocty to match one of our times.
    for vy in range(target.max_vy(), 0, -1):
        min_t, max_t = target.find_times_y_in_target(vy)
        if min_t is None:
            continue
        if vx_0_start is not None and min_t >= vx_0_start:
            # If the probe will be in the target at some time, we found the
            # largest vy we can use.
            highest_vy = vy
            break
        for t in range(min_t, max_t + 1):
            if t in discrete_times:
                highest_vy = vy
                break

    # Since our velocities are always integers, the highest y is just the sum of the
    # first highest_vy integers.
    print((highest_vy * (highest_vy + 1)) / 2)

def solve2():
    target = LaunchTarget()

    # To find every valid velocity, we'll grab the intervals every y velocity is in
    # the target. Since we are only counting pairs, we don't care what the actual
    # velocity is.
    vys = []
    for vy in range(target.min_vy(), target.max_vy() + 1):
        min_t, max_t = target.find_times_y_in_target(vy)
        if min_t is None:
            continue
        vys.append((min_t, max_t))

    # Now we will find every x velocity time and count the number of overlapping
    # intervals.
    num_velocity_pairs = 0
    for vx in range(target.min_vx(), target.max_vx() + 1):
        min_t, max_t = target.find_times_x_in_target(vx)
        if min_t is None:
            continue
        for min_vy_t, max_vy_t in vys:
            if max_vy_t < min_t:
                continue
            if max_t is not None and min_vy_t > max_t:
                continue
            num_velocity_pairs += 1
    
    print(num_velocity_pairs)
    