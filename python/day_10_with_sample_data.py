import os
from collections import defaultdict, namedtuple
import pprint
from copy import deepcopy
import sys

SAMPLE_DATA = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

TURNS = {
    'noop': 1,
    'addx' : 2
}

def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


Instruction = namedtuple("Instruction", ["command","value"])

if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__10.txt"))
    # input = get_input(None)
    raw_rows = input.split("\n")
    commands = []
    for line in raw_rows:
        try:
            commands.append( Instruction(
                line.split(' ')[0],
                int(line.split(' ')[1])
        ))
        except IndexError:
            try:
                commands.append( Instruction(
                line.split(' ')[0], 0
                ))
            except:
                print(line, line.split(' '))
                raise
    current_x = 1
    current_step = 0
    steps = dict()
    pixels = []
    for cmd in commands:
        turns = TURNS[cmd.command]
        for i in range(turns):
            current_step += 1
            # -- part 2 --
            tracker = (current_step - 1 ) % 40
            if (tracker - 1) <= current_x  <= (tracker + 1):
                pix = '#'
            else:
                pix = '.'
            pixels.append(pix)
            # -- end part 2 --
            if i == turns - 1:
                current_x += cmd.value
            steps[current_step] = current_x
        
    ct1 = 0
    for item in range(20,221,40):
        ct1 += item * steps[item-1]
    print('part1\t',ct1)
    print('part2')
    for i in range(0,6):
        print(''.join(pixels[i*40:i*40+40]))