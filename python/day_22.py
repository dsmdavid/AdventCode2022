import os
import re
import operator
from collections import deque, defaultdict, Counter
import sys

GRID = defaultdict(lambda: ' ')
MOVERS = 0
FACE_SIZE = 49

SAMPLE_DATA = """        ...#                        
        .#..                                
        #...                                
        ....                                
...#.......#                                
........#...                                
..#....#....                                
..........#.                                
        ...#....                        
        .....#..                        
        .#......                        
        ......#.                        

10R5L5R10L4R5L5"""


MAP_POINTS = {
    'N'  : (1  ,0),
    'E'  : (0  ,1),
    'S'  : (-1 ,0),
    'W'  : (0  ,-1)
}
MAP_DIRECTIONS = {
    'N'  : {'R':'E','L':'W'},
    'E'  : {'R':'S','L':'N'},
    'S'  : {'R':'W','L':'E'},
    'W'  : {'R':'N','L':'S'}
}
MAP_BLIZZARD = {
    '<':'W',
    '>':'E',
    '^':'N',
    'v':'S'
}
MAP_DIRECTION_SCORE = {
    'N': 3,
    'E': 0,
    'S': 1,
    'W': 2
}
MAP_FACE={
    'A': {'ROW_MIN':150, 'ROW_MAX': 199,'COL_MIN':  50, 'COL_MAX':  99},
    'B': {'ROW_MIN':100, 'ROW_MAX': 149,'COL_MIN':  50, 'COL_MAX':  99},
    'C': {'ROW_MIN': 50, 'ROW_MAX':  99,'COL_MIN':  50, 'COL_MAX':  99},
    'D': {'ROW_MIN':  0, 'ROW_MAX':  49,'COL_MIN':   0, 'COL_MAX':  49},
    'E': {'ROW_MIN':150, 'ROW_MAX': 199,'COL_MIN': 100, 'COL_MAX': 149},
    'F': {'ROW_MIN': 50, 'ROW_MAX':  99,'COL_MIN':   0, 'COL_MAX':  49}
}
MAP_FACE_EDGE_RAW = '''A-N-> D-E (A-COL-0-> D-ROW-0)
A-W-> F-E (A-ROW-0-> F-ROW-49)
B-W-> F-S (B-ROW-0-> F-COL-0)
B-E-> E-N (B-ROW-0-> E-COL-0)
C-E-> E-W (C-ROW-0-> E-ROW-49)
C-S-> D-W (C-COL-0-> D-ROW-0)
F-N-> B-E (F-COL-0-> B-ROW-0)
F-W-> A-E (F-ROW-0-> A-ROW-49)
D-E-> C-N (D-ROW-0-> C-COL-0)
D-S-> E-S (D-COL-0-> E-COL-0)
D-W-> A-S (D-ROW-0-> A-COL-0)
E-E-> C-W (E-ROW-0-> C-ROW-49)
E-N-> D-N (E-COL-0-> D-COL-0)
E-S-> B-W (E-COL-0-> B-ROW-0)'''
pattern = re.compile(r"([A-Z])\-([A-Z]).{3}([A-Z])\-([A-Z]).{2}([A-Z]).([A-Z]+).(\d+).{3}([A-Z]).([A-Z]+).(\d+)")
list_edges = pattern.findall(MAP_FACE_EDGE_RAW)
MAP_EDGES = {}
def get_edges(list_edges):
    for item in list_edges:
        face, direction, new_face, new_direction, _, type_, _, _, new_type, order = item
        if not MAP_EDGES.get(face, None):
            MAP_EDGES[face] = {}
        MAP_EDGES[face][direction] = {'new_face':new_face, 'new_direction':new_direction, 'type':type_, 'new_type':new_type, 'order':int(order)}

def sum_tup(a,b):
    return tuple([sum(tup) for tup in zip(a,b)])

def get_input(fn):
    if not fn:
        return SAMPLE_DATA
    with open(fn, "r") as f:
        return f.read()

