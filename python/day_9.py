import os
from collections import defaultdict
import pprint
from copy import deepcopy
import sys

SAMPLE_DATA = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


class Knot:
    def __init__(self, starting_position=(0, 0), name=0):
        self.parent_knot = None
        self.children_knots = []
        self.current_position = starting_position
        self.is_tail = False
        self.is_head = False
        self.visited = defaultdict(int)
        # useful for inspection purposes
        self.name = name

    def move_tail(self):
        chx = self.parent_knot.current_position[0]
        chy = self.parent_knot.current_position[1]
        ctx = self.current_position[0]
        cty = self.current_position[1]
        dx = (chx - ctx) ** 2
        dy = (chy - cty) ** 2
        distance = dx + dy
        current_position = self.current_position
        if distance <= 2:
            # no need to move
            return current_position
        else:
            # move vertically:
            if chx > ctx:
                dir = "U"
            elif chx < ctx:
                dir = "D"
            else:
                dir = "X"
            current_position = self.move_straight(dir, current_position)
            # move horizontally:
            if chy > cty:
                dir = "R"
            elif chy < cty:
                dir = "L"
            else:
                dir = "X"
            current_position = self.move_straight(dir, current_position)

        return current_position

    def move_straight(self, dir, current_position):
        val = 1
        if dir in "DL":
            val = -1 * val
        if dir in "UD":
            new_position = (current_position[0] + val, current_position[1])
            # self.current_head = (self.current_head[0] + val, self.current_head[1])
        elif dir in "LR":
            new_position = (current_position[0], current_position[1] + val)
        else:
            # don't move
            new_position = current_position
            # self.current_head = (self.current_head[1], self.current_head[1] + val)
        return new_position

    def move(self):
        self.current_position = self.move_tail()
        self.visited[self.current_position] += 1


class Rope:
    def __init__(self, starting_position=(0, 0), rope_length=2):
        self.knots = []
        self.rope_length = rope_length
        self.current_position = starting_position
        self.populate_knots()
        self.current_head = self.knots[0]

    def populate_knots(self, rope_length=None):
        if not rope_length:
            rope_length = self.rope_length
        starting_position = self.current_position
        for i in range(rope_length):
            if i == 0:
                # starting_knot
                self.knots.append(Knot(starting_position=starting_position, name=i))
                self.knots[i].is_head = True
            else:
                self.knots.append(Knot(starting_position=starting_position, name=i))
                self.knots[i - 1].children_knots.append(self.knots[i])
                if i == rope_length - 1:
                    self.knots[i].is_tail = True

        for i in range(rope_length):
            if i != 0:
                self.knots[i].parent_knot = self.knots[i - 1]

    def process_instruction(self, instruction):
        # sample instruction = 'R 4'
        dir = instruction.split(" ")[0]
        moves = int(instruction.split(" ")[1])
        for step in range(int(moves)):
            self.move(dir)

    def move(self, dir):
        for i, knot in enumerate(self.knots):
            if knot.is_head:
                # head moves as head, not as tail
                knot.current_position = knot.move_straight(dir, knot.current_position)
            else:
                # others move as tails
                knot.move()

    def n_visited_by_tail(self):
        ct = 0
        for knot in self.knots:
            if knot.is_tail:
                ct = len(knot.visited.keys())
        return ct


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__9.txt"))
    # input = get_input(None)
    raw_rows = input.split("\n")
    rope = Rope()
    ropeii = Rope(rope_length=10)
    for line in raw_rows:
        rope.process_instruction(line)
        ropeii.process_instruction(line)
    ct1 = rope.n_visited_by_tail()
    ct2 = ropeii.n_visited_by_tail()
    print("part1\t", ct1, "\npart2\t", ct2)
