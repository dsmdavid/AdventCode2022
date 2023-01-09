import os
from collections import defaultdict, namedtuple, deque, OrderedDict
import pprint
from copy import deepcopy
import sys
import operator
from functools import reduce
import math

SAMPLE_DATA = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

MAP_OPERATOR = {"+": operator.add, "*": operator.mul}

MONKEYS = OrderedDict()


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def lcm_(denominators):
    return reduce(lambda x, y: x * y // math.gcd(x, y), denominators)


class Monkey:
    def __init__(
        self,
        name,
        starting_items,
        operation,
        divisible_by,
        monkey_if_true,
        monkey_if_false,
        decrease="old,3",
    ):
        self.name = name
        self.list_of_items = deque(starting_items)
        self.worriness_increase_operator = MAP_OPERATOR[operation[0]]
        self.worriness_increase_value = (
            None if operation[1] == "old" else int(operation[1])
        )
        self.worriness_decrease = decrease
        self.test_divisible_by = divisible_by
        self.monkey_if_true = monkey_if_true
        self.monkey_if_false = monkey_if_false
        self.inspected = 0

    def process_all_items(self):
        while self.list_of_items:
            item = self.list_of_items.popleft()
            self.handle_one_item(item)

    def inspect_item(self, item):
        self.inspected += 1
        current_worriness = item
        modifier = (
            current_worriness
            if not self.worriness_increase_value
            else self.worriness_increase_value
        )
        # Monkey starts inspection
        new_worriness = self.worriness_increase_operator(current_worriness, modifier)
        test = new_worriness
        # Monkey gets bored
        if self.worriness_decrease == "old,3":
            new_worriness = new_worriness // 3
        elif not self.worriness_decrease:
            pass
        else:
            new_worriness = new_worriness % self.worriness_decrease
        return new_worriness

    def test_and_send_item(self, item):
        if item % self.test_divisible_by == 0:
            chosen = MONKEYS[self.monkey_if_true]
        else:
            chosen = MONKEYS[self.monkey_if_false]
        chosen.list_of_items.append(item)

    def handle_one_item(self, item):
        item = self.inspect_item(item)
        self.test_and_send_item(item)


def parse_block(block: str):
    #     block = '''Monkey 1:
    #   Starting items: 83, 78, 81, 55, 81, 59, 69
    #   Operation: new = old + 1
    #   Test: divisible by 3
    #     If true: throw to monkey 7
    #     If false: throw to monkey 4'''

    block_lines = block.split("\n")
    monkey = int(block_lines[0].split()[1].replace(":", ""))
    starting_items = list(
        map(int, block_lines[1].split(":")[1].replace(" ", "").split(","))
    )
    operation = block_lines[2].split(":")[1].split("=")[1].strip().split(" ")[1:]
    divisible_by = int(block_lines[3].replace("Test: divisible by", "").strip())
    monkey_if_true = int(block_lines[4].replace("If true: throw to monkey", "").strip())
    monkey_if_false = int(
        block_lines[5].replace("If false: throw to monkey", "").strip()
    )

    return (
        monkey,
        starting_items,
        operation,
        divisible_by,
        monkey_if_true,
        monkey_if_false,
    )


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__11.txt"))
    # input = get_input(None)
    blocks = input.split("\n\n")
    for block in blocks:
        init = parse_block(block)
        MONKEYS[init[0]] = Monkey(*init)

    for r in range(1, 21):
        for i, monkey in MONKEYS.items():
            monkey.process_all_items()
    inspected = [monkey.inspected for k, monkey in MONKEYS.items()]
    vals = sorted(inspected, reverse=True)
    print("part1\t", vals[0] * vals[1])
    MONKEYS = {}
    for block in blocks:
        init = parse_block(block)
        MONKEYS[init[0]] = Monkey(*init)
    decrease = lcm_([monkey.test_divisible_by for monkey in MONKEYS.values()])
    for i, monkey in MONKEYS.items():
        monkey.worriness_decrease = decrease
    for r in range(10000):
        for i, monkey in MONKEYS.items():
            monkey.process_all_items()
    inspected = [monkey.inspected for k, monkey in MONKEYS.items()]
    vals = sorted(inspected, reverse=True)
    print("part2\t", vals[0] * vals[1])
# 9699690
# 9699690
