import os
import re
from collections import defaultdict
import sys
from copy import deepcopy

SAMPLE_DATA = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def get_input(fn):
    """remove strip, spaces matter!"""
    if not fn:
        return SAMPLE_DATA
    with open(fn, "r") as f:
        return f.read()


def split_cols_instructions(l):
    midpoint = l.index("")
    return l[: midpoint - 1], l[midpoint + 1 :]


def convert_to_columns(matrix_input):
    columns = defaultdict(list)

    for row in matrix_input[::-1]:
        length = range(0, len(row), 4)
        for i, pos in enumerate(length):
            try:
                val = row[pos : pos + 4].replace(" ", "")
            except:
                val = ""
            if val != "[_]" and val != "":
                columns[i + 1].append(val)
    return columns


def execute_instruction(columns, instruction_step, mode=9000):
    if instruction_step == "":
        return columns
    quantity, from_, to_ = map(int, re.findall("(\d+)", instruction_step))
    transit = columns[from_][len(columns[from_]) - quantity :][:]
    if len(transit) != quantity:
        sys.exit(1)
    columns[from_] = columns[from_][:-quantity]
    if mode == 9000:
        columns[to_].extend(transit[::-1])
    elif mode == 9001:
        columns[to_].extend(transit)

    return columns


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__5.txt"))
    # input = get_input(None)
    rounds = input.split("\n")
    matrix_input, instructions = split_cols_instructions(rounds)
    columns = convert_to_columns(matrix_input)
    columns_part2 = deepcopy(columns)
    for instruction_step in instructions:
        columns = execute_instruction(columns, instruction_step)
        columns_part2 = execute_instruction(columns_part2, instruction_step, mode=9001)

    answer = ""
    for k, v in columns.items():
        try:
            answer += v[-1]
        except:
            print(k, v)
    answer2 = ""
    for k, v in columns_part2.items():
        try:
            answer2 += v[-1]
        except:
            print(k, v)

    print("part1\t", answer.replace("[", "").replace("]", ""))
    print("part2\t", answer2.replace("[", "").replace("]", ""))
