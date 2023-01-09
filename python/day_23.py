import os
import re
import operator
from collections import deque, defaultdict, Counter

GRID = defaultdict(lambda: '.')
MOVERS = 0

SAMPLE_DATA = """.....
..##.
..#..
.....
..##.
....."""

SAMPLE_DATA="""....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

MAP_POINTS = {
    'NW' : (1  ,-1),
    'N'  : (1  ,0),
    'NE' : (1  ,1),
    'E'  : (0  ,1),
    'SE' : (-1 ,1),
    'S'  : (-1 ,0),
    'SW' : (-1 ,-1),
    'W'  : (0  ,-1)
}

MAP_ORDER = {
    'N' : ['NW','N','NE'],
    'S' : ['SW','S','SE'],
    'W' : ['NW','W','SW'],
    'E' : ['NE','E','SE']
}

def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def parse_input(string):
    lines = [] 
    elves = []
    for line in string.split('\n'):
        lines.append(list(line))
    for i, k in enumerate(range(len(lines)-1,-1,-1)):
        for pos in range(len(lines[i])):
            if lines[i][pos] == '#':
                elf = Elf(x = k , y = pos)
                GRID[(k,pos)] = elf 
                elves.append(elf)
    return elves

class Elf():
    def __init__(self, x, y):
        self.position = (x,y)
        self.order = deque(['N','S','W','E'])
        self.next_position = None
        self.flag_move = True

    def get_neighbours(self):
        self.neighbours = {}
        for k,v in MAP_POINTS.items():
            self.neighbours[k] = GRID[(self.position[0] + v[0], self.position[1] + v[1])]
        self.flag_move = sum(1 for v in self.neighbours.values() if v == '.') != 8

    def get_next_point(self):
        self.get_neighbours()
        if self.flag_move:
            # only find next_move if there's at least one surrounding space occupied 
            for item in self.order:
                free_neighbours = sum([1 for neighbour in MAP_ORDER[item] if self.neighbours[neighbour] == '.'])
                if free_neighbours == 3:
                    self.next_position = (
                        self.position[0] + MAP_POINTS[item][0],
                        self.position[1] + MAP_POINTS[item][1]
                    )
                    return
            self.next_position = self.position
        return

    def move(self, counter):
        global MOVERS
        # update self.order:
        self.order.append(self.order.popleft())
        # shall we move?
        if self.flag_move and counter[self.next_position] == 1:
            # update grid
            GRID[self.position] = '.'
            GRID[self.next_position] = self
            # update attributes
            self.position = self.next_position
            self.next_position = None
            MOVERS += 1
        else:
            self.next_position = None




    def __repr__(self):
        return f"Elf at {str(self.position)}"
    def __str__(self):
        return '#'


def print_grid():
    minx = maxx = miny = maxy = 0
    for elf in elves:
        minx = min(minx, elf.position[0])
        maxx = max(maxx, elf.position[0])
        miny = min(miny, elf.position[1])
        maxy = max(maxy, elf.position[1])

    for i in range(maxx,minx-1,-1):
        for j in range(miny, maxy+1):
            print(GRID[(i,j)], end='')
        print('\n', end = '')


def play_round():
    next_positions = Counter()
    for elf in elves:
        elf.get_next_point()
        next_positions[elf.next_position] += 1
    # print(next_positions)
    for elf in elves:
        elf.move(next_positions)



if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__23.txt"))
    # input = get_input(None)
    elves = parse_input(input)
    minx = maxx = miny = maxy = 0
    ct = 0
    rounds = 0
    print('---')
    for i in range(10):
        play_round()
        rounds += 1
        # print_grid()
    for elf in elves:
        minx = min(minx, elf.position[0])
        maxx = max(maxx, elf.position[0])
        miny = min(miny, elf.position[1])
        maxy = max(maxy, elf.position[1])
        ct += 1
    area = (maxx - minx + 1) * (maxy - miny + 1)
    print('part_1:\t',area - ct)
    # part_2: no elf moves
    while MOVERS > 0:
        MOVERS = 0
        play_round()
        rounds += 1
    print('part_2:\t',rounds)