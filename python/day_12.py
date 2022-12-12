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
START = tuple()
END = tuple()

def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()

class Puzzle():
    def __init__(self, map, start, end, stop_if = 1000000):
        self.map = map
        self.start = start
        self.end = end
        self.paths = deque([[start]])
        self.visited = set(start)
        self.step_to_end = None
        self.found = False
        self.stop_if = stop_if

    def add_step(self, current_path, next_path_pos, current_height):
        if next_path_pos not in self.visited and next_path_pos in self.map.keys() and (self.map.get(next_path_pos,0) -1) <= current_height:
            next_path = current_path[:]
            next_path.append(next_path_pos)
            self.paths.append(next_path)
            self.visited.add(next_path_pos)

            if next_path_pos == self.end:
                self.found = True
    

    def solve(self):
        while not self.found and self.paths and len(self.paths) <= self.stop_if:
            current_path = self.paths.popleft()

            if current_path:
                current = current_path[-1]
                current_height = self.map[current]
                for i in (-1,1):
                    next_path_pos = (current[0] + i, current[1])
                    self.add_step(current_path, next_path_pos,current_height)
                for j in (-1,1):
                    next_path_pos = (current[0], current[1] + j)
                    self.add_step(current_path, next_path_pos, current_height)


    def get_max_steps(self):
        if self.paths:
            self.step_to_end = reduce(lambda x,y: x if x < y else y, map(len, self.paths))
        else:
            self.step_to_end = self.stop_if+1


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



if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__12.txt"))
    # input = get_input(None)
    create_map(input)
    ### part 1
    puzzle = Puzzle(map = MAP, start = START, end = END)
    puzzle.solve()
    puzzle.get_max_steps()
    print('part1\t',puzzle.step_to_end)
    ### part 2
    starting_sites = [k for k,v in MAP.items() if v == ord('a')]
    puzzles = []
    stop_if = puzzle.step_to_end

    for start in starting_sites:
        puzzle = Puzzle(map = MAP, start = start, end = END, stop_if = stop_if)
        puzzle.solve()
        puzzle.get_max_steps()
        stop_if = min(stop_if, puzzle.step_to_end)s

    print('part2\t',stop_if)