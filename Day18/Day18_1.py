#Advent of Code Day 18 Part 1
#Solved Dec. 18, 2024

from queue import Queue

def get_neighbors(coor, width, height):
    x = coor[0]
    y = coor[1]
    neighbors = []
    if x-1 >= 0:
        neighbors.append((x-1, y))
    if x+1 < width:
        neighbors.append((x+1, y))
    if y-1 >= 0:
        neighbors.append((x, y-1))
    if y+1 < height:
        neighbors.append((x, y+1))
    return neighbors

do_real_input = True

start_coor = (0, 0)

if do_real_input:
    f = open("input.txt")
    bytes_to_simulate = 1024
    width = 71
    height = 71
    exit_coor = (70, 70)
else:
    f = open("sample.txt")
    bytes_to_simulate = 12
    width = 7
    height = 7
    exit_coor = (6, 6)

corrupted = set()

lines = f.read().split("\n")
for i in range(bytes_to_simulate):
    line = lines[i]
    coor = tuple(map(int, line.split(",")))
    corrupted.add(coor)

to_visit = Queue()
to_visit.put((start_coor, 0))

visited = {}

while not to_visit.empty():
    node = to_visit.get()
    current_coor = node[0]
    current_steps = node[1]
    if current_coor in visited:
        continue

    if current_coor == exit_coor:
        print(current_steps)
        break

    neighbors = get_neighbors(current_coor, width, height)

    for i in neighbors:
        if i not in corrupted:
            to_visit.put((i, current_steps + 1))

    visited[current_coor] = current_steps

