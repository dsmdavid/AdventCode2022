import os
from collections import defaultdict, namedtuple, deque, OrderedDict
import pprint
from copy import deepcopy
import sys
import operator
from functools import reduce
import math

SAMPLE_DATA = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

MAP = {}
VISITED = set()
START = tuple()
END = tuple()
PATHS = deque()

def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()

def lcm_(denominators):
    return reduce(lambda x,y: x*y // math.gcd(x,y), denominators)


class Puzzle():
    def __init__(self, map, start, end):
        self.map = map
        self.start = start
        self.end = end
        self.paths = deque([[start]])
        self.visited = set(start)
        self.step_to_end = None
        self.found = False

    def add_step(self, current_path, next_path_pos, current_height):
        # print('start of step')
        # print(current_path, next_path_pos, current_height, found)
        ct = 0
        if next_path_pos not in self.visited and next_path_pos in self.map.keys() and (self.map.get(next_path_pos,0) -1) <= current_height:
            ct = 1
            next_path = current_path[:]
            next_path.append(next_path_pos)
            self.paths.append(next_path)
            self.visited.add(next_path_pos)
            # if next_path_pos == 0:
            #     print('*'*100, 'adding 0')
            if next_path_pos == self.end:
                self.found = True
            # if self.found:
            #     print(self.end, next_path_pos, current_path)
            #     print(f'found {next_path_pos}')
        return ct

    # def increase(cp, i, val):


    def solve(self):
        while not self.found and self.paths:
            current_path = self.paths.popleft()
            # print('path_start')
            # print(current_path)
            if current_path:
                # print(current_path)
                current = current_path[-1]
                current_height = self.map[current]
                ct = 0
                for i in (-1,1):
                    next_path_pos = (current[0] + i, current[1])
                    ctx = self.add_step(current_path, next_path_pos,current_height)
                    ct += ctx
                for j in (-1,1):
                    next_path_pos = (current[0], current[1] + j)
                    cty = self.add_step(current_path, next_path_pos, current_height)
                    ct += cty
        # if self.found:
        #     print(self.paths)

    def get_max_steps(self):
        if self.paths:
            self.step_to_end = reduce(lambda x,y: x if x < y else y, map(len, self.paths))
        else:
            self.step_to_end = 1000000


def create_map(input):
    '''x,y - x = rows, y = columns'''
    global START, END
    for i, row in enumerate(input.split('\n')):
        for k, col in enumerate(list(row)):
            if col == 'S':
                START = (i,k)
                col = 'a'
                print(f'found start at {START}')
            elif col == 'E':
                END = (i,k)
                col ='z'
                print(f'found end at {END}')

            MAP[(i,k)] = ord(col)


def add_step(current_path, next_path_pos, found):
    ct = 0
    if next_path_pos not in VISITED and next_path_pos in MAP.keys() and (MAP.get(next_path_pos,0) -1) <= current_height:
        ct = 1
        next_path = current_path[:]
        next_path.append(next_path_pos)
        PATHS.append(next_path)
        VISITED.add(next_path_pos)
        if  next_path_pos == END:
            found = True
    # try:
    #     if found:
    #         print('found')
    #         print(current_path)
    #         print(next_path)
    # except:
    #     print(current_path, next_path_pos, found)
    return ct, found



def add_step_part_ii(current_path, next_path_pos, visited: set, paths: list, found):
    ct = 0
    if next_path_pos not in visited and next_path_pos in MAP.keys() and (MAP.get(next_path_pos,0) -1) <= current_height and MAP.get(next_path_pos) != ord('a'):
        ct = 1
        next_path = current_path[:]
        next_path.append(next_path_pos)
        paths.append(next_path)
        visited.add(next_path_pos)
        if next_path_pos == END:
            found = True
    try:
        if found:
            print('found')
            print(current_path)
            print(next_path)
    except:
        print(current_path, next_path_pos, found)
    if next_path_pos == (2,5):
        print('got you')
    return ct, found


if __name__ == "__main__":
    # input = get_input(os.path.join("./inputs", "2022__12.txt"))
    input = get_input(None)
    create_map(input)
    # print(MAP)
    print(START, END)
    found = False
    starting_path = [START]
    PATHS.append(starting_path)
    VISITED.add(START)
    print(PATHS)
    print('starting')
    check = 0
    distance = 0
    while not found: 
        current_path = PATHS.popleft()
        if current_path:
            current = current_path[-1]
            current_height = MAP[current]
            ct = 0
            for i in (-1,1):
                next_path_pos = (current[0] + i, current[1])
                ctx, found = add_step(current_path, next_path_pos, found)
                ct += ctx
            for j in (-1,1):
                next_path_pos = (current[0], current[1] + j)
                cty, found = add_step(current_path, next_path_pos, found)
                ct += cty

    max_distance = 0
    for path in PATHS:
        max_distance = max(len(path), max_distance)

    print('--->>>')
    print(max_distance - 1)
    # for path in PATHS:
    #     if len(path) == max_distance:
    #         print(max_distance-1)
    #         print(path)
    print('---')
    puzzle = Puzzle(map = MAP, start = START, end = END)
    puzzle.solve()
    puzzle.get_max_steps()
    print(puzzle.step_to_end)

    starting_sites = [k for k,v in MAP.items() if v == ord('a')]
    puzzles = []
    for start in starting_sites:
        # print(start)
        puzzles.append(Puzzle(map = MAP, start = start, end = END))
    distances = []
    for puzzle in puzzles:
        puzzle.solve()
        puzzle.get_max_steps()
        distances.append(puzzle.step_to_end)
        # print(puzzle.start, puzzle.end, puzzle.step_to_end)
    print(sorted(list(set(distances))))
    print(min(distances))


    # # for path in PATHS:
    # #     if (3,6) in path:
    # #         print(path)
    # starting_sites = [k for k,v in MAP.items() if v == ord('a')]
    # # print(starting_sites)
    # winning_path = None
    # for start in [(4,0)]: #starting_sites:

    #     found = False
    #     paths = deque()
    #     visited = set()
    #     starting_path = [start]
    #     paths.append(starting_path)
    #     visited.add(start)
    #     print(f'starting\t {start}')
    #     round_ = 0
    #     totals = []
    #     max_distance_internal = 1000000
    #     while not found and paths: 
    #         round_ += 1
    #         current_path = paths.popleft()
    #         if current_path:
    #             current = current_path[-1]
    #             current_height = MAP[current]
    #             ct = 0
    #             for i in (-1,1):
    #                 next_path_pos = (current[0] + i, current[1])   
    #                 ctx, found = add_step_part_ii(current_path, next_path_pos, visited, paths, found)
    #                 ct += ctx
    #                 if found:
    #                     'found in i, breaking'
    #                     break
    #             for j in (-1,1):
    #                 next_path_pos = (current[0], current[1] + j)
    #                 cty, found = add_step_part_ii(current_path, next_path_pos, visited, paths, found)
    #                 ct += cty
    #                 if found:
    #                     'found in j, breaking'
    #                     break
    #         if round_ > max_distance:
    #             print(f'here {found}')
    #             print(start,paths)
    #             break
    #     # print('debut -->>')
    #     # print(paths)
    #     # print('single paths')
    #     for path in paths:
    #         print('here path')
    #         print(path)
    #         print('stats')
    #         print(len(path), END, END in path, found)
    #     for path in paths:
    #         if path:
    #             max_distance_internal = min(len(path), max_distance_internal)
    #     # if paths and found:
    #         # print(f'this was found: \t {start}')
    #         # max_distance = min(max_distance, max_distance_internal)
            
    #     # print(max_distance)
    #     max_distance = min(max_distance, max_distance_internal)
    # print(max_distance)
    # 376 is too low,
    # 382 is too high