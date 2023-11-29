import os
import re
import operator
from collections import deque, defaultdict, Counter
from math import ceil, floor, log

TRANSLATION_CODE = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2, 4: "-", 3: "="}

SAMPLE_DATA = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def parse_input(string):
    vals = []
    for line in string.split("\n"):
        vals.append(snafu(line))
    return vals


def snafu(string):
    temp = list(map(lambda x: TRANSLATION_CODE[x], list(string)))
    ct = 0
    val = 0
    while temp:
        val += pow(5, ct) * temp.pop()
        ct += 1
    return val


def reverse_snafu(number):
    number_string = ""

    while number:
        left, mods = divmod(number, 5)
        if mods > 2:
            left += 1

            next_str = TRANSLATION_CODE.get(mods, None)
            if not next_str:
                next_str = str(mods)
        else:
            next_str = str(mods)

        number_string += next_str
        number = left

    return number_string[::-1]


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__25.txt"))
    # input = get_input(None)
    fuels = parse_input(input)
    # print( snafu('10'), snafu('1=11-2'), snafu('1-0---0'), snafu('1121-1110-1=0'))
    print(sum(fuels))
    print("part_1\t", reverse_snafu(sum(fuels)))
    # print(reverse_snafu(2022))