def create_grid_face():
    grid_face = {}
    for item in GRID.keys():
        face = ''
        for k,v in MAP_FACE.items():
            if (v['ROW_MIN'] <= item[0] <= v['ROW_MAX']) and (v['COL_MIN'] <= item[1] <= v['COL_MAX']):
                face = k
        if face == '' and GRID[item] != ' ':
            print('error - no face found for this coord:\t', item)
            raise
        grid_face[item] = face
    return grid_face

def parse_instructions(string):
    pattern = re.compile(r"(\d+|R|L)")    
    instructions = pattern.findall(string)
    return instructions

def parse_input(string):
    global max_move_rows, max_move_cols
    grid, instructions = string.split('\n\n')
    instructions = parse_instructions(instructions)
    lines = [] 
    for line in grid.split('\n'):
        lines.append(list(line))
    for i, k in enumerate(range(len(lines)-1,-1,-1)):
        for pos in range(len(lines[i])):
            GRID[(k,pos)] = lines[i][pos]

    max_move_rows = len(lines) - 1
    max_move_cols = max(map(len,lines))
    return instructions

def print_grid():
    minx = maxx = miny = maxy = 0
    for k in GRID.keys():
        minx = min(minx, k[0])
        maxx = max(maxx, k[0])
        miny = min(miny, k[1])
        maxy = max(maxy, k[1])
    s = ''
    for i in range(maxx,minx-1,-1):
        # print('row: ',i,'\t', end = '\t')
        print("'    ", end='')
        s += "'    "
        for j in range(miny, maxy+1):
            val = GRID[(i,j)]
            print(val, end='')
            s += val
        print('\n', end = '')
        s += '\n'
    return s

