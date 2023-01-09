import os
import re
import operator
import sympy

SAMPLE_DATA = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

PATTERN_NUMBER = re.compile(r"(\d+)")
PATTERN_OPERATION = re.compile(r"(\w+):\s(\w+)\s(.)\s(\w+)")

MAP_OPERATOR = {
    "+": operator.add,
    "*": operator.mul,
    "-": operator.sub,
    "/": operator.truediv,
    "=": operator.eq,
}


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def parse_input(string):
    monkeys = {}
    for line in string.split("\n"):
        monkeys[line[0:4]] = Monkey(line)
    return monkeys


class Monkey:
    def __init__(self, initial_string):
        self.value = None
        self.parents = []
        self.type = None
        self.get_attributes(initial_string)

    def get_attributes(self, initial_string):
        self.name = initial_string[0:4]

        if PATTERN_NUMBER.search(initial_string):
            self.value = int(PATTERN_NUMBER.findall(initial_string)[0])
            self.type = "number"
        else:
            _ = PATTERN_OPERATION.findall(initial_string)
            self.parents = [_[0][1], _[0][3]]
            self.type = _[0][2]

    def solve_monkey(self):
        if self.type == "number":
            return self.value
        else:
            parent_0 = monkeys[self.parents[0]]
            parent_1 = monkeys[self.parents[1]]
            return MAP_OPERATOR[self.type](
                parent_0.solve_monkey(), parent_1.solve_monkey()
            )

    def solve_monkey_symbol(self):
        if self.type == "number":
            return str(self.value)
        else:
            parent_0 = monkeys[self.parents[0]]
            parent_1 = monkeys[self.parents[1]]

            return (
                "("
                + parent_0.solve_monkey_symbol()
                + self.type
                + parent_1.solve_monkey_symbol()
                + ")"
            )


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__21.txt"))
    # input = get_input(None)
    monkeys = parse_input(input)
    # part_1
    print("part_1:\t", int(monkeys["root"].solve_monkey()))
    # part_2
    # set adjustments
    monkeys["root"].type = "="
    monkeys["humn"].value = "x"
    # get equation
    solver = monkeys["root"].solve_monkey_symbol()
    # print(solver)
    # convert from an eq comparison to a '-' sub operand
    #  a = b --> a - b = 0
    solver_string = " - ".join(solver.split("="))

    x = sympy.Symbol("x")
    # simplify
    solver_eq = eval(solver_string)
    # print(solver_eq)
    print("part_2:\t", int(sympy.solvers.solve(solver_eq)[0]))
