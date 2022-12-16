import os
import json
from itertools import zip_longest
import pandas as pd
from copy import deepcopy
import re
import sys

SAMPLE_DATA = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

points_dict_ = {}
sensors = {}
beacons = set()


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def parse_numbers(string):
    pattern = re.compile(r"(\-?\d+)")
    for line in string.split("\n"):
        raw = map(int, pattern.findall(line))
        sx, sy, bx, by = raw
        distance = abs(sx - bx) + abs(sy - by)
        sensors[(sx, sy)] = distance
        beacons.add((bx, by))


def part1(line=10):
    x = []
    y = []
    for k, v in sensors.items():
        x.append(k[0] - v)
        x.append(k[0] + v)
        y.append(k[1] - v)
        y.append(k[1] + v)
    min_x, max_x, min_y, max_y = min(x), max(x), min(y), max(y)

    y = line
    vals = []
    ct = 0
    for coord in range(min_x, max_x + 1):
        if ct % 300000 == 0:
            print(".")
        ct += 1
        # print('coord: ', coord, line)
        if (coord, line) in beacons:
            # print('beacon found')
            continue
        is_available = []
        for k, v in sensors.items():
            if abs(k[0] - coord) + abs(k[1] - line) <= v:
                is_available.append(-1)
            else:
                is_available.append(1)
        vals.append(min(is_available))

    n = len(list(filter(lambda x: x == -1, vals)))
    return n


def perimeter(p, distance):
    x, y = p[0], p[1]
    # vals = set()
    for dx in range(distance + 2):
        dy = distance + 1 - dx
        # vals = vals.union(set( [(x + dx, y + dy), (x + dx, y - dy), (x - dx, y + dy), (x - dx, y - dy)]))
        # return vals
        yield x + dx, y + dy
        yield x + dx, y - dy
        yield x - dx, y + dy
        yield x - dx, y - dy


def part2(limit):
    # points = set()
    points = {}
    explored = set()
    for k, v in sensors.items():
        for i, j in perimeter(k, v):
            p = (i, j)
            points[p] = []
            is_available = 1
            if p in explored:
                continue
            for k, v in sensors.items():
                if abs(k[0] - p[0]) + abs(k[1] - p[1]) <= v:
                    is_available = -1
                    explored.add(p)
                points[p].append(is_available)
            #     if is_available == -1:
            #         continue
            if is_available == 1:
                return p


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__15.txt"))
    # input = get_input(None)
    parse_numbers(input)
    # print(sensors)
    # print(beacons)
    # print(part1(2000000)) # 5142231
    # print(part2(limit= 20))
    p2 = part2(limit=4000000)
    print(p2, p2[0] * 4000000 + p2[1])