class Traveller():
    def __init__(self, x, y, type = 'flat'):
        self.position = (x,y)
        self.direction = 'E'
        self.move_dir = MAP_POINTS[self.direction]
        self.type = type

    def set_direction(self, turn):
        self.direction = MAP_DIRECTIONS[self.direction][turn]
        self.move_dir = MAP_POINTS[self.direction]

    def get_next_position(self):
        temp_next_position = (
            self.position[0] + self.move_dir[0],
            self.position[1] + self.move_dir[1]
            )

        if GRID[temp_next_position] == '.':
            # all good
            pass
        elif GRID[temp_next_position] == ' ':
            # need to wrap around
            temp_next_position = self.wrap_next_available(type = self.type)
        
        if GRID[temp_next_position] == '#':
            temp_next_position = self.position
        GRID[self.position] = self.direction
        self.position = temp_next_position
        # GRID[self.position] = self.direction

    def wrap_next_available(self, type='flat'):
        '''Accepts 2 types: flat and cube'''
        global grid_face
        found = False
        if type == 'flat':
            if self.direction == 'E':
                pos = 0
                while not found:
                    if GRID[(self.position[0], pos)] != ' ':
                        found = True
                        next_pos = (self.position[0], pos)
                    pos += 1
            elif self.direction == 'W':
                # print('going_west')
                pos = max_move_cols
                while not found:
                    # print(f'attempting_west at row {self.position[0]}, column= ',pos)
                    if GRID[(self.position[0], pos)] != ' ':
                        found = True
                        next_pos = (self.position[0], pos)
                    pos -= 1
            elif self.direction == 'S':
                pos = max_move_rows
                while not found:
                    if GRID[(pos, self.position[1])] != ' ':
                        found = True
                        next_pos = (pos, self.position[1])
                    pos -= 1
            elif self.direction == 'N':
                pos = 0
                while not found:
                    if GRID[(pos, self.position[1])] != ' ':
                        found = True
                        next_pos = (pos, self.position[1])
                    pos += 1
        elif type =='cube':
            # which face are we in?
            current_face = grid_face[self.position]
            # which direction are we currently going?
            new_instructions = MAP_EDGES[current_face][self.direction]
            # which is the next position?

            # - find starting offsets
            current_offset_row = self.position[0] - MAP_FACE[current_face]['ROW_MIN']
            current_offset_col = self.position[1] - MAP_FACE[current_face]['COL_MIN']
            new_face = new_instructions['new_face']
            base_new_face_row = MAP_FACE[new_face]['ROW_MIN']
            base_new_face_col = MAP_FACE[new_face]['COL_MIN']
            # - do we change from col to row?
            if new_instructions['new_direction'] in ('N','E'):
                # we enter the face from the South or West
                delta = 0
            else:
                delta = FACE_SIZE

            if new_instructions['type'] == new_instructions['new_type']:
                # row -> row or col -> col
                new_offset_row = current_offset_row
                new_offset_col = current_offset_col
            # we have a row -> col or col -> row swap:
            # - what is the new offset (and direction!)
            elif new_instructions['type'] == 'COL':
                new_offset_row = FACE_SIZE - current_offset_col
                new_offset_col = current_offset_row
            else:
                new_offset_row = current_offset_col
                new_offset_col = FACE_SIZE - current_offset_row                       
            if new_instructions['new_type'] == 'COL':
                new_offset_row = delta
                if new_instructions['order'] != 0:
                    new_offset_col = new_instructions['order'] - new_offset_col
            else:
                new_offset_col = delta 
                if new_instructions['order'] != 0:
                    new_offset_row = new_instructions['order'] - new_offset_row



            next_pos = sum_tup(
                (base_new_face_row, base_new_face_col),
                (new_offset_row, new_offset_col)
            )
            # - what is the new offset (and direction!)
            # direction, order,...
            # is it blocked? -- if so, don't change the direction.
            if GRID[next_pos] == ' ':
                # debug --should not happen if I wrapped the cube correctly
                print('we --unexpectedly-- got to the void!')
                print(current_face,'->', new_face, delta, new_instructions['type'], new_instructions['new_type'],'\n',
                'current_offsets:\t',current_offset_row, current_offset_col,
                'new_offsets:\t', new_offset_row, new_offset_col, base_new_face_row, base_new_face_col, self.position, next_pos,
                GRID[self.position]
                )
                raise
            elif GRID[next_pos] == '#':
                # we're blocked, no need to update direction
                pass
            else:
                self.direction = new_instructions['new_direction']
                self.move_dir = MAP_POINTS[self.direction]
        return next_pos

    def parse_instruction(self, instruction):
        if instruction in ('R', 'L'):
            self.set_direction(instruction)
        else:
            self.move(int(instruction))
    def move(self, steps):
        for i in range(steps):
            self.get_next_position()



sample_instructions = '''10L5R100L1L1L15R1L3L19R20L100L17R5L1R10R1L15R4L100R3L100R1L12'''
if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__22.txt"))
    # input = get_input(None)
    instructions = parse_input(input)
    # for debugging:
    # instructions = parse_instructions(sample_instructions)
    grid_face = create_grid_face()
    get_edges(list_edges)
    ct = 0
    travel = Traveller(x=max_move_rows,y=50, type = 'cube')
    for instruction in instructions:
        try:
            travel.parse_instruction(instruction)
            # print(travel.position, grid_face[travel.position])

        except:
            print('ERROR HERE')
            print(instruction)
            print(travel.position, grid_face[travel.position])
            raise

        # print(instruction)
        # print(travel.__dict__)
        # ct += 1
        # if ct == 15:
        #     break
    GRID[travel.position] = 'X'
    # print_grid()
    print(travel.__dict__)
    row = max_move_rows - travel.position[0] + 1
    col = travel.position[1] + 1
    print(row, col, travel.direction)
    answer = 1000 * row + 4* col + MAP_DIRECTION_SCORE[travel.direction]
    # with open('./grid.csv','w') as f:
    #     f.write(print_grid())
    print(answer)


    # 163029 is too high
    # 95291 that's right!