#Advent of Code Day 18 Part 2
#Solved Dec. 18, 2024

#Solves the problem by doing a binary search through the corrupted bytes to find the first one that doesn't have a path
#My other idea was to keep track of my current best path, and update when a new byte landed on that path
#But the binary search was easier to implement

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
    lower_bound = 1024
    width = 71
    height = 71
    exit_coor = (70, 70)
else:
    f = open("sample.txt")
    lower_bound = 12
    width = 7
    height = 7
    exit_coor = (6, 6)

corrupted_ever = []

for i in f:
    coor = tuple(map(int, i.split(",")))
    corrupted_ever.append(coor)

upper_bound = len(corrupted_ever) - 1

solved = False

while not solved:
    interval = upper_bound - lower_bound

    if interval == 1:
        #lower_bound works and upper_bound doesn't
        #if they're only one apart, then upper_bound must be the first one that blocks the path
        byte_coor = corrupted_ever[upper_bound]
        coor_string = str(byte_coor[0]) + "," + str(byte_coor[1])
        print(coor_string)
        solved = True
        break

    byte_to_test = lower_bound + int(interval / 2)

    corrupted = set(corrupted_ever[:byte_to_test+1])

    to_visit = Queue()
    to_visit.put((start_coor, 0))

    visited = {}
    
    path_found = False

    while not to_visit.empty():
        node = to_visit.get()
        current_coor = node[0]
        current_steps = node[1]
        if current_coor in visited:
            continue

        if current_coor == exit_coor:
            #path found - this still works
            lower_bound = byte_to_test
            path_found = True
            break

        neighbors = get_neighbors(current_coor, width, height)

        for i in neighbors:
            if i not in corrupted:
                to_visit.put((i, current_steps + 1))

        visited[current_coor] = current_steps

    if not path_found:
        #to_visit emptied without finding exit - path is blocked
        upper_bound = byte_to_test
