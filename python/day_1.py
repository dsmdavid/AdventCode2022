import os

def get_input(fn):
    with open(fn,'r') as f:
        return f.read().strip()

input = get_input(os.path.join('./inputs','2022__1.txt'))

elves_list = [list(map(int,elve.split('\n'))) for elve in input.split('\n\n')]
# elves ={i:val for i,val in enumerate(elves_list)}
elves_sum = {i:sum(val) for i,val in enumerate(elves_list)}
# print(elves)
print('answer 1')
print(max(elves_sum.values()))
# selected =  sum(sorted(elves_sum.values())[-3:])
# print(selected)
print('answer 2')
print(sum(sorted(elves_sum.values())[-3:]))
