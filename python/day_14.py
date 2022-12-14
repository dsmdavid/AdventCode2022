import os
import json
from itertools import zip_longest
import pandas as pd
from copy import deepcopy
import sys

SAMPLE_DATA = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

points_dict_ = {}


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


class RockPath:
    def __init__(self, input: str):
        self.input = input
        self.points = []

    def parse_input(self):
        # 498,4 -> 498,6 -> 496,6
        current_point = next_point = None
        for i, item in enumerate(self.input.split("->")):
            point = tuple(map(int, item.strip().split(",")))
            self.points.append(point)
            current_point = point
            self.get_intermediate(current_point, next_point)
            next_point = point

    def get_intermediate(self, p1=None, p2=None):
        if p1 is None or p2 is None:
            return
        pmax, pmix = max(p1[0], p2[0]), min(p1[0], p2[0])
        pmay, pmiy = max(p1[1], p2[1]), min(p1[1], p2[1])
        if pmax == pmix:
            for i in range(pmiy, pmay + 1):
                self.points.append((p1[0], i))
        elif pmay == pmiy:
            for i in range(pmix, pmax + 1):
                self.points.append((i, p1[1]))
        else:
            print("unexcpected points")
            raise

    def update_map(self):
        for point in set(self.points):
            points_dict_[point] = "#"


def get_max_min(point_dict):
    min_x = max_x = min_y = max_y = 0
    x = []
    y = []
    for k in point_dict.keys():
        x.append(k[0])
        y.append(k[1])

    min_x, max_x, min_y, max_y = min(x), max(x), min(y), max(y)
    return min_x, max_x, min_y, max_y


def create_map(point_dict):
    # snow falling from...
    point_dict[(500, 0)] = "S"
    min_x, max_x, min_y, max_y = get_max_min(point_dict)
    # populate all points inside the map
    for xi in range(min_x, max_x + 1):
        for yi in range(min_y, max_y + 1):
            point_dict[(xi, yi)] = point_dict.get((xi, yi), ".")


def plot_map(point_dict, min_x, max_x, min_y, max_y):
    rows = []
    for row in range(min_y, max_y + 1):
        r = []
        for col in range(min_x, max_x + 1):
            r.append(point_dict[(col, row)])
        rows.append("".join(r))
    print("\n".join(rows))


def play_snow_ball(ball_position, max_y, points_dict_={}, part=1):
    """returns the position of the ball that starts in a given ball_position
    for part = 1 the arena is limited, for part = 2 the arena is only
    limited on the floor
    """
    if ball_position == (-999, -999) and part == 1:
        # we're already in the abyss. Unexpectedly.
        # print("oh, no, we're in the abyss")
        return (-999, -999)
    elif ball_position[1] == max_y and part == 2:
        points_dict_[(ball_position[0], max_y)] = "."
        return ball_position
    elif points_dict_.get((ball_position[0], ball_position[1] + 1), "X") == ".":
        return play_snow_ball(
            (ball_position[0], ball_position[1] + 1),
            max_y=max_y,
            points_dict_=points_dict_,
            part=part,
        )
    elif points_dict_.get((ball_position[0], ball_position[1] + 1), "X") == "X":
        if ball_position[1] <= max_y - 1 and part == 2:
            points_dict_[(ball_position[0], ball_position[1] + 1)] = "."
            return play_snow_ball(
                (ball_position[0], ball_position[1] + 1),
                max_y=max_y,
                points_dict_=points_dict_,
                part=part,
            )
        return (-999, -999)
    elif points_dict_.get((ball_position[0] - 1, ball_position[1] + 1), "X") == ".":
        return play_snow_ball(
            (ball_position[0] - 1, ball_position[1] + 1),
            max_y=max_y,
            points_dict_=points_dict_,
            part=part,
        )
    elif points_dict_.get((ball_position[0] - 1, ball_position[1] + 1), "X") == "X":
        if ball_position[1] <= max_y - 1 and part == 2:
            points_dict_[(ball_position[0] - 1, ball_position[1] + 1)] = "."
            return play_snow_ball(
                (ball_position[0] - 1, ball_position[1] + 1),
                max_y=max_y,
                points_dict_=points_dict_,
                part=part,
            )
        return (-999, -999)
    elif points_dict_.get((ball_position[0] + 1, ball_position[1] + 1), "X") == ".":
        return play_snow_ball(
            (ball_position[0] + 1, ball_position[1] + 1),
            max_y=max_y,
            points_dict_=points_dict_,
            part=part,
        )
    elif points_dict_.get((ball_position[0] + 1, ball_position[1] + 1), "X") == "X":
        if ball_position[1] <= max_y - 1 and part == 2:
            points_dict_[(ball_position[0] + 1, ball_position[1] + 1)] = "."
            return play_snow_ball(
                (ball_position[0] + 1, ball_position[1] + 1),
                max_y=max_y,
                points_dict_=points_dict_,
                part=part,
            )
        return (-999, -999)
    else:
        return ball_position


def create_df(points_dict, round):
    df = pd.DataFrame.from_dict(
        orient="index",
        data=points_dict,
    )

    df["col"] = df.index
    df["row"] = df.index
    df["col"] = df["col"].apply(lambda x: x[0])
    df["row"] = df["row"].apply(lambda x: x[1])
    df["round"] = round
    return df


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__14.txt"))
    # input = get_input(None)
    for i, block in enumerate(input.split("\n")):
        # 498,4 -> 498,6 -> 496,6
        t = RockPath(block)
        t.parse_input()
        t.update_map()

    create_map(points_dict_)
    part_ii_points = deepcopy(points_dict_)
    # end of start

    # for viz
    # dfs = []
    # dfs.append(create_df(points_dict_,0))
    # plot_map(points_dict_, *get_max_min(points_dict_))


    print("--- ball --- ")
    flag = True
    ct = 0
    while flag:
        ct += 1
        end = play_snow_ball((500, 0), max_y=100, points_dict_=points_dict_, part=1)
        if end == (-999, -999):
            print("ending\t", ct)
            flag = False
            break
        if points_dict_[end] == ".":
            points_dict_[end] = "O"
        else:
            flag = False
        # for viz
        # dfs.append(create_df(points_dict_,ct))
    ct = 0
    for v in points_dict_.values():
        if v == "O":
            ct += 1
    part1 = ct
    print("part1\t", part1)
    # for viz
    # df = pd.concat(dfs,axis='index')
    # df.to_csv('../points_round.csv')

    # part_II
    print("part II")
    min_x, max_x, min_y, max_y = get_max_min(part_ii_points)
    floor_y = max_y + 1
    flag = True
    ct = 0
    # for viz
    # dfs = []
    # dfs.append(create_df(part_ii_points, 0))
    while flag:
        ct += 1
        end = play_snow_ball(
            (500, 0), max_y=floor_y, points_dict_=part_ii_points, part=2
        )
        if end == (-999, -999):
            flag = False
            break
        if part_ii_points[end] == ".":
            part_ii_points[end] = "O"
        else:
            flag = False
        # for viz
        # if ct % 100 == 0:
        #     dfs.append(create_df(part_ii_points, ct))

    print(ct)
    # for viz
    # plot_map(part_ii_points, *get_max_min(part_ii_points))
    # df = pd.concat(dfs,axis='index')
    # df.to_csv('../points_round_partII.csv')
    print("part1\t", part1)
    print("part2\t", ct)
