import os

SAMPLE_DATA = """mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def distinct_chars(s, n):
    for i in range(len(s)):
        _ = list(round[i : i + n])
        if len(_) == len(set(_)):
            return i + n


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__6.txt"))
    # input = get_input(None)
    rounds = input.split("\n")
    for round in rounds:
        print("part1\t", distinct_chars(round, 4))
        print("part2\t", distinct_chars(round, 14))
