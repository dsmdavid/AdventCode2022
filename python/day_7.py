import os
from collections import defaultdict
import pprint
from copy import deepcopy

SAMPLE_DATA = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

SUMS = []


def get_input(fn):
    if not fn:
        return SAMPLE_DATA.strip()
    with open(fn, "r") as f:
        return f.read().strip()


def create_tree(input):
    """creates the full hierarchy as nested dictionaries
    '/a/e'
    {'/':{'files':{fn:size},'a':{'files':{fn:size},e:{'files':size}}}}

    """
    current_path = ""
    rounds = input.split("\n")
    tree = defaultdict(dict)
    for round in rounds:
        # print(round)
        if round[0:4] == "$ cd":  # update current path
            change_to = round[4:].strip()
            current_path = os.path.normpath(os.path.join(current_path, change_to))
        elif round[0:4] == "dir ":  # create child directory
            dir_to_add = "/" + round[4:]
            curr_dict = get_current_dict(current_path, tree)
            curr_dict[round[4:]] = {"files": {}}
        elif round[0] != "$":  # store files
            size, filename = round.split(" ")
            curr_dict = get_current_dict(current_path, tree)
            curr_dict["files"][filename] = int(size)
    return tree


def get_current_dict(path_string, tree):
    """given a path string returns the relevant
    dictionary in the tree. e.g.
    path string like '/a/e
    tree = {'/':{'/a':{'/e':{'this':{}}}}}
    dictionary returned : {'this':{}}
    """
    curr_dict = tree
    for item in path_string.split("/"):
        if item:
            # print('curr_dict:\t',curr_dict, 'item:\t',item)
            curr_dict = curr_dict.get(item, {})
    return curr_dict


def get_sums_dictionary(dictionary):
    """for a given dictionary, retrieves the
    sum of the files sizes plus the children directories
    and appends those to the SUMS"""
    size = 0
    for k, v in dictionary.get("files", {}).items():
        if k:
            size += v
    # are there any other keys in the dictionary?
    l_keys = list(dictionary.keys())

    if l_keys:
        for k in dictionary.keys():
            # is it a directory?
            if k != "files":
                size += get_sums_dictionary(dictionary[k])

        if "files" in list(dictionary.keys()):
            # are we at the most inner level (only key is 'files')
            if not list(dictionary.keys()).remove("files"):
                SUMS.append(size)

    return size


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__7.txt"))
    # input = get_input(None)
    rounds = input.split("\n")
    full_tree = create_tree(input)
    get_sums_dictionary(full_tree)
    filtered = list(filter(lambda x: x <= 100000, SUMS))
    part_1 = sum(filtered)

    sums_part_2 = SUMS[:]
    tree_part_2 = deepcopy(full_tree)
    space_in_use = get_sums_dictionary(tree_part_2)
    total_file_size = 70000000
    space_needed = 30000000
    free_space = total_file_size - space_in_use
    diff_needed = space_needed - free_space

    print(
        space_in_use,
        part_1,
        space_in_use - part_1,
        total_file_size - space_in_use,
        diff_needed,
    )

    needed = list(filter(lambda x: x >= diff_needed, SUMS))
    part_2 = min(needed)
    print("part1\t", part_1)
    print("part2\t", part_2)
