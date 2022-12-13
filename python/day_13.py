import os
import json
from itertools import zip_longest


SAMPLE_DATA = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def compare_two(one, two):
    """returns integer 1 if packets are in order, -1 if not in order, 0 if unknown"""
    # one and two are numbers:
    if isinstance(one, int) and isinstance(two, int):
        if one < two:
            return 1
        elif two < one:
            return -1
        else:
            return 0
    #  one of each
    elif not isinstance(one, int) and isinstance(two, int):
        return compare_two(one, [two])
    elif isinstance(one, int) and not isinstance(two, int):
        return compare_two([one], two)
    else:
        # both are lists
        for a, b in zip_longest(one, two):
            if a is None and b is not None:
                return 1
            elif a is not None and b is None:
                return -1
            result = compare_two(a, b)
            if result != 0:
                return result
        return 0


class Packet:
    # I define compare_two as 1, 0, -1 so the lt, gt are mixed up!
    def __init__(self, obj, *args):
        self.obj = obj

    def __lt__(self, other):
        return compare_two(self.obj, other.obj) > 0

    def __gt__(self, other):
        return compare_two(self.obj, other.obj) < 0

    def __eq__(self, other):
        return compare_two(self.obj, other.obj) == 0


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__13.txt"))
    # input = get_input(None)
    pairs = {}
    for i, block in enumerate(input.split("\n\n")):
        pairs[i] = []
        for k, pair in enumerate(block.split("\n")):
            pairs[i].append(json.loads(pair))

    ct = 0
    for k, v in pairs.items():
        if compare_two(v[0], v[1]) == 1:
            ct += k + 1
    print("part1\t", ct)
    ### Part 2 ###
    # additional inputs (Divider packets)
    DIVIDER_PACKET_1 = Packet([[2]])
    DIVIDER_PACKET_2 = Packet([[6]])
    l_pairs = []
    for v in pairs.values():
        l_pairs.extend(v)
    packets_list = [Packet(i) for i in l_pairs]
    packets_list.extend([DIVIDER_PACKET_1, DIVIDER_PACKET_2])

    packets_list.sort()
    t1 = packets_list.index(DIVIDER_PACKET_1) + 1
    t2 = packets_list.index(DIVIDER_PACKET_2) + 1
    print(t1, t2, t1 * t2)
