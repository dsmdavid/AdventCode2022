import os
import json
import numpy as np

from collections import deque, Counter
from copy import deepcopy
import re
import sys

SAMPLE_DATA = """1
2
-3
3
-2
0
4"""


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def parse_input(string):
    order = tuple(map(Number, string.split("\n")))
    return order


class Number:
    __slots__ = "value"

    def __init__(self, value):
        self.value = int(value)


def mix(order, times=1):
    numbers, sz = list(order), len(order)

    for _ in range(times):
        print(_)

        for num in order:
            i = numbers.index(num)
            numbers.pop(i)
            numbers.insert((i + num.value) % (sz - 1), num)
        for i, num in enumerate(numbers):
            if num.value == 0:
                break
        print(
            list(numbers[(i + delta) % sz].value for delta in (1000, 2000, 3000)),
            sum(numbers[(i + delta) % sz].value for delta in (1000, 2000, 3000)),
        )
    for i, num in enumerate(numbers):
        if num.value == 0:
            break

    return sum(numbers[(i + delta) % sz].value for delta in (1000, 2000, 3000))


if __name__ == "__main__":
    # input = get_input(os.path.join("./inputs", "2022__20.txt"))
    input = get_input(None)
    # linked_list, array = parse_input(input, multiplier=811589153)
    order = parse_input(input)

    answer = mix(order)
    # advent.print_answer(1, answer)
    print(answer)

    for num in order:
        num.value *= 811589153

    answer = mix(order, 10)
    # advent.print_answer(2, answer)
    print(answer)
