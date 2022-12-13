from collections import deque
# from copy import deepcopy
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

def compare_two(one,two):
    '''returns integer 1 if packets are in order, -1 if not in order, 0 if unknown'''
    # print(one,two)
    # one and two are numbers:
    if isinstance(one, int) and isinstance(two, int):
        if one < two:
            return 1
        elif two < one:
            return -1
        else:
            return 0

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
            result = compare_two(a,b)
            if result != 0:
                return result
        return 0
# Use a merge_sort strategy
def merge(left, right):
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left

    result = []
    index_left = index_right = 0

    while len(result) < len(left) + len(right):
        if compare_two(left[index_left], right[index_right]) == 1:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1
        if index_right == len(right):
            result += left[index_left:]
            break

        if index_left == len(left):
            result += right[index_right:]
            break

    return result

def merge_sort(array):
    if len(array) < 2:
        return array

    middle = len(array) // 2

    return merge(
                left=merge_sort(array[:middle]),
                right=merge_sort(array[middle:]))


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__13.txt"))
    # input = get_input(None)
    pairs = {}
    for i, block in enumerate(input.split('\n\n')):
        pairs[i] = []
        for k, pair in enumerate(block.split('\n')):
            pairs[i].append(json.loads(pair))

    ct = 0
    for k,v in pairs.items():
        if compare_two(v[0],v[1]) == 1:
            ct += k+1
    print('part1\t', ct)
    ### Part 2 ###
    DIVIDER_PACKET_1 = [[2]]
    DIVIDER_PACKET_2 = [[6]]   
    l_pairs = []
    for v in pairs.values():
        l_pairs.extend(v)
    l_pairs.extend([DIVIDER_PACKET_1, DIVIDER_PACKET_2])
    print(len(l_pairs))
    m = merge_sort(l_pairs)
    # for i, v in enumerate(m):
        # print(i+1, '\t', v)
    c1 = m.index(DIVIDER_PACKET_1) + 1
    c2 = m.index(DIVIDER_PACKET_2) + 1
    print(c1, c2, 'part2\t', c1*c2)
  