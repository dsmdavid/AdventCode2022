import os

SAMPLE_DATA = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def get_containers(s):
    midpoint = int(len(s) / 2)
    return s[0:midpoint], s[midpoint:]


def get_common(s1, s2):
    common = [c for c in s1 if c in s2]
    return common


def get_priority(char):
    """
    a-z =  1-26
    A-Z = 27-52
    """
    val = ord(char)
    if val > 96:
        val = val - 96
    else:
        val = val - 64 + 26
    return val


def get_badge(sublist):
    """
    take a group of 3 rows
    return the common string to all of them
    """
    badge = get_common(get_common(sublist[0], sublist[1]), sublist[2])
    return badge


def play_round1():
    priorities = []
    for round in rounds:
        c1, c2 = get_containers(round)
        common = get_common(c1, c2)[0]
        priority = get_priority(common)
        priorities.append(priority)
    return sum(priorities)


def play_round2():
    priorities = []
    for i in range(0, len(rounds), 3):
        badge = get_badge(rounds[i : i + 3])[0]
        priority = get_priority(badge)
        priorities.append(priority)
    return sum(priorities)


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__3.txt"))
    # input = get_input(None)
    rounds = input.split("\n")
    print("part1\t", play_round1())
    print("part2\t", play_round2())
