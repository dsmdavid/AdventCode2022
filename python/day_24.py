import os
import re
import operator
from collections import deque, defaultdict, Counter

GRID = dict() # defaultdict(list)
MOVERS = 0

SAMPLE_DATA = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

SAMPLE_DATA = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

GRID_FILLER = {
    '.' : [],
    '#' : '#'
}
MAP_POINTS = {
    'N'  : (1  ,0),
    'E'  : (0  ,1),
    'S'  : (-1 ,0),
    'W'  : (0  ,-1)
}

MAP_BLIZZARD = {
    '<':'W',
    '>':'E',
    '^':'N',
    'v':'S'
}

def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def parse_input(string):
    global max_move_rows, max_move_cols
    lines = [] 
    blizzards = []
    for line in string.split('\n'):
        lines.append(list(line))
    for i, k in enumerate(range(len(lines)-1,-1,-1)):
        for pos in range(len(lines[i])):
            if lines[i][pos] in MAP_BLIZZARD.keys():
                blizzard = Blizzard(x = k , y = pos, dir = lines[i][pos])
                GRID[(k,pos)] = [blizzard]
                blizzards.append(blizzard)
            else:
                GRID[(k,pos)] = GRID_FILLER[lines[i][pos]][:]
    max_move_rows = len(lines)
    max_move_cols = len(lines[i])
    return blizzards

class Blizzard():
    def __init__(self, x, y, dir):
        self.position = (x,y)
        self.original_rep = dir
        self.type = MAP_BLIZZARD[dir]
        self.move_dir = MAP_POINTS[self.type]
        self.next_position = None

    def get_next_position(self):
        global max_move_rows
        global max_move_cols

        temp_next_position = (
            self.position[0] + self.move_dir[0],
            self.position[1] + self.move_dir[1]
        )
        if GRID[temp_next_position] == '#':
            # print('clash!',temp_next_position, self.next_position, max_move_rows,max_move_cols )
            if temp_next_position[0] == 0:
                # bottom, going south
                temp_next_position = (max_move_rows - 2, temp_next_position[1])
            elif temp_next_position[0] == max_move_rows - 1:
                temp_next_position = (1, temp_next_position[1])
        
            elif temp_next_position[1] == 0:
                # left, going east
                temp_next_position = (temp_next_position[0], max_move_cols - 2)
            elif temp_next_position[1] == max_move_cols - 1:
                temp_next_position = (temp_next_position[0], 1)
        self.next_position = temp_next_position
        

    def move(self):
        # update grid
        GRID[self.position].remove(self)
        GRID[self.next_position].append(self)
        # update attributes
        self.position = self.next_position
        self.next_position = None


    def __repr__(self):
        return self.original_rep

        return f"Blizzard at {str(self.position)}"
    def __str__(self):
        return self.original_rep


def print_grid():
    minx = maxx = miny = maxy = 0
    for k in GRID.keys():
        minx = min(minx, k[0])
        maxx = max(maxx, k[0])
        miny = min(miny, k[1])
        maxy = max(maxy, k[1])

    for i in range(maxx,minx-1,-1):
        for j in range(miny, maxy+1):
            val = GRID[(i,j)]
            if not val:
                val = '.'
            elif len(val) == 1:
                val = val[0]
            else:
                val = len(val)
            print(val, end='')
        print('\n', end = '')


def play_round(blizzards):
    for bliz in blizzards:
        bliz.get_next_position()
        bliz.move()

def find_valid_options(point):
    options = []
    for val in MAP_POINTS.values():
        next_point = (point[0] + val[0], point[1] + val[1])
        if next_point not in GRID.keys():
            continue
        if GRID[next_point] == []:
            options.append(next_point)
    if GRID[point] == []:
        options.append(point)
    return options

def get_to_the_end(end, paths, blizzards):
    i = 0
    flag = True
    while flag:
        play_round(blizzards)
        _ = []
        for j in range(len(paths)):
            next = paths.pop()
            if next == end:
                flag = False
                return next, i
            
            _.extend(find_valid_options(next))

        paths = list(set(_))
        i += 1

if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__24.txt"))
    # input = get_input(None)
    blizzards = parse_input(input)

    start = (max_move_rows - 1,1)
    end = (0, max_move_cols - 2)
    paths = [(max_move_rows - 1,1)]


    next, found_at = get_to_the_end(end, paths, blizzards)
    print('Part_1:\t', found_at)
    
    # part_2:
    # return to base
    total = found_at
    paths = [end]
    next, found_at = get_to_the_end(start, paths, blizzards)
    total += found_at + 1
    print('temp_\t', found_at, total)
    # return to end
    paths = [start]
    next, found_at = get_to_the_end(end, paths, blizzards)
    total += found_at + 1
    print('Part_2:\t', found_at, total)
