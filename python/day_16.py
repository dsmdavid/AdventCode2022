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

def get_score(valve_dict, max_turns = 30):
    score = 0
    for open_valve, turn in valve_dict.items():
        points = (max_turns - turn - 1) * valves[open_valve]
        score += points
    return score

def solver(target_valves = set(), starting_path = (['AA'],0), turns_remaining = 30):
    if len(target_valves) == 0:
        return
    for valve in target_valves:
        current_valve = starting_path[0][-1]
        if distances[current_valve][valve] <= turns_remaining :
            turns_remaining = turns_remaining - distances[current_valve][valve] - 1
            # flow_rate = starting_path[1] + valves[valve]
            max_flow = starting_path[1] + valves[valve] * turns_remaining
            new_path = (starting_path[0][:] + [valve],max_flow)
            valve_paths.append(new_path)
            target_valves = target_valves.copy()
            solver(target_valves = target_valves - set(new_path[0]),starting_path= new_path,turns_remaining= turns_remaining)






    


if __name__ == "__main__":
    # input = get_input(os.path.join("./inputs", "2022__16.txt"))
    input = get_input(None)
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
    valve_paths = []
    target_valves = set(list(valves.keys()))  # all valves with flow
    # print(score)
    solver(target_valves, starting_path = (['AA'],0,0), turns_remaining = 30)
    # print(valve_paths)
    max_score = max([path[1] for path in valve_paths])
    print(valves)
    print(max_score, len(valve_paths))


    

# part 1:
# 1944 is the right answer
# part 2:
# ?
# too low 1425 + 1070 = 2495