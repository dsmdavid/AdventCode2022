import os
import json
from itertools import zip_longest
import pandas as pd
from copy import deepcopy
import re
import sys
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
from shapely import union_all, box, intersection, difference

# from figures import SIZE, BLUE, GRAY, RED, set_limits
from shapely.plotting import plot_polygon, plot_points, plot_line

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

sensors = {}


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


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__15.txt"))

    # input = get_input(None)
    parse_numbers(input)
    fig, axs = plt.subplots(1, 2, layout="constrained", figsize=(5.5, 3.5))
    ax = axs[0]
    ax_b = axs[1]

    #  Create polygons
    polygons = []
    for k, v in sensors.items():
        ext = [
            (k[0], k[1] - v),
            (k[0] - v, k[1]),
            (k[0], k[1] + v),
            (k[0] + v, k[1]),
            (k[0], k[1] - v),
        ]
        polygon = Polygon(ext)
        polygons.append(polygon)

    # Single polygon containing all
    combined = union_all(polygons)
    bounds = combined.bounds
    bounding_box_i = box(*bounds)  # minx, miny, maxx, maxy

    #  Part I:
    target_line = 2000000
    # target_line = 10
    line = LineString([[bounds[0], target_line], [bounds[2], target_line]])
    occupied = intersection(combined, line)
    print("line_length", line.length, "occupied\t", occupied.length)

    # part_2:
    # target_box = 20
    target_box = 4000000
    bounding_box = box(0, 0, target_box, target_box)
    diff = difference(bounding_box, combined)
    bounds = diff.bounds
    x = (bounds[2] + bounds[0]) / 2
    y = (bounds[3] + bounds[1]) / 2
    ans = 4000000 * x + y

    print("part_2/t", int(ans))

    # Plot
    plot_polygon(combined, ax=ax, add_points=False, color="blue")
    plot_polygon(bounding_box_i, ax=ax, add_points=True, color="gray")
    plot_line(line, ax=ax, add_points=False, color="green")
    plot_line(occupied, ax=ax, add_points=False, color="firebrick")

    plot_polygon(combined, ax=ax_b, add_points=False, color="blue")
    plot_polygon(bounding_box, ax=ax_b, add_points=False, color="grey")
    plot_polygon(diff, ax=ax_b, color="firebrick")
    plt.show()
