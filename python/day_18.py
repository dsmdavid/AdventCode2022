from functools import reduce
from math import inf as INFINITY
import os
import json
import networkx as nx
from itertools import zip_longest
from collections import deque
import pandas as pd
from copy import deepcopy
import re
import sys
import matplotlib.pyplot as plt

# from shapely.geometry import Polygon, LineString
# from shapely import union_all, box, intersection, difference

# from shapely.plotting import plot_polygon, plot_points, plot_line

SAMPLE_DATA = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def parse_input(string):
    pattern = re.compile(r"(\d+)")

    cubes = {}
    for line in string.split("\n"):
        raw = pattern.findall(line)
        tp = tuple(map(int, raw))
        cubes[tp] = {"potential_neighbours": find_potential_neighbours(tp)}
    return cubes


def find_potential_neighbours(tuple_xyz):
    """given a xyz coordinates, returns the 6 possible neighbours"""

    x, y, z = tuple_xyz
    x1 = tuple([x + 1, y, z])
    x2 = tuple([x - 1, y, z])
    y1 = tuple([x, y + 1, z])
    y2 = tuple([x, y - 1, z])
    z1 = tuple([x, y, z + 1])
    z2 = tuple([x, y, z - 1])

    return set([x1, x2, y1, y2, z1, z2])


def find_actual_neighbours(tuple_xyz, cube_dict):
    neighbours = []
    for key in cube_dict.keys():
        if key in cube_dict[tuple_xyz]["potential_neighbours"]:
            neighbours.append(key)

    cube_dict[tuple_xyz]["actual_neighbours"] = set(neighbours)


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__18.txt"))
    # input = get_input(None)
    cubes = parse_input(input)

    surface = 0
    # actual neighbours:
    for item in cubes.keys():
        find_actual_neighbours(item, cubes)
        cubes[item]["surface"] = 6 - len(cubes[item]["actual_neighbours"])
        surface += cubes[item]["surface"]
    print(cubes)
    print(surface)
