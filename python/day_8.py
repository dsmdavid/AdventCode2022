# I should have used custom classes for day 7.
# so I'm going to try to force myself to use some classes
# for other days, hopefully one day I'll get it right...


import os
from collections import defaultdict
import pprint
from copy import deepcopy
import sys

SAMPLE_DATA = """30373
25512
65332
33549
35390"""

SUMS = []


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


class ForestTree:
    def __init__(self, height, row_index, col_index, row, col) -> None:
        self.height = height
        self.row_index = row_index
        self.col_index = col_index
        self.row = row
        self.col = col
        self.is_visible = ""

    def return_trees_fragment(self, index, fragment, order):
        ct = 0
        test_fragment = fragment[0:index] if order == 1 else fragment[0:index][::-1]

        for i in test_fragment:
            if i < self.height:
                ct += 1
            elif i >= self.height:
                ct += 1
                return ct
            else:
                return ct
        return ct

    # def print_me(self):
    #     print(self.row_index, self.col_index, self.height, self.row, self.col)
    def max_visibility(self):
        n, e, s, w = 0, 0, 0, 0
        # borders
        if self.col_index == 0 or self.col_index == len(self.row) - 1:
            return 0
        elif self.row_index == 0 or self.row_index == len(self.col) - 1:
            return 0
        else:
            pass
        n = self.return_trees_fragment(self.row_index, self.col, order=-1)
        e = self.return_trees_fragment(self.col_index, self.row, order=-1)
        s = self.return_trees_fragment(
            len(self.row) - self.row_index - 1, self.col[::-1], order=-1
        )
        w = self.return_trees_fragment(
            len(self.col) - self.col_index - 1, self.row[::-1], order=-1
        )
        return n * e * s * w

    def set_visible(self):
        self.is_visible = self.is_tree_visible()

    def is_tree_visible(self):
        try:
            if self.col_index == 0 or self.col_index == len(self.row) - 1:
                return True
            elif self.row_index == 0 or self.row_index == len(self.col) - 1:
                return True
            elif max(self.row[0 : self.col_index]) < self.height:
                return True
            elif max(self.row[self.col_index + 1 :]) < self.height:
                return True
            elif max(self.col[0 : self.row_index]) < self.height:
                return True
            elif max(self.col[self.row_index + 1 :]) < self.height:
                return True
            else:
                return False
        except:
            print(self.__dict__)
            raise


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__8.txt"))
    # input = get_input(None)
    raw_rows = input.split("\n")
    rows = []
    columns = []
    for i, row in enumerate(raw_rows):
        rows.append(list(map(int, list(row))))
    for i in range(len(rows[0])):
        _ = [r[i] for r in rows]
        columns.append(_)
    forest_trees = []
    # create trees and set visibility from outside
    for i, row in enumerate(rows):
        for k, item in enumerate(row):
            FT = ForestTree(
                height=item, row_index=i, col_index=k, row=row, col=columns[k]
            )
            FT.set_visible()
            forest_trees.append(FT)

    ct = 0
    mx = 0
    for tree in forest_trees:
        mx = max(mx, tree.max_visibility())
        if tree.is_visible:
            ct += 1
    print("part1\t", ct, "\npart2\t", mx)
