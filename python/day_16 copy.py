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

SAMPLE_DATA = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def parse_input(string):
    pattern = re.compile(r"([A-Z]{2})")
    flow_pattern = re.compile(r"(\d+)")

    nodes = {}
    for line in string.split("\n"):
        raw = pattern.findall(line)
        nodes[raw[0]] = {"links": raw[1:], "flow": int(flow_pattern.findall(line)[0])}
    return nodes


def print_short_path_vals(graph, source, target, nodes):
    short_path = nx.shortest_path(graph, source, target)
    for item in short_path:
        print(item, nodes[item]["flow"])
    return len(short_path) - 1


class ValvePath:
    def __init__(
        self,
        path,
        current_valve,
        closed_valves,
        current_turn,
        current_score,
        points_per_round,
        has_helper=False,
        helper_path=[],
        helper_current_valve=None,
        max_turns=30,
    ):
        self.path = path
        self.current_valve = current_valve
        self.closed_valves = closed_valves[:]
        self.current_turn = current_turn
        self.current_score = current_score
        self.points_per_round = points_per_round
        self.max_turns = max_turns
        self.has_helper = has_helper
        self.helper_path = helper_path
        self.helper_current_valve = helper_current_valve
        self.set_max_points_current_settings()
        self.set_max_points_all_open()

    def set_max_points_all_open(self):
        self.max_points_all_open = self.current_score + (
            self.points_per_round + sum([valves[v] for v in self.closed_valves])
        ) * (self.max_turns - self.current_turn)

    def set_max_points_current_settings(self):
        self.max_points_current_settings = self.current_score + (
            self.points_per_round * (self.max_turns - self.current_turn)
        )

    def get_available_closed_valves(self):
        return [
            v
            for v in self.closed_valves
            if distances[self.current_valve].get(v, INFINITY) <= self.max_turns + 1
        ]

    def get_available_closed_valves_helper(self):
        return [
            v
            for v in self.closed_valves
            if distances[self.helper_current_valve].get(v, INFINITY)
            <= self.max_turns + 1
        ]

    def elephant_play_round(self):
        v_h_rounds = []
        if self.helper_current_valve in self.closed_valves:
            idx = self.closed_valves.index(self.helper_current_valve)
            self.closed_valves = (
                self.closed_valves[0:idx] + self.closed_valves[idx + 1 :]
            )
            self.points_per_round += valves[self.helper_current_valve]
            self.set_max_points_current_settings()

            return [self]

        new_paths = []
        available_valves = self.get_available_closed_valves()
        if available_valves:
            for v in available_valves:
                # create a new_valve_path

                n_p = ValvePath(
                    path=self.path[:] + [v],
                    current_valve=v,
                    closed_valves=self.closed_valves,
                    current_turn=self.current_turn + distances[self.current_valve][v],
                    current_score=self.current_score
                    + self.points_per_round * distances[self.current_valve][v],
                    points_per_round=self.points_per_round,
                )
                new_paths.append(n_p)
            return new_paths
        else:
            # no additional available valves, wait until the end
            self.set_max_points_current_settings()
            self.current_score = self.max_points_current_settings
            self.current_turn = self.max_turns
            return [self]

    def play_round(self):
        """start at the beginning of the minute
        if placed on a closed_valve --> open it:
            self.score += self.pointsperround
            create a new valve with the additional points released to continue the path
        else: move to one of the closed valves.
            self.score = self.pointsperround * distance
        """
        v_round = []
        if self.current_valve in self.closed_valves:
            self.current_score += self.points_per_round
            self.current_turn += 1
            idx = self.closed_valves.index(self.current_valve)
            self.closed_valves = (
                self.closed_valves[0:idx] + self.closed_valves[idx + 1 :]
            )
            self.points_per_round += valves[self.current_valve]
            self.set_max_points_current_settings()
            if not self.has_helper:
                v_round.extend([self])
            else:
                v_round.extend(self.elefant_play_round())

        new_paths = []
        available_valves = self.get_available_closed_valves()
        if available_valves:
            for v in available_valves:
                # create a new_valve_path

                n_p = ValvePath(
                    path=self.path[:] + [v],
                    current_valve=v,
                    closed_valves=self.closed_valves,
                    current_turn=self.current_turn + distances[self.current_valve][v],
                    current_score=self.current_score
                    + self.points_per_round * distances[self.current_valve][v],
                    points_per_round=self.points_per_round,
                )
                new_paths.append(n_p)
            return new_paths
        else:
            # no additional available valves, wait until the end
            self.set_max_points_current_settings()
            self.current_score = self.max_points_current_settings
            self.current_turn = self.max_turns
            return [self]


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__16.txt"))
    # input = get_input(None)
    nodes = parse_input(input)
    valves = {}
    for k, v in nodes.items():
        if v["flow"] > 0:  # or k == 'AA':
            valves[k] = v["flow"]

    G = nx.Graph()
    G.add_nodes_from(nodes.keys())

    print(G)
    keys_ = sorted(list(nodes.keys()))

    for k, v in nodes.items():
        for n in v["links"]:
            G.add_edge(k, n)
    print(G)
    pos = nx.spring_layout(G, seed=7)

    node_list = G.nodes
    colors = [nodes[g]["flow"] for g in node_list]
    sizes = [c * 800 / max(colors) for c in colors]
    nx.draw(
        G,
        pos=pos,
        nodelist=node_list,
        node_color=colors,
        node_size=sizes,
        cmap=plt.cm.Blues,
    )
    nx.draw_networkx_labels(G, pos=pos)

    paths = dict(nx.all_pairs_shortest_path(G))

    distances = {}
    for k, v in paths.items():
        distances[k] = {}
        for kv, vv in v.items():
            distances[k][kv] = len(vv) - 1

    target_valves = list(valves.keys())  # all valves with flow

    max_points_per_round = sum(colors)
    print(f"max_points per round {max_points_per_round}")

    starting_path = ValvePath(
        path=["AA"],
        current_valve="AA",
        closed_valves=list(valves.keys()),  # [0:2],
        current_turn=0,
        current_score=0,
        points_per_round=0,
    )

    all_paths = deque([starting_path])
    finished_paths = []
    ct = 0
    current_score = 0
    while all_paths:
        ct += 1
        c_path = all_paths.popleft()
        current_score = max(current_score, c_path.current_score)
        if c_path.current_turn > c_path.max_turns + 1:
            continue
        if (
            c_path.current_turn == c_path.max_turns
        ):  # or (c_path.current_score + (c_path.max_turns - c_path.current_turn) * max_points_per_round) < current_score:
            finished_paths.append(c_path)
        else:
            all_paths.extend(c_path.play_round())
            # print(ct, c_path.__dict__)

    scores = [item.current_score for item in finished_paths if item.current_turn <= 30]
    score = max(scores)

    for item in finished_paths:
        if item.current_score == score:
            print(item.__dict__)


# part 1:
# 1417 is too low
# 1491 is too low
# 1601 is too low
# 2186 not the right answer
# 2054 not the right answer
# 1932 not the right answer
# 1944 is the right answer
# part 2:
