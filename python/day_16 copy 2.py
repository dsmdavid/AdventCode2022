from functools import reduce
from math import inf as INFINITY
import os
import json
import networkx as nx
from itertools import zip_longest
from collections import deque, defaultdict

import pandas as pd
from copy import deepcopy
import re
import sys
import matplotlib.pyplot as plt
from itertools import product

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

class ValveOpener():
    '''someone opening valves
    has a turn info
    and a log of all the valves opened and when
    '''
    def __init__(self, current_valve):
        self.turn = 0
        self.valves_opened = {}
        self.current_valve = current_valve
        self.used_this_turn = False
        self.is_idle = False
        self.remaining_until_active = 0

class ValveSolution():
    '''group of valves
    contains current open valves
    current closed valves
    a list of ValveOpeners'''
    def __init__(self,
         valve_openers, 
         closed_valves,
         valves_open = [],
         current_score = 0,
         points_per_round = 0,
         max_turns = 30):
        self.valve_openers = valve_openers
        self.closed_valves = closed_valves
        self.valves_open = {} # key: valve_name, value: turn it was open, e.g. "AA: 12"
        self.current_score = current_score
        self.points_per_round = points_per_round
        self.max_turns = max_turns
        self.flag_continue = True

    def get_available_closed_valves(self, valveopener):
            return [
            v
            for v in self.closed_valves
            if (valveopener.turn + distances[valveopener.current_valve].get(v, INFINITY) ) < self.max_turns + 1
        ]
    
    def play_round(self):
        """start at the beginning of the minute
        For each valve opener:
            if placed on a closed_valve --> open it:
                create a new valve with the additional points released to continue the path
            else: move to one of the closed valves and update the turn
        """
        self.flag_continue = True
        for vo in self.valve_openers:
            vo.used_this_turn = False
            if not vo.is_idle:
                if vo.current_valve in self.closed_valves and vo.turn < self.max_turns:
                    idx = self.closed_valves.index(vo.current_valve)
                    self.closed_valves = (
                        self.closed_valves[0:idx] + self.closed_valves[idx + 1 :]
                        )
                    # self.points_per_round += valves[vo.current_valve]
                    vo.valves_opened[vo.current_valve] = vo.turn * 1
                    vo.used_this_turn = True
                    vo.turn += 1
                self.flag_continue *= (vo.turn < self.max_turns)
            else:
                vo.remaining_until_active -= 1
                vo.used_this_turn = True
                vo.turn += 1
                if vo.remaining_until_active == 0:
                    vo.is_idle = False

        new_valve_openers_ready = []
        for vo in self.valve_openers:
            if vo.used_this_turn:
                new_valve_openers_ready.append([vo])
            else:
                new_valve_openers_temp = []
                destinations =  self.get_available_closed_valves(vo)
                self.flag_continue *= (len(destinations) > 0)
                if len(destinations) == 0:
                    new_valve_openers_temp.append(vo)
                else:
                    for destination in destinations:
                        v = deepcopy(vo)
                        v.current_valve = destination
                        v.remaining_until_active += distances[vo.current_valve][destination]
                        v.is_idle = True
                        new_valve_openers_temp.append(v)
                new_valve_openers_ready.append(new_valve_openers_temp)
        all_combinations = product(*new_valve_openers_ready)
        valid_combinations = []
        for combination in all_combinations:
            temp = []
            n_vo = len(combination)
            valves_ = set()
            for vo in combination:
                valves_.add(vo.current_valve[:])
                t_v = deepcopy(vo)
                temp.append(t_v)
            if (len(valves_) == n_vo) or (valves_ == set(['AA'])):
                valid_combinations.append(temp)
            # print(valves_)


        new_solutions = []
        for combination in valid_combinations:
            solution = deepcopy(self)
            solution.valve_openers = combination
            new_solutions.append(solution)
        # print('new solutions:', new_solutions)
        return new_solutions

            
    def get_score(self):
        score = 0
        for valveopener in self.valve_openers:
            for open_valve, turn in valveopener.valves_opened.items():
                points = (self.max_turns - turn - 1) * valves[open_valve]
                score += points
        self.score = score
        return score


    # def set_max_points_all_open(self):
    #     self.max_points_all_open = self.current_score + (
    #         self.points_per_round + sum([valves[v] for v in self.closed_valves])
    #     ) * (self.max_turns - self.current_turn)

    # def set_max_points_current_settings(self):
    #     self.max_points_current_settings = self.current_score + (
    #         self.points_per_round * (self.max_turns - self.current_turn)
    #     )

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

    human_valveopener = ValveOpener(
        current_valve="AA"
    )
 
    starting_solution = ValveSolution(
        closed_valves=list(valves.keys()),
        valve_openers = [human_valveopener],
        max_turns=28
    )
    #  valve_openers = [human_valveopener, elephant_valveopener],


    all_paths = deque([starting_solution])
    # starting_path = ValvePath(
    #     path=["AA"],
    #     current_valve="AA",
    #     closed_valves=list(valves.keys()),  # [0:2],
    #     current_turn=0,
    #     current_score=0,
    #     points_per_round=0,
    # )

    finished_paths = []
    ct = 0
    current_score = 0
    while all_paths:
        ct += 1
        c_path = all_paths.popleft()
        # all_paths = deque([])
        # current_score = max(current_score, c_path.current_score)
        if not c_path.flag_continue:
            finished_paths.append(c_path)
        else:
            extension = c_path.play_round()
            all_paths.extend(extension)

    print(len(finished_paths))
    print(len(all_paths))

    scores = [item.get_score() for item in finished_paths]
    score = max(scores)
    print('MAX SCORE:\t', score)
    for item in finished_paths:
        if item.score == score:
            print(item.__dict__)
            for vo in item.valve_openers:
                print(vo.__dict__)

#    part 2:
    elephant_valveopener = ValveOpener(
        current_valve="AA"
    )
    starting_solution = ValveSolution(
        closed_valves=list(
            set(list(valves.keys())) - set(vo.valves_opened.keys())
        ),
        valve_openers = [elephant_valveopener],
        max_turns=28
    )
    #  valve_openers = [human_valveopener, elephant_valveopener],


    all_paths = deque([starting_solution])

    finished_paths = []
    ct = 0
    current_score = 0
    while all_paths:
        ct += 1
        c_path = all_paths.popleft()
        # all_paths = deque([])
        # current_score = max(current_score, c_path.current_score)
        if not c_path.flag_continue:
            finished_paths.append(c_path)
        else:
            extension = c_path.play_round()
            all_paths.extend(extension)

    print(len(finished_paths))
    print(len(all_paths))

    scores = [item.get_score() for item in finished_paths]
    score = max(scores)
    print('MAX SCORE:\t', score)
    for item in finished_paths:
        if item.score == score:
            print(item.__dict__)
            for vo in item.valve_openers:
                print(vo.__dict__)

# part 1:
# 1944 is the right answer
# part 2:
# ?
# too low 1425 + 1070 = 2495