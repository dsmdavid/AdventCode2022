import os


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


def parse_input(string, multiplier=1):
    # values may be repeated, so using a dictionary with
    # the original order as keys

    vals = {}
    for i, k in enumerate(string.split("\n")):
        vals[i] = {"value": int(k)}
    array = list(range(len(vals.keys())))
    max_val = len(array) - 1
    for item in array:
        vals[item]["previous"] = item - 1 if item - 1 >= 0 else len(array) - 1
        vals[item]["next"] = item + 1 if item + 1 < len(array) else 0
        vals[item]["original_value"] = vals[item]["value"] * multiplier
        if vals[item]["value"] >= 0:
            vals[item]["value"] = vals[item]["original_value"] % max_val
        else:
            vals[item]["value"] = vals[item]["original_value"] % -(max_val)

    return vals, array


def linked_list_process(array, position_0, rounds=1):
    # create the initial linked list
    #   (next item position, previous item position, current item position, current item value)
    # updates:
    # - make a copy of the original array
    # - go through all the nodes in the original array in order
    # - for each node: move it to the desired position
    # - update the previous prior node and after node to point to the relevant nodes
    # - update the new prior node and after node to point to the relevant nodes
    original = array[:]
    for round in range(rounds):
        for item in original:
            rotation_value = linked_list[item]["value"]
            if rotation_value == 0:
                continue
            else:

                # update current prev / next
                current_prev = linked_list[item]["previous"]
                current_next = linked_list[item]["next"]
                linked_list[current_prev]["next"] = current_next
                linked_list[current_next]["previous"] = current_prev

                # find new position
                ct = 0
                cursor = item
                if rotation_value < 0:
                    direction = "previous"
                else:
                    direction = "next"
                while ct < abs(rotation_value) + 1:
                    cursor = linked_list[cursor][direction]
                    ct += 1

                # update new prev / next
                new_prev = linked_list[cursor]["previous"]
                new_next = cursor
                if direction == "previous":
                    # print('change course!')
                    new_prev = cursor
                    new_next = linked_list[cursor]["next"]
                linked_list[new_prev]["next"] = item
                linked_list[new_next]["previous"] = item
                linked_list[item]["previous"] = new_prev
                linked_list[item]["next"] = new_next

    return True


def find_item(index, position_0):
    ct = 0
    node = position_0

    while ct < index:
        node = linked_list[node]["next"]
        ct += 1
    return linked_list[node]["original_value"]


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__20.txt"))
    # input = get_input(None)
    linked_list, array = parse_input(input, multiplier=1)
    position_0 = [k for k, v in linked_list.items() if v["value"] == 0][0]

    linked_list_process(array, position_0, rounds=1)

    a = find_item(1000, position_0)
    b = find_item(2000, position_0)
    c = find_item(3000, position_0)
    print(a, b, c, "answer part1:\t", a + b + c)
    # 2215 p1

    linked_list, array = parse_input(input, multiplier=811589153)
    new_array = linked_list_process(array, position_0, rounds=10)

    a = find_item(1000, position_0)
    b = find_item(2000, position_0)
    c = find_item(3000, position_0)
    print(a, b, c, "answer part2:\t", a + b + c)
    # # 1623178306
