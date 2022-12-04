import os

SAMPLE_DATA = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def is_contained(a, b):
    """returns true if a is wholly contained in b"""
    if a[0] >= b[0] and a[1] <= b[1]:
        return True
    else:
        return False


def has_overlap(a, b):
    """returns true if there's any overlap between a,b"""
    # sort by min boundary
    temp = [a, b]
    temp.sort(key=lambda x: x[0])
    a, b = temp
    if a[0] <= b[0]:
        if a[1] >= b[0]:
            return True
        else:
            return False
    else:
        if a[1] <= b[1]:
            return True
        else:
            return False


def parse_elf(s):
    a, b = map(int, s.split("-"))
    min_s = min(a, b)
    max_s = max(a, b)
    return min_s, max_s


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__4.txt"))
    # input = get_input(None)
    rounds = input.split("\n")
    ct = 0
    ov = 0
    for round in rounds:
        elf1, elf2 = map(parse_elf, round.split(","))
        if is_contained(elf1, elf2) or is_contained(elf2, elf1):
            ct += 1
        if has_overlap(elf1, elf2):
            ov += 1
    print("part1\t", ct)
    print("part2\t", ov)
