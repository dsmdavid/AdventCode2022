from functools import reduce
import numpy as np
from math import inf as INFINITY
import os
import json
import networkx as nx
from itertools import zip_longest, cycle
from collections import deque
import pandas as pd
from copy import deepcopy
import re
import sys
import matplotlib.pyplot as plt

# from shapely.geometry import Polygon, LineString
# from shapely import union_all, box, intersection, difference

# from shapely.plotting import plot_polygon, plot_points, plot_line

SAMPLE_DATA = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""

ROCK_PATTERN = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""


def get_next_wind():
    for item in cycle(parsed_input):
        yield item


def get_next_rock():
    for item in cycle([parse_rocks(block) for block in ROCK_PATTERN.split("\n\n")]):
        yield item


def parse_rocks(block: str):
    output = []
    lines = block.split("\n")
    for line in lines:
        output.append(list(map(lambda x: 1 if x == "#" else 0, list(line))))

    return np.matrix(output)


class Rock:
    def __init__(self, matrix, starting_height, starting_pos, max_width=7):
        self.piece = matrix
        self.height = starting_height
        self.pos_x = starting_pos
        self.max_width = max_width
        self.is_settled = False
        self.matrix = None

    def pad(self, height_neg=0, height_pos=0, left=0, right=0):
        if self.matrix is None:
            self.matrix = np.pad(
                self.piece, ((height_neg, height_pos), (left, right)), mode="constant"
            )
        else:
            self.matrix = np.pad(
                self.matrix, ((height_neg, height_pos), (left, right)), mode="constant"
            )

    def position(self):
        """pad the matrix on the right and left"""
        left = self.pos_x
        right = max(self.max_width - self.piece.shape[1] - self.pos_x, 0)
        height_pos = height_neg = 0
        if self.height < 0:
            height_neg = abs(self.height)
        else:
            height_pos = self.height
        # print('here',height_neg)
        self.pad(height_neg=height_neg, height_pos=height_pos, left=left, right=right)

    def move_lateral(self):
        if self.is_settled:
            return
        # can it move laterally?
        # would it clash with the walls?
        self.next_w = next(w)
        nidx = [(x - self.next_w) % self.max_width for x in range(self.max_width)]
        # print(f'wind is {self.next_w}, new_nidx is {nidx}')

        if (self.pos_x + self.next_w) < 0:
            # print('no good_1', self.pos_x, self.next_w, self.piece.shape)
            # print(self.matrix)
            pass
        elif (self.pos_x + self.piece.shape[1] + self.next_w) > self.max_width:
            # print('no good_2', self.pos_x, self.next_w, self.piece.shape, self.max_width)
            # print(self.matrix)
            pass
        # would it clash with the fallen rocks?
        elif not collide(self.matrix[:, nidx], cave.matrix):
            self.pos_x += self.next_w
            self.matrix = self.matrix[:, nidx]

    def move_down(self):
        if self.is_settled:
            return
        # can it move down?
        # would it clash with the cave?
        nidx = [(x - 1) % self.matrix.shape[0] for x in range(self.matrix.shape[0])]
        if not collide(self.matrix[nidx, :], cave.matrix):
            self.matrix = self.matrix[nidx, :]
        else:
            self.is_settled = True

    def move(self):
        self.move_lateral()
        self.move_down()

    def settle(self):
        pass

    def collide(self, other):
        """true if there's a collision, false if not"""
        prod = np.multiply(self.matrix, other.matrix)
        return prod.any()


class RockGroup(Rock):
    pass

    def grow(self, other):
        self.matrix = self.matrix | other.matrix

    def readjust_matrix(self):
        reshape_mx = min(
            [i for i in range(self.matrix.shape[0]) if self.matrix[i, :].any()]
        )
        self.matrix = self.matrix[reshape_mx:, :]

    def get_baseline(self):
        reshape_mx = [
            i for i in range(0, self.matrix.shape[0]) if self.matrix[i, :].all()
        ]
        return reshape_mx

        # self.pad(height_neg=0, height_pos=0, left=0, right=0)
        # print(reshape_mx)


def collide(matrix_1, matrix_2):
    """true if there's a collision, false if not"""
    prod = np.multiply(matrix_1, matrix_2)
    return prod.any()


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def consec_repeat_starts(a, n):
    N = n - 1
    m = a[:-1] == a[1:]
    return np.flatnonzero(np.convolve(m, np.ones(N, dtype=int)) == N) - N + 1


if __name__ == "__main__":
    # input = get_input(os.path.join("./inputs", "2022__17.txt"))
    input = get_input(None)
    parsed_input = list(map(lambda x: -1 if x == "<" else 1, list(input)))
    # print(parsed_input)
    falling_rocks = cycle([parse_rocks(block) for block in ROCK_PATTERN.split("\n\n")])

    cave = RockGroup(
        np.matrix(np.ones(7, dtype=int)), starting_height=0, starting_pos=0, max_width=7
    )
    print("cave forming")
    print("positioning")
    cave.position()
    print(cave.__dict__)
    # cave.readjust_matrix()
    print(cave.matrix)
    ct = 0
    r = get_next_rock()
    w = get_next_wind()

    while ct < 10000:  # < 2022:
        cave.readjust_matrix()
        t = Rock(matrix=next(r), starting_height=0, starting_pos=2)
        t.position()
        ch = cave.matrix.shape[0] + 3
        th = t.matrix.shape[0] + 3
        t.pad(height_pos=ch)
        cave.pad(height_neg=th)
        while not t.is_settled:
            t.move()

        cave.grow(t)
        if [i for i in range(5) if cave.matrix[i, :].all()]:
            print("found!", ct, cave.matrix[0:5, :])
        # print('turn:\t',ct,'\n',cave.matrix)
        ct += 1
        if ct % 1000 == 0:
            print(ct)

    cave.readjust_matrix()
    print(cave.matrix.shape)
    # print(cave.matrix[0:5,:])
    print("part1\t:", cave.matrix.shape[0] - 1)

    # part 2:
    # -- is there a pattern that repeats?
    # len(wind) = 40 (test_data) // 10091 (actual data)
    # len(rock_pattern) = 5
    print(cave.matrix[0, :])
    print(cave.matrix[-1, :])
    print(cave.get_baseline())
    print(len(parsed_input))
    print(5, "rocks")

    # 1_000_000_000_000
    # 1_514_285_714_288
    primes = np.matrix([2, 3, 5, 7, 11, 13, 17])
    compare = np.multiply(cave.matrix, primes)
    compare_sum = np.sum(compare, axis=1)
    compare_flatten = compare[::-1].flatten()
    compare_pattern = np.squeeze(np.asarray(compare_flatten))

    print(compare_flatten)
    # print('2')
    # print(consec_repeat_starts(compare_pattern, 2))
    # print('5')
    # print(consec_repeat_starts(compare_pattern, 5))
    print("10")
    print(consec_repeat_starts(compare_pattern, 10))
